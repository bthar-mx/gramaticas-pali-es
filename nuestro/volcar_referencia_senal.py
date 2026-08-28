#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vuelca la referencia de la señal de detección en modo solo-canon, para el
porte a JS (etapa 3, briefing sesión 30 §6).

    python3 nuestro/volcar_referencia_senal.py

Para cada forma ÚNICA de los dos corpus de `Sandhi` (versos y comentario)
guarda la señal que devuelve `solucionar()` —«segura», «posible» o nada— y
su motivo, palabra por palabra. El arnés de Node compara contra esto.
Generado, no fuente; nunca se edita a mano.
"""

import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import solucionar_sandhis as S                                     # noqa: E402
import medir_contra_corpus as M                                    # noqa: E402


def main():
    S.SOLO_CANON = True
    formas = []
    vistas = set()
    for archivo in (M.VERSOS, M.COMENT):
        d = json.load(open(archivo, encoding="utf-8"))
        for w in d["palabras"]:
            if w["forma"] not in vistas:
                vistas.add(w["forma"])
                formas.append(w["forma"])

    filas = []
    cuenta = {"segura": 0, "posible": 0, None: 0}
    for voz in formas:
        try:
            r = S.solucionar(voz)
            s, m = r.get("senal"), r.get("senal_motivo")
        except Exception as e:                                     # noqa: BLE001
            s, m = None, "ERROR {0}".format(e)
        filas.append({"forma": voz, "senal": s, "motivo": m})
        cuenta[s if s in ("segura", "posible") else None] += 1

    destino = os.path.join(AQUI, "js", "referencia-senal-solo-canon.json")
    json.dump({"formas": len(filas),
               "segura": cuenta["segura"], "posible": cuenta["posible"],
               "filas": filas},
              open(destino, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("{0} formas únicas · segura {1} · posible {2} · escrito {3}".format(
        len(filas), cuenta["segura"], cuenta["posible"], destino))
    return 0


if __name__ == "__main__":
    sys.exit(main())
