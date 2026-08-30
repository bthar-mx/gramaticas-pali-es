#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
El criterio de categoría gramatical del IEBH, mecanizado y medido.

    python3 herramientas/generar_informe_criterio_pos.py
    PROCLITICAS_CACHE=/tmp/cache-informes.json python3 herramientas/…

Palabras del IEBH (briefing 35 §6): *«sattānaṃ is a noun, caranto is a
present participle, cittaṃ is a noun. I can almost with 100 % confidence say
that never caranto = ca + anto.»* De ahí el criterio: **si el diccionario da
la forma entera como palabra con su categoría gramatical, no es sandhi
proclítico.** En la sesión 35 se comprobó que no se podía computar, porque
el léxico de la carpeta era una lista de formas desnuda. Ya no: `dpd-pos.tsv`
(555.280 pares forma-lema-categoría) trae la categoría, y el DPD tiene entre
las suyas una que dice **«sandhi»** — 1.522 formas.

## Dos formulaciones, y NO son equivalentes

  (a) **POSITIVA** — afirmar sólo si el DPD registra la forma como «sandhi».
  (b) **NEGATIVA** — descartar si la forma tiene cualquier categoría ajena.

La (b) es la literal del enunciado, y es la peor: tira ocho de las catorce
lecturas que el testigo confirma, porque una forma de sandhi corriente
aparece además como otra cosa (cetaṃ es masc y nt aparte de sandhi). La (a)
conserva las catorce.

## El hallazgo: el criterio y el testigo son complementarios

Ni uno ni otro basta solo. Cuatro de las nueve lecturas falsas —sāpi, sāyaṃ,
yāyaṃ, yeva— el DPD SÍ las marca «sandhi»: reconoce que hay sandhi y
descompone distinto (sā + api, con el femenino, no so + api). La categoría
no las puede cortar; la descomposición sí. Juntas cortan las nueve y
conservan las catorce.

## Y el límite, que es serio: la etiqueta tiene 50 % de recall

Sobre las 18 respuestas ya adjudicadas de la clase, el DPD etiqueta «sandhi»
sólo 9. Deja fuera netaṃ, cāti y nātivattati —adjudicadas por el propio
IEBH—, y cesā, nayimassa, nopeti, anabhineyya, soyeva y svassa. De modo que
la etiqueta sirve de **licencia** (lo que marca, casi seguro es sandhi) y no
de **prueba de verdad** (lo que no marca puede serlo igualmente). Usarla
como puerta única silenciaría sandhis reales.

El informe PREPARA; no adjudica nada. Firmar el criterio es del IEBH.

Salida: docs/solucionador/informe-criterio-pos.md
"""

import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "nuestro"))

from normalizar import cotejo                                      # noqa: E402
import solucionar_sandhis as S                                     # noqa: E402
from solucionar_sandhis import partir_componentes                  # noqa: E402

DESTINO = os.path.join(RAIZ, "docs", "solucionador",
                       "informe-criterio-pos.md")
POS = os.path.join(RAIZ, "dpd-pos.tsv")

VOCALES = "aāiīuūeo"
LARGA = {"a": "ā", "i": "ī", "u": "ū"}
PRIMAS = ["ca", "na", "so", "yo"]
N = 5000


def hay_pos():
    return os.path.exists(POS)


def cargar_pos():
    d = {}
    with open(POS, encoding="utf-8") as fh:
        for linea in fh:
            p = linea.rstrip("\n").split("\t")
            if len(p) >= 3:
                d.setdefault(cotejo(p[0]), set()).add(p[2])
    return d


def es_de_la_clase(q, prima, seg, frec):
    return (prima in PRIMAS and seg[:1] in VOCALES
            and prima + seg != q and frec.get(seg, 0) > 0)


def gemelas(c):
    if len(c) != 2:
        return None
    (p1, s1), (p2, s2) = sorted(c)
    if p1 == p2 and s1 and s2 and s1[1:] == s2[1:] \
            and LARGA.get(s1[:1]) == s2[:1]:
        return (p1, s1)
    return None


def veredicto(n, cands, frec):
    piso = max(n, 1)
    ok = [(p, s) for p, s in cands if frec.get(s, 0) >= piso]
    if not ok:
        return None
    g = gemelas(ok)
    if g:
        return g
    return ok[0] if len(ok) == 1 else None


def dpd_dice(f, afirmada):
    descs = [tuple(cotejo(x) for x in d) for d in S.descomposicion(f)
             if len(d) == 2]
    if not descs:
        return "calla", "—"
    txt = "; ".join(" + ".join(d) for d in descs[:3])
    return ("coincide" if tuple(afirmada) in descs else "difiere"), txt


def analizar(f):
    try:
        r = S.solucionar(f)
    except Exception:                                              # noqa: BLE001
        return None
    lect = r.get("lecturas") or []
    l0 = lect[0] if lect else {}
    pares = []
    for l in lect:
        comp = [cotejo(x) for x in (l.get("componentes") or [])]
        if len(comp) == 2 and comp not in pares:
            pares.append(comp)
    return {"senal": r.get("senal"),
            "autoridad": bool(r.get("del_banco") or l0.get("adjudicada")
                              or l0.get("patron") or l0.get("origen")),
            "pares": pares}


def num(x):
    return "{0:,}".format(x).replace(",", ".")


def main():
    S.SOLO_CANON = True
    S.DPD_FILTRO = True
    c = S.cargar()
    frec = c["frecuencia"]

    if not hay_pos():
        print("falta dpd-pos.tsv en la raíz; no se escribe nada.")
        return
    pos = cargar_pos()
    con_sandhi = sum(1 for v in pos.values() if "sandhi" in v)

    cache_path = os.environ.get("PROCLITICAS_CACHE")
    cache = {}
    if cache_path and os.path.exists(cache_path):
        cache = json.load(open(cache_path, encoding="utf-8"))

    afirmables = []
    nuevos = 0
    for f, n in sorted(frec.items(), key=lambda x: (-x[1], x[0]))[:N]:
        if f in c["banco"] or f in c["casos"]:
            continue
        if f not in cache:
            cache[f] = analizar(f)
            nuevos += 1
            if cache_path and nuevos % 200 == 0:
                json.dump(cache, open(cache_path, "w", encoding="utf-8"),
                          ensure_ascii=False)
        info = cache[f]
        if not info or info["autoridad"]:
            continue
        cands = [tuple(p) for p in info["pares"]
                 if es_de_la_clase(f, p[0], p[1], frec)]
        if not cands:
            continue
        dicho = veredicto(n, cands, frec)
        if dicho is None:
            continue
        d_clave, d_txt = dpd_dice(f, dicho)
        afirmables.append({"forma": f, "frec": n, "par": dicho,
                           "dpd": d_clave, "dpd_txt": d_txt,
                           "pos": sorted(pos.get(f, ()))})
    if cache_path:
        json.dump(cache, open(cache_path, "w", encoding="utf-8"),
                  ensure_ascii=False)

    def positiva(x):
        return "sandhi" in pos.get(x["forma"], ())

    def negativa(x):
        p = pos.get(x["forma"], set())
        return bool(p) and p <= {"sandhi"}

    def combinada(x):
        return positiva(x) and x["dpd"] != "difiere"

    # ── las respuestas conocidas ────────────────────────────────────────
    conocidas = set()
    for q, lista in c["banco"].items():
        for dato, _a, _r in lista:
            comp = dato.get("comp") if "s" in dato \
                else dato.get("forma_inicial")
            partes = [cotejo(x) for x in partir_componentes(comp or "")]
            if (len(partes) == 2 and partes[0] in PRIMAS
                    and partes[1][:1] in VOCALES
                    and partes[0] + partes[1] != q):
                conocidas.add((q, tuple(partes), "banco"))
                break
    for q, caso in c["casos"].items():
        if not caso.get("sandhi"):
            continue
        partes = [cotejo(x) for x in
                  partir_componentes(caso.get("componentes", ""))]
        if (len(partes) == 2 and partes[0] in PRIMAS
                and partes[1][:1] in VOCALES and partes[0] + partes[1] != q):
            conocidas.add((q, tuple(partes), "caso adjudicado"))
    conocidas = sorted(conocidas)
    etiquetadas = [k for k in conocidas if "sandhi" in pos.get(k[0], ())]

    # ── el informe ──────────────────────────────────────────────────────
    out = []
    w = out.append
    w("# El criterio de categoría gramatical del IEBH, mecanizado y medido\n")
    w("*Generado por `herramientas/generar_informe_criterio_pos.py` — modo "
      "de la página (solo-canon + dpd-filtro), sobre las {0} formas más "
      "frecuentes del canon. Este informe PREPARA la firma; no adjudica "
      "nada: firmar el criterio es del IEBH.*\n".format(num(N)))

    w("## El criterio y lo que hacía falta\n")
    w("Palabras del IEBH (briefing 35 §6): *«sattānaṃ is a noun, caranto is "
      "a present participle, cittaṃ is a noun. I can almost with 100 % "
      "confidence say that never caranto = ca + anto.»* De ahí: **si el "
      "diccionario da la forma entera como palabra con su categoría "
      "gramatical, no es sandhi proclítico.** En la sesión 35 no se pudo "
      "computar —el léxico de la carpeta era una lista de formas desnuda—. "
      "Ya se puede: `dpd-pos.tsv` trae {0} formas con categoría, y entre "
      "las categorías del DPD hay una que dice **«sandhi»**: {1} formas.\n"
      .format(num(len(pos)), num(con_sandhi)))

    w("## Las dos formulaciones, que no son equivalentes\n")
    w("| | formulación |")
    w("| --- | --- |")
    w("| **(a) positiva** | afirmar sólo si el DPD registra la forma como "
      "«sandhi» |")
    w("| **(b) negativa** | descartar si la forma tiene cualquier categoría "
      "ajena |")
    w("")
    w("Medidas sobre las **{0} formas que el mecanismo espejo afirmaría**, "
      "con el testigo DPD de árbitro:\n".format(len(afirmables)))
    w("| criterio | conserva de las {0} correctas | deja pasar de las {1} "
      "falsas | de las {2} mudas | precisión |".format(
          sum(1 for x in afirmables if x["dpd"] == "coincide"),
          sum(1 for x in afirmables if x["dpd"] == "difiere"),
          sum(1 for x in afirmables if x["dpd"] == "calla")))
    w("| --- | ---: | ---: | ---: | ---: |")
    for nombre, pred in (("(a) positiva", positiva),
                         ("(b) negativa", negativa),
                         ("**(a) + el testigo**", combinada)):
        b = sum(1 for x in afirmables
                if x["dpd"] == "coincide" and pred(x))
        m = sum(1 for x in afirmables if x["dpd"] == "difiere" and pred(x))
        k = sum(1 for x in afirmables if x["dpd"] == "calla" and pred(x))
        w("| {0} | {1} | {2} | {3} | {4} |".format(
            nombre, b, m, k,
            "{0:.1f} %".format(100.0 * b / (b + m)) if b + m else "—"))
    w("")
    w("**La (b), que es la literal del enunciado, es la peor**: tira lecturas "
      "correctas porque una forma de sandhi corriente aparece además como "
      "otra cosa (cetaṃ es *masc* y *nt* aparte de *sandhi*). La (a) las "
      "conserva todas.\n")

    w("## El hallazgo: el criterio y el testigo son complementarios\n")
    w("Ni uno ni otro basta solo. Estas lecturas falsas el DPD **sí** las "
      "marca «sandhi» — reconoce que hay sandhi y descompone distinto:\n")
    w("| forma | frec. | la receta diría | el DPD (testigo) | categorías |")
    w("| --- | ---: | --- | --- | --- |")
    for x in afirmables:
        if x["dpd"] == "difiere" and positiva(x):
            w("| {0} | {1} | {2} | {3} | {4} |".format(
                x["forma"], num(x["frec"]), " + ".join(x["par"]),
                x["dpd_txt"], ", ".join(x["pos"])))
    w("")
    w("La categoría no las puede cortar; la descomposición sí. **Juntas "
      "cortan las {0} falsas y conservan las {1} correctas.**\n".format(
          sum(1 for x in afirmables if x["dpd"] == "difiere"),
          sum(1 for x in afirmables if x["dpd"] == "coincide")))

    w("## El límite, que es serio: la etiqueta tiene {0:.0f} % de recall\n"
      .format(100.0 * len(etiquetadas) / max(len(conocidas), 1)))
    w("Sobre las {0} respuestas YA adjudicadas de la clase, el DPD etiqueta "
      "«sandhi» sólo {1}.\n".format(len(conocidas), len(etiquetadas)))
    w("| forma | conocida | de dónde | ¿la etiqueta el DPD? | categorías |")
    w("| --- | --- | --- | --- | --- |")
    for q, par, de in conocidas:
        p = sorted(pos.get(q, ()))
        w("| {0} | {1} | {2} | {3} | {4} |".format(
            q, " + ".join(par), de,
            "sí" if "sandhi" in pos.get(q, ()) else "**no**",
            ", ".join(p) if p else "—"))
    w("")
    w("Deja fuera netaṃ, cāti y nātivattati —adjudicadas por el propio "
      "IEBH—. De modo que la etiqueta sirve de **licencia** (lo que marca, "
      "casi seguro es sandhi) y **no de prueba de verdad** (lo que no marca "
      "puede serlo igualmente). Usarla como puerta única silenciaría "
      "sandhis reales, y por eso el informe no la propone como tal.\n")

    w("## Lo que el criterio combinado dejaría pasar\n")
    w("| forma | frec. | lectura | el testigo | categorías |")
    w("| --- | ---: | --- | --- | --- |")
    for x in afirmables:
        if combinada(x):
            w("| {0} | {1} | {2} | {3} | {4} |".format(
                x["forma"], num(x["frec"]), " + ".join(x["par"]), x["dpd"],
                ", ".join(x["pos"])))
    w("")

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    with open(DESTINO, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    print("criterio pos:", len(afirmables), "afirmables ·",
          sum(1 for x in afirmables if combinada(x)), "pasan el combinado",
          "· escrito", DESTINO)


if __name__ == "__main__":
    main()
