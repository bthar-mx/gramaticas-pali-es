#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la clasificación de los suttas de Kaccāyana.

    python3 herramientas/generar_clasificacion.py

Junta tres cosas:

  recursos/clasificacion/datos.json      el tipo de cada sutta (saññā,
                                         adhikāra, paribhāsā, vidhi), la
                                         vidhi, la operación, el fundamento
                                         en Rūpasiddhi y Nyāsa y las notas
                                         de interpretación, en español e
                                         inglés
  kaccayana/0N-*.md y 0N-*.en.md         el texto pāḷi de cada aforismo, su
                                         número en la Rūpasiddhi, la primera
                                         línea de la traducción y las
                                         secciones (kaṇḍa)
  recursos/clasificacion/plantilla.html  el maquetado y la lógica

y escribe site/recursos/clasificacion/index.html.

Antes de escribir verifica: que cada capítulo declarado tenga todos sus
aforismos, sin huecos ni sobrantes, tanto en los datos como en los dos
markdown; que cada tipo y cada vidhi estén en las listas declaradas; que
toda vidhi tenga tipo vidhi y al revés; que cada aforismo tenga operación
y fundamento en los dos idiomas; y que todo el texto esté en NFC. Si algo
no cuadra, no publica.
"""

import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(RAIZ, "recursos", "clasificacion")
DATOS = os.path.join(DIR, "datos.json")
PLANTILLA = os.path.join(DIR, "plantilla.html")
DESTINO = os.path.join(RAIZ, "site", "recursos", "clasificacion", "index.html")

# el número de la Rūpasiddhi puede ser doble: «**271\. 88, 308\. …**»
# el punto puede ir escapado («271\.», capítulos 1–3) o no («316.», capítulo 4)
CABECERA = re.compile(r"^\*\*(\d+)\\?\.\s+(\d+(?:,\s*\d+)*)\\?\.\s+(.+?)\*\*")
KANDA = re.compile(r"^\*\*([A-ZĀĪŪṄÑṬḌṆḶṂ]+-KAṆḌA)\*\*")
ORD = {"PAṬHAMA": 1, "DUTIYA": 2, "TATIYA": 3, "CATUTTHA": 4, "PAÑCAMA": 5,
       "CHAṬṬHA": 6, "SATTAMA": 7, "AṬṬHAMA": 8}


def limpiar(t):
    """De markdown a texto: sin notas, sin escapes, sin negritas ni glosas."""
    t = re.sub(r"\[\^\d+\]", "", t)
    t = re.sub(r"\{([^|{}]*)\|[^{}]*\}", r"\1", t)
    t = t.replace("**", "")
    t = re.sub(r"\\([\[\].+\-*_()!#])", r"\1", t)
    return re.sub(r"\s+", " ", t).strip()


def leer_md(ruta):
    """{n: {ru, sutta, tr}} y [(kaṇḍa, primer §)] de un capítulo."""
    lin = open(ruta, encoding="utf-8").read().split("\n")
    suttas, kandas, pend = {}, [], None
    i = 0
    while i < len(lin):
        # «**339. 358. Jāyāya tudaṃ-jāni[^19]** **patimhi (731).**»: negrita partida
        l = lin[i].strip().replace("** **", " ")
        m = KANDA.match(l)
        if m:
            pend = m.group(1)
        m = CABECERA.match(l)
        if m:
            n, txt = int(m.group(1)), m.group(3)
            ru = re.sub(r"\s+", " ", m.group(2))
            ru = None if ru == "0" else ru
            sadd = None
            ms = re.search(r"\s*\(([\d\-–, ]+)\)\.?$", txt)
            if ms:
                sadd = ms.group(1)
                txt = txt[:ms.start()]
            txt = limpiar(txt).rstrip(".")
            # la traducción: la primera línea no vacía tras el primer «---»
            j, tr = i + 1, ""
            while j < len(lin) and lin[j].strip() != "---" and not CABECERA.match(lin[j].strip()):
                j += 1
            if j < len(lin) and lin[j].strip() == "---":
                j += 1
                while j < len(lin) and not lin[j].strip():
                    j += 1
                if j < len(lin) and not CABECERA.match(lin[j].strip()):
                    tr = limpiar(lin[j])
            suttas[n] = {"ru": ru, "sutta": txt, "sadd": sadd, "tr": tr}
            if pend:
                kandas.append([pend, n])
                pend = None
        i += 1
    return suttas, kandas


def nfc(t):
    return not isinstance(t, str) or unicodedata.normalize("NFC", t) == t


def verificar(d, textos):
    fallos = []
    tipos, vidhis = set(d["tipos"]), set(d["vidhis"])
    claves = set(d["suttas"])
    esperadas = set()
    for c in d["capitulos"]:
        rango = set(range(c["desde"], c["hasta"] + 1))
        esperadas |= {str(n) for n in rango}
        for lengua in ("es", "en"):
            t = textos[c["clave"]][lengua][0]
            if set(t) != rango:
                falta = sorted(rango - set(t))[:8]
                sobra = sorted(set(t) - rango)[:8]
                fallos.append("{0} ({1}): faltan {2}, sobran {3}".format(c["md"], lengua, falta, sobra))
            for n in rango:
                if n in t and not t[n]["tr"]:
                    fallos.append("§{0} ({1}): sin primera línea de traducción".format(n, lengua))
    if claves != esperadas:
        fallos.append("datos.json: faltan {0}, sobran {1}".format(
            sorted(esperadas - claves, key=int)[:8], sorted(claves - esperadas, key=int)[:8]))
    for n, e in d["suttas"].items():
        if e["tipo"] not in tipos:
            fallos.append("§{0}: tipo desconocido «{1}»".format(n, e["tipo"]))
        partes = [v.strip() for v in e["vidhi"].split("+")] if e["vidhi"] else []
        for v in partes:
            if v not in vidhis:
                fallos.append("§{0}: vidhi desconocida «{1}»".format(n, v))
        if (e["tipo"] == "V") != bool(partes):
            fallos.append("§{0}: tipo y vidhi no casan".format(n))
        for campo in (e["op"], e["base"]["ru"], e["base"]["nyasa"], e.get("nota", {"es": "x", "en": "x"})):
            for lengua in ("es", "en"):
                if not campo.get(lengua, "").strip():
                    fallos.append("§{0}: falta texto ({1})".format(n, lengua))
                if not nfc(campo.get(lengua)):
                    fallos.append("§{0}: texto que no está en NFC".format(n))
    return fallos


def main():
    d = json.load(open(DATOS, encoding="utf-8"))
    textos = {}
    for c in d["capitulos"]:
        textos[c["clave"]] = {
            "es": leer_md(os.path.join(RAIZ, "kaccayana", c["md"] + ".md")),
            "en": leer_md(os.path.join(RAIZ, "kaccayana", c["md"] + ".en.md")),
        }
    fallos = verificar(d, textos)
    if fallos:
        print("La clasificación NO cuadra; no se publica:")
        for f in fallos[:25]:
            print("  ✗", f)
        return 1

    filas = []
    for c in d["capitulos"]:
        es, en = textos[c["clave"]]["es"][0], textos[c["clave"]]["en"][0]
        for n in range(c["desde"], c["hasta"] + 1):
            e = dict(d["suttas"][str(n)])
            e.update(n=n, cap=c["clave"], ru=es[n]["ru"], sutta=es[n]["sutta"],
                     sadd=es[n]["sadd"], tr={"es": es[n]["tr"], "en": en[n]["tr"]})
            filas.append(e)
    kandas = {c["clave"]: [[k, n, ORD.get(k.split("-")[0], 0)] for k, n in textos[c["clave"]]["es"][1]]
              for c in d["capitulos"]}
    salida = {k: d[k] for k in ("version", "fecha", "estado", "nota_version", "capitulos", "tipos", "vidhis")}
    salida.update(filas=filas, kandas=kandas)

    pl = open(PLANTILLA, encoding="utf-8").read()
    m = re.search(r'/\*__DATOS__\*/.*?/\*__FIN__\*/', pl, re.S)
    if not m:
        print("La plantilla no tiene el marcador /*__DATOS__*/…/*__FIN__*/")
        return 1
    datos = json.dumps(salida, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = pl[:m.start()] + datos + pl[m.end():]
    html = html.replace("__VERSION_DATE__", d["fecha"]).replace("__VERSION__", d["version"])
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    open(DESTINO, "w", encoding="utf-8").write(html)

    cuenta = {}
    for f in filas:
        cuenta[f["tipo"]] = cuenta.get(f["tipo"], 0) + 1
    notas = sum(1 for f in filas if "nota" in f)
    print("v{0} ({1}) · {2} aforismos · {3} · {4} con nota → {5}".format(
        d["version"], d.get("estado", ""), len(filas),
        " · ".join("{0} {1}".format(d["tipos"][t]["pali"], cuenta[t]) for t in d["tipos"] if t in cuenta),
        notas, os.path.relpath(DESTINO, RAIZ)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
