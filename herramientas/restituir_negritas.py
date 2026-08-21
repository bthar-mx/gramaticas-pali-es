#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Restituye en los maestros la negrita que Nandisena imprime **dentro del
vutti**: las letras o sílabas que el propio sutta nombra.

    §237 Itthiyam ato āpaccayo
         Itthiyaṃ vattamānāya **a**kārato **ā**paccayo hoti.

No es adorno. Señala qué parte de la explicación responde a qué palabra del
aforismo, y es de las pocas ayudas de lectura que trae la edición base.

Se perdió al convertir el PDF a texto: los maestros no tienen ni una marca
dentro del vutti. Sobrevive sólo en el PDF, donde la negrita es una fuente
aparte (`Times-Bold`), de modo que `pdftohtml -xml` la devuelve etiquetada.

Principio de siempre: **proponer y verificar, nunca afirmar.**

  1. Del PDF se sacan las líneas con la negrita marcada.
  2. Una línea sólo se usa si, sin marcas, aparece **una sola vez** en los
     bloques pāḷi de todo el capítulo. Eso acota el alcance a lo que debe
     llevarla —el vutti— sin adivinar qué línea es cuál, y descarta solo
     encabezados, líneas inglesas, notas y numeración.
  3. Se compara sin espacios: en el PDF los diacríticos vienen de otra
     fuente, así que las palabras llegan partidas y el espacio que separa
     los tramos es a veces posición y no carácter («si gasañño» sale como
     «sigasañño»). Y se busca por subcadena, porque el PDF parte en líneas
     físicas lo que el maestro guarda como párrafo entero.
  4. Aplicada la negrita, quitarla tiene que devolver el maestro **idéntico
     byte a byte**. Si no, no se escribe nada.

Lo que no encaja se informa; no se coloca a ojo. En particular **no se toca
el título del sutta**, que en el PDF va entero en negrita y aquí no la
lleva.

    python3 herramientas/restituir_negritas.py --pdf ~/ruta.pdf --capitulo nama
    python3 herramientas/restituir_negritas.py --pdf ~/ruta.pdf --capitulo nama --aplicar
"""

import argparse
import os
import re
import subprocess
import sys
import unicodedata
import xml.etree.ElementTree as ET

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# El archivo que el generador lee de verdad. El Sandhi no tiene
# `convertir_sandhi.py`: su fuente viva es la de `kaccayana/`, y
# `docs/1. Sandhi-Kappa.md` es sólo el maestro archivado.
MAESTROS = {
    "sandhi": "kaccayana/01-sandhi-kappa.md",
    "nama":   "docs/2. Nāma-Kappa.md",
    "karaka": "docs/3. Kāraka-Kappa.md",
}

RE_HDR = re.compile(r'^\*\*(\d{1,3})\\\.\s')
RE_NEGRITA = re.compile(r'\*\*([^*]+)\*\*')
RE_TITULO_PDF = re.compile(r'^\*\*\d{1,3}\.\s+[\d, ]+\.\s')
MINIMO = 24          # una línea más corta no identifica nada por sí sola
_SIGLAS = ("Khu|Vin|Abhi|DhA|DA|MA|SA|AA|VinA|ItivuttaA|UdānaA"
           "|PetavatthuA|Sad|Mog|D|M|A|S|J")
RE_SALTABLE = re.compile(
    r'\[\^\d+\]'                                   # nota al pie
    r'|\((?:' + _SIGLAS + r')\.?\s*[ivxlIVXL]+\s*,[^()]*\)')  # cita


def normalizar(s):
    """(texto comparable, mapa al original).

    mapa[i] es la posición en `s` del carácter i del texto normalizado.

    Se vuelve ciego a todo lo que un lado tiene y el otro no:

    - **espacios**: en el PDF los diacríticos vienen de otra fuente, así que
      las palabras llegan partidas y el espacio que separa los tramos es a
      veces posición y no carácter («si gasañño» sale «sigasañño»);
    - **asteriscos**: el Kāraka ya trae en negrita los rótulos del vutti;
    - **glosas emergentes** `{akkharā|letras}`, que sólo están en el
      maestro del Sandhi;
    - **marcadores de nota** `[^22]` y **citas canónicas** `(Khu. i, 27)`:
      el Sandhi guarda en notas al pie lo que el PDF imprime entre
      paréntesis, y el Nāma al revés.
    """
    saltar = set()
    for m in RE_SALTABLE.finditer(s):
        saltar.update(range(m.start(), m.end()))
    fuera, mapa, en_glosa = [], [], False
    for i, c in enumerate(s):
        if i in saltar:
            continue
        if en_glosa:
            if c == "}":
                en_glosa = False
            continue
        if c == "|":
            en_glosa = True
            continue
        if c in "\\*{}" or c.isspace():
            continue
        c = {"’": "'", "‘": "'", "“": '"', "”": '"',
             "–": "-", "—": "-"}.get(c, c)
        fuera.append(unicodedata.normalize("NFC", c))
        mapa.append(i)
    # División adoptada por el proyecto (guía de estilo §5 bis): el maestro
    # escribe «Saṃ-sāsv iti» donde el PDF imprime «Saṃ-sāsvī ti». Sin
    # espacios queda «svīti» frente a «sviti»; se igualan las dos. Es una
    # equivalencia estrecha a propósito: en pāḷi la cantidad vocálica
    # significa, y no se toca la 'ī' en ningún otro contexto.
    # La sustitución conserva la longitud, así que `mapa` sigue valiendo.
    return re.sub("svīti", "sviti", "".join(fuera)), mapa


def lineas_del_pdf(ruta):
    """Líneas del PDF con la negrita marcada `**así**`."""
    xml = subprocess.run(["pdftohtml", "-xml", "-i", "-stdout", ruta],
                         capture_output=True).stdout
    raiz = ET.fromstring(xml)
    salida = []
    for pg in raiz.iter("page"):
        filas = {}
        for t in pg.iter("text"):
            filas.setdefault(int(t.get("top")), []).append(
                (int(t.get("left")), "".join(t.itertext()),
                 t.find("b") is not None))
        for top in sorted(filas):
            linea, negrita = "", False
            for _, txt, neg in sorted(filas[top]):
                if neg != negrita:
                    linea += "**"
                linea += txt
                negrita = neg
            if negrita:
                linea += "**"
            linea = re.sub(r'\*\*\s*\*\*', '', linea).strip()
            if linea:
                salida.append(linea)
    return salida


def region_pali(bloque):
    """(inicio, fin) del bloque pāḷi: del encabezado al primer `---`."""
    lineas = bloque.split("\n")
    ini = len(lineas[0]) + 1 if lineas else 0
    pos = ini
    for l in lineas[1:]:
        if l.strip() == "---":
            return ini, pos
        pos += len(l) + 1
    return ini, len(bloque)


def partir(texto):
    bloques, actual, buf = {}, None, []
    for l in texto.split("\n"):
        m = RE_HDR.match(l)
        if m:
            if actual is not None:
                bloques[actual] = "\n".join(buf)
            actual, buf = int(m.group(1)), [l]
        elif actual is not None:
            buf.append(l)
    if actual is not None:
        bloques[actual] = "\n".join(buf)
    return bloques


def tramos(linea_pdf):
    """(texto plano normalizado, [(ini, fin)] en esa forma)."""
    plano, marcas, pos = "", [], 0
    for trozo in re.split(r'(\*\*[^*]+\*\*)', linea_pdf):
        if not trozo:
            continue
        if trozo.startswith("**"):
            cuerpo = trozo[2:-2]
            marcas.append((pos, pos + len(cuerpo)))
            plano += cuerpo
            pos += len(cuerpo)
        else:
            plano += trozo
            pos += len(trozo)
    norm, _ = normalizar(plano)
    fuera = []
    for ini, fin in marcas:
        a, _ = normalizar(plano[:ini])
        b, _ = normalizar(plano[:fin])
        if len(b) > len(a):
            fuera.append((len(a), len(b)))
    return norm, fuera


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--capitulo", required=True, choices=sorted(MAESTROS))
    ap.add_argument("--aplicar", action="store_true")
    args = ap.parse_args()

    ruta = os.path.join(RAIZ, MAESTROS[args.capitulo])
    original = open(ruta, encoding="utf-8").read()
    bloques = partir(original)

    # Región pāḷi de cada sutta, normalizada, con su mapa al bloque.
    regiones = {}
    for sutta, bloque in bloques.items():
        ini, fin = region_pali(bloque)
        norm, mapa = normalizar(bloque[ini:fin])
        regiones[sutta] = (norm, [ini + i for i in mapa])

    colocadas, ambiguas, ausentes = [], [], []
    for linea_pdf in lineas_del_pdf(args.pdf):
        if "**" not in linea_pdf or RE_TITULO_PDF.match(linea_pdf):
            continue
        norm, marcas = tramos(linea_pdf)
        if not marcas or len(norm) < MINIMO:
            continue
        hits = []
        for sutta, (region, mapa) in regiones.items():
            desde = region.find(norm)
            while desde != -1:
                hits.append((sutta, desde, mapa))
                desde = region.find(norm, desde + 1)
                if len(hits) > 1:
                    break
            if len(hits) > 1:
                break
        if not hits:
            ausentes.append(linea_pdf)
        elif len(hits) > 1:
            ambiguas.append(linea_pdf)
        else:
            sutta, desde, mapa = hits[0]
            colocadas.append((sutta, [(desde + a, desde + b)
                                      for a, b in marcas], mapa))

    # Aplicar por sutta, de atrás hacia delante.
    por_sutta = {}
    for sutta, marcas, mapa in colocadas:
        por_sutta.setdefault(sutta, []).append(marcas)

    nuevos, puestos, solapes, ya_estaban = dict(bloques), 0, 0, 0
    for sutta, grupos in por_sutta.items():
        bloque = bloques[sutta]
        _, mapa = regiones[sutta]
        planas = sorted(m for g in grupos for m in g)
        limpias, ultimo = [], -1
        for a, b in planas:
            if a < ultimo:            # dos líneas del PDF pisan lo mismo
                solapes += 1
                continue
            limpias.append((a, b))
            ultimo = b
        for a, b in sorted(limpias, reverse=True):
            if b > len(mapa):
                continue
            i, j = mapa[a], mapa[b - 1] + 1
            # Si el maestro ya lo trae en negrita, no se anida otra.
            if bloque[max(0, i - 2):i] == "**" and bloque[j:j + 2] == "**":
                ya_estaban += 1
                continue
            bloque = bloque[:i] + "**" + bloque[i:j] + "**" + bloque[j:]
            puestos += 1
        nuevos[sutta] = bloque

    salida, actual, cabecera = [], None, []
    for l in original.split("\n"):
        m = RE_HDR.match(l)
        if m:
            if actual is not None:
                salida.append(nuevos[actual])
            actual = int(m.group(1))
        elif actual is None:
            cabecera.append(l)
    if actual is not None:
        salida.append(nuevos[actual])
    nuevo = "\n".join(cabecera + salida)

    pelar = lambda t: RE_NEGRITA.sub(lambda m: m.group(1), t)
    ok = pelar(nuevo) == pelar(original)

    print("· {0}: {1} tramos en negrita colocados".format(
        args.capitulo, puestos))
    print("  líneas del PDF aprovechadas : {0}".format(len(colocadas)))
    print("  ambiguas (sale más de una vez): {0}".format(len(ambiguas)))
    print("  ausentes (no está en el pāḷi) : {0}".format(len(ausentes)))
    print("  solapes descartados           : {0}".format(solapes))
    print("  ya estaban en negrita         : {0}".format(ya_estaban))
    print("  negrita en el maestro: {0} → {1}".format(
        len(RE_NEGRITA.findall(original)), len(RE_NEGRITA.findall(nuevo))))
    print("  reconstrucción: {0}".format("OK" if ok else "FALLA"))
    for l in ausentes[:10]:
        print("    ausente: {0}".format(l[:94]))

    if not ok:
        print("NO SE ESCRIBE NADA.")
        return 1
    if args.aplicar:
        open(ruta, "w", encoding="utf-8").write(nuevo)
        print("  escrito {0}".format(MAESTROS[args.capitulo]))
    else:
        print("  (simulacro: no se ha tocado el maestro; usa --aplicar)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
