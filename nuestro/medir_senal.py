#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mide la **señal**: no si resolvemos bien, sino si sabemos *dónde mirar*.

Son dos preguntas distintas y se confundían. `medir_contra_corpus.py` pregunta
«dada una forma con sandhi, ¿la partimos donde la parte `Sandhi`?».
Ésta pregunta «dado un texto entero, ¿en qué palabras hay que detenerse?».

**Se mide sobre el texto completo, no sobre dos montones.** Una medida anterior
comparaba las formas con sandhi contra las marcadas «sin sandhi» y dejaba fuera
las 276 y 2.025 que `Sandhi` clasifica como compuesto, formación o juntura. Eso
daba 95 % de precisión. Sobre el texto entero, que es lo que un lector pega, la
precisión real es **83 % en verso y 68 % en prosa**. La diferencia son casi
todos compuestos —que sí tienen una juntura, pero están fuera del encargo—.

De cada cien palabras marcadas:

    versos       83 sandhi · 8 compuesto o formación ·  9 sin nada
    comentario   68 sandhi · 19 compuesto o formación · 12 sin nada

Es decir: **9 de cada 10 palabras marcadas tienen de verdad una juntura**, y en
8 de cada 10 esa juntura es un sandhi del encargo.

    python3 medir_senal.py
    python3 medir_senal.py --comentario
"""

import argparse
import collections
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from normalizar import cotejo                                      # noqa: E402
import solucionar_sandhis as S                                     # noqa: E402
import medir_contra_corpus as M                                    # noqa: E402


def senales(voz):
    c = cotejo(voz)
    fuera = not S.es_palabra(voz)
    iti = c.endswith("ti") and len(c) > 3 and c[-3] in "āīū"
    comp = S._compuesto_aparente(c)
    nip = S.cargar()["nipata"]
    cola_nip = any(len(n) >= 2 and c.endswith(n) and len(c) > len(n) + 2
                   for n in nip)
    return {
        "el DPD la descompone": bool(S.descomposicion(voz)),
        "no está en el DPD": fuera,
        "cola de «iti»": iti,
        "termina en un nipāta": cola_nip,
        "once letras o más": len(c) >= 11,
        "sello ortográfico (’ - ')": any(x in voz for x in "’'-"),
        "LA SEÑAL: descomposición del DPD, o no-DPD, o iti":
            bool(S.descomposicion(voz)) or (fuera and not comp) or iti,
    }


def medir(archivo):
    d = json.load(open(archivo, encoding="utf-8"))
    P = d["palabras"]

    def en_alcance(w):
        return (w.get("categoria") == "sandhi"
                and not M.es_yuxtaposicion(
                    w["forma"], M.normalizar_piezas(w.get("piezas"))))

    reales = sum(1 for w in P if en_alcance(w))
    cuenta = collections.OrderedDict()
    for w in P:
        for k, v in senales(w["forma"]).items():
            c = cuenta.setdefault(k, collections.Counter())
            if not v:
                continue
            c["marca"] += 1
            if en_alcance(w):
                c["sandhi"] += 1
            elif w.get("categoria") in ("sandhi", "compuesto", "formacion",
                                        "juntura"):
                c["estructura"] += 1
            else:
                c["nada"] += 1

    n = len(P)
    print("\n  {0}".format(os.path.basename(archivo)))
    print("  {0} palabras · sandhis del encargo: {1} — {2:.1f} de cada 100"
          .format(n, reales, 100.0 * reales / n))
    print("  " + "-" * 76)
    print("  {0:<40}{1:>8}{2:>10}{3:>9}{4:>9}".format(
        "señal", "marca", "sandhi", "otra", "nada"))
    for k, c in cuenta.items():
        m = c["marca"]
        print("  {0:<40}{1:7.1f}%{2:9.0f}%{3:8.0f}%{4:8.0f}%".format(
            k, 100.0 * m / n,
            100.0 * c["sandhi"] / m if m else 0,
            100.0 * c["estructura"] / m if m else 0,
            100.0 * c["nada"] / m if m else 0))
    print("  " + "-" * 76)
    print("  «marca» es cada cuántas palabras de cien se señala. Las otras tres")
    print("  columnas reparten lo marcado: sandhi del encargo · otra juntura")
    print("  —compuesto o formación, que están fuera— · nada.")
    print()
    print("  Lo que la señal no marca **no se pierde: se calla**. Cada voz sigue")
    print("  siendo consultable una por una, con todas sus lecturas.")
    return cuenta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--comentario", action="store_true")
    a = ap.parse_args()
    medir(M.COMENT if a.comentario else M.VERSOS)


if __name__ == "__main__":
    S.consola_utf8()
    main()
