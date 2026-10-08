#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La cabecera común del sitio (rediseño de la navegación, etapa 1; diseño
aprobado por el IEBH el 2026-10-08).

Una sola fuente para el marcado de la barra que va arriba en las 26 páginas:
el árbol del IEBH y «Gramáticas Pāḷi» → portada; Kaccāyana · Recursos ·
Glosario · Clases; la caja «Ir a §»; el conmutador ES|EN y el del tema.

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
        "ir": "Ir al sutta número",
        "ir_ph": "Ir a §…",
        "idioma": "Idioma",
        "es": "Español",
        "en": "English",
        "solo_es": "Solo en español",
        "tema": "Modo oscuro",
        "menu": "Menú",
        "no_publicado": "§{n} aún no está publicado",
        "no_numero": "Escriba un número de sutta, por ejemplo 290",
        "sin_indice": "No se pudo cargar el índice de los suttas",
        "palabras": "La búsqueda en todo el sitio llega en una etapa posterior.",
        "ver_recursos": "Cada recurso tiene su propio buscador: ver los recursos",
    },
    "en": {
        "marca": "Pāḷi Grammars",
        "inicio": "Home · Pāḷi Grammars",
        "nav": "Main",
        "kaccayana": "Kaccāyana",
        "recursos": "Resources",
        "glosario": "Glossary",
        "clases": "Classes",
        "ir": "Go to sutta number",
        "ir_ph": "Go to §…",
        "idioma": "Language",
        "es": "Español",
        "en": "English",
        "solo_es": "Spanish only",
        "tema": "Dark mode",
        "menu": "Menu",
        "no_publicado": "§{n} is not published yet",
        "no_numero": "Type a sutta number, for example 290",
        "sin_indice": "The sutta index could not be loaded",
        "palabras": "Site-wide search comes in a later stage.",
        "ver_recursos": "Each resource has its own search: see the resources",
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

ARCHIVOS_VERSION = ("pali.css", "pali.js", "cabecera.css", "cabecera.js")


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
        '<form class="cab-ir" data-ir-sutta="" aria-label="{ir}" '
        'data-cab-aria="ir" novalidate="">'
        '<label class="cab-ir-l" for="cab-ir-n">§<span class="cab-sr" data-cab-t="ir">{ir}</span></label>'
        '<input class="cab-ir-n" id="cab-ir-n" name="n" type="text" inputmode="numeric" '
        'autocomplete="off" enterkeyhint="go" placeholder="{ir_ph}" data-cab-ph="ir_ph"/>'
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
             icono_menu=ICONO_MENU)


def ocultos(clave):
    """Los mandos de la página que la barra sustituye. Se ocultan, no se
    quitan: la barra los pulsa."""
    p = PAGINAS[clave]
    sel = [p["ctl_tema"]]
    if p.get("ctl_idioma"):
        sel += p["ctl_idioma"].split("|")
    return ",".join(sel)


# Las letras de la barra: Gentium para la marca y el §, Inter para lo demás,
# las de pali.css. Las páginas de recursos/ no cargaban Inter, y algunas
# (nombre, verbo) tampoco Gentium.
FUENTES = ("https://fonts.googleapis.com/css2?family=Gentium+Book+Plus:wght@400;700"
           "&amp;family=Inter:wght@400;500;600&amp;display=swap")

MARCA_INI = "<!-- cabecera:inicio -->"
MARCA_FIN = "<!-- cabecera:fin -->"
_BLOQUE = re.compile(re.escape(MARCA_INI) + r".*?" + re.escape(MARCA_FIN) + r"\n?", re.S)


def insertar(html, clave, idioma="es", otra_url=None, raiz=None):
    """Pone la barra, su hoja y su guion en una página ya compuesta.

    Es idempotente: si la página ya los lleva (una plantilla que se volviera
    a leer de la salida, por ejemplo), los reemplaza."""
    p = PAGINAS[clave]
    r = p["raiz"] if raiz is None else raiz
    v = version_assets()
    html = _BLOQUE.sub("", html)
    cabeza = ('{ini}\n<link href="{fuentes}" rel="stylesheet"/>\n'
              '<link href="{r}assets/cabecera.css?v={v}" rel="stylesheet"/>\n'
              '<style>{ocultos}{{display:none!important}}</style>\n{fin}\n'
              .format(ini=MARCA_INI, fin=MARCA_FIN, r=r, v=v, ocultos=ocultos(clave),
                      fuentes=FUENTES))
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
    html = html.replace("</head>", cabeza + "</head>", 1)
    m = cuerpo.search(html, html.index("</head>"))
    html = html[:m.end()] + barra + html[m.end():]
    html = html.replace("</body>", guion + "</body>", 1)
    return html


# ---------------------------------------------------------------- tokens
#
# cabecera.css repite los valores de la paleta «hoja de palma» de pali.css,
# porque la mitad de las páginas (las de recursos/) no cargan pali.css. Para
# que no se separen, esto comprueba que coincidan; generar_secciones.py lo
# llama en cada regeneración y falla si no.

TOKENS = ("bg", "bg2", "bg3", "text", "text2", "text3", "border", "border2",
          "accent", "accent-bg", "accent-mid", "haritala")


def _tokens(bloque):
    return {k: v.strip() for k, v in re.findall(r"--([a-z0-9-]+):\s*([^;]+);", bloque)}


def comprobar_tokens():
    """Lista de discrepancias entre cabecera.css y pali.css (vacía si
    coinciden)."""
    pali = open(os.path.join(ASSETS, "pali.css"), encoding="utf-8").read()
    cab = open(os.path.join(ASSETS, "cabecera.css"), encoding="utf-8").read()
    claro_p = _tokens(re.search(r":root\s*\{(.*?)\}", pali, re.S).group(1))
    oscuro_p = _tokens(re.search(r"body\.dark\s*\{(.*?)\}", pali, re.S).group(1))
    claro_c = _tokens(re.search(r"/\*claro\*/(.*?)\}", cab, re.S).group(1))
    oscuro_c = _tokens(re.search(r"/\*oscuro\*/(.*?)\}", cab, re.S).group(1))
    malos = []
    for nombre, p, c in (("claro", claro_p, claro_c), ("oscuro", oscuro_p, oscuro_c)):
        for t in TOKENS:
            if p.get(t, "").lower() != c.get("cab-" + t, "").lower():
                malos.append("{0} --{1}: pali.css {2!r}, cabecera.css {3!r}".format(
                    nombre, t, p.get(t), c.get("cab-" + t)))
    return malos
