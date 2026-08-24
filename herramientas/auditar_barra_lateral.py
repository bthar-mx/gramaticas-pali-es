#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Comprueba qué «position» acaba aplicándose a cada control del índice.

    python3 herramientas/auditar_barra_lateral.py site/assets/pali.css


Recorre las reglas en orden, entrando en los @media, y se queda con la
última declaración que le toca al elemento —no a su ::after—. Es la
comprobación que faltaba cuando una regla posterior le puso «relative» al
botón de ocultar y lo devolvió al flujo, encima del título.
"""
import re, sys

def reglas(css):
    """[(selectores, cuerpo)] aplanando los @media."""
    fuera, i, n = [], 0, len(css)
    pila = []
    while i < n:
        j = css.find('{', i)
        if j < 0: break
        cab = css[i:j].strip()
        # cerrar bloques @media pendientes antes de esta cabecera
        k, prof = j + 1, 1
        while k < n and prof:
            if css[k] == '{': prof += 1
            elif css[k] == '}': prof -= 1
            k += 1
        cuerpo = css[j+1:k-1]
        if cab.startswith('@'):
            fuera.extend(reglas(cuerpo))
        else:
            fuera.append((cab, cuerpo))
        i = k
    return fuera

def ultima_position(css, sel):
    vistas = []
    for cab, cuerpo in reglas(css):
        sels = [x.strip() for x in cab.split(',')]
        # Vale cualquier selector cuyo último tramo sea el elemento
        # —«html.sin-toc #toc-volver» lo es—, pero no sus pseudoelementos.
        def apunta(x):
            if '::' in x:
                return False
            ultimo = x.split()[-1] if x.split() else ''
            return (ultimo == sel or ultimo.startswith(sel + '[')
                    or ultimo.startswith(sel + ':'))
        propio = [x for x in sels if apunta(x)]
        if not propio:
            continue
        for d in re.finditer(r'(?<![-\w])position:\s*([a-z]+)', cuerpo):
            vistas.append(d.group(1))
    return vistas

import os
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    RAIZ, "site", "assets", "pali.css")
css = open(ruta, encoding='utf-8').read()
mal = 0
for sel, esperado in (('.toc-ocultar', 'absolute'), ('#toc-volver', 'fixed')):
    v = ultima_position(css, sel)
    ok = v and v[-1] == esperado
    mal += 0 if ok else 1
    print(('✓' if ok else '✗'), sel, '→', v[-1] if v else '(ninguna)',
          '· esperado:', esperado, '· todas:', v or '—')

# Un globo que cuelgue de algo metido en la barra lateral tiene que ir en
# «fixed»: la barra lleva overflow-y:auto, que recorta también a los lados,
# y el globo es más ancho que ella. En «absolute» sale cortado.
#
# Como arriba, lo que cuenta es la última declaración que le aplica, no cada
# regla por separado: hay una regla común que pone «absolute» a todos los
# globos y luego la propia que la corrige.
for sel, dentro in (('.toc-ocultar', True), ('#toc-volver', False)):
    pos = []
    for cab, cuerpo in reglas(css):
        sels = [x.strip() for x in cab.split(',')]
        if not any(x.startswith(sel) and '::after' in x for x in sels):
            continue
        pos += re.findall(r'(?<![-\w])position:\s*([a-z]+)', cuerpo)
    if not pos:
        continue
    esperado = 'fixed' if dentro else 'absolute'
    bien = pos[-1] == esperado
    mal += 0 if bien else 1
    print(('✓' if bien else '✗'), sel + '::after →', pos[-1],
          '· esperado:', esperado,
          '· dentro de la barra' if dentro else '· fuera de la barra',
          '· todas:', pos)

sys.exit(1 if mal else 0)
