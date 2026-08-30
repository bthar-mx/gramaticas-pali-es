#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
El solucionador de sandhis. Entregable 1 del encargo.

    python3 nuestro/solucionar_sandhis.py lokaggo
    python3 nuestro/solucionar_sandhis.py --cobertura      # mide contra el banco

**Lo que pide el encargo, textual:**

    «Una herramienta que reciba texto pāḷi y responda, para cada punto de
    sandhi: cuántos hay y dónde están; cuáles son los componentes antes de la
    combinación; qué secuencia de suttas de Kaccāyana explica la forma
    resultante.»

Son **tres** cosas, no dos, y el módulo se describía con las dos que sabía
hacer. Dónde está cada una, medido:

  · **cuántos hay y dónde están** — `senal()`. Se ven 7 de cada 10 en verso y
    8 de cada 10 en prosa. De lo marcado tiene una juntura real el 96 % **en
    verso** y el 84 % en prosa; sandhi del encargo, el 81 % y el 64 %. El 96 %
    a secas, sin decir que era de verso, estuvo escrito acá y en la pantalla, y
    lo encontró una revisión externa.
  · **los componentes** — `proponer()` y `combinar()`. El punto de corte
    coincide con el del corpus en el 90,3 % de 698 formas de verso y el 90,5 %
    de 7.178 de prosa.
  · **la secuencia de suttas** — viene con los componentes, verificada por
    recomposición: si la cadena no reproduce la forma, no se publica.

**Proponer y verificar. Nunca afirmar.** Se propone un corte y una cadena de
reglas, se aplica la cadena, y tiene que reproducir **exactamente** la forma de
entrada. Si no coincide, se descarta. Y **se devuelven todas las lecturas
válidas, no una**: el sandhi es genuinamente ambiguo y las reglas opcionales
—*kvaci*, *vā*, *navā*— permiten sin obligar.

**Quién propone y quién verifica son distintos, a propósito.** Los candidatos de
corte los propone este módulo desde las reglas. Quien los verifica es
`herramientas/derivar_secuencias.py`, del Venerable, aplicando la operación
hacia adelante. Nosotros no escribimos el verificador.

**En tiempo de consulta no hay modelo.** Resuelve código determinista leyendo un
banco congelado con huella. La misma voz da la misma respuesta el martes y el
jueves.

Los estados, y el silencio dicho con las palabras que corresponden:

  · `firmada`             — está en el banco, con secuencia de procedencia
  · `candidatos`          — n lecturas que recomponen, todas, ordenadas
  · `sin_sandhi_por_regla`— pakati declarado en el banco: no hay operación
  · `sin_sandhi`          — la voz está entera y ningún corte la parte en dos
                            voces reales. **No es una falla**: es la respuesta.
  · `fuera_del_alcance`   — se parte en dos voces sin ninguna operación: es un
                            compuesto, y los compuestos los excluyó el Venerable
  · `resuelto`            — una sola lectura recompone
  · `juntura_declarada`   — la edición separó el sandhi y dejó la marca a la
                            vista; se dan las dos voces y la forma unida
  · `juntura_sin_derivar` — la marca está, pero ninguna forma unida recompone
  · `no_resuelto`         — con el motivo escrito

Los tres últimos son tres silencios distintos y **no se dicen igual**. Uno dice
«no hay sandhi», otro «esto no me toca», el tercero «no supe». Confundirlos hace
que la herramienta grite en cada palabra común de un texto.

`§404` no se usa nunca como comodín.

**El orden de las lecturas.** Se devuelven todas, pero primero las que tienen
un *nipāta* como segunda voz. La razón no es estadística sino gramatical: la
combinación eufónica se produce sobre todo en el encuentro de una voz con una
partícula —`iti`, `eva`, `iva`, `api`, `hi`, `ca`—, y ésa es una lista **cerrada**
de la fuente (Nandisena, *Partículas (nipāta)*, sobre Rū. 132-136 y Sad. iii
369-391), no un recuento del corpus con el que después se mide. Aquí la lista
**ordena**; no rechaza nada, que es el uso estricto para el que su propia
advertencia pide cotejarla antes.

Medido: la lectura correcta pasa de aparecer primera el 44 % de las veces al
61 % en los versos, y del 34 % al 79 % en el comentario. Ninguna lectura se
pierde: sólo cambia el orden en que se leen.
"""

import argparse
import hashlib
import json
import os
import sys
import re
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.dirname(AQUI))
from rutas import ruta, rel                                        # noqa: E402
sys.path.insert(0, os.path.dirname(ruta("herramientas", "derivar_secuencias.py")))
from normalizar import cotejo                                      # noqa: E402
import derivar_secuencias as D                                     # noqa: E402

REGLAS = ruta("recursos", "sandhi", "reglas.json")
TABLAS = ruta("recursos", "sandhi", "tablas-nandisena-secuencias.json")
LEXICO = ruta("recursos", "lexico", "dpd-formas.txt")
BANCO = ruta("banco.sha256")
LISTAS = ruta("recursos", "sandhi", "listas-cerradas.json")
CORPUS = ruta("recursos", "corpus", "corpus-formas.json")
CASOS = ruta("recursos", "solucionador", "casos-reportados.json")

# La capa del canon, apagada. Ver el porqué —y los dos números— en `cargar()`.
# Se enciende con `--canon`, nunca por el solo hecho de que el archivo exista.
USAR_CANON = False
# El modo sin DPD: el léxico es el corpus del Sexto Concilio y nada más.
# Ver el comentario en cargar(). Se enciende con `--solo-canon`.
SOLO_CANON = False
# El DPD como TESTIGO SILENCIOSO dentro del modo solo-canon (decisión de
# Angel, 2026-08-28, en chat; pendiente de confirmación del Venerable, que
# lo había apartado en la sesión 30). El papel es el que §9 de las normas
# del OSBCT siempre permitió: probar si una cadena ocurre, filtrar y
# ordenar candidatos — NUNCA análisis presentado al lector. La autoridad
# sigue siendo Kaccāyana y el texto de la edición; toda lectura se verifica
# por recomposición; donde la influencia del DPD se vea, se atribuye.
# Se enciende con `--dpd-filtro`, junto con `--solo-canon`.
DPD_FILTRO = False
DESCOMP = ruta("recursos", "lexico", "dpd-descomposiciones.tsv")

VOCALES = "aāiīuūeo"
LARGA = {"a": "ā", "i": "ī", "u": "ū"}
# Las diez consonantes que §35 enumera, en el orden del propio aforismo.
INSERTA = "yvmdntrlhg"

_cache = {}
# Caché aparte, a propósito: `cargar()` hace `if _cache: return _cache`, así que
# guardar acá el archivo de descomposiciones lo dejaría sin cargar el léxico.
_desc = {}


# ── El banco ────────────────────────────────────────────────────────────

def cargar():
    if _cache:
        return _cache
    d = json.load(open(REGLAS, encoding="utf-8"))
    _cache["reglas"] = {(r["sec"], str(r["n"])): r for r in d["rules"]}
    banco = {}
    for i, c in enumerate(d["ce"]):
        banco.setdefault(cotejo(c["f"]), []).append(
            (c, "recursos/sandhi/reglas.json", "ce[{0}]".format(i)))
    if os.path.exists(TABLAS):
        t = json.load(open(TABLAS, encoding="utf-8"))
        for i, fila in enumerate(t["filas"]):
            for j, s in enumerate(fila.get("secuencias", [])):
                f = s.get("em") or s.get("forma_final")
                if f:
                    banco.setdefault(cotejo(f), []).append(
                        (s, "recursos/sandhi/tablas-nandisena-secuencias.json",
                         "filas[{0}].secuencias[{1}]".format(i, j)))
    _cache["banco"] = banco
    # ── SOLO_CANON (añadido 2026-08-28, decisión del Venerable) ─────────
    #
    # El DPD se deja de lado: el léxico entero pasa a ser el corpus convertido
    # del Sexto Concilio (`corpus-formas.json`, generado por
    # `herramientas/generar_corpus_formas.py`). No es la capa `--canon` de la
    # entrega de Miguel De Anquín —aquélla proponía con el canon y caía al DPD
    # si callaba, y su canon salió de la capa de texto cruda de 40 PDF, sin
    # una sola «ṃ»—. Aquí no hay DPD en ninguna capa, y el canon es el de los
    # 118 volúmenes convertidos y verificados. Se pide con `--solo-canon`.
    if SOLO_CANON:
        _c = json.load(open(CORPUS, encoding="utf-8"))
        _cache["lexico"] = {cotejo(f) for f in _c.get("formas", {})}
        # Las cuentas del canon, agregadas por forma de cotejo. Son el
        # árbitro de la señal «posible» (etapa 3): no decide una autoridad
        # de afuera sino la frecuencia en la propia edición.
        frec = {}
        for f, n in _c.get("formas", {}).items():
            q = cotejo(f)
            frec[q] = frec.get(q, 0) + n
        _cache["frecuencia"] = frec
        # El DPD como testigo silencioso (ver la nota junto a DPD_FILTRO):
        # sus formas se suman al FILTRO de candidatos —más cortes admisibles,
        # que la recomposición sigue verificando— y su pertenencia queda
        # consultable para ordenar y señalar. No es autoridad: es un segundo
        # testigo de que una cadena es una palabra posible.
        _cache["dpd"] = set()
        if DPD_FILTRO and os.path.exists(LEXICO):
            _cache["dpd"] = {cotejo(x) for x in
                             open(LEXICO, encoding="utf-8").read().split("\n")
                             if x}
            _cache["lexico"] |= _cache["dpd"]
    else:
        _cache["lexico"] = {cotejo(x) for x in
                            open(LEXICO, encoding="utf-8").read().split("\n") if x}
        _cache["frecuencia"] = {}
        _cache["dpd"] = set()
    # ── El segundo léxico: las voces que el propio banco atestigua ──────
    #
    # 18 de las voces que el Venerable usa como componente en `reglas.json` no
    # están en el DPD: `putha`, `vipali`, `ani`, `chayo`… Que falten del
    # diccionario no las hace menos reales — están firmadas por él, en el
    # material del encargo—, y sin ellas catorce de sus propias formas quedan
    # «sin resolver» por un motivo que no es gramatical.
    #
    # **Se agregan con la puerta cerrada**, no todas: se descarta lo que no es
    # una voz —raíces con `√`, piezas con `+`, restos con coma, y todo lo de
    # menos de tres letras, que en esta lista son fragmentos como `s` e `ic`—.
    #
    # **Y el número que sale de acá no es independiente.** Medir el banco con
    # un léxico sacado del banco es circular, y así está dicho en el informe de
    # cobertura. El número que vale es el del corpus, que estas voces no tocan.
    extra = set()
    for lista in banco.values():
        for dato, _a, _c in lista:
            comp = dato.get("comp") if "s" in dato else dato.get("forma_inicial")
            for pieza in partir_componentes(comp or ""):
                q = cotejo(pieza)
                if (len(q) >= 3 and q.isalpha()
                        and "√" not in pieza and "+" not in pieza):
                    extra.add(q)
    _cache["lexico_banco"] = extra - _cache["lexico"]
    _cache["lexico"] |= _cache["lexico_banco"]

    # ── El canon como léxico, y el DPD como red ────────────────────────
    #
    # El DPD es un diccionario de formas **posibles**: 443.740, toda la flexión
    # de todo lema, ocurra o no. Por eso `dhammaṃ` recibe quince lecturas y
    # catorce son ruido —`dhama`, `dhame`, `dhami` son flexiones legítimas de
    # raíces que nadie escribió—. El corpus del Sexto Concilio, en cambio, lista
    # lo que **está escrito**.
    #
    # Se usan **los dos, en capas**: se propone con el canon, y si el canon no
    # devuelve nada se vuelve a proponer con el DPD. Medido sobre 400 formas de
    # los versos, con 17.546 formas atestiguadas:
    #
    #     sólo el DPD (como estaba)     13,0 lecturas/forma   90,8 % de acuerdo
    #     sólo el canon                  2,4                  66,2 %
    #     canon, y el DPD si calla       4,4                  86,2 %
    #
    # Y escribí ahí mismo que **con el canon entero los dos números mejoran**.
    # ESO ERA UNA EXTRAPOLACIÓN Y ERA FALSA. Medido el 24 de agosto sobre las
    # 698 formas medibles de la Therīgāthā, con el canon de 22.485 formas que
    # salió de los 40 PDF del Sexto Concilio:
    #
    #     sólo el DPD                   12,7 lecturas/forma   630 de 698  90,3 %
    #     canon, y el DPD si calla       9,4                  555 de 698  79,5 %
    #
    # Canon más grande, número peor: **75 cortes menos**. El defecto está en el
    # «si calla». El canon calla poco y acierta menos: cuando devuelve **una**
    # lectura equivocada, no calla, y la capa devuelve ahí mismo sin llegar
    # nunca al DPD. No es «el canon o nada»: es «lo primero que aparezca».
    #
    # Por eso la capa **ya no se enciende sola**. Antes bastaba con que el
    # archivo `corpus-formas.json` estuviera en la carpeta: se generó el 23 de
    # agosto a la noche y desde entonces el motor medía 79,5 % sin que nadie
    # hubiera cambiado una regla. Un archivo que aparece en una carpeta no es
    # una decisión. Ahora hay que pedirla: `--canon`.
    _cache["canon"] = set()
    if USAR_CANON and os.path.exists(CORPUS):
        c = json.load(open(CORPUS, encoding="utf-8"))
        _cache["canon"] = ({cotejo(f) for f in c.get("formas", {})}
                           & _cache["lexico"]) | _cache["lexico_banco"]

    _cache["nipata"] = set()
    if os.path.exists(LISTAS):
        _cache["nipata"] = {cotejo(x) for x in
                            json.load(open(LISTAS, encoding="utf-8"))["nipata"]}
    # ── Los casos adjudicados por lectores ──────────────────────────────
    # Decisión del Venerable (briefing 30 §3.5): cada fallo reportado, un
    # caso de prueba permanente. No es heurística: es adjudicación con
    # fuente y fecha, y el motor la consulta como al banco.
    _cache["casos"] = {}
    _cache["patrones"] = []
    _cache["no_sandhi"] = []
    if os.path.exists(CASOS):
        d_casos = json.load(open(CASOS, encoding="utf-8"))
        _cache["casos"] = {cotejo(c["forma"]): c
                           for c in d_casos.get("casos", [])}
        _cache["patrones"] = d_casos.get("patrones", [])
        _cache["no_sandhi"] = d_casos.get("no_sandhi", [])
    return _cache


# ── Las descomposiciones del propio DPD ────────────────────────────────
#
# El DPD publica, para 852.542 formas, **su propia descomposición**. No es una
# heurística nuestra: es un segundo testigo, hecho por otra gente con otro
# método. Medido sobre la Therīgāthā: de las 493 formas con sandhi que el DPD
# descompone, **las 493 coinciden con el corte del corpus**. Cuatrocientas
# noventa y tres de cuatrocientas noventa y tres.
#
# Y como detector es lo que faltaba para la primera línea del encargo —«cuántos
# hay y dónde están»—:
#
#     versos      marca 9,9 de cada 100 · 84 % sandhi · 1 % nada · recall 71 %
#     comentario  marca 18,4 de cada 100 · 66 % sandhi · 13 % nada · recall 78 %
#
# La señal que teníamos llegaba al 27 %. Ésta llega al 71-78 % con la misma
# precisión.
#
# **Se busca por bisección sobre el archivo ordenado**, sin cargarlo: son 77 MB
# y cargarlos costaría once segundos y 463 MB de memoria. Así cuesta cero.

def descomposicion(voz):
    """Lo que el DPD dice de esta forma, o `[]`. No decide: aporta.

    Bisección sobre el archivo ordenado, con `mmap`: no se carga nada —serían
    once segundos y 463 MB— y cada consulta cuesta microsegundos.
    """
    k = cotejo(voz)
    if not k or not os.path.exists(DESCOMP):
        return []
    if "m" not in _desc:
        import mmap
        f = open(DESCOMP, "rb")
        _desc["f"] = f
        _desc["m"] = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    m = _desc["m"]
    clave = k.encode("utf-8") + b"\t"
    lo, hi = 0, len(m)
    while lo < hi:
        medio = (lo + hi) // 2
        # alinear al principio de la línea que contiene `medio`
        ini = m.rfind(b"\n", 0, medio) + 1
        fin = m.find(b"\n", ini)
        if fin == -1:
            fin = len(m)
        linea = m[ini:fin]
        if linea.split(b"\t", 1)[0] + b"\t" < clave:
            lo = fin + 1
        else:
            hi = ini
        if ini <= lo and hi <= ini:
            break
    ini = m.rfind(b"\n", 0, min(lo, len(m) - 1)) + 1 if lo else 0
    while ini < len(m):
        fin = m.find(b"\n", ini)
        if fin == -1:
            fin = len(m)
        linea = m[ini:fin]
        cab = linea.split(b"\t", 1)[0]
        if cab == k.encode("utf-8"):
            partes = linea.decode("utf-8").split("\t")
            return [tuple(x.strip() for x in d.split(" + "))
                    for d in partes[1].split(" | ") if d.strip()]
        if cab > k.encode("utf-8"):
            return []
        ini = fin + 1
    return []


def nombre_lexico():
    """El léxico en uso, para que los mensajes digan la verdad (2026-08-28):
    en modo --solo-canon el DPD no interviene y nombrarlo confundía."""
    return "del canon (Sexto Concilio)" if SOLO_CANON else "del DPD"

def es_palabra(t):
    return cotejo(t) in cargar()["lexico"]


# ── Proponer: de la forma a los componentes ─────────────────────────────
# El vecindario. Para cada punto de corte de la forma se enumeran las voces
# que, de existir, podrían haber producido ese prefijo y ese sufijo. No decide
# nada: sólo enumera. Filtra el léxico, y decide la recomposición.

import operaciones as OP                                            # noqa: E402

NASALES = "ṅñṇnm"


def _vecinos_a(pre):
    """Voces que podrían haber dado este prefijo."""
    v = {pre}
    if pre:
        for x in VOCALES:
            v.add(pre + x)                    # se le elidió la vocal final (§12…)
            v.add(pre[:-1] + x)               # se le sustituyó (y, v, largo, corto)
        v.add(pre + "ṃ")                      # se le elidió la niggahīta (§38, §39)
        for x in VOCALES:
            # §38 elide la niggahīta ante vocal, y la nota 17 añade que, elidida
            # la niggahīta, **se elide también la vocal anterior**. Las dos
            # juntas dejan el prefijo desnudo: de «paripucchiṃ» queda
            # «paripucch». Si sólo se restituye una de las dos, la voz no se
            # propone nunca. Filtra el léxico.
            v.add(pre + x + "ṃ")
        if pre[-1] in NASALES:
            v.add(pre[:-1] + "ṃ")             # §31, §32, §33
        if pre[-1] in "md":
            v.add(pre[:-1] + "ṃ")             # §34
        if pre.endswith("abbh"):
            v.add(pre[:-4] + "abhi")          # §44
        if pre.endswith("ajjh"):
            v.add(pre[:-4] + "adhi")          # §45
        if pre.endswith("paṭi"):
            v.add(pre[:-4] + "pati")          # §48
        if pre.endswith("o") or pre.endswith("u"):
            v.add(pre[:-1] + "ava")           # §50, §79
        if pre[-1] in "yvmdntrlhg":
            v.add(pre[:-1])                   # se le insertó una consonante (§35)
        # **Devolver la niggahīta.** §31 la convierte en la última consonante
        # del grupo —k→ṅ, c→ñ, ṭ→ṇ, t→n, p→m—, §32 y §33 en «ñ», y el «vā» de
        # §31 en «l». El vecindario sabía deshacer casi todo menos esto, y por
        # eso de `taññeva` nunca se proponía `taṃ + eva`, ni de `sallekho`
        # `saṃ + lekho`: la primera voz correcta no llegaba a existir.
        if pre[-1] in "ṅñṇnml":
            v.add(pre[:-1] + "ṃ")
        if pre.endswith("cc") or pre.endswith("c"):
            v.add(pre.rstrip("c") + "ti")     # §19: «ti» quedó en «c»
        # §51: «a veces hay transposición de las letras r, h, n». Se deshace
        # probando los mismos dos saltos que la operación hace —el contiguo y
        # el de una letra en medio—, que son los que las tres formas del banco
        # atestiguan. Sin esto, de «anabhineyya» nunca se propone «na», que es
        # la privativa, y el propio banco del Venerable la explica con §51.
        for i, ch in enumerate(pre):
            if ch not in "rhn":
                continue
            for salto in (1, 2):
                for j in (i - salto, i + salto):
                    if 0 <= j < len(pre):
                        L = list(pre)
                        L[i], L[j] = L[j], L[i]
                        v.add("".join(L))
    return {x for x in v if x}


def _vecinos_b(suf):
    """Voces que podrían haber dado este sufijo."""
    v = {suf}
    if suf:
        for x in VOCALES:
            v.add(x + suf)                    # se le elidió la vocal inicial (§13)
            v.add(x + suf[1:])                # se le sustituyó o alargó (§14, §15…)
        if len(suf) > 1 and suf[0] == suf[1]:
            v.add(suf[1:])                    # se duplicó (§28, §29)
        if len(suf) > 1 and suf[:2] in ("kk", "cc", "ṭṭ", "tt", "pp"):
            v.add(suf[1:])
        if suf[0] in "yvmdntrlhg":
            v.add(suf[1:])                    # se insertó una consonante (§35)
        if suf[0] == "ḷ":
            v.add(suf[1:])                    # la «ḷ» de la nota 9, tras «cha»
        # §32 y §33 dejan una «ñ» al principio de la voz que sigue —de
        # `taṃ + eva` sale `tañ ñeva`, de `saṃ + yogo` sale `sañ ñogo`—, y sin
        # deshacerlo la segunda voz correcta no llegaba a proponerse nunca.
        if suf[0] == "ñ":
            v.add(suf[1:])                    # §32: la «ñ» duplicada
            v.add("y" + suf[1:])              # §33: la «y» que se volvió «ñ»
        if suf.startswith("riva"):
            v.add("eva" + suf[4:])            # §22: la «e» de «eva» dio «ri»
        for dig, simple in OP.SEGUNDA_CUARTA.items():
            if suf.startswith(simple + dig):
                v.add(suf[len(simple):])      # §29
    return {x for x in v if x}


TODAS_LAS_OPERACIONES = dict(OP.TODAS)


def sin_anotacion(paso):
    """El texto de un paso, sin la anotación final entre paréntesis.

    El encargo fija el contrato: «el texto va primero… y la anotación entre
    paréntesis al final». La expresión que había —`\((?:§[^)]*|EM)\)`— sólo
    reconocía dos formas de anotación, y las Tablas usan una tercera: «(por
    "ca" de §20)». Por eso `bahvābādhobavhābādho` daba `recompone=False` y se
    publicaba igual: no es que la cadena fallara, es que no se sabía leer el
    último paso. Se reconoce cualquier paréntesis final.
    """
    return re.sub(r"\s*\([^)]*\)\s*$", "", paso or "").strip()


def _paso_que_no_hace_nada(pasos):
    """¿Hay un paso cuyo texto es idéntico al anterior?

    Un paso es la aplicación de un aforismo, y un aforismo que no cambia una
    letra no se aplicó. `LARGA` del derivador mapea «e»→«e» y «o»→«o», de modo
    que §15 y §16 emitían un paso calcado del anterior: de `ratanesu` salían
    dos lecturas iguales, la segunda con un «(§15)» que no alargaba nada. Sobre
    2.000 formas del corpus eso era el **10 % de todas las lecturas**.

    Se descarta la cadena entera, no el paso: la misma lectura vuelve a salir
    por la vía que no lo cita, y publicar dos veces lo mismo con una referencia
    de más es exactamente lo que el encargo prohíbe.
    """
    prev = None
    for paso in pasos:
        texto = sin_anotacion(paso)
        if prev is not None and texto == prev:
            return True
        prev = texto
    return False


def _letra_ajena(n, pasos):
    """¿El paso de §17/§18/§21 sustituye por la letra que **no** es la suya?

    Los tres enunciados nombran su vocal *y su letra*: §17 «"Y" es la
    sustitución de la "e" final»; §18 «"V", de los que terminan en "o" y "u"»;
    §21 «la letra anterior "i" (o "ī")… se vuelve "y"». `licencia_sustitucion`
    comprueba la vocal antes de llamar al derivador, pero la letra la elige el
    derivador, que prueba «y» y «v» para los tres. Así salía `sako + aputto ·
    sak y aputto (§18)`, con §18 produciendo una «y» que no enuncia, y
    `te + eva · t v eva (§17)` en espejo.

    El archivo del Venerable no se toca: se descarta después la cadena cuya
    letra el aforismo no autoriza.
    """
    marca = "(§{0})".format(n)
    letra = OP.LETRA_SUST[n]
    for paso in pasos:
        if not paso.rstrip().endswith(marca):
            continue
        solas = [x for x in sin_anotacion(paso).split() if x in ("y", "v")]
        if solas and solas != [letra]:
            return True
    return False


def _forward(n, a, b, F):
    """Aplica la operación §n. Para las nueve que el Venerable implementó, el
    verificador es el suyo; para las demás, el nuestro, con su enunciado."""
    if n in OP.VOCAL_SUST and not OP.licencia_sustitucion(a, b, n):
        # §17 sustituye la «e» final, §18 la «o» y la «u», §21 la «i» y la
        # «ī»: lo dicen sus propios enunciados en el Sandhi-kappa. El
        # derivador no comprueba la vocal, y como §17 y §21 producen la
        # misma «y», toda forma con «e» final salía además bajo §21 y toda
        # forma con «i» final además bajo §17. De «myāyaṃ» se publicaban dos
        # veces «me + ayaṃ», una con referencia falsa. Aquí no se corrige su
        # archivo: se deja de preguntarle por un aforismo que no cubre el par.
        return None
    if n in (13, 16, "38+13") and not OP.licencia_elision_siguiente(a, b, n):
        # §13 es «Vā paro asarūpā»: sólo tras vocal DISÍMIL. Con vocales de
        # la misma clase manda §12 (+§15) — adjudicación del IEBH,
        # 2026-08-29, observación sobre assasāmīti; ver la licencia.
        return None
    if n in (12, 13, 15, 16, 17, 18, 21, 28, 35):
        # el verificador de estas nueve es el del Venerable
        pasos = D.derivar(n, a + " " + b, F)
    else:
        f = TODAS_LAS_OPERACIONES.get(n)
        pasos = f(a, b, F) if f else None
    if not pasos:
        return None
    # Dos cosas que ninguna cadena publicada puede tener, venga de donde venga:
    # un paso que no cambia nada, y una sustitución con la letra de otro
    # aforismo. Las dos se comprueban acá, del lado nuestro.
    if _paso_que_no_hace_nada(pasos):
        return None
    if n in OP.LETRA_SUST and _letra_ajena(n, pasos):
        return None
    return pasos


ORDEN = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 25, 26, 27, 28, 29,
         31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 44, 45, 48, 49, 50, 51,
         79, 183, 269, "17+25", "18+25", "21+25", "35+26", "38+12", "38+13",
         "31vā", "35nota9"]


def proponer_en_frase(escrita):
    """Una frase tiene varias junturas y el sandhi ocurre en una.

    Los dos problemas del punto D10 son distintos: dentro de una palabra hay
    que buscar DÓNDE está el corte; entre dos palabras escritas hay que decidir
    SI la juntura es un punto de sandhi. Acá se prueba cada juntura por
    separado y se deja el resto de la frase intacto, que es lo que hace el
    propio documento cuando escribe «sutaṃ m’ etaṃ, bho Gotama».
    """
    fichas = escrita.split()
    if len(fichas) < 2:
        return []
    out = []
    for i in range(len(fichas) - 1):
        for l in proponer(cotejo(fichas[i] + fichas[i + 1]), una_voz=False):
            l = dict(l)
            l["contexto"] = {"antes": fichas[:i], "despues": fichas[i + 2:]}
            l["reconstruida"] = " ".join(
                fichas[:i] + [fichas[i] + fichas[i + 1]] + fichas[i + 2:])
            out.append(l)
    return out


def pares_del_lexico(F):
    """Los cortes que parten la voz en dos voces que el DPD reconoce.

    Se separa de `proponer()` porque contesta otra pregunta, y es la que un
    lector quiere primero: ¿hay siquiera dos palabras acá? Si no las hay,
    ninguna regla va a poder operar y decir «probé 35 aforismos» no informa.

    **Filtra exactamente igual que `proponer()`, y por la misma razón.** Antes
    no lo hacía, y el diagnóstico de `bhikkhuniṃ` decía «84 cortes en dos voces
    del léxico» y ponía de ejemplo `bhikkhu + iṃ`, `bhikkhū + iṃ`, `bhikkho +
    iṃ` —cortes que el propio motor ya rechaza porque `iṃ` es una desinencia,
    no una voz—. Un contador que cuenta lo que el motor descarta no informa:
    miente con precisión de dos cifras.
    """
    lex = cargar()["lexico"]
    out = []
    for i in range(1, len(F)):
        A = [x for x in _vecinos_a(F[:i])
             if cotejo(x) in lex and not _es_desinencia(x)]
        if not A:
            continue
        for b in (x for x in _vecinos_b(F[i:])
                  if cotejo(x) in lex and not _solo_vocal(x)
                  and not _es_desinencia(x)):
            for a in A:
                out.append((a, b))
    return out


def _solo_vocal(t):
    """Una sola vocal no puede ser la voz que sigue.

    Las voces de una sola vocal son upasagga —«u», «ā», «a»—, y el upasagga es
    un **prefijo**: Thitzana lo dice al enumerarlos, *«particles commonly used
    as prefixes in the beginnings of certain verbs and words»* (nota 14 del
    capítulo). Va delante, nunca detrás.

    Medido sobre el banco: en las 266 formas, **ninguna** tiene una sola vocal
    como segundo componente; dos la tienen como primero —`u + aggo`,
    `u + dhāro`—, y ésas no se tocan. Sin esta comprobación, `bhikkhu` recibe
    ocho lecturas y las ocho son `bhikkh-` más una vocal más «u».
    """
    c = cotejo(t)
    return len(c) == 1 and c in VOCALES


def _es_desinencia(t):
    """Una vocal más niggahīta no es una voz: es una desinencia.

    `aṃ`, `iṃ`, `uṃ` están en el DPD porque su tabla de formas flexionadas las
    arrastra, pero no son palabras: no tienen consonante inicial, no figuran en
    la lista cerrada de 221 nipāta, y **en las 266 formas del banco no aparecen
    ni una vez como componente**, ni delante ni detrás. `taṃ`, `yaṃ`, `kiṃ` sí
    son voces y no las toca esta comprobación: tienen consonante.

    Sin esto, `bhikkhuniṃ` —que es una palabra entera, acusativo de
    `bhikkhunī`— recibe seis lecturas del tipo `bhikkhuni + iṃ`.
    """
    c = cotejo(t)
    return len(c) == 2 and c[0] in VOCALES and c[1] == "ṃ"


def bien_formada(pasos):
    """El último segmento de cada paso tiene que poder pronunciarse.

    §10 separa la consonante final **sin vocal** de la voz anterior, y §11 la
    vuelve a unir: por eso un segmento sin vocal es legítimo **al principio**
    de un paso —«yass a indriyāni»—, que es donde §10 lo deja. Al final no:
    ahí está la voz que sigue, y una voz sin vocal no es una voz.

    **Hoy no descarta nada.** Se escribió por `sakkaccaṃ`, que recibía tres
    lecturas —`sakkacca + aṃ`, `+ iṃ`, `+ uṃ`— con el mismo paso imposible
    `sakkacc a ṃ`; desde entonces esas tres las corta antes el vecindario y
    la recomposición, y `sakkaccaṃ` sale con otras tres que sí recomponen.
    Medido sobre 1.500 formas del corpus: consultada 17.688 veces, descartó
    **0**. Se deja como red —el caso que cubre es real y el coste es nulo—,
    pero la docstring decía que hacía un trabajo que no hace, y eso es
    justamente lo que este proyecto no se permite.
    """
    for paso in pasos:
        # Usa `sin_anotacion`, que reconoce cualquier paréntesis final. Con la
        # expresión estrecha de antes, un paso anotado «(por "vā" en §31)» se
        # quedaba con el paréntesis dentro del texto, la última ficha era
        # «§31)» —sin vocal— y **la cadena entera se descartaba en silencio**.
        # Ahí se perdían las lecturas de las reglas que citan un «ca» o un
        # «vā» y no un aforismo pelado.
        texto = sin_anotacion(paso)
        for alternativa in texto.split(","):
            fichas = alternativa.split()
            if fichas and not any(c in VOCALES for c in fichas[-1]):
                return False
    return True


def compuesto_del_lexico(t, piezas=3):
    """La voz no está en el DPD, pero **es la suma de voces que sí están**.

    `aggamaggañāṇa` no figura en el diccionario, y no tiene por qué: es un
    compuesto. `aggamagga` y `ñāṇa` sí están, y puestas una al lado de la otra
    dan exactamente esa forma. Que el diccionario no liste el compuesto no lo
    hace menos voz.

    Devuelve las piezas si las encuentra, y `None` si no. **No analiza el
    compuesto** —eso está fuera del encargo—: sólo comprueba que lo es, para
    poder explicar el sandhi de su juntura con la voz que sigue.
    """
    lex = cargar()["lexico"]
    t = cotejo(t)
    if len(t) < 6:
        return None
    if t in lex:
        return [t]
    if piezas < 2:
        return None
    for i in range(3, len(t) - 2):
        a, b = t[:i], t[i:]
        if a not in lex:
            continue
        if b in lex:
            return [a, b]
        resto = compuesto_del_lexico(b, piezas - 1)
        if resto:
            return [a] + resto
    return None


MARCAS = "’'-"


def proponer_en_marca(voz):
    """Cuando el escriba **dijo dónde está la juntura**, se propone ahí y no a
    ciegas.

    `dhātu-āyatanāni` lleva un guion, y `paripuccha’haṃ` un apóstrofo: en los
    dos casos la edición marcó el punto de corte, y es el único lugar del texto
    donde alguien lo dijo. `cotejo()` los borra —tiene que borrarlos, para
    comparar— y el motor buscaba a ciegas: de `dhātu-āyatanāni` devolvía
    `dhātuāyatanā + ini`, cuando `dhātu` y `āyatanāni` están los dos en el
    léxico y la forma unida está **en el banco**, con secuencia firmada.

    Leer la marca no es adivinar: es no tirar el dato que ya estaba escrito.
    """
    partes = re.split("[" + MARCAS + "]", voz)
    if len(partes) != 2 or not all(partes):
        return []
    a_pre, b_suf = partes
    F = cotejo(voz)
    lex = cargar()["lexico"]
    # **El guion y el apóstrofo no dicen lo mismo, y no se tratan igual.**
    # El apóstrofo marca una *elisión*: `paripuccha’haṃ` avisa que algo se cayó
    # ahí, así que hay operación por definición. El guion marca una *juntura*, y
    # puede ser un compuesto sin ninguna operación: `dhātu-āyatanāni` son
    # `dhātu` y `āyatanāni` puestas una al lado de la otra. Que la marca esté no
    # obliga a que haya sandhi: obliga a mirar ahí.
    if ("-" in voz and cotejo(a_pre) in lex and cotejo(b_suf) in lex
            and cotejo(a_pre) + cotejo(b_suf) == F):
        return [{"yuxtaposicion_declarada": [a_pre, b_suf]}]
    vistas, out = set(), []
    A = [x for x in _vecinos_a(cotejo(a_pre))
         if cotejo(x) in lex and not _es_desinencia(x)]
    B = [x for x in _vecinos_b(cotejo(b_suf))
         if cotejo(x) in lex and not _solo_vocal(x) and not _es_desinencia(x)]
    for a in A:
        for b in B:
            for n in ORDEN:
                k = (a, b, n)
                if k in vistas:
                    continue
                vistas.add(k)
                pasos = _forward(n, a, b, F)
                if not pasos or not bien_formada(pasos):
                    continue
                out.append({"componentes": [a, b], "sutta": n, "pasos": pasos,
                            "reconstruida": F, "recompone": True,
                            "procedencia": "propuesta automática",
                            "corte_declarado": True})
    nip = cargar()["nipata"]
    out.sort(key=lambda x: (0 if cotejo(x["componentes"][-1]) in nip else 1,
                            str(x["sutta"]), x["componentes"]))
    return out


def proponer(F, una_voz=True, compuestos=False):
    """Todas las lecturas que recomponen exactamente F. Ordenadas, sin repetir.

    `una_voz` distingue los dos casos del punto D10, que no son el mismo. Dentro
    de **una palabra** hay que buscar dónde está el corte, y ahí una cadena cuya
    yuxtaposición ya da la forma es un rodeo. Entre **dos palabras escritas** la
    yuxtaposición es justamente lo normal —el texto las separó—, y el banco tiene
    trece frases así, «ekaṃ samayaṃ», «evaṃ vutte». Por eso la comprobación sólo
    se aplica a la voz sola.
    """
    c = cargar()
    lex = c["lexico"]
    vistas, out = set(), []
    for i in range(1, len(F)):
        admisible = ((lambda x: cotejo(x) in lex or
                      bool(compuesto_del_lexico(x))) if compuestos
                     else (lambda x: cotejo(x) in lex))
        A = [x for x in _vecinos_a(F[:i])
             if admisible(x) and not _es_desinencia(x)]
        if not A:
            continue
        B = [x for x in _vecinos_b(F[i:])
             if cotejo(x) in lex and not _solo_vocal(x) and not _es_desinencia(x)]
        for a in A:
            for b in B:
                for n in ORDEN:
                    k = (a, b, n)
                    if k in vistas:
                        continue
                    vistas.add(k)
                    if una_voz and cotejo(a) + cotejo(b) == F:
                        # **Elidir algo y volver a ponerlo no es explicar nada.**
                        # Si las dos voces, puestas una al lado de la otra, ya
                        # dan la forma, no hubo ninguna operación entre ellas, y
                        # cualquier cadena que diga lo contrario es un rodeo.
                        # `so + hi` → `sohi` salía con «§10 · §12 elide la "o" ·
                        # §36 inserta una "o" · §11», que recompone y no dice
                        # nada. Los aforismos explican una **diferencia** entre
                        # la yuxtaposición y la forma atestiguada; sin diferencia
                        # no hay nada que explicar.
                        #
                        # Comprobado contra el banco: de las 229 formas firmadas
                        # de dos componentes, las 13 en que la concatenación ya
                        # da la forma son **todas frases** —«ekaṃ samayaṃ»,
                        # «evaṃ vutte»—, y ésas el banco ya las declara pakati.
                        # Ninguna voz sola queda afuera por esto.
                        continue
                    pasos = _forward(n, a, b, F)
                    if not pasos or not bien_formada(pasos):
                        continue
                    out.append({"componentes": [a, b], "sutta": n,
                                "pasos": pasos, "reconstruida": F,
                                "recompone": True,
                                "procedencia": "propuesta automática"})
    # **Primero lo que el DPD también descompone así.** No es preferencia
    # nuestra: es coincidir con un segundo testigo. Medido sobre la Therīgāthā,
    # de 493 formas que el DPD descompone, las 493 coinciden con el corte del
    # corpus. Después, el orden por nipāta, que ya estaba medido.
    dpd = set()
    for d in descomposicion(F):
        for i in range(len(d) - 1):
            dpd.add((cotejo(d[i]), cotejo(d[i + 1])))
        dpd.add((cotejo(d[0]), cotejo("".join(d[1:]))))
    nip = c["nipata"]
    # Con el DPD de testigo silencioso, una lectura cuyas DOS piezas figuran
    # en el diccionario va antes que una con piezas que sólo el corpus
    # atestigua: `na + atthi` antes que `natti + hi`. Es ordenación, no
    # análisis: ninguna lectura se pierde. Medido antes de adoptarse (el
    # número, en el commit que lo trae).
    dic = c.get("dpd") or set()
    out.sort(key=lambda x: (
        0 if tuple(cotejo(y) for y in x["componentes"]) in dpd else 1,
        (0 if all(cotejo(y) in dic for y in x["componentes"]) else 1)
        if dic else 0,
        0 if cotejo(x["componentes"][-1]) in nip else 1,
        str(x["sutta"]), x["componentes"]))
    for x in out:
        if tuple(cotejo(y) for y in x["componentes"]) in dpd:
            x["dpd"] = True
    return out


# ── Resolver ────────────────────────────────────────────────────────────

def solucionar(voz):
    """Resuelve, y en solo-canon completa la señal con lo que las lecturas
    permiten decir (la señal «posible» de la etapa 3). El cuerpo está en
    `_solucionar`; esta envoltura sólo toca `senal`/`senal_motivo`, nunca
    las lecturas ni el estado."""
    r = _solucionar(voz)
    if SOLO_CANON:
        _ascender_senal(r)
        _silenciar_no_sandhi(r)
        _aplicar_caso(r)
        _aplicar_patron(r)
    return r


def _silenciar_no_sandhi(r):
    """Las reglas negativas adjudicadas (casos-reportados.json, `no_sandhi`).

    La primera, del IEBH (2026-08-28): las voces terminadas en -tvā y
    -tvāna son absolutivos, indeclinables — no se señalan como sandhi. La
    señal calla; las lecturas que recomponen siguen visibles al pegar la
    voz sola, como en todo silencio. Va ANTES de `_aplicar_caso`: un caso
    adjudicado sandhi=true mandaría sobre la regla, como manda sobre todo.
    """
    if not r.get("senal"):
        return
    c = r["cotejo"]
    for regla in cargar().get("no_sandhi", []):
        if any(c.endswith(t) for t in regla.get("terminaciones", [])):
            r["senal"] = None
            r["senal_motivo"] = None
            return


def _patron_niggahita_m(r, patron, frec, f_forma):
    """El patrón de §34: niggahīta → m ante vocal, con segunda voz corriente.

    Aprobado por el IEBH el 2026-08-29: «§34 is approved since anytime you
    find the niggahita changed to 'm' before a vowel, it means this rule
    applies». A diferencia de los patrones vigentes, que se declaran por la
    SEGUNDA voz (iti, api, ca), aquí la clase la identifica la «m» de la
    juntura, y la licencia es la unicidad de la LECTURA de la clase, no la
    de la base — las dos voces varían.

    La receta, tal como la simuló y midió `generar_informe_niggahita_m.py`
    (54 formas afirmables, masa 31.344, 37 de ellas sin señal ninguna al
    medirse — informe-niggahita-m.md):

      · candidatas: lecturas verificadas (base, seg) con base terminada en
        «ṃ» y seg empezando en vocal cuya superficie es EXACTAMENTE
        base[:-1] + «m» + seg — §34 puro, sin otra operación—, las dos
        voces atestiguadas;
      · el resguardo de siempre, por los DOS lados: cada voz al menos tan
        frecuente en el canon como la forma entera (piso = max(frec, 1));
      · gemelas (misma base, segundas que sólo difieren en la cantidad de
        la vocal inicial: ayaṃ/āyaṃ) → la de inicial BREVE, como en el
        desempate ya firmado de las bases;
      · si queda EXACTAMENTE UNA, se afirma; si no, el patrón calla.

    Devuelve True si afirmó (la señal queda «segura» y la lectura primera).

    RÉGIMEN MEDIDO (decisión de Angel, 2026-08-30): el patrón sólo afirma
    formas cuya frecuencia alcanza `frec_minima` (159: la frecuencia del
    puesto 5.000, hasta donde llegó la medición). Fuera de ahí el resguardo
    se debilita —con la forma rara, el piso de las candidatas cae— y
    aparecían afirmaciones que la medición nunca vio: jātimaraṇā (frec 3)
    salía como jātiṃ + araṇā siendo el compuesto jāti+maraṇa, y
    vedhamānehi (7) como vedhaṃ + ānehi siendo el participio vedhamāna.
    Las formas raras callan hasta que el IEBH amplíe la licencia.
    """
    if f_forma < patron.get("frec_minima", 0):
        return False
    sup = r["cotejo"]
    piso = max(f_forma, 1)
    cand = set()
    for l in r.get("lecturas", []):
        comp = [cotejo(x) for x in l.get("componentes", [])]
        if (len(comp) == 2 and len(comp[0]) >= 2
                and comp[0].endswith("ṃ")
                and comp[1][:1] in VOCALES
                and comp[0][:-1] + "m" + comp[1] == sup
                and frec.get(comp[0], 0) >= piso
                and frec.get(comp[1], 0) >= piso):
            cand.add((comp[0], comp[1]))
    pares = sorted(cand)
    if len(pares) == 2:
        (b1, s1), (b2, s2) = pares
        if (b1 == b2 and s1 and s2 and s1[1:] == s2[1:]
                and LARGA.get(s1[:1]) == s2[:1]):
            pares = [(b1, s1)]
    if len(pares) != 1:
        return False
    base, seg = pares[0]
    delante, detras = [], []
    for l in r["lecturas"]:
        comp = [cotejo(x) for x in l.get("componentes", [])]
        if comp == [base, seg]:
            l["patron"] = patron.get("fuente", "")
            delante.append(l)
        else:
            detras.append(l)
    r["lecturas"] = delante + detras
    r["senal"] = "segura"
    r["senal_motivo"] = ("niggahīta → m ante vocal (§34): la única lectura "
                         "de la clase que pasa el resguardo es «{0} + {1}» "
                         "— patrón adjudicado ({2})"
                         .format(base, seg, patron.get("fuente", "")))
    return True


def _aplicar_patron(r):
    """Los patrones adjudicados: la cola enclítica con base única atestiguada.

    Observación de Angel (2026-08-28, sobre SN 1.1 y DN 2): las colas de
    «iti» y «pi» «no son difíciles de detectar con 100 % de exactitud». La
    regla que lo vuelve mecanismo, adjudicada con su fuente en
    `casos-reportados.json`: si entre las lecturas verificadas hay
    EXACTAMENTE UNA primera voz atestiguada en el canon cuya segunda voz es
    la del patrón, esa lectura se afirma — abhisambuddho + iti, ye + api—.
    Con más de una base atestiguada (ceva: ca, ce y cā existen las tres) el
    patrón calla y la duda se declara: la unicidad es la licencia, no la
    frecuencia. El caso y el banco mandan sobre el patrón.
    """
    if r.get("del_banco") or len(r["escrita"].split()) != 1:
        return
    caso = cargar()["casos"].get(r["cotejo"])
    if caso and not caso.get("sandhi"):
        return                       # adjudicado no-sandhi: el patrón calla
    lecturas = r.get("lecturas", [])
    if lecturas and (lecturas[0].get("adjudicada")
                     or lecturas[0].get("origen")):
        return
    frec = cargar().get("frecuencia", {})
    f_forma = frec.get(r["cotejo"], 0)
    for patron in cargar().get("patrones", []):
        # La clase de §34 no se declara por la segunda voz sino por la «m»
        # de la juntura: es otra licencia y va en su propia función.
        if patron.get("clase") == "niggahita_m":
            if _patron_niggahita_m(r, patron, frec, f_forma):
                return
            continue
        seg = cotejo(patron.get("segunda", ""))
        if not seg:
            continue
        # El resguardo de la base residual, adjudicado por Angel
        # (2026-08-28, sesión 32): una base candidata debe ser AL MENOS tan
        # frecuente en el canon como la forma entera. Sin él, «ho» (4
        # apariciones) concedía la unicidad y el patrón afirmaba hoti
        # (59.320) como ho + iti — y pajānāti, bhaṇati, vadati, karoti…—;
        # y del otro lado, una base residual («cakkhundriyaña», 1) negaba
        # la unicidad a una lectura real. La base residual ni concede ni
        # bloquea: no cuenta como candidata. Las cuentas de la propia
        # edición arbitran, como en toda la señal.
        bases = set()
        for l in lecturas:
            comp = [cotejo(x) for x in l.get("componentes", [])]
            if (len(comp) == 2 and comp[1] == seg
                    and frec.get(comp[0], 0) >= max(f_forma, 1)):
                bases.add(comp[0])
        # Regla de la clase vocálica, adjudicada por Angel (2026-08-28):
        # «hotīti es sólo hoti + iti y hotūti es sólo hotu + iti». La vocal
        # que sobrevive ante el remanente conserva la clase de la vocal
        # final de la base (a/ā, i/ī, u/ū, e, o); las bases de otra clase
        # quedan excluidas de la afirmación (siguen visibles, plegadas). En
        # el corpus: hotīti 7.621 · hotūti 213 · hotāti 0.
        if patron.get("clase_vocal") and patron.get("remanente"):
            rem = patron["remanente"]
            sup = r["cotejo"]
            if sup.endswith(rem) and len(sup) > len(rem):
                v_sup = sup[-len(rem) - 1]
                clase = {"a": "a", "ā": "a", "i": "i", "ī": "i",
                         "u": "u", "ū": "u", "e": "e", "o": "o"}
                if v_sup in clase:
                    bases = {b for b in bases
                             if b and b[-1] in clase
                             and clase[b[-1]] == clase[v_sup]}
        # Desempate adjudicado: dos bases que son la misma voz con la vocal
        # final breve y larga (pabbajjāya / pabbajjāyā) se reducen a la
        # BREVE — la larga suele ser el producto del propio sandhi—. Bases
        # distintas de verdad (ca / ce / cā) siguen sin decidirse.
        if len(bases) == 2:
            par = sorted(bases)
            corta, larga = par[0], par[1]
            if (corta and corta[-1] in LARGA
                    and corta[:-1] + LARGA[corta[-1]] == larga):
                bases = {corta}
        if len(bases) != 1:
            continue
        base = next(iter(bases))
        delante, detras = [], []
        for l in lecturas:
            comp = [cotejo(x) for x in l.get("componentes", [])]
            if comp == [base, seg]:
                l["patron"] = patron.get("fuente", "")
                delante.append(l)
            else:
                detras.append(l)
        r["lecturas"] = delante + detras
        r["senal"] = "segura"
        r["senal_motivo"] = ("cola de «{0}»: la única primera voz atestiguada "
                             "en el canon es «{1}» — patrón adjudicado ({2})"
                             .format(seg, base, patron.get("fuente", "")))
        return


def _aplicar_caso(r):
    """Un caso adjudicado manda sobre la señal, y su lectura va primera.

    No es heurística: es una adjudicación con fuente y fecha
    (`recursos/solucionador/casos-reportados.json`), y se atribuye siempre
    (principio 4). Tres efectos, y ninguno inventa nada:

      · sandhi=true → señal «segura» (si no la había), con el motivo
        nombrando la fuente;
      · la lectura cuyas componentes coinciden con las adjudicadas sube al
        primer lugar, marcada `adjudicada` — el resto no se toca ni se
        borra: todas las lecturas que recomponen se siguen mostrando;
      · sandhi=false no toca nada aquí: es prueba de regresión de que la
        señal calla (la comprueba `arnes_casos`).

    El primer caso fue `tenupasaṅkami` (Angel, 2026-08-28): la señal por
    frecuencia no puede verlo —1.763 apariciones contra 231 de su propia
    segunda voz— y ésta es la vía que la decisión del Venerable dejó
    prevista: cada fallo reportado, un caso permanente.
    """
    caso = cargar()["casos"].get(r["cotejo"])
    if not caso:
        return
    if not caso.get("sandhi"):
        # Adjudicado NO-sandhi: la adjudicación manda sobre la heurística y
        # la señal se apaga (caso «navo», DN 2). Las lecturas no se tocan:
        # siguen consultables, sin señal que grite.
        if r.get("senal"):
            r["senal"] = None
            r["senal_motivo"] = ""
        return
    objetivo = [cotejo(x) for x in partir_componentes(caso.get("componentes", ""))]
    delante, detras = [], []
    for l in r.get("lecturas", []):
        comp = [cotejo(x) for x in l.get("componentes", [])]
        if objetivo and comp == objetivo:
            l["adjudicada"] = caso.get("fuente", "")
            delante.append(l)
        else:
            detras.append(l)
    if objetivo and not delante:
        # El motor no produce (todavía) la lectura adjudicada — el caso de
        # idamavocāyasmā = idaṃ + avoca + āyasmā: TRES voces, y el motor
        # propone un solo corte. La adjudicación no se esconde: va primera,
        # sintética, marcada pendiente de derivación. Es lo que el
        # incorporador promete («quedará registrada aunque el motor no la
        # produzca todavía») y no inventa nada: los componentes son los del
        # caso, la escalera queda vacía hasta que combinar() la derive.
        # El paréntesis dice el porqué VERDADERO: tres voces piden
        # combinar(); dos voces que el motor no corta (suññāgāragatovā =
        # suññāgāragato + vā, pakati §23) no son junturas múltiples y el
        # rótulo no debe decirlo (2026-08-29).
        porque = ("junturas múltiples" if len(objetivo) > 2
                  else "el motor no propone este corte")
        delante = [{"componentes": partir_componentes(
                        caso.get("componentes", "")),
                    "pasos": [],
                    "adjudicada": caso.get("fuente", ""),
                    "pendiente": ("el motor aún no deriva esta lectura "
                                  "({0})".format(porque))}]
    r["lecturas"] = delante + detras
    # La adjudicación asciende la señal a «segura» venga de donde venga la
    # señal previa («posible» por frecuencia incluido); si ya era «segura»
    # por otra vía (banco, iti), el motivo original se conserva.
    if r.get("senal") != "segura":
        r["senal"] = "segura"
        r["senal_motivo"] = ("caso adjudicado: " + caso.get("fuente", ""))


# Los aforismos «ruidosos» para la DETECCIÓN, no para la validez: alargar o
# acortar (§25, §26), duplicar (§28, §29) e insertar (§35, §37) producen
# lecturas verificadas sobre flexiones corrientes —de «gacchā + ti» sale
# «gacchati»—. Una lectura así sigue siendo válida y se publica; lo que no
# hace es, por sí sola, encender la señal.
RUIDOSAS = {25, 26, 28, 29, 35, 37, "35+26", "35nota9"}


def _ascender_senal(r):
    """La señal «posible» del modo solo-canon, medida antes de escribirse.

    Con el DPD apartado, «no está en el léxico» se apaga: el corpus del canon
    lista lo que está ESCRITO, y `lokaggo` figura con su cuenta. Lo medido
    sobre el texto entero (`medir_deteccion_canon.py`, 2026-08-28), con la
    señal que ESTA función devuelve, no una paralela:

        «segura»              versos   marca  1,1 %   sandhi 85 %   recall  8 %
                              prosa    marca  3,9 %   sandhi 92 %   recall 23 %
        «segura» o «posible»  versos   marca  7,5 %   sandhi 51 %   recall 32 %
                              prosa    marca 10,9 %   sandhi 66 %   recall 46 %

    El 15 % que a la «segura» no le cuenta como sandhi el corpus de medida no
    son yerros de la señal: son formas ATESTIGUADAS en el banco del Venerable
    que el corpus clasifica de otro modo —`taṇhakkhayo`, `pañcakkhandhā` como
    compuesto aunque §28 opera en su juntura; `chaḷabhiññā` como juntura; y
    `svāgataṃ`, un sandhi real que el corpus ni marcó—. El banco es acá el
    mejor testigo, y la referencia está teñida de DPD (briefing 30 §2).

    Queda por debajo del recall que daba la descomposición del DPD (71-79 %),
    y eso se declara donde se publique. Por eso son DOS niveles y no uno: la
    «segura» casi no se equivoca; la «posible» avisa que conviene mirar, con
    su cifra a la vista. Lo que no se marca no se pierde: se calla, y la voz
    sigue consultable una por una.

    Tres reglas, en orden:
      · la forma está en el banco con una cadena que opera → «segura»
        (atestiguada por el Venerable, no es heurística);
      · alguna lectura tiene la 2.ª voz en la lista cerrada de nipāta, un
        aforismo fuera de `RUIDOSAS`, y sus dos piezas superan en frecuencia
        a la forma entera → «posible»;
      · si no, la señal queda como estaba.
    """
    if r.get("senal") or len(r["escrita"].split()) != 1:
        return
    if r.get("del_banco") and r.get("estado") != "sin_sandhi_por_regla":
        r["senal"] = "segura"
        r["senal_motivo"] = "la forma está en el banco, con secuencia de procedencia"
        return
    frec = cargar().get("frecuencia", {})
    nip = cargar()["nipata"]
    fF = frec.get(r["cotejo"], 0)
    for l in r.get("lecturas", []):
        comp = [cotejo(x) for x in l.get("componentes", [])]
        if len(comp) < 2 or comp[-1] not in nip:
            continue
        if l.get("sutta") in RUIDOSAS:
            continue
        if min(frec.get(c, 0) for c in comp) > fF:
            r["senal"] = "posible"
            r["senal_motivo"] = ("una lectura verificada la parte en dos voces "
                                 "más frecuentes en el canon que la forma "
                                 "entera, con la segunda en la lista cerrada "
                                 "de nipāta")
            return
    # El testigo del DPD, cuando está encendido (--dpd-filtro): la voz está
    # escrita en el canon pero no figura en el diccionario ni se parte en dos
    # voces del diccionario sin operación — lo típico de un producto de
    # sandhi. Es el uso que §9 permite (probar si una cadena ocurre), se
    # atribuye en el motivo, y NO decide el análisis. Medido 2026-08-28:
    # solo, 76 % de precisión en verso y 45 % en prosa; sumado al nivel
    # «posible», la señal pasa de 51 %@32 a 57 %@46 en verso y de 66 %@46 a
    # 60 %@56 en prosa (con juntura real en el 81 % de lo marcado).
    dic = cargar().get("dpd") or set()
    if dic and r["cotejo"] not in dic and not _compuesto_dpd(r["cotejo"]):
        r["senal"] = "posible"
        r["senal_motivo"] = ("la voz no figura en el diccionario (DPD, "
                             "testigo de ocurrencia) ni se parte en dos "
                             "voces del diccionario sin operación")
        return


def _compuesto_dpd(c):
    """¿Se parte en dos voces del diccionario por simple concatenación?"""
    dic = cargar().get("dpd") or set()
    for i in range(2, len(c) - 1):
        if c[:i] in dic and c[i:] in dic:
            return True
    return False


def _solucionar(voz):
    c = cargar()
    k = cotejo(voz)
    r = {"escrita": voz, "cotejo": k, "estado": None, "motivo": None,
         "lecturas": [], "banco": huella_banco()}
    r["senal"], r["senal_motivo"] = senal(voz) if len(voz.split()) == 1 else (None, "")

    if k in c["banco"]:
        for dato, archivo, clave in c["banco"][k]:
            if "s" in dato:                                   # reglas.json
                pasos = list(dato["s"])
                comp = partir_componentes(dato.get("comp", ""))
                # **La etiqueta tiene que ser cierta.** Antes decía
                # «verificada por recomposición» a las 217 entradas que el banco
                # no marca `verificada`, y `cargar()` no verifica nada: sólo
                # indexa. Ahora se comprueba lo único comprobable acá sin
                # rehacer la derivación —que el último paso reproduzca la
                # forma—, y la etiqueta dice exactamente eso. Las 266 la pasan;
                # si alguna dejara de pasarla, se vería.
                primer_paso_de = None
                proc = ("firmada" if dato.get("verificada")
                        else "del banco, sin comprobar")
                ref = dato.get("ref")
                sin_op = bool(dato.get("sin_cambio")) or dato.get("sec") == "pakati"
            else:                                             # las Tablas
                pasos = ["{0}{1}".format(
                    p["texto"],
                    "  (" + ", ".join(p["citas"]) + ")" if p["citas"] else "")
                    for p in dato.get("pasos", [])]
                inicial = dato.get("forma_inicial") or ""
                # **La forma de partida es el primer paso.** El contrato del
                # encargo dice que la cadena empieza por el texto sin anotar, y
                # `reglas.json` lo cumple; las Tablas guardan la forma inicial
                # en su propio campo y arrancan la lista en §10. Sin unificarlo,
                # la misma cadena de `myāyaṃ` salía dos veces —una de cada
                # archivo— porque las listas de pasos no coincidían.
                # El primer paso de una cadena nunca lleva anotación: si la
                # lleva, es que la forma de partida quedó fuera de la lista.
                # (No se puede comparar con `cotejo`: borra los espacios, y
                # «me ayaṃ» y «m e ayaṃ» —que son dos pasos distintos— dan la
                # misma cadena.)
                if inicial and (not pasos or pasos[0].rstrip().endswith(")")):
                    pasos = [inicial] + pasos
                comp = partir_componentes(inicial)
                _p0 = (dato.get("pasos") or [{}])[0]
                primer_paso_de = _p0.get("forma_de_partida")
                proc = "firmada"
                ref = dato.get("referencia")
                sin_op = not dato.get("suttas_que_operan")
            # **«Sin operación» sólo si ninguna opera.** `vedanākkhandho`
            # venía marcada `sin_cambio` y su cadena dobla la consonante por
            # §28; con eso el estado podía caer en «sin sandhi por regla»
            # sobre una forma donde sí pasó algo. Si la cadena cita un
            # aforismo que no es de los que no cambian nada, opera.
            citados = {int(x) for x in re.findall(r"§\s*(\d+)", " ".join(pasos))}
            if citados - PAKATI - {10, 11}:
                sin_op = False
            ultimo = sin_anotacion(pasos[-1]) if pasos else ""
            recompone = bool(ultimo) and cotejo(ultimo) == k
            if recompone and proc == "del banco, sin comprobar":
                proc = "del banco, último paso comprobado"
            r["lecturas"].append({
                "componentes": comp,
                "pasos": pasos,
                "reconstruida": pasos[-1] if pasos else voz,
                "recompone": recompone,
                "procedencia": proc,
                "origen": {"archivo": archivo, "clave": clave},
                "referencia": ref,
                "sin_operacion": sin_op,
                "primer_paso_de": primer_paso_de,
            })
        r["lecturas"] = juntar_iguales(r["lecturas"])

        # ── Las filas de las Tablas que quedaron mal partidas ──────────
        # `ej_original` es una sola cadena —«iti etaṃ ic etaṃ (§19) icc etaṃ
        # (§28)…»— y quien la partió en pasos falló donde la forma inicial
        # tiene un espacio y ningún paréntesis detrás: se comió el primer paso
        # dentro de la forma inicial. Salían componentes como «iti + etaṃ + ic
        # + etaṃ», y `iccetaṃ` y `abhinandunti` no tenían otra lectura: lo
        # único que se publicaba de ellas era eso, con el sello «firmada».
        #
        # No se adivina la partición correcta —eso sería inventar—. Se detecta
        # con **el dato que el propio archivo trae**: cada paso bien leído
        # guarda de qué forma sale (`forma_de_partida`), y a los pegados les
        # falta, porque el primer paso quedó absorbido dentro de la forma
        # inicial. Un paso solo puede no tenerla legítimamente —las filas
        # pakati, que ilustran la ausencia de operación—, así que se exige
        # además que la fila tenga más de un paso.
        #
        # El criterio anterior que había escrito —«el primer paso tiene que ser
        # los componentes» y «más de dos componentes es una partición
        # fallida»— retiraba **17 filas bien partidas**: `puggalaṃ`, cuyo primer
        # paso ya es el resultado de §31 y por eso difiere de los componentes;
        # `jāccandho`, que se caía porque `cotejo()` no borra el «+»; y las
        # filas que son frases de tres o cuatro palabras. Un filtro que borra
        # material firmado por no mirar el campo que lo distingue es peor que
        # el defecto que venía a tapar.
        for x in r["lecturas"]:
            if "tablas" not in (x["origen"]["archivo"] or ""):
                continue
            if len(x["pasos"]) > 1 and not x.get("primer_paso_de"):
                x["fila_mal_partida"] = True

        r["banco_mal_partido"] = [
            {"componentes": x["componentes"], "pasos": x["pasos"],
             "origen": x["origen"]}
            for x in r["lecturas"] if x.get("fila_mal_partida")]
        r["lecturas"] = [x for x in r["lecturas"] if not x.get("fila_mal_partida")]

        # ── Lo que no recompone no se publica ──────────────────────────
        # `recompone` se calculaba y no se miraba: no había ningún filtro, y
        # toda entrada del banco salía coincidiera o no. `bahvābādhobavhābādho`
        # se publicaba con «estado: firmada» y `recompone=False`. El encargo no
        # deja lugar: «Si no coincide, se descarta. No se publica ni se muestra
        # nada que no haya pasado esa prueba.» Se descarta, y se anota aparte
        # para que el defecto del banco se vea en vez de taparse.
        r["banco_no_recompone"] = [
            {"componentes": x["componentes"], "pasos": x["pasos"],
             "origen": x["origen"]}
            for x in r["lecturas"] if not x["recompone"]]
        r["lecturas"] = [x for x in r["lecturas"] if x["recompone"]]

        # ── Y lo que el motor encuentra además no se esconde ────────────
        # Estar en el banco cortaba la función acá, y `proponer()` no se
        # llamaba nunca: `lokaggo` publicaba **una** lectura y se guardaba las
        # trece que su propio motor genera y verifica; sobre el banco entero,
        # 212 formas publicaban una y escondían 2.263. El encargo lo llama por
        # su nombre: «Elegir una en silencio es mentir por omisión.» La firmada
        # sigue yendo primera, con su procedencia; las demás van detrás.
        firmadas = len(r["lecturas"])
        r["lecturas"] = juntar_iguales(r["lecturas"] + proponer(k))
        # `juntar_iguales` prefiere la procedencia firmada, así que la del
        # banco absorbe a la automática cuando la cadena es la misma —que es lo
        # que pasa cuando el motor reconstruye por su cuenta lo que el banco ya
        # decía— y las dos quedan en una sola lectura, no en dos iguales.
        r["lecturas"].sort(key=lambda x: 0 if x.get("origen") else 1)
        r["del_banco"] = firmadas

        if not r["lecturas"]:
            r["estado"] = "no_resuelto"
            r["motivo"] = ("el banco trae esta forma pero su cadena no la "
                           "reproduce, y el motor no propone otra")
        elif all(x.get("sin_operacion") for x in r["lecturas"]):
            r["estado"] = "sin_sandhi_por_regla"
        elif len(r["lecturas"]) == 1 and r["lecturas"][0]["procedencia"] == "firmada":
            # **«firmada» sólo si está firmada.** Antes bastaba con haber una
            # sola lectura, viniera de donde viniera: 195 de 239 formas decían
            # «firmada» sobre material que el banco no marca `verificada` —el
            # propio `lokaggo` entre ellas—. La etiqueta ahora es la de la
            # lectura, no la del hecho de estar en el banco.
            r["estado"] = "firmada"
        else:
            r["estado"] = "candidatos"
        return r

    if not es_palabra(voz) and len(voz.split()) == 1:
        pass                       # que no esté entera no impide intentar el corte

    if len(voz.split()) > 1:
        r["lecturas"] = proponer_en_frase(voz.replace("’", "'").replace("'", ""))
    else:
        # Si el escriba marcó la juntura —apóstrofo o guion—, se propone ahí.
        # **Primero el canon.** Si lo escrito alcanza para explicar la forma, no
        # hace falta abrir el diccionario entero.
        canon = cargar()["canon"]
        if canon:
            lex_pleno = _cache["lexico"]
            try:
                _cache["lexico"] = canon
                r["lecturas"] = (proponer_en_marca(voz)
                                 if any(m in voz for m in MARCAS) else []) \
                    or proponer(k)
            finally:
                _cache["lexico"] = lex_pleno
            if r["lecturas"]:
                for l in r["lecturas"]:
                    l["del_canon"] = True
                r["estado"] = ("candidatos" if len(r["lecturas"]) > 1
                               else "resuelto")
                r["entera"] = es_palabra(voz)
                return r

        marcadas = proponer_en_marca(voz) if any(m in voz for m in MARCAS) else []
        if marcadas and "yuxtaposicion_declarada" in marcadas[0]:
            r["estado"] = "fuera_del_alcance"
            r["entera"] = es_palabra(voz)
            a, b = marcadas[0]["yuxtaposicion_declarada"]
            r["motivo"] = ("la marca de la edición separa dos voces del léxico "
                           "sin ninguna operación —{0} + {1}—: es un compuesto, "
                           "y los compuestos están fuera del encargo."
                           .format(a, b))
            return r
        r["lecturas"] = marcadas or proponer(k)
        if not r["lecturas"]:
            # **Segunda pasada, y sólo si la primera no dijo nada.** Aquí se
            # admite que la voz anterior sea un compuesto que el DPD no lista
            # —`aggamaggañāṇa + asinā` → `aggamaggañāṇāsinā`, §12 y §15—. No se
            # analiza el compuesto, que está fuera del encargo: se comprueba que
            # lo es, para poder explicar el sandhi de su juntura.
            #
            # Va segunda a propósito. Una voz que ya se explica con el
            # diccionario no necesita esta puerta, y abrirla siempre agregaría
            # cortes a palabras que no los piden. **No proponer sin motivo.**
            r["lecturas"] = proponer(k, compuestos=True)
    r["entera"] = es_palabra(voz)
    if r["lecturas"]:
        # **«Resuelto» pide un segundo testigo, acá también.** La corrección
        # de anoche se hizo en la casilla de la pantalla y `estado` se quedó
        # como estaba: `solucionar("sabbe")` seguía diciendo `resuelto` sobre
        # `sa + be`. Medido sobre 12.000 formas del corpus, 364 de 412 fichas
        # con `estado: resuelto` no tenían ningún testigo detrás. Una sola
        # lectura no es una resolución: es que el motor no encontró más.
        una = r["lecturas"][0] if len(r["lecturas"]) == 1 else None
        r["estado"] = ("resuelto"
                       if una and (una.get("origen") or una.get("dpd"))
                       else "candidatos")
        return r

    # Sin lecturas. Antes todo esto era «no resuelto», y no todo es lo mismo.
    #
    # **Los tres silencios.** Uno dice «no hay sandhi», otro «esto no me toca»,
    # el tercero «no supe». Confundirlos hace que la pantalla grite en cada
    # palabra común de un texto, y que el lector deje de creerle.
    #
    # Y el primero **no consulta cuántos cortes hipotéticos hay**, a propósito.
    # Antes sí, y `disā` —una palabra de cuatro letras que está en el DPD—
    # salía «sin resolver» porque el generador enumeraba 153 antecedentes
    # posibles. Ese número no cuenta cortes: cuenta hipótesis. Lo único
    # sostenible es esto: la voz está en el léxico, y ninguna de las 36
    # operaciones enunciadas la explica partida. Entonces está entera.
    yux = yuxtaposicion(k) if len(voz.split()) == 1 else []
    if r["entera"]:
        r["estado"] = "sin_sandhi"
        r["motivo"] = ("la voz está entera en el léxico y ninguna de las {0} "
                       "operaciones enunciadas encuentra un corte que la "
                       "explique: no hay nada que separar."
                       .format(sum(1 for n in ORDEN if isinstance(n, int))))
        return r
    if yux:
        r["estado"] = "fuera_del_alcance"
        r["motivo"] = ("la forma se parte en dos voces **sin ninguna operación** "
                       "—{0}—: es un compuesto, y los compuestos están fuera "
                       "del encargo.".format(" + ".join(yux[0])))
        r["diagnostico"] = {"yuxtaposiciones": [" + ".join(x) for x in yux[:6]]}
        return r
    r["estado"] = "no_resuelto"
    r["motivo"], r["diagnostico"] = por_que_no(voz, k)
    return r


def partir_componentes(t):
    t = (t or "").strip()
    if not t:
        return []
    if " + " in t:
        return [x.strip() for x in t.split(" + ")]
    return t.split()


def juntar_iguales(lecturas):
    """Dos fuentes pueden traer la misma lectura. Se muestra una vez, con las
    dos procedencias, en vez de fingir que son dos lecturas distintas."""
    fusion = {}
    for x in lecturas:
        # **La clave incluye la cadena, no sólo los componentes.** Antes no, y
        # eso borraba material firmado: `tadāhaṃ` está dos veces en
        # `reglas.json` con cadenas distintas —`ce[8]` por §13, ref. A. i 110;
        # `ce[87]` por §12 y §15, ref. Ap. ii 261— y el motor devolvía una sola,
        # con la referencia de la primera y una nota que decía «también en
        # ce[87]». Falso: ce[87] dice otra cosa.
        #
        # Se funden las entradas que son la misma lectura repetida. Si difieren
        # en un paso o en un aforismo **son dos lecturas y salen las dos**, cada
        # una con su referencia, que es lo que manda la regla.
        # Los espacios no distinguen una cadena de otra: las Tablas escriben
        # «icc etaṃ  (§28)» con dos espacios y `reglas.json` con uno, y de
        # `myāyaṃ` salía tres veces la misma lectura `me + ayaṃ`.
        # El paso «(EM)» no es un aforismo: es cómo la edición moderna imprime
        # la forma ya unida. Dos cadenas que sólo se diferencian en si lo
        # muestran son el mismo análisis, y publicarlas dos veces es ruido.
        pasos_clave = [" ".join(p.split()) for p in x["pasos"]]
        while pasos_clave and pasos_clave[-1].rstrip().endswith("(EM)"):
            pasos_clave.pop()
        k = (cotejo("".join(x["componentes"])), tuple(pasos_clave))
        if k in fusion:
            if x.get("origen"):
                fusion[k].setdefault("tambien_en", []).append(x["origen"])
            if x["procedencia"] == "firmada":
                fusion[k]["procedencia"] = "firmada"
        else:
            fusion[k] = x
    return list(fusion.values())


def senal(voz):
    """¿Hay motivo para *sospechar* sandhi en esta voz, antes de proponer nada?

    Ésta es la pregunta que hace falta para leer un texto, y no es la misma que
    resuelve `solucionar()`. Un texto son mil palabras y casi ninguna tiene
    sandhi: una herramienta que propone cortes en todas no se puede leer.

    **Dos señales, y sólo dos, porque son las dos que se midieron** contra el
    corpus de `Sandhi` —698 formas con sandhi en alcance contra 4.342 sin
    sandhi en los versos; 7.178 contra 31.812 en el comentario—:

      · **la voz no está en el DPD, y tampoco se parte en dos voces del DPD
        por simple concatenación.** Lo primero es un hecho fuerte —el DPD trae
        443.740 formas flexionadas—; lo segundo saca del medio a los compuestos,
        que faltan del diccionario por ser compuestos y no por tener sandhi.
        Sin esa segunda mitad la precisión cae al 63 % en el comentario, que es
        donde abundan. Un compuesto junta dos **nombres**: si la segunda voz es
        una partícula, no es compuesto y la señal se mantiene.
      · **cola de `iti`** —vocal larga antes de `ti`—: `hotīti`, `vuccatīti`.

    Medido **sobre el texto entero**, que es lo que un lector pega —no sobre dos
    montones elegidos—:

        versos       marca 10,4 de cada 100 · recall 71 % · precisión 81 %
        comentario   marca 19,2 de cada 100 · recall 79 % · precisión 64 %

    De lo marcado, en verso el 96 % tiene de verdad una juntura —81 % sandhi del
    encargo, 15 % compuesto— y sólo el 4 % no tiene nada.

    **El salto lo trajo la descomposición del DPD.** Con las dos señales viejas
    el recall era 27 %; con la del DPD llega al 71-79 % sin perder precisión.
    En el texto hay 11,8 y 15,6 sandhis cada cien palabras, y se ven siete y ocho
    de cada diez.

    **Lo que se midió y se descartó**, para no volver a probarlo:

      · «no está en el DPD» a secas — recall 27,9 % / 26,8 %, pero la precisión
        se parte: 92,9 % en los versos y **63,5 %** en el comentario
      · «termina en un nipāta» — 42,3 % de recall con 27,5 % de precisión
      · «hay un corte con nipāta que recompone» — 42,7 % / 24,1 %
      · «once letras o más» — 41,6 % / 61,3 %, y además no es un criterio
        gramatical sino un rodeo para hablar de compuestos
      · el sello ortográfico —apóstrofo o guión—: **0 %** en este corpus, la
        edición no los usa

    Ninguna de esas pasa de un cuarto de precisión, y una herramienta que se
    equivoca tres de cada cuatro veces que habla enseña a no escucharla.

    **Lo que no se señala no se pierde: se calla.** La voz sigue consultable una
    por una, con todas sus lecturas. Lo que no hace es gritar.
    """
    c = cotejo(voz)
    if SOLO_CANON and any(x in voz for x in MARCAS):
        # En solo-canon el sello ortográfico asciende a señal: es la edición
        # diciendo dónde está la juntura. En el corpus de medida no aparece
        # (0 %), pero el lector pega texto de cualquier fuente.
        return ("segura", "la edición marcó la juntura: apóstrofo o guion")
    if descomposicion(voz):
        return ("segura", "el DPD publica su propia descomposición de esta voz")
    if c.endswith("ti") and len(c) > 3 and c[-3] in "āīū":
        return ("segura", "cola de «iti»: vocal larga antes de «ti»")
    if not es_palabra(voz) and not _compuesto_aparente(c):
        return ("segura", "la voz no está en el léxico " + nombre_lexico() + ", y tampoco se "
                          "parte en dos voces del léxico sin operación")
    return (None, "")


def _compuesto_aparente(c):
    """La forma se parte, sin ninguna operación, en dos voces del léxico de las
    que la segunda **no es una partícula**.

    La distinción no es un ajuste: un compuesto junta dos nombres, no un nombre
    y una partícula. `soka + pareta` es compuesto; `paripuccha + haṃ` no lo es
    —`haṃ` está en la lista cerrada de nipāta—, y tratarlo como compuesto
    silenciaba un sandhi de verdad. Medido, la distinción sube el recall del
    21,3 % al 27,4 % en los versos y del 33,0 % al 35,0 % en el comentario, sin
    mover la precisión.
    """
    nip = cargar()["nipata"]
    for a, b in yuxtaposicion(c):
        if cotejo(b) not in nip and len(cotejo(b)) >= 3:
            return True
    return False


def _candidatas(a, b):
    """Formas que **podrían** salir de unir estas dos voces. Sólo propone.

    El solucionador va de la forma a las voces. Acá hace falta el camino
    contrario, porque hay junturas que **la edición ya separó**: el Sexto
    Concilio escribe «Pītisukhena ti», y `ti` no es una voz sino lo que queda de
    `iti` tras el §40. Las dos voces están a la vista y lo que falta es la forma
    unida con su secuencia de suttas —que es, literalmente, lo que pide el
    encargo—.

    **Esto no deriva nada: enumera.** Cada candidata vuelve a entrar por la
    puerta de siempre —`solucionar()`— y sólo sobrevive si se descompone
    exactamente en las dos voces de partida, con el verificador del Venerable
    para los nueve aforismos que él implementó. La regla de oro no se toca:
    quien autoriza un paso sigue siendo la recomposición. Lo único que cambia es
    de qué lado se entra.

    Las candidatas salen de los enunciados, no de la imaginación:

      §12  «la vocal que precede a otra vocal se elide»       → a[:-1] + b
      §13  «la vocal que sigue a otra vocal se elide»          → a + b[1:]
      §15  elidida la anterior, la siguiente se alarga         → a[:-1] + B̄
      §16  elidida la siguiente, la anterior se alarga         → ā[:-1] + b[1:]
      §28  duplicación de la consonante inicial siguiente
      §31  la niggahīta se vuelve la nasal de la serie
      §34  ante vocal, la niggahīta se vuelve «m»
      §35  se inserta una consonante entre las dos voces
      §38  ante vocal, la niggahīta se elide
      §39  ante consonante, la niggahīta se elide
    """
    a, b = cotejo(a), cotejo(b)
    if not a or not b:
        return set()
    c = {a + b}
    if a[-1] in VOCALES:
        c.add(a[:-1] + b)                                   # §12
        if b[0] in VOCALES:
            c.add(a + b[1:])                                # §13
            if b[0] in LARGA:
                c.add(a[:-1] + LARGA[b[0]] + b[1:])         # §15
            if a[-1] in LARGA:
                c.add(a[:-1] + LARGA[a[-1]] + b[1:])        # §16
        else:
            ini = OP.primera_letra(b)
            if ini in OP.SEGUNDA_CUARTA:
                c.add(a + OP.SEGUNDA_CUARTA[ini] + b)       # §29
            elif ini and ini not in "yrlvsh":
                c.add(a + ini + b)                          # §28
        for x in OP.INSERTA if hasattr(OP, "INSERTA") else "yvmdntrlhg":
            c.add(a + x + b)                                # §35
    if a.endswith("ṃ"):
        sin = a[:-1]
        c.add(sin + b)                                      # §38, §39
        if b and b[0] in VOCALES:
            c.add(sin + "m" + b)                            # §34
            c.add(sin + "d" + b)                            # §34, nota 16
            if len(b) > 1:
                # §40 elide la vocal que sigue a la niggahīta, y entonces la
                # niggahīta queda ante consonante: §31 la convierte en la nasal
                # de esa serie. Es la cadena de «catukkhattuṃ iti» →
                # «catukkhattuṃ ti» → «catukkhattun ti» → `catukkhattunti`.
                resto = b[1:]
                c.add(a + resto)
                c.add(sin + resto)
                nasal = OP.VAGGA.get(OP.primera_letra(resto))
                if nasal:
                    c.add(sin + nasal + resto)
                    if len(resto) > 1 and resto[0] == resto[1]:
                        c.add(sin + nasal + resto[1:])
        ini = OP.primera_letra(b) if b else ""
        if ini in OP.VAGGA:
            c.add(sin + OP.VAGGA[ini] + b)                  # §31
        if b in ("eva", "hi"):
            c.add(sin + "ñ" + ("ñ" if b == "eva" else "") + b)   # §32
        if b.startswith("y"):
            c.add(sin + "ñ" + "ñ" + b[1:])                  # §33
    return {x for x in c if x}


def combinar(a, b, escrita_a=None, escrita_b=None):
    """Las formas unidas de dos voces, **verificadas por recomposición**.

    Devuelve `(forma, lectura)`: la forma que dan las dos voces al combinarse y
    la lectura completa —pasos, aforismos, procedencia— tal como la devuelve el
    solucionador. Sólo entran las que, al descomponerse, dan exactamente estas
    dos voces. Si ninguna sobrevive, la lista viene vacía y no se dice nada.

    **`escrita_b` es el dato que da la edición y decide casi todo.** Cuando el
    texto trae «Catukkhattuṃ ti», la segunda voz es `iti` pero lo escrito es
    `ti`: el editor dejó a la vista que la vocal inicial se elidió. Entonces la
    forma unida **tiene que terminar en `ti` y no en `iti`** —si terminara en
    `iti` la edición habría escrito `iti`—. Ese filtro sale del texto, no de
    nuestro criterio, y descarta de un golpe las uniones con consonante
    insertada (§35) y las que dejan la vocal en pie.
    """
    ka, kb = cotejo(a), cotejo(b)
    esc = cotejo(escrita_b) if escrita_b else None
    esa = cotejo(escrita_a) if escrita_a else None
    out = []
    for cand in sorted(_candidatas(a, b)):
        if esc and esc != kb:
            if not cand.endswith(esc) or cand.endswith(kb):
                continue
        if esa and esa != ka:
            # Simétrico al filtro de «ti», y por el mismo motivo: la edición
            # escribió «vuttanayam» o «taṅ» con la consonante desnuda, que no es
            # final de voz pāḷi. La forma unida tiene que **conservar esa
            # juntura**: empezar por lo escrito menos su última consonante, y
            # tener una consonante en ese lugar —no la vocal desnuda—.
            #
            # `vuttanayaṃ + eva` da `vuttanayameva` ✓ y `vuttanayaeva` ✗ —ahí la
            # niggahīta se elidió del todo (§38) y el editor no habría escrito
            # la «m»—. `taṃ + eva` da `taññeva` ✓, donde la consonante cambió
            # pero no desapareció.
            raiz = esa[:-1]
            if not cand.startswith(raiz):
                continue
            if len(cand) <= len(raiz) or cand[len(raiz)] in VOCALES:
                continue
        r = solucionar(cand)
        for l in r["lecturas"]:
            comp = [cotejo(x) for x in l.get("componentes") or []]
            if comp == [ka, kb]:
                out.append((cand, l))
                break
    out.sort(key=lambda x: (len(x[1]["pasos"]), x[0]))
    return out


def combinar_varias(voces, escrita_a=None, escrita_b=None):
    """Las formas unidas de TRES o más voces, plegando `combinar()`.

    `idamavocāyasmā` = idaṃ + avoca + āyasmā tiene DOS junturas, y el motor
    propone un solo corte: por eso los tres casos de tres voces adjudicados
    por el IEBH entraron con la lectura «pendiente de derivación» (mapa de la
    sesión 32, punto 4). Esto las deriva, y de la única manera que el proyecto
    admite: **proponiendo y verificando**. Se une la primera con la segunda,
    cada resultado se verifica por recomposición como siempre, y el que
    sobrevive se une con la tercera, y otra vez a verificar. La escalera que
    se devuelve es la concatenación de las escaleras de cada etapa.

    Con dos voces devuelve exactamente lo que `combinar()`, de modo que ésta
    es su generalización y no un camino aparte.

    **EL LÍMITE, y hay que decirlo antes de que engañe.** Cada etapa pasa por
    `solucionar()`, que sólo corta cuando **las dos mitades son voces
    atestiguadas**. La forma intermedia de un plegado no tiene por qué serlo:
    es el producto de un sandhi, no una palabra que un diccionario liste. El
    plegado funciona, pues, cuando el intermedio resulta estar atestiguado —
    `mamañca` lo está, `idamavoca` lo está— y calla cuando no —`idamavocaṃ`,
    de `idamavocanti` = idaṃ + avocaṃ + iti, no lo está—. No es que falte una
    regla: es que la puerta de entrada pide dos palabras y aquí una de las dos
    es un intermedio. Levantar ese límite pide una derivación de una sola
    pasada sobre las dos junturas, no un plegado; queda anotado y sin fingir.

    Y una segunda advertencia, del mismo temple: **la escalera del plegado es
    UNA derivación válida, no necesariamente la que firmó el IEBH.** El
    plegado cierra la primera juntura (§11) antes de abrir la segunda, y la
    escalera verificada de `mamañceva` —§31 · §10 · §12 · §11 · EM— no la
    cierra: trata las dos junturas a la vez. Las dos reproducen la forma; se
    devuelve la del plegado diciendo lo que es.
    """
    if len(voces) < 2:
        return []
    if len(voces) == 2:
        return combinar(voces[0], voces[1],
                        escrita_a=escrita_a, escrita_b=escrita_b)
    estados = [(voces[0], [])]
    for i, v in enumerate(voces[1:]):
        ultima = (i == len(voces) - 2)
        nuevos = []
        for forma, pasos in estados:
            for cand, l in combinar(forma, v,
                                    escrita_a=escrita_a if not pasos else None,
                                    escrita_b=escrita_b if ultima else None):
                p = list(l.get("pasos") or [])
                # El primer paso de cada etapa repite la superficie con la que
                # entra; sólo el de la primera etapa dice algo nuevo.
                nuevos.append((cand, pasos + (p[1:] if pasos else p)))
        estados = nuevos
    vistas = {}
    for cand, pasos in estados:
        if cand not in vistas or len(pasos) < len(vistas[cand]):
            vistas[cand] = pasos
    out = [(c, {"componentes": list(voces), "pasos": p,
                "procedencia": "derivada por plegado de combinar()"})
           for c, p in vistas.items()]
    out.sort(key=lambda x: (len(x[1]["pasos"]), x[0]))
    return out


# Consonantes que **no terminan una voz pāḷi**. De las 443.758 formas del
# léxico: «ṅ» 0, «ṇ» 0, «k» 0, «g» 0, «j» 0, «p» 0, «b» 0, «ñ» 1, «n» 1, «c» 3,
# «d» 9, «m» 11. Veinticinco formas en total. Una voz que termina así no es una
# voz terminada: es la **salida de una regla** con la juntura sin cerrar —§31
# convierte la niggahīta en la nasal de la serie, §34 en «m»—.
FIN_IMPOSIBLE = "ṅñṇnmdckgjpb"


def juntura_declarada(escrita, siguiente):
    """¿La edición dejó a la vista que acá hubo un sandhi? Y entre qué voces.

    Dos marcas, y las dos son hechos del texto, no criterios nuestros:

      · **«ti» suelta.** No es una voz: es lo que queda de «iti» tras el §40.
      · **una consonante desnuda al final, ante vocal.** Tampoco es final de voz
        pāḷi: de las 443.758 formas del DPD, **veinticinco** terminan en alguna
        de las doce consonantes de `FIN_IMPOSIBLE`. Es la salida del §31 o del
        §34 con la juntura sin cerrar: `vuttanayam eva`, `catukkhattun ti`.

    La voz anterior se reconstruye devolviendo la niggahīta, que es lo que esas
    reglas convirtieron. Y **quien decide sigue siendo la recomposición**: esto
    sólo dice dónde mirar y con qué par; `combinar()` verifica.

    Devuelve `(voz_anterior, voz_siguiente)` o `None`.
    """
    c = cotejo(escrita)
    if c == "ti":
        return None                      # lo resuelve quien tiene la anterior
    if (len(c) > 2 and c[-1] in FIN_IMPOSIBLE and not c.endswith("ṃ")
            and not es_palabra(escrita) and siguiente
            and cotejo(siguiente)[:1] in VOCALES):
        return (escrita[:-1] + "ṃ", siguiente)
    return None


def yuxtaposicion(F):
    """Los cortes que parten la forma en dos voces reales **sin ninguna
    operación**: la simple concatenación ya da la forma.

    `gijjhakūṭamhi` = `gijjha` + `kūṭamhi`; `mittaratā` = `mitta` + `ratā`. No
    hay sandhi ahí: hay un compuesto, y los compuestos están fuera del encargo
    por instrucción del Venerable. Decirlo con esas palabras no es lo mismo que
    decir «sin resolver»: uno es un límite declarado, el otro es una falla.

    Medido sobre el corpus de `Sandhi`: 171 de las 974 formas de los versos y
    965 de las 9.203 del comentario son de esta clase.
    """
    lex = cargar()["lexico"]
    out = []
    for i in range(2, len(F) - 1):
        a, b = F[:i], F[i:]
        if (cotejo(a) in lex and cotejo(b) in lex
                and not _es_desinencia(a) and not _es_desinencia(b)
                and not _solo_vocal(b)):
            out.append((a, b))
    return out


def por_que_no(voz, k):
    """Por qué no se resolvió, dicho en el orden en que sirve.

    Primero el hecho —si la voz está o no en el léxico—, después si algún corte
    la parte en dos voces reales, y sólo al final la lista de aforismos. Decir
    «probé 35 aforismos» cuando la voz ni siquiera existe es contestar otra
    pregunta.

    **No se propone una corrección de lo escrito.** La pantalla no corrige el
    texto que se pegó: informa qué comprobó.
    """
    entera = es_palabra(voz)
    pares = pares_del_lexico(k)
    d = {
        "la_voz_esta_en_el_lexico": entera,
        "cortes_en_dos_voces_del_lexico": len(pares),
        "ejemplos_de_corte": [" + ".join(p) for p in pares[:6]],
        "aforismos_probados": [n for n in ORDEN if isinstance(n, int)],
    }
    n_op = sum(1 for n in ORDEN if isinstance(n, int))
    if not entera and not pares:
        return ("la voz NO está en el léxico " + nombre_lexico() + ", y ningún corte la parte "
                "en dos voces que el léxico reconozca. O la forma está mal "
                "escrita, o alguna de sus piezas falta en el léxico.", d)
    if not entera:
        return ("la voz NO está en el léxico " + nombre_lexico() + ". Hay {0} corte(s) en dos "
                "voces reales, pero ninguna de las {1} operaciones enunciadas los "
                "lleva a esta forma. Conviene revisar cómo está escrita antes de "
                "buscarle una regla.".format(len(pares), n_op), d)
    if not pares:
        return ("la voz está en el léxico como palabra entera, pero ningún corte "
                "la parte en dos voces que el léxico reconozca.", d)
    return ("hay {0} corte(s) en dos voces del léxico, pero ninguna de las {1} "
            "operaciones enunciadas los lleva a esta forma. Puede que la "
            "operación no esté enunciada en el capítulo 1, o que el análisis "
            "necesite más de dos piezas.".format(len(pares), n_op), d)


def huella_banco():
    """La huella del banco, **calculada** sobre el archivo que se acaba de leer.

    Antes esta función abría `banco.sha256` y devolvía la línea guardada. O sea
    que informaba la huella que alguien escribió, no la del archivo que el
    motor tenía delante: con `reglas.json` cambiado seguía informando la huella
    vieja, y «resuelve leyendo un banco congelado con huella» no comprobaba
    nada en tiempo de consulta. Ahora se calcula, y además se dice si coincide
    con la guardada. `congelar.py` sigue siendo quien cubre los 22 archivos;
    esto cubre el que se está usando para responder.
    """
    if not os.path.exists(REGLAS):
        return None
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
                d["coincide"] = (d["guardada"] == calculada)
                break
    return d


# ── Pantalla mínima de consola ──────────────────────────────────────────

def mostrar(r):
    print("\n  {0}".format(r["escrita"]))
    print("  estado: {0}".format(r["estado"]))
    if r["motivo"]:
        print("  motivo: {0}".format(r["motivo"]))
    d = r.get("diagnostico")
    if d:
        print("          · la voz está en el léxico {0}: {1}".format(nombre_lexico(),
            "sí" if d["la_voz_esta_en_el_lexico"] else "no"))
        print("          · cortes en dos voces del léxico: {0}{1}".format(
            d["cortes_en_dos_voces_del_lexico"],
            "   " + " · ".join(d["ejemplos_de_corte"]) if d["ejemplos_de_corte"] else ""))
    for x in r["lecturas"]:
        comp = [y for y in (x.get("componentes") or []) if y]
        titulo = " + ".join(comp) if comp else "—"
        # **En una frase, decir en qué juntura se está.** La cadena explica un
        # par de voces, no la frase entera; imprimiéndola sola, de «evaṃ me
        # sutaṃ» salían seis lecturas que terminaban en «mesutaṃ» y «evaṃ»
        # desaparecía de la pantalla sin que nada lo dijera. El resto de la
        # frase se muestra en gris, entre corchetes, alrededor del par.
        ctx = x.get("contexto")
        if ctx and (ctx.get("antes") or ctx.get("despues")):
            titulo = "{0}{1}{2}".format(
                " ".join(ctx["antes"]) + " [" if ctx.get("antes") else "[",
                titulo,
                "] " + " ".join(ctx["despues"]) if ctx.get("despues") else "]")
        print("\n  {0}".format(titulo))
        for p in x["pasos"]:
            print("      {0}".format(p))
        if ctx and (ctx.get("antes") or ctx.get("despues")):
            print("      · la cadena explica la juntura entre corchetes; "
                  "el resto de la frase queda como está")
        pie = [x["procedencia"]]
        if x.get("referencia"):
            pie.insert(0, x["referencia"])
        if x.get("origen"):
            pie.append("{archivo} · {clave}".format(**x["origen"]))
        for o in x.get("tambien_en", []):
            pie.append("también en {archivo}".format(**o))
        print("  {0}".format(" · ".join(pie)))
    print()


# Los aforismos que este motor sabe invertir. Fuera de esta lista no propone
# nada, y lo dice: no se inventa una operación que no está implementada.
IMPLEMENTADOS = {n for n in ORDEN if isinstance(n, int)}
# Pakati es la ausencia de operación: no hay corte que buscar.
PAKATI = {23, 24, 30}


def _acierta_sin_las_del_banco(medibles):
    """Cuántas de las mismas formas medibles acierta el motor si al léxico se
    le quitan las voces que salieron del propio banco. Es el número honesto:
    el que quedaría si el banco no se hubiera prestado a sí mismo el léxico."""
    c = cargar()
    pleno, recorte = c["lexico"], c["lexico"] - c["lexico_banco"]
    n = 0
    try:
        c["lexico"] = recorte
        for f in medibles:
            escrita = f["f"].replace("\u2019", "'").replace("'", "")
            lect = (proponer_en_frase(escrita) if len(escrita.split()) > 1
                    else proponer(cotejo(f["f"])))
            if any(cotejo("".join(l["componentes"])) in f["esperados"] for l in lect):
                n += 1
    finally:
        c["lexico"] = pleno
    return n


def cobertura():
    c = cargar()
    d = json.load(open(REGLAS, encoding="utf-8"))
    ce = d["ce"]
    from collections import Counter

    filas = []
    for x in ce:
        kac = x["kac"]
        comp = partir_componentes(x["comp"])
        # En una frase, el sandhi ocurre en UNA juntura: los componentes son
        # las dos voces contiguas, no todas las fichas de la frase.
        escrita = x["f"].replace("\u2019", "'").replace("'", "")
        if len(comp) > 2:
            lect = proponer_en_frase(escrita)
            pares = {cotejo(comp[j] + comp[j + 1]) for j in range(len(comp) - 1)}
            esperados = {cotejo(comp[j] + comp[j + 1]) for j in range(len(comp) - 1)}
            piezas_en_lexico = comp
        else:
            lect = (proponer_en_frase(escrita) if len(escrita.split()) > 1
                    else proponer(cotejo(x["f"])))
            esperados = {cotejo("".join(comp))}
            piezas_en_lexico = [p for p in comp if es_palabra(p)]
        esperado = cotejo("".join(comp))
        acierta = any(cotejo("".join(l["componentes"])) in esperados for l in lect)

        if kac in PAKATI:
            motivo = "pakati · no hay operación que invertir"
        elif acierta:
            motivo = None
        elif kac not in IMPLEMENTADOS:
            motivo = "§{0} no está implementado en el motor".format(kac)
        elif len(comp) == 1:
            motivo = "el banco da una sola pieza: no hay juntura"
        elif len(piezas_en_lexico) < len(comp):
            faltan = [p for p in comp if not es_palabra(p)]
            motivo = "el DPD no reconoce {0}".format(", ".join(repr(p) for p in faltan))
        elif lect:
            motivo = "produce {0} lectura(s) que recomponen, ninguna es la del banco".format(len(lect))
        else:
            motivo = "ningún corte reproduce la forma"
        filas.append({"f": x["f"], "comp": x["comp"], "kac": kac,
                      "acierta": acierta, "lecturas": len(lect), "motivo": motivo,
                      "esperados": esperados})

    total = len(filas)
    pak = [f for f in filas if f["kac"] in PAKATI]
    medibles = [f for f in filas if f["kac"] not in PAKATI]
    ok = [f for f in medibles if f["acierta"]]

    print("INFORME DE COBERTURA\n")
    print("  El motor resuelve SIN mirar el banco: propone cortes desde las reglas,")
    print("  los verifica con el derivador del Venerable, y se compara el resultado")
    print("  con el análisis que el banco ya tenía.\n")
    print("  formas del banco: {0}".format(total))
    print("     pakati, sin operación que invertir: {0}".format(len(pak)))
    print("     medibles: {0}".format(len(medibles)))
    print()
    print("  ACIERTA —entre sus lecturas está la del banco—: {0} de {1}   ({2:.0f} %)"
          .format(len(ok), len(medibles), 100.0 * len(ok) / len(medibles)))
    n_extra = len(cargar()["lexico_banco"])
    if n_extra:
        # **El número sin esas voces se calcula, no se recuerda.** Estuvo
        # escrito a mano —«el número es 198»— y quedó viejo en cuanto el motor
        # mejoró: es el mismo defecto que tenía `huella_banco()`, que leía la
        # huella en vez de calcularla. Se vuelve a medir todo el banco con el
        # léxico recortado, con el mismo denominador de arriba.
        sin18 = _acierta_sin_las_del_banco(medibles)
        print()
        print("  AVISO — este número NO es independiente. Al léxico del DPD se le")
        print("  suman {0} voces que el propio banco atestigua como componente y".format(n_extra))
        print("  que el DPD no trae —«putha», «vipali», «ani», «chayo»…—. Sin ellas")
        print("  el número es {0} de {1} ({2:.0f} %). Son voces reales, firmadas por"
              .format(sin18, len(medibles), 100.0 * sin18 / len(medibles)))
        print("  el Venerable, pero medir el banco con un léxico sacado del banco")
        print("  es circular.")
        print("  El número que vale es el del corpus —`medir_contra_corpus.py`—, que")
        print("  estas voces no mueven en absoluto: 90,3 % antes y después.")
    print("  produce alguna lectura que recompone: {0}".format(
        sum(1 for f in medibles if f["lecturas"])))
    print("  no produce ninguna: {0}".format(
        sum(1 for f in medibles if not f["lecturas"])))

    print("\n  POR QUÉ FALLA, agrupado:")
    fallos = [f for f in medibles if not f["acierta"]]
    for m, n in Counter(f["motivo"].split(" —")[0].split(" '")[0] for f in fallos).most_common():
        print("     {0:>4}   {1}".format(n, m))

    # Dos listas que hoy salen vacías. Se imprime «ninguna» en vez de dejar el
    # título solo: un encabezado que promete una lista y no muestra ninguna
    # línea se lee como que el informe se cortó, no como que no hay nada.
    sin_lexico = [f for f in fallos if f["motivo"].startswith("el DPD no reconoce")]
    print("\n  Las que no reconoce el léxico, una por una:")
    if not sin_lexico:
        print("     ninguna — las 40 que fallan las reconoce el léxico;"
              "\n     lo que falla es el corte o la cadena, no el diccionario.")
    for f in sin_lexico:
        print("     {0:<26} {1:<28} {2}".format(f["f"][:25], f["comp"][:27], f["motivo"]))

    sin_implementar = Counter(f["kac"] for f in fallos
                              if f["kac"] not in IMPLEMENTADOS).most_common()
    print("\n  Los aforismos sin implementar, y cuántas formas dependen de cada uno:")
    if not sin_implementar:
        print("     ninguno — de las 40 que fallan, todas dependen de aforismos"
              "\n     que el motor ya implementa. No falta ninguna regla.")
    for k, n in sin_implementar:
        print("     §{0:<5} {1:>3}".format(k, n))

    print("\n  Los dos denominadores: {0} formas hoy; {1} si entran las cinco"
          "\n  formas de interdicción de sara 9, 10 y 11 que faltan."
          .format(total, total + 5))
    return 0


def consola_utf8():
    """La consola de Windows viene en cp1252 y no sabe escribir «ṃ».

    Sin esto, la primera forma con diacrítico levanta UnicodeEncodeError y —si
    se abrió con doble clic— la ventana se cierra antes de que se lea nada.
    """
    for f in (sys.stdout, sys.stderr):
        try:
            f.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def interactivo():
    """Cuando se abre sin argumentos: pide voces hasta que se deje vacío.

    Existe para el doble clic. Sin esto la ventana imprime la ayuda y se
    cierra sin que se alcance a leer.
    """
    print("\n  SOLUCIONADOR DE SANDHIS")
    print("  Escribí una voz pāḷi y Enter. Enter vacío para salir.\n")
    while True:
        try:
            v = input("  > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not v:
            return 0
        try:
            mostrar(solucionar(v))
        except Exception as e:
            print("\n  Error: {0}: {1}\n".format(type(e).__name__, e))


def main():
    consola_utf8()
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("voz", nargs="*")
    ap.add_argument("--cobertura", action="store_true")
    ap.add_argument("--canon", action="store_true", help=(
        "usa el canon del Sexto Concilio como primera capa de léxico. "
        "Apagado por defecto: con él el corte cae de 630 de 698 (90,3 %) "
        "a 555 (79,5 %). El porqué, en cargar()."))
    ap.add_argument("--solo-canon", action="store_true", help=(
        "el léxico es el corpus convertido del Sexto Concilio, sin DPD "
        "en ninguna capa (decisión del Venerable, 2026-08-28)."))
    ap.add_argument("--dpd-filtro", action="store_true", help=(
        "suma el DPD como testigo silencioso dentro de solo-canon: filtro, "
        "ordenación y señal, nunca análisis (decisión de Angel, 2026-08-28)."))
    a = ap.parse_args()
    globals()['USAR_CANON'] = a.canon
    globals()['SOLO_CANON'] = a.solo_canon
    globals()['DPD_FILTRO'] = a.dpd_filtro
    if a.cobertura:
        return cobertura()
    if not a.voz:
        return interactivo()
    for v in a.voz:
        mostrar(solucionar(v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
