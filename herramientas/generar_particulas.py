#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la referencia de las partículas (nipāta).

    python3 herramientas/generar_particulas.py

Junta dos cosas:

  recursos/particulas/particulas.json  el documento «Partículas (Nipāta)» de
                                       Bhikkhu Nandisena (2013), con las
                                       erratas evidentes corregidas y su
                                       inglés (borrador)
  recursos/particulas/plantilla.html   el maquetado y la lógica

y escribe site/recursos/particulas/index.html. La fuente del texto está en
docs/fuentes/nandisena/particulas.md; la revisión, en docs/privado/nipatas/.

Antes de escribir verifica los datos: identificadores únicos, toda entrada
con su cabecera en los dos idiomas, todo ejemplo con pāḷi, toda llamada [^n]
con su nota, casos dentro de la lista y todo el texto en NFC. Si algo no
cuadra, no publica.
"""

import json
import os
import re
import sys
import unicodedata
import cabecera  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(RAIZ, "recursos", "particulas", "particulas.json")
PLANTILLA = os.path.join(RAIZ, "recursos", "particulas", "plantilla.html")
DESTINO = os.path.join(RAIZ, "site", "recursos", "particulas", "index.html")
CASOS = {"1", "1v", "2", "3", "4", "5", "6", "7"}


def verificar(d):
    fallos = []
    vistos = set()

    def nfc(t, donde):
        if isinstance(t, str) and unicodedata.normalize("NFC", t) != t:
            fallos.append("{0}: texto que no está en NFC".format(donde))

    for x in d["entradas"]:
        i = x["id"]
        if i in vistos:
            fallos.append("id repetido: " + i)
        vistos.add(i)
        for l in ("es", "en"):
            if not x["cab"].get(l, "").strip():
                fallos.append("{0}: cabecera sin {1}".format(i, l))
            nfc(x["cab"].get(l), i)
        for c in x["caso"]:
            if c not in CASOS:
                fallos.append("{0}: caso desconocido «{1}»".format(i, c))
        llamadas = set()
        for n, b in enumerate(x["bloques"]):
            donde = "{0} bloque {1}".format(i, n + 1)
            if b["tipo"] == "ej" and not b.get("pali", "").strip():
                fallos.append(donde + ": ejemplo sin pāḷi")
            for campo in ("pali", "es", "en", "ref"):
                nfc(b.get(campo), donde)
                llamadas |= set(re.findall(r"\[\^(\d+)\]", b.get(campo) or ""))
        for l in ("es", "en"):
            llamadas |= set(re.findall(r"\[\^(\d+)\]", x["cab"].get(l, "")))
        notas = {n["n"] for n in x["notas"]}
        for n in sorted(llamadas - notas):
            fallos.append("{0}: llamada [^{1}] sin nota".format(i, n))
    if not d["meta"].get("atribucion", {}).get("es"):
        fallos.append("meta: falta la atribución")
    return fallos


def main():
    d = json.load(open(DATOS, encoding="utf-8"))
    fallos = verificar(d)
    if fallos:
        print("particulas.json NO cuadra; no se publica:")
        for f in fallos[:20]:
            print("  ✗", f)
        return 1
    pl = open(PLANTILLA, encoding="utf-8").read()
    m = re.search(r'/\*__DATOS__\*/.*?/\*__FIN__\*/', pl, re.S)
    if not m:
        print("La plantilla no tiene el marcador /*__DATOS__*/…/*__FIN__*/")
        return 1
    datos = json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = pl[:m.start()] + datos + pl[m.end():]
    meta = d["meta"]
    html = html.replace("__VERSION_DATE__", meta["fecha"]).replace("__VERSION__", meta["version"])
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    open(DESTINO, "w", encoding="utf-8").write(cabecera.insertar(html, "particulas"))
    ej = sum(1 for x in d["entradas"] for b in x["bloques"] if b["tipo"] == "ej")
    nuevas = sum(1 for x in d["entradas"] if x.get("nuevo"))
    print("v{0} ({1}) · {2} entradas ({3} añadidas por IEBH) · {4} ejemplos · "
          "{5} erratas → {6}".format(meta["version"], meta["estado"]["es"], len(d["entradas"]),
                                     nuevas, ej, len(meta["erratas"]),
                                     os.path.relpath(DESTINO, RAIZ)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
