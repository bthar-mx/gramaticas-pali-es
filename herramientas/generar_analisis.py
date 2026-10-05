#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera «Análisis de los suttas de Kaccāyana según la Visuddhāyuṃ
Kaccāyana-ṭīkā» (borrador), en español e inglés en la misma página.

    python3 herramientas/generar_analisis.py

Junta:

  recursos/analisis/meta.json          versión, estado y cita del libro
  recursos/analisis/datos/NN-*.json    un archivo por capítulo: clase de
                                          sutta según el libro, aṅga,
                                          funciones (kāriyī / kāriya /
                                          nimitta, saññā / saññī, visaya /
                                          visayī), ejemplo marcado, notas y
                                          página del PDF; notas en es/en
  kaccayana/0N-*.md                       el texto pāḷi de cada aforismo
  recursos/analisis/plantilla.html     el maquetado y la lógica

y escribe site/recursos/analisis/index.html, más preguntar.json al lado: lo
que el botón «Preguntar» le pasa al modelo (v. worker/index.js) — cada fila con
lo que la página enseña de ella y, del glosario, sólo las entradas que la fila
usa y sólo los campos del globo. La «fuente» de cada término no sale nunca.

Antes de escribir verifica que cada capítulo tenga todos sus aforismos, sin
huecos ni sobrantes; que la página del PDF esté dentro del capítulo y no
retroceda; que las marcas del ejemplo ({k|…} {n|…} {r|…} {x|…} {kx|…} {nx|…})
estén bien formadas; que cada nimitta lleve su caso; y que todo esté en NFC.
Si algo no cuadra, no publica.

También escribe la guía para el estudiante, site/recursos/analisis/guia/,
con recursos/analisis/guia.md (el texto, tal cual: el español y el inglés,
separados por «---» o por el «# título» inglés) y recursos/analisis/guia-plantilla.html. La página del
análisis enlaza a ella, así que sin guia.md no se publica nada.
"""

import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generar_clasificacion import leer_md  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(RAIZ, "recursos", "analisis")
PLANTILLA = os.path.join(DIR, "plantilla.html")
DESTINO = os.path.join(RAIZ, "site", "recursos", "analisis", "index.html")
PREGUNTAR = os.path.join(RAIZ, "site", "recursos", "analisis", "preguntar.json")
GUIA = os.path.join(DIR, "guia.md")
GUIA_PLANTILLA = os.path.join(DIR, "guia-plantilla.html")
GUIA_DESTINO = os.path.join(RAIZ, "site", "recursos", "analisis", "guia", "index.html")

ROLES = {"kāriyī", "kāriya", "nimitta", "saññā", "saññī", "visaya", "visayī", "visesana"}
# «visesana» como función propia: cuando el libro lo enumera suelto (§221, «စ-ဝိသေသန»)
# y no se sabe a qué palabra califica (v0.7).
CASOS = {"7", "5", "3", "5+7"}
MARCA = re.compile(r"\{(k|n|r|x|kx|nx)\|([^{}|]+)\}")
# Las funciones de la columna llevan globo por su nombre (RK de la plantilla).
RK = {"kāriyī": "kariyi", "kāriya": "kariya", "nimitta": "nimitta", "saññā": "sannaroles",
      "saññī": "sannaroles", "visaya": "visaya", "visayī": "visaya"}
CITA = re.compile(r"«[^»]*»|“[^”]*”")


def nfc(x):
    if isinstance(x, str):
        return unicodedata.normalize("NFC", x) == x
    if isinstance(x, list):
        return all(nfc(i) for i in x)
    if isinstance(x, dict):
        return all(nfc(v) for v in x.values())
    return True


def verificar(cap, textos):
    fallos = []
    rango = set(range(cap["desde"], cap["hasta"] + 1))
    ns = [s["n"] for s in cap["suttas"]]
    if set(ns) != rango or len(ns) != len(rango):
        fallos.append("{0}: faltan {1}, sobran {2}".format(
            cap["clave"], sorted(rango - set(ns))[:8], sorted(set(ns) - rango)[:8]))
    faltan_md = sorted(rango - set(textos))
    if faltan_md:
        fallos.append("{0}: el markdown no tiene {1}".format(cap["md"], faltan_md[:8]))
    previa = 0
    for s in cap["suttas"]:
        n = s["n"]
        if not cap["pdf"][0] <= s["pdf"] <= cap["pdf"][1]:
            fallos.append("§{0}: página del PDF {1} fuera del capítulo".format(n, s["pdf"]))
        if s["pdf"] < previa:
            fallos.append("§{0}: la página del PDF retrocede".format(n))
        previa = s["pdf"]
        for r in s["roles"] + s.get("respuesta", []):
            if r[0] not in ROLES:
                fallos.append("§{0}: función desconocida «{1}»".format(n, r[0]))
            if r[0] == "nimitta" and (len(r) < 4 or r[3] not in CASOS):
                fallos.append("§{0}: nimitta sin caso".format(n))
        resto = MARCA.sub("", s["ejemplo"])
        if any(c in resto for c in "{}|"):
            fallos.append("§{0}: marca mal formada en el ejemplo".format(n))
        if s.get("ejercicio") and MARCA.search(s["ejemplo"]):
            fallos.append("§{0}: un ejercicio no lleva el ejemplo marcado".format(n))
        nota = s.get("nota", {})
        if bool(nota.get("es", "").strip()) != bool(nota.get("en", "").strip()):
            fallos.append("§{0}: la nota no está en las dos lenguas".format(n))
        if s.get("respuesta") and not s.get("ejercicio"):
            fallos.append("§{0}: respuesta sin ejercicio".format(n))
        if not nfc(s):
            fallos.append("§{0}: texto que no está en NFC".format(n))
    return fallos


def terminos_de_fila(s, glosario, gre, gfk):
    """Las entradas del glosario que la fila enseña en globo, con el mismo
    criterio que glosar() en la plantilla: clase, notas y funciones; nada
    dentro de una cita pāḷi de dos palabras o más; respetando «no_en»."""
    usados = {RK[r[0]] for r in s["roles"] + s.get("respuesta", []) if r[0] in RK}
    for texto in [s.get("clase", "")] + [s.get("nota", {}).get(l, "") for l in ("es", "en")]:
        citas = [m.span() for m in CITA.finditer(texto) if re.search(r"\s", m.group().strip())]
        for m in gre.finditer(texto):
            k = gfk.get(m.group(1).lower())
            if k and not any(a <= m.start() < b for a, b in citas) \
                    and s["n"] not in glosario[k].get("no_en", []):
                usados.add(k)
    return sorted(k for k in usados if k in glosario)


def datos_preguntar(meta, filas, glosario):
    """preguntar.json: el contexto del botón «Preguntar», fila por fila."""
    gk = {t["clave"]: t for t in glosario}
    formas = sorted(((f, t["clave"]) for t in glosario for f in t["formas"]), key=lambda x: -len(x[0]))
    gfk = {f.lower(): k for f, k in formas}
    gre = re.compile(r"(?<![^\W\d_])(" + "|".join(re.escape(f) for f, _ in formas) + r")(?![^\W\d_])",
                     re.I) if formas else None
    out = {"version": meta["version"], "filas": {}, "terminos": {}}
    for s in filas:
        usados = terminos_de_fila(s, gk, gre, gfk) if gre else []
        out["filas"][str(s["n"])] = {
            "cap": s["cap"], "n": s["n"], "sutta": s.get("sutta", ""), "tr": s.get("tr", {}),
            "clase": s["clase"], "anuvatti": s["anuvatti"], "roles": s["roles"],
            "ejercicio": bool(s.get("ejercicio")), "respuesta": s.get("respuesta", []),
            "ejemplo": s["ejemplo"], "nota": s.get("nota", {}), "pdf": s["pdf"], "terminos": usados}
        for k in usados:
            t = gk[k]
            e = t.get("ejemplo")
            out["terminos"][k] = {"termino": t["termino"], "def": t["def"],
                                  "ejemplo": {"n": e["n"], "sutta": e.get("sutta", ""),
                                              "nota": e.get("nota", {}), "tr": e.get("tr", {})} if e else None}
    return out


def guia(meta):
    """La guía para el estudiante: (html, fallos). El markdown se convierte
    con el mismo intérprete de prosa que generar_recurso.py; el texto no se
    toca. Las dos lenguas se separan por una línea «---» o, si no la hay, por
    el segundo «# título»; el «# título» de cada lengua es el h1 de la página.
    Además de lo que entiende ese intérprete: «> cita» y `código`."""
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
    if len(corte) == 1:
        partes = {"es": lineas[:corte[0]], "en": lineas[corte[0] + 1:]}
    else:
        h1s = [i for i, l in enumerate(lineas) if re.match(r"^#\s+\S", l)]
        if corte or len(h1s) != 2:
            return None, fallos + ["guia.md: el español y el inglés se separan con una sola "
                                   "línea «---» o con dos «# título» (hay {0} y {1})".format(
                                       len(corte), len(h1s))]
        partes = {"es": lineas[:h1s[1]], "en": lineas[h1s[1]:]}
    base = R.inline
    R.inline = lambda t: re.sub(r"`([^`]+)`", r"<code>\1</code>", base(t))

    def bloques(ls):
        # las citas «> …» aparte; lo demás, al intérprete de prosa
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
        # lista numerada: el número va en el texto (generar_recurso lo deja literal)
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
            titulos[lg] = {"h1": limpio, "titulo": limpio, "h1_html": R.inline(h1)}
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
                         ("__VERSION__", meta["version"]),
                         ("__ES__", cuerpos["es"]), ("__EN__", cuerpos["en"])):
        pl = pl.replace(clave, valor)
    return pl, []


def main():
    meta = json.load(open(os.path.join(DIR, "meta.json"), encoding="utf-8"))
    caps, fallos = [], []
    for nombre in meta["capitulos"]:
        cap = json.load(open(os.path.join(DIR, "datos", nombre), encoding="utf-8"))
        textos = leer_md(os.path.join(RAIZ, "kaccayana", cap["md"] + ".md"))[0]
        en = os.path.join(RAIZ, "kaccayana", cap["md"] + ".en.md")
        textos_en = leer_md(en)[0] if os.path.exists(en) else {}
        fallos += verificar(cap, textos)
        # aviso de cabecera del capítulo (Kāraka, v0.9): si lo hay, en las dos lenguas
        aviso = cap.get("aviso")
        if aviso is not None and not (aviso.get("es") and aviso.get("en")):
            fallos.append("{0}: el aviso del capítulo no está en español e inglés".format(cap["clave"]))
        for s in cap["suttas"]:
            if s["n"] in textos:
                s["sutta"] = textos[s["n"]]["sutta"]
                # la traducción publicada: no se muestra en la tabla, pero entra
                # en la búsqueda (v0.3.3)
                s["tr"] = {"es": textos[s["n"]]["tr"],
                           "en": textos_en.get(s["n"], {}).get("tr", "")}
        caps.append(cap)
    indice = []
    for c in meta["indice"]:
        e = {"clave": c["clave"], "pali": c["pali"], "kandas": [], "desde": None, "hasta": None}
        ruta = os.path.join(RAIZ, "kaccayana", c["md"] + ".md") if c["md"] else ""
        if ruta and os.path.exists(ruta):
            t, ks = leer_md(ruta)
            e["desde"], e["hasta"] = min(t), max(t)
            for i, (k, desde) in enumerate(ks):
                hasta = ks[i + 1][1] - 1 if i + 1 < len(ks) else e["hasta"]
                e["kandas"].append([k, desde, hasta])
        indice.append(e)
    if not nfc(meta):
        fallos.append("meta.json: texto que no está en NFC")
    pagina_guia, f_guia = guia(meta)
    fallos += f_guia
    if fallos:
        print("El análisis de los suttas NO cuadra; no se publica:")
        for f in fallos[:25]:
            print("  ✗", f)
        return 1

    filas = []
    for cap in caps:
        for s in cap["suttas"]:
            s["cap"] = cap["clave"]
            filas.append(s)
    try:
        import terminos
        glosario = terminos.cargar(RAIZ)
    except ValueError as err:
        print("El glosario de los globos NO cuadra; no se publica:", err)
        return 1
    # a la página, sólo los campos que enseña el globo, como en
    # /recursos/comentarios/: la «fuente» de cada entrada (que puede nombrar
    # docs/fuentes/) y la marca «revisar» no viajan
    globos = [{k: t[k] for k in ("clave", "termino", "formas", "def", "ejemplo", "no_en") if k in t}
              for t in glosario]
    salida = {"meta": meta, "indice": indice, "terminos": globos,
              "capitulos": [{k: c[k] for k in ("clave", "pali", "desde", "hasta", "pdf", "paginas", "aviso") if k in c}
                            for c in caps],
              "filas": filas}

    pl = open(PLANTILLA, encoding="utf-8").read()
    m = re.search(r'/\*__DATOS__\*/.*?/\*__FIN__\*/', pl, re.S)
    if not m:
        print("La plantilla no tiene el marcador /*__DATOS__*/…/*__FIN__*/")
        return 1
    datos = json.dumps(salida, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = pl[:m.start()] + datos + pl[m.end():]
    html = html.replace("__VERSION_DATE__", meta["fecha"]).replace("__VERSION__", meta["version"])
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    open(DESTINO, "w", encoding="utf-8").write(html)
    os.makedirs(os.path.dirname(GUIA_DESTINO), exist_ok=True)
    open(GUIA_DESTINO, "w", encoding="utf-8").write(pagina_guia)
    with open(PREGUNTAR, "w", encoding="utf-8") as f:
        json.dump(datos_preguntar(meta, filas, glosario), f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")

    ej = sum(1 for f in filas if f.get("ejercicio"))
    print("Análisis (Visuddhāyuṃ) v{0} ({1}) · {2} aforismos · {3} ejercicios → {4}".format(
        meta["version"], meta["estado"], len(filas), ej, os.path.relpath(DESTINO, RAIZ)))
    print("Guía para el estudiante → {0}".format(os.path.relpath(GUIA_DESTINO, RAIZ)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
