#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pasada de visibilidad en buscadores, la última de generar_todo.py.

    python3 herramientas/generar_seo.py

Por qué existe (2026-10-01).  La inspección de URLs de Search Console mostró
que el sitio está indexado, pero ninguna página declaraba su URL canónica, los
capítulos no tenían descripción, la pareja español/inglés solo se anunciaba en
un sentido y con rutas relativas, y no había sitemap.  Tocar cada uno de los
generadores para eso sería repetir lo mismo en veinte sitios; esta pasada lo
hace una vez, sobre la salida ya generada.

Qué hace, en cada site/**/index.html:
  * inserta, antes de </head>, un bloque delimitado por
    <!-- seo:inicio --> … <!-- seo:fin -->  con
      - <link rel="canonical"> absoluto;
      - hreflang recíproco (es, en y x-default=es) cuando existe la página
        par en site/en/… o fuera de ella;
      - <meta name="description"> SOLO si la página no tiene ya una, tomada
        del título y de la línea «hdr-meta» de la cabecera (datos que la
        página ya muestra; no se inventa nada).
  * escribe site/sitemap.xml y site/robots.txt.

Es idempotente: si el bloque ya está, se reemplaza.  No toca nada fuera de él.
"""

import html
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITIO = os.path.join(RAIZ, "site")
BASE = "https://gramaticas.buddha-dhamma.net"

# Rutas que no se anuncian: /clases* está detrás de Cloudflare Access.
EXCLUIDAS = ("/clases",)

BLOQUE = re.compile(r"\n?<!-- seo:inicio -->.*?<!-- seo:fin -->\n?", re.S)


def ruta_url(archivo):
    rel = os.path.relpath(os.path.dirname(archivo), SITIO).replace(os.sep, "/")
    return "/" if rel == "." else "/" + rel + "/"


def par_idioma(ruta):
    """Devuelve (ruta_es, ruta_en) si la página tiene pareja; si no, None."""
    if ruta.startswith("/en/"):
        es, en = ruta[3:], ruta
    else:
        es, en = ruta, "/en" + ruta
    existe = lambda r: os.path.exists(os.path.join(SITIO, r.strip("/"), "index.html"))
    return (es, en) if existe(es) and existe(en) else None


def texto(fragmento):
    sin_etiquetas = re.sub(r"<span[^>]*aria-label.*", "", fragmento, flags=re.S)
    sin_etiquetas = re.sub(r"<[^>]+>", " ", sin_etiquetas)
    return re.sub(r"\s+", " ", html.unescape(sin_etiquetas)).strip()


def descripcion(s):
    m_t = re.search(r"<title>([^<]*)</title>", s)
    m_h = re.search(r'<div class="hdr-meta">(.*?)</div>', s, re.S)
    if not m_t:
        return None
    partes = [html.unescape(m_t.group(1)).strip()]
    if m_h:
        meta = texto(m_h.group(1))
        if meta:
            partes.append(meta)
    d = ". ".join(partes)
    return d[:300]


def bloque(ruta, s):
    lineas = ['<link rel="canonical" href="{0}{1}"/>'.format(BASE, ruta)]
    par = par_idioma(ruta)
    if par:
        es, en = par
        lineas += [
            '<link rel="alternate" hreflang="es" href="{0}{1}"/>'.format(BASE, es),
            '<link rel="alternate" hreflang="en" href="{0}{1}"/>'.format(BASE, en),
            '<link rel="alternate" hreflang="x-default" href="{0}{1}"/>'.format(BASE, es),
        ]
    if 'name="description"' not in s:
        d = descripcion(s)
        if d:
            lineas.append('<meta name="description" content="{0}"/>'.format(
                html.escape(d, quote=True)))
    return "<!-- seo:inicio -->\n" + "\n".join(lineas) + "\n<!-- seo:fin -->\n"


def main():
    rutas = []
    for dirpath, _, files in os.walk(SITIO):
        if "index.html" not in files:
            continue
        archivo = os.path.join(dirpath, "index.html")
        ruta = ruta_url(archivo)
        if ruta.startswith(EXCLUIDAS):
            continue
        s = open(archivo, encoding="utf-8").read()
        if "</head>" not in s:
            print("sin </head>, se omite:", ruta, file=sys.stderr)
            continue
        if re.search(r'<meta[^>]+name="robots"[^>]+noindex', s):
            continue
        s = BLOQUE.sub("\n", s)
        s = s.replace("</head>", bloque(ruta, s) + "</head>", 1)
        open(archivo, "w", encoding="utf-8").write(s)
        rutas.append(ruta)

    rutas.sort(key=lambda r: (r.startswith("/en/"), r.count("/"), r))
    with open(os.path.join(SITIO, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write("<!-- Generado por herramientas/generar_seo.py; no editar a mano. -->\n")
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for r in rutas:
            f.write("  <url><loc>{0}{1}</loc></url>\n".format(BASE, r))
        f.write("</urlset>\n")

    with open(os.path.join(SITIO, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("# Generado por herramientas/generar_seo.py; no editar a mano.\n"
                "User-agent: *\n"
                "Allow: /\n"
                "Disallow: /api/\n\n"
                "Sitemap: {0}/sitemap.xml\n".format(BASE))

    print("{0} páginas con canónica; sitemap.xml y robots.txt escritos".format(len(rutas)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
