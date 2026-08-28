#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera las tres páginas de índice del sitio.

    python3 herramientas/generar_indices.py

Escribe:

    site/index.html             portada — las cuatro obras
    site/kaccayana/index.html   los ocho capítulos de Kaccāyana
    site/recursos/index.html    el material de apoyo

Lo que antes había que corregir a mano —«1 de 8 capítulos», «51 suttas»—
se cuenta ahora del markdown: publicar un capítulo es añadirlo a CAPITULOS
en generar_capitulo.py y dejar su .md en su sitio; la insignia, el total y
la tarjeta se actualizan solos. Un capítulo cuyo .md no exista todavía sale
como «prevista», sin enlace.
"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "herramientas"))

from generar_capitulo import CAPITULOS, parsear, version_assets  # noqa: E402

# ---------------------------------------------------------------- datos

# Los ocho capítulos de Kaccāyana. El número, el título y la descripción
# viven aquí; si el capítulo está publicado, el slug y el recuento de suttas
# salen de CAPITULOS y del markdown.
CAPITULOS_KACC = [
    (1, "Sandhi-Kappa", "01-sandhi-kappa",
     "Capítulo de <i>sandhi</i> — la combinación eufónica de letras."),
    (2, "Nāma-Kappa", "02-nama-kappa",
     "Capítulo del nombre — declinación nominal y pronominal."),
    (3, "Kāraka-Kappa", "03-karaka-kappa",
     "Capítulo de casos gramaticales — las relaciones sintácticas y las "
     "inflexiones que las expresan."),
    (4, "Samāsa-Kappa", "04-samasa-kappa", "Capítulo de los compuestos."),
    (5, "Taddhita-Kappa", "05-taddhita-kappa",
     "Capítulo de los derivados nominales."),
    (6, "Ākhyāta-Kappa", "06-akhyata-kappa", "Capítulo del verbo."),
    (7, "Kibbidhāna-Kappa", "07-kibbidhana-kappa",
     "Capítulo de los sufijos primarios."),
    (8, "Uṇādi-Kappa", "08-unadi-kappa",
     "Capítulo de los sufijos <i>uṇādi</i>."),
]

# Coletilla propia de cada capítulo publicado: rango de suttas y secciones.
DETALLE = {
    1: "§1–§51, en cinco kaṇḍas.",
    2: "§52–§270, en cinco kaṇḍas.",
    3: "§271–§315, sexta sección del Nāma-kappa.",
}

OBRAS = [
    ("kaccayana/", "Kacc<span class=\"dia\">ā</span>yana-By<span class=\"dia\">ā"
     "</span>kara<span class=\"dia\">ṇ</span>a<span class=\"dia\">ṃ</span>",
     "Gramática de Kaccāyana. La más antigua de las gramáticas pāḷi. "
     "Edición base: Bhikkhu U Nandisena (ITBMU)."),
    (None, "Nyāsa",
     "Atribuido a Vimalabuddhi (siglo XI), y llamado también "
     "<i>Mukhamattadīpanī</i>. El comentario clásico de la gramática de "
     "Kaccāyana: recorre los aforismos uno a uno y suple lo que la brevedad "
     "del aforismo calla. El proyecto ya lo consulta y utiliza como fuente "
     "de segunda capa."),
    (None, "Padarūpasiddhi",
     "De Buddhappiya. Reordena el material de Kaccāyana por temas."),
    (None, "Saddanīti", "De Aggavaṃsa. La gramática pāḷi más extensa."),
    (None, "Nirutti-dīpanī",
     "De Ledi Sayadaw. Una gramática moderna en siete capítulos en el mismo "
     "orden que Kaccāyana."),
]

RECURSOS = [
    ("sandhi/", "__SANDHI_BADGE__", "Sandhi — referencia interactiva",
     "Las reglas de combinación eufónica y los 51 aforismos del Sandhi-Kappa, "
     "con la derivación paso a paso de cada forma y la concordancia entre "
     "Kaccāyana, Rūpasiddhi y Saddanīti. Buscador que ignora los diacríticos."),
    ("solucionador/", "88 % del banco", "Solucionador de sandhis",
     "Pegue un pasaje pāḷi: cuántos sandhis hay, cuáles son las voces, y qué "
     "secuencia de aforismos de Kaccāyana explica cada una. Toda lectura se "
     "verifica por recomposición; se afirma una sola cuando hay autoridad "
     "detrás y se declara la duda cuando no la hay. El léxico es el corpus "
     "del Sexto Concilio. Publicado con su cobertura medida a la vista."),
    ("nombre/", "10 pasos", "Formación del nombre — pācako",
     "La derivación de <i>pācako</i> «uno que cocina» paso a paso, de la raíz "
     "<i>√paca</i> al nominativo singular, con el aforismo que ampara cada "
     "paso. Cruza el Kibbidhāna, el Nāma-Kappa y el Sandhi-Kappa."),
    ("paradigmas/", "__PARADIGMAS_BADGE__", "Paradigmas de declinación",
     "Los 83 paradigmas de declinación nominal y pronominal de la lengua "
     "pāḷi, con "
     "todas las variantes de cada forma: nombres por género y tema, "
     "pronombres, numerales y los sufijos que son inflexiones. Buscador que "
     "ignora los diacríticos y filtros por género y por tema."),
    ("raices/", "__RAICES_BADGE__", "Raíces pāḷi comparadas con las sánscritas",
     "Las raíces de la <i>Dhātumālā</i> del <i>Saddanīti</i> con su "
     "significado en español y en inglés, la raíz sánscrita correspondiente "
     "cuando la hay, y el <i>gaṇa</i> y la página de cada una, del libro "
     "<i>Pali Roots in Saddanīti</i> del Ven. U Sīlānanda, editado por "
     "Bhikkhu Nandisena. Con el índice inverso, que va del "
     "sentido a las raíces que lo expresan, y el <i>Dhātupāṭha</i> y la "
     "<i>Dhātumañjūsā</i> de Andersen y Smith concordados lema a lema."),
]

# Fuera de este sitio. Van en su propia sección y marcadas como externas:
# «Disponible» significa material del IEBH alojado aquí, y conviene que
# seguir siendo verdad.
CORPUS = [
    ("https://buddha-dhamma.net/", "118 volúmenes",
     "Chaṭṭhasaṅgītipiṭaka — Tipiṭaka del Sexto Concilio",
     "La edición del Sexto Concilio romanizada: canon, comentarios y "
     "subcomentarios enlazados capa a capa, de modo que desde cualquier "
     "párrafo se llega a su aṭṭhakathā y su ṭīkā. 83.751 párrafos y 54.036 "
     "variantes, con búsqueda que ignora los diacríticos."),
]

FUENTES = ('<a href="https://github.com/bthar-mx/gramaticas-pali-es">'
           'github.com/bthar-mx/gramaticas-pali-es</a>')

# ---------------------------------------------------------------- plantilla

# El script del tema va justo tras <body> para que la clase esté puesta
# antes de pintar: si se deja al final, quien tenga el modo oscuro guardado
# ve un fogonazo blanco en cada carga.
PAGINA = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{titulo}</title>
<meta content="{descripcion}" name="description"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Gentium+Book+Plus:ital,wght@0,400;0,700;1,400;1,700&amp;family=Inter:wght@400;500&amp;family=JetBrains+Mono:wght@400&amp;display=swap" rel="stylesheet"/>
<link href="{raiz}assets/favicon.svg" rel="icon" type="image/svg+xml"/>
<link href="{raiz}assets/pali.css?v={assets_v}" rel="stylesheet"/>
</head>
<body>
<script>/* Tema guardado, antes de pintar. */
try{{var _d=localStorage.getItem('pali_dark');
if(_d==='1'||(_d===null&&matchMedia('(prefers-color-scheme: dark)').matches))
document.body.classList.add('dark');}}catch(e){{}}</script>
<main class="idx">
{volver}
<p class="idx-eyebrow"><span class="marca-arbol"></span>{eyebrow}</p>
<h1 class="display">{h1}</h1>
{cuerpo}
<div class="idx-foot">
<span class="marca-lockup"></span>
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
}})();
</script>
</body>
</html>
"""


def tarjeta(href, insignia, titulo, desc, wip=False, externo=False):
    ins = ""
    if insignia:
        ins = '      <span class="idx-badge{0}">{1}</span>\n'.format(
            " wip" if wip else "", insignia)
    marca = ('<span aria-hidden="true" class="idx-ext">↗</span>'
             if externo else "")
    cuerpo = ('{0}      <span class="t">{1}{2}</span>\n'
              '      <span class="d">{3}</span>\n').format(
                  ins, titulo, marca, desc)
    if href and externo:
        interior = ('    <a class="idx-card ext" href="{0}" '
                    'rel="noopener" target="_blank">\n{1}    </a>').format(
                        href, cuerpo)
    elif href:
        interior = '    <a class="idx-card" href="{0}">\n{1}    </a>'.format(
            href, cuerpo)
    else:
        interior = '    <div class="idx-card pend">\n{0}    </div>'.format(cuerpo)
    return "  <li>\n{0}\n  </li>".format(interior)


def lista(tarjetas):
    return '<ul class="idx-list">\n{0}\n</ul>'.format("\n".join(tarjetas))


# ---------------------------------------------------------------- recuentos

def capitulos_publicados():
    """[(num, slug, n_suttas)] de los capítulos de Kaccāyana con markdown."""
    fuera = {}
    for clave, meta in CAPITULOS.items():
        if meta["obra_slug"] != "kaccayana":
            continue
        md = os.path.join(RAIZ, clave.split("/")[0] if "/" in clave
                          else meta["obra_slug"], clave + ".md")
        if not os.path.exists(md):
            continue
        fuera[meta["num"]] = (meta["slug"], len(parsear(md)["suttas"]))
    return fuera


def formas_sandhi():
    """Número de formas de reglas.json, para la insignia del recurso."""
    import json
    p = os.path.join(RAIZ, "recursos", "sandhi", "reglas.json")
    if not os.path.exists(p):
        return None
    d = json.load(open(p, encoding="utf-8"))
    return len(d.get("rules", [])), len(d.get("ce", []))


def tablas_paradigmas():
    """Número de paradigmas de paradigmas.json (sin el documento de
    sufijos), para la insignia del recurso."""
    import json
    p = os.path.join(RAIZ, "recursos", "paradigmas", "paradigmas.json")
    if not os.path.exists(p):
        return None
    d = json.load(open(p, encoding="utf-8"))
    return sum(1 for x in d.get("paradigmas", [])
               if x.get("genero") != "sufijos")


def cuenta_raices():
    """(raíces, con cognado sánscrito) de raices.json, para la insignia."""
    import json
    p = os.path.join(RAIZ, "recursos", "raices", "raices.json")
    if not os.path.exists(p):
        return None
    d = json.load(open(p, encoding="utf-8"))
    rs = d.get("raices", [])
    dp = os.path.join(RAIZ, "recursos", "raices", "dhatupatha.json")
    dm = os.path.join(RAIZ, "recursos", "raices", "dhatumanjusa.json")
    n_dp = n_dm = 0
    if os.path.exists(dp):
        n_dp = len(json.load(open(dp, encoding="utf-8")).get("entradas", []))
    if os.path.exists(dm):
        n_dm = len(json.load(open(dm, encoding="utf-8")).get("estrofas", []))
    return len(rs), sum(1 for r in rs if r.get("sanscrito")), n_dp, n_dm


# ---------------------------------------------------------------- páginas

def portada(pub):
    n = len(pub)
    tarjetas = []
    for href, titulo, desc in OBRAS:
        if href == "kaccayana/":
            tarjetas.append(tarjeta(
                href, "{0} de {1} capítulos".format(n, len(CAPITULOS_KACC)),
                titulo, desc))
        else:
            tarjetas.append(tarjeta(None, "prevista", titulo, desc, wip=True))

    cuerpo = (
        '<p class="idx-sub">Traducciones de las gramáticas clásicas de la '
        'lengua pāḷi</p>\n'
        '<p class="idx-lede">\n'
        '  Traducciones al español de las gramáticas clásicas pāḷi, con glosario\n'
        '  terminológico común y concordancia entre las obras. Un término pāḷi se\n'
        '  traduce siempre igual en todas ellas.\n'
        '</p>\n\n'
        '<h2>Obras</h2>\n{0}\n\n'
        '<h2>Recursos</h2>\n{1}\n'
    ).format(lista(tarjetas), lista([tarjeta(
        "recursos/", None, "Material de apoyo",
        "Reglas de combinación eufónica (<i>sandhi</i>), tablas y glosarios "
        "de referencia para el estudio de la lengua.")]))

    return PAGINA.format(
        assets_v=version_assets(),
        titulo="Gramáticas Pāḷi en español",
        descripcion="Traducciones al español de las gramáticas clásicas de la "
                    "lengua pāḷi. Instituto de Estudios Buddhistas Hispano.",
        raiz="", volver="",
        eyebrow="Instituto de Estudios Buddhistas Hispano",
        h1='Gramáticas P<span class="dia">ā</span><span class="dia">ḷ</span>i '
           'en español',
        cuerpo=cuerpo,
        pie=('  Textos relacionados: corpus del Sexto Concilio en\n'
             '  <a href="https://buddha-dhamma.net">buddha-dhamma.net</a>.<br/>\n'
             '  Código y traducciones:\n  {0}.').format(FUENTES))


def indice_kaccayana(pub):
    tarjetas = []
    for num, titulo, _clave, desc in CAPITULOS_KACC:
        if num in pub:
            slug, n = pub[num]
            detalle = DETALLE.get(num, "")
            d = "{0} {1} Traducción completa.".format(desc, detalle).replace(
                "  ", " ").strip()
            tarjetas.append(tarjeta(slug + "/", "{0} suttas".format(n),
                                    "{0} · {1}".format(num, titulo), d))
        else:
            tarjetas.append(tarjeta(None, "prevista",
                                    "{0} · {1}".format(num, titulo), desc,
                                    wip=True))

    cuerpo = (
        '<p class="idx-lede">\n'
        '  La más antigua de las gramáticas pāḷi conservadas. Ocho capítulos\n'
        '  (<i>kappa</i>), cada uno dividido en secciones (<i>kaṇḍa</i>).\n'
        '  Edición base de esta traducción: Kaccāyana-vyākaraṇa, ed. y trad.\n'
        '  Bhikkhu U Nandisena (ITBMU).\n'
        '</p>\n\n'
        '<h2>Capítulos</h2>\n{0}\n\n'
        '<h2>Sobre la numeración</h2>\n'
        '<p class="idx-lede">\n'
        '  Cada sutta lleva tres números, como en la edición de Nandisena:\n'
        '  <b>§30. 58. Aṃ byañjane niggahitaṃ (153).</b> El primero es el número\n'
        '  secuencial de Kaccāyana — el que usamos para citar (<b>§30</b>) y el que fija\n'
        '  el enlace permanente de cada sutta. El segundo es el número correspondiente en\n'
        '  Padarūpasiddhi; el que va entre paréntesis, el de Saddanīti-Suttamālā, ausente\n'
        '  en algunos suttas.\n'
        '</p>\n'
    ).format(lista(tarjetas))

    return PAGINA.format(
        assets_v=version_assets(),
        titulo="Kaccāyana-Byākaraṇaṃ · Gramáticas Pāḷi en español",
        descripcion="Traducción al español de la gramática de Kaccāyana, "
                    "capítulo por capítulo.",
        raiz="../",
        volver='<a class="idx-back" href="../">← Gramáticas Pāḷi</a>\n',
        eyebrow="Gramática de Kaccāyana",
        h1='Kacc<span class="dia">ā</span>yana-By<span class="dia">ā</span>'
           'kara<span class="dia">ṇ</span>a<span class="dia">ṃ</span>',
        cuerpo=cuerpo,
        pie=('  Traducción del Instituto de Estudios Buddhistas Hispano.<br/>\n'
             '  Fuentes y concordancia:\n  {0}.').format(FUENTES))


def indice_recursos():
    conteo = formas_sandhi()
    badge = "{0} reglas · {1} formas".format(*conteo) if conteo else "sandhi"
    n_par = tablas_paradigmas()
    badge_par = "{0} paradigmas".format(n_par) if n_par else "paradigmas"
    n_rai = cuenta_raices()
    def miles(n):
        """12345 → «12.345». El punto de millar, como en el resto del sitio."""
        return "{0:,}".format(n).replace(",", ".")

    if n_rai:
        badge_rai = "{0} raíces · {1} con sánscrito".format(
            miles(n_rai[0]), miles(n_rai[1]))
        if n_rai[2]:
            badge_rai += " · {0} del Dhātupāṭha".format(n_rai[2])
        if n_rai[3]:
            badge_rai += " · {0} estrofas".format(n_rai[3])
    else:
        badge_rai = "raíces"
    insignias = {"__SANDHI_BADGE__": badge, "__PARADIGMAS_BADGE__": badge_par,
                 "__RAICES_BADGE__": badge_rai}
    tarjetas = [tarjeta(href, insignias.get(ins, ins), titulo, desc)
                for href, ins, titulo, desc in RECURSOS
                if ins != "__RAICES_BADGE__" or n_rai]

    externas = [tarjeta(href, ins, titulo, desc, externo=True)
                for href, ins, titulo, desc in CORPUS]

    cuerpo = ('<p class="idx-lede">\n'
              '  Material de referencia para el estudio de la lengua pāḷi, '
              'complementario a\n  las traducciones de las gramáticas, y el '
              'corpus en el que leer los\n  pasajes que citan.\n'
              '</p>\n\n'
              '<h2>Disponible</h2>\n{0}\n\n'
              '<h2>Corpus</h2>\n{1}\n').format(lista(tarjetas),
                                               lista(externas))

    return PAGINA.format(
        assets_v=version_assets(),
        titulo="Recursos · Gramáticas Pāḷi en español",
        descripcion="Material de apoyo para el estudio de la gramática pāḷi: "
                    "reglas, tablas y glosarios.",
        raiz="../",
        volver='<a class="idx-back" href="../">← Gramáticas Pāḷi</a>\n',
        eyebrow="Material de apoyo",
        h1="Recursos",
        cuerpo=cuerpo,
        pie="  Fuentes: {0}.".format(FUENTES))


def escribir(ruta, html):
    destino = os.path.join(RAIZ, ruta)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(html)
    return ruta


def main():
    pub = capitulos_publicados()
    hechas = [
        escribir("site/index.html", portada(pub)),
        escribir("site/kaccayana/index.html", indice_kaccayana(pub)),
        escribir("site/recursos/index.html", indice_recursos()),
    ]
    total = sum(n for _slug, n in pub.values())
    print("{0} de {1} capítulos · {2} suttas → {3}".format(
        len(pub), len(CAPITULOS_KACC), total, ", ".join(hechas)))

    faltan = [num for num, _t, _c, _d in CAPITULOS_KACC if num not in pub]
    if faltan:
        print("  en preparación: {0}".format(
            ", ".join(str(n) for n in faltan)))
    sin_detalle = [n for n in pub if n not in DETALLE]
    if sin_detalle:
        print("  aviso — capítulos publicados sin rango en DETALLE: "
              "{0}".format(sin_detalle))
    return 0


if __name__ == "__main__":
    sys.exit(main())
