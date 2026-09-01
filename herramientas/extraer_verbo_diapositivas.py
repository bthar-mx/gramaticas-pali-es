#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrae las escaleras de formación de las presentaciones de clase.

    python3 herramientas/extraer_verbo_diapositivas.py

Fuente: docs/fuentes/verbo-diapositivas/GP-T - Verbo-*.pdf — trece
presentaciones de Bhikkhu Nandisena, exportadas de Keynote. **No viajan con el
repositorio** (los PDF están en .gitignore, como los tres del Saddanīti): lo
que se publica es el JSON ya extraído. Sólo hay que volver a extraer si cambia
una fuente.

Por qué las diapositivas y no sólo el documento
-----------------------------------------------

Las diapositivas traen tres cosas que el documento «Verbo» no tiene:

1. **El par Kacc/Rū.** El documento da un solo número y su nota al pie dice
   que es de Rūpasiddhi; las diapositivas citan siempre «457/424», es decir
   Kaccāyana y Rūpasiddhi. Sobre los 30 pares distintos que aparecen —107
   citas— ninguno discrepa de la concordancia del repositorio.
2. **Una operación por fila.** El documento funde el último paso de elisión
   con el de formación del verbo, y en «bhū» eso deja invisible la forma
   intermedia «bhav». Ver `docs/verbo/escaleras-por-adjudicar.md` §3.
3. **Siete escaleras que el documento no tiene**: «gaha»; «anu-bhū» y «paca»
   en voz pasiva; y los causativos de «bhū» —activo y pasivo— y de «paca».

Cómo se leen las tablas
-----------------------

Con `pdftotext -bbox-layout`, que da la caja de cada palabra. Las columnas se
deciden por los encabezados impresos en la propia diapositiva —PASO,
OPERACIONES GRAMATICALES, AUTORIDAD, EXPLICACIÓN—, no por conjeturas de
alineación. Las líneas de explicación que se parten en dos se asignan al paso
cuyo número está más cerca en vertical, que es como las compone Keynote.

De las columnas de forma, la de resultado se reconoce porque sólo la última
fila la rellena; las demás son, de izquierda a derecha, [prefijo] raíz, signo
e inflexión.

Nada se da por bueno sin comprobarlo: `auditar_verbo.py` coteja estas
escaleras con las del documento paso a paso.
"""

import glob
import json
import os
import re
import shutil
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUENTES = os.path.join(RAIZ, "docs", "fuentes", "verbo-diapositivas")
DESTINO = os.path.join(RAIZ, "recursos", "verbo", "diapositivas.json")

RE_PAGINA = re.compile(r'<page width="[\d.]+" height="[\d.]+">(.*?)</page>',
                       re.S)
RE_PALABRA = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" '
                        r'xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>')
RE_AUTORIDAD = re.compile(r"^(\d{1,3})/(\d{1,3})$")
RE_PASO = re.compile(r"^\d{1,2}$")

# Margen, en puntos, con que se ensancha cada encabezado para decidir a qué
# columna pertenece una palabra.
MARGEN = 60
# Dos palabras están en la misma línea si sus «y» distan menos que esto.
ALTO_LINEA = 8
# Dos valores caen en la misma columna de forma si sus «x» distan menos que
# esto. El texto va centrado en su celda, de modo que una misma columna varía
# una decena de puntos; las tablas más apretadas —las de causativo, que tienen
# cinco columnas de forma— dejan huecos de unos cuarenta. Treinta separa las
# dos cosas: con cuarenta y cinco, «ti» y «bhāvīyate» caían en la misma.
AGRUPA_X = 30

# pdftotext pierde las ligaduras fi/fl de la tipografía de estas diapositivas
# y las suelta al pie de la página. Se restituyen aquí; el aviso de
# `auditar_verbo.py` señala cualquier resto.
LIGADURAS = [("in exión", "inflexión"), ("in exiones", "inflexiones"),
             ("vocal nal", "vocal final"), ("la nal", "la final"),
             ("se re ere", "se refiere"), ("identi ca", "identifica"),
             ("signi ca", "significa"), ("su jo", "sufijo"),
             ("su jos", "sufijos")]


def limpiar(texto):
    for malo, bueno in LIGADURAS:
        texto = texto.replace(malo, bueno)
    return re.sub(r"\s+", " ", texto).strip()


def escapes(texto):
    return (texto.replace("&amp;", "&").replace("&lt;", "<")
            .replace("&gt;", ">").replace("&quot;", '"')
            .replace("&apos;", "'"))


def paginas(pdf):
    salida = subprocess.run(["pdftotext", "-bbox-layout", pdf, "-"],
                            capture_output=True, text=True)
    if salida.returncode != 0:
        sys.exit(f"pdftotext falló con {os.path.basename(pdf)}")
    for cuerpo in RE_PAGINA.findall(salida.stdout):
        yield [(float(x), float(y), escapes(t))
               for x, y, _, _, t in RE_PALABRA.findall(cuerpo) if t.strip()]


def lineas(palabras):
    """Agrupa las palabras de una página en líneas por su «y»."""
    fuera = []
    for x, y, t in sorted(palabras, key=lambda p: (p[1], p[0])):
        if fuera and abs(y - fuera[-1][0]) < ALTO_LINEA:
            fuera[-1][1].append((x, t))
        else:
            fuera.append((y, [(x, t)]))
    return [(y, sorted(ws)) for y, ws in fuera]


def encabezados(lns):
    """
    Columnas de la fila de títulos de la tabla.

    Devuelve {'paso': x, 'autoridad': x, 'explicacion': x, 'y': y}, donde «y»
    es la altura de esa misma fila: todo lo que esté por encima es el título
    de la diapositiva, no la tabla.
    """
    for y, ws in lns:
        texto = " ".join(t for _, t in ws).upper()
        if "PASO" in texto and "AUTORIDAD" in texto and "EXPLICACIÓN" in texto:
            col = {}
            for x, t in ws:
                clave = {"PASO": "paso", "AUTORIDAD": "autoridad",
                         "EXPLICACIÓN": "explicacion"}.get(t.upper())
                if clave:
                    col[clave] = x
            if len(col) == 3:
                col["y"] = y
                return col
    return None


def escalera(lns, col):
    """Los pasos de una tabla de formación, según los encabezados «col»."""
    lim_paso = col["paso"] + MARGEN
    lim_autoridad = col["autoridad"] - MARGEN
    lim_explicacion = col["explicacion"] - MARGEN
    if not (lim_paso < lim_autoridad < lim_explicacion):
        return None

    # las filas son las líneas que empiezan por un número en la columna PASO
    filas = []
    for y, ws in lns:
        if y <= col["y"]:
            continue
        x, t = ws[0]
        if x < lim_paso and RE_PASO.match(t):
            filas.append({"n": int(t), "y": y, "celdas": {},
                          "autoridades": [], "explicacion": []})
    if not filas:
        return None

    def paso_de(y):
        return min(filas, key=lambda f: abs(f["y"] - y))

    # Dónde acaba la tabla. Debajo suelen ir la nota al pie de la diapositiva
    # («Nota: la autoridad se refiere…») y el pie con la traducción del verbo;
    # si se colaran, sus palabras inventarían columnas. El límite se toma del
    # propio interlineado de la tabla.
    ys = [f["y"] for f in filas]
    huecos = sorted(b - a for a, b in zip(ys, ys[1:]))
    paso_medio = huecos[len(huecos) // 2] if huecos else 50.0
    fondo = filas[-1]["y"] + 0.8 * paso_medio
    for y, ws in lns:
        if y > filas[-1]["y"] and ws and ws[0][1].rstrip(":").lower() == "nota":
            fondo = min(fondo, y - 1)

    for y, ws in lns:
        if y <= col["y"] or y > fondo:
            continue
        destino = paso_de(y)
        for x, t in ws:
            if x < lim_paso:
                continue
            if x >= lim_explicacion:
                destino["explicacion"].append((y, x, t))
            elif x >= lim_autoridad:
                m = RE_AUTORIDAD.match(t)
                if m:
                    destino["autoridades"].append({"kacc": int(m.group(1)),
                                                   "ru": int(m.group(2))})
                else:
                    destino["explicacion"].append((y, x, t))
            else:
                destino["celdas"].setdefault(round(x), []).append((y, x, t))

    if any(not f["autoridades"] for f in filas):
        return None

    # columnas de forma: se agrupan las «x» vecinas
    xs = sorted({x for f in filas for x in f["celdas"]})
    grupos = []
    for x in xs:
        if grupos and x - grupos[-1][-1] <= AGRUPA_X:
            grupos[-1].append(x)
        else:
            grupos.append([x])

    def grupo_de(x):
        for i, g in enumerate(grupos):
            if x in g:
                return i
        return None

    # la columna de resultado sólo la rellena la última fila
    ocupadas = [{grupo_de(x) for x in f["celdas"]} for f in filas]
    col_resultado = None
    for i in range(len(grupos)):
        if i in ocupadas[-1] and all(i not in o for o in ocupadas[:-1]):
            col_resultado = i
    formas = [i for i in range(len(grupos)) if i != col_resultado]
    nombres = ["prefijo", "raiz", "signo", "inflexion"][-len(formas):] \
        if len(formas) <= 4 else ["prefijo", "raiz", "signo", "inflexion"]
    mapa = dict(zip(formas[-len(nombres):], nombres))

    pasos = []
    for f in filas:
        paso = {"n": f["n"], "prefijo": "", "raiz": "", "signo": "",
                "inflexion": "", "resultado": "",
                "autoridades": f["autoridades"]}
        for x, trozos in sorted(f["celdas"].items()):
            valor = " ".join(t for _, _, t in sorted(trozos))
            clave = ("resultado" if grupo_de(x) == col_resultado
                     else mapa.get(grupo_de(x)))
            if clave:
                paso[clave] = (paso[clave] + " " + valor).strip()
        texto = " ".join(t for _, _, t in sorted(f["explicacion"]))
        paso["operacion"] = limpiar(texto)
        pasos.append(paso)
    return pasos


def titulo(lns, col):
    """El «√ B H Ū (existiendo/estando)» y la línea «Formación: …»."""
    lema, glosa, formacion = "", "", ""
    for y, ws in lns:
        if y >= col["y"]:
            break
        texto = limpiar(" ".join(t for _, t in ws))
        if texto.startswith("√"):
            cuerpo = texto[1:].strip()
            lema = re.sub(r"\s+", "", cuerpo.split("(")[0]).lower()
            if "(" in cuerpo:
                glosa = cuerpo.split("(", 1)[1].rstrip(")").strip()
        elif texto.lower().startswith("formación"):
            formacion = texto
    return lema, glosa, formacion


def main():
    if not shutil.which("pdftotext"):
        sys.exit("Falta pdftotext (paquete poppler-utils).")
    pdfs = sorted(glob.glob(os.path.join(FUENTES, "*.pdf")))
    if not pdfs:
        sys.exit(f"No hay PDF en {os.path.relpath(FUENTES, RAIZ)}. "
                 "No viajan con el repositorio; ver el docstring.")

    escaleras, ilegibles = [], 0
    for pdf in pdfs:
        for n, palabras in enumerate(paginas(pdf), 1):
            lns = lineas(palabras)
            col = encabezados(lns)
            if not col:
                continue
            pasos = escalera(lns, col)
            if not pasos:
                ilegibles += 1
                print(f"  aviso: tabla ilegible en "
                      f"{os.path.basename(pdf)} p.{n}", file=sys.stderr)
                continue
            lema, glosa, formacion = titulo(lns, col)
            escaleras.append({
                "lema": lema,
                "glosa": glosa,
                "formacion": formacion,
                "fuente": "diapositiva",
                "presentacion": os.path.basename(pdf)[:-4],
                "pagina": n,
                "pasos": pasos,
            })

    datos = {
        "_nota": ("Extraído de las presentaciones por "
                  "herramientas/extraer_verbo_diapositivas.py. Los PDF no "
                  "viajan con el repositorio."),
        "fuente": {
            "autor": "Bhikkhu Nandisena",
            "obra": "GP-T · presentaciones de clase sobre el verbo",
            "presentaciones": len(pdfs),
        },
        "escaleras": escaleras,
    }
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    with open(DESTINO, "w", encoding="utf-8") as fh:
        json.dump(datos, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    print(os.path.relpath(DESTINO, RAIZ))
    print(f"  presentaciones  {len(pdfs)}")
    print(f"  escaleras       {len(escaleras)}"
          + (f"   ({ilegibles} ilegibles)" if ilegibles else ""))
    for e in escaleras:
        print(f"    {e['lema'] or '?':9s} {len(e['pasos'])} pasos   "
              f"{e['formacion'][:60]}")


if __name__ == "__main__":
    main()
