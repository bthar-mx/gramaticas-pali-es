#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprueba que ningún texto de los dos borradores —la clasificación
(recursos/clasificacion/datos.json) y el análisis según Visuddhāyuṃ
(recursos/analisis/datos/*.json)— haya llegado a las páginas de cada sutta,
/s/N/ y /en/s/N/, que se indexan (decisión del IEBH, 2026-10-08).

    python3 herramientas/comprobar_hub_borradores.py

De cada cadena de 30 caracteres o más de esos datos toma tres trozos de 30
(principio, medio y final) y los busca en el texto de las 810 páginas. Un
trozo que aparece y que también está en las páginas de los capítulos no
cuenta: es texto del capítulo que el borrador cita (el vutti, la glosa). Sale
con 1 si queda alguno que no esté en el capítulo.
"""

import glob
import html
import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def norm(t):
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", t)).strip().lower()


def cadenas():
    out = []

    def junta(x, origen):
        if isinstance(x, str):
            if len(x) >= 30:
                out.append((origen, x))
        elif isinstance(x, dict):
            for v in x.values():
                junta(v, origen)
        elif isinstance(x, list):
            for v in x:
                junta(v, origen)

    d = json.load(open(os.path.join(RAIZ, "recursos", "clasificacion", "datos.json"), encoding="utf-8"))
    for n, e in d["suttas"].items():
        junta(e, "clasificación §" + n)
    m = json.load(open(os.path.join(RAIZ, "recursos", "analisis", "meta.json"), encoding="utf-8"))
    for f in m["capitulos"]:
        for s in json.load(open(os.path.join(RAIZ, "recursos", "analisis", "datos", f), encoding="utf-8"))["suttas"]:
            junta(s, "análisis §{0}".format(s["n"]))
    return out


def main():
    trozos = []
    for o, x in cadenas():
        t = norm(x)
        for i in sorted({0, max(0, len(t) // 2 - 15), max(0, len(t) - 30)}):
            trozos.append((o, t[i:i + 30]))
    paginas = glob.glob(os.path.join(RAIZ, "site", "s", "*", "index.html")) + \
        glob.glob(os.path.join(RAIZ, "site", "en", "s", "*", "index.html"))
    todo = "\n".join(norm(open(p, encoding="utf-8").read()) for p in paginas)
    caps = "\n".join(norm(open(p, encoding="utf-8").read()) for p in
                     glob.glob(os.path.join(RAIZ, "site", "kaccayana", "*", "index.html")) +
                     glob.glob(os.path.join(RAIZ, "site", "en", "kaccayana", "*", "index.html")))
    vistos = [(o, t) for o, t in trozos if t in todo]
    ajenos = [(o, t) for o, t in vistos if t not in caps]
    print("{0} trozos de los borradores en {1} páginas de sutta: {2} aparecen, "
          "{3} son texto del capítulo, {4} no".format(
              len(trozos), len(paginas), len(vistos), len(vistos) - len(ajenos), len(ajenos)))
    for o, t in ajenos:
        print("   ", o, repr(t))
    return 1 if ajenos else 0


if __name__ == "__main__":
    sys.exit(main())
