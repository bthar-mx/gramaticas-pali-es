#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la página «Formación del nombre · pācako».

    python3 herramientas/generar_nombre.py

Junta dos cosas:

  recursos/nombre/plantilla.html  el maquetado y el contenido
  kaccayana/*.md                  los capítulos publicados — de ahí se saca
                                  qué §N existe ya y en qué capítulo está,
                                  para enlazar cada referencia a su sutta

y escribe site/recursos/nombre/index.html.

Las referencias §N se derivan del markdown, nunca se copian: el día que se
publique el Kibbidhāna-Kappa, §457 y compañía se enlazan solas sin tocar la
plantilla. Las que todavía no tienen capítulo se dejan en texto plano, con
un title que dice por qué.
"""

import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "herramientas"))

from generar_capitulo import CAPITULOS, parsear  # noqa: E402

PLANTILLA = os.path.join(RAIZ, "recursos", "nombre", "plantilla.html")
DESTINO = os.path.join(RAIZ, "site", "recursos", "nombre", "index.html")

VERSION = "1.0"
VERSION_FECHA = "2026-08-18"

# Sólo se enlazan las referencias que van dentro de estos contenedores: la
# columna «Kacc.» de la tabla. El resto del texto se deja como está.
RE_CELDA_REF = re.compile(r'(<td class="ref">)(.*?)(</td>)', re.S)
RE_REF = re.compile(r'§(\d+)')


def mapa_suttas():
    """{numero_de_sutta: (slug_obra, slug_capitulo, titulo)} de lo publicado."""
    mapa = {}
    for clave, meta in CAPITULOS.items():
        md = os.path.join(RAIZ, meta["obra_slug"], clave + ".md")
        if not os.path.exists(md):
            continue
        for s in parsear(md)["suttas"]:
            mapa[int(s["n"])] = (meta["obra_slug"], meta["slug"],
                                 meta["titulo_pali"])
    return mapa


def enlazar(html, mapa):
    pendientes, enlazadas = [], []

    def una(m):
        n = int(m.group(1))
        destino = mapa.get(n)
        if not destino:
            pendientes.append(n)
            return ('<span class="xref-pend" title="Capítulo todavía en '
                    'preparación">§{0}</span>'.format(n))
        obra, cap, titulo = destino
        enlazadas.append(n)
        return ('<a class="xref" href="../../{0}/{1}/#s{2}" '
                'title="{3} · §{2}">§{2}</a>'.format(obra, cap, n, titulo))

    def celda(m):
        return m.group(1) + RE_REF.sub(una, m.group(2)) + m.group(3)

    return RE_CELDA_REF.sub(celda, html), enlazadas, pendientes


def main():
    if not os.path.exists(PLANTILLA):
        print("falta {0}".format(os.path.relpath(PLANTILLA, RAIZ)))
        return 1

    html = open(PLANTILLA, encoding="utf-8").read()
    mapa = mapa_suttas()
    html, enlazadas, pendientes = enlazar(html, mapa)

    html = html.replace("__VERSION_DATE__", VERSION_FECHA)
    html = html.replace("__VERSION__", VERSION)

    if "__VERSION" in html:
        print("aviso — han quedado marcadores sin sustituir")

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    with open(DESTINO, "w", encoding="utf-8") as f:
        f.write(html)

    print("{0} referencias enlazadas · {1} pendientes de capítulo → {2}".format(
        len(enlazadas), len(pendientes), os.path.relpath(DESTINO, RAIZ)))
    if pendientes:
        print("  sin capítulo publicado: {0}".format(
            ", ".join("§{0}".format(n) for n in sorted(set(pendientes)))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
