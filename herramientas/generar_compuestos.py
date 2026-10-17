#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la referencia de los compuestos (samāsa).

    python3 herramientas/generar_compuestos.py

Junta:

  recursos/compuestos/compuestos.json    «Compuesto (samāsa)» de Bhikkhu
                                         Nandisena (2004–2005), en revisión
                                         por IEBH; lo escribe
                                         herramientas/compuestos_a_json.py a
                                         partir del texto (congelado o revisado)
  recursos/compuestos/plantilla.html     el maquetado y la lógica: pestañas de
                                         las seis clases, resoluciones
                                         interlineales, búsqueda, «Practicar» y
                                         «¿Qué compuesto es?»
  recursos/compuestos/guia.md            la guía para el estudiante (español e
  recursos/compuestos/guia-plantilla.html  inglés, separados por una sola «---»)

y escribe site/recursos/compuestos/index.html y su guía,
site/recursos/compuestos/guia/index.html, las dos con la cabecera común.

Antes de escribir verifica los datos: identificadores únicos, las seis clases,
todo el texto en NFC, toda llamada [^n] con su nota, todo bloque con texto
español, todo «Kacc. §N» con su página de sutta (site/s/N/) y la atribución.
Si algo no cuadra, no publica.
"""

import json
import os
import re
import sys
import unicodedata

import cabecera  # noqa: E402
import generar_indeclinables as GI  # noqa: E402  (la guía se arma igual)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(RAIZ, "recursos", "compuestos")
DATOS = os.path.join(DIR, "compuestos.json")
PLANTILLA = os.path.join(DIR, "plantilla.html")
DESTINO = os.path.join(RAIZ, "site", "recursos", "compuestos", "index.html")
GUIA = os.path.join(DIR, "guia.md")
GUIA_PLANTILLA = os.path.join(DIR, "guia-plantilla.html")
GUIA_DESTINO = os.path.join(RAIZ, "site", "recursos", "compuestos", "guia", "index.html")
SUTTAS = os.path.join(RAIZ, "site", "s")

CLASES = ["abyayibhava", "kammadharaya", "digu", "tappurisa", "bahubbihi", "dvanda"]
TIPOS = {"p", "h", "lista", "tabla", "paradigma", "interlineal", "ejemplos"}


def textos_es(b):
    """Todo el español de un bloque, para comprobar que lo tiene."""
    out = []

    def rec(x, k=None):
        if isinstance(x, dict):
            for kk, v in x.items():
                if kk == "es" and isinstance(v, str):
                    out.append(v)
                else:
                    rec(v, kk)
        elif isinstance(x, list):
            for v in x:
                rec(v, k)
        elif isinstance(x, str) and k in ("p", "compuesto", "resolucion"):
            out.append(x)
    rec(b)
    return out


def cuenta(d):
    """(clases, subtipos, compuestos resueltos) para la insignia y la portada."""
    sub = sum(1 for c in d["clases"] for b in c["bloques"] if b["tipo"] == "h" or b.get("def"))
    # como el banco de la práctica de la plantilla: sin repetir el mismo
    # compuesto con la misma resolución dentro de una clase (pavaddhaṃ, L0535 y L0543)
    vistos = set()
    for c in d["clases"]:
        for b in c["bloques"]:
            if b["tipo"] == "interlineal" and b.get("compuesto"):
                res = " ".join(t["p"] for t in b["viggaha"] if not re.match(r"^[,;.]+$", t["p"]))
                vistos.add((c["id"], b["compuesto"], res))
            elif b["tipo"] == "ejemplos":
                for f in b["filas"]:
                    rs = f["resolucion"].split("\n")
                    for j, x in enumerate(f["compuesto"].split("\n")):
                        if x.strip():
                            vistos.add((c["id"], x, rs[j] if j < len(rs) else ""))
    return len(d["clases"]), sub, len(vistos)


def verificar(d):
    fallos = []
    vistos = set()
    if [c["id"] for c in d.get("clases", [])] != CLASES:
        fallos.append("las clases no son las seis, en su orden: " +
                      ", ".join(c["id"] for c in d.get("clases", [])))
    s = json.dumps(d, ensure_ascii=False)
    if unicodedata.normalize("NFC", s) != s:
        fallos.append("hay texto que no está en NFC")
    if "ṁ" in s:
        fallos.append("queda algún «ṁ» (debe ser «ṃ»)")
    llamadas = set(re.findall(r"\[\^(\w+)\]", s))
    for n in sorted(llamadas - set(d.get("notas", {}))):
        fallos.append("llamada [^{0}] sin nota".format(n))
    for n, v in d.get("notas", {}).items():
        if not (v.get("es") or "").strip():
            fallos.append("nota {0} sin texto".format(n))
    sec = [("intro", d["intro"])] + [(c["id"], c["bloques"]) for c in d["clases"]]
    for donde, bs in sec:
        for b in bs:
            ref = "{0} L{1}".format(donde, b.get("L", "?"))
            if b.get("tipo") not in TIPOS:
                fallos.append("{0}: tipo de bloque desconocido «{1}»".format(ref, b.get("tipo")))
            i = b.get("id")
            if not i:
                fallos.append(ref + ": bloque sin id")
            elif i in vistos:
                fallos.append(ref + ": id repetido " + i)
            vistos.add(i)
            if not any(t.strip() for t in textos_es(b)):
                fallos.append(ref + ": bloque sin texto en español")
            if b.get("iebh") and not b.get("fuente"):
                fallos.append(ref + ": bloque del IEBH sin fuente")
    # los suttas citados tienen su página
    for n in sorted({int(x) for x in re.findall(r"Kacc?\. ?§(\d+)", s)} |
                    {k for c in d["clases"] for k in c.get("kacc", [])}):
        if not os.path.exists(os.path.join(SUTTAS, str(n), "index.html")):
            fallos.append("Kacc. §{0}: no hay site/s/{0}/".format(n))
    m = d.get("meta", {})
    for k in ("version", "fecha", "estado", "atribucion"):
        if not m.get(k):
            fallos.append("meta: falta «{0}»".format(k))
    if not (m.get("atribucion") or {}).get("es"):
        fallos.append("meta: falta la atribución")
    return fallos


def guia(version, fecha):
    """La guía, con el mismo intérprete que la de los indeclinables."""
    viejo = (GI.GUIA, GI.GUIA_PLANTILLA)
    GI.GUIA, GI.GUIA_PLANTILLA = GUIA, GUIA_PLANTILLA
    try:
        return GI.guia(version, fecha)
    finally:
        GI.GUIA, GI.GUIA_PLANTILLA = viejo


def main():
    if not os.path.exists(DATOS):
        print("falta {0}: ejecute antes herramientas/compuestos_a_json.py".format(
            os.path.relpath(DATOS, RAIZ)))
        return 1
    d = json.load(open(DATOS, encoding="utf-8"))
    fallos = verificar(d)
    pagina_guia, f_guia = guia(d["meta"]["version"], d["meta"]["fecha"])
    fallos += f_guia
    if fallos:
        print("compuestos NO cuadra; no se publica:")
        for f in fallos[:25]:
            print("  ✗", f)
        if len(fallos) > 25:
            print("  … y {0} más".format(len(fallos) - 25))
        return 1
    pl = open(PLANTILLA, encoding="utf-8").read()
    m = re.search(r"/\*__DATOS__\*/.*?/\*__FIN__\*/", pl, re.S)
    if not m:
        print("La plantilla no tiene el marcador /*__DATOS__*/…/*__FIN__*/")
        return 1
    datos = json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = pl[:m.start()] + datos + pl[m.end():]
    meta = d["meta"]
    html = html.replace("__VERSION_DATE__", meta["fecha"]).replace("__VERSION__", meta["version"])
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    open(DESTINO, "w", encoding="utf-8").write(cabecera.insertar(html, "compuestos"))
    os.makedirs(os.path.dirname(GUIA_DESTINO), exist_ok=True)
    open(GUIA_DESTINO, "w", encoding="utf-8").write(
        cabecera.insertar(pagina_guia, "compuestos-guia"))
    n_cl, n_sub, n_ej = cuenta(d)
    iebh = sum(1 for c in d["clases"] for b in c["bloques"] if b.get("iebh"))
    print("v{0} ({1}) · {2} clases · {3} subtipos · {4} compuestos resueltos · {5} notas"
          "{6} → {7} (y la guía)".format(
              meta["version"], meta["estado"]["es"], n_cl, n_sub, n_ej, len(d["notas"]),
              " · {0} bloques del IEBH".format(iebh) if iebh else "",
              os.path.relpath(DESTINO, RAIZ)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
