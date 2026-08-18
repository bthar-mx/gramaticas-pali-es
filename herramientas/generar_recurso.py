#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el HTML de un documento en prosa (no un capítulo de gramática).

    python3 herramientas/generar_recurso.py recursos/combinacion-eufonica.md

Para material de apoyo: reglas, glosarios, tablas de declinación, ejercicios.
Los capítulos de las gramáticas usan generar_capitulo.py, que entiende
suttas, kaṇḍas y numeración triple; este script sólo entiende prosa:
encabezados, párrafos, listas anidadas y tablas.

El markdown puede llevar encabezamiento YAML (title, author, source_pdf,
estado…). Si `estado` empieza por "sin verificar", la página lo advierte.
"""

import html
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ── Encabezamiento YAML ─────────────────────────────────────────────────

def separar_portada(txt):
    if not txt.startswith("---"):
        return {}, txt
    fin = txt.find("\n---", 3)
    if fin == -1:
        return {}, txt
    meta = {}
    for l in txt[3:fin].split("\n"):
        m = re.match(r'^([a-zA-Z_]+):\s*(.*)$', l.strip())
        if m:
            v = m.group(2).strip().strip('"').strip("'")
            meta[m.group(1)] = v
    return meta, txt[fin + 4:]


# ── Texto en línea ──────────────────────────────────────────────────────

def inline(t):
    t = html.escape(t, quote=False)
    t = t.replace("&lt;br&gt;", "<br/>")
    t = t.replace("&lt;sup&gt;", "<sup>").replace("&lt;/sup&gt;", "</sup>")
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'__(.+?)__', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!_)_([^_]+)_(?!_)', r'<i>\1</i>', t)
    t = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', t)
    t = re.sub(r'\[(.+?)\]\((https?://[^)]+)\)', r'<a href="\2">\1</a>', t)
    return t


def solo_texto(t):
    """Título limpio para el id de un encabezado."""
    t = re.sub(r'[*_`]', '', t)
    t = re.sub(r'\s+', '-', t.strip().lower())
    t = re.sub(r'[^a-z0-9áéíóúüñāīūṃṇṭḍñṅḷ\-]', '', t)
    return re.sub(r'-+', '-', t).strip('-')


# ── Bloques ─────────────────────────────────────────────────────────────

RE_H = re.compile(r'^(#{1,4})\s+(.*)$')
RE_LI = re.compile(r'^(\s*)([-*]|\d+[.)])\s+(.*)$')
RE_FILA = re.compile(r'^\s*\|(.+)\|\s*$')


def celdas(l):
    return [c.strip() for c in RE_FILA.match(l).group(1).split("|")]


def es_separador(l):
    return RE_FILA.match(l) and all(
        re.fullmatch(r':?-{2,}:?', c) for c in celdas(l) if c)


def render(lineas):
    out, i, indice = [], 0, []
    ultima_cabecera = [None]
    while i < len(lineas):
        l = lineas[i]
        t = l.strip()

        if not t:
            i += 1
            continue

        # tabla — un tramo seguido de filas.
        # La conversión del PDF parte las tablas en cada encabezado y sólo la
        # primera lleva fila de cabecera; las siguientes reutilizan la misma.
        if RE_FILA.match(l):
            j = i
            while j < len(lineas) and RE_FILA.match(lineas[j]):
                j += 1
            tramo = lineas[i:j]
            i = j
            cab = None
            if len(tramo) > 1 and es_separador(tramo[1]):
                cab = celdas(tramo[0])
                cuerpo = [celdas(x) for x in tramo[2:]]
                ultima_cabecera[0] = cab
            else:
                cuerpo = [celdas(x) for x in tramo]
                previa = ultima_cabecera[0]
                if previa and cuerpo and len(cuerpo[0]) == len(previa):
                    cab = previa
            if not cuerpo:
                continue
            th = ("<thead><tr>{0}</tr></thead>".format(
                "".join("<th>{0}</th>".format(inline(c)) for c in cab))
                if cab else "")
            tr = "".join(
                "<tr>{0}</tr>".format(
                    "".join("<td>{0}</td>".format(inline(c)) for c in fila))
                for fila in cuerpo)
            out.append('<div class="doc-tabla-wrap"><table class="doc-tabla">'
                       '{0}<tbody>{1}</tbody></table></div>'.format(th, tr))
            continue

        # encabezado
        mh = RE_H.match(t)
        if mh:
            n = len(mh.group(1))
            texto = re.sub(r'^\*\*|\*\*$', '', mh.group(2).strip()).strip()
            texto = re.sub(r'\*\*', '', texto)
            ident = solo_texto(texto)
            if n <= 2:
                indice.append((n, ident, texto))
            out.append('<h{0} id="{1}">{2}</h{0}>'.format(
                min(n + 1, 6), ident, inline(texto)))
            i += 1
            continue

        # listas (con anidamiento por sangría)
        if RE_LI.match(l):
            bloque, base = [], None
            while i < len(lineas):
                if not lineas[i].strip():
                    # una línea en blanco no corta la lista si sigue habiendo ítems
                    j = i + 1
                    while j < len(lineas) and not lineas[j].strip():
                        j += 1
                    if j < len(lineas) and RE_LI.match(lineas[j]):
                        i = j
                        continue
                    break
                m = RE_LI.match(lineas[i])
                if not m:
                    break
                sangria = len(m.group(1).expandtabs(4))
                if base is None:
                    base = sangria
                nivel = max(0, (sangria - base) // 3)
                marca = m.group(2)
                texto = m.group(3).strip()
                # El documento trae su propia numeración (I., 1.1., …).
                # Se conserva literal para no duplicarla ni contradecirla.
                if marca not in ("-", "*"):
                    texto = "{0} {1}".format(marca, texto)
                bloque.append((nivel, texto))
                i += 1
            out.append(render_lista(bloque))
            continue

        # fila de tabla suelta (sin fila separadora): se trata como párrafo
        if RE_FILA.match(l):
            out.append("<p>{0}</p>".format(
                inline(" · ".join(c for c in celdas(l) if c))))
            i += 1
            continue

        # párrafo
        buf = []
        while i < len(lineas) and lineas[i].strip() \
                and not RE_H.match(lineas[i].strip()) \
                and not RE_LI.match(lineas[i]) and not RE_FILA.match(lineas[i]):
            buf.append(lineas[i].strip())
            i += 1
        if not buf:                       # nunca dejar de avanzar
            buf.append(lineas[i].strip())
            i += 1
        out.append("<p>{0}</p>".format(inline(" ".join(buf))))

    return "\n".join(out), indice


def render_lista(items, nivel=0):
    """Listas anidadas; la sublista va dentro del <li> que la introduce."""
    if not items:
        return ""
    partes, i, abierto = ['<ul class="doc-lista">'], 0, False
    while i < len(items):
        n, texto = items[i]
        if n > nivel:
            sub, j = [], i
            while j < len(items) and items[j][0] > nivel:
                sub.append(items[j]); j += 1
            partes.append(render_lista(sub, nivel + 1))
            i = j
            continue
        if abierto:
            partes.append("</li>")
        partes.append("<li>{0}".format(inline(texto)))
        abierto = True
        i += 1
    if abierto:
        partes.append("</li>")
    partes.append("</ul>")
    return "".join(partes)


PLANTILLA = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{titulo} · Gramáticas Pāḷi en español</title>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Gentium+Book+Plus:ital,wght@0,400;0,700;1,400;1,700&amp;family=Inter:wght@400;500;700&amp;family=JetBrains+Mono:wght@400;700&amp;display=swap" rel="stylesheet"/>
<link href="../../assets/pali.css" rel="stylesheet"/>
</head>
<body>
<main class="doc">
<a class="idx-back" href="../">← Recursos</a>
<p class="idx-eyebrow">{eyebrow}</p>
<h1>{titulo}</h1>
{autoria}
{aviso}
{cuerpo}
<div class="idx-foot">
{pie}
</div>
</main>
<script>
(function () {{
  var b = document.createElement('button');
  b.id = 'dark-btn'; b.type = 'button';
  b.setAttribute('aria-label', 'Modo oscuro');
  b.textContent = '◐';
  b.onclick = function () {{
    document.body.classList.toggle('dark');
    try {{ localStorage.setItem('pali_dark', document.body.classList.contains('dark') ? '1' : '0'); }} catch (e) {{}}
  }};
  document.body.appendChild(b);
  try {{ if (localStorage.getItem('pali_dark') === '1') document.body.classList.add('dark'); }} catch (e) {{}}
}})();
</script>
</body>
</html>
'''


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    ruta = sys.argv[1]
    ruta_abs = ruta if os.path.isabs(ruta) else os.path.join(RAIZ, ruta)
    meta, cuerpo_md = separar_portada(open(ruta_abs, encoding="utf-8").read())

    cuerpo, indice = render(cuerpo_md.split("\n"))

    titulo = meta.get("title") or os.path.basename(ruta_abs).replace(".md", "")
    autoria = ""
    if meta.get("author"):
        autoria = '<p class="doc-autor">{0}</p>'.format(html.escape(meta["author"]))

    aviso = ""
    if meta.get("estado", "").lower().startswith("sin verificar"):
        aviso = ('<div class="doc-aviso"><strong>Texto sin verificar.</strong> '
                 'Conversión automática pendiente de cotejo con el original; '
                 'puede contener errores de transcripción.</div>')

    pie = []
    if meta.get("copyright"):
        pie.append(html.escape(meta["copyright"]))
    if meta.get("publicacion_iebh"):
        pie.append("Publicación IEBH: {0}".format(html.escape(meta["publicacion_iebh"])))
    if meta.get("source_pdf"):
        pie.append("Original: {0}".format(html.escape(meta["source_pdf"])))
    pie.append('<a href="https://github.com/admin-iebh/gramaticas-pali-es">'
               'github.com/admin-iebh/gramaticas-pali-es</a>')

    nombre = os.path.splitext(os.path.basename(ruta_abs))[0]
    destino = os.path.join(RAIZ, "site", "recursos", nombre, "index.html")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(PLANTILLA.format(
            titulo=html.escape(titulo),
            eyebrow=html.escape(meta.get("basado_en", "Recurso")),
            autoria=autoria, aviso=aviso, cuerpo=cuerpo,
            pie=" · ".join(pie)))

    print("{0} encabezados · {1} tablas · {2} listas → {3}".format(
        len(indice), cuerpo.count('class="doc-tabla"'),
        cuerpo.count('class="doc-lista"'),
        os.path.relpath(destino, RAIZ)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
