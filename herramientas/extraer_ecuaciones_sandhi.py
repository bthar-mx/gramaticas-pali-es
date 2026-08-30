#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Las ecuaciones de sandhi que el Venerable escribe, no las que se infieren.

    python3 herramientas/extraer_ecuaciones_sandhi.py
    python3 herramientas/extraer_ecuaciones_sandhi.py --ver-fallos

Los documentos de capítulo de la Therīgāthā traen una sección «Lista de
voces» donde cada palabra se analiza, y donde las formas de sandhi vienen
**resueltas con un signo igual**:

    Nāccharāsaṅghātamattam = na accharāsaṅghātamattaṃ
    Cittassūpasam’         = cittassa upasamaṃ
    Kāmarāgen’             = kāmarāgena
    Sāsanan                = sāsanaṃ
    Ti                     = iti

Esto es mejor evidencia que el corte por espacios de
`extraer_junturas_separadas.py`, y en dos sentidos:

  · **la resolución está DICHA**, no inferida de un espacio ni de una final
    consonántica: no hay heurística que pueda equivocarse;
  · **da los componentes SUBYACENTES** —cittassa + upasamaṃ— y no sólo el
    corte de superficie. Eso es exactamente lo que un caso necesita y lo que
    al corpus de junturas le faltaba.

Hay dos clases de ecuación y conviene no mezclarlas:

  · **juntura** —dos o más voces a la derecha: «na accharāsaṅghātamattaṃ»—,
    que es un sandhi de los que este proyecto persigue;
  · **ortográfica** —una sola voz: «sāsanan = sāsanaṃ», «ti = iti»—, que no
    une dos palabras sino que devuelve la forma plena de una. Sirve igual,
    pero no es lo mismo y se cuenta aparte.

## Cómo se verifica, y por qué NO se verifica como el otro extractor

La primera versión exigía que la forma de la IZQUIERDA estuviera atestiguada
en la edición, como hace `extraer_junturas_separadas.py`. **Descartaba
todo**, y con razón: «Nāccharāsaṅghātamattam» acaba en «m» porque va seguida
de «pi», y en la edición existe unida a ella, no suelta. La izquierda de una
ecuación es un fragmento a media operación, no una forma del canon.

Lo que sí se puede exigir, y es la prueba correcta:

  · **cada voz de la DERECHA está atestiguada** en la edición — son palabras
    de verdad, no invenciones;
  · y **el motor recompone**: se pide a `combinar()` que una las voces de la
    derecha y se mira si alguna de sus salidas reproduce la izquierda,
    tolerando la «m» final por «ṃ» —que es justo la operación de §34— y los
    apóstrofos.

Lo que no pasa la primera condición se aparta. Lo que pasa la primera pero
no la segunda **se publica igual, marcado**: significa que la resolución del
Venerable es buena y que el motor no sabe llegar a ella, que es precisamente
la clase de hallazgo que interesa.

NO ADJUDICA NADA. La ecuación es del Venerable y vale como tal, pero
convertirla en caso es adjudicar, y eso lo firma él.

Salida: recursos/corpus-separado/ecuaciones.json
"""

import argparse
import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "nuestro"))

from normalizar import cotejo                                      # noqa: E402
import solucionar_sandhis as S                                     # noqa: E402

FUENTES = os.path.join(RAIZ, "recursos", "corpus-separado")
DESTINO = os.path.join(FUENTES, "ecuaciones.json")

APOSTROFOS = "’'‘ʼ"
# Una línea de ecuación: «forma = voz [voz…]», sin corchetes de análisis por
# medio. El lado izquierdo es una sola palabra pāḷi, con o sin apóstrofo.
LINEA = re.compile(
    r"^\s*([A-Za-zĀāĪīŪūṂṃṄṅÑñṬṭḌḍṆṇḶḷ" + APOSTROFOS + r"-]+)"
    r"\s*=\s*"
    r"([A-Za-zĀāĪīŪūṂṃṄṅÑñṬṭḌḍṆṇḶḷ" + APOSTROFOS + r"\- ]+?)\s*$")


# La entrada de la «Lista de voces» sigue después de la ecuación con el
# análisis morfológico y la traducción:
#
#     Kāmarāgen’ = kāmarāgena, [n., cmp., kāma, sensual, + rāga, pasión, …]
#
# La primera versión de este guion saltaba **toda línea con un corchete**, y
# eso se escribió mirando las MUESTRAS —dos capítulos recortados a mano—,
# donde las ecuaciones venían limpias. En los 23 documentos completos casi
# todas las entradas llevan su gloss: de 233 líneas con «=» el filtro dejaba
# pasar 52, y de las 181 restantes se perdían 9 junturas dichas por el
# Venerable. La ecuación termina donde empieza el gloss, así que se corta ahí
# en vez de tirar la línea entera.
CORTE_GLOSS = re.compile(r"[\[,;]")


def recortar(linea):
    """La ecuación sola: lo que sigue al «=» hasta el gloss."""
    izq, sep, der = linea.partition("=")
    if not sep:
        return linea
    return izq + "=" + CORTE_GLOSS.split(der, 1)[0]


def sin_apostrofos(x):
    for ap in APOSTROFOS:
        x = x.replace(ap, "")
    return x


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ver-fallos", action="store_true")
    a = ap.parse_args()

    S.SOLO_CANON = True
    S.DPD_FILTRO = True
    c = S.cargar()
    frec = c["frecuencia"]

    fuentes = sorted(f for f in os.listdir(FUENTES) if f.endswith(".txt"))
    filas, fallos = [], []
    vistas = set()
    for nombre in fuentes:
        texto = unicodedata.normalize(
            "NFC", open(os.path.join(FUENTES, nombre), encoding="utf-8").read())
        for linea in texto.split("\n"):
            if "=" not in linea:
                continue
            m = LINEA.match(recortar(linea).strip())
            if not m:
                continue
            izq_bruto, der_bruto = m.group(1), m.group(2)
            izq = cotejo(sin_apostrofos(izq_bruto))
            voces = [cotejo(sin_apostrofos(v)) for v in der_bruto.split()]
            if not izq or not voces or izq in vistas:
                continue
            # 1ª condición: las voces de la derecha son palabras de la edición.
            sin_atestiguar = [v for v in voces if not frec.get(v, 0)]
            if sin_atestiguar:
                fallos.append((nombre, izq_bruto, der_bruto,
                               "voz sin atestiguar: " + ", ".join(sin_atestiguar)))
                continue
            vistas.add(izq)
            clase = "juntura" if len(voces) > 1 else "ortográfica"
            # 2ª condición: ¿recompone el motor? Tolerando «m» final por «ṃ»,
            # que es la operación de §34 y la razón de que la izquierda acabe
            # en consonante.
            def tol(x):
                return x[:-1] + "ṃ" if x.endswith("m") else x
            recompone = False
            if len(voces) == 2:
                try:
                    for forma, _l in S.combinar(voces[0], voces[1]):
                        if tol(cotejo(forma)) == tol(izq):
                            recompone = True
                            break
                except Exception:                                  # noqa: BLE001
                    pass
            r = S.solucionar(izq)
            l0 = (r.get("lecturas") or [{}])[0]
            comp = [cotejo(x) for x in (l0.get("componentes") or [])]
            filas.append({
                "forma": izq,
                "frec": frec.get(izq, 0),
                "ecuacion_iebh": voces,
                "clase": clase,
                "fuente": nombre,
                "recompone": recompone,
                "senal": r.get("senal"),
                "componentes_motor": comp,
                "acuerdo": comp == voces,
            })

    filas.sort(key=lambda x: (-x["frec"], x["forma"]))
    json.dump({"ecuaciones": len(filas), "filas": filas},
              open(DESTINO, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    junt = [f for f in filas if f["clase"] == "juntura"]
    orto = [f for f in filas if f["clase"] == "ortográfica"]
    print("textos leídos      :", len(fuentes))
    print("ecuaciones         :", len(filas),
          "· junturas", len(junt), "· ortográficas", len(orto))
    print("descartadas        :", len(fallos))
    if junt:
        ac = sum(1 for f in junt if f["acuerdo"])
        rec = sum(1 for f in junt if f["recompone"])
        mudas = sum(1 for f in junt if not f["senal"])
        print()
        print("SOBRE LAS JUNTURAS")
        print("  el motor RECOMPONE la ecuación     : %d de %d" % (rec, len(junt)))
        print("  el motor da los MISMOS componentes : %d de %d" % (ac, len(junt)))
        print("  el motor no las ve                 : %d" % mudas)
        print()
        print("%-26s %-30s %-6s %-9s %s"
              % ("forma", "ecuación del Venerable", "rec.", "señal", "el motor"))
        for f in junt[:20]:
            print("%-26s %-30s %-6s %-9s %s" % (
                f["forma"], " + ".join(f["ecuacion_iebh"]),
                "sí" if f["recompone"] else "NO", f["senal"] or "—",
                " + ".join(f["componentes_motor"]) or "—"))
    if a.ver_fallos and fallos:
        print()
        print("DESCARTADAS (la izquierda no está atestiguada):")
        for n, i, d, por in fallos[:25]:
            print("   %-30s = %-30s (%s)" % (i, d, por))
        if len(fallos) > 25:
            print("   … y %d más" % (len(fallos) - 25))
    print()
    print("escrito", DESTINO)
    return 0


if __name__ == "__main__":
    sys.exit(main())
