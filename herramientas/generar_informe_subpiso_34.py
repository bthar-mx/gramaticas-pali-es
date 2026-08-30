#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qué calla §34 por debajo de su piso, y qué dice el DPD de cada cosa callada.

    python3 herramientas/generar_informe_subpiso_34.py
    SUBPISO_CACHE=/tmp/subpiso.json python3 herramientas/…

El régimen medido de §34 (briefing 36 §3) fijó `frec_minima` = 159 porque
la medición que licenció el patrón se detuvo en el puesto 5.000 y, por
debajo, la receta afirmaba en falso: jātimaraṇā (frec 3) como «jātiṃ +
araṇā» siendo el compuesto jāti + maraṇā, y vedhamānehi (7) como «vedhaṃ +
ānehi» siendo vedhamāna, compuesto también (las dos, enmendadas por el IEBH el
2026-08-30). Ampliar la licencia es del IEBH, y
para eso hace falta ver ENTERO lo que el piso calla. Eso mide este informe.

## La población: la referencia de señal, no un corte por frecuencia

**Las 16.366 formas de la referencia de señal NO son «las 16.366 formas más
frecuentes».** Son las formas únicas de los dos corpus de Sandhi (versos y
comentario), y por eso bajan hasta frecuencia 0; el corte por frecuencia se
detiene en 45. La confusión no es teórica: jātimaraṇā (frec 3) ocupa el
puesto 167.330 y vedhamānehi (7) el 86.261, de modo que **ninguna de las
dos aparece en un `--n 16366`** de los otros dos informes, siendo las dos
que motivaron el piso. Este informe recorre la referencia, que es la
población que citan los briefings 33-36.

## Qué hace

Aplica la receta EXACTA del patrón embarcado (`_patron_niggahita_m`) con el
piso QUITADO, y parte el resultado en dos: lo que el patrón ya afirma hoy
(frec >= `frec_minima`) y lo que CALLA por el régimen medido. De cada
afirmación callada se le pregunta al DPD, que aquí es TESTIGO y no
autoridad, nunca.

El acuerdo se cuenta dos veces: con `cotejo()` tal cual y con una
comparación TOLERANTE que iguala «m» final con «ṃ». La operación de §34 es
precisamente ésa, y el DPD escribe «sabbam + idaṃ» donde el motor escribe
«sabbaṃ + idaṃ»: la misma lectura contada como discrepancia. Medido, el
artefacto resultó ser de UN caso en 419 — pequeño, pero contado en lugar de
supuesto.

## Las tres firmas de lo falso

El informe mide tres condiciones que separan lo falso de lo correcto mucho
mejor que la frecuencia, y da para cada una cuánto corta y cuánto cuesta.
Son CANDIDATAS que el informe prepara; no se aplican a nada.

## Dos límites que el informe declara y no disimula

1. **El DPD calla sobre jātimaraṇā y sobre vedhamānehi.** El testigo no
   puede adjudicar los dos casos que motivaron el piso; los adjudicó el
   juicio de Angel, y sigue haciendo falta.
2. **La cuenta no cuadra con el briefing 36 §3**, que da 385 afirmaciones
   sin piso donde aquí salen 441 (sin contar las conocidas). Queda SIN
   RECONCILIAR. La causa probable es la precedencia entre patrones —dentro
   de `senal()` otro patrón reclama la forma antes y a §34 no se le
   pregunta—, que esta receta suelta no modela. Se deja dicho, no resuelto.

El informe PREPARA; no adjudica nada. Ampliar la licencia es del IEBH.

Salida: docs/solucionador/informe-subpiso-34.md
"""

import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "nuestro"))

from normalizar import cotejo                                      # noqa: E402
import solucionar_sandhis as S                                     # noqa: E402

DESTINO = os.path.join(RAIZ, "docs", "solucionador",
                       "informe-subpiso-34.md")
REFERENCIA = os.path.join(RAIZ, "nuestro", "js",
                          "referencia-senal-solo-canon.json")
CASOS = os.path.join(RAIZ, "recursos", "solucionador",
                     "casos-reportados.json")

VOCALES = "aāiīuūeo"
LARGA = {"a": "ā", "i": "ī", "u": "ū"}

# Las partículas que ya tienen patrón propio: si la segunda voz acaba en
# una de ellas, la forma es de aquel patrón y no de §34.
PARTICULAS_AJENAS = ("ca", "ñca", "pi", "mpi", "api", "ti")


def tolerante(x):
    """Iguala «m» final con «ṃ»: la operación de §34 es ésa misma, y el DPD
    la escribe de las dos maneras."""
    x = cotejo(x)
    return x[:-1] + "ṃ" if x.endswith("m") else x


def candidata(r, frec, f_forma):
    """La receta del patrón embarcado, SIN el piso de frecuencia. Espejo
    literal de `_patron_niggahita_m`: si cambia allí, cambia aquí."""
    sup = r["cotejo"]
    piso = max(f_forma, 1)
    cand = set()
    for l in r.get("lecturas", []):
        comp = [cotejo(x) for x in l.get("componentes", [])]
        if (len(comp) == 2 and len(comp[0]) >= 2
                and comp[0].endswith("ṃ")
                and comp[1][:1] in VOCALES
                and comp[0][:-1] + "m" + comp[1] == sup
                and frec.get(comp[0], 0) >= piso
                and frec.get(comp[1], 0) >= piso):
            cand.add((comp[0], comp[1]))
    pares = sorted(cand)
    if len(pares) == 2:
        (b1, s1), (b2, s2) = pares
        if (b1 == b2 and s1 and s2 and s1[1:] == s2[1:]
                and LARGA.get(s1[:1]) == s2[:1]):
            pares = [(b1, s1)]
    return pares[0] if len(pares) == 1 else None


def hay_testigo():
    return os.path.exists(S.DESCOMP)


def dpd_dice(f, afirmada):
    """(estricto, tolerante, texto). El DPD es testigo, no autoridad."""
    if not hay_testigo():
        return "ausente", "ausente", "—"
    crudas = [d for d in S.descomposicion(f) if len(d) == 2]
    if not crudas:
        return "calla", "calla", "—"
    estr = [tuple(cotejo(x) for x in d) for d in crudas]
    tol = [tuple(tolerante(x) for x in d) for d in crudas]
    txt = "; ".join(" + ".join(cotejo(x) for x in d) for d in crudas[:3])
    return ("coincide" if tuple(afirmada) in estr else "difiere",
            "coincide" if tuple(tolerante(x) for x in afirmada) in tol
            else "difiere",
            txt)


# ── las tres firmas candidatas ──────────────────────────────────────────
def firma_base(x):
    """La base es «saṃ» o «maṃ»: un preverbo y un acusativo que no encabezan
    una juntura de §34 (samāgama es compuesto; el genitivo es «mama»)."""
    return x["par"][0] in ("saṃ", "maṃ")


def firma_iti(x):
    """La forma acaba en «-ti» y la segunda voz también: territorio del
    patrón de «iti», ya firmado, al que §34 le quita formas."""
    return x["forma"].endswith("ti") and x["par"][1].endswith("ti")


def firma_particula(x):
    """La segunda voz acaba en una partícula con patrón propio."""
    s = x["par"][1]
    return any(s.endswith(p) and s != p for p in PARTICULAS_AJENAS)


FIRMAS = (
    ("la base es «saṃ» o «maṃ»", firma_base),
    ("la forma en «-ti» con segunda voz en «-ti»", firma_iti),
    ("la segunda voz acaba en partícula ajena", firma_particula),
)


def num(x):
    return "{0:,}".format(x).replace(",", ".")


def main():
    S.SOLO_CANON = True
    S.DPD_FILTRO = True
    c = S.cargar()
    frec = c["frecuencia"]

    patrones = json.load(open(CASOS, encoding="utf-8"))["patrones"]
    piso = next(p.get("frec_minima", 0) for p in patrones
                if p.get("clase") == "niggahita_m")

    formas = [r["forma"] for r in
              json.load(open(REFERENCIA, encoding="utf-8"))["filas"]]

    cache_path = os.environ.get("SUBPISO_CACHE")
    cache = {}
    if cache_path and os.path.exists(cache_path):
        cache = json.load(open(cache_path, encoding="utf-8"))

    def guardar():
        if cache_path:
            json.dump(cache, open(cache_path, "w", encoding="utf-8"),
                      ensure_ascii=False)

    nuevos = 0
    for f in formas:
        if f in cache:
            continue
        try:
            r = S.solucionar(f)
        except Exception:                                          # noqa: BLE001
            cache[f] = None
            continue
        par = candidata(r, frec, frec.get(f, 0))
        cache[f] = {"par": list(par) if par else None,
                    "conocida": bool(f in c["banco"] or f in c["casos"])}
        nuevos += 1
        if nuevos % 200 == 0:
            guardar()
    guardar()

    encima, debajo = [], []
    conocidas = 0
    for f in formas:
        info = cache.get(f)
        if not info or not info["par"]:
            continue
        conocidas += bool(info["conocida"])
        (debajo if frec.get(f, 0) < piso else encima).append(
            (f, frec.get(f, 0), tuple(info["par"]), info["conocida"]))

    filas = []
    cuenta_e = {"coincide": 0, "difiere": 0, "calla": 0}
    cuenta_t = {"coincide": 0, "difiere": 0, "calla": 0}
    for f, n, par, conocida in sorted(debajo, key=lambda x: (-x[1], x[0])):
        a_e, a_t, txt = dpd_dice(f, par)
        cuenta_e[a_e] = cuenta_e.get(a_e, 0) + 1
        cuenta_t[a_t] = cuenta_t.get(a_t, 0) + 1
        filas.append({"forma": f, "frec": n, "par": par,
                      "estricto": a_e, "tolerante": a_t, "dpd": txt})

    # ── el informe ──────────────────────────────────────────────────────
    out = []
    w = out.append
    w("# Lo que §34 calla por debajo de su piso, y qué dice el DPD\n")
    w("*Generado por `herramientas/generar_informe_subpiso_34.py` — modo de "
      "la página (solo-canon + dpd-filtro), sobre las {0} formas de la "
      "REFERENCIA DE SEÑAL. Este informe PREPARA la decisión de ampliar la "
      "licencia de §34; no adjudica nada: ampliarla es del IEBH.*\n"
      .format(num(len(formas))))

    w("## La población, que no es la de los otros dos informes\n")
    w("Las {0} formas de la referencia de señal **no son «las {0} formas más "
      "frecuentes»**: son las formas únicas de los dos corpus de Sandhi, y "
      "bajan hasta frecuencia 0, mientras que el corte por frecuencia se "
      "detiene en 45. La distinción decide el informe: jātimaraṇā (frec 3) "
      "ocupa el puesto 167.330 y vedhamānehi (7) el 86.261, de modo que "
      "**ninguna de las dos cabe en un `--n 16366`** — siendo las dos que "
      "motivaron el piso.\n".format(num(len(formas))))

    w("## Lo que el piso calla\n")
    w("| | |")
    w("| --- | ---: |")
    w("| piso firmado (`frec_minima`) | {0} |".format(piso))
    w("| afirmaciones de la receta SIN piso | {0} |"
      .format(len(encima) + len(debajo)))
    w("| de ellas, ya conocidas (banco o caso) | {0} |".format(conocidas))
    w("| dentro del régimen medido (frec ≥ {0}) | {1} |"
      .format(piso, len(encima)))
    w("| **CALLADAS por el piso** (frec < {0}) | **{1}** |"
      .format(piso, len(debajo)))
    w("")

    if hay_testigo():
        w("**El testigo DPD, sobre las {0} calladas:**\n".format(len(debajo)))
        w("| cotejo | coincide | difiere | calla |")
        w("| --- | ---: | ---: | ---: |")
        w("| estricto | {0} | {1} | {2} |".format(
            cuenta_e["coincide"], cuenta_e["difiere"], cuenta_e["calla"]))
        w("| tolerante (m final ≡ ṃ) | {0} | {1} | {2} |".format(
            cuenta_t["coincide"], cuenta_t["difiere"], cuenta_t["calla"]))
        w("")
        w("La diferencia entre las dos filas es el artefacto «m»/«ṃ»: el DPD "
          "escribe «sabbam + idaṃ» donde el motor escribe «sabbaṃ + idaṃ». "
          "Medido, es de {0} caso(s) — pequeño, pero contado y no supuesto.\n"
          .format(abs(cuenta_e["difiere"] - cuenta_t["difiere"])))
        w("**El piso suprime del orden de tres lecturas correctas por cada "
          "una falsa**, y las falsas confirmadas ({0}) son muchas más que "
          "las dos que se conocían.\n".format(cuenta_t["difiere"]))
    else:
        w("**El testigo DPD no está disponible en esta máquina** "
          "(`recursos/lexico/dpd-descomposiciones.tsv`): sin él este informe "
          "no puede decir nada. Correrlo donde esté el archivo.\n")

    w("## Las tres firmas de lo falso — y no es la frecuencia\n")
    w("*Candidatas que el informe mide; no se aplican a nada. Cada una se "
      "cuenta por lo que corta y por lo que cuesta.*\n")
    w("| condición | falsas que corta | correctas que pierde | mudas |")
    w("| --- | ---: | ---: | ---: |")
    for nombre, pred in FIRMAS:
        w("| {0} | {1} | {2} | {3} |".format(
            nombre,
            sum(1 for x in filas if x["tolerante"] == "difiere" and pred(x)),
            sum(1 for x in filas if x["tolerante"] == "coincide" and pred(x)),
            sum(1 for x in filas if x["tolerante"] == "calla" and pred(x))))
    resto = [x for x in filas if not any(p(x) for _n, p in FIRMAS)]
    r_mal = sum(1 for x in resto if x["tolerante"] == "difiere")
    r_bien = sum(1 for x in resto if x["tolerante"] == "coincide")
    w("| **las tres juntas** | **{0} → {1}** | **{2} → {3}** | — |".format(
        cuenta_t["difiere"], r_mal, cuenta_t["coincide"], r_bien))
    w("")
    if cuenta_t["coincide"] + cuenta_t["difiere"]:
        antes = 100.0 * cuenta_t["coincide"] / (cuenta_t["coincide"]
                                                + cuenta_t["difiere"])
        despues = 100.0 * r_bien / max(r_bien + r_mal, 1)
        w("Sobre lo adjudicable (coincide frente a difiere), la precisión "
          "pasa de **{0:.1f} %** a **{1:.1f} %** conservando {2} de las {3} "
          "lecturas correctas.\n".format(antes, despues, r_bien,
                                         cuenta_t["coincide"]))
    w("«saṃ» y «maṃ» son el caso limpio: cortan sin coste ninguno. Ni uno "
      "ni otro encabeza una juntura de §34 — «saṃ-» es preverbo, y "
      "samāgama es un compuesto, no dos voces; «maṃ» es el acusativo donde "
      "la lectura verdadera lleva el genitivo «mama». El grupo de «-ti» es "
      "§34 quitándole formas al patrón de «iti», que ya está firmado: "
      "satimantoti es satimanto + iti, no satiṃ + antoti.\n")

    w("## Dos límites de este informe\n")
    w("1. **El DPD calla sobre jātimaraṇā y sobre vedhamānehi.** El testigo "
      "no adjudica los dos casos que motivaron el piso; los adjudicó el "
      "juicio de Angel, y sigue haciendo falta. La correcta que el piso "
      "silencia y el testigo confirma es tvamasi = tvaṃ + asi. **Enmienda "
      "del IEBH (2026-08-30):** ekamante, que se citaba junto a ella como "
      "segunda correcta silenciada, **es compuesta** — ahí el piso acierta, "
      "y el ejemplo estaba mal elegido. El testigo callaba sobre ella, de "
      "modo que nunca entró en las confirmadas y ninguna cifra se mueve.")
    w("2. **La cuenta no cuadra con el briefing 36 §3**, que da 385 "
      "afirmaciones sin piso donde aquí salen {0} descontando las "
      "conocidas. Queda SIN RECONCILIAR; la causa probable es la "
      "precedencia entre patrones, que esta receta suelta no modela. Se "
      "deja dicho, no resuelto.\n".format(len(encima) + len(debajo)
                                          - conocidas))

    w("## Las falsas, una a una\n")
    w("*Lo que la receta afirmaría bajo el piso y el DPD contradice.*\n")
    w("| forma | frec. | la receta diría | el DPD (testigo) | ¿la corta "
      "alguna firma? |")
    w("| --- | ---: | --- | --- | --- |")
    for x in filas:
        if x["tolerante"] != "difiere":
            continue
        cual = [n for n, p in FIRMAS if p(x)]
        w("| {0} | {1} | {2} | {3} | {4} |".format(
            x["forma"], num(x["frec"]), " + ".join(x["par"]), x["dpd"],
            "; ".join(cual) if cual else "**no**"))
    w("")

    w("## Las correctas que el piso silencia\n")
    w("*Lo que la receta afirmaría bajo el piso y el DPD confirma.*\n")
    w("| forma | frec. | lectura | ¿la cortaría alguna firma? |")
    w("| --- | ---: | --- | --- |")
    for x in filas:
        if x["tolerante"] != "coincide":
            continue
        cual = [n for n, p in FIRMAS if p(x)]
        w("| {0} | {1} | {2} | {3} |".format(
            x["forma"], num(x["frec"]), " + ".join(x["par"]),
            "; ".join(cual) if cual else "no"))
    w("")
    w("Y {0} formas más sobre las que el DPD calla: ni las confirma ni las "
      "contradice, y quedan enteras al juicio del IEBH.\n"
      .format(cuenta_t["calla"]))

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    with open(DESTINO, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    print("subpiso §34:", len(debajo), "calladas · testigo",
          cuenta_t, "· escrito", DESTINO)


if __name__ == "__main__":
    main()
