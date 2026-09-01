#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la página «El verbo · ākhyāta».

    python3 herramientas/generar_verbo.py

Junta cuatro cosas:

  recursos/verbo/plantilla.html      maquetado y lógica
  recursos/verbo/verbo.json          el documento «Verbo» de Nandisena
  recursos/verbo/diapositivas.json   las escaleras de las presentaciones
  herramientas/escaleras_verbo.py    las decisiones de Angel, en un sitio

y escribe site/recursos/verbo/index.html.

Las referencias §N se deducen del markdown, nunca se copian: cada autoridad
sale de aquí con su enlace ya resuelto si el capítulo está publicado, y sin él
—con un `title` que dice por qué— si no lo está. **Hoy no lo está**: el
Ākhyāta-kappa no tiene todavía su `kaccayana/06-akhyata-kappa.md`, de modo que
casi todos los §N verbales saldrán en texto plano. El día que entre, se
enlazan solos sin tocar nada.

No publica si los datos no cuadran. Ver `verificar()`.
"""

import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "herramientas"))

from escaleras_verbo import escaleras  # noqa: E402
from generar_capitulo import CAPITULOS, parsear  # noqa: E402
from generar_ingles_verbo import comprobar  # noqa: E402

PLANTILLA = os.path.join(RAIZ, "recursos", "verbo", "plantilla.html")
VERBO = os.path.join(RAIZ, "recursos", "verbo", "verbo.json")
INGLES = os.path.join(RAIZ, "recursos", "verbo", "ingles.json")
DESTINO = os.path.join(RAIZ, "site", "recursos", "verbo", "index.html")

VERSION = "1.1"
VERSION_FECHA = "2026-09-01"


def mapa_suttas():
    """{n: (obra, capitulo, titulo)} de los capítulos ya publicados."""
    mapa = {}
    for clave, meta in CAPITULOS.items():
        md = os.path.join(RAIZ, meta["obra_slug"], clave + ".md")
        if not os.path.exists(md):
            continue
        for s in parsear(md)["suttas"]:
            mapa[int(s["n"])] = (meta["obra_slug"], meta["slug"],
                                 meta["titulo_pali"])
    return mapa


def resolver(datos, mapa):
    """Añade a cada autoridad su enlace, si el capítulo está publicado."""
    enlazadas = pendientes = 0
    for esc in datos["escaleras"]:
        for paso in esc["pasos"]:
            for a in paso["autoridades"]:
                destino = mapa.get(a["kacc"])
                if destino:
                    obra, cap, titulo = destino
                    a["href"] = f"../../{obra}/{cap}/#s{a['kacc']}"
                    a["titulo"] = f"{titulo} · §{a['kacc']}"
                    enlazadas += 1
                else:
                    a["titulo"] = ("El Ākhyāta-kappa no está publicado "
                                   "todavía; la referencia se enlazará sola "
                                   "cuando lo esté.")
                    pendientes += 1
    return enlazadas, pendientes


def verificar(verbo, escs):
    """Lo que tiene que cuadrar para publicar."""
    fallos = []

    intro = verbo.get("introduccion") or {}
    if len(intro.get("items", [])) != 13:
        fallos.append(f"la introducción trae {len(intro.get('items', []))} "
                      "ítems; deberían ser 13")
    if len(verbo["inflexiones"]) != 8:
        fallos.append(f"{len(verbo['inflexiones'])} tablas de inflexión; "
                      "deberían ser 8")
    if len(verbo["ganas"]) != 9:
        fallos.append(f"la tabla de gaṇas trae {len(verbo['ganas'])} filas; "
                      "deberían ser 9 (cabecera + 8 grupos)")
    if len(verbo["paradigmas"]) != 105:
        fallos.append(f"{len(verbo['paradigmas'])} paradigmas; "
                      "deberían ser 105")

    for p in verbo["paradigmas"]:
        if not p["entrada"] or not p["tiempo"]:
            fallos.append(f"paradigma sin entrada o sin tiempo: {p!r:.70}")
        if len(p["filas"]) != 3:
            fallos.append(f"{p['entrada']} · {p['tiempo']}: "
                          f"{len(p['filas'])} personas, deberían ser 3")

    for e in escs:
        if not e["pasos"]:
            fallos.append(f"escalera «{e['lema']}» sin pasos")
            continue
        if not e["resultado"]:
            fallos.append(f"escalera «{e['lema']}» sin forma final")
        for paso in e["pasos"]:
            if paso["origen"] not in ("documento", "diapositiva", "propuesta"):
                fallos.append(f"{e['lema']} paso {paso['n']}: origen "
                              f"desconocido «{paso['origen']}»")
            if not paso["autoridades"] and paso["origen"] != "propuesta":
                fallos.append(f"{e['lema']} paso {paso['n']}: sin autoridad")
            for a in paso["autoridades"]:
                if not (1 <= a["kacc"] <= 675):
                    fallos.append(f"{e['lema']} paso {paso['n']}: "
                                  f"Kacc. §{a['kacc']} fuera de rango")
    return fallos


def main():
    if not os.path.exists(PLANTILLA):
        print(f"falta {os.path.relpath(PLANTILLA, RAIZ)}")
        return 1

    verbo = json.load(open(VERBO, encoding="utf-8"))
    escs = escaleras()

    fallos = verificar(verbo, escs)
    if fallos:
        print("Los datos del verbo NO cuadran; no se publica:")
        for f in fallos[:20]:
            print("  ✗", f)
        if len(fallos) > 20:
            print(f"  … y {len(fallos) - 20} más")
        return 1

    # El inglés va en dos capas. La INTERFAZ —rótulos de la página— se
    # publica siempre. La PROSA es del IEBH y sólo viaja cuando está
    # ADJUDICADA: mientras «adjudicado» sea false se comprueba pero no se
    # inyecta, y el modo inglés muestra el español con el aviso del pie.
    ing = (json.load(open(INGLES, encoding="utf-8"))
           if os.path.exists(INGLES) else {})
    if ing:
        _, faltan, _ = comprobar(verbo, escs, ing)
        if faltan:
            print(f"  aviso — el borrador inglés no cubre {len(faltan)} "
                  "cadenas; no se inyecta la prosa")
            ing = dict(ing, adjudicado=False)

    datos = {
        "fuente": verbo["fuente"],
        "introduccion": verbo.get("introduccion", {}),
        "usos": verbo["usos"],
        "voces": verbo["voces"],
        "inflexiones": verbo["inflexiones"],
        "ganas": verbo["ganas"],
        "escaleras": escs,
        "paradigmas": verbo["paradigmas"],
    }
    if ing:
        datos["ingles"] = {
            "adjudicado": bool(ing.get("adjudicado")),
            "adjudicado_por": ing.get("adjudicado_por", ""),
            "interfaz": ing.get("interfaz", {}),
        }
        if ing.get("adjudicado"):
            datos["ingles"]["prosa"] = ing["prosa"]
    enlazadas, pendientes = resolver(datos, mapa_suttas())

    plantilla = open(PLANTILLA, encoding="utf-8").read()
    marca = re.search(r"/\*__DATOS__\*/.*?/\*__FIN__\*/", plantilla, re.S)
    if not marca:
        print("La plantilla no tiene el marcador /*__DATOS__*/…/*__FIN__*/")
        return 1
    html = (plantilla[:marca.start()]
            + json.dumps(datos, ensure_ascii=False, separators=(",", ":"))
            + plantilla[marca.end():])
    html = html.replace("__VERSION_DATE__", VERSION_FECHA)
    html = html.replace("__VERSION__", VERSION)
    if "__VERSION" in html:
        print("aviso — han quedado marcadores sin sustituir")

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    open(DESTINO, "w", encoding="utf-8").write(html)

    propuestas = sum(1 for e in escs for p in e["pasos"]
                     if p["origen"] == "propuesta")
    de_dia = sum(1 for e in escs if e["procedencia"] == "diapositiva")
    buddhadatta = sum(1 for p in verbo["paradigmas"]
                      if p["obra"].startswith("Buddhadatta"))
    print(f"{os.path.relpath(DESTINO, RAIZ)}")
    print(f"  escaleras   {len(escs)}  ({de_dia} de las diapositivas, "
          f"{propuestas} filas propuestas)")
    print(f"  paradigmas  {len(verbo['paradigmas'])}  "
          f"({buddhadatta} de Buddhadatta)")
    print(f"  §N          {enlazadas} enlazados, {pendientes} sin capítulo "
          "publicado")
    if ing:
        estado = ("prosa ADJUDICADA por " + (ing.get("adjudicado_por") or "?")
                  if ing.get("adjudicado")
                  else "interfaz publicada · prosa SIN ADJUDICAR")
        print(f"  inglés      {estado}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
