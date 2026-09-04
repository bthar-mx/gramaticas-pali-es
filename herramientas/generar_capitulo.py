#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el HTML de un capítulo a partir de su markdown.

    python3 herramientas/generar_capitulo.py kaccayana/01-sandhi-kappa.md
    python3 herramientas/generar_capitulo.py kaccayana/01-sandhi-kappa.en.md

La fuente es el markdown; el HTML es salida y no debe editarse a mano.
Un maestro `NN-nombre.en.md` es la edición inglesa del mismo capítulo: usa
los mismos metadatos de CAPITULOS (más `titulo_en`), las cadenas de
IDIOMAS["en"], y se publica en site/en/<obra>/<slug>/. Las dos páginas se
enlazan entre sí (botón EN/ES y `hreflang`) sólo si la otra existe.
Los estilos y la lógica son compartidos (site/assets/); este script sólo
produce la estructura del capítulo.
"""

import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Metadatos de cada capítulo ──────────────────────────────────────────
# Lo único que hay que añadir al empezar un capítulo nuevo.
CAPITULOS = {
    "01-sandhi-kappa": {
        "slug": "sandhi",
        "obra": "Kaccāyana-Byākaraṇaṃ",
        "obra_sub": "Gramática de Kaccāyana",
        "obra_slug": "kaccayana",
        "num": 1,
        "titulo_pali": "1-Sandhi-Kappa",
        "titulo_es": "1-Capítulo de Sandhi",
        "titulo_en": "1-Sandhi Chapter",
        "anterior": None,
        "siguiente": "2-Nāma-Kappa",
        "version": "1.5",
        "version_fecha": "2026-09-03",
        "version_nota": "Las citas canónicas pasan de las notas al pie al "
                        "bloque pāḷi, en línea y con la forma de la edición "
                        "base (Khu. i, 67), como en Nāma y Kāraka; repuestas "
                        "las que faltaban (§20, §36). Repuestos el "
                        "contraejemplo «upanīyati» de §26 con su nota y las "
                        "notas de variante de Nandisena (§1, §7, §28, §35, "
                        "§51). Corregidas seis erratas (§15–16, §31, §32, "
                        "§41 y el emergente de kvaci). Edición inglesa "
                        "paralela en /en/.",
        "version_en": "1.0",
        "version_fecha_en": "2026-09-03",
        "version_nota_en": "First English edition: Bhikkhu U Nandisena's "
                           "translation with the apparatus of the Spanish "
                           "edition (formation sequences, counter-examples, "
                           "word-count breakdowns after Thitzana, glossary "
                           "tooltips) and a fixed glossary for the technical "
                           "terms.",
    },
    "02-nama-kappa": {
        "slug": "nama",
        "obra": "Kaccāyana-Byākaraṇaṃ",
        "obra_sub": "Gramática de Kaccāyana",
        "obra_slug": "kaccayana",
        "num": 2,
        "titulo_pali": "2-Nāma-Kappa",
        "titulo_es": "2-Capítulo del Nombre",
        "titulo_en": "2-Noun Chapter",
        "anterior": "1-Sandhi-Kappa",
        "siguiente": "3-Kāraka-Kappa",
        "version": "1.2",
        "version_fecha": "2026-08-20",
        "version_nota": "Restituidas 118 referencias canónicas que la fase de "
                        "traducción había retirado (briefings 04–05, §10.1) y "
                        "806 tramos de la negrita que Nandisena pone dentro "
                        "del vutti, ambas tomadas de la edición base y "
                        "verificadas por reconstrucción. La sigla de cada "
                        "referencia se desata al pasar el cursor.",
        "version_en": "1.0",
        "version_fecha_en": "2026-09-03",
        "version_nota_en": "First English edition: Bhikkhu U Nandisena's "
                           "translation with the apparatus of the Spanish "
                           "edition (formation of every example with its "
                           "suttas, word-count breakdowns after Thitzana, "
                           "glossary tooltips) and a fixed glossary for the "
                           "technical terms.",
    },
    "03-karaka-kappa": {
        "slug": "karaka",
        "obra": "Kaccāyana-Byākaraṇaṃ",
        "obra_sub": "Gramática de Kaccāyana",
        "obra_slug": "kaccayana",
        "num": 3,
        "titulo_pali": "3-Kāraka-Kappa",
        "titulo_es": "3-Capítulo de casos gramaticales",
        "titulo_en": "3-Case Chapter",
        "anterior": "2-Nāma-Kappa",
        "siguiente": "4-Samāsa-Kappa",     # en preparación: botón inactivo
        "version": "1.1",
        "version_fecha": "2026-08-20",
        "version_nota": "Restituidas 96 referencias canónicas que la fase de "
                        "traducción había retirado (briefings 04–05, §10.1) y "
                        "la negrita del vutti cotejada con el PDF de la "
                        "edición base (74 tramos, 14 nuevos). La sigla de "
                        "cada referencia se desata al pasar el cursor.",
        "version_en": "1.0",
        "version_fecha_en": "2026-09-03",
        "version_nota_en": "First English edition: Bhikkhu U Nandisena's "
                           "translation with the apparatus of the Spanish "
                           "edition (numbered examples with the word "
                           "under study in bold, word-count breakdowns "
                           "after Thitzana, references and notes) and the "
                           "fixed glossary for the technical terms.",
    },
}

# ── Idiomas ────────────────────────────────────────────────────────────
# Todo lo que la página dice por su cuenta (no el texto del capítulo) sale de
# aquí. La edición inglesa es decisión del IEBH (sesión 45), con permiso del
# Venerable Nandisena: su inglés donde lo hay, el aparato del español encima.
IDIOMAS = {
    "es": {
        "lang": "es",
        "raiz": "../../",
        "obra_sub": None,                     # el de CAPITULOS
        "kandas": ["Primera sección", "Segunda sección", "Tercera sección",
                   "Cuarta sección", "Quinta sección", "Sexta sección",
                   "Séptima sección", "Octava sección"],
        "meses": ["enero", "febrero", "marzo", "abril", "mayo", "junio",
                  "julio", "agosto", "septiembre", "octubre", "noviembre",
                  "diciembre"],
        "fecha": "{d} de {mes} de {a}",
        "version": "Versión",
        "voz": ("voz", "voces"),
        "kacc_sutta": "Kaccāyana Sutta",
        "rup_sutta": "Rūpasiddhi Sutta",
        "sadd_sutta": "Saddanīti-Suttamālā Sutta",
        "tomo_pag": "{obra} · tomo {tomo}, página {pag}",
        "mostrar_mas": "Mostrar más (formación, etc.)",
        "ver_notas": "Ver notas",
        "estudiado": "Estudiado",
        "marcar_estudiado": "Marcar como estudiado",
        "enlace": "Enlace",
        "copiar_enlace": "Copiar enlace a este sutta",
        "copiar": "Copiar §",
        "copiar_sutta": "Copiar sutta al portapapeles",
        "inicio": "Inicio ↑",
        "volver_inicio": "Volver al inicio",
        "versos": "Versos introductorios",
        "cap_anterior": "Capítulo anterior",
        "cap_siguiente": "Capítulo siguiente",
        "introduccion": "Introducción",
        "capitulo_de": "Capítulo {n} de 8",
        "toc_aria": "Ir a un sutta o filtrar por título",
        "toc_placeholder": "Ir a §… / filtrar",
        "toc_label": "Tabla de contenidos",
        "kanda_ir": "Ir a la {es} ({pali}, §{a}–§{b})",
        "kanda_aria": "Ir al sutta número…",
        "kanda_label": "Kaṇḍa:",
        "modo_oscuro": "Alternar modo oscuro",
        "modo_oscuro_t": "Modo oscuro/claro",
        "edicion": "Edición bilingüe Pāḷi–Español",
        "secciones": ("sección", "secciones"),
        "buscar": "Buscar sutta (pāḷi o español)…",
        "imprimir": "Imprimir / PDF",
        "expandir": "Expandir todo",
        "colapsar": "Colapsar todo",
        "reducir": "Reducir texto",
        "aumentar": "Aumentar texto",
        "estudiados": "estudiados",
        "estudiados_t": "Suttas estudiados",
        "pie_ayuda": "Pasa el cursor sobre los términos pāḷi o los superíndices "
                     "numéricos para ver su significado. Expande «Ver notas» "
                     "para leer las notas completas.",
        "lang_btn": "EN",
        "lang_btn_aria": "View this chapter in English",
        # cadenas que usa pali.js
        "js": {
            "estudiados": "estudiados", "abiertos": "abiertos",
            "ocultar_notas": "Ocultar notas", "ver_notas": "Ver notas",
            "ocultar": "Ocultar", "mostrar_mas": "Mostrar más (formación, etc.)",
            "encontrados": "sutta(s) encontrado(s)", "copiado": "✓ Copiado",
            "copiar": "Copiar §",
        },
    },
    "en": {
        "lang": "en",
        "raiz": "../../../",
        "obra_sub": "Kaccāyana's Grammar",
        "kandas": ["First section", "Second section", "Third section",
                   "Fourth section", "Fifth section", "Sixth section",
                   "Seventh section", "Eighth section"],
        "meses": ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November",
                  "December"],
        "fecha": "{d} {mes} {a}",
        "version": "Version",
        "voz": ("word", "words"),
        "kacc_sutta": "Kaccāyana Sutta",
        "rup_sutta": "Rūpasiddhi Sutta",
        "sadd_sutta": "Saddanīti-Suttamālā Sutta",
        "tomo_pag": "{obra} · vol. {tomo}, p. {pag}",
        "mostrar_mas": "Show more (formation, etc.)",
        "ver_notas": "Show notes",
        "estudiado": "Studied",
        "marcar_estudiado": "Mark as studied",
        "enlace": "Link",
        "copiar_enlace": "Copy link to this sutta",
        "copiar": "Copy §",
        "copiar_sutta": "Copy sutta to clipboard",
        "inicio": "Top ↑",
        "volver_inicio": "Back to top",
        "versos": "Introductory verses",
        "cap_anterior": "Previous chapter",
        "cap_siguiente": "Next chapter",
        "introduccion": "Introduction",
        "capitulo_de": "Chapter {n} of 8",
        "toc_aria": "Go to a sutta or filter by title",
        "toc_placeholder": "Go to §… / filter",
        "toc_label": "Contents",
        "kanda_ir": "Go to the {es} ({pali}, §{a}–§{b})",
        "kanda_aria": "Go to sutta number…",
        "kanda_label": "Kaṇḍa:",
        "modo_oscuro": "Toggle dark mode",
        "modo_oscuro_t": "Dark/light mode",
        "edicion": "Bilingual Pāḷi–English edition",
        "secciones": ("section", "sections"),
        "buscar": "Search sutta (Pāḷi or English)…",
        "imprimir": "Print / PDF",
        "expandir": "Expand all",
        "colapsar": "Collapse all",
        "reducir": "Smaller text",
        "aumentar": "Larger text",
        "estudiados": "studied",
        "estudiados_t": "Suttas studied",
        "pie_ayuda": "Hover over the Pāḷi terms or the numeric superscripts to "
                     "see their meaning. Expand “Show notes” to read the full "
                     "notes.",
        "lang_btn": "ES",
        "lang_btn_aria": "Ver este capítulo en español",
        "js": {
            "estudiados": "studied", "abiertos": "open",
            "ocultar_notas": "Hide notes", "ver_notas": "Show notes",
            "ocultar": "Hide", "mostrar_mas": "Show more (formation, etc.)",
            "encontrados": "sutta(s) found", "copiado": "✓ Copied",
            "copiar": "Copy §",
        },
    },
}
L = IDIOMAS["es"]          # el idioma en curso; main() lo fija

COPYRIGHT_EN = (
    "Pāḷi text and English translation by Bhikkhu U Nandisena (ITBMU); "
    "edition, apparatus and glossary by the Instituto de Estudios Buddhistas "
    "Hispano (IEBH). This material may be reproduced for personal use and "
    "distributed free of charge. Copyright © 2026 IEBH. Published under "
    '<a href="https://creativecommons.org/licenses/by-nc-nd/4.0/" '
    'rel="license">CC BY-NC-ND 4.0</a> · DOI '
    '<a href="https://doi.org/10.5281/zenodo.21948010">'
    "10.5281/zenodo.21948010</a>."
)

COPYRIGHT = (
    "Edición del texto en pāḷi y traducción al español por Bhikkhu Nandisena. "
    "Este material puede ser reproducido para uso personal y distribuido de "
    "forma gratuita. Copyright © 2026 Instituto de Estudios Buddhistas "
    "Hispano (IEBH). Publicado bajo licencia "
    '<a href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.es" '
    'rel="license">CC BY-NC-ND 4.0</a> · DOI '
    '<a href="https://doi.org/10.5281/zenodo.21948010">'
    "10.5281/zenodo.21948010</a>."
)
# Éste es el DOI de *concepto* —el que Zenodo llama «Cite all versions»—, no
# el de ninguna versión concreta: resuelve siempre a la más reciente, que es
# lo que corresponde a una página que siempre muestra lo último. Con un DOI
# de versión el pie se quedaría atrás en cada entrega.
# Los de versión son 21948011 (v1.0.0) y 22037060 (v1.1.0), y viven en la
# lista `identifiers` de `CITATION.cff`.

KANDAS_PALI = ["Paṭhama-Kaṇḍa", "Dutiya-Kaṇḍa", "Tatiya-Kaṇḍa",
               "Catuttha-Kaṇḍa", "Pañcama-Kaṇḍa", "Chaṭṭha-Kaṇḍa",
               "Sattama-Kaṇḍa", "Aṭṭhama-Kaṇḍa"]
KANDAS_ES = ["Primera sección", "Segunda sección", "Tercera sección",
             "Cuarta sección", "Quinta sección", "Sexta sección",
             "Séptima sección", "Octava sección"]

# El número de Rūpasiddhi puede ser doble: «271. 88, 308.» (§271 del Kāraka).
RE_SUTTA = re.compile(
    r'^\*\*(\d+)\\?\.\s*(\d+(?:,\s*\d+)*)\\?\.\s*(.+?)\*\*\s*(.*)$')
RE_KANDA = re.compile(r'^\*\*([A-ZĀĪŪṂṆṬḌÑṄḶ]+-KAṆḌA)\*\*')
RE_FN_DEF = re.compile(r'^\[\^(\d+)\]:\s*(.*)$')

# Numeración de kaṇḍas: la del capítulo es correlativa (1, 2, 3…), pero el
# nombre que le toca lo dice el propio markdown. El Kāraka-kappa es el
# CHAṬṬHA-KAṆḌA aunque sea el primer (y único) kaṇḍa de su archivo.
KANDA_NOMBRE = {}          # nº correlativo del capítulo → índice en KANDAS_*


def indice_kanda(k):
    return KANDA_NOMBRE.get(k, k - 1)


def kanda_pali(k):
    return KANDAS_PALI[indice_kanda(k)]


def kanda_es(k):
    return L["kandas"][indice_kanda(k)]


# ── Utilidades de texto ─────────────────────────────────────────────────

def desescapar(t):
    """El markdown viene de una exportación con escapes tipo \\[ \\+ \\= \\."""
    return re.sub(r'\\([\[\]\+\.\(\)\*\-=!])', r'\1', t)


def escapar_html(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# Abreviaturas de otras obras: "Rū. §49", "Sad. §139", "Bā. §41" remiten a
# Rūpasiddhi, Saddanīti y Bālāvatāra, no a un sutta de este capítulo.
# Admite un tomo en números romanos por medio: "Sad. iii §25".
RE_OTRA_OBRA = re.compile(
    r'[A-ZĀĪŪÑṄ][a-zāīūṃṇṭḍñṅḷ]{0,4}\.\s*(?:[ivxlcdm]+\s+)?$')
# "Kac. §79" es la propia obra: sí se enlaza si el sutta está en el capítulo.
RE_PROPIA_OBRA = re.compile(r'Kac\.\s*$')

SUTTAS_VALIDOS = set()
SUTTAS_OTROS_CAP = {}     # n → (slug, título del capítulo, título del sutta)
RESUMEN_SUTTAS = {}       # n → «Título — glosa» de este capítulo
FIN_CAPITULO = {}
NO_ENLAZADOS = []


def atributo(t):
    """Texto seguro para un atributo HTML entre comillas dobles."""
    return escapar_html(t).replace('"', '&quot;')


def cargar_capitulos_publicados(clave_actual, obra_slug):
    """Suttas de otros capítulos ya publicados, desde comun/concordancia.json.

    Permite enlazar las citas cruzadas (p. ej. §20 del Sandhi-kappa citado
    desde el Nāma-kappa). Sólo se enlaza a capítulos cuyo HTML existe.
    """
    ruta = os.path.join(RAIZ, "comun", "concordancia.json")
    if not os.path.exists(ruta):
        return
    with open(ruta, encoding="utf-8") as f:
        conc = json.load(f)
    for clave, cap in conc.get("capitulos", {}).items():
        if clave == clave_actual or clave not in CAPITULOS:
            continue
        meta = CAPITULOS[clave]
        destino = os.path.join(RAIZ, "site", meta["obra_slug"], meta["slug"],
                               "index.html")
        if meta["obra_slug"] != obra_slug or not os.path.exists(destino):
            continue
        for s in cap.get("suttas", []):
            SUTTAS_OTROS_CAP[s["kaccayana"]] = (meta["slug"],
                                                meta["titulo_pali"],
                                                s.get("pali", ""))


def enlazar_suttas(t):
    """§N → enlace al ancla del sutta: en este capítulo o, si pertenece a
    otro capítulo ya publicado (concordancia), a su página."""
    def rep(m):
        n = int(m.group(1))
        previo = t[max(0, m.start() - 14):m.start()]
        otra = RE_OTRA_OBRA.search(previo) and not RE_PROPIA_OBRA.search(previo)
        if not otra and (not SUTTAS_VALIDOS or n in SUTTAS_VALIDOS):
            resumen = RESUMEN_SUTTAS.get(n, "")
            return ('<a class="sutta-xref" href="#s{0}" onclick="jumpOpen(\'s{0}\')" '
                    'data-tip="§{0}{1}">§{0}</a>').format(
                        n, " · " + atributo(resumen) if resumen else "")
        if not otra and n in SUTTAS_OTROS_CAP:
            slug, titulo, pali = SUTTAS_OTROS_CAP[n]
            return ('<a class="sutta-xref" href="../{1}/#s{0}" '
                    'data-tip="§{0}{3} ({2})">§{0}</a>').format(
                        n, slug, atributo(titulo),
                        " · " + atributo(pali) if pali else "")
        NO_ENLAZADOS.append((n, previo.strip()))
        return m.group(0)
    return re.sub(r'§(\d+)', rep, t)


def marcar_notas(t, notas):
    """[^n] → superíndice con tooltip que contiene el texto de la nota."""
    def rep(m):
        n = m.group(1)
        cuerpo = notas.get(n, "")
        return ('<span class="fn-tip"><span class="fn-sup">{0}</span>'
                '<span class="fn-tip-box">{1}</span></span>').format(n, cuerpo)
    return re.sub(r'\[\^(\d+)\]', rep, t)


def enfasis(t):
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*(?!\s)([^*]+?)(?<!\s)\*(?!\*)', r'<i>\1</i>', t)
    return t


def glosas_emergentes(t):
    """{término|glosa} → término con glosa emergente al pasar el ratón."""
    return re.sub(
        r'\{([^|{}]+)\|([^{}]+)\}',
        lambda m: ('<span class="tip-wrap"><span class="tip-term">{0}</span>'
                   '<span class="tip-box">{1}</span></span>').format(
                       m.group(1), m.group(2)),
        t)


# Abreviaturas canónicas tal como las imprime Nandisena. La expansión es
# mecánica —desatar la sigla—, no una identificación de la edición: el tomo
# y la página remiten a la edición que él usa, que no consta en los archivos
# del proyecto. Ver `comun/guia-de-estilo.md` §5.
ABREVIATURAS = {
    "D":            "Dīgha-nikāya",
    "M":            "Majjhima-nikāya",
    "S":            "Saṃyutta-nikāya",
    "A":            "Aṅguttara-nikāya",
    "Khu":          "Khuddaka-nikāya",
    "Vin":          "Vinaya-piṭaka",
    "Abhi":         "Abhidhamma-piṭaka",
    "J":            "Jātaka",
    "DA":           "Dīgha-nikāya-aṭṭhakathā",
    "MA":           "Majjhima-nikāya-aṭṭhakathā",
    "SA":           "Saṃyutta-nikāya-aṭṭhakathā",
    "AA":           "Aṅguttara-nikāya-aṭṭhakathā",
    "DhA":          "Dhammapada-aṭṭhakathā",
    "JA":           "Jātaka-aṭṭhakathā",
    "VinA":         "Vinaya-aṭṭhakathā",
    "AbhiA":        "Abhidhamma-aṭṭhakathā",
    "SuttanipātaA": "Suttanipāta-aṭṭhakathā",
    "UdānaA":       "Udāna-aṭṭhakathā",
    "PetavatthuA":  "Petavatthu-aṭṭhakathā",
    "Sad":          "Saddanīti",
    "Mog.-pañcikā": "Moggallāna-pañcikā",
}

# (Khu. i, 336) — una o varias siglas conocidas seguidas de tomo y página.
_SIGLAS = "|".join(re.escape(k) for k in
                   sorted(ABREVIATURAS, key=len, reverse=True))
RE_CITA = re.compile(
    r'\((?P<cuerpo>(?:' + _SIGLAS + r')\.?\s*[ivxlIVXL]+\s*,[^()]*?)\)')
RE_SIGLA_EN_CITA = re.compile(r'\b(' + _SIGLAS + r')\.')
RE_CITA_SIMPLE = re.compile(
    r'^(?P<sigla>' + _SIGLAS + r')\.?\s*(?P<tomo>[ivxlIVXL]+)\s*,\s*'
    r'(?P<pag>[\d\-–]+)$')


def citas_canonicas(t):
    """(Khu. i, 336) → la cita, con la sigla desatada al pasar el ratón.

    Se detectan solas: la sigla es un conjunto cerrado y el tomo va en
    numeración romana, de modo que no hay que marcarlas en el maestro y las
    que ya estaban puestas —las 30 del Sandhi-Kappa— ganan el emergente sin
    tocar el texto. Regla de colocación: guía de estilo §5, sólo en el
    bloque pāḷi.
    """
    def rep(m):
        cuerpo = m.group("cuerpo").strip()
        simple = RE_CITA_SIMPLE.match(cuerpo)
        if simple:
            glosa = L["tomo_pag"].format(
                obra=ABREVIATURAS[simple.group("sigla")],
                tomo=simple.group("tomo").lower(), pag=simple.group("pag"))
        else:
            vistas, obras = set(), []
            for s in RE_SIGLA_EN_CITA.findall(cuerpo):
                if s not in vistas:
                    vistas.add(s)
                    obras.append(ABREVIATURAS[s])
            glosa = " · ".join(obras)
        return ('<span class="ref-tip"><span class="cita-term">({0})</span>'
                '<span class="ref-tip-box">{1}</span></span>').format(
                    m.group("cuerpo"), glosa)
    return RE_CITA.sub(rep, t)


def inline(t, notas):
    """Cadena de transformaciones para texto corrido."""
    t = escapar_html(desescapar(t))
    t = enfasis(t)
    t = glosas_emergentes(t)
    t = marcar_notas(t, notas)
    t = enlazar_suttas(t)
    t = citas_canonicas(t)
    return t


# ── Lectura del markdown ────────────────────────────────────────────────

def leer_notas(lineas):
    notas, orden = {}, []
    for l in lineas:
        m = RE_FN_DEF.match(l)
        if m:
            notas[m.group(1)] = m.group(2).strip()
            orden.append(m.group(1))
    return notas, orden


RE_CIERRE_PALI = re.compile(r'^\*\*(Iti\s+.+?kaṇḍo)\.?\*\*$')
RE_FIN_PALI = re.compile(r'^\*\*(.+?[Nn]iṭṭhito)\.?\*\*$')
RE_FIN_ES = re.compile(r'^\*\*((?:Fin del capítulo|End of the .+? [Cc]hapter).*?)\.?\*\*$')
RE_CIERRE_ES = re.compile(r'^\*\*((?:Así termina la|Thus ends the) .+?)\.?\*\*$')


def separar_cierre(cuerpo):
    """Aparta la fórmula de cierre de kaṇḍa del cuerpo del último sutta.

    En el markdown la fórmula va en un bloque propio detrás del último sutta
    de la sección; en el HTML es un elemento aparte, no parte del sutta.
    """
    pali = es = fin_pali = fin_es = None
    limpio = []
    for l in cuerpo:
        t = l.strip()
        mp, me = RE_CIERRE_PALI.match(t), RE_CIERRE_ES.match(t)
        mfp, mfe = RE_FIN_PALI.match(t), RE_FIN_ES.match(t)
        if mp:
            pali = mp.group(1); continue
        if me:
            es = me.group(1); continue
        if mfp:
            fin_pali = mfp.group(1); continue
        if mfe:
            fin_es = mfe.group(1); continue
        limpio.append(l)
    FIN_CAPITULO.update({k: v for k, v in
                         (("pali", fin_pali), ("es", fin_es)) if v})
    if pali or es:
        # quitar el separador --- que quedaba justo antes de la fórmula
        while limpio and limpio[-1].strip() in ("", "---"):
            limpio.pop()
        return limpio, {"pali": pali, "es": es}
    return cuerpo, None


def parsear(path):
    txt = open(path, encoding="utf-8").read()
    lineas = txt.split("\n")

    notas_crudas, _ = leer_notas(lineas)
    # el cuerpo de la nota también puede llevar §N y énfasis
    notas = {k: inline(v, {}) for k, v in notas_crudas.items()}

    fin_cuerpo = next((i for i, l in enumerate(lineas) if RE_FN_DEF.match(l)),
                      len(lineas))

    suttas, kanda_actual = [], 0
    versos = []
    i = 0
    while i < fin_cuerpo:
        l = lineas[i]
        mk = RE_KANDA.match(l)
        if mk:
            kanda_actual += 1
            nombres = [x.upper() for x in KANDAS_PALI]
            if mk.group(1) in nombres:
                KANDA_NOMBRE[kanda_actual] = nombres.index(mk.group(1))
            i += 1
            continue
        m = RE_SUTTA.match(l)
        if m:
            n, pali, resto = int(m.group(1)), m.group(3), m.group(4)
            rup = ", ".join(x for x in re.split(r'[,\s]+', m.group(2)) if x)
            # notas al pie ancladas en el encabezado (título o tras él)
            notas_hdr = re.findall(r'\[\^(\d+)\]', resto)
            resto = re.sub(r'\[\^\d+\]\s*', '', resto)
            # (Saddanīti) al final del texto pāḷi
            sadd = None
            ms = re.search(r'\(([\d,\s\-–]+)\)\s*\\?\.?\s*$', pali)
            if ms:
                sadd = [x for x in re.split(r'[,\s]+', ms.group(1)) if x]
                pali = pali[:ms.start()].strip()
            pali = desescapar(pali).rstrip(". ").strip()
            pali_notas = pali                       # con anclas, para el título
            pali = re.sub(r'\[\^\d+\]', '', pali)   # limpio: TOC, pastillas…
            # desglose [A + B, n]
            desglose, voces = None, None
            md = re.search(r'\\?\[(.+?),\s*(\d+)\\?\]', resto)
            if md:
                desglose = desescapar(md.group(1)).strip()
                voces = int(md.group(2))
            # cuerpo hasta el siguiente sutta o kaṇḍa
            j = i + 1
            while j < fin_cuerpo and not RE_SUTTA.match(lineas[j]) \
                    and not RE_KANDA.match(lineas[j]):
                j += 1
            cuerpo_s, cierre = separar_cierre(lineas[i + 1:j])
            suttas.append({
                "n": n, "rup": rup, "sadd": sadd, "pali": pali,
                "pali_notas": pali_notas, "notas_hdr": notas_hdr,
                "desglose": desglose, "voces": voces,
                "kanda": max(kanda_actual, 1),
                "cuerpo": cuerpo_s, "cierre": cierre,
            })
            i = j
            continue
        if not suttas and re.match(r'^\s*\d+\)\s', l):
            # Verso introductorio: las líneas pāḷi llevan salto forzado
            # (dos espacios al final); la traducción española, no.
            pali, trad = [re.sub(r'^\s*\d+\)\s*', '', l).rstrip()], []
            k = i + 1
            while k < fin_cuerpo and not re.match(r'^\s*\d+\)\s', lineas[k]) \
                    and not RE_SUTTA.match(lineas[k]) and lineas[k].strip():
                if lineas[k].endswith("  ") and not trad:
                    pali.append(lineas[k].strip())
                else:
                    trad.append(lineas[k].strip())
                k += 1
            versos.append({"pali": pali, "trad": " ".join(trad)})
            i = k
            continue
        i += 1

    return {"suttas": suttas, "notas": notas, "versos": versos,
            "kandas": kanda_actual}


def partir_bloques(cuerpo):
    """Divide el cuerpo de un sutta por los separadores ---."""
    bloques, actual = [], []
    for l in cuerpo:
        if l.strip() == "---":
            bloques.append(actual)
            actual = []
        else:
            actual.append(l)
    bloques.append(actual)
    return [b for b in bloques if any(x.strip() for x in b)]


# ── Renderizado de bloques ──────────────────────────────────────────────

def parrafos(lineas, notas, clase="rest-para"):
    """Agrupa líneas en párrafos, listas numeradas (con sub-ítems `  * `
    anidados, que pueden llegar tras línea en blanco) y títulos en negrita."""
    out, buf, lista = [], [], []
    gap = [False]                     # línea en blanco vista con lista abierta
    # Las listas de «Ejemplos» son prosa (pāḷi + traducción) y van en la
    # serif; las de «Secuencia» son pasos de derivación y siguen en mono.
    ejemplos = [False]

    def volcar_buf():
        if buf:
            out.append('<p class="{0}">{1}</p>'.format(
                clase, inline(" ".join(buf).strip(), notas)))
            buf.clear()

    def volcar_lista():
        if lista:
            items = "".join(
                "<li>{0}{1}</li>".format(
                    inline(x, notas),
                    '<ul class="seq-sub">{0}</ul>'.format("".join(
                        "<li>{0}</li>".format(inline(s, notas)) for s in subs))
                    if subs else "")
                for x, subs in lista)
            out.append('<ol class="seq-list{0}">{1}</ol>'.format(
                " seq-ejemplos" if ejemplos[0] else "", items))
            lista.clear()
        gap[0] = False

    for l in lineas:
        t = l.strip()
        if not t:
            volcar_buf()
            gap[0] = bool(lista)      # la lista queda abierta por si siguen sub-ítems
            continue
        if lista and re.match(r'^\s+\*\s+', l):
            lista[-1][1].append(re.sub(r'^\s+\*\s+', '', l).strip())
            continue
        mi = re.match(r'^(\d+)\.\s+(.*)$', t)
        if mi:
            volcar_buf()
            if lista and gap[0] and mi.group(1) == "1":
                volcar_lista()        # empieza una lista nueva, no continúa la abierta
            lista.append([mi.group(2), []])
            gap[0] = False
            continue
        volcar_lista()
        mt = re.match(r'^\*\*(.+?)\*\*$', t)
        if mt:
            volcar_buf()
            out.append('<div class="formation-title"><strong>{0}</strong></div>'
                       .format(inline(mt.group(1), notas)))
            continue
        me = re.match(r'^(Secuencia|Ejemplos?[^:]*|Contraejemplos?[^:]*'
                      r'|Sequence|Examples?[^:]*|Counter-examples?[^:]*):\s*$', t)
        if me:
            volcar_buf()
            ejemplos[0] = me.group(1).startswith(
                ("Ejemplo", "Contraejemplo", "Example", "Counter-example"))
            out.append('<div class="section-label">{0}</div>'
                       .format(inline(desescapar(me.group(0).rstrip(":")), notas)))
            continue
        buf.append(t)
    volcar_buf(); volcar_lista()
    return "".join(out)


def bloque_pali(lineas, notas):
    """El primer bloque, párrafo por párrafo, como en el maestro.

    Hasta la sesión 14 el bloque se unía en un solo párrafo corrido salvo
    que hubiera un verso, de modo que las separaciones entre las
    explicaciones —«**Dūratthe** tāva: …», «**Antikatthe**: …»— se perdían
    (§275 del Kāraka tiene 22 párrafos; 213 de los 219 suttas del Nāma y 50
    de los 51 del Sandhi estaban igual). Ahora se respetan siempre.

    Modo verso: un párrafo cuyas líneas acaban en salto forzado (dos
    espacios) se mantiene pāda por pāda; el párrafo siguiente es su
    traducción."""
    paras, buf = [], []
    for l in lineas:
        if l.strip():
            buf.append(l)
        elif buf:
            paras.append(buf); buf = []
    if buf:
        paras.append(buf)
    # Pādas según briefing-05 §7.7: salto forzado (dos espacios) y coma
    # final en todas las líneas menos la última.
    es_verso = [len(p) > 1 and all(x.endswith("  ") and
                                   x.rstrip().endswith(",") for x in p[:-1])
                for p in paras]
    out = []
    for i, p in enumerate(paras):
        texto = " ".join(x.strip() for x in p)
        if es_verso[i]:
            out.append('<div class="pali-verse">{0}</div>'.format(
                "<br/>".join(inline(x.strip(), notas) for x in p)))
        elif i and es_verso[i - 1]:
            out.append('<div class="pali-verse-trans">{0}</div>'.format(
                inline(texto, notas)))
        else:
            out.append('<p class="pali-para">{0}</p>'.format(
                inline(texto, notas)))
    return '<div class="pali-block">{0}</div>'.format("".join(out))


def render_sutta(s, notas):
    n = s["n"]
    sid = "s{0}".format(n)
    bloques = partir_bloques(s["cuerpo"])

    pali_html = ""
    if bloques:
        pali_html = bloque_pali(bloques[0], notas)

    gloss_html = vutti_html = ""
    if len(bloques) > 1:
        lineas_es = [x.strip() for x in bloques[1] if x.strip()]
        if lineas_es:
            gloss_html = '<div class="gloss">{0}</div>'.format(
                inline(lineas_es[0], notas))
            for extra in lineas_es[1:]:
                vutti_html += '<div class="vutti">{0}</div>'.format(
                    inline(extra, notas))

    resto_html = ""
    if len(bloques) > 2:
        cuerpo = "".join(parrafos(b, notas) for b in bloques[2:])
        resto_html = (
            '<hr class="divider"/>'
            '<button class="collapsible-btn" data-type="rest" '
            'onclick="toggleSeq(\'{0}seq\', this)">'
            '<svg fill="none" stroke="currentColor" stroke-width="1.5" viewbox="0 0 20 20">'
            '<path d="M4 6h12M4 10h8M4 14h10"></path></svg>\n'
            '        {2}\n      </button>\n'
            '<div class="collapsible-content" id="{0}seq">'
            '<div class="rest-content">{1}</div></div>\n'
        ).format(sid, cuerpo, L["mostrar_mas"])

    # notas al pie usadas en este sutta (primero las del encabezado)
    usadas = []
    for k in re.findall(r'\[\^(\d+)\]', s["pali_notas"]) + s["notas_hdr"]:
        if k not in usadas:
            usadas.append(k)
    for l in s["cuerpo"]:
        for m in re.finditer(r'\[\^(\d+)\]', l):
            if m.group(1) not in usadas:
                usadas.append(m.group(1))
    notas_html = ""
    if usadas:
        items = "".join(
            '<div class="fn-item"><span class="fn-num">{0}</span>'
            '<span class="fn-text">{1}</span></div>'.format(k, notas.get(k, ""))
            for k in usadas)
        notas_html = (
            '<hr class="divider"/>'
            '<button class="collapsible-btn" data-type="fn" data-count="{1}" '
            'onclick="toggleSeq(\'{0}fn\', this)">'
            '<svg fill="none" stroke="currentColor" stroke-width="1.5" viewbox="0 0 20 20">'
            '<path d="M4 6h12M4 10h8M4 14h10"></path></svg>\n'
            '        {3} ({1})\n      </button>\n'
            '<div class="collapsible-content" id="{0}fn">'
            '<div class="fn-block">{2}</div></div>\n'
        ).format(sid, len(usadas), items, L["ver_notas"])

    desglose_html = ""
    if s["desglose"]:
        voces = "{0} {1}".format(s["voces"], L["voz"][0] if s["voces"] == 1 else L["voz"][1])
        desglose_html = '<div class="sutta-breakdown">[{0} = {1}]</div>'.format(
            escapar_html(s["desglose"]), voces)

    ref = ('<span class="sutta-ref">'
           '<span class="ref-tip"><span class="ref-tip-term">{0}</span>'
           '<span class="ref-tip-box">{3}</span></span>. '
           '<span class="ref-tip"><span class="ref-tip-term">{1}</span>'
           '<span class="ref-tip-box">{4}{2}</span></span>.</span>'
           ).format(n, s["rup"], "s" if "," in s["rup"] else "",
                    L["kacc_sutta"], L["rup_sutta"])

    sadd_html = ""
    if s["sadd"]:
        sadd_html = (' <span class="sutta-ref-num"><span class="ref-tip">'
                     '<span class="ref-tip-term">({0})</span>'
                     '<span class="ref-tip-box">{1}</span>'
                     '</span></span>').format(", ".join(s["sadd"]), L["sadd_sutta"])
    if s["notas_hdr"]:
        sadd_html += marcar_notas(
            "".join("[^{0}]".format(k) for k in s["notas_hdr"]), notas)

    return (
        '<div class="sutta-card" id="{sid}">\n'
        '<div class="sutta-header" onclick="toggleCard(\'{sid}\')" role="button" tabindex="0">\n'
        '<div class="sutta-meta">\n'
        '<div class="sutta-ref-line">{ref}<span class="sutta-pali-title">{pali}{sadd}</span></div>\n'
        '{desglose}\n'
        '</div>\n'
        '<svg class="chevron" fill="none" stroke="currentColor" stroke-width="1.5" '
        'viewbox="0 0 20 20"><path d="M5 7.5l5 5 5-5"></path></svg>\n'
        '</div>\n'
        '<div class="sutta-body">\n{palib}{gloss}{vutti}{resto}{notas}'
        '{pie}'
        '</div>\n</div>\n'
    ).format(sid=sid, ref=ref, sadd=sadd_html, pie=pie_tarjeta(sid),
             pali=marcar_notas(escapar_html(s["pali_notas"]), notas),
             desglose=desglose_html, palib=pali_html, gloss=gloss_html,
             vutti=vutti_html, resto=resto_html, notas=notas_html)


def pie_tarjeta(sid):
    return (
        '<div class="sutta-footer">\n'
        '<span class="done-wrap" onclick="toggleDone(\'{sid}\')" title="{marcar}">\n'
        '<span class="done-cb" id="cb-{sid}"></span>\n'
        '<span class="done-label">{estudiado}</span>\n</span>\n'
        '<button class="share-btn" onclick="shareSutta(\'{sid}\')" title="{copiar_enlace}">\n'
        '<svg fill="none" stroke="currentColor" stroke-width="1.5" viewbox="0 0 20 20">'
        '<circle cx="15" cy="5" r="2"></circle><circle cx="5" cy="10" r="2"></circle>'
        '<circle cx="15" cy="15" r="2"></circle><path d="M7 11l6 3M7 9l6-3"></path></svg>\n'
        '          {enlace}\n        </button>\n'
        '<button class="copy-btn" onclick="copySutta(\'{sid}\')" title="{copiar_sutta}">{copiar}</button>\n'
        '<button class="back-top-btn" onclick="volverArriba()" title="{volver}">\n'
        '<svg fill="none" stroke="currentColor" stroke-width="1.5" viewbox="0 0 20 20">'
        '<path d="M10 15V5M5 10l5-5 5 5"></path></svg>\n'
        '          {inicio}\n        </button>\n'
        '</div>\n').format(
            sid=sid, marcar=L["marcar_estudiado"], estudiado=L["estudiado"],
            copiar_enlace=L["copiar_enlace"], enlace=L["enlace"],
            copiar_sutta=L["copiar_sutta"], copiar=L["copiar"],
            volver=L["volver_inicio"], inicio=L["inicio"])


def render_intro(versos, notas):
    bloques = []
    for k, v in enumerate(versos, start=1):
        pali = "<br/>".join(inline(x, notas) for x in v["pali"])
        bloques.append(
            '<div class="intro-verse"><div class="intro-num">{0}</div>'
            '<div class="intro-pali">{1}</div>'
            '<div class="intro-trans">{2}</div></div>'.format(
                k, pali, inline(v["trad"], notas)))
    return (
        '<div class="sutta-card" id="intro">'
        '<div class="sutta-header" onclick="toggleCard(\'intro\')" role="button" tabindex="0">'
        '<div class="sutta-meta"><div class="sutta-ref-line">'
        '<span class="sutta-pali-title">{2}</span></div></div>'
        '<svg class="chevron" fill="none" stroke="currentColor" stroke-width="1.5" '
        'viewbox="0 0 20 20"><path d="M5 7.5l5 5 5-5"></path></svg></div>'
        '<div class="sutta-body"><div class="intro-block">{0}</div>\n{1}</div>\n</div>\n'
    ).format("".join(bloques), pie_tarjeta("intro"), L["versos"])


MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def datos_version(meta):
    """(versión, fecha, nota) del idioma en curso; en inglés, las claves _en."""
    if L["lang"] == "en":
        return (meta.get("version_en"), meta.get("version_fecha_en"),
                meta.get("version_nota_en"))
    return meta.get("version"), meta.get("version_fecha"), meta.get("version_nota")


def insignia_version(meta):
    """Insignia de versión en la cabecera, con la nota como título emergente."""
    v, f, nota = datos_version(meta)
    if not v or not f:
        return ""
    a, m, d = (int(x) for x in f.split("-"))
    largo = L["fecha"].format(d=d, mes=L["meses"][m - 1], a=a)
    titulo = "{3} {0} · {1}{2}".format(
        v, largo, " · " + nota if nota else "", L["version"])
    return ('<span aria-label="{0}" class="version-badge" data-tip="{0}">'
            'v{1}<time datetime="{2}">{2}</time></span>').format(
        escapar_html(titulo), v, f)


DIACRITICOS = "āīūṃṇṭḍñṅḷĀĪŪṂṆṬḌÑṄḶ"


def marcar_diacriticos(t):
    """Envuelve cada letra con diacrítico para poder darle color."""
    return "".join(
        '<span class="dia">{0}</span>'.format(c) if c in DIACRITICOS else c
        for c in t)


def glosa_breve(s):
    """La primera línea de traducción, para la ayuda de las pastillas."""
    bloques = partir_bloques(s["cuerpo"])
    if len(bloques) < 2:
        return ""
    for l in bloques[1]:
        if l.strip():
            t = re.sub(r'\[\^\d+\]', '', l.strip())
            t = re.sub(r'\{([^|{}]+)\|[^{}]*\}', r'\1', t)
            return desescapar(t)
    return ""


def barra_capitulos(meta):
    """Navegación entre capítulos; enlaza sólo los que ya existen."""
    def buscar(titulo):
        for clave, m in CAPITULOS.items():
            if m["titulo_pali"] == titulo:
                destino = ruta_salida(m)
                return m, os.path.exists(destino)
        return None, False

    def boton(titulo, etiqueta, flecha, lado):
        if not titulo:
            cuerpo = ('<span><span class="chapter-nav-label">{0}</span>'
                      '{1}</span>').format(etiqueta, L["introduccion"])
            return '<button class="chapter-nav-btn disabled">{0}</button>'.format(
                flecha + cuerpo if lado == "izq" else cuerpo + flecha)
        m, existe = buscar(titulo)
        cuerpo = ('<span><span class="chapter-nav-label">{0}</span>{1}</span>'
                  ).format(etiqueta, escapar_html(titulo))
        interior = flecha + cuerpo if lado == "izq" else cuerpo + flecha
        if m and existe:
            return '<a class="chapter-nav-btn" href="../{0}/">{1}</a>'.format(
                m["slug"], interior)
        return '<button class="chapter-nav-btn disabled">{0}</button>'.format(interior)

    izq = ('<svg fill="none" stroke="currentColor" stroke-width="1.5" '
           'viewbox="0 0 20 20"><path d="M12 5l-5 5 5 5"></path></svg>')
    der = ('<svg fill="none" stroke="currentColor" stroke-width="1.5" '
           'viewbox="0 0 20 20"><path d="M8 5l5 5-5 5"></path></svg>')
    total = len(CAPITULOS)
    return (
        '<div class="chapter-nav">\n{0}\n'
        '<div class="chapter-nav-title"><strong>{1}</strong><br/>'
        '<span style="font-size:11px">{2}</span></div>\n{3}\n</div>\n'
    ).format(boton(meta.get("anterior"), L["cap_anterior"], izq, "izq"),
             escapar_html(meta["titulo_pali"]), L["capitulo_de"].format(n=meta["num"]),
             boton(meta.get("siguiente"), L["cap_siguiente"], der, "der"))


def version_pie(meta):
    v, f, nota = datos_version(meta)
    if not v or not f:
        return ""
    a, m, d = (int(x) for x in f.split("-"))
    largo = L["fecha"].format(d=d, mes=L["meses"][m - 1], a=a)
    nota = " " + nota if nota else ""
    return ('<p class="version-foot">{4} {0} — <time datetime="{1}">{2}'
            '</time>.{3}</p>').format(v, f, largo, escapar_html(nota), L["version"])


def rangos_kanda(suttas):
    """(primero, último) de cada kaṇḍa, para el TOC y la mini-navegación."""
    rangos = {}
    for s in suttas:
        a, b = rangos.get(s["kanda"], (s["n"], s["n"]))
        rangos[s["kanda"]] = (min(a, s["n"]), max(b, s["n"]))
    return rangos


def render_toc(suttas, meta):
    """TOC con grupos de kaṇḍa plegables y caja «ir a §…» / filtro."""
    rangos = rangos_kanda(suttas)
    partes = ['<p class="toc-title">{0}</p>'.format(meta["titulo_pali"])]
    partes.append(
        '<div class="toc-jump-wrap">'
        '<input aria-label="{0}" '
        'class="toc-jump" id="toc-jump" oninput="filterToc(this.value)" '
        'onkeydown="tocJumpKey(event)" placeholder="{1}" '
        'type="search"/></div>'.format(L["toc_aria"], L["toc_placeholder"]))
    kanda = None
    for s in suttas:
        if s["kanda"] != kanda:
            if kanda is not None:
                partes.append('</div></div>')
            kanda = s["kanda"]
            a, b = rangos[kanda]
            partes.append(
                '<div class="toc-group" id="tocg-{0}">'
                '<button class="toc-kanda toc-kanda-btn" '
                'onclick="toggleTocGroup({0})">'
                '<span class="toc-caret">▸</span><span>{1}</span>'
                '<span class="toc-kanda-range">§{2}–§{3}</span></button>'
                '<div class="toc-group-items">'.format(
                    kanda, kanda_pali(kanda), a, b))
        titulo = s["pali"]
        corto = titulo if len(titulo) <= 26 else titulo[:24].rstrip() + "…"
        partes.append(
            '<a class="toc-item" id="toc-s{0}" onclick="jumpTo(\'s{0}\')">§{0} {1}</a>'
            .format(s["n"], escapar_html(corto)))
    partes.append('</div></div>')
    return "".join(partes)


def render_kanda_nav(suttas):
    """Mini-navegación fija de los kaṇḍas del capítulo."""
    rangos = rangos_kanda(suttas)
    botones = []
    for k in sorted(rangos):
        a, b = rangos[k]
        botones.append(
            '<button aria-label="{1}" class="kanda-nav-btn" id="knav-{0}" '
            'onclick="jumpKanda({0})" data-tip="{1}">'
            '{2}</button>'.format(
                k,
                L["kanda_ir"].format(
                    es=kanda_es(k).lower(), pali=kanda_pali(k), a=a, b=b),
                kanda_pali(k).split("-")[0]))
    return ('<div class="kanda-nav" id="kanda-nav">'
            '<span class="kanda-nav-label">{1}</span>{0}'
            '<input aria-label="{2}" class="kanda-jump" '
            'id="kanda-jump" onkeydown="kandaJumpKey(event)" '
            'placeholder="§…" type="search"/></div>'
            .format("".join(botones), L["kanda_label"], L["kanda_aria"]))


def version_assets():
    """Huella de pali.css + pali.js para invalidar la caché al cambiarlos."""
    import hashlib
    h = hashlib.md5()
    for f in ("pali.css", "pali.js"):
        with open(os.path.join(RAIZ, "site", "assets", f), "rb") as fh:
            h.update(fh.read())
    return h.hexdigest()[:8]


def render(cap, meta, notas):
    suttas = cap["suttas"]
    total = len(suttas)
    nk = max(s["kanda"] for s in suttas)

    cuerpo = []
    if cap.get("versos"):
        cuerpo.append(render_intro(cap["versos"], notas))
    kanda = None
    for s in suttas:
        if s["kanda"] != kanda:
            if kanda is not None:
                cuerpo.append('</div>\n')
            kanda = s["kanda"]
            cuerpo.append('<div class="kanda-section">\n')
            cuerpo.append(
                '<div class="kanda-heading" id="kanda-{2}">{0}'
                '<span class="kanda-es">· {1}</span></div>\n'
                .format(kanda_pali(kanda), kanda_es(kanda), kanda))
        cuerpo.append(render_sutta(s, notas))
        if s.get("cierre"):
            cuerpo.append(cierre_kanda(s["cierre"]))
    cuerpo.append('</div>\n')

    es_en = L["lang"] == "en"
    obra_sub = L["obra_sub"] or meta["obra_sub"]
    titulo_es = meta.get("titulo_en", meta["titulo_es"]) if es_en else meta["titulo_es"]
    raiz = L["raiz"]
    # la otra lengua, sólo si su página existe
    otra = IDIOMAS["es" if es_en else "en"]
    otra_ruta = ruta_salida(meta, otra)
    alt_html = lang_btn = ""
    if os.path.exists(otra_ruta):
        alt_url = "/{0}{1}/{2}/".format(
            "" if es_en else "en/", meta["obra_slug"], meta["slug"])
        alt_html = ('<link href="{0}" hreflang="{1}" rel="alternate"/>'
                    .format(alt_url, otra["lang"]))
        lang_btn = ('<a aria-label="{2}" href="{0}" id="lang-btn" '
                    'onclick="try{{localStorage.setItem(\'pali_lang\',\'{1}\')}}'
                    'catch(e){{}};this.href=\'{0}\'+location.hash">{3}</a>'
                    .format(alt_url, otra["lang"], L["lang_btn_aria"], L["lang_btn"]))
        # La elección viaja con el lector (clave «pali_lang», la misma de la
        # portada y los recursos): si eligió la otra lengua, se le lleva a la
        # otra página, con su ancla. Pulsar el botón cambia la elección.
        lang_btn += ('<script>try{{if(localStorage.getItem(\'pali_lang\')===\'{1}\')'
                     'location.replace(\'{0}\'+location.hash)}}catch(e){{}}</script>'
                     .format(alt_url, otra["lang"]))
    return PLANTILLA.format(
        lang=L["lang"], raiz=raiz, alt=alt_html, lang_btn=lang_btn,
        volver=raiz + meta["obra_slug"] + "/" if es_en else "../",
        obra=meta["obra"], obra_sub=obra_sub,
        obra_display=marcar_diacriticos(escapar_html(meta["obra"])),
        insignia=insignia_version(meta),
        fin_capitulo=cierre_capitulo(),
        barra_capitulos=barra_capitulos(meta),
        copyright=COPYRIGHT_EN if es_en else COPYRIGHT,
        version_pie=version_pie(meta),
        primero=min(s["n"] for s in suttas), ultimo=max(s["n"] for s in suttas),
        version=datos_version(meta)[0] or "", version_fecha=datos_version(meta)[1] or "",
        titulo_pali=meta["titulo_pali"], titulo_es=titulo_es,
        total=total, nk=nk,
        nk_txt="{0} {1}".format(nk, L["secciones"][0] if nk == 1 else L["secciones"][1]),
        edicion=L["edicion"], buscar=L["buscar"], imprimir=L["imprimir"],
        expandir=L["expandir"], colapsar=L["colapsar"], reducir=L["reducir"],
        aumentar=L["aumentar"], estudiados=L["estudiados"],
        estudiados_t=L["estudiados_t"], pie_ayuda=L["pie_ayuda"],
        modo_oscuro=L["modo_oscuro"], modo_oscuro_t=L["modo_oscuro_t"],
        volver_inicio=L["volver_inicio"], toc_label=L["toc_label"],
        js_textos=json.dumps(L["js"], ensure_ascii=False),
        toc=render_toc(suttas, meta),
        kanda_nav=render_kanda_nav(suttas),
        assets_v=version_assets(),
        cuerpo="".join(cuerpo),
        done_key="{0}_{1}{2}_done".format(meta["obra_slug"], meta["slug"],
                                         "_en" if es_en else ""),
        cap_id="{0}-{1}{2}".format(meta["obra_slug"], meta["slug"],
                                  "-en" if es_en else ""),
        epub="{0}-{1}{2}.epub".format(meta["obra"].split("-")[0],
                                     meta["titulo_pali"], "-en" if es_en else ""),
    )


def ruta_salida(meta, idioma=None):
    """site/<obra>/<slug>/index.html, o site/en/<obra>/<slug>/ en inglés."""
    idioma = idioma or L
    partes = [RAIZ, "site"]
    if idioma["lang"] != "es":
        partes.append(idioma["lang"])
    partes += [meta["obra_slug"], meta["slug"], "index.html"]
    return os.path.join(*partes)


def cierre_capitulo():
    """El «Sandhi-kappo niṭṭhito» final, tomado literal del markdown."""
    if not FIN_CAPITULO:
        return ""
    partes = ['<div class="chapter-end">']
    if FIN_CAPITULO.get("pali"):
        partes.append('<div class="chapter-end-pali">{0}</div>'.format(
            escapar_html(desescapar(FIN_CAPITULO["pali"]))))
    if FIN_CAPITULO.get("es"):
        partes.append('<div class="chapter-end-es">{0}</div>'.format(
            escapar_html(desescapar(FIN_CAPITULO["es"]))))
    partes.append('</div>\n')
    return "".join(partes)


def cierre_kanda(c):
    """La fórmula viene literal del markdown; no se sintetiza."""
    partes = ['<div class="kanda-end">']
    if c.get("pali"):
        partes.append('<div class="kanda-end-pali">{0}</div>'.format(
            escapar_html(desescapar(c["pali"]))))
    if c.get("es"):
        partes.append('<div class="kanda-end-es">{0}</div>'.format(
            escapar_html(desescapar(c["es"]))))
    partes.append('</div>\n')
    return "".join(partes)


PLANTILLA = '''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<link href="{raiz}assets/favicon.svg" rel="icon" type="image/svg+xml"/>
{alt}
<title>{obra} · {titulo_pali}</title>
<meta content="{version}" name="version"/>
<meta content="{version_fecha}" name="version-date"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Gentium+Book+Plus:ital,wght@0,400;0,700;1,400;1,700&amp;family=Inter:wght@400;500;700&amp;family=JetBrains+Mono:wght@400;700&amp;display=swap" rel="stylesheet"/>
<link href="{raiz}assets/pali.css?v={assets_v}" rel="stylesheet"/>
</head>
<body>
<script>/* Tema guardado (clave compartida con /recursos/sandhi/), antes de pintar. */
try{{var _d=localStorage.getItem('pali_dark');
if(_d==='1'||(_d===null&&matchMedia('(prefers-color-scheme: dark)').matches))
document.body.classList.add('dark');}}catch(e){{}}</script>
<div id="pbar-wrap"><div id="pbar"></div></div>
<div id="pbadge"></div>
<button aria-label="{modo_oscuro}" id="dark-btn" onclick="toggleDark()" title="{modo_oscuro_t}">🌓</button>
{lang_btn}
<button aria-label="{volver_inicio}" id="top-btn" onclick="volverArriba()" title="{volver_inicio}">↑</button>
<nav aria-label="{toc_label}" id="toc">
{toc}
</nav>
<div id="main">
<div id="inner">
<div class="page-hdr">
<a class="idx-back" href="{volver}">← {obra}</a>
<div class="hdr-marca"><span class="marca-arbol"></span></div>
<div class="hdr-grammar">{obra_display}</div>
<div class="hdr-sub">{obra_sub}</div>
<div class="hdr-chapter">{titulo_pali} · {titulo_es}</div>
<div class="hdr-meta">{edicion} · {total} suttas · {nk_txt}{insignia}</div>
</div>
<div class="search-wrap">
<input class="search-input" id="search-box" oninput="doSearch(this.value)" placeholder="{buscar}" type="search"/>
<svg class="search-icon" fill="none" height="14" stroke="currentColor" stroke-width="1.5" viewbox="0 0 20 20" width="14"><circle cx="8" cy="8" r="5"></circle><path d="M13 13l4 4"></path></svg>
<div id="search-count"></div>
</div>
{barra_capitulos}
<div class="controls">
<button class="ctrl-btn" onclick="window.print()">{imprimir}</button>
<div class="ctrl-sep"></div>
<button class="ctrl-btn" onclick="expandAll()">{expandir}</button>
<button class="ctrl-btn" onclick="collapseAll()">{colapsar}</button>
<div class="ctrl-sep"></div>
<button class="ctrl-btn" onclick="changeFont(-1)" title="{reducir}">A−</button>
<span id="font-lbl">100%</span>
<button class="ctrl-btn" onclick="changeFont(1)" title="{aumentar}">A+</button>
<span class="done-count" id="done-count" title="{estudiados_t}">0 / {total} {estudiados}</span>
<button class="epub-btn" onclick="exportEpub()">EPUB</button>
</div>
{kanda_nav}{cuerpo}{fin_capitulo}
<div class="footer-box">
<div class="footer-box-main">
<strong>{obra}</strong> — {titulo_pali} · {total} suttas (§{primero}–§{ultimo}).
{pie_ayuda}
</div>
<div class="footer-box-copy">
<span class="marca-lockup"></span>
{copyright}
{version_pie}</div>
</div>
</div>
</div>
<script>
window.PALI_CAPITULO = {{
  id:            '{cap_id}',
  doneKey:       '{done_key}',
  obra:          '{obra}',
  obraSubtitulo: '{obra_sub}',
  capituloPali:  '{titulo_pali}',
  capituloEs:    '{titulo_es}',
  epubNombre:    '{epub}',
  idioma:        '{lang}',
  textos:        {js_textos}
}};
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
<script src="{raiz}assets/pali.js?v={assets_v}"></script>
</body>
</html>
'''


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    global L
    ruta = sys.argv[1]
    clave = os.path.splitext(os.path.basename(ruta))[0]
    if clave.endswith(".en"):
        clave, L = clave[:-3], IDIOMAS["en"]
    if clave not in CAPITULOS:
        print("No hay metadatos para '{0}'. Añádelos en CAPITULOS.".format(clave))
        return 1
    meta = CAPITULOS[clave]

    ruta_abs = ruta if os.path.isabs(ruta) else os.path.join(RAIZ, ruta)
    cargar_capitulos_publicados(clave, meta["obra_slug"])
    # primera pasada: saber qué suttas existen antes de enlazar referencias,
    # y armar el resumen (título — glosa) para el tooltip de cada §N
    SUTTAS_VALIDOS.update(
        int(m.group(1)) for m in
        (RE_SUTTA.match(l) for l in open(ruta_abs, encoding="utf-8"))
        if m)
    for s in parsear(ruta_abs)["suttas"]:
        glosa = glosa_breve(s)
        RESUMEN_SUTTAS[s["n"]] = (s["pali"] + (" — " + glosa if glosa else ""))
    cap = parsear(ruta_abs)
    html = render(cap, meta, cap["notas"])

    destino = ruta_salida(meta)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(html)

    print("{0} suttas · {1} kaṇḍa(s) · {2} notas → {3}".format(
        len(cap["suttas"]), max(s["kanda"] for s in cap["suttas"]),
        len(cap["notas"]), os.path.relpath(destino, RAIZ)))

    if NO_ENLAZADOS:
        vistos = sorted({(n, p) for n, p in NO_ENLAZADOS})
        print("\nReferencias §N dejadas sin enlazar "
              "(remiten a otra obra o a un sutta de otro capítulo):")
        for n, p in vistos:
            print("   §{0}  tras «…{1}»".format(n, p[-24:]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
