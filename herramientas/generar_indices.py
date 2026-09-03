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
    ("solucionador/", "__SOLUCIONADOR_BADGE__", "Solucionador de sandhis",
     "Pegue un pasaje pāḷi: cuántos sandhis hay, cuáles son las voces, y qué "
     "secuencia de aforismos de Kaccāyana explica cada una. Toda lectura se "
     "verifica por recomposición; se afirma una sola cuando hay autoridad "
     "detrás y se declara la duda cuando no la hay. El léxico es el corpus "
     "del Sexto Concilio. Publicado con su cobertura medida a la vista."),
    ("nombre/", "__NOMBRE_BADGE__", "Formación del nombre — pācako",
     "La derivación de <i>pācako</i> «uno que cocina» paso a paso, de la raíz "
     "<i>√paca</i> al nominativo singular, con el aforismo que ampara cada "
     "paso. Cruza el Kibbidhāna, el Nāma-Kappa y el Sandhi-Kappa."),
    ("verbo/", "__VERBO_BADGE__", "El verbo — ākhyāta",
     "Las ocho inflexiones del verbo pāḷi y los ocho grupos de raíces, la "
     "derivación paso a paso de cada forma con el aforismo que la ampara —en "
     "el par Kaccāyana/Rūpasiddhi—, y los paradigmas de conjugación en las "
     "tres voces. Del documento <i>Verbo</i> de Bhikkhu Nandisena y de sus "
     "presentaciones de clase; los paradigmas de <i>otros paradigmas</i>, del "
     "<i>Higher Pali Course</i> del Ven. Buddhadatta Thera."),
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

# ---------------------------------------------------------------- inglés
#
# Las tres páginas de índice van en los dos idiomas. Las dos versiones viajan
# en el HTML —`<span class="i-es">` y `<span class="i-en">`— y un botón enseña
# una u otra; sin JavaScript se ve el español, que es la lengua del sitio.
#
# Los títulos de las obras y de los capítulos NO se traducen: son nombres
# pāḷi. Sí se traduce lo que los describe.

EN = {
    # --- portada -------------------------------------------------------
    "Instituto de Estudios Buddhistas Hispano":
        "Instituto de Estudios Buddhistas Hispano",
    "Traducciones de las gramáticas clásicas de la lengua pāḷi":
        "Translations of the classical grammars of the Pāḷi language",
    "Obras": "Works",
    "Recursos": "Resources",
    "Material de apoyo": "Reference material",
    "Reglas de combinación eufónica (<i>sandhi</i>), tablas y glosarios de "
    "referencia para el estudio de la lengua.":
        "Rules of euphonic combination (<i>sandhi</i>), tables and glossaries "
        "for the study of the language.",
    "prevista": "planned",

    "Gramática de Kaccāyana. La más antigua de las gramáticas pāḷi. "
    "Edición base: Bhikkhu U Nandisena (ITBMU).":
        "Kaccāyana's grammar, the oldest of the Pāḷi grammars. Base edition: "
        "Bhikkhu U Nandisena (ITBMU).",
    "Atribuido a Vimalabuddhi (siglo XI), y llamado también "
    "<i>Mukhamattadīpanī</i>. El comentario clásico de la gramática de "
    "Kaccāyana: recorre los aforismos uno a uno y suple lo que la brevedad "
    "del aforismo calla. El proyecto ya lo consulta y utiliza como fuente "
    "de segunda capa.":
        "Attributed to Vimalabuddhi (11th century) and also called "
        "<i>Mukhamattadīpanī</i>. The classical commentary on Kaccāyana's "
        "grammar: it goes through the aphorisms one by one and supplies what "
        "their brevity leaves unsaid. The project already consults it as a "
        "second-layer source.",
    "De Buddhappiya. Reordena el material de Kaccāyana por temas.":
        "By Buddhappiya. It rearranges Kaccāyana's material by topic.",
    "De Aggavaṃsa. La gramática pāḷi más extensa.":
        "By Aggavaṃsa. The most extensive of the Pāḷi grammars.",
    "De Ledi Sayadaw. Una gramática moderna en siete capítulos en el mismo "
    "orden que Kaccāyana.":
        "By Ledi Sayadaw. A modern grammar in seven chapters, in the same "
        "order as Kaccāyana.",

    # --- Kaccāyana -----------------------------------------------------
    "Gramática de Kaccāyana": "Kaccāyana's grammar",
    "Capítulos": "Chapters",
    "Sobre la numeración": "About the numbering",
    "Capítulo de <i>sandhi</i> — la combinación eufónica de letras.":
        "Chapter on <i>sandhi</i> — the euphonic combination of letters.",
    "Capítulo del nombre — declinación nominal y pronominal.":
        "Chapter on the noun — nominal and pronominal declension.",
    "Capítulo de casos gramaticales — las relaciones sintácticas y las "
    "inflexiones que las expresan.":
        "Chapter on grammatical cases — the syntactic relations and the "
        "inflections that express them.",
    "Capítulo de los compuestos.": "Chapter on compounds.",
    "Capítulo de los derivados nominales.":
        "Chapter on nominal derivatives.",
    "Capítulo del verbo.": "Chapter on the verb.",
    "Capítulo de los sufijos primarios.": "Chapter on primary suffixes.",
    "Capítulo de los sufijos <i>uṇādi</i>.":
        "Chapter on the <i>uṇādi</i> suffixes.",
    "§1–§51, en cinco kaṇḍas.": "§1–§51, in five kaṇḍas.",
    "§52–§270, en cinco kaṇḍas.": "§52–§270, in five kaṇḍas.",
    "§271–§315, sexta sección del Nāma-kappa.":
        "§271–§315, sixth section of the Nāma-kappa.",
    "Traducción completa.": "Complete translation.",

    # --- recursos ------------------------------------------------------
    "Material de apoyo · Recursos": "Reference material · Resources",
    "Disponible": "Available",
    "Corpus": "Corpus",
    "Sandhi — referencia interactiva": "Sandhi — interactive reference",
    "Las reglas de combinación eufónica y los 51 aforismos del Sandhi-Kappa, "
    "con la derivación paso a paso de cada forma y la concordancia entre "
    "Kaccāyana, Rūpasiddhi y Saddanīti. Buscador que ignora los diacríticos.":
        "The rules of euphonic combination and the 51 aphorisms of the "
        "Sandhi-Kappa, with the step-by-step derivation of each form and the "
        "concordance between Kaccāyana, Rūpasiddhi and Saddanīti. Search "
        "ignores diacritics.",
    "Solucionador de sandhis": "Sandhi solver",
    "Pegue un pasaje pāḷi: cuántos sandhis hay, cuáles son las voces, y qué "
    "secuencia de aforismos de Kaccāyana explica cada una. Toda lectura se "
    "verifica por recomposición; se afirma una sola cuando hay autoridad "
    "detrás y se declara la duda cuando no la hay. El léxico es el corpus "
    "del Sexto Concilio. Publicado con su cobertura medida a la vista.":
        "Paste a Pāḷi passage: how many sandhis it holds, what the "
        "components are, and which sequence of Kaccāyana's aphorisms explains "
        "each one. Every reading is verified by recomposition; a single one "
        "is asserted only when there is authority behind it, and the doubt is "
        "declared when there is not. The lexicon is the Sixth Council corpus. "
        "Published with its coverage measured in plain sight.",
    "Formación del nombre — pācako": "Formation of the noun — pācako",
    "La derivación de <i>pācako</i> «uno que cocina» paso a paso, de la raíz "
    "<i>√paca</i> al nominativo singular, con el aforismo que ampara cada "
    "paso. Cruza el Kibbidhāna, el Nāma-Kappa y el Sandhi-Kappa.":
        "The derivation of <i>pācako</i> “one who cooks” step by step, from "
        "the root <i>√paca</i> to the nominative singular, with the aphorism "
        "that authorises each step. It crosses the Kibbidhāna, the Nāma-Kappa "
        "and the Sandhi-Kappa.",
    "El verbo — ākhyāta": "The verb — ākhyāta",
    "Las ocho inflexiones del verbo pāḷi y los ocho grupos de raíces, la "
    "derivación paso a paso de cada forma con el aforismo que la ampara —en "
    "el par Kaccāyana/Rūpasiddhi—, y los paradigmas de conjugación en las "
    "tres voces. Del documento <i>Verbo</i> de Bhikkhu Nandisena y de sus "
    "presentaciones de clase; los paradigmas de <i>otros paradigmas</i>, del "
    "<i>Higher Pali Course</i> del Ven. Buddhadatta Thera.":
        "The eight inflections of the Pāḷi verb and the eight groups of "
        "roots, the step-by-step derivation of each form with the aphorism "
        "that authorises it —as the Kaccāyana/Rūpasiddhi pair— and the "
        "conjugation paradigms in the three voices. From Bhikkhu Nandisena's "
        "<i>Verbo</i> document and his class presentations; the paradigms in "
        "<i>other paradigms</i>, from the <i>Higher Pali Course</i> of Ven. "
        "Buddhadatta Thera.",
    "Paradigmas de declinación": "Declension paradigms",
    "Los 83 paradigmas de declinación nominal y pronominal de la lengua "
    "pāḷi, con todas las variantes de cada forma: nombres por género y tema, "
    "pronombres, numerales y los sufijos que son inflexiones. Buscador que "
    "ignora los diacríticos y filtros por género y por tema.":
        "The 83 paradigms of nominal and pronominal declension in Pāḷi, with "
        "every variant of each form: nouns by gender and stem, pronouns, "
        "numerals and the suffixes that are inflections. Search ignores "
        "diacritics, with filters by gender and by stem.",
    "Raíces pāḷi comparadas con las sánscritas":
        "Pāḷi roots compared with the Sanskrit ones",
    "Las raíces de la <i>Dhātumālā</i> del <i>Saddanīti</i> con su "
    "significado en español y en inglés, la raíz sánscrita correspondiente "
    "cuando la hay, y el <i>gaṇa</i> y la página de cada una, del libro "
    "<i>Pali Roots in Saddanīti</i> del Ven. U Sīlānanda, editado por "
    "Bhikkhu Nandisena. Con el índice inverso, que va del sentido a las "
    "raíces que lo expresan, y el <i>Dhātupāṭha</i> y la <i>Dhātumañjūsā</i> "
    "de Andersen y Smith concordados lema a lema.":
        "The roots of the <i>Dhātumālā</i> of the <i>Saddanīti</i> with their "
        "meaning in Spanish and English, the corresponding Sanskrit root "
        "where there is one, and the <i>gaṇa</i> and page of each, from "
        "<i>Pali Roots in Saddanīti</i> by Ven. U Sīlānanda, edited by "
        "Bhikkhu Nandisena. With the reverse index, which goes from the sense "
        "to the roots that express it, and the <i>Dhātupāṭha</i> and the "
        "<i>Dhātumañjūsā</i> of Andersen and Smith concorded lemma by lemma.",
    "Chaṭṭhasaṅgītipiṭaka — Tipiṭaka del Sexto Concilio":
        "Chaṭṭhasaṅgītipiṭaka — Tipiṭaka of the Sixth Council",
    "La edición del Sexto Concilio romanizada: canon, comentarios y "
    "subcomentarios enlazados capa a capa, de modo que desde cualquier "
    "párrafo se llega a su aṭṭhakathā y su ṭīkā. 83.751 párrafos y 54.036 "
    "variantes, con búsqueda que ignora los diacríticos.":
        "The Sixth Council edition romanised: canon, commentaries and "
        "subcommentaries linked layer by layer, so that from any paragraph "
        "one reaches its aṭṭhakathā and its ṭīkā. 83,751 paragraphs and "
        "54,036 variants, with search that ignores diacritics.",
    "118 volúmenes": "118 volumes",
}


def bi(es, en=None):
    """
    Las dos lenguas, para que el botón enseñe una u otra.

    Es idempotente: si la cadena ya viene con sus dos versiones —porque quien
    la compuso ya llamó aquí— se devuelve tal cual. Así `tarjeta()` puede
    envolverlo todo sin duplicar lo ya envuelto.
    """
    if 'class="i-es"' in es:
        return es
    ingles = en if en is not None else EN.get(es)
    if not ingles:
        SIN_INGLES.add(es)
        return es
    return ('<span class="i-es">{0}</span><span class="i-en">{1}</span>'
            .format(es, ingles))


SIN_INGLES = set()

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
<p class="idx-licencia"><span class="i-es">Copyright &copy; 2026 Instituto de Estudios Buddhistas Hispano (IEBH). Publicado bajo licencia <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.es" rel="license noopener" target="_blank">CC&nbsp;BY-NC-ND&nbsp;4.0</a>.</span><span class="i-en">Copyright &copy; 2026 Instituto de Estudios Buddhistas Hispano (IEBH). Published under licence <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/" rel="license noopener" target="_blank">CC&nbsp;BY-NC-ND&nbsp;4.0</a>.</span></p>
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

  /* Idioma. La clave «pali_lang» es la misma que usan las páginas de
     recurso, de modo que la elección viaja con el lector por todo el sitio. */
  var TITULOS = {{ es: {titulo_json}, en: {lang_en_json} }};
  var l = document.createElement('button');
  l.id = 'lang-btn'; l.type = 'button';
  function pinta() {{
    var en = document.body.classList.contains('en');
    document.documentElement.lang = en ? 'en' : 'es';
    document.title = en ? TITULOS.en : TITULOS.es;
    l.textContent = en ? 'ES' : 'EN';
    l.setAttribute('aria-label', en ? 'Ver en español' : 'View in English');
  }}
  try {{ if (localStorage.getItem('pali_lang') === 'en') document.body.classList.add('en'); }} catch (e) {{}}
  l.onclick = function () {{
    document.body.classList.toggle('en');
    try {{ localStorage.setItem('pali_lang', document.body.classList.contains('en') ? 'en' : 'es'); }} catch (e) {{}}
    pinta();
  }};
  pinta();
  document.body.appendChild(l);
}})();
</script>
</body>
</html>
"""


def tarjeta(href, insignia, titulo, desc, wip=False, externo=False,
            traducir_titulo=True):
    """
    Una tarjeta del índice, en los dos idiomas.

    El título se traduce en los recursos —«Paradigmas de declinación»— pero
    no en las obras ni en los capítulos, que son nombres pāḷi.
    """
    ins = ""
    if insignia:
        ins = '      <span class="idx-badge{0}">{1}</span>\n'.format(
            " wip" if wip else "", bi(insignia))
    if traducir_titulo:
        titulo = bi(titulo)
    desc = bi(desc)
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
                href,
                bi("{0} de {1} capítulos".format(n, len(CAPITULOS_KACC)),
                   "{0} of {1} chapters".format(n, len(CAPITULOS_KACC))),
                titulo, desc, traducir_titulo=False))
        else:
            tarjetas.append(tarjeta(None, "prevista", titulo, desc, wip=True,
                                    traducir_titulo=False))

    cuerpo = (
        '<p class="idx-sub">' + bi('Traducciones de las gramáticas clásicas '
        'de la lengua pāḷi') + '</p>\n'
        '<p class="idx-lede">' + bi(
            'Traducciones al español de las gramáticas clásicas pāḷi, con '
            'glosario terminológico común y concordancia entre las obras. '
            'Un término pāḷi se traduce siempre igual en todas ellas.',
            'Spanish translations of the classical Pāḷi grammars, with a '
            'shared terminological glossary and a concordance between the '
            'works. A Pāḷi term is always translated the same way in all of '
            'them.') + '</p>\n\n'
        '<h2>' + bi('Obras') + '</h2>\n{0}\n\n'
        '<h2>' + bi('Recursos') + '</h2>\n{1}\n'
    ).format(lista(tarjetas), lista([tarjeta(
        "recursos/", None, "Material de apoyo",
        "Reglas de combinación eufónica (<i>sandhi</i>), tablas y glosarios "
        "de referencia para el estudio de la lengua.")]))

    return pagina(
        assets_v=version_assets(),
        titulo="Gramáticas Pāḷi en español",
        descripcion="Traducciones al español de las gramáticas clásicas de la "
                    "lengua pāḷi. Instituto de Estudios Buddhistas Hispano.",
        raiz="", volver="",
        eyebrow="Instituto de Estudios Buddhistas Hispano",
        lang_en="Pāḷi Grammars in Spanish",
        h1='Gramáticas P<span class="dia">ā</span><span class="dia">ḷ</span>i '
           'en español',
        cuerpo=cuerpo,
        pie=(bi('Textos relacionados: corpus del Sexto Concilio en',
                'Related texts: the Sixth Council corpus at')
             + ' <a href="https://buddha-dhamma.net">buddha-dhamma.net</a>.'
             '<br/>\n  ' + bi('Código y traducciones:', 'Code and translations:')
             + '\n  {0}.').format(FUENTES))


def indice_kaccayana(pub):
    tarjetas = []
    for num, titulo, _clave, desc in CAPITULOS_KACC:
        if num in pub:
            slug, n = pub[num]
            detalle = DETALLE.get(num, "")
            d = (bi(desc) + " " + (bi(detalle) if detalle else "")
                 + " " + bi("Traducción completa.")).replace("  ", " ").strip()
            tarjetas.append(tarjeta(
                slug + "/", bi("{0} suttas".format(n),
                               "{0} suttas".format(n)),
                "{0} · {1}".format(num, titulo), d,
                traducir_titulo=False))
        else:
            tarjetas.append(tarjeta(None, "prevista",
                                    "{0} · {1}".format(num, titulo), desc,
                                    wip=True, traducir_titulo=False))

    cuerpo = (
        '<p class="idx-lede">' + bi(
            'La más antigua de las gramáticas pāḷi conservadas. Ocho '
            'capítulos (<i>kappa</i>), cada uno dividido en secciones '
            '(<i>kaṇḍa</i>). Edición base de esta traducción: '
            'Kaccāyana-byākaraṇa, ed. y trad. Bhikkhu U Nandisena (ITBMU).',
            'The oldest of the surviving Pāḷi grammars. Eight chapters '
            '(<i>kappa</i>), each divided into sections (<i>kaṇḍa</i>). Base '
            'edition of this translation: Kaccāyana-byākaraṇa, ed. and trans. '
            'Bhikkhu U Nandisena (ITBMU).') + '</p>\n\n'
        '<h2>' + bi('Capítulos') + '</h2>\n{0}\n\n'
        '<h2>' + bi('Sobre la numeración') + '</h2>\n'
        '<p class="idx-lede">' + bi(
            'Cada sutta lleva tres números, como en la edición de Nandisena: '
            '<b>§30. 58. Aṃ byañjane niggahitaṃ (153).</b> El primero es el '
            'número secuencial de Kaccāyana — el que usamos para citar '
            '(<b>§30</b>) y el que fija el enlace permanente de cada sutta. '
            'El segundo es el número correspondiente en Padarūpasiddhi; el '
            'que va entre paréntesis, el de Saddanīti-Suttamālā, ausente en '
            'algunos suttas.',
            'Each sutta carries three numbers, as in Nandisena\'s edition: '
            '<b>§30. 58. Aṃ byañjane niggahitaṃ (153).</b> The first is '
            'Kaccāyana\'s sequential number — the one we cite by (<b>§30</b>) '
            'and the one that fixes each sutta\'s permanent link. The second '
            'is the corresponding number in Padarūpasiddhi; the one in '
            'parentheses is that of the Saddanīti-Suttamālā, absent in some '
            'suttas.') + '</p>\n'
    ).format(lista(tarjetas))

    return pagina(
        assets_v=version_assets(),
        titulo="Kaccāyana-Byākaraṇaṃ · Gramáticas Pāḷi en español",
        descripcion="Traducción al español de la gramática de Kaccāyana, "
                    "capítulo por capítulo.",
        raiz="../",
        volver='<a class="idx-back" href="../">← Gramáticas Pāḷi</a>\n',
        eyebrow=bi("Gramática de Kaccāyana"),
        lang_en="Kaccāyana-Byākaraṇaṃ · Pāḷi Grammars in Spanish",
        h1='Kacc<span class="dia">ā</span>yana-By<span class="dia">ā</span>'
           'kara<span class="dia">ṇ</span>a<span class="dia">ṃ</span>',
        cuerpo=cuerpo,
        pie=(bi('Traducción del Instituto de Estudios Buddhistas Hispano.',
                'Translated by the Instituto de Estudios Buddhistas Hispano.')
             + '<br/>\n  ' + bi('Fuentes y concordancia:',
                                'Sources and concordance:')
             + '\n  {0}.').format(FUENTES))


def cuenta_verbo():
    """(escaleras, paradigmas) de la página del verbo, si ya está armada."""
    import json
    ruta = os.path.join(RAIZ, "recursos", "verbo", "verbo.json")
    if not os.path.exists(ruta):
        return None
    try:
        datos = json.load(open(ruta, encoding="utf-8"))
        from escaleras_verbo import escaleras
        return len(escaleras()), len(datos["paradigmas"])
    except Exception:
        return None


def indice_recursos():
    conteo = formas_sandhi()
    badge = (bi("{0} reglas · {1} formas".format(*conteo),
                "{0} rules · {1} forms".format(*conteo))
             if conteo else "sandhi")
    n_par = tablas_paradigmas()
    badge_par = (bi("{0} paradigmas".format(n_par),
                    "{0} paradigms".format(n_par)) if n_par else "paradigmas")
    n_rai = cuenta_raices()
    def miles(n):
        """12345 → «12.345». El punto de millar, como en el resto del sitio."""
        return "{0:,}".format(n).replace(",", ".")

    if n_rai:
        _es = "{0} raíces · {1} con sánscrito".format(
            miles(n_rai[0]), miles(n_rai[1]))
        _en = "{0} roots · {1} with Sanskrit".format(
            miles(n_rai[0]), miles(n_rai[1]))
        if n_rai[2]:
            _es += " · {0} del Dhātupāṭha".format(n_rai[2])
            _en += " · {0} from the Dhātupāṭha".format(n_rai[2])
        if n_rai[3]:
            _es += " · {0} estrofas".format(n_rai[3])
            _en += " · {0} stanzas".format(n_rai[3])
        badge_rai = bi(_es, _en)
    else:
        badge_rai = "raíces"
    n_ver = cuenta_verbo()
    badge_ver = (bi("{0} derivaciones · {1} paradigmas".format(*n_ver),
                    "{0} derivations · {1} paradigms".format(*n_ver))
                 if n_ver else "verbo")
    insignias = {"__SANDHI_BADGE__": badge, "__PARADIGMAS_BADGE__": badge_par,
                 "__RAICES_BADGE__": badge_rai, "__VERBO_BADGE__": badge_ver,
                 "__SOLUCIONADOR_BADGE__": bi("88 % del banco",
                                              "88 % of the bench"),
                 "__NOMBRE_BADGE__": bi("10 pasos", "10 steps")}
    tarjetas = [tarjeta(href, insignias.get(ins, ins), titulo, desc)
                for href, ins, titulo, desc in RECURSOS
                if (ins != "__RAICES_BADGE__" or n_rai)
                and (ins != "__VERBO_BADGE__" or n_ver)]

    externas = [tarjeta(href, ins, titulo, desc, externo=True)
                for href, ins, titulo, desc in CORPUS]

    cuerpo = ('<p class="idx-lede">' + bi(
                  'Material de referencia para el estudio de la lengua pāḷi, '
                  'complementario a las traducciones de las gramáticas, y el '
                  'corpus en el que leer los pasajes que citan.',
                  'Reference material for the study of the Pāḷi language, '
                  'complementary to the translations of the grammars, and the '
                  'corpus in which to read the passages they cite.')
              + '</p>\n\n'
              '<h2>' + bi('Disponible') + '</h2>\n{0}\n\n'
              '<h2>' + bi('Corpus') + '</h2>\n{1}\n').format(
                  lista(tarjetas), lista(externas))

    return pagina(
        assets_v=version_assets(),
        titulo="Recursos · Gramáticas Pāḷi en español",
        descripcion="Material de apoyo para el estudio de la gramática pāḷi: "
                    "reglas, tablas y glosarios.",
        raiz="../",
        volver='<a class="idx-back" href="../">← Gramáticas Pāḷi</a>\n',
        eyebrow=bi("Material de apoyo"),
        lang_en="Resources · Pāḷi Grammars in Spanish",
        h1=bi("Recursos"),
        cuerpo=cuerpo,
        pie="  {0} {1}.".format(bi("Fuentes:", "Sources:"), FUENTES))


def pagina(**kw):
    """PAGINA con los dos títulos ya serializados para el botón de idioma."""
    import json as _json
    kw.setdefault("lang_en", kw["titulo"])
    kw["titulo_json"] = _json.dumps(kw["titulo"], ensure_ascii=False)
    kw["lang_en_json"] = _json.dumps(kw.pop("lang_en"), ensure_ascii=False)
    return PAGINA.format(**kw)


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
    if SIN_INGLES:
        print("  aviso — sin inglés ({0}):".format(len(SIN_INGLES)))
        for t in sorted(SIN_INGLES)[:12]:
            print("      {0}".format(t[:88]))
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
