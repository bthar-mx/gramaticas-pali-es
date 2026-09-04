#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""De la página IMPRESA del Saddanīti a la hoja del PDF, y al revés.

Para qué sirve
--------------
Las referencias de Helmer Smith son del tipo «755,11—15»: página impresa y
línea. Los subíndices de línea del Conspectus no se leen con seguridad a
400 dpi, y el remedio es abrir la página citada y contar las líneas del
margen (briefing de la sesión 48, §2). Para eso hay que saber qué hoja del
PDF es la página impresa N, y ahí es fácil equivocarse:

- La correspondencia NO es la misma en los cinco volúmenes, y el signo
  CAMBIA: en el vol. 01 la hoja del PDF es MAYOR que la página impresa
  (hoja = impresa + 15, por las portadas y el prefacio), y en los otros
  cuatro es menor, porque cada volumen empieza a numerar donde acabó el
  anterior.
- El campo `leafNum` de los `.paginas.json` empieza en 0 y `pdftoppm -f`
  empieza en 1: hay un desfase de una unidad que se cuela con facilidad.
- Dentro de un mismo volumen puede haber MÁS DE UN desfase. El vol. 04 usa
  uno para las pp. 930-945 y otro a partir de la 946.

Por eso este guion no calcula nada: lee la correspondencia real de los
`.paginas.json`, que es la que trae el propio escaneo.

Uso
---
    python3 herramientas/pagina_saddaniti.py 755
    python3 herramientas/pagina_saddaniti.py 127 129 1132
    python3 herramientas/pagina_saddaniti.py --tabla

Imprime, para cada página impresa, el volumen, la hoja del PDF y la orden
de pdftoppm lista para copiar.
"""

import collections
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(RAIZ, "recursos", "saddaniti")
VOLUMENES = ("01", "02", "03", "04", "05")


def mapa():
    """{página impresa: (volumen, hoja del PDF 1-based)}, leído del escaneo."""
    salida = {}
    for vol in VOLUMENES:
        ruta = os.path.join(DIR, "saddaniti-smith-{0}.paginas.json".format(vol))
        if not os.path.exists(ruta):
            continue
        for p in json.load(open(ruta, encoding="utf-8"))["pages"]:
            numero = (p.get("pageNumber") or "").strip()
            if numero.isdigit():
                # leafNum va desde 0; pdftoppm -f cuenta desde 1
                salida[int(numero)] = (vol, p["leafNum"] + 1)
    return salida


def tabla(m):
    """Los tramos de desfase constante, volumen por volumen."""
    por_vol = collections.defaultdict(list)
    for impresa, (vol, hoja) in m.items():
        por_vol[vol].append((impresa, hoja))
    filas = []
    for vol in VOLUMENES:
        paginas = sorted(por_vol.get(vol, []))
        if not paginas:
            continue
        inicio, desfase_previo = None, None
        for impresa, hoja in paginas:
            desfase = hoja - impresa
            if desfase != desfase_previo:
                if inicio is not None:
                    filas.append((vol, inicio, anterior, desfase_previo))
                inicio, desfase_previo = impresa, desfase
            anterior = impresa
        filas.append((vol, inicio, anterior, desfase_previo))
    return filas


def main(argv):
    m = mapa()
    if not m:
        print("No hay .paginas.json en recursos/saddaniti/")
        return 1

    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0

    if argv[0] == "--tabla":
        print("vol.  páginas impresas      hoja del PDF = impresa +")
        for vol, desde, hasta, desfase in tabla(m):
            print("  {0}   {1:>5} - {2:<5}        {3:+d}".format(
                vol, desde, hasta, desfase))
        print("\nOjo: el signo cambia. En el vol. 01 la hoja del PDF es MAYOR "
              "que la página\nimpresa; en los otros cuatro, menor. Y hay "
              "volúmenes con más de un tramo.")
        return 0

    fallo = 0
    for arg in argv:
        if not arg.isdigit():
            print("{0}: no es un número de página".format(arg))
            fallo = 1
            continue
        impresa = int(arg)
        if impresa not in m:
            print("p. {0}: no está en el escaneo (el rango es {1}-{2})".format(
                impresa, min(m), max(m)))
            fallo = 1
            continue
        vol, hoja = m[impresa]
        print("p. {0}  →  vol. {1}, hoja {2} del PDF".format(impresa, vol, hoja))
        print("    pdftoppm -r 400 -f {0} -l {0} -png -singlefile \\\n"
              "      recursos/saddaniti/saddaniti-smith-{1}.pdf /tmp/s{2}"
              .format(hoja, vol, impresa))
    return fallo


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
