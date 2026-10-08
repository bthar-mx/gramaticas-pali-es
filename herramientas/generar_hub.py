#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Las páginas de cada sutta, «§ hub» (rediseño de la navegación, etapa 2;
diseño aprobado por el IEBH el 2026-10-08, mesas de trabajo 2 y 4).

    python3 herramientas/generar_hub.py

Escribe site/s/N/index.html (español) y site/en/s/N/index.html (inglés) para
cada § que tiene tarjeta publicada en su capítulo: los mismos § que
site/assets/secciones.json (generar_secciones.mapa). Dos URL por sutta, como
los capítulos: pareja hreflang (la pone generar_seo.py), la misma redirección
por `pali_lang`, y el ES|EN de la cabecera común pasa de una a otra
conservando el #ancla.

Qué lleva cada página, de arriba abajo:

  * migas (Inicio › Kaccāyana › capítulo › kaṇḍa › §N) y §N anterior y
    siguiente, que cruzan de capítulo;
  * §N, el sutta en pāḷi (de comun/concordancia.json) y la línea de
    traducción del capítulo;
  * los números: Kaccāyana, Rūpasiddhi, Saddanīti, capítulo y kaṇḍa;
  * «Texto y traducción»: lo que enseña la tarjeta del capítulo, con el MISMO
    análisis del markdown de generar_capitulo.py (parsear, bloque_pali,
    parrafos, inline), sin las notas al pie;
  * «Dónde se cita»: las páginas publicadas que enlazan a este § (véase
    citas());
  * los dos borradores, SÓLO como enlace con su rótulo: la clasificación y el
    análisis según Visuddhāyuṃ son páginas noindex, y su contenido no entra en
    estas, que sí se indexan (decisión del IEBH, 2026-10-08);
  * «Preguntar sobre §N», que lleva al diálogo del análisis (véase la nota en
    PREGUNTAR, abajo).

Va en generar_todo.py después de los capítulos y de los recursos que lee, y
antes de generar_indices.py y generar_seo.py. Es determinista.
"""

import html as H
import json
import os
import re
import sys
import time
from urllib.parse import urljoin, urlparse

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "herramientas"))

import generar_capitulo as GC  # noqa: E402
import cabecera  # noqa: E402
from generar_secciones import mapa as mapa_secciones  # noqa: E402

SITIO = os.path.join(RAIZ, "site")

# ---------------------------------------------------------------- textos

T = {
    "es": {
        "inicio": "Inicio", "migas": "Ruta", "anterior": "Sutta anterior",
        "siguiente": "Sutta siguiente", "numeros": "Numeraciones",
        "en_pagina": "En esta página", "texto": "Texto y traducción",
        "leer": "Leer en el capítulo →", "citado": "Dónde se cita",
        "borradores": "Borradores", "borrador": "borrador",
        "clasif": "Clasificación del sutta", "analisis": "Análisis según Visuddhāyuṃ",
        "preguntar": "Preguntar sobre §{n}",
        "preg_txt": "La pregunta se hace desde el análisis según Visuddhāyuṃ "
                    "(borrador): responde con la fila de este sutta y las fuentes "
                    "del proyecto. Es para estudiantes inscritos y pide iniciar "
                    "sesión.",
        "preg_btn": "Preguntar sobre §{n} →",
        "preg_entrar": "Iniciar sesión para preguntar",
        "preg_ok": "Sesión iniciada. Le quedan hoy {r} preguntas.",
        "kaccayana": "Kaccāyana", "rupasiddhi": "Rūpasiddhi",
        "saddaniti": "Saddanīti", "sin_notas":
            "Sin las notas al pie: están en la tarjeta del capítulo.",
        "titulo_sitio": "Gramáticas Pāḷi",
        "cap_de": "capítulo {n} de 8",
    },
    "en": {
        "inicio": "Home", "migas": "Breadcrumb", "anterior": "Previous sutta",
        "siguiente": "Next sutta", "numeros": "Numberings",
        "en_pagina": "On this page", "texto": "Text and translation",
        "leer": "Read in the chapter →", "citado": "Where it is cited",
        "borradores": "Drafts", "borrador": "draft",
        "clasif": "Classification of the sutta", "analisis": "Analysis following Visuddhāyuṃ",
        "preguntar": "Ask about §{n}",
        "preg_txt": "Questions are asked from the analysis following Visuddhāyuṃ "
                    "(draft): the answer uses this sutta's row and the project's "
                    "sources. It is for enrolled students and requires signing "
                    "in.",
        "preg_btn": "Ask about §{n} →",
        "preg_entrar": "Sign in to ask",
        "preg_ok": "Signed in. {r} questions left today.",
        "kaccayana": "Kaccāyana", "rupasiddhi": "Rūpasiddhi",
        "saddaniti": "Saddanīti", "sin_notas":
            "Without the footnotes: they are on the chapter card.",
        "titulo_sitio": "Pāḷi Grammars",
        "cap_de": "chapter {n} of 8",
    },
}

# Las páginas de una sola URL que pueden citar un §, con su nombre en las dos
# lenguas (el <title> sólo da el español). «borrador»: noindex.
PAGINAS_FUENTE = {
    "/recursos/sandhi/": ("Sandhi — referencia interactiva", "Sandhi — interactive reference", False),
    "/recursos/paradigmas/": ("Paradigmas de declinación", "Declension paradigms", False),
    "/recursos/nombre/": ("Formación del nombre — pācako", "Formation of the noun — pācako", False),
    "/recursos/verbo/": ("El verbo — ākhyāta", "The verb — ākhyāta", False),
    "/recursos/casos/": ("Usos de las inflexiones", "Uses of the inflections", True),
    "/recursos/glosario/": ("Glosario de terminología gramatical", "Glossary of grammatical terminology", False),
    "/recursos/raices/": ("Raíces pāḷi", "Pāḷi roots", False),
    "/recursos/solucionador/": ("Solucionador de sandhis", "Sandhi solver", False),
    "/recursos/comentarios/": ("Comentarios de la escuela de Kaccāyana", "Commentaries of the Kaccāyana school", True),
}
# No citan: los índices; y las dos páginas de borrador que la página del
# sutta ya enlaza aparte, cada una con su rótulo.
NO_FUENTES = ("/recursos/analisis/", "/recursos/clasificacion/")

# ---------------------------------------------------------------- utilidades


def ruta_url(archivo):
    rel = os.path.relpath(os.path.dirname(archivo), SITIO).replace(os.sep, "/")
    return "/" if rel == "." else "/" + rel + "/"


def sin_etiquetas(t):
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", H.unescape(t)).strip()


def e(t):
    return H.escape(t, quote=True)


# ---------------------------------------------------------------- capítulos


def cargar_capitulo(clave, idioma):
    """El estado de generar_capitulo.py para un capítulo y una lengua, como lo
    deja su main(): se reutiliza su análisis del markdown, no se escribe otro."""
    meta = GC.CAPITULOS[clave]
    GC.L = GC.IDIOMAS[idioma]
    GC.SUTTAS_VALIDOS.clear()
    GC.RESUMEN_SUTTAS.clear()
    GC.SUTTAS_OTROS_CAP.clear()
    GC.KANDA_NOMBRE.clear()
    GC.FIN_CAPITULO.clear()
    del GC.NO_ENLAZADOS[:]
    ruta = os.path.join(RAIZ, meta["obra_slug"],
                        clave + (".en.md" if idioma == "en" else ".md"))
    GC.cargar_capitulos_publicados(clave, meta["obra_slug"])
    GC.SUTTAS_VALIDOS.update(
        int(m.group(1)) for m in
        (GC.RE_SUTTA.match(l) for l in open(ruta, encoding="utf-8")) if m)
    cap = GC.parsear(ruta)
    for s in cap["suttas"]:
        glosa = GC.glosa_breve(s)
        GC.RESUMEN_SUTTAS[s["n"]] = s["pali"] + (" — " + glosa if glosa else "")
    # parsear() deja los nombres de kaṇḍa en KANDA_NOMBRE; se guardan aquí
    # porque el capítulo siguiente los borra
    cap["kandas_pali"] = {s["kanda"]: GC.kanda_pali(s["kanda"]) for s in cap["suttas"]}
    return {s["n"]: s for s in cap["suttas"]}, cap


RE_NOTA = re.compile(r"\[\^\d+\]")


def para_hub(html, hubs):
    """El HTML de la tarjeta, adaptado a esta página:
    · los §N enlazan a la página de ese sutta (../N/), no al ancla del
      capítulo;
    · las glosas emergentes {término|glosa} se escriben a la vista, entre
      paréntesis (aquí no hay pali.js que las abra con el dedo);
    · las citas canónicas conservan la sigla desatada sólo como title."""
    def xref(m):
        n = int(m.group(1))
        return '<a class="sutta-xref" href="../{0}/"'.format(n) if n in hubs else m.group(0)
    html = re.sub(r'<a class="sutta-xref" href="#s(\d+)" onclick="jumpOpen\(\'s\d+\'\)"', xref, html)
    html = re.sub(r'<a class="sutta-xref" href="\.\./[a-z]+/#s(\d+)"', xref, html)
    html = re.sub(r'<span class="tip-wrap"><span class="tip-term">(.*?)</span>'
                  r'<span class="tip-box">(.*?)</span></span>',
                  r'\1 <span class="hub-glosa">(\2)</span>', html)
    html = re.sub(r'<span class="ref-tip"><span class="cita-term">(.*?)</span>'
                  r'<span class="ref-tip-box">(.*?)</span></span>',
                  lambda m: '<abbr class="hub-cita" title="{0}">{1}</abbr>'.format(
                      e(sin_etiquetas(m.group(2))), m.group(1)), html)
    return html


def texto_sutta(s, hubs):
    """Lo que enseña la tarjeta del capítulo, con las funciones del capítulo,
    sin notas al pie y con todo desplegado."""
    limpio = dict(s, cuerpo=[RE_NOTA.sub("", l) for l in s["cuerpo"]])
    bloques = GC.partir_bloques(limpio["cuerpo"])
    partes = []
    if bloques:
        partes.append(GC.bloque_pali(bloques[0], {}))
    traduccion = ""
    if len(bloques) > 1:
        lineas = [x.strip() for x in bloques[1] if x.strip()]
        if lineas:
            traduccion = GC.inline(lineas[0], {})
            partes.append('<div class="gloss">{0}</div>'.format(traduccion))
            for extra in lineas[1:]:
                partes.append('<div class="vutti">{0}</div>'.format(GC.inline(extra, {})))
    if len(bloques) > 2:
        partes.append('<div class="rest-content hub-resto">{0}</div>'.format(
            "".join(GC.parrafos(b, {}) for b in bloques[2:])))
    cab = '<p class="hub-ref">{0}. {1}. <span class="sutta-pali-title">{2}</span>{3}</p>'.format(
        s["n"], GC.escapar_html(s["rup"]), GC.escapar_html(s["pali"]),
        " <span class=\"sutta-ref-num\">({0})</span>".format(", ".join(s["sadd"])) if s["sadd"] else "")
    desglose = ""
    if s["desglose"]:
        voces = "{0} {1}".format(s["voces"], GC.L["voz"][0] if s["voces"] == 1 else GC.L["voz"][1])
        desglose = '<div class="sutta-breakdown">[{0} = {1}]</div>'.format(
            GC.escapar_html(s["desglose"]), voces)
    return para_hub(cab + desglose + "".join(partes), hubs), para_hub(traduccion, hubs)


# ---------------------------------------------------------------- citas


def citas(secc):
    """§N → [(lengua, orden, título_es, título_en, href, texto, borrador)].

    Lo que se cuenta como cita: un enlace de una página publicada a la
    tarjeta /kaccayana/<capítulo>/#sN (o /en/…), fuera de la página de ese
    mismo capítulo. Dos maneras de encontrarlos:

    1. En el HTML publicado, todo <a href> que resuelva ahí (los capítulos
       entre sí, nombre, verbo…). En un capítulo, la cita se nombra por la
       tarjeta que la contiene («§64 …») y lleva a la página de ese sutta.
    2. Las páginas que arman sus enlaces en el navegador a partir de sus
       datos se leen con la misma regla que su guion, sobre los mismos datos:
       sandhi (las secuencias «verificada», kac_seq), paradigmas (las
       referencias «§N» de los sufijos, al Nāma-Kappa) y casos (los
       aforismos de Kaccāyana de cada uso, por la concordancia de la página).

    No entran: el solucionador (sus enlaces dependen del pasaje que pegue el
    lector), los globos de términos (sólo viven en páginas de borrador) y el
    análisis y la clasificación, que la página del sutta enlaza aparte.
    De cada página fuente sólo se toma su título y el texto visible del
    enlace: nada de su contenido."""
    out = {}

    def poner(n, lengua, orden, tes, ten, href, texto, borrador):
        if str(n) not in secc["secciones"]:
            return
        out.setdefault(n, set()).add((lengua, orden, tes, ten, href, texto, borrador))

    titulos_cap = {}
    for clave, meta in GC.CAPITULOS.items():
        titulos_cap["/kaccayana/{0}/".format(meta["slug"])] = (meta["num"], meta["titulo_pali"])
        titulos_cap["/en/kaccayana/{0}/".format(meta["slug"])] = (meta["num"], meta["titulo_pali"])

    # 1. enlaces escritos en el HTML
    re_a = re.compile(r'<a\b[^>]*?\bhref="([^"]*#s(\d+))"[^>]*>(.*?)</a>', re.S)
    re_tarjeta = re.compile(r'<div class="sutta-card" id="s(\d+)"')
    for dirpath, _dirs, files in sorted(os.walk(SITIO)):
        if "index.html" not in files:
            continue
        archivo = os.path.join(dirpath, "index.html")
        url = ruta_url(archivo)
        if re.match(r"^/(en/)?s/", url) or url.startswith(NO_FUENTES):
            continue
        es_cap = url in titulos_cap
        if not es_cap and url not in PAGINAS_FUENTE:
            continue
        s = open(archivo, encoding="utf-8").read()
        tarjetas = [(m.start(), int(m.group(1))) for m in re_tarjeta.finditer(s)] if es_cap else []
        for m in re_a.finditer(s):
            href = m.group(1)
            if "$" in href or "'" in href or "+" in href:
                continue                      # plantillas del guion, no enlaces
            destino = urlparse(urljoin("https://x" + url, href))
            dm = re.match(r"^/(en/)?kaccayana/([a-z]+)/$", destino.path)
            if not dm or destino.path == url:
                continue
            n = int(m.group(2))
            if secc["secciones"].get(str(n)) != dm.group(2):
                continue
            if es_cap:
                previas = [t for t in tarjetas if t[0] < m.start()]
                if not previas:
                    continue
                cita = previas[-1][1]
                num, titulo = titulos_cap[url]
                lengua = "en" if url.startswith("/en/") else "es"
                poner(n, lengua, (0, num, cita), titulo, titulo,
                      "@hub:{0}".format(cita), "§{0}".format(cita), False)
            else:
                tes, ten, borr = PAGINAS_FUENTE[url]
                poner(n, "ambas", (1, tes, 0), tes, ten, url,
                      sin_etiquetas(m.group(3)), borr)
        # los datos que la página lleva dentro con la dirección ya hecha
        # («href»: "../../kaccayana/nama/#s83", en el verbo): su guion pinta
        # el enlace con el texto «§N»
        if not es_cap:
            for m in re.finditer(r'"(?:url|href)":\s*"([^"]*kaccayana/[a-z]+/#s(\d+))"', s):
                destino = urlparse(urljoin("https://x" + url, m.group(1)))
                dm = re.match(r"^/(en/)?kaccayana/([a-z]+)/$", destino.path)
                n = int(m.group(2))
                if dm and secc["secciones"].get(str(n)) == dm.group(2):
                    tes, ten, borr = PAGINAS_FUENTE[url]
                    poner(n, "ambas", (1, tes, 0), tes, ten, url, "§{0}".format(n), borr)

    # 2. enlaces que arma el guion de la página
    def de_pagina(url, n, texto):
        tes, ten, borr = PAGINAS_FUENTE[url]
        poner(n, "ambas", (1, tes, 0), tes, ten, url, texto, borr)

    reglas = os.path.join(RAIZ, "recursos", "sandhi", "reglas.json")
    if os.path.exists(reglas):
        for f in json.load(open(reglas, encoding="utf-8"))["ce"]:
            if f.get("verificada") and f.get("kac_seq"):
                de_pagina("/recursos/sandhi/", int(f["kac_seq"]), "§{0}".format(f["kac_seq"]))

    para = os.path.join(RAIZ, "recursos", "paradigmas", "paradigmas.json")
    if os.path.exists(para):
        def recorrer(x):
            if isinstance(x, dict):
                if isinstance(x.get("ref"), str):
                    for tok in re.split(r",\s*", x["ref"]):
                        mt = re.match(r"^§(\d+)", tok.strip())
                        if mt and secc["secciones"].get(mt.group(1)) == "nama":
                            de_pagina("/recursos/paradigmas/", int(mt.group(1)),
                                      "§{0}".format(mt.group(1)))
                for v in x.values():
                    recorrer(v)
            elif isinstance(x, list):
                for v in x:
                    recorrer(v)
        recorrer(json.load(open(para, encoding="utf-8")))

    usos = os.path.join(RAIZ, "recursos", "casos", "usos.json")
    if os.path.exists(usos):
        d = json.load(open(usos, encoding="utf-8"))
        conc = d["concordancia"]["rupasiddhi→kaccayana→saddaniti"]
        # la tabla de los casos (K en la plantilla)
        for _k, n in (("kattu", 281), ("kamma", 280), ("karaṇa", 279), ("sampadāna", 276),
                      ("apādāna", 271), ("okāsa", 278), ("sāmī", 283)):
            de_pagina("/recursos/casos/", n, "§{0}".format(n))

        def usos_de(u):
            for r in u.get("rupasiddhi", []):
                k = conc.get(str(r), ["—"])[0]
                if k != "—":
                    de_pagina("/recursos/casos/", int(k), "Kacc. §{0}".format(k))
            for ej in u.get("ejemplos", []):
                if ej.get("procedencia") == "kacc":
                    mk = re.search(r"Kacc\. §(\d+)", ej.get("nota") or "")
                    ks = [mk.group(1)] if mk else sorted(
                        {conc[str(r)][0] for r in u.get("rupasiddhi", [])
                         if conc.get(str(r), ["—"])[0] != "—"}, key=int)
                    for k in ks:
                        de_pagina("/recursos/casos/", int(k), "Kacc. §{0}".format(k))
            for s in u.get("sub", []):
                usos_de(s)
        for inf in d["inflexiones"]:
            for u in inf.get("sub", []):
                usos_de(u)
    return out


def html_citas(lista, lengua, raiz, n_hub):
    """Las citas de un §, agrupadas por página, para una lengua."""
    if not lista:
        return ""
    grupos = {}
    for (leng, orden, tes, ten, href, texto, borr) in lista:
        if leng not in ("ambas", lengua):
            continue
        grupos.setdefault((orden[:2], tes, ten, href if not href.startswith("@") else "", borr), []).append(
            (orden, href, texto))
    if not grupos:
        return ""
    t = T[lengua]
    filas = []
    for (orden, tes, ten, href, borr), items in sorted(grupos.items()):
        titulo = ten if lengua == "en" else tes
        etiqueta = (' <span class="ini-borrador">{0}</span>'.format(t["borrador"])
                    if borr else "")
        enlaces = []
        vistos = set()
        for o, h, texto in sorted(items):
            if (h, texto) in vistos:
                continue
            vistos.add((h, texto))
            if h.startswith("@hub:"):
                m = int(h[5:])
                enlaces.append('<a href="../{0}/">{1} <i>{2}</i></a>'.format(
                    m, e(texto), e(prev_sig_pali.get(m, ""))))
            else:
                enlaces.append(e(texto))
        cab = ('<a href="{0}{1}">{2}</a>'.format(raiz, href.lstrip("/"), e(titulo))
               if href else e(titulo))
        filas.append('<li><span class="hub-cita-fuente">{0}{1}</span> '
                     '<span class="hub-cita-lugares">{2}</span></li>'.format(
                         cab, etiqueta, " · ".join(enlaces)))
    return '<ul class="hub-citas">{0}</ul>'.format("".join(filas))


# ---------------------------------------------------------------- página

PAGINA = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{titulo}</title>
<meta content="{descripcion}" name="description"/>
<link href="{raiz}assets/favicon.svg" rel="icon" type="image/svg+xml"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Gentium+Book+Plus:ital,wght@0,400;0,700;1,400;1,700&amp;family=Inter:wght@400;500;700&amp;family=JetBrains+Mono:wght@400;700&amp;display=swap" rel="stylesheet"/>
<link href="{raiz}assets/pali.css?v={v}" rel="stylesheet"/>
</head>
<body>
<script>/* Tema guardado, antes de pintar (clave común pali_dark). */
try{{var _d=localStorage.getItem('pali_dark');
if(_d==='1'||(_d===null&&matchMedia('(prefers-color-scheme: dark)').matches))
document.body.classList.add('dark');}}catch(e){{}}
/* Lengua: la misma regla y la misma redirección que los capítulos. */
function paliLang(){{var g=null;
try{{g=localStorage.getItem('pali_lang');}}catch(e){{}}
if(g==='en'||g==='es')return g;
var n=(navigator.languages&&navigator.languages[0])||navigator.language||'';
return /^en\\b/i.test(n)?'en':'es';}}
try{{if(paliLang()==='{otra_lang}')location.replace('{otra_url}'+location.hash)}}catch(e){{}}</script>
<button id="dark-btn" type="button" aria-label="{tema}" onclick="document.body.classList.toggle('dark');try{{localStorage.setItem('pali_dark',document.body.classList.contains('dark')?'1':'0')}}catch(e){{}}">◐</button>
<a id="lang-btn" href="{otra_url}" onclick="try{{localStorage.setItem('pali_lang','{otra_lang}')}}catch(e){{}};this.href='{otra_url}'+location.hash">{otra_lang_may}</a>
<main class="hub">
{cuerpo}
<div class="idx-foot hub-pie">
<span class="marca-lockup"></span>
<p>{copyright}</p>
</div>
</main>
<script>
/* «Preguntar»: la misma sonda que el análisis —GET /api/preguntar?json=1 con
   redirect:'manual'; sin sesión, Access redirige y no se lee nada—. Sólo
   cambia el texto de la línea de estado; la pregunta se hace en el análisis. */
(function(){{var st=document.getElementById('hub-preg-estado');if(!st||!window.fetch)return;
fetch('/api/preguntar?json=1',{{redirect:'manual',credentials:'same-origin'}})
.then(function(r){{return r.ok?r.json():null}}).catch(function(){{return null}})
.then(function(j){{if(j&&j.ok){{st.textContent={preg_ok}.replace('{{r}}',j.restantes);}}
else{{st.innerHTML='<a href="/api/preguntar">'+{preg_entrar}+'</a>';}}st.hidden=false;}});}})();
</script>
</body>
</html>
"""


def pagina(n, lengua, s, conc_s, info, prev, sig, citas_html, hubs, kanda_nombre):
    t = T[lengua]
    raiz = "../../" if lengua == "es" else "../../../"
    slug = info["slug"]
    cap_url = "{0}{1}kaccayana/{2}/".format(raiz, "en/" if lengua == "en" else "", slug)
    otra = "en" if lengua == "es" else "es"
    otra_url = "/{0}s/{1}/".format("en/" if otra == "en" else "", n)
    texto, traduccion = texto_sutta(s, hubs)
    pali = conc_s["pali"]
    titulo_cap = info["titulo_pali"]

    # migas y pasos
    def paso(m, clase, rotulo, flecha_izq):
        if m is None:
            return ""
        nombre = e(prev_sig_pali[m])
        cont = ('<span aria-hidden="true">←</span> §{0} <i>{1}</i>'.format(m, nombre)
                if flecha_izq else
                '<i>{1}</i> §{0} <span aria-hidden="true">→</span>'.format(m, nombre))
        return '<a class="hub-paso {0}" href="../{1}/" rel="{2}" aria-label="{3}: §{1} {4}">{5}</a>'.format(
            clase, m, "prev" if flecha_izq else "next", rotulo, nombre, cont)

    inicio = raiz + ("?lang=en" if lengua == "en" else "")
    kacc = raiz + "kaccayana/" + ("?lang=en" if lengua == "en" else "")
    migas = (
        '<nav class="hub-migas" aria-label="{0}"><ol>'
        '<li><a href="{1}">{2}</a></li><li><a href="{3}">Kaccāyana</a></li>'
        '<li><a href="{4}">{5}</a></li><li><a href="{4}#kanda-{6}">{7}</a></li>'
        '<li aria-current="page">§{8}</li></ol></nav>').format(
            t["migas"], inicio, t["inicio"], kacc, cap_url, e(titulo_cap),
            s["kanda"], e(kanda_nombre), n)
    pasos = '<div class="hub-pasos">{0}{1}</div>'.format(
        paso(prev, "prev", t["anterior"], True), paso(sig, "sig", t["siguiente"], False))

    # números
    rup = conc_s["rupasiddhi"]
    rup = ", ".join(str(x) for x in rup) if isinstance(rup, list) else str(rup)
    chips = ['<li class="hub-chip-k">{0} {1}</li>'.format(t["kaccayana"], n),
             '<li>{0} {1}</li>'.format(t["rupasiddhi"], e(rup))]
    if conc_s.get("saddaniti_suttamala"):
        chips.append('<li>{0} {1}</li>'.format(
            t["saddaniti"], e(", ".join(conc_s["saddaniti_suttamala"]))))
    chips.append('<li>{0} · {1}</li>'.format(e(titulo_cap), e(kanda_nombre)))

    lq = "?lang=en" if lengua == "en" else ""
    borradores = (
        '<ul class="hub-borradores">'
        '<li><a href="{r}recursos/clasificacion/{lq}#s{n}">{c}</a> <span class="ini-borrador">{b}</span></li>'
        '<li><a href="{r}recursos/analisis/{lq}#s{n}">{a}</a> <span class="ini-borrador">{b}</span></li>'
        '</ul>').format(r=raiz, lq=lq, n=n, c=t["clasif"] + " →", a=t["analisis"] + " →",
                        b=t["borrador"])

    secciones = [("texto", t["texto"])]
    if citas_html:
        secciones.append(("citado", t["citado"]))
    secciones += [("borradores", t["borradores"]), ("preguntar", t["preguntar"].format(n=n))]
    indice = '<nav class="hub-indice" aria-label="{0}"><p>{0}</p>{1}</nav>'.format(
        t["en_pagina"], "".join('<a href="#{0}">{1}</a>'.format(i, x) for i, x in secciones))

    preg_url = "{0}recursos/analisis/?preguntar={1}{2}#s{1}".format(
        raiz, n, "&amp;lang=en" if lengua == "en" else "")
    cuerpo = (
        '<div class="hub-cab">{migas}{pasos}</div>\n'
        '<header class="hub-titulo">\n'
        '<p class="hub-obra">Kaccāyana-Byākaraṇaṃ · {capde}</p>\n'
        '<div class="hub-titulo-fila"><span class="hub-n">§{n}</span>'
        '<h1 lang="pi">{pali}</h1></div>\n'
        '<p class="hub-trad">{trad}</p>\n'
        '<ul class="hub-chips" aria-label="{numeros}">{chips}</ul>\n'
        '</header>\n'
        '<div class="hub-cuerpo">\n{indice}\n<div class="hub-secs">\n'
        '<section class="hub-sec" id="texto" aria-labelledby="t-texto">'
        '<div class="hub-sec-cab"><h2 id="t-texto">{t_texto}</h2>'
        '<a class="hub-leer" href="{cap_url}#s{n}">{leer}</a></div>\n'
        '<div class="hub-sutta">{texto}</div>\n'
        '<p class="hub-nota">{sin_notas}</p></section>\n'
        '{citado}'
        '<section class="hub-sec hub-sec-plana" id="borradores" aria-labelledby="t-borr">'
        '<h2 id="t-borr">{t_borr}</h2>{borradores}</section>\n'
        '<section class="hub-sec hub-preg" id="preguntar" aria-labelledby="t-preg">'
        '<h2 id="t-preg">{t_preg}</h2><p>{preg_txt}</p>'
        '<p><a class="ini-btn prim" href="{preg_url}">{preg_btn}</a></p>'
        '<p class="hub-preg-estado" id="hub-preg-estado" role="status" hidden=""></p></section>\n'
        '</div>\n</div>'
    ).format(
        migas=migas, pasos=pasos, n=n, pali=e(pali), trad=traduccion,
        capde=t["cap_de"].format(n=info["num"]), numeros=t["numeros"],
        chips="".join(chips), indice=indice, t_texto=t["texto"], cap_url=cap_url,
        leer=t["leer"], texto=texto, sin_notas=t["sin_notas"],
        citado=('<section class="hub-sec hub-sec-plana" id="citado" aria-labelledby="t-cit">'
                '<h2 id="t-cit">{0}</h2>{1}</section>\n'.format(t["citado"], citas_html)
                if citas_html else ""),
        t_borr=t["borradores"], borradores=borradores,
        t_preg=t["preguntar"].format(n=n), preg_txt=t["preg_txt"],
        preg_url=preg_url, preg_btn=t["preg_btn"].format(n=n))

    trad_txt = sin_etiquetas(traduccion)
    titulo = "§{0} {1} · Kaccāyana · {2}".format(n, pali, t["titulo_sitio"])
    descripcion = "§{0} {1}. {2} Kaccāyana, {3}.".format(
        n, pali, trad_txt if trad_txt.endswith(".") or not trad_txt else trad_txt + ".",
        titulo_cap)
    html = PAGINA.format(
        lang=lengua, titulo=e(titulo), descripcion=e(re.sub(r"\s+", " ", descripcion)),
        raiz=raiz, v=cabecera.version_assets(), otra_lang=otra, otra_url=otra_url,
        otra_lang_may=otra.upper(), tema=e(cabecera.TEXTOS[lengua]["tema"]),
        cuerpo=cuerpo,
        copyright=GC.COPYRIGHT_EN if lengua == "en" else GC.COPYRIGHT,
        preg_ok=json.dumps(t["preg_ok"], ensure_ascii=False),
        preg_entrar=json.dumps(t["preg_entrar"], ensure_ascii=False))
    return cabecera.insertar(html, "hub", idioma=lengua, otra_url=otra_url, raiz=raiz)


prev_sig_pali = {}


def main():
    t0 = time.time()
    secc = mapa_secciones()
    conc = json.load(open(os.path.join(RAIZ, "comun", "concordancia.json"), encoding="utf-8"))
    por_n = {s["kaccayana"]: s for c in conc["capitulos"].values() for s in c["suttas"]}
    hubs = sorted(int(k) for k in secc["secciones"])
    hubs_set = set(hubs)
    prev_sig_pali.update({n: por_n[n]["pali"] for n in hubs})
    cit = citas(secc)

    escritas = 0
    for lengua in ("es", "en"):
        destino_raiz = os.path.join(SITIO, "s") if lengua == "es" else os.path.join(SITIO, "en", "s")
        for clave, meta in GC.CAPITULOS.items():
            info = secc["capitulos"].get(meta["slug"])
            if not info or (lengua == "en" and not info["en"]):
                continue
            info = dict(info, slug=meta["slug"], titulo_pali=meta["titulo_pali"])
            suttas, cap = cargar_capitulo(clave, lengua)
            for n in hubs:
                if secc["secciones"][str(n)] != meta["slug"]:
                    continue
                i = hubs.index(n)
                prev = hubs[i - 1] if i > 0 else None
                sig = hubs[i + 1] if i + 1 < len(hubs) else None
                s = suttas[n]
                raiz_rel = "../../" if lengua == "es" else "../../../"
                html = pagina(n, lengua, s, por_n[n], info, prev, sig,
                              html_citas(cit.get(n), lengua, raiz_rel, n), hubs_set,
                              cap["kandas_pali"][s["kanda"]])
                d = os.path.join(destino_raiz, str(n))
                os.makedirs(d, exist_ok=True)
                with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
                    f.write(html)
                escritas += 1
    # restos de una generación anterior (un § que dejara de tener tarjeta)
    for raiz_s in (os.path.join(SITIO, "s"), os.path.join(SITIO, "en", "s")):
        if os.path.isdir(raiz_s):
            for nombre in os.listdir(raiz_s):
                if nombre.isdigit() and int(nombre) not in hubs_set:
                    import shutil
                    shutil.rmtree(os.path.join(raiz_s, nombre))
    con_citas = sum(1 for n in hubs if cit.get(n))
    print("{0} páginas de sutta (§{1}–§{2}, ES y EN) · {3} con «Dónde se cita» · {4:.1f} s".format(
        escritas, hubs[0], hubs[-1], con_citas, time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
