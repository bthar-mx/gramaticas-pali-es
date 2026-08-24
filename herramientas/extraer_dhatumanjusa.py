#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrae la Dhātumañjūsā del transcrito de A. Ruiz-Falqués.

    python3 herramientas/extraer_dhatumanjusa.py ruta/al/dhatupatha.pdf

Escribe recursos/raices/dhatumanjusa.json.

La fuente es la misma que la del Dhātupāṭha: «The Pāli Dhātupāṭha and the
Dhātumañjūsā», ed. Dines Andersen y Helmer Smith (Copenhague, 1921), en la
transcripción de A. Ruiz-Falqués (Taunggyi, 2019). La obra es la
Kaccāyana-Dhātumañjūsā, atribuida a Sīlavaṃsa, que pone en verso la lista de
raíces.

Qué se extrae y qué no
----------------------
La Dhātumañjūsā es un poema: 154 estrofas en śloka, en las que las raíces y
sus significados van encajados en el metro, con elisión, compuestos y
palabras partidas entre pādas. Sacar de ahí pares raíz-significado exigiría
deshacer el metro, y eso es interpretar, no transcribir.

De modo que aquí se extrae lo que el texto dice sin ambigüedad:

  - la estrofa, con su número y sus versos tal como se imprimen;
  - el rango de raíces que cada verso numera —«(97—99)»—, que es del propio
    editor y va entre paréntesis;
  - la sección de gaṇa en que cae la estrofa;
  - las notas críticas, que la edición numera por raíz y no por estrofa.

El enlace con una raíz concreta se establece sólo cuando el lema aparece
literalmente como palabra en el verso. No se deduce ninguno del metro.

Requiere pymupdf.
"""

import json
import os
import re
import sys
import unicodedata

try:
    import pymupdf
except ImportError:
    sys.exit("Hace falta pymupdf:  pip3 install pymupdf")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, "recursos", "raices", "dhatumanjusa.json")

INICIO = "Namo Buddhāya"
FIN = "Kaccāyana-Dhātumañjūsā samattā"

# Cabecera de sección de gaṇa: «I, a.», «II.»…
GANA = re.compile(r'^(IX|VIII|VII|VI|IV|V|III|II|I)\s*,?\s*([a-d])?\.\s*$')
# Número de estrofa al principio del verso.
ESTROFA = re.compile(r'^(\d{1,3})\.\s+')
# Rango de raíces que la edición imprime entre paréntesis al final del verso.
RANGO = re.compile(r'\((\d{1,3})\s*[—–-]\s*(\d{1,3})\)|\((\d{1,3})\)')

# En esta obra las notas van en el mismo cuerpo de letra que el texto, al
# revés que en el Dhātupāṭha, así que no se pueden separar por tamaño. Y el
# salto vertical tampoco vale: una estrofa con una palabra interlineada abre
# un hueco tan grande como el del pie.
#
# Lo que sí distingue: la edición cierra cada verso con el rango de raíces
# entre paréntesis, y las notas no llevan ninguno. De modo que las notas son
# la tirada final de líneas sin rango. Para no confundir con ellas un último
# verso que se quedara sin rango, se exige además que la primera línea del
# bloque empiece por un número de raíz o cite un manuscrito.
SIGLA = re.compile(r"(\bC[kbip]+\b|\bKD\b|Mss\.|\bcf\.|\bvide\b|\bW\.)")


def lineas(doc, pno):
    """[(y, texto)] de la página, ordenadas de arriba abajo."""
    fuera = []
    for b in doc[pno].get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            t = "".join(s["text"] for s in l["spans"])
            if t.strip():
                fuera.append((round(l["bbox"][1], 1), t.strip()))
    fuera.sort()
    return fuera


def partir(ls):
    """(cuerpo, notas) de una página."""
    ts = [t for _, t in ls
          if not (t.startswith("[") and t.endswith("]"))]
    i = len(ts)
    while i > 0 and not RANGO.search(ts[i - 1]):
        i -= 1
    cuerpo, notas = ts[:i], ts[i:]
    while notas and not (re.match(r"^\d{1,3}\s*[-–—]?\s*\d{0,3}\.", notas[0])
                         or SIGLA.search(notas[0])):
        cuerpo.append(notas.pop(0))
    return cuerpo, notas


def parsear_notas(trozos):
    """(notas de raíz, notas de estrofa) del bloque al pie.

    La edición encadena las notas separándolas con raya, y las numera de dos
    maneras que no hay que confundir: «v.2.» habla de la estrofa 2, mientras
    que «14.» o «No. 14.» hablan de la raíz 14.
    """
    texto = re.sub(r"\s+", " ", " ".join(trozos)).strip()
    de_raiz, de_estrofa = {}, {}
    if not texto:
        return de_raiz, de_estrofa
    for pieza in re.split(r"\s+[—–]\s+", texto):
        pieza = pieza.strip()
        m = re.match(r"^v\.\s*(\d{1,3})\.\s*(.+)$", pieza)
        if m:
            de_estrofa[int(m.group(1))] = m.group(2).strip()
            continue
        m = re.match(r"^(?:No\.\s*)?(\d{1,3})(?:\s*[-–—]\s*\d{1,3})?\.\s*(.+)$",
                     pieza)
        if m:
            de_raiz[int(m.group(1))] = m.group(2).strip()
    return de_raiz, de_estrofa


def parsear(pdf):
    doc = pymupdf.open(pdf)
    estrofas, notas, gana, signo = [], {}, None, None
    notas_estrofa = {}
    descartadas = []
    terminado = False
    dentro = False
    actual = None

    for pno in range(len(doc)):
        ls = lineas(doc, pno)
        entera = " ".join(t for _, t in ls)
        if not dentro and INICIO in entera:
            dentro = True
        if not dentro:
            continue

        cuerpo, pie = partir(ls)
        a, b = parsear_notas(pie)
        notas.update(a)
        notas_estrofa.update(b)

        for t in cuerpo:
            if FIN in t:
                terminado = True
            if terminado or INICIO in t or t.startswith("_") \
               or t.strip("_ *") == "":
                continue
            g = GANA.match(t)
            if g:
                gana, signo = g.group(1), g.group(2)
                continue
            m = ESTROFA.match(t)
            # Una nota al pie empieza igual que una estrofa, por un número y
            # un punto. Lo que las separa es que las estrofas van seguidas:
            # sólo se abre una si el número es el siguiente al último. Así el
            # propio texto verifica la lectura, sin heurísticas.
            if m and int(m.group(1)) == (estrofas[-1]["n"] + 1 if estrofas else 1):
                actual = {"n": int(m.group(1)), "versos": [], "rangos": [],
                          "gana": gana, "signo": signo, "pagina": pno + 1,
                          "notas": []}
                estrofas.append(actual)
                t = t[m.end():]
            elif m:
                # No es una estrofa: es una nota al pie que se coló en el
                # cuerpo. Se manda al analizador de notas, no se tira.
                descartadas.append((pno + 1, t[:60]))
                a, b = parsear_notas([t])
                notas.update(a)
                notas_estrofa.update(b)
                continue
            if actual is None:
                continue
            for a, b, solo in RANGO.findall(t):
                if solo:
                    actual["rangos"].append([int(solo), int(solo)])
                else:
                    actual["rangos"].append([int(a), int(b)])
            verso = RANGO.sub("", t).strip()
            if verso:
                actual["versos"].append(verso)

        if FIN in entera:
            break

    # Las notas van numeradas por raíz; se cuelgan de la estrofa cuyo rango
    # la contiene.
    for e in estrofas:
        for n, txt in notas.items():
            if any(a <= n <= b for a, b in e["rangos"]):
                e["notas"].append({"raiz_n": n, "texto": txt})
        e["notas"].sort(key=lambda x: x["raiz_n"])
        if e["n"] in notas_estrofa:
            e["notas"].insert(0, {"raiz_n": None,
                                  "texto": notas_estrofa[e["n"]]})
    sueltas = [n for n in notas
               if not any(any(a <= n <= b for a, b in e["rangos"])
                          for e in estrofas)]
    return estrofas, notas, sorted(sueltas), descartadas


# --------------------------------------------------------------------------

def palabras(verso):
    """Las palabras de un verso, deshechos apóstrofos y guiones."""
    limpio = re.sub(r"[’'‘\-–—.,;!?()]", " ", verso)
    return [unicodedata.normalize("NFC", w.lower())
            for w in limpio.split() if w]


CABECERA = {
    "_nota": "La Kaccāyana-Dhātumañjūsā, atribuida a Sīlavaṃsa: la lista de "
             "raíces puesta en verso. Transcrita de «The Pāli Dhātupāṭha and "
             "the Dhātumañjūsā», ed. Dines Andersen y Helmer Smith, "
             "Copenhague 1921, en la transcripción de A. Ruiz-Falqués "
             "(Taunggyi, 2019). Se transcriben las estrofas tal como se "
             "imprimen, con el rango de raíces que la edición numera entre "
             "paréntesis y las notas críticas, que van numeradas por raíz. "
             "NO se separan aquí pares de raíz y significado: en el verso van "
             "encajados en el metro, y deshacerlo sería interpretar. La "
             "numeración de raíces de esta obra es la suya propia y no "
             "coincide con la del Dhātupāṭha.",
    "fuente": {
        "titulo": "The Pāli Dhātupāṭha and the Dhātumañjūsā",
        "obra": "Kaccāyana-Dhātumañjūsā",
        "autor": "Sīlavaṃsa",
        "editores": "Dines Andersen y Helmer Smith",
        "lugar": "Copenhague",
        "anyo": 1921,
        "transcripcion": "A. Ruiz-Falqués, Taunggyi, 2019",
    },
}


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: python3 herramientas/extraer_dhatumanjusa.py "
                 "ruta/al/dhatupatha.pdf")
    estrofas, notas, sueltas, descartadas = parsear(sys.argv[1])

    if not estrofas:
        sys.exit("no se ha encontrado la Dhātumañjūsā en ese PDF")

    datos = dict(CABECERA)
    datos["estrofas"] = estrofas
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    json.dump(datos, open(DESTINO, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    versos = sum(len(e["versos"]) for e in estrofas)
    maxr = max((b for e in estrofas for _, b in e["rangos"]), default=0)
    print("{0} estrofas · {1} versos · raíces numeradas hasta la {2} · "
          "{3} notas críticas → {4}".format(
              len(estrofas), versos, maxr, len(notas),
              os.path.relpath(DESTINO, RAIZ)))
    ns = [e["n"] for e in estrofas]
    faltan = sorted(set(range(min(ns), max(ns) + 1)) - set(ns))
    if faltan:
        print("  aviso — estrofas sin texto: {0}".format(faltan))
    if sueltas:
        print("  notas cuyo número de raíz no cae en ninguna estrofa: "
              "{0}".format(sueltas))
    if descartadas:
        print("  líneas numeradas descartadas por romper la secuencia: "
              "{0}".format(len(descartadas)))
        for pg, t in descartadas[:5]:
            print("      p.{0} {1!r}".format(pg, t))
    return 0


if __name__ == "__main__":
    sys.exit(main())
