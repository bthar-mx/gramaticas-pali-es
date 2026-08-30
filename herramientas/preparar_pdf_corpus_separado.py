#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deja un PDF bilingüe del IEBH en la forma de .txt que el extractor espera.

    python3 herramientas/preparar_pdf_corpus_separado.py <archivo.pdf>
    python3 herramientas/preparar_pdf_corpus_separado.py <archivo.pdf> --medir

El LEEME de recursos/corpus-separado dice, y con razón, que a un .txt
exportado de Google Docs **no hay que tocarle nada**. Un PDF es otro caso, y
por una razón medible, no por gusto: Google Docs exporta **un párrafo por
línea** —la mediana del Mahāsatipaṭṭhāna es una línea de 1.693 caracteres—
mientras que `pdftotext` corta por el ancho de la caja, con una mediana de 93.
Y `extraer_junturas_separadas.py` trabaja **línea a línea**: una juntura que
caiga justo en un corte de línea desaparece sin dejar rastro.

Este guion hace dos cosas, las dos conservadoras, y no hace ninguna más.

## 1. Las llamadas de nota pegadas a la palabra

En el .txt de Google Docs la llamada sale como «[8]» y `limpiar()` ya la
quita. En el PDF sale **pegada al final de la voz**: «ekam idāhaṃ8»,
«Sārandade9», «Akaraṇīyāva10». Y eso rompe justamente lo que interesa: la
juntura «ekam | idāhaṃ» se une como «ekamidāhaṃ8», que no está atestiguada en
ninguna edición, y se pierde como fallo. En el Mahāparinibbāna son 100.

Se quitan sólo los dígitos que van **pegados detrás de una letra**. Un número
de párrafo («135.») o de verso («(7)») no lleva letra delante y no se toca.
Ninguna voz pāḷi acaba en cifra, de modo que la operación no puede borrar
texto.

## 2. El re-flujo, por RACHAS DE IDIOMA

Las líneas pāḷi consecutivas se unen en una sola; las españolas se dejan
como están. El corte de idioma lo decide `es_pali()` **del propio extractor**,
importado de allí, para que las dos herramientas no puedan discrepar.

Unir dos párrafos pāḷi seguidos es inofensivo, y conviene decir por qué: la
única adjacencia nueva es la última voz de uno con la primera del otro, y un
párrafo acaba en punto —«…no parihānī ti.»—, de modo que tras `limpiar()` la
voz final queda en vocal y no abre juntura. Y si alguna la abriera, la
publicación exige que la forma unida esté **atestiguada en la edición**, que
es el resguardo de siempre.

El .txt queda al lado del PDF, y el extractor lo toma en la siguiente corrida.
Con `--medir` no escribe nada: dice cuántas junturas ve el crudo y cuántas el
preparado, para que la diferencia se vea antes de aceptarla.
"""

import argparse
import os
import re
import subprocess
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "herramientas"))

from extraer_junturas_separadas import es_pali, junturas_de        # noqa: E402

# Un dígito pegado detrás de LETRA es llamada de nota. Detrás de nada, o de
# un paréntesis, es número de verso o de párrafo y no se toca.
NOTA_PEGADA = re.compile(r"(?<=[^\W\d_])\d{1,3}(?![\d\w])", re.UNICODE)


def texto_del_pdf(ruta):
    r = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", "-nopgbrk", ruta, "-"],
        capture_output=True, check=True)
    return unicodedata.normalize("NFC", r.stdout.decode("utf-8"))


def preparar(crudo):
    """Las llamadas de nota fuera, y las líneas pāḷi seguidas en una sola."""
    salida, racha = [], []

    def cerrar():
        if racha:
            salida.append(" ".join(racha))
            racha.clear()

    for linea in crudo.split("\n"):
        l = linea.strip()
        if not l:
            cerrar()
            salida.append("")
            continue
        if es_pali(l):
            racha.append(NOTA_PEGADA.sub("", l))
        else:
            cerrar()
            salida.append(l)
    cerrar()
    return "\n".join(salida) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("pdf")
    p.add_argument("--medir", action="store_true",
                   help="no escribe: sólo compara crudo y preparado")
    p.add_argument("--salida", default=None,
                   help="ruta del .txt (por omisión, junto al PDF)")
    a = p.parse_args()

    crudo = texto_del_pdf(a.pdf)
    listo = preparar(crudo)

    j_crudo = junturas_de(crudo)
    j_listo = junturas_de(listo)
    print(f"{os.path.basename(a.pdf)}")
    print(f"  U+FFFD ...................... {crudo.count(chr(0xFFFD))}")
    print(f"  NFC ......................... {unicodedata.normalize('NFC', listo) == listo}")
    print(f"  llamadas de nota quitadas ... {len(NOTA_PEGADA.findall(crudo))}")
    print(f"  candidatas, crudo ........... {len(j_crudo)}")
    print(f"  candidatas, preparado ....... {len(j_listo)}")
    print(f"  ganadas por el re-flujo ..... {len(j_listo) - len(j_crudo)}")

    if a.medir:
        return
    destino = a.salida or os.path.splitext(a.pdf)[0] + ".txt"
    with open(destino, "w", encoding="utf-8") as f:
        f.write(listo)
    print(f"  escrito ..................... {destino}")


if __name__ == "__main__":
    main()
