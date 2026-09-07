#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audita las derivaciones paso a paso de un capítulo de Kaccāyana.

    python3 herramientas/auditar_derivaciones.py
    python3 herramientas/auditar_derivaciones.py kaccayana/02-nama-kappa.md
    python3 herramientas/auditar_derivaciones.py --comprobacion recomposicion
    python3 herramientas/auditar_derivaciones.py --detalle

Es el equivalente nominal de `auditar_secuencias.py`: allí se comprueban las
secuencias de sandhi de recursos/sandhi/reglas.json; aquí, las derivaciones
en prosa de la forma

    **Ādiṃ** = ādi + smiṃ (‘smiṃ’ se sustituye por ‘aṃ’ (§69);
               ‘i’ de “ādi” recibe el nombre de ‘jha’ (§58);
               ‘aṃ’ se convierte en ‘ṃ’ (§82))

Hace cinco comprobaciones, de menor a mayor coste:

  0. TIPOGRAFÍA   — comillas simples o dobles sin cerrar dentro de un paso.
  1. SIN CITA     — pasos que no citan ningún §N.
  2. DIVERGENCIA  — una misma forma, con los MISMOS componentes, derivada en
                    dos sitios con cadenas distintas. Se comparan las
                    operaciones y sus §N, no la redacción: la comilla usada,
                    el verbo elegido, el orden de los pasos y las glosas que
                    no tocan la forma no cuentan como divergencia.
  3. CLASE        — ¿el sutta citado hace de veras esa CLASE de operación
                    —elidir, sustituir, acortar, nombrar…—? La clase de cada
                    sutta se lee de su propia traducción castellana en este
                    mismo archivo; para §1-§51 se toma la tabla revisada a
                    mano de `auditar_secuencias.py`.
  4. RECOMPOSICIÓN — se aplica la cadena a los componentes y se compara con
                    el lema. Es la que caza «ādi + smiṃ → ādaṃ» sin juicio
                    ninguno.

DOS LÍMITES, Y SE DECLARAN AQUÍ COMO LOS DECLARA EL GUION DE SANDHI:

  · No decide cuál de varios suttas correctos es la MEJOR cita. Que un paso
    pase la comprobación 3 sólo dice que el aforismo citado hace esa clase de
    cosa, no que sea el aforismo que toca.
  · No firma nada. Da candidatos; cada uno se le enseña al IEBH con su
    evidencia y su corrección propuesta, y firma él.

Y un tercero, propio de la comprobación 4: **donde un tipo de paso no está
implementado, el guion lo dice** —bucket «no simulable»— en lugar de dejarlo
pasar en silencio. Una derivación que no recompone es un CANDIDATO, no un
error probado: la cadena puede estar abreviada a propósito, o ilustrar lo que
un sutta NO hace (esas se apartan como «ilustrativas»).

AVISO SOBRE DÓNDE SE CORRIGE. En los capítulos 2, 3 y 4 el archivo de
`kaccayana/` es SALIDA: la fuente es su maestro de `docs/` y la rehace
`herramientas/convertir_<obra>.py`. El guion lee la salida —que es lo
publicado— pero avisa de dónde hay que tocar.
"""

import argparse
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POR_DEFECTO = os.path.join("kaccayana", "02-nama-kappa.md")

# Capítulos cuyo markdown de kaccayana/ es salida de un conversor.
CONVERTIDOS = {
    "02-nama-kappa.md": ("docs/2. Nāma-Kappa.md", "convertir_nama.py"),
    "03-karaka-kappa.md": ("docs/3. Kāraka-Kappa.md", "convertir_karaka.py"),
    "04-samasa-kappa.md": ("docs/4. Samāsa-Kappa.md", "convertir_samasa.py"),
}

NOMBRE_OP = {
    "elision": "elisión",
    "sustitucion": "sustitución",
    "acortamiento": "acortamiento",
    "alargamiento": "alargamiento",
    "nombre": "nombre (saññā)",
    "insercion": "inserción",
    "duplicacion": "duplicación",
    "sin_cambio": "sin cambio",
    "separacion": "separación",
    "union": "unión",
}

LARGAS = {"a": "ā", "i": "ī", "u": "ū"}
CORTAS = {v: k for k, v in LARGAS.items()}

COMILLAS = {"‘": "’", "“": "”"}


# ── Normalización ───────────────────────────────────────────────────────

def nfc(t):
    return unicodedata.normalize("NFC", t)


def desnudar(t):
    """Quita lo que no distingue una forma: espacios, apóstrofos, guiones."""
    t = nfc(t).lower()
    for c in " \t’'‘’ʼ-–—":
        t = t.replace(c, "")
    return t


def limpiar_md(t):
    """Deshace los escapes del markdown y las cursivas."""
    t = t.replace("\\=", "=").replace("\\+", "+").replace("\\[", "[")
    t = t.replace("\\]", "]").replace("\\.", ".").replace("\\!", "!")
    t = t.replace("\\-", "-").replace("\\_", "_")
    t = re.sub(r"\*([^*]+)\*", r"\1", t)
    return t


# ── Lectura del capítulo ────────────────────────────────────────────────

RE_SUTTA = re.compile(r"^\*\*(\d+)\\?\.\s")
RE_DERIV = re.compile(
    r"\*\*(?P<lema>[^*]+?)\*\*"
    r"(?P<mas>(?:\s*,\s*\*\*[^*]+?\*\*)*)"
    r"\s*\\=\s*(?P<comp>[^()]*?)\s*\((?P<resto>.*)$"
)
RE_LEMA_EXTRA = re.compile(r"\*\*([^*]+?)\*\*")


def bloque_parentesis(resto):
    """Devuelve el contenido del paréntesis ya abierto en `resto`."""
    hondo, buf = 1, []
    for ch in resto:
        if ch == "(":
            hondo += 1
        elif ch == ")":
            hondo -= 1
            if hondo == 0:
                return "".join(buf)
        buf.append(ch)
    return None


def partir_pasos(bloque):
    """Parte el bloque en pasos.

    El separador es ‘;’. Dentro de un mismo tramo, una ‘y’ que introduzca
    otra operación con su propia cita —«… (§179) y se inserta ‘s’ (§62)»—
    es otro paso.

    Si el segundo trozo no nombra operando —«‘si’ recibe el nombre de ‘ga’
    (§57) y se elide (§220)»—, es que lo comparte con el primero, y se le
    antepone para que se lea solo.
    """
    pasos = []
    for tramo in bloque.split(";"):
        trozos = re.split(r"\)\s+y\s+(?=se\s)", tramo)
        if len(trozos) > 1:
            trozos = [t if t.endswith(")") else t + ")" for t in trozos[:-1]] + [trozos[-1]]
        sujeto = None
        for pos, t in enumerate(trozos):
            t = t.strip()
            if not t:
                continue
            if pos == 0:
                m = re.match(r"\s*([‘“][^‘’“”]+[’”])", t)
                sujeto = m.group(1) if m else None
            elif sujeto and not re.search(r"[‘“]", t):
                t = "{0} {1}".format(sujeto, t)
            pasos.append(t)
    return pasos


def citas(paso):
    return [int(x) for x in re.findall(r"§(\d+)", paso)]


def leer_capitulo(ruta):
    """Devuelve (suttas, derivaciones).

    suttas: {n: {"linea", "pali", "castellano"}}
    derivaciones: lista de dicts con lema(s), componentes y pasos.
    """
    texto = open(ruta, encoding="utf-8").read()
    lineas = texto.split("\n")

    suttas, derivaciones = {}, []
    actual = None
    for i, linea in enumerate(lineas):
        m = RE_SUTTA.match(linea)
        if m:
            actual = int(m.group(1))
            suttas.setdefault(actual, {"linea": i + 1, "pali": [], "castellano": []})
            continue
        for mm in RE_DERIV.finditer(linea):
            if "\\+" not in mm.group("comp"):
                continue
            bloque = bloque_parentesis(mm.group("resto"))
            if bloque is None:
                continue
            quita_nota = lambda t: re.sub(r"\[\^\d+\]", "", limpiar_md(t)).strip()
            lemas = [quita_nota(mm.group("lema"))]
            lemas += [quita_nota(x) for x in RE_LEMA_EXTRA.findall(mm.group("mas") or "")]
            comps = [limpiar_md(c).strip().strip("“”‘’")
                     for c in limpiar_md(mm.group("comp")).split("+")]
            derivaciones.append({
                "sutta": actual,
                "linea": i + 1,
                "lemas": [l for l in lemas if l],
                "componentes": [c for c in comps if c],
                "pasos": partir_pasos(limpiar_md(bloque)),
                "bloque": limpiar_md(bloque),
            })

    # El castellano de cada sutta: del primer «---» posterior a su cabecera
    # hasta el siguiente. Es donde va la glosa y su explicación; los ejemplos
    # y los «¿Cuál es la finalidad…?» quedan fuera.
    orden = sorted(suttas.items(), key=lambda kv: kv[1]["linea"])
    for pos, (n, d) in enumerate(orden):
        fin = orden[pos + 1][1]["linea"] - 1 if pos + 1 < len(orden) else len(lineas)
        tramo = lineas[d["linea"]: fin]
        cortes = [k for k, l in enumerate(tramo) if l.strip() == "---"]
        d["pali"] = "\n".join(tramo[: cortes[0]]) if cortes else ""
        if len(cortes) >= 2:
            d["castellano"] = "\n".join(tramo[cortes[0] + 1: cortes[1]])
        elif cortes:
            d["castellano"] = "\n".join(tramo[cortes[0] + 1:])
        else:
            d["castellano"] = "\n".join(tramo)
    return suttas, derivaciones


# ── Qué clase de operación hace cada sutta ──────────────────────────────

MARCAS_CLASE = [
    ("elision", (r"elisión", r"se elide", r"se eliden", r"elidir", r"lopa\b")),
    # «deviene» es la palabra que esta edición usa para el ādesa: sin ella se
    # quedan sin clasificar tres docenas de suttas.
    ("sustitucion", (r"se sustituy", r"sustitución", r"sustitucion", r"sustituto",
                     r"se convierte", r"se convierten", r"se considera",
                     r"devien", r"en lugar de", r"ādes")),
    ("acortamiento", (r"se acorta", r"acortamiento", r"acortad", r"\brasso?\b", r"rassa")),
    ("alargamiento", (r"se alarga", r"alargamiento", r"alargad", r"dīgh")),
    ("nombre", (r"recibe el nombre", r"reciben el nombre", r"nombres? de ‘",
                r"saññ")),
    ("insercion", (r"se inserta", r"inserción", r"insercion", r"āgam")),
    ("duplicacion", (r"se duplica", r"duplicación", r"duplicacion")),
]


def clases_del_sutta(d):
    """Clases de operación que la traducción castellana del sutta atribuye a él.

    Se lee del castellano —no del pāḷi— porque es el mismo vocabulario que
    usan los pasos: «se sustituye por», «se elide», «se acorta», «recibe el
    nombre de», «se inserta». La comparación es, así, entre dos textos de la
    misma edición.
    """
    t = nfc(d.get("castellano", "")).lower()
    clases = set()
    for clase, marcas in MARCAS_CLASE:
        if any(re.search(m, t) for m in marcas):
            clases.add(clase)
    # «niggahita» es sustitución de ‘aṃ’/‘ma’ por ‘ṃ’.
    if "niggahita" in t:
        clases.add("sustitucion")
    return clases


def tabla_sandhi():
    """La tabla de §1-§51, revisada a mano, que ya vive en auditar_secuencias."""
    try:
        sys.path.insert(0, os.path.join(RAIZ, "herramientas"))
        import auditar_secuencias
        return {n: set(v) for n, v in auditar_secuencias.OPERACIONES.items()}
    except Exception:
        return {}


# ── Lectura de un paso ──────────────────────────────────────────────────

Q = r"[‘“]([^‘’“”]+)[’”]"

NEGACION = re.compile(
    r"\bno\s+(?:se\s+)?(?:cambia|convierte|convierten|sustituye|sustituyen|"
    r"elide|eliden|acorta|acortan|alarga|alargan|opera|aplica)\b|"
    r"\bno\s+ha\s+sido\b|\bpermanece\b|\bsino\s+que\b|\bno\s+opera\b")

# Cada patrón devuelve (clase, acción). El orden importa: lo más específico
# primero.
PATRONES = [
    # X (de W) junto con (la inflexión) (Y) se sustituye/convierte por/en Z
    # → fusión: desaparece el tramo que va de X al final de Y.
    ("sustitucion", "fusion", re.compile(
        r"{q}(?:\s*,[^,]*,)?\s*(?:de\s+{q}\s*)?junto\s+con\s+(?:la\s+[^‘“]*?)?"
        r"(?:{q}\s*)?(?:se\s+sustituye|se\s+convierte)n?\s+(?:por|en)\s+{q}".format(q=Q))),
    # se inserta Y (tras W)
    ("insercion", "insercion", re.compile(
        r"se\s+inserta[n]?\s+{q}(?:\s+tras\s+{q})?".format(q=Q))),
    # X de W se sustituye/convierte/considera por/en/como Y
    ("sustitucion", "sustitucion", re.compile(
        r"{q}(?:\s+final)?(?:\s+de\s+{q})?[^‘“]*?"
        r"(?:se\s+sustituye|se\s+sustituyen|se\s+convierte|se\s+convierten|"
        r"se\s+considera|se\s+debe\s+considerar)[^‘“]*?"
        r"(?:por|en|como)\s+{q}".format(q=Q))),
    # (hay) elisión de la vocal X de W  |  X de W se elide
    ("elision", "elision", re.compile(
        r"elisión\s+de\s+(?:la\s+vocal\s+)?{q}(?:\s+de\s+{q})?".format(q=Q))),
    ("elision", "elision", re.compile(
        r"{q}(?:\s+de\s+{q})?[^‘“]*?se\s+elide".format(q=Q))),
    ("acortamiento", "acortamiento", re.compile(
        r"{q}(?:\s+de\s+{q})?[^‘“]*?se\s+acorta".format(q=Q))),
    ("alargamiento", "alargamiento", re.compile(
        r"{q}(?:\s+de\s+{q})?[^‘“]*?se\s+alarga".format(q=Q))),
    ("duplicacion", "duplicacion", re.compile(
        r"{q}(?:\s+de\s+{q})?[^‘“]*?se\s+duplica".format(q=Q))),
    ("nombre", "nada", re.compile(
        r"{q}(?:\s+de\s+{q})?[^‘“]*?recibe\s+el\s+nombre(?:\s+de)?\s+{q}".format(q=Q))),
    # semántica pura: no toca la forma
    ("", "nada", re.compile(
        r"{q}\s+se\s+usa\s+con\s+el\s+significado".format(q=Q))),
]


def leer_paso(paso):
    """Devuelve (clase, accion, argumentos, negado, texto_sin_citas)."""
    t = re.sub(r"\s*\((?:[^()]|\([^()]*\))*\)", "", paso).strip()
    negado = bool(NEGACION.search(t))
    for clase, accion, rx in PATRONES:
        m = rx.search(t)
        if m:
            args = [g for g in m.groups()]
            # «‘a’ se convierte en ‘ā’» dice sustitución y hace alargamiento:
            # se clasifica por lo que hace, como en auditar_secuencias.py.
            if accion == "sustitucion" and args[0] and args[-1]:
                x, y = nfc(args[0]), nfc(args[-1])
                if LARGAS.get(x) == y:
                    clase = "alargamiento"
                elif CORTAS.get(x) == y:
                    clase = "acortamiento"
            return clase or None, ("nada" if negado else accion), args, negado, t
    if negado:
        # Un paso negado —«‘a’ de ‘aṃ’ no cambia», «este sutta no opera»— no
        # toca la forma: no hace falta saber leerlo para simular la cadena.
        return None, "nada", [], True, t
    return None, None, [], negado, t


# ── Aplicar la cadena ───────────────────────────────────────────────────

TOPE_ESTADOS = 400


def ocurrencias(partes, aguja, alcance=None, alias=None):
    """Posiciones (i_parte, pos) de `aguja`, opcionalmente dentro de `alcance`.

    Si la aguja no aparece y es un NOMBRE ya puesto por un paso anterior
    —«‘si’ recibe el nombre ‘ga’» y después «‘ga’ se elide»—, se busca lo
    que ese nombre designa. Es lo que el propio texto quiere decir.
    """
    if alias:
        directas = ocurrencias(partes, aguja, alcance)
        if directas:
            return directas
        nombrado = alias.get(nfc(aguja).lower())
        if nombrado:
            return ocurrencias(partes, nombrado, alcance)
        return []
    aguja = nfc(aguja)
    if not aguja:
        return []
    fuera = []
    for i, p in enumerate(partes):
        p = nfc(p)
        inicio = 0
        while True:
            k = p.find(aguja, inicio)
            if k < 0:
                break
            fuera.append((i, k))
            inicio = k + 1
    if alcance:
        alc = nfc(alcance)
        vanos = []
        for i, p in enumerate(partes):
            p = nfc(p)
            inicio = 0
            while True:
                k = p.find(alc, inicio)
                if k < 0:
                    break
                vanos.append((i, k, k + len(alc)))
                inicio = k + 1
        if vanos:
            dentro = [(i, k) for (i, k) in fuera
                      if any(i == vi and vk <= k and k + len(aguja) <= vf
                             for (vi, vk, vf) in vanos)]
            # Si el alcance existe pero no contiene la aguja, se prueba sin él:
            # el alcance suele nombrar el componente original, ya modificado.
            if dentro:
                return dentro
    return fuera


def reemplazar(partes, i, k, largo, nuevo):
    fuera = list(partes)
    fuera[i] = nfc(fuera[i])[:k] + nuevo + nfc(fuera[i])[k + largo:]
    return fuera


def aplicar(partes, accion, args, alias=None):
    """Devuelve la lista de estados posibles tras el paso, o None si no se sabe."""
    a = [nfc(x) if x else None for x in args]

    if accion == "nada":
        return [list(partes)]

    if accion == "insercion":
        nuevo, tras = a[0], a[1] if len(a) > 1 else None
        salidas = []
        if tras:
            for i, k in ocurrencias(partes, tras, alias=alias):
                salidas.append(reemplazar(partes, i, k, len(tras), tras + nuevo))
        if not salidas:
            # sin ancla: la juntura, que es donde inserta ‘s’ (§61-62)
            for j in range(1, len(partes)):
                salidas.append(list(partes[:j]) + [nuevo] + list(partes[j:]))
            if len(partes) == 1:
                salidas.append([partes[0] + nuevo])
        return salidas or None

    if accion == "fusion":
        # «X (de W) junto con (la inflexión) (Y) se sustituye por Z»: se
        # sustituye el tramo entero que va del principio de X al final de Y.
        # Sin Y —«“tumha” junto con la inflexión se sustituye por “tayā”»—
        # el tramo llega hasta el final de la forma.
        x, w, y, z = (a + [None] * 4)[:4]
        crudo = nfc("".join(partes))
        salidas = []
        for k in [m.start() for m in re.finditer(re.escape(nfc(x)), crudo)]:
            if y:
                j = crudo.find(nfc(y), k + len(nfc(x)))
                if j < 0:
                    continue
                fin = j + len(nfc(y))
            else:
                fin = len(crudo)
            salidas.append([crudo[:k] + z + crudo[fin:]])
        if not salidas and not y:
            salidas.append([z])
        return salidas or None

    if accion == "sustitucion":
        x, w, y = (a + [None, None, None])[:3]
        y = a[-1]
        if len(a) >= 3 and a[1]:
            x, w = a[0], a[1]
        else:
            x, w = a[0], None
        pos = ocurrencias(partes, x, w, alias)
        return [reemplazar(partes, i, k, len(x), y) for i, k in pos] or None

    if accion == "elision":
        x, w = a[0], (a[1] if len(a) > 1 else None)
        pos = ocurrencias(partes, x, w, alias)
        return [reemplazar(partes, i, k, len(x), "") for i, k in pos] or None

    if accion in ("acortamiento", "alargamiento"):
        x, w = a[0], (a[1] if len(a) > 1 else None)
        tabla = CORTAS if accion == "acortamiento" else LARGAS
        salidas = []
        for i, k in ocurrencias(partes, x, w, alias):
            if len(x) == 1 and x in tabla:
                salidas.append(reemplazar(partes, i, k, 1, tabla[x]))
            else:
                # la cita nombra ya la vocal resultante, o es plurilítera
                trans = "".join(tabla.get(c, c) for c in x)
                salidas.append(reemplazar(partes, i, k, len(x), trans))
        return salidas or None

    if accion == "duplicacion":
        x, w = a[0], (a[1] if len(a) > 1 else None)
        pos = ocurrencias(partes, x, w, alias)
        return [reemplazar(partes, i, k, len(x), x + x) for i, k in pos] or None

    return None


def recomponer(der):
    """Aplica la cadena. Devuelve (estado, resultados, motivo)."""
    estados = [[nfc(c) for c in der["componentes"]]]
    ilustrativa = False
    alias = {}
    for paso in der["pasos"]:
        clase, accion, args, negado, t = leer_paso(paso)
        if negado:
            ilustrativa = True
        if accion is None:
            return "no simulable", [], "paso no implementado: «{0}»".format(t)
        if clase == "nombre" and args and args[0] and args[-1]:
            alias[nfc(args[-1]).lower()] = nfc(args[0])
        nuevos, vistos = [], set()
        for e in estados:
            salidas = aplicar(e, accion, args, alias)
            # Que una lectura anterior deje el operando sin dónde aplicarse
            # sólo descarta ESA lectura. Si ninguna sobrevive, el paso no se
            # puede simular y se dice.
            if salidas is None:
                continue
            for s in salidas:
                clave = tuple(s)
                if clave not in vistos:
                    vistos.add(clave)
                    nuevos.append(s)
        if not nuevos:
            return "no simulable", [], "no se localiza el operando: «{0}»".format(t)
        estados = nuevos[:TOPE_ESTADOS]
        if len(nuevos) > TOPE_ESTADOS:
            return "no simulable", [], "demasiadas lecturas del operando"
    resultados = sorted({"".join(e) for e in estados})
    metas = {desnudar(l) for l in der["lemas"]}
    if any(desnudar(r) in metas for r in resultados):
        return "recompone", resultados, ""
    return ("ilustrativa" if ilustrativa else "no recompone"), resultados, ""


# ── Comprobaciones ──────────────────────────────────────────────────────

def firma_cadena(pasos):
    """Qué HACE la cadena, dejando fuera la redacción.

    Entran la clase de cada paso, sus operandos y sus §N. Quedan fuera:

      · los pasos que no tocan la forma —«‘to’ se usa con el significado de
        la quinta inflexión»—, que son glosa y no derivación;
      · los pasos negados —«‘smiṃ’ no se convierte en ‘mhi’»—, que dicen lo
        que NO pasa y que un sitio puede querer decir y otro no;
      · la comilla usada (‘ vs “), el verbo elegido («se sustituye por» vs
        «se convierte en») y el ORDEN de los pasos.

    Así, dos presentaciones de la misma derivación no se cuentan como
    divergentes; lo que queda es cita distinta u operando distinto, que es la
    clase de «itthiṃ».
    """
    firma = []
    for p in pasos:
        clase, accion, args, negado, t = leer_paso(p)
        if clase is None or negado:
            continue
        firma.append((clase,
                      tuple(nfc(x).lower() if x else "" for x in args),
                      tuple(sorted(citas(p)))))
    return tuple(sorted(firma))


def comprobar(ruta, cuales):
    suttas, derivaciones = leer_capitulo(ruta)
    sandhi = tabla_sandhi()
    clases = {n: clases_del_sutta(d) for n, d in suttas.items()}
    rango = (min(suttas), max(suttas)) if suttas else (0, 0)

    inf = {
        "ruta": ruta,
        "suttas": len(suttas),
        "rango": rango,
        "derivaciones": len(derivaciones),
        "pasos": sum(len(d["pasos"]) for d in derivaciones),
    }
    avisos = defaultdict(list)

    # 0 · tipografía
    if "tipografia" in cuales:
        for d in derivaciones:
            for paso in d["pasos"]:
                sencillas = paso.count("‘") - paso.count("’")
                dobles = paso.count("“") - paso.count("”")
                if sencillas or dobles:
                    avisos["tipografia"].append({
                        "linea": d["linea"], "sutta": d["sutta"],
                        "lema": d["lemas"][0], "paso": paso,
                        "que": "comillas sin cerrar ({0}{1})".format(
                            "simples " if sencillas else "",
                            "dobles" if dobles else "").strip(),
                    })

    # 1 · pasos sin cita
    if "sincita" in cuales:
        for d in derivaciones:
            for paso in d["pasos"]:
                if not citas(paso):
                    avisos["sincita"].append({
                        "linea": d["linea"], "sutta": d["sutta"],
                        "lema": d["lemas"][0], "paso": paso,
                    })

    # 2 · misma forma, cadenas distintas
    if "divergencia" in cuales:
        por_lema = defaultdict(list)
        for d in derivaciones:
            for l in d["lemas"]:
                por_lema[desnudar(l)].append(d)
        for lema, ds in sorted(por_lema.items()):
            # Sólo divergen de veras las que parten de los MISMOS componentes.
            # Dos lemas homógrafos de bases distintas —«asmiṃ» de “ta” y de
            # “ima”— no son un caso a revisar, y son la mayoría.
            por_comp = defaultdict(list)
            for d in ds:
                por_comp[tuple(desnudar(c) for c in d["componentes"])].append(d)
            for comp, grupo in por_comp.items():
                firmas = {}
                for d in grupo:
                    firmas.setdefault(firma_cadena(d["pasos"]), []).append(d)
                if len(firmas) > 1:
                    avisos["divergencia"].append({
                        "lema": grupo[0]["lemas"][0],
                        "variantes": [
                            {"sutta": v[0]["sutta"], "lineas": [x["linea"] for x in v],
                             "componentes": v[0]["componentes"], "pasos": v[0]["pasos"]}
                            for v in firmas.values()],
                    })
            if len(por_comp) > 1:
                avisos["homografas"].append({
                    "lema": ds[0]["lemas"][0],
                    "variantes": [
                        {"sutta": v[0]["sutta"], "lineas": [x["linea"] for x in v],
                         "componentes": v[0]["componentes"], "pasos": v[0]["pasos"]}
                        for v in por_comp.values()],
                })

    # 3 · clase de operación contra el sutta citado
    fuera_de_rango = Counter()
    sin_clasificar = Counter()
    if "clase" in cuales:
        for d in derivaciones:
            for paso in d["pasos"]:
                clase, accion, args, negado, t = leer_paso(paso)
                if clase is None or negado:
                    continue
                for n in citas(paso):
                    if n in sandhi and n < rango[0]:
                        esperado = sandhi[n]
                    elif n in clases:
                        esperado = clases[n]
                    elif n > rango[1] or n < rango[0]:
                        fuera_de_rango[n] += 1
                        continue
                    else:
                        sin_clasificar[n] += 1
                        continue
                    if not esperado:
                        sin_clasificar[n] += 1
                        continue
                    # Un cambio de cantidad —a ↔ ā— es a la vez alargamiento
                    # y ādesa, y la edición lo dice de las dos maneras: «‘a’
                    # se alarga» y «‘a’ deviene ‘ā’». No es discrepancia.
                    admitidas = {clase}
                    # (Sólo en esa dirección: la clase del paso ya se ha leído
                    # de sus operandos, así que aquí «alargamiento» significa
                    # que son de veras una pareja de cantidad.)
                    if clase in ("alargamiento", "acortamiento"):
                        admitidas.add("sustitucion")
                    if not (admitidas & esperado):
                        avisos["clase"].append({
                            "linea": d["linea"], "sutta": d["sutta"],
                            "lema": d["lemas"][0], "paso": t, "cita": n,
                            "hace": NOMBRE_OP.get(clase, clase),
                            "esperado": sorted(NOMBRE_OP.get(o, o) for o in esperado),
                        })
    inf["fuera_de_rango"] = fuera_de_rango
    inf["sin_clasificar"] = sin_clasificar

    # 4 · recomposición
    if "recomposicion" in cuales:
        cuenta = Counter()
        for d in derivaciones:
            estado, resultados, motivo = recomponer(d)
            cuenta[estado] += 1
            if estado in ("no recompone", "no simulable", "ilustrativa"):
                avisos[estado].append({
                    "linea": d["linea"], "sutta": d["sutta"],
                    "lema": " / ".join(d["lemas"]),
                    "componentes": " + ".join(d["componentes"]),
                    "pasos": d["pasos"], "da": resultados[:6], "motivo": motivo,
                })
        inf["recomposicion"] = cuenta

    return inf, avisos


# ── Informe ─────────────────────────────────────────────────────────────

def encabezado(t):
    print()
    print(t)
    print("─" * len(t))


def informar(inf, avisos, detalle):
    base = os.path.basename(inf["ruta"])
    print("{0} · {1} suttas (§{2}-§{3}) · {4} derivaciones · {5} pasos".format(
        base, inf["suttas"], inf["rango"][0], inf["rango"][1],
        inf["derivaciones"], inf["pasos"]))
    if base in CONVERTIDOS:
        fuente, conv = CONVERTIDOS[base]
        print("AVISO: este archivo es SALIDA. Lo que se corrija va en")
        print("       «{0}», que es lo que lee {1}.".format(fuente, conv))
        print("       Un cambio hecho aquí lo revierte el hook de pre-commit,")
        print("       en el momento del commit y sin avisar.")

    if inf.get("fuera_de_rango"):
        print()
        print("  citas a suttas de otros capítulos, sin clasificar: {0}".format(
            ", ".join("§{0}×{1}".format(k, v)
                      for k, v in sorted(inf["fuera_de_rango"].items()))))
    if inf.get("sin_clasificar"):
        print("  suttas de este capítulo cuya traducción no deja leer la clase: {0}".format(
            ", ".join("§{0}".format(k) for k in sorted(inf["sin_clasificar"]))))

    if "recomposicion" in inf:
        c = inf["recomposicion"]
        print()
        print("  recomposición: {0} recomponen · {1} no recomponen · "
              "{2} ilustrativas · {3} no simulables".format(
                  c["recompone"], c["no recompone"], c["ilustrativa"],
                  c["no simulable"]))

    total = 0

    if avisos["tipografia"]:
        total += len(avisos["tipografia"])
        encabezado("0 · TIPOGRAFÍA — {0} pasos".format(len(avisos["tipografia"])))
        for x in avisos["tipografia"]:
            print("  §{0} · {1} (línea {2}) — {3}".format(
                x["sutta"], x["lema"], x["linea"], x["que"]))
            print("      {0}".format(x["paso"]))

    if avisos["sincita"]:
        total += len(avisos["sincita"])
        encabezado("1 · PASOS SIN §N — {0} pasos".format(len(avisos["sincita"])))
        for x in avisos["sincita"]:
            print("  §{0} · {1} (línea {2})".format(x["sutta"], x["lema"], x["linea"]))
            print("      {0}".format(x["paso"]))

    if avisos["divergencia"]:
        total += len(avisos["divergencia"])
        encabezado("2 · MISMOS COMPONENTES, CADENAS DISTINTAS — {0} formas".format(
            len(avisos["divergencia"])))
        print("  No todas son erratas: dos suttas pueden ilustrar aspectos")
        print("  distintos de la misma forma. Cada una hay que mirarla.")
        print()
        for x in avisos["divergencia"]:
            print("  {0}".format(x["lema"]))
            for v in x["variantes"]:
                print("      §{0} (línea{1} {2}): {3}".format(
                    v["sutta"], "s" if len(v["lineas"]) > 1 else "",
                    ", ".join(str(n) for n in v["lineas"]),
                    " + ".join(v["componentes"])))
                for p in v["pasos"]:
                    print("          · {0}".format(p))
            print()

    if detalle and avisos["homografas"]:
        encabezado("2 bis · MISMO LEMA, COMPONENTES DISTINTOS — {0} formas".format(
            len(avisos["homografas"])))
        print("  Informativo: «asmiṃ» de “ta” y «asmiṃ» de “ima” son dos")
        print("  derivaciones legítimas, no una divergencia.")
        print()
        for x in avisos["homografas"]:
            print("  {0}: {1}".format(x["lema"], " | ".join(
                "§{0} {1}".format(v["sutta"], " + ".join(v["componentes"]))
                for v in x["variantes"])))

    if avisos["clase"]:
        total += len(avisos["clase"])
        encabezado("3 · LA CLASE DEL PASO NO ES LA DEL SUTTA — {0} pasos".format(
            len(avisos["clase"])))
        for x in avisos["clase"]:
            print("  §{0} citado en §{1} · {2} (línea {3})".format(
                x["cita"], x["sutta"], x["lema"], x["linea"]))
            print("      {0}".format(x["paso"]))
            print("      el paso hace: {0}   ·   §{1} hace: {2}".format(
                x["hace"], x["cita"], ", ".join(x["esperado"]) or "—"))
            print()

    if avisos["no recompone"]:
        total += len(avisos["no recompone"])
        encabezado("4 · LA CADENA NO DA EL LEMA — {0} derivaciones".format(
            len(avisos["no recompone"])))
        print("  Es la comprobación que caza «ādi + smiṃ → ādaṃ». Candidatos,")
        print("  no errores probados.")
        print()
        for x in avisos["no recompone"]:
            print("  §{0} · {1} = {2} (línea {3})".format(
                x["sutta"], x["lema"], x["componentes"], x["linea"]))
            for p in x["pasos"]:
                print("      · {0}".format(p))
            print("      da: {0}".format(", ".join(x["da"]) or "—"))
            print()

    if detalle and avisos["ilustrativa"]:
        encabezado("4 bis · CADENAS ILUSTRATIVAS QUE NO DAN EL LEMA — {0}".format(
            len(avisos["ilustrativa"])))
        print("  Llevan una negación («no cambia», «este sutta no opera»): la")
        print("  cadena enseña lo que NO pasa, y no se espera que recomponga.")
        print()
        for x in avisos["ilustrativa"]:
            print("  §{0} · {1} = {2} (línea {3}) → {4}".format(
                x["sutta"], x["lema"], x["componentes"], x["linea"],
                ", ".join(x["da"]) or "—"))

    if avisos["no simulable"]:
        encabezado("4 ter · NO SIMULABLE — {0} derivaciones".format(
            len(avisos["no simulable"])))
        print("  El guion no las juzga: dice por qué no ha podido.")
        motivos = Counter(x["motivo"].split(":")[0] for x in avisos["no simulable"])
        for m, n in motivos.most_common():
            print("      {0}: {1}".format(m, n))
        if detalle:
            print()
            for x in avisos["no simulable"]:
                print("  §{0} · {1} = {2} (línea {3})".format(
                    x["sutta"], x["lema"], x["componentes"], x["linea"]))
                print("      {0}".format(x["motivo"]))

    print()
    if not total:
        print("Ninguna comprobación levanta candidatos.")
    else:
        print("{0} candidatos en total. Ninguno está firmado: cada uno se le".format(total))
        print("enseña al IEBH con su evidencia y su corrección propuesta.")
    return 1 if total else 0


TODAS = ["tipografia", "sincita", "divergencia", "clase", "recomposicion"]

# La errata de la sesión 61 y sus vecinas, congeladas como prueba: si el
# simulador se toca, esto dice si sigue cazando lo que ya cazó.
AUTOPRUEBA = [
    ("ādiṃ, como estaba antes de la sesión 61", "no recompone", ["Ādiṃ"],
     ["ādi", "smiṃ"],
     ["‘smiṃ’ se sustituye por ‘aṃ’ (§69)", "‘i’ de “ādi” se elide (§83)"]),
    ("ādiṃ, ya corregida", "recompone", ["Ādiṃ"], ["ādi", "smiṃ"],
     ["‘smiṃ’ se sustituye por ‘aṃ’ (§69)",
      "‘i’ de “ādi” recibe el nombre de ‘jha’ (§58)",
      "‘aṃ’ se convierte en ‘ṃ’ (§82)"]),
    ("bārāṇasiṃ, ya corregida", "recompone", ["Bārāṇasiṃ"], ["Bārāṇasī", "smiṃ"],
     ["‘smiṃ’ se sustituye por ‘aṃ’ (§69)",
      "‘ī’ de “Bārāṇasī” se acorta (§84)", "‘aṃ’ se convierte en ‘ṃ’ (§82)"]),
    ("ratto, ya corregida", "recompone", ["Ratto"], ["ratti", "smiṃ"],
     ["‘smiṃ’ se sustituye por ‘o’ (§69)", "‘i’ de “ratti” se elide (§83)"]),
    ("saññā: ‘ga’ nombra a ‘si’", "recompone", ["Itthi"], ["itthī", "si"],
     ["‘si’ recibe el nombre ‘ga’ (§57)", "‘ī’ se acorta (§245)",
      "‘ga’ se elide (§220)"]),
    ("fusión hasta la inflexión", "recompone", ["Guṇavati"], ["guṇavantu", "smiṃ"],
     ["‘ntu’ junto con la inflexión ‘smiṃ’ se sustituye por ‘ti’ (§127)"]),
]


def autoprueba():
    fallos = 0
    for nombre, espera, lemas, comp, pasos in AUTOPRUEBA:
        estado, da, motivo = recomponer(
            {"lemas": lemas, "componentes": comp, "pasos": pasos})
        bien = estado == espera
        fallos += 0 if bien else 1
        print("  {0} {1} — se esperaba «{2}», da «{3}» {4}".format(
            "ok  " if bien else "FALLA", nombre, espera, estado,
            "→ " + ", ".join(da) if da else motivo))
    print()
    print("Autoprueba: {0} de {1}".format(len(AUTOPRUEBA) - fallos, len(AUTOPRUEBA)))
    return 1 if fallos else 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("capitulo", nargs="?", default=POR_DEFECTO,
                    help="markdown del capítulo (por defecto {0})".format(POR_DEFECTO))
    ap.add_argument("--comprobacion", "-c", action="append",
                    choices=TODAS, help="sólo ésta (repetible)")
    ap.add_argument("--detalle", "-d", action="store_true",
                    help="muestra las cadenas completas y los buckets menores")
    ap.add_argument("--autoprueba", action="store_true",
                    help="comprueba el simulador contra las erratas ya conocidas")
    a = ap.parse_args()

    if a.autoprueba:
        return autoprueba()

    ruta = a.capitulo
    if not os.path.isabs(ruta):
        cand = os.path.join(RAIZ, ruta)
        ruta = cand if os.path.exists(cand) else ruta
    if not os.path.exists(ruta):
        print("No existe: {0}".format(ruta), file=sys.stderr)
        return 2

    cuales = a.comprobacion or TODAS
    inf, avisos = comprobar(ruta, cuales)
    return informar(inf, avisos, a.detalle)


if __name__ == "__main__":
    sys.exit(main())
