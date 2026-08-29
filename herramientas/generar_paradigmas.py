#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la referencia de paradigmas de declinación.

    python3 herramientas/generar_paradigmas.py

Junta dos cosas:

  recursos/paradigmas/paradigmas.json   las 84 entradas (83 documentos únicos),
                                        transcritas de los documentos del IEBH
  recursos/paradigmas/plantilla.html    el maquetado y la lógica

y escribe site/recursos/paradigmas/index.html.

Antes de escribir, verifica la integridad de los datos: cada paradigma con
tabla ha de tener las ocho inflexiones, tantas celdas por fila como columnas,
y ninguna celda vacía fuera del vocativo (donde el guion del documento se
transcribe como lista vacía). También coteja códigos, documentos y géneros
contra recursos/paradigmas/indice.json. Si algo no cuadra, no publica.
"""

import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "herramientas"))

from generar_capitulo import parsear, partir_bloques, desescapar  # noqa: E402

DATOS = os.path.join(RAIZ, "recursos", "paradigmas", "paradigmas.json")
INDICE = os.path.join(RAIZ, "recursos", "paradigmas", "indice.json")
INGLES = os.path.join(RAIZ, "recursos", "paradigmas", "ingles.json")
PLANTILLA = os.path.join(RAIZ, "recursos", "paradigmas", "plantilla.html")
DESTINO = os.path.join(RAIZ, "site", "recursos", "paradigmas", "index.html")
MD_NAMA = os.path.join(RAIZ, "kaccayana", "02-nama-kappa.md")


def _limpiar(t):
    """Quita marcadores de nota, glosas emergentes y escapes."""
    t = re.sub(r'\[\^\d+\]', '', t)
    t = re.sub(r'\{([^|{}]+)\|[^{}]*\}', r'\1', t)
    t = desescapar(t)
    return re.sub(r'\s+', ' ', t).strip()


def suttas_citados(datos):
    """Los §N del Nāma-Kappa citados en el detalle de los sufijos.

    Sólo las referencias desnudas «§N»; las de otras obras (Rū. §N) no
    remiten a este sitio y quedan fuera.
    """
    citados = set()
    for p in datos["paradigmas"]:
        for d in p.get("detalle", []):
            for u in (d.get("usos") or [d]):
                for tok in re.split(r',\s*', u.get("ref", "")):
                    m = re.match(r'§(\d+)', tok.strip())
                    if m:
                        citados.add(int(m.group(1)))
    return citados


def suttas_nama(citados):
    """{n: {pali, es}} para el tooltip de las referencias §N."""
    if not citados or not os.path.exists(MD_NAMA):
        return {}
    fuera = {}
    for s in parsear(MD_NAMA)["suttas"]:
        if s["n"] not in citados:
            continue
        bloques = partir_bloques(s["cuerpo"])
        es = ""
        if len(bloques) > 1:
            lineas = [x.strip() for x in bloques[1] if x.strip()]
            if lineas:
                es = _limpiar(lineas[0])
        fuera[str(s["n"])] = {"pali": _limpiar(s["pali"]), "es": es}
    return fuera


def verificar_ingles(datos, ing):
    """El borrador inglés, contra los datos. Devuelve la lista de fallos.

    Se comprueba SIEMPRE, esté adjudicado o no: un borrador que no cuadra con
    los datos no mejora por esperar, y así el fallo aparece el día que se
    escribe y no el día que se firma.
    """
    fallos = []
    entradas = ing.get("paradigmas", {})
    codigos = {p["codigo"] for p in datos["paradigmas"]}
    for c in sorted(codigos - set(entradas)):
        fallos.append("inglés: falta la entrada {0}".format(c))
    for c in sorted(set(entradas) - codigos):
        fallos.append("inglés: sobra la entrada {0}".format(c))
    for p in datos["paradigmas"]:
        c = p["codigo"]
        e = entradas.get(c)
        if not e:
            continue
        if not (e.get("paradigma") or "").strip():
            fallos.append("inglés {0}: sin glosa".format(c))
        # cada campo de prosa que exista en español ha de existir en inglés
        for campo in ("subtitulo", "familia", "texto"):
            if p.get(campo) and not (e.get(campo) or "").strip():
                fallos.append("inglés {0}: falta «{1}»".format(c, campo))
        if len(e.get("notas") or []) != len(p.get("notas") or []):
            fallos.append("inglés {0}: {1} notas para {2}".format(
                c, len(e.get("notas") or []), len(p.get("notas") or [])))
        if p.get("detalle"):
            den = {d["s"]: d for d in e.get("detalle") or []}
            for d in p["detalle"]:
                usos = d.get("usos") or [d]
                dn = den.get(d["s"])
                if not dn:
                    fallos.append("inglés {0}: falta el sufijo «{1}»".format(
                        c, d["s"]))
                    continue
                if len(dn.get("usos") or []) != len(usos):
                    fallos.append("inglés {0} «{1}»: {2} usos para {3}".format(
                        c, d["s"], len(dn.get("usos") or []), len(usos)))
                    continue
                for i, u in enumerate(usos):
                    if len(dn["usos"][i].get("ej") or []) != len(u.get("ej") or []):
                        fallos.append(
                            "inglés {0} «{1}» uso {2}: {3} ejemplos para "
                            "{4}".format(c, d["s"], i,
                                         len(dn["usos"][i].get("ej") or []),
                                         len(u.get("ej") or [])))
    return fallos


def verificar(datos, indice):
    """Devuelve la lista de fallos; vacía si todo cuadra."""
    fallos = []
    entradas = datos["paradigmas"]
    imap = {e["codigo"]: e for e in indice["entradas"]}
    pmap = {p["codigo"]: p for p in entradas}

    for c in sorted(set(imap) - set(pmap)):
        fallos.append("falta en paradigmas.json: {0}".format(c))
    for c in sorted(set(pmap) - set(imap)):
        fallos.append("sobra respecto al índice: {0}".format(c))
    for c in sorted(set(imap) & set(pmap)):
        if imap[c]["doc"] != pmap[c]["doc"]:
            fallos.append("{0}: doc distinto del índice".format(c))
        if imap[c]["genero"] != pmap[c]["genero"]:
            fallos.append("{0}: género distinto del índice".format(c))

    n_infl = len(datos["inflexiones"])
    for p in entradas:
        c = p["codigo"]
        if "filas" not in p:
            continue  # F-O (igual_que) y Sufijos-Inflexiones
        if len(p["filas"]) != n_infl:
            fallos.append("{0}: {1} filas, se esperaban {2}".format(
                c, len(p["filas"]), n_infl))
            continue
        for i, fila in enumerate(p["filas"]):
            if len(fila) != len(p["columnas"]):
                fallos.append("{0} fila {1}: {2} celdas para {3} columnas".format(
                    c, i, len(fila), len(p["columnas"])))
            for celda in fila:
                if not celda and i != 1:  # sólo el vocativo admite guion
                    fallos.append("{0} fila {1}: celda vacía fuera del "
                                  "vocativo".format(c, i))
                for v in celda:
                    if not v.strip() or v != v.strip():
                        fallos.append("{0} fila {1}: variante mal recortada "
                                      "{2!r}".format(c, i, v))
                    if unicodedata.normalize("NFC", v) != v:
                        fallos.append("{0} fila {1}: {2!r} no está en "
                                      "NFC".format(c, i, v))
    return fallos


def main():
    datos = json.load(open(DATOS, encoding="utf-8"))
    indice = json.load(open(INDICE, encoding="utf-8"))

    ing = (json.load(open(INGLES, encoding="utf-8"))
           if os.path.exists(INGLES) else {})

    fallos = verificar(datos, indice) + verificar_ingles(datos, ing)
    if fallos:
        print("paradigmas.json NO cuadra; no se publica:")
        for f in fallos[:20]:
            print("  ✗", f)
        if len(fallos) > 20:
            print("  … y {0} más".format(len(fallos) - 20))
        return 1

    # El inglés de la prosa del IEBH sólo viaja a la página cuando ESTÁ
    # ADJUDICADO. Mientras «adjudicado» sea false el borrador se comprueba
    # pero no se publica, y el modo inglés muestra el español —que es lo que
    # el pie en inglés de la página dice—. Firmarlo es cambiar un booleano.
    if ing.get("adjudicado"):
        datos["ingles"] = ing["paradigmas"]
        datos["ingles_por"] = ing.get("adjudicado_por", "")

    citados = suttas_citados(datos)
    datos["nama"] = suttas_nama(citados)
    sin_texto = sorted(n for n in citados if str(n) not in datos["nama"])
    if sin_texto:
        print("  aviso — §N citados sin texto en el Nāma-Kappa: {0}".format(
            sin_texto))

    plantilla = open(PLANTILLA, encoding="utf-8").read()
    marca = re.search(r'/\*__DATOS__\*/.*?/\*__FIN__\*/', plantilla, re.S)
    if not marca:
        print("La plantilla no tiene el marcador /*__DATOS__*/…/*__FIN__*/")
        return 1
    html = (plantilla[:marca.start()]
            + json.dumps(datos, ensure_ascii=False, separators=(",", ":"))
            + plantilla[marca.end():])

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    open(DESTINO, "w", encoding="utf-8").write(html)

    entradas = datos["paradigmas"]
    con_tabla = [p for p in entradas if "filas" in p]
    formas = sum(len(v) for p in con_tabla
                 for fila in p["filas"] for v in fila)
    docs = len({p["doc"] for p in entradas})
    print("{0} entradas · {1} tablas · {2} documentos · {3} formas → {4}".format(
        len(entradas), len(con_tabla), docs, formas,
        os.path.relpath(DESTINO, RAIZ)))

    # avisos útiles, sin detener la publicación
    con_nota = [p["codigo"] for p in entradas if p.get("notas")]
    if con_nota:
        print("  con nota de transcripción: {0}".format(", ".join(con_nota)))
    if ing:
        n = len(ing.get("paradigmas", {}))
        if ing.get("adjudicado"):
            print("  inglés de la prosa: {0} entradas, ADJUDICADO por {1} "
                  "({2}) — publicado".format(n, ing.get("adjudicado_por") or "?",
                                             ing.get("fecha") or "?"))
        else:
            print("  inglés de la prosa: {0} entradas redactadas y "
                  "comprobadas, SIN adjudicar — no se publica (cotejo en "
                  "docs/paradigmas/ingles-por-adjudicar.md)".format(n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
