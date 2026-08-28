#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Separa los dos problemas de la detección y los mide sobre el banco.

    python3 nuestro/medir_deteccion.py

No son un problema sino dos, y mezclarlos hace que el número de cobertura no
signifique nada:

  · **Dentro de una palabra** hay que buscar **dónde** está el corte.
  · **Entre dos palabras escritas** hay que decidir **si** la juntura es un
    punto de sandhi.

El encargo llama a lo segundo *«un problema distinto y más difícil»* y lo deja
para la tercera etapa. Esta medición dice cuánto del banco cae de cada lado.

Mide también la señal de superficie —apóstrofo, guion, grupo inicial imposible—
y, sobre todo, **cuántas formas no traen ninguna**. La puerta se calibra a
recall y no a precisión: el falso positivo lo limpia el motor cuando el corte no
recompone; el falso negativo no lo limpia nadie, porque el motor nunca ve esa
palabra.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rutas import ruta                                            # noqa: E402
from grupos_iniciales import grupo_inicial, letras                # noqa: E402

REGLAS = ruta("recursos", "sandhi", "reglas.json")
GRUPOS = ruta("recursos", "lexico", "grupos-iniciales.json")
LEXICO = ruta("recursos", "lexico", "dpd-formas.txt")

SELLOS = "’'-"


def main():
    d = json.load(open(REGLAS, encoding="utf-8"))
    formas = [c["f"] for c in d["ce"]]
    atestiguados = set(json.load(open(GRUPOS, encoding="utf-8"))["atestiguados"])
    lexico = set(x for x in open(LEXICO, encoding="utf-8").read().split("\n") if x)

    un_token = [f for f in formas if len(f.split()) == 1]
    varios = [f for f in formas if len(f.split()) > 1]

    def sello(f):
        return any(c in f for c in SELLOS)

    def grupo_malo(f):
        return any(grupo_inicial(p) not in atestiguados
                   for p in f.replace("’", " ").replace("'", " ").split() if p)

    def en_lexico(f):
        return f.replace("’", "").replace("'", "").replace("-", "").replace(" ", "") in lexico

    print("LOS DOS PROBLEMAS, MEDIDOS SOBRE LAS 266\n")
    print("  un solo token: {0}   ·   dos o más: {1}".format(len(un_token), len(varios)))
    print("     dentro de una palabra se busca DÓNDE está el corte")
    print("     entre dos palabras se decide SI la juntura es sandhi")

    for nombre, grupo in (("un solo token", un_token), ("dos o más tokens", varios),
                          ("las 266", formas)):
        con_sello = [f for f in grupo if sello(f)]
        con_grupo = [f for f in grupo if not sello(f) and grupo_malo(f)]
        sin_nada = [f for f in grupo if not sello(f) and not grupo_malo(f)]
        print("\n  {0} ({1}):".format(nombre, len(grupo)))
        print("     con sello ortográfico —apóstrofo o guion—: {0}".format(len(con_sello)))
        print("     sin sello, con grupo inicial no atestiguado: {0}".format(len(con_grupo)))
        print("     SIN NINGUNA SEÑAL DE SUPERFICIE: {0}   ({1:.0f} %)".format(
            len(sin_nada), 100.0 * len(sin_nada) / max(1, len(grupo))))

    entera = [f for f in un_token if en_lexico(f)]
    print("\n  De las {0} de un solo token, el DPD reconoce entera a {1}."
          .format(len(un_token), len(entera)))
    print("     Son las que ninguna señal de superficie puede delatar: están")
    print("     escritas como una palabra y además son una palabra del léxico.")
    print("     A éstas sólo las encuentra intentar el corte y comprobar.")
    for f in entera[:14]:
        print("        {0}".format(f))
    if len(entera) > 14:
        print("        … y {0} más".format(len(entera) - 14))
    return 0


if __name__ == "__main__":
    sys.exit(main())
