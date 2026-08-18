#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el HTML de un capítulo a partir de su markdown.

    python3 herramientas/generar_capitulo.py kaccayana/01-sandhi-kappa.md

La fuente es el markdown; el HTML es salida y no debe editarse a mano.
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
        "anterior": None,
        "siguiente": "2-Nāma-Kappa",
        "version": "1.3",
        "version_fecha": "2026-08-15",
        "version_nota": "Mejoras de diseño compartidas de las sesiones 08–09: "
                        "TOC plegable con caja «ir a §…», navegación fija de "
                        "kaṇḍas, tooltips en las referencias §N, botón «↑», "
                        "caché de estilos con huella y contraste del acento "
                        "en modo oscuro.",
    },
    "02-nama-kappa": {
        "slug": "nama",
        "obra": "Kaccāyana-Byākaraṇaṃ",
        "obra_sub": "Gramática de Kaccāyana",
        "obra_slug": "kaccayana",
        "num": 2,
        "titulo_pali": "2-Nāma-Kappa",
        "titulo_es": "2-Capítulo del Nombre",
        "anterior": "1-Sandhi-Kappa",
        "siguiente": "3-Kāraka-Kappa",
        "version": "1.1",
        "version_fecha": "2026-08-15",
        "version_nota": "Revisión de la sesión 09: «inflexión» en lugar de "
                        "«inflexión nominal»; §237 cita §174 para ta → sa; "
                        "separador de §77 y comilla de §83 en el maestro; "
                        "sub-listas de ejemplos anidadas.",
    },
    "03-karaka-kappa": {
        "slug": "karaka",
        "obra": "Kaccāyana-Byākaraṇaṃ",
        "obra_sub": "Gramática de Kaccāyana",
        "obra_slug": "kaccayana",
        "num": 3,
        "titulo_pali": "3-Kāraka-Kappa",
        "titulo_es": "3-Capítulo de casos gramaticales",
        "anterior": "2-Nāma-Kappa",
        "siguiente": "4-Samāsa-Kappa",     # en preparación: botón inactivo
        "version": "1.0",
        "version_fecha": "2026-08-17",
        "version_nota": "Primera publicación del Kāraka-Kappa (§271–§315, "
                        "45 suttas, 55 notas): los ocho nombres kāraka se "
                        "traducen en la prosa (ablativo, dativo, locativo, "
                        "instrumental, objeto, sujeto, causa, posesivo).",
    },
}

COPYRIGHT = (
    "Edición del texto en pāḷi y traducción al español por Bhikkhu Nandisena. "
    "Este material puede ser reproducido para uso personal y distribuido de "
    "forma gratuita. Copyright © 2026 Instituto de Estudios Buddhistas "
    "Hispano (IEBH). Publicado bajo licencia "
    '<a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es" '
    'rel="license">CC BY-NC-SA 4.0</a> · DOI '
    '<a href="https://doi.org/10.5281/zenodo.21948011">'
    "10.5281/zenodo.21948011</a>."
)

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
    return KANDAS_ES[indice_kanda(k)]


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


def inline(t, notas):
    """Cadena de transformaciones para texto corrido."""
    t = escapar_html(desescapar(t))
    t = enfasis(t)
    t = glosas_emergentes(t)
    t = marcar_notas(t, notas)
    t = enlazar_suttas(t)
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
RE_FIN_ES = re.compile(r'^\*\*(Fin del capítulo.+?)\.?\*\*$')
RE_CIERRE_ES = re.compile(r'^\*\*(Así termina la .+?)\.?\*\*$')


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
        me = re.match(r'^(Secuencia|Ejemplos?[^:]*|Contraejemplos?[^:]*):\s*$', t)
        if me:
            volcar_buf()
            ejemplos[0] = me.group(1).startswith(("Ejemplo", "Contraejemplo"))
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
            '        Mostrar más (formación, etc.)\n      </button>\n'
            '<div class="collapsible-content" id="{0}seq">'
            '<div class="rest-content">{1}</div></div>\n'
        ).format(sid, cuerpo)

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
            '        Ver notas ({1})\n      </button>\n'
            '<div class="collapsible-content" id="{0}fn">'
            '<div class="fn-block">{2}</div></div>\n'
        ).format(sid, len(usadas), items)

    desglose_html = ""
    if s["desglose"]:
        voces = "{0} {1}".format(s["voces"], "voz" if s["voces"] == 1 else "voces")
        desglose_html = '<div class="sutta-breakdown">[{0} = {1}]</div>'.format(
            escapar_html(s["desglose"]), voces)

    ref = ('<span class="sutta-ref">'
           '<span class="ref-tip"><span class="ref-tip-term">{0}</span>'
           '<span class="ref-tip-box">Kaccāyana Sutta</span></span>. '
           '<span class="ref-tip"><span class="ref-tip-term">{1}</span>'
           '<span class="ref-tip-box">Rūpasiddhi Sutta{2}</span></span>.</span>'
           ).format(n, s["rup"], "s" if "," in s["rup"] else "")

    sadd_html = ""
    if s["sadd"]:
        sadd_html = (' <span class="sutta-ref-num"><span class="ref-tip">'
                     '<span class="ref-tip-term">({0})</span>'
                     '<span class="ref-tip-box">Saddanīti-Suttamālā Sutta</span>'
                     '</span></span>').format(", ".join(s["sadd"]))
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
        '<div class="sutta-footer">\n'
        '<span class="done-wrap" onclick="toggleDone(\'{sid}\')" title="Marcar como estudiado">\n'
        '<span class="done-cb" id="cb-{sid}"></span>\n'
        '<span class="done-label">Estudiado</span>\n</span>\n'
        '<button class="share-btn" onclick="shareSutta(\'{sid}\')" title="Copiar enlace a este sutta">\n'
        '<svg fill="none" stroke="currentColor" stroke-width="1.5" viewbox="0 0 20 20">'
        '<circle cx="15" cy="5" r="2"></circle><circle cx="5" cy="10" r="2"></circle>'
        '<circle cx="15" cy="15" r="2"></circle><path d="M7 11l6 3M7 9l6-3"></path></svg>\n'
        '          Enlace\n        </button>\n'
        '<button class="copy-btn" onclick="copySutta(\'{sid}\')" title="Copiar sutta al portapapeles">Copiar §</button>\n'
        '<button class="back-top-btn" onclick="volverArriba()" title="Volver al inicio">\n'
        '<svg fill="none" stroke="currentColor" stroke-width="1.5" viewbox="0 0 20 20">'
        '<path d="M10 15V5M5 10l5-5 5 5"></path></svg>\n'
        '          Inicio ↑\n        </button>\n'
        '</div>\n</div>\n</div>\n'
    ).format(sid=sid, ref=ref, sadd=sadd_html,
             pali=marcar_notas(escapar_html(s["pali_notas"]), notas),
             desglose=desglose_html, palib=pali_html, gloss=gloss_html,
             vutti=vutti_html, resto=resto_html, notas=notas_html)


PIE_TARJETA = (
    '<div class="sutta-footer">\n'
    '<span class="done-wrap" onclick="toggleDone(\'{sid}\')" title="Marcar como estudiado">\n'
    '<span class="done-cb" id="cb-{sid}"></span>\n'
    '<span class="done-label">Estudiado</span>\n</span>\n'
    '<button class="share-btn" onclick="shareSutta(\'{sid}\')" title="Copiar enlace a este sutta">\n'
    '<svg fill="none" stroke="currentColor" stroke-width="1.5" viewbox="0 0 20 20">'
    '<circle cx="15" cy="5" r="2"></circle><circle cx="5" cy="10" r="2"></circle>'
    '<circle cx="15" cy="15" r="2"></circle><path d="M7 11l6 3M7 9l6-3"></path></svg>\n'
    '          Enlace\n        </button>\n'
    '<button class="copy-btn" onclick="copySutta(\'{sid}\')" title="Copiar sutta al portapapeles">Copiar §</button>\n'
    '<button class="back-top-btn" onclick="volverArriba()" title="Volver al inicio">\n'
    '<svg fill="none" stroke="currentColor" stroke-width="1.5" viewbox="0 0 20 20">'
    '<path d="M10 15V5M5 10l5-5 5 5"></path></svg>\n'
    '          Inicio ↑\n        </button>\n'
    '</div>\n')


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
        '<span class="sutta-pali-title">Versos introductorios</span></div></div>'
        '<svg class="chevron" fill="none" stroke="currentColor" stroke-width="1.5" '
        'viewbox="0 0 20 20"><path d="M5 7.5l5 5 5-5"></path></svg></div>'
        '<div class="sutta-body"><div class="intro-block">{0}</div>\n{1}</div>\n</div>\n'
    ).format("".join(bloques), PIE_TARJETA.format(sid="intro"))


MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def insignia_version(meta):
    """Insignia de versión en la cabecera, con la nota como título emergente."""
    v, f = meta.get("version"), meta.get("version_fecha")
    if not v or not f:
        return ""
    a, m, d = (int(x) for x in f.split("-"))
    largo = "{0} de {1} de {2}".format(d, MESES[m - 1], a)
    titulo = "Versión {0} · {1}{2}".format(
        v, largo, " · " + meta["version_nota"] if meta.get("version_nota") else "")
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
                destino = os.path.join(RAIZ, "site", m["obra_slug"], m["slug"],
                                       "index.html")
                return m, os.path.exists(destino)
        return None, False

    def boton(titulo, etiqueta, flecha, lado):
        if not titulo:
            cuerpo = ('<span><span class="chapter-nav-label">{0}</span>'
                      'Introducción</span>').format(etiqueta)
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
        '<span style="font-size:11px">Capítulo {2} de 8</span></div>\n{3}\n</div>\n'
    ).format(boton(meta.get("anterior"), "Capítulo anterior", izq, "izq"),
             escapar_html(meta["titulo_pali"]), meta["num"],
             boton(meta.get("siguiente"), "Capítulo siguiente", der, "der"))


def version_pie(meta):
    v, f = meta.get("version"), meta.get("version_fecha")
    if not v or not f:
        return ""
    a, m, d = (int(x) for x in f.split("-"))
    largo = "{0} de {1} de {2}".format(d, MESES[m - 1], a)
    nota = " " + meta["version_nota"] if meta.get("version_nota") else ""
    return ('<p class="version-foot">Versión {0} — <time datetime="{1}">{2}'
            '</time>.{3}</p>').format(v, f, largo, escapar_html(nota))


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
        '<input aria-label="Ir a un sutta o filtrar por título" '
        'class="toc-jump" id="toc-jump" oninput="filterToc(this.value)" '
        'onkeydown="tocJumpKey(event)" placeholder="Ir a §… / filtrar" '
        'type="search"/></div>')
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
                "Ir a la {0} ({1}, §{2}–§{3})".format(
                    kanda_es(k).lower(), kanda_pali(k), a, b),
                kanda_pali(k).split("-")[0]))
    return ('<div class="kanda-nav" id="kanda-nav">'
            '<span class="kanda-nav-label">Kaṇḍa:</span>{0}'
            '<input aria-label="Ir al sutta número…" class="kanda-jump" '
            'id="kanda-jump" onkeydown="kandaJumpKey(event)" '
            'placeholder="§…" type="search"/></div>'
            .format("".join(botones)))


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

    return PLANTILLA.format(
        obra=meta["obra"], obra_sub=meta["obra_sub"],
        obra_display=marcar_diacriticos(escapar_html(meta["obra"])),
        insignia=insignia_version(meta),
        fin_capitulo=cierre_capitulo(),
        barra_capitulos=barra_capitulos(meta),
        copyright=COPYRIGHT,
        version_pie=version_pie(meta),
        primero=min(s["n"] for s in suttas), ultimo=max(s["n"] for s in suttas),
        version=meta.get("version", ""), version_fecha=meta.get("version_fecha", ""),
        titulo_pali=meta["titulo_pali"], titulo_es=meta["titulo_es"],
        total=total, nk=nk,
        nk_txt="{0} {1}".format(nk, "sección" if nk == 1 else "secciones"),
        toc=render_toc(suttas, meta),
        kanda_nav=render_kanda_nav(suttas),
        assets_v=version_assets(),
        cuerpo="".join(cuerpo),
        done_key="{0}_{1}_done".format(meta["obra_slug"], meta["slug"]),
        cap_id="{0}-{1}".format(meta["obra_slug"], meta["slug"]),
        epub="{0}-{1}.epub".format(meta["obra"].split("-")[0], meta["titulo_pali"]),
    )


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
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<link href="../../assets/favicon.svg" rel="icon" type="image/svg+xml"/>
<title>{obra} · {titulo_pali}</title>
<meta content="{version}" name="version"/>
<meta content="{version_fecha}" name="version-date"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Gentium+Book+Plus:wght@400;700&amp;family=Noto+Serif:ital,wght@0,400;0,500;0,700;1,400;1,500;1,700&amp;family=Inter:wght@400;500;700&amp;family=JetBrains+Mono:wght@400;700&amp;display=swap" rel="stylesheet"/>
<link href="../../assets/pali.css?v={assets_v}" rel="stylesheet"/>
</head>
<body>
<script>/* Tema guardado (clave compartida con /recursos/sandhi/), antes de pintar. */
try{{var _d=localStorage.getItem('pali_dark');
if(_d==='1'||(_d===null&&matchMedia('(prefers-color-scheme: dark)').matches))
document.body.classList.add('dark');}}catch(e){{}}</script>
<div id="pbar-wrap"><div id="pbar"></div></div>
<div id="pbadge"></div>
<button aria-label="Alternar modo oscuro" id="dark-btn" onclick="toggleDark()" title="Modo oscuro/claro">🌓</button>
<button aria-label="Volver al inicio" id="top-btn" onclick="volverArriba()" title="Volver al inicio">↑</button>
<nav aria-label="Tabla de contenidos" id="toc">
{toc}
</nav>
<div id="main">
<div id="inner">
<div class="page-hdr">
<a class="idx-back" href="../">← {obra}</a>
<div class="hdr-grammar">{obra_display}</div>
<div class="hdr-sub">{obra_sub}</div>
<div class="hdr-chapter">{titulo_pali} · {titulo_es}</div>
<div class="hdr-meta">Edición bilingüe Pāḷi–Español · {total} suttas · {nk_txt}{insignia}</div>
</div>
<div class="search-wrap">
<input class="search-input" id="search-box" oninput="doSearch(this.value)" placeholder="Buscar sutta (pāḷi o español)…" type="search"/>
<svg class="search-icon" fill="none" height="14" stroke="currentColor" stroke-width="1.5" viewbox="0 0 20 20" width="14"><circle cx="8" cy="8" r="5"></circle><path d="M13 13l4 4"></path></svg>
<div id="search-count"></div>
</div>
{barra_capitulos}
<div class="controls">
<button class="ctrl-btn" onclick="window.print()">Imprimir / PDF</button>
<div class="ctrl-sep"></div>
<button class="ctrl-btn" onclick="expandAll()">Expandir todo</button>
<button class="ctrl-btn" onclick="collapseAll()">Colapsar todo</button>
<div class="ctrl-sep"></div>
<button class="ctrl-btn" onclick="changeFont(-1)" title="Reducir texto">A−</button>
<span id="font-lbl">100%</span>
<button class="ctrl-btn" onclick="changeFont(1)" title="Aumentar texto">A+</button>
<span class="done-count" id="done-count" title="Suttas estudiados">0 / {total} estudiados</span>
<button class="epub-btn" onclick="exportEpub()">EPUB</button>
</div>
{kanda_nav}{cuerpo}{fin_capitulo}
<div class="footer-box">
<div class="footer-box-main">
<strong>{obra}</strong> — {titulo_pali} · {total} suttas (§{primero}–§{ultimo}).
Pasa el cursor sobre los términos pāḷi o los superíndices numéricos para ver
su significado. Expande «Ver notas» para leer las notas completas.
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
  epubNombre:    '{epub}'
}};
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
<script src="../../assets/pali.js?v={assets_v}"></script>
</body>
</html>
'''


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    ruta = sys.argv[1]
    clave = os.path.splitext(os.path.basename(ruta))[0]
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

    destino = os.path.join(RAIZ, "site", meta["obra_slug"], meta["slug"], "index.html")
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
