#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
El bloque del título y el pie de las páginas de recursos (rediseño de la
navegación, etapa 4b, 2026-10-08).

Una sola fuente para su MARCADO. Lo que cada página dice —el rótulo de la
ceja, el título, la descripción, las insignias, las notas y la licencia— se
queda en su plantilla, dentro de unas etiquetas de trabajo que nunca llegan
al sitio:

    <rc-titulo>
      <rc-volver href="../">← …</rc-volver>   el enlace de vuelta, si la barra
                                                 común no lleva allí (opcional)
      <rc-ceja>Instituto de Estudios Buddhistas Hispano</rc-ceja>
      <rc-h1 data-t="title">Análisis de los suttas de Kaccāyana</rc-h1>
      <rc-sub>según <i>Visuddhāyuṃ</i></rc-sub>                  (opcional)
      <rc-desc data-t-html="intro"></rc-desc>                     (opcional)
      <rc-insignias>…</rc-insignias>   la versión y, si lo es, la etiqueta
                                       <span class="borrador">  (opcional)
      <rc-lado>…</rc-lado>          lo que va a la derecha del título (opcional)
      <rc-debajo>…</rc-debajo>      lo que va debajo, a todo el ancho (opcional)
    </rc-titulo>

    <rc-pie>
      <rc-notas resumen="Notas, cifras y fuentes">…</rc-notas>   (opcional;
                         o un <summary> propio al principio del contenido)
      <rc-licencia>…</rc-licencia>
      <rc-extra>…</rc-extra>      lo que la página tenga además, donde vaya
    </rc-pie>

`componer(html)` las cambia por el marcado común, cuyas clases estila
site/assets/recursos.css. Los atributos de una etiqueta de trabajo pasan al
elemento que la sustituye (un `class` se suma al de la pieza), de modo que
los `id`, los `data-t` de las páginas bilingües y los `i-es`/`i-en` siguen
donde la lógica de cada página los busca.

Lo llama herramientas/cabecera.py (insertar) en cada página que las lleve:
ningún generador tiene que acordarse.
"""

import html as _html
import re

_ETQ = re.compile(r"<rc-([a-z0-9]+)((?:\s+[^>]*)?)>(.*?)</rc-\1>", re.S)
_ATR = re.compile(r'([a-zA-Z_:][-a-zA-Z0-9_:.]*)(?:\s*=\s*"([^"]*)")?')

# los atributos que son de la pieza y no del elemento
_PROPIOS = {"resumen"}


def _atributos(cadena):
    return [(k, v) for k, v in _ATR.findall(cadena or "")]


def _abrir(etiqueta, clase, atributos):
    """«<etiqueta class="clase …" …>» con los atributos de la etiqueta de
    trabajo, el `class` sumado y los propios de la pieza fuera."""
    clases = [clase] if clase else []
    resto = []
    for k, v in atributos:
        if k in _PROPIOS:
            continue
        if k == "class":
            clases += v.split()
        elif v == "":
            resto.append(k)          # atributo sin valor: hidden, open…
        else:
            resto.append('{0}="{1}"'.format(k, v))
    partes = [etiqueta]
    if clases:
        partes.append('class="{0}"'.format(" ".join(clases)))
    return "<" + " ".join(partes + resto) + ">"


def _piezas(cuerpo):
    """{nombre: [(atributos, contenido)]} de las etiquetas de trabajo de un
    bloque, en su orden."""
    out = {}
    for m in _ETQ.finditer(cuerpo):
        out.setdefault(m.group(1), []).append((_atributos(m.group(2)), m.group(3).strip()))
    return out


def _attr(atributos, nombre, defecto=None):
    for k, v in atributos:
        if k == nombre:
            return _html.unescape(v) if v else ""
    return defecto


_PIEZAS_TITULO = {"volver", "ceja", "h1", "sub", "desc", "insignias", "lado", "debajo"}


def titulo(cuerpo, atributos=()):
    """El bloque del título: ceja con el árbol del IEBH, h1, subtítulo,
    descripción de una línea e insignias (versión, «borrador»)."""
    p = _piezas(cuerpo)
    raras = set(p) - _PIEZAS_TITULO
    if raras:
        raise ValueError("recursos_comun.titulo: pieza desconocida <rc-{0}>"
                         .format(sorted(raras)[0]))
    lineas = [_abrir("header", "rc-titulo", atributos),
              '<div class="wrap rc-mast">', '<div class="rc-titulo-texto">']
    for a, c in p.get("volver", []):
        lineas.append(_abrir("a", "volver-sitio", a) + c + "</a>")
    for a, c in p.get("ceja", []):
        lineas.append(_abrir("p", "eyebrow-iebh", a)
                      + '<span class="marca-arbol" aria-hidden="true"></span>'
                      '<span class="lbl">{0}</span></p>'.format(c))
    for a, c in p.get("h1", []):
        lineas.append(_abrir("h1", "rc-h1", a) + c + "</h1>")
    for a, c in p.get("sub", []):
        lineas.append(_abrir("p", "rc-sub", a) + c + "</p>")
    for a, c in p.get("desc", []):
        lineas.append(_abrir("p", "tag", a) + c + "</p>")
    for a, c in p.get("insignias", []):
        lineas.append(_abrir("div", "rc-insignias", a) + c + "</div>")
    lineas.append("</div>")
    for a, c in p.get("lado", []):
        lineas.append(_abrir("div", "rc-lado", a) + c + "</div>")
    lineas.append("</div>")
    for a, c in p.get("debajo", []):
        lineas.append(_abrir("div", "wrap rc-debajo", a) + c + "</div>")
    lineas.append("</header>")
    return "\n".join(lineas)


def pie(cuerpo, atributos=()):
    """El pie: las notas plegadas, el imagotipo del IEBH con la licencia y,
    si la página lo tiene, algo más (<rc-extra>), en el orden en que vienen."""
    lineas = [_abrir("footer", "rc-pie", atributos), '<div class="wrap">']
    for m in _ETQ.finditer(cuerpo):
        nombre, a, c = m.group(1), _atributos(m.group(2)), m.group(3).strip()
        if nombre == "notas":
            # el rótulo: el atributo «resumen», o un <summary> propio al
            # principio (cuando lleva marcado: las dos lenguas, un id…)
            if c.startswith("<summary"):
                cabeza = ""
            else:
                cabeza = ("<summary>" + _html.escape(_attr(a, "resumen", "Notas, cifras y fuentes"))
                          + "</summary>\n")
            lineas.append(_abrir("details", "pie-notas", a) + cabeza + c + "\n</details>")
        elif nombre == "licencia":
            lineas.append(_abrir("p", "licencia", a)
                          + '<span class="marca-lockup" aria-hidden="true"></span>' + c + "</p>")
        elif nombre == "extra":
            lineas.append(c)
        else:
            raise ValueError("recursos_comun.pie: pieza desconocida <rc-{0}>".format(nombre))
    lineas += ["</div>", "</footer>"]
    return "\n".join(lineas)


_BLOQUES = (("titulo", titulo), ("pie", pie))


def componer(html):
    """Cambia <rc-titulo> y <rc-pie> por el marcado común. Una página sin
    ellos sale igual."""
    for nombre, f in _BLOQUES:
        patron = re.compile(r"<rc-{0}((?:\s+[^>]*)?)>(.*?)</rc-{0}>".format(nombre), re.S)
        html = patron.sub(lambda m: f(m.group(2), _atributos(m.group(1))), html)
    if "<rc-" in html:
        resto = sorted(set(re.findall(r"<rc-[a-z0-9]+", html)))
        raise ValueError("recursos_comun: quedan etiquetas de trabajo sin componer: "
                         + ", ".join(resto))
    return html
