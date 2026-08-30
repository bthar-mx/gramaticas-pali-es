#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Las junturas que el IEBH ya separó: corpus de segmentación verificado.

    python3 herramientas/extraer_junturas_separadas.py
    python3 herramientas/extraer_junturas_separadas.py --ver-fallos

Los textos bilingües del IEBH (Bhikkhu Nandisena) imprimen el pāḷi con las
junturas de sandhi ABIERTAS —«Evam eva kho», «yad idaṃ», «Puna c’ aparaṃ»,
«sato ’va»— mientras que la edición del Sexto Concilio las imprime unidas
—evameva, yadidaṃ, caparaṃ, satova—. Cada espacio así es, por tanto, **una
juntura etiquetada a mano por el Venerable**, que es exactamente el dato que
al proyecto le faltaba: dónde corta una forma. CLAUDE.md lo dice sin rodeos —
«el cuello de botella es la segmentación, no las reglas».

## Cómo se distingue una juntura de un espacio corriente

El documento usa el MISMO espacio para separar palabras normales y para
abrir un sandhi, así que el espacio solo no sirve. Dos señales lo resuelven:

1. **El apóstrofo** —«pan’ assa», «c’ aparaṃ», «sato ’va»— marca vocal
   elidida y es inequívoco.
2. **La forma acabada en consonante.** En pāḷi una palabra termina en vocal
   o en «ṃ»; una que acaba en «m», «d», «ñ», «n», «t» está a media
   operación: evam, yad, kathañ, imam, tam, tañ, yāvad, ayam, muttan. Ésa
   es la primera voz de una juntura abierta.

## Y cómo se verifica, que es lo que lo hace utilizable

Unir es literal: se quitan el espacio y el apóstrofo. Una candidata sólo se
publica si **la forma unida está atestiguada en la edición** (aparece en el
recuento de frecuencias del canon). Lo que no está atestiguado no se
inventa: se aparta y se cuenta como fallo, para mirarlo.

Cada fila del corpus dice: la forma de la edición, el corte del IEBH, si el
motor la resuelve hoy y con qué componentes. Eso permite tres cosas que
antes no se podían hacer:

  · **medir el recall sobre texto corrido** y no sobre un banco;
  · **cotejar** el corte del Venerable con el que deriva el motor;
  · alimentar el futuro solucionador, cuyo problema es justamente segmentar.

NO adjudica nada. El corte es suyo; los componentes subyacentes los propone
el motor, y donde discrepen es pregunta para él, no dato que importar.

Salida: recursos/corpus-separado/junturas.json + un resumen por pantalla.
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
DESTINO = os.path.join(FUENTES, "junturas.json")

# Una palabra pāḷi acaba en vocal o en niggahīta. Cualquier otra final deja
# la voz a media operación, y eso es la marca de una juntura abierta.
FINAL_DE_PALABRA = set("aāiīuūeoṃ")
APOSTROFOS = "’'‘ʼ"


def limpiar(t):
    """Fuera lo que no es texto pāḷi: números de párrafo, de página, la
    marca de repetición «-pa-», las llamadas de nota y la puntuación."""
    t = unicodedata.normalize("NFC", t)
    t = re.sub(r"\[\d+\]", " ", t)          # [232], y las llamadas de nota
    t = re.sub(r"\b-pa-\b", " ", t)         # la abreviatura de repetición
    t = re.sub(r"^\s*\d+\.\s*", " ", t)     # 373.
    t = t.replace("“", " ").replace("”", " ").replace("«", " ").replace("»", " ")
    t = re.sub(r"[,;.?!]", " ", t)
    return t


def es_pali(linea):
    """Las líneas españolas del bilingüe se descartan: llevan palabras que
    el pāḷi no tiene. Basta con un puñado muy frecuente."""
    l = " " + linea.lower() + " "
    for w in (" el ", " la ", " los ", " las ", " que ", " de ", " en ",
              " un ", " una ", " como ", " para ", " por ", " con ",
              " cuerpo ", " bhikkhus, "):
        if w in l:
            return False
    return bool(re.search(r"[āīūṃṅñṭḍṇḷ]", linea))


def junturas_de(texto):
    """Los pares (a, b) que el documento deja abiertos, en orden.

    OJO CON EL APÓSTROFO, que costó la primera corrida: «pan’ assa» ya ES la
    forma de la edición una vez quitado el apóstrofo —panassa—, y NO hay que
    pegarle la palabra siguiente. La primera versión hacía justo eso y salían
    engendros como «caparaṃbhikkhave». El apóstrofo cierra la juntura; el
    espacio sin apóstrofo, tras final consonántica, la abre."""
    fuera = []
    # La cabecera del archivo no es texto: empieza tras la raya.
    if "\n---\n" in texto:
        texto = texto.split("\n---\n", 1)[1]
    for linea in texto.split("\n"):
        if not es_pali(linea):
            continue
        t = limpiar(linea)
        # El apóstrofo suelto se pega a su vecino: «pan’ assa» → «pan’assa»,
        # «sato ’va» → «sato’va».
        for ap in APOSTROFOS:
            t = t.replace(ap + " ", ap).replace(" " + ap, ap)
        piezas = t.split()
        i = 0
        while i < len(piezas):
            a = piezas[i]
            partido = None
            for ap in APOSTROFOS:
                if ap in a:
                    izq, _, der = a.partition(ap)
                    if izq and der:
                        partido = (izq, der, "apóstrofo")
                    break
            if partido:
                fuera.append(partido)
                i += 1
                continue
            if (i + 1 < len(piezas) and a
                    and a[-1] not in FINAL_DE_PALABRA and a[-1].isalpha()):
                fuera.append((a, piezas[i + 1], "final consonántica"))
                i += 2
                continue
            i += 1
    return fuera


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ver-fallos", action="store_true",
                    help="lista las candidatas cuya forma unida no está "
                         "atestiguada en la edición")
    a = ap.parse_args()

    S.SOLO_CANON = True
    S.DPD_FILTRO = True
    c = S.cargar()
    frec = c["frecuencia"]

    fuentes = sorted(f for f in os.listdir(FUENTES)
                     if f.endswith(".txt")) if os.path.isdir(FUENTES) else []
    if not fuentes:
        print("No hay textos en", FUENTES)
        return 2

    filas, fallos = [], []
    vistas = set()
    for nombre in fuentes:
        texto = open(os.path.join(FUENTES, nombre), encoding="utf-8").read()
        for a_, b_, marca in junturas_de(texto):
            unida = cotejo(a_ + b_)
            n = frec.get(unida, 0)
            if not n:
                fallos.append((nombre, a_, b_, unida, marca))
                continue
            if unida in vistas:
                continue
            vistas.add(unida)
            r = S.solucionar(unida)
            l0 = (r.get("lecturas") or [{}])[0]
            comp = [cotejo(x) for x in (l0.get("componentes") or [])]
            # ¿El motor corta donde corta el Venerable? Su corte es de
            # superficie (evam | eva); el del motor, subyacente (evaṃ + eva).
            # Coinciden cuando la segunda voz es la misma.
            acuerdo = bool(comp) and len(comp) == 2 and comp[1] == cotejo(b_)
            filas.append({
                "forma": unida,
                "frec": n,
                "corte_iebh": [a_, b_],
                "marca": marca,
                "fuente": nombre,
                "senal": r.get("senal"),
                "componentes_motor": comp,
                "acuerdo_segunda_voz": acuerdo,
            })

    filas.sort(key=lambda x: (-x["frec"], x["forma"]))
    json.dump({"junturas": len(filas), "filas": filas},
              open(DESTINO, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    con_senal = [f for f in filas if f["senal"]]
    seguras = [f for f in filas if f["senal"] == "segura"]
    acuerdo = [f for f in filas if f["acuerdo_segunda_voz"]]
    print("textos leídos            :", ", ".join(fuentes))
    print("junturas distintas       :", len(filas))
    print("  atestiguadas y unidas  :", len(filas), "(sólo se publican ésas)")
    print("  descartadas sin atestiguar:", len(fallos))
    print()
    print("QUÉ HACE EL MOTOR HOY CON ELLAS")
    print("  con señal              : %3d  (%4.1f %%)"
          % (len(con_senal), 100.0 * len(con_senal) / max(len(filas), 1)))
    print("     de ellas «segura»   : %3d" % len(seguras))
    # OJO con esta cifra: es una COTA INFERIOR y nada más. El corte del
    # Venerable es de superficie («sato | va») y los componentes del motor
    # son subyacentes («sato + eva»), de modo que muchas coincidencias reales
    # no casan carácter a carácter y aquí cuentan como desacuerdo. Sirve para
    # ordenar la revisión, no para juzgar al motor: eso se hace mirando la
    # tabla, que es corta a propósito.
    print("  la segunda voz casa literalmente        : %3d  (%4.1f %%) "
          "— cota inferior, ver el aviso del código"
          % (len(acuerdo), 100.0 * len(acuerdo) / max(len(filas), 1)))
    print()
    print("LAS QUE EL MOTOR NO VE (recall que falta), por frecuencia:")
    mudas = [f for f in filas if not f["senal"]]
    for f in mudas[:15]:
        print("   %-18s %7s   corte: %s"
              % (f["forma"], format(f["frec"], ",d").replace(",", "."),
                 " | ".join(f["corte_iebh"])))
    if len(mudas) > 15:
        print("   … y %d más" % (len(mudas) - 15))
    if a.ver_fallos and fallos:
        print()
        print("CANDIDATAS SIN ATESTIGUAR (no se publican):")
        for nombre, x, y, u, m in fallos[:30]:
            print("   %-28s de «%s %s» (%s)" % (u, x, y, m))
        if len(fallos) > 30:
            print("   … y %d más" % (len(fallos) - 30))
    print()
    print("escrito", DESTINO)
    return 0


if __name__ == "__main__":
    sys.exit(main())
