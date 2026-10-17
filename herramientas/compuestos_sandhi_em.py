#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post-paso EM («edición moderna») de «Compuestos (samāsa)»: separa las junturas de
sandhi entre palabras en las citas pāḷi (ti, enclíticos, vocal elidida con ’),
según la tabla recursos/compuestos/sandhi-em.json.

    python3 herramientas/compuestos_sandhi_em.py [--comprobar]

Cada cambio es una sustitución exacta «antes» → «despues»:
  · texto-revisado.txt: sólo dentro de la línea con ese id (L);
  · guia.md: en todo el archivo, y «antes» ha de aparecer una sola vez
    (el número de línea de la tabla es orientativo: la guía se edita a mano).

Idempotente: si «antes» ya no está y «despues» sí, el cambio cuenta como hecho.
Si no está ninguno de los dos, falla (el texto cambió: hay que revisar la tabla).
compuestos_aplicar.py lo llama al final, porque rehace texto-revisado.txt.
--comprobar no escribe nada: sólo dice si queda algo por aplicar.
"""

import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(RAIZ, "recursos", "compuestos")
TABLA = os.path.join(DIR, "sandhi-em.json")


def nfc(s):
    return unicodedata.normalize("NFC", s)


def aplicar_texto(s, cambios):
    """s: el texto revisado entero. Devuelve (texto, hechos, ya, fallos)."""
    lineas = s.split("\n")
    pos = {}
    for i, ln in enumerate(lineas):
        m = re.match(r"^(\d{4}[a-z]*)  ", ln)
        if m:
            pos[m.group(1)] = i
    hechos, ya, fallos = 0, 0, []
    for c in cambios:
        i = pos.get(c["L"])
        if i is None:
            fallos.append("L{0}: no existe la línea".format(c["L"]))
            continue
        ln = lineas[i]
        # Si «antes» está contenido en «despues» (un añadido al final, como
        # C-031), mirar primero «despues»: si no, cada corrida lo añade otra vez.
        if c["antes"] in c["despues"] and c["despues"] in ln:
            ya += 1
        elif c["antes"] in ln:
            lineas[i] = ln.replace(c["antes"], c["despues"])
            hechos += 1
        elif c["despues"] in ln:
            ya += 1
        else:
            fallos.append("L{0}: no está «{1}»".format(c["L"], c["antes"]))
    return "\n".join(lineas), hechos, ya, fallos


def aplicar_guia(s, cambios):
    hechos, ya, fallos = 0, 0, []
    for c in cambios:
        n = s.count(c["antes"])
        if c["antes"] in c["despues"] and c["despues"] in s:
            ya += 1
        elif n == 1:
            s = s.replace(c["antes"], c["despues"])
            hechos += 1
        elif n == 0 and c["despues"] in s:
            ya += 1
        else:
            fallos.append("guía l.{0}: «{1}» aparece {2} veces".format(c["L"], c["antes"], n))
    return s, hechos, ya, fallos


def aplicar(comprobar=False, solo=None):
    """Aplica la tabla. solo: None (los dos archivos) o un nombre de archivo."""
    t = json.load(open(TABLA, encoding="utf-8"))
    total_fallos = []
    for arch, fn in (("texto-revisado.txt", aplicar_texto), ("guia.md", aplicar_guia)):
        if solo and arch != solo:
            continue
        cambios = [c for c in t["cambios"] if c["archivo"] == arch]
        ruta = os.path.join(DIR, arch)
        s = nfc(open(ruta, encoding="utf-8").read())
        nuevo, hechos, ya, fallos = fn(s, cambios)
        nuevo = nfc(nuevo)
        total_fallos += fallos
        if fallos:
            for f in fallos:
                print("  ✗ " + f)
        if comprobar:
            print("{0}: {1} por aplicar, {2} ya aplicados, {3} fallos".format(arch, hechos, ya, len(fallos)))
        elif not fallos:
            if nuevo != s:
                open(ruta, "w", encoding="utf-8").write(nuevo)
            print("→ sandhi EM en {0}: {1} aplicados, {2} ya estaban".format(arch, hechos, ya))
    if total_fallos:
        raise SystemExit("✗ sandhi EM: {0} cambio(s) no aplicable(s); revisar recursos/compuestos/sandhi-em.json"
                         .format(len(total_fallos)))
    return 0


if __name__ == "__main__":
    sys.exit(aplicar(comprobar="--comprobar" in sys.argv[1:]))
