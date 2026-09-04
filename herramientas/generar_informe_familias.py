#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
El informe de las familias que siguen en «no sabe», para firmar patrones
en tanda (mapa de la sesión 32, punto 3; lo pidió IEBH el 2026-08-28).

    python3 herramientas/generar_informe_familias.py               # top 5000
    python3 herramientas/generar_informe_familias.py --n 8000
    FAMILIAS_CACHE=/tmp/familias.json python3 herramientas/generar_informe_familias.py

Recorre las formas del canon por frecuencia descendente (las --n más
frecuentes) EN EL MODO DE LA PÁGINA (solo-canon + dpd-filtro) y aparta las
que la señal marca («segura» o «posible») pero ninguna autoridad afirma:
ni banco firmado, ni caso adjudicado, ni patrón. Ante el lector, ésas son
«el motor no sabe cuál es».

Cada forma se asigna a la familia de la SEGUNDA VOZ de sus lecturas
verificadas de dos componentes (una forma puede caer en varias familias);
las familias se ordenan por MASA en el canon (suma de frecuencias de sus
formas). Para cada familia se simula qué haría el mecanismo vigente de los
patrones —la base única atestiguada— si IEBH firmara esa segunda voz:

  · «única»   — exactamente una base atestiguada: el patrón la afirmaría.
  · «única ⚠» — única, pero la base es MENOS frecuente que la forma entera:
                la firma del defecto de pajānāti (base residual que concede
                la unicidad; pajāna 1 aparición contra pajānāti 2.814). Si
                se firma la familia sin resguardo de frecuencia, estas
                formas se afirmarían igual que se afirmó pajānāti.
  · «n bases» — varias bases atestiguadas: el patrón callaría (la unicidad
                es la licencia).

El informe PREPARA; no adjudica nada. La regla la firma IEBH, con grado y
resguardo si lo decide, y se incorpora a `casos-reportados.json` (patrones).

Salida: docs/solucionador/familias-no-sabe.md
La caché (FAMILIAS_CACHE) es de cómputo, no de datos: borrarla sólo cuesta
tiempo. Bustearla cuando cambie la señal.
"""

import argparse
import collections
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "nuestro"))
from normalizar import cotejo                                      # noqa: E402
import solucionar_sandhis as S                                     # noqa: E402

DESTINO = os.path.join(RAIZ, "docs", "solucionador", "familias-no-sabe.md")


def analizar_forma(f, frec):
    """Lo que el informe necesita de una forma: señal, autoridad, y por
    cada segunda voz candidata las bases atestiguadas. Serializable, para
    la caché."""
    try:
        r = S.solucionar(f)
    except Exception:                                              # noqa: BLE001
        return None
    if not r.get("senal"):
        return None
    lect = r.get("lecturas") or []
    if not lect:
        return None
    l0 = lect[0]
    autoridad = bool(l0.get("adjudicada") or l0.get("patron")
                     or l0.get("procedencia") == "firmada"
                     or l0.get("origen"))
    if autoridad:
        return None
    familias = {}
    for l in lect:
        comp = [cotejo(x) for x in (l.get("componentes") or [])]
        if len(comp) != 2:
            continue
        base, seg = comp
        # Las dos voces deben estar atestiguadas en el canon: una segunda
        # voz no atestiguada («aca», «añca») no es familia firmable — las
        # cuentas de la propia edición arbitran, como en toda la señal.
        if frec.get(base, 0) and frec.get(seg, 0):
            familias.setdefault(seg, set()).add(base)
    if not familias:
        return None
    return {"senal": r["senal"], "n_lecturas": len(lect),
            "familias": {k: sorted(v) for k, v in familias.items()}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5000,
                    help="cuántas formas del canon, por frecuencia")
    ap.add_argument("--top-formas", type=int, default=15,
                    help="cuántas formas se listan por familia")
    ap.add_argument("--min-masa", type=int, default=200,
                    help="masa mínima para que una familia salga en detalle")
    ap.add_argument("--min-seg", type=int, default=100,
                    help="apariciones mínimas de la segunda voz para que "
                         "sea familia — una segunda de 1 aparición es la "
                         "misma base residual del defecto de pajānāti, "
                         "vista del otro lado")
    a = ap.parse_args()

    S.SOLO_CANON = True
    S.DPD_FILTRO = True
    c = S.cargar()
    frec = c["frecuencia"]

    cache_path = os.environ.get("FAMILIAS_CACHE")
    cache = {}
    if cache_path and os.path.exists(cache_path):
        cache = json.load(open(cache_path, encoding="utf-8"))

    formas = sorted(frec.items(), key=lambda x: (-x[1], x[0]))[:a.n]
    nuevos = 0
    filas = []                     # (forma, n, info)
    for f, n in formas:
        if f in c["banco"] or f in c["casos"]:
            continue
        if f not in cache:
            cache[f] = analizar_forma(f, frec)
            nuevos += 1
            if cache_path and nuevos % 200 == 0:
                json.dump(cache, open(cache_path, "w", encoding="utf-8"),
                          ensure_ascii=False)
        info = cache[f]
        if info:
            filas.append((f, n, info))
    if cache_path:
        json.dump(cache, open(cache_path, "w", encoding="utf-8"),
                  ensure_ascii=False)

    # ── agrupar por segunda voz ─────────────────────────────────────────
    fam = collections.defaultdict(list)     # seg -> [(forma, n, bases)]
    for f, n, info in filas:
        for seg, bases in info["familias"].items():
            if frec.get(seg, 0) < a.min_seg:
                continue
            fam[seg].append((f, n, bases))

    def masa(seg):
        return sum(n for _, n, _ in fam[seg])

    orden = sorted(fam, key=lambda s: -masa(s))

    def clasificar(f, n, bases):
        if len(bases) == 1:
            b = bases[0]
            if frec.get(b, 0) < n:
                return "única ⚠", b
            return "única", b
        return "{0} bases".format(len(bases)), None

    def num(x):
        return "{0:,}".format(x).replace(",", ".")

    out = []
    w = out.append
    w("# Las familias que siguen en «no sabe», por segunda voz candidata\n")
    w("*Generado por `herramientas/generar_informe_familias.py` — modo de la "
      "página (solo-canon + dpd-filtro), las {0} formas más frecuentes del "
      "canon; banco, casos y patrones vigentes descontados. Este informe "
      "PREPARA la firma de los próximos patrones; no adjudica nada: la regla, "
      "su grado y su resguardo los firma IEBH.*\n".format(num(a.n)))
    w("**Cómo leerlo.** Cada familia es una segunda voz candidata; su masa es "
      "la suma de frecuencias en el canon de las formas marcadas que ninguna "
      "autoridad afirma. «única» = el mecanismo vigente (base única "
      "atestiguada) la afirmaría con solo firmar la familia; «única ⚠» = la "
      "afirmaría, pero la base es menos frecuente que la forma entera — la "
      "firma del defecto de pajānāti—; «n bases» = el patrón callaría. Si una "
      "familia trae muchas ⚠, conviene firmarla CON el resguardo de "
      "frecuencia (base ≥ forma), que está medido y espera decisión. Las "
      "segundas voces con menos de {0} apariciones propias no forman "
      "familia aquí: una segunda de 1 aparición es la misma base residual "
      "del defecto de pajānāti, vista del otro lado (--min-seg las "
      "recupera).\n".format(num(a.min_seg)))

    # ── resumen ─────────────────────────────────────────────────────────
    w("## Resumen, por masa en el canon\n")
    w("| familia (2.ª voz, con sus apariciones) | formas | masa | única | única ⚠ | varias bases |")
    w("| --- | ---: | ---: | ---: | ---: | ---: |")
    for seg in orden:
        if masa(seg) < a.min_masa:
            continue
        unica = riesgo = varias = 0
        for f, n, bases in fam[seg]:
            k, _ = clasificar(f, n, bases)
            if k == "única":
                unica += 1
            elif k == "única ⚠":
                riesgo += 1
            else:
                varias += 1
        w("| {0} ({1}) | {2} | {3} | {4} | {5} | {6} |".format(
            seg, num(frec.get(seg, 0)), len(fam[seg]), num(masa(seg)),
            unica, riesgo, varias))
    w("")

    # ── detalle ─────────────────────────────────────────────────────────
    w("## Detalle, familia por familia\n")
    for seg in orden:
        if masa(seg) < a.min_masa:
            continue
        w("### «{0}» ({1} apariciones propias) — masa {2} · {3} formas\n".format(
            seg, num(frec.get(seg, 0)), num(masa(seg)), len(fam[seg])))
        w("| forma | frec. | lectura candidata | bases atestiguadas | veredicto del mecanismo |")
        w("| --- | ---: | --- | --- | --- |")
        top = sorted(fam[seg], key=lambda x: -x[1])[:a.top_formas]
        for f, n, bases in top:
            k, b = clasificar(f, n, bases)
            if b is not None:
                lectura = "{0} + {1}".format(b, seg)
                col_b = "{0} ({1})".format(b, num(frec.get(b, 0)))
            else:
                lectura = "¿? + " + seg
                col_b = ", ".join("{0} ({1})".format(x, num(frec.get(x, 0)))
                                  for x in bases[:6])
                if len(bases) > 6:
                    col_b += ", …"
            w("| {0} | {1} | {2} | {3} | {4} |".format(
                f, num(n), lectura, col_b, k))
        w("")

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    with open(DESTINO, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    print("familias:", len([s for s in orden if masa(s) >= a.min_masa]),
          "· formas no-sabe:", len(filas),
          "· escrito", DESTINO)


if __name__ == "__main__":
    main()
