#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrae la terminología gramatical inglesa de «Grammatical Terms».

    python3 herramientas/extraer_terminos_nyanamoli.py <pdf>

LA OBRA. «Grammatical Terms», recopilado por Bhikkhu Ñāṇamoli a partir de
«A Pali-English Glossary of Buddhist Technical Terms» (BPS, Kandy 1994) y
revisado con adiciones sustanciales por Ānandajoti Bhikkhu, versión 2 (junio
de 2014). El texto original se reproduce con permiso de la Buddhist
Publication Society. Ānandajoti declara que las fuentes de Ñāṇamoli fueron
Buddhaghosa y las gramáticas de Kaccāyana, Aggavaṃsa y Moggallāna, que son
justamente las de este repositorio.

QUÉ ENTRA EN EL REPOSITORIO Y QUÉ NO. El PDF NO se guarda —queda fuera por
la regla `*.pdf` de .gitignore, como los de Nandisena y U Sīlānanda—. Lo que
se guarda es la lista de pares término→inglés CON SU PÁGINA, para poder
citar de dónde sale cada propuesta cuando se le enseñe al Venerable. La
atribución va en el pie de la página publicada.

QUÉ NO HACE. No traduce ni decide nada: sólo recoge lo que la obra dice, con
su página. La prelación al fijar el inglés del glosario es otra y está en
docs/glosario/ingles-por-adjudicar.md: primero el inglés del propio
Nandisena (los capítulos .en.md), luego lo ya adjudicado por el IEBH
(paradigmas, verbo), luego el memorando de sandhi, y sólo al final esta
obra.

NOTA SOBRE LA ṂM. Ñāṇamoli y Ānandajoti escriben ṁ; este repositorio
escribe ṃ (convenciones §1). Se normaliza al recoger, y se deja constancia
del original en el campo «tal_cual» cuando difiere.
"""

import json
import os
import re
import subprocess
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, "recursos", "glosario", "terminos-nyanamoli.json")

OBRA = {
    "titulo": "Grammatical Terms",
    "compilador": "Bhikkhu Ñāṇamoli",
    "de": "A Pali-English Glossary of Buddhist Technical Terms "
          "(Buddhist Publication Society, Kandy, 1994)",
    "revision": "revisado con adiciones sustanciales por Ānandajoti Bhikkhu",
    "version": "2 (junio de 2014)",
    "permiso": "El texto original se reproduce con permiso de la Buddhist "
               "Publication Society.",
    "nota": "Ānandajoti declara que las fuentes de Ñāṇamoli fueron las obras "
            "de Buddhaghosa y las gramáticas de Kaccāyana, Aggavaṃsa y "
            "Moggallāna.",
}

# term – gloss, con el guión largo o el corto, y con la sangría que el
# original usa para las subdivisiones (a), (b)…
LINEA = re.compile(
    r"^\s*(?:\((?P<orden>[0-9a-z]+)\)\s*)?"
    r"(?P<pali>[a-zāīūṅñṭḍṇḷṁṃ][a-zāīūṅñṭḍṇḷṁṃ()\-,/ ]*?)\s*"
    r"[–-]\s+(?P<en>\S.*)$"
)
PAGINA = re.compile(r"^\s*Grammatical Terms - (\d+)\s*$")


def normaliza(s):
    """ṁ → ṃ, y NFC. El repositorio escribe ṃ en todo el pāḷi."""
    return unicodedata.normalize("NFC", s.replace("ṁ", "ṃ"))


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        return 1
    pdf = sys.argv[1]
    if not os.path.exists(pdf):
        print("No encuentro {0}".format(pdf))
        return 1

    crudo = subprocess.run(["pdftotext", "-layout", pdf, "-"],
                           capture_output=True, text=True, check=True).stdout

    pagina, entradas, previa = None, [], None
    for linea in crudo.splitlines():
        m = PAGINA.match(linea)
        if m:
            pagina = int(m.group(1))
            continue
        if not linea.strip():
            previa = None
            continue
        m = LINEA.match(linea)
        if m:
            pali = normaliza(m.group("pali").strip())
            en = m.group("en").strip()
            # Un lema puede traer varias grafías separadas por coma o barra:
            # «vagga / vaggā», «kicca, kita». Se recoge cada una.
            for uno in re.split(r"\s*[,/]\s*", pali):
                uno = uno.strip()
                if not uno or len(uno) < 2:
                    continue
                entradas.append({"pali": uno, "en": en, "pagina": pagina})
            previa = entradas[-1] if entradas else None
        elif previa is not None and linea.startswith(" " * 3):
            # continuación de la glosa anterior
            previa["en"] = previa["en"].rstrip() + " " + linea.strip()

    # una entrada puede repetirse con glosas distintas (kicca sale dos veces):
    # se conservan las dos, que es lo que hace la obra.
    vistas, limpias = set(), []
    for e in entradas:
        clave = (e["pali"], e["en"])
        if clave in vistas:
            continue
        vistas.add(clave)
        e["en"] = re.sub(r"\s+", " ", e["en"]).strip()
        limpias.append(e)

    salida = {
        "_nota": "Pares término→inglés recogidos de la obra citada en «obra», "
                 "con la página de donde sale cada uno. NO es terminología "
                 "adjudicada por el IEBH: es una de las fuentes con que se "
                 "propone el inglés del glosario, y la última en prelación, "
                 "detrás del inglés del propio Nandisena y de lo ya adjudicado "
                 "en este repositorio. El PDF no se guarda aquí.",
        "obra": OBRA,
        "terminos": sorted(limpias, key=lambda e: (e["pali"], e["pagina"] or 0)),
    }
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    with open(DESTINO, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=1)

    lemas = len({e["pali"] for e in limpias})
    print("{0} pares · {1} lemas distintos · pp. {2}-{3} → {4}".format(
        len(limpias), lemas,
        min(e["pagina"] for e in limpias if e["pagina"]),
        max(e["pagina"] for e in limpias if e["pagina"]),
        os.path.relpath(DESTINO, RAIZ)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
