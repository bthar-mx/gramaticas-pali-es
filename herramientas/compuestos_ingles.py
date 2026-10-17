#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edición inglesa de «Compuestos (samāsa)»: rellena los campos «en» vacíos de
compuestos.json con la tabla recursos/compuestos/ingles.json, que va de cada
cadena española (tal como sale en compuestos.json) a su inglés.

    python3 herramientas/compuestos_ingles.py            # rellena compuestos.json
    python3 herramientas/compuestos_ingles.py --faltan   # lista lo que no tiene inglés

compuestos_a_json.py llama a rellenar() antes de escribir, así que la cadena de
siempre ya trae el inglés. La tabla se busca por el texto español entero: si una
línea cambia en español, su inglés deja de aplicarse y aparece en «--faltan»
(la página muestra entonces el español en la edición inglesa, como hasta ahora).
Un «en» que ya trae algo (estado, atribución, cabecera «Meaning») no se toca.
"""

import json
import os
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(RAIZ, "recursos", "compuestos")
TABLA = os.path.join(DIR, "ingles.json")
DATOS = os.path.join(DIR, "compuestos.json")


def nfc(s):
    return unicodedata.normalize("NFC", s)


def cargar():
    if not os.path.exists(TABLA):
        return {}
    t = json.load(open(TABLA, encoding="utf-8"))
    t.pop("_nota", None)
    return {nfc(k): nfc(v) for k, v in t.items()}


def rellenar(datos, tabla=None):
    """Rellena en su sitio. Devuelve (rellenados, faltan: lista de cadenas)."""
    tabla = cargar() if tabla is None else tabla
    hechos, faltan = 0, []

    def walk(x):
        nonlocal hechos
        if isinstance(x, dict):
            if isinstance(x.get("es"), str) and "en" in x and not x["en"] and x["es"].strip():
                en = tabla.get(nfc(x["es"]))
                if en:
                    x["en"] = en
                    hechos += 1
                else:
                    faltan.append(x["es"])
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(datos)
    return hechos, faltan


def main(argv):
    datos = json.load(open(DATOS, encoding="utf-8"))
    hechos, faltan = rellenar(datos)
    if "--faltan" in argv:
        for s in dict.fromkeys(faltan):
            print(s)
        return 0
    s = json.dumps(datos, ensure_ascii=False, indent=1)
    open(DATOS, "w", encoding="utf-8").write(nfc(s) + "\n")
    print("→ inglés: {0} campos rellenados; {1} sin inglés ({2} cadenas distintas)".format(
        hechos, len(faltan), len(set(faltan))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
