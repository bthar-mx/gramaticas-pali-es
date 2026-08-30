#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
El ciclo completo de los veredictos, en UNA orden — la independencia de
quien firma (pedido del IEBH, 2026-08-29: «Can I do that independently?»).

    VEREDICTOS_CLAVE=… python3 herramientas/ciclo_veredictos.py
    VEREDICTOS_CLAVE=… python3 herramientas/ciclo_veredictos.py --sin-push

Hace, en orden, y SE DETIENE ante el primer fallo:

  1. traer_veredictos.py — recoge la cola, archiva cada lote en
     veredictos-recibidos/, incorpora los casos y vacía lo incorporado.
  2. Si algún caso nuevo toca los corpus de referencia, re-vierte las
     referencias que correspondan (la de señal usa una caché persistente
     en ~/.cache/, así que sólo la primera corrida es lenta).
  3. generar_solucionador.py — la página nueva.
  4. Los CINCO arneses. Si uno falla, NO hay commit: el árbol queda tal
     cual para diagnosticar, y no se publica nada.
  5. git commit con un mensaje estándar que lista los casos, y git push
     (que despliega), salvo --sin-push.

La puerta NO cambia: correr este guion ES la firma de quien lo corre —
por eso pide la clave, que sólo quien firma conoce—. Las observaciones
de los lotes siguen sin volverse casos: quedan en los archivos
recibidos, para leerse.
"""

import argparse
import datetime
import json
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASOS = os.path.join(RAIZ, "recursos", "solucionador", "casos-reportados.json")
JS = os.path.join(RAIZ, "nuestro", "js")
ARNESES = ["arnes", "arnes_corpus", "arnes_deteccion", "arnes_pagina",
           "arnes_casos"]
CACHE_SENAL = os.path.expanduser("~/.cache/gramaticas-pali-senal.json")

sys.path.insert(0, os.path.join(RAIZ, "nuestro"))
from normalizar import cotejo                                      # noqa: E402


def correr(descripcion, cmd, env=None):
    print("\n── {0}".format(descripcion))
    e = dict(os.environ)
    if env:
        e.update(env)
    r = subprocess.run(cmd, cwd=RAIZ, env=e)
    if r.returncode != 0:
        print("\nFALLÓ: {0} (código {1}). Nada se publicó; el árbol queda "
              "tal cual para diagnosticar.".format(" ".join(cmd),
                                                   r.returncode))
        sys.exit(r.returncode)


def formas_de_casos():
    d = json.load(open(CASOS, encoding="utf-8"))
    return {cotejo(c["forma"]) for c in d.get("casos", [])}


def formas_de_referencia(nombre, campo):
    ruta = os.path.join(JS, nombre)
    if not os.path.exists(ruta):
        return set()
    d = json.load(open(ruta, encoding="utf-8"))
    return {cotejo(x.get(campo, "")) for x in d.get("filas", [])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sin-push", action="store_true",
                    help="deja el commit hecho pero no lo empuja")
    a = ap.parse_args()
    if not os.environ.get("VEREDICTOS_CLAVE"):
        print("Falta VEREDICTOS_CLAVE en el entorno.")
        return 2

    # árbol limpio: un ciclo no debe mezclarse con trabajo a medias
    sucio = subprocess.run(["git", "status", "--porcelain"], cwd=RAIZ,
                           capture_output=True, text=True).stdout.strip()
    if sucio:
        print("El árbol tiene cambios sin commit; el ciclo no se mezcla "
              "con trabajo a medias:\n" + sucio)
        return 2

    antes = formas_de_casos()

    # 1 · recoger e incorporar
    correr("La cola: recoger, archivar, incorporar, vaciar",
           [sys.executable, "herramientas/traer_veredictos.py"])

    nuevas = formas_de_casos() - antes
    if not nuevas:
        print("\nSin casos nuevos: nada que regenerar ni publicar.")
        return 0
    print("\ncasos nuevos:", ", ".join(sorted(nuevas)))

    # 2 · referencias, sólo las que los casos nuevos tocan
    en_senal = nuevas & formas_de_referencia(
        "referencia-senal-solo-canon.json", "forma")
    if en_senal:
        print("   tocan la referencia de señal:", ", ".join(sorted(en_senal)))
        # Aquí se borraban a mano de la caché las formas recién adjudicadas.
        # No bastaba: sólo cubría los casos que ENTRABAN POR ESTE CICLO, y un
        # caso añadido por otro camino —a mano, o desde el chat— dejaba su
        # entrada rancia. Eso fue exactamente lo que pasó el 2026-08-29 con
        # «netaṃ» y «svāyaṃ»: la referencia salió diciendo «sin señal» de
        # dos formas que el motor ya daba por adjudicadas, arnes_deteccion
        # falló, y el ciclo se detuvo sin publicar DOCE veredictos que ya
        # estaban incorporados en el árbol. Desde entonces la invalidación
        # vive en volcar_referencia_senal.py y es por HUELLA del contenido de
        # casos-reportados.json y reglas.json: cambie quien cambie los casos,
        # la caché se descarta sola.
        os.makedirs(os.path.dirname(CACHE_SENAL), exist_ok=True)
        correr("Re-vertir la referencia de señal (con caché persistente; "
               "la primera corrida es lenta)",
               [sys.executable, "nuestro/volcar_referencia_senal.py",
                "--dpd-filtro"], env={"SENAL_CACHE": CACHE_SENAL})
    en_corpus = (nuevas & (formas_de_referencia(
        "referencia-corpus-versos-solo-canon.json", "forma")
        | formas_de_referencia(
        "referencia-corpus-comentario-solo-canon.json", "forma")))
    if en_corpus:
        print("   tocan los corpus de referencia:",
              ", ".join(sorted(en_corpus)))
        correr("Re-vertir la referencia del corpus (verso)",
               [sys.executable, "nuestro/volcar_referencia_corpus.py",
                "--solo-canon", "--dpd-filtro"])
        correr("Re-vertir la referencia del corpus (prosa)",
               [sys.executable, "nuestro/volcar_referencia_corpus.py",
                "--solo-canon", "--dpd-filtro", "--comentario"])

    # 3 · la página
    correr("La página nueva", [sys.executable,
                               "herramientas/generar_solucionador.py"])

    # 4 · los cinco arneses — la puerta que no se salta
    for arnes in ARNESES:
        correr("Arnés: " + arnes, ["node", "nuestro/js/{0}.js".format(arnes)])

    # 5 · commit y push
    hoy = datetime.date.today().isoformat()
    lista = ", ".join(sorted(nuevas))
    msg = ("Casos de la cola del {0}: {1}\n\n"
           "Incorporados por herramientas/ciclo_veredictos.py — recogidos "
           "de la cola, archivados en veredictos-recibidos/, incorporados, "
           "referencias re-vertidas donde tocaba, página regenerada y los "
           "cinco arneses en verde. La firma es de quien corrió el ciclo "
           "con la clave.").format(hoy, lista)
    correr("Commit", ["git", "add", "-A"])
    correr("Commit", ["git", "commit", "-m", msg])
    if a.sin_push:
        print("\nListo, SIN push (--sin-push): recuerde empujar para "
              "desplegar.")
    else:
        correr("Push (despliega)", ["git", "push"])
        print("\nListo: incorporado, verificado, publicado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
