#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
El informe de la familia de §34 con segunda voz corriente —la clase de
«idamavoca»—, para preparar su firma con medición previa (mapa de la
sesión 33, punto 1; los casos de la sesión 32 la detectaron).

    python3 herramientas/generar_informe_niggahita_m.py            # top 5000
    python3 herramientas/generar_informe_niggahita_m.py --n 8000
    NIGGAHITA_CACHE=/tmp/niggahita.json python3 herramientas/…

La operación: niggahīta → m ante vocal (§34). Hoy sólo la ven los casos
adjudicados (idamavoca, kimahaṃ…); este informe recorre las formas del
canon por frecuencia EN EL MODO DE LA PÁGINA (solo-canon + dpd-filtro) y
aparta las que tienen una lectura verificada de la clase:

    base terminada en «ṃ» + segunda voz que empieza en vocal,
    ambas atestiguadas en el canon, y la superficie es EXACTAMENTE
    base[:-1] + «m» + segunda (§34 puro, sin otra operación).

A diferencia de los patrones vigentes, la segunda voz es CORRIENTE (avoca,
ahaṃ, eva…), no una partícula fija: el mecanismo que se firme tendrá que
licenciarse por la unicidad de la LECTURA de la clase, no por la de la
base. Por cada forma se simula el veredicto COMO EN EL MECANISMO VIGENTE
(_aplicar_patron): el resguardo de la base residual FILTRA candidatas
—aquí por los DOS lados, porque las dos voces varían— y la unicidad de lo
que queda es la licencia:

  · «única»    — una sola lectura de la clase, y pasa el resguardo.
  · «única por resguardo» — quedó una sola PORQUE el resguardo descartó
                 rivales: la categoría que conviene mirar con lupa.
  · «gemelas»  — dos lecturas que sólo difieren en la cantidad de la vocal
                 inicial de la segunda (ayaṃ/āyaṃ): pedirían un desempate
                 como el breve/larga ya firmado para las bases.
  · «n lecturas» — varias pasan el resguardo: el mecanismo callaría.
  · «calla (resguardo)» — ninguna candidata lo pasa (samaye = saṃ + aye y
                 demás palabras corrientes caen aquí: es el resguardo
                 haciendo su trabajo).

El DPD entra como TESTIGO, no como autoridad: su propia descomposición de
la forma, cuando existe, se coteja con la lectura que el mecanismo
afirmaría, y el acuerdo se cuenta. Al final, las respuestas CONOCIDAS
—banco firmado y casos adjudicados de la clase— se contrastan una a una
con lo que el mecanismo habría dicho: ésa es la medición previa.

El informe PREPARA; no adjudica nada. La regla, su grado y sus resguardos
los firma IEBH. Una forma puede aparecer también en el informe de
familias por segunda voz (tameva está aquí por «taṃ + eva» y allá en la
familia «eva»): son cortes distintos del mismo «no sabe».

Salida: docs/solucionador/informe-niggahita-m.md
La caché (NIGGAHITA_CACHE) es de cómputo, no de datos: guarda señal y
pares verificados por forma. Bustearla cuando cambie la señal.
"""

import argparse
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "nuestro"))
from normalizar import cotejo                                      # noqa: E402
import solucionar_sandhis as S                                     # noqa: E402

DESTINO = os.path.join(RAIZ, "docs", "solucionador", "informe-niggahita-m.md")

VOCALES = "aāiīuūeo"
LARGA = {"a": "ā", "i": "ī", "u": "ū"}


def analizar_forma(f):
    """Señal y pares verificados de dos componentes (en cotejo), con marca
    de autoridad. Serializable, para la caché."""
    try:
        r = S.solucionar(f)
    except Exception:                                              # noqa: BLE001
        return None
    lect = r.get("lecturas") or []
    l0 = lect[0] if lect else {}
    autoridad = bool(r.get("del_banco") or l0.get("adjudicada")
                     or l0.get("patron") or l0.get("origen"))
    pares = []
    for l in lect:
        comp = [cotejo(x) for x in (l.get("componentes") or [])]
        if len(comp) == 2 and comp not in pares:
            pares.append(comp)
    return {"senal": r.get("senal"), "autoridad": autoridad, "pares": pares}


def es_de_la_clase(q, base, seg, frec):
    """¿Es (base, seg) una lectura §34 pura de la superficie `q`?"""
    return (len(base) >= 2 and base.endswith("ṃ")
            and seg[:1] in VOCALES
            and base[:-1] + "m" + seg == q
            and frec.get(base, 0) > 0 and frec.get(seg, 0) > 0)


def gemelas(cands):
    """Dos candidatas con la misma base cuyas segundas sólo difieren en la
    cantidad de la vocal inicial → la de inicial BREVE, o None."""
    if len(cands) != 2:
        return None
    (b1, s1), (b2, s2) = sorted(cands)
    if b1 == b2 and s1 and s2 and s1[1:] == s2[1:] \
            and LARGA.get(s1[:1]) == s2[:1]:
        return (b1, s1)
    return None


def veredicto(q, n, cands, frec):
    """(clave, lectura afirmada o None). Simula el mecanismo como el
    vigente: el resguardo FILTRA candidatas (no cuenta la que sea menos
    frecuente que la forma entera — aquí por los DOS lados, porque las dos
    voces varían) y la unicidad de lo que queda es la licencia."""
    piso = max(n, 1)
    ok = [(b, s) for b, s in cands
          if frec.get(b, 0) >= piso and frec.get(s, 0) >= piso]
    if not ok:
        return "calla (resguardo)", None
    g = gemelas(ok)
    if g:
        return "gemelas", g
    if len(ok) != 1:
        return "{0} lecturas".format(len(ok)), None
    if len(cands) > 1:
        return "única por resguardo", ok[0]
    return "única", ok[0]


def hay_testigo():
    """`dpd-descomposiciones.tsv` vive en la Mac del IEBH (briefing 33 §3.4)
    y no viaja con el repositorio. Sin él, el informe lo dice — no finge
    que el DPD «calla» cuando lo que pasa es que no se le preguntó."""
    return os.path.exists(S.DESCOMP)


def dpd_dice(f, afirmada):
    """El testigo: («coincide»|«difiere»|«calla», texto para la tabla)."""
    if not hay_testigo():
        return "ausente", "—"
    descs = [tuple(cotejo(x) for x in d) for d in S.descomposicion(f)
             if len(d) == 2]
    if not descs:
        return "calla", "—"
    txt = "; ".join(" + ".join(d) for d in descs[:3])
    if afirmada is None:
        return "aporta", txt
    if tuple(afirmada) in descs:
        return "coincide", txt
    return "difiere", txt


def num(x):
    return "{0:,}".format(x).replace(",", ".")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5000,
                    help="cuántas formas del canon, por frecuencia")
    ap.add_argument("--top-formas", type=int, default=60,
                    help="cuántas formas se listan en la tabla de detalle")
    a = ap.parse_args()

    S.SOLO_CANON = True
    S.DPD_FILTRO = True
    c = S.cargar()
    frec = c["frecuencia"]

    cache_path = os.environ.get("NIGGAHITA_CACHE")
    cache = {}
    if cache_path and os.path.exists(cache_path):
        cache = json.load(open(cache_path, encoding="utf-8"))

    formas = sorted(frec.items(), key=lambda x: (-x[1], x[0]))[:a.n]
    filas = []                     # (forma, n, senal, cands)
    nuevos = 0
    for f, n in formas:
        if f in c["banco"] or f in c["casos"]:
            continue               # respuestas conocidas: van a la medición
        if f not in cache:
            cache[f] = analizar_forma(f)
            nuevos += 1
            if cache_path and nuevos % 200 == 0:
                json.dump(cache, open(cache_path, "w", encoding="utf-8"),
                          ensure_ascii=False)
        info = cache[f]
        if not info or info["autoridad"]:
            continue
        cands = [tuple(p) for p in info["pares"]
                 if es_de_la_clase(f, p[0], p[1], frec)]
        if cands:
            filas.append((f, n, info["senal"], cands))
    if cache_path:
        json.dump(cache, open(cache_path, "w", encoding="utf-8"),
                  ensure_ascii=False)

    # ── la medición previa: banco y casos de la clase ───────────────────
    from solucionar_sandhis import partir_componentes
    conocidas = []                 # (forma, conocida, de_donde)
    for q, lista in c["banco"].items():
        for dato, _a, _r in lista:
            comp = dato.get("comp") if "s" in dato else dato.get("forma_inicial")
            partes = [cotejo(x) for x in partir_componentes(comp or "")]
            if len(partes) == 2 and es_de_la_clase(q, partes[0], partes[1],
                                                   dict(frec, **{partes[0]: 1,
                                                                 partes[1]: 1})):
                conocidas.append((q, tuple(partes), "banco"))
                break
    for q, caso in c["casos"].items():
        if not caso.get("sandhi"):
            continue
        partes = [cotejo(x)
                  for x in partir_componentes(caso.get("componentes", ""))]
        if len(partes) == 2 and es_de_la_clase(q, partes[0], partes[1],
                                               dict(frec, **{partes[0]: 1,
                                                             partes[1]: 1})):
            conocidas.append((q, tuple(partes), "caso adjudicado"))
    medidas = []                   # (forma, conocida, de_donde, clave, dicho)
    for q, conocida, de_donde in sorted(set(conocidas)):
        info = analizar_forma(q)
        if not info:
            continue
        cands = [tuple(p) for p in info["pares"]
                 if es_de_la_clase(q, p[0], p[1], frec)]
        clave, dicho = veredicto(q, frec.get(q, 0), cands, frec)
        medidas.append((q, conocida, de_donde, clave, dicho))

    # ── el informe ──────────────────────────────────────────────────────
    out = []
    w = out.append
    w("# La familia de §34 con segunda voz corriente — la clase de «idamavoca»\n")
    w("*Generado por `herramientas/generar_informe_niggahita_m.py` — modo de "
      "la página (solo-canon + dpd-filtro), las {0} formas más frecuentes del "
      "canon; banco, casos y formas ya afirmadas por una autoridad, "
      "descontados de la tabla y contrastados aparte en la medición. Este "
      "informe PREPARA la firma; no adjudica nada: la regla, su grado y sus "
      "resguardos los firma IEBH.*\n".format(num(a.n)))
    w("**La clase.** Niggahīta → m ante vocal (§34), con la segunda voz "
      "corriente: idamavoca = idaṃ + avoca, kimahaṃ = kiṃ + ahaṃ. Hoy sólo "
      "la ven los casos adjudicados. Cuenta como lectura de la clase la "
      "verificada cuya superficie es exactamente base[:-1] + «m» + segunda, "
      "con las dos voces atestiguadas. El DPD figura como TESTIGO (su "
      "descomposición publicada, cotejada), nunca como autoridad.\n")

    total_masa = sum(n for _, n, _, _ in filas)
    por_senal = {}
    por_clave = {}
    acuerdo = {"coincide": 0, "difiere": 0, "calla": 0}
    af = af_sin_senal = masa_af = 0
    detalle = []
    for f, n, senal, cands in sorted(filas, key=lambda x: -x[1]):
        clave, dicho = veredicto(f, n, cands, frec)
        if dicho is not None:
            af += 1
            masa_af += n
            if not senal:
                af_sin_senal += 1
        por_senal[senal or "sin señal"] = \
            por_senal.get(senal or "sin señal", 0) + 1
        por_clave[clave] = por_clave.get(clave, 0) + 1
        d_clave, d_txt = dpd_dice(f, dicho if clave in
                                  ("única", "única por resguardo", "gemelas") else None)
        if clave in ("única", "única por resguardo", "gemelas") and d_clave in acuerdo:
            acuerdo[d_clave] += 1
        detalle.append((f, n, senal, cands, clave, dicho, d_clave, d_txt))

    w("## Resumen\n")
    w("| | |")
    w("| --- | ---: |")
    w("| formas de la clase (sin autoridad previa) | {0} |".format(len(filas)))
    w("| masa en el canon | {0} |".format(num(total_masa)))
    for k in ("segura", "posible", "sin señal"):
        if k in por_senal:
            w("| con señal «{0}» hoy | {1} |".format(k, por_senal[k]))
    for k in sorted(por_clave):
        w("| veredicto «{0}» | {1} |".format(k, por_clave[k]))
    w("")
    w("**La firma afirmaría {0} formas (masa {1}); {2} de ellas HOY no "
      "tienen señal** — recall nuevo, no sólo «no sabe» resuelto. Las "
      "gemelas cuentan como afirmables sólo si se firma también su "
      "desempate.\n".format(af, num(masa_af), af_sin_senal))
    if hay_testigo():
        w("El testigo DPD, sobre las afirmables: coincide {0} · difiere {1} "
          "· calla {2}.\n".format(acuerdo["coincide"], acuerdo["difiere"],
                                  acuerdo["calla"]))
    else:
        w("**El testigo DPD no está disponible en esta máquina** "
          "(`dpd-descomposiciones.tsv` vive en la Mac del IEBH): la columna "
          "queda vacía. Correr este mismo informe allí la llena.\n")

    w("## Detalle, por frecuencia\n")
    w("| forma | frec. | señal hoy | lecturas de la clase | veredicto | el DPD (testigo) |")
    w("| --- | ---: | --- | --- | --- | --- |")
    for f, n, senal, cands, clave, dicho, d_clave, d_txt in \
            detalle[:a.top_formas]:
        col = "; ".join("{0} ({1}) + {2} ({3})".format(
            b, num(frec.get(b, 0)), s, num(frec.get(s, 0)))
            for b, s in cands[:4])
        if len(cands) > 4:
            col += "; …"
        w("| {0} | {1} | {2} | {3} | {4} | {5}: {6} |".format(
            f, num(n), senal or "—", col, clave, d_clave, d_txt))
    if len(detalle) > a.top_formas:
        w("\n*…y {0} formas más (--top-formas las lista).*".format(
            len(detalle) - a.top_formas))
    w("")

    w("## La medición previa: las respuestas conocidas de la clase\n")
    w("*Banco firmado y casos adjudicados cuya descomposición conocida es de "
      "la clase, contrastados con lo que el mecanismo simulado habría "
      "dicho SIN conocerlos.*\n")
    w("| forma | conocida | de dónde | el mecanismo habría dicho | ¿acierta? |")
    w("| --- | --- | --- | --- | --- |")
    aciertos = comparables = 0
    for q, conocida, de_donde, clave, dicho in medidas:
        if dicho is not None:
            comparables += 1
            bien = tuple(dicho) == conocida
            aciertos += bien
            j = "sí" if bien else "**NO**"
            habria = "{0} + {1} ({2})".format(dicho[0], dicho[1], clave)
        else:
            j = "calla"
            habria = clave
        w("| {0} | {1} | {2} | {3} | {4} |".format(
            q, " + ".join(conocida), de_donde, habria, j))
    w("")
    w("Afirmaría {0} de las {1} conocidas; aciertos {2} de {3}.\n".format(
        comparables, len(medidas), aciertos, comparables))

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    with open(DESTINO, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    print("clase §34:", len(filas), "formas · masa", num(total_masa),
          "· conocidas medidas:", len(medidas), "· escrito", DESTINO)


if __name__ == "__main__":
    main()
