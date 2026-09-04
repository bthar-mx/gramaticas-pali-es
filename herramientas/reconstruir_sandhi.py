#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reconstruye recursos/sandhi/reglas.json desde el documento de Nandisena.

    python3 herramientas/reconstruir_sandhi.py            # sólo informa
    python3 herramientas/reconstruir_sandhi.py --escribir # además guarda

Lee recursos/combinacion-eufonica.md y transcribe:

  · las secciones y sus reglas, con la numeración del propio documento
  · las filas de cada regla: componentes, resultado y referencia canónica

No inventa nada. El documento no contiene pasos intermedios ni citas §N de
Kaccāyana dentro de las formas, así que la reconstrucción tampoco los tiene.

Los aforismos §N que encabezan cada regla se toman del archivo anterior
emparejando por el TEXTO de la regla, no por su número —que es justamente lo
que estaba mal—, y se informa de cada emparejamiento para poder revisarlo.
"""

import argparse
import json
import os
import re
import sys
import unicodedata
from difflib import SequenceMatcher

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(RAIZ, "recursos", "combinacion-eufonica.md")
ANTERIOR = os.path.join(RAIZ, "recursos", "sandhi", "reglas.json")
DESTINO = ANTERIOR

SECCIONES = [
    ("sara", "SARA-SANDHI", "COMBINACIÓN EUFÓNICA DE VOCALES", "Vocal + vocal"),
    ("byanjana", "BYAÑJANA-SANDHI", "COMBINACIÓN EUFÓNICA DE UNA VOCAL Y UNA CONSONANTE",
     "Vocal + consonante"),
    ("niggahita", "NIGGAHITA-SANDHI", "COMBINACIÓN EUFÓNICA DE LA", "Niggahīta + vocal o consonante"),
    ("pakati", "PAKATI-SANDHI", "CASOS EN QUE NO SE APLICAN", "Sin combinación"),
]

RE_FILA = re.compile(r'^\s*\|(.+)\|\s*$')
RE_SEP = re.compile(r'^\s*\|(\s*:?-{2,}:?\s*\|)+\s*$')


def limpiar(t):
    t = re.sub(r'<sup>.*?</sup>', '', t)
    t = t.replace("**", "").replace("__", "")
    t = re.sub(r'^\s*##\s*', '', t)
    t = re.sub(r'^\s*-\s*', '', t)
    t = re.sub(r'\\(.)', r'\1', t)
    return re.sub(r'\s+', ' ', t).strip()


def norm(t):
    t = unicodedata.normalize("NFKD", t.lower())
    t = re.sub(r'[^a-z ]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()


def es_encabezado_seccion(t):
    for clave, nombre, marca, sub in SECCIONES:
        if marca in t and ("SANDHI" in t or "PAKATI" in t):
            return clave, nombre, sub
    return None


def parsear_documento():
    texto = open(DOC, encoding="utf-8").read()
    cuerpo = texto[texto.index("# **COMBINACIÓN EUFÓNICA (SANDHI)**"):]
    lineas = cuerpo.split("\n")

    reglas, seccion, regla, sin_numero = [], None, None, 0
    for l in lineas:
        t = l.strip()
        if not t:
            continue

        if RE_FILA.match(l):
            if regla is None or RE_SEP.match(l):
                continue
            celdas = [c.strip() for c in RE_FILA.match(l).group(1).split("|")]
            # \uf022 es la flecha que la conversión del PDF dejó dentro de una
            # celda cuando el documento muestra varias etapas seguidas.
            celdas = [c.replace("\uf022", " → ") for c in celdas]
            if any(re.search(r'VOCAL|EJEMPLO|SANDHI|REFERENCIA|COMPONENTES', c, re.I)
                   for c in celdas):
                continue                       # fila de cabecera repetida
            # Formas de tabla del documento:
            #   5 columnas  vocal ant | vocal post | ejemplo | sandhi | referencia
            #   4 columnas  letra insertada | componentes | resultado | referencia
            #   3 columnas  componentes | resultado | referencia
            if len(celdas) >= 5:
                comp, res, ref = celdas[2], celdas[3], celdas[4]
            elif len(celdas) == 4:
                comp, res, ref = celdas[1], celdas[2], celdas[3]
            elif len(celdas) == 3:
                comp, res, ref = celdas[0], celdas[1], celdas[2]
            else:
                continue
            # Algunas filas empaquetan dos formas con <br> en las tres columnas.
            # <br> se usa para dos cosas distintas: empaquetar dos formas en una
            # fila, y partir una celda larga en dos líneas. Sólo es lo primero
            # cuando las TRES columnas se parten en el mismo número de trozos.
            partes = [[limpiar(y) for y in x.split("<br>")] for x in (comp, res, ref)]
            n_sub = max(len(x) for x in partes)
            if n_sub == 1 or not all(len(x) == n_sub for x in partes):
                n_sub = 1
                partes = [[limpiar(re.sub(r'<br>', ' ', x))] for x in (comp, res, ref)]
            for k in range(n_sub):
                c_, r_, f_ = (x[k] if len(x) > 1 else x[0] for x in partes)
                if not c_ or not r_:
                    continue
                # Si el documento da varias etapas —en la columna de
                # componentes, en la de resultado o en ambas— se conservan:
                # son suyas, no reconstruidas por nosotros.
                izq = [x.strip() for x in c_.split("→") if x.strip()]
                der = [x.strip() for x in r_.split("→") if x.strip()]
                etapas = izq[1:] + der[:-1]
                regla["filas"].append({"comp": izq[0], "res": der[-1], "ref": f_,
                                       "etapas": etapas})
            continue

        if t.startswith(">"):                  # nota al pie del documento
            continue

        # Una regla (sara 12) da su ejemplo en prosa, no en tabla.
        mp = re.search(r'Ejemplos?:\s*“([^”]+)”\s*Sandhi:\s*“([^”]+)”\s*\(([^)]+)\)', t)
        if mp and regla is not None:
            regla["filas"].append({"comp": limpiar(mp.group(1)),
                                   "res": limpiar(mp.group(2)),
                                   "ref": limpiar(mp.group(3)), "etapas": []})
            continue

        plano = limpiar(t)
        sec = es_encabezado_seccion(plano.upper())
        if sec:
            seccion = sec
            sin_numero = 0
            regla = None
            continue

        if seccion is None or "**" not in t:
            continue

        # encabezado de regla: número opcional al principio
        m = re.match(r'^(\d+(?:\.\d+)?)\.\s*(.+)$', plano)
        if m:
            num, cuerpo_regla = m.group(1), m.group(2)
        else:
            # las dos primeras de sara vienen sin numerar en el cuerpo
            if seccion[0] != "sara" or sin_numero >= 2 or len(plano) < 25:
                continue
            sin_numero += 1
            num, cuerpo_regla = str(sin_numero), plano
        if len(cuerpo_regla) < 15:
            continue
        regla = {"sec": seccion[0], "secName": seccion[1], "secSub": seccion[2],
                 "n": num, "rule": cuerpo_regla.rstrip(".") + ".", "filas": []}
        reglas.append(regla)

    return reglas


def emparejar_aforismos(reglas):
    """Toma el §N de cada regla del archivo anterior, emparejando por texto."""
    if not os.path.exists(ANTERIOR):
        return {}
    viejas = json.load(open(ANTERIOR, encoding="utf-8"))["rules"]
    # Los textos del archivo anterior eran correctos; sólo su numeración estaba
    # mal. Se empareja uno a uno, del par más parecido al menos, para que dos
    # reglas distintas no acaben apuntando al mismo aforismo.
    pares = []
    for r in reglas:
        if "." in r["n"]:                       # las subreglas heredan del padre
            continue
        for v in viejas:
            if v["sec"] != r["sec"] or v.get("sub"):
                continue
            pares.append((SequenceMatcher(None, norm(r["rule"]), norm(v["rule"])).ratio(),
                          r["sec"], r["n"], v))
    pares.sort(key=lambda x: -x[0])
    mapa, usadas, tomadas = {}, set(), set()
    for punt, sec, n, v in pares:
        if punt < 0.60 or (sec, n) in tomadas or id(v) in usadas:
            continue
        mapa[(sec, n)] = (v.get("kac", []), v.get("ru", []), punt, v["n"])
        tomadas.add((sec, n)); usadas.add(id(v))
    # subreglas: el aforismo de su regla madre
    for r in reglas:
        if "." in r["n"]:
            padre = mapa.get((r["sec"], r["n"].split(".")[0]))
            if padre:
                mapa[(r["sec"], r["n"])] = padre
    return mapa


def clave_forma(t):
    t = unicodedata.normalize("NFC", t.lower())
    t = t.replace("\u2019", "").replace("'", "").replace("-", "")
    t = re.sub(r'\s*\([^)]*\)\s*', '', t)
    return re.sub(r'[\s+]', '', t)


def secuencias_verificadas():
    """Las secuencias del markdown del capítulo: obra del IEBH, ya revisadas.

    Son las únicas secuencias con procedencia. Se adjuntan a la forma del
    documento cuando coinciden; para las demás no se inventa ninguna.
    """
    sys.path.insert(0, os.path.join(RAIZ, "herramientas"))
    from generar_sandhi import suttas_desde_markdown
    mapa = {}
    for s in suttas_desde_markdown():
        for e in s["ex"]:
            final = re.sub(r'\s*\([^)]*\)\s*$', '', e["s"][-1])
            for k in (e["f"], final):
                mapa.setdefault(clave_forma(k), (e["s"], s["kac"]))
    return mapa


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--escribir", action="store_true")
    a = ap.parse_args()

    reglas = parsear_documento()
    mapa = emparejar_aforismos(reglas)
    verificadas = secuencias_verificadas()
    n_verif = 0

    salida_reglas, salida_formas = [], []
    for r in reglas:
        kac, ru, punt, num_viejo = mapa.get((r["sec"], r["n"]), ([], [], 0, "—"))
        entrada = {"sec": r["sec"], "secName": r["secName"], "secSub": r["secSub"],
                   "n": r["n"], "rule": r["rule"], "kac": kac, "ru": ru, "ex": ""}
        if "." in r["n"]:
            entrada["sub"] = True
            entrada["parent"] = r["n"].split(".")[0]
        salida_reglas.append(entrada)
        for f in r["filas"]:
            salida_formas.append({
                "f": f["res"], "comp": f["comp"], "ref": f["ref"],
                "sec": r["sec"], "secName": r["secName"], "rule": r["n"],
                "title": r["rule"].rstrip("."),
                "kac": kac[0] if kac else 0,
                "s": ([f["comp"]] + f.get("etapas", []) + [f["res"]]
                      if f["comp"] != f["res"] else [f["res"]]),
                "full": False, "transcrito": True,
            })
            v = (verificadas.get(clave_forma(f["res"]))
                 or verificadas.get(clave_forma(f["comp"])))
            if v:
                salida_formas[-1]["s"] = list(v[0])
                salida_formas[-1]["kac_seq"] = v[1]
                salida_formas[-1]["full"] = True
                salida_formas[-1]["verificada"] = True
                salida_formas[-1].pop("transcrito", None)
                n_verif += 1

    from collections import Counter
    print("RECONSTRUCCIÓN DESDE EL DOCUMENTO\n")
    print("  reglas: {0}   ({1})".format(
        len(salida_reglas),
        ", ".join("{0} {1}".format(k, v)
                  for k, v in Counter(r["sec"] for r in salida_reglas).items())))
    print("  formas: {0}   ({1})".format(
        len(salida_formas),
        ", ".join("{0} {1}".format(k, v)
                  for k, v in Counter(f["sec"] for f in salida_formas).items())))
    print()
    for r in salida_reglas:
        n_formas = sum(1 for f in salida_formas
                       if f["sec"] == r["sec"] and f["rule"] == r["n"])
        kac = "§" + ", §".join(map(str, r["kac"])) if r["kac"] else "—"
        print("  {0:10} {1:>5}  {2:<7} {3:>3} formas   {4}".format(
            r["sec"], r["n"], kac, n_formas, r["rule"][:56]))

    if a.escribir:
        json.dump({"rules": salida_reglas, "ce": salida_formas},
                  open(DESTINO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("\nEscrito {0}".format(os.path.relpath(DESTINO, RAIZ)))
    else:
        print("\n(sin escribir — usa --escribir)")

    print("\n  formas con secuencia verificada del markdown: {0}".format(n_verif))
    print("  formas sin secuencia (el documento sólo da componentes y resultado): {0}"
          .format(len(salida_formas) - n_verif))
    return 0


if __name__ == "__main__":
    sys.exit(main())
