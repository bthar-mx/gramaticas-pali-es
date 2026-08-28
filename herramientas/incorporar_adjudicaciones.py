#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Incorpora los veredictos de un lote de adjudicación a
`recursos/solucionador/casos-reportados.json`.

    python3 herramientas/incorporar_adjudicaciones.py docs/solucionador/por-adjudicar-lote-1.md
    python3 herramientas/incorporar_adjudicaciones.py ... --fuente "Angel, 2026-08-29 · lote 1"

Lee las líneas `VEREDICTO:` del lote. Acepta: una letra (`a`, `b`…) que
señala la lectura listada; `no` (no es sandhi); `compuesto` (fuera del
encargo, se registra como no-sandhi con nota); o componentes explícitos
(`tena + upasaṅkami`). Lo vacío se salta. No borra ni reescribe casos ya
adjudicados: si una forma ya está, avisa y no la toca — cambiar una
adjudicación es una decisión que se toma en el archivo de casos, a mano y
con nota.

Después de incorporar: regenerar la página y correr el arnés de casos.
"""

import argparse
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "nuestro"))
from normalizar import cotejo                                      # noqa: E402

CASOS = os.path.join(RAIZ, "recursos", "solucionador",
                     "casos-reportados.json")

RE_FORMA = re.compile(r"^## \d+\.\s+(\S+)\s+·")
RE_LECTURA = re.compile(r"^- \*\*([a-j])\)\*\*\s+(.+?)(?:\s+\(§[^)]*\))?\s+—")
RE_VEREDICTO = re.compile(r"^VEREDICTO:\s*(.*)$")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lote")
    ap.add_argument("--fuente", default=None)
    a = ap.parse_args()

    fuente = a.fuente or "Angel · " + os.path.basename(a.lote)
    d = json.load(open(CASOS, encoding="utf-8"))
    existentes = {cotejo(c["forma"]) for c in d["casos"]}

    forma, lecturas = None, {}
    nuevos, saltados, avisos = [], 0, []
    for linea in open(a.lote, encoding="utf-8"):
        m = RE_FORMA.match(linea)
        if m:
            forma, lecturas = m.group(1), {}
            continue
        m = RE_LECTURA.match(linea)
        if m and forma:
            lecturas[m.group(1)] = m.group(2).strip()
            continue
        m = RE_VEREDICTO.match(linea)
        if not (m and forma):
            continue
        v = m.group(1).strip()
        if not v:
            saltados += 1
            continue
        if cotejo(forma) in existentes:
            avisos.append("ya adjudicada, no se toca: " + forma)
            continue
        caso = {"forma": forma, "fuente": fuente}
        bajo = v.lower()
        if bajo in ("no", "no sandhi", "no-sandhi"):
            caso["sandhi"] = False
        elif bajo == "compuesto":
            caso["sandhi"] = False
            caso["nota"] = "Compuesto: fuera del encargo por instrucción del Venerable."
        elif len(bajo) == 1 and bajo in lecturas:
            caso["sandhi"] = True
            caso["componentes"] = lecturas[bajo]
        elif "+" in v:
            caso["sandhi"] = True
            caso["componentes"] = " + ".join(
                x.strip() for x in v.split("+"))
        else:
            avisos.append("veredicto ilegible en {0}: {1!r}".format(forma, v))
            continue
        nuevos.append(caso)
        existentes.add(cotejo(forma))

    d["casos"].extend(nuevos)
    json.dump(d, open(CASOS, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("{0} casos incorporados · {1} en blanco · total {2}".format(
        len(nuevos), saltados, len(d["casos"])))
    for x in avisos:
        print("  aviso — " + x)
    if nuevos:
        print("\nAhora:  python3 herramientas/generar_solucionador.py"
              "\n        node nuestro/js/arnes_casos.js")
    return 0


if __name__ == "__main__":
    sys.exit(main())
