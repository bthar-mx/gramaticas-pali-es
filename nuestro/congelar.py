#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Congela el banco: huella SHA-256 de cada archivo que el motor lee.

    python3 nuestro/congelar.py              # comprueba contra banco.sha256
    python3 nuestro/congelar.py --escribir   # (re)escribe banco.sha256

Cuando el banco cambia es versión nueva, no deriva silenciosa. Este script no
impide el cambio: lo hace visible. Se corre antes y después de cualquier cosa
que toque la carpeta, y si una huella se movió lo dice con el nombre del
archivo.

**`reglas.json` es fuente, no salida** *(21 de agosto de 2026)*. No se puede
regenerar: 121 de sus 266 secuencias —las 42 marcadas `aforismo` y 79 de las
175 `derivada`— no las reproduce ningún script de la carpeta. La copia que
mandó el Venerable es idéntica byte por byte a la nuestra, así que el archivo
es auténtico y no derivó. Por eso se congela y **nunca** se corre
`reconstruir_sandhi.py --escribir` sobre él.

El formato de salida es el de `sha256sum`, así que se puede comprobar también
con `sha256sum -c banco.sha256` sin este script.
"""

import argparse
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rutas import ruta, raiz, destino                                       # noqa: E402
RAIZ = raiz()
DESTINO = destino("banco.sha256")

# Qué se congela, y por qué. Un archivo que no esté acá es que el motor no lo
# lee; si el motor empieza a leerlo, entra a esta lista en el mismo cambio.
BANCO = [
    ("recursos/sandhi/reglas.json",                  "fuente · 49 reglas, 266 formas — no regenerable"),
    ("recursos/sandhi/notas-combinacion-eufonica.json", "salida · 22 notas, 9 enunciados, 6 formas"),
    ("recursos/combinacion-eufonica.md",             "fuente · cotejada contra el PDF el 2026-08-21"),
    ("recursos/combinacion-eufonica.pdf",            "fuente · el PDF del Venerable"),
    ("kaccayana/01-sandhi-kappa.md",                 "fuente · los 51 aforismos traducidos"),
    ("comun/concordancia-sandhi-kac-ru.json",        "fuente · los 51 pares Kac ↔ Rū"),
    ("comun/concordancia-tres-numeraciones-sandhi.json", "fuente · Kac, Rū y Sad para el capítulo"),
    ("recursos/sandhi/tablas-sandhi-nandisena.json", "fuente · las 41 secuencias del Venerable"),
    # Corregido al incorporarse al árbol (2026-08-28): el banco decía
    # `recursos/listas-cerradas.json` pero el motor lee
    # `recursos/sandhi/listas-cerradas.json` (solucionar_sandhis.py, LISTAS).
    # La carpeta plana de la entrega enmascaraba la diferencia, porque
    # rutas.py cae al nombre a secas. Se fija la ruta del motor.
    ("recursos/sandhi/listas-cerradas.json",         "fuente · 20 upasagga, 221 nipāta"),
    ("fuentes-derivadas/thitzana-sandhi-51-tabla.json", "derivado · extracción, no lectura"),
    ("recursos/sandhi/tablas-nandisena-secuencias.json", "salida · las 41 filas en pasos"),
    ("fuentes-derivadas/thitzana-evidencia-negativa.json", "salida · 34 «kasmā?» y 42 ejemplos"),
    ("recursos/lexico/dpd-formas.txt",                  "fuente · 443.740 formas del DPD v0.4.20260728"),
    ("recursos/lexico/dpd-descomposiciones.tsv",        "derivado · 2.058.431 descomposiciones del propio DPD"),
    ("recursos/lexico/grupos-iniciales.json",           "salida · la lista cerrada de grupos iniciales"),
    ("nuestro/operaciones.py",                          "motor · una función por aforismo"),
    ("nuestro/solucionar_sandhis.py",                   "motor · el entregable 1"),
    # El motor importa estos cuatro y hasta hoy no estaban congelados: la lista
    # decía «un archivo que no esté acá es que el motor no lo lee», y de estos
    # cuatro no era cierto. `derivar_secuencias.py` es el que más importa: es
    # del Venerable y es el verificador de nueve aforismos —§12, §13, §15, §16,
    # §17, §18, §21, §28 y §35—; si cambiara sin que nadie lo note, cambiaría
    # en silencio la mitad de las secuencias que publicamos.
    ("herramientas/derivar_secuencias.py",              "fuente · el derivador del Venerable — no se toca"),
    ("nuestro/normalizar.py",                           "motor · cotejo(): cómo se comparan dos formas"),
    ("nuestro/rutas.py",                                "motor · dónde se busca cada archivo"),
    ("nuestro/glosas.py",                               "motor · las glosas de la pantalla"),
    ("nuestro/pantalla.py",                             "motor · el entregable 2, la pantalla"),
]


def huella(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def leer_guardado():
    if not os.path.exists(DESTINO):
        return None
    guardado = {}
    for l in open(DESTINO, encoding="utf-8"):
        l = l.rstrip("\n")
        if not l or l.startswith("#"):
            continue
        sha, _, nombre = l.partition("  ")
        guardado[nombre] = sha
    return guardado


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--escribir", action="store_true")
    a = ap.parse_args()

    guardado = leer_guardado()
    actual, ausentes = {}, []
    for rel, nota in BANCO:
        p = ruta(*rel.split("/"))
        if os.path.exists(p):
            actual[rel] = huella(p)
        else:
            ausentes.append(rel)

    print("EL BANCO\n")
    problemas = 0
    for rel, nota in BANCO:
        if rel in ausentes:
            print("  {0:<9} {1:<52} {2}".format("AUSENTE", rel, nota))
            problemas += 1
            continue
        sha = actual[rel]
        if guardado is None:
            estado = "nuevo"
        elif rel not in guardado:
            estado = "NUEVO"
            problemas += 1
        elif guardado[rel] != sha:
            estado = "CAMBIÓ"
            problemas += 1
        else:
            estado = "igual"
        print("  {0:<9} {1:<52} {2}".format(estado, rel, sha[:16] + "…"))
        if estado == "CAMBIÓ":
            print("            guardada: {0}…".format(guardado[rel][:16]))

    if guardado:
        for rel in guardado:
            if rel not in actual and rel not in ausentes:
                print("  {0:<9} {1}".format("SE FUE", rel))
                problemas += 1

    print()
    if a.escribir:
        with open(DESTINO, "w", encoding="utf-8") as f:
            f.write("# El banco congelado. Generado por nuestro/congelar.py.\n")
            f.write("# Formato sha256sum: se comprueba con `sha256sum -c banco.sha256`.\n")
            for rel, nota in BANCO:
                if rel in actual:
                    f.write("# {0}\n{1}  {2}\n".format(nota, actual[rel], rel))
        print("Escrito {0}  ({1} archivos)".format(
            os.path.relpath(DESTINO, RAIZ) if DESTINO.startswith(RAIZ) else DESTINO, len(actual)))
        return 0

    if guardado is None:
        print("No hay banco.sha256 todavía. Corré con --escribir para crearlo.")
        return 1
    if problemas:
        print("{0} diferencia(s). Si el cambio es intencional, --escribir.".format(problemas))
        return 1
    print("Sin cambios: {0} archivos, todas las huellas iguales.".format(len(actual)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
