#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera «Comentarios y tratados de la escuela gramatical de Kaccāyana»
(borrador), en español e inglés en la misma página.

    python3 herramientas/generar_comentarios.py

Junta:

  docs/referencias/comentarios_kaccayana.md    la tabla en español (fuente)
  docs/referencias/kaccayana_commentaries.md   la tabla en inglés (fuente)
  recursos/comentarios/meta.json               versión, estado, atribución
  recursos/comentarios/enlaces.json            el material del propio sitio,
                                               que va delante de los enlaces
                                               externos en «Texto en línea»
  recursos/terminos/terminos.json              los globos (vía terminos.py)
  recursos/comentarios/plantilla.html          el maquetado y la lógica

y escribe site/recursos/comentarios/index.html.

Las dos tablas son la fuente y no se tocan: el generador las lee tal cual.
Antes de escribir verifica que las dos lenguas tengan las mismas secciones,
el mismo número de filas y la misma columna «Ñ» fila a fila; que cada entrada
de enlaces.json case con una fila y sólo con una; que los enlaces internos
apunten a páginas que existen en site/; que nada enlace a docs/fuentes/; y que
todo esté en NFC. Si algo no cuadra, no publica.
"""

import html
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generar_capitulo import CAPITULOS  # noqa: E402
import cabecera  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(RAIZ, "recursos", "comentarios")
PLANTILLA = os.path.join(DIR, "plantilla.html")
DESTINO = os.path.join(RAIZ, "site", "recursos", "comentarios", "index.html")


def nfc(x):
    if isinstance(x, str):
        return unicodedata.normalize("NFC", x) == x
    if isinstance(x, list):
        return all(nfc(i) for i in x)
    if isinstance(x, dict):
        return all(nfc(v) for v in x.values())
    return True


# ── Markdown en línea ───────────────────────────────────────────────────

def enlace(m):
    texto, url = m.group(1), m.group(2)
    return '<a href="{0}" rel="noopener" target="_blank">{1}</a>'.format(
        html.escape(url, quote=True), texto)


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'&lt;br\s*/?&gt;', '<br>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    # cursiva: *…* sin asteriscos dentro (la de la entradilla ya se quitó)
    t = re.sub(r'(?<![*\w])\*([^*\n]+?)\*(?![*\w])', r'<i>\1</i>', t)
    t = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', enlace, t)
    # URL desnuda (nota 5): enlazarla, fuera de los <a> ya puestos
    t = re.sub(r'(?<![">])(https?://[^\s<)]+?)([.,;]?)(?=\s|$|<)',
               lambda m: '<a href="{0}" rel="noopener" target="_blank">{0}</a>{1}'.format(m.group(1), m.group(2)), t)
    return t


def celdas(linea):
    return [c.strip() for c in linea.strip().strip('|').split('|')]


# ── Lectura de una tabla ────────────────────────────────────────────────

def leer(ruta):
    """{titulo, entradilla, secciones:[{titulo, tabla, cabecera, filas} | {titulo, prosa}]}"""
    lineas = open(ruta, encoding="utf-8").read().split("\n")
    doc = {"titulo": "", "entradilla": "", "secciones": []}
    sec = None
    for l in lineas:
        if l.startswith("# "):
            doc["titulo"] = l[2:].strip()
            continue
        if l.startswith("## "):
            sec = {"titulo": l[3:].strip(), "filas": [], "bloques": []}
            doc["secciones"].append(sec)
            continue
        if sec is None:
            if l.strip().startswith("*") and l.strip().endswith("*"):
                # la entradilla va entera en cursiva y lleva otra cursiva
                # dentro (*Reference Table…*): se quitan los asteriscos de
                # fuera y lo de dentro queda como cursiva normal.
                doc["entradilla"] = inline(l.strip()[1:-1])
            continue
        if l.startswith("|"):
            c = celdas(l)
            if all(re.fullmatch(r':?-{3,}:?', x) for x in c):
                continue
            if "cabecera" not in sec:
                sec["cabecera"] = c
            else:
                sec["filas"].append(c)
            continue
        if not l.strip():
            continue
        m = re.match(r'^(\d+)\.\s+(.*)$', l)
        if m:
            sec["bloques"].append({"t": "ol", "html": inline(m.group(2))})
        elif l.startswith("- "):
            sec["bloques"].append({"t": "ul", "html": inline(l[2:])})
        else:
            sec["bloques"].append({"t": "p", "html": inline(l)})
    return doc


def nombre(celda):
    """Nombre en negrita del comienzo de la celda «Obra», sin marcas."""
    m = re.match(r'\*\*(.+?)\*\*', celda)
    return m.group(1) if m else celda


# ── Material del propio sitio ───────────────────────────────────────────

def capitulos_publicados():
    caps = []
    for clave, meta in CAPITULOS.items():
        if meta.get("obra_slug", "kaccayana") != "kaccayana":
            continue
        slug = meta["slug"]
        es = os.path.join(RAIZ, "site", "kaccayana", slug, "index.html")
        en = os.path.join(RAIZ, "site", "en", "kaccayana", slug, "index.html")
        if os.path.exists(es):
            caps.append((slug, os.path.exists(en)))
    return caps


def propios_html(items, lengua, caps, fallos):
    trozos = []
    for it in items:
        if it.get("traduccion"):
            n = len(caps)
            if lengua == "es":
                rot = '<a href="../../kaccayana/">Traducción en este sitio</a>, caps. 1–{0}:'.format(n)
                nums = " · ".join('<a href="../../kaccayana/{0}/">{1}</a>'.format(s, i + 1)
                                  for i, (s, _) in enumerate(caps))
            else:
                faltan = [s for s, en in caps if not en]
                if faltan:
                    fallos.append("falta la edición inglesa de: " + ", ".join(faltan))
                rot = 'English edition on this site, chs. 1–{0}:'.format(n)
                nums = " · ".join('<a href="../../en/kaccayana/{0}/">{1}</a>'.format(s, i + 1)
                                  for i, (s, _) in enumerate(caps))
            nota = " ({0})".format(html.escape(it["nota"][lengua])) if it.get("nota") else ""
            trozos.append('<span class="propio">{0} {1}{2}</span>'.format(rot, nums, nota))
            continue
        rot = html.escape(it[lengua])
        if "href" in it:
            href = it["href"]
            destino = os.path.normpath(os.path.join(RAIZ, "site", "recursos", "comentarios", href, "index.html"))
            if not os.path.exists(destino):
                fallos.append("enlace interno sin página: " + href)
            trozos.append('<span class="propio"><a href="{0}">{1}</a></span>'.format(html.escape(href), rot))
        else:
            trozos.append('<span class="propio prep">{0}</span>'.format(rot))
    return trozos


# ── Principal ───────────────────────────────────────────────────────────

def main():
    meta = json.load(open(os.path.join(DIR, "meta.json"), encoding="utf-8"))
    enl = json.load(open(os.path.join(DIR, "enlaces.json"), encoding="utf-8"))
    docs = {l: leer(os.path.join(RAIZ, meta["fuentes"][l])) for l in ("es", "en")}
    fallos = []

    es, en = docs["es"], docs["en"]
    if len(es["secciones"]) != len(en["secciones"]):
        fallos.append("las dos lenguas no tienen las mismas secciones")
    caps = capitulos_publicados()
    usados = {e["fila"]: 0 for e in enl["filas"]}

    secciones = []
    n_filas = 0
    for i, (se, sn) in enumerate(zip(es["secciones"], en["secciones"])):
        s = {"id": "sec{0}".format(i + 1), "titulo": {"es": se["titulo"], "en": sn["titulo"]}}
        if se["filas"] or sn["filas"]:
            if len(se["filas"]) != len(sn["filas"]):
                fallos.append("{0}: {1} filas en español, {2} en inglés".format(
                    se["titulo"], len(se["filas"]), len(sn["filas"])))
            cab = {"es": se.get("cabecera", []), "en": sn.get("cabecera", [])}
            if len(cab["es"]) != 7 or len(cab["en"]) != 7:
                fallos.append("{0}: la tabla no tiene siete columnas".format(se["titulo"]))
            s["cabecera"] = cab
            s["filas"] = []
            for fe, fn in zip(se["filas"], sn["filas"]):
                n_filas += 1
                if len(fe) != 7 or len(fn) != 7:
                    fallos.append("fila {0}: no tiene siete celdas".format(n_filas))
                    continue
                # sólo los números de sección: «— (posterior a Ñ)» se traduce
                if re.sub(r'[^\d.,;–-]', '', fe[5]) != re.sub(r'[^\d.,;–-]', '', fn[5]):
                    fallos.append("fila {0} ({1}): «Ñ» distinta en español ({2}) e inglés ({3})".format(
                        n_filas, nombre(fe[0]), fe[5], fn[5]))
                fila = {"id": "o{0}".format(n_filas), "nombre": nombre(fe[0])}
                propios = []
                for e in enl["filas"]:
                    if fila["nombre"].startswith(e["fila"]):
                        usados[e["fila"]] += 1
                        propios = e["propios"]
                for lengua, f in (("es", fe), ("en", fn)):
                    c = [inline(x) for x in f]
                    # columna «Texto en línea»: lo del sitio, delante
                    p = propios_html(propios, lengua, caps, fallos)
                    if p:
                        c[6] = "<br>".join(p) + "<br>" + c[6]
                    fila[lengua] = c
                s["filas"].append(fila)
        else:
            s["prosa"] = {"es": se["bloques"], "en": sn["bloques"]}
        secciones.append(s)

    for k, v in usados.items():
        if v != 1:
            fallos.append("enlaces.json: «{0}» casa con {1} filas (debe ser una)".format(k, v))

    datos = {"meta": meta, "titulo": {"es": es["titulo"], "en": en["titulo"]},
             "entradilla": {"es": es["entradilla"], "en": en["entradilla"]},
             "secciones": secciones}
    try:
        import terminos
        # sólo lo que la página usa: la «fuente» interna de cada entrada (que
        # puede nombrar docs/fuentes/) no viaja a la página
        datos["terminos"] = [{k: t[k] for k in ("clave", "termino", "formas", "def", "ejemplo") if k in t}
                             for t in terminos.cargar(RAIZ)]
    except ValueError as err:
        fallos.append("glosario de los globos: {0}".format(err))

    plano = json.dumps(datos, ensure_ascii=False)
    if "docs/fuentes" in plano or "fuentes/" in re.sub(r'https?://\S+', '', plano):
        fallos.append("algo enlaza o nombra docs/fuentes/: no se publica nada de ahí")
    if not nfc(datos):
        fallos.append("texto que no está en NFC")

    if fallos:
        print("Los comentarios de Kaccāyana NO cuadran; no se publica:")
        for f in fallos[:25]:
            print("  ✗", f)
        return 1

    pl = open(PLANTILLA, encoding="utf-8").read()
    m = re.search(r'/\*__DATOS__\*/.*?/\*__FIN__\*/', pl, re.S)
    if not m:
        print("La plantilla no tiene el marcador /*__DATOS__*/…/*__FIN__*/")
        return 1
    js = json.dumps(datos, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    salida = pl[:m.start()] + js + pl[m.end():]
    salida = salida.replace("__VERSION_DATE__", meta["fecha"]).replace("__VERSION__", meta["version"])
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    open(DESTINO, "w", encoding="utf-8").write(
        cabecera.insertar(salida, "comentarios"))  # la barra común del sitio
    print("Comentarios de Kaccāyana v{0} ({1}) · {2} obras · {3} con material del sitio → {4}".format(
        meta["version"], meta["estado"], n_filas, sum(usados.values()), os.path.relpath(DESTINO, RAIZ)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
