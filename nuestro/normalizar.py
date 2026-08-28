#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
`cotejo()`: la forma canónica para COMPARAR dos voces pāḷi.

    python3 nuestro/normalizar.py          # se mide sobre el banco y se informa

Normalizar es sólo para comparar. **Nunca para guardar ni para mostrar**: si se
aplicara al escribir se perderían los nombres propios —Gotama, Sāriputta— y la
niggahīta tal como la escribe cada fuente. Quien muestre una forma al usuario
muestra la escrita, no ésta.

`cotejo(t)` hace, en este orden (`CLAUDE.md` §4):

  1. NFC
  2. saca `’`, `'`, guiones y espacios
  3. baja a minúscula
  4. lleva `ṁ` (U+1E41) a `ṃ` (U+1E43)

Los pasos 3 y 4 no están en el `cotejo()` de `derivar_secuencias.py` y salieron
de casos reales: Thitzana cita sus ejemplos con mayúscula inicial, y un piloto
de transcripción del tomo II venía con `ṁ` mientras el resto del proyecto usa
`ṃ`. El DPD y el Abhidhān vienen los dos en NFC y con la niggahīta de punto
abajo: el problema del punto arriba está en los PDF.

El paso 4 va **después** de bajar a minúscula a propósito, para que `Ṁ`
(U+1E40) llegue a `ṁ` y de ahí a `ṃ` sin necesitar una regla aparte.

Este módulo es nuestro. No toca ningún archivo del Venerable.
"""

import re
import sys
import unicodedata

APOSTROFOS = "’'"                 # ’  '
GUIONES = "-‐‑‒–—−"
BORRAR = {ord(c): None for c in APOSTROFOS + GUIONES}

NIGGAHITA = {0x1E41: "ṃ"}              # ṁ → ṃ


def cotejo(t):
    """Forma canónica para comparar. No sirve para guardar ni para mostrar."""
    t = unicodedata.normalize("NFC", t)
    t = t.translate(BORRAR)
    t = re.sub(r"\s+", "", t)
    t = t.lower()
    return t.translate(NIGGAHITA)


def iguales(a, b):
    return cotejo(a) == cotejo(b)


# ── Medición ────────────────────────────────────────────────────────────
# El módulo se mide contra el banco cada vez que se corre: cuántas formas
# toca, y sobre todo si funde dos que hoy están separadas. Fundir dos formas
# distintas sería peor que no normalizar nada.

def medir(formas, etiqueta):
    from collections import Counter, defaultdict
    tocadas = [f for f in formas if cotejo(f) != f]
    solo_nfc = [f for f in formas
                if unicodedata.normalize("NFC", f) != f]
    mayus = [f for f in formas if f != f.lower()]
    punto_arriba = [f for f in formas if "ṁ" in f or "Ṁ" in f]

    grupos = defaultdict(set)
    for f in formas:
        grupos[cotejo(f)].add(f)
    fusiones = {k: v for k, v in grupos.items() if len(v) > 1}

    print("  {0}: {1} formas".format(etiqueta, len(formas)))
    print("     ya en NFC: {0}   ·   con mayúscula: {1}   ·   con ṁ de punto arriba: {2}"
          .format(len(formas) - len(solo_nfc), len(mayus), len(punto_arriba)))
    print("     las cambia cotejo(): {0}".format(len(tocadas)))
    print("     formas distintas que quedan fundidas: {0}".format(len(fusiones)))
    for k, v in sorted(fusiones.items())[:12]:
        print("        {0}  ←  {1}".format(k, "  ·  ".join(sorted(v))))
    return len(fusiones)


def main():
    import json
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from rutas import ruta
    reglas = ruta("recursos", "sandhi", "reglas.json")
    notas = ruta("recursos", "sandhi", "notas-combinacion-eufonica.json")

    print("COTEJO() MEDIDO SOBRE EL BANCO\n")
    fus = 0
    if os.path.exists(reglas):
        d = json.load(open(reglas, encoding="utf-8"))
        fus += medir([c["f"] for c in d["ce"]], "reglas.json · formas atestiguadas")
        fus += medir([c["comp"] for c in d["ce"]], "reglas.json · componentes")
        pasos = [p for c in d["ce"] for p in c["s"]]
        fus += medir(pasos, "reglas.json · pasos de las secuencias")
    if os.path.exists(notas):
        d = json.load(open(notas, encoding="utf-8"))
        f = [x["f"] for e in d["enunciados"] for x in e.get("formas", [])]
        if f:
            fus += medir(f, "notas · formas de interdicción")

    print("\n  Casos de la documentación:")
    for a, b in [("Sabbaṁ", "sabbaṃ"), ("yass’ indriyāni", "yassindriyāni"),
                 ("yatha-y-idaṃ", "yathayidaṃ"), ("Gotama", "gotama"),
                 ("cattāro ’me", "cattārome")]:
        print("     {0!r:24} = {1!r:20} → {2}".format(a, b, iguales(a, b)))

    print("\n  Y lo que NO debe fundir:")
    for a, b in [("lokaggo", "loka aggo"), ("esa attho", "eso attho"),
                 ("atīritaṃ", "atiritaṃ")]:
        print("     {0!r:24} = {1!r:20} → {2}".format(a, b, iguales(a, b)))

    return 1 if fus else 0


if __name__ == "__main__":
    sys.exit(main())
