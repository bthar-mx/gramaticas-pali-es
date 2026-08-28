#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qué hace cada aforismo, en una línea, para poder mostrarlo al lado del paso.

Una pantalla que da el corte sin decir qué hace cada regla obliga a creerle.
Con la operación al lado, el lector verifica. Es la diferencia entre una
herramienta de consulta y una de estudio *(`CLAUDE.md` §9)*.

**Las glosas no se inventan: salen del banco.** El texto de cada una es el
enunciado de la regla del documento del Venerable que cita ese aforismo,
recortado. Los dos que el documento no enuncia porque son el andamiaje —§10 y
§11— salen del `CLAUDE.md` §5, que a su vez cita a Thitzana.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rutas import ruta                                              # noqa: E402

# El andamiaje. Thitzana los llama «two important fundamental procedures of the
# morphology» (impresa 125).
ANDAMIAJE = {
    10: "separa la consonante final sin vocal de la voz anterior",
    11: "vuelve a unir",
}

CORTES = (". ", "; ", ", y ", " respectivamente")


def _recortar(t, n=104):
    t = t.strip().rstrip(".")
    for c in CORTES:
        if c in t and len(t) > n:
            t = t.split(c)[0]
    t = t.replace("A veces, ", "").replace("A veces ", "")
    t = t.replace("En algunos casos, ", "")
    if len(t) <= n:
        return t
    # Cortar en el espacio, no a mitad de palabra: «se convierte en en la úl…»
    # quedaba feo y además escondía que el «en en» es del original —está así en
    # `reglas.json`, niggahīta 1, y es una errata más para el Venerable—.
    corte = t.rfind(" ", 0, n)
    return t[:corte if corte > n // 2 else n].rstrip(",;: ") + "…"


def cargar():
    d = json.load(open(ruta("recursos", "sandhi", "reglas.json"), encoding="utf-8"))
    g = dict(ANDAMIAJE)
    # Se recorre dos veces: primero las reglas donde el aforismo es el
    # principal —el primero de su lista—, después el resto. Si no, §28 se
    # queda con el enunciado de §19, que lo nombra de paso.
    for principal in (True, False):
        for r in d["rules"]:
            for i, k in enumerate(r["kac"]):
                if (i == 0) != principal or k in g:
                    continue
                g[k] = _recortar(r["rule"])
    return g


GLOSAS = None


def glosa(n):
    global GLOSAS
    if GLOSAS is None:
        GLOSAS = cargar()
    return GLOSAS.get(n)


if __name__ == "__main__":
    g = cargar()
    print("{0} aforismos con glosa\n".format(len(g)))
    for k in sorted(g):
        print("  §{0:<5} {1}".format(k, g[k]))
