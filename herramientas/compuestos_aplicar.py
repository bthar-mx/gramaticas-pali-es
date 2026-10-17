#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplica la revisión verificada de «Compuesto (samāsa)» al texto congelado de
Bhikkhu Nandisena y escribe el texto REVISADO que lee compuestos_a_json.py.

    python3 herramientas/compuestos_aplicar.py TRABAJO

TRABAJO  la carpeta de trabajo de la revisión (no está en el repositorio):
           base.txt                         el texto congelado
           propuestas/lote-*.json           las propuestas
           verificacion/verif-*.json        el consejo de cada una (approve,
                                            amend, reject, later, answered)
           verificacion/auditoria-refs.json el texto final, con las
                                            referencias auditadas
           revision/overrides.json          consejos que mandan sobre los anteriores
           revision/extra.json              los puntos generales (sólo T-004)

Escribe
  recursos/compuestos/texto-revisado.txt   el texto revisado
  recursos/compuestos/aplicado.json        el registro: qué se aplicó, cómo,
                                           los conflictos y lo que no se aplicó

Qué texto se aplica (decisión del IEBH: todo consejo, como si estuviera
aprobado): approve → «despues»; amend → la «enmienda» del verificador; en los
dos casos, si la auditoría de referencias tiene el punto, su «texto_final».
No se aplica nada con consejo reject, later o answered, ni los H-002…H-018
(L «0000»: corrigen el documento de Google del IEBH, no este texto).

Cómo:
  · SUSTITUCIÓN («antes» no vacío): «antes» se cambia por el texto final dentro
    de las líneas L..hasta del texto ACTUAL. Si un punto anterior ya cambió esas
    líneas y «antes» no está, se busca en el resto del texto y se registra un
    CONFLICTO; nunca se adivina en silencio. Orden: por línea y luego por id.
  · INSERCIÓN («antes» vacío): después de la línea L, como material del IEBH
    ({IEBH fuente="…"}), con los rótulos de los lotes («IEBH: », «[Nota IEBH] »,
    «Atestación (IEBH): »…) normalizados: el rótulo lo pone la etiqueta.
  · Filas «| … |» con L dentro de una tabla de Nandisena: se añaden a esa tabla,
    marcadas «| {IEBH} …»; cualquier otra inserción con L dentro de una tabla va
    después de la tabla.
  · L dentro de <<NOTAS>>: añadido del IEBH a esa nota ({IEBH} tras su línea).
  · El lote G (L1125) va en el orden «orden N» de su «seccion»; sus llamadas
    [^G-0NN] se numeran después de las notas de Nandisena.

Determinista: las mismas entradas dan el mismo texto, byte a byte.
"""

import glob
import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, "recursos", "compuestos", "texto-revisado.txt")
REGISTRO = os.path.join(RAIZ, "recursos", "compuestos", "aplicado.json")

VERSION = "0.2"
FECHA = "2026-10-17"
ESTADO_ES = "Borrador revisado (pendiente de aprobación del IEBH)"
ESTADO_EN = "Revised draft (pending IEBH approval)"
NOTA_VERSION = ("Se aplicaron las propuestas de revisión según el consejo verificado "
                "(correcciones, referencias y añadidos rotulados IEBH), a la espera de "
                "la aprobación del IEBH.")

# Notas propuestas como «[^n]: …» que ningún texto llama y que tienen un
# destino mejor que un párrafo suelto en su L. Cada una, con su porqué en el
# registro.
DESTINO_NOTA = {
    # el verificador la quiso como nota adjunta a la nota 11 (tagguṇa / atagguṇa):
    # en L0981, antes de la definición del bahubbīhi, no se entendería
    "I-014": ("nota", "11"),
}

# Colocación: además de la que da el verificador en su «nota» («Colocación: tras
# L0113…», que se lee sola), la que pidió el coordinador. Estos puntos se
# insertan al final, detrás de lo que ya haya en esa línea.
COLOCACION_EXTRA = {
    # C-012 partía «… los siguientes significados:» de su lista: va tras la lista (y tras C-019)
    "C-012": "0448",
}

# Referencias puras que se pliegan al rótulo, como las de las demás clases
# (A-012, B-001, F-001): «Compuesto copulativo (dvanda-samāsa) (Kacc. §329; …)».
PLEGAR_EN_ROTULO = {"G-001": "1125", "C-007": "0400"}

# Lo que una sustitución añade dentro de la frase de Nandisena y es del IEBH:
# se separa y va rotulado. (patrón, destino: «anexo» tras la línea, «anexo-tabla»
# tras la tabla, «nota» como añadido a la nota)
COLA_IEBH = {
    "F-016": (r"\.\s+(Cf\. «.*)$", ".", "anexo"),
    "C-030": (r" \((cf\. «[^»]*», [^()|]*\([^()]*\))\)", "", "anexo-tabla"),
    "A-002": (r" \((en la edición del Sexto Concilio[^()]*)\)(?=\.$)", "", "nota"),
}

# Fusiones editoriales (pedidas por el coordinador tras la verificación): quitan
# duplicados entre puntos o arreglan cortes. Cada una queda en el registro.
EDICIONES = {
    "I-001": [
        ("La resolución (viggaha) [IEBH]\nLa resolución (viggaha), también",
         "**La resolución (viggaha).** La resolución, también",
         "el rótulo pasa a entrada en negrita de su párrafo: como subtítulo abarcaba L0007–L0016"),
        ("Puesto que cada clase de compuesto tiene su propia forma de resolución, la resolución permite "
         "determinar a qué clase pertenece un compuesto (según Thitzana, p. 45). ", "",
         "repetía la última frase de Nandisena en L0005"),
        ("con samīpaṃ en lugar de upa («so ca niccasamāso ti assapadaviggaho», Rū. §330 (p. 176)).",
         "con samīpaṃ en lugar de upa (véase la nota 3).",
         "la cita de Rūpasiddhi queda sólo en el añadido de A-044 a la nota 3"),
    ],
    "I-010": [
        ("Rūpasiddhi da dos resoluciones del compuesto numérico colectivo: con el participio, «tayo lokā "
         "samāhaṭā cittena sampiṇḍitā», los tres mundos reunidos, juntados por la mente; y con el sustantivo "
         "y la sexta inflexión, «tiṇṇaṃ lokānaṃ samāhāro ti vā», o bien la reunión de los tres mundos "
         "(Rū. §348 (p. 190); Kacc. §325). Es esa palabra la que",
         "En las dos resoluciones de Rūpasiddhi (Rū. §348 (p. 190); Kacc. §325), es la palabra «samāhaṭā» "
         "o «samāhāro» la que",
         "las dos resoluciones ya las da D-005 justo antes (se conserva su traducción, «agrupados por la mente»)"),
    ],
    "S-005": [
        (" Así lo explica U Sīlānanda (clase de Rūpasiddhi n.º 42), de acuerdo con Suttaniddesa, que llama "
         "obligatorio al compuesto adverbial sólo «en la mayoría de los casos» (yebhūyyena) (Suttaniddesa, ad Kacc. §319).",
         " Así lo explica U Sīlānanda (clase de Rūpasiddhi n.º 42).",
         "el «yebhūyyena» de Suttaniddesa queda sólo en el añadido de A-044 a la nota 3"),
    ],
    "G-008": [
        ("por eso el compuesto está siempre en plural,",
         "por eso el compuesto está siempre en plural [salvo cuando depende de «yuga», par: véase la nota],",
         "la nota 14 da el singular «Sāriputtamoggallānaṃ … sāvakayugaṃ» (D. ii 4) y Sad. (Smith p. 768)"),
        ("etc. (Rū. §357)\n", "etc. (Rū. §357)[^G-009]\n",
         "la llamada a la nota 14 pasa al párrafo que dice «siempre en plural»"),
        ("(Kacc. §404; Rū. §370).[^G-009]", "(Kacc. §404; Rū. §370).",
         "(la llamada, movida al párrafo anterior)"),
    ],
    "C-019": [
        ("IEBH: Mera partícula (nipātamatta):", "IEBH: Otro sentido, fuera de la lista: mera partícula (nipātamatta):",
         "deja claro que es un sentido añadido a la lista de Nandisena"),
    ],
}

# El anexo que sale del corchete «[IEBH, …]» de una resolución, como frase entera.
ANEXO_TEXTO = {
    "E-021": "Según Niruttidīpanī: «guṇena adhiko guṇādhiko».",
    "E-022": "La palabra «sampayuttaṃ» de la resolución es de Niruttidīpanī.",
}

# Llamadas de Nandisena que se mueven (coordinador): la nota 11 habla ya de toda
# la clase, no sólo del subtipo (i).
MOVER_LLAMADAS = [("11", "0994", "0992", "la nota 11 (con F-018 y F-043) habla del compuesto relativo entero")]

# Rótulos de los lotes: se quitan del texto (la etiqueta IEBH ya lo dice); el
# tipo, si lo hay, queda como «clase» del bloque.
ROTULOS = [
    (r"\*Nota \(IEBH\)\.\*\s*", None),
    (r"\[(?:Nota|Añadido) IEBH\]\s*", None),
    (r"\[IEBH\]\s*", None),
    (r"Nota \(IEBH\):\s*", None),
    (r"Nota \(IEBH\)\s+(?=sobre\b)", None),
    (r"Atestaci[oó]n(es)? \(IEBH\):\s*", "Atestación"),
    (r"Atestaci[oó]n(es)?:\s*", "Atestación"),
    (r"Referencia \(IEBH\):\s*", "Referencia"),
    (r"Referencia:\s*", "Referencia"),
    (r"IEBH[:.]\s*Tipiṭaka:\s*", "Atestación"),
    (r"Tipiṭaka:\s*", "Atestación"),
    (r"IEBH[:.]\s*", None),
]

OBRAS = [
    (r"\bRū\.|Rūpasiddhi", "Rūpasiddhi"),
    (r"\bKacc?\.|Kaccāyana", "Kaccāyana"),
    (r"\bSad\.|Saddanīti", "Saddanīti"),
    (r"\bNir\.|Niruttidīpanī", "Niruttidīpanī"),
    (r"Suttaniddesa", "Suttaniddesa"),
    (r"Nyāsa", "Nyāsa"),
    (r"Mogg-p-ṭ|[Pp]añcikā-ṭīkā", "Moggallāna-pañcikā-ṭīkā"),
    (r"Mogg\.|Moggallāna(?!-pañcikā)", "Moggallāna"),
    (r"Payogasiddhi", "Payogasiddhi"),
    (r"Thitzana", "Thitzana"),
    (r"Sīlānanda", "U Sīlānanda"),
    (r"Sīmavisodhanī", "Sīmavisodhanī"),
    (r"Bālāvatāra", "Bālāvatāra"),
    (r"Vis-ṭ\.|mahāṭīkā", "Visuddhimagga-mahāṭīkā"),
    (r"\b(?:D|M|S|A|Dh|Dhs|V|J|Thag|Thī|Sn|Ud|Vv|Ap|Bv|Pu|Nidd|Paṭṭh|Vis)\. [ivxI0-9]", "Tipiṭaka"),
    (r"\b(?:DA|SA|JA|VvA|ApA|ThīA)\. ", "Aṭṭhakathā"),
    (r"Tipiṭaka|en el canon|canon", "Tipiṭaka"),
]


def nfc(s):
    return unicodedata.normalize("NFC", s).replace("ṁ", "ṃ").replace("Ṁ", "Ṃ")


def html_a_md(s):
    s = re.sub(r"</?b>", "**", s)
    s = re.sub(r"</?i>", "*", s)
    return re.sub(r"<[^>]+>", "", s)


# ---------------------------------------------------------------- entradas

def cargar(trabajo):
    props, ver = {}, {}
    for f in sorted(glob.glob(os.path.join(trabajo, "propuestas", "lote-*.json"))):
        for x in json.load(open(f, encoding="utf-8")):
            props[x["id"]] = x
    for f in sorted(glob.glob(os.path.join(trabajo, "verificacion", "verif-*.json"))):
        for x in json.load(open(f, encoding="utf-8")):
            ver[x["id"]] = x
    aud = {x["id"]: x for x in json.load(open(os.path.join(
        trabajo, "verificacion", "auditoria-refs.json"), encoding="utf-8"))}
    ov = json.load(open(os.path.join(trabajo, "revision", "overrides.json"), encoding="utf-8"))
    extra = json.load(open(os.path.join(trabajo, "revision", "extra.json"), encoding="utf-8"))
    return props, ver, aud, ov, extra


def puntos(props, ver, aud, ov, extra):
    """Los puntos que se aplican, con su texto final; y los que no, con el porqué."""
    aplicar, no = [], []
    for i in sorted(props):
        p, v = props[i], ver[i]
        consejo = ov[i]["rec"] if i in ov else v["consejo"]
        if p["L"] == "0000":
            no.append({"id": i, "motivo": "L 0000: corrige el documento de Google del IEBH, no este texto"})
            continue
        if consejo not in ("approve", "amend"):
            no.append({"id": i, "motivo": "consejo «{0}»{1}: {2}".format(
                consejo, " (overrides.json)" if i in ov else "",
                (ov[i]["why"] if i in ov else v.get("por_que", ""))[:200])})
            continue
        if i in aud:
            texto, origen = aud[i]["texto_final"], "auditoría"
        elif v["consejo"] == "amend" and v.get("enmienda", "").strip():
            texto, origen = v["enmienda"], "enmienda"
        else:
            texto, origen = p["despues"], "propuesta"
        L = p["L"]
        hasta = L
        if "-" in L:
            L, hasta = L.split("-", 1)
        aplicar.append({"id": i, "L": L, "hasta": hasta, "tipo": p["tipo"],
                        "seccion": p.get("seccion", ""), "antes": nfc(p["antes"]),
                        "texto": nfc(texto), "origen": origen, "consejo": consejo,
                        "fuentes": p.get("fuentes", [])})
    for x in extra:
        it, adv = x["item"], x["adv"]
        if it["id"] == "T-004":
            aplicar.append({"id": "T-004", "L": it["lin"], "hasta": it["lin"], "tipo": "nota",
                            "seccion": it["pref"], "antes": "",
                            "texto": nfc(html_a_md(it["prop"])), "origen": "extra.json",
                            "consejo": adv["rec"], "fuentes": []})
        else:
            motivo = {"T-001": "ya aplicada (decisión del IEBH del 16 de octubre)",
                      "T-002": "la hace el conversor (voces pāḷi en cursiva)",
                      "T-003": "forma de las referencias: la aplican los puntos auditados",
                      "T-005": "sin respuesta del IEBH: las citas de Saddanīti quedan como en los puntos",
                      "T-006": "sin respuesta del IEBH: las citas de U Sīlānanda quedan como en los puntos",
                      }.get(it["id"], "punto K: es de otra página")
            no.append({"id": it["id"], "motivo": motivo})
    return aplicar, no


# ---------------------------------------------------------------- el texto

class Texto:
    """El texto base por líneas, con lo que se le inserta detrás de cada una."""

    def __init__(self, ruta):
        self.cab = []
        self.L = []           # orden de las líneas originales
        self.c = {}           # L → contenido actual («{Normal} …», «| … |», «[^n]: …»)
        self.orig = {}
        self.tras = {}        # L → lista de líneas insertadas detrás
        self.tablas = []      # (desde, hasta)
        self.notas_desde = None
        abierta = None
        for crudo in open(ruta, encoding="utf-8"):
            crudo = nfc(crudo.rstrip("\n"))
            m = re.match(r"^(\d{4})  (.*)$", crudo)
            if not m:
                if crudo.strip() == "<<NOTAS>>":
                    self.notas_desde = self.L[-1] if self.L else "0000"
                    self.L.append("NOTAS")
                    self.c["NOTAS"] = self.orig["NOTAS"] = "<<NOTAS>>"
                elif not self.L:
                    self.cab.append(crudo)
                continue
            L, r = m.groups()
            self.L.append(L)
            self.c[L] = self.orig[L] = r
            if r.strip() == "<<NOTAS>>":
                self.notas_desde = L
            if r.startswith("<<TABLA"):
                abierta = L
            elif r.startswith("<</TABLA"):
                self.tablas.append((abierta, L))
                abierta = None

    def en_notas(self, L):
        return self.notas_desde is not None and L > self.notas_desde

    def tabla_de(self, L):
        for a, b in self.tablas:
            if a <= L <= b:
                return a, b
        return None

    def rango(self, L, hasta):
        return [x for x in self.L if x != "NOTAS" and L <= x <= hasta]

    def insertar(self, L, lineas):
        self.tras.setdefault(L, []).extend(lineas)

    def escribir(self):
        out = list(self.cab)
        for L in self.L:
            if L == "NOTAS":
                out.append("<<NOTAS>>")
                continue
            out.append("{0}  {1}".format(L, self.c[L]))
            for k, (estilo, txt) in enumerate(self.tras.get(L, [])):
                Lk = L + sufijo(k)
                if self.en_notas(L):
                    out.append("{0}  {1}".format(Lk, (estilo + " " + txt).strip()))
                elif estilo is None:          # una fila o una marca de tabla
                    out.append("{0}  {1}".format(Lk, txt))
                else:
                    out.append("{0}  {1}".format(Lk, (estilo + " " + txt).rstrip() if txt else estilo + " "))
        return "\n".join(out) + "\n"


def sufijo(k):
    """0 → a … 25 → z, 26 → aa, 27 → ab … (base 26 biyectiva: sin colisiones)."""
    s = ""
    k += 1
    while k:
        k, r = divmod(k - 1, 26)
        s = "abcdefghijklmnopqrstuvwxyz"[r] + s
    return s


# ---------------------------------------------------------------- rótulos y fuentes

def quitar_rotulo(t):
    """(texto sin el rótulo de lote, clase o None, fuente del rótulo o None)."""
    clase, fuente = None, None
    m0 = None
    for pat, cl in ROTULOS:
        m = m0 = re.match(pat, t)
        if m:
            t = t[m.end():]
            clase = clase or cl
            break
    # «Otros ejemplos (IEBH, Rū., p. 201).» → «Otros ejemplos (Rū., p. 201).»
    m = re.match(r"^([^()«»]{0,40}?)\s*\(IEBH,\s*([^()]*(?:\([^()]*\))?[^()]*)\)", t)
    if m:
        fuente = m.group(2).strip()
        t = "{0} ({1}){2}".format(m.group(1), fuente, t[m.end():])
    # «La resolución (viggaha) [IEBH]» → «La resolución (viggaha)»
    t = re.sub(r"\s*\[IEBH\]\s*$", "", t)
    t = re.sub(r"\s*\[IEBH\]\s*", " ", t)
    if t and t[0].islower() and (m0 is not None):
        t = t[0].upper() + t[1:]
    if t.startswith("sobre "):
        t = "S" + t[1:]
    return t.strip(), clase, fuente


def obras(texto, fuentes_prop=()):
    """Las obras citadas en el texto, para la fuente del bloque."""
    vistas = []
    for pat, nombre in OBRAS:
        if re.search(pat, texto) and nombre not in vistas:
            vistas.append(nombre)
    if not vistas and fuentes_prop:
        # las obras de las fuentes de la propuesta (sin «base.txt» ni lo publicado)
        citas = " ".join("{0} {1}".format(f.get("obra") or "", f.get("ref") or "") for f in fuentes_prop
                         if "base.txt" not in (f.get("obra") or "") and "publicad" not in (f.get("obra") or ""))
        for pat, nombre in OBRAS:
            if re.search(pat, citas) and nombre not in vistas:
                vistas.append(nombre)
    return " · ".join(vistas) or "IEBH"


def estilo_iebh(fuente, forma=None, clase=None):
    s = '{IEBH fuente="' + fuente.replace('"', "'") + '"'
    if forma:
        s += " forma=" + forma
    if clase:
        s += ' clase="' + clase + '"'
    return s + "}"


# ---------------------------------------------------------------- bloques del IEBH

GLOSA = re.compile(r"\(([^()]*)\)")


def glosas(t):
    return len(GLOSA.findall(t))


def es_cabecera_par(linea, siguiente):
    return (bool(re.match(r"^[^\s():.,;\"«»]+$", linea.strip()))
            and siguiente is not None and glosas(siguiente) >= 2)


def es_titulo(linea):
    s = linea.strip()
    s2 = s.strip('"»«').rstrip()
    return (0 < len(s) <= 80 and not s.startswith("|") and not s.startswith("[^")
            and s2[-1] not in ".,;:" and "«" not in s and not re.match(r"^\S+$", s))


def partir_resolucion(linea, comp):
    """Separa de una línea de resolución lo que sigue a la glosa del compuesto
    («… dasabalo Bhagavā (el Sublime…) (Kacc. §328). «Punāparaṃ…», Bv. 346»):
    (resolución, resto). Cuenta la ÚLTIMA aparición del compuesto: en
    «suvaṇṇavaṇṇo (el color dorado) viya … suvaṇṇavaṇṇo Bhagavā (…)» la
    primera es un miembro."""
    i, fin = 0, None
    corte = linea.find("«")          # una cita (atestación) no es la resolución
    for m in GLOSA.finditer(linea if corte < 0 else linea[:corte]):
        antes = linea[i:m.start()]
        i = m.end()
        if comp in antes.replace(",", " ").split():
            fin = i
    if fin is None:
        return linea, ""
    # una referencia entre paréntesis pegada a la resolución se queda con ella
    m = re.match(r"\s*\((?:Kacc?|Rū|Sad|Nir)\.[^()]*\)", linea[fin:])
    if m:
        fin += m.end()
    resto = linea[fin:].strip()
    if resto in ("", ".", ")."):
        return linea, ""
    return linea[:fin] + ".", resto.lstrip(".").strip()


def lineas_iebh(texto, fuente, clase=None, llamadas=None):
    """Una inserción (posiblemente de varias líneas) → [(estilo, texto)].
    Los párrafos van entre líneas en blanco; el par «voz» + «resolución» de un
    bahubbīhi, junto; las tablas, como <<TABLA IEBH>>. llamadas: {«G-005»: «13»}."""
    out = []
    blanco = ("{Normal}", "")

    def nl(estilo, t):
        if llamadas:
            t = re.sub(r"\[\^([A-Z]-\d{3})\]", lambda m: "[^" + llamadas.get(m.group(1), m.group(1)) + "]", t)
        out.append((estilo, t))

    trozos = re.split(r"\n\s*\n", texto.strip("\n"))
    primero = True
    ultimo_par = None          # una vez: la llamada tras una tabla va al párrafo anterior
    verso = None               # índice de un verso que espera su traducción
    for trozo in trozos:
        lineas = [x.rstrip() for x in trozo.split("\n") if x.strip()]
        k = 0
        while k < len(lineas):
            ln = lineas[k]
            # una tabla
            if ln.strip().startswith("<<TABLA"):
                filas = []
                k += 1
                while k < len(lineas) and not lineas[k].strip().startswith("<</TABLA"):
                    filas.append(lineas[k].strip())
                    k += 1
                cierre = lineas[k].strip() if k < len(lineas) else "<</TABLA>>"
                k += 1
                llamada = cierre[len("<</TABLA>>"):].strip()
                if llamada and ultimo_par is None:
                    raise SystemExit("✗ llamada tras una tabla sin párrafo donde ponerla: " + llamada)
                if llamada:
                    # la llamada tras la tabla, al final del párrafo que la presenta
                    e, t = out[ultimo_par]
                    out[ultimo_par] = (e, t + llamada if not llamadas else t + re.sub(
                        r"\[\^([A-Z]-\d{3})\]", lambda m: "[^" + llamadas.get(m.group(1), m.group(1)) + "]", llamada))
                out.append(blanco)
                out.append((None, '<<TABLA IEBH fuente="' + fuente + '">>'))
                for f in filas:
                    out.append((None, f))
                out.append((None, "<</TABLA>>"))
                out.append(blanco)
                continue
            # filas sueltas (sin marcas de tabla): una tabla nueva
            if ln.strip().startswith("|"):
                out.append(blanco)
                out.append((None, '<<TABLA IEBH fuente="' + fuente + '">>'))
                while k < len(lineas) and lineas[k].strip().startswith("|"):
                    out.append((None, lineas[k].strip()))
                    k += 1
                out.append((None, "<</TABLA>>"))
                out.append(blanco)
                continue
            sig = lineas[k + 1] if k + 1 < len(lineas) else None
            # el par «voz» / «resolución» de un bahubbīhi
            if es_cabecera_par(ln, sig):
                comp = ln.strip()
                res, resto = partir_resolucion(sig.strip(), comp)
                out.append(blanco)
                nl(estilo_iebh(fuente), comp)
                nl(estilo_iebh(fuente), res)
                if resto:
                    nl(estilo_iebh(fuente, "anexo"), resto)
                out.append(blanco)
                k += 2
                continue
            t, cl, f = quitar_rotulo(ln)
            # un verso: varias líneas cortas seguidas
            cortas = []
            j = k
            while (j < len(lineas) and len(lineas[j]) <= 70 and not lineas[j].strip().startswith("|")
                   and not es_titulo(lineas[j])
                   and not es_cabecera_par(lineas[j], lineas[j + 1] if j + 1 < len(lineas) else None)):
                cortas.append(lineas[j].strip())
                j += 1
            if len(cortas) >= 2:
                # un verso: con el párrafo que lo presenta («… en un verso:») y su
                # traducción (el párrafo siguiente), una sola unidad
                entrada = ""
                while out and out[-1] == blanco:
                    out.pop()
                if out and out[-1][0] and "forma=p" in out[-1][0] and out[-1][1].rstrip().endswith(":"):
                    entrada = out.pop()[1]
                out.append(blanco)
                versos = " // ".join(x.strip('"') for x in cortas)
                nl(estilo_iebh(fuente, "verso", cl or clase), entrada + " ‖ " + versos + " ‖ ")
                verso = len(out) - 1
                ultimo_par = None
                out.append(blanco)
                k = j
                primero = False
                continue
            if es_titulo(t) and (len(lineas) > 1 or len(trozos) > 1):
                out.append(blanco)
                nl(estilo_iebh(fuente, "h"), t)
                out.append(blanco)
            elif verso is not None:
                e, tv = out[verso]
                out[verso] = (e, tv + t)        # la traducción del verso
                verso = None
            else:
                out.append(blanco)
                nl(estilo_iebh(fuente, "p", cl or clase), t)
                ultimo_par = len(out) - 1
                out.append(blanco)
            primero = False
            k += 1
    # sin blancos repetidos
    limpio = []
    for x in out:
        if x == blanco and limpio and limpio[-1] == blanco:
            continue
        limpio.append(x)
    return limpio


# ---------------------------------------------------------------- aplicar

def orden_g(p, por_id):
    m = re.search(r"orden (\d+)", p["seccion"])
    if m:
        return float(m.group(1))
    m = re.search(r"nota a ([A-Z]-\d{3})", p["seccion"])
    if m and m.group(1) in por_id:
        return orden_g(por_id[m.group(1)], por_id) + 0.5
    return 0.0


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    trabajo = argv[1]
    props, ver, aud, ov, extra = cargar(trabajo)
    items, no_aplicados = puntos(props, ver, aud, ov, extra)
    T = Texto(os.path.join(trabajo, "base.txt"))
    registro = []
    conflictos = []
    fusiones = []

    # las fusiones editoriales, sobre el texto final de cada punto
    for it in items:
        for viejo, nuevo, motivo in EDICIONES.get(it["id"], []):
            if viejo not in it["texto"]:
                raise SystemExit("✗ fusión editorial de {0}: no está «{1}»".format(it["id"], viejo[:60]))
            it["texto"] = it["texto"].replace(viejo, nuevo, 1)
            fusiones.append({"id": it["id"], "antes": viejo, "despues": nuevo, "motivo": motivo})
    # la colocación que pide el verificador en su «nota» (o el coordinador)
    for it in items:
        nota = (ver.get(it["id"]) or {}).get("nota") or ""
        m = re.search(r"Colocación:[^.]*?\bL(\d{4})", nota)
        destino = COLOCACION_EXTRA.get(it["id"]) or (m.group(1) if m and not it["antes"] else None)
        if destino:
            it["colocar"] = destino

    def modo(como):
        for pref, m in [("CONFLICTO", "conflicto"), ("sustitución convertida", "convertida en inserción"),
                        ("sustitución de fila", "fila del resumen rellenada"),
                        ("sustitución", "sustitución"), ("añadido del IEBH a la nota", "añadido a una nota"),
                        ("añadido del IEBH tras", "añadido separado de la frase"),
                        ("fila(s)", "filas añadidas a una tabla"), ("nota al pie nueva", "nota al pie nueva"),
                        ("nota «[^n]» sin llamada → añadido", "añadido a una nota"),
                        ("nota «[^n]» sin llamada", "nota sin llamada → párrafo"),
                        ("referencia sola", "anexo a una tarjeta"), ("referencia plegada", "referencia plegada al rótulo"),
                        ("inserción", "inserción")]:
            if como.startswith(pref):
                return m
        return "otro"

    def log(it, como, **kw):
        d = {"id": it["id"], "L": it["L"] + ("-" + it["hasta"] if it["hasta"] != it["L"] else ""),
             "tipo": it["tipo"], "origen": it["origen"], "modo": modo(como), "como": como,
             "texto": it.get("aplicado", it["texto"])}
        if it.get("L_propuesta"):
            d["L"] = it["L_propuesta"]
            d["colocado_tras"] = "L" + it["L"]
            d["como"] += " (colocado tras L{0}, como pide {1})".format(
                it["L"], "el coordinador" if it["id"] in COLOCACION_EXTRA else "la verificación")
        d.update(kw)
        registro.append(d)

    # las notas del lote G (y las del S que las comentan): las que se llaman
    # con [^X-0NN] se numeran en el orden de las llamadas
    todo = "\n".join(it["texto"] for it in items)
    llamadas = {}
    sig_nota = 12
    por_id = {it["id"]: it for it in items}
    g_items = sorted([it for it in items if it["L"] == "1125" and not it["antes"]],
                     key=lambda it: (orden_g(it, por_id), it["id"]))
    for it in g_items:
        for m in re.finditer(r"\[\^([A-Z]-\d{3})\]", it["texto"]):
            if m.group(1) not in llamadas:
                llamadas[m.group(1)] = str(sig_nota)
                sig_nota += 1
    llamadas_otras = set(re.findall(r"\[\^([A-Z]-\d{3})\]", todo)) - set(llamadas)
    if llamadas_otras:
        print("⚠ llamadas a notas fuera del lote G: " + ", ".join(sorted(llamadas_otras)))

    orden = sorted(items, key=lambda it: (it["L"], it["id"]))
    # el lote G, en su orden propio, al llegar a L1125
    orden = [it for it in orden if it not in g_items]
    k = next((n for n, it in enumerate(orden) if it["L"] > "1125"), len(orden))
    orden = orden[:k] + g_items + orden[k:]

    # los que tienen colocación propia, al final: detrás de lo que ya haya en su línea
    diferidos = [it for it in orden if it.get("colocar")]
    orden = [it for it in orden if not it.get("colocar")] + diferidos
    for it in diferidos:
        it["L_propuesta"] = it["L"]
        it["L"] = it["hasta"] = it["colocar"]

    for it in orden:
        L, hasta, antes, texto = it["L"], it["hasta"], it["antes"], it["texto"]
        fuente = obras(texto, it["fuentes"])

        # ---- sustituciones
        if antes:
            resto_iebh = None
            anexo = None
            t_rot = quitar_rotulo(texto)
            if antes not in texto and t_rot[0] != texto and not texto.startswith(antes):
                # el texto final ya no es una corrección de la frase sino una nota
                # aparte (el verificador lo pide así: A-001)
                lineas = lineas_iebh(texto, fuente, llamadas=llamadas)
                T.insertar(hasta, lineas)
                log(it, "sustitución convertida en inserción del IEBH (el verificador la saca de la frase de Nandisena)")
                continue
            if texto.startswith(antes):
                cola = texto[len(antes):].strip()
                if cola and re.match(r"^(\[(Nota )?IEBH[^\]]*\]|IEBH[:.])", cola):
                    resto_iebh = cola
                    texto = antes
            m = re.search(r"\s*\[IEBH[,:][^\]]*\]\s*$", texto)
            if m:
                anexo = re.sub(r"^\[IEBH[,:]\s*", "", m.group(0).strip())[:-1].strip()
                anexo = ANEXO_TEXTO.get(it["id"], anexo)
                texto = texto[:m.start()]
            cola = None
            if it["id"] in COLA_IEBH:
                pat, sust, destino_cola = COLA_IEBH[it["id"]]
                m = re.search(pat, texto)
                if not m:
                    raise SystemExit("✗ {0}: no se encuentra la parte del IEBH".format(it["id"]))
                cola = m.group(1).strip()
                cola = cola[0].upper() + cola[1:]
                if not cola.endswith("."):
                    cola += "."
                texto = texto[:m.start()] + sust + texto[m.end():]
                if texto == antes:
                    resto_iebh = None
            rng = T.rango(L, hasta)
            actual = "\n".join(T.c[x] for x in rng)
            if (resto_iebh is not None or cola) and texto == antes:
                pass                      # sólo el añadido
            elif antes in actual:
                nuevo = actual.replace(antes, texto, 1)
                partes = nuevo.split("\n")
                if len(partes) != len(rng):
                    conflictos.append({"id": it["id"], "problema": "cambia el número de líneas", "resuelto": "no aplicado"})
                    log(it, "CONFLICTO: no aplicado")
                    continue
                for x, s in zip(rng, partes):
                    T.c[x] = s
            else:
                # ¿lo cambió un punto anterior?
                original = "\n".join(T.orig[x] for x in rng)
                previo = [r["id"] for r in registro if r.get("lineas") and set(r["lineas"]) & set(rng)]
                donde = [x for x in T.L if x != "NOTAS" and antes in T.c[x]]
                if texto in actual:
                    conflictos.append({"id": it["id"], "problema": "«antes» ya no está en L{0}; el texto final ya está (lo puso {1})".format(
                        L, ", ".join(previo) or "otro punto"), "resuelto": "nada que hacer"})
                    log(it, "CONFLICTO: ya aplicado por otro punto", lineas=rng)
                    continue
                if len(donde) == 1:
                    x = donde[0]
                    T.c[x] = T.c[x].replace(antes, texto, 1)
                    conflictos.append({"id": it["id"], "problema": "«antes» no está en L{0}{1}; está en L{2}".format(
                        L, " (cambiado antes por " + ", ".join(previo) + ")" if previo else "", x),
                        "resuelto": "aplicado en L" + x})
                    log(it, "sustitución (CONFLICTO resuelto: aplicada en L{0})".format(x), lineas=[x])
                    rng = [x]
                else:
                    conflictos.append({"id": it["id"], "problema": "«antes» no está en L{0}{1}{2}".format(
                        L, " (cambiado antes por " + ", ".join(previo) + ")" if previo else "",
                        "" if antes in original else "; tampoco en el texto base"),
                        "resuelto": "NO aplicado: " + ("aparece en varias líneas" if donde else "no está en el texto")})
                    log(it, "CONFLICTO: no aplicado")
                    continue
            como = "sustitución"
            # las filas que el IEBH rellena en la tabla del resumen: marcadas IEBH
            # sólo las celdas que estaban vacías y ya no lo están
            if it["tipo"] == "añadido" and T.tabla_de(L) and T.c[L].startswith("| "):
                a_c = [c.strip() for c in antes.strip().strip("|").split("|")]
                n_c = [c.strip() for c in T.c[L].strip().strip("|").split("|")]
                cel = [str(i) for i, (x, y) in enumerate(zip(a_c, n_c)) if not x and y]
                T.c[L] = '| {IEBH fuente="' + fuente + '" celdas="' + ",".join(cel) + '"} ' + T.c[L][2:]
                como = "sustitución de fila (celdas {0} marcadas IEBH)".format(",".join(cel))
            if cola:
                if destino_cola == "nota":
                    T.insertar(L, [(estilo_iebh(obras(cola, it["fuentes"])), cola)])
                else:
                    pos = T.tabla_de(L)[1] if destino_cola == "anexo-tabla" else hasta
                    T.insertar(pos, [(estilo_iebh(obras(cola, it["fuentes"]), "anexo", "Atestación"
                                                  if destino_cola != "nota" else None), cola)])
                como += " + la parte del IEBH, separada y rotulada («" + cola[:40] + "…»)"
            if resto_iebh is not None:
                t, cl, f = quitar_rotulo(resto_iebh)
                if T.en_notas(L):
                    T.insertar(L, [(estilo_iebh(obras(t, it["fuentes"])), t)])
                    como = "añadido del IEBH a la nota" if texto == antes else como + " + añadido del IEBH a la nota"
                else:
                    T.insertar(hasta, lineas_iebh(t, obras(t, it["fuentes"]), cl))
                    como = "añadido del IEBH tras la línea (separado de la frase de Nandisena)"
            if anexo:
                T.insertar(hasta, [(estilo_iebh(obras(anexo, it["fuentes"]), "anexo"), anexo)])
                como += " + anexo del IEBH a la tarjeta («" + anexo[:40] + "…»)"
            it["aplicado"] = (texto + ((" ‖ " + resto_iebh) if resto_iebh else "") + ((" ‖ " + anexo) if anexo else "")
                              + ((" ‖ " + cola) if cola else ""))
            log(it, como, lineas=rng)
            continue

        # ---- inserciones
        cuerpo = texto
        if it["id"] in PLEGAR_EN_ROTULO:
            Lr = PLEGAR_EN_ROTULO[it["id"]]
            t = re.sub(r"^\[\^\w+\]:\s*", "", cuerpo)
            t, cl, f = quitar_rotulo(t)
            t = t.rstrip(". ")
            pre, _, rot = T.c[Lr].partition("} ")
            T.c[Lr] = pre + "} " + rot.rstrip(". ") + " (" + t + ")"
            it["aplicado"] = t
            log(it, "referencia plegada al rótulo L{0}, como en las demás clases".format(Lr), lineas=[Lr])
            continue
        if it["id"] in DESTINO_NOTA:
            _, n = DESTINO_NOTA[it["id"]]
            t = re.sub(r"^\[\^\w+\]:\s*", "", cuerpo)
            t, cl, f = quitar_rotulo(t)
            Ln = next(x for x in T.L if x != "NOTAS" and T.c[x].startswith("[^{0}]:".format(n)))
            T.insertar(Ln, [(estilo_iebh(obras(t, it["fuentes"])), t)])
            log(it, "nota «[^n]» sin llamada → añadido del IEBH a la nota {0} (como pidió el verificador)".format(n))
            continue
        m = re.match(r"^\[\^(\w+)\]:\s*", cuerpo)
        if m:
            t = cuerpo[m.end():]
            t, cl, f = quitar_rotulo(t)
            if it["id"] in llamadas:
                n = llamadas[it["id"]]
                T.insertar(L, [(estilo_iebh(obras(t, it["fuentes"]), None).replace("{IEBH ", "{IEBH-nota ", 1),
                                "[^{0}]: {1}".format(n, t))])
                log(it, "nota al pie nueva del IEBH, n.º {0}".format(n))
            else:
                T.insertar(L, lineas_iebh(t, obras(t, it["fuentes"]), cl))
                log(it, "nota «[^n]» sin llamada → párrafo del IEBH en L{0}".format(L))
            continue
        if T.en_notas(L):
            t, cl, f = quitar_rotulo(cuerpo)
            T.insertar(L, [(estilo_iebh(obras(t, it["fuentes"])), t)])
            log(it, "añadido del IEBH a la nota de L{0}".format(L))
            continue
        tab = T.tabla_de(hasta)
        lineas_txt = [x for x in cuerpo.split("\n") if x.strip()]
        if tab and all(x.strip().startswith("|") for x in lineas_txt):
            # filas para una tabla de Nandisena: detrás de la fila L
            pos = hasta if hasta != tab[1] else T.L[T.L.index(tab[1]) - 1]
            filas = [(None, '| {IEBH fuente="' + fuente + '"} ' + x.strip()[1:].lstrip()) for x in lineas_txt]
            T.insertar(pos, filas)
            log(it, "fila(s) del IEBH añadida(s) a la tabla L{0}–L{1}, tras L{2}".format(tab[0], tab[1], pos))
            continue
        if re.match(r"^\([^()]*\)$", cuerpo.strip()):
            T.insertar(hasta, [(estilo_iebh(obras(cuerpo, it["fuentes"]), "anexo"), cuerpo.strip())])
            log(it, "referencia sola → anexo del IEBH a la tarjeta de L{0}".format(hasta))
            continue
        pos = tab[1] if tab else hasta
        lineas = lineas_iebh(cuerpo, fuente, llamadas=llamadas)
        T.insertar(pos, lineas)
        log(it, "inserción del IEBH tras L{0}{1}".format(pos, " (después de la tabla L{0}–L{1})".format(*tab) if tab else ""))

    # llamadas de Nandisena que se mueven
    for n, de, a, motivo in MOVER_LLAMADAS:
        llamada = "[^{0}]".format(n)
        if llamada not in T.c[de]:
            raise SystemExit("✗ la llamada {0} no está en L{1}".format(llamada, de))
        T.c[de] = T.c[de].replace(llamada, "", 1)
        T.c[a] = T.c[a].rstrip() + llamada
        fusiones.append({"id": "nota " + n, "antes": "llamada en L" + de, "despues": "llamada al final de L" + a,
                         "motivo": motivo})

    # la cabecera del texto revisado
    T.cab = [
        "# samasa6.doc — texto REVISADO (U Nandisena, 2004–2005; revisión del IEBH)",
        "# Lo escribe herramientas/compuestos_aplicar.py a partir de base.txt y de las",
        "# propuestas verificadas. No se edita a mano: se rehace.",
        "#meta version=" + VERSION,
        "#meta fecha=" + FECHA,
        "#meta estado=" + ESTADO_ES,
        "#meta estado_en=" + ESTADO_EN,
        "#meta nota_version=" + NOTA_VERSION,
        "",
    ]
    s = nfc(T.escribir())
    # toda nota con una llamada, y toda llamada con su nota
    defs = re.findall(r"\[\^(\w+)\]:", s)
    calls = re.findall(r"\[\^(\w+)\](?!:)", s)
    malas = sorted({n for n in defs if calls.count(n) != 1} | {n for n in calls if n not in defs})
    if malas or len(defs) != len(set(defs)):
        raise SystemExit("✗ notas sin llamada única o llamadas sin nota: " + ", ".join(malas))
    open(DESTINO, "w", encoding="utf-8").write(s)
    # post-paso: sandhi en edición moderna (EM) de las citas pāḷi, según
    # recursos/compuestos/sandhi-em.json (decisión del IEBH, 2026-10-17).
    # Va después de escribir: así una nueva pasada no pierde ese trabajo.
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import compuestos_sandhi_em
    compuestos_sandhi_em.aplicar(solo="texto-revisado.txt")

    from collections import Counter
    cuenta = Counter(r["modo"] for r in registro)
    rg = {"version": VERSION, "fecha": FECHA,
          "aplicados": len(registro), "por_tipo": dict(Counter(r["tipo"] for r in registro)),
          "por_modo": dict(sorted(cuenta.items())),
          "conflictos": conflictos, "fusiones_editoriales": fusiones, "no_aplicados": no_aplicados,
          "llamadas_G": llamadas, "registro": registro}
    open(REGISTRO, "w", encoding="utf-8").write(json.dumps(rg, ensure_ascii=False, indent=1) + "\n")
    print("→ {0} ({1} puntos aplicados, {2} conflictos, {3} sin aplicar)".format(
        os.path.relpath(DESTINO, RAIZ), len(registro), len(conflictos), len(no_aplicados)))
    for c in conflictos:
        print("  ⚠ {id}: {problema} → {resuelto}".format(**c))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
