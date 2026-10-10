#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera las tres páginas de índice del sitio.

    python3 herramientas/generar_indices.py

Escribe:

    site/index.html             portada — las cuatro obras
    site/kaccayana/index.html   los ocho capítulos de Kaccāyana
    site/recursos/index.html    el material de apoyo
    site/guia-clases/index.html guía para estudiantes de las clases grabadas

Lo que antes había que corregir a mano —«1 de 8 capítulos», «51 suttas»—
se cuenta ahora del markdown: publicar un capítulo es añadirlo a CAPITULOS
en generar_capitulo.py y dejar su .md en su sitio; la insignia, el total y
la tarjeta se actualizan solos. Un capítulo cuyo .md no exista todavía sale
como «prevista», sin enlace.
"""

import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "herramientas"))

from generar_capitulo import CAPITULOS, parsear, version_assets  # noqa: E402
import cabecera  # noqa: E402
from generar_secciones import mapa as mapa_secciones  # noqa: E402

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
    (4, "Samāsa-Kappa", "04-samasa-kappa",
     "Capítulo de compuestos — las seis clases de compuesto nominal "
     "(abyayībhāva, dvanda, kammadhāraya, digu, tappurisa, bahubbīhi) y "
     "sus reglas de formación."),
    (5, "Taddhita-Kappa", "05-taddhita-kappa",
     "Capítulo de los derivados secundarios."),
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
    4: "§316–§343, séptima sección del Nāma-kappa.",
    5: "§344–§405, octava sección del Nāma-kappa.",
}

OBRAS = [
    ("kaccayana/", "Kacc<span class=\"dia\">ā</span>yana-By<span class=\"dia\">ā"
     "</span>kara<span class=\"dia\">ṇ</span>a<span class=\"dia\">ṃ</span>",
     "Gramática de Kaccāyana. La más antigua de las gramáticas pāḷi. "
     "Edición base: Bhikkhu Nandisena."),
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
     "De Ledi Sayadaw. Explicación propia, en pāḷi, de los aforismos de la "
     "gramática de Moggallāna."),
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
     "paso. Cruza Kibbidhāna, el Nāma-Kappa y el Sandhi-Kappa."),
    ("verbo/", "__VERBO_BADGE__", "El verbo — ākhyāta",
     "Las ocho inflexiones del verbo pāḷi y los ocho grupos de raíces, la "
     "derivación paso a paso de cada forma con el aforismo que la ampara —en "
     "el par Kaccāyana/Rūpasiddhi—, y los paradigmas de conjugación en las "
     "tres voces. Del documento <i>Verbo</i> de Bhikkhu Nandisena y de sus "
     "presentaciones de clase; los paradigmas de <i>otros paradigmas</i>, del "
     "<i>Higher Pali Course</i> del Ven. Buddhadatta Thera."),
    ("paradigmas/", "__PARADIGMAS_BADGE__", "Paradigmas de declinación",
     "Los __N_PARADIGMAS__ paradigmas de declinación nominal y pronominal de la lengua "
     "pāḷi, con "
     "todas las variantes de cada forma: nombres por género y tema, "
     "pronombres, numerales y los sufijos que son inflexiones. Buscador que "
     "ignora los diacríticos y filtros por género y por tema."),
    ("casos/", "__CASOS_BADGE__", "Usos de las inflexiones — kāraka",
     "Qué expresa cada una de las siete inflexiones nominales, uso por uso, "
     "según el capítulo de los casos de <i>Rūpasiddhi</i>, con un ejemplo "
     "o más para cada uso y la concordancia con Kaccāyana y Saddanīti. Dos "
     "órdenes —el de Rūpasiddhi y el de Kaccāyana— y un modo de revisión "
     "que enseña de dónde viene cada traducción. Borrador en revisión."),
    ("clasificacion/", "__CLASIFICACION_BADGE__",
     "Clasificación de los suttas de Kaccāyana",
     "Cada aforismo de Kaccāyana clasificado según "
     "los cuatro tipos de sutta —saññā, adhikāra, paribhāsā y vidhi— y, "
     "cuando es vidhi, según las ocho operaciones (lopa, dīgha, rassa, "
     "ādesa, āgama, paṭisedha, paccaya y vibhatti), con la operación "
     "descrita en una frase. Por ahora, el Sandhi-Kappa, el Nāma-Kappa, "
     "el Kāraka-Kappa, el Samāsa-Kappa y el Taddhita-Kappa; "
     "los demás capítulos se irán añadiendo. Cada decisión se apoya en "
     "<i>Rūpasiddhi</i> y <i>Nyāsa</i>, contrastados con "
     "<i>Bhāsāṭīkā</i>, <i>Saddanīti</i> y las clases del Ven. U "
     "Sīlānanda; donde la tradición discrepa, se expone la divergencia y "
     "se justifica la determinación. Para el estudiante, un mapa de qué "
     "hace cada regla; para el investigador, las fuentes de cada "
     "clasificación. Cada aforismo enlaza a su texto y traducción. "
     "Borrador en revisión."),
    ("analisis/", "__ANALISIS_BADGE__",
     "Análisis de los suttas de Kaccāyana",
     "Clase, aṅga, funciones (kāriyī, kāriya, nimitta) y ejemplo de cada sutta, según <i>Visuddhāyuṃ Kaccāyana-ṭīkā</i>.",
     # quinto elemento: un enlace secundario bajo la tarjeta (href, es, en)
     ("analisis/guia/", "Guía para el estudiante", "Student guide")),
    ("comentarios/", "__COMENTARIOS_BADGE__",
     "Comentarios de la escuela de Kaccāyana",
     "Las obras de la escuela gramatical de Kaccāyana —el texto raíz, sus "
     "comentarios, los compendios y sus ṭīkās, los tratados auxiliares y "
     "las glosas vernáculas— con autor, fecha, lugar, relación con "
     "Kaccāyana, la sección de Ñāṇatusita (<i>Reference Table of Pāli "
     "Literature</i>) y el texto en línea, con el material de este sitio "
     "en primer lugar. Borrador en revisión."),
    ("glosario/", "__GLOSARIO_BADGE__", "Glosario de terminología gramatical",
     "Los términos técnicos de la gramática pāḷi en una sola lista "
     "alfabética, con tres capas por lema: <i>Glosario de términos "
     "gramaticales de la lengua pali</i> de Bhikkhu Nandisena (IEBH, 2013), "
     "<i>Conspectus Terminorum</i> de Helmer Smith (<i>Saddanīti</i> IV) "
     "en colación página a página sobre la plancha, y la terminología fijada en estas "
     "traducciones. Buscador que ignora los diacríticos e índice por el "
     "alfabeto pāḷi."),
    ("raices/", "__RAICES_BADGE__", "Raíces pāḷi comparadas con las sánscritas",
     "Las raíces de <i>Dhātumālā</i> de <i>Saddanīti</i> con su "
     "significado en español y en inglés, la raíz sánscrita correspondiente "
     "cuando la hay, y el <i>gaṇa</i> y la página de cada una, del libro "
     "<i>Pali Roots in Saddanīti</i> del Ven. U Sīlānanda, editado por "
     "Bhikkhu Nandisena. Con el índice inverso, que va del "
     "sentido a las raíces que lo expresan, y <i>Dhātupāṭha</i> y "
     "<i>Dhātumañjūsā</i> de Andersen y Smith concordados lema a lema, y "
     "las raíces de <i>Dhātvatthasaṅgaha</i> con el sentido de su "
     "<i>nissaya</i> birmano."),
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
    ("https://abhidhana.buddha-dhamma.net/", "25 volúmenes",
     "Tipiṭaka Pāḷi-Myanmā Abhidhāna",
     "El diccionario pāḷi-birmano del Ministerio de Asuntos Religiosos de "
     "Myanmar, en 25 volúmenes, digitalizado: 221.154 entradas con el "
     "titular romanizado y la página impresa al lado. Los significados en "
     "español son borradores sin revisar; edición en curso.", True),
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
    "Edición base: Bhikkhu Nandisena.":
        "Kaccāyana's grammar, the oldest of the Pāḷi grammars. Base edition: "
        "Bhikkhu Nandisena.",
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
    "De Ledi Sayadaw. Explicación propia, en pāḷi, de los aforismos de la "
    "gramática de Moggallāna.":
        "By Ledi Sayadaw. His own explanation, in Pāḷi, of the aphorisms of "
        "Moggallāna's grammar.",

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
    "Capítulo de compuestos — las seis clases de compuesto nominal "
    "(abyayībhāva, dvanda, kammadhāraya, digu, tappurisa, bahubbīhi) y "
    "sus reglas de formación.":
        "Chapter on compounds — the six kinds of nominal compound "
        "(abyayībhāva, dvanda, kammadhāraya, digu, tappurisa, bahubbīhi) "
        "and the rules that form them.",
    "§316–§343, séptima sección del Nāma-kappa.":
        "§316–§343, seventh section of the Nāma-kappa.",
    "§344–§405, octava sección del Nāma-kappa.":
        "§344–§405, eighth section of the Nāma-kappa.",
    "Capítulo de los derivados secundarios.":
        "Chapter on secondary derivatives.",
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
    "paso. Cruza Kibbidhāna, el Nāma-Kappa y el Sandhi-Kappa.":
        "The derivation of <i>pācako</i> “one who cooks” step by step, from "
        "the root <i>√paca</i> to the nominative singular, with the aphorism "
        "that authorises each step. It crosses Kibbidhāna, the Nāma-Kappa "
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
    "Los __N_PARADIGMAS__ paradigmas de declinación nominal y pronominal de la lengua "
    "pāḷi, con todas las variantes de cada forma: nombres por género y tema, "
    "pronombres, numerales y los sufijos que son inflexiones. Buscador que "
    "ignora los diacríticos y filtros por género y por tema.":
        "The __N_PARADIGMAS__ paradigms of nominal and pronominal declension in Pāḷi, with "
        "every variant of each form: nouns by gender and stem, pronouns, "
        "numerals and the suffixes that are inflections. Search ignores "
        "diacritics, with filters by gender and by stem.",
    "Usos de las inflexiones — kāraka": "Uses of the inflections — kāraka",
    "Qué expresa cada una de las siete inflexiones nominales, uso por uso, "
    "según el capítulo de los casos de <i>Rūpasiddhi</i>, con un ejemplo "
    "o más para cada uso y la concordancia con Kaccāyana y Saddanīti. Dos "
    "órdenes —el de Rūpasiddhi y el de Kaccāyana— y un modo de revisión "
    "que enseña de dónde viene cada traducción. Borrador en revisión.":
        "What each of the seven nominal inflections expresses, use by use, "
        "following the chapter on cases of <i>Rūpasiddhi</i>, with one "
        "example or more for each use and the concordance with Kaccāyana and "
        "Saddanīti. Two orders —Rūpasiddhi's and Kaccāyana's— and a review "
        "mode that shows where each translation comes from. Draft under review; "
        "the page itself is in Spanish.",
    "Análisis de los suttas de Kaccāyana":
        "Analysis of the Kaccāyana suttas",
    "Clase, aṅga, funciones (kāriyī, kāriya, nimitta) y ejemplo de cada sutta, según <i>Visuddhāyuṃ Kaccāyana-ṭīkā</i>.":
        "Class, aṅga, roles (kāriyī, kāriya, nimitta) and example for each "
        "sutta, following <i>Visuddhāyuṃ Kaccāyana-ṭīkā</i>.",
    "Comentarios de la escuela de Kaccāyana":
        "Commentaries of the Kaccāyana school",
    "Las obras de la escuela gramatical de Kaccāyana —el texto raíz, sus "
    "comentarios, los compendios y sus ṭīkās, los tratados auxiliares y "
    "las glosas vernáculas— con autor, fecha, lugar, relación con "
    "Kaccāyana, la sección de Ñāṇatusita (<i>Reference Table of Pāli "
    "Literature</i>) y el texto en línea, con el material de este sitio "
    "en primer lugar. Borrador en revisión.":
        "The works of the Kaccāyana school of grammar —the root text, its "
        "commentaries, the digests and their ṭīkās, the auxiliary treatises "
        "and the vernacular glosses— with author, date, place, relation to "
        "Kaccāyana, Ñāṇatusita's section (<i>Reference Table of Pāli "
        "Literature</i>) and the online text, this site's own material first."
        " Draft under review.",
    "Clasificación de los suttas de Kaccāyana":
        "Classification of the Kaccāyana suttas",
    "Cada aforismo de Kaccāyana clasificado según "
    "los cuatro tipos de sutta —saññā, adhikāra, paribhāsā y vidhi— y, "
    "cuando es vidhi, según las ocho operaciones (lopa, dīgha, rassa, "
    "ādesa, āgama, paṭisedha, paccaya y vibhatti), con la operación "
    "descrita en una frase. Por ahora, el Sandhi-Kappa, el Nāma-Kappa, "
     "el Kāraka-Kappa, el Samāsa-Kappa y el Taddhita-Kappa; "
    "los demás capítulos se irán añadiendo. Cada decisión se apoya en "
    "<i>Rūpasiddhi</i> y <i>Nyāsa</i>, contrastados con "
    "<i>Bhāsāṭīkā</i>, <i>Saddanīti</i> y las clases del Ven. U "
    "Sīlānanda; donde la tradición discrepa, se expone la divergencia y "
    "se justifica la determinación. Para el estudiante, un mapa de qué "
    "hace cada regla; para el investigador, las fuentes de cada "
    "clasificación. Cada aforismo enlaza a su texto y traducción. "
    "Borrador en revisión.":
        "Every aphorism of Kaccāyana classified by "
        "the four kinds of sutta —saññā, adhikāra, paribhāsā and vidhi— and, "
        "when it is a vidhi, by the eight operations (lopa, dīgha, rassa, "
        "ādesa, āgama, paṭisedha, paccaya and vibhatti), with the operation "
        "stated in one sentence. For now, the Sandhi-Kappa, the Nāma-Kappa, "
        "the Kāraka-Kappa, the Samāsa-Kappa and the Taddhita-Kappa; "
        "the other chapters will be added in turn. "
        "Each decision rests on <i>Rūpasiddhi</i>"
        " and <i>Nyāsa</i>, checked against <i>Bhāsāṭīkā</i>, "
        "<i>Saddanīti</i> and the Ven. U Sīlānanda's classes; where the "
        "tradition disagrees, the divergence is set out and the determination"
        " justified. For students, a map of what each rule does; for "
        "scholars, the sources behind every classification. Each aphorism "
        "links to its text and translation. Draft under review.",
    "Glosario de terminología gramatical": "Glossary of grammatical terminology",
    "Los términos técnicos de la gramática pāḷi en una sola lista "
    "alfabética, con tres capas por lema: <i>Glosario de términos "
    "gramaticales de la lengua pali</i> de Bhikkhu Nandisena (IEBH, 2013), "
    "<i>Conspectus Terminorum</i> de Helmer Smith (<i>Saddanīti</i> IV) "
    "en colación página a página sobre la plancha, y la terminología fijada en estas "
    "traducciones. Buscador que ignora los diacríticos e índice por el "
    "alfabeto pāḷi.":
        "The technical terms of Pāḷi grammar in a single alphabetical list, "
        "with three layers per lemma: Bhikkhu Nandisena's <i>Glosario de "
        "términos gramaticales de la lengua pali</i> (IEBH, 2013), Helmer "
        "Smith's <i>Conspectus Terminorum</i> (<i>Saddanīti</i> IV), being collated "
        "page by page against the printed text, and the terminology fixed in these "
        "translations. Search ignores diacritics, with an index in the Pāḷi "
        "alphabet.",
    "Raíces pāḷi comparadas con las sánscritas":
        "Pāḷi roots compared with the Sanskrit ones",
    "Las raíces de <i>Dhātumālā</i> de <i>Saddanīti</i> con su "
    "significado en español y en inglés, la raíz sánscrita correspondiente "
    "cuando la hay, y el <i>gaṇa</i> y la página de cada una, del libro "
    "<i>Pali Roots in Saddanīti</i> del Ven. U Sīlānanda, editado por "
    "Bhikkhu Nandisena. Con el índice inverso, que va del sentido a las "
    "raíces que lo expresan, y <i>Dhātupāṭha</i> y <i>Dhātumañjūsā</i> "
    "de Andersen y Smith concordados lema a lema, y las raíces de "
    "<i>Dhātvatthasaṅgaha</i> con el sentido de su <i>nissaya</i> birmano.":
        "The roots of <i>Dhātumālā</i> of <i>Saddanīti</i> with their "
        "meaning in Spanish and English, the corresponding Sanskrit root "
        "where there is one, and the <i>gaṇa</i> and page of each, from "
        "<i>Pali Roots in Saddanīti</i> by Ven. U Sīlānanda, edited by "
        "Bhikkhu Nandisena. With the reverse index, which goes from the sense "
        "to the roots that express it, and <i>Dhātupāṭha</i> and "
        "<i>Dhātumañjūsā</i> of Andersen and Smith concorded lemma by lemma, "
        "and the roots of <i>Dhātvatthasaṅgaha</i> with the meaning of its "
        "Burmese <i>nissaya</i>.",
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
    "Tipiṭaka Pāḷi-Myanmā Abhidhāna": "Tipiṭaka Pāḷi-Myanmā Abhidhāna",
    "El diccionario pāḷi-birmano del Ministerio de Asuntos Religiosos de "
    "Myanmar, en 25 volúmenes, digitalizado: 221.154 entradas con el "
    "titular romanizado y la página impresa al lado. Los significados en "
    "español son borradores sin revisar; edición en curso.":
        "The Pāḷi-Burmese dictionary of Myanmar's Ministry of Religious "
        "Affairs, in 25 volumes, digitised: 221,154 entries with the headword "
        "romanised and the printed page alongside. The Spanish meanings are "
        "unreviewed drafts; a work in progress.",
    "25 volúmenes": "25 volumes",
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
<link href="{raiz}assets/favicon.svg" rel="icon" type="image/svg+xml"/>
<link href="{raiz}assets/pali.css?v={assets_v}" rel="stylesheet"/>
</head>
<body>
<script>/* Tema guardado, antes de pintar. */
try{{var _d=localStorage.getItem('pali_dark');
if(_d==='1'||(_d===null&&matchMedia('(prefers-color-scheme: dark)').matches))
document.body.classList.add('dark');}}catch(e){{}}
/* Lengua de arranque, antes de pintar y con el mismo criterio en todo el
   sitio (sesión 63). Manda la elección del lector si la hizo; si no la hizo,
   manda la lengua de su navegador, que es la de su sistema operativo. El
   español es el que queda por defecto: es la lengua del proyecto, y a ella
   van a parar las lenguas que no son el inglés. */
function paliLang(){{var g=null;
/* ?lang=en|es en la dirección manda sobre todo lo demás, sin guardarse: es
   como abren estos índices en inglés los capítulos de /en/ desde la barra
   común (2026-10-08), y como ya lo hacían el análisis y la clasificación. */
var q=/[?&]lang=(en|es)(&|$)/.exec(location.search);if(q)return q[1];
try{{g=localStorage.getItem('pali_lang');}}catch(e){{}}
if(g==='en'||g==='es')return g;
var n=(navigator.languages&&navigator.languages[0])||navigator.language||'';
return /^en\\b/i.test(n)?'en':'es';}}</script>
{principal}

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
     recurso, de modo que la elección viaja con el lector por todo el sitio.
     Y `paliLang()` —definida en la cabecera, antes de que se pinte nada— da
     la lengua de arranque: la elegida si la hay, y si no la del navegador,
     que es la del sistema operativo del lector. */
  var TITULOS = {{ es: {titulo_json}, en: {lang_en_json} }};
  var DESCRIPCIONES = {{ es: {descripcion_json}, en: {descripcion_en_json} }};
  var META_DESC = document.querySelector('meta[name="description"]');
  var l = document.createElement('button');
  l.id = 'lang-btn'; l.type = 'button';
  /* Dos segmentos, ES | EN: el de la lengua en curso va relleno (sesión
     60; mismo dibujo que en las páginas de capítulo). */
  var sES = document.createElement('span'), sEN = document.createElement('span');
  sES.className = sEN.className = 'lang-seg';
  sES.textContent = 'ES'; sEN.textContent = 'EN';
  l.appendChild(sES); l.appendChild(sEN);
  function pinta() {{
    var en = document.body.classList.contains('en');
    document.documentElement.lang = en ? 'en' : 'es';
    document.title = en ? TITULOS.en : TITULOS.es;
    if (META_DESC) {{ META_DESC.content = en ? DESCRIPCIONES.en : DESCRIPCIONES.es; }}
    sES.classList.toggle('lang-cur', !en);
    sEN.classList.toggle('lang-cur', en);
    l.setAttribute('aria-label', en ? 'Ver en español' : 'View in English');
    l.setAttribute('data-tip', en ? 'Ver en español' : 'View in English');
  }}
  {arranque_en}
  l.onclick = function () {{
    document.body.classList.toggle('en');
    try {{ localStorage.setItem('pali_lang', document.body.classList.contains('en') ? 'en' : 'es'); }} catch (e) {{}}
    pinta();
  }};
  pinta();
  /* Arriba, a la derecha de la línea de la marca: flotando abajo tapaba
     el texto (sesión 60). */
  var eb = document.querySelector('.idx-eyebrow');
  if (eb) {{ eb.appendChild(l); }} else {{ document.body.appendChild(l); }}
}})();
</script>
</body>
</html>
"""


# El cuerpo de la portada, de /kaccayana/ y de la guía de las clases. El de
# /recursos/ es otro: el bloque del título y el pie comunes de los recursos
# (recursos_comun.py, etapa 4b), como en cada una de sus páginas.
PRINCIPAL_IDX = """<main class="{clase_main}">
<p class="idx-eyebrow"><span class="marca-arbol"></span>{eyebrow}</p>
<h1 class="display">{h1}</h1>
{cuerpo}
<div class="idx-foot">
<span class="marca-lockup"></span>
{pie}
<p class="idx-licencia">{licencia}</p>
</div>

</main>"""

LICENCIA = ('<span class="i-es">Copyright &copy; 2026 Instituto de Estudios Buddhistas Hispano (IEBH). '
            'Publicado bajo licencia <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.es" '
            'rel="license noopener" target="_blank">CC&nbsp;BY-NC-ND&nbsp;4.0</a>.</span>'
            '<span class="i-en">Copyright &copy; 2026 Instituto de Estudios Buddhistas Hispano (IEBH). '
            'Published under licence <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/" '
            'rel="license noopener" target="_blank">CC&nbsp;BY-NC-ND&nbsp;4.0</a>.</span>')


def tarjeta(href, insignia, titulo, desc, wip=False, externo=False,
            traducir_titulo=True, extra=None, borrador=False):
    """
    Una tarjeta del índice, en los dos idiomas.

    El título se traduce en los recursos —«Paradigmas de declinación»— pero
    no en las obras ni en los capítulos, que son nombres pāḷi.

    «extra» = (href, es, en): un enlace pequeño bajo la tarjeta, fuera de
    ella (la tarjeta ya es un <a> y no puede llevar otro dentro).
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
    if borrador:
        marca += ' <span class="borrador">' + bi("borrador", "draft") + '</span>'
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
    if extra:
        interior += ('\n    <a class="idx-sub" href="{0}" style="display:inline-block;'
                     'margin:.35rem 0 0 1.25rem;font:400 .8rem/1.4 var(--mono);'
                     'color:var(--accent)">→ {1}</a>').format(extra[0], bi(extra[1], extra[2]))
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
    # la misma regla que la propia página (generar_paradigmas.cuenta)
    from generar_paradigmas import cuenta
    return cuenta(json.load(open(p, encoding="utf-8")))[0]


def cuenta_casos():
    """(usos, ejemplos) de recursos/casos/usos.json, para la insignia."""
    import json
    p = os.path.join(RAIZ, "recursos", "casos", "usos.json")
    if not os.path.exists(p):
        return None
    d = json.load(open(p, encoding="utf-8"))
    usos = sum(len(i.get("sub", [])) for i in d.get("inflexiones", []))
    ej = 0
    pila = [u for i in d.get("inflexiones", []) for u in i.get("sub", [])]
    while pila:
        u = pila.pop()
        ej += len(u.get("ejemplos", []))
        pila.extend(u.get("sub", []))
    return usos, ej, d.get("version", "")


def cuenta_clasificacion():
    """(aforismos, con nota, versión) de recursos/clasificacion/datos.json."""
    import json
    p = os.path.join(RAIZ, "recursos", "clasificacion", "datos.json")
    if not os.path.exists(p):
        return None
    d = json.load(open(p, encoding="utf-8"))
    s = d.get("suttas", {})
    return len(s), sum(1 for e in s.values() if "nota" in e), d.get("version", "")


def cuenta_analisis():
    """(capítulos, suttas, versión) de recursos/analisis/."""
    import json
    p = os.path.join(RAIZ, "recursos", "analisis", "meta.json")
    if not os.path.exists(p):
        return None
    m = json.load(open(p, encoding="utf-8"))
    caps, n = [], 0
    for f in m.get("capitulos", []):
        d = json.load(open(os.path.join(RAIZ, "recursos", "analisis", "datos", f), encoding="utf-8"))
        caps.append(d["pali"].replace("-Kappa", ""))
        n += len(d["suttas"])
    return " · ".join(caps), n, m.get("version", ""), m.get("etiqueta")


def cuenta_comentarios():
    """(obras, versión) de las tablas de docs/referencias/, para la insignia."""
    import json
    p = os.path.join(RAIZ, "recursos", "comentarios", "meta.json")
    if not os.path.exists(p):
        return None
    m = json.load(open(p, encoding="utf-8"))
    md = open(os.path.join(RAIZ, m["fuentes"]["es"]), encoding="utf-8").read()
    return len(re.findall(r"^\| \*\*", md, re.M)), m.get("version", "")


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

# La portada (rediseño de la navegación, etapa 1; mesa de trabajo 1 del diseño
# aprobado por el IEBH el 2026-10-08). Los rangos de § salen de
# comun/concordancia.json (por generar_secciones.mapa), los recuentos de los
# datos de cada recurso; aquí no se teclea ningún número.

# Estado de los capítulos de Kaccāyana que no están publicados.
ESTADO_KACC = {6: ("en preparación", "in preparation")}

# Los recursos de la portada, en tres grupos por lo que hace el estudiante.
# (href, título es, título en, línea es, línea en, borrador). Los «__X__» se
# rellenan con los datos en grupos_recursos().
GRUPOS_RECURSOS = [
    (("Consultar", "Look up"), [
        ("glosario/", "Glosario gramatical", "Grammatical glossary",
         "Nandisena, el <i>Conspectus Terminorum</i> de Smith y la terminología "
         "de estas traducciones",
         "Nandisena, Smith's <i>Conspectus Terminorum</i> and the terminology "
         "of these translations", False),
        ("raices/", "Raíces", "Roots",
         "Las __N_RAICES__ raíces de <i>Saddanīti</i>, con <i>Dhātupāṭha</i>, "
         "<i>Dhātumañjūsā</i> y <i>Dhātvatthasaṅgaha</i>",
         "The __N_RAICES_EN__ roots of <i>Saddanīti</i>, with <i>Dhātupāṭha</i>, "
         "<i>Dhātumañjūsā</i> and <i>Dhātvatthasaṅgaha</i>", False),
        ("paradigmas/", "Paradigmas", "Paradigms",
         # texto del IEBH, 2026-10-08
         "Declinación nominal y pronominal · <i>vibhatti-paccaya</i>, "
         "sufijos-inflexiones",
         "Nominal and pronominal declension · <i>vibhatti-paccaya</i>, "
         "inflectional suffixes", False),
    ]),
    (("Derivar y practicar", "Derive and practise"), [
        ("sandhi/", "Sandhi", "Sandhi",
         "Las __N_REGLAS__ reglas de combinación eufónica y __N_FORMAS__ formas, "
         "paso a paso",
         "The __N_REGLAS__ rules of euphonic combination and __N_FORMAS__ "
         "forms, step by step", False),
        ("solucionador/", "Solucionador de sandhis", "Sandhi solver",
         "Separar un pasaje pāḷi en sus voces, con la secuencia de cada sandhi",
         "Split a Pāḷi passage into its words, with the sequence of each sandhi",
         False),
        ("nombre/", "Formación del nombre", "Formation of the noun",
         "<i>pācako</i>, de la raíz al nominativo, paso a paso",
         "<i>pācako</i>, from the root to the nominative, step by step", False),
        ("verbo/", "El verbo", "The verb",
         "Las inflexiones del verbo y __N_PARADIGMAS_VERBO__ paradigmas de "
         "conjugación",
         "The inflections of the verb and __N_PARADIGMAS_VERBO__ conjugation "
         "paradigms", False),
    ]),
    (("Estudiar los suttas", "Study the suttas"), [
        ("clasificacion/", "Clasificación de los suttas",
         "Classification of the suttas",
         "Saññā, adhikāra, paribhāsā y vidhi, __RANGO_CLASIFICACION__",
         "Saññā, adhikāra, paribhāsā and vidhi, __RANGO_CLASIFICACION__", True),
        ("analisis/", "Análisis según Visuddhāyuṃ",
         "Analysis following Visuddhāyuṃ",
         "Clase, aṅga, funciones y ejemplo de cada sutta, __RANGO_ANALISIS__",
         "Class, aṅga, roles and example of each sutta, __RANGO_ANALISIS__",
         True),
        ("casos/", "Usos de las inflexiones", "Uses of the inflections",
         "Qué expresa cada inflexión, según <i>Rūpasiddhi</i>",
         "What each inflection expresses, following <i>Rūpasiddhi</i> "
         "(in Spanish)", True),
        ("comentarios/", "Comentarios", "Commentaries",
         "Las obras de la escuela gramatical de Kaccāyana",
         "The works of the Kaccāyana school of grammar", True),
    ]),
]

NUMEROS = {1: ("Una", "One"), 2: ("dos", "two"), 3: ("tres", "three"),
           4: ("cuatro", "four"), 5: ("cinco", "five"), 6: ("seis", "six")}


def rango(ns):
    ns = sorted(ns)
    return "§{0}–§{1}".format(ns[0], ns[-1]) if ns else ""


def rango_analisis():
    """§ mínimo y máximo de las filas de recursos/analisis/datos/."""
    p = os.path.join(RAIZ, "recursos", "analisis", "meta.json")
    if not os.path.exists(p):
        return ""
    m = json.load(open(p, encoding="utf-8"))
    ns = []
    for f in m.get("capitulos", []):
        d = json.load(open(os.path.join(RAIZ, "recursos", "analisis", "datos", f),
                           encoding="utf-8"))
        ns += [s["n"] for s in d["suttas"]]
    return rango(ns)


def rango_clasificacion():
    p = os.path.join(RAIZ, "recursos", "clasificacion", "datos.json")
    if not os.path.exists(p):
        return ""
    return rango(int(k) for k in json.load(open(p, encoding="utf-8"))["suttas"])


def recursos_descritos():
    """GRUPOS_RECURSOS con los «__X__» ya rellenos: [((grupo es, grupo en),
    [(href, título es, título en, línea es, línea en, borrador), …]), …].
    La portada pinta esto, y la búsqueda del sitio (generar_busqueda.py)
    toma de aquí el título y la línea de cada recurso."""
    miles = lambda n: "{0:,}".format(n).replace(",", ".")
    rai = cuenta_raices() or (0, 0, 0, 0)
    sandhi = formas_sandhi() or (0, 0)
    verbo = cuenta_verbo() or (0, 0)
    valores = {
        "__N_RAICES__": miles(rai[0]), "__N_RAICES_EN__": "{0:,}".format(rai[0]),
        "__N_PARADIGMAS__": str(tablas_paradigmas() or 0),
        "__N_REGLAS__": str(sandhi[0]), "__N_FORMAS__": str(sandhi[1]),
        "__N_PARADIGMAS_VERBO__": str(verbo[1]),
        "__RANGO_CLASIFICACION__": rango_clasificacion(),
        "__RANGO_ANALISIS__": rango_analisis(),
    }
    out = []
    for grupo, items in GRUPOS_RECURSOS:
        llenos = []
        for href, t_es, t_en, d_es, d_en, borrador in items:
            for k, v in valores.items():
                d_es, d_en = d_es.replace(k, v), d_en.replace(k, v)
            llenos.append((href, t_es, t_en, d_es, d_en, borrador))
        out.append((grupo, llenos))
    return out


def grupos_recursos():
    """Los tres grupos de la portada, con los números tomados de los datos."""
    bloques = []
    for (g_es, g_en), items in recursos_descritos():
        tarjetas = []
        for href, t_es, t_en, d_es, d_en, borrador in items:
            etiqueta = (' <span class="borrador">' + bi("borrador", "draft")
                        + '</span>') if borrador else ""
            tarjetas.append(
                '<li><a class="ini-rec" href="recursos/{0}">'
                '<span class="ini-rec-t">{1}{2}</span>'
                '<span class="ini-rec-d">{3}</span></a></li>'.format(
                    href, bi(t_es, t_en), etiqueta, bi(d_es, d_en)))
        bloques.append(
            '<div class="ini-grupo">\n<h3>{0}</h3>\n<ul class="ini-recs">\n{1}\n</ul>\n</div>'
            .format(bi(g_es, g_en), "\n".join(tarjetas)))
    return "\n".join(bloques)


def portada(pub):
    secc = mapa_secciones()
    caps = secc["capitulos"]
    por_num = {c["num"]: (slug, c) for slug, c in caps.items()}
    total = rango(int(k) for k in secc["secciones"])

    # Kaccāyana: ocho baldosas, las publicadas con su rango de §
    baldosas = []
    for num, titulo, _clave, _desc in CAPITULOS_KACC:
        nombre = titulo.replace("-Kappa", "")
        if num in pub and num in por_num:
            slug, c = por_num[num]
            baldosas.append(
                '<li><a class="ini-cap" href="kaccayana/{0}/">'
                '<span class="ini-cap-n">{1}</span>'
                '<span class="ini-cap-t">{2}</span>'
                '<span class="ini-cap-r">§{3}–§{4}</span></a></li>'.format(
                    slug, num, nombre, c["desde"], c["hasta"]))
        else:
            es, en = ESTADO_KACC.get(num, ("prevista", "planned"))
            baldosas.append(
                '<li><div class="ini-cap pend">'
                '<span class="ini-cap-n">{0}</span>'
                '<span class="ini-cap-t">{1}</span>'
                '<span class="ini-cap-r">{2}</span></div></li>'.format(
                    num, nombre, bi(es, en)))

    n_pub = len(pub)
    kacc = OBRAS[0]
    previstas = [o for o in OBRAS if not o[0]]
    en_curso = len(OBRAS) - len(previstas)
    resumen = bi("{0} traducción en curso, {1} previstas".format(
                     NUMEROS[en_curso][0], NUMEROS[len(previstas)][0]),
                 "{0} translation in progress, {1} planned".format(
                     NUMEROS[en_curso][1], NUMEROS[len(previstas)][1]))
    obra = (
        '<article class="ini-obra">\n'
        '<div class="ini-obra-cab"><h3><a href="kaccayana/">{titulo}</a></h3>'
        '<span class="ini-estado">{estado}</span></div>\n'
        '<p class="ini-obra-d">{desc}</p>\n'
        '<ul class="ini-caps">\n{baldosas}\n</ul>\n'
        '</article>').format(
            titulo=kacc[1], desc=bi(kacc[2]), baldosas="\n".join(baldosas),
            estado=bi("{0} de {1} capítulos · {2}".format(n_pub, len(CAPITULOS_KACC), total),
                      "{0} of {1} chapters · {2}".format(n_pub, len(CAPITULOS_KACC), total)))
    otras = "\n".join(
        '<li class="ini-prev"><span class="ini-prev-e">{0}</span>'
        '<span class="ini-prev-t">{1}</span><span class="ini-prev-d">{2}</span></li>'
        .format(bi("prevista"), titulo, bi(desc)) for _h, titulo, desc in previstas)

    heroe = (
        '<p class="idx-lede ini-lede">' + bi(
            'Traducciones al español de las gramáticas clásicas pāḷi, con '
            'glosario terminológico común y concordancia entre las obras. '
            'Un término pāḷi se traduce siempre igual en todas ellas.',
            'English translations of the classical Pāḷi grammars, with a '
            'shared terminological glossary and a concordance between the '
            'works. A Pāḷi term is always translated the same way in all of '
            'them.') + '</p>\n'
        # La caja grande de búsqueda se quitó (pedido del IEBH, 2026-10-08):
        # la de la barra común, en todas las páginas, es la única. Su
        # explicación está ahora arriba de /buscar/ (generar_busqueda.py).
        )

    cuerpo = (
        heroe +
        '<section class="ini-sec" aria-labelledby="t-obras">\n'
        '<div class="ini-sec-cab"><h2 id="t-obras">' + bi('Obras') + '</h2>'
        '<span>' + resumen + '</span></div>\n'
        + obra + '\n<ul class="ini-prevs">\n' + otras + '\n</ul>\n</section>\n\n'
        '<section class="ini-sec" id="recursos" aria-labelledby="t-recursos">\n'
        '<div class="ini-sec-cab"><h2 id="t-recursos">' + bi('Recursos') + '</h2>'
        '<a href="recursos/">' + bi('Todos los recursos →', 'All resources →')
        + '</a></div>\n<div class="ini-grupos">\n' + grupos_recursos()
        + '\n</div>\n</section>\n\n'
        # Las clases grabadas viven en otro worker (pali-clases) bajo /clases/,
        # detrás del acceso por correo de Cloudflare Access; aquí sólo va el
        # enlace. La guía es pública: está fuera de /clases/ para que se pueda
        # leer antes de entrar.
        '<section class="ini-clases" id="clases" aria-labelledby="t-clases">\n'
        '<div class="ini-clases-t"><h2 id="t-clases">'
        + bi('Clases de Kaccāyana y Rūpasiddhi', 'Kaccāyana &amp; Rūpasiddhi classes')
        + '</h2>\n<p>' + bi(
            'Clases grabadas de gramática pāḷi del Muy Venerable U Sīlānanda, '
            'con transcripción sincronizada, traducción al español y el texto '
            'de cada sutta. Acceso para estudiantes inscritos.',
            'Recorded Pāḷi grammar classes of the Most Venerable U Sīlānanda, '
            'with synced transcript, Spanish translation and the text of each '
            'sutta. Access for enrolled students.') + '</p></div>\n'
        '<div class="ini-clases-b">'
        '<a class="ini-btn prim" href="clases/">' + bi('Entrar a las clases', 'Enter the classes')
        + '</a><a class="ini-btn" href="guia-clases/">' + bi('Guía de las clases', 'Guide to the classes')
        + '</a></div>\n</section>\n')

    return pagina(
        assets_v=version_assets(), clase_main="idx ini",
        titulo="Gramáticas Pāḷi en español",
        descripcion="Traducciones al español de las gramáticas clásicas de la "
                    "lengua pāḷi. Instituto de Estudios Buddhistas Hispano.",
        raiz="",
        eyebrow="Instituto de Estudios Buddhistas Hispano",
        lang_en="Pāḷi Grammars in English",
        descripcion_en="English translations of the classical grammars of the "
                       "Pāḷi language. Instituto de Estudios Buddhistas Hispano.",
        # El inglés es el mismo que ya llevaba `lang_en` para la pestaña del
        # navegador, de modo que el título de la página y el de la pestaña
        # dicen lo mismo.
        h1=bi('Gramáticas P<span class="dia">ā</span><span class="dia">ḷ</span>i '
              'en español',
              'P<span class="dia">ā</span><span class="dia">ḷ</span>i '
              'Grammars in English'),
        cuerpo=cuerpo,
        pie=(bi('Edición con DOI', 'Edition with DOI')
             + ' <a href="https://doi.org/10.5281/zenodo.21948010">'
             '10.5281/zenodo.21948010</a>.<br/>\n  '
             + bi('Textos relacionados: corpus del Sexto Concilio en',
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
            'Kaccāyana-byākaraṇa, ed. y trad. Bhikkhu Nandisena.',
            'The oldest of the surviving Pāḷi grammars. Eight chapters '
            '(<i>kappa</i>), each divided into sections (<i>kaṇḍa</i>). Base '
            'edition of this translation: Kaccāyana-byākaraṇa, ed. and trans. '
            'Bhikkhu Nandisena.') + '</p>\n\n'
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
            'parentheses is that of Saddanīti-Suttamālā, absent in some '
            'suttas.') + '</p>\n'
    ).format(lista(tarjetas))

    return pagina(
        assets_v=version_assets(),
        titulo="Kaccāyana-Byākaraṇaṃ · Gramáticas Pāḷi en español",
        descripcion="Traducción al español de la gramática de Kaccāyana, "
                    "capítulo por capítulo.",
        raiz="../",
        eyebrow=bi("Gramática de Kaccāyana"),
        lang_en="Kaccāyana-Byākaraṇaṃ · Pāḷi Grammars in English",
        descripcion_en="English translation of Kaccāyana's grammar, chapter "
                       "by chapter.",
        h1='Kacc<span class="dia">ā</span>yana-By<span class="dia">ā</span>'
           'kara<span class="dia">ṇ</span>a<span class="dia">ṃ</span>',
        cuerpo=cuerpo,
        pie=(bi('Traducción del Instituto de Estudios Buddhistas Hispano.',
                'Translated by the Instituto de Estudios Buddhistas Hispano.')
             + '<br/>\n  ' + bi('Fuentes y concordancia:',
                                'Sources and concordance:')
             + '\n  {0}.').format(FUENTES))


def cuenta_glosario():
    """(entradas de Nandisena, términos de Smith) para la insignia, si la
    página del glosario está armada; None si no."""
    base = os.path.join(RAIZ, "recursos", "glosario")
    nand = os.path.join(base, "nandisena.json")
    pags = os.path.join(base, "conspectus")
    if not (os.path.exists(nand) and os.path.isdir(pags)):
        return None
    try:
        n = len(json.load(open(nand, encoding="utf-8"))["entradas"])
        c = 0
        for nombre in os.listdir(pags):
            if re.fullmatch(r"p\d{4}\.json", nombre):
                c += len(json.load(open(os.path.join(pags, nombre),
                                        encoding="utf-8"))["terminos"])
        return n, c
    except (OSError, ValueError, KeyError):
        return None


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
            _es += " · {0} de Dhātupāṭha".format(n_rai[2])
            _en += " · {0} from Dhātupāṭha".format(n_rai[2])
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
    n_glo = cuenta_glosario()
    badge_glo = (bi("{0} entradas · {1} términos".format(miles(n_glo[0]), miles(n_glo[1])),
                    "{0} entries · {1} terms".format("{0:,}".format(n_glo[0]), "{0:,}".format(n_glo[1])))
                 if n_glo else "glosario")
    n_cas = cuenta_casos()
    badge_cas = (bi("{0} usos · {1} ejemplos · v{2}".format(*n_cas),
                    "{0} uses · {1} examples · v{2}".format(*n_cas))
                 if n_cas else "casos")
    n_cla = cuenta_clasificacion()
    badge_cla = (bi("{0} aforismos · {1} notas · v{2}".format(*n_cla),
                    "{0} aphorisms · {1} notes · v{2}".format(*n_cla))
                 if n_cla else "clasificación")
    n_ana = cuenta_analisis()
    # Capítulos y rango de §, de los datos; no de la «etiqueta» de meta.json,
    # que se escribe a mano y puede quedarse atrás (la auditoría de la
    # navegación encontró un «§52–§343» que ya no era verdad).
    badge_ana = (bi("{0} {1} · v{2}".format(
                        n_ana[0].replace(" · ", " + "), rango_analisis(), n_ana[2]),
                    "{0} {1} · v{2}".format(
                        n_ana[0].replace(" · ", " + "), rango_analisis(), n_ana[2]))
                 if n_ana else "análisis")
    n_com = cuenta_comentarios()
    badge_com = (bi("{0} obras · v{1}".format(*n_com),
                    "{0} works · v{1}".format(*n_com))
                 if n_com else "comentarios")
    insignias = {"__SANDHI_BADGE__": badge, "__PARADIGMAS_BADGE__": badge_par,
                 "__CASOS_BADGE__": badge_cas,
                 "__CLASIFICACION_BADGE__": badge_cla,
                 "__ANALISIS_BADGE__": badge_ana,
                 "__COMENTARIOS_BADGE__": badge_com,
                 "__GLOSARIO_BADGE__": badge_glo,
                 "__RAICES_BADGE__": badge_rai, "__VERBO_BADGE__": badge_ver,
                 "__SOLUCIONADOR_BADGE__": bi("88 % del banco",
                                              "88 % of the bench"),
                 "__NOMBRE_BADGE__": bi("10 pasos", "10 steps")}
    # Los borradores, los mismos que marca la portada (GRUPOS_RECURSOS): la
    # etiqueta común «borrador» va junto al título (etapa 4b), no dentro de
    # la insignia.
    borradores = {href for _g, items in recursos_descritos()
                  for href, _te, _tn, _de, _dn, b in items if b}
    tarjetas = [tarjeta(href, insignias.get(ins, ins), titulo, desc,
                        extra=extra[0] if extra else None,
                        borrador=href in borradores)
                for href, ins, titulo, desc, *extra in RECURSOS
                if (ins != "__RAICES_BADGE__" or n_rai)
                and (ins != "__VERBO_BADGE__" or n_ver)
                and (ins != "__GLOSARIO_BADGE__" or n_glo)
                and (ins != "__CASOS_BADGE__" or n_cas)
                and (ins != "__CLASIFICACION_BADGE__" or n_cla)
                and (ins != "__ANALISIS_BADGE__" or n_ana)
                and (ins != "__COMENTARIOS_BADGE__" or n_com)]

    # El número de paradigmas, de los datos: la descripción decía «83» a
    # mano mientras la insignia contaba 85 (2026-10-08).
    tarjetas = [t.replace("__N_PARADIGMAS__", str(n_par)) for t in tarjetas]

    # Un quinto elemento True marca la obra como en curso: insignia apagada y
    # la etiqueta común «borrador».
    externas = [tarjeta(href, ins, titulo, desc, externo=True,
                        wip=bool(resto and resto[0]),
                        borrador=bool(resto and resto[0]))
                for href, ins, titulo, desc, *resto in CORPUS]

    lede = bi('Material de referencia para el estudio de la lengua pāḷi, '
              'complementario a las traducciones de las gramáticas, y el '
              'corpus en el que leer los pasajes que citan.',
              'Reference material for the study of the Pāḷi language, '
              'complementary to the translations of the grammars, and the '
              'corpus in which to read the passages they cite.')
    # El bloque del título y el pie, los comunes de los recursos: el marcado
    # lo pone recursos_comun.componer() al pasar por cabecera.insertar().
    principal = (
        '<rc-titulo>\n'
        '<rc-ceja>' + bi("Material de apoyo", "Reference material") + '</rc-ceja>\n'
        '<rc-h1>' + bi("Recursos") + '</rc-h1>\n'
        '<rc-desc>' + lede + '</rc-desc>\n'
        '</rc-titulo>\n'
        '<main class="idx idx-rec">\n'
        '<h2>' + bi('Disponible') + '</h2>\n' + lista(tarjetas) + '\n\n'
        '<h2>' + bi('Corpus') + '</h2>\n' + lista(externas) + '\n'
        '</main>\n'
        '<rc-pie>\n'
        '<rc-licencia>{0} {1}.<br>\n{2}</rc-licencia>\n'
        '</rc-pie>'.format(bi("Fuentes:", "Sources:"), FUENTES, LICENCIA))

    return pagina(
        assets_v=version_assets(),
        titulo="Recursos · Gramáticas Pāḷi en español",
        descripcion="Material de apoyo para el estudio de la gramática pāḷi: "
                    "reglas, tablas y glosarios.",
        raiz="../",
        lang_en="Resources · Pāḷi Grammars in English",
        descripcion_en="Reference material for the study of Pāḷi grammar: "
                       "rules, tables and glossaries.",
        principal=principal)


def guia_clases():
    """
    La guía para estudiantes de las clases grabadas de U Sīlānanda.

    El cuerpo vive en herramientas/guia_clases.html (sólo en español: la
    escriben y la leen los estudiantes hispanohablantes); aquí sólo se envuelve
    con la plantilla de los índices. La ruta no empieza por «clases»: la
    aplicación de Cloudflare Access cubre gramaticas.buddha-dhamma.net/clases*
    y la guía tiene que poder leerse antes de entrar.
    """
    cuerpo = open(os.path.join(RAIZ, "herramientas", "guia_clases.html"),
                  encoding="utf-8").read()
    return pagina(
        assets_v=version_assets(), solo_es=True,
        titulo="Guía para estudiantes · Clases de U Sīlānanda",
        descripcion="Cómo entrar a las clases grabadas de gramática pāḷi del "
                    "Muy Venerable U Sīlānanda, usar el reproductor y "
                    "escucharlas sin conexión.",
        raiz="../",
        eyebrow=bi("Clases de Kaccāyana y Rūpasiddhi",
                   "Kaccāyana &amp; Rūpasiddhi classes"),
        lang_en="Student guide · Classes of U Sīlānanda",
        descripcion_en="How to access the recorded Pāḷi grammar classes of "
                       "the Most Venerable U Sīlānanda (guide in Spanish).",
        h1=bi("Guía para estudiantes", "Student guide"),
        cuerpo=cuerpo,
        pie='  {0} <a href="mailto:admin@iebh.org">admin@iebh.org</a>.'.format(
            bi("Dudas y solicitudes de acceso:",
               "Questions and access requests:")))


def pagina(**kw):
    """PAGINA con los dos títulos ya serializados para el botón de idioma."""
    import json as _json
    kw.setdefault("lang_en", kw["titulo"])
    kw.setdefault("clase_main", "idx")
    if "principal" not in kw:
        kw["principal"] = PRINCIPAL_IDX.format(
            clase_main=kw.pop("clase_main"), eyebrow=kw.pop("eyebrow"),
            h1=kw.pop("h1"), cuerpo=kw.pop("cuerpo"), pie=kw.pop("pie"),
            licencia=LICENCIA)
    else:
        kw.pop("clase_main")
    # Una página sólo en español (la guía de las clases) no arranca en inglés
    # aunque el lector lo haya elegido: no tendría con qué volver, porque su
    # conmutador lo sustituye la barra común, que allí dice «Solo en español».
    kw["arranque_en"] = ("" if kw.pop("solo_es", False) else
                         "if (paliLang() === 'en') {{ document.body.classList.add('en'); }}"
                         .replace("{{", "{").replace("}}", "}"))
    kw.setdefault("descripcion_en", kw["descripcion"])
    kw["titulo_json"] = _json.dumps(kw["titulo"], ensure_ascii=False)
    kw["lang_en_json"] = _json.dumps(kw.pop("lang_en"), ensure_ascii=False)
    kw["descripcion_json"] = _json.dumps(kw["descripcion"], ensure_ascii=False)
    kw["descripcion_en_json"] = _json.dumps(kw.pop("descripcion_en"),
                                            ensure_ascii=False)
    return PAGINA.format(**kw)


def escribir(ruta, html, clave):
    html = cabecera.insertar(html, clave)
    destino = os.path.join(RAIZ, ruta)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(html)
    return ruta


def main():
    pub = capitulos_publicados()
    hechas = [
        escribir("site/index.html", portada(pub), "portada"),
        escribir("site/kaccayana/index.html", indice_kaccayana(pub), "kaccayana"),
        escribir("site/recursos/index.html", indice_recursos(), "recursos"),
        escribir("site/guia-clases/index.html", guia_clases(), "guia-clases"),
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
