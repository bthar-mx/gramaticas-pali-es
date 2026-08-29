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
import subprocess
import sys
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clave", default=os.environ.get("VEREDICTOS_CLAVE", ""))
    ap.add_argument("--solo-mirar", action="store_true",
                    help="lista la cola sin guardar, incorporar ni borrar")
    ap.add_argument("--api", default=API)
    a = ap.parse_args()
    if not a.clave:
        print("Falta la clave: --clave o VEREDICTOS_CLAVE en el entorno.")
        return 2

    q = "?clave=" + urllib.parse.quote(a.clave)
    d = pedir(a.api + q)
    cola = d.get("veredictos", [])
    print("{0} entrada{1} en la cola".format(len(cola), "" if len(cola) == 1 else "s"))
    if not cola:
        return 0
    if a.solo_mirar:
        for e in cola:
            md = e.get("md") or ""
            n = md.count("VEREDICTO:")
            print("  · {0} — {1} veredicto{2}".format(
                e["id"], n, "" if n == 1 else "s"))
        return 0

    os.makedirs(DESTINO, exist_ok=True)
    fuente = "IEBH, {0} · revisión en la página".format(
        datetime.date.today().isoformat())
    incorporados = []
    for e in cola:
        ruta = os.path.join(DESTINO, e["id"] + ".md")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(e.get("md") or "")
        print("\n== {0} → {1}".format(e["id"], os.path.relpath(ruta, RAIZ)))
        r = subprocess.run([sys.executable, INCORPORADOR, ruta,
                            "--fuente", fuente])
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
