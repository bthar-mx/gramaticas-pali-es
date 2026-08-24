#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrae las raíces pāḷi y sánscritas de «Pali Roots in Saddanīti».

    python3 herramientas/extraer_raices.py ruta/al/dhatu.pdf

Escribe recursos/raices/raices.json.

Por qué hace falta un extractor propio
--------------------------------------
«Pali Roots in Saddanīti» (CMBT, 2005) se compuso con Quartz de Mac OS X
10.5, que incrustó 477 subconjuntos tipográficos distintos, cada uno con su
propia codificación y con el mapa ToUnicode roto. Sacar el texto con
pdftotext, PyMuPDF o cualquier lector normal devuelve basura: los códigos de
carácter se asignaron por orden de aparición, no por Unicode.

La reconstrucción no adivina nada. Descompone cada glifo incrustado a su
contorno, lo normaliza y lo identifica por la forma. En todo el libro hay
sólo 161 contornos distintos, identificados una vez a mano y recogidos en
GLIFOS; ese mapa se propaga a los 477 subconjuntos. Las celdas se recortan
con las propias líneas de la tabla del PDF, no por posición estimada.

Los diacríticos salen íntegros —ā ī ū ṃ ṅ ñ ṭ ḍ ṇ ḷ y los sánscritos
ṛ ṝ ś ṣ ḥ— porque se leen del contorno del glifo, no de un OCR.

Requiere pymupdf y fonttools.
"""

import collections
import hashlib
import io
import json
import os
import re
import sys
import unicodedata

try:
    import pymupdf
    from fontTools.ttLib import TTFont
    from fontTools.pens.recordingPen import DecomposingRecordingPen
except ImportError:
    sys.exit("Hacen falta pymupdf y fonttools:  pip3 install pymupdf fonttools")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, "recursos", "raices", "raices.json")

# Páginas del PDF (1-based en el archivo; aquí 0-based).
P_TABLA = range(69, 380)        # la tabla comparada
P_INDICE = range(381, 449)      # el índice de significados → raíz

# Los 161 contornos del libro, en orden de frecuencia, identificados a la
# vista una sola vez. El índice es la posición en ese orden; el valor, el
# carácter. Las variantes de estilo (cursiva, negrita) colapsan al mismo
# carácter a propósito: aquí sólo interesa el texto.
GLIFOS = list(
    " aierntosdglchu.pIIm;kāvfyb12R,=3zí495j)(76ṃSṇ0-8PMVṭīwṣñśáXūxAṛḍDóqEḥ’TḷCṅK‘BON"
    "LGéUHF–“”:•?WJY+a/ĀoiÍrṝúRÉÓtnZ—ṬṆaiízesfdelnc&#°*Mggof..ôĪ\"'[]QPlpSskrátü@©¿ÁýŚĂ"
)
assert len(GLIFOS) == 161, len(GLIFOS)

ROMANOS = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
           "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10}
REF = re.compile(r"\b(X|IX|VIII|VII|VI|V|IV|III|II|I)\s+([\d,\s]+)", re.I)

# El separador entre el inglés y el español se compone con dos «I».
SEP = " II "

ORDEN = ["a", "ā", "i", "ī", "u", "ū", "e", "o", "k", "kh", "g", "gh", "ṅ",
         "c", "ch", "j", "jh", "ñ", "ṭ", "ṭh", "ḍ", "ḍh", "ṇ", "t", "th",
         "d", "dh", "n", "p", "ph", "b", "bh", "m", "y", "r", "l", "ḷ",
         "v", "s", "h"]
DOBLES = sorted([x for x in ORDEN if len(x) > 1], key=len, reverse=True)
RANGO = {c: i for i, c in enumerate(ORDEN)}


# --------------------------------------------------------------------------
# 1. Identificación de glifos por contorno
# --------------------------------------------------------------------------

def tabla_de_glifos(doc):
    """{xref de la tipografía: {código: hash del contorno}} para todo el PDF."""
    fuera = {}
    for pno in range(len(doc)):
        for x in doc.get_page_fonts(pno):
            xref = x[0]
            if xref in fuera:
                continue
            try:
                datos = doc.extract_font(xref)[3]
                tt = TTFont(io.BytesIO(datos))
                glifos = tt.getGlyphSet()
                cmap = tt["cmap"].tables[0].cmap
            except Exception:
                fuera[xref] = {}
                continue
            m = {}
            for codigo, nombre in cmap.items():
                pluma = DecomposingRecordingPen(glifos)
                try:
                    glifos[nombre].draw(pluma)
                except Exception:
                    continue
                # Se redondean las coordenadas y se resuelven los glifos
                # compuestos: así el mismo signo hashea igual en los 477
                # subconjuntos.
                firma = repr([(op, tuple((round(p[0]), round(p[1])) if p else None
                                         for p in args))
                              for op, args in pluma.value])
                m[codigo] = hashlib.md5(firma.encode()).hexdigest()[:12]
            fuera[xref] = m
    return fuera


def mapa_caracteres(doc, glifos):
    """{hash de contorno: carácter}, ordenando los contornos por frecuencia."""
    cuenta = collections.Counter()
    for pno in range(len(doc)):
        fmap = {x[3].split("+")[-1]: x[0] for x in doc.get_page_fonts(pno)}
        for b in doc[pno].get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    t = glifos.get(fmap.get(s["font"].split("+")[-1]), {})
                    for ch in s["text"]:
                        h = t.get(ord(ch))
                        if h:
                            cuenta[h] += 1
    orden = [h for h, _ in cuenta.most_common()]
    if len(orden) != len(GLIFOS):
        print("  aviso — {0} contornos distintos, GLIFOS tiene {1}".format(
            len(orden), len(GLIFOS)))
    return {h: GLIFOS[i] for i, h in enumerate(orden) if i < len(GLIFOS)}


# --------------------------------------------------------------------------
# 2. Lectura de la página
# --------------------------------------------------------------------------

MARCA = "\x01"   # antepuesto a los dígitos en superíndice (llamadas de nota)


def caracteres(doc, glifos, mapa, pno):
    """[(bbox, carácter, cuerpo)] de la página, ya descifrada."""
    fmap = {x[3].split("+")[-1]: x[0] for x in doc.get_page_fonts(pno)}
    fuera = []
    for b in doc[pno].get_text("rawdict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                t = glifos.get(fmap.get(s["font"].split("+")[-1]), {})
                for c in s["chars"]:
                    ch = c["c"]
                    u = " " if ch == " " else mapa.get(t.get(ord(ch)), "�")
                    # Menos de 7 puntos y dígito: es llamada de nota.
                    if s["size"] < 7.0 and u.isdigit():
                        u = MARCA + u
                    fuera.append((c["bbox"], u, s["size"]))
    return fuera


def rejilla(doc, pno):
    """Las líneas de la tabla: (horizontales, verticales)."""
    hs, vs = set(), set()
    for x in doc[pno].get_drawings():
        r = x["rect"]
        if r.height < 2 and r.width > 50:
            hs.add(round(r.y0, 1))
        if r.width < 2 and r.height > 10:
            vs.add(round(r.x0, 1))

    def juntar(v):
        v, fuera = sorted(v), []
        for x in v:
            if fuera and x - fuera[-1] < 1.5:
                continue
            fuera.append(x)
        return fuera

    return juntar(hs), juntar(vs)


def lineas(cs):
    """Agrupa caracteres en líneas y les devuelve los espacios."""
    cs = sorted(cs, key=lambda c: (round(c[0][1] / 3), c[0][0]))
    grupos, actual, ultimo = [], [], None
    for c in cs:
        y = c[0][1]
        if ultimo is None or abs(y - ultimo) < 3:
            actual.append(c)
        else:
            grupos.append(actual)
            actual = [c]
        ultimo = y
    if actual:
        grupos.append(actual)
    fuera = []
    for g in grupos:
        g = sorted(g, key=lambda c: c[0][0])
        t, prev = "", None
        for bb, u, sz in g:
            if prev is not None and bb[0] - prev > sz * 0.28 \
               and t and not t.endswith(" ") and not u.startswith(MARCA):
                t += " "
            t += u
            prev = bb[2]
        fuera.append(t.strip())
    return fuera


# En las dos columnas de raíz el texto va con espaciado entre letras, así que
# los espacios se cierran. Salvo en una celda de todo el libro —la de «chu»,
# página 155— donde el autor puso una remisión en prosa en lugar de una raíz:
# «see che in Sad. divādi-gaṇa». Estas palabras inglesas no son raíces ni
# pāḷi ni sánscritas, de modo que sirven para reconocer la prosa sin tocar
# nada más.
PROSA = {"see", "in", "the", "and", "of", "not", "is", "are", "no", "cf"}


def es_prosa(ls):
    # Sólo cuentan las palabras sin diacríticos: «ṇis» no es «is». Y hacen
    # falta dos para no confundir una raíz suelta con una frase.
    palabras = {w.lower() for x in ls
                for w in re.findall(r"[^\W\d_]+", x, re.UNICODE) if w.isascii()}
    return len(palabras & PROSA) >= 2


def celda(ls, pegada=False):
    """Une las líneas de una celda. `pegada` para las columnas de raíz."""
    ls = [x for x in ls if x]
    if pegada and not es_prosa(ls):
        return " / ".join(x.replace(" ", "") for x in ls)
    # El original es una tabla de Word y Word no parte palabras al final de
    # línea: ninguna de las dos rayas que aparecen —«-» y «–»— es un guion
    # de corte. Son del texto, y segmentan los compuestos
    # («sadda-saṅghāṭesu», «hiṃsā-saṃkleśa–nayoḥ»). Así que se conservan tal
    # cual y la línea siguiente se pega sin espacio.
    fuera = ""
    for x in ls:
        if not fuera:
            fuera = x
        elif fuera.endswith(("-", "–")):
            fuera += x
        else:
            fuera += " " + x
    return fuera


def filas(doc, glifos, mapa, pno):
    """Las filas de la tabla comparada: seis celdas por fila."""
    hs, vs = rejilla(doc, pno)
    if len(vs) < 7 or len(hs) < 3:
        return []
    vs, cs, fuera = vs[:7], caracteres(doc, glifos, mapa, pno), []
    for i in range(len(hs) - 1):
        y0, y1 = hs[i], hs[i + 1]
        cel = []
        for j in range(6):
            x0, x1 = vs[j], vs[j + 1]
            sub = [c for c in cs
                   if x0 - 1 <= c[0][0] < x1 and y0 <= (c[0][1] + c[0][3]) / 2 <= y1]
            cel.append(celda(lineas(sub), pegada=j in (0, 3)))
        if any(cel):
            fuera.append(cel)
    return fuera


def notas(doc, glifos, mapa, pno):
    """{número: texto} de las notas al pie de la página."""
    hs, _ = rejilla(doc, pno)
    if not hs:
        return {}
    cs = caracteres(doc, glifos, mapa, pno)
    sub = [c for c in cs if c[0][1] > max(hs) - 2]
    fuera, ultima = {}, None
    for bruto in lineas(sub):
        if "Pali-Sanskrit Roots" in bruto or "Root Meanings" in bruto:
            continue
        t = bruto.replace(MARCA, "").strip()
        if not t:
            continue
        m = re.match(r"^(\d{1,3})\s+(.+)$", t)
        if m and bruto.startswith(MARCA):
            ultima = m.group(1)
            fuera[ultima] = m.group(2).strip()
        elif ultima:
            fuera[ultima] = (fuera[ultima] + " " + t).strip()
    return fuera


# --------------------------------------------------------------------------
# 3. Análisis del contenido de las celdas
# --------------------------------------------------------------------------

def refs(s):
    """«I 12, 210» → [{gana:1, pagina:12}, {gana:1, pagina:210}]."""
    fuera = []
    for g, pp in REF.findall(s or ""):
        for p in re.split(r",\s*", pp.strip()):
            if p.strip().isdigit():
                fuera.append({"gana": ROMANOS[g.upper()], "pagina": int(p.strip())})
    return fuera


def significado(m):
    """«gatyatthe = going II ir.» → (glosa pāḷi, inglés, español)."""
    m = (m or "").strip()
    if set(m) <= set(". "):   # «......» es «no hay», no un significado
        return "", "", ""
    en, es = m.split(SEP, 1) if SEP in m else (m, "")
    en, es = en.strip(), es.strip()
    glosa = ""
    mm = re.match(r"^(.*?)\s*=\s*(.*)$", en, re.S)
    if mm:
        glosa, en = mm.group(1).strip(), mm.group(2).strip()
    return glosa, en, es


def raices_de(celda_txt):
    """Los lemas de una celda de raíz. «......» significa que no hay ninguna;
    una celda en prosa es una remisión del autor, no un lema."""
    if not celda_txt or set(celda_txt.strip()) <= set("."):
        return []
    if es_prosa([celda_txt]):
        return []
    return [r for r in (x.strip() for x in celda_txt.split("/"))
            if r and not set(r) <= set(".")]


def unidades(w):
    # El autor encierra entre corchetes la raíz que da por no atestiguada
    # («[jha]»); para ordenar y agrupar cuenta la letra, no el corchete.
    w = re.sub(r"[\[\]()’'-]", "", w or "")
    w, fuera, i = unicodedata.normalize("NFC", w.lower()), [], 0
    while i < len(w):
        for m in DOBLES:
            if w.startswith(m, i):
                fuera.append(m)
                i += len(m)
                break
        else:
            fuera.append(w[i])
            i += 1
    return fuera


def clave(w):
    return [RANGO.get(u, 99) for u in unidades(w)]


def inicial(w):
    u = unidades(w)
    return u[0] if u else "?"


# --------------------------------------------------------------------------
# 4. Las dos secciones
# --------------------------------------------------------------------------

def tabla_comparada(doc, glifos, mapa):
    todas = {p: notas(doc, glifos, mapa, p) for p in P_TABLA}
    fuera, n = [], 0
    for pno in P_TABLA:
        fs = filas(doc, glifos, mapa, pno)
        if not fs:
            continue
        # Una llamada puede quedar en una página y su nota en la contigua.
        pie = dict(todas.get(pno) or {})
        for vecina in (pno + 1, pno - 1):
            for k, v in (todas.get(vecina) or {}).items():
                pie.setdefault(k, v)
        for c in fs:
            if c[0].startswith("PaliRoot") or not c[0]:
                continue
            recogidas = []

            def limpiar(s):
                def rep(m):
                    num = m.group(0).replace(MARCA, "")
                    if num in pie:
                        recogidas.append({"n": int(num), "texto": pie[num]})
                    return ""
                return re.sub(r"(?:\x01\d)+", rep, s or "")

            c = [limpiar(x) for x in c]
            glosa, en, es = significado(c[1])
            n += 1
            rr = raices_de(c[0])
            skt = raices_de(c[3])
            # Celda sánscrita en prosa: es una remisión del autor.
            remite = re.sub(r"\s+", " ", c[3].replace("– ", "–")).strip() \
                if (c[3].strip() and not skt
                    and not set(c[3].strip()) <= set(".")) else ""
            fuera.append({
                "id": n,
                "raices": rr,
                "glosa": glosa,
                "en": en,
                "es": es,
                "refs": refs(c[2]),
                "ref": (c[2] or "").strip(),
                "sanscrito": skt,
                "sanscrito_glosa": (c[4] or "").strip(),
                "sanscrito_refs": refs(c[5]),
                "sanscrito_ref": (c[5] or "").strip(),
                "remite": remite,
                "notas": recogidas,
                "pagina": pno + 1,
                "letra": inicial(rr[0]) if rr else "?",
            })
    fuera.sort(key=lambda x: (clave(x["raices"][0]) if x["raices"] else [99], x["id"]))
    return fuera


RX_RAIZ = re.compile(
    r"([a-zāīūṛśṣḥṃṅñṭḍṇḷ’'-]+)\s+"
    r"((?:x|ix|viii|vii|vi|v|iv|iii|ii|i)\s+\d+(?:\s*,\s*\d+)*)", re.I)


def indice_significados(doc, glifos, mapa):
    fuera = []
    for pno in P_INDICE:
        hs, vs = rejilla(doc, pno)
        if len(vs) < 3 or len(hs) < 2:
            continue
        cs = caracteres(doc, glifos, mapa, pno)
        for i in range(len(hs) - 1):
            y0, y1 = hs[i], hs[i + 1]
            cel = []
            for j in range(2):
                x0, x1 = vs[j], vs[j + 1]
                sub = [c for c in cs
                       if x0 - 1 <= c[0][0] < x1 and y0 <= (c[0][1] + c[0][3]) / 2 <= y1]
                cel.append(celda(lineas(sub)))
            if not cel[0] or "Root Meaning" in cel[0]:
                continue
            glosa, en, es = significado(cel[0])
            rr = [{"raiz": m.group(1),
                   "refs": refs(m.group(2)),
                   "ref": m.group(2).strip()}
                  for m in RX_RAIZ.finditer(cel[1].replace(MARCA, ""))]
            fuera.append({"glosa": glosa, "en": en, "es": es,
                          "raices": rr, "pagina": pno + 1,
                          "letra": inicial(glosa)})
    return fuera


# --------------------------------------------------------------------------

CABECERA = {
    "_nota": "Raíces pāḷi comparadas con las sánscritas. Transcrito de «Pali "
             "Roots in Saddanīti», del Venerable U Sīlānanda, edición de "
             "Bhikkhu Nandisena, CMBT 2005. El PDF no tiene capa de texto "
             "utilizable: "
             "la transcripción se reconstruyó carácter a carácter desde los "
             "contornos de las tipografías incrustadas "
             "(herramientas/extraer_raices.py). El texto es literal; nada se "
             "ha corregido ni completado.",
    "fuente": {
        "titulo": "Pali Roots in Saddanīti",
        "subtitulo": "Pali Roots in Saddanīti Dhātu-Mālā Compared with "
                     "Pāṇinīya-Dhātupāṭha",
        "autor": "Venerable U Sīlānanda",
        "editor": "Bhikkhu Nandisena",
        "editorial": "Centro Mexicano del Buddhismo Theravada (CMBT)",
        "anyo": 2005,
        "copyright": "© 2001 U Sīlānanda",
        "enlace": "https://drive.google.com/open?id=16neD1t6MKCsHNkf0zbi0zdG6nt7IamQl",
        "paginas_pdf": "70-380 (tabla comparada), 382-449 (índice de significados)",
    },
    # Los ocho gaṇas pāḷi son los del Saddanīti-dhātumālā, y el signo de
    # conjugación (vikaraṇa) de cada uno es el que da la «Guía de las raíces
    # pali» del libro, página 45 de la edición (52 del PDF),
    # con sus observaciones. Los totales son los del libro, que advierte
    # que son aproximados. Los diez grupos sánscritos son los del
    # Pāṇinīya-dhātupāṭha.
    "ganas": {
        "pali": {
            "1": {"nombre": "bhūvādigaṇa", "signo": "a", "total": 1110},
            "2": {"nombre": "rudhādigaṇa", "signo": "ṃ-a", "total": 18,
                  "nota": "«ṃ» se inserta después de la primera sílaba de la raíz"},
            "3": {"nombre": "divādigaṇa", "signo": "ya", "total": 104},
            "4": {"nombre": "svādigaṇa", "signo": "ṇu, ṇā, uṇā", "total": 30,
                  "nota": "«ṇ» no es una letra que indica fortalecimiento de la "
                          "vocal de la primera sílaba"},
            "5": {"nombre": "kiyādigaṇa", "signo": "nā", "total": 32},
            "6": {"nombre": "gahādigaṇa", "signo": "ppa, ṇhā", "total": 10},
            "7": {"nombre": "tanādigaṇa", "signo": "o, yira", "total": 14},
            "8": {"nombre": "curādigaṇa", "signo": "ṇe, ṇaya", "total": 399,
                  "nota": "«ṇ» indica fortalecimiento de la vocal de la primera "
                          "sílaba si ésta no es larga o si no está seguida por "
                          "dos consonantes"},
        },
        "sanscrito": {
            "1": {"nombre": "bhvādi", "signo": "a (śap)"},
            "2": {"nombre": "adādi", "signo": "sin signo (luk)"},
            "3": {"nombre": "juhotyādi", "signo": "reduplicación (ślu)"},
            "4": {"nombre": "divādi", "signo": "ya (śyan)"},
            "5": {"nombre": "svādi", "signo": "nu (śnu)"},
            "6": {"nombre": "tudādi", "signo": "a (śa)"},
            "7": {"nombre": "rudhādi", "signo": "na infijo (śnam)"},
            "8": {"nombre": "tanādi", "signo": "u"},
            "9": {"nombre": "kryādi", "signo": "nā (śnā)"},
            "10": {"nombre": "curādi", "signo": "aya (ṇic)"},
        },
    },
    # Qué es cada número, según la propia leyenda del libro (página 46 de
    # la edición): en pāḷi, grupo y número de PÁGINA; en sánscrito, grupo y
    # número de RAÍZ. No son la misma cosa.
    "obras": {
        "pali": {"sigla": "SD", "nombre": "Saddanīti-dhātumālā",
                 "cifra": "página"},
        "sanscrito": {"sigla": "PD", "nombre": "Pāṇinīya-dhātupāṭha",
                      "cifra": "raíz nº"},
    },
}


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__.strip().splitlines()[2].strip())
    pdf = sys.argv[1]
    doc = pymupdf.open(pdf)
    print("leyendo los contornos de {0} tipografías…".format(
        len({x[0] for p in range(len(doc)) for x in doc.get_page_fonts(p)})))
    glifos = tabla_de_glifos(doc)
    mapa = mapa_caracteres(doc, glifos)

    raices = tabla_comparada(doc, glifos, mapa)
    significados = indice_significados(doc, glifos, mapa)

    sin_leer = sum(json.dumps(x, ensure_ascii=False).count("�")
                   for x in raices + significados)
    if sin_leer:
        print("  aviso — {0} caracteres sin identificar".format(sin_leer))

    datos = dict(CABECERA)
    datos["raices"] = raices
    datos["significados"] = significados
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    json.dump(datos, open(DESTINO, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    con_skt = sum(1 for x in raices if x["sanscrito"])
    notas_n = sum(len(x["notas"]) for x in raices)
    print("{0} raíces · {1} con cognado sánscrito · {2} notas · "
          "{3} significados → {4}".format(
              len(raices), con_skt, notas_n, len(significados),
              os.path.relpath(DESTINO, RAIZ)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
