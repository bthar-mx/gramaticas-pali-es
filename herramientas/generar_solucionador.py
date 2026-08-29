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

VERSION = "1.5"
FECHA = "2026-08-28"
NOTA = ("Nuevo MODO REVISIÓN (✎): quien sabe de sandhi marca veredictos "
        "sobre cada voz señalada —la primera lectura es correcta, no es "
        "sandhi, u otra lectura—, registra los sandhis que la señal NO "
        "detectó (voz = voz + voz) y exporta todo en el formato de los "
        "lotes de adjudicación; nada se adjudica sin firma. Con señal segura se "
        "muestra sólo la lectura afirmada, sin «candidatos» ni las demás "
        "lecturas. "
        "Reglas firmadas por el IEBH sobre pasajes reales de Vedanā: los "
        "absolutivos en -tvā y -tvāna (indeclinables) nunca se señalan como "
        "sandhi; casos phusitva, passanto y cetā = ca + etā; con señal "
        "segura ya no se muestra «candidatos». Y tras el informe de familias: el "
        "RESGUARDO DE LA BASE RESIDUAL —una base candidata debe ser al "
        "menos tan frecuente que la forma entera; corrige el defecto por "
        "el que «ho» (4 apariciones) concedía la unicidad y el patrón "
        "afirmaba hoti (59.320) como ho + iti, y con él pajānāti, "
        "bhaṇati, vadati…— y el patrón de «ca» (sandhi de niggahīta, "
        "§31): tañca = taṃ + ca, evañca, yañca, kathañca… Con ambos, lo "
        "«seguro» acierta juntura real en 9 de cada 10 casos en los dos "
        "corpus de medida. Antes, en la versión 1.4: "
        "tres casos adjudicados por el IEBH sobre el verso «Samāhito "
        "sampajāno» (Vedanā): pajānāti NO es sandhi (verbo, kiyādi-gaṇa) — "
        "el patrón de «iti» lo afirmaba por una base residual de 1 "
        "aparición, defecto medido que espera regla firmada—; vedanānañca "
        "= vedanānaṃ + ca y maggañca = maggaṃ + ca (sandhi de niggahīta, "
        "§31), que la señal daba como «posible» sin atreverse a afirmar. "
        "El ejemplo de la portada es ahora el de la referencia de sandhi "
        "(yassindriyāni) y hay botón Limpiar. Antes, en la versión 1.3: "
        "la regla de la clase vocálica, adjudicada por el IEBH: «hotīti es "
        "sólo hoti + iti y hotūti es sólo hotu + iti» — la vocal que "
        "sobrevive ante «ti» conserva la clase de la vocal final de la "
        "base, y las bases de otra clase quedan excluidas de la "
        "afirmación. Con ella, toda la familia de colas de «iti» se "
        "afirma sola: hotīti, vuccatīti, bhavissatīti… Antes, en la "
        "versión 1.2: los patrones adjudicados de las enclíticas: cuando una voz termina "
        "en la cola de «iti» o de «pi» y entre las lecturas verificadas hay "
        "una sola primera voz atestiguada en el canon, esa lectura se afirma "
        "con su fuente — abhisambuddho + iti, ye + api—; con varias bases "
        "atestiguadas (ceva: ca, ce y cā) la duda se declara. Una "
        "adjudicación de no-sandhi apaga la señal (caso «navo»). Antes, en "
        "la versión 1.1: el Digital Pāḷi Dictionary entra como testigo "
        "silencioso de ocurrencia (decisión del IEBH, 2026-08-28): amplía el filtro de "
        "cortes, ordena candidatos y aviva la señal, nunca decide el "
        "análisis. Con el testigo, el motor reencuentra el análisis firmado "
        "en 221 de las 251 formas medibles del banco (88 %) y el corte "
        "coincide con la partición independiente en el 90,7 % de los versos "
        "y el 92,5 % de la prosa; la señal marca entre el 46 % y el 56 % de "
        "los sandhis presentes. La caja afirma una sola lectura por sandhi "
        "cuando hay autoridad detrás —banco firmado o adjudicación con "
        "fuente— y declara la ignorancia cuando no la hay. Antes, en la "
        "versión 1.0: primera versión pública, 218/251, 78,9 % y 84,3 %, "
        "señal del 32-46 %; motor JavaScript comprobado secuencia por "
        "secuencia contra la referencia en Python.")

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


def main():
    reglas = json.load(open(REGLAS, encoding="utf-8"))
    tablas = json.load(open(TABLAS, encoding="utf-8"))
    listas = json.load(open(LISTAS, encoding="utf-8"))
    datos = {
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
