#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convierte el texto de «Compuesto (samāsa)» de Bhikkhu Nandisena en los datos
de la página /recursos/compuestos/.

    python3 herramientas/compuestos_a_json.py TEXTO [FORMATO]

TEXTO   el texto en el formato de samasa6-base.txt: una línea por párrafo,
        «NNNN  {estilo} texto»; las tablas, filas «NNNN  | a | b |» entre
        «NNNN  <<TABLA>>» y «NNNN  <</TABLA>>»; las notas al pie, «[^n]: …»
        después de «<<NOTAS>>». Hoy es el texto congelado; mañana, el texto
        REVISADO, que además trae las líneas que añade el IEBH:

          NNNNa  {IEBH} texto                       un bloque nuevo, rotulado IEBH
          NNNNa  {IEBH fuente="Rū. §339"} texto     … con su fuente
          NNNNa  {IEBH-nota} texto                  una nota al pie nueva, que se
                                                    llama desde el bloque anterior
          NNNNa  {IEBH-nota} [^12]: texto           … con número propio (la llamada
                                                    [^12] la pone el texto revisado)
          NNNNa  <<TABLA IEBH fuente="…">>          una tabla nueva
          {IEBH} texto  (dentro de <<NOTAS>>)       añadido a la nota anterior

        La fuente puede ir también al final del texto: «… [fuente: Rū. §339]».
        Un «IEBH: » al principio del texto se quita: lo dice ya la etiqueta.

        Lo que añadió la aplicación de la revisión (compuestos_aplicar.py):

          {IEBH … forma=h} texto     un subtítulo, sin pasar por las heurísticas
          {IEBH … forma=p} texto     un párrafo, ídem
          {IEBH … forma=anexo} texto un añadido a la tarjeta (o bloque) anterior:
                                     una referencia, una atestación, la fuente
                                     de una resolución que completó el IEBH
          {IEBH … clase="atestación"}  el tipo del añadido, que la etiqueta dice
          | {IEBH} a | b |           una fila del IEBH en una tabla de Nandisena
          #meta clave=valor          versión, fecha, estado y nota de versión
                                     (en la cabecera del texto revisado)

FORMATO samasa6-formato.json (negritas y cursivas por línea L). Por defecto, el
        que está junto al texto (samasa6-formato.json en la misma carpeta o en
        pagina/). Sólo se usa para la negrita: los rótulos en negrita y la voz
        en negrita que encabeza cada resolución de bahubbīhi.

Escribe recursos/compuestos/compuestos.json. Lo publica
herramientas/generar_compuestos.py; esto no se ejecuta en cada commit (el
texto fuente no está en el repositorio).

Lo que se cambia del texto, y nada más:
  · las voces pāḷi entre comillas pasan a cursiva (decisión T-002 del IEBH):
    «"rāja-putto"» → «*rāja-putto*». Las comillas de una palabra española
    («"resolución"», «"malo"») se quedan; ver ES_ENTRE_COMILLAS;
  · lo que en el original va en negrita, en **negrita**;
  · ṁ → ṃ y NFC (ya en el texto congelado).

Las heurísticas con las que se reconoce cada bloque están explicadas en cada
función, y el resumen final dice cuántos bloques de cada tipo salen.
"""

import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, "recursos", "compuestos", "compuestos.json")

# Las seis clases, en el orden del documento. «kacc»: el sutta de Kaccāyana
# que define la clase, en la numeración de Nandisena
# (kaccayana/04-samasa-kappa.md).
CLASES = [
    dict(id="abyayibhava", pali="abyayībhāva", kacc=[319],
         titulo_en="Adverbial compound"),
    dict(id="kammadharaya", pali="kammadhāraya", kacc=[324],
         titulo_en="Adjectival compound"),
    dict(id="digu", pali="digu", kacc=[325], titulo_en="Numerical compound"),
    dict(id="tappurisa", pali="tappurisa", kacc=[326, 327],
         titulo_en="Determinative compound"),
    dict(id="bahubbihi", pali="bahubbīhi", kacc=[328],
         titulo_en="Relative compound"),
    dict(id="dvanda", pali="dvanda", kacc=[329],
         titulo_en="Copulative compound"),
]

# Palabras españolas que el documento pone entre comillas: no son pāḷi y no
# pasan a cursiva. Lo que lleva tilde española (á é í ó ú) tampoco.
ES_ENTRE_COMILLAS = {"resuelve", "eleva", "malo", "audaz como un cuervo"}

# Comillas que el original deja sin cerrar y que, sin arreglo, emparejarían
# mal todas las de la línea. Sólo se aplican si el texto sigue diciendo eso.
CIERRES = {
    "0450": ('"a-sūriya-passā rājadārā, las', '"a-sūriya-passā rājadārā", las'),
}

ROMANOS = r"(?:i|ii|iii|iv|v|vi|vii|viii|ix|x)"

AVISOS = []
META = {}



# Significado de los compuestos de la tabla de resumen (glosas de Nandisena:
# texto del documento y Kaccāyana, cap. 4, §319, §322, §324, §326, §329)
SIGNIFICADO_RESUMEN = {
    "upanagaraṃ": {"es": "cerca de la ciudad", "en": "near the city"},
    "Buddhaghosācariyo": {"es": "el maestro Buddhaghosa", "en": "the teacher Buddhaghosa"},
    "tilokaṃ": {"es": "los tres mundos", "en": "the three worlds"},
    "rājaputto": {"es": "hijo del rey", "en": "son of the king"},
    "chinnahattho": {"es": "(hombre) cuyas manos han sido cortadas",
                     "en": "(a man) whose hands have been cut off"},
    "Sāriputtamoggallānā": {"es": "Sāriputta y Moggallāna", "en": "Sāriputta and Moggallāna"},
}

def avisar(L, txt):
    AVISOS.append("L{0}: {1}".format(L, txt))


def nfc(s):
    return unicodedata.normalize("NFC", s)


def bil(es):
    return {"es": es, "en": ""}


# ---------------------------------------------------------------- lectura

LINEA = re.compile(r"^(\d{4}[a-z0-9.]*)  (.*)$")
ESTILO = re.compile(r"^\{([^}]*)\} ?(.*)$")


def atributos(estilo):
    """«IEBH fuente="Rū. §339" num=2/0» → ('IEBH', {'fuente': 'Rū. §339', 'num': '2/0'})."""
    nombre = estilo.split(" ", 1)[0]
    attrs = {}
    for m in re.finditer(r'(\w+)=(?:"([^"]*)"|(\S+))', estilo):
        attrs[m.group(1)] = m.group(2) if m.group(2) is not None else m.group(3)
    return nombre, attrs


def fuente_final(texto):
    """«… [fuente: Rū. §339]» → («…», «Rū. §339»)."""
    m = re.search(r"\s*\[(?:fuente|Fuente):\s*([^\]]+)\]\s*$", texto)
    if m:
        return texto[:m.start()], m.group(1).strip()
    return texto, None


def leer(ruta):
    """Lista de elementos en el orden del texto:
         ("p", L, estilo, attrs, texto)
         ("tabla", L, hasta, filas, attrs)
       y el diccionario de notas {n: {"es":…, "iebh":[…]}}."""
    elems, notas, orden_notas = [], {}, []
    META.clear()
    tabla = None
    en_notas = False
    ultima_nota = None
    for crudo in open(ruta, encoding="utf-8"):
        crudo = nfc(crudo.rstrip("\n").replace("ṁ", "ṃ").replace("Ṁ", "Ṃ"))
        m = re.match(r"^#meta (\w+)=(.*)$", crudo)
        if m:
            META[m.group(1)] = m.group(2).strip()
            continue
        if crudo.startswith("#") or not crudo.strip():
            continue
        if crudo.strip() == "<<NOTAS>>" or crudo.endswith("  <<NOTAS>>"):
            en_notas = True
            continue
        if en_notas:
            crudo = re.sub(r"^\d{4}[a-z0-9.]*  (?=\[\^)", "", crudo)
            m = re.match(r"^\[\^(\w+)\]:\s*(.*)$", crudo)
            if m:
                ultima_nota = m.group(1)
                notas[ultima_nota] = {"es": m.group(2).strip(), "iebh": []}
                orden_notas.append(ultima_nota)
                continue
            m = re.match(r"^(?:\d{4}[a-z0-9.]*\s+)?\{(IEBH(?:-nota)?)([^}]*)\}\s*(.*)$", crudo)
            if m and ultima_nota:
                _n, at = atributos(m.group(1) + m.group(2))
                txt, f = fuente_final(m.group(3))
                txt = re.sub(r"^IEBH:\s*", "", txt)
                notas[ultima_nota]["iebh"].append({"es": txt, "fuente": at.get("fuente") or f})
                continue
            avisar("NOTAS", "línea que no se entiende: " + crudo[:60])
            continue
        m = LINEA.match(crudo)
        if not m:
            avisar("?", "línea que no se entiende: " + crudo[:60])
            continue
        L, resto = m.groups()
        if resto.startswith("<<TABLA"):
            _n, at = atributos(resto.strip("<>").replace("TABLA", "", 1).strip() or "TABLA")
            if "IEBH" in resto:
                at["IEBH"] = True
            tabla = {"L": L, "filas": [], "attrs": at, "iebh": []}
            continue
        if resto.startswith("<</TABLA>>"):
            if tabla["iebh"]:
                tabla["attrs"]["filas_iebh"] = tabla["iebh"]
            elems.append(("tabla", tabla["L"], L, tabla["filas"], tabla["attrs"]))
            tabla = None
            continue
        if tabla is not None:
            if resto.startswith("|"):
                fila = resto.strip()
                # «| {IEBH} a | b |»: una fila que añade el IEBH
                mi = re.match(r"^\|\s*\{IEBH((?: \w+=\"[^\"]*\")*)\}\s?", fila)
                if mi:
                    _n, at_f = atributos("IEBH" + mi.group(1))
                    tabla["iebh"].append({"i": len(tabla["filas"]), "fuente": at_f.get("fuente"), "L": L,
                                          "celdas": [int(x) for x in at_f.get("celdas", "").split(",") if x]})
                    fila = "| " + fila[mi.end():]
                celdas = [c.strip() for c in fila.strip("|").split(" | ")]
                # «a / b» es un salto de párrafo dentro de la celda
                tabla["filas"].append([c.replace(" / ", "\n") for c in celdas])
            continue
        m = ESTILO.match(resto)
        estilo, texto = (m.group(1), m.group(2)) if m else ("Normal", resto)
        nombre, at = atributos(estilo)
        elems.append(("p", L, nombre, at, texto.rstrip()))
    return elems, notas, orden_notas


# ---------------------------------------------------------------- texto

ACENTO_ES = re.compile("[áéíóúÁÉÍÓÚ¿¡]")


def comillas(t, L=""):
    """Las voces pāḷi entre comillas → *cursiva* (T-002). Se emparejan de
    izquierda a derecha; una comilla suelta (sin pareja) se deja como está."""
    if L in CIERRES and CIERRES[L][0] in t:
        t = t.replace(CIERRES[L][0], CIERRES[L][1])
    partes = t.split('"')
    if len(partes) < 3:
        return t
    out = [partes[0]]
    i = 1
    while i < len(partes):
        if i + 1 >= len(partes):          # comilla suelta al final
            out.append('"' + partes[i])
            break
        dentro, despues = partes[i], partes[i + 1]
        if (ACENTO_ES.search(dentro) or dentro.strip().lower() in ES_ENTRE_COMILLAS
                or not dentro.strip()):
            out.append('"' + dentro + '"')
        else:
            # el espacio de los bordes queda fuera de la cursiva
            a = len(dentro) - len(dentro.lstrip())
            b = len(dentro.rstrip())
            out.append(dentro[:a] + "*" + dentro[a:b] + "*" + dentro[b:])
        out.append(despues)
        i += 2
    return "".join(out)


def negritas(t, runs):
    """Pone en **negrita** lo que el original tiene en negrita. Las corridas
    se buscan en el texto (que puede haber cambiado en la revisión): una
    corrida que ya no está, no se pone."""
    for txt in runs:
        s = txt.strip()
        if not s or "**" + s + "**" in t:
            continue
        k = t.find(s)
        if k >= 0:
            t = t[:k] + "**" + s + "**" + t[k + len(s):]
    return t


def corridas_negras(fmt, L):
    """El texto de las corridas en negrita de un párrafo (no de una tabla)."""
    v = fmt.get(L[:4]) if fmt else None
    if not v or not isinstance(v, list) or not v or not isinstance(v[0], list):
        return []
    if v and v[0] and isinstance(v[0][0], list):     # es una tabla
        return []
    return [r[0] for r in v if len(r) >= 2 and r[1]]


def limpio(t):
    """Sin marcas de formato, para comparar."""
    return re.sub(r"\*+", "", t).strip()


# ---------------------------------------------------------------- formas

# Una resolución en una línea: «compuesto (traducción): voz (glosa) voz (glosa)».
# El compuesto tiene una o dos palabras; tras la glosa del compuesto va «:» o
# «;» (antevāsiko, L0974). Puede faltar la traducción («nibbānaṃ: …»), y el
# paréntesis puede quedar sin cerrar («atthakāmo (que desea beneficio: …»).
RES_LINEA_ESTRICTA = re.compile(r"^(?P<c>[^\s:();,\"]+(?: [^\s:();,\"]+)?)"
                                r"(?: \((?P<t>[^)]*)\))?\s*[:;](?P<v>.*)$")
RES_LINEA_SUELTA = re.compile(r"^(?P<c>[^\s:();,\"]+(?: [^\s:();,\"]+)?)"
                              r"(?: \((?P<t>[^)]*?)\)?)?\s*[:;](?P<v>.*)$")


class _ResLinea:
    """Primero con el paréntesis cerrado («addhamāsaṃ (medio mes; quincena):
    …»); si no, sin cerrar («atthakāmo (que desea beneficio: …»)."""
    @staticmethod
    def match(t):
        return RES_LINEA_ESTRICTA.match(t) or RES_LINEA_SUELTA.match(t)


RES_LINEA = _ResLinea()
# Sólo el compuesto con su traducción: «muhuttasukhaṃ (felicidad por un momento)»
# y «kammajaṃ (generado por el kamma). Aquí hay solamente compuesto.»
RES_SOLO = re.compile(r"^(?P<c>[^\s:();,\"]+) \((?P<t>[^)]*)\)(?P<r>\.?(?:\s.*)?)$")
GLOSA = re.compile(r"\(([^()]*)\)")


def glosadas(t):
    """Cuántas glosas «(…)» tiene una línea."""
    return len(GLOSA.findall(t))


def tokens(t):
    """«āgatā (venidos) samaṇā (monjes), so (éste) …» →
    [{"p": "āgatā", "g": "venidos"}, …, {"p": ",", "g": ""}, …].
    Lo que va entre dos glosas es la voz (o las voces: «so ayaṃ (éste)»); la
    puntuación que la precede va en una ficha propia, sin glosa. El texto
    entero se puede recomponer con las fichas."""
    out, i = [], 0
    for m in GLOSA.finditer(t):
        antes = t[i:m.start()]
        i = m.end()
        pre = re.match(r"^\s*([,;.]+)\s*", antes)
        if pre:
            out.append({"p": pre.group(1), "g": bil("")})
            antes = antes[pre.end():]
        out.append({"p": antes.strip(), "g": bil(m.group(1).strip())})
    cola = t[i:].strip()
    if cola:
        pre = re.match(r"^([,;.]+)\s*(.*)$", cola)
        if pre:
            out.append({"p": pre.group(1), "g": bil("")})
            cola = pre.group(2).strip()
        if cola:
            out.append({"p": cola, "g": bil("")})
    return out


def es_resolucion(t):
    t = limpio(t)
    if RES_SOLO.match(t):
        return True
    m = RES_LINEA.match(t)
    if not m:
        return False
    # «Otros ejemplos:» — dos palabras y dos puntos, sin glosa ni resolución
    return bool(m.group("t") is not None or glosadas(m.group("v")))


def resolucion_linea(t, L):
    """Un bloque interlineal a partir de una línea de resolución."""
    base = limpio(t)
    m = RES_SOLO.match(base)
    if m and not RES_LINEA.match(base):
        r = m.group("r").strip()
        b = {"compuesto": m.group("c"), "traduccion": bil(m.group("t").strip()),
             "viggaha": []}
        if r and r != ".":
            b["resto"] = bil(re.sub(r"^\.\s*", "", r))
        return b
    m = RES_LINEA.match(base)
    trad = (m.group("t") or "").strip()
    if m.group("t") is not None and not RES_LINEA_ESTRICTA.match(base):
        avisar(L, "paréntesis de la traducción sin cerrar: «{0}»".format(base[:50]))
    return {"compuesto": m.group("c").strip(), "traduccion": bil(trad),
            "viggaha": tokens(m.group("v").strip())}


def es_cabecera_bahubbihi(t, siguiente):
    """La voz sola (en negrita en el original) que encabeza una resolución
    de bahubbīhi: «āgatasamaṇo» y, en la línea siguiente, «āgatā (venidos)
    samaṇā (monjes) …»."""
    s = limpio(t)
    return (bool(re.match(r"^[^\s():.,;\"]+$", s)) and siguiente is not None
            and glosadas(siguiente) >= 2)


# ---------------------------------------------------------------- rótulos

REF_FINAL = re.compile(r"\s*\((?:Kacc?|Rū|Sad|Nir)\.[^()]*(?:\([^()]*\)[^()]*)*\)\s*$")


def sin_ref_final(s):
    """Sin la referencia que la revisión añade al final de un rótulo o de una
    frase («… (upamānuttarapada) (Kacc. §324; Rū. §339 (pp. 186–187))»,
    «… en la séptima inflexión. (Rū. §351 (pp. 197–198))»): para decidir si
    la línea es un rótulo, cuenta lo de Nandisena."""
    prev = None
    while prev != s:
        prev, s = s, REF_FINAL.sub("", s)
    return s.strip() or prev


def es_rotulo(t, prev_vacia, sig_vacia, todo_negrita):
    """Un subtítulo: línea suelta y corta, que no acaba en punto, coma, punto
    y coma ni dos puntos, y que no es una resolución. O una línea entera en
    negrita («Con derivados primarios»)."""
    s = sin_ref_final(limpio(t))
    if not s:
        return False
    if todo_negrita and len(s) < 80:
        return True
    if not (prev_vacia and sig_vacia):
        return False
    if len(s) > 110 or s[-1] in ".,;:" or es_resolucion(s):
        return False
    return True


def nivel_rotulo(t, negrita):
    s = limpio(t)
    if re.match(r"^\(" + ROMANOS + r"\)", s) or negrita:
        return 3
    return 2


def ascii(s):
    s = unicodedata.normalize("NFD", limpio(s).lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def slug_rotulo(t):
    """El término pāḷi del último paréntesis, si lo hay («… (visesanapubbapada)»);
    si no, el texto entero."""
    s = sin_ref_final(re.sub(r"\[\^\w+\]", "", limpio(t)))
    m = re.findall(r"\(([^()]+)\)", s)
    if m and not re.match(r"^" + ROMANOS + r"$|^\d+$", m[-1]):
        return ascii(m[-1])
    return ascii(s)[:60]


# ---------------------------------------------------------------- tablas

def clasificar_tabla(filas, fmt_celdas):
    """paradigma | resumen | interlineal | ejemplos | tabla."""
    if not filas:
        return "tabla"
    c0 = filas[0][0].strip().lower()
    if c0.startswith("infl"):
        return "paradigma"
    if c0 == "#":
        return "resumen"
    if (len(filas) == 2 and len(filas[0]) >= 3
            and filas[0][1].strip().lower().startswith("resoluci")):
        return "interlineal"
    if len(filas) == 2 and len(filas[0]) == len(filas[1]) and len(filas[0]) >= 3:
        return "glosa"           # palabra por palabra, sin el compuesto (L0110)
    if all(len(f) in (3, 4) for f in filas) and len({len(f) for f in filas}) == 1:
        return "ejemplos"
    return "tabla"


def cabecera_en_negrita(filas, fmt_celdas):
    """¿La primera fila es cabecera? Sí, si en el original va en negrita o
    si dice «resolución…»."""
    if not filas:
        return False
    n = len(filas[0])
    if fmt_celdas and len(fmt_celdas) >= n:
        neg = []
        for celda in fmt_celdas[:n]:
            runs = [r for par in celda for r in par if r and r[0].strip()]
            neg.append(bool(runs) and all(r[1] for r in runs))
        if all(neg):
            return True
    return any(c.strip().lower().startswith("resoluci") for c in filas[0])


def bloque_tabla(tipo, L, hasta, filas, fmt_celdas, filas_iebh=()):
    """filas_iebh: [{"i": índice en filas, "fuente": …}] — las filas del IEBH."""
    iebh = {x["i"]: x for x in filas_iebh}
    if iebh and tipo not in ("ejemplos", "resumen", "tabla"):
        avisar(L, "filas del IEBH en una tabla de tipo «{0}»: no se marcan".format(tipo))
    if tipo == "paradigma":
        cab = filas[0]
        return {"tipo": "paradigma",
                "cabecera": [bil(c) for c in cab],
                "filas": [[bil(f[0])] + f[1:] for f in filas[1:]]}
    if tipo == "resumen":
        b = {"tipo": "resumen", "cabecera": [bil(c) for c in filas[0]],
             "filas": [[bil(c) for c in f] for f in filas[1:]]}
        # columna del significado (pedido del IEBH, 2026-10-17): las glosas de
        # Nandisena en este documento y en el capítulo 4 (español e inglés)
        b["cabecera"].append({"es": "Significado", "en": "Meaning"})
        for f in b["filas"]:
            g = SIGNIFICADO_RESUMEN.get(f[2]["es"].strip())
            if g is None:
                avisar(L, "resumen: sin significado para «{0}»".format(f[2]["es"]))
                g = {"es": "", "en": ""}
            f.append(dict(g))
        b["significado"] = True
        if iebh:
            b["filas_iebh"] = [i - 1 for i in sorted(iebh)]
            # las celdas que llenó el IEBH (las demás de la fila son de Nandisena)
            b["celdas_iebh"] = {str(i - 1): iebh[i]["celdas"] for i in sorted(iebh) if iebh[i]["celdas"]}
            b["fuente_iebh"] = next((iebh[i]["fuente"] for i in sorted(iebh) if iebh[i]["fuente"]), None)
        return b
    if tipo == "interlineal":
        a, b = filas
        if len(a) != len(b):
            avisar(L, "interlineal con filas de distinto largo ({0} y {1})".format(len(a), len(b)))
        vig = [{"p": p, "g": bil(b[k] if k < len(b) else "")} for k, p in enumerate(a[2:], 2)]
        return {"tipo": "interlineal", "origen": "tabla", "compuesto": a[0],
                "traduccion": bil(b[0]), "rotulo": bil(a[1]), "viggaha": vig}
    if tipo == "glosa":
        a, b = filas
        return {"tipo": "interlineal", "origen": "tabla", "compuesto": "",
                "traduccion": bil(""),
                "viggaha": [{"p": p, "g": bil(b[k])} for k, p in enumerate(a)]}
    if tipo == "ejemplos":
        cab = None
        desde = 0
        if cabecera_en_negrita(filas, fmt_celdas):
            cab, filas = filas[0], filas[1:]
            desde = 1
        n = len(filas[0]) if filas else 4
        out = []
        for k, f in enumerate(filas):
            if n == 4:
                s, r, c, t = f
            else:
                s, (r, c, t) = "", f
            fila = {"sentido": bil(s), "resolucion": r, "compuesto": c,
                    "traduccion": bil(t)}
            if k + desde in iebh:
                fila["iebh"] = True
                fila["fuente"] = iebh[k + desde]["fuente"] or "IEBH"
                fila["L"] = iebh[k + desde]["L"]
            out.append(fila)
        b = {"tipo": "ejemplos", "columnas": n, "filas": out}
        if cab:
            b["cabecera"] = [bil(x) for x in cab]
        return b
    b = {"tipo": "tabla", "filas": [[bil(c) for c in f] for f in filas]}
    if iebh:
        b["filas_iebh"] = sorted(iebh)
    return b


# ---------------------------------------------------------------- bloques

def construir(elems, fmt):
    """Recorre el texto y arma intro, clases y resumen."""
    intro, clases, resumen = [], [], None
    actual = intro
    notas_nuevas = []          # (L, texto, fuente, n o None)
    titulo_doc = None
    pend = {}                  # lo que se arrastra: rótulo, iebh

    # índice de los párrafos por posición, para mirar el anterior y el siguiente
    def vacio(e):
        return e is None or (e[0] == "p" and not e[4].strip())

    def marca(b, e):
        """iebh / fuente / L de un elemento ("p" o "tabla")."""
        if e[0] == "p":
            L, nombre, at = e[1], e[2], e[3]
            b["L"] = L
            if nombre.startswith("IEBH"):
                b["iebh"] = True
                if at.get("fuente"):
                    b["fuente"] = at["fuente"]
                if at.get("clase"):
                    b["clase"] = bil(at["clase"])
        else:
            b["L"], b["hasta"] = e[1], e[2]
            if e[4].get("IEBH"):
                b["iebh"] = True
                if e[4].get("fuente"):
                    b["fuente"] = e[4]["fuente"]
        return b

    def texto(e):
        L, t = e[1], e[4]
        t, f = fuente_final(t)
        if f and e[2].startswith("IEBH"):
            e[3].setdefault("fuente", f)
        if e[2].startswith("IEBH"):
            t = re.sub(r"^IEBH:\s*", "", t)
        else:                   # la negrita del original es de Nandisena, no del IEBH
            t = negritas(t, corridas_negras(fmt, L))
        return comillas(t, L[:4])

    i, n = 0, len(elems)
    while i < n:
        e = elems[i]
        prev = elems[i - 1] if i else None
        sig = elems[i + 1] if i + 1 < n else None
        if e[0] == "tabla":
            fmt_c = fmt.get(e[1]) if fmt else None
            if fmt_c and not (fmt_c and isinstance(fmt_c[0], list) and fmt_c[0]
                              and isinstance(fmt_c[0][0], list)):
                fmt_c = None
            tipo = clasificar_tabla(e[3], fmt_c)
            b = marca(bloque_tabla(tipo, e[1], e[2], e[3], fmt_c, e[4].get("filas_iebh", ())), e)
            # las celdas con texto: comillas → cursiva también ahí
            if b["tipo"] == "resumen":
                resumen = b
            else:
                actual.append(b)
            i += 1
            continue
        L, nombre, at, t = e[1], e[2], e[3], e[4]
        if not t.strip():
            i += 1
            continue
        if titulo_doc is None and L.startswith("0001"):
            titulo_doc = t.strip()
            i += 1
            continue
        if nombre == "IEBH-nota":
            tt, f = fuente_final(t)
            m = re.match(r"^\[\^(\w+)\]:\s*(.*)$", tt)
            notas_nuevas.append((L, comillas(re.sub(r"^IEBH:\s*", "", m.group(2) if m else tt), L[:4]),
                                 at.get("fuente") or f, m.group(1) if m else None, actual))
            i += 1
            continue
        # lo que el IEBH añade con su forma ya decidida (compuestos_aplicar.py)
        forma = at.get("forma") if nombre.startswith("IEBH") else None
        if forma == "anexo":
            tt = texto(e).strip()
            if actual:
                b = actual[-1]
                ax = {"es": tt, "en": "", "fuente": at.get("fuente"), "L": L}
                if at.get("clase"):
                    ax["clase"] = bil(at["clase"])
                b.setdefault("anexos", []).append(ax)
            else:
                avisar(L, "anexo del IEBH sin bloque anterior")
            i += 1
            continue
        if forma == "h":
            tt = re.sub(r"\*\*", "", texto(e)).strip()
            actual.append(marca({"tipo": "h", "nivel": nivel_rotulo(t, False), "texto": bil(tt)}, e))
            i += 1
            continue
        if forma == "p":
            actual.append(marca({"tipo": "p", "texto": bil(texto(e).strip())}, e))
            i += 1
            continue
        if forma == "verso":
            # «entrada ‖ verso // verso ‖ traducción»: una sola unidad
            partes = (t.split(" ‖ ") + ["", "", ""])[:3]
            b = marca({"tipo": "p", "texto": bil(comillas(partes[0].strip(), L[:4])),
                       "verso": bil(partes[1].strip().replace(" // ", "\n")),
                       "traduccion_verso": bil(comillas(partes[2].strip(), L[:4]))}, e)
            actual.append(b)
            i += 1
            continue
        # el rótulo de una de las seis clases (num=3/0 en el original)
        if at.get("num", "").startswith("3/"):
            s = limpio(t).lower()
            c = next((c for c in CLASES if c["pali"] + "-samāsa" in s), None)
            if c:
                tit = sin_ref_final(limpio(t)).rstrip(".")
                ref_t = limpio(t)[len(tit):].strip(" .")
                clases.append({"id": c["id"], "n": len(clases) + 1, "pali": c["pali"],
                               "titulo": {"es": tit, "en": ""},
                               "kacc": c["kacc"], "L": L, "bloques": []})
                if ref_t.startswith("(") and ref_t.endswith(")"):
                    clases[-1]["ref"] = ref_t[1:-1]
                actual = clases[-1]["bloques"]
                i += 1
                continue
            avisar(L, "rótulo de clase que no se reconoce: " + t[:50])
        # una lista: líneas seguidas con num= (salvo 3/), o varias líneas
        # seguidas, sin blanco entre ellas, que empiezan por «(1)», «(2)»…
        if at.get("num"):
            j = i
            items = []
            while (j < n and elems[j][0] == "p" and elems[j][3].get("num")
                   and not elems[j][3]["num"].startswith("3/") and elems[j][4].strip()):
                items.append(texto(elems[j]))
                j += 1
            b = marca({"tipo": "lista", "items": [bil(x.strip()) for x in items]}, e)
            b["hasta"] = elems[j - 1][1]
            if len(items) >= 4 and all(x.strip().endswith(":") for x in items[::2]):
                b["forma"] = "pares"
            actual.append(b)
            i = j
            continue
        # resoluciones de bahubbīhi: la voz sola y, debajo, su resolución
        sig_t = sig[4] if sig and sig[0] == "p" and sig[4].strip() else None
        if es_cabecera_bahubbihi(t, sig_t):
            j = i + 1
            lineas = []
            while (j < n and elems[j][0] == "p" and elems[j][4].strip() and glosadas(elems[j][4]) >= 1
                   and not elems[j][3].get("forma")):      # un anexo del IEBH no es otra resolución
                lineas.append(elems[j])
                j += 1
            comp = limpio(t)
            vs = [tokens(limpio(comillas(x[4], x[1][:4]))) for x in lineas]
            v0 = vs[0]
            # la traducción es la glosa de la ficha que lleva el propio compuesto
            # la ÚLTIMA ficha que lleva el compuesto: en «suvaṇṇavaṇṇo (el color dorado)
            # viya … suvaṇṇavaṇṇo Bhagavā (…)» la primera es un miembro
            res = next((k for k in range(len(v0) - 1, -1, -1) if comp in v0[k]["p"].split(" ")), None)
            if res is None:
                # la resolución escribe el compuesto de otro modo
                # («idapaccayā» / «idappaccayā», L1074): la última ficha glosada
                glos = [k for k, tk in enumerate(v0) if tk["g"]["es"]]
                res = glos[-1] if glos else None
                avisar(L, "bahubbīhi «{0}»: la resolución no repite el compuesto tal cual; "
                          "se toma la última glosa («{1}»)".format(
                              comp, v0[res]["p"] if res is not None else ""))
            trad = v0[res]["g"]["es"] if res is not None else ""
            resto_par = None
            if res is not None:
                v0[res]["r"] = True
                # lo que la revisión añade detrás de la resolución («… matakāyo (…).
                # Cf. «Chuddho…», Dh. 19 (PTS p. 6), verso 41»): no son fichas
                cola = v0[res + 1:]
                k = 0
                while k < len(cola) and re.match(r"^[,;.]+$", cola[k]["p"]) and not cola[k]["g"]["es"]:
                    k += 1
                if cola[k:]:
                    resto_par = " ".join(tk["p"] + (" (" + tk["g"]["es"] + ")" if tk["g"]["es"] else "")
                                         for tk in cola[k:]).replace(" ,", ",").strip()
                    del v0[res + 1 + k:]
            b = marca({"tipo": "interlineal", "origen": "par", "compuesto": comp,
                       "traduccion": bil(trad), "viggaha": v0,
                       "texto": bil(comillas(lineas[0][4].strip(), lineas[0][1][:4]))}, e)
            b["L_resolucion"] = lineas[0][1]
            if resto_par:
                b["resto"] = bil(resto_par)
            if len(vs) > 1:
                for x, v in zip(lineas[1:], vs[1:]):
                    for tk in v:
                        if comp in tk["p"].split(" "):
                            tk["r"] = True
                b["alternativas"] = [{"L": x[1], "viggaha": v,
                                      "texto": bil(comillas(x[4].strip(), x[1][:4]))}
                                     for x, v in zip(lineas[1:], vs[1:])]
            if any(x[2].startswith("IEBH") for x in lineas):
                b["iebh"] = True
            actual.append(b)
            i = j
            continue
        # una resolución en una línea («Buddhabhāsito (dicho por el Buddha): …»)
        if es_resolucion(t):
            tt = texto(e)
            b = marca(dict(tipo="interlineal", origen="linea", **resolucion_linea(tt, L)), e)
            b["texto"] = bil(tt.strip())
            actual.append(b)
            i += 1
            continue
        # varias líneas seguidas, sin blanco: un párrafo que introduce («…:»)
        # y una lista, o una lista sola («(1) el primer miembro…»)
        seguidas = []
        j = i
        while (j < n and elems[j][0] == "p" and elems[j][4].strip()
               and not elems[j][3].get("num") and not es_resolucion(elems[j][4])):
            seguidas.append(elems[j])
            j += 1
        if len(seguidas) >= 3 or (len(seguidas) == 2 and limpio(seguidas[0][4]).endswith(":")):
            cab = seguidas[0] if limpio(seguidas[0][4]).endswith(":") else None
            if cab:
                actual.append(marca({"tipo": "p", "texto": bil(texto(cab).strip())}, cab))
            resto = seguidas[1:] if cab else seguidas
            b = marca({"tipo": "lista", "items": [bil(texto(x).strip()) for x in resto]}, resto[0])
            b["hasta"] = resto[-1][1]
            if any(x[2].startswith("IEBH") for x in resto):
                b["iebh"] = True
            actual.append(b)
            i = j
            continue
        # un subtítulo
        negs = corridas_negras(fmt, L)
        todo_neg = bool(negs) and limpio("".join(negs)).replace(" ", "") == limpio(t).replace(" ", "")
        if es_rotulo(t, vacio(prev), vacio(sig) or (sig and sig[0] == "tabla"), todo_neg):
            tt = re.sub(r"\*\*", "", texto(e)).strip()
            b = marca({"tipo": "h", "nivel": nivel_rotulo(t, todo_neg), "texto": bil(tt)}, e)
            actual.append(b)
            i += 1
            continue
        # un párrafo; si empieza por un término en negrita seguido de coma
        # («dvipada-bhinnādhikaraṇa, una de las 9 clases…»), ese término es
        # un subtipo y va al índice
        tt = texto(e).strip()
        b = marca({"tipo": "p", "texto": bil(tt)}, e)
        m = re.match(r"^\*\*([^*]+)\*\*,", tt)
        if m:
            b["def"] = m.group(1)
        actual.append(b)
        i += 1
    return titulo_doc, intro, clases, resumen, notas_nuevas


def anexar_a_tarjetas(bloques):
    """Una nota del IEBH que sigue a una tarjeta y habla sólo de ella (la nombra,
    o es una atestación que no nombra otra) pasa a ser un anexo de esa tarjeta:
    así no parte la rejilla de tarjetas. La que habla de varias se queda como
    bloque (la plantilla la pone a todo lo ancho dentro de la rejilla)."""
    out = []
    n = 0
    for b in bloques:
        if (b.get("iebh") and b["tipo"] == "p" and not b.get("verso") and not b.get("def")
                and out and out[-1]["tipo"] == "interlineal"):
            corrida = []
            for x in reversed(out):
                if x["tipo"] != "interlineal":
                    break
                corrida.append(x)
            txt = limpio(b["texto"]["es"]).lower()
            nombradas = [x for x in corrida if x.get("compuesto") and x["compuesto"].lower() in txt]
            clase = (b.get("clase") or {}).get("es", "")
            # una atestación, o una nota que señala la tarjeta anterior sin nombrarla
            deictica = clase == "Atestación" or re.match(
                r"^(«|tipiṭaka|este compuesto|el canon lo|la frase sin componer)", txt)
            destino = None
            if len(nombradas) == 1 and nombradas[0] in corrida[:2]:
                destino = nombradas[0]
            elif not nombradas and deictica:
                destino = out[-1]
            if destino is not None:
                prev = destino
                ax = {"es": b["texto"]["es"], "en": "", "fuente": b.get("fuente"), "L": b["L"]}
                if b.get("clase"):
                    ax["clase"] = b["clase"]
                prev.setdefault("anexos", []).append(ax)
                n += 1
                continue
        out.append(b)
    bloques[:] = out
    return n


def poner_ids(intro, clases):
    """Un id estable por bloque: los rótulos por su término pāḷi, los
    interlineales por su compuesto, lo demás por su línea."""
    vistos = set()

    def unico(base):
        k, s = 1, base
        while s in vistos:
            k += 1
            s = "{0}-{1}".format(base, k)
        vistos.add(s)
        return s

    for pref, bloques in [("intro", intro)] + [(c["id"], c["bloques"]) for c in clases]:
        for b in bloques:
            if b["tipo"] == "h":
                b["id"] = unico(pref + "-" + slug_rotulo(b["texto"]["es"]))
            elif b.get("def"):
                b["id"] = unico(pref + "-" + ascii(b["def"]))
            elif b["tipo"] == "interlineal" and b.get("compuesto"):
                b["id"] = unico("c-" + ascii(b["compuesto"]))
            else:
                b["id"] = unico(pref + "-l" + b["L"])


def comillas_en_todo(x):
    """Las comillas → cursiva en las celdas de las tablas, que no pasan por
    texto(). Los párrafos, listas y resoluciones en línea ya pasaron."""
    if isinstance(x, dict):
        for k, v in x.items():
            if k == "es" and isinstance(v, str):
                x[k] = comillas(v, "")
            elif isinstance(v, (dict, list)):
                comillas_en_todo(v)
    elif isinstance(x, list):
        for v in x:
            comillas_en_todo(v)


def de_tabla(b):
    return b["tipo"] in ("tabla", "paradigma", "ejemplos") or b.get("origen") == "tabla"


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    texto_ruta = argv[1]
    if len(argv) > 2:
        fmt_ruta = argv[2]
    else:
        d = os.path.dirname(os.path.abspath(texto_ruta))
        cand = [os.path.join(d, "samasa6-formato.json"),
                os.path.join(d, "pagina", "samasa6-formato.json")]
        fmt_ruta = next((c for c in cand if os.path.exists(c)), None)
    fmt = json.load(open(fmt_ruta, encoding="utf-8")) if fmt_ruta else {}
    if not fmt:
        print("⚠ sin archivo de formato: no habrá negritas")

    elems, notas_doc, orden = leer(texto_ruta)
    titulo_doc, intro, clases, resumen, nuevas = construir(elems, fmt)
    faltan = [c["id"] for c in CLASES if c["id"] not in {x["id"] for x in clases}]
    if faltan:
        print("✗ faltan clases: " + ", ".join(faltan))
        return 1
    anexadas = sum(anexar_a_tarjetas(bs) for bs in [intro] + [c["bloques"] for c in clases])
    poner_ids(intro, clases)

    # las notas: las del documento, con lo que el IEBH añada, y las nuevas
    notas = {}
    for k in orden:
        v = notas_doc[k]
        notas[k] = {"es": comillas(v["es"]), "en": ""}
        if v["iebh"]:
            notas[k]["iebh"] = [{"es": comillas(x["es"]), "en": "", "fuente": x["fuente"]}
                                for x in v["iebh"] if x["es"]]
    sig = max([int(k) for k in notas if k.isdigit()] + [0]) + 1
    for L, txt, fuente, num, donde in nuevas:
        if num is None:
            num = str(sig)
            sig += 1
            # la llamada, al final del bloque anterior
            if donde:
                b = donde[-1]
                campo = b.get("texto") if isinstance(b.get("texto"), dict) else None
                if campo is not None:
                    campo["es"] += "[^{0}]".format(num)
                elif b.get("traduccion"):
                    b["traduccion"]["es"] += "[^{0}]".format(num)
        notas[num] = {"es": txt, "en": "", "iebh": True, "L": L}
        if fuente:
            notas[num]["fuente"] = fuente

    # las notas, por su número
    notas = dict(sorted(notas.items(), key=lambda kv: (0, int(kv[0])) if kv[0].isdigit() else (1, kv[0])))
    for bs in [intro] + [c["bloques"] for c in clases]:
        for b in bs:
            if de_tabla(b):
                comillas_en_todo(b)
    if resumen:
        comillas_en_todo(resumen)

    viejo = {}
    if os.path.exists(DESTINO):
        try:
            viejo = json.load(open(DESTINO, encoding="utf-8")).get("meta", {})
        except ValueError:
            viejo = {}
    meta = {
        "version": META.get("version") or viejo.get("version", "0.1"),
        "fecha": META.get("fecha") or viejo.get("fecha", "2026-10-16"),
        "estado": ({"es": META["estado"], "en": META.get("estado_en", "")} if META.get("estado")
                   else {"es": "Borrador en revisión", "en": "Draft under review"}),
        "atribucion": {"es": "Bhikkhu Nandisena, edición revisada por IEBH",
                       "en": "Bhikkhu Nandisena, edited by IEBH"},
        "titulo_doc": titulo_doc or "Compuesto (samāsa)",
        "fuente": os.path.basename(texto_ruta),
        "nota_version": {"es": META["nota_version"], "en": ""} if META.get("nota_version") else viejo.get("nota_version", {
            "es": "Primera publicación, como borrador: el texto de Bhikkhu Nandisena "
                  "tal como lo dejó, con las voces pāḷi en cursiva. Las propuestas de "
                  "revisión esperan la decisión del IEBH.",
            "en": ""}),
    }
    out = {"meta": meta, "intro": intro, "clases": clases,
           "resumen": resumen, "notas": notas}
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    s = json.dumps(out, ensure_ascii=False, indent=1)
    open(DESTINO, "w", encoding="utf-8").write(nfc(s) + "\n")

    from collections import Counter
    cuenta = Counter()
    for bs in [intro] + [c["bloques"] for c in clases]:
        for b in bs:
            cuenta[b["tipo"] + ("·" + b["origen"] if b.get("origen") else "")] += 1
    print("→ {0}".format(os.path.relpath(DESTINO, RAIZ)))
    print("  " + " · ".join("{0} {1}".format(v, k) for k, v in sorted(cuenta.items())))
    print("  clases: " + " · ".join("{0} ({1})".format(c["pali"], len(c["bloques"])) for c in clases))
    print("  notas: {0} · resumen: {1} filas".format(len(notas), len(resumen["filas"]) if resumen else 0))
    iebh = sum(1 for bs in [intro] + [c["bloques"] for c in clases] for b in bs if b.get("iebh"))
    if iebh:
        anex = sum(len(b.get("anexos", [])) for bs in [intro] + [c["bloques"] for c in clases] for b in bs)
        filas = sum(1 for bs in [intro] + [c["bloques"] for c in clases] for b in bs
                    if b["tipo"] == "ejemplos" for f in b["filas"] if f.get("iebh"))
        print("  bloques del IEBH: {0} · anexos: {1} (de ellos, {3} notas pasadas a su tarjeta) · filas del IEBH en tablas: {2}".format(
            iebh, anex, filas, anexadas))
    for a in AVISOS:
        print("  ⚠ " + a)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
