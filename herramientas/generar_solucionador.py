#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la página del solucionador de sandhis (etapa 4 del porte a JS).

    python3 herramientas/generar_solucionador.py

Junta tres cosas:

  nuestro/js/*.js                    EL MOTOR — la única copia que se edita;
                                     probado idéntico al Python por los
                                     arneses de las etapas 1-3
  recursos/sandhi/reglas.json        el banco (con las Tablas y las listas)
  recursos/solucionador/plantilla.html   el maquetado y la interfaz

y escribe site/recursos/solucionador/index.html. Los módulos CommonJS se
envuelven en un mini-require de tres líneas: nada de empaquetadores, la
salida es legible y el diff también.

El léxico fragmentado lo escribe aparte `generar_lexico_solucionador.py`
(site/recursos/solucionador/lexico/); la página lo pide por fetch.

La puerta de la etapa 4 la comprueba `node nuestro/js/arnes_pagina.js`:
evalúa el <script id="motor"> de la página YA GENERADA y exige que sus
secuencias sean byte-idénticas a las del Python en las 266 formas del banco.
"""

import hashlib
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS = os.path.join(RAIZ, "nuestro", "js")
REGLAS = os.path.join(RAIZ, "recursos", "sandhi", "reglas.json")
TABLAS = os.path.join(RAIZ, "recursos", "sandhi",
                      "tablas-nandisena-secuencias.json")
LISTAS = os.path.join(RAIZ, "recursos", "sandhi", "listas-cerradas.json")
CASOS = os.path.join(RAIZ, "recursos", "solucionador",
                     "casos-reportados.json")
BANCO = os.path.join(RAIZ, "banco.sha256")
PLANTILLA = os.path.join(RAIZ, "recursos", "solucionador", "plantilla.html")
DESTINO = os.path.join(RAIZ, "site", "recursos", "solucionador", "index.html")
LEXICO = os.path.join(RAIZ, "site", "recursos", "solucionador", "lexico")

# Los módulos del motor, en orden de dependencia (motor requiere a los tres).
MODULOS = ["normalizar", "operaciones", "derivar", "motor"]

VERSION = "2.0"
FECHA = "2026-08-31"
NOTA = ("EL MOTOR YA NO ES SÓLO KACCĀYANA, y por eso cambia el número entero. "
        "El 2026-08-30 entró en él la primera operación que Kaccāyana no "
        "enuncia: SADDANĪTI SUTTAMĀLĀ §49 —«evassekāre itissaññassa cissa "
        "vo»—, sin la cual «tveva» no ofrecía su lectura citativa. Hasta "
        "entonces la herramienta explicaba el canon con una sola gramática; "
        "desde entonces, con las que hagan falta, y lo dice en cada escalera "
        "que la cita. Lo demás de esa noche va con ello: «tveva» = ti + eva y "
        "«avijjāyatveva» = tu + eva, adjudicados después de RETIRAR una "
        "primera adjudicación que daba por única una voz de dos lecturas; y "
        "con el criterio que lo gobierna, que es del IEBH: hay formas de "
        "sandhi teóricamente plausibles que son inverosímiles en el Tipiṭaka "
        "— recomponer no basta, y atestiguar la pieza no atestigua la "
        "juntura. Del 2026-08-31: enviar a la cola pide identidad verificada, "
        "con dos papeles —revisor y aprendiz—, de modo que cada veredicto "
        "sabe de quién viene y la atribución deja de suponerse. "
        "Antes, en la versión 1.12: LO REGISTRADO A MANO YA SE VE. Una voz "
        "dada de alta por el campo «sandhi no detectado» no aparecía por "
        "ninguna parte, porque la página sólo dibuja tarjeta para lo que el "
        "motor señala y una voz registrada a mano es, por definición, una "
        "sobre la que el motor calla. Ahora llevan su tarjeta, rotulada "
        "aparte y a la vista aunque se analice otro pasaje, con su campo de "
        "nota y de escalera.")

PRELUDIO = """\
/* Mini-require: los módulos de nuestro/js/ tal cual, envueltos. */
const __f = {};
const __m = {};
function __def(n, f){ __f[n] = f; }
function __req(p){
  const n = p.replace(/^\\.\\//, "");
  if(!(n in __m)){
    const module = { exports: {} };
    __m[n] = module.exports;
    __f[n](module, module.exports, __req);
    __m[n] = module.exports;
  }
  return __m[n];
}
"""


def huella():
    h = hashlib.sha256()
    with open(REGLAS, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    calculada = h.hexdigest()
    d = {"reglas.json": calculada, "coincide": None}
    if os.path.exists(BANCO):
        for l in open(BANCO, encoding="utf-8"):
            if l.strip() and not l.startswith("#") and "reglas.json" in l:
                d["guardada"] = l.split("  ")[0]
                d["coincide"] = d["guardada"] == calculada
                break
    return d


def empaquetar():
    partes = [PRELUDIO]
    for nombre in MODULOS:
        src = open(os.path.join(JS, nombre + ".js"), encoding="utf-8").read()
        partes.append('__def("{0}", function(module, exports, require) {{\n'
                      .format(nombre) + src + "\n});\n")
    return "\n".join(partes)


def inyectar(plantilla, marca_ini, marca_fin, contenido):
    m = re.search(re.escape(marca_ini) + r".*?" + re.escape(marca_fin),
                  plantilla, re.S)
    if not m:
        raise SystemExit("La plantilla no tiene el marcador {0}…{1}"
                         .format(marca_ini, marca_fin))
    return plantilla[:m.start()] + contenido + plantilla[m.end():]


def suttas_para_tooltip():
    """Los 51 aforismos para el tooltip de §N — los mismos que muestra
    /recursos/sandhi/, sin los campos pesados (ex, gloss). Se derivan del
    capítulo, vía el extractor de generar_sandhi.py: una sola fuente."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import generar_sandhi as GS
    return [{k: s[k] for k in ("kac", "ru", "sad", "pali", "es", "split")}
            for s in GS.suttas_desde_markdown()]


def main():
    reglas = json.load(open(REGLAS, encoding="utf-8"))
    tablas = json.load(open(TABLAS, encoding="utf-8"))
    listas = json.load(open(LISTAS, encoding="utf-8"))
    datos = {
        "suttas": suttas_para_tooltip(),
        "version": VERSION, "fecha": FECHA, "nota": NOTA,
        "huella": huella(),
        # El motor sólo consulta `reglas.ce`; el resto del archivo no viaja.
        "reglas": {"ce": reglas["ce"]},
        "tablas": tablas,
        "listas": listas,
        # Los casos adjudicados por lectores: cada fallo, un caso permanente.
        "casos": (json.load(open(CASOS, encoding="utf-8"))
                  if os.path.exists(CASOS) else {"casos": []}),
    }

    plantilla = open(PLANTILLA, encoding="utf-8").read()
    html = inyectar(plantilla, "/*__DATOS__*/", "/*__FIN__*/",
                    json.dumps(datos, ensure_ascii=False,
                               separators=(",", ":")))
    html = inyectar(html, "/*__MOTOR__*/", "/*__FIN_MOTOR__*/", empaquetar())

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    open(DESTINO, "w", encoding="utf-8").write(html)

    avisos = []
    if not os.path.exists(os.path.join(LEXICO, "indice.json")):
        avisos.append("falta el léxico fragmentado: "
                      "python3 herramientas/generar_lexico_solucionador.py")
    print("{0} formas del banco · {1} filas de Tablas · motor {2} módulos → {3}"
          .format(len(reglas["ce"]), len(tablas["filas"]), len(MODULOS),
                  os.path.relpath(DESTINO, RAIZ)))
    for a in avisos:
        print("  aviso — " + a)
    return 1 if avisos else 0


if __name__ == "__main__":
    sys.exit(main())
