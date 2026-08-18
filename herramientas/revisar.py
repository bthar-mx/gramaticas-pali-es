#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Revisa el markdown de un capítulo antes de generar el HTML.

    python3 herramientas/revisar.py kaccayana/02-nama-kappa.md
    python3 herramientas/revisar.py kaccayana/02-nama-kappa.md --desde 52 --hasta 76

Pensado para pasarlo después de convertir cada kaṇḍa, no sólo al final del
capítulo: los problemas de conversión son mucho más fáciles de resolver
mientras los suttas están recientes.

Distingue ERRORES (rompen la generación o el texto) de AVISOS (conviene
mirarlos, pero pueden ser correctos). Devuelve código de salida 1 si hay
errores, 0 si no.
"""

import argparse
import os
import re
import sys
import unicodedata
from collections import Counter

# El número de Rūpasiddhi puede ser doble: «271. 88, 308.» (§271 del Kāraka).
RE_SUTTA = re.compile(
    r'^\*\*(\d+)\\?\.\s*(\d+(?:,\s*\d+)*)\\?\.\s*(.+?)\*\*\s*(.*)$')
RE_KANDA = re.compile(r'^\*\*[A-ZĀĪŪṂṆṬḌÑṄḶ]+-KAṆḌA\*\*')
RE_FN_DEF = re.compile(r'^\[\^(\d+)\]:')
RE_CIERRE = re.compile(r'^\*\*Iti\s+.+?kaṇḍo\.?\*\*$')
# Abreviaturas de otras obras: Rū. §49, Sad. §139, Bā. §41, Mo. §12
RE_OTRA_OBRA = re.compile(r'[A-ZĀĪŪÑṄ][a-zāīūṃṇṭḍñṅḷ]{0,4}\.\s*$')

errores, avisos = [], []


def fragmento(linea, marca, margen=22):
    """Trozo de línea alrededor de la primera aparición de `marca`."""
    k = linea.find(marca)
    if k < 0:
        return linea.strip()[:50]
    a, b = max(0, k - margen), min(len(linea), k + margen)
    return ("…" if a else "") + linea[a:b].strip() + ("…" if b < len(linea) else "")


def err(linea, msg):
    errores.append((linea, msg))


def avi(linea, msg):
    avisos.append((linea, msg))


def revisar(path, desde=None, hasta=None):
    crudo = open(path, encoding="utf-8").read()
    lineas = crudo.split("\n")

    # ── Unicode ─────────────────────────────────────────────────────────
    if unicodedata.normalize("NFC", crudo) != crudo:
        err(0, "El archivo no está en Unicode NFC. Los diacríticos pueden "
               "verse bien y aun así no coincidir en búsquedas ni anclas.")

    # Apóstrofos. ‘a’ entrecomillando letras o sílabas es correcto según la
    # guía de estilo; sólo se avisa de las comillas de apertura sin cierre.
    for i, l in enumerate(lineas, start=1):
        if "'" in l:
            avi(i, "Apóstrofo recto ('): en el texto pāḷi el apóstrofo de "
                   "elisión es ’ — «{0}»".format(fragmento(l, "'")))
        for m in re.finditer(r'‘', l):
            if "’" not in l[m.end():m.end() + 14]:
                avi(i, "Comilla ‘ sin cierre cercano — «{0}»".format(
                    fragmento(l, "‘")))

    # ── Suttas ──────────────────────────────────────────────────────────
    suttas, kandas, cierres = [], 0, 0
    fin = next((i for i, l in enumerate(lineas) if RE_FN_DEF.match(l)), len(lineas))

    for i, l in enumerate(lineas[:fin], start=1):
        if RE_KANDA.match(l):
            kandas += 1
        if RE_CIERRE.match(l.strip()):
            cierres += 1
        m = RE_SUTTA.match(l)
        if not m:
            continue
        n, rup, pali, resto = int(m.group(1)), m.group(2), m.group(3), m.group(4)
        if desde and n < desde:
            continue
        if hasta and n > hasta:
            continue
        suttas.append((n, i))

        if "{" in l:
            err(i, "§{0}: hay una glosa emergente {{…|…}} en la línea de "
                   "cabecera. El título pāḷi se reutiliza en el índice y en "
                   "las pastillas, donde no cabe.".format(n))

        md = re.search(r'\\?\[(.+?),\s*(\d+)\\?\]', resto)
        if not md:
            avi(i, "§{0}: sin desglose [A + B, n] tras el título.".format(n))
        else:
            partes = [x for x in re.split(r'\\?\+', md.group(1)) if x.strip()]
            voces = int(md.group(2))
            if len(partes) != voces:
                avi(i, "§{0}: el desglose tiene {1} elemento(s) pero declara "
                       "{2} voces.".format(n, len(partes), voces))

        # bloques del sutta
        j = i
        while j < fin and not RE_SUTTA.match(lineas[j]) and not RE_KANDA.match(lineas[j]):
            j += 1
        cuerpo = lineas[i:j]
        seps = sum(1 for x in cuerpo if x.strip() == "---")
        if seps == 0:
            err(i, "§{0}: no hay ningún separador ---. Sin él no se puede "
                   "distinguir el pāḷi de la traducción.".format(n))
        elif seps == 1:
            avi(i, "§{0}: un solo separador ---; el sutta no tendrá glosa "
                   "o no tendrá vutti.".format(n))

    if not suttas:
        err(0, "No se ha reconocido ningún sutta. ¿El formato de cabecera es "
               "**N. M. Texto pāḷi (S).** ?")
        return

    nums = [n for n, _ in suttas]
    rep = [n for n, c in Counter(nums).items() if c > 1]
    for n in sorted(rep):
        err(0, "§{0} aparece {1} veces.".format(n, Counter(nums)[n]))

    faltan = [n for n in range(min(nums), max(nums) + 1) if n not in nums]
    if faltan:
        err(0, "Faltan suttas en la secuencia {0}–{1}: {2}".format(
            min(nums), max(nums),
            ", ".join("§{0}".format(x) for x in faltan[:20])
            + (" …" if len(faltan) > 20 else "")))

    if nums != sorted(nums):
        desorden = [nums[k] for k in range(1, len(nums)) if nums[k] < nums[k - 1]]
        err(0, "Los suttas no están en orden creciente; primero descolocado: "
               "§{0}".format(desorden[0]))

    if kandas and cierres != kandas:
        avi(0, "Hay {0} apertura(s) de kaṇḍa y {1} fórmula(s) de cierre "
               "«Iti … kaṇḍo».".format(kandas, cierres))

    # ── Notas al pie ────────────────────────────────────────────────────
    definidas = {m.group(1) for m in (RE_FN_DEF.match(l) for l in lineas) if m}
    usadas = Counter(re.findall(r'\[\^(\d+)\](?!:)', crudo))
    sin_def = sorted(set(usadas) - definidas, key=int)
    if sin_def:
        err(0, "Marcador(es) de nota sin definición: {0}".format(
            ", ".join("[^{0}]".format(x) for x in sin_def)))
    sin_uso = sorted(definidas - set(usadas), key=int)
    if sin_uso:
        avi(0, "Nota(s) definida(s) pero nunca citada(s): {0}".format(
            ", ".join("[^{0}]".format(x) for x in sin_uso)))
    for k, v in sorted(usadas.items(), key=lambda x: int(x[0])):
        if v > 1:
            avi(0, "La nota [^{0}] se cita {1} veces.".format(k, v))

    # ── Referencias §N ──────────────────────────────────────────────────
    validos = set(nums)
    fuera, otras = set(), set()
    for i, l in enumerate(lineas, start=1):
        for m in re.finditer(r'§(\d+)', l):
            previo = l[max(0, m.start() - 8):m.start()]
            if RE_OTRA_OBRA.search(previo):
                otras.add(m.group(0))
            elif int(m.group(1)) not in validos:
                fuera.add((int(m.group(1)), i))
    if fuera:
        avi(0, "Referencia(s) §N a suttas que no están en este archivo "
               "(normales si remiten a otro capítulo): {0}".format(
                   ", ".join("§{0} (línea {1})".format(n, i)
                             for n, i in sorted(fuera)[:12])))
    if otras:
        avi(0, "Referencia(s) a otras obras que no se enlazarán: {0}".format(
            ", ".join(sorted(otras))))

    # ── Glosas emergentes ───────────────────────────────────────────────
    sueltas = re.findall(r'\{[^{}]*\}', crudo)
    malas = [x for x in sueltas if "|" not in x]
    if malas:
        err(0, "Glosa(s) emergente(s) mal formada(s) (falta |): {0}".format(
            ", ".join(malas[:6])))

    print("{0} suttas (§{1}–§{2}) · {3} kaṇḍas · {4} notas · {5} glosas".format(
        len(suttas), min(nums), max(nums), kandas, len(definidas),
        len([x for x in sueltas if "|" in x])))


def main():
    ap = argparse.ArgumentParser(add_help=True, description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("archivo")
    ap.add_argument("--desde", type=int, help="primer sutta a revisar")
    ap.add_argument("--hasta", type=int, help="último sutta a revisar")
    a = ap.parse_args()

    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta = a.archivo if os.path.isabs(a.archivo) else os.path.join(raiz, a.archivo)
    if not os.path.exists(ruta):
        print("No existe:", a.archivo)
        return 2

    revisar(ruta, a.desde, a.hasta)

    for etiqueta, lista in (("ERROR", errores), ("aviso", avisos)):
        if not lista:
            continue
        print()
        for linea, msg in lista:
            sitio = "línea {0}".format(linea) if linea else "archivo"
            print("{0}  {1}: {2}".format(etiqueta, sitio, msg))

    print()
    if errores:
        print("{0} error(es), {1} aviso(s).".format(len(errores), len(avisos)))
    elif avisos:
        print("Sin errores. {0} aviso(s) para mirar.".format(len(avisos)))
    else:
        print("Sin errores ni avisos.")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
