#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
¿Está ya en la web lo que hay en la Mac?

    python3 herramientas/comprobar_despliegue.py

Pedido del IEBH, 2026-08-31: «¿hay manera simple de saber cuándo el push ya ha
cambiado la página?». La hay, y no es mirar la versión: la versión cambia una
vez cada muchos empujones, de modo que sirve para las veces en que no hace
falta y calla justo cuando sí.

Lo que se compara es el ARCHIVO: el sha256 del `site/…/index.html` de aquí
contra el de la página que sirve el dominio. Si coinciden, lo desplegado es
exactamente esto; si no, no lo es. No hay que embeber nada en la página —el
gancho de pre-commit la regenera ANTES de que el commit exista, de modo que un
sha de git metido dentro iría siempre uno por detrás, y una marca de tiempo
dejaría el archivo sucio en cada regeneración—.

Distingue TRES estados, que es la gracia, porque «no se ve el cambio» tiene
dos causas muy distintas y se arreglan al revés:

    1. hay commits sin empujar      → falta el push
    2. empujado, pero la página no coincide  → el despliegue va en camino
    3. coincide                      → ya está

Sin argumentos mira el solucionador. Con «--todo», también la portada y los
demás recursos generados.
"""

import argparse
import hashlib
import os
import subprocess
import sys
import urllib.error
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITIO = "https://gramaticas.buddha-dhamma.net"

# (ruta dentro de site/, ruta en la web)
PAGINAS = [
    ("recursos/solucionador/index.html", "/recursos/solucionador/"),
]
PAGINAS_TODO = PAGINAS + [
    ("index.html", "/"),
    ("recursos/sandhi/index.html", "/recursos/sandhi/"),
    ("recursos/raices/index.html", "/recursos/raices/"),
    ("recursos/paradigmas/index.html", "/recursos/paradigmas/"),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()[:12]


def git(*args):
    r = subprocess.run(["git"] + list(args), cwd=RAIZ,
                       capture_output=True, text=True)
    return r.stdout.strip()


def bajar(url, espera):
    pet = urllib.request.Request(url, headers={
        # Sin caché: se pregunta por lo que hay AHORA, no por lo que había.
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "User-Agent": "comprobar-despliegue/1.0",
    })
    with urllib.request.urlopen(pet, timeout=espera) as r:
        return r.read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--todo", action="store_true",
                    help="mira también la portada y los demás recursos")
    ap.add_argument("--espera", type=float, default=20.0)
    a = ap.parse_args()

    # 1 · ¿queda algo sin empujar?
    git("fetch", "-q", "origin")
    pendientes = [l for l in git("log", "origin/main..main",
                                 "--oneline").splitlines() if l]
    sucio = [l for l in git("status", "--porcelain").splitlines() if l]

    print()
    if sucio:
        print("  ⚠ El árbol tiene cambios SIN COMMIT ({0}).".format(len(sucio)))
        print("    Lo que se compara abajo es el archivo del disco, no el commit.")
    if pendientes:
        print("  ⚠ Hay {0} commit(s) SIN EMPUJAR:".format(len(pendientes)))
        for l in pendientes:
            print("      " + l)
        print("    → git push origin main")
    else:
        print("  ✓ Todo lo del repositorio está empujado.")
    print()

    paginas = PAGINAS_TODO if a.todo else PAGINAS
    iguales = 0
    for rel, ruta in paginas:
        local = os.path.join(RAIZ, "site", rel)
        if not os.path.exists(local):
            print("  · {0:<34} (no existe en site/)".format(ruta))
            continue
        with open(local, "rb") as f:
            b_local = f.read()
        try:
            b_web = bajar(SITIO + ruta, a.espera)
        except (urllib.error.URLError, OSError) as e:
            print("  · {0:<34} no se pudo consultar: {1}".format(ruta, e))
            continue
        if sha(b_local) == sha(b_web):
            iguales += 1
            print("  ✓ {0:<34} AL DÍA   ({1})".format(ruta, sha(b_local)))
        else:
            print("  ✗ {0:<34} DISTINTA".format(ruta))
            print("      aquí: {0} · {1:>9} bytes".format(
                sha(b_local), len(b_local)))
            print("      web:  {0} · {1:>9} bytes".format(
                sha(b_web), len(b_web)))

    print()
    if iguales == len(paginas) and not pendientes and not sucio:
        print("  Ya está: lo que sirve el dominio es exactamente esto.")
        return 0
    if pendientes:
        print("  Falta el push.")
    elif iguales != len(paginas):
        print("  Empujado, pero el despliegue todavía no ha llegado.")
        print("  Cloudflare tarda unos segundos; vuelva a correrlo.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
