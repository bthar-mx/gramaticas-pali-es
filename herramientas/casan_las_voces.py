#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""¿Es la misma segunda voz, escrita de dos maneras?

**Por qué existe este archivo.** El IEBH escribe la segunda voz tal como sale
en la página, ya elidida —«vuttan + ti»—; el motor la escribe subyacente
—«vuttaṃ + iti»—. Es el mismo análisis. Comparar las dos cadenas con `==`
cuenta como desacuerdo lo que es una convención de escritura, y
`extraer_junturas_separadas.py` ya lo advierte en un comentario.

Lo que este archivo añade es lo contrario, y es la lección de la sesión 40: al
aflojar la comparación para no contar de más, se cuenta de menos. Tres medidas
salieron mal en una tarde por comparadores sueltos:

  · con `==` a secas             → 2.032 «desacuerdos» donde no los hay
  · con «una es cola de la otra» → «imāha» casaba con «āha», y «ha» también,
                                   de modo que un experimento parecía arreglar
                                   siete junturas y arreglaba una

De ahí la regla que aplica `casan`, y que es gramatical, no de conveniencia:

    **el sandhi puede ELIDIR la vocal inicial de la segunda voz, o cambiarle
    la cantidad; NO puede añadirle una vocal.**

Por eso «iti»→«ti» casa y «ha»→«āha» no: «ha» no es «āha» con algo elidido,
es otra voz. La cláusula inversa —la que permitiría que la voz del IEBH fuese
más larga que la del motor— **no existe a propósito**; si alguien la echa de
menos, que lea antes este párrafo.

    python3 herramientas/casan_las_voces.py     # corre las pruebas

<!-- DUDA: la cláusula de cantidad («iti» casa con «īti») está puesta porque
     el alargamiento en juntura existe y aparece en el banco. Pero es más
     ancha que las otras dos y no se ha medido cuánto admite de más. Si el
     IEBH prefiere quitarla, la medida se rehace sin ella. -->
"""

import os
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "nuestro"))
from normalizar import cotejo                                      # noqa: E402

VOCALES = set("aāiīuūeo")
CANTIDAD = {"a": "ā", "i": "ī", "u": "ū", "ā": "a", "ī": "i", "ū": "u"}


def _n(s):
    s = unicodedata.normalize("NFC", str(s)).strip().strip("’'`").lower()
    return cotejo(s)


def casan(superficie, subyacente):
    """`superficie` es la voz del IEBH; `subyacente`, la del motor."""
    a, b = _n(superficie), _n(subyacente)
    if not a or not b:
        return False
    if a == b:
        return True
    if b[0] in VOCALES and b[1:] == a:            # elisión de la vocal inicial
        return True
    if b[0] in CANTIDAD and CANTIDAD[b[0]] + b[1:] == a:          # cantidad
        return True
    return False


PRUEBAS = [
    # la misma voz, escrita de dos modos — tienen que casar
    ("ti", "iti", True), ("pi", "api", True), ("va", "eva", True),
    ("ssa", "assa", True), ("āha", "āha", True), ("ca", "ca", True),
    ("ettha", "ettha", True), ("ānanda", "ānanda", True),
    ("iti", "īti", True),
    # voces distintas — NO pueden casar
    ("āha", "iha", False),        # el fallo de masa del banco
    ("āha", "ha", False),         # el que colaba el «endswith»
    ("atthaṃ", "amatthaṃ", False),
    ("ānanda", "āmānanda", False),
    ("araṃ", "aparaṃ", False),
]


def main():
    mal = 0
    for sup, sub, esperado in PRUEBAS:
        obtenido = casan(sup, sub)
        if obtenido != esperado:
            mal += 1
            print(f"  MAL  IEBH «{sup}»  motor «{sub}»  "
                  f"-> {obtenido}, se esperaba {esperado}")
    print(f"{len(PRUEBAS) - mal}/{len(PRUEBAS)} pruebas pasan.")
    return 1 if mal else 0


if __name__ == "__main__":
    sys.exit(main())
