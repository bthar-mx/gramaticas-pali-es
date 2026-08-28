#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vuelca la referencia de la medida contra el corpus, para el porte a JS
(etapa 2, briefing sesión 30 §6).

    python3 nuestro/volcar_referencia_corpus.py --solo-canon
    python3 nuestro/volcar_referencia_corpus.py --solo-canon --comentario

Repite exactamente el bucle de `medir_contra_corpus.py` y guarda, por forma:
la categoría (fuera_de_alcance / acuerdo / corte / desacuerdo / silencio), el
rango en que aparece el corte de `Sandhi` entre nuestras lecturas, y las
lecturas mismas (componentes en forma de cotejo). El arnés de Node compara
contra esto, forma por forma. Generado, no fuente; nunca se edita a mano.
"""

import argparse
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from normalizar import cotejo                                      # noqa: E402
import solucionar_sandhis as S                                     # noqa: E402
import medir_contra_corpus as M                                    # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--comentario", action="store_true")
    ap.add_argument("--solo-canon", action="store_true")
    ap.add_argument("--categorias", default="sandhi")
    a = ap.parse_args()
    S.SOLO_CANON = a.solo_canon

    archivo = M.COMENT if a.comentario else M.VERSOS
    cats = set(a.categorias.split(","))
    d = json.load(open(archivo, encoding="utf-8"))
    filas = [w for w in d["palabras"] if w.get("categoria") in cats]

    out = []
    for w in filas:
        suyas = M.normalizar_piezas(w.get("piezas"))
        fila = {"forma": w["forma"]}
        if M.es_yuxtaposicion(w["forma"], suyas):
            fila["categoria"] = "fuera_de_alcance"
            out.append(fila)
            continue
        try:
            r = S.solucionar(w["forma"])
        except Exception as e:                                     # noqa: BLE001
            fila["categoria"] = "desacuerdo"
            fila["error"] = "{0}: {1}".format(type(e).__name__, e)
            out.append(fila)
            continue
        mias = M.nuestras(r)
        fila["mias"] = [list(m) for m in mias]
        if not mias:
            fila["categoria"] = "silencio"
            out.append(fila)
            continue
        hallada = None
        for i, m in enumerate(mias):
            if m in suyas:
                hallada = i + 1
                break
        if hallada:
            fila["categoria"] = "acuerdo"
            fila["rango"] = hallada
        else:
            primeras = {x[0] for x in mias if x}
            fila["categoria"] = ("corte" if any(s and s[0] in primeras
                                                for s in suyas)
                                 else "desacuerdo")
        out.append(fila)

    from collections import Counter
    cuenta = Counter(f["categoria"] for f in out)
    en_alcance = len(out) - cuenta["fuera_de_alcance"]
    coincide = cuenta["acuerdo"] + cuenta["corte"]
    nombre = ("referencia-corpus-{0}-{1}.json".format(
        "comentario" if a.comentario else "versos",
        "solo-canon" if a.solo_canon else "dpd"))
    destino = os.path.join(AQUI, "js", nombre)
    json.dump({"archivo": os.path.basename(archivo),
               "modo": "solo-canon" if a.solo_canon else "dpd",
               "medidas": len(out), "en_alcance": en_alcance,
               "coincide": coincide, "cuenta": dict(cuenta),
               "filas": out},
              open(destino, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("coincide el corte: {0} de {1} · escrito {2}".format(
        coincide, en_alcance, destino))
    return 0


if __name__ == "__main__":
    sys.exit(main())
