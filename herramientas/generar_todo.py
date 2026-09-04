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
        # edición inglesa del mismo capítulo, si existe (sesión 45). Va
        # después del español y se genera dos veces: la primera crea la
        # página inglesa; la segunda pasada del español (abajo) ya la ve y
        # pone el botón EN/ES y el `hreflang` en las dos.
        md_en = os.path.join(RAIZ, meta["obra_slug"], clave + ".en.md")
        if os.path.exists(md_en):
            fallos += correr("generar_capitulo.py",
                             os.path.join(meta["obra_slug"], clave + ".en.md"))
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

    # el verbo · ākhyāta
    # El cotejo del inglés se rehace siempre: es lo que IEBH firma, y si el
    # español cambia tiene que verse en el acto qué se queda sin traducir.
    if os.path.exists(os.path.join(recursos, "verbo", "plantilla.html")):
        if os.path.exists(os.path.join(recursos, "verbo", "ingles.json")):
            fallos += correr("generar_ingles_verbo.py")
        fallos += correr("generar_verbo.py")

    # solucionador de sandhis
    # El léxico fragmentado (20 MB) sólo se rehace si el corpus cambió: en
    # cada commit sería medio minuto para escribir lo mismo byte a byte.
    if os.path.exists(os.path.join(recursos, "solucionador", "plantilla.html")):
        corpus = os.path.join(recursos, "corpus", "corpus-formas.json")
        indice = os.path.join(RAIZ, "site", "recursos", "solucionador",
                              "lexico", "indice.json")
        if os.path.exists(corpus) and (
                not os.path.exists(indice)
                or os.path.getmtime(indice) < os.path.getmtime(corpus)):
            fallos += correr("generar_lexico_solucionador.py")
        fallos += correr("generar_solucionador.py")

    # paradigmas de declinación
    if os.path.exists(os.path.join(recursos, "paradigmas", "plantilla.html")):
        fallos += correr("generar_paradigmas.py")

    # raíces pāḷi y sánscritas
    # Los datos los producen extraer_raices.py, extraer_dhatupatha.py y
    # extraer_dhatumanjusa.py a partir de los PDF, que no están en el
    # repositorio; aquí sólo se publica lo ya extraído.
    if os.path.exists(os.path.join(recursos, "raices", "raices.json")):
        fallos += correr("generar_raices.py")

    # glosario de terminología gramatical
    # El cotejo del inglés del Glosario de Nandisena se rehace siempre, como
    # el del verbo: es lo que el IEBH firma.
    if os.path.exists(os.path.join(recursos, "glosario", "plantilla.html")):
        if os.path.exists(os.path.join(recursos, "glosario", "ingles.json")):
            fallos += correr("generar_ingles_glosario.py")
        fallos += correr("generar_glosario.py")

    # las tres páginas de índice — al final, porque cuentan lo ya generado
    fallos += correr("generar_indices.py")

    print()
    print("Todo regenerado." if not fallos else "{0} paso(s) con error.".format(fallos))
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
