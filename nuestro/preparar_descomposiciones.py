#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deja las descomposiciones del DPD en un archivo **ordenado y buscable**.

`dpd-descomposicion.tsv` son 101 MB y 2.058.431 líneas. Cargarlo en memoria
tarda once segundos y ocupa 463 MB: demasiado para una pantalla que arranca con
un doble clic. Ordenado por la clave de cotejo se busca por bisección sobre el
archivo, sin cargar nada y sin esperar.

Sigue siendo un archivo de texto que se puede abrir y leer, que es la condición
de todo lo que este proyecto guarda.

    python3 preparar_descomposiciones.py
"""

import io
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from rutas import ruta, destino                                    # noqa: E402
from normalizar import cotejo                                      # noqa: E402

ENTRADA = ruta("recursos", "lexico", "dpd-descomposicion.tsv")
if not __import__("os").path.exists(ENTRADA):
    ENTRADA = ruta("dpd-descomposicion.tsv")
SALIDA = destino("recursos", "lexico", "dpd-descomposiciones.tsv")


def main():
    if not os.path.exists(ENTRADA):
        print("  Falta {0}. Lo genera exportar-dpd.bat.".format(ENTRADA))
        return 1
    print("  Leyendo {0}…".format(os.path.basename(ENTRADA)))
    junto = {}
    n = 0
    with io.open(ENTRADA, encoding="utf-8") as f:
        for ln in f:
            i = ln.find("\t")
            if i < 1:
                continue
            k = cotejo(ln[:i])
            v = ln[i + 1:].rstrip("\n").strip()
            if not k or not v:
                continue
            n += 1
            if k in junto:
                if v not in junto[k]:
                    junto[k].append(v)
            else:
                junto[k] = [v]
    print("  {0} líneas · {1} formas distintas".format(n, len(junto)))
    with io.open(SALIDA, "w", encoding="utf-8", newline="\n") as s:
        for k in sorted(junto):
            s.write("{0}\t{1}\n".format(k, " | ".join(junto[k])))
    print("  escrito: {0}  ({1:.1f} MB)"
          .format(os.path.basename(SALIDA), os.path.getsize(SALIDA) / 1e6))
    return 0


if __name__ == "__main__":
    sys.exit(main())
