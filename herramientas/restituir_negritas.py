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
# Suelo de longitud del ancla. Estuvo en 24 desde el principio, cuando la
# única regla de colocación era «aparece una sola vez»: entonces una línea
# corta sí era peligrosa, porque cuanto más corta más fácil que casara por
# casualidad. Bajado a 16 en la sesión 24, y no por optimismo — se midió.
#
# De las 17 líneas del Nāma que caían por debajo de 24:
#
#     10  únicas en el PDF y únicas en el maestro (1=1) → colocables
#      6  ausentes de todos modos: «**2-NĀMA-KAPPA**», rótulos ingleses,
#         fragmentos de nota al pie. El suelo no aportaba nada aquí.
#      1  «honti **aṃ**mhi vibhattimhi» — 2 en el maestro y 1 en el PDF
#
# Esa última es la única de verdad peligrosa, y **no la para el suelo: la para
# la regla de las cuentas** (sesión 23), que exige que el maestro repita la
# línea tantas veces como el PDF. De modo que el suelo no atrapaba ya nada que
# las demás reglas no atrapasen, y a cambio rechazaba nueve lemas legítimos
# —«**Vā** ti kimatthaṃ? Aggi.», 19 caracteres— por el solo hecho de que el
# ejemplo que los ilustra es corto.
#
# Se conserva un suelo, no se quita: por debajo de 16 quedan los rótulos y los
# restos de numeración, que no son texto que colocar.
MINIMO = 16
# Siglas de cita, **de más larga a más corta**. El orden importa: la
# alternación de `re` se queda con la primera que case, de modo que un `Vin`
# colocado antes que `VinA` se comía las tres primeras letras de «VinA» y
# dejaba una `A` que ya no encajaba con lo que sigue. Estaba así, y por eso
# `VinA` y `AbhiA` no se reconocían nunca (sesión 24).
#
# `AbhiA` y `Rū` faltaban directamente: la primera sale en el PDF del Nāma
# —«(AbhiA. i, 337)», §94—, la segunda en los maestros.
_SIGLAS = ("ItivuttaA|PetavatthuA|UdānaA|AbhiA|VinA|Abhi|Khu|Sad|Mog|DhA"
           "|Rū|DA|MA|SA|AA|Vin|D|M|A|S|J")
RE_SALTABLE = re.compile(
    r'\[\^\d+\]'                                   # nota al pie
    # `\(\s*` y no `\(`: el PDF imprime «( D. ii, 6)» con un espacio suelto
    # tras el paréntesis (§93), y sin esta holgura la cita no se reconocía,
    # de modo que quedaba dentro del ancla y ninguna línea encontraba sitio.
    r'|\(\s*(?:' + _SIGLAS + r')\.?\s*[ivxlIVXL]+\s*,[^()]*\)')  # cita


# La única divergencia de división registrada del proyecto (sesión 22, y
# «vale para toda su clase»): en el locativo ante «iti», Nandisena contrae
# —«Yosvī ti», «Sesesū ti»— y el maestro escribe la forma suelta, «Yosv
# iti». El IEBH decidió que manda el maestro.
#
# La negrita del PDF cubre el lemma contraído, «**Yosvī** ti», de modo que
# sin bridge ninguna de estas líneas encuentra su sitio: son la mayor parte
# de las 57 ausentes del Nāma. Se reescribe la línea del PDF a la división
# del maestro —«**Yosv** iti»—, que deja la negrita justo donde le toca.
#
# No es tolerancia de emparejamiento: es una regla cerrada y documentada,
# como `VARIANTES` en `restituir_citas.py`. Lo que no encaje en ella sigue
# informándose como ausente.
#
# **La negrita acaba en el locativo, no dentro de «iti»** (el IEBH, sesión
# 23). En el PDF la 'ī' de «Yosvī» es la 'i' de «iti» absorbida por la
# contracción, así que al deshacerla esa letra vuelve a «iti» y sale de la
# negrita: lo que el sutta nombra es «yosu», no «yosv i».
RE_REDIV = (
    # «**Yosvī** ti» · «**Sesesū** ti» → «**Yosv** iti»
    (re.compile(r'\*\*([^*]+?)s(?:vī|ū)\s*\*\*\s*ti\b'), r'**\1sv** iti'),
    # «**Su-naṃ-hi-**sū ti» → la negrita acaba antes del locativo
    (re.compile(r'\*\*([^*]+?)\*\*s(?:vī|ū)\s+ti\b'), r'**\1sv** iti'),
)


# Dos averías del PDF que **cambian la longitud** y por eso no caben en
# `VARIANTES`, que trabaja sobre la cadena normalizada y necesita conservarla.
# Se reparan aquí, sobre la línea cruda, antes de normalizar nada.
#
#     PDF                    maestro              qué pasó
#     **Etevī** ti           Etesv iti            's' salió como 'v'
#     **Tumha-mhākam** iti   Tumha-amhākaṃ iti    se perdió la 'a' y la 'ṃ'
#
# Igual que `VARIANTES`, es tabla cerrada y cotejada a mano, no tolerancia.
# Las dos formas de la izquierda salen **una sola vez en el PDF** y **ninguna
# en el maestro**, de modo que la regla no puede dispararse donde no toca. Y
# el PDF escribe «Etesvī» bien otras cinco veces, que es lo que confirma que
# «Etevī» es esa misma palabra estropeada y no otra cosa.
RE_DEFECTO = (
    (re.compile(r'\*\*Etevī\*\*\s*ti\b'), r'**Etesv** iti'),
    (re.compile(r'\*\*Tumha-mhākam\*\*\s*iti\b'), r'**Tumha-amhākaṃ** iti'),
)


def redividir(linea):
    """Reescribe el locativo contraído del PDF a la división del maestro.

    Y repara de paso las dos averías de `RE_DEFECTO`, que no son división
    sino letras que la capa de texto perdió.
    """
    n = 0
    for regex, con in RE_DEFECTO + RE_REDIV:
        linea, k = regex.subn(con, linea)
        n += k
    return linea, n


# Lo que la capa de texto del PDF pierde, cotejado una a una (sesión 24).
#
# Nueve líneas del Nāma no encontraban su sitio por **un solo carácter**, y
# siempre el mismo tipo de avería: un diacrítico que `pdftohtml` no devuelve.
# No son variantes de lectura ni erratas de Nandisena —el PDF *imprime* el
# diacrítico, lo que falla es extraerlo—, así que **no se corrige nada**: se
# le enseña al emparejador, igual que `VARIANTES` en `restituir_citas.py`.
#
#     PDF (capa de texto)        maestro          avería
#     kimattham                  kimatthaṃ        m por ṃ   (§76, §194)
#     Pancādīnaṃ                 Pañcādīnaṃ       n por ñ   (§90)
#     Vibhasā                    Vibhāsā          a por ā   (§154)
#
# **Esto no es tolerancia de emparejamiento.** Es una tabla cerrada: cada
# entrada se comprobó contra el PDF con los ojos, y lo que no esté en ella
# sigue saliendo como ausente. La alternativa —plegar los diacríticos y
# aceptar el ancla si el resultado es único— se descartó: en pāḷi la cantidad
# vocálica significa, y la comprobación de reconstrucción **no detectaría** una
# negrita bien puesta sobre la letra equivocada, porque sólo demuestra que al
# quitar el marcado vuelve el maestro intacto.
#
# Dos condiciones que hacen segura cada entrada:
#
#   1. **La forma de la izquierda no existe en el maestro.** Comprobado: el
#      maestro escribe `kimatthaṃ` 198 veces y `kimattham` ninguna, de modo que
#      la sustitución no puede pisar nada legítimo.
#   2. **Conserva la longitud**, carácter por carácter, porque las marcas de
#      negrita son índices sobre la cadena normalizada. Lo garantiza el
#      `assert` de abajo.
#
# Sustituida la grafía, decide la regla de siempre: el ancla se coloca sólo si
# aparece una vez. La tabla no coloca nada por sí misma.
#
# §190 merece nota aparte. Es la única de las nueve donde el diacrítico está en
# el PDF y falta en el maestro —`evamādīto` frente a `evamādito`—, que leído sin
# más parecería errata nuestra. No lo es: **el propio PDF imprime `evamādito`
# cuatro veces y `evamādīto` una**, justo ahí. El maestro sigue a la mayoría y
# se queda como está; es un singleton de la edición base, de la clase de
# `brāhamaṇā` (sesión 23).
VARIANTES = (
    ("kimattham",      "kimatthaṃ"),       # §76, §194
    ("Pancādīnaṃ",     "Pañcādīnaṃ"),      # §90
    ("Pañcadīnam",     "Pañcādīnam"),      # §134
    ("Vibhasā",        "Vibhāsā"),         # §154
    ("parealutte",     "pareālutte"),      # §77
    ("aṃ-āadesā",      "aṃ-āādesā"),       # §68
    ("aṃnamiccetesu",  "aṃnaṃiccetesu"),   # §132
    ("evamādīto",      "evamādito"),       # §190 — al revés, ver arriba
)

for _pdf, _mae in VARIANTES:
    assert len(_pdf) == len(_mae), (
        "VARIANTES: «{0}» y «{1}» no miden lo mismo; las marcas de negrita son "
        "índices sobre la cadena normalizada y se descolocarían.".format(
            _pdf, _mae))


def variantes(norm):
    """Reescribe la grafía del PDF a la del maestro. Sólo del lado del PDF."""
    n = 0
    for pdf, mae in VARIANTES:
        norm, k = norm.replace(pdf, mae), norm.count(pdf)
        n += k
    return norm, n


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
    # Grafías que la capa de texto del PDF pierde. Va aquí y no en
    # `normalizar` porque sólo se aplica al lado del PDF: el maestro es la
    # referencia y no se toca. Conserva la longitud, así que las marcas de
    # abajo —índices sobre esta misma cadena— siguen valiendo.
    norm, _ = variantes(norm)
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

    # Primera pasada: cuántas veces trae el PDF cada línea. Hace falta antes
    # de colocar nada, porque una línea repetida sólo es colocable si el
    # maestro la repite **el mismo número de veces**.
    utiles, redivididas = [], 0
    for linea_pdf in lineas_del_pdf(args.pdf):
        if "**" not in linea_pdf or RE_TITULO_PDF.match(linea_pdf):
            continue
        linea_pdf, n = redividir(linea_pdf)
        redivididas += n
        norm, marcas = tramos(linea_pdf)
        if not marcas or len(norm) < MINIMO:
            continue
        utiles.append((linea_pdf, norm, marcas))

    veces_pdf = {}
    for _, norm, _ in utiles:
        veces_pdf[norm] = veces_pdf.get(norm, 0) + 1
    usadas = dict.fromkeys(veces_pdf, 0)

    colocadas, ambiguas, ausentes = [], [], []
    emparejadas = 0
    for linea_pdf, norm, marcas in utiles:
        hits = []
        for sutta, (region, mapa) in regiones.items():
            desde = region.find(norm)
            while desde != -1:
                hits.append((sutta, desde, mapa))
                desde = region.find(norm, desde + 1)
        if not hits:
            ausentes.append(linea_pdf)
        elif len(hits) == 1:
            sutta, desde, mapa = hits[0]
            colocadas.append((sutta, [(desde + a, desde + b)
                                      for a, b in marcas], mapa))
        elif len(hits) == veces_pdf[norm]:
            # Repetida no es ambigua **cuando las cuentas cuadran**
            # (sesión 23). «Ekavacanesv iti kimatthaṃ? Tāsaṃ, sabbāsaṃ.»
            # sale dos veces en el PDF —una por sutta— y dos veces en el
            # maestro, §62 y §66: no hay nada que adivinar, es una
            # correspondencia uno a uno que se resuelve por orden.
            #
            # Exigir que las cuentas coincidan es lo que hace segura la
            # regla. Un primer intento colocó la línea en *todas* sus
            # apariciones sin más, y falló: las líneas que se repiten son
            # las genéricas, salen en muchos más sitios de los que el PDF
            # tiene, el marcado se entrelaza con la negrita ya puesta y la
            # reconstrucción deja de reproducir el maestro. Con las cuentas
            # de por medio, ésas se descartan solas.
            orden = usadas[norm]
            usadas[norm] += 1
            if orden < len(hits):
                sutta, desde, mapa = sorted(
                    hits, key=lambda h: (h[0], h[1]))[orden]
                colocadas.append((sutta, [(desde + a, desde + b)
                                          for a, b in marcas], mapa))
                emparejadas += 1
        else:
            ambiguas.append(linea_pdf)

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
            # Y si el tramo *pisa a medias* una negrita que ya está, se
            # descarta (sesión 23). Antes sólo se miraba la coincidencia
            # exacta, de modo que un tramo que empezara dentro de una
            # negrita existente y acabara fuera producía marcado
            # entrelazado —`**a**b**c**`— que `pelar` ya no sabe deshacer:
            # es lo que hacía fallar la reconstrucción al colocar una misma
            # línea en varios suttas.
            if any(not (j <= m.start() or i >= m.end())
                   and not (i >= m.start() and j <= m.end())
                   for m in RE_NEGRITA.finditer(bloque)):
                solapes += 1
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
    print("  líneas redivididas (locativo) : {0}".format(redivididas))
    print("  repetidas emparejadas por orden: {0}".format(emparejadas))
    print("  solapes descartados           : {0}".format(solapes))
    print("  ya estaban en negrita         : {0}".format(ya_estaban))
    print("  negrita en el maestro: {0} → {1}".format(
        len(RE_NEGRITA.findall(original)), len(RE_NEGRITA.findall(nuevo))))
    print("  reconstrucción: {0}".format("OK" if ok else "FALLA"))
    for l in ausentes:
        print("    ausente: {0}".format(l[:150]))

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
