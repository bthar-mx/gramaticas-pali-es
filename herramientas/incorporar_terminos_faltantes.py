#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplica los veredictos del IEBH sobre los términos que faltaban en el glosario.

    python3 herramientas/incorporar_terminos_faltantes.py [docs/glosario/veredictos-terminos-faltantes.json]

Lee docs/glosario/terminos-faltantes.json (la cosecha, con las propuestas) y
el archivo de veredictos que exporta el formulario
docs/glosario/terminos-faltantes.html. Por cada término ACEPTADO:

  · añade una fila al final de la tabla de comun/glosario.md, con el español
    del IEBH si lo escribió y el propuesto si no, la nota, y en «Fijado en»
    «cosecha s. 57» y, tras una raya, los suttas donde el término aparece en
    Kaccāyana, la Rūpasiddhi y el Nyāsa, buscados por referenciar_terminos.py
    (si no se encuentra en ninguno, se deja la referencia propuesta por la
    cosecha, marcada como tal);
  · añade la clave a recursos/glosario/glosario-ingles.json con el inglés del
    IEBH si lo escribió y el propuesto si no.

Los rechazados y los no decididos no tocan nada. El guion no repite: si el
lema ya está en comun/glosario.md, avisa y lo salta. Después hay que correr
generar_todo.py, que es quien los publica en la página del glosario.
"""
import json, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import referenciar_terminos as REF

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COSECHA = os.path.join(RAIZ, "docs", "glosario", "terminos-faltantes.json")
VEREDICTOS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, "docs", "glosario", "veredictos-terminos-faltantes.json")
NORMA = os.path.join(RAIZ, "comun", "glosario.md")
INGLES = os.path.join(RAIZ, "recursos", "glosario", "glosario-ingles.json")


def lema_norma(termino, tipo):
    """El lema tal como va en comun/glosario.md: los sufijos, sin la palabra
    «sufijo»; las designaciones, sin «(saññā)»."""
    if tipo == "sufijo":
        return termino.replace("sufijo ", "", 1)
    if tipo == "designación":
        return termino.replace(" (saññā)", "")
    return termino


def main():
    if not os.path.exists(VEREDICTOS):
        print("No hay veredictos: " + os.path.relpath(VEREDICTOS, RAIZ))
        return 1
    cosecha = {d["id"]: d for d in json.load(open(COSECHA, encoding="utf-8"))}
    v = json.load(open(VEREDICTOS, encoding="utf-8"))
    veredictos = v.get("veredictos", v)
    quien = v.get("adjudicado_por", "IEBH")
    fecha = v.get("fecha", "")

    norma = open(NORMA, encoding="utf-8").read()
    ya = set(re.sub(r"[*_]", "", m.group(1)).strip()
             for m in re.finditer(r"^\|\s*(\*[^|]+\*)\s*\|", norma, flags=re.M))
    ing = json.load(open(INGLES, encoding="utf-8"))

    filas, puestos, saltados, sin_sutta = [], [], [], []
    for clave, vd in veredictos.items():
        if vd.get("veredicto") != "acepta" or clave not in cosecha:
            continue
        d = cosecha[clave]
        lema = lema_norma(d["termino"], d["tipo"])
        if lema in ya:
            saltados.append(lema)
            continue
        es = (vd.get("es") or "").strip() or d["es"]
        en = (vd.get("en") or "").strip() or d["en"]
        nota = (vd.get("nota") or "").strip()
        ref = d.get("ref") or ""
        fuentes = " · ".join("{0} {1}".format(k, n) for k, n in (d.get("fuentes") or {}).items())
        celda_nota = nota or d.get("comentario", "")
        celda_nota = celda_nota.replace("|", "／").replace("\n", " ")
        hallado = REF.formatear(REF.buscar(d["termino"], d["tipo"]))
        if not hallado:
            sin_sutta.append(lema)
            hallado = "sin sutta localizado; la cosecha proponía: " + ref.replace("|", "／") if ref else "sin sutta localizado"
        fijado = "cosecha s. 57, {0} {1}".format(quien, fecha).strip() + " — " + hallado
        filas.append("| *{0}* | {1} | {2} | {3} |".format(
            lema, es.replace("|", "／"), celda_nota, fijado))
        ing["ingles"][lema] = en
        puestos.append(lema)
        ya.add(lema)

    if not puestos:
        print("Nada que incorporar (aceptados nuevos: 0; ya en la norma: {0}).".format(len(saltados)))
        return 0

    # Las filas nuevas van DENTRO de la tabla, a continuación de la última
    # fila (la tabla acaba donde empieza «## En discusión»); la marca de
    # procedencia va en la celda «Fijado en», no en un comentario que
    # partiría la tabla en dos.
    lineas = norma.split("\n")
    ultima = max(i for i, l in enumerate(lineas) if l.startswith("|"))
    lineas[ultima + 1:ultima + 1] = filas
    norma = "\n".join(lineas)
    norma = unicodedata.normalize("NFC", norma)
    open(NORMA, "w", encoding="utf-8").write(norma)
    json.dump(ing, open(INGLES, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(INGLES, "a", encoding="utf-8").write("\n")
    print("Incorporados {0}: {1}".format(len(puestos), ", ".join(puestos)))
    # Las notas del IEBH en las filas aceptadas se enseñan aquí para que se
    # lean antes de dar el trabajo por hecho: pueden pedir un cambio que el
    # guion no sabe hacer («mejor X en inglés»).
    con_nota = [(k, vd["nota"]) for k, vd in veredictos.items()
                if vd.get("veredicto") == "acepta" and (vd.get("nota") or "").strip()]
    if con_nota:
        print("NOTAS DEL IEBH en filas aceptadas, léanse ({0}):".format(len(con_nota)))
        for k, n in con_nota:
            print("  · {0}: {1}".format(k, n.strip()))
    if sin_sutta:
        print("SIN SUTTA LOCALIZADO en Kacc./Rū./Nyāsa (queda la referencia de la cosecha): " + ", ".join(sin_sutta))
    if saltados:
        print("Ya estaban en comun/glosario.md y se saltaron: " + ", ".join(saltados))
    print("Ahora: python3 herramientas/generar_todo.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
