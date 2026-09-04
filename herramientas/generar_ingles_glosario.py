#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Escribe el cotejo lado a lado del inglés del Glosario de Bhikkhu Nandisena,
para que el IEBH lo firme.

    python3 herramientas/generar_ingles_glosario.py

Lee recursos/glosario/nandisena.json (el español, que manda) y
recursos/glosario/ingles.json (el borrador inglés, con la fuente de cada
término) y escribe docs/glosario/ingles-por-adjudicar.md: cada entrada con
su español y su inglés enfrentados, el término principal con la fuente de
donde sale, y aparte las notas que piden decisión.

Adjudicar es poner «adjudicado»: true en ingles.json, con «adjudicado_por» y
«fecha». Hasta entonces generar_glosario.py comprueba el borrador pero no lo
publica, y el modo inglés de la página enseña el español de estas entradas.
"""

import json
import os
import sys
from collections import Counter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NANDISENA = os.path.join(RAIZ, "recursos", "glosario", "nandisena.json")
INGLES = os.path.join(RAIZ, "recursos", "glosario", "ingles.json")
DESTINO = os.path.join(RAIZ, "docs", "glosario", "ingles-por-adjudicar.md")

sys.path.insert(0, os.path.join(RAIZ, "herramientas"))
from generar_glosario import claves_nandisena, verificar_ingles_nandisena  # noqa: E402


def celda(t):
    return (t or "").replace("|", "\\|").replace("\n", " ")


def familia(fuente):
    f = (fuente or "").lower()
    if f.startswith("n-en"):
        return "N-EN"
    if f.startswith("iebh"):
        return "IEBH"
    if f.startswith("ñāṇamoli"):
        return "Ñāṇamoli"
    if f.startswith("glosario-ingles"):
        return "propuesta (glosario-ingles.json)"
    if f.startswith("remisión"):
        return "remisión"
    return "traducción"


def main():
    nand = json.load(open(NANDISENA, encoding="utf-8"))
    ing = json.load(open(INGLES, encoding="utf-8"))
    entradas = nand["entradas"]
    fallos, avisos, borr = verificar_ingles_nandisena(entradas, ing)
    if fallos:
        print("No se escribe el cotejo. {0} fallo(s):".format(len(fallos)))
        for f in fallos:
            print("  · " + f)
        return 1
    for a in avisos:
        print("  aviso — " + a)

    claves = claves_nandisena(entradas)
    total = len(entradas)
    traducibles = sum(1 for e in entradas if e.get("es") and not e.get("remite_a"))
    hechas = len(borr)
    cuenta = Counter(familia(b.get("fuente")) for b in borr.values())
    tandas = ing.get("tanda", {})

    L = []
    L.append("# El inglés del Glosario de Nandisena")
    L.append("")
    L.append("*Cotejo escrito por `herramientas/generar_ingles_glosario.py` a partir de "
             "`recursos/glosario/nandisena.json` (el español, que manda) y "
             "`recursos/glosario/ingles.json` (el borrador). No se edita a mano: se "
             "corrige el JSON y se vuelve a escribir.*")
    L.append("")
    # La adjudicación va POR TANDA (sesión 57): lo que se publica es lo
    # que el IEBH ha firmado tanda a tanda; lo demás se comprueba y espera.
    firmadas = sorted(n for n, t in tandas.items() if t.get("adjudicado"))
    pendientes = sorted(n for n, t in tandas.items() if not t.get("adjudicado"))
    if firmadas:
        L.append("**Adjudicadas por el IEBH las tandas {0}.** El inglés de esas entradas es "
                 "ya el que publica la página.".format(", ".join(firmadas)))
    if pendientes:
        L.append("**SIN ADJUDICAR las tandas {0}.** `generar_glosario.py` comprueba esas "
                 "entradas contra el español —clave, ejemplos citados, NFC— pero no las "
                 "inyecta: el modo inglés de la página enseña ahí el español. Firmar una "
                 "tanda es poner `\"adjudicado\": true` en su entrada de `tanda` en "
                 "`ingles.json`, con `adjudicado_por` y `fecha`.".format(", ".join(pendientes)))
    L.append("")
    L.append("**{0} de {1} entradas redactadas** ({2} traducibles; las {3} restantes "
             "son remisiones o no tienen definición en el impreso).".format(
                 hechas, total, traducibles, total - traducibles))
    L.append("")
    for n, t in sorted(tandas.items()):
        estado = ("adjudicada por {0} el {1}".format(t.get("adjudicado_por"), t.get("fecha"))
                  if t.get("adjudicado") else "SIN ADJUDICAR")
        L.append("- Tanda {0}: {1} → {2} (pp. {3}), {4} entradas, {5} — **{6}**{7}".format(
            n, t.get("desde"), t.get("hasta"), t.get("paginas"),
            t.get("entradas"), t.get("redactada"), estado,
            ". " + t["veredicto"] if t.get("veredicto") else "."))
    L.append("")
    L.append("## 1. La prelación de fuentes, y cuántas entradas salen de cada una")
    L.append("")
    L.append("El **término** principal de cada entrada se toma de la primera fuente que "
             "lo dé, en este orden; la **definición** entera se traduce siempre del "
             "español de Nandisena, sin añadir ni quitar.")
    L.append("")
    L.append("| orden | fuente | qué es | entradas |")
    L.append("| ---: | --- | --- | ---: |")
    filas = [
        ("N-EN", "el inglés del propio Nandisena: Sandhi inglés y su memo §2, el "
                 "apéndice sobre «ca», y sus Taddhita, Ākhyāta, Kibbidhāna y Uṇādi ingleses"),
        ("IEBH", "lo ya adjudicado en este repositorio: `recursos/verbo/ingles.json` y "
                 "los casos e inflexiones de `recursos/paradigmas/paradigmas.json`"),
        ("Ñāṇamoli", "«Grammatical Terms» (BPS 1994, rev. Ānandajoti 2014), "
                     "`recursos/glosario/terminos-nyanamoli.json`, con página"),
        ("propuesta (glosario-ingles.json)", "la propuesta inglesa, sin adjudicar, de "
                                             "los términos normativos de `comun/glosario.md`"),
        ("traducción", "ninguna de las anteriores da el término: se traduce el español "
                       "del Glosario y se dice"),
        ("remisión", "«v. …»: no hay nada que traducir"),
    ]
    for i, (f, q) in enumerate(filas, 1):
        L.append("| {0} | {1} | {2} | {3} |".format(i, f, q, cuenta.get(f, 0)))
    L.append("")
    L.append("## 2. Las entradas, lado a lado")
    L.append("")
    L.append("La columna «término» es la palabra inglesa del lema y de dónde sale. "
             "Las entradas con **nota** piden decisión y se repiten en el §3.")
    L.append("")
    L.append("| # | tanda | lema (p.) | español (manda) | inglés | término · fuente |")
    L.append("| ---: | :---: | --- | --- | --- | --- |")
    notas = []
    i = 0
    for clave, e in zip(claves, entradas):
        if clave not in borr:
            continue
        b = borr[clave]
        i += 1
        lema = e["pali"] + (" · {0}".format(e["homonimo"]) if e.get("homonimo") else "")
        refs = " · ".join(e.get("refs") or [])
        lema_celda = "**{0}** ({1}){2}".format(
            celda(lema), e.get("pagina"), (" · " + celda(refs)) if refs else "")
        term = celda(b.get("termino") or "")
        fuente = celda(b.get("fuente") or "")
        marca = " ⚑" if b.get("nota") else ""
        nt = b.get("tanda")
        firmada = bool(tandas.get(str(nt), {}).get("adjudicado")) if nt is not None else bool(ing.get("adjudicado"))
        L.append("| {0} | {1} | {2} | {3} | {4} | {5} — {6}{7} |".format(
            i, "{0} {1}".format(nt if nt is not None else "—", "✓" if firmada else "…"),
            lema_celda, celda(e.get("es")), celda(b.get("en")),
            term, fuente, marca))
        if b.get("nota"):
            notas.append((i, clave, b["nota"], firmada))
    L.append("")
    L.append("## 3. Lo que pide decisión")
    L.append("")
    abiertas = [n for n in notas if not n[3]]
    cerradas = [n for n in notas if n[3]]
    if not notas:
        L.append("Ninguna entrada lleva nota.")
    else:
        L.append("Cada nota dice qué fuente de más autoridad dice otra cosa que el "
                 "español del Glosario, o con qué choca el término. **La traducción "
                 "sigue siempre al Glosario**; lo que se decide aquí es si el inglés "
                 "publicado debe apartarse de él, y en qué.")
        L.append("")
        if not abiertas:
            L.append("Ninguna nota pendiente: las tandas redactadas están adjudicadas.")
            L.append("")
        for k, (i, clave, nota, _) in enumerate(abiertas, 1):
            L.append("{0}. **{1}** (#{2}): {3}".format(k, clave, i, nota))
        if cerradas:
            L.append("")
            L.append("### Notas de tandas ya adjudicadas (resueltas con la tanda; quedan de constancia)")
            L.append("")
            for k, (i, clave, nota, _) in enumerate(cerradas, 1):
                L.append("{0}. **{1}** (#{2}): {3}".format(k, clave, i, nota))
    L.append("")
    L.append("## 4. Lo que falta")
    L.append("")
    L.append("{0} entradas traducibles sin inglés todavía, de la {1} en adelante, en el "
             "orden del impreso.".format(
                 traducibles - hechas,
                 next((e["pali"] for c, e in zip(claves, entradas)
                       if c not in borr and e.get("es") and not e.get("remite_a")), "—")))
    L.append("")

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    open(DESTINO, "w", encoding="utf-8").write("\n".join(L))
    print("{0} entradas de {1} → {2} ({3} con nota)".format(
        hechas, total, os.path.relpath(DESTINO, RAIZ), len(notas)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
