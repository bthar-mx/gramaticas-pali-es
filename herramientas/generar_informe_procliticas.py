#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
El informe de la regla de PRIMERA voz —los proclíticos de la clase de
«cetā»—, para preparar su firma con medición previa (mapa de la sesión
33, punto 1; el caso cetā = ca + etā la detectó).

    python3 herramientas/generar_informe_procliticas.py            # top 5000
    python3 herramientas/generar_informe_procliticas.py --primas ca,na,so,yo,su
    PROCLITICAS_CACHE=/tmp/procliticas.json python3 herramientas/…

La clase: una primera voz de un puñado cerrado de partículas y pronombres
—ca, na, so, yo (las superficies c-, n-, sv-, yv-)— pegada a una segunda
que empieza en vocal: cetā = ca + etā, cāyaṃ, cassa, cidaṃ, netaṃ,
nāyaṃ, svāyaṃ = so + ayaṃ, yvāyaṃ = yo + ayaṃ.

Los patrones vigentes se licencian por la SEGUNDA voz (iti, api, ca) y no
tienen mecanismo de primera voz: diseñarlo pide firma. Este informe mide
lo que ese mecanismo haría, espejo del vigente:

  · la primera voz es la fija (el puñado firmable); la SEGUNDA es la que
    varía — y por eso el resguardo de la base residual se refleja: aquí
    la voz que debe ser al menos tan frecuente como la forma entera es la
    segunda (una segunda de 1 aparición es el resto de recortar la
    consonante, el defecto de pajānāti visto en espejo), y COMO EN EL
    MECANISMO VIGENTE el resguardo filtra candidatas antes de contar;
  · «única»    — una sola lectura de la clase, y pasa el resguardo;
  · «única por resguardo» — quedó una sola PORQUE el resguardo descartó
    rivales: mirar con lupa;
  · «gemelas»  — dos lecturas de la misma primera cuyas segundas sólo
                 difieren en la cantidad de la vocal inicial (ayaṃ/āyaṃ):
                 pedirían un desempate como el breve/larga firmado;
  · «n lecturas» — varias pasan el resguardo: el mecanismo callaría;
  · «calla (resguardo)» — ninguna lo pasa.

OJO CON LO QUE LA MEDICIÓN MUESTRA: a diferencia de §34 —donde la «m» en
la juntura es huella visible—, esta clase no tiene huella superficial:
cualquier palabra corriente en c-, n-, s-, y- + vocal es candidata, y el
veredicto «única» incluye lecturas a todas luces falsas (sattānaṃ = so +
attānaṃ, caranto = ca + anto, yehi = yo + ehi) que el resguardo NO
frena, porque la segunda es más frecuente que la forma. El espejo del
mecanismo vigente, tal cual, no parece firmable: la firma tendrá que
decidir qué condición extra pide la primera voz (¿sólo formas que la
señal ya marca?, ¿un puñado también de segundas?, ¿el testigo DPD?).
Ese es exactamente el dato que este informe existe para dar.

El DPD entra como TESTIGO, no como autoridad, cuando su archivo de
descomposiciones está presente (vive en la Mac del IEBH). Al final, las
respuestas CONOCIDAS —banco firmado y casos adjudicados de la clase— se
contrastan una a una con lo que el mecanismo habría dicho: ésa es la
medición previa.

El informe PREPARA; no adjudica nada. La regla, el puñado de primeras
voces, su grado y sus resguardos los firma IEBH. Una forma puede
aparecer también en el informe de familias por segunda voz (ceva está
aquí por «ca + eva» y allá en la familia «eva», donde el patrón de
segunda voz callaba por tres bases): son cortes distintos del mismo
problema, y éste es el lado que lo resuelve.

Salida: docs/solucionador/informe-procliticas.md
La caché (PROCLITICAS_CACHE) es de cómputo, no de datos, y su formato es
el mismo del informe de §34: apuntarlas al mismo archivo las comparte.
Bustearla cuando cambie la señal.
"""

import argparse
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "nuestro"))
from normalizar import cotejo                                      # noqa: E402
import solucionar_sandhis as S                                     # noqa: E402
from solucionar_sandhis import partir_componentes                  # noqa: E402

DESTINO = os.path.join(RAIZ, "docs", "solucionador",
                       "informe-procliticas.md")

VOCALES = "aāiīuūeo"
LARGA = {"a": "ā", "i": "ī", "u": "ū"}


def analizar_forma(f):
    """Señal y pares verificados de dos componentes (en cotejo), con marca
    de autoridad. Serializable; mismo formato que el informe de §34."""
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


def es_de_la_clase(q, prima, seg, primas, frec):
    """¿Es (prima, seg) una lectura proclítica de la superficie `q`?
    La recomposición ya la verificó el motor; aquí sólo se exige la clase:
    primera del puñado, segunda vocálica y atestiguada, y que haya habido
    operación (la yuxtaposición sin sandhi queda fuera del encargo)."""
    return (prima in primas and seg[:1] in VOCALES
            and prima + seg != q
            and frec.get(seg, 0) > 0)


def gemelas(cands):
    """Dos candidatas con la misma primera cuyas segundas sólo difieren en
    la cantidad de la vocal inicial → la de inicial BREVE, o None."""
    if len(cands) != 2:
        return None
    (p1, s1), (p2, s2) = sorted(cands)
    if p1 == p2 and s1 and s2 and s1[1:] == s2[1:] \
            and LARGA.get(s1[:1]) == s2[:1]:
        return (p1, s1)
    return None


def veredicto(q, n, cands, frec):
    """(clave, lectura afirmada o None). Simula el mecanismo como el
    vigente: el resguardo FILTRA candidatas (la segunda que sea menos
    frecuente que la forma entera no cuenta) y la unicidad de lo que
    queda es la licencia."""
    piso = max(n, 1)
    ok = [(p, s) for p, s in cands if frec.get(s, 0) >= piso]
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
    """`dpd-descomposiciones.tsv` vive en la Mac del IEBH (briefing 33
    §3.4) y no viaja con el repositorio. Sin él, el informe lo dice — no
    finge que el DPD «calla» cuando no se le preguntó."""
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
    ap.add_argument("--primas", default="ca,na,so,yo",
                    help="el puñado de primeras voces, separado por comas")
    ap.add_argument("--top-formas", type=int, default=40,
                    help="cuántas formas se listan por primera voz")
    a = ap.parse_args()
    primas = [cotejo(x.strip()) for x in a.primas.split(",") if x.strip()]

    S.SOLO_CANON = True
    S.DPD_FILTRO = True
    c = S.cargar()
    frec = c["frecuencia"]

    cache_path = os.environ.get("PROCLITICAS_CACHE")
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
                 if es_de_la_clase(f, p[0], p[1], primas, frec)]
        if cands:
            filas.append((f, n, info["senal"], cands))
    if cache_path:
        json.dump(cache, open(cache_path, "w", encoding="utf-8"),
                  ensure_ascii=False)

    # ── la medición previa: banco y casos de la clase ───────────────────
    def de_la_clase_conocida(q, partes):
        return (len(partes) == 2
                and partes[0] in primas and partes[1][:1] in VOCALES
                and partes[0] + partes[1] != q)

    conocidas = []                 # (forma, conocida, de_donde)
    for q, lista in c["banco"].items():
        for dato, _a, _r in lista:
            comp = dato.get("comp") if "s" in dato else dato.get("forma_inicial")
            partes = [cotejo(x) for x in partir_componentes(comp or "")]
            if de_la_clase_conocida(q, partes):
                conocidas.append((q, tuple(partes), "banco"))
                break
    for q, caso in c["casos"].items():
        if not caso.get("sandhi"):
            continue
        partes = [cotejo(x)
                  for x in partir_componentes(caso.get("componentes", ""))]
        if de_la_clase_conocida(q, partes):
            conocidas.append((q, tuple(partes), "caso adjudicado"))
    medidas = []                   # (forma, conocida, de_donde, clave, dicho)
    for q, conocida, de_donde in sorted(set(conocidas)):
        info = analizar_forma(q)
        if not info:
            continue
        cands = [tuple(p) for p in info["pares"]
                 if es_de_la_clase(q, p[0], p[1], primas, frec)]
        clave, dicho = veredicto(q, frec.get(q, 0), cands, frec)
        medidas.append((q, conocida, de_donde, clave, dicho))

    # ── el informe ──────────────────────────────────────────────────────
    out = []
    w = out.append
    w("# La regla de primera voz — los proclíticos de la clase de «cetā»\n")
    w("*Generado por `herramientas/generar_informe_procliticas.py` — modo de "
      "la página (solo-canon + dpd-filtro), las {0} formas más frecuentes "
      "del canon; puñado medido: {1}. Banco, casos y formas ya afirmadas "
      "por una autoridad, descontados de la tabla y contrastados aparte en "
      "la medición. Este informe PREPARA la firma; no adjudica nada: la "
      "regla, el puñado, su grado y sus resguardos los firma IEBH.*\n"
      .format(num(a.n), ", ".join(primas)))
    w("**La clase.** Primera voz proclítica ante vocal: cetā = ca + etā, "
      "netaṃ = na + etaṃ, svāyaṃ = so + ayaṃ, yvāyaṃ = yo + ayaṃ. Los "
      "patrones vigentes se licencian por la segunda voz; el mecanismo "
      "espejo que aquí se simula se licencia por la primera, con el "
      "resguardo reflejado sobre la segunda (segunda ≥ forma). Otras "
      "primeras candidatas (su-, …) se miden con `--primas`. El DPD figura "
      "como TESTIGO, nunca como autoridad.\n")

    total_masa = sum(n for _, n, _, _ in filas)
    por_senal = {}
    por_clave = {}
    por_prima = {}
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
        p0 = (dicho or cands[0])[0]
        por_prima.setdefault(p0, []).append(n)
        d_clave, d_txt = dpd_dice(f, dicho if clave in
                                  ("única", "única por resguardo", "gemelas") else None)
        if clave in ("única", "única por resguardo", "gemelas") and d_clave in acuerdo:
            acuerdo[d_clave] += 1
        detalle.append((f, n, senal, cands, clave, dicho, d_clave, d_txt, p0))

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
    w("| primera voz | formas | masa |")
    w("| --- | ---: | ---: |")
    for p in primas:
        if p in por_prima:
            w("| {0} ({1}) | {2} | {3} |".format(
                p, num(frec.get(p, 0)), len(por_prima[p]),
                num(sum(por_prima[p]))))
    w("")
    w("**El espejo del mecanismo vigente afirmaría {0} formas (masa {1}); "
      "{2} de ellas hoy sin señal.** Pero —a diferencia de §34, donde la "
      "«m» en la juntura es huella visible— esta clase no tiene huella "
      "superficial: cualquier palabra corriente en c-, n-, s-, y- + vocal "
      "es candidata, y el veredicto «única» incluye lecturas a todas luces "
      "falsas (sattānaṃ = so + attānaṃ, caranto = ca + anto, yehi = yo + "
      "ehi) que el resguardo no frena, porque la segunda es más frecuente "
      "que la forma. **El espejo, tal cual, no parece firmable**: la firma "
      "tendrá que decidir qué condición extra pide la primera voz — ¿sólo "
      "formas que la señal ya marca?, ¿un puñado también de segundas?, "
      "¿el testigo DPD? Ése es el dato que este informe existe para "
      "dar.\n".format(af, num(masa_af), af_sin_senal))
    if hay_testigo():
        w("El testigo DPD, sobre las afirmables: coincide {0} · difiere {1} "
          "· calla {2}.\n".format(acuerdo["coincide"], acuerdo["difiere"],
                                  acuerdo["calla"]))
    else:
        w("**El testigo DPD no está disponible en esta máquina** "
          "(`dpd-descomposiciones.tsv` vive en la Mac del IEBH): la columna "
          "queda vacía. Correr este mismo informe allí la llena.\n")

    w("## Detalle, por primera voz y frecuencia\n")
    for p in primas:
        del_p = [d for d in detalle if d[8] == p]
        if not del_p:
            continue
        w("### «{0}» ({1} apariciones propias) — {2} formas · masa {3}\n"
          .format(p, num(frec.get(p, 0)), len(del_p),
                  num(sum(d[1] for d in del_p))))
        w("| forma | frec. | señal hoy | lecturas de la clase | veredicto | el DPD (testigo) |")
        w("| --- | ---: | --- | --- | --- | --- |")
        for f, n, senal, cands, clave, dicho, d_clave, d_txt, _p in \
                del_p[:a.top_formas]:
            col = "; ".join("{0} + {1} ({2})".format(
                x, s, num(frec.get(s, 0))) for x, s in cands[:4])
            if len(cands) > 4:
                col += "; …"
            w("| {0} | {1} | {2} | {3} | {4} | {5}: {6} |".format(
                f, num(n), senal or "—", col, clave, d_clave, d_txt))
        if len(del_p) > a.top_formas:
            w("\n*…y {0} formas más (--top-formas las lista).*".format(
                len(del_p) - a.top_formas))
        w("")

    w("## La medición previa: las respuestas conocidas de la clase\n")
    w("*Banco firmado y casos adjudicados cuya descomposición conocida es "
      "de la clase, contrastados con lo que el mecanismo simulado habría "
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
    print("proclíticos:", len(filas), "formas · masa", num(total_masa),
          "· conocidas medidas:", len(medidas), "· escrito", DESTINO)


if __name__ == "__main__":
    main()
