#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la referencia de raíces pāḷi.

    python3 herramientas/generar_raices.py

Junta dos cosas:

  recursos/raices/raices.json      1.698 raíces y 776 significados, extraídos
                                   de «Pali Roots in Saddanīti» por
                                   herramientas/extraer_raices.py
  recursos/raices/plantilla.html   el maquetado y la lógica

y escribe site/recursos/raices/index.html.

Antes de escribir comprueba la integridad de los datos: que toda raíz tenga
lema y referencia, que las referencias sean de un gaṇa existente —ocho en
pāḷi, diez en sánscrito—, que no haya quedado ningún carácter sin descifrar
y que la inicial de cada entrada esté en el alfabeto pāḷi. Si algo no cuadra,
no publica.
"""

import collections
import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(RAIZ, "recursos", "raices", "raices.json")
DHATUPATHA = os.path.join(RAIZ, "recursos", "raices", "dhatupatha.json")
DP_INGLES = os.path.join(RAIZ, "recursos", "raices", "dhatupatha-ingles.json")
DHATUMANJUSA = os.path.join(RAIZ, "recursos", "raices", "dhatumanjusa.json")
PLANTILLA = os.path.join(RAIZ, "recursos", "raices", "plantilla.html")
DESTINO = os.path.join(RAIZ, "site", "recursos", "raices", "index.html")

ALFABETO = {"a", "ā", "i", "ī", "u", "ū", "e", "o", "k", "kh", "g", "gh",
            "ṅ", "c", "ch", "j", "jh", "ñ", "ṭ", "ṭh", "ḍ", "ḍh", "ṇ", "t",
            "th", "d", "dh", "n", "p", "ph", "b", "bh", "m", "y", "r", "l",
            "ḷ", "v", "s", "h"}


def verificar(datos):
    """Devuelve la lista de fallos; vacía si todo cuadra."""
    fallos = []
    raices = datos["raices"]
    sigs = datos["significados"]

    if not raices:
        fallos.append("no hay ninguna raíz")
    if not sigs:
        fallos.append("no hay ningún significado")

    crudo = json.dumps(datos, ensure_ascii=False)
    sin_leer = crudo.count("�")
    if sin_leer:
        fallos.append("{0} caracteres sin descifrar (�)".format(sin_leer))

    vistos = set()
    for r in raices:
        n = r.get("id")
        if n in vistos:
            fallos.append("id repetido: {0}".format(n))
        vistos.add(n)
        if not r.get("raices"):
            fallos.append("entrada {0} sin lema".format(n))
        if not r.get("refs"):
            fallos.append("entrada {0} sin referencia del Saddanīti".format(n))
        for x in r.get("refs", []):
            if not 1 <= x["gana"] <= 8:
                fallos.append("entrada {0}: gaṇa pāḷi {1} fuera de 1-8".format(
                    n, x["gana"]))
        for x in r.get("sanscrito_refs", []):
            if not 1 <= x["gana"] <= 10:
                fallos.append("entrada {0}: gaṇa sánscrito {1} fuera de "
                              "1-10".format(n, x["gana"]))
        if r.get("letra") not in ALFABETO:
            fallos.append("entrada {0}: inicial «{1}» fuera del alfabeto "
                          "pāḷi".format(n, r.get("letra")))
        for lema in r.get("raices", []):
            if unicodedata.normalize("NFC", lema) != lema:
                fallos.append("entrada {0}: «{1}» no está en NFC".format(n, lema))
            if re.search(r"\d", lema):
                fallos.append("entrada {0}: «{1}» conserva una llamada de "
                              "nota".format(n, lema))
        if r.get("sanscrito") and not r.get("sanscrito_glosa"):
            fallos.append("entrada {0}: raíz sánscrita sin glosa".format(n))

    for i, s in enumerate(sigs):
        if not s.get("raices"):
            fallos.append("significado {0} sin raíces".format(i))
        if not (s.get("es") or s.get("en") or s.get("glosa")):
            fallos.append("significado {0} vacío".format(i))
    return fallos


def _n(s):
    return unicodedata.normalize("NFC", (s or "").strip().lower().strip(" .,;"))


# Una glosa puede empezar con consonante doble por sandhi —«cchedane» por
# «chedane»—. Deshacerlo es el único retoque que se permite al cotejar.
_DOBLE = re.compile(r"^(kkh|ggh|cch|jjh|ṭṭh|ḍḍh|tth|ddh|pph|bbh|kk|gg|cc|jj|"
                    r"ṭṭ|ḍḍ|tt|dd|pp|bb|mm|nn|ll|ss|yy|vv)")
_SIMPLE = {"kkh": "kh", "ggh": "gh", "cch": "ch", "jjh": "jh", "ṭṭh": "ṭh",
           "ḍḍh": "ḍh", "tth": "th", "ddh": "dh", "pph": "ph", "bbh": "bh",
           "kk": "k", "gg": "g", "cc": "c", "jj": "j", "ṭṭ": "ṭ", "ḍḍ": "ḍ",
           "tt": "t", "dd": "d", "pp": "p", "bb": "b", "mm": "m", "nn": "n",
           "ll": "l", "ss": "s", "yy": "y", "vv": "v"}


def _simple(s):
    s = _n(s)
    m = _DOBLE.match(s)
    return _SIMPLE[m.group(1)] + s[m.end():] if m else s


def traducir_dp(datos, dp, ingles):
    """Pone significado en español y en inglés a las entradas del Dhātupāṭha.

    Andersen y Smith no traducen: la entrada trae sólo la glosa pāḷi. El
    inglés viene de la hoja de cálculo de la digitalización; el español, de
    Nandisena, cuando su tabla usa exactamente la misma glosa pāḷi para
    alguna raíz. No se traduce nada aquí: se reutiliza lo ya traducido, y
    cada entrada dice de dónde le viene.
    """
    voc = {}
    for r in datos["raices"]:
        if r["glosa"] and (r["es"] or r["en"]):
            voc.setdefault(_n(r["glosa"]), (r["es"], r["en"]))
    for x in datos["significados"]:
        if x["glosa"] and (x["es"] or x["en"]):
            voc.setdefault(_n(x["glosa"]), (x["es"], x["en"]))
    voc_s = {}
    for k, v in voc.items():
        voc_s.setdefault(_simple(k), v)

    en_map = (ingles or {}).get("en", {})
    con_en = con_es = 0
    for x in dp["entradas"]:
        clave = "{0}{1}".format(x["n"], x["sufijo"])
        x["en"] = en_map.get(clave, "")
        if x["en"]:
            con_en += 1
        par = voc.get(_n(x["glosa"])) or voc_s.get(_simple(x["glosa"]))
        x["es"] = par[0] if par else ""
        x["es_de_nandisena"] = bool(par)
        if par:
            con_es += 1
    return con_en, con_es


def concordar_dm(datos, dm):
    """Enlaza cada raíz con las estrofas de la Dhātumañjūsā que la nombran.

    El enlace es una coincidencia literal de palabra en el verso, y nada
    más. No se deshace el metro ni se deducen pares de raíz y significado:
    en el verso van encajados, y separarlos sería interpretar. Los lemas de
    una o dos letras quedan fuera, porque a esa longitud la coincidencia deja
    de decir nada.
    """
    idx = collections.defaultdict(set)
    for e in dm["estrofas"]:
        for v in e["versos"]:
            for w in re.sub(r"[’'‘\-–—.,;!?()⟨⟩]", " ", v).split():
                idx[unicodedata.normalize("NFC", w.lower())].add(e["n"])
    con = 0
    for r in datos["raices"]:
        hits = set()
        for lema in r["raices"]:
            lema = unicodedata.normalize("NFC", lema.lower())
            if len(lema) >= 3:
                hits |= idx.get(lema, set())
        r["dm"] = sorted(hits)
        if hits:
            con += 1
    return con


def concordar(datos, dp):
    """Cruza las raíces de Nandisena con las del Dhātupāṭha, por lema.

    El cruce es por lema y nada más: una misma raíz puede figurar en las dos
    obras con significados distintos, y no toca decidir aquí cuál es cuál.
    Cuando además coincide el significado, se marca «glosa: true», que es la
    correspondencia que se puede dar por segura.
    """
    por_lema = collections.defaultdict(list)
    for x in dp["entradas"]:
        por_lema[unicodedata.normalize("NFC", x["raiz"].lower())].append(x)

    con, seguras = 0, 0
    for r in datos["raices"]:
        vistos, hits = set(), []
        for lema in r["raices"]:
            for x in por_lema.get(unicodedata.normalize("NFC", lema.lower()), []):
                clave = (x["n"], x["sufijo"])
                if clave in vistos:
                    continue
                vistos.add(clave)
                hits.append({
                    "n": x["n"], "sufijo": x["sufijo"], "raiz": x["raiz"],
                    "glosa": x["glosa"], "gana": x["gana"], "signo": x["signo"],
                    "notas": x["notas"],
                    "misma_glosa": (unicodedata.normalize("NFC", x["glosa"].lower())
                                    == unicodedata.normalize("NFC", r["glosa"].lower())),
                })
        hits.sort(key=lambda h: (h["n"], h["sufijo"]))
        r["dp"] = hits
        if hits:
            con += 1
            if any(h["misma_glosa"] for h in hits):
                seguras += 1

    huerfanas = sorted(
        set(por_lema) - {unicodedata.normalize("NFC", l.lower())
                         for r in datos["raices"] for l in r["raices"]})
    return con, seguras, huerfanas


def main():
    if not os.path.exists(DATOS):
        print("Falta {0}. Se obtiene con:".format(os.path.relpath(DATOS, RAIZ)))
        print("    python3 herramientas/extraer_raices.py ruta/al/dhatu.pdf")
        return 1

    datos = json.load(open(DATOS, encoding="utf-8"))

    fallos = verificar(datos)
    if fallos:
        print("raices.json NO cuadra; no se publica:")
        for f in fallos[:20]:
            print("  ✗", f)
        if len(fallos) > 20:
            print("  … y {0} más".format(len(fallos) - 20))
        return 1

    # El Dhātupāṭha es opcional: si no está extraído, la página se publica
    # igual, sólo que sin la concordancia y sin su pestaña.
    con = seguras = 0
    huerfanas = []
    con_en = con_es = con_dm = 0
    if os.path.exists(DHATUPATHA):
        dp = json.load(open(DHATUPATHA, encoding="utf-8"))
        ingles = (json.load(open(DP_INGLES, encoding="utf-8"))
                  if os.path.exists(DP_INGLES) else None)
        con_en, con_es = traducir_dp(datos, dp, ingles)
        con, seguras, huerfanas = concordar(datos, dp)
        datos["dhatupatha"] = dp
    else:
        print("  aviso — sin recursos/raices/dhatupatha.json: se publica sin "
              "la concordancia del Dhātupāṭha")
        for r in datos["raices"]:
            r["dp"] = []

    if os.path.exists(DHATUMANJUSA):
        dm = json.load(open(DHATUMANJUSA, encoding="utf-8"))
        con_dm = concordar_dm(datos, dm)
        datos["dhatumanjusa"] = dm
    else:
        for r in datos["raices"]:
            r["dm"] = []

    plantilla = open(PLANTILLA, encoding="utf-8").read()
    marca = re.search(r'/\*__DATOS__\*/.*?/\*__FIN__\*/', plantilla, re.S)
    if not marca:
        print("La plantilla no tiene el marcador /*__DATOS__*/…/*__FIN__*/")
        return 1
    html = (plantilla[:marca.start()]
            + json.dumps(datos, ensure_ascii=False, separators=(",", ":"))
            + plantilla[marca.end():])

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    open(DESTINO, "w", encoding="utf-8").write(html)

    raices = datos["raices"]
    con_skt = sum(1 for r in raices if r["sanscrito"])
    notas = sum(len(r["notas"]) for r in raices)
    enlaces = sum(len(s["raices"]) for s in datos["significados"])
    print("{0} raíces · {1} con cognado sánscrito · {2} notas · "
          "{3} significados con {4} remisiones → {5} ({6} KB)".format(
              len(raices), con_skt, notas, len(datos["significados"]), enlaces,
              os.path.relpath(DESTINO, RAIZ), len(html) // 1024))

    sin_skt = len(raices) - con_skt
    if sin_skt:
        print("  sin cognado sánscrito en el original: {0}".format(sin_skt))
    if "dhatupatha" in datos:
        n_dp = len(datos["dhatupatha"]["entradas"])
        print("  concordancia con el Dhātupāṭha: {0} raíces, {1} de ellas con "
              "el mismo significado; {2} lemas del Dhātupāṭha no están en "
              "el Saddanīti".format(con, seguras, len(huerfanas)))
        print("  significado de las entradas del Dhātupāṭha: {0}/{1} en inglés "
              "(hoja de la digitalización), {2}/{1} en español (glosa pāḷi "
              "idéntica en el Saddanīti)".format(con_en, n_dp, con_es))
    if "dhatumanjusa" in datos:
        print("  Dhātumañjūsā: {0} estrofas; {1} raíces nombradas literalmente "
              "en alguna".format(len(datos["dhatumanjusa"]["estrofas"]), con_dm))
    return 0


if __name__ == "__main__":
    sys.exit(main())
