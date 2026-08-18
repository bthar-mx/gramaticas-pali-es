#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenera todo el sitio a partir de las fuentes.

    python3 herramientas/generar_todo.py

Recorre los capítulos de las gramáticas, los documentos de recursos/ y la
referencia interactiva de sandhi. Es el comando que hay que ejecutar tras
tocar cualquier markdown, y el que conviene poner como orden de compilación
en Cloudflare para que nunca haga falta acordarse.

Devuelve código de salida 1 si algo falla.
"""

import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERR = os.path.join(RAIZ, "herramientas")
PY = sys.executable or "python3"


def correr(script, *args):
    orden = [PY, os.path.join(HERR, script), *args]
    etiqueta = " ".join([script, *args])
    r = subprocess.run(orden, cwd=RAIZ, capture_output=True, text=True)
    salida = (r.stdout or "").strip()
    if r.returncode == 0:
        print("· {0}\n    {1}".format(etiqueta, salida.replace("\n", "\n    ")))
    else:
        print("✗ {0}".format(etiqueta))
        print((salida + "\n" + (r.stderr or "")).strip())
    return r.returncode


def main():
    fallos = 0

    # capítulos de las gramáticas
    sys.path.insert(0, HERR)
    from generar_capitulo import CAPITULOS
    for clave, meta in CAPITULOS.items():
        md = os.path.join(RAIZ, meta["obra_slug"], clave + ".md")
        if os.path.exists(md):
            fallos += correr("generar_capitulo.py",
                             os.path.join(meta["obra_slug"], clave + ".md"))

    # documentos en prosa
    #
    # combinacion-eufonica.md ya no se publica: la referencia interactiva de
    # /recursos/sandhi/ lo reemplaza. El markdown se conserva porque
    # reconstruir_sandhi.py lo lee para rehacer reglas.json.
    SIN_PUBLICAR = {"combinacion-eufonica.md"}

    recursos = os.path.join(RAIZ, "recursos")
    if os.path.isdir(recursos):
        for f in sorted(os.listdir(recursos)):
            if f.endswith(".md") and f not in SIN_PUBLICAR:
                fallos += correr("generar_recurso.py", os.path.join("recursos", f))

    # referencia interactiva de sandhi
    if os.path.exists(os.path.join(recursos, "sandhi", "plantilla.html")):
        fallos += correr("generar_sandhi.py")

    # formación del nombre · pācako
    if os.path.exists(os.path.join(recursos, "nombre", "plantilla.html")):
        fallos += correr("generar_nombre.py")

    # paradigmas de declinación
    if os.path.exists(os.path.join(recursos, "paradigmas", "plantilla.html")):
        fallos += correr("generar_paradigmas.py")

    # las tres páginas de índice — al final, porque cuentan lo ya generado
    fallos += correr("generar_indices.py")

    print()
    print("Todo regenerado." if not fallos else "{0} paso(s) con error.".format(fallos))
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
