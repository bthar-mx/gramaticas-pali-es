# -*- coding: utf-8 -*-
"""
Glosario de los globos (tooltips) que comparten /recursos/clasificacion/ y
/recursos/analisis/.

    recursos/terminos/terminos.json   término, formas que se buscan en el
                                      texto, definición ES/EN, ejemplo (§ y
                                      capítulo), fuente y marca «revisar»

cargar(raiz) devuelve la lista con cada ejemplo completado con el texto pāḷi
del sutta y la primera línea de su traducción publicada (kaccayana/0N-*.md y
0N-*.en.md), para no redactar glosas nuevas. Si un § no existe, o una forma
está repetida en dos términos, lanza ValueError: el generador no publica.
"""

import json
import os
import unicodedata

from generar_clasificacion import leer_md

MD = {"sandhi": "01-sandhi-kappa", "nama": "02-nama-kappa", "karaka": "03-karaka-kappa",
      "samasa": "04-samasa-kappa", "taddhita": "05-taddhita-kappa"}


def cargar(raiz):
    d = json.load(open(os.path.join(raiz, "recursos", "terminos", "terminos.json"), encoding="utf-8"))
    textos, vistas, fallos = {}, {}, []
    for t in d["terminos"]:
        e = t["ejemplo"]
        md = MD.get(e["cap"])
        if not md:
            fallos.append("{0}: capítulo desconocido «{1}»".format(t["clave"], e["cap"]))
            continue
        for lengua, suf in (("es", ".md"), ("en", ".en.md")):
            k = md + suf
            if k not in textos:
                textos[k] = leer_md(os.path.join(raiz, "kaccayana", k))[0]
            s = textos[k].get(e["n"])
            if not s:
                fallos.append("{0}: §{1} no está en {2}".format(t["clave"], e["n"], k))
                continue
            e["sutta"] = s["sutta"]
            e.setdefault("tr", {})[lengua] = s["tr"]
        for f in t["formas"]:
            if f in vistas:
                fallos.append("forma «{0}» repetida en {1} y {2}".format(f, vistas[f], t["clave"]))
            vistas[f] = t["clave"]
        for x in (t["def"]["es"], t["def"]["en"]):
            if unicodedata.normalize("NFC", x) != x:
                fallos.append("{0}: texto que no está en NFC".format(t["clave"]))
    if fallos:
        raise ValueError("; ".join(fallos[:10]))
    return d["terminos"]
