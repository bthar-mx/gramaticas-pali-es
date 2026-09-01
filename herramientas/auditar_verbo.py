#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coteja las escaleras del documento «Verbo» con las de las presentaciones.

    python3 herramientas/auditar_verbo.py

No corrige nada: informa. Es el guion que sostiene lo que
`docs/verbo/escaleras-por-adjudicar.md` afirma, de modo que cualquiera pueda
rehacer la comprobación en vez de creerse el informe.

Qué comprueba
-------------

1. **Que todo par Kacc/Rū cuadre con la concordancia del repositorio**, la
   deducida de `kaccayana/*.md` y `docs/*.md`. Vale para los dos JSON.
2. **Que el documento y la diapositiva cuenten la misma derivación.** Se
   emparejan por la FORMA FINAL, no por el lema: «su» da dos escaleras —con
   ‘ṇu’ y con ‘ṇā’—, y el documento deriva «vikkiṇāti» donde la diapositiva
   deriva «kiṇāti», que son palabras distintas y no se deben cotejar. Luego se
   comparan paso a paso, sabiendo que el documento funde el último paso de
   elisión con el de formación del verbo y que en los pasos de elisión muestra
   la forma anterior. Lo que sobrepase esas dos diferencias conocidas se
   informa.
3. **Que ninguna forma retroceda** dentro de una escalera: si un paso deshace
   lo que hizo el anterior sin regla que lo explique, se señala.
4. **Que no queden ligaduras rotas** del PDF («in exión» por «inflexión»).

Nada de esto decide: la firma es de Angel. Ver el informe.
"""

import glob
import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERBO = os.path.join(RAIZ, "recursos", "verbo", "verbo.json")
DIAPOS = os.path.join(RAIZ, "recursos", "verbo", "diapositivas.json")

RE_SUTTA = re.compile(r"\*\*(\d+)\\?\.\s*(\d+)\\?\.\s")
# Restos de ligadura fi/fl que pdftotext deja al leer estas diapositivas.
RE_LIGADURA = re.compile(r"\b(in exi|re ere|identi ca|signi ca|su jo|"
                         r"[a-zá-ú]+ nal\b)")


def concordancia():
    ru2kacc = {}
    for patron in ("kaccayana/*.md", "docs/*.md"):
        for ruta in sorted(glob.glob(os.path.join(RAIZ, patron))):
            with open(ruta, encoding="utf-8") as fh:
                for m in RE_SUTTA.finditer(fh.read()):
                    ru2kacc.setdefault(int(m.group(2)), int(m.group(1)))
    return ru2kacc


def normalizar(forma):
    """Para comparar formas: sin espacios, sin apóstrofos, en NFC."""
    forma = unicodedata.normalize("NFC", forma or "")
    return re.sub(r"[\s'’‘\-]", "", forma).lower()


def cuerpo(paso):
    """Las cuatro celdas de forma de un paso, para comparar."""
    return tuple(normalizar(paso.get(c, ""))
                 for c in ("prefijo", "raiz", "signo", "inflexion"))


def pares(datos, donde):
    """Todos los (kacc, ru) que aparecen, con su sitio, para comprobarlos."""
    for esc in datos["escaleras"]:
        etiqueta = esc.get("lema") or esc.get("titulo", "?")
        for paso in esc["pasos"]:
            for a in paso["autoridades"]:
                yield (a["kacc"], a["ru"], f"{donde} · {etiqueta} · paso "
                       f"{paso['n']}")


def main():
    for ruta in (VERBO, DIAPOS):
        if not os.path.exists(ruta):
            sys.exit(f"Falta {os.path.relpath(ruta, RAIZ)}. Ejecutar antes "
                     "extraer_verbo.py y extraer_verbo_diapositivas.py.")
    doc = json.load(open(VERBO, encoding="utf-8"))
    dia = json.load(open(DIAPOS, encoding="utf-8"))
    ru2kacc = concordancia()
    problemas = 0

    # ---------------------------------------------------------------- 1
    print("1. Pares Kacc/Rū contra la concordancia del repositorio")
    malos = comprobados = 0
    for kacc, ru, donde in list(pares(doc, "documento")) + \
            list(pares(dia, "diapositiva")):
        comprobados += 1
        esperado = ru2kacc.get(ru)
        if esperado is None:
            print(f"   Rū {ru} no está en la concordancia — {donde}")
            malos += 1
        elif esperado != kacc:
            print(f"   Rū {ru} debería ser Kacc. §{esperado}, "
                  f"no §{kacc} — {donde}")
            malos += 1
    print(f"   {comprobados} citas comprobadas, {malos} discrepan")
    problemas += malos

    # ---------------------------------------------------------------- 2
    print("\n2. Documento contra diapositiva, paso a paso")
    # Se emparejan por la forma final, no por el lema: una misma raíz da
    # varias escaleras —«su» con ‘ṇu’ y con ‘ṇā’, «cura» con ‘ṇe’ y con
    # ‘ṇaya’—, y el documento deriva «vikkiṇāti» donde la diapositiva deriva
    # «kiṇāti», que son palabras distintas y no se deben cotejar.
    def resultado(esc):
        for paso in reversed(esc["pasos"]):
            if paso.get("resultado"):
                return normalizar(paso["resultado"])
        return ""

    por_forma = {}
    for esc in dia["escaleras"]:
        por_forma.setdefault(resultado(esc), []).append(esc)

    sin_cotejo, cotejadas, emparejadas = [], 0, set()
    for esc in doc["escaleras"]:
        candidatas = por_forma.get(resultado(esc), [])
        candidatas = [c for c in candidatas if id(c) not in emparejadas]
        if not candidatas:
            sin_cotejo.append(f"{esc['titulo']} → {resultado(esc)}")
            continue
        d = candidatas[0]
        emparejadas.add(id(d))
        cotejadas += 1
        cuerpos_doc = [cuerpo(p) for p in esc["pasos"]]
        cuerpos_dia = [cuerpo(p) for p in d["pasos"]]
        faltan = [c for c in cuerpos_dia if c not in cuerpos_doc and any(c)]
        sobran = [c for c in cuerpos_doc if c not in cuerpos_dia and any(c)]
        difpasos = len(d["pasos"]) - len(esc["pasos"])
        if faltan or sobran:
            print(f"   {esc['titulo']}  ({d['presentacion']})")
            print(f"     documento {len(esc['pasos'])} pasos, "
                  f"diapositiva {len(d['pasos'])}  ({difpasos:+d})")
            for c in faltan:
                print(f"     sólo en la diapositiva: "
                      f"{'+'.join(x for x in c if x)}")
            for c in sobran:
                print(f"     sólo en el documento:   "
                      f"{'+'.join(x for x in c if x)}")
    print(f"   {cotejadas} escaleras cotejadas")
    if sin_cotejo:
        print(f"   sin diapositiva que las coteje: {', '.join(sin_cotejo)}")

    solo_dia = [e for e in dia["escaleras"] if id(e) not in emparejadas]
    print(f"   sólo en las diapositivas: {len(solo_dia)}")
    for e in solo_dia:
        print(f"     {e['lema']:9s} {e['formacion'][:56]}  "
              f"({e['presentacion']})")

    # ---------------------------------------------------------------- 3
    print("\n3. Formas que retroceden dentro de una escalera")
    retrocesos = 0
    for datos, donde in ((doc, "documento"), (dia, "diapositiva")):
        for esc in datos["escaleras"]:
            etiqueta = esc.get("titulo") or esc.get("lema")
            vistas = []
            for paso in esc["pasos"]:
                raiz = normalizar(paso.get("raiz", ""))
                if not raiz:
                    continue
                if len(vistas) >= 2 and raiz == vistas[-2] and \
                        raiz != vistas[-1]:
                    print(f"   {donde} · {etiqueta} · paso {paso['n']}: "
                          f"vuelve a «{paso['raiz']}» tras «{vistas[-1]}»")
                    retrocesos += 1
                vistas.append(raiz)
    print(f"   {retrocesos} retrocesos")
    problemas += retrocesos

    # ---------------------------------------------------------------- 4
    print("\n4. Ligaduras rotas del PDF")
    rotas = 0
    for esc in dia["escaleras"]:
        for paso in esc["pasos"]:
            m = RE_LIGADURA.search(paso.get("operacion", ""))
            if m:
                print(f"   {esc['lema']} · paso {paso['n']}: "
                      f"{paso['operacion'][:60]}")
                rotas += 1
    print(f"   {rotas} restos")
    problemas += rotas

    print(f"\n{'sin problemas' if not problemas else f'{problemas} a revisar'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
