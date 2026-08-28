#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el lote de formas por adjudicar (decisión de Angel, 2026-08-28:
«adjudication now»).

    python3 herramientas/generar_por_adjudicar.py            # lote de 250
    python3 herramientas/generar_por_adjudicar.py --n 100

Recorre las formas del canon por frecuencia descendente y aparta las que la
señal del solucionador marcaría ante un lector —«segura» o «posible»— y que
todavía no están ni en el banco ni adjudicadas. Son las de mayor valor: lo
que la página AFIRMA es lo primero que conviene verificar, y las más
frecuentes cubren la mayor parte de lo que un lector pega.

Salida: `docs/solucionador/por-adjudicar-lote-N.md`, con las lecturas del
motor y una línea VEREDICTO por forma. El veredicto se escribe a mano y se
incorpora con:

    python3 herramientas/incorporar_adjudicaciones.py docs/solucionador/por-adjudicar-lote-N.md
"""

import argparse
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "nuestro"))
from normalizar import cotejo                                      # noqa: E402
import solucionar_sandhis as S                                     # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=250)
    ap.add_argument("--lote", type=int, default=1)
    a = ap.parse_args()
    S.SOLO_CANON = True
    c = S.cargar()
    frec = c["frecuencia"]

    filas = []
    revisadas = 0
    for f, n in sorted(frec.items(), key=lambda x: (-x[1], x[0])):
        if len(filas) >= a.n:
            break
        revisadas += 1
        if f in c["banco"] or f in c["casos"]:
            continue
        try:
            r = S.solucionar(f)
        except Exception:                                          # noqa: BLE001
            continue
        if not r.get("senal"):
            continue
        filas.append({"f": f, "n": n, "senal": r["senal"],
                      "motivo": r.get("senal_motivo", ""),
                      "lecturas": r.get("lecturas", [])})

    destino = os.path.join(RAIZ, "docs", "solucionador",
                           "por-adjudicar-lote-{0}.md".format(a.lote))
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as out:
        out.write("""# Formas por adjudicar — lote {0}

*Generado por `herramientas/generar_por_adjudicar.py`. Las {1} formas más
frecuentes del canon que la señal del solucionador marcaría ante un lector
y que aún no están en el banco ni adjudicadas, en orden de frecuencia. Se
revisaron las {2} formas más frecuentes del corpus para reunirlas.*

**Cómo se adjudica.** En la línea `VEREDICTO:` de cada forma se escribe:

- la **letra** de la lectura correcta — `a`, `b`, `c`… —;
- **`no`** si la forma no es sandhi (palabra entera, flexión);
- **`compuesto`** si es un compuesto, fuera del encargo;
- o los componentes explícitos — `tena + upasaṅkami` — si la lectura
  correcta no está entre las listadas (quedará registrada aunque el motor
  no la produzca todavía: el arnés la mostrará como pendiente).

Lo que quede en blanco no se incorpora. Después:

    python3 herramientas/incorporar_adjudicaciones.py docs/solucionador/por-adjudicar-lote-{0}.md
    python3 herramientas/generar_solucionador.py
    node nuestro/js/arnes_casos.js

---

""".format(a.lote, len(filas), revisadas))
        for i, x in enumerate(filas, 1):
            out.write("## {0}. {1}  ·  {2} veces  ·  señal {3}\n\n".format(
                i, x["f"], x["n"], x["senal"]))
            letras = "abcdefghij"
            for j, l in enumerate(x["lecturas"][:8]):
                comp = " + ".join(l.get("componentes", []))
                citas = []
                if l.get("sutta") is not None:
                    citas.append("§{0}".format(l["sutta"]))
                pasos = l.get("pasos") or []
                out.write("- **{0})** {1}{2} — `{3}`\n".format(
                    letras[j], comp,
                    " (" + ", ".join(citas) + ")" if citas else "",
                    " · ".join(pasos)))
            if len(x["lecturas"]) > 8:
                out.write("- … y {0} lecturas más\n".format(
                    len(x["lecturas"]) - 8))
            if not x["lecturas"]:
                out.write("- *el motor no produce ninguna lectura; "
                          "la señal fue: {0}*\n".format(x["motivo"]))
            out.write("\nVEREDICTO: \n\n---\n\n")

    print("{0} formas por adjudicar (de las {1} más frecuentes) → {2}".format(
        len(filas), revisadas, os.path.relpath(destino, RAIZ)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
