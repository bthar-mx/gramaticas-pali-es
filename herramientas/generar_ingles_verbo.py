#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprueba el borrador inglés del verbo y escribe el cotejo para firmarlo.

    python3 herramientas/generar_ingles_verbo.py

Hace dos cosas:

1. **Comprueba la cobertura, campo por campo.** Toda cadena española que la
   página muestre tiene que tener su inglés. Lo que falte se enumera; lo que
   sobre —inglés sin español al que corresponder— también, porque suele
   significar que la fuente cambió y el borrador se quedó atrás.
2. **Escribe `docs/verbo/ingles-por-adjudicar.md`**, el cotejo lado a lado con
   el que Angel firma. Firmarlo es poner `"adjudicado": true` en
   `recursos/verbo/ingles.json`, con `adjudicado_por` y `fecha`; entonces
   `generar_verbo.py` inyecta la prosa y el aviso del pie cede el sitio al
   crédito.

**Las formas pāḷi no se traducen** y no aparecen aquí: son el objeto de la
página. Las referencias §N tampoco: son la cita, y es la misma en los dos
idiomas.
"""

import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "herramientas"))

from escaleras_verbo import escaleras  # noqa: E402

VERBO = os.path.join(RAIZ, "recursos", "verbo", "verbo.json")
INGLES = os.path.join(RAIZ, "recursos", "verbo", "ingles.json")
INFLEXIONES = os.path.join(RAIZ, "recursos", "verbo", "inflexiones.json")
DESTINO = os.path.join(RAIZ, "docs", "verbo", "ingles-por-adjudicar.md")


def _inflexiones():
    if not os.path.exists(INFLEXIONES):
        return {"inflexiones": [], "cabecera": [[], []]}
    return json.load(open(INFLEXIONES, encoding="utf-8"))


def españolas(verbo, escs):
    """Las cadenas que la página muestra, por sección."""
    infl = _inflexiones()
    fuera = {}
    fuera["operaciones"] = sorted({p["operacion"] for e in escs
                                   for p in e["pasos"] if p["operacion"]})
    fuera["glosas"] = sorted({e["glosa"] for e in escs if e["glosa"]})
    fuera["formacion"] = sorted({e["formacion"] for e in escs
                                 if e["formacion"]})
    fuera["tiempos"] = sorted({p["tiempo"] for p in verbo["paradigmas"]
                               if p["tiempo"]}
                              | {i["titulo"] for i in infl["inflexiones"]})
    fuera["voces"] = sorted({p["voz"] for p in verbo["paradigmas"] if p["voz"]})
    intro = verbo.get("introduccion") or {}
    cadenas = [intro.get("entradilla", "")]
    for it in intro.get("items", []):
        cadenas += [it["texto"], it.get("nota", "")] + it.get("sub", [])
    fuera["intro"] = sorted({c for c in cadenas if c})
    fuera["personas"] = sorted({f["persona"].replace(" / ", " ")
                                for p in verbo["paradigmas"]
                                for f in p["filas"]}
                               | {fila[0] for i in infl["inflexiones"]
                                  for fila in i["filas"]})
    fuera["numeros"] = sorted({n.replace(" / ", " ")
                               for p in verbo["paradigmas"] for n in p["numeros"]}
                              | set(infl["cabecera"][1][1:]))
    # Las notas de las tablas de terminaciones, que el documento «Verbo» no
    # traía y sí traen los ocho documentos del índice.
    fuera["notas"] = sorted({n["texto"] for i in infl["inflexiones"]
                             for n in i["notas"]})
    fuera["usos_inf"] = sorted({u for i in infl["inflexiones"]
                                for u in i.get("usos", [])})
    return fuera


def comprobar(verbo, escs, ing):
    prosa = ing.get("prosa", {})
    esp = españolas(verbo, escs)
    faltan, sobran = [], []
    for seccion, cadenas in esp.items():
        tabla = prosa.get(seccion, {})
        if not isinstance(tabla, dict):
            continue
        for c in cadenas:
            if c not in tabla or not str(tabla[c]).strip():
                faltan.append(f"{seccion}: «{c}»")
        for c in tabla:
            if c not in cadenas:
                sobran.append(f"{seccion}: «{c}»")

    # las tres tablas de referencia, fila a fila y celda a celda
    for clave, origen in (("usos", verbo["usos"]),
                          ("voces_tabla", verbo["voces"]),
                          ("ganas", verbo["ganas"])):
        destino = prosa.get(clave) or []
        if len(destino) != len(origen):
            faltan.append(f"{clave}: {len(destino)} filas en inglés frente a "
                          f"{len(origen)} en español")
            continue
        for i, (fe, fi) in enumerate(zip(origen, destino)):
            if len(fe) != len(fi):
                faltan.append(f"{clave} fila {i}: {len(fi)} celdas frente a "
                              f"{len(fe)}")
                continue
            for j, (ce, ci) in enumerate(zip(fe, fi)):
                if ce.strip() and not str(ci).strip():
                    faltan.append(f"{clave} fila {i} celda {j}: sin traducir")
    return esp, faltan, sobran


def informe(verbo, escs, ing, esp):
    prosa = ing["prosa"]
    L = []
    a = L.append
    a("# El verbo en inglés: cotejo para adjudicar\n")
    a("Borrador de `recursos/verbo/ingles.json`. **No está publicado**: "
      "mientras `\"adjudicado\"` sea `false`, la página en inglés muestra la "
      "prosa en español con un aviso en el pie. Firmarlo es poner "
      "`\"adjudicado\": true` con `adjudicado_por` y `fecha`.\n")
    a("La terminología sale de la traducción inglesa del Ākhyāta-kappa del "
      "propio Bhikkhu Nandisena (`docs/6 - Ākhyāta-Kaccāyana.md`), no de "
      "criterio ajeno. De ahí: los nombres de las vibhatti se conservan en "
      "pāḷi entre comillas; «root», «person», «conjugational sign» y "
      "«reduplication» son sus palabras; y *sattamī* es **potential**, no "
      "«optative».\n")
    a("**Las formas pāḷi no se traducen** y no salen aquí. Las referencias "
      "§N tampoco: son la cita.\n")

    a("## 1. Operaciones de las escaleras\n")
    a("| español | inglés |")
    a("| --- | --- |")
    for c in esp["operaciones"]:
        a(f"| {c} | {prosa['operaciones'].get(c, '**FALTA**')} |")

    a("\n## 2. Glosas de las raíces\n")
    a("| español | inglés |")
    a("| --- | --- |")
    for c in esp["glosas"]:
        a(f"| {c} | {prosa['glosas'].get(c, '**FALTA**')} |")

    a("\n## 3. Tiempos, voces, personas y números\n")
    a("| español | inglés |")
    a("| --- | --- |")
    for seccion in ("tiempos", "voces", "personas", "numeros"):
        for c in esp[seccion]:
            a(f"| {c} | {prosa[seccion].get(c, '**FALTA**')} |")

    a("\n## 4. Líneas «Formación:»\n")
    a("| español | inglés |")
    a("| --- | --- |")
    for c in esp["formacion"]:
        a(f"| {c} | {prosa['formacion'].get(c, '**FALTA**')} |")

    for titulo, clave, origen in (
            ("5. Usos de las inflexiones verbales", "usos", verbo["usos"]),
            ("6. Las tres voces", "voces_tabla", verbo["voces"]),
            ("7. Los ocho grupos de raíces", "ganas", verbo["ganas"])):
        a(f"\n## {titulo}\n")
        destino = prosa.get(clave) or []
        for i, fila in enumerate(origen):
            if i >= len(destino):
                a("**FALTA la fila {0}**\n".format(i))
                continue
            a(f"**{fila[1].replace(' / ', ' · ') or '—'}**\n")
            for j, celda in enumerate(fila):
                if not celda.strip():
                    continue
                a(f"- ES · {celda}")
                a(f"- EN · {destino[i][j]}")
            a("")

    a("\n## 8. Lo que queda por decidir\n")
    a("1. **«potential» por *sattamī***, siguiendo su propia traducción. La "
      "mayoría de las gramáticas modernas escriben «optative».")
    a("2. **«parassapada» y «attanopada» se glosan** —«the word for another», "
      "«the word for oneself»— porque el español los glosa. Su traducción "
      "del Ākhyāta los deja sin glosar.")
    a("3. **«kāraka» rotula las tres voces**, aquí y en el español. En el "
      "Kāraka-kappa la misma voz nombra las relaciones de caso, y un lector "
      "atento puede tropezar.")
    a("4. **«double ‘v’» por «duplicar ‘v’»**, no «reduplicate»: la "
      "reduplicación de sílaba es *abbhāsa*, y es otra cosa.")
    a("5. La celda de explicación del **gahādi-gaṇa está vacía también en "
      "inglés**, porque lo está en el español. Es el defecto del documento "
      "base descrito en `escaleras-por-adjudicar.md` §5, no un hueco de "
      "traducción.")
    return "\n".join(L) + "\n"


def main():
    if not os.path.exists(INGLES):
        sys.exit("Falta recursos/verbo/ingles.json. Ejecutar antes "
                 "construir_ingles_verbo.py.")
    verbo = json.load(open(VERBO, encoding="utf-8"))
    ing = json.load(open(INGLES, encoding="utf-8"))
    escs = escaleras()

    esp, faltan, sobran = comprobar(verbo, escs, ing)

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    open(DESTINO, "w", encoding="utf-8").write(informe(verbo, escs, ing, esp))

    total = sum(len(v) for v in esp.values())
    print(os.path.relpath(DESTINO, RAIZ))
    print(f"  cadenas comprobadas  {total}")
    print(f"  sin traducir         {len(faltan)}")
    print(f"  inglés sin español   {len(sobran)}")
    for f in faltan[:15]:
        print("   ✗", f)
    for s in sobran[:15]:
        print("   ·", s, "(sobra)")
    estado = ("ADJUDICADO por " + (ing.get("adjudicado_por") or "?")
              if ing.get("adjudicado") else "SIN ADJUDICAR — no se publica")
    print(f"  estado               {estado}")
    return 1 if faltan else 0


if __name__ == "__main__":
    sys.exit(main())
