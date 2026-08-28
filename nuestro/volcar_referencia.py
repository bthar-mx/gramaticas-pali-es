#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vuelca la referencia del banco para el porte a JS (etapa 1, briefing sesión 30 §6).

    python3 nuestro/volcar_referencia.py            # modo DPD (no se usa hoy)
    python3 nuestro/volcar_referencia.py --solo-canon

Para cada una de las 266 formas de `reglas.json` repite exactamente lo que hace
`cobertura()` —proponer sin mirar el banco— y guarda **todas** las lecturas con
sus pasos, en el orden en que el motor las devuelve. El arnés de Node
(`nuestro/js/arnes.js`) compara su salida contra este archivo, secuencia por
secuencia: el Python es la referencia permanente y todo cambio del JS se mide
contra él.

Salida: `nuestro/js/referencia-banco-solo-canon.json` (o `-dpd` sin la opción).
No es fuente del motor: es una medición reproducible. Se regenera cuando cambie
el motor Python o el banco; nunca se edita a mano.
"""

import argparse
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import solucionar_sandhis as S                                     # noqa: E402
from normalizar import cotejo                                      # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo-canon", action="store_true")
    a = ap.parse_args()
    S.SOLO_CANON = a.solo_canon

    d = json.load(open(S.REGLAS, encoding="utf-8"))
    filas = []
    for x in d["ce"]:
        kac = x["kac"]
        comp = S.partir_componentes(x["comp"])
        escrita = x["f"].replace("’", "'").replace("'", "")
        if len(comp) > 2:
            lect = S.proponer_en_frase(escrita)
            esperados = sorted({cotejo(comp[j] + comp[j + 1])
                                for j in range(len(comp) - 1)})
        else:
            lect = (S.proponer_en_frase(escrita) if len(escrita.split()) > 1
                    else S.proponer(cotejo(x["f"])))
            esperados = [cotejo("".join(comp))]
        acierta = any(cotejo("".join(l["componentes"])) in esperados
                      for l in lect)
        filas.append({
            "f": x["f"], "comp": x["comp"], "kac": kac,
            "pakati": kac in S.PAKATI,
            "acierta": acierta,
            "esperados": esperados,
            "lecturas": [{"componentes": l["componentes"],
                          "sutta": l["sutta"],
                          "pasos": l["pasos"]} for l in lect],
        })

    medibles = [f for f in filas if not f["pakati"]]
    ok = sum(1 for f in medibles if f["acierta"])
    out = {
        "modo": "solo-canon" if a.solo_canon else "dpd",
        "total": len(filas),
        "medibles": len(medibles),
        "acierta": ok,
        "filas": filas,
    }
    nombre = ("referencia-banco-solo-canon.json" if a.solo_canon
              else "referencia-banco-dpd.json")
    destino = os.path.join(AQUI, "js", nombre)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    json.dump(out, open(destino, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("{0} de {1} medibles · escrito {2}".format(ok, len(medibles), destino))
    return 0


if __name__ == "__main__":
    sys.exit(main())
