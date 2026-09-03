#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepara para la revisión los lotes de veredictos que llegan del modo
revisión — la lectura ANTES de la firma (pedido del IEBH, 2026-09-03).

    python3 herramientas/revisar_lote.py exportado.md
    python3 herramientas/revisar_lote.py a.md b.md c.md
    python3 herramientas/revisar_lote.py *.md --salida docs/solucionador/lote-limpio.md

Qué hace, y por qué existe:

Un lector exporta su revisión desde la página, y lo que llega suelen ser
VARIOS archivos del mismo rato —el mismo lote guardado tres veces según
iba avanzando—, con las formas repetidas. Ese montón hay que leerlo
entero para descubrir que son dos veredictos, no seis.

Y sobre todo: `incorporar_adjudicaciones.py` **no verifica**. Toma los
componentes que trae el veredicto y los guarda. Es lo correcto —el
Tipiṭaka es la fuente y quien firma manda—, pero significa que unos
componentes que el motor no sabe recomponer entran al banco sin que nadie
lo note, y la ficha queda sin escalera. Este guion los recompone ANTES,
para que quien firma lo sepa al decidir.

Lo que imprime, por forma:

  1. la frase de contexto, sacada de las observaciones del lote;
  2. las lecturas del motor con su escalera, y cuál coincide con el
     veredicto;
  3. el veredicto del revisor, y **si recompone**: se aplica
     `combinar()` —o `combinar_varias()` si trae tres voces— y se mira
     si entre sus salidas está la forma atestiguada;
  4. los precedentes del banco de casos que tocan la misma segunda voz,
     que es donde salen las contradicciones (el «+ yeva» frente al
     «+ eva» de `sabbesaṁyeva`);
  5. el estado: nueva, ya adjudicada, o en conflicto con lo guardado.

**AVISA, NO RECHAZA.** Un veredicto que no recompone puede ser la lectura
correcta del canon: el motor explica el texto, no lo autoriza (CLAUDE.md,
«EL TIPIṬAKA ES LA FUENTE»). Por eso este guion no toca nada ni devuelve
código de error por un fallo de recomposición: informa y se calla.

Con `--salida` escribe además UN lote limpio y deduplicado, con la
evidencia en comentarios HTML, listo para editar los VEREDICTO: y pasarlo
al incorporador de siempre.
"""

import argparse
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "nuestro"))
sys.path.insert(0, os.path.join(RAIZ, "herramientas"))

from normalizar import cotejo                                      # noqa: E402
import solucionar_sandhis as S                                     # noqa: E402
from incorporar_adjudicaciones import partir                       # noqa: E402

CASOS = os.path.join(RAIZ, "recursos", "solucionador",
                     "casos-reportados.json")

RAYA = "─" * 72
DOBLE = "=" * 72


# ── Leer y deduplicar ───────────────────────────────────────────────────

def normalizar_veredicto(bloque):
    """El veredicto como lista de voces, o como palabra suelta.

    Devuelve `(clase, valor)`. `clase` es «voces» (lista de componentes),
    «no» (no es sandhi), «compuesto», o `None` si viene en blanco. Se
    resuelve la letra —`a`, `b`…— contra las lecturas listadas, y se tira
    la parte izquierda de una ecuación entera, igual que el incorporador.
    """
    v = (bloque.get("veredicto") or "").strip()
    if not v:
        return None, None
    if "=" in v:
        v = v.split("=", 1)[1].strip()
    bajo = v.lower()
    if bajo in ("no", "no sandhi", "no-sandhi"):
        return "no", v
    if bajo == "compuesto":
        return "compuesto", v
    if len(bajo) == 1 and bajo in bloque["lecturas"]:
        v = bloque["lecturas"][bajo]
    return "voces", [x.strip() for x in v.split("+") if x.strip()]


def recoger(rutas):
    """Los bloques de todos los archivos, agrupados por forma.

    Dos archivos que traen la misma forma con el MISMO veredicto son el
    mismo veredicto guardado dos veces: se cuenta una vez y se nombran
    los archivos. Si el veredicto DIFIERE, no se elige: se guardan los
    dos y se avisa, porque cuál vale lo decide quien firma.
    """
    formas, observaciones, archivos = {}, [], []
    for ruta in rutas:
        with open(ruta, encoding="utf-8") as f:
            bloques, obs = partir(f.read())
        nombre = os.path.basename(ruta)
        archivos.append(nombre)
        if obs and obs not in observaciones:
            observaciones.append(obs)
        for b in bloques:
            clave = cotejo(b["forma"])
            entrada = formas.setdefault(clave, {"forma": b["forma"],
                                                "variantes": []})
            clase, valor = normalizar_veredicto(b)
            firma = (clase, tuple(valor) if isinstance(valor, list) else valor)
            for var in entrada["variantes"]:
                if var["firma"] == firma:
                    var["archivos"].append(nombre)
                    break
            else:
                entrada["variantes"].append({
                    "firma": firma, "clase": clase, "valor": valor,
                    "bloque": b, "archivos": [nombre]})
    return formas, observaciones, archivos


def frase_de(texto, forma):
    """La oración de las observaciones donde aparece la forma."""
    if not texto:
        return None
    k = cotejo(forma)
    for frase in re.split(r"(?<=[.;—])\s+", texto):
        if k in cotejo(frase):
            return " ".join(frase.split())
    return None


# ── Verificar ───────────────────────────────────────────────────────────

def recompone(forma, voces):
    """¿Las voces del veredicto dan la forma atestiguada?

    Devuelve `(veredicto, escalera, cuantas)`: `True/False/None` —None es
    «el motor no puede decirlo», que no es lo mismo que «no»—, la escalera
    si la hay, y cuántas salidas produjo la combinación.
    """
    if len(voces) < 2:
        return None, None, 0
    k = cotejo(forma)
    try:
        if len(voces) == 2:
            salidas = S.combinar(voces[0], voces[1])
        else:
            salidas = S.combinar_varias(voces)
    except Exception as e:                                    # noqa: BLE001
        return None, ["error del motor: {0}".format(e)], 0
    for cand, lectura in salidas:
        if cotejo(cand) == k:
            return True, lectura["pasos"], len(salidas)
    if not salidas and len(voces) > 2:
        # El plegado de tres voces calla cuando la forma intermedia no
        # está atestiguada; es un límite conocido del motor, no un
        # veredicto contra la lectura. Véase combinar_varias().
        return None, None, 0
    return False, None, len(salidas)


def junturas(voces):
    """Cada juntura por separado, para cuando el plegado entero calla.

    Que `a + b + c` no se recomponga de una pasada no dice nada contra
    `b + c`: el plegado pide que el intermedio esté atestiguado. Mirar
    las junturas de a dos enseña dónde está el paso que sí se explica.
    """
    fuera = []
    for i in range(len(voces) - 1):
        a, b = voces[i], voces[i + 1]
        try:
            salidas = S.combinar(a, b)
        except Exception:                                     # noqa: BLE001
            salidas = []
        fuera.append((a, b, salidas))
    return fuera


def lecturas_del_motor(forma):
    try:
        return S.solucionar(forma)
    except Exception as e:                                    # noqa: BLE001
        return {"estado": "error: {0}".format(e), "lecturas": []}


# ── Precedentes del banco ───────────────────────────────────────────────

def precedentes(casos, forma, voces):
    """Lo que el banco ya dijo sobre esta forma y sobre esta segunda voz.

    La segunda voz es donde salen las contradicciones: `sabbesaṁyeva` se
    corrigió a mano a «+ eva» porque la «y» es de §35, y sin embargo
    `atikkamiyeva` y `tassāyeva` siguen guardados con «+ yeva». Un
    veredicto nuevo que elija uno de los dos caminos está tomando partido
    en algo ya decidido, y conviene verlo.
    """
    mismo = None
    parientes = []
    ultima = cotejo(voces[-1]) if voces else None
    for c in casos:
        if cotejo(c["forma"]) == cotejo(forma):
            mismo = c
            continue
        comp = c.get("componentes")
        if not comp or not ultima:
            continue
        piezas = [x.strip() for x in str(comp).split("+")]
        if len(piezas) >= 2 and cotejo(piezas[-1]) == ultima:
            parientes.append(c)
        elif cotejo(c["forma"]).endswith(ultima) and len(piezas) >= 2:
            parientes.append(c)
    return mismo, parientes[:8]


# ── Informe ─────────────────────────────────────────────────────────────

def informar(formas, observaciones, archivos, casos):
    lineas = []
    a = lineas.append
    obs = "\n\n".join(observaciones)

    a(DOBLE)
    a("REVISIÓN DE LOTE — {0} archivo(s), {1} forma(s) distinta(s)".format(
        len(archivos), len(formas)))
    a(DOBLE)
    for nombre in archivos:
        a("  · " + nombre)
    if len(archivos) > len(formas):
        a("")
        a("  Los archivos repiten formas: lo que sigue las cuenta UNA vez.")
    a("")

    for entrada in formas.values():
        forma = entrada["forma"]
        a(RAYA)
        a("  " + forma)
        a(RAYA)

        frase = frase_de(obs, forma)
        if frase:
            a("")
            a("  CONTEXTO (de las observaciones del lote)")
            for trozo in _envolver(frase, 66):
                a("    " + trozo)

        r = lecturas_del_motor(forma)
        a("")
        a("  EL MOTOR dice: {0}".format(r.get("estado")))
        for i, l in enumerate(r.get("lecturas") or []):
            comp = l.get("componentes") or []
            a("    {0}) {1}".format("abcdefghij"[i] if i < 10 else "?",
                                    " + ".join(comp)))
            for paso in l.get("pasos") or []:
                a("         " + paso)

        if len(entrada["variantes"]) > 1:
            a("")
            a("  ATENCIÓN: los archivos traen veredictos DISTINTOS para esta "
              "forma.")
            a("  No se elige ninguno; van los dos.")

        for var in entrada["variantes"]:
            _informar_veredicto(a, forma, var, r, casos)
        a("")

    a(DOBLE)
    a("Recordatorio: esto AVISA, no rechaza. Que el motor no recomponga unos")
    a("componentes no los desmiente — el Tipiṭaka es la fuente y Kaccāyana la")
    a("autoridad que lo explica, no la que lo autoriza. Lo que el aviso dice")
    a("es que, de entrar así, la ficha quedará sin escalera.")
    a(DOBLE)
    return "\n".join(lineas)


def _informar_veredicto(a, forma, var, r, casos):
    clase, valor = var["clase"], var["valor"]
    a("")
    a("  VEREDICTO DEL REVISOR ({0})".format(", ".join(var["archivos"])))
    if clase is None:
        a("    (en blanco — no se incorpora)")
        return
    if clase in ("no", "compuesto"):
        a("    {0} — entra como no-sandhi; no hay nada que recomponer".format(
            valor))
        return

    a("    " + " + ".join(valor))

    # ¿Coincide con alguna lectura del motor?
    del_motor = None
    for i, l in enumerate(r.get("lecturas") or []):
        comp = [cotejo(x) for x in (l.get("componentes") or [])]
        if comp == [cotejo(x) for x in valor]:
            del_motor = "abcdefghij"[i] if i < 10 else "?"
            break
    if del_motor:
        a("    ↳ es la lectura {0} del motor".format(del_motor))
    else:
        a("    ↳ NO está entre las lecturas del motor")

    ok, escalera, cuantas = recompone(forma, valor)
    a("")
    if ok is True:
        a("    RECOMPONE ✓")
        for paso in escalera:
            a("        " + paso)
    elif ok is False:
        a("    NO RECOMPONE ✗ — de {0} salida(s), ninguna es «{1}»".format(
            cuantas, forma))
        if cuantas == 0:
            a("        Ninguna combinación: alguna de las voces no está")
            a("        atestiguada en el léxico {0}.".format(
                S.nombre_lexico()))
    else:
        a("    EL MOTOR NO PUEDE DECIRLO")
        if escalera:
            for paso in escalera:
                a("        " + paso)
        elif len(valor) > 2:
            a("        Tres voces: el plegado pide que la forma intermedia")
            a("        esté atestiguada, y no siempre lo está. No es un")
            a("        veredicto contra la lectura. Las junturas de a dos:")

    if len(valor) > 2 or ok is False:
        for x, y, salidas in junturas(valor):
            marca = "{0} salida(s)".format(len(salidas)) if salidas \
                else "ninguna salida — voz no atestiguada"
            a("        · {0} + {1}: {2}".format(x, y, marca))
            if salidas:
                for cand, lect in salidas[:1]:
                    a("            p. ej. {0}: {1}".format(
                        cand, " ; ".join(lect["pasos"])))

    mismo, parientes = precedentes(casos, forma, valor)
    if mismo:
        a("")
        guardado = mismo.get("componentes", "(no-sandhi)")
        if cotejo(str(guardado).replace("+", "")) == \
                cotejo("".join(valor)):
            a("    YA ADJUDICADA, y dice lo mismo: nada que cambiar.")
        else:
            a("    YA ADJUDICADA, y dice OTRA COSA: «{0}».".format(guardado))
            a("    El incorporador declinará el veredicto. Se decide a mano.")
        a("      fuente: {0}".format(mismo.get("fuente", "—")))
    if parientes:
        a("")
        a("    PRECEDENTES con la misma segunda voz:")
        for c in parientes:
            a("      · {0} = {1}   ({2})".format(
                c["forma"], c.get("componentes", "no-sandhi"),
                c.get("fuente", "—")))
            if c.get("nota"):
                for trozo in _envolver("nota: " + c["nota"], 58):
                    a("          " + trozo)


def _envolver(texto, ancho):
    import textwrap
    return textwrap.wrap(texto, ancho) or [""]


# ── El lote limpio ──────────────────────────────────────────────────────

def lote_limpio(formas, observaciones, casos):
    hoy = __import__("datetime").date.today().isoformat()
    out = ["# Veredictos de revisión — lote unificado ({0})".format(hoy),
           "",
           "*Deduplicado por `herramientas/revisar_lote.py`. La evidencia va "
           "en comentarios: el incorporador no la lee.*",
           "",
           "---",
           "",
           "## Observaciones del revisor",
           ""]
    out.append("\n\n".join(observaciones))
    out.append("")
    out.append("---")
    out.append("")

    for n, entrada in enumerate(formas.values(), 1):
        forma = entrada["forma"]
        out.append("## {0}. {1}  ·  señal ninguna  ·  revisado en la página"
                   .format(n, forma))
        r = lecturas_del_motor(forma)
        for i, l in enumerate(r.get("lecturas") or []):
            comp = " + ".join(l.get("componentes") or [])
            marca = " — la primera lectura del motor" if i == 0 else \
                    " — lectura del motor"
            out.append("- **{0})** {1}{2}".format(
                "abcdefghij"[i] if i < 10 else "?", comp, marca))
        out.append("")
        for var in entrada["variantes"]:
            clase, valor = var["clase"], var["valor"]
            if clase == "voces":
                ok, escalera, cuantas = recompone(forma, valor)
                estado = {True: "recompone ✓", False: "NO recompone ✗",
                          None: "el motor no puede decirlo"}[ok]
                out.append("<!-- del revisor ({0}): {1} — {2} -->".format(
                    ", ".join(var["archivos"]), " + ".join(valor), estado))
                if ok is True:
                    for paso in escalera:
                        out.append("<!--     {0} -->".format(paso))
                mismo, _ = precedentes(casos, forma, valor)
                if mismo:
                    out.append("<!-- YA en el banco: {0} ({1}) -->".format(
                        mismo.get("componentes", "no-sandhi"),
                        mismo.get("fuente", "—")))
                out.append("VEREDICTO: " + " + ".join(valor))
            elif clase is None:
                out.append("VEREDICTO:")
            else:
                out.append("VEREDICTO: " + str(valor))
            out.append("")
        out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lotes", nargs="+")
    ap.add_argument("--salida", default=None,
                    help="escribe además un lote unificado en este archivo")
    a = ap.parse_args()

    with open(CASOS, encoding="utf-8") as f:
        casos = json.load(f)["casos"]

    formas, observaciones, archivos = recoger(a.lotes)
    if not formas:
        print("No hay ninguna forma con veredicto en lo que se dio.")
        return 0

    print(informar(formas, observaciones, archivos, casos))

    if a.salida:
        with open(a.salida, "w", encoding="utf-8") as f:
            f.write(lote_limpio(formas, observaciones, casos))
        print("\nLote unificado escrito en: {0}".format(a.salida))
        print("Edítense los VEREDICTO: y páseselo al incorporador de siempre.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
