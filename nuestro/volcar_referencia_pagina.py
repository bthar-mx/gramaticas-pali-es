#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vuelca la referencia de la PÁGINA (etapa 4, briefing sesión 30 §6): lo que
`solucionar()` devuelve, en modo solo-canon, para cada una de las 266 formas
del banco — estado, señal y todas las lecturas con sus pasos.

    python3 nuestro/volcar_referencia_pagina.py

La puerta de la etapa 4 exige que la página publicada dé secuencias
byte-idénticas al Python en las 266: `node nuestro/js/arnes_pagina.js`
evalúa el motor de la página YA GENERADA y compara contra este archivo.
Generado, no fuente; nunca se edita a mano.
"""

import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import solucionar_sandhis as S                                     # noqa: E402


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--dpd-filtro", action="store_true")
    a = ap.parse_args()
    S.SOLO_CANON = True
    S.DPD_FILTRO = a.dpd_filtro
    d = json.load(open(S.REGLAS, encoding="utf-8"))
    filas = []
    for c in d["ce"]:
        r = S.solucionar(c["f"])
        filas.append({
            "f": c["f"],
            "estado": r.get("estado"),
            "senal": r.get("senal"),
            "lecturas": [{
                "componentes": l.get("componentes"),
                "pasos": l.get("pasos"),
                "procedencia": l.get("procedencia"),
                "referencia": l.get("referencia") if l.get("referencia")
                is not None else None,
            } for l in r.get("lecturas", [])],
        })
    destino = os.path.join(AQUI, "js", "referencia-pagina-solo-canon.json")
    json.dump({"formas": len(filas), "filas": filas},
              open(destino, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("{0} formas · escrito {1}".format(len(filas), destino))
    return 0


if __name__ == "__main__":
    sys.exit(main())
