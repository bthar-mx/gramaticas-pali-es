#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coteja las escaleras del documento «Verbo» con las de las presentaciones.

    python3 herramientas/auditar_verbo.py

No corrige nada: informa. Es el guion que sostiene lo que
`docs/verbo/escaleras-por-adjudicar.md` afirma, de modo que cualquiera pueda
rehacer la comprobación en vez de creerse el informe.

Qué comprueba
-------------

1. **Que todo par Kacc/Rū cuadre con la concordancia del repositorio**, la
   deducida de `kaccayana/*.md` y `docs/*.md`. Vale para los dos JSON.
2. **Que el documento y la diapositiva cuenten la misma derivación.** Se
   emparejan por la FORMA FINAL, no por el lema: «su» da dos escaleras —con
   ‘ṇu’ y con ‘ṇā’—, y el documento deriva «vikkiṇāti» donde la diapositiva
   deriva «kiṇāti», que son palabras distintas y no se deben cotejar. Luego se
   comparan paso a paso, sabiendo que el documento funde el último paso de
   elisión con el de formación del verbo y que en los pasos de elisión muestra
   la forma anterior. Lo que sobrepase esas dos diferencias conocidas se
   informa.
3. **Que ninguna forma retroceda** dentro de una escalera: si un paso deshace
   lo que hizo el anterior sin regla que lo explique, se señala.
4. **Que no queden ligaduras rotas** del PDF («in exión» por «inflexión»).
5. **Que las ocho tablas de terminaciones** del índice de paradigmas cuadren
   con las del documento «Verbo» y con las de las diapositivas, casilla a
   casilla. Se espera que difieran del documento: da una sola terminación por
   casilla, y ésa fue la errata que costó la v1.3.
6. **Que el gaṇa que dice /verbo/ sea el que dice /recursos/raices/.** Las dos
   páginas lo afirman por caminos distintos —una citando el sutta del signo de
   conjugación, la otra por la referencia del Saddanīti— y nada garantiza que
   coincidan. Al final se informa además de cuántos lemas tienen ficha en
   raíces, que es lo que hace falta saber antes de enlazar una página con la
   otra.

Nada de esto decide: la firma es del IEBH. Ver el informe.
"""

import glob
import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "herramientas"))

VERBO = os.path.join(RAIZ, "recursos", "verbo", "verbo.json")
INFLEXIONES = os.path.join(RAIZ, "recursos", "verbo", "inflexiones.json")
PDFS = os.path.join(RAIZ, "docs", "fuentes", "verbo-diapositivas")
DIAPOS = os.path.join(RAIZ, "recursos", "verbo", "diapositivas.json")
RAICES = os.path.join(RAIZ, "recursos", "raices", "raices.json")

RE_SUTTA = re.compile(r"\*\*(\d+)\\?\.\s*(\d+)\\?\.\s")
# Restos de ligadura fi/fl que pdftotext deja al leer estas diapositivas.
RE_LIGADURA = re.compile(r"\b(in exi|re ere|identi ca|signi ca|su jo|"
                         r"[a-zá-ú]+ nal\b)")


def concordancia():
    ru2kacc = {}
    for patron in ("kaccayana/*.md", "docs/*.md"):
        for ruta in sorted(glob.glob(os.path.join(RAIZ, patron))):
            with open(ruta, encoding="utf-8") as fh:
                for m in RE_SUTTA.finditer(fh.read()):
                    ru2kacc.setdefault(int(m.group(2)), int(m.group(1)))
    return ru2kacc


def normalizar(forma):
    """Para comparar formas: sin espacios, sin apóstrofos, en NFC."""
    forma = unicodedata.normalize("NFC", forma or "")
    return re.sub(r"[\s'’‘\-]", "", forma).lower()


def cuerpo(paso):
    """Las cuatro celdas de forma de un paso, para comparar."""
    return tuple(normalizar(paso.get(c, ""))
                 for c in ("prefijo", "raiz", "signo", "inflexion"))


def pares(datos, donde):
    """Todos los (kacc, ru) que aparecen, con su sitio, para comprobarlos."""
    for esc in datos["escaleras"]:
        etiqueta = esc.get("lema") or esc.get("titulo", "?")
        for paso in esc["pasos"]:
            for a in paso["autoridades"]:
                yield (a["kacc"], a["ru"], f"{donde} · {etiqueta} · paso "
                       f"{paso['n']}")


# --------------------------------------------------------------------------
# Las tablas de terminaciones, cotejadas con las otras dos fuentes
# --------------------------------------------------------------------------
#
# Esto es lo que faltaba y por lo que la página publicó, hasta la v1.2, las
# terminaciones del documento «Verbo» —una sola por casilla— en vez de las
# del índice de paradigmas, que trae las alternativas. La auditoría cotejaba
# las escaleras y no estas tablas.

RE_FILA_DIAPO = re.compile(r"^\s*(tercera|segunda|primera)\s+(.*)$", re.I)
PERSONAS_DIAPO = {"tercera": 0, "segunda": 1, "primera": 2}


def normaliza_term(t):
    """«Ā -TTHA» y «ā - ttha» son la misma casilla."""
    t = unicodedata.normalize("NFC", str(t or "")).lower()
    t = re.sub(r"\s*-\s*", " - ", t)
    return re.sub(r"[\s()]+", "", t)


def tablas_de_diapositivas():
    """
    Las tablas de terminaciones que imprimen las presentaciones.

    Se reconocen por sus tres filas «tercera / segunda / primera», que en las
    diapositivas van en versalitas. Devuelve {pali: [[4 casillas] x 3]}.
    """
    import glob
    import shutil
    import subprocess

    if not shutil.which("pdftotext"):
        return {}
    fuera = {}
    for pdf in sorted(glob.glob(os.path.join(PDFS, "*.pdf"))):
        salida = subprocess.run(["pdftotext", "-layout", pdf, "-"],
                                capture_output=True, text=True)
        if salida.returncode != 0:
            continue
        lineas = salida.stdout.split("\n")
        for i, linea in enumerate(lineas):
            m = re.search(r"\((VATTAMĀNĀ|PAÑCAMĪ|SATTAMĪ|HIYYATTANĪ|PAROKKHĀ|"
                          r"AJJATANĪ|BHAVISSANTĪ|KĀLĀTIPATTI)\)", linea, re.I)
            if not m:
                continue
            pali = m.group(1).lower()
            # La tabla es la que sigue INMEDIATAMENTE al nombre pāḷi, y se
            # corta en cuanto aparece otro nombre pāḷi: si se barren treinta
            # líneas a ciegas se recogen las filas de la tabla siguiente y se
            # coteja «vattamānā» contra las terminaciones del imperfecto.
            filas = [None, None, None]
            for l in lineas[i + 1:i + 26]:
                if re.search(r"\((VATTAMĀNĀ|PAÑCAMĪ|SATTAMĪ|HIYYATTANĪ|"
                             r"PAROKKHĀ|AJJATANĪ|BHAVISSANTĪ|KĀLĀTIPATTI)\)",
                             l, re.I):
                    break
                f = RE_FILA_DIAPO.match(l)
                if not f:
                    continue
                celdas = re.split(r"\s{2,}", f.group(2).strip())
                celdas = [c for c in celdas if c.strip()]
                persona = PERSONAS_DIAPO[f.group(1).lower()]
                if len(celdas) == 4 and filas[persona] is None:
                    filas[persona] = celdas
            if all(filas):
                fuera.setdefault(pali, filas)
    return fuera


def cotejar_inflexiones(infl, verbo):
    """Las ocho tablas contra el documento «Verbo» y contra las diapositivas."""
    print("\n5. Tablas de terminaciones: índice contra documento y "
          "diapositivas")
    diapos = tablas_de_diapositivas()
    por_pali_doc = {}
    for i in verbo.get("inflexiones", []):
        if isinstance(i, dict) and i.get("pali"):
            por_pali_doc[i["pali"].lower()] = i.get("tabla", [])[2:]

    dif_doc = dif_dia = comparadas = 0
    for inf in infl["inflexiones"]:
        pali = inf["pali"].lower()
        bueno = [f[1:] for f in inf["filas"]]

        doc = por_pali_doc.get(pali)
        if doc:
            comparadas += 1
            for j, fila in enumerate(bueno):
                for k, celda in enumerate(fila):
                    otra = doc[j][k + 1] if k + 1 < len(doc[j]) else ""
                    if normaliza_term(celda) != normaliza_term(otra):
                        print(f"   {pali} · fila {j + 1} col {k + 1}: "
                              f"índice «{celda}» ≠ documento «{otra}»")
                        dif_doc += 1

        dia = diapos.get(pali)
        if dia:
            for j, fila in enumerate(bueno):
                for k, celda in enumerate(fila):
                    otra = dia[j][k] if k < len(dia[j]) else ""
                    if normaliza_term(celda) != normaliza_term(otra):
                        print(f"   {pali} · fila {j + 1} col {k + 1}: "
                              f"índice «{celda}» ≠ diapositiva «{otra}»")
                        dif_dia += 1

    print(f"   {comparadas} tablas cotejadas con el documento · "
          f"{len(diapos)} halladas en las diapositivas")
    print(f"   difieren del documento: {dif_doc}  "
          f"(esperado: el documento da una sola forma por casilla)")
    print(f"   difieren de las diapositivas: {dif_dia}")
    return dif_dia


# --------------------------------------------------------------------------
# El gaṇa, cotejado con /recursos/raices/
# --------------------------------------------------------------------------
#
# Las dos páginas dicen, cada una por su lado, a qué gaṇa pertenece una raíz:
#
#   /verbo/  lo dice sin nombrarlo, citando en la escalera el sutta que da el
#            signo de conjugación de su grupo — «Svādito ṇu-ṇā-uṇā ca» para
#            «su», Kacc. §448.
#   /raices/ lo dice con todas las letras, en la referencia del Saddanīti que
#            acompaña a cada raíz: «IV 219» es gaṇa IV, página 219.
#
# Que coincidan no está garantizado por nada: son dos obras distintas leídas
# por caminos distintos. Por eso se comprueba. Y es el cotejo que hace falta
# antes de enlazar una página con la otra: enlazar dos fichas que se
# contradicen sería peor que no enlazarlas.
#
# Ni el número de sutta ni el gaṇa se escriben a mano. El sutta se nombra a sí
# mismo —«Bhūvādito», «Rudhādito»…— y la tabla de los ocho grupos del propio
# documento «Verbo» fija el orden; de ahí sale el número romano.

ROMANOS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
RE_GANA_TABLA = re.compile(r"\(([a-zāīūṇṭḍṃñḷ]+)ādi-gaṇa\)", re.I)
RE_SUTTA_GANA = re.compile(r"\*\*(\d+)\\?\.\s*\d+\\?\.\s*"
                           r"([A-Za-zāīūṇṭḍṃñḷ]+)ādito\b")


def mapa_sutta_gana(verbo):
    """{num_kacc: «IV»} — qué gaṇa implica citar cada sutta de signo."""
    orden = {}
    for i, fila in enumerate(verbo.get("ganas", [])[1:]):
        m = RE_GANA_TABLA.search(" ".join(fila))
        if m and i < len(ROMANOS):
            orden[m.group(1).lower()] = ROMANOS[i]
    fuera = {}
    for patron in ("kaccayana/*.md", "docs/*.md"):
        for ruta in sorted(glob.glob(os.path.join(RAIZ, patron))):
            with open(ruta, encoding="utf-8") as fh:
                for m in RE_SUTTA_GANA.finditer(fh.read()):
                    gana = orden.get(m.group(2).lower())
                    if gana:
                        fuera.setdefault(int(m.group(1)), gana)
    return fuera


def indice_raices():
    """{lema normalizado: [entradas]} de recursos/raices/raices.json."""
    if not os.path.exists(RAICES):
        return None
    datos = json.load(open(RAICES, encoding="utf-8"))
    idx = {}
    for r in datos.get("raices", []):
        formas = r["raices"] if isinstance(r["raices"], list) else [r["raices"]]
        for f in formas:
            idx.setdefault(normalizar(f), []).append(r)
    return idx


PREFIJOS = ("vi-", "anu-", "upa-", "sam-", "pa-", "ā-")


def entradas_de(lema, idx):
    """Las entradas de raices.json de un lema, probando sin prefijo."""
    ents = idx.get(normalizar(lema))
    if ents:
        return ents, lema
    for pre in PREFIJOS:
        if lema.startswith(pre):
            ents = idx.get(normalizar(lema[len(pre):]))
            if ents:
                return ents, lema[len(pre):]
    return [], lema


def cotejar_gana(verbo, escs):
    """El gaṇa de cada escalera contra el del Saddanīti."""
    print("\n6. El gaṇa de cada raíz: /verbo/ contra /recursos/raices/")
    idx = indice_raices()
    if idx is None:
        print("   no está recursos/raices/raices.json; no se coteja")
        return 0
    suttas = mapa_sutta_gana(verbo)
    if len(suttas) != 8:
        print(f"   aviso — se dedujeron {len(suttas)} suttas de signo de "
              "conjugación; deberían ser 8. No se coteja.")
        return 0

    ok = mal = sin_gana = sin_entrada = 0
    for e in escs:
        gana = None
        for paso in e["pasos"]:
            for a in paso["autoridades"]:
                if a["kacc"] in suttas:
                    gana = suttas[a["kacc"]]
        if not gana:
            sin_gana += 1
            continue
        ents, usado = entradas_de(e["lema"], idx)
        if not ents:
            print(f"   {e['lema']}: sin entrada en raices.json")
            sin_entrada += 1
            continue
        suyos = {str(r.get("ref") or "").split()[0] for r in ents
                 if str(r.get("ref") or "").strip()}
        if gana in suyos:
            ok += 1
        else:
            mal += 1
            print(f"   ✗ {e['lema']}: /verbo/ dice gaṇa {gana}; el Saddanīti, "
                  f"{', '.join(sorted(suyos)) or '—'}")
    print(f"   {ok} coinciden · {mal} discrepan · "
          f"{sin_entrada} sin entrada · {sin_gana} sin sutta de signo")
    return mal


def lemas_del_verbo(verbo, escs):
    """Los lemas que nombra /verbo/: los de las escaleras y los de las
    entradas de los paradigmas, sin el número de orden ni la glosa."""
    lemas = {e["lema"] for e in escs}
    for p in verbo.get("paradigmas", []):
        t = re.sub(r"^\d+[a-z]?-", "", p.get("entrada", "")).split("(")[0]
        if t.strip():
            lemas.add(t.strip())
    return lemas


def cobertura(verbo, escs):
    """Qué comparten /verbo/ y /recursos/raices/, en números.

    Lo usan la auditoría y **los dos generadores**: las cifras del globo del
    enlace cruzado salen de aquí y no se escriben a mano, de modo que se
    corrigen solas el día que cambie cualquiera de las dos páginas. Devuelve
    None si no está raices.json, y entonces el enlace no se publica.
    """
    idx = indice_raices()
    if idx is None:
        return None
    lemas = lemas_del_verbo(verbo, escs)
    hallados, huerfanos, homonimos = 0, [], []
    for l in sorted(lemas):
        ents, _ = entradas_de(l, idx)
        if not ents:
            huerfanos.append(l)
            continue
        hallados += 1
        # un lema con varias fichas no se puede enlazar a una sola
        if len(ents) > 1:
            homonimos.append((l, len(ents)))
    datos = json.load(open(RAICES, encoding="utf-8"))
    return {"con_ficha": hallados, "lemas": len(lemas),
            "raices": len(datos.get("raices", [])),
            "huerfanos": huerfanos, "homonimos": homonimos}


def cobertura_raices(verbo, escs):
    """Cuántos lemas de /verbo/ tienen ficha en /recursos/raices/."""
    c = cobertura(verbo, escs)
    if c is None:
        return
    print(f"   cobertura para enlazar: {c['con_ficha']} de {c['lemas']} lemas "
          "tienen ficha")
    if c["huerfanos"]:
        print(f"      sin ficha: {', '.join(c['huerfanos'])}")
    if c["homonimos"]:
        print("      con homónimos, el enlace ha de mostrarlos todos: "
              + ", ".join(f"{l}×{n}" for l, n in c["homonimos"]))


def main():
    for ruta in (VERBO, DIAPOS):
        if not os.path.exists(ruta):
            sys.exit(f"Falta {os.path.relpath(ruta, RAIZ)}. Ejecutar antes "
                     "extraer_verbo.py y extraer_verbo_diapositivas.py.")
    doc = json.load(open(VERBO, encoding="utf-8"))
    dia = json.load(open(DIAPOS, encoding="utf-8"))
    infl = (json.load(open(INFLEXIONES, encoding="utf-8"))
            if os.path.exists(INFLEXIONES) else None)
    # Las escaleras PUBLICABLES, no las crudas del documento: es lo que la
    # página enseña y, por tanto, lo que hay que cotejar.
    from escaleras_verbo import escaleras as _escaleras
    escs = _escaleras(doc, dia)
    ru2kacc = concordancia()
    problemas = 0

    # ---------------------------------------------------------------- 1
    print("1. Pares Kacc/Rū contra la concordancia del repositorio")
    malos = comprobados = 0
    for kacc, ru, donde in list(pares(doc, "documento")) + \
            list(pares(dia, "diapositiva")):
        comprobados += 1
        esperado = ru2kacc.get(ru)
        if esperado is None:
            print(f"   Rū {ru} no está en la concordancia — {donde}")
            malos += 1
        elif esperado != kacc:
            print(f"   Rū {ru} debería ser Kacc. §{esperado}, "
                  f"no §{kacc} — {donde}")
            malos += 1
    print(f"   {comprobados} citas comprobadas, {malos} discrepan")
    problemas += malos

    # ---------------------------------------------------------------- 2
    print("\n2. Documento contra diapositiva, paso a paso")
    # Se emparejan por la forma final, no por el lema: una misma raíz da
    # varias escaleras —«su» con ‘ṇu’ y con ‘ṇā’, «cura» con ‘ṇe’ y con
    # ‘ṇaya’—, y el documento deriva «vikkiṇāti» donde la diapositiva deriva
    # «kiṇāti», que son palabras distintas y no se deben cotejar.
    def resultado(esc):
        for paso in reversed(esc["pasos"]):
            if paso.get("resultado"):
                return normalizar(paso["resultado"])
        return ""

    por_forma = {}
    for esc in dia["escaleras"]:
        por_forma.setdefault(resultado(esc), []).append(esc)

    sin_cotejo, cotejadas, emparejadas = [], 0, set()
    for esc in doc["escaleras"]:
        candidatas = por_forma.get(resultado(esc), [])
        candidatas = [c for c in candidatas if id(c) not in emparejadas]
        if not candidatas:
            sin_cotejo.append(f"{esc['titulo']} → {resultado(esc)}")
            continue
        d = candidatas[0]
        emparejadas.add(id(d))
        cotejadas += 1
        cuerpos_doc = [cuerpo(p) for p in esc["pasos"]]
        cuerpos_dia = [cuerpo(p) for p in d["pasos"]]
        faltan = [c for c in cuerpos_dia if c not in cuerpos_doc and any(c)]
        sobran = [c for c in cuerpos_doc if c not in cuerpos_dia and any(c)]
        difpasos = len(d["pasos"]) - len(esc["pasos"])
        if faltan or sobran:
            print(f"   {esc['titulo']}  ({d['presentacion']})")
            print(f"     documento {len(esc['pasos'])} pasos, "
                  f"diapositiva {len(d['pasos'])}  ({difpasos:+d})")
            for c in faltan:
                print(f"     sólo en la diapositiva: "
                      f"{'+'.join(x for x in c if x)}")
            for c in sobran:
                print(f"     sólo en el documento:   "
                      f"{'+'.join(x for x in c if x)}")
    print(f"   {cotejadas} escaleras cotejadas")
    if sin_cotejo:
        print(f"   sin diapositiva que las coteje: {', '.join(sin_cotejo)}")

    solo_dia = [e for e in dia["escaleras"] if id(e) not in emparejadas]
    print(f"   sólo en las diapositivas: {len(solo_dia)}")
    for e in solo_dia:
        print(f"     {e['lema']:9s} {e['formacion'][:56]}  "
              f"({e['presentacion']})")

    # ---------------------------------------------------------------- 3
    print("\n3. Formas que retroceden dentro de una escalera")
    retrocesos = 0
    for datos, donde in ((doc, "documento"), (dia, "diapositiva")):
        for esc in datos["escaleras"]:
            etiqueta = esc.get("titulo") or esc.get("lema")
            vistas = []
            for paso in esc["pasos"]:
                raiz = normalizar(paso.get("raiz", ""))
                if not raiz:
                    continue
                if len(vistas) >= 2 and raiz == vistas[-2] and \
                        raiz != vistas[-1]:
                    print(f"   {donde} · {etiqueta} · paso {paso['n']}: "
                          f"vuelve a «{paso['raiz']}» tras «{vistas[-1]}»")
                    retrocesos += 1
                vistas.append(raiz)
    print(f"   {retrocesos} retrocesos")
    problemas += retrocesos

    # ---------------------------------------------------------------- 4
    print("\n4. Ligaduras rotas del PDF")
    rotas = 0
    for esc in dia["escaleras"]:
        for paso in esc["pasos"]:
            m = RE_LIGADURA.search(paso.get("operacion", ""))
            if m:
                print(f"   {esc['lema']} · paso {paso['n']}: "
                      f"{paso['operacion'][:60]}")
                rotas += 1
    print(f"   {rotas} restos")
    problemas += rotas

    if infl:
        problemas += cotejar_inflexiones(infl, doc)

    problemas += cotejar_gana(doc, escs)
    cobertura_raices(doc, escs)

    print(f"\n{'sin problemas' if not problemas else f'{problemas} a revisar'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
