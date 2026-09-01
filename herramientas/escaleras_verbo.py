#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arma las escaleras publicables del verbo a partir de las dos fuentes.

    python3 herramientas/escaleras_verbo.py          # las imprime para revisar

Lo importa `generar_verbo.py`; suelto sirve para verlas antes de maquetar.

Aquí viven las cinco decisiones que Angel firmó el 1-sep-2026, y no en el
maquetado, para que se puedan leer y discutir sin abrir el HTML. Están en
`docs/verbo/escaleras-por-adjudicar.md` con su porqué; en resumen:

1. **Par Kacc/Rū** en cada paso.
2. **Una operación por fila**: cada fila muestra la forma RESULTANTE de la
   regla que la acompaña, de modo que la escalera se comprueba línea a línea.
3. **Entra lo que sólo está en las diapositivas**, si no está en el documento.
4. **«rudhi»**, no «rudha», como lema.
5. **«suṇāti» se corrige** a Kacc. §448 / Rū 512.

Cada fila lleva su procedencia —`documento`, `diapositiva` o `propuesta`— y la
página la rotula. Ninguna fila sin fuente sale sin marca.

Cómo se decide qué versión de una escalera se publica
-----------------------------------------------------

Las dos fuentes se emparejan **por la forma final**, no por el lema: «su» da
dos escaleras y el documento deriva «vikkiṇāti» donde la diapositiva deriva
«kiṇāti», que son palabras distintas. Cuando hay diapositiva, manda la
diapositiva, porque ya viene con una operación por fila y con el par Kacc/Rū.
Cuando no la hay, se parte la fila fundida del documento, y eso obliga a
distinguir dos casos:

- si la operación fundida deja su forma a la vista —«gamu», «tuda» y las
  demás—, partirla no añade nada nuevo y las dos filas son `documento`;
- si la esconde —«hū» y «hu», donde de `hū + a + ti` a `ho + ti` ocurren dos
  operaciones—, la forma intermedia se calcula de la regla citada y la fila
  se marca `propuesta`.
"""

import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERBO = os.path.join(RAIZ, "recursos", "verbo", "verbo.json")
DIAPOS = os.path.join(RAIZ, "recursos", "verbo", "diapositivas.json")

# Decisión 4: el documento llama «rudha» a la raíz que su propia glosa
# —«obstruir»— y `recursos/raices/raices.json` llaman «rudhi».
LEMAS = {"rudha": "rudhi"}

# Decisión 5: la segunda escalera de «su» cita Rū 513, que es la regla del
# grupo de «kī». «su» es svādi: le toca Kacc. §448 / Rū 512.
CORRECCIONES = {
    ("suṇāti", 513): {
        "kacc": 448, "ru": 512,
        "segun_documento": 513,
        "nota": ("El documento cita Rū 513 (Kacc. §449 «Kiyādito nā»), que es "
                 "la regla del grupo de «kī». «su» es svādi: la regla que le "
                 "da ‘ṇā’ es Kacc. §448 «Svādito ṇu-ṇā-uṇā ca» (Rū 512), que "
                 "es lo que citan las presentaciones."),
    },
}

CELDAS = ("prefijo", "raiz", "signo", "inflexion")


# --------------------------------------------------------------------------
# Explicaciones prestadas de las diapositivas
# --------------------------------------------------------------------------
#
# El documento «Verbo» NO tiene columna de explicación: sus escaleras enseñan
# el paso y la autoridad y callan el porqué. Las diapositivas sí la traen, y
# describen la misma regla con las mismas palabras. De ahí se toma, con tres
# cautelas, porque «la misma regla» no siempre es «la misma operación»:
#
# 1. Sólo se presta cuando **todas** las diapositivas redactan esa regla
#    igual. Kacc. §449 la usa una vez para colocar el signo ‘nā’ y otra para
#    sustituir ‘n’ por ‘ṇ’ —son dos operaciones—, y Kacc. §483 la redacta
#    según la vocal de cada raíz. Ésas se dejan vacías.
# 2. Las diferencias de puntuación no cuentan como redacciones distintas:
#    «colocar inflexión verbal, presente indicativo» y la misma sin coma son
#    la misma frase, y se toma la más frecuente.
# 3. **Nunca se presta una frase que entrecomille una letra o una forma.**
#    Ésta es la cautela que más recorta, y la que hace falta: Kacc. §485 es
#    la regla general de vuddhi y las diapositivas sólo la usan con «bhū», de
#    modo que su redacción dice «fortalecer vocal ‘ū’» —falsa para «su», que
#    en ese paso hace ṇu → ṇo—. Y Kacc. §20, el comodín del «ca», aparece
#    como «sustituir ‘v’ por ‘b’» en «divu» y ampara una duplicación en
#    «vi-kī». Sólo se presta lo puramente estructural: «colocar la raíz»,
#    «elidir la vocal final», «colocar signo de conjugación», «formar el
#    verbo». Lo demás se queda en blanco, que es lo honrado.
#
# Cada celda prestada queda marcada con `explicacion_prestada`, y la página
# lo dice.

RE_FORMA_CITADA = re.compile(r"[‘'\"“][^’'\"”]+[’'\"”]")


def texto_de_regla(dia):
    """{(kacc, ru): explicación} de las reglas que las diapositivas redactan
    siempre igual y sin nombrar una forma concreta."""
    import collections
    bruto = collections.defaultdict(collections.Counter)
    for esc in dia["escaleras"]:
        for paso in esc["pasos"]:
            op = (paso.get("operacion") or "").strip()
            if not op:
                continue
            for a in paso["autoridades"]:
                bruto[(a["kacc"], a["ru"])][op] += 1

    def clave(t):
        return re.sub(r"[\s,;.]+", " ", t).strip().lower()

    fuera = {}
    for regla, cuenta in bruto.items():
        formas = {clave(t) for t in cuenta}
        if len(formas) != 1:
            continue                       # cautela 1
        texto = cuenta.most_common(1)[0][0]   # cautela 2
        if RE_FORMA_CITADA.search(texto):
            continue                       # cautela 3
        fuera[regla] = texto
    return fuera


def normalizar(forma):
    forma = unicodedata.normalize("NFC", forma or "")
    return re.sub(r"[\s'’‘\-]", "", forma).lower()


def lema_documento(titulo):
    t = re.sub(r"^\d+[a-z]?-", "", (titulo or "").strip()).split("(")[0]
    t = t.strip().lower()
    return LEMAS.get(t, t)


def glosa_documento(titulo):
    m = re.search(r"\(([^)]*)\)\s*$", titulo or "")
    return m.group(1).strip() if m else ""


def forma_final(esc):
    for paso in reversed(esc["pasos"]):
        if paso.get("resultado"):
            return normalizar(paso["resultado"])
    return ""


def _paso(n, origen, raiz="", signo="", inflexion="", prefijo="",
          resultado="", autoridades=(), operacion="", nota=""):
    return {"n": n, "origen": origen, "prefijo": prefijo, "raiz": raiz,
            "signo": signo, "inflexion": inflexion, "resultado": resultado,
            "autoridades": list(autoridades), "operacion": operacion,
            "explicacion_prestada": False, "nota": nota}


def corregir(autoridad, final):
    """Aplica la decisión 5 si toca; devuelve (autoridad, hubo_correccion)."""
    clave = (final, autoridad["ru"])
    arreglo = CORRECCIONES.get(clave)
    if not arreglo:
        return dict(autoridad), False
    nueva = dict(autoridad)
    nueva.update(kacc=arreglo["kacc"], ru=arreglo["ru"],
                 segun_documento=arreglo["segun_documento"],
                 corregida=True, nota=arreglo["nota"])
    return nueva, True


def de_diapositiva(esc, lema, glosa):
    """La diapositiva ya viene con una operación por fila."""
    pasos = []
    for i, p in enumerate(esc["pasos"], 1):
        pasos.append(_paso(i, "diapositiva", p["raiz"], p["signo"],
                           p["inflexion"], p["prefijo"], p["resultado"],
                           p["autoridades"], p.get("operacion", "")))
    return {"lema": lema, "glosa": glosa,
            "formacion": esc.get("formacion", ""),
            "resultado": esc["pasos"][-1].get("resultado", ""),
            "procedencia": "diapositiva",
            "presentacion": esc.get("presentacion", ""),
            "pasos": pasos}


def celdas(paso):
    return {c: (paso.get(c) or "").strip() for c in CELDAS}


def resultante(fila, siguiente):
    """
    La forma que deja la regla de esta fila.

    El documento imprime, en los pasos de elisión, la forma ANTERIOR a la
    operación; la resultante está en la fila de abajo, mezclada con lo que
    haya hecho la regla de esa otra fila. Se adopta de la siguiente fila
    únicamente la celda que la elisión vacía o acorta, y se dejan las demás
    como están. Nada se inventa: los dos valores son del documento.
    """
    a, b = celdas(fila), celdas(siguiente)
    fuera = dict(a)
    for c in CELDAS:
        vacia = a[c] and not b[c]
        acorta = a[c] and b[c] and b[c] != a[c] and a[c].startswith(b[c])
        if vacia or acorta:
            fuera[c] = b[c]
    return fuera


def del_documento(esc, impresas):
    """
    Pone el documento en una operación por fila.

    Dos cosas: mostrar en cada paso la forma RESULTANTE de su regla, y partir
    la última fila, que funde la última operación con la de formar el verbo.
    Una fila se marca «propuesta» cuando la combinación de celdas que muestra
    no está impresa en ninguna fila del documento — que es lo que pasa en
    «hū» y «hu», donde la elisión del signo de conjugación y el
    fortalecimiento de la vocal ocurren en la misma fila.
    """
    final = forma_final(esc)
    lema = lema_documento(esc["titulo"])
    pasos, corregidas = [], 0

    def autoridades(paso):
        nonlocal corregidas
        fuera = []
        for a in paso["autoridades"]:
            nueva, hubo = corregir(a, final)
            corregidas += hubo
            fuera.append(nueva)
        return fuera

    crudos = esc["pasos"]
    for i, p in enumerate(crudos[:-1]):
        forma = resultante(p, crudos[i + 1])
        origen = ("documento" if tuple(forma[c] for c in CELDAS) in impresas
                  else "propuesta")
        pasos.append(_paso(len(pasos) + 1, origen, forma["raiz"],
                           forma["signo"], forma["inflexion"],
                           forma["prefijo"], "", autoridades(p),
                           nota=("" if origen == "documento" else
                                 "El documento no imprime esta forma "
                                 "intermedia: funde esta operación con la "
                                 "siguiente en una sola fila. Se deduce de "
                                 "la regla citada, no de una regla nueva.")))

    ultima = crudos[-1]
    auts = autoridades(ultima)
    # la fila de formar el verbo es siempre la que cita Kacc. §11
    formar = [a for a in auts if a["kacc"] == 11]
    previas = [a for a in auts if a["kacc"] != 11]
    forma = celdas(ultima)
    if previas:
        pasos.append(_paso(len(pasos) + 1, "documento", forma["raiz"],
                           forma["signo"], forma["inflexion"],
                           forma["prefijo"], "", previas))
    pasos.append(_paso(len(pasos) + 1, "documento", forma["raiz"],
                       forma["signo"], forma["inflexion"], forma["prefijo"],
                       ultima.get("resultado", ""), formar or auts,
                       "formar el verbo"))

    return {"lema": lema, "glosa": glosa_documento(esc["titulo"]),
            "formacion": "Formación: presente indicativo, tercera persona "
                         "singular",
            "resultado": ultima.get("resultado", ""),
            "procedencia": "documento",
            "presentacion": "",
            "correcciones": corregidas,
            "pasos": pasos}


def escaleras(doc=None, dia=None):
    """Las escaleras publicables, en el orden del documento y luego el resto."""
    doc = doc or json.load(open(VERBO, encoding="utf-8"))
    dia = dia or json.load(open(DIAPOS, encoding="utf-8"))
    reglas = texto_de_regla(dia)

    por_forma = {}
    for esc in dia["escaleras"]:
        por_forma.setdefault(forma_final(esc), []).append(esc)

    # Todas las combinaciones de celdas que el documento imprime: sirven para
    # saber si una fila resultante está impresa o hay que marcarla propuesta.
    impresas = {tuple((p.get(c) or "").strip() for c in CELDAS)
                for e in doc["escaleras"] for p in e["pasos"]}

    fuera, gastadas = [], set()
    for esc in doc["escaleras"]:
        final = forma_final(esc)
        lema = lema_documento(esc["titulo"])
        glosa = glosa_documento(esc["titulo"])
        libres = [d for d in por_forma.get(final, []) if id(d) not in gastadas]
        if libres:
            gastadas.add(id(libres[0]))
            fuera.append(de_diapositiva(libres[0], lema, glosa))
        else:
            fuera.append(del_documento(esc, impresas))

    # Las escaleras del documento no traen explicación: se presta de las
    # diapositivas la de cada regla, cuando es segura. Ver texto_de_regla().
    for e in fuera:
        for paso in e["pasos"]:
            if paso.get("operacion"):
                continue
            for a in paso["autoridades"]:
                texto = reglas.get((a["kacc"], a["ru"]))
                if texto:
                    paso["operacion"] = texto
                    paso["explicacion_prestada"] = True
                    break

    # Decisión 3: lo que sólo está en las diapositivas, sin repetir.
    vistas = {(e["lema"], e["resultado"], e["formacion"]) for e in fuera}
    for esc in dia["escaleras"]:
        if id(esc) in gastadas:
            continue
        clave = (esc["lema"], esc["pasos"][-1].get("resultado", ""),
                 esc.get("formacion", ""))
        if clave in vistas:
            continue
        vistas.add(clave)
        gastadas.add(id(esc))
        fuera.append(de_diapositiva(esc, esc["lema"], esc.get("glosa", "")))
    return fuera


def main():
    for ruta in (VERBO, DIAPOS):
        if not os.path.exists(ruta):
            sys.exit(f"Falta {os.path.relpath(ruta, RAIZ)}.")
    todas = escaleras()
    propuestas = corregidas = 0
    for e in todas:
        origen = (e["presentacion"] or "documento «Verbo»")
        print(f"\n### {e['lema']} ({e['glosa']}) → {e['resultado']}"
              f"   [{origen}]")
        print(f"    {e['formacion']}")
        for p in e["pasos"]:
            piezas = " + ".join(x for x in (p["prefijo"], p["raiz"],
                                            p["signo"], p["inflexion"]) if x)
            auts = " ".join(f"§{a['kacc']}/Rū{a['ru']}"
                            + ("*" if a.get("corregida") else "")
                            for a in p["autoridades"])
            marca = {"documento": " ", "diapositiva": " ",
                     "propuesta": "?"}[p["origen"]]
            if p["origen"] == "propuesta":
                propuestas += 1
            corregidas += sum(1 for a in p["autoridades"]
                              if a.get("corregida"))
            res = f"  = {p['resultado']}" if p["resultado"] else ""
            print(f"  {marca}{p['n']}  {piezas:26s}{res:14s} "
                  f"{auts:16s} {p['operacion']}")
    print(f"\n{len(todas)} escaleras · {propuestas} filas propuestas (?) · "
          f"{corregidas} autoridades corregidas (*)")


if __name__ == "__main__":
    main()
