#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Del DPD completo a lo que el solucionador necesita, sin mover el giga de base.

Hoy el motor lee `dpd-formas.txt`: 443.740 líneas y nada más. Sin categoría,
`dhama` y `dhamma` valen lo mismo, y por eso `dhammaṃ` recibe quince lecturas de
las que catorce son ruido.

La base trae dos cosas que cambian eso:

  · **`lookup`** —1.281.569 filas— asocia cada forma flexionada con sus
    `headwords`, y **trae una columna `deconstructor`**: la descomposición que
    el propio DPD publica para esa forma. Es un segundo testigo del corte,
    independiente de nuestras reglas.
  · **`dpd_headwords`** —89.280 filas— da `lemma_1`, `lemma_2` y `pos`.

Escribe dos archivos de texto, chicos y auditables:

    dpd-pos.tsv            forma <tab> lema <tab> categoría   (una línea por par)
    dpd-descomposicion.tsv forma <tab> descomposición del DPD

    python3 exportar_dpd.py "C:\\...\\dpd-mobile.db"

**Abre la base en sólo lectura y no la toca.** Antes de escribir muestra una
muestra de lo que encontró, para que se vea si el formato es el esperado.
"""

import argparse
import io
import json
import os
import re
import sqlite3
import sys

if hasattr(sys.stdout, "reconfigure"):                    # Windows: cp1252 no
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def ids(v):
    """La columna `headwords` puede venir como JSON, como lista separada por
    comas, o vacía. Se acepta lo que haya y se ignora lo que no se entienda."""
    if not v:
        return []
    v = v.strip()
    try:
        d = json.loads(v)
        if isinstance(d, list):
            return [str(x) for x in d]
        if isinstance(d, (int, str)):
            return [str(d)]
    except (ValueError, TypeError):
        pass
    return [x for x in re.split(r"[,\s]+", v.strip("[]")) if x]


def piezas(v):
    """`deconstructor` viene como JSON con una o más descomposiciones."""
    if not v:
        return []
    try:
        d = json.loads(v)
        if isinstance(d, list):
            return [str(x) for x in d if x]
        if isinstance(d, str):
            return [d]
    except (ValueError, TypeError):
        return [v]
    return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base")
    ap.add_argument("--dir", default=".")
    a = ap.parse_args()
    if not os.path.exists(a.base):
        print("  No encuentro {0}".format(a.base))
        return 1

    cx = sqlite3.connect("file:{0}?mode=ro".format(a.base), uri=True)

    print("  Leyendo los lemas…")
    lema = {}
    for hid, l1, l2, pos in cx.execute(
            "SELECT id, lemma_1, lemma_2, pos FROM dpd_headwords"):
        lema[str(hid)] = ((l2 or l1 or "").strip(), (pos or "").strip())
    print("     {0} lemas".format(len(lema)))

    print("  Leyendo las formas…")
    fpos = os.path.join(a.dir, "dpd-pos.tsv")
    fdec = os.path.join(a.dir, "dpd-descomposicion.tsv")
    n = ndec = pares = 0
    muestra_pos, muestra_dec = [], []
    with io.open(fpos, "w", encoding="utf-8", newline="\n") as sp, \
         io.open(fdec, "w", encoding="utf-8", newline="\n") as sd:
        for clave, hw, dec in cx.execute(
                "SELECT lookup_key, headwords, deconstructor FROM lookup"):
            if not clave:
                continue
            n += 1
            vistos = set()
            for i in ids(hw):
                par = lema.get(i)
                if not par or par in vistos:
                    continue
                vistos.add(par)
                sp.write("{0}\t{1}\t{2}\n".format(clave, par[0], par[1]))
                pares += 1
                if len(muestra_pos) < 6:
                    muestra_pos.append((clave, par[0], par[1]))
            for d in piezas(dec):
                sd.write("{0}\t{1}\n".format(clave, d))
                ndec += 1
                if len(muestra_dec) < 6:
                    muestra_dec.append((clave, d))
    cx.close()

    print("\n  MUESTRA · forma → lema · categoría")
    for c, l, p in muestra_pos:
        print("     {0:<20} {1:<20} {2}".format(c[:20], l[:20], p[:28]))
    print("\n  MUESTRA · descomposición del propio DPD")
    for c, d in muestra_dec:
        print("     {0:<20} {1}".format(c[:20], d[:56]))

    print("\n  {0} formas · {1} pares forma-lema · {2} descomposiciones"
          .format(n, pares, ndec))
    for f in (fpos, fdec):
        print("  escrito: {0}  ({1:.1f} MB)"
              .format(os.path.basename(f), os.path.getsize(f) / 1e6))
    return 0


if __name__ == "__main__":
    sys.exit(main())
