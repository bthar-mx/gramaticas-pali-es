#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Escribe el cotejo lado a lado del inglés de /recursos/paradigmas/, para que
el IEBH lo firme.

    python3 herramientas/generar_ingles_paradigmas.py

Lee recursos/paradigmas/paradigmas.json (el español, que manda) y
recursos/paradigmas/ingles.json (el borrador inglés) y escribe
docs/paradigmas/ingles-por-adjudicar.md con las dos columnas enfrentadas.

Las FORMAS pāḷi no salen aquí: no se traducen, y por tanto no hay nada que
adjudicar en ellas. Lo que sale es la prosa: la glosa de cada paradigma, el
subtítulo, la familia, las notas de transcripción, el texto de los sufijos y
el uso y los ejemplos de cada sufijo.

Adjudicar es poner «adjudicado»: true en ingles.json, con «adjudicado_por» y
«fecha». Hasta entonces generar_paradigmas.py comprueba el borrador pero no
lo publica, y el modo inglés de la página muestra el español.
"""

import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(RAIZ, "recursos", "paradigmas", "paradigmas.json")
INGLES = os.path.join(RAIZ, "recursos", "paradigmas", "ingles.json")
DESTINO = os.path.join(RAIZ, "docs", "paradigmas", "ingles-por-adjudicar.md")

sys.path.insert(0, os.path.join(RAIZ, "herramientas"))
from generar_paradigmas import verificar_ingles  # noqa: E402


def celda(t):
    """Una celda de tabla markdown: sin barras sueltas ni saltos."""
    return (t or "").replace("|", "\\|").replace("\n", " ")


def main():
    datos = json.load(open(DATOS, encoding="utf-8"))
    ing = json.load(open(INGLES, encoding="utf-8"))

    fallos = verificar_ingles(datos, ing)
    if fallos:
        print("El borrador inglés NO cuadra con los datos; no se escribe:")
        for f in fallos[:20]:
            print("  ✗", f)
        return 1

    E = ing["paradigmas"]
    L = []
    A = L.append
    firmado = bool(ing.get("adjudicado"))
    A("# El inglés de los paradigmas" + ("" if firmado else ", por adjudicar"))
    A("")
    A("*Redactado en la sesión 35 (2026-08-29). El español manda: es lo que")
    A("transcriben los documentos del IEBH.*")
    A("")
    if firmado:
        A("**Adjudicado por {0} el {1}.** El inglés de esta columna es ya el"
          .format(ing.get("adjudicado_por") or "?", ing.get("fecha") or "?"))
        A("que publica la página: `generar_paradigmas.py` lo inyecta y el pie")
        A("en inglés lo acredita. Este documento queda como el cotejo con el")
        A("que se firmó, y como el sitio donde revisarlo si algo hubiera que")
        A("enmendar.")
    else:
        A("El inglés de esta columna lo redactó el chat y **no está")
        A("adjudicado**. Mientras `adjudicado` sea `false` en")
        A("`recursos/paradigmas/ingles.json`, `generar_paradigmas.py` comprueba")
        A("el borrador pero **no lo publica**: el modo inglés de la página")
        A("muestra el español, y el pie en inglés lo dice. Firmarlo es poner")
        A("`\"adjudicado\": true` con `adjudicado_por` y `fecha`.")
    A("")
    A("Las **formas pāḷi no están aquí**: no se traducen, y no hay nada que")
    A("adjudicar en ellas. Lo que sigue es sólo la prosa.")
    A("")

    A("## 1. La glosa de cada paradigma")
    A("")
    A("| Código | Español (manda) | Inglés (borrador) |")
    A("| --- | --- | --- |")
    for p in datos["paradigmas"]:
        A("| {0} | {1} | {2} |".format(
            celda(p["codigo"]), celda(p["paradigma"]),
            celda(E[p["codigo"]]["paradigma"])))
    A("")

    subt = [p for p in datos["paradigmas"] if p.get("subtitulo")]
    A("## 2. Los subtítulos ({0})".format(len(subt)))
    A("")
    A("| Código | Español | Inglés |")
    A("| --- | --- | --- |")
    for p in subt:
        A("| {0} | {1} | {2} |".format(
            celda(p["codigo"]), celda(p["subtitulo"]),
            celda(E[p["codigo"]].get("subtitulo"))))
    A("")

    fam = [p for p in datos["paradigmas"] if p.get("familia")]
    A("## 3. Las familias ({0})".format(len(fam)))
    A("")
    for p in fam:
        A("**{0}**".format(p["codigo"]))
        A("")
        A("- ES — {0}".format(p["familia"]))
        A("- EN — {0}".format(E[p["codigo"]].get("familia")))
        A("")

    notas = [p for p in datos["paradigmas"] if p.get("notas")]
    A("## 4. Las notas de transcripción ({0} entradas)".format(len(notas)))
    A("")
    for p in notas:
        A("**{0}**".format(p["codigo"]))
        A("")
        for i, n in enumerate(p["notas"]):
            A("- ES — {0}".format(n))
            A("- EN — {0}".format(E[p["codigo"]]["notas"][i]))
            A("")

    txt = [p for p in datos["paradigmas"] if p.get("texto")]
    if txt:
        A("## 5. El texto de los sufijos")
        A("")
        for p in txt:
            A("- ES — {0}".format(p["texto"]))
            A("- EN — {0}".format(E[p["codigo"]].get("texto")))
            A("")

    det = [p for p in datos["paradigmas"] if p.get("detalle")]
    if det:
        A("## 6. El uso y los ejemplos de cada sufijo")
        A("")
        A("La **referencia** (§248, Rū. §260…) no se traduce: es la cita, y es")
        A("la misma en los dos idiomas.")
        A("")
        for p in det:
            por = {d["s"]: d for d in E[p["codigo"]]["detalle"]}
            for d in p["detalle"]:
                usos = d.get("usos") or [d]
                for i, u in enumerate(usos):
                    un = por[d["s"]]["usos"][i]
                    A("**‘{0}’** — {1}".format(d["s"], u.get("ref", "")))
                    A("")
                    A("- ES — {0}".format(u["uso"]))
                    A("- EN — {0}".format(un["uso"]))
                    A("- ES — {0}".format(", ".join(u["ej"])))
                    A("- EN — {0}".format(", ".join(un["ej"])))
                    A("")

    A("## 7. Lo que hay que mirar con lupa")
    A("")
    A("Cuatro sitios donde el borrador tomó una decisión y no una traducción:")
    A("")
    A("1. **«brahma (dios)» → «brahma (god)»**. El documento dice «dios»; en")
    A("   inglés «god» con minúscula, no «Brahmā», para no cambiar lo que la")
    A("   edición dice.")
    A("2. **«jambū (yambo)» → «jambū (rose-apple tree)»**. El español nombra el")
    A("   árbol con su nombre castellano; el inglés no tiene uno de una sola")
    A("   palabra que se entienda.")
    A("3. **El género gramatical se pierde**. «sabba (todo)» y «sabba (toda)»")
    A("   dan las dos «sabba (all)»; «ta (ese)» y «ta (esa)», las dos «ta")
    A("   (that)». El subtítulo —masculine, feminine, neuter— sigue")
    A("   distinguiéndolas, así que no se pierde nada en la página.")
    A("4. **«con el visto bueno de Angel»** aparece en TRES notas publicadas")
    A("   (N-Ā1, #1 y la segunda de Sufijos-Inflexiones). La regla del")
    A("   proyecto es que la atribución pública dice IEBH, nunca «Angel»: el")
    A("   inglés pone «with the approval of the IEBH», y **el español habría")
    A("   que corregirlo igual**. No se ha tocado: es la edición, y la decisión")
    A("   es del IEBH.")
    A("")

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    open(DESTINO, "w", encoding="utf-8").write("\n".join(L))

    n_usos = sum(len(d.get("usos") or [d])
                 for p in det for d in p["detalle"])
    print("{0} glosas · {1} subtítulos · {2} familias · {3} notas · "
          "{4} usos de sufijo → {5}".format(
              len(datos["paradigmas"]), len(subt), len(fam),
              sum(len(p["notas"]) for p in notas), n_usos,
              os.path.relpath(DESTINO, RAIZ)))
    print("  estado: {0}".format(
        "ADJUDICADO por {0} ({1})".format(ing.get("adjudicado_por") or "?",
                                          ing.get("fecha") or "?")
        if ing.get("adjudicado") else "SIN adjudicar — no se publica"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
