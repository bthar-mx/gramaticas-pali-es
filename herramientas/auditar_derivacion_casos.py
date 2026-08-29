#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
¿Deriva el motor la lectura que el IEBH adjudicó, en cada caso?

    python3 herramientas/auditar_derivacion_casos.py
    python3 herramientas/auditar_derivacion_casos.py --md

`arnes_casos` comprueba que la lectura adjudicada **se afirme** —que salga
primera y con la señal debida—, y eso lo pasan los 82 casos. Es otra
pregunta la que hace este guion: si el motor sabe **derivarla**, es decir,
si sabe llegar de la forma escrita a esas dos (o tres) voces con una
escalera de aforismos. Varios casos entraron con la lectura adjudicada y la
escalera vacía, «pendiente de derivación», y eso está bien dicho en su nota
—una adjudicación no es una derivación—, pero conviene saber cuántos son y
por qué, y que la cuenta no crezca sin que nadie mire.

No es una puerta: no detiene nada. Es un termómetro, y devuelve 0 aunque
haya casos sin derivar. Lo que sí hace es separar los motivos, que es lo
único que convierte una lista en trabajo:

  · **pakati** — el caso dice que no hay operación (§23). El motor no
    propone cortes donde no pasa nada, y hace bien: no es un fallo.
  · **voz no atestiguada** — una de las voces adjudicadas no está en el
    léxico, así que `solucionar()` nunca puede proponer ese corte. No falta
    una regla: falta un lema. Es el caso de «kenacid», y es también el techo
    del plegado de tres voces, cuyo intermedio no tiene por qué ser palabra.
  · **el motor corta, pero no ahí** — la única clase que de verdad interroga
    a las reglas.
"""

import argparse
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from nuestro.solucionar_sandhis import (  # noqa: E402
    combinar_varias, cotejo, es_palabra, solucionar)

CASOS = os.path.join(RAIZ, "recursos", "solucionador", "casos-reportados.json")


def voces_de(caso):
    return [v.strip() for v in (caso.get("componentes") or "").split("+")
            if v.strip()]


def revisar(caso):
    """(estado, motivo, escalera). estado ∈ deriva | plegado | sin_derivar."""
    voces = voces_de(caso)
    if not caso.get("sandhi") or len(voces) < 2:
        return "no_aplica", "el caso no afirma sandhi", []

    esperada = [cotejo(v) for v in voces]

    if len(voces) == 2:
        r = solucionar(caso["forma"])
        for l in r["lecturas"]:
            if [cotejo(x) for x in (l.get("componentes") or [])] == esperada:
                return "deriva", "", list(l.get("pasos") or [])

    # Tres voces, o dos que el motor no corta ahí: se prueba el plegado.
    for cand, l in combinar_varias(voces):
        if cotejo(cand) == cotejo(caso["forma"]):
            return "plegado", "", list(l.get("pasos") or [])

    faltan = [v for v in voces if not es_palabra(v)]
    if faltan:
        return ("sin_derivar",
                "voz no atestiguada en el léxico: " + ", ".join(faltan), [])
    # «pakati» puede venir en la nota o en la fuente («adjudicado en el chat
    # (pakati, §23)»), así que se miran las dos.
    dice = ((caso.get("nota") or "") + " " + (caso.get("fuente") or "")).lower()
    if "pakati" in dice or "§23" in dice:
        return "sin_derivar", "pakati: no hay operación que derivar", []
    n = len(solucionar(caso["forma"])["lecturas"])
    return ("sin_derivar",
            "el motor corta, pero no ahí ({0} lecturas)".format(n), [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", action="store_true",
                    help="tabla markdown en vez de texto")
    a = ap.parse_args()

    datos = json.load(open(CASOS, encoding="utf-8"))
    casos = datos["casos"] if isinstance(datos, dict) and "casos" in datos \
        else datos

    filas = []
    for c in casos:
        estado, motivo, pasos = revisar(c)
        if estado == "no_aplica":
            continue
        filas.append((c["forma"], " + ".join(voces_de(c)), estado, motivo,
                      pasos))

    cuenta = {}
    for f in filas:
        cuenta[f[2]] = cuenta.get(f[2], 0) + 1
    tres = [f for f in filas if f[1].count("+") > 1]

    if a.md:
        print("| forma | voces adjudicadas | ¿deriva? | por qué no |")
        print("| --- | --- | --- | --- |")
        for forma, voces, estado, motivo, _ in filas:
            print("| {0} | {1} | {2} | {3} |".format(
                forma, voces,
                {"deriva": "sí", "plegado": "sí, plegando",
                 "sin_derivar": "**no**"}[estado], motivo or "—"))
        return 0

    print("DERIVACIÓN DE LAS LECTURAS ADJUDICADAS — {0} casos con sandhi"
          .format(len(filas)))
    print("  el motor la deriva de un corte : {0}".format(
        cuenta.get("deriva", 0)))
    print("  la deriva plegando combinar()  : {0}".format(
        cuenta.get("plegado", 0)))
    print("  sin derivar                    : {0}".format(
        cuenta.get("sin_derivar", 0)))
    print()
    print("Los de TRES voces ({0}):".format(len(tres)))
    for forma, voces, estado, motivo, pasos in tres:
        print("  · {0} = {1} — {2}{3}".format(
            forma, voces, estado, ": " + motivo if motivo else ""))
        for p in pasos:
            print("        {0}".format(p))
    sin = [f for f in filas if f[2] == "sin_derivar"]
    if sin:
        print()
        print("Sin derivar, por motivo:")
        for forma, voces, _, motivo, _ in sin:
            print("  · {0} = {1}".format(forma, voces))
            print("      {0}".format(motivo))
    return 0


if __name__ == "__main__":
    sys.exit(main())
