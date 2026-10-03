#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera «Análisis de los suttas de Kaccāyana según la Visuddhāyuṃ
Kaccāyana-ṭīkā» (borrador), en español e inglés en la misma página.

    python3 herramientas/generar_analisis.py

Junta:

  recursos/analisis/meta.json          versión, estado y cita del libro
  recursos/analisis/datos/NN-*.json    un archivo por capítulo: clase de
                                          sutta según el libro, anuvatti,
                                          funciones (kāriyī / kāriya /
                                          nimitta, saññā / saññī, visaya /
                                          visayī), ejemplo marcado, notas y
                                          página del PDF; notas en es/en
  kaccayana/0N-*.md                       el texto pāḷi de cada aforismo
  recursos/analisis/plantilla.html     el maquetado y la lógica

y escribe site/recursos/analisis/index.html.

Antes de escribir verifica que cada capítulo tenga todos sus aforismos, sin
huecos ni sobrantes; que la página del PDF esté dentro del capítulo y no
retroceda; que las marcas del ejemplo ({k|…} {n|…} {r|…} {x|…} {kx|…} {nx|…})
estén bien formadas; que cada nimitta lleve su caso; y que todo esté en NFC.
Si algo no cuadra, no publica.
"""

import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generar_clasificacion import leer_md  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(RAIZ, "recursos", "analisis")
PLANTILLA = os.path.join(DIR, "plantilla.html")
DESTINO = os.path.join(RAIZ, "site", "recursos", "analisis", "index.html")

ROLES = {"kāriyī", "kāriya", "nimitta", "saññā", "saññī", "visaya", "visayī"}
CASOS = {"7", "5", "3", "5+7"}
MARCA = re.compile(r"\{(k|n|r|x|kx|nx)\|([^{}|]+)\}")


def nfc(x):
    if isinstance(x, str):
        return unicodedata.normalize("NFC", x) == x
    if isinstance(x, list):
        return all(nfc(i) for i in x)
    if isinstance(x, dict):
        return all(nfc(v) for v in x.values())
    return True


def verificar(cap, textos):
    fallos = []
    rango = set(range(cap["desde"], cap["hasta"] + 1))
    ns = [s["n"] for s in cap["suttas"]]
    if set(ns) != rango or len(ns) != len(rango):
        fallos.append("{0}: faltan {1}, sobran {2}".format(
            cap["clave"], sorted(rango - set(ns))[:8], sorted(set(ns) - rango)[:8]))
    faltan_md = sorted(rango - set(textos))
    if faltan_md:
        fallos.append("{0}: el markdown no tiene {1}".format(cap["md"], faltan_md[:8]))
    previa = 0
    for s in cap["suttas"]:
        n = s["n"]
        if not cap["pdf"][0] <= s["pdf"] <= cap["pdf"][1]:
            fallos.append("§{0}: página del PDF {1} fuera del capítulo".format(n, s["pdf"]))
        if s["pdf"] < previa:
            fallos.append("§{0}: la página del PDF retrocede".format(n))
        previa = s["pdf"]
        for r in s["roles"] + s.get("respuesta", []):
            if r[0] not in ROLES:
                fallos.append("§{0}: función desconocida «{1}»".format(n, r[0]))
            if r[0] == "nimitta" and (len(r) < 4 or r[3] not in CASOS):
                fallos.append("§{0}: nimitta sin caso".format(n))
        resto = MARCA.sub("", s["ejemplo"])
        if any(c in resto for c in "{}|"):
            fallos.append("§{0}: marca mal formada en el ejemplo".format(n))
        if s.get("ejercicio") and MARCA.search(s["ejemplo"]):
            fallos.append("§{0}: un ejercicio no lleva el ejemplo marcado".format(n))
        nota = s.get("nota", {})
        if bool(nota.get("es", "").strip()) != bool(nota.get("en", "").strip()):
            fallos.append("§{0}: la nota no está en las dos lenguas".format(n))
        if s.get("respuesta") and not s.get("ejercicio"):
            fallos.append("§{0}: respuesta sin ejercicio".format(n))
        if not nfc(s):
            fallos.append("§{0}: texto que no está en NFC".format(n))
    return fallos


def main():
    meta = json.load(open(os.path.join(DIR, "meta.json"), encoding="utf-8"))
    caps, fallos = [], []
    for nombre in meta["capitulos"]:
        cap = json.load(open(os.path.join(DIR, "datos", nombre), encoding="utf-8"))
        textos = leer_md(os.path.join(RAIZ, "kaccayana", cap["md"] + ".md"))[0]
        fallos += verificar(cap, textos)
        for s in cap["suttas"]:
            if s["n"] in textos:
                s["sutta"] = textos[s["n"]]["sutta"]
        caps.append(cap)
    indice = []
    for c in meta["indice"]:
        e = {"clave": c["clave"], "pali": c["pali"], "kandas": [], "desde": None, "hasta": None}
        ruta = os.path.join(RAIZ, "kaccayana", c["md"] + ".md") if c["md"] else ""
        if ruta and os.path.exists(ruta):
            t, ks = leer_md(ruta)
            e["desde"], e["hasta"] = min(t), max(t)
            for i, (k, desde) in enumerate(ks):
                hasta = ks[i + 1][1] - 1 if i + 1 < len(ks) else e["hasta"]
                e["kandas"].append([k, desde, hasta])
        indice.append(e)
    if not nfc(meta):
        fallos.append("meta.json: texto que no está en NFC")
    if fallos:
        print("El análisis de los suttas NO cuadra; no se publica:")
        for f in fallos[:25]:
            print("  ✗", f)
        return 1

    filas = []
    for cap in caps:
        for s in cap["suttas"]:
            s["cap"] = cap["clave"]
            filas.append(s)
    try:
        import terminos
        glosario = terminos.cargar(RAIZ)
    except ValueError as err:
        print("El glosario de los globos NO cuadra; no se publica:", err)
        return 1
    salida = {"meta": meta, "indice": indice, "terminos": glosario,
              "capitulos": [{k: c[k] for k in ("clave", "pali", "desde", "hasta", "pdf", "paginas")} for c in caps],
              "filas": filas}

    pl = open(PLANTILLA, encoding="utf-8").read()
    m = re.search(r'/\*__DATOS__\*/.*?/\*__FIN__\*/', pl, re.S)
    if not m:
        print("La plantilla no tiene el marcador /*__DATOS__*/…/*__FIN__*/")
        return 1
    datos = json.dumps(salida, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = pl[:m.start()] + datos + pl[m.end():]
    html = html.replace("__VERSION_DATE__", meta["fecha"]).replace("__VERSION__", meta["version"])
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    open(DESTINO, "w", encoding="utf-8").write(html)

    ej = sum(1 for f in filas if f.get("ejercicio"))
    print("Análisis (Visuddhāyuṃ) v{0} ({1}) · {2} aforismos · {3} ejercicios → {4}".format(
        meta["version"], meta["estado"], len(filas), ej, os.path.relpath(DESTINO, RAIZ)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
