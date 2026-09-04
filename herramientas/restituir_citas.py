#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Restituye en los maestros españoles las referencias canónicas que la fase de
traducción retiró (guía de estilo §5; briefings 04 y 05, §10.1).

Qué pasó: durante la traducción se retiraron las referencias que Nandisena
imprime tras sus ejemplos —(Khu. i, 336) y semejantes— con el plan de
reponerlas «en la fase HTML». Nunca se hizo. El Nāma-Kappa publicado no
tiene ninguna y el Kāraka-Kappa sólo las de una nota al pie. El Sandhi-Kappa
sí las conserva: es anterior a aquella decisión.

Principio, el mismo que salvó las secuencias de sandhi: **proponer y
verificar, nunca afirmar.**

  1. Se extrae de la edición base cada referencia con el texto que la
     precede.
  2. Se busca ese texto en el sutta que le corresponde del maestro español.
     El ancla es el sufijo más largo que aparezca **una sola vez** en ese
     sutta. Si no hay ancla única, no se inserta nada: se informa.
  3. Aplicado el cambio, se quitan todas las citas insertadas y el archivo
     resultante tiene que ser **idéntico byte a byte** al original. Si no lo
     es, no se escribe nada.

Nunca se inventa una colocación para rellenar un hueco.

La edición base no vive en el repositorio. Se le pasa su ruta:

    python3 herramientas/restituir_citas.py --base ~/ruta/a/nandisena
    python3 herramientas/restituir_citas.py --base ~/ruta --aplicar

Sin `--aplicar` no toca nada: escribe la propuesta y el informe.
"""

import argparse
import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Capítulo → (archivo de la edición base, maestro español, primer §, último §)
CAPITULOS = {
    "nama": ("Kaccāyana 2 - Nāma-Kappa (U Nandisena).md",
             "docs/2. Nāma-Kappa.md", 52, 270),
    "karaka": ("3 - Kāraka-Kappa–Kaccāyana.md",
               "docs/3. Kāraka-Kappa.md", 271, 315),
}

PROPUESTA = "docs/fuentes/citas-canonicas.json"

SIGLAS = ("Khu|Vin|Abhi|DhA|DA|MA|SA|AA|UdānaA|PetavatthuA|Mog\\.-pañcikā"
          "|Sad|D|M|A|S|J")

# (Khu. i, 336) — sigla conocida, tomo en romanos, y lo que siga.
RE_CITA = re.compile(r'\((?:' + SIGLAS + r')\.?\s*[ivxlIVXL]+\s*,[^()]*?\)')

# Encabezado de sutta: «52. 60. Título» en la base, «**52\. 60\. Título»
# en el maestro español.
RE_HDR_BASE = re.compile(r'^\s*\*{0,2}(\d{2,3})\\?\.\s+[\d, ]+\\?\.\s+\**\S')
RE_HDR_ESP = re.compile(r'^\*\*(\d{2,3})\\\.\s')

# Caracteres que no deben cortar un ancla por la izquierda.
RE_PALABRA = re.compile(r"[^\s;,.!?()\[\]]+")


# Erratas de la edición base que el español ya trae corregidas (el IEBH,
# sesión 22). No se corrige nada: se le enseñan al emparejador para que la
# cita encuentre su sitio pese a la errata.
VARIANTES = {
    "saṅkhameyya": "saṅkameyya",   # §275
    "bhikhave":    "bhikkhave",    # §277
    "samyena":     "samayena",     # §290
    "brāhamaṇā":   "brāhmaṇā",     # §132
}
RE_VARIANTES = re.compile("|".join(VARIANTES), re.IGNORECASE)

# Puntuación y marcas de énfasis, que se descartan al comparar. Ver
# `normalizar`: el ancla se arma uniendo voces con un espacio, mientras que
# el maestro conserva entre ellas las comas y los puntos del original.
RE_PUNTUACION = re.compile(r"[;,.:!?*]")


def normalizar(s):
    """Comparación indulgente: comillas, guiones y escapes del markdown.

    También se prescinde de mayúsculas —Nandisena capitaliza el ejemplo que
    abre la frase y el maestro no siempre— y se rectifican las erratas
    conocidas de la edición base.

    **Y se prescinde de la puntuación** (sesión 23). `anclas_candidatas`
    arma el ancla uniendo voces con un solo espacio, pero entre esas voces
    el maestro imprime comas, puntos y punto y coma —«Duve samaṇā. Duve»—,
    de modo que mientras se comparó la puntuación al pie de la letra
    **ningún ancla de más de una voz pudo coincidir jamás**: el emparejador
    caía siempre al ancla de una sola voz, y las quince citas que quedaron
    pendientes lo quedaron por eso, no por ser ambiguas. Se descartan
    igualmente los asteriscos, que son marcado y no texto: desde que
    `restituir_negritas.py` marca el vutti, un ancla puede cruzar un tramo
    en negrita.
    """
    s = s.replace("\\", "")
    s = (s.replace("’", "'").replace("‘", "'")
          .replace("“", '"').replace("”", '"')
          .replace("–", "-").replace("—", "-"))
    s = unicodedata.normalize("NFC", s).lower()
    s = RE_VARIANTES.sub(lambda m: VARIANTES[m.group(0).lower()], s)
    s = RE_PUNTUACION.sub("", s)
    return re.sub(r"\s+", " ", s).strip()


def partir_por_sutta(texto, regex):
    """{n.º de sutta: bloque de texto}, en el orden del archivo."""
    bloques, actual, buf = {}, None, []
    for linea in texto.split("\n"):
        m = regex.match(linea)
        if m:
            if actual is not None:
                bloques[actual] = "\n".join(buf)
            actual, buf = int(m.group(1)), [linea]
        elif actual is not None:
            buf.append(linea)
    if actual is not None:
        bloques[actual] = "\n".join(buf)
    return bloques


def extraer(base_txt, desde, hasta):
    """Cada cita de la edición base, con el texto que la precede."""
    fuera = []
    for sutta, bloque in sorted(partir_por_sutta(base_txt,
                                                 RE_HDR_BASE).items()):
        if not desde <= sutta <= hasta:
            continue
        for m in RE_CITA.finditer(bloque):
            previo = bloque[max(0, m.start() - 120):m.start()]
            # La edición base intercala en ese tramo cosas que el maestro
            # español no lleva: otras citas y los marcadores de nota, que
            # allí van como números sueltos pegados al texto. Si quedaran
            # dentro del ancla, ninguna coincidiría.
            previo = RE_CITA.sub(" ", previo)
            previo = re.sub(r'(?<=[\s.,;])\d{1,3}(?=\s)', " ", previo)
            previo = re.sub(r'(?<=[a-zāīūṃṅñṇṭḍḷ])\.\d{1,3}\b', ".", previo)
            previo = previo.rstrip()
            if not previo:
                continue
            fuera.append({
                "sutta": sutta,
                "previo": previo,
                "cita": m.group(0),
            })
    return fuera


def region_pali(bloque):
    """(inicio, fin) del bloque pāḷi dentro del sutta: del encabezado al
    primer `---`.

    La guía de estilo §5 sólo admite la cita en el texto pāḷi, nunca en la
    línea española. Acotar la búsqueda ahí no es sólo prudencia: es la regla
    del proyecto, y de paso deshace casi toda la ambigüedad, porque el mismo
    ejemplo suele repetirse abajo en la lista de ejemplos traducidos.
    """
    lineas = bloque.split("\n")
    ini = len(lineas[0]) + 1 if lineas else 0
    pos = ini
    for linea in lineas[1:]:
        if linea.strip() == "---":
            return ini, pos
        pos += len(linea) + 1
    return ini, len(bloque)


def anclas_candidatas(previo):
    """Sufijos del texto previo, del más largo al más corto (hasta 6 voces).

    Se cortan por palabra: un ancla que empiece a mitad de palabra
    emparejaría por casualidad.
    """
    voces = RE_PALABRA.findall(previo)
    for n in range(min(6, len(voces)), 0, -1):
        yield " ".join(voces[-n:])


def emparejar(citas, esp_bloques):
    """Para cada cita, el ancla única más larga dentro de su propio sutta."""
    resueltas, pendientes = [], []
    for c in citas:
        bloque = esp_bloques.get(c["sutta"])
        if bloque is None:
            c["motivo"] = "el sutta no está en el maestro"
            pendientes.append(c)
            continue
        ini, fin = region_pali(bloque)
        norm = normalizar(bloque[ini:fin])
        elegida = None
        for ancla in anclas_candidatas(normalizar(c["previo"])):
            if len(ancla) < 4:
                break
            if norm.count(ancla) == 1:
                elegida = ancla
                break
        if elegida is None:
            c["motivo"] = "sin ancla única en su sutta"
            pendientes.append(c)
        else:
            resueltas.append(dict(c, ancla=elegida))
    return resueltas, pendientes


def localizar(bloque, ancla):
    """Posición final del ancla en el bloque real (no normalizado).

    Se avanza carácter a carácter comparando en forma normalizada, para no
    depender de que los escapes del markdown coincidan.
    """
    objetivo = normalizar(ancla)
    for ini in range(len(bloque)):
        acumulado = ""
        for fin in range(ini, min(len(bloque), ini + len(objetivo) * 3)):
            acumulado = normalizar(bloque[ini:fin + 1])
            if acumulado == objetivo:
                return fin + 1
            if len(acumulado) > len(objetivo):
                break
    return None


def aplicar(esp_txt, resueltas):
    """Inserta cada cita tras su ancla. Devuelve (texto, aplicadas, fallos)."""
    bloques = partir_por_sutta(esp_txt, RE_HDR_ESP)
    por_sutta = {}
    for r in resueltas:
        por_sutta.setdefault(r["sutta"], []).append(r)

    nuevos, aplicadas, fallos, intactos = {}, 0, [], True
    for sutta, grupo in por_sutta.items():
        bloque = bloques[sutta]
        marcas = []
        ini, fin = region_pali(bloque)
        posiciones = []
        for r in grupo:
            rel = localizar(bloque[ini:fin], r["ancla"])
            pos = None if rel is None else ini + rel
            if pos is None:
                r["motivo"] = "el ancla no se localiza en el texto real"
                fallos.append(r)
            else:
                posiciones.append((pos, r))
        # De delante hacia atrás, anotando dónde queda cada inserción en el
        # texto nuevo: así la verificación puede deshacerlas exactamente,
        # sin tener que reconocerlas por su forma.
        trozos, cursor = [], 0
        for pos, r in sorted(posiciones, key=lambda x: x[0]):
            trozos.append(bloque[cursor:pos])
            inserto = " " + r["cita"]
            marcas.append((sum(len(t) for t in trozos), len(inserto)))
            trozos.append(inserto)
            cursor = pos
            aplicadas += 1
        trozos.append(bloque[cursor:])
        nuevo = "".join(trozos)
        # Verificación por reconstrucción, sutta a sutta: deshechas las
        # inserciones por sus posiciones —no reconociéndolas por su forma,
        # que confundiría las citas que ya estaban— hay que recuperar el
        # bloque original exacto.
        rehecho = nuevo
        for desde, largo in sorted(marcas, reverse=True):
            rehecho = rehecho[:desde] + rehecho[desde + largo:]
        if rehecho != bloque:
            intactos = False
        nuevos[sutta] = nuevo

    salida, actual, buf = [], None, []
    for linea in esp_txt.split("\n"):
        m = RE_HDR_ESP.match(linea)
        if m:
            if actual is not None:
                salida.append(nuevos.get(actual, "\n".join(buf)))
            actual, buf = int(m.group(1)), [linea]
        elif actual is not None:
            buf.append(linea)
        else:
            salida.append(linea)
            continue
    if actual is not None:
        salida.append(nuevos.get(actual, "\n".join(buf)))
    return "\n".join(salida), aplicadas, fallos, intactos


def main_pendientes(escribir):
    """Reemparejar las pendientes contra los maestros de hoy.

    Mismo camino que el modo normal —mismo emparejador, misma verificación
    por reconstrucción—; sólo cambia de dónde salen las citas.
    """
    algo_mal, resumen = False, []

    for nombre, (_, maestro, _, _) in CAPITULOS.items():
        ruta_esp = os.path.join(RAIZ, maestro)
        esp_txt = open(ruta_esp, encoding="utf-8").read()
        esp_bloques = partir_por_sutta(esp_txt, RE_HDR_ESP)

        citas = desde_pendientes(nombre)
        resueltas, siguen = emparejar(citas, esp_bloques)
        nuevo, aplicadas, fallos, ok = aplicar(esp_txt, resueltas)
        siguen.extend(fallos)
        if not ok:
            algo_mal = True

        print("· {0}: {1} pendientes · {2} resueltas · {3} siguen · "
              "reconstrucción {4}".format(
                  nombre, len(citas), aplicadas, len(siguen),
                  "OK" if ok else "FALLA"))
        for r in resueltas:
            print("    §{0} {1}  ← «{2}»".format(
                r["sutta"], r["cita"], r["ancla"]))
        for p in siguen:
            print("    §{0} {1}  SIGUE ({2})".format(
                p["sutta"], p["cita"], p["motivo"]))

        resumen.append((nombre, resueltas, siguen))
        if escribir and ok:
            open(ruta_esp, "w", encoding="utf-8").write(nuevo)

    # Sin esto la operación no sería idempotente: las resueltas seguirían
    # figurando como pendientes y una segunda pasada las insertaría por
    # duplicado, porque el ancla sigue estando donde estaba.
    if escribir and not algo_mal:
        ruta_prop = os.path.join(RAIZ, PROPUESTA)
        with open(ruta_prop, encoding="utf-8") as f:
            datos = json.load(f)
        for nombre, resueltas, siguen in resumen:
            bloque = datos["citas"][nombre]
            bloque["aplicadas"].extend(
                {"sutta": r["sutta"], "ancla": r["ancla"], "cita": r["cita"]}
                for r in resueltas)
            bloque["pendientes"] = [
                {"sutta": p["sutta"], "cita": p["cita"],
                 "previo": p["previo"][-60:], "motivo": p["motivo"]}
                for p in siguen]
            for fila in datos["informe"]:
                if fila["capitulo"] == nombre:
                    fila["aplicadas"] += len(resueltas)
                    fila["pendientes"] = len(siguen)
        with open(ruta_prop, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=1)
        print("propuesta actualizada en {0}".format(PROPUESTA))

    if algo_mal:
        print("LA RECONSTRUCCIÓN NO REPRODUCE EL MAESTRO — no se ha escrito.")
        return 1
    if not escribir:
        print("(prueba: sin --aplicar no se ha tocado nada)")
    return 0


def desde_pendientes(nombre):
    """Las citas que quedaron pendientes, releídas de la propuesta anterior.

    La edición base no vive en el repositorio, de modo que sin ella no se
    puede repetir la extracción. Pero `citas-canonicas.json` guarda de cada
    pendiente su sutta, su cita y las sesenta últimas letras del texto que
    la precede, y eso basta para volver a emparejarla: el ancla nunca pasa
    de seis voces. Así la corrección de la sesión 23 pudo aplicarse sin
    tener delante los archivos de Nandisena.
    """
    ruta = os.path.join(RAIZ, PROPUESTA)
    with open(ruta, encoding="utf-8") as f:
        datos = json.load(f)
    return [dict(c) for c in datos["citas"][nombre]["pendientes"]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base",
                    help="carpeta con los archivos de la edición base")
    ap.add_argument("--pendientes", action="store_true",
                    help="reemparejar sólo las pendientes de "
                         "citas-canonicas.json, sin la edición base")
    ap.add_argument("--aplicar", action="store_true",
                    help="escribir los maestros (sin esto no toca nada)")
    args = ap.parse_args()

    if not args.base and not args.pendientes:
        print("hace falta --base o --pendientes")
        return 1

    if args.pendientes:
        return main_pendientes(args.aplicar)

    informe, propuesta = [], {}
    algo_mal = False

    for nombre, (arch_base, maestro, desde, hasta) in CAPITULOS.items():
        ruta_base = os.path.join(os.path.expanduser(args.base), arch_base)
        ruta_esp = os.path.join(RAIZ, maestro)
        if not os.path.exists(ruta_base):
            print("no encuentro la edición base: {0}".format(ruta_base))
            return 1

        base_txt = open(ruta_base, encoding="utf-8").read()
        esp_txt = open(ruta_esp, encoding="utf-8").read()

        citas = extraer(base_txt, desde, hasta)
        esp_bloques = partir_por_sutta(esp_txt, RE_HDR_ESP)
        resueltas, pendientes = emparejar(citas, esp_bloques)

        nuevo, aplicadas, fallos, ok = aplicar(esp_txt, resueltas)
        pendientes.extend(fallos)
        if not ok:
            algo_mal = True

        informe.append({
            "capitulo": nombre,
            "detectadas": len(citas),
            "aplicadas": aplicadas,
            "pendientes": len(pendientes),
            "reconstruccion": ok,
        })
        propuesta[nombre] = {
            "aplicadas": [{"sutta": r["sutta"], "ancla": r["ancla"],
                           "cita": r["cita"]} for r in resueltas],
            "pendientes": [{"sutta": p["sutta"], "cita": p["cita"],
                            "previo": p["previo"][-60:],
                            "motivo": p["motivo"]} for p in pendientes],
        }

        print("· {0}: {1} detectadas · {2} aplicadas · {3} pendientes · "
              "reconstrucción {4}".format(
                  nombre, len(citas), aplicadas, len(pendientes),
                  "OK" if ok else "FALLA"))
        for p in pendientes:
            print("    §{0} {1}  ← {2}  ({3})".format(
                p["sutta"], p["cita"], p["previo"][-40:].strip(),
                p["motivo"]))

        if args.aplicar and ok:
            open(ruta_esp, "w", encoding="utf-8").write(nuevo)

    ruta_prop = os.path.join(RAIZ, PROPUESTA)
    os.makedirs(os.path.dirname(ruta_prop), exist_ok=True)
    with open(ruta_prop, "w", encoding="utf-8") as f:
        json.dump({"informe": informe, "citas": propuesta}, f,
                  ensure_ascii=False, indent=1)
    print("propuesta escrita en {0}".format(PROPUESTA))

    if algo_mal:
        print("LA RECONSTRUCCIÓN NO REPRODUCE EL MAESTRO — no se ha escrito.")
        return 1
    if not args.aplicar:
        print("(simulacro: no se ha tocado ningún maestro; usa --aplicar)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
