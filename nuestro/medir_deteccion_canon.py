#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mide los candidatos a señal de detección EN MODO SOLO-CANON (etapa 3 del
porte a JS, briefing sesión 30 §6): con el DPD apartado, ¿qué señales quedan
para decir «en esta palabra hay que detenerse»?

    python3 nuestro/medir_deteccion_canon.py
    python3 nuestro/medir_deteccion_canon.py --comentario
    python3 nuestro/medir_deteccion_canon.py --limite 500

**El problema cambió de forma al cambiar el léxico.** El DPD lista formas de
diccionario, y «no está en el DPD» delataba a la forma con sandhi. El corpus
del canon lista lo que ESTÁ ESCRITO: `lokaggo` figura, con su cuenta, porque
está impreso. Para un texto del canon esa señal se apaga casi entera, y hay
que medir qué la reemplaza.

**Lo que no se vuelve a intentar** (INFORME-AL-VENERABLE, y estaba medido en
`LA-DETECCION-medida.md`, que la entrega no trajo — defecto registrado en
PROCEDENCIA): «termina en un nipāta» (acierta 1 de 5), «once letras o más»
(1 de 4), la frecuencia a secas en un corpus grande (1 de 3). No están aquí.

**El candidato nuevo, que sólo el canon hace posible:** la forma tiene una
lectura verificada por recomposición Y sus dos piezas son más frecuentes en
el canon que la forma entera. No decide una autoridad de afuera: arbitran
las cuentas de la propia edición (8.062.163 fichas). Se mide con tres
umbrales —min(piezas) > 1·, 10· y 100· la frecuencia de la forma— para ver
dónde está el codo, y con la frecuencia de la forma unida en el numerador
porque un sandhi lexicalizado (`natthi`, `cāhaṃ`) es frecuente él mismo y el
umbral bajo lo deja pasar.

Se mide sobre el texto completo —todas las palabras, no dos montones—, que
es lo que un lector pega. Columnas como en `medir_senal.py`, más el recall:
de los sandhis del encargo, cuántos se marcan.
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

VOCALES = "aāiīuūeo"


def frecuencias():
    """Las cuentas del canon, agregadas por forma de cotejo."""
    d = json.load(open(S.CORPUS, encoding="utf-8"))
    f = collections.Counter()
    for forma, n in d["formas"].items():
        f[cotejo(forma)] += n
    return f


def grupos_iniciales_canon(frec):
    """Los grupos consonánticos iniciales atestiguados en el canon.

    El criterio es el de `grupos-iniciales.json` —§28 enuncia la duplicación
    «después de una vocal»: una consonante doble no puede abrir palabra—,
    recalculado sobre el canon en vez del DPD. Un grupo doble atestiguado en
    el corpus es artefacto o juntura, no apertura de voz: se descarta por el
    enunciado, no por la cuenta.
    """
    grupos = set()
    for forma in frec:
        i = 0
        while i < len(forma) and forma[i] not in VOCALES:
            i += 1
        g = forma[:i]
        if not g:
            continue
        if len(g) >= 2 and g[0] == g[1]:
            continue                       # §28: doble no abre palabra
        grupos.add(g)
    return grupos


def grupo_inicial(t):
    i = 0
    while i < len(t) and t[i] not in VOCALES:
        i += 1
    return t[:i]


_solucion = {}


def resultado_de(forma):
    if forma not in _solucion:
        try:
            _solucion[forma] = S.solucionar(forma)
        except Exception:                                          # noqa: BLE001
            _solucion[forma] = {"lecturas": [], "senal": None}
    return _solucion[forma]


def lecturas_de(forma):
    return resultado_de(forma).get("lecturas", [])


def medir(archivo, limite=None):
    frec = frecuencias()
    grupos = grupos_iniciales_canon(frec)

    d = json.load(open(archivo, encoding="utf-8"))
    P = d["palabras"]
    if limite:
        P = P[:limite]

    def en_alcance(w):
        return (w.get("categoria") == "sandhi"
                and not M.es_yuxtaposicion(
                    w["forma"], M.normalizar_piezas(w.get("piezas"))))

    # Los aforismos «ruidosos» para la DETECCIÓN: alargar o acortar (§25,
    # §26), duplicar (§28, §29) e insertar (§35, §37) producen lecturas
    # verificadas sobre flexiones corrientes —de `gacchā + ti` sale
    # `gacchati`—. No se les quita validez como lecturas: se mide qué pasa
    # si la SEÑAL exige además una lectura que elide o sustituye algo.
    RUIDOSOS = {25, 26, 28, 29, 35, 37, "35+26", "35nota9"}

    nip = S.cargar()["nipata"]

    def ratio_explica(forma, umbral, solo_nipata=False, solo_sustantiva=False):
        """¿Alguna lectura verificada tiene las dos piezas más frecuentes
        que la forma entera, con este margen? Con dos restricciones
        opcionales: segunda voz en la lista cerrada de nipāta, y lectura
        cuya operación no sea de las ruidosas."""
        fF = frec.get(cotejo(forma), 0)
        for l in lecturas_de(forma):
            comp = [cotejo(x) for x in l.get("componentes", [])]
            if len(comp) < 2:
                continue
            if solo_nipata and comp[-1] not in nip:
                continue
            if solo_sustantiva and l.get("sutta") in RUIDOSOS:
                continue
            if min(frec.get(c, 0) for c in comp) > umbral * fF:
                return True
        return False

    def senales(w):
        voz = w["forma"]
        c = cotejo(voz)
        fuera = not S.es_palabra(voz)
        comp_ap = S._compuesto_aparente(c)
        iti = c.endswith("ti") and len(c) > 3 and c[-3] in "āīū"
        g = grupo_inicial(c)
        r1 = ratio_explica(voz, 1)
        r10 = r1 and ratio_explica(voz, 10)
        r100 = r10 and ratio_explica(voz, 100)
        rn1 = ratio_explica(voz, 1, solo_nipata=True)
        rn10 = rn1 and ratio_explica(voz, 10, solo_nipata=True)
        rs1 = ratio_explica(voz, 1, solo_sustantiva=True)
        rs10 = rs1 and ratio_explica(voz, 10, solo_sustantiva=True)
        rns1 = ratio_explica(voz, 1, solo_nipata=True, solo_sustantiva=True)
        rns10 = rns1 and ratio_explica(voz, 10, solo_nipata=True,
                                       solo_sustantiva=True)
        base = (any(x in voz for x in "’'-") or iti or (fuera and not comp_ap))
        return collections.OrderedDict([
            ("sello ortográfico (’ - ')", any(x in voz for x in "’'-")),
            ("cola de «iti»", iti),
            ("no está en el canon", fuera),
            ("no está, y no es compuesto aparente", fuera and not comp_ap),
            ("grupo inicial no atestiguado", bool(g) and g not in grupos),
            ("lectura con piezas > 1× la forma", r1),
            ("lectura con piezas > 10× la forma", r10),
            ("lectura con piezas > 100× la forma", r100),
            ("… > 1×, 2.ª voz nipāta", rn1),
            ("… > 10×, 2.ª voz nipāta", rn10),
            ("… > 1×, operación sustantiva", rs1),
            ("… > 10×, operación sustantiva", rs10),
            ("… > 1×, nipāta y sustantiva", rns1),
            ("… > 10×, nipāta y sustantiva", rns10),
            ("BASE: sello, o iti, o fuera-no-compuesto", base),
            ("BASE, o piezas > 10× la forma", base or r10),
            ("BASE, o > 1× nipāta y sustantiva", base or rns1),
            ("BASE, o > 10× nipāta y sustantiva", base or rns10),
            # Las dos últimas filas NO se recalculan acá: salen de la señal
            # que el motor de verdad devuelve (`solucionar()["senal"]`), para
            # que el número publicado sea el de la función que se publica.
            ("LA SEÑAL DEL MOTOR: «segura»",
             resultado_de(voz).get("senal") == "segura"),
            ("LA SEÑAL DEL MOTOR: «segura» o «posible»",
             resultado_de(voz).get("senal") in ("segura", "posible")),
        ])

    reales = sum(1 for w in P if en_alcance(w))
    cuenta = collections.OrderedDict()
    for w in P:
        for k, v in senales(w).items():
            cu = cuenta.setdefault(k, collections.Counter())
            if not v:
                continue
            cu["marca"] += 1
            if en_alcance(w):
                cu["sandhi"] += 1
            elif w.get("categoria") in ("sandhi", "compuesto", "formacion",
                                        "juntura"):
                cu["estructura"] += 1
            else:
                cu["nada"] += 1

    n = len(P)
    print("\n  {0} · modo solo-canon".format(os.path.basename(archivo)))
    print("  {0} palabras · sandhis del encargo: {1} — {2:.1f} de cada 100"
          .format(n, reales, 100.0 * reales / n))
    print("  " + "-" * 86)
    print("  {0:<44}{1:>7}{2:>9}{3:>8}{4:>8}{5:>9}".format(
        "señal", "marca", "sandhi", "otra", "nada", "recall"))
    for k, cu in cuenta.items():
        m = cu["marca"]
        print("  {0:<44}{1:6.1f}%{2:8.0f}%{3:7.0f}%{4:7.0f}%{5:8.0f}%".format(
            k, 100.0 * m / n,
            100.0 * cu["sandhi"] / m if m else 0,
            100.0 * cu["estructura"] / m if m else 0,
            100.0 * cu["nada"] / m if m else 0,
            100.0 * cu["sandhi"] / reales if reales else 0))
    print("  " + "-" * 86)
    print("  «marca»: cuántas de cada cien palabras se señalan. «sandhi/otra/")
    print("  nada» reparten lo marcado. «recall»: de los sandhis del encargo,")
    print("  cuántos se marcan. Lo que no se marca no se pierde: se calla.")
    return cuenta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--comentario", action="store_true")
    ap.add_argument("--limite", type=int)
    a = ap.parse_args()
    S.SOLO_CANON = True
    medir(M.COMENT if a.comentario else M.VERSOS, a.limite)
    return 0


if __name__ == "__main__":
    S.consola_utf8()
    sys.exit(main())
