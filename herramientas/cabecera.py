#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La cabecera común del sitio (rediseño de la navegación, etapa 1; diseño
aprobado por el IEBH el 2026-10-08).

Una sola fuente para el marcado de la barra que va arriba en las 26 páginas:
el árbol del IEBH y «Gramáticas Pāḷi» → portada; Kaccāyana · Recursos ·
Glosario · Clases; la caja «§» (un número va a ese sutta; lo demás, a la
búsqueda del sitio, desde la etapa 4a); el conmutador ES|EN y el del tema.

Cada generador llama a `insertar(html, clave)` justo antes de escribir su
página. `insertar` pone:

  * en el <head>, la hoja site/assets/cabecera.css (con el mismo ?v= que
    pali.css) y un <style> mínimo que oculta los mandos de la página que la
    barra sustituye;
  * nada más abrir el <body>, la barra;
  * antes de </body>, site/assets/cabecera.js.

La barra NO trae un mecanismo de idioma ni de tema propio: ACCIONA el que
cada página ya tenía (sus botones siguen en el DOM, ocultos, y la barra los
pulsa). Así se conservan las dos URL de los capítulos con su redirección, los
conmutadores de las páginas de una sola URL, las claves `pali_lang`,
`pali_dark` y las de «estudiados», y los dos modos de tema del sitio
(body.dark y html[data-theme=dark]). Qué botón acciona en cada página lo dice
PAGINAS, más abajo.

cabecera.css y cabecera.js son FUENTE, no salida, como pali.css y pali.js:
ningún generador los escribe.
"""

import hashlib
import html as _html
import json
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(RAIZ, "site", "assets")

# ---------------------------------------------------------------- textos
#
# Lo que la barra dice, en las dos lenguas. Va entero en el atributo
# data-textos de la barra para que cabecera.js lo cambie al conmutar la
# lengua en las páginas de una sola URL; la primera pintura sale de aquí.

TEXTOS = {
    "es": {
        "marca": "Gramáticas Pāḷi",
        "inicio": "Inicio · Gramáticas Pāḷi",
        "nav": "Principal",
        "kaccayana": "Kaccāyana",
        "recursos": "Recursos",
        "glosario": "Glosario",
        "clases": "Clases",
        "ir": "Ir a un sutta por su número o buscar en el sitio",
        "ir_ph": "Buscar…",
        "idioma": "Idioma",
        "es": "Español",
        "en": "English",
        "solo_es": "Solo en español",
        "tema": "Modo oscuro",
        "menu": "Menú",
        "no_publicado": "§{n} aún no está publicado",
        "sin_indice": "No se pudo cargar el índice de los suttas",
    },
    "en": {
        "marca": "Pāḷi Grammars",
        "inicio": "Home · Pāḷi Grammars",
        "nav": "Main",
        "kaccayana": "Kaccāyana",
        "recursos": "Resources",
        "glosario": "Glossary",
        "clases": "Classes",
        "ir": "Go to a sutta by its number or search the site",
        "ir_ph": "Search…",
        "idioma": "Language",
        "es": "Español",
        "en": "English",
        "solo_es": "Spanish only",
        "tema": "Dark mode",
        "menu": "Menu",
        "no_publicado": "§{n} is not published yet",
        "sin_indice": "The sutta index could not be loaded",
    },
}

# ---------------------------------------------------------------- páginas
#
#   raiz      prefijo relativo hasta site/
#   seccion   inicio | kaccayana | recursos | glosario | clases
#   indice    True si la página ES la de su sección (aria-current="page");
#             si no, el enlace de la sección lleva aria-current="true"
#   idioma    enlace   dos URL (capítulos): el segmento de la otra lengua es
#                      un enlace, y cabecera.js pulsa el #lang-btn de la
#                      página, que guarda la elección y conserva el #ancla
#             alterna  una URL con un solo conmutador (ctl_idioma)
#             par      una URL con dos botones, uno por lengua
#                      (ctl_idioma = "selector-es|selector-en")
#             solo-es  página sólo en español: la barra lo dice y no conmuta
#   tema      clase    body.dark (capítulos, índices)
#             atributo html[data-theme=dark]
#             medio    html[data-theme] si el lector eligió; si no, el
#                      prefers-color-scheme del sistema (nombre, verbo)
#   ocultar   lo de la página que la barra sustituye: sus mandos de tema y de
#             idioma, que siguen en el DOM porque la barra los acciona

PAGINAS = {
    "portada":     dict(raiz="", seccion="inicio", indice=True,
                        idioma="alterna", ctl_idioma="#lang-btn",
                        tema="clase", ctl_tema="#dark-btn"),
    "kaccayana":   dict(raiz="../", seccion="kaccayana", indice=True,
                        idioma="alterna", ctl_idioma="#lang-btn",
                        tema="clase", ctl_tema="#dark-btn"),
    "recursos":    dict(raiz="../", seccion="recursos", indice=True,
                        idioma="alterna", ctl_idioma="#lang-btn",
                        tema="clase", ctl_tema="#dark-btn"),
    # sólo en español, pero la plantilla de los índices le pone su ES|EN:
    # se oculta como los demás (ctl_idioma), y la barra dice «Solo en español»
    "guia-clases": dict(raiz="../", seccion="clases", indice=True,
                        idioma="solo-es", ctl_idioma="#lang-btn",
                        tema="clase", ctl_tema="#dark-btn"),
    # los capítulos fijan raiz e idioma al llamar (ES ../../, EN ../../../)
    "capitulo":    dict(raiz="../../", seccion="kaccayana", indice=False,
                        idioma="enlace", ctl_idioma="#lang-btn",
                        tema="clase", ctl_tema="#dark-btn"),
    # las páginas de cada sutta (etapa 2): /s/N/ y /en/s/N/, dos URL como
    # los capítulos; su #lang-btn y su #dark-btn ocultos los pone
    # generar_hub.py, y raiz e idioma se fijan al llamar
    "hub":         dict(raiz="../../", seccion="kaccayana", indice=False,
                        idioma="enlace", ctl_idioma="#lang-btn",
                        tema="clase", ctl_tema="#dark-btn"),
    # la búsqueda en todo el sitio (etapa 4a): /buscar/ y /en/buscar/, dos
    # URL como las páginas de sutta; generar_busqueda.py pone su #lang-btn y
    # su #dark-btn ocultos, y raiz e idioma se fijan al llamar. No es ninguna
    # de las secciones de la barra: ningún enlace lleva aria-current.
    "buscar":      dict(raiz="../", seccion="buscar", indice=True,
                        idioma="enlace", ctl_idioma="#lang-btn",
                        tema="clase", ctl_tema="#dark-btn"),
    "sandhi":      dict(raiz="../../", seccion="recursos", indice=False,
                        idioma="solo-es", tema="atributo", ctl_tema="#theme"),
    "solucionador": dict(raiz="../../", seccion="recursos", indice=False,
                         idioma="alterna", ctl_idioma="#en-btn",
                         tema="atributo", ctl_tema="#theme"),
    "nombre":      dict(raiz="../../", seccion="recursos", indice=False,
                        idioma="solo-es", tema="medio",
                        ctl_tema="#themeToggle"),
    "verbo":       dict(raiz="../../", seccion="recursos", indice=False,
                        idioma="alterna", ctl_idioma="#langToggle",
                        tema="medio", ctl_tema="#themeToggle"),
    "paradigmas":  dict(raiz="../../", seccion="recursos", indice=False,
                        idioma="alterna", ctl_idioma="#en-btn",
                        tema="atributo", ctl_tema="#theme"),
    "raices":      dict(raiz="../../", seccion="recursos", indice=False,
                        idioma="alterna", ctl_idioma="#en-btn",
                        tema="atributo", ctl_tema="#theme"),
    "glosario":    dict(raiz="../../", seccion="glosario", indice=True,
                        idioma="par", ctl_idioma="#b-es|#b-en",
                        tema="atributo", ctl_tema="#theme"),
    "casos":       dict(raiz="../../", seccion="recursos", indice=False,
                        idioma="solo-es", tema="atributo", ctl_tema="#theme"),
    "clasificacion": dict(raiz="../../", seccion="recursos", indice=False,
                          idioma="alterna", ctl_idioma="#lang-btn",
                          tema="atributo", ctl_tema="#theme"),
    "analisis":    dict(raiz="../../", seccion="recursos", indice=False,
                        idioma="alterna", ctl_idioma="#lang-btn",
                        tema="atributo", ctl_tema="#theme"),
    "analisis-guia": dict(raiz="../../../", seccion="recursos", indice=False,
                          idioma="alterna", ctl_idioma="#lang-btn",
                          tema="atributo", ctl_tema="#theme"),
    "comentarios": dict(raiz="../../", seccion="recursos", indice=False,
                        idioma="alterna", ctl_idioma="#lang-btn",
                        tema="atributo", ctl_tema="#theme"),
    # documentos en prosa de recursos/*.md (hoy ninguno se publica)
    "recurso":     dict(raiz="../../", seccion="recursos", indice=False,
                        idioma="solo-es", tema="clase", ctl_tema="#dark-btn"),
}

NAV = (("kaccayana", "kaccayana/"), ("recursos", "recursos/"),
       ("glosario", "recursos/glosario/"), ("clases", "guia-clases/"))

# En inglés de dos URL (los capítulos de /en/) los destinos que tienen
# conmutador en la propia página se abren en inglés con ?lang=en. Antes el
# «←» de esos capítulos llevaba a /kaccayana/ sin más, la URL española.
CON_LANG = {"", "kaccayana/", "recursos/", "recursos/glosario/"}

ARCHIVOS_VERSION = ("base.css", "recursos.css", "pali.css", "pali.js",
                    "cabecera.css", "cabecera.js")


def version_assets():
    """Huella de los estilos y la lógica compartidos, para el ?v= que
    invalida la caché al cambiarlos. Una sola para todo el sitio."""
    h = hashlib.md5()
    for f in ARCHIVOS_VERSION:
        ruta = os.path.join(ASSETS, f)
        if os.path.exists(ruta):
            with open(ruta, "rb") as fh:
                h.update(fh.read())
    return h.hexdigest()[:8]


def _e(t):
    return _html.escape(t, quote=True)


ICONO_LUNA = ('<svg class="cab-ico-luna" width="18" height="18" viewBox="0 0 24 24" '
              'fill="none" stroke="currentColor" stroke-width="1.8" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"></path></svg>')
ICONO_SOL = ('<svg class="cab-ico-sol" width="18" height="18" viewBox="0 0 24 24" '
             'fill="none" stroke="currentColor" stroke-width="1.8" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2'
             'M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4'
             'M17.7 6.3l1.4-1.4"></path></svg>')
ICONO_MENU = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" '
              'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
              'aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"></path></svg>')


def cabecera_html(clave, idioma="es", otra_url=None, raiz=None):
    """El marcado de la barra para la página `clave` de PAGINAS."""
    p = dict(PAGINAS[clave])
    if raiz is not None:
        p["raiz"] = raiz
    r = p["raiz"]
    T = TEXTOS[idioma]
    dos_url_en = p["idioma"] == "enlace" and idioma == "en"

    def href(destino):
        h = r + destino if (r + destino) else "./"
        if dos_url_en and destino in CON_LANG:
            h += "?lang=en"
        return h

    marca_cur = ' aria-current="page"' if p["seccion"] == "inicio" else ""
    enlaces = []
    for sec, destino in NAV:
        cur = ""
        if p["seccion"] == sec:
            cur = ' aria-current="{0}"'.format("page" if p["indice"] else "true")
        enlaces.append('<a class="cab-enlace" href="{0}" data-cab-t="{1}"{2}>{3}</a>'
                       .format(href(destino), sec, cur, _e(T[sec])))

    # el conmutador de lengua
    modo = p["idioma"]
    if modo == "solo-es":
        lengua = ('<span class="cab-solo-es" data-cab-t="solo_es">{0}</span>'
                  .format(_e(T["solo_es"])))
    else:
        segs = []
        for l in ("es", "en"):
            actual = (l == idioma)
            if modo == "enlace" and not actual and otra_url:
                segs.append('<a class="cab-seg" data-l="{0}" href="{1}" hreflang="{0}" '
                            'lang="{0}" aria-label="{2}">{3}</a>'
                            .format(l, _e(otra_url), _e(T[l]), l.upper()))
            elif modo == "enlace":
                segs.append('<span class="cab-seg{0}" data-l="{1}" lang="{1}"{2} '
                            'aria-label="{3}">{4}</span>'
                            .format(" cab-cur" if actual else " cab-inactivo", l,
                                    ' aria-current="true"' if actual else "",
                                    _e(T[l]), l.upper()))
            else:
                segs.append('<button type="button" class="cab-seg{0}" data-l="{1}" '
                            'lang="{1}" aria-pressed="{2}" aria-label="{3}">{4}</button>'
                            .format(" cab-cur" if actual else "", l,
                                    "true" if actual else "false", _e(T[l]),
                                    l.upper()))
        lengua = ('<div class="cab-lengua" role="group" aria-label="{0}" '
                  'data-cab-aria="idioma">{1}</div>'.format(_e(T["idioma"]),
                                                           "".join(segs)))

    datos = {
        "data-raiz": r,
        "data-idioma": idioma,
        "data-modo-idioma": modo,
        "data-ctl-idioma": p.get("ctl_idioma", ""),
        "data-tema": p["tema"],
        "data-ctl-tema": p["ctl_tema"],
    }
    atributos = " ".join('{0}="{1}"'.format(k, _e(v)) for k, v in datos.items())
    textos = _e(json.dumps(TEXTOS, ensure_ascii=False, separators=(",", ":")))

    return (
        '<header class="cab" id="cab" {atr} data-textos="{textos}">\n'
        '<div class="cab-in">\n'
        '<a class="cab-marca" href="{inicio}" aria-label="{aria_inicio}" '
        'data-cab-aria="inicio"{marca_cur}><span class="marca-arbol" aria-hidden="true"></span>'
        '<span class="cab-nombre" data-cab-t="marca">{marca}</span></a>\n'
        '<div class="cab-panel" id="cab-panel">\n'
        '<nav class="cab-nav" aria-label="{nav}" data-cab-aria="nav">{enlaces}</nav>\n'
        '<div class="cab-herr">{lengua}'
        '<button type="button" class="cab-tema" aria-pressed="false" aria-label="{tema}" '
        'data-cab-aria="tema">{luna}{sol}</button></div>\n'
        '</div>\n'
        '<form class="cab-ir" data-ir-sutta="" role="search" aria-label="{ir}" '
        'data-cab-aria="ir" action="{buscar}" method="get" novalidate="">'
        '<label class="cab-ir-l" for="cab-ir-n">§<span class="cab-sr" data-cab-t="ir">{ir}</span></label>'
        '<input class="cab-ir-n" id="cab-ir-n" name="q" type="text" '
        'autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="search" '
        'placeholder="{ir_ph}" data-cab-ph="ir_ph"/>'
        '<p class="cab-aviso" role="status" aria-live="polite" hidden=""></p></form>\n'
        '<button type="button" class="cab-menu" aria-expanded="false" aria-controls="cab-panel" '
        'aria-label="{menu}" data-cab-aria="menu">{icono_menu}</button>\n'
        '</div>\n'
        '</header>\n'
        '<div class="cab-hueco" aria-hidden="true"></div>\n'
        '<script>document.documentElement.classList.add("cab-js")</script>\n'
    ).format(atr=atributos, textos=textos, inicio=href(""),
             aria_inicio=_e(T["inicio"]), marca_cur=marca_cur,
             marca=_e(T["marca"]), nav=_e(T["nav"]), enlaces="".join(enlaces),
             lengua=lengua, tema=_e(T["tema"]), luna=ICONO_LUNA, sol=ICONO_SOL,
             ir=_e(T["ir"]), ir_ph=_e(T["ir_ph"]), menu=_e(T["menu"]),
             buscar=_e(r + ("en/" if idioma == "en" and p["idioma"] == "enlace" else "")
                       + "buscar/"),
             icono_menu=ICONO_MENU)


def ocultos(clave):
    """Los mandos de la página que la barra sustituye. Se ocultan, no se
    quitan: la barra los pulsa."""
    p = PAGINAS[clave]
    sel = [p["ctl_tema"]]
    if p.get("ctl_idioma"):
        sel += p["ctl_idioma"].split("|")
    return ",".join(sel)


# Las tres familias de letra de todo el sitio (base.css, --serif, --sans,
# --mono), de una sola petición: Gentium Book Plus para el texto y los
# títulos, Inter para la interfaz, JetBrains Mono para rótulos y cifras.
# Hasta la etapa 4b cada plantilla pedía las suyas, y nombre y verbo traían
# otras tres (Fraunces, Spectral, IBM Plex Mono).
FUENTES = ("https://fonts.googleapis.com/css2?family=Gentium+Book+Plus:ital,wght@"
           "0,400;0,700;1,400;1,700&amp;family=Inter:wght@400;500;600;700"
           "&amp;family=JetBrains+Mono:wght@400;500;600;700&amp;display=swap")

# Las páginas que llevan además recursos.css, la hoja común de los recursos
# (etapa 4b): el bloque del título, el índice lateral, la barra de mandos,
# los botones, las fichas y el pie.
CON_RECURSOS_CSS = {"recursos", "sandhi", "solucionador", "nombre", "verbo",
                    "paradigmas", "raices", "glosario", "casos", "clasificacion",
                    "analisis", "analisis-guia", "comentarios"}

MARCA_INI = "<!-- cabecera:inicio -->"
MARCA_FIN = "<!-- cabecera:fin -->"
_BLOQUE = re.compile(re.escape(MARCA_INI) + r".*?" + re.escape(MARCA_FIN) + r"\n?", re.S)


def insertar(html, clave, idioma="es", otra_url=None, raiz=None):
    """Pone la barra, sus hojas y su guion en una página ya compuesta.

    Arriba del todo del <head>, ANTES de las hojas de la página: las letras,
    base.css (paleta, letra, marca del IEBH) y, en los recursos,
    recursos.css. Van primero para que lo propio de cada página —un tamaño,
    un margen— pueda ajustarlas sin pelear. La hoja de la barra va al final,
    como antes: es la barra la que no debe dejarse tocar.

    Compone además el bloque del título y el pie de los recursos
    (recursos_comun.componer), si la página los trae.

    Es idempotente: si la página ya los lleva (una plantilla que se volviera
    a leer de la salida, por ejemplo), los reemplaza."""
    import recursos_comun
    p = PAGINAS[clave]
    r = p["raiz"] if raiz is None else raiz
    v = version_assets()
    html = _BLOQUE.sub("", html)
    html = recursos_comun.componer(html)
    hojas = ('{ini}\n<link href="https://fonts.googleapis.com" rel="preconnect"/>\n'
             '<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>\n'
             '<link href="{fuentes}" rel="stylesheet"/>\n'
             '<link href="{r}assets/base.css?v={v}" rel="stylesheet"/>\n'
             '{rec}{fin}\n'
             .format(ini=MARCA_INI, fin=MARCA_FIN, r=r, v=v, fuentes=FUENTES,
                     rec=('<link href="{0}assets/recursos.css?v={1}" rel="stylesheet"/>\n'
                          .format(r, v) if clave in CON_RECURSOS_CSS else "")))
    cabeza = ('{ini}\n<link href="{r}assets/cabecera.css?v={v}" rel="stylesheet"/>\n'
              '<style>{ocultos}{{display:none!important}}</style>\n{fin}\n'
              .format(ini=MARCA_INI, fin=MARCA_FIN, r=r, v=v, ocultos=ocultos(clave)))
    barra = "{0}\n{1}{2}\n".format(MARCA_INI, cabecera_html(clave, idioma, otra_url, r),
                                   MARCA_FIN)
    guion = ('{ini}\n<script defer src="{r}assets/cabecera.js?v={v}"></script>\n{fin}\n'
             .format(ini=MARCA_INI, fin=MARCA_FIN, r=r, v=v))
    for marca in ("</head>", "</body>"):
        if html.count(marca) != 1:
            raise ValueError("cabecera.insertar({0}): la página no tiene un solo "
                             "{1}".format(clave, marca))
    # El <body> de verdad es el primero DESPUÉS de </head>: en el <style>
    # de alguna plantilla hay comentarios que dicen «<body>».
    cuerpo = re.compile(r"<body(\s[^>]*)?>\n?")
    if not cuerpo.search(html, html.index("</head>")):
        raise ValueError("cabecera.insertar({0}): la página no tiene <body>".format(clave))
    # las hojas comunes, delante de la primera hoja o estilo de la página
    fin_head = html.index("</head>")
    primera = re.compile(r'<link[^>]*rel="?stylesheet|<link[^>]*rel="?preconnect|<style')
    m = primera.search(html, 0, fin_head)
    pos = m.start() if m else fin_head
    html = html[:pos] + hojas + html[pos:]
    html = html.replace("</head>", cabeza + "</head>", 1)
    m = cuerpo.search(html, html.index("</head>"))
    html = html[:m.end()] + barra + html[m.end():]
    html = html.replace("</body>", guion + "</body>", 1)
    return html


# ---------------------------------------------------------------- tokens
#
# La paleta «hoja de palma» vive SÓLO en site/assets/base.css (etapa 4b).
# Hasta entonces estaba copiada en pali.css, en cabecera.css y en cada
# plantilla de recursos/, y esto comprobaba que las copias coincidieran. Ahora
# comprueba que no vuelva a haber copias: ningún valor de la paleta —los
# colores de base.css, en hexadecimal— en otra hoja de site/assets/ ni en el
# <style> de una plantilla de recursos/. generar_secciones.py lo llama en cada
# regeneración y falla si encuentra alguno.
#
# Excepciones, porque no son la paleta: los colores de impresión (#000,
# #fff…), que no dependen del tema.

def _hex_paleta():
    base = open(os.path.join(ASSETS, "base.css"), encoding="utf-8").read()
    return {h.lower() for h in re.findall(r"--[a-z0-9-]+:\s*(#[0-9A-Fa-f]{6})\b", base)}


def _sin_impresion(css):
    """El CSS sin sus bloques @media print, con las llaves contadas."""
    out, i = [], 0
    for m in re.finditer(r"@media\s+print\s*\{", css):
        if m.start() < i:
            continue
        out.append(css[i:m.start()])
        prof, j = 1, m.end()
        while j < len(css) and prof:
            prof += {"{": 1, "}": -1}.get(css[j], 0)
            j += 1
        i = j
    out.append(css[i:])
    return "".join(out)


def comprobar_tokens():
    """Lista de los sitios fuera de base.css donde aparece un valor de la
    paleta (vacía si no hay ninguno)."""
    paleta = _hex_paleta()
    if len(paleta) < 20:
        return ["base.css: la paleta no está (sólo {0} colores)".format(len(paleta))]
    sitios = [os.path.join(ASSETS, f) for f in sorted(os.listdir(ASSETS))
              if f.endswith((".css", ".js")) and f != "base.css"]
    recursos = os.path.join(RAIZ, "recursos")
    for d in sorted(os.listdir(recursos)):
        for f in ("plantilla.html", "guia-plantilla.html"):
            ruta = os.path.join(recursos, d, f)
            if os.path.exists(ruta):
                sitios.append(ruta)
    malos = []
    for ruta in sitios:
        texto = open(ruta, encoding="utf-8").read()
        if ruta.endswith(".html"):
            texto = "".join(re.findall(r"<style[^>]*>(.*?)</style>", texto, re.S))
        texto = _sin_impresion(texto)
        for h in sorted({x.lower() for x in re.findall(r"#[0-9A-Fa-f]{6}\b", texto)} & paleta):
            malos.append("{0}: {1}".format(os.path.relpath(ruta, RAIZ), h))
    return malos
