#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recoge la cola de veredictos del modo revisión y los incorpora — la
automatización de grado medio (decisión del IEBH, 2026-08-28).

    VEREDICTOS_CLAVE=… python3 herramientas/traer_veredictos.py
    python3 herramientas/traer_veredictos.py --clave …
    python3 herramientas/traer_veredictos.py --solo-mirar    # lista sin tocar

Qué hace, en orden, y qué NO hace:

  1. GET /api/veredictos con la clave → la cola completa.
  2. Guarda cada entrada en docs/solucionador/veredictos-recibidos/,
     que es el registro permanente de lo recibido.
  3. Pasa cada una por herramientas/incorporar_adjudicaciones.py — el
     mismo incorporador de los lotes: veredictos ilegibles se avisan,
     formas ya adjudicadas no se tocan.
  4. Borra de la cola SOLO lo que quedó guardado e incorporado sin error.
  5. NO regenera, NO corre arneses, NO hace commit: eso queda impreso al
     final y lo hace quien firma. La cola acerca los veredictos; la
     puerta sigue siendo el incorporador, los arneses y la firma.

Las OBSERVACIONES y las NOTAS DEL REVISOR no son casos: el incorporador
las ignora a propósito. Quedan en los archivos guardados, para leerse y
convertirse —si quien firma lo decide— en reglas como la de los
absolutivos en -tvā/-tvāna.
"""

import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://gramaticas.buddha-dhamma.net/api/veredictos"
DESTINO = os.path.join(RAIZ, "docs", "solucionador", "veredictos-recibidos")
INCORPORADOR = os.path.join(RAIZ, "herramientas", "incorporar_adjudicaciones.py")


def pedir(url, metodo="GET"):
    # El User-Agent identifica al recolector: el de urllib a secas
    # («Python-urllib/3.9») es de los que el anti-bot del borde de
    # Cloudflare bloquea con un 403 genérico sin llegar al worker.
    req = urllib.request.Request(url, method=metodo, headers={
        "User-Agent": "traer-veredictos/1.0 (gramaticas-pali-es)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        # Decir QUÉ respondió el servidor, no sólo el número: un 403 del
        # worker trae «la clave no coincide»; un 403 del borde de
        # Cloudflare trae una página HTML de bloqueo (2026-08-29).
        cuerpo = ""
        try:
            cuerpo = e.read().decode("utf-8", "replace")[:400]
        except Exception:                                          # noqa: BLE001
            pass
        print("HTTP {0} de {1}".format(e.code, url.split("?")[0]))
        if cuerpo:
            print("respuesta del servidor:\n" + cuerpo)
        if "<html" in cuerpo.lower() or "cloudflare" in cuerpo.lower():
            print("\n(Esto NO es el worker: es el borde de Cloudflare "
                  "bloqueando al cliente. Revisar Security → Bots.)")
        sys.exit(1)


def quien(e):
    """De quién es una entrada, dicho para leerlo de un vistazo."""
    if "correo" not in e:
        return "sin identidad (entrada anterior al 2026-08-31)"
    return e["correo"] if e.get("correo") else "SIN IDENTIDAD (cola abierta)"


def fuente_de(e):
    """La procedencia de una entrada, SIN suponerla.

    Hasta el 2026-08-31 esto rotulaba «IEBH, <fecha>» todo lo que bajara de
    la cola, y la cola era un buzón anónimo: lo que dejara un desconocido
    entraba al proyecto con la firma de quien no lo había escrito. Es el
    principio 4 roto en silencio, que es la peor manera de romperlo.

    Ahora la procedencia sale de lo que se sabe, y cuando no se sabe LO DICE:

      · correo verificado por Access → ese correo, marcado como verificado;
      · «correo: null» → la cola estaba abierta: SIN IDENTIDAD;
      · sin el campo → entrada anterior a este cambio: sin identidad, y de antes.

    Nunca se vuelve a escribir «IEBH» por omisión. Eso lo pone quien firma,
    a mano, con --fuente, si decide que le corresponde.
    """
    hoy = datetime.date.today().isoformat()
    if "correo" not in e:
        return ("cola web, sin identidad, entrada anterior al 2026-08-31, "
                "recogida el {0} · revisión en la página".format(hoy))
    c = e.get("correo")
    if not c:
        return ("cola web, SIN IDENTIDAD VERIFICADA, recogida el {0} "
                "· revisión en la página".format(hoy))
    return ("{0} (identidad verificada por Access), recogida el {1} "
            "· revisión en la página".format(c, hoy))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clave", default=os.environ.get("VEREDICTOS_CLAVE", ""))
    ap.add_argument("--solo-mirar", action="store_true",
                    help="lista la cola sin guardar, incorporar ni borrar")
    ap.add_argument("--ensayo", action="store_true",
                    help="ENSAYO: baja la cola y dice qué pasaría con cada "
                         "veredicto, sin escribir, sin archivar y sin "
                         "vaciar la cola")
    ap.add_argument("--api", default=API)
    ap.add_argument("--fuente", default=None,
                    help="rotula TODAS las entradas con esta procedencia, en "
                         "vez de deducirla de la identidad verificada. Es un "
                         "acto deliberado de quien firma: por omisión no se "
                         "atribuye nada a nadie")
    a = ap.parse_args()
    if not a.clave:
        print("Falta la clave: --clave o VEREDICTOS_CLAVE en el entorno.")
        return 2

    q = "?clave=" + urllib.parse.quote(a.clave)
    # «--solo-mirar» sólo necesita el id y la cuenta, y desde el 2026-08-30 el
    # worker los da con list() a secas: ni un .md viaja por la red. Antes se
    # descargaba la cola ENTERA para contar apariciones de «VEREDICTO:», que
    # es lo que hacía lenta una orden que no toca nada.
    d = pedir(a.api + q + ("&resumen=1" if a.solo_mirar else ""))
    cola = d.get("veredictos", [])
    print("{0} entrada{1} en la cola".format(len(cola), "" if len(cola) == 1 else "s"))
    if not cola:
        return 0
    if a.solo_mirar:
        for e in cola:
            # El worker viejo no conoce «resumen»: si no vino la cuenta, se
            # saca del .md como siempre. Así la orden funciona contra un
            # despliegue anterior a este cambio.
            n = e.get("n")
            if n is None:
                n = (e.get("md") or "").count("VEREDICTO:")
            print("  · {0} — {1} veredicto{2} — {3}".format(
                e["id"], n, "" if n == 1 else "s", quien(e)))
        return 0


    # ENSAYO: se baja la cola de verdad, pero cada lote va a un archivo
    # temporal y el incorporador corre con «--sin-tocar». No se archiva en
    # veredictos-recibidos/, no se escriben casos y NO se borra nada de la
    # cola. Sirve para ver qué va a pasar antes de gastar la corrida buena:
    # la cola se vacía al incorporar y el archivo no se vuelve a leer, de
    # modo que un veredicto mal emitido se gasta sin remedio. Con esto se ve
    # primero.
    if a.ensayo:
        print("\nENSAYO: no se archiva, no se incorpora, la cola NO se "
              "vacía.")
        tmp = tempfile.mkdtemp(prefix="ensayo-veredictos-")
        try:
            for e in cola:
                ruta = os.path.join(tmp, e["id"] + ".md")
                with open(ruta, "w", encoding="utf-8") as f:
                    f.write(e.get("md") or "")
                print("\n== {0}".format(e["id"]))
                subprocess.run([sys.executable, INCORPORADOR, ruta,
                                "--fuente", a.fuente or fuente_de(e),
                                "--sin-tocar"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        print("\nEnsayo terminado. La cola queda intacta; para incorporar "
              "de verdad, córrase sin «--ensayo».")
        return 0

    os.makedirs(DESTINO, exist_ok=True)
    incorporados = []
    for e in cola:
        ruta = os.path.join(DESTINO, e["id"] + ".md")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(e.get("md") or "")
        print("\n== {0} → {1}".format(e["id"], os.path.relpath(ruta, RAIZ)))
        r = subprocess.run([sys.executable, INCORPORADOR, ruta,
                            "--fuente", a.fuente or fuente_de(e)])
        if r.returncode == 0:
            incorporados.append(e["id"])
        else:
            print("  el incorporador devolvió {0}: la entrada QUEDA en la "
                  "cola".format(r.returncode))

    for id_ in incorporados:
        pedir(a.api + q + "&id=" + urllib.parse.quote(id_), metodo="DELETE")
    print("\n{0} incorporada{1} y retirada{1} de la cola.".format(
        len(incorporados), "" if len(incorporados) == 1 else "s"))
    if incorporados:
        print("\nAhora, lo de siempre — la puerta no se salta:"
              "\n    python3 herramientas/generar_solucionador.py"
              "\n    node nuestro/js/arnes_casos.js"
              "\n    (y las referencias/arneses que toquen, si la señal cambió)"
              "\n    git add -A && git commit && git push")
    return 0


if __name__ == "__main__":
    sys.exit(main())
