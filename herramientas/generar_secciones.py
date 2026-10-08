#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
El mapa §N → capítulo, para «Ir a §» (rediseño de la navegación, etapa 1).

    python3 herramientas/generar_secciones.py

Escribe site/assets/secciones.json a partir de comun/concordancia.json:

    {"capitulos": {"sandhi": {"num": 1, "titulo": "Sandhi-Kappa",
                              "desde": 1, "hasta": 51, "en": true}, …},
     "secciones": {"1": "sandhi", …, "405": "taddhita"}}

Sólo entra un § si su capítulo está publicado y la página lleva de verdad el
ancla id="sN": un número sin § publicado no lleva a ninguna parte, y la barra
lo dice («§406 aún no está publicado») en vez de dar un enlace muerto. «en»
dice si existe la edición inglesa del capítulo.

Va en generar_todo.py después de los capítulos (lee su HTML) y antes de
generar_indices.py (la portada toma de aquí los rangos de cada capítulo) y
de generar_seo.py. Es determinista: mismo origen, mismo archivo, byte a byte.

De paso comprueba que la paleta de site/assets/cabecera.css siga siendo la de
pali.css (véase cabecera.comprobar_tokens) y falla si no.
"""

import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "herramientas"))

from generar_capitulo import CAPITULOS  # noqa: E402
import cabecera  # noqa: E402

DESTINO = os.path.join(RAIZ, "site", "assets", "secciones.json")


def mapa():
    conc = json.load(open(os.path.join(RAIZ, "comun", "concordancia.json"),
                          encoding="utf-8"))
    capitulos, secciones = {}, {}
    for clave, meta in CAPITULOS.items():
        if meta["obra_slug"] != "kaccayana" or clave not in conc["capitulos"]:
            continue
        slug = meta["slug"]
        pagina = os.path.join(RAIZ, "site", "kaccayana", slug, "index.html")
        if not os.path.exists(pagina):
            continue
        anclas = set(re.findall(r'\bid="s(\d+)"', open(pagina, encoding="utf-8").read()))
        ns = [s["kaccayana"] for s in conc["capitulos"][clave]["suttas"]
              if str(s["kaccayana"]) in anclas]
        if not ns:
            continue
        for n in ns:
            if str(n) in secciones:
                raise SystemExit("§{0} en dos capítulos: {1} y {2}".format(
                    n, secciones[str(n)], slug))
            secciones[str(n)] = slug
        # la edición inglesa cuenta si existe y lleva las mismas anclas
        pagina_en = os.path.join(RAIZ, "site", "en", "kaccayana", slug, "index.html")
        en = os.path.exists(pagina_en) and set(map(str, ns)) <= set(
            re.findall(r'\bid="s(\d+)"', open(pagina_en, encoding="utf-8").read()))
        capitulos[slug] = {"num": meta["num"],
                           "titulo": conc["capitulos"][clave]["titulo"],
                           "desde": min(ns), "hasta": max(ns), "en": en}
    orden = sorted(secciones, key=int)
    return {"_nota": "Generado por herramientas/generar_secciones.py a partir de "
                     "comun/concordancia.json; no editar a mano.",
            "capitulos": capitulos,
            "secciones": {k: secciones[k] for k in orden}}


def main():
    malos = cabecera.comprobar_tokens()
    if malos:
        print("La paleta de cabecera.css no es la de pali.css:")
        for m in malos:
            print("   ", m)
        return 1
    d = mapa()
    texto = json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "\n"
    with open(DESTINO, "w", encoding="utf-8") as f:
        f.write(texto)
    rangos = ", ".join("{0} §{1}–§{2}".format(s, c["desde"], c["hasta"])
                       for s, c in d["capitulos"].items())
    print("{0} §§ en {1} capítulos ({2}) → site/assets/secciones.json".format(
        len(d["secciones"]), len(d["capitulos"]), rangos))
    return 0


if __name__ == "__main__":
    sys.exit(main())
