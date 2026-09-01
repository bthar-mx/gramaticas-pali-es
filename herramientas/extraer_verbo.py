#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrae el documento «Verbo» a recursos/verbo/verbo.json.

    python3 herramientas/extraer_verbo.py

Fuente: docs/fuentes/verbo.docx — «Verbo», material preparado por Bhikkhu
Nandisena, IEBH, última revisión 7-abr-2013, publicación 20130407-BN-T0021.
Los paradigmas de la sección «otros paradigmas» proceden de *The Higher Pali
Course for Advanced Students*, del Venerable Buddhadatta Thera (The Colombo
Apothecaries' Co., Ltd., Colombo, 1951), según dicen la nota al pie 2 y el
colofón del propio documento.

Lo que hace, y lo que NO hace
-----------------------------

Copia el documento **verbatim**. No corrige, no completa y no reordena. Las
dos únicas cosas que añade son:

1. **El número de Kaccāyana** junto al de Rūpasiddhi que trae el documento,
   deducido de la concordancia de `kaccayana/*.md` y `docs/*.md` — nunca
   escrito a mano. Si un número de Rū no está en la concordancia, el guion se
   detiene.
2. **La marca de las celdas de autoridad que mezclan numeraciones.** La nota
   al pie 1 del documento declara que toda la última columna es de
   Padarūpasiddhi, pero la última fila de las catorce escaleras cita «11», que
   es un número de Kaccāyana (Kacc. §11 *Naye paraṃ yutte* = Rū 14). Está
   cotejado con las trece presentaciones, que citan siempre el par Kacc/Rū.
   Ver `docs/verbo/escaleras-por-adjudicar.md` §1.

Todo lo demás —erratas incluidas— pasa tal cual y se señala en el informe,
no aquí.
"""

import json
import os
import re
import sys

try:
    import docx
    from docx.table import Table
    from docx.text.paragraph import Paragraph
except ImportError:
    sys.exit("Falta python-docx:  pip install python-docx")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUENTE = os.path.join(RAIZ, "docs", "fuentes", "verbo.docx")
DESTINO = os.path.join(RAIZ, "recursos", "verbo", "verbo.json")

# El «11» final de cada escalera es Kaccāyana, no Rūpasiddhi. Ver el docstring.
KACC_EN_COLUMNA_RU = {11}

# Índices de tabla dentro del documento. Se validan por forma más abajo: si el
# documento cambiara, el guion se detiene en vez de publicar datos torcidos.
T_USOS = 0
T_VOCES = 1
T_INFLEXIONES = range(2, 10)
T_GANAS = 10
T_ESCALERAS = range(11, 25)
T_PARADIGMAS = range(25, 130)
# A partir de esta tabla empieza «otros paradigmas» (Buddhadatta).
T_BUDDHADATTA_DESDE = 57


# --------------------------------------------------------------------------
# concordancia Rū → Kacc, deducida del markdown; jamás escrita a mano
# --------------------------------------------------------------------------

RE_SUTTA = re.compile(r"\*\*(\d+)\\?\.\s*(\d+)\\?\.\s")


def concordancia():
    """{num_rupasiddhi: num_kaccayana} de todo el markdown del repositorio."""
    import glob

    ru2kacc, kacc2ru = {}, {}
    patrones = [os.path.join(RAIZ, "kaccayana", "*.md"),
                os.path.join(RAIZ, "docs", "*.md")]
    for patron in patrones:
        for ruta in sorted(glob.glob(patron)):
            with open(ruta, encoding="utf-8") as fh:
                for m in RE_SUTTA.finditer(fh.read()):
                    kacc, ru = int(m.group(1)), int(m.group(2))
                    ru2kacc.setdefault(ru, kacc)
                    kacc2ru.setdefault(kacc, ru)
    if len(ru2kacc) < 500:
        sys.exit(f"Concordancia demasiado corta ({len(ru2kacc)} pares): "
                 "¿falta algún capítulo en docs/?")
    return ru2kacc, kacc2ru


# --------------------------------------------------------------------------
# lectura del documento
# --------------------------------------------------------------------------

def cuerpo(doc):
    """Párrafos y tablas del documento, en el orden en que aparecen."""
    for hijo in doc.element.body.iterchildren():
        etiqueta = hijo.tag.split("}")[1]
        if etiqueta == "p":
            yield "p", Paragraph(hijo, doc)
        elif etiqueta == "tbl":
            yield "tbl", Table(hijo, doc)


def celdas(fila):
    """Texto de cada celda, con los saltos de línea internos como ' / '."""
    return [c.text.strip().replace("\n", " / ").strip() for c in fila.cells]


def matriz(tabla):
    return [celdas(f) for f in tabla.rows]


# El documento parte los encabezados en dos: «1a-bhū (ser/estar)» por un lado
# y «voz activa» por otro, ambos con estilo Título 1. Y el tiempo verbal —«(i)
# presente»— no es encabezado siquiera: va con estilo de pie de página. Hay
# que recoger las tres cosas por separado.
RE_ENTRADA = re.compile(r"^\d+[a-z]?-")
RE_VOZ = re.compile(r"^voz\b", re.I)
RE_TIEMPO = re.compile(r"^\((i{1,3}|iv|v|vi{1,3})\)\s*(.*)$", re.I)
RE_TIEMPO_PALI = re.compile(r"^\((vattamānā|pañcamī|sattamī|hiyyattanī|"
                            r"parokkhā|ajjatanī|bhavissantī|kālātipatti)\)$",
                            re.I)


def leer(doc):
    """
    Devuelve (tablas, contextos). contextos[i] describe dónde cae la tabla i:
    entrada («2a-paca (cocinar)»), voz, tiempo y su nombre pāḷi.
    """
    tablas, contextos = [], []
    ctx = {"entrada": "", "voz": "", "tiempo": "", "tiempo_pali": "",
           "titulo": "", "previos": []}
    # Índice de la tabla que espera todavía su nombre pāḷi de tiempo: el
    # documento unas veces lo pone antes de la tabla y otras después.
    pendiente = None

    for clase, obj in cuerpo(doc):
        if clase == "p":
            texto = obj.text.strip()
            if not texto:
                continue
            encabezado = obj.style.name in ("Título 1", "Heading 1")
            if encabezado:
                ctx["titulo"] = texto
                ctx["previos"] = []
            else:
                # Lo que va entre el encabezado y la tabla: el nombre pāḷi de
                # la vibhatti —«(vattamānā vibhatti)»— y, a veces, una nota
                # como «inserción de ‘a’ es opcional».
                ctx["previos"] = ctx["previos"] + [texto]
            # Un mismo párrafo puede llevar dos cosas separadas por salto de
            # línea: «paradigmas de conjugación⏎1a-bhū (ser/estar)».
            for linea in (l.strip() for l in texto.split("\n")):
                if not linea:
                    continue
                if encabezado and RE_ENTRADA.match(linea):
                    ctx.update(entrada=linea, voz="", tiempo="",
                               tiempo_pali="")
                elif encabezado and RE_VOZ.match(linea):
                    ctx["voz"] = linea
                m = RE_TIEMPO.match(linea)
                if m:
                    ctx["tiempo"] = m.group(2).strip()
                    ctx["tiempo_pali"] = ""
                m = RE_TIEMPO_PALI.match(linea)
                if m:
                    ctx["tiempo_pali"] = m.group(1)
                    if pendiente is not None:
                        contextos[pendiente]["tiempo_pali"] = m.group(1)
                        pendiente = None
        else:
            tablas.append(matriz(obj))
            contextos.append(dict(ctx))
            ctx["previos"] = []
            pendiente = len(tablas) - 1 if not ctx["tiempo_pali"] else None
    return tablas, contextos


# --------------------------------------------------------------------------
# autoridades
# --------------------------------------------------------------------------

RE_NUM = re.compile(r"\d+")


def autoridades(celda, ru2kacc, kacc2ru):
    """
    Convierte la celda de autoridad en una lista de referencias.

    Cada una queda como {'kacc': N, 'ru': M, 'segun_documento': '...'} más,
    cuando procede, 'mezcla': True — que es la marca de que el documento
    escribió ahí un número de Kaccāyana en una columna declarada de
    Rūpasiddhi.
    """
    refs = []
    for bruto in RE_NUM.findall(celda):
        n = int(bruto)
        if n in KACC_EN_COLUMNA_RU:
            if n not in kacc2ru:
                sys.exit(f"Kacc. §{n} no está en la concordancia.")
            refs.append({"kacc": n, "ru": kacc2ru[n],
                         "segun_documento": bruto, "mezcla": True})
        else:
            if n not in ru2kacc:
                sys.exit(f"Rū {n} no está en la concordancia "
                         f"(celda: {celda!r}).")
            refs.append({"kacc": ru2kacc[n], "ru": n,
                         "segun_documento": bruto})
    return refs


# --------------------------------------------------------------------------
# escaleras
# --------------------------------------------------------------------------

RE_TITULO_ESC = re.compile(r"^(\d+)-(.+?)\s*\((.+)\)\s*$")

# «(vattamānā vibhatti)» o «(ajjatanī vibhatti) —inserción de ‘a’ es opcional»
RE_VIBHATTI = re.compile(r"^\(([^)]*?)\s*vibhatti\)\s*(.*)$", re.I)


def vibhatti(previos):
    """El nombre pāḷi de la inflexión y la nota que la acompañe."""
    pali, notas = "", []
    for linea in previos:
        m = RE_VIBHATTI.match(linea.strip())
        if m:
            pali = m.group(1).strip()
            resto = m.group(2).strip(" —-–")
            if resto:
                notas.append(resto)
        elif linea.strip() and pali:
            notas.append(linea.strip())
    return pali, " · ".join(notas)


def escalera(tabla, titulo, ru2kacc, kacc2ru):
    """
    Una tabla de formación. Columnas:

        6:  n | raíz | signo | inflexión | resultado | autoridad
        7:  n | prefijo | raíz | signo | inflexión | resultado | autoridad
    """
    ancho = max(len(f) for f in tabla)
    if ancho not in (6, 7):
        sys.exit(f"Escalera «{titulo}» con {ancho} columnas; se esperaban 6 o 7.")
    con_prefijo = ancho == 7

    m = RE_TITULO_ESC.match(titulo)
    orden, lema, glosa = (int(m.group(1)), m.group(2), m.group(3)) if m \
        else (None, titulo, "")

    pasos = []
    for fila in tabla:
        fila = fila + [""] * (ancho - len(fila))
        i = 0
        n = fila[i]; i += 1
        prefijo = fila[i] if con_prefijo else ""
        if con_prefijo:
            i += 1
        raiz, signo, inflexion, resultado, autoridad = fila[i:i + 5]
        pasos.append({
            "n": int(n) if n.isdigit() else n,
            "prefijo": prefijo,
            "raiz": raiz,
            "signo": signo,
            "inflexion": inflexion,
            "resultado": resultado,
            "autoridades": autoridades(autoridad, ru2kacc, kacc2ru),
        })
    return {
        "orden": orden,
        "lema": lema,
        "glosa": glosa,
        "titulo": titulo,
        "con_prefijo": con_prefijo,
        "fuente": "documento",
        "pasos": pasos,
    }


# --------------------------------------------------------------------------
# paradigmas de conjugación
# --------------------------------------------------------------------------

def paradigma(tabla, ctx, indice):
    """Tabla 5x5 de conjugación: cabecera de pada, cabecera de número y 3 filas."""
    if len(tabla) != 5:
        sys.exit(f"Paradigma «{ctx['entrada']} / {ctx['tiempo']}» "
                 f"(tabla {indice}) con {len(tabla)} filas; se esperaban 5.")
    filas = [{"persona": f[0], "formas": f[1:]} for f in tabla[2:]]
    return {
        "entrada": ctx["entrada"],
        "voz": ctx["voz"],
        "tiempo": ctx["tiempo"],
        "tiempo_pali": ctx["tiempo_pali"],
        "padas": tabla[0][1:],
        "numeros": tabla[1][1:],
        "filas": filas,
        "seccion": ("otros paradigmas" if indice >= T_BUDDHADATTA_DESDE
                    else "paradigmas de conjugación"),
        "obra": ("Buddhadatta, The Higher Pali Course for Advanced Students, "
                 "Colombo, 1951")
        if indice >= T_BUDDHADATTA_DESDE else "Nandisena, «Verbo»",
    }


# --------------------------------------------------------------------------

def main():
    if not os.path.exists(FUENTE):
        sys.exit(f"No está la fuente: {FUENTE}")

    ru2kacc, kacc2ru = concordancia()
    doc = docx.Document(FUENTE)
    tablas, contextos = leer(doc)
    titulos = [c["titulo"] for c in contextos]

    if len(tablas) != 130:
        sys.exit(f"El documento trae {len(tablas)} tablas; se esperaban 130. "
                 "¿Cambió la fuente? Revisar los índices de este guion.")

    datos = {
        "_nota": ("Extraído de docs/fuentes/verbo.docx por "
                  "herramientas/extraer_verbo.py. Verbatim: no se corrige "
                  "nada aquí. Las erratas conocidas están en "
                  "docs/verbo/escaleras-por-adjudicar.md."),
        "fuente": {
            "titulo": "Verbo (ākhyāta)",
            "autor": "Bhikkhu Nandisena",
            "basado_en": "Rū. pp. 256-33 y Sad. iii pp. 267-311",
            "otros_paradigmas": ("The Higher Pali Course for Advanced "
                                 "Students, Ven. Buddhadatta Thera, The "
                                 "Colombo Apothecaries' Co., Ltd., Colombo, "
                                 "Sri Lanka, 1951"),
            "revision_original": "2013-04-07",
            "publicacion_iebh": "20130407-BN-T0021",
            "referencias": ("Kaccāyana cap. vi; Rūpasiddhi cap. vi; "
                            "Saddanīti-Suttamālā xv, 811-844"),
        },
        "usos": tablas[T_USOS],
        "voces": tablas[T_VOCES],
        "inflexiones": [
            dict(zip(("titulo", "pali", "nota", "tabla"),
                     (titulos[i], *vibhatti(contextos[i]["previos"]),
                      tablas[i])))
            for i in T_INFLEXIONES],
        "ganas": tablas[T_GANAS],
        "escaleras": [escalera(tablas[i], titulos[i], ru2kacc, kacc2ru)
                      for i in T_ESCALERAS],
        "paradigmas": [paradigma(tablas[i], contextos[i], i)
                       for i in T_PARADIGMAS],
    }

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    with open(DESTINO, "w", encoding="utf-8") as fh:
        json.dump(datos, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    mezclas = sum(1 for e in datos["escaleras"] for p in e["pasos"]
                  for a in p["autoridades"] if a.get("mezcla"))
    buddhadatta = sum(1 for p in datos["paradigmas"]
                      if p["obra"].startswith("Buddhadatta"))
    print(f"{os.path.relpath(DESTINO, RAIZ)}")
    print(f"  escaleras            {len(datos['escaleras'])}")
    print(f"  paradigmas           {len(datos['paradigmas'])}"
          f"  (de ellos {buddhadatta} de Buddhadatta)")
    print(f"  tablas de inflexión  {len(datos['inflexiones'])}")
    print(f"  celdas con numeración mezclada Kacc/Rū  {mezclas}")


if __name__ == "__main__":
    main()
