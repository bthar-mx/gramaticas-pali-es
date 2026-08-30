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

import hashlib
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import solucionar_sandhis as S                                     # noqa: E402
import medir_contra_corpus as M                                    # noqa: E402

# Lo que, si cambia, cambia la señal de una forma. La caché guarda esta
# huella y se DESCARTA ENTERA cuando no coincide.
FUENTES_SENAL = [
    os.path.join(os.path.dirname(AQUI), "recursos", "solucionador",
                 "casos-reportados.json"),
    os.path.join(os.path.dirname(AQUI), "recursos", "sandhi", "reglas.json"),
]


def huella(dpd_filtro):
    """Huella de lo que decide la señal: los casos, los patrones y el banco.

    La caché es por VOZ y nada más, así que un caso nuevo no la invalidaba:
    «netaṃ» quedaba cacheado como «sin señal» de antes de adjudicarse, la
    referencia salía contradiciendo al motor, `arnes_deteccion` fallaba y
    `ciclo_veredictos.py` se detenía sin publicar — con los veredictos ya
    incorporados en el árbol. El síntoma era desconcertante: se enviaban
    veredictos, se recargaba duro, y la página seguía igual. (Diagnosticado
    el 2026-08-29 sobre doce casos del Mahāpadāna que no llegaban a
    publicarse.)
    """
    h = hashlib.sha256()
    h.update(b"1|dpd_filtro=" + (b"1" if dpd_filtro else b"0"))
    for p in FUENTES_SENAL:
        h.update(b"|" + os.path.basename(p).encode())
        if os.path.exists(p):
            with open(p, "rb") as f:
                h.update(hashlib.sha256(f.read()).digest())
    return h.hexdigest()


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--dpd-filtro", action="store_true")
    a = ap.parse_args()
    S.SOLO_CANON = True
    S.DPD_FILTRO = a.dpd_filtro
    # caché reanudable: con el testigo del DPD el léxico crece y la pasada
    # supera el tope de tiempo del sandbox; se retoma donde quedó.
    cache_path = os.environ.get("SENAL_CACHE")
    hue = huella(a.dpd_filtro)
    cache = {}
    if cache_path and os.path.exists(cache_path):
        try:
            guardada = json.load(open(cache_path, encoding="utf-8"))
        except ValueError:
            guardada = {}
        if guardada.get("_huella") == hue:
            cache = guardada.get("senales") or {}
        else:
            print("  caché descartada: cambió lo que decide la señal "
                  "(casos, patrones o banco). Esta pasada es la lenta.")
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
    nuevos = 0
    for voz in formas:
        if voz in cache:
            s, m = cache[voz]
        else:
            try:
                r = S.solucionar(voz)
                s, m = r.get("senal"), r.get("senal_motivo")
            except Exception as e:                                 # noqa: BLE001
                s, m = None, "ERROR {0}".format(e)
            cache[voz] = [s, m]
            nuevos += 1
            if cache_path and nuevos % 300 == 0:
                json.dump({"_huella": hue, "senales": cache},
                          open(cache_path, "w", encoding="utf-8"),
                          ensure_ascii=False)
        filas.append({"forma": voz, "senal": s, "motivo": m})
        cuenta[s if s in ("segura", "posible") else None] += 1

    # La caché completa, al final: si la pasada terminó, lo cacheado vale
    # para la huella con la que se calculó, y sólo para ésa.
    if cache_path:
        json.dump({"_huella": hue, "senales": cache},
                  open(cache_path, "w", encoding="utf-8"), ensure_ascii=False)

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
