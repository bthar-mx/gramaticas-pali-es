#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parte el léxico del canon en fragmentos por letra inicial, para la carga bajo
demanda del solucionador en el navegador (etapa 2 del porte a JS, briefing
sesión 30 §6).

    python3 herramientas/generar_lexico_solucionador.py

Fuente: `recursos/corpus/corpus-formas.json` (las 681.927 formas de los 118
volúmenes convertidos del OSBCT). Cada forma pasa por `cotejo()` —el léxico
del motor compara en forma canónica— y se deduplica; cada fragmento va
ordenado, para que la salida sea determinista y el diff legible.

Salida: `recursos/solucionador/lexico/<letra>.json` + `indice.json`. Los
nombres de archivo son ASCII a propósito: en macOS el sistema de archivos
normaliza a NFD y un `ā.json` puede volverse otro byte a byte sin que nadie lo
toque. La tabla letra → archivo va en el índice; nadie deduce el nombre.

Generado, no fuente: se regenera cuando cambie el corpus; nunca se edita a
mano.
"""

import json
import os
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "nuestro"))
from normalizar import cotejo                                      # noqa: E402

CORPUS = os.path.join(RAIZ, "recursos", "corpus", "corpus-formas.json")
DESTINO = os.path.join(RAIZ, "recursos", "solucionador", "lexico")

# Letra inicial → nombre de archivo ASCII. La larga y la retrofleja doblan la
# letra; las nasales con diacrítico van por su clase (ñ→ny, ṅ→ng). No hay
# colisión: la clave del léxico es la primera LETRA (un solo carácter), nunca
# un dígrafo.
ASCII = {"ā": "aa", "ī": "ii", "ū": "uu",
         "ṭ": "tt", "ḍ": "dd", "ṇ": "nn", "ḷ": "ll",
         "ñ": "ny", "ṅ": "ng", "ṃ": "mm"}


def nombre(letra):
    if letra in ASCII:
        return ASCII[letra]
    if letra.isascii() and letra.isalnum():
        return letra
    return "x" + "-".join("{0:04x}".format(ord(c)) for c in letra)


def main():
    d = json.load(open(CORPUS, encoding="utf-8"))
    formas = sorted({cotejo(f) for f in d.get("formas", {})} - {""})

    grupos = {}
    for f in formas:
        grupos.setdefault(f[0], []).append(f)

    os.makedirs(DESTINO, exist_ok=True)
    indice = {"origen": "recursos/corpus/corpus-formas.json",
              "total": len(formas), "fragmentos": {}}
    usados = {}
    for letra in sorted(grupos):
        arch = nombre(letra) + ".json"
        if arch in usados:
            raise SystemExit("colisión de nombre: {0!r} y {1!r} dan {2}"
                             .format(usados[arch], letra, arch))
        usados[arch] = letra
        with open(os.path.join(DESTINO, arch), "w", encoding="utf-8") as f:
            json.dump(grupos[letra], f, ensure_ascii=False,
                      separators=(",", ":"))
        indice["fragmentos"][letra] = {"archivo": arch,
                                       "formas": len(grupos[letra])}
    with open(os.path.join(DESTINO, "indice.json"), "w", encoding="utf-8") as f:
        json.dump(indice, f, ensure_ascii=False, indent=1)

    print("{0} formas en {1} fragmentos → {2}".format(
        len(formas), len(grupos), os.path.relpath(DESTINO, RAIZ)))
    for letra in sorted(grupos):
        print("   {0}  {1:<8} {2:>7}".format(
            letra, indice["fragmentos"][letra]["archivo"],
            len(grupos[letra])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
