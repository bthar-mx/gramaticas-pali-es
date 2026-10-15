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

y escribe site/recursos/particulas/index.html.

También escribe la guía para el estudiante, site/recursos/particulas/guia/,
con recursos/particulas/guia.md (el texto, tal cual: el español y el inglés,
separados por una sola línea «---») y recursos/particulas/guia-plantilla.html,
como la del análisis (generar_analisis.py). La página enlaza a ella, así que
sin guia.md no se publica nada. La fuente del texto está en
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
GUIA = os.path.join(RAIZ, "recursos", "particulas", "guia.md")
GUIA_PLANTILLA = os.path.join(RAIZ, "recursos", "particulas", "guia-plantilla.html")
GUIA_DESTINO = os.path.join(RAIZ, "site", "recursos", "particulas", "guia", "index.html")
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


def guia(version):
    """La guía para el estudiante: (html, fallos). Como la del análisis: el
    markdown pasa por el intérprete de prosa de generar_recurso.py, con «> cita»
    y `código` además; el texto no se toca. Español e inglés, separados por
    una sola línea «---»; el «# título» de cada parte es el h1."""
    import html as H
    import generar_recurso as R
    if not os.path.exists(GUIA):
        return None, ["falta " + os.path.relpath(GUIA, RAIZ)]
    txt = open(GUIA, encoding="utf-8").read().replace("\r\n", "\n")
    fallos = []
    if unicodedata.normalize("NFC", txt) != txt:
        fallos.append("guia.md: texto que no está en NFC")
    lineas = txt.split("\n")
    corte = [i for i, l in enumerate(lineas) if l.strip() == "---" and i > 0]
    if len(corte) != 1:
        return None, fallos + ["guia.md: el español y el inglés se separan con una sola "
                               "línea «---» (hay {0})".format(len(corte))]
    partes = {"es": lineas[:corte[0]], "en": lineas[corte[0] + 1:]}
    base = R.inline
    R.inline = lambda t: re.sub(r"`([^`]+)`", r"<code>\1</code>", base(t))

    def bloques(ls):
        out, i = [], 0
        while i < len(ls):
            if ls[i].startswith(">"):
                j = i
                while j < len(ls) and ls[j].startswith(">"):
                    j += 1
                cita = " ".join(re.sub(r"^>\s?", "", x).strip() for x in ls[i:j]).strip()
                out.append("<blockquote><p>{0}</p></blockquote>".format(R.inline(cita)))
                i = j
                continue
            j = i
            while j < len(ls) and not ls[j].startswith(">"):
                j += 1
            out.append(R.render(ls[i:j])[0])
            i = j
        h = "\n".join(x for x in out if x)
        return re.sub(r'<ul class="doc-lista">(?=<li>\d+[.)] )', '<ul class="doc-lista num">', h)

    cuerpos, titulos = {}, {}
    try:
        for lg, ls in partes.items():
            ls = list(ls)
            i = next((k for k, l in enumerate(ls) if l.strip()), None)
            if i is None or not re.match(r"^#\s+\S", ls[i].strip()):
                fallos.append("guia.md: la parte «{0}» no empieza por «# título»".format(lg))
                continue
            h1 = re.sub(r"^#\s+", "", ls[i].strip())
            del ls[i]
            cuerpos[lg] = bloques(ls)
            limpio = re.sub(r"[*_`]", "", h1)
            titulos[lg] = {"titulo": limpio, "h1": limpio, "h1_html": R.inline(h1)}
    finally:
        R.inline = base
    if fallos:
        return None, fallos
    pl = open(GUIA_PLANTILLA, encoding="utf-8").read()
    js = json.dumps({lg: {"titulo": t["titulo"], "h1": t["h1"]} for lg, t in titulos.items()},
                    ensure_ascii=False).replace("</", "<\\/")
    pl = re.sub(r"/\*__TITULOS__\*/.*?/\*__FIN__\*/", lambda m: js, pl, flags=re.S)
    for clave, valor in (("__ES_TITULO__", H.escape(titulos["es"]["titulo"])),
                         ("__ES_H1__", titulos["es"]["h1_html"]),
                         ("__VERSION__", version),
                         ("__ES__", cuerpos["es"]), ("__EN__", cuerpos["en"])):
        pl = pl.replace(clave, valor)
    return pl, []


def main():
    d = json.load(open(DATOS, encoding="utf-8"))
    fallos = verificar(d)
    pagina_guia, f_guia = guia(d["meta"]["version"])
    fallos += f_guia
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
    os.makedirs(os.path.dirname(GUIA_DESTINO), exist_ok=True)
    open(GUIA_DESTINO, "w", encoding="utf-8").write(
        cabecera.insertar(pagina_guia, "particulas-guia"))
    ej = sum(1 for x in d["entradas"] for b in x["bloques"] if b["tipo"] == "ej")
    nuevas = sum(1 for x in d["entradas"] if x.get("nuevo"))
    print("v{0} ({1}) · {2} entradas ({3} añadidas por IEBH) · {4} ejemplos · "
          "{5} erratas → {6} (y la guía)".format(meta["version"], meta["estado"]["es"], len(d["entradas"]),
                                     nuevas, ej, len(meta["erratas"]),
                                     os.path.relpath(DESTINO, RAIZ)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
