#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dónde está cada archivo, sin obligar a una sola disposición de carpetas.

El proyecto vive en dos formas: el árbol del `CLAUDE.md` §7 —`nuestro/`,
`recursos/sandhi/`, `herramientas/`— y una carpeta plana donde está todo junto,
que es como se comparte. Los módulos no deberían romperse por eso.

`ruta("recursos", "sandhi", "reglas.json")` busca, en este orden:

  1. la ruta completa a partir de la raíz del árbol (la carpeta madre del script)
  2. la misma ruta a partir de la carpeta del script
  3. **sólo el nombre del archivo**, en la carpeta del script y en su madre

Devuelve la primera que exista. Si no existe ninguna, devuelve la primera —para
que el mensaje de error diga dónde se esperaba encontrarla—.
"""

import os

AQUI = os.path.dirname(os.path.abspath(__file__))
MADRE = os.path.dirname(AQUI)


def ruta(*partes):
    nombre = partes[-1]
    candidatas = [
        os.path.join(MADRE, *partes),
        os.path.join(AQUI, *partes),
        os.path.join(AQUI, nombre),
        os.path.join(MADRE, nombre),
    ]
    for c in candidatas:
        if os.path.exists(c):
            return c
    return candidatas[0]


def destino(*partes):
    """Dónde ESCRIBIR un archivo que puede no existir todavía.

    Si ya existe en algún lado, ahí. Si no, en el árbol cuando el árbol
    existe, y si no, junto al script — que es el caso de la carpeta plana.
    """
    p = ruta(*partes)
    if os.path.exists(p):
        return p
    if os.path.isdir(os.path.join(MADRE, partes[0])):
        return os.path.join(MADRE, *partes)
    return os.path.join(AQUI, partes[-1])


def raiz():
    """La carpeta que manda: la madre si el árbol existe, si no la del script."""
    return MADRE if os.path.isdir(os.path.join(MADRE, "recursos")) else AQUI


def rel(p):
    try:
        return os.path.relpath(p, raiz())
    except ValueError:
        return p
