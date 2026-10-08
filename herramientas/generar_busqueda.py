#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La búsqueda en todo el sitio (rediseño de la navegación, etapa 4a,
2026-10-08).

    python3 herramientas/generar_busqueda.py

Escribe:

  * site/assets/busqueda-es.json y site/assets/busqueda-en.json, el índice.
    Sólo lo descarga site/assets/buscar.js, y sólo cuando alguien busca:
    ninguna página lo pide al cargar;
  * site/buscar/index.html y site/en/buscar/index.html, la página de
    resultados: una caja y la lista. Son noindex, como los borradores, de
    modo que generar_seo.py no las mete en sitemap.xml.

Qué entra en el índice —título, un texto corto, la dirección y el tipo—, y
de dónde sale. Se lee lo YA PUBLICADO (o los datos que la página publica tal
cual), para que la búsqueda no encuentre nada que el sitio no enseñe:

  Suttas      las 405 páginas /s/N/ (/en/s/N/): §N, el sutta en pāḷi, su
              línea de traducción y, como claves que no se enseñan, las
              palabras pāḷi del bloque del sutta (vutti y ejemplos) y de su
              desglose;
  Glosario    las fichas de la vista alfabética del glosario publicado
              (#g-<id>, el ancla que la página ya tenía): el lema y su
              traducción (la lista normativa, si no Nandisena, si no Smith);
  Raíces      las raíces de Saddanīti-dhātumālā (#r<id>): raíz y
              significado, con la glosa pāḷi como clave;
  Paradigmas  los paradigmas de declinación (#<código>): nombre y género;
  Recursos    las páginas de /recursos/, con su línea de la portada.

BORRADORES (análisis, clasificación, casos, comentarios): NI UNA PALABRA de
su texto. Entran sólo por el título de la página, rotulados «borrador», y
—clasificación y análisis, que tienen una fila por §— por su número: el
índice lleva el título y los § que cubren, y buscar.js arma «§N ·
Clasificación de los suttas» al buscar un número. Decisión del IEBH,
2026-10-08: el contenido de borrador se queda en las páginas de borrador.

La normalización de las claves (norm(), abajo) es la de buscar.js y la de
los buscadores de las páginas (plegar() de pali.js, fold() de raíces):
minúsculas, sin diacríticos (ā = a, ṃ = m, ñ = n…), sin puntuación.

Va en generar_todo.py después de generar_hub.py (lee sus páginas) y antes
de generar_indices.py y generar_seo.py. Es determinista.
"""

import hashlib
import html as H
import json
import os
import re
import sys
import time
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "herramientas"))

import cabecera  # noqa: E402
import generar_capitulo as GC  # noqa: E402
import generar_indices as GI  # noqa: E402
from generar_secciones import mapa as mapa_secciones  # noqa: E402

SITIO = os.path.join(RAIZ, "site")
ASSETS = os.path.join(SITIO, "assets")

# Los tipos, en el orden en que salen los grupos de resultados.
TIPOS = ("suttas", "glosario", "raices", "paradigmas", "recursos")

# Las páginas de una sola URL que entienden ?lang=en; las demás siguen la
# lengua guardada (pali_lang).
CON_LANG = ("recursos/glosario/", "recursos/analisis/",
            "recursos/clasificacion/", "recursos/comentarios/")

# El texto corto de una ficha del glosario no pasa de aquí: la definición
# entera está en la página, y el índice tiene que ser pequeño.
CORTO = 110

T = {
    "es": {
        "titulo": "Buscar en el sitio",
        "titulo_pagina": "Buscar · Gramáticas Pāḷi",
        "descripcion": "Búsqueda en todo el sitio: suttas, glosario, raíces, "
                       "paradigmas y recursos.",
        # La explicación que llevaba la caja grande de la portada, que se quitó
        # (pedido del IEBH, 2026-10-08): la caja de la barra es la única.
        "intro": "Un número lleva a la página de ese sutta ({n} publicados). "
                 "Una palabra, en pāḷi o en español, con diacríticos o sin "
                 "ellos, se busca en los suttas, el glosario, las raíces, los "
                 "paradigmas y los recursos.",
        "etiqueta": "Palabra, término, raíz o número de sutta",
        "boton": "Buscar",
        "ayuda": "Con diacríticos o sin ellos: «karaka» encuentra kāraka. "
                 "Un número busca ese §.",
        "sin_js": "La búsqueda necesita JavaScript. Los suttas se pueden "
                  "abrir por su número desde la barra (§).",
        "tema": "Modo oscuro",
        "copyright": GC.COPYRIGHT,
    },
    "en": {
        "titulo": "Search the site",
        "titulo_pagina": "Search · Pāḷi Grammars",
        "descripcion": "Search the whole site: suttas, glossary, roots, "
                       "paradigms and resources.",
        "intro": "A number takes you to that sutta's page ({n} published). "
                 "A word, in Pāḷi or English, with or without diacritics, is "
                 "looked up in the suttas, the glossary, the roots, the "
                 "paradigms and the resources.",
        "etiqueta": "Word, term, root or sutta number",
        "boton": "Search",
        "ayuda": "With or without diacritics: «karaka» finds kāraka. "
                 "A number looks up that §.",
        "sin_js": "Search needs JavaScript. Suttas can be opened by number "
                  "from the bar (§).",
        "tema": "Dark mode",
        "copyright": GC.COPYRIGHT_EN,
    },
}

# Lo que buscar.js escribe: van en el atributo data-textos de la página.
TEXTOS_JS = {
    "es": {
        "grupos": {"suttas": "Suttas", "glosario": "Glosario", "raices": "Raíces",
                   "paradigmas": "Paradigmas", "recursos": "Recursos"},
        "borrador": "borrador",
        "cargando": "Cargando el índice…",
        "error": "No se pudo cargar el índice de búsqueda.",
        "n_resultados": "{n} resultados para «{q}»",
        "un_resultado": "1 resultado para «{q}»",
        "nada": "Nada coincide con «{q}».",
        "sugerencia": "Pruebe sin diacríticos (karaka, no kāraka) o con un "
                      "número de sutta, por ejemplo 290.",
        "ver_mas": "Ver {n} más",
        "quedan": "de {n}",
    },
    "en": {
        "grupos": {"suttas": "Suttas", "glosario": "Glossary", "raices": "Roots",
                   "paradigmas": "Paradigms", "recursos": "Resources"},
        "borrador": "draft",
        "solo_es": "No English text yet",
        "cargando": "Loading the index…",
        "error": "The search index could not be loaded.",
        "n_resultados": "{n} results for «{q}»",
        "un_resultado": "1 result for «{q}»",
        "nada": "Nothing matches «{q}».",
        "sugerencia": "Try without diacritics (karaka, not kāraka) or with a "
                      "sutta number, for example 290.",
        "ver_mas": "Show {n} more",
        "quedan": "of {n}",
    },
}

GENERO = {
    "masculino": ("masculino", "masculine"),
    "femenino": ("femenino", "feminine"),
    "neutro": ("neutro", "neuter"),
    "pronombre-m": ("pronombre, masculino", "pronoun, masculine"),
    "pronombre-f": ("pronombre, femenino", "pronoun, feminine"),
    "pronombre-n": ("pronombre, neutro", "pronoun, neuter"),
    "pronombre": ("pronombre", "pronoun"),
    "numeral": ("numeral", "numeral"),
    "sufijos": ("sufijos que son inflexiones", "inflectional suffixes"),
}

# ---------------------------------------------------------------- texto

# La puntuación que los buscadores de las páginas quitan sin dejar hueco
# (plegar() de pali.js): «§290» → «290», «Sattamī-atthe» → «sattamiatthe».
PUNTUACION = re.compile(r"[’'‘\"“”«».,;:()\[\]§+=¿?—–\-]")


def norm(s):
    """Minúsculas, sin diacríticos y sin puntuación: lo mismo que norm() de
    buscar.js. Lo demás que no es letra ni cifra, a espacio."""
    s = unicodedata.normalize("NFD", unicodedata.normalize("NFC", s or ""))
    s = "".join(c for c in s if not unicodedata.category(c).startswith("M"))
    s = s.replace("ŋ", "n").replace("Ŋ", "n").lower()
    s = PUNTUACION.sub("", s)
    s = re.sub(r"[^0-9a-z]+", " ", s)
    return s.strip()


def plano(fragmento):
    t = re.sub(r"<[^>]+>", " ", fragmento or "")
    return re.sub(r"\s+", " ", H.unescape(t)).strip()


def corto(t, n=CORTO):
    t = re.sub(r"\s+", " ", t or "").strip()
    if len(t) <= n:
        return t
    t = t[:n].rsplit(" ", 1)[0].rstrip(" ,;:.—–-")
    return t + "…"


def nfc(t):
    return unicodedata.normalize("NFC", t or "")


def claves(*textos, quitar=""):
    """Las palabras, normalizadas y sin repetir, en el orden en que salen;
    sin las que ya están en `quitar` (el título) ni las de una letra."""
    vistas = set(norm(quitar).split())
    out = []
    for t in textos:
        for w in norm(t).split():
            if len(w) > 1 and not w.isdigit() and w not in vistas:
                vistas.add(w)
                out.append(w)
    return " ".join(out)


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------- suttas


def suttas(lengua, secc):
    """Las páginas /s/N/ ya escritas por generar_hub.py: lo que enseñan."""
    out = []
    for n in sorted(int(k) for k in secc["secciones"]):
        cap = secc["secciones"][str(n)]
        en = lengua == "en" and secc["capitulos"][cap]["en"]
        url = "{0}s/{1}/".format("en/" if en else "", n)
        s = leer(os.path.join(SITIO, url, "index.html"))
        pali = plano(re.search(r'<h1 lang="pi">(.*?)</h1>', s, re.S).group(1))
        trad = plano(re.search(r'<p class="hub-trad">(.*?)</p>', s, re.S).group(1))
        bloque = re.search(r'<div class="pali-block">(.*?)</div>', s, re.S)
        bloque = re.sub(r"<abbr\b[^>]*>.*?</abbr>", " ", bloque.group(1) if bloque else "",
                        flags=re.S)
        desglose = re.search(r'<div class="sutta-breakdown">\[(.*?)=', s, re.S)
        k = claves(plano(desglose.group(1)) if desglose else "", plano(bloque),
                   quitar=pali)
        out.append(["suttas", "§{0} {1}".format(n, pali), trad, url, k])
    return out


# ---------------------------------------------------------------- glosario


def datos_glosario():
    """El JSON que lleva dentro la página publicada del glosario."""
    s = leer(os.path.join(SITIO, "recursos", "glosario", "index.html"))
    i = s.index('{"nota"')
    datos, _ = json.JSONDecoder().raw_decode(s[i:])
    return datos


def glosario(lengua, d):
    url = "recursos/glosario/" + ("?lang=en" if lengua == "en" else "")
    out = []
    for g in d["agrupado"]:
        norma = [d["normativo"][i] for i in g["g"]]
        nand = [d["nandisena"][i] for i in g["n"]]
        smith = [d["conspectus"][i] for i in g["c"]]
        texto = ""
        solo_es = False
        # la traducción que enseña la ficha, por la misma prelación que el
        # lema: la lista normativa, Nandisena, Smith. En inglés, lo que la
        # página publica en inglés; si no hay, el español, como la página,
        # y rotulado igual que en ella: «ES», sólo en español (el séptimo
        # campo de la entrada, que buscar.js convierte en la etiqueta).
        for capa in (norma, nand, smith):
            for e in capa:
                t = (e.get("en") if lengua == "en" else None) or e.get("es")
                if t:
                    texto = t
                    solo_es = lengua == "en" and not e.get("en")
                    break
            if texto:
                break
        texto = corto(plano(re.sub(r"\*\*?|`", "", texto)))
        otras = " ".join(p for p, _f in g.get("gr", [])[1:])
        fila = ["glosario", nfc(g["p"]), texto, url + "#g-" + g["id"],
                claves(otras, quitar=g["p"])]
        if solo_es:
            fila += [0, "es"]
        out.append(fila)
    return out


# ---------------------------------------------------------------- raíces


def raices(lengua):
    d = json.load(open(os.path.join(RAIZ, "recursos", "raices", "raices.json"),
                       encoding="utf-8"))
    out = []
    for r in d["raices"]:
        texto = (r.get("en") if lengua == "en" else r.get("es")) or r.get("es") or ""
        out.append(["raices", " / ".join(r["raices"]), corto(texto),
                    "recursos/raices/#r{0}".format(r["id"]),
                    claves(r.get("glosa", ""), quitar=" ".join(r["raices"]))])
    return out


# ---------------------------------------------------------------- paradigmas


def paradigmas(lengua):
    base = os.path.join(RAIZ, "recursos", "paradigmas")
    d = json.load(open(os.path.join(base, "paradigmas.json"), encoding="utf-8"))
    ing = json.load(open(os.path.join(base, "ingles.json"), encoding="utf-8"))
    en_ok = bool(ing.get("adjudicado"))
    out = []
    for p in d["paradigmas"]:
        nombre = p["paradigma"]
        if lengua == "en" and en_ok:
            nombre = ing.get("paradigmas", {}).get(p["codigo"], {}).get("paradigma") or nombre
        gen = GENERO.get(p.get("genero"), (p.get("genero", ""),) * 2)
        out.append(["paradigmas", "{0} · {1}".format(p["codigo"], nombre),
                    gen[1 if lengua == "en" else 0],
                    "recursos/paradigmas/#" + p["codigo"].replace("#", "num"), ""])
    return out


# ---------------------------------------------------------------- recursos


def recursos(lengua):
    out = []
    for _grupo, items in GI.recursos_descritos():
        for href, t_es, t_en, d_es, d_en, borrador in items:
            url = "recursos/" + href
            if lengua == "en" and url in CON_LANG:
                url += "?lang=en"
            titulo = t_en if lengua == "en" else t_es
            # de un borrador, sólo el título: ni su línea
            # las etiquetas de la línea son de texto corrido (<i>…</i>): se
            # quitan sin dejar hueco, o queda «Saddanīti , con»
            texto = "" if borrador else plano(re.sub(r"<[^>]+>", "", d_en if lengua == "en" else d_es))
            e = ["recursos", titulo, texto, url, ""]
            if borrador:
                e.append(1)
            out.append(e)
    return out


def tramos(ns):
    """[1, 2, 3, 7] → [[1, 3], [7, 7]]."""
    out = []
    for n in sorted(ns):
        if out and n == out[-1][1] + 1:
            out[-1][1] = n
        else:
            out.append([n, n])
    return out


def borradores_por_sutta(lengua):
    """Los dos borradores que tienen una fila por §: su título y los § que
    cubren. Nada más."""
    lq = "?lang=en" if lengua == "en" else ""
    titulos = {}
    for _g, items in GI.recursos_descritos():
        for href, t_es, t_en, _de, _dn, _b in items:
            titulos[href] = t_en if lengua == "en" else t_es
    return [
        {"t": titulos["clasificacion/"], "u": "recursos/clasificacion/" + lq + "#s{n}",
         "n": tramos(GC.filas_borrador("clasificacion"))},
        {"t": titulos["analisis/"], "u": "recursos/analisis/" + lq + "#s{n}",
         "n": tramos(GC.filas_borrador("analisis"))},
    ]


# ---------------------------------------------------------------- página

PAGINA = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta name="robots" content="noindex"/>
<title>{titulo_pagina}</title>
<meta content="{descripcion}" name="description"/>
<link href="{raiz}assets/favicon.svg" rel="icon" type="image/svg+xml"/>
<link href="{raiz}assets/pali.css?v={v}" rel="stylesheet"/>
</head>
<body>
<script>/* Tema guardado, antes de pintar (clave común pali_dark). */
try{{var _d=localStorage.getItem('pali_dark');
if(_d==='1'||(_d===null&&matchMedia('(prefers-color-scheme: dark)').matches))
document.body.classList.add('dark');}}catch(e){{}}
/* Lengua: la misma regla y la misma redirección que los capítulos y las
   páginas de sutta; la búsqueda (?q=) viaja con ella. */
function paliLang(){{var g=null;
try{{g=localStorage.getItem('pali_lang');}}catch(e){{}}
if(g==='en'||g==='es')return g;
var n=(navigator.languages&&navigator.languages[0])||navigator.language||'';
return /^en\\b/i.test(n)?'en':'es';}}
try{{if(paliLang()==='{otra_lang}')location.replace('{otra_url}'+location.search+location.hash)}}catch(e){{}}</script>
<button id="dark-btn" type="button" aria-label="{tema}" onclick="document.body.classList.toggle('dark');try{{localStorage.setItem('pali_dark',document.body.classList.contains('dark')?'1':'0')}}catch(e){{}}">◐</button>
<a id="lang-btn" href="{otra_url}" onclick="try{{localStorage.setItem('pali_lang','{otra_lang}')}}catch(e){{}};this.href='{otra_url}'+location.search+location.hash">{otra_lang_may}</a>
<main class="busca" id="busca" data-indice="{raiz}assets/busqueda-{lang}.json?v={vi}" data-textos="{textos}">
<h1>{titulo}</h1>
<p class="busca-intro">{intro}</p>
<form class="busca-form" id="busca-form" role="search" action="./" method="get">
<label for="busca-q">{etiqueta}</label>
<div class="busca-fila"><input id="busca-q" name="q" type="search" autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="search" aria-describedby="busca-ayuda"/>
<button type="submit">{boton}</button></div>
<p class="busca-ayuda" id="busca-ayuda">{ayuda}</p>
</form>
<p class="busca-estado" id="busca-estado" role="status" aria-live="polite"></p>
<div class="busca-res" id="busca-res"></div>
<noscript><p class="busca-estado">{sin_js}</p></noscript>
<div class="idx-foot hub-pie">
<span class="marca-lockup"></span>
<p>{copyright}</p>
</div>
</main>
<script defer src="{raiz}assets/buscar.js?v={vb}"></script>
</body>
</html>
"""


def huella(ruta):
    with open(ruta, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


def pagina(lengua, v_indice, n_suttas):
    t = T[lengua]
    raiz = "../" if lengua == "es" else "../../"
    otra = "en" if lengua == "es" else "es"
    otra_url = "/en/buscar/" if otra == "en" else "/buscar/"
    buscar_js = os.path.join(ASSETS, "buscar.js")
    html = PAGINA.format(
        lang=lengua, raiz=raiz, v=cabecera.version_assets(), vi=v_indice,
        vb=huella(buscar_js) if os.path.exists(buscar_js) else "0",
        titulo_pagina=H.escape(t["titulo_pagina"]), descripcion=H.escape(t["descripcion"]),
        otra_lang=otra, otra_url=otra_url, otra_lang_may=otra.upper(),
        tema=H.escape(t["tema"]), titulo=H.escape(t["titulo"]),
        intro=H.escape(t["intro"].format(n=n_suttas)),
        etiqueta=H.escape(t["etiqueta"]), boton=H.escape(t["boton"]),
        ayuda=H.escape(t["ayuda"]), sin_js=H.escape(t["sin_js"]),
        copyright=t["copyright"],
        textos=H.escape(json.dumps(TEXTOS_JS[lengua], ensure_ascii=False,
                                   separators=(",", ":")), quote=True))
    return cabecera.insertar(html, "buscar", idioma=lengua, otra_url=otra_url, raiz=raiz)


# ---------------------------------------------------------------- main


def main():
    t0 = time.time()
    secc = mapa_secciones()
    glos = datos_glosario()
    informe = []
    for lengua in ("es", "en"):
        entradas = (suttas(lengua, secc) + glosario(lengua, glos) + raices(lengua)
                    + paradigmas(lengua) + recursos(lengua))
        for e in entradas:
            e[0] = TIPOS.index(e[0])
            e[1], e[2] = nfc(e[1]), nfc(e[2])
        indice = {
            "_nota": "Generado por herramientas/generar_busqueda.py; no editar a mano. "
                     "Cada entrada: [tipo, título, texto, dirección desde la raíz del "
                     "sitio, claves normalizadas, borrador, lengua del texto "
                     "si no es la de la página].",
            "tipos": list(TIPOS),
            "borradores": borradores_por_sutta(lengua),
            "e": entradas,
        }
        texto = json.dumps(indice, ensure_ascii=False, separators=(",", ":"))
        ruta = os.path.join(ASSETS, "busqueda-{0}.json".format(lengua))
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(texto + "\n")
        tam = os.path.getsize(ruta)
        if tam > 2 * 1024 * 1024:
            print("✗ {0}: {1} bytes, más de 2 MB".format(os.path.relpath(ruta, RAIZ), tam))
            return 1
        cuenta = [sum(1 for e in entradas if e[0] == i) for i in range(len(TIPOS))]
        destino = os.path.join(SITIO, "buscar") if lengua == "es" else os.path.join(SITIO, "en", "buscar")
        os.makedirs(destino, exist_ok=True)
        with open(os.path.join(destino, "index.html"), "w", encoding="utf-8") as f:
            f.write(pagina(lengua, huella(ruta), cuenta[TIPOS.index("suttas")]))
        informe.append("{0}: {1} entradas ({2}) · {3} KB".format(
            lengua.upper(), len(entradas),
            " · ".join("{0} {1}".format(c, n) for c, n in zip(cuenta, TIPOS)),
            (tam + 1023) // 1024))
    print("índice de búsqueda y /buscar/, /en/buscar/ · {0:.1f} s\n{1}".format(
        time.time() - t0, "\n".join(informe)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
