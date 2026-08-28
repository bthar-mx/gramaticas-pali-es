#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mide el solucionador contra el corpus del proyecto `Sandhi`.

`Sandhi` resolvió la Etapa 1 —partir la forma— sobre la Therīgāthā entera y su
comentario. Este proyecto hace la Etapa 2 —decir bajo qué sutta opera cada
cambio— pero no tenía contra qué medirse: 194 de 251 formas del propio banco no
es una medida del mundo, es una medida de la casa.

Lo que se pregunta aquí es una sola cosa, y no es «¿acertamos?»:

  · **acuerdo pleno** — las dos voces de `Sandhi` están entre nuestras lecturas
  · **acuerdo en el corte** — coincide la primera voz y difiere la segunda.
    Casi siempre es convención, no análisis: `Sandhi` cita **lemas** —«na +
    abhijānāti»— y nosotros **voces flexionadas** —«na + abhijānāmi»—. El punto
    donde se parte la forma es el mismo.
  · **silencio**  — no proponemos nada (`no_resuelto`)
  · **desacuerdo**— proponemos, pero su corte no está
  · **ruido**     — cuántas lecturas hay que mirar para encontrar la suya

El corte de `Sandhi` **no es la verdad**: es otro proponente, con menos fuentes
y las suyas propias. Un desacuerdo puede ser un error nuestro o suyo. Por eso se
escribe la lista completa de desacuerdos, para leerla, no un porcentaje.

    python3 medir_contra_corpus.py                 # los versos (5.902 palabras)
    python3 medir_contra_corpus.py --comentario    # + el aṭṭhakathā
    python3 medir_contra_corpus.py --limite 200
"""

import argparse
import json
import os
import re
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from rutas import ruta                                             # noqa: E402
from normalizar import cotejo                                      # noqa: E402
import solucionar_sandhis as S                                     # noqa: E402

def corpus(nombre):
    """Los dos corpus vienen del proyecto `Sandhi`. Se buscan primero dentro de
    este proyecto —que es donde deben estar, para que sea independiente— y, si
    no están, en la carpeta hermana `Sandhi/generado`, que es de donde salieron.
    Se leen; no se escriben nunca."""
    p = ruta("recursos", "corpus", nombre)
    if os.path.exists(p):
        return p
    hermana = os.path.join(os.path.dirname(os.path.dirname(AQUI)),
                           "Sandhi", "generado", nombre)
    return hermana if os.path.exists(hermana) else p


VERSOS = corpus("therigatha_sandhi.json")
COMENT = corpus("therigatha_atthakatha_sandhi.json")


def normalizar_piezas(p):
    """`piezas` viene en dos formas: un corte, o una lista de cortes alternos."""
    if not p:
        return []
    if isinstance(p[0], list):
        return [tuple(cotejo(x) for x in c) for c in p]
    return [tuple(cotejo(x) for x in p)]


def sin_desinencia(t):
    """La misma voz sin la marca final de flexión: cantidad de la vocal última
    y niggahīta. No es un análisis morfológico; sólo permite comparar el corte
    de `Sandhi` —que da temas— con el nuestro —que da voces flexionadas—."""
    t = t.rstrip("ṃ")
    return re.sub(r"[āīū]$",
                  lambda x: {"ā": "a", "ī": "i", "ū": "u"}[x.group()], t)


def es_yuxtaposicion(forma, cortes):
    """La **primera juntura** del corte de `Sandhi` no lleva ninguna operación:
    concatenar las dos primeras piezas ya reproduce el principio de la forma.

    Eso no es un sandhi. Es un compuesto —`soka + pareta` → `sokaparetāya`,
    `sabba + saṃyojana + khaya` → `sabbasaṃyojanakkhaye`— o una formación con
    sufijo, y los compuestos están fuera del encargo por instrucción del
    Venerable. No se cuenta como desacuerdo nuestro: se cuenta aparte.

    **Se mira la primera juntura y no la concatenación entera** porque la
    última pieza viene como lema y la forma va flexionada: `soka + pareta`
    nunca va a reproducir `sokaparetāya` letra por letra, y comparar el total
    dejaba pasar como «desacuerdo» a veintiún compuestos. Se compara entonces
    la primera pieza más la segunda **sin su vocal final**, que es lo que la
    flexión no toca.

    Y se mira la **primera**, no cualquiera: si la primera juntura no opera, el
    corte de esa forma es un corte de compuesto, sea lo que sea lo que pase más
    adentro. Al revés no vale —`valāhakaṃ + iva + addhagū` sí opera en la
    primera, y se mide—.
    """
    if len(forma.split()) > 1:
        # Una **frase** ya viene partida en voces por el propio texto: la
        # operación puede estar en cualquiera de sus junturas, no en la
        # primera. `puttā + me + atthi` → «puttā m’ atthi» opera en la segunda.
        # Mirar sólo la primera las excluiría todas, y son sandhis firmados.
        return False
    f = cotejo(forma)
    for c in cortes:
        if len(c) < 2:
            continue
        a, b = c[0], c[1]
        sin_vocal = b[:-1] if b and b[-1] in "aāiīuūeo" else b
        if f.startswith(a + sin_vocal):
            return True
        if sin_desinencia(f) == sin_desinencia("".join(c)):
            return True
    return False


def nuestras(r):
    salida = []
    for L in r.get("lecturas", []):
        salida.append(tuple(cotejo(x) for x in L.get("componentes", [])))
    return salida


def medir(archivo, categorias, limite=None):
    d = json.load(open(archivo, encoding="utf-8"))
    filas = [w for w in d["palabras"] if w.get("categoria") in categorias]
    if limite:
        filas = filas[:limite]

    cuenta = {"acuerdo": 0, "corte": 0, "desacuerdo": 0, "silencio": 0,
              "fuera_de_alcance": 0}
    rangos = []
    desacuerdos = []
    silencios = []
    lecturas_totales = 0

    for w in filas:
        suyas = normalizar_piezas(w.get("piezas"))
        if es_yuxtaposicion(w["forma"], suyas):
            cuenta["fuera_de_alcance"] += 1
            continue
        try:
            r = S.solucionar(w["forma"])
        except Exception as e:                                     # noqa: BLE001
            desacuerdos.append((w["forma"], suyas, "ERROR " + str(e)))
            cuenta["desacuerdo"] += 1
            continue
        mias = nuestras(r)
        lecturas_totales += len(mias)
        if not mias:
            cuenta["silencio"] += 1
            silencios.append((w["forma"], suyas, r.get("motivo")))
            continue
        hallada = None
        for i, m in enumerate(mias):
            if m in suyas:
                hallada = i + 1
                break
        if hallada:
            cuenta["acuerdo"] += 1
            rangos.append(hallada)
        else:
            primeras = {x[0] for x in mias if x}
            if any(s and s[0] in primeras for s in suyas):
                cuenta["corte"] += 1
            else:
                cuenta["desacuerdo"] += 1
                desacuerdos.append((w["forma"], suyas, mias[:4]))

    en_alcance = len(filas) - cuenta["fuera_de_alcance"]
    return {
        "archivo": os.path.basename(archivo),
        "meta": d["meta"],
        "medidas": len(filas),
        "en_alcance": en_alcance,
        "cuenta": cuenta,
        "lecturas_por_forma": round(lecturas_totales / en_alcance, 1) if en_alcance else 0,
        "rango_medio": round(sum(rangos) / len(rangos), 1) if rangos else None,
        "rango_1": sum(1 for x in rangos if x == 1),
        "desacuerdos": desacuerdos,
        "silencios": silencios,
    }


def informe(m):
    c = m["cuenta"]
    n = m["en_alcance"]
    pc = lambda x: "{0:5.1f}%".format(100.0 * x / n) if n else "  --  "
    print("\n  {0}   ·   {1} formas marcadas «sandhi» por Sandhi"
          .format(m["archivo"], m["medidas"]))
    print("  de ellas {0} son yuxtaposición —compuesto o sufijo, sin operación"
          .format(c["fuera_de_alcance"]))
    print("  entre las voces—, fuera del encargo. Quedan {0} medibles.".format(n))
    print("  " + "-" * 62)
    print("  acuerdo pleno    {0:6d}  {1}   (las dos voces coinciden)"
          .format(c["acuerdo"], pc(c["acuerdo"])))
    print("  acuerdo en corte {0:6d}  {1}   (misma primera voz; lema vs. forma)"
          .format(c["corte"], pc(c["corte"])))
    print("  desacuerdo       {0:6d}  {1}   (parten en otro punto)"
          .format(c["desacuerdo"], pc(c["desacuerdo"])))
    print("  silencio         {0:6d}  {1}   (no proponemos nada)"
          .format(c["silencio"], pc(c["silencio"])))
    print("  " + "-" * 62)
    print("  el punto de corte coincide en {0} de {1}   {2}"
          .format(c["acuerdo"] + c["corte"], n, pc(c["acuerdo"] + c["corte"])))
    print("  " + "-" * 62)
    print("  lecturas por forma: {0}      su corte en 1er lugar: {1}"
          .format(m["lecturas_por_forma"], m["rango_1"]))
    print("  rango medio de su corte entre las nuestras: {0}".format(m["rango_medio"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--comentario", action="store_true")
    ap.add_argument("--limite", type=int)
    ap.add_argument("--categorias", default="sandhi")
    ap.add_argument("--salida")
    ap.add_argument("--canon", action="store_true", help=(
        "mide con la capa del canon encendida. Apagada por defecto: "
        "555 de 698 (79,5 %) con ella, 630 (90,3 %) sin ella."))
    a = ap.parse_args()
    S.USAR_CANON = a.canon

    cats = set(a.categorias.split(","))
    archivo = COMENT if a.comentario else VERSOS
    m = medir(archivo, cats, a.limite)
    informe(m)

    if a.salida:
        json.dump(m, open(a.salida, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("\n  escrito: {0}".format(a.salida))
    return m


if __name__ == "__main__":
    S.consola_utf8()
    main()
