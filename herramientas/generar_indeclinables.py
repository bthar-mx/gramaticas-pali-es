#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la referencia de los indeclinables (abyaya), con las partículas.

    python3 herramientas/generar_indeclinables.py

Junta tres cosas:

  recursos/particulas/particulas.json      «Partículas (Nipāta)» de Bhikkhu
                                           Nandisena (2013): 310 entradas, con
                                           las erratas evidentes corregidas y
                                           su inglés (borrador)
  recursos/indeclinables/indeclinables.json «Indeclinables (Avyaya)» (2013):
                                           las clases 1 y 3-6, la definición,
                                           las notas y las erratas; y las
                                           partículas añadidas por IEBH
                                           («nuevo»: true), que aquí se
                                           intercalan en orden alfabético pāḷi
  recursos/indeclinables/plantilla.html    el maquetado y la lógica

y escribe site/recursos/indeclinables/index.html, con su guía para el
estudiante (recursos/indeclinables/guia.md y guia-plantilla.html; español e
inglés separados por una sola línea «---»).

La página antigua /recursos/particulas/ (y su guía) pasa a ser una remisión a
la pestaña de las partículas, que conserva el #ancla de cada entrada: ningún
enlace publicado se rompe. Las fuentes del texto están en docs/fuentes/nandisena/;
la revisión, en docs/privado/nipatas/.

Antes de escribir verifica los datos: identificadores únicos, toda entrada
con su cabecera en los dos idiomas, todo ejemplo con pāḷi, toda llamada [^n]
con su nota, casos dentro de la lista y todo el texto en NFC. Si algo no
cuadra, no publica.
"""

import json
import os
import re
import sys
import unicodedata
import cabecera  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(RAIZ, "recursos", "particulas", "particulas.json")
DATOS_I = os.path.join(RAIZ, "recursos", "indeclinables", "indeclinables.json")
PLANTILLA = os.path.join(RAIZ, "recursos", "indeclinables", "plantilla.html")
DESTINO = os.path.join(RAIZ, "site", "recursos", "indeclinables", "index.html")
GUIA = os.path.join(RAIZ, "recursos", "indeclinables", "guia.md")
GUIA_PLANTILLA = os.path.join(RAIZ, "recursos", "indeclinables", "guia-plantilla.html")
GUIA_DESTINO = os.path.join(RAIZ, "site", "recursos", "indeclinables", "guia", "index.html")
VIEJA = os.path.join(RAIZ, "site", "recursos", "particulas", "index.html")
VIEJA_GUIA = os.path.join(RAIZ, "site", "recursos", "particulas", "guia", "index.html")
ALF = ["a", "ā", "i", "ī", "u", "ū", "e", "o", "k", "kh", "g", "gh", "ṅ", "c", "ch",
       "j", "jh", "ñ", "ṭ", "ṭh", "ḍ", "ḍh", "ṇ", "t", "th", "d", "dh", "n", "p", "ph",
       "b", "bh", "m", "y", "r", "l", "v", "s", "h", "ḷ", "ṃ"]


def clave(w):
    """Orden alfabético pāḷi (las aspiradas son una letra)."""
    w = re.sub(r"<[^>]+>", "", w).lower()
    out, i = [], 0
    while i < len(w):
        if w[i:i + 2] in ALF:
            out.append(ALF.index(w[i:i + 2]))
            i += 2
        else:
            out.append(ALF.index(w[i]) if w[i] in ALF else 99)
            i += 1
    return out


def unir(p, ind):
    """Las 310 de Nandisena, en su orden, con las de IEBH intercaladas."""
    ent = list(p["entradas"])
    nip = next(c for c in ind["clases"] if c["id"] == "nipata")
    for x in sorted(nip["entradas"], key=lambda e: clave(e["lema"])):
        k = clave(x["lema"])
        pos = next((i for i, e in enumerate(ent) if clave(e["lema"]) > k), len(ent))
        ent.insert(pos, x)
    nip["entradas"] = ent
    ind["meta"]["erratas"] = p["meta"]["erratas"]
    return ind


REMISION = """<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="robots" content="noindex"><title>{titulo}</title>
<link rel="canonical" href="{destino}">
<script>(function(){{var q=new URLSearchParams(location.search),l=q.get('lang');
location.replace('{destino}'+'{extra}'+(l?'&lang='+l:'')+location.hash)}})();</script>
<meta http-equiv="refresh" content="0; url={destino}{extra}">
</head><body><p>Esta página está ahora en <a href="{destino}{extra}">{titulo}</a>.
· This page has moved to <a href="{destino}{extra}">{titulo}</a>.</p></body></html>
"""
CASOS = {"1", "1v", "2", "3", "4", "5", "6", "7"}


def verificar(d):
    fallos = []
    vistos = set()

    def nfc(t, donde):
        if isinstance(t, str) and unicodedata.normalize("NFC", t) != t:
            fallos.append("{0}: texto que no está en NFC".format(donde))

    entradas = next(c for c in d["clases"] if c["id"] == "nipata")["entradas"]
    for c in d["clases"]:
        for x in c.get("entradas", []) if c["id"] != "nipata" else []:
            if x["id"] in vistos:
                fallos.append("id repetido: " + x["id"])
            vistos.add(x["id"])
    for x in entradas:
        i = x["id"]
        if i in vistos:
            fallos.append("id repetido: " + i)
        vistos.add(i)
        for l in ("es", "en"):
            if not x["cab"].get(l, "").strip():
                fallos.append("{0}: cabecera sin {1}".format(i, l))
            nfc(x["cab"].get(l), i)
        for c in x["caso"]:
            if c not in CASOS:
                fallos.append("{0}: caso desconocido «{1}»".format(i, c))
        llamadas = set()
        for n, b in enumerate(x["bloques"]):
            donde = "{0} bloque {1}".format(i, n + 1)
            if b["tipo"] == "ej" and not b.get("pali", "").strip():
                fallos.append(donde + ": ejemplo sin pāḷi")
            for campo in ("pali", "es", "en", "ref"):
                nfc(b.get(campo), donde)
                llamadas |= set(re.findall(r"\[\^(\d+)\]", b.get(campo) or ""))
        for l in ("es", "en"):
            llamadas |= set(re.findall(r"\[\^(\d+)\]", x["cab"].get(l, "")))
        notas = {n["n"] for n in x["notas"]}
        for n in sorted(llamadas - notas):
            fallos.append("{0}: llamada [^{1}] sin nota".format(i, n))
    if not d["meta"].get("atribucion", {}).get("es"):
        fallos.append("meta: falta la atribución")
    return fallos


def guia(version, fecha):
    """La guía para el estudiante: (html, fallos). Como la del análisis: el
    markdown pasa por el intérprete de prosa de generar_recurso.py, con «> cita»
    y `código` además; el texto no se toca. Español e inglés, separados por
    una sola línea «---»; el «# título» de cada parte es el h1."""
    import html as H
    import generar_recurso as R
    if not os.path.exists(GUIA):
        return None, ["falta " + os.path.relpath(GUIA, RAIZ)]
    txt = open(GUIA, encoding="utf-8").read().replace("\r\n", "\n")
    fallos = []
    if unicodedata.normalize("NFC", txt) != txt:
        fallos.append("guia.md: texto que no está en NFC")
    lineas = txt.split("\n")
    corte = [i for i, l in enumerate(lineas) if l.strip() == "---" and i > 0]
    if len(corte) != 1:
        return None, fallos + ["guia.md: el español y el inglés se separan con una sola "
                               "línea «---» (hay {0})".format(len(corte))]
    partes = {"es": lineas[:corte[0]], "en": lineas[corte[0] + 1:]}
    base = R.inline
    R.inline = lambda t: re.sub(r"`([^`]+)`", r"<code>\1</code>", base(t))

    def bloques(ls):
        out, i = [], 0
        while i < len(ls):
            if ls[i].startswith(">"):
                j = i
                while j < len(ls) and ls[j].startswith(">"):
                    j += 1
                cita = " ".join(re.sub(r"^>\s?", "", x).strip() for x in ls[i:j]).strip()
                out.append("<blockquote><p>{0}</p></blockquote>".format(R.inline(cita)))
                i = j
                continue
            j = i
            while j < len(ls) and not ls[j].startswith(">"):
                j += 1
            out.append(R.render(ls[i:j])[0])
            i = j
        h = "\n".join(x for x in out if x)
        return re.sub(r'<ul class="doc-lista">(?=<li>\d+[.)] )', '<ul class="doc-lista num">', h)

    cuerpos, titulos = {}, {}
    try:
        for lg, ls in partes.items():
            ls = list(ls)
            i = next((k for k, l in enumerate(ls) if l.strip()), None)
            if i is None or not re.match(r"^#\s+\S", ls[i].strip()):
                fallos.append("guia.md: la parte «{0}» no empieza por «# título»".format(lg))
                continue
            h1 = re.sub(r"^#\s+", "", ls[i].strip())
            del ls[i]
            cuerpos[lg] = bloques(ls)
            limpio = re.sub(r"[*_`]", "", h1)
            titulos[lg] = {"titulo": limpio, "h1": limpio, "h1_html": R.inline(h1)}
    finally:
        R.inline = base
    if fallos:
        return None, fallos
    pl = open(GUIA_PLANTILLA, encoding="utf-8").read()
    js = json.dumps({lg: {"titulo": t["titulo"], "h1": t["h1"]} for lg, t in titulos.items()},
                    ensure_ascii=False).replace("</", "<\\/")
    pl = re.sub(r"/\*__TITULOS__\*/.*?/\*__FIN__\*/", lambda m: js, pl, flags=re.S)
    for clave, valor in (("__ES_TITULO__", H.escape(titulos["es"]["titulo"])),
                         ("__ES_H1__", titulos["es"]["h1_html"]),
                         ("__VERSION_DATE__", fecha),
                         ("__VERSION__", version),
                         ("__ES__", cuerpos["es"]), ("__EN__", cuerpos["en"])):
        pl = pl.replace(clave, valor)
    return pl, []


def main():
    d = unir(json.load(open(DATOS, encoding="utf-8")),
             json.load(open(DATOS_I, encoding="utf-8")))
    fallos = verificar(d)
    pagina_guia, f_guia = guia(d["meta"]["version"], d["meta"]["fecha"])
    fallos += f_guia
    if fallos:
        print("indeclinables NO cuadra; no se publica:")
        for f in fallos[:20]:
            print("  ✗", f)
        return 1
    pl = open(PLANTILLA, encoding="utf-8").read()
    m = re.search(r'/\*__DATOS__\*/.*?/\*__FIN__\*/', pl, re.S)
    if not m:
        print("La plantilla no tiene el marcador /*__DATOS__*/…/*__FIN__*/")
        return 1
    datos = json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = pl[:m.start()] + datos + pl[m.end():]
    meta = d["meta"]
    html = html.replace("__VERSION_DATE__", meta["fecha"]).replace("__VERSION__", meta["version"])
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    open(DESTINO, "w", encoding="utf-8").write(cabecera.insertar(html, "indeclinables"))
    os.makedirs(os.path.dirname(GUIA_DESTINO), exist_ok=True)
    open(GUIA_DESTINO, "w", encoding="utf-8").write(
        cabecera.insertar(pagina_guia, "indeclinables-guia"))
    # las direcciones antiguas remiten a la página nueva
    for ruta, destino, extra in ((VIEJA, "../indeclinables/", "?c=nipata"),
                                 (VIEJA_GUIA, "../../indeclinables/guia/", "?")):
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        open(ruta, "w", encoding="utf-8").write(REMISION.format(
            titulo="Indeclinables (abyaya)", destino=destino, extra=extra))
    ent = next(c for c in d["clases"] if c["id"] == "nipata")["entradas"]
    ej = sum(1 for x in ent for b in x["bloques"] if b["tipo"] == "ej")
    nuevas = sum(1 for x in ent if x.get("nuevo"))
    pref = len(d["clases"][0]["entradas"])
    print("v{0} ({1}) · {2} prefijos · {3} partículas ({4} añadidas por IEBH) · {5} ejemplos · "
          "{6}+{7} erratas → {8} (y la guía; /recursos/particulas/ remite)".format(
              meta["version"], meta["estado"]["es"], pref, len(ent), nuevas, ej,
              len(meta["erratas"]), len(meta.get("erratas_indeclinables", [])),
              os.path.relpath(DESTINO, RAIZ)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
