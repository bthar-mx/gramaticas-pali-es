#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la referencia de paradigmas de declinación.

    python3 herramientas/generar_paradigmas.py

Junta dos cosas:

  recursos/paradigmas/paradigmas.json   las 84 entradas (83 documentos únicos),
                                        transcritas de los documentos del IEBH
  recursos/paradigmas/plantilla.html    el maquetado y la lógica

y escribe site/recursos/paradigmas/index.html.

Antes de escribir, verifica la integridad de los datos: cada paradigma con
tabla ha de tener las ocho inflexiones, tantas celdas por fila como columnas,
y ninguna celda vacía fuera del vocativo (donde el guion del documento se
transcribe como lista vacía). También coteja códigos, documentos y géneros
contra recursos/paradigmas/indice.json. Si algo no cuadra, no publica.
"""

import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATOS = os.path.join(RAIZ, "recursos", "paradigmas", "paradigmas.json")
INDICE = os.path.join(RAIZ, "recursos", "paradigmas", "indice.json")
PLANTILLA = os.path.join(RAIZ, "recursos", "paradigmas", "plantilla.html")
DESTINO = os.path.join(RAIZ, "site", "recursos", "paradigmas", "index.html")


def verificar(datos, indice):
    """Devuelve la lista de fallos; vacía si todo cuadra."""
    fallos = []
    entradas = datos["paradigmas"]
    imap = {e["codigo"]: e for e in indice["entradas"]}
    pmap = {p["codigo"]: p for p in entradas}

    for c in sorted(set(imap) - set(pmap)):
        fallos.append("falta en paradigmas.json: {0}".format(c))
    for c in sorted(set(pmap) - set(imap)):
        fallos.append("sobra respecto al índice: {0}".format(c))
    for c in sorted(set(imap) & set(pmap)):
        if imap[c]["doc"] != pmap[c]["doc"]:
            fallos.append("{0}: doc distinto del índice".format(c))
        if imap[c]["genero"] != pmap[c]["genero"]:
            fallos.append("{0}: género distinto del índice".format(c))

    n_infl = len(datos["inflexiones"])
    for p in entradas:
        c = p["codigo"]
        if "filas" not in p:
            continue  # F-O (igual_que) y Sufijos-Inflexiones
        if len(p["filas"]) != n_infl:
            fallos.append("{0}: {1} filas, se esperaban {2}".format(
                c, len(p["filas"]), n_infl))
            continue
        for i, fila in enumerate(p["filas"]):
            if len(fila) != len(p["columnas"]):
                fallos.append("{0} fila {1}: {2} celdas para {3} columnas".format(
                    c, i, len(fila), len(p["columnas"])))
            for celda in fila:
                if not celda and i != 1:  # sólo el vocativo admite guion
                    fallos.append("{0} fila {1}: celda vacía fuera del "
                                  "vocativo".format(c, i))
                for v in celda:
                    if not v.strip() or v != v.strip():
                        fallos.append("{0} fila {1}: variante mal recortada "
                                      "{2!r}".format(c, i, v))
                    if unicodedata.normalize("NFC", v) != v:
                        fallos.append("{0} fila {1}: {2!r} no está en "
                                      "NFC".format(c, i, v))
    return fallos


def main():
    datos = json.load(open(DATOS, encoding="utf-8"))
    indice = json.load(open(INDICE, encoding="utf-8"))

    fallos = verificar(datos, indice)
    if fallos:
        print("paradigmas.json NO cuadra; no se publica:")
        for f in fallos[:20]:
            print("  ✗", f)
        if len(fallos) > 20:
            print("  … y {0} más".format(len(fallos) - 20))
        return 1

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

    entradas = datos["paradigmas"]
    con_tabla = [p for p in entradas if "filas" in p]
    formas = sum(len(v) for p in con_tabla
                 for fila in p["filas"] for v in fila)
    docs = len({p["doc"] for p in entradas})
    print("{0} entradas · {1} tablas · {2} documentos · {3} formas → {4}".format(
        len(entradas), len(con_tabla), docs, formas,
        os.path.relpath(DESTINO, RAIZ)))

    # avisos útiles, sin detener la publicación
    con_nota = [p["codigo"] for p in entradas if p.get("notas")]
    if con_nota:
        print("  con nota de transcripción: {0}".format(", ".join(con_nota)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
