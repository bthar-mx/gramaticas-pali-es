#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deriva la secuencia de formación de las formas del documento de Nandisena.

    python3 herramientas/derivar_secuencias.py            # sólo informa
    python3 herramientas/derivar_secuencias.py --escribir # además guarda

El documento da componentes, resultado y referencia, pero no los pasos. Los
pasos se calculan aquí siguiendo, para cada aforismo, el patrón de las
secuencias ya traducidas y revisadas en kaccayana/01-sandhi-kappa.md:

    §12   yassa indriyāni · yass a indriyāni (§10) · yass indriyāni (§12)
          · yassindriyāni (§11) · yass’ indriyāni (EM)
    §13   cattāro ime · cattār o ime (§10) · cattār o me (§13)
          · cattārome (§11) · cattāro ’me (EM)

La regla de oro: una secuencia sólo se emite si, al aplicarla, se llega
exactamente a la forma que Nandisena da como atestiguada. Si no coincide, no
se emite nada y la forma queda listada para revisión humana. Nunca se publica
un paso que no haya pasado esa comprobación.
"""

import argparse
import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGLAS = os.path.join(RAIZ, "recursos", "sandhi", "reglas.json")

VOCALES = "aāiīuūeo"
LARGA = {"a": "ā", "i": "ī", "u": "ū", "e": "e", "o": "o"}
CORTA = {"ā": "a", "ī": "i", "ū": "u"}


def nfc(t):
    return unicodedata.normalize("NFC", t)


def cotejo(t):
    """Forma canónica para comparar con lo atestiguado."""
    t = nfc(t).replace("’", "").replace("'", "").replace("-", "")
    return re.sub(r'\s+', '', t)


def dos_voces(comp):
    partes = [x for x in re.split(r'\s*\+\s*|\s+', comp.strip()) if x]
    return partes if len(partes) == 2 else None


def cierre(pasos, unido, atestiguada):
    """Añade el paso §11 y, si procede, el de la edición moderna."""
    pasos.append("{0} (§11)".format(unido))
    if cotejo(unido) != cotejo(atestiguada):
        return None
    if nfc(atestiguada).strip() != nfc(unido).strip():
        pasos.append("{0} (EM)".format(atestiguada))
    return pasos


# ── Un derivador por aforismo ───────────────────────────────────────────
# Cada uno reproduce el patrón de la secuencia correspondiente del capítulo.

def d_elide_anterior(a, b, atestiguada, n):
    """§12: se separa la vocal final de la primera voz y se elide."""
    if not a or a[-1] not in VOCALES:
        return None
    raiz, v = a[:-1], a[-1]
    if not raiz:
        return None
    return cierre(["{0} {1}".format(a, b),
                   "{0} {1} {2} (§10)".format(raiz, v, b),
                   "{0} {1} (§{2})".format(raiz, b, n)],
                  raiz + b, atestiguada)


CLASE_VOCAL = {"a": "a", "ā": "a", "i": "i", "ī": "i", "u": "u", "ū": "u",
               "e": "e", "o": "o"}


def _asarupa(a, b):
    """§13 es «Vā paro asarūpā»: la siguiente se elide tras vocal DISÍMIL.
    Con vocales de la misma clase (a/ā, i/ī, u/ū) manda §12 (+§15) —
    adjudicación del IEBH, 2026-08-29; la propia edición pone tadāhaṃ,
    migīva y vadhūdaraṃ bajo «una vocal que precede a otra se elide»."""
    u, v = a[-1], b[0]
    return not (u in CLASE_VOCAL and v in CLASE_VOCAL
                and CLASE_VOCAL[u] == CLASE_VOCAL[v])


def d_elide_siguiente(a, b, atestiguada, n):
    """§13: se elide la vocal inicial de la segunda voz."""
    if not a or a[-1] not in VOCALES or not b or b[0] not in VOCALES:
        return None
    if not _asarupa(a, b):
        return None
    raiz, v = a[:-1], a[-1]
    if not raiz or len(b) < 2:
        return None
    return cierre(["{0} {1}".format(a, b),
                   "{0} {1} {2} (§10)".format(raiz, v, b),
                   "{0} {1} {2} (§{3})".format(raiz, v, b[1:], n)],
                  raiz + v + b[1:], atestiguada)


def d_elide_y_alarga(a, b, atestiguada, n):
    """§15: elidida la anterior, la siguiente se alarga."""
    if not a or a[-1] not in VOCALES or not b or b[0] not in VOCALES:
        return None
    raiz, v = a[:-1], a[-1]
    if not raiz or b[0] not in LARGA:
        return None
    largo = LARGA[b[0]] + b[1:]
    return cierre(["{0} {1}".format(a, b),
                   "{0} {1} {2} (§10)".format(raiz, v, b),
                   "{0} {1} (§12)".format(raiz, b),
                   "{0} {1} (§{2})".format(raiz, largo, n)],
                  raiz + largo, atestiguada)


def d_alarga_anterior(a, b, atestiguada, n):
    """§16: elidida la siguiente, la anterior se alarga."""
    if not a or a[-1] not in VOCALES or not b or b[0] not in VOCALES:
        return None
    if not _asarupa(a, b):
        return None                    # su §13 interno pide vocal disímil
    raiz, v = a[:-1], a[-1]
    if not raiz or v not in LARGA or len(b) < 2:
        return None
    return cierre(["{0} {1}".format(a, b),
                   "{0} {1} {2} (§10)".format(raiz, v, b),
                   "{0} {1} {2} (§13)".format(raiz, v, b[1:]),
                   "{0} {1} {2} (§{3})".format(raiz, LARGA[v], b[1:], n)],
                  raiz + LARGA[v] + b[1:], atestiguada)


def d_sustituye_anterior(a, b, atestiguada, n, destino):
    """§17 (e→y), §18 (o,u→v), §21 (i,ī→y): cambia la vocal final."""
    if not a or a[-1] not in VOCALES:
        return None
    raiz, v = a[:-1], a[-1]
    if not raiz:
        return None
    return cierre(["{0} {1}".format(a, b),
                   "{0} {1} {2} (§10)".format(raiz, v, b),
                   "{0} {1} {2} (§{3})".format(raiz, destino, b, n)],
                  raiz + destino + b, atestiguada)


def d_duplica(a, b, atestiguada, n):
    """§28: se duplica la consonante inicial de la segunda voz."""
    if not b or b[0] in VOCALES:
        return None
    doble = b[0] + b
    return cierre(["{0} {1}".format(a, b),
                   "{0} {1} (§{2})".format(a, doble, n)],
                  a + doble, atestiguada)


def d_inserta(a, b, atestiguada, n, letra):
    """§35: se inserta una consonante entre las dos voces."""
    return cierre(["{0} {1}".format(a, b),
                   "{0} {1} {2} (§{3})".format(a, letra, b, n)],
                  a + letra + b, atestiguada)


def derivar(kac, comp, atestiguada):
    par = dos_voces(comp)
    if not par:
        return None
    a, b = par
    intentos = []
    if kac == 12:
        intentos.append(lambda: d_elide_anterior(a, b, atestiguada, 12))
    elif kac == 13:
        intentos.append(lambda: d_elide_siguiente(a, b, atestiguada, 13))
    elif kac == 15:
        intentos.append(lambda: d_elide_y_alarga(a, b, atestiguada, 15))
    elif kac == 16:
        intentos.append(lambda: d_alarga_anterior(a, b, atestiguada, 16))
    elif kac in (17, 18, 21):
        for destino in ("y", "v"):
            intentos.append(lambda d=destino: d_sustituye_anterior(a, b, atestiguada, kac, d))
    elif kac == 28:
        intentos.append(lambda: d_duplica(a, b, atestiguada, 28))
    elif kac == 35:
        for letra in "yvmdntrlhg":
            intentos.append(lambda x=letra: d_inserta(a, b, atestiguada, 35, x))
    for f in intentos:
        r = f()
        if r:
            return r
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--escribir", action="store_true")
    a = ap.parse_args()

    d = json.load(open(REGLAS, encoding="utf-8"))
    reglas = {(r["sec"], str(r["n"])): r for r in d["rules"]}

    hechas, fallidas, ya = 0, [], 0
    for c in d["ce"]:
        if c.get("verificada"):
            ya += 1
            continue
        r = reglas.get((c["sec"], str(c["rule"])))
        kac = r["kac"][0] if r and r["kac"] else 0
        pasos = derivar(kac, c["comp"], c["f"])
        if pasos:
            c["s"] = pasos
            c["full"] = True
            c["derivada"] = True
            c.pop("transcrito", None)
            hechas += 1
        else:
            fallidas.append((kac, c["comp"], c["f"]))

    print("formas con secuencia de tu traducción: {0}".format(ya))
    print("formas con secuencia derivada y comprobada: {0}".format(hechas))
    print("formas sin secuencia: {0}".format(len(fallidas)))

    from collections import Counter
    print("\nsin secuencia, por aforismo:")
    for k, v in Counter(x[0] for x in fallidas).most_common(12):
        print("   §{0:<5} {1:>3}".format(k, v))

    if a.escribir:
        json.dump(d, open(REGLAS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("\nEscrito {0}".format(os.path.relpath(REGLAS, RAIZ)))
    else:
        print("\n(sin escribir — usa --escribir)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
