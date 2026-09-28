#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la referencia de los usos de las inflexiones (Kāraka).

    python3 herramientas/generar_casos.py

Junta dos cosas:

  recursos/casos/usos.json      los usos de las siete inflexiones según la
                                Rūpasiddhi (cap. 3), con la concordancia
                                Rūpasiddhi → Kaccāyana → Saddanīti
  recursos/casos/plantilla.html el maquetado y la lógica

y escribe site/recursos/casos/index.html.

Antes de escribir verifica los datos: identificadores únicos, toda cita de la
Rūpasiddhi presente en la concordancia, todo número de Kaccāyana dentro del
Kāraka-Kappa (§271–§315) o marcado «—», toda fuente del español dentro de la
lista declarada, ningún ejemplo sin pāḷi y todo el texto en NFC. Si algo no
cuadra, no publica.
"""

import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(RAIZ, "recursos", "casos", "usos.json")
PLANTILLA = os.path.join(RAIZ, "recursos", "casos", "plantilla.html")
DESTINO = os.path.join(RAIZ, "site", "recursos", "casos", "index.html")


def recorrer(u, cb, inf):
    cb(u, inf)
    for s in u.get("sub", []):
        recorrer(s, cb, inf)


def verificar(d):
    fallos = []
    conc = d["concordancia"]["rupasiddhi→kaccayana→saddaniti"]
    fuentes = set(d["es_fuente"])
    procs = set(d["procedencia"])
    vistos = set()
    for r, (k, _s) in conc.items():
        if k != "—" and not 271 <= int(k) <= 315:
            fallos.append("Rū. §{0} → Kacc. §{1}: fuera del Kāraka-Kappa".format(r, k))

    def nfc(t, donde):
        if isinstance(t, str) and unicodedata.normalize("NFC", t) != t:
            fallos.append("{0}: texto que no está en NFC".format(donde))

    def uno(u, inf):
        i = u["id"]
        if i in vistos:
            fallos.append("id repetido: " + i)
        vistos.add(i)
        for r in u.get("rupasiddhi", []):
            if r not in conc:
                fallos.append("{0}: Rū. §{1} sin concordancia".format(i, r))
        if u.get("es_fuente") and u["es_fuente"] not in fuentes:
            fallos.append("{0}: fuente desconocida «{1}»".format(i, u["es_fuente"]))
        for campo in ("pali", "es"):
            nfc(u.get(campo), i)
        for n, e in enumerate(u.get("ejemplos", [])):
            donde = "{0} ej. {1}".format(i, n + 1)
            if not e.get("pali", "").strip():
                fallos.append(donde + ": sin pāḷi")
            if e.get("es_fuente") and e["es_fuente"] not in fuentes:
                fallos.append("{0}: fuente desconocida «{1}»".format(donde, e["es_fuente"]))
            if e.get("es") and not e.get("es_fuente"):
                fallos.append(donde + ": traducción sin fuente")
            if e.get("procedencia") not in procs:
                fallos.append(donde + ": procedencia desconocida")
            for campo in ("pali", "es", "nota", "canon"):
                nfc(e.get(campo), donde)
    for inf in d["inflexiones"]:
        recorrer(inf, uno, inf["id"])
    return fallos


def contar(d):
    usos = ejemplos = 0

    def c(u, _):
        nonlocal usos, ejemplos
        usos += 1
        ejemplos += len(u.get("ejemplos", []))
    for inf in d["inflexiones"]:
        for s in inf["sub"]:
            recorrer(s, c, inf["id"])
    tope = sum(len(inf["sub"]) for inf in d["inflexiones"])
    return tope, usos, ejemplos


def main():
    d = json.load(open(DATOS, encoding="utf-8"))
    fallos = verificar(d)
    if fallos:
        print("usos.json NO cuadra; no se publica:")
        for f in fallos[:20]:
            print("  ✗", f)
        return 1
    d["_version"] = d["version"]
    d["_version_fecha"] = d["fecha"]
    d["_version_nota"] = d.get("nota_version", "")

    pl = open(PLANTILLA, encoding="utf-8").read()
    m = re.search(r'/\*__DATOS__\*/.*?/\*__FIN__\*/', pl, re.S)
    if not m:
        print("La plantilla no tiene el marcador /*__DATOS__*/…/*__FIN__*/")
        return 1
    datos = json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = pl[:m.start()] + datos + pl[m.end():]
    html = html.replace("__VERSION_DATE__", d["fecha"]).replace("__VERSION__", d["version"])
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    open(DESTINO, "w", encoding="utf-8").write(html)
    tope, usos, ejemplos = contar(d)
    print("v{0} ({1}) · {2} inflexiones · {3} usos ({4} con subdivisiones) · "
          "{5} ejemplos → {6}".format(d["version"], d.get("estado", ""),
                                      len(d["inflexiones"]), tope, usos, ejemplos,
                                      os.path.relpath(DESTINO, RAIZ)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
