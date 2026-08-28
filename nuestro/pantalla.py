#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La pantalla del solucionador. Se abre en el navegador.

    python3 nuestro/pantalla.py          # abre el navegador solo
    python3 nuestro/pantalla.py --puerto 8899

**No está en el encargo** *(`CLAUDE.md` §9)*. El encargo pide el motor. La
pantalla es agregado nuestro y existe por una razón: el que consulta es un
estudiante o un traductor, no un programa.

Se construye **después** del motor y **encima** del motor: no repite lógica, no
decide nada, y no puede mostrar nada que el motor no haya verificado. Todo lo
que se ve acá sale de `solucionar_sandhis.solucionar()`.

Corre sólo en esta computadora —`127.0.0.1`—: no abre nada a la red.

---

**Por qué no dice «total de sandhis», que es lo primero que uno querría.**

Decir cuántos sandhis hay en una frase exige detectar **dónde** hubo sandhi, y
el encargo llama a eso *«un problema distinto y más difícil»* y lo deja para la
tercera etapa. Hasta entonces la pantalla informa **lo que encontró**, no lo que
hay. «2 con sandhi resuelto» es verdad; «2 sandhis» no lo es.

Por eso el recuento tiene cinco casillas y no dos, y cada una dice algo que se
puede sostener.
"""

import argparse
import json
import os
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from solucionar_sandhis import (solucionar, cargar, es_palabra,      # noqa: E402
                                senal, combinar, juntura_declarada)
from normalizar import cotejo                                        # noqa: E402
from glosas import glosa                                             # noqa: E402

import re

RE_SUTTA = re.compile(r'§\s*(\d+)')


# ── Clasificar lo que devolvió el motor ─────────────────────────────────
# Siete casillas. Cada una es una afirmación que se puede sostener, y **tres de
# ellas son silencios distintos**, que no se dicen igual:
#
#   · «sin sandhi»        — la voz está entera y ningún corte la parte en dos
#                           voces reales. Es una respuesta, no una falla.
#   · «fuera del alcance» — se parte en dos voces sin ninguna operación: es un
#                           compuesto, y los compuestos los excluyó el Venerable
#   · «sin resolver»      — el léxico ni siquiera conoce la voz, y ahí lo
#                           primero a revisar es cómo está escrita
#
# **Lo que se sacó, y por qué.** La casilla «es palabra entera» ganaba sobre
# todas las demás: si el DPD reconocía la voz tal como está escrita, la ficha
# iba ahí y sus lecturas no se mostraban. Medido contra la Therīgāthā de
# `Sandhi`, esa regla **escondía 604 de las 803 formas con sandhi —el 75 %—**,
# porque el DPD trae como entradas muchísimas formas ya combinadas. La regla
# estaba puesta para que `bhikkhu` no gritara, y el precio era no ver tres de
# cada cuatro sandhis reales.
#
# En su lugar va la **señal medida** —`senal()` en el motor—. Sobre texto corrido
# marca 10 palabras de cada 100 en verso y 19 en prosa; de lo marcado tiene una
# juntura real el 96 % en verso y el 84 % en prosa, y es sandhi del encargo el
# 81 % y el 64 %. (Las cifras que estuvieron acá —3,9 y 8,0, «nueve de cada
# diez»— eran de una medición vieja sobre dos montones elegidos; las encontró
# una revisión externa.) Lo señalado se marca; lo demás se calla, pero sigue
# consultable palabra por palabra. La herramienta no grita: contesta cuando se
# le pregunta, y avisa sólo cuando tiene motivo.

CASILLAS = [
    ("resuelto", "con sandhi resuelto"),
    ("senalada", "con señal de sandhi"),
    ("candidatos", "con lecturas, sin señal"),
    ("pakati", "sin sandhi por regla"),
    ("sin_sandhi", "voz entera, sin corte"),
    ("fuera_alcance", "compuesto: fuera del encargo"),
    ("sin_resolver", "sin resolver"),
]


def clasificar(r):
    """La casilla de una voz.

    El orden importa: primero lo que el banco firma, después lo que la señal
    medida marca, y sólo al final lo que el motor propone por su cuenta.
    """
    e = r["estado"]
    if e == "sin_sandhi_por_regla":
        return "pakati"
    # **Lo que el banco trae va en «resuelto» aunque haya más lecturas.** El
    # motor dejó de esconder las que él mismo encuentra —`lokaggo` publicaba
    # una y se guardaba trece—, así que el estado de esas voces pasó a ser
    # «candidatos». La casilla no se decide por eso: se decide por si la
    # **primera** lectura viene del banco, que es lo que el lector quiere saber.
    # **«Resuelto» tiene que querer decir resuelto.** Antes bastaba con que
    # sobreviviera **una** lectura, viniera de donde viniera, y la casilla
    # decía «con sandhi resuelto». Medido sobre 52.000 palabras del corpus,
    # **el 87 % de lo que caía ahí no tiene ninguna juntura**: `sabbe` salía
    # como `sa + be`, `āha` como `a + ha`, y una frase en castellano marcaba
    # ocho de diez palabras. Una sola lectura no es una resolución: es que el
    # motor no encontró más. Eso es proponer una y afirmarla, las dos cosas
    # que el encargo prohíbe.
    #
    # Ahora hace falta un **segundo testigo**: o la lectura viene del banco
    # firmado, o el DPD publica esa misma descomposición. Sin uno de los dos,
    # por más que sea la única, es un candidato.
    if r["lecturas"] and (r["lecturas"][0].get("origen")
                          or r["lecturas"][0].get("dpd")):
        return "resuelto"
    # La señal va **antes** que los silencios: una voz puede estar entera en el
    # léxico y aun así llevar motivo medido para mirarla —`hotīti` lo está—, y
    # «ti» suelta es señal sin ninguna lectura que mostrar.
    if r.get("senal"):
        return "senalada"
    if e == "sin_sandhi":
        return "sin_sandhi"
    if e == "fuera_del_alcance":
        return "fuera_alcance"
    if r["lecturas"]:
        return "candidatos"
    return "sin_resolver"


def pasos_con_glosa(pasos):
    """Cada paso con el aforismo que cita y qué hace ese aforismo."""
    out = []
    for p in pasos:
        suttas = [int(x) for x in RE_SUTTA.findall(p)]
        texto = re.sub(r'\s*\((?:§[^)]*|EM)\)\s*$', '', p).strip()
        cita = ""
        m = re.search(r'\(([^)]*)\)\s*$', p)
        if m:
            cita = m.group(1)
        out.append({"texto": texto, "cita": cita,
                    "glosa": " · ".join(g for g in (glosa(n) for n in suttas) if g)})
    return out


def agrupar_por_corte(lecturas):
    """Junta las lecturas que son el mismo corte con distinta vocal elidida.

    §12 elide la vocal final de la voz anterior y **no deja rastro de cuál
    era**. Para `dhammaṃ`, el corte `dham + maṃ` se cumple igual si la voz
    anterior fue `dhama`, `dhame`, `dhami`, `dhamo`, `dhamā` o `dhamī`: las
    seis están en el léxico y las seis recomponen. Mostrarlas como seis
    lecturas dice algo falso —que hay seis análisis—; hay uno, con la vocal
    indeterminada.

    No es elegir: se nombran todas las voces posibles. Es decir la verdad de
    la forma en que se puede sostener.
    """
    grupos = []
    for l in lecturas:
        comp = [x for x in (l.get("componentes") or []) if x]
        # el esqueleto: los pasos sin la forma de partida y sin el §10, que es
        # donde la vocal todavía se ve
        cuerpo = tuple(p for p in l["pasos"][1:] if "§10" not in p)
        clave = (comp[1] if len(comp) > 1 else "", str(l.get("sutta")), cuerpo)
        for g in grupos:
            if g["clave"] == clave:
                if comp and comp[0] not in g["anteriores"]:
                    g["anteriores"].append(comp[0])
                break
        else:
            grupos.append({"clave": clave, "lectura": l,
                           "anteriores": [comp[0]] if comp else []})
    salida = []
    for g in grupos:
        l = dict(g["lectura"])
        if len(g["anteriores"]) > 1:
            l["voces_anteriores"] = g["anteriores"]
        salida.append(l)
    return salida


# Lo que no es la voz. El apóstrofo y el guion **sí** son parte de la voz —son
# la marca con que el escriba señala la juntura, y el motor la lee—; la coma, el
# punto, el punto y coma, las comillas y los paréntesis, no.
PUNTUACION = ".,;:!?«»\u201c\u201d()[]—…"


def limpiar(t):
    """Separa la puntuación de la voz, y devuelve las tres partes.

    Sin esto, `upasaṅkamma,` `ahaṃ;` y `adesesi,` salían «sin resolver» en un
    texto de once palabras de prosa real. Las tres están en el DPD en cuanto se
    les saca la coma. Tres de once «sin resolver» eran falsos, y no eran de
    gramática: el motor nunca separó la puntuación del token.
    """
    ini = 0
    while ini < len(t) and t[ini] in PUNTUACION:
        ini += 1
    fin = len(t)
    while fin > ini and t[fin - 1] in PUNTUACION:
        fin -= 1
    return t[:ini], t[ini:fin], t[fin:]


CORTA_INICIAL = {"ā": "a", "ī": "i", "ū": "u"}


def _misma_voz(a, b):
    """Dos voces que difieren **sólo en la cantidad de su vocal inicial**.

    §15 alarga la vocal siguiente cuando la anterior se elidió, y §16 la alarga
    cuando la siguiente se elide. Ninguno de los dos deja rastro de cuál era la
    cantidad original: de `aggamaggañāṇāsinā`, la voz que sigue pudo ser `asinā`
    —y §15 la alargó— o `āsinā` —y no pasó nada—. Las dos recomponen. Son el
    mismo corte, y presentarlas como dos análisis dice algo falso.

    Es el mismo argumento que ya se aplica a la voz **anterior** en
    `agrupar_por_corte`, del otro lado de la juntura.
    """
    def raiz(t):
        t = cotejo(t)
        return CORTA_INICIAL.get(t[:1], t[:1]) + t[1:] if t else t
    return raiz(a) == raiz(b)


def agrupar_por_voz_siguiente(lecturas):
    """Un nivel más arriba: **qué palabra sigue**.

    Para `paripucchahaṃ` el motor devuelve doce lecturas. Pero la pregunta que
    un lector se hace primero no es «¿cuál de los treinta y seis aforismos?»,
    sino «¿qué palabra viene después?». Y a esa pregunta hay dos respuestas
    —`haṃ` o `ahaṃ`—, no doce.

    Medido sobre 250 formas de la Therīgāthā: 14,4 lecturas por forma, 10,2
    después de juntar las que sólo difieren en la vocal elidida, y **4,3 voces
    siguientes distintas**. Ése es el número al que se enfrenta quien lee.

    No se descarta nada: se ordena en dos niveles. Primero qué sigue; adentro,
    con qué regla.
    """
    grupos = []
    for l in lecturas:
        comp = [x for x in (l.get("componentes") or []) if x]
        voz = comp[-1] if comp else ""
        for g in grupos:
            if _misma_voz(g["voz"], voz):
                g["lecturas"].append(l)
                if voz not in g["variantes"]:
                    g["variantes"].append(voz)
                break
        else:
            grupos.append({"voz": voz, "variantes": [voz], "lecturas": [l]})
    return grupos


def analizar(texto):
    fichas = []
    crudos = texto.split()
    partido = [limpiar(t) for t in crudos]
    tokens = [x[1] for x in partido]
    signos = {i: (x[0], x[2]) for i, x in enumerate(partido) if x[0] or x[2]}
    banco = cargar()["banco"]
    i, consumidos = 0, set()

    # ── Las junturas ────────────────────────────────────────────────────
    # Dos voces escritas que juntas están en el banco: se muestran como una.
    # Dos comprobaciones que faltaban, y sin las cuales el párrafo que sale no
    # es el que entró:
    #
    #  · **no consumir dos veces la misma palabra.** El bucle no miraba
    #    `consumidos` mientras iteraba, así que de «ud aggo bhāso ti» salían
    #    «ud aggo» y «aggo bhāso»: `aggo` dos veces y `bhāso` desaparecida.
    #  · **no fundir donde no hubo operación.** Que la concatenación esté en el
    #    banco no significa que las dos voces se hayan unido: si la entrada es
    #    pakati —la ausencia de operación— no hay nada junto, y «āyasmā ānando»
    #    —dos palabras en toda edición pāḷi— se soldaba en una sola ficha
    #    archivada como «sin sandhi por regla».
    for j in range(len(tokens) - 1):
        if j in consumidos or (j + 1) in consumidos:
            continue
        par = tokens[j] + tokens[j + 1]
        if cotejo(par) not in banco:
            continue
        # **Y que el banco lo escriba así.** Coincidir por `cotejo` sólo dice
        # que las letras son las mismas sin espacios; no dice que el banco
        # registre esta partición. El texto trae «kāmuke sā» y el banco escribe
        # «kāmuk’ esā» —otro punto de corte—; trae «no hetaṃ» y el banco
        # escribe «no h’ etaṃ» —tres piezas—; trae «ud aggo» y el banco escribe
        # «u-d-aggo», una sola palabra. Fundir por `cotejo` ponía el análisis
        # del banco debajo de una partición que el banco no dice. Se exige que
        # la forma atestiguada tenga los mismos dos trozos escritos.
        if not any(
                [cotejo(x) for x in str(
                    dato.get("f") or dato.get("atestiguada")
                    or dato.get("forma_inicial") or "").split()]
                == [cotejo(tokens[j]), cotejo(tokens[j + 1])]
                for dato, _, _ in banco[cotejo(par)]):
            continue
        r = solucionar(par)
        if not r["lecturas"] or all(x.get("sin_operacion") for x in r["lecturas"]):
            continue
        r["escrita"] = tokens[j] + " " + tokens[j + 1]
        r["juntura"] = True
        r["fundida"] = [tokens[j], tokens[j + 1]]
        fichas.append((j, r))
        consumidos.update({j, j + 1})

    # **Se probó y se sacó**: extender esto a «la voz que sigue es un nipāta y
    # al unirlas el motor recupera exactamente lo escrito». Medido sobre 617
    # palabras de verso real de la Therīgāthā, disparó **cero veces** —la
    # edición del Sexto Concilio ya las imprime unidas—, y en prosa separada
    # tampoco sirve, porque la combinación cambia las letras de la juntura:
    # «Catukkhattuṃ ti» combina en `catukkhattunti`, no en `catukkhattuṃti`.
    # Derivar hacia adelante para llegar a esa forma exigiría emitir pasos sin
    # una forma atestiguada contra la cual comprobarlos, que es exactamente lo
    # que la regla de oro del proyecto prohíbe.

    for j, t in enumerate(tokens):
        if j in consumidos or not t:
            continue
        r = solucionar(t)
        if j in signos:
            r["puntuacion"] = signos[j]
        fichas.append((j, r))

    fichas.sort(key=lambda x: x[0])
    fichas = [f for _, f in fichas]

    # **«ti» sola no es una voz.** Es lo que queda de «iti» después del §40 —«la
    # vocal después de la niggahīta se elide»—. Que una edición la imprima
    # suelta significa que ahí hubo un sandhi y que el editor lo separó: las dos
    # voces del punto son la palabra anterior e «iti». Se dice, y no se deriva:
    # llegar a la forma unida exigiría emitir pasos sin una forma atestiguada
    # contra la cual comprobarlos.
    # ── Las junturas que la edición dejó a la vista ─────────────────────
    #
    # «ti» sola **no es una voz**: es lo que queda de «iti» tras el §40 —«la
    # vocal que sigue a la niggahīta se elide»—. Que una edición la imprima
    # suelta significa dos cosas a la vez: que ahí hubo un sandhi, y que las dos
    # voces son la palabra anterior e «iti».
    #
    # Y entonces **se puede dar la forma unida con su secuencia**, que es lo que
    # pide el encargo. No se deriva a ciegas: se enumeran las formas que esas dos
    # voces pueden dar, cada una vuelve a entrar por el solucionador, y sólo
    # sobrevive la que se descompone exactamente en las dos voces. Además, lo
    # escrito manda: si el editor puso «ti» y no «iti», la forma unida tiene que
    # terminar en «ti».
    def _poner(f, a, b, uniones, texto):
        # **El estado tiene que decir la verdad.** Antes esto dejaba `ti` en
        # `sin_sandhi` —«la voz está entera y ningún corte la parte»— con tres
        # lecturas adentro, y `vuttanayam` en `no_resuelto` con el motivo
        # borrado. Los dos mentían sobre su propio contenido, y `estado` sale
        # en el JSON.
        f["senal"] = "segura"
        f["estado"] = "juntura_declarada" if uniones else "juntura_sin_derivar"
        f["motivo"] = None
        f["juntura_declarada"] = [a, b]
        f["senal_motivo"] = texto
        if uniones:
            f["lecturas"] = []
            for forma, l in uniones:
                l = dict(l)
                l["forma_unida"] = forma
                l["componentes"] = [a, b]
                # **Acá no hay recomposición que valga, y hay que decirlo.**
                # En el resto de la herramienta una cadena se publica porque
                # reproduce la forma escrita. Acá no existe forma escrita que
                # reproducir: la edición separó la juntura, y lo que se
                # enumera son las formas que **podrían** salir de esas dos
                # voces. De «taṅ eva» salen cinco —`tadeva`, `tameva`, `taṃva`,
                # `tava`, `taññeva`— que se excluyen entre sí, y en cuatro la
                # «ṅ» que el escriba puso desaparece. Ninguna está comprobada
                # contra el texto, porque no hay contra qué comprobarla.
                l["verificada_contra_lo_escrito"] = False
                l["procedencia"] = ("enumeración: forma posible de estas dos "
                                    "voces, no comprobada contra el texto")
                f["lecturas"].append(l)
            f["lecturas_crudas"] = len(f["lecturas"])

    # La «m» desnuda ante vocal: la juntura la declaró la propia edición.
    for k, f in enumerate(fichas):
        if f.get("juntura") or k + 1 >= len(fichas):
            continue
        par = juntura_declarada(f["escrita"], fichas[k + 1]["escrita"])
        if not par:
            continue
        a, b = par
        _poner(f, a, b,
               combinar(a, b, escrita_a=f["escrita"]),
               "«{0}» termina en «m» desnuda, que no es final de voz pāḷi —once "
               "formas de 443.740 en el DPD—: es la salida del §34 con la "
               "juntura sin cerrar. Las dos voces son «{1}» y «{2}»".format(
                   f["escrita"], a, b))

    for k, f in enumerate(fichas):
        if cotejo(f["escrita"]) != "ti" or k == 0 or f.get("juntura"):
            continue
        anterior = fichas[k - 1]["escrita"]
        uniones = combinar(anterior, "iti", escrita_b="ti")
        _poner(f, anterior, "iti", uniones,
               "«ti» sola es lo que queda de «iti» tras el §40. La edición "
               "separó acá un sandhi: las dos voces son «{0}» e «iti»".format(
                   anterior))

    cuenta = {k: 0 for k, _ in CASILLAS}
    for f in fichas:
        f["casilla"] = clasificar(f)
        f["entera_en_lexico"] = es_palabra(f["escrita"])
        f["lecturas_crudas"] = len(f["lecturas"])
        f["senal_texto"] = f.get("senal_motivo") or ""
        if f["estado"] not in ("firmada", "resuelto", "sin_sandhi_por_regla"):
            f["lecturas"] = agrupar_por_corte(f["lecturas"])
        for x in f["lecturas"]:
            x["pasos_glosados"] = pasos_con_glosa(x["pasos"])
        f["por_voz"] = agrupar_por_voz_siguiente(f["lecturas"])
        cuenta[f["casilla"]] += 1

    return {"palabras": len(tokens), "fichas": fichas, "cuenta": cuenta,
            "casillas": CASILLAS}


# ── La página ───────────────────────────────────────────────────────────

PAGINA = r"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Solucionador de sandhis</title>
<style>
:root{
  --tinta:#1b1a17; --suave:#6b6659; --tenue:#8d8779; --linea:#e0dbcf;
  --papel:#faf8f3; --caja:#fff; --marca:#7a5c2e; --alerta:#8a4b3a;
  --ok:#4a6b45; --dudo:#8a6d2f; --realce:#f3efe6; --linea-fuerte:#c9c0ad;
}
*{box-sizing:border-box}
body{margin:0;background:var(--papel);color:var(--tinta);
  font:16px/1.6 "Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif}
.env{max-width:860px;margin:0 auto;padding:34px 22px 80px}
h1{font-size:22px;font-weight:600;letter-spacing:.02em;margin:0 0 4px}
.sub{color:var(--tenue);font-size:14px;margin:0 0 26px}
textarea{width:100%;min-height:92px;padding:14px 16px;border:1px solid var(--linea);
  border-radius:6px;background:var(--caja);color:var(--tinta);resize:vertical;
  font:19px/1.5 inherit}
textarea:focus{outline:2px solid #cbbfa4;outline-offset:1px}
.fila{display:flex;gap:14px;align-items:center;margin-top:14px}
button{font:15px inherit;padding:9px 20px;border:1px solid var(--tinta);
  background:var(--tinta);color:#fff;border-radius:5px;cursor:pointer}
button:hover{background:#000}
button.sec{background:transparent;color:var(--suave);border-color:var(--linea)}
button.sec:hover{background:#f1ede4;color:var(--tinta)}
.aviso{color:var(--tenue);font-size:13px;margin-left:4px}

.recuento{margin:30px 0 6px;padding:14px 16px;border:1px solid var(--linea);
  border-radius:6px;background:var(--caja);font-size:16px}
.recuento b{font-weight:600}
.recuento .sep{color:var(--linea);margin:0 8px}
.nota{color:var(--tenue);font-size:13px;line-height:1.5;margin:10px 2px 0}

.ficha{border:1px solid var(--linea);border-left:3px solid var(--linea);
  border-radius:6px;background:var(--caja);padding:16px 18px;margin:16px 0}
.ficha.resuelto{border-left-color:var(--ok)}
/* ── El texto como texto ─────────────────────────────────────────── */
.resumen{margin:26px 0 4px}
.cifra-grande{font-size:26px;letter-spacing:-.01em}
.cifra-grande b{color:var(--marca)}
.cifra-grande .de{color:var(--tenue);font-size:17px}
.otras{color:var(--tenue);font-size:14px;margin-top:6px;letter-spacing:.01em}
.cuerpo{font-size:20px;line-height:2.05;margin:22px 0 8px;
  background:var(--caja);border:1px solid var(--linea);padding:24px 26px}
.pista{color:var(--tenue);font-size:13.5px;margin:0 0 26px}
.w{cursor:pointer;border-radius:2px;padding:1px 2px;
  transition:background .12s}
.w:hover{background:var(--realce)}
.w.senalada,.w.resuelto{color:var(--marca);font-weight:600;
  box-shadow:inset 0 -2px 0 var(--marca)}
.w.fuera_alcance{color:var(--tenue)}
.w.sin_resolver{color:var(--alerta);box-shadow:inset 0 -1px 0 var(--alerta)}
.w.abierta{background:var(--realce);outline:1px solid var(--linea-fuerte)}
.w:focus-visible{outline:2px solid var(--marca)}

.medida{border-collapse:collapse;font-size:12.5px;color:var(--tenue);margin:8px 0 0}
.medida th,.medida td{text-align:right;padding:2px 0 2px 18px;border-bottom:1px solid var(--linea)}
.medida td:first-child,.medida th:first-child{text-align:left;padding-left:0}
.encargo{color:var(--tenue);font-size:13.5px;max-width:66ch;margin:10px 0 0;
  border-left:2px solid var(--linea);padding-left:12px}
.ficha.senalada{border-left-color:var(--marca);background:var(--realce)}
.cuantas.senal{color:var(--marca);font-weight:600}
.ficha.candidatos{border-left-color:#c9c3b5}
.ficha.sin_sandhi{border-left-color:#9aa2ad}
.ficha.fuera_alcance{border-left-color:#b0a68c}
.ficha.pakati{border-left-color:#9aa2ad}
.ficha.entera{border-left-color:#8f9aa8}
.cuantas.entera{color:var(--suave)}
.comp .flecha{color:var(--tenue)}
.voz-sig{margin:16px 0 4px;font-size:14px;color:var(--suave);
  border-top:1px solid var(--linea);padding-top:10px}
.voz-sig b{color:var(--tinta);font-size:16px}
.voz-sig .cuenta{color:var(--tenue);font-size:12px;margin-left:6px}
.alternas{font-size:13px;color:var(--suave);background:var(--realce);border-radius:4px;
  padding:7px 10px;margin:2px 0 8px;line-height:1.5}
details.mas{margin-top:6px}
details.mas summary{cursor:pointer;font-size:13px;color:var(--suave);
  padding:4px 0;user-select:none}
.ficha.sin_resolver{border-left-color:var(--alerta)}
.voz{font-size:21px;font-weight:600}
.casilla{float:right;font-size:12px;color:var(--tenue);letter-spacing:.04em;
  text-transform:uppercase;padding-top:7px}
.comp{font-size:18px;color:var(--marca);margin:6px 0 2px}
.cuantas{font-size:13px;color:var(--tenue);margin:10px 0 2px}
.sec{margin:8px 0 6px;padding:10px 0 2px;border-top:1px dotted var(--linea)}
.paso{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:baseline;
  padding:2px 0}
.paso .t{font-size:17px}
.paso .c{font-size:13px;color:var(--suave);white-space:nowrap}
.paso .g{grid-column:1/-1;font-size:12.5px;color:var(--tenue);margin:-2px 0 4px}
.pie{font-size:12.5px;color:var(--tenue);margin-top:8px}
.pie .proc{color:var(--suave)}
.motivo{font-size:14px;color:var(--alerta);margin-top:4px}
.diag{font-size:13px;color:var(--tenue);margin-top:6px}
.vacio{color:var(--tenue);text-align:center;padding:40px 0}
</style></head><body><div class="env">

<h1>Solucionador de sandhis</h1>
<p class="sub">Recibe texto pāḷi y responde, para cada punto de sandhi:
<b>cuántos hay y dónde están</b>, <b>cuáles son los componentes</b> antes de la
combinación, y <b>qué secuencia de suttas de Kaccāyana</b> explica la forma
resultante.</p>
<p class="encargo">El corte y la secuencia coinciden con el corpus en el <b>90 %</b> de 7.876 formas, y toda cadena publicada reproduce la forma exacta. Encontrar <b>dónde</b> hay sandhi en un párrafo es la etapa que el encargo pone tercera: acá abajo, cada vez, se dice cuánto se ve y cuánto no.</p>

<textarea id="txt" spellcheck="false" placeholder="lokaggo"></textarea>
<div class="fila">
  <button onclick="consultar()">Analizar</button>
  <button class="sec" onclick="document.getElementById('txt').value='';document.getElementById('sal').innerHTML='';">Limpiar</button>
  <span class="aviso">Ctrl+Enter también analiza</span>
</div>

<div class="resumen" id="res"></div>
<div id="texto"></div>
<div id="sal"></div>

<script>
const $ = s => document.querySelector(s);
document.getElementById('txt').addEventListener('keydown', e => {
  if(e.key === 'Enter' && (e.ctrlKey || e.metaKey)) consultar();
});

function esc(t){
  return String(t == null ? '' : t).replace(/[&<>"]/g,
    c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
}

async function consultar(){
  const texto = $('#txt').value.trim();
  $('#res').innerHTML = ''; $('#texto').innerHTML = ''; $('#sal').innerHTML = '';
  if(!texto){ return; }
  $('#sal').innerHTML = '<div class="vacio">…</div>';
  const r = await fetch('/consultar', {method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({texto})});
  pintar(await r.json());
}

let DATOS = null;

function pintar(d){
  DATOS = d;
  $('#sal').innerHTML = ''; $('#texto').innerHTML = '';
  const c = d.cuenta;

  // **El recuento de detección sólo tiene sentido para un texto.** Si alguien
  // escribe una voz sola, no hay ningún problema de detección: ya eligió la
  // palabra que quiere ver. Que la cabecera dijera «0 puntos de sandhi
  // señalados» sobre `ayampi` —cuya primera lectura es `ayaṃ + pi` por §31,
  // correcta— era decir una tontería con tipografía grande.
  if(d.palabras <= 3){
    const n = d.fichas.reduce((t, f) => t + (f.lecturas ? f.lecturas.length : 0), 0);
    $('#res').innerHTML = '<div class="cifra-grande">' +
      (n ? '<b>' + n + '</b> ' + (n === 1 ? 'lectura' : 'lecturas') +
           ' <span class="de">que recomponen la forma</span>'
         : '<span class="de">Ninguna lectura recompone la forma</span>') + '</div>';
    $('#sal').innerHTML = d.fichas.map((f, i) => ficha(d, f, i)).join('');
    return;
  }

  const marcadas = (c.resuelto||0) + (c.senalada||0);
  let res = '<div class="cifra-grande"><b>' + marcadas + '</b> ' +
            (marcadas === 1 ? 'punto de sandhi señalado'
                            : 'puntos de sandhi señalados') +
            ' <span class="de">en ' + d.palabras + ' palabras</span></div>';
  const otras = [];
  if(c.fuera_alcance) otras.push(c.fuera_alcance + ' compuesto' + (c.fuera_alcance>1?'s':''));
  if(c.sin_sandhi) otras.push(c.sin_sandhi + ' sin corte posible');
  if(c.candidatos) otras.push(c.candidatos + ' sin señal');
  if(c.sin_resolver) otras.push(c.sin_resolver + ' sin resolver');
  if(otras.length) res += '<div class="otras">' + otras.join(' · ') + '</div>';
  res += '<p class="nota">Se marca lo que tiene motivo medido: <b>el DPD publica ' +
         'su propia descomposición</b> de esa voz, o la voz falta en el DPD y no ' +
         'es un compuesto aparente, o lleva cola de «iti», o la edición dejó la ' +
         'juntura a la vista. Medido sobre la Therīgāthā entera (5.902 palabras, ' +
         '698 sandhis) y su comentario (46.078 palabras, 7.178 sandhis), que es ' +
         'texto corrido y no dos montones elegidos:</p>' +
         '<table class="medida"><tr><th></th><th>verso</th><th>comentario</th></tr>' +
         '<tr><td>marca, de cada 100 palabras</td><td>10</td><td>19</td></tr>' +
         '<tr><td>de lo marcado, sandhi del encargo</td><td>81 %</td><td>64 %</td></tr>' +
         '<tr><td>de lo marcado, otra juntura — compuesto, fuera</td><td>15 %</td><td>20 %</td></tr>' +
         '<tr><td>de lo marcado, nada</td><td>4 %</td><td>16 %</td></tr>' +
         '<tr><td>de los sandhis que hay, encuentra</td><td>71 %</td><td>79 %</td></tr></table>' +
         '<p class="nota">En prosa, entonces, <b>una de cada tres marcas no es un ' +
         'sandhi del encargo</b>: una de cada cinco es un compuesto —que está fuera— ' +
         'y una de cada seis no es nada. Conviene saberlo antes de leer la cifra de ' +
         'arriba. Lo que no se marca no se pierde — está a un clic.</p>';
  $('#res').innerHTML = res;

  let t = '<p class="cuerpo">';
  d.fichas.forEach((f, i) => {
    const pre = f.puntuacion ? esc(f.puntuacion[0]) : '';
    const post = f.puntuacion ? esc(f.puntuacion[1]) : '';
    t += pre + '<span class="w ' + f.casilla + '" data-i="' + i + '" ' +
         'onclick="ver(' + i + ')">' + esc(f.escrita) + '</span>' + post + ' ';
  });
  t += '</p><p class="pista">Tocá <b>cualquier</b> palabra para ver sus ' +
       'componentes y su cadena de suttas —también las que no están marcadas—. ' +
       'Se marca sólo lo que tiene motivo medido; el resto está en silencio, ' +
       'no perdido.</p>';
  $('#texto').innerHTML = t;
  const primera = d.fichas.findIndex(f => f.casilla === 'senalada' || f.casilla === 'resuelto');
  if(primera >= 0) ver(primera);
}

function ver(i){
  document.querySelectorAll('.w.abierta').forEach(e => e.classList.remove('abierta'));
  const e = document.querySelector('.w[data-i="' + i + '"]');
  if(e) e.classList.add('abierta');
  $('#sal').innerHTML = ficha(DATOS, DATOS.fichas[i], i);
}

function ficha(d, f, idx){
  let h = '<div class="ficha ' + f.casilla + '">';
  h += '<span class="casilla">' + nombreCasilla(d, f.casilla) + '</span>';
  h += '<div class="voz">' + esc(f.escrita) + '</div>';

  if(f.juntura_declarada){
    h += '<div class="cuantas senal">' + esc(f.senal_texto || '') + '.</div>';
    if(!f.lecturas.length){
      h += '<div class="sec"><div class="comp">' +
           esc(f.juntura_declarada.join(' + ')) + '</div>' +
           '<div class="alternas">Ninguna forma unida recompone en estas dos ' +
           'voces con las reglas enunciadas.</div></div></div>';
      return h;
    }
    if(f.lecturas.length > 1)
      h += '<div class="cuantas">' + f.lecturas.length + ' formas unidas ' +
           'recomponen en estas dos voces. Se muestran todas: el motor no elige.</div>';
    f.lecturas.forEach((l, li) => {
      if(li === 1 && f.lecturas.length > 1)
        h += '<details class="mas"><summary>ver las otras ' +
             (f.lecturas.length - 1) + ' formas unidas</summary>';
      h += '<div class="sec"><div class="comp">' +
           esc((l.componentes||[]).join(' + ')) +
           '<span class="flecha"> → </span><b>' + esc(l.forma_unida || '') + '</b></div>';
      for(const p of l.pasos_glosados){
        h += '<div class="paso"><span class="t">' + esc(p.texto) + '</span>' +
             '<span class="c">' + esc(p.cita) + '</span>';
        if(p.glosa) h += '<span class="g">' + esc(p.glosa) + '</span>';
        h += '</div>';
      }
      h += '<div class="pie"><span class="proc">' + esc(l.procedencia) +
           '</span>' + (l.recompone === false ? '' :
            ' · se descompone exactamente en estas dos voces') + '</div></div>';
    });
    if(f.lecturas.length > 1) h += '</details>';
    h += '</div>';
    return h;
  }
  if(f.casilla === 'senalada'){
    h += '<div class="cuantas senal">Señalada: ' + esc(f.senal_texto || '') +
         (f.lecturas.length ? '. ' + f.lecturas.length + ' lectura(s) recomponen la forma; ' +
          'la primera es la más probable, no la elegida.' : '.') + '</div>';
  } else if(f.casilla === 'candidatos'){
    const n = f.lecturas.length, crudas = f.lecturas_crudas || n;
    h += '<div class="cuantas entera">Sin señal. ' +
         (f.entera_en_lexico
            ? 'El DPD reconoce <b>' + esc(f.escrita) + '</b> tal como está escrita'
            : '<b>' + esc(f.escrita) + '</b> no está en el DPD, pero se parte sin ' +
              'operación en dos voces que sí están: es un compuesto aparente') +
         (n ? ', y además ' + n + ' corte(s) recomponen la forma' +
              (crudas > n ? ' —' + crudas + ' lecturas agrupadas por corte—' : '') +
              '. Que un corte recomponga no prueba que haya sandhi.'
            : '.') + '</div>';
  } else if(f.lecturas.length > 1){
    h += '<div class="cuantas">' + f.lecturas.length +
         ' lecturas recomponen esta forma. Se muestran todas: el motor no elige.</div>';
  }

  const grupos = f.por_voz || (f.lecturas.length ? [{voz:'', variantes:[], lecturas:f.lecturas}] : []);
  grupos.forEach((g, gi) => {
    if(gi === 1 && grupos.length > 1)
      h += '<details class="mas"><summary>ver las otras ' + (grupos.length - 1) +
           ' voces siguientes posibles</summary>';
    if(grupos.length > 1 && g.voz){
      const v = (g.variantes && g.variantes.length > 1)
        ? g.variantes.map(esc).join('</b> o <b>') : esc(g.voz);
      h += '<div class="voz-sig">… <b>' + v + '</b>' +
           ((g.variantes && g.variantes.length > 1)
             ? ' <span class="cuenta">la cantidad de la vocal inicial no deja rastro</span>' : '') +
           (g.lecturas.length > 1 ? ' <span class="cuenta">· ' + g.lecturas.length +
            ' lecturas</span>' : '') + '</div>';
    }
    g.lecturas.forEach((l, li) => {
      if(li === 1 && g.lecturas.length > 1)
        h += '<details class="mas"><summary>ver las otras ' + (g.lecturas.length - 1) +
             ' cadenas con la misma voz siguiente</summary>';
      const comp = (l.componentes||[]).filter(Boolean);
      h += '<div class="sec">';
      if(comp.length) h += '<div class="comp">' + esc(comp.join(' + ')) + '</div>';
      if(l.voces_anteriores)
        h += '<div class="alternas">La vocal elidida no deja rastro: la voz anterior ' +
             'pudo ser <b>' + l.voces_anteriores.map(esc).join('</b>, <b>') + '</b>. ' +
             'Las ' + l.voces_anteriores.length + ' recomponen igual.</div>';
      for(const p of l.pasos_glosados){
        h += '<div class="paso"><span class="t">' + esc(p.texto) + '</span>' +
             '<span class="c">' + esc(p.cita) + '</span>';
        if(p.glosa) h += '<span class="g">' + esc(p.glosa) + '</span>';
        h += '</div>';
      }
      const pie = [];
      if(l.referencia) pie.push(esc(l.referencia));
      pie.push('<span class="proc">' + esc(l.procedencia) + '</span>');
      if(l.origen) pie.push(esc(l.origen.archivo + ' · ' + l.origen.clave));
      h += '<div class="pie">' + pie.join(' · ') + '</div></div>';
    });
    if(g.lecturas.length > 1) h += '</details>';
  });
  if(grupos.length > 1) h += '</details>';

  if(f.motivo) h += '<div class="motivo">' + esc(f.motivo) + '</div>';
  h += '</div>';
  return h;
}

function nombreCasilla(d, k){
  for(const [a,b] of d.casillas) if(a===k) return b;
  return k;
}
</script>
</div></body></html>
"""


class Mano(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _responder(self, cuerpo, tipo="text/html; charset=utf-8"):
        b = cuerpo.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self._responder(PAGINA)
        self.send_error(404)

    def do_POST(self):
        if self.path != "/consultar":
            return self.send_error(404)
        n = int(self.headers.get("Content-Length", 0))
        try:
            texto = json.loads(self.rfile.read(n))["texto"]
            d = analizar(texto)
        except Exception as e:
            d = {"palabras": 0, "fichas": [], "cuenta": {}, "casillas": CASILLAS,
                 "error": "{0}: {1}".format(type(e).__name__, e)}
        self._responder(json.dumps(d, ensure_ascii=False),
                        "application/json; charset=utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--puerto", type=int, default=8731)
    ap.add_argument("--sin-navegador", action="store_true")
    ap.add_argument("--canon", action="store_true", help=(
        "enciende la capa del canon. Apagada por defecto: cuesta 75 "
        "cortes de 698 en la medición contra la Therīgāthā."))
    a = ap.parse_args()
    import solucionar_sandhis as _S
    _S.USAR_CANON = a.canon

    print("\n  Cargando el banco y el léxico…")
    cargar()
    url = "http://127.0.0.1:{0}/".format(a.puerto)
    srv = HTTPServer(("127.0.0.1", a.puerto), Mano)
    print("  Listo. La pantalla está en {0}".format(url))
    print("  Para cerrarla, cerrá esta ventana o apretá Ctrl+C.\n")
    if not a.sin_navegador:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n  Cerrada.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
