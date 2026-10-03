# -*- coding: utf-8 -*-
"""
Glosario de los globos (tooltips) que comparten /recursos/clasificacion/ y
/recursos/analisis/.

    recursos/terminos/terminos.json   término, formas que se buscan en el
                                      texto, definición ES/EN, ejemplo (§ y
                                      capítulo), fuente y marca «revisar»

Desde la v0.2 del JSON: «grupo» («obra» o «capitulo») permite una entrada
sin ejemplo, y «no_en» lista los § donde la forma es palabra del propio sutta
y la página no debe glosarla.

cargar(raiz) devuelve la lista con cada ejemplo completado con el texto pāḷi
del sutta y la primera línea de su traducción publicada (kaccayana/0N-*.md y
0N-*.en.md), para no redactar glosas nuevas. Si un § no existe, o una forma
está repetida en dos términos, lanza ValueError: el generador no publica.
"""

import json
import os
import unicodedata

from generar_clasificacion import leer_md

GRUPOS = {"obra", "capitulo"}

MD = {"sandhi": "01-sandhi-kappa", "nama": "02-nama-kappa", "karaka": "03-karaka-kappa",
      "samasa": "04-samasa-kappa", "taddhita": "05-taddhita-kappa"}


def cargar(raiz):
    d = json.load(open(os.path.join(raiz, "recursos", "terminos", "terminos.json"), encoding="utf-8"))
    textos, vistas, fallos = {}, {}, []
    for t in d["terminos"]:
        grupo = t.get("grupo")
        if grupo and grupo not in GRUPOS:
            fallos.append("{0}: grupo desconocido «{1}»".format(t["clave"], grupo))
        if not all(isinstance(n, int) for n in t.get("no_en", [])):
            fallos.append("{0}: «no_en» debe ser una lista de §".format(t["clave"]))
        e = t.get("ejemplo")
        if e is None:
            # Las obras citadas y los capítulos sin publicar no llevan ejemplo:
            # el globo da sólo la descripción. Cualquier otra entrada, sí.
            if not grupo:
                fallos.append("{0}: falta el ejemplo".format(t["clave"]))
        md = MD.get(e["cap"]) if e else None
        if e and not md:
            fallos.append("{0}: capítulo desconocido «{1}»".format(t["clave"], e["cap"]))
        if md:
            for lengua, suf in (("es", ".md"), ("en", ".en.md")):
                k = md + suf
                if k not in textos:
                    textos[k] = leer_md(os.path.join(raiz, "kaccayana", k))[0]
                s = textos[k].get(e["n"])
                if not s:
                    fallos.append("{0}: §{1} no está en {2}".format(t["clave"], e["n"], k))
                    continue
                e["sutta"] = s["sutta"]
                e.setdefault("tr", {})[lengua] = s["tr"]
        for f in t["formas"]:
            if f in vistas:
                fallos.append("forma «{0}» repetida en {1} y {2}".format(f, vistas[f], t["clave"]))
            vistas[f] = t["clave"]
        for x in (t["def"]["es"], t["def"]["en"]):
            if unicodedata.normalize("NFC", x) != x:
                fallos.append("{0}: texto que no está en NFC".format(t["clave"]))
    if fallos:
        raise ValueError("; ".join(fallos[:10]))
    return d["terminos"]


# ---------------------------------------------------------------------------
# Términos técnicos sin entrada (aviso de generar_todo.py, 2026-10-03)
#
# Las páginas no marcan los términos técnicos: el globo sale buscando las
# formas del glosario en el texto. Esta comprobación hace lo mismo al revés:
# recorre el texto explicativo de las dos páginas (operación, notas, fuentes,
# leyenda, introducción; nunca el texto pāḷi del sutta ni los ejemplos), quita
# lo que va entre comillas —son palabras citadas—, y se queda con las palabras
# pāḷi: las que llevan diacríticos y unas pocas sin ellos (SIN_DIACRITICOS).
# Lo que no cubre ninguna forma del glosario ni está en «no_terminos» de
# terminos.json (palabras ya revisadas que no son terminología) sale como
# aviso. No impide publicar.

import re as _re

_DIAC = set("āīūṃṅñṭḍṇḷĀĪŪṂṄÑṬḌṆḶ")
SIN_DIACRITICOS = {"sutta", "suttas", "vidhi", "sandhi", "ca", "kvaci", "kappa",
                   "vutti", "vagga", "sara", "lopa", "rassa", "liṅga", "kamma",
                   "hetu", "digu", "dvanda", "tappurisa", "kita", "nimitta",
                   "niyama", "atidesa", "pakati", "paccaya", "vibhatti",
                   "visesana", "anuvatti", "visaya", "pariccheda", "taddhita",
                   # nombres de obras y autores sin diacríticos (grupo «obra»)
                   "thitzana", "nandisena"}
# Títulos de obras sin diacríticos: se reconocen por la terminación
# (Payogasiddhi, Kaccāyanavutti, Ekakkharakosa, Mukhamattasāra…).
_OBRA = _re.compile(r"(siddhi|vutti|kosa|sāra|sara|ṭīkā|tika|vaṇṇanā|dīpanī|nīti|niti|avatāra)$")
_PAL = _re.compile(r"[A-Za-zāīūṃṅñṭḍṇḷĀĪŪṂṄÑṬḌṆḶ’']+(?:-[A-Za-zāīūṃṅñṭḍṇḷĀĪŪṂṄÑṬḌṆḶ]+)*")
_CITA = _re.compile(r"«[^»]*»|“[^”]*”|‘[^’]*’|\"[^\"]*\"")


def _textos(raiz):
    """(página, dónde, texto) del texto explicativo de las dos páginas."""
    J = lambda *p: json.load(open(os.path.join(raiz, *p), encoding="utf-8"))
    c = J("recursos", "clasificacion", "datos.json")
    for k in ("tipos", "vidhis"):
        for v in c[k].values():
            for l in ("es", "en"):
                yield "clasificación", k, v[l]
    for l in ("es", "en"):
        yield "clasificación", "nota_version", c["nota_version"][l]
    for n, s in c["suttas"].items():
        for f in ("op", "nota"):
            if f in s:
                for l in ("es", "en"):
                    yield "clasificación", "§{0} {1}".format(n, f), s[f][l]
        for b, v in s["base"].items():
            for l in ("es", "en"):
                yield "clasificación", "§{0} {1}".format(n, b), v[l]
    m = J("recursos", "analisis", "meta.json")
    for l in ("es", "en"):
        yield "análisis", "nota_version", m["nota_version"][l]
    d = os.path.join(raiz, "recursos", "analisis", "datos")
    for f in sorted(os.listdir(d)):
        for s in json.load(open(os.path.join(d, f), encoding="utf-8"))["suttas"]:
            yield "análisis", "§{0} clase".format(s["n"]), s.get("clase", "")
            for r in s.get("roles", []) + s.get("respuesta", []):
                yield "análisis", "§{0} rol".format(s["n"]), r[0]
            for l in ("es", "en"):
                yield "análisis", "§{0} nota".format(s["n"]), s["nota"][l]
    for pag, p in (("clasificación", "clasificacion"), ("análisis", "analisis")):
        h = open(os.path.join(raiz, "recursos", p, "plantilla.html"), encoding="utf-8").read()
        h = _re.sub(r"<style.*?</style>", " ", h, flags=_re.S)
        # sólo las cadenas de texto del script (los diccionarios ES/EN) y el HTML visible
        cadenas = _re.findall(r"'((?:[^'\\\n]|\\.)*)'", h) + _re.findall(r"`([^`]*)`", h)
        visible = _re.sub(r"<script.*?</script>", " ", h, flags=_re.S)
        for x in cadenas + [_re.sub(r"<[^>]+>", " ", visible)]:
            yield pag, "plantilla", _re.sub(r"<[^>]+>|\$\{[^}]*\}", " ", x)


def sin_entrada(raiz):
    """{palabra: [(página, dónde), …]} de las palabras pāḷi sin entrada.

    Cubre también las obras citadas (grupo «obra»): sus nombres llevan casi
    siempre diacríticos, y los que no (Thitzana, Nandisena, «…siddhi»,
    «…vutti») se buscan aparte. Las palabras que aparecen con mayúscula
    inicial van marcadas con «obra?» en el primer lugar de la lista."""
    d = json.load(open(os.path.join(raiz, "recursos", "terminos", "terminos.json"), encoding="utf-8"))
    formas = {f.lower() for t in d["terminos"] for f in t["formas"]}
    ignorar = {w.lower() for w in d.get("no_terminos", [])}
    faltan, mayus = {}, set()
    for pag, donde, txt in _textos(raiz):
        txt = _CITA.sub(" ", unicodedata.normalize("NFC", txt or ""))
        for tok in _PAL.findall(txt):
            w = _re.sub(r"[’']s$", "", tok).strip("’'").lower()
            # español con ñ («añade», «señala»): la ñ sola no hace pāḷi si no
            # va en grupo pāḷi (ññ, ñc, ñj); y las letras y sufijos sueltos
            # (ā, ṇa, kaṇ) son objeto de la regla, no terminología.
            pali = (_DIAC - {"ñ", "Ñ"}) & set(w) or _re.search("ñ[ñcj]", w)
            obra = tok[:1].isupper() and bool(_OBRA.search(w))
            if not w or not (pali or obra or w in SIN_DIACRITICOS) or len(w) <= 3 and w not in SIN_DIACRITICOS:
                continue
            # Un compuesto glosado por una de sus partes (pubbalopa-vidhi →
            # vidhi) basta para un término; para una obra con nombre
            # compuesto (Kalāpa-ṭīkā) hace falta la entrada del nombre entero.
            partes = not (obra and "-" in w)
            if w in formas or w in ignorar or partes and any(p in formas for p in w.split("-")):
                continue
            # con mayúscula inicial en el texto: casi siempre una obra o un autor
            if tok[:1].isupper():
                mayus.add(w)
            faltan.setdefault(w, [])
            if len(faltan[w]) < 3 and (pag, donde) not in faltan[w]:
                faltan[w].append((pag, donde))
    for w in mayus & set(faltan):
        faltan[w].insert(0, ("obra?", "con mayúscula"))
    return faltan
