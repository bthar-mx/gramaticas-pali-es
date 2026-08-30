#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Incorpora los veredictos de un lote de adjudicación a
`recursos/solucionador/casos-reportados.json`.

    python3 herramientas/incorporar_adjudicaciones.py docs/solucionador/por-adjudicar-lote-1.md
    python3 herramientas/incorporar_adjudicaciones.py ... --fuente "Angel, 2026-08-29 · lote 1"

Lee las líneas `VEREDICTO:` del lote. Acepta: una letra (`a`, `b`…) que
señala la lectura listada; `no` (no es sandhi); `compuesto` (fuera del
encargo, se registra como no-sandhi con nota); o componentes explícitos
(`tena + upasaṅkami`). Lo vacío se salta. No borra ni reescribe casos ya
adjudicados: si una forma ya está, avisa y no toca su veredicto — cambiar
una adjudicación es una decisión que se toma en el archivo de casos, a mano
y con nota.

Desde el 2026-08-30 (briefing 35 §6 quater — las observaciones se perdían,
y ahí venían las escaleras del IEBH) también recoge, por voz:

- `NOTA DEL REVISOR: …`  → el campo `nota` del caso, verbatim y rotulada
  como del revisor;
- `ESCALERA:` seguida de líneas sangradas, un paso por línea → el campo
  `escalera_iebh`, verbatim, con su `escalera_fuente`. La página la
  muestra rotulada como del revisor cuando el motor no deriva la lectura.

A un caso YA adjudicado que llegue con escalera o nota se le AÑADEN si no
las tiene —el veredicto no se toca—; si ya las tiene, se avisa y no se
tocan.

Las **Observaciones del revisor** (el cuadro libre) siguen sin volverse
datos —son prosa, no campos—, pero ya no pasan calladas: se imprimen
enteras con un aviso, para que quien corre el ciclo las lea en el acto.

Después de incorporar: regenerar la página y correr el arnés de casos.
"""

import argparse
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "nuestro"))
from normalizar import cotejo                                      # noqa: E402

CASOS = os.path.join(RAIZ, "recursos", "solucionador",
                     "casos-reportados.json")

RE_FORMA = re.compile(r"^## \d+\.\s+(\S+)\s+·")
RE_OBS = re.compile(r"^## Observaciones del revisor\s*$")
RE_LECTURA = re.compile(r"^- \*\*([a-j])\)\*\*\s+(.+?)(?:\s+\(§[^)]*\))?\s+—")
RE_VEREDICTO = re.compile(r"^VEREDICTO:\s*(.*)$")
RE_NOTA = re.compile(r"^NOTA DEL REVISOR:\s*(.*)$")
RE_ESCALERA = re.compile(r"^ESCALERA:\s*$")
RE_PASO = re.compile(r"^\s+(\S.*)$")


def partir(texto):
    """El lote, en bloques por forma, más las observaciones generales.

    Se parte primero y se procesa después porque la NOTA y la ESCALERA
    vienen DESPUÉS de la línea VEREDICTO: procesar línea a línea, como se
    hacía, era exactamente lo que las tiraba.
    """
    bloques, obs = [], []
    cur, en_obs, en_esc = None, False, False
    for linea in texto.split("\n"):
        m = RE_FORMA.match(linea)
        if m:
            cur = {"forma": m.group(1), "lecturas": {},
                   "veredicto": None, "nota": None, "escalera": []}
            bloques.append(cur)
            en_obs, en_esc = False, False
            continue
        if RE_OBS.match(linea):
            cur, en_obs, en_esc = None, True, False
            continue
        if en_obs:
            if linea.strip() == "---":
                en_obs = False
            else:
                obs.append(linea)
            continue
        if cur is None:
            continue
        if en_esc:
            m = RE_PASO.match(linea)
            if m:
                cur["escalera"].append(m.group(1).strip())
                continue
            en_esc = False
        m = RE_LECTURA.match(linea)
        if m:
            cur["lecturas"][m.group(1)] = m.group(2).strip()
            continue
        m = RE_VEREDICTO.match(linea)
        if m:
            cur["veredicto"] = m.group(1).strip()
            continue
        m = RE_NOTA.match(linea)
        if m:
            cur["nota"] = m.group(1).strip() or None
            continue
        if RE_ESCALERA.match(linea):
            en_esc = True
    return bloques, "\n".join(obs).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lote")
    ap.add_argument("--fuente", default=None)
    a = ap.parse_args()

    fuente = a.fuente or "Angel · " + os.path.basename(a.lote)
    d = json.load(open(CASOS, encoding="utf-8"))
    por_clave = {cotejo(c["forma"]): c for c in d["casos"]}

    bloques, obs = partir(open(a.lote, encoding="utf-8").read())

    nuevos, enriquecidos, saltados, avisos = [], 0, 0, []
    for b in bloques:
        forma, v = b["forma"], b["veredicto"]
        if not v:
            # Sin veredicto no hay caso, pero una escalera o nota sueltas
            # tampoco se tiran: se avisa, que alguien las escribió.
            if b["escalera"] or b["nota"]:
                avisos.append("escalera o nota SIN veredicto en {0}: no se "
                              "incorpora sola — póngase el veredicto o "
                              "hágase a mano".format(forma))
            else:
                saltados += 1
            continue
        existente = por_clave.get(cotejo(forma))
        if existente is not None:
            # El veredicto no se toca. La escalera y la nota se AÑADEN si
            # faltan: así las del cuadro de observaciones dejaron de
            # perderse (briefing 35 §6 quater).
            #
            # Pero sólo si el veredicto del lote DICE LO MISMO que el caso
            # guardado: colgar la escalera del revisor de unos componentes
            # que él no afirmó sería mezclar dos análisis. Si difieren, no
            # se toca nada y se decide a mano.
            if "+" in v or (len(v) == 1 and v.lower() in b["lecturas"]):
                dicho = (b["lecturas"][v.lower()] if len(v) == 1
                         else " + ".join(x.strip() for x in v.split("+")))
                guardado = existente.get("componentes", "")
                if cotejo(dicho.replace("+", "")) != \
                        cotejo(str(guardado).replace("+", "")):
                    avisos.append(
                        "el veredicto de {0} difiere del caso guardado "
                        "({1!r} frente a {2!r}): no se toca nada — "
                        "decídase a mano".format(forma, dicho, guardado))
                    continue
            toco = []
            if b["escalera"] and not existente.get("escalera_iebh"):
                existente["escalera_iebh"] = b["escalera"]
                existente["escalera_fuente"] = (
                    fuente + " · escalera del revisor (verbatim)")
                toco.append("escalera")
            elif b["escalera"]:
                avisos.append("ya tiene escalera, no se toca: " + forma)
            if b["nota"] and not existente.get("nota"):
                existente["nota"] = "Nota del revisor (verbatim): " + b["nota"]
                toco.append("nota")
            elif b["nota"]:
                avisos.append("ya tiene nota, no se toca: " + forma)
            if toco:
                enriquecidos += 1
                avisos.append("ya adjudicada ({0}): se le añade {1} del "
                              "revisor; el veredicto no se toca".format(
                                  forma, " y ".join(toco)))
            else:
                avisos.append("ya adjudicada, no se toca: " + forma)
            continue
        caso = {"forma": forma, "fuente": fuente}
        bajo = v.lower()
        if bajo in ("no", "no sandhi", "no-sandhi"):
            caso["sandhi"] = False
        elif bajo == "compuesto":
            caso["sandhi"] = False
            caso["nota"] = ("Compuesto: fuera del encargo por instrucción "
                            "del Venerable.")
        elif len(bajo) == 1 and bajo in b["lecturas"]:
            caso["sandhi"] = True
            caso["componentes"] = b["lecturas"][bajo]
        elif "+" in v:
            caso["sandhi"] = True
            caso["componentes"] = " + ".join(
                x.strip() for x in v.split("+"))
        else:
            avisos.append("veredicto ilegible en {0}: {1!r}".format(forma, v))
            continue
        if b["nota"] and "nota" not in caso:
            caso["nota"] = "Nota del revisor (verbatim): " + b["nota"]
        if b["escalera"]:
            caso["escalera_iebh"] = b["escalera"]
            caso["escalera_fuente"] = (
                fuente + " · escalera del revisor (verbatim)")
        nuevos.append(caso)
        por_clave[cotejo(forma)] = caso

    if nuevos or enriquecidos:
        d["casos"].extend(nuevos)
        json.dump(d, open(CASOS, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
    print("{0} casos incorporados · {1} enriquecidos · {2} en blanco · "
          "total {3}".format(len(nuevos), enriquecidos, saltados,
                             len(d["casos"])))
    for x in avisos:
        print("  aviso — " + x)
    if obs:
        print()
        print("=" * 72)
        print("OBSERVACIONES DEL REVISOR — prosa, NO se vuelven datos. Léanse:")
        print("si dan escaleras o corrigen componentes de una voz, eso va en")
        print("los campos de la tarjeta (que sí se incorporan) o a mano.")
        print("=" * 72)
        print(obs)
        print("=" * 72)
    if nuevos or enriquecidos:
        print("\nAhora:  python3 herramientas/generar_solucionador.py"
              "\n        node nuestro/js/arnes_casos.js")
    return 0


if __name__ == "__main__":
    sys.exit(main())
