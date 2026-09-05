#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el glosario de terminología gramatical pāḷi.

    python3 herramientas/generar_glosario.py

DOS FUENTES PRINCIPALES, Y UNA TERCERA INTERNA.

  1. recursos/glosario/nandisena.json  el «Glosario de términos gramaticales
     de la lengua pali», de Bhikkhu Nandisena (IEBH, 2013). 649 entradas con
     definición en ESPAÑOL y referencia a Kac., Rū., Sad. y Nir. Su español
     es suyo y se reproduce literal.
  2. recursos/glosario/glosario.json   el Conspectus Terminorum (saññāmātikā)
     de Helmer Smith, Saddanīti IV, pp. 1105-1148, con la definición en
     FRANCÉS, transcrito a ojo del escaneo.
  3. comun/glosario.md                 la lista normativa de este repositorio:
     qué palabra castellana se usa para cada término, decidida sobre la
     marcha al traducir. Es interna, no una obra.

  recursos/glosario/glosario-ingles.json  la propuesta inglesa para la lista 3
  recursos/glosario/ingles.json           el inglés del Glosario de Nandisena
                                          (lista 1): se comprueba siempre y se
                                          publica sólo con «adjudicado»: true
  recursos/glosario/plantilla.html        el maquetado y la lógica

y escribe site/recursos/glosario/index.html.

LAS DOS FUENTES NO SON INDEPENDIENTES, y conviene no presentarlas como si lo
fueran: en su propia bibliografía, Nandisena declara que le fue «muy útil» el
Conspectus de Smith. La coincidencia entre las dos, por tanto, no es un cotejo
de testigos separados; es filiación.

QUÉ ESTÁ ADJUDICADO. El español de Nandisena lo firma él. El español de
comun/glosario.md lo fijó IEBH. Todo lo demás —el español y el inglés de las
entradas del Conspectus, y el inglés de las otras dos— es PROPUESTA del
traductor, y la página lo dice en su cabecera y en cada ficha.

Antes de escribir comprueba la integridad de los datos: NFC en todo el pāḷi,
que ninguna entrada del Conspectus se quede sin glosa francesa, que las
páginas caigan dentro de 1105-1148, que los epígrafes tengan la forma N.N.N y
que no haya lemas repetidos dentro de un mismo epígrafe. Si algo no cuadra,
no publica.
"""

import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NORMATIVO = os.path.join(RAIZ, "comun", "glosario.md")
NANDISENA = os.path.join(RAIZ, "recursos", "glosario", "nandisena.json")
DATOS = os.path.join(RAIZ, "recursos", "glosario", "conspectus.json")
PAGINAS_DIR = os.path.join(RAIZ, "recursos", "glosario", "conspectus")
DIPLOMADO = os.path.join(RAIZ, "recursos", "glosario", "diplomado.json")
INGLES = os.path.join(RAIZ, "recursos", "glosario", "glosario-ingles.json")
INGLES_NANDISENA = os.path.join(RAIZ, "recursos", "glosario", "ingles.json")
PLANTILLA = os.path.join(RAIZ, "recursos", "glosario", "plantilla.html")
DESTINO = os.path.join(RAIZ, "site", "recursos", "glosario", "index.html")

PAGINAS = (1105, 1148)

# El orden del alfabeto pāḷi, que no es el latino. Se usa para ordenar los
# lemas dentro de cada epígrafe y en la vista alfabética.
ALFABETO = ["a", "ā", "i", "ī", "u", "ū", "e", "o",
            "k", "kh", "g", "gh", "ṅ",
            "c", "ch", "j", "jh", "ñ",
            "ṭ", "ṭh", "ḍ", "ḍh", "ṇ",
            "t", "th", "d", "dh", "n",
            "p", "ph", "b", "bh", "m",
            "y", "r", "l", "ḷ", "v", "s", "h"]
ORDEN = {c: i for i, c in enumerate(ALFABETO)}


def clave_pali(s):
    """Ordena una cadena pāḷi por el alfabeto pāḷi, ignorando lo que no es
    letra. Los dígrafos aspirados cuentan como una letra."""
    s = unicodedata.normalize("NFC", s).lower()
    s = re.sub(r"[^a-zāīūṅñṭḍṇḷṃ]", "", s)
    salida, i = [], 0
    while i < len(s):
        if i + 1 < len(s) and s[i:i + 2] in ORDEN:
            salida.append(ORDEN[s[i:i + 2]])
            i += 2
        else:
            salida.append(ORDEN.get(s[i], 99))
            i += 1
    return salida


def leer_normativo(ruta):
    """Lee la tabla de comun/glosario.md.

    Formato: | *lema* | español | nota | fijado en |
    La entrada cuyo lema es «—» fija una palabra castellana, no una pāḷi; se
    guarda con la marca `sin_lema` para que la página no la enseñe como si
    fuera un término pāḷi.
    """
    entradas = []
    for linea in open(ruta, encoding="utf-8"):
        linea = linea.strip()
        if not linea.startswith("|"):
            continue
        celdas = [c.strip() for c in linea.strip("|").split("|")]
        if len(celdas) < 4:
            continue
        lema, es, nota, fijado = celdas[0], celdas[1], celdas[2], celdas[3]
        if lema.lower() in ("pāḷi", "----", "---- ") or set(lema) <= set("- "):
            continue
        sin_lema = lema == "—"
        # quitar cursivas y negritas de markdown, y las barras de escape
        limpio = re.sub(r"[*_]", "", lema).strip()
        es_limpio = re.sub(r"\*\*(.+?)\*\*", r"\1", es).replace("\\[", "[").replace("\\]", "]")
        nota = re.sub(r"\*\*(.+?)\*\*", r"\1", nota).replace("\\[", "[").replace("\\]", "]")
        # «Fijado en» puede llevar, tras una raya, las referencias por sutta
        # («cosecha s. 57, IEBH 2026-09-05 — Kacc. §291 · Nyāsa §286, §291»);
        # van aparte, para que la ficha las enseñe como enseña las de Nandisena.
        refs = []
        if " — " in fijado:
            fijado, tras = fijado.split(" — ", 1)
            if not tras.startswith("sin sutta"):
                refs = [r.strip() for r in tras.split(" · ") if r.strip()]
            else:
                fijado = fijado + " — " + tras
        entradas.append({
            "pali": limpio,
            "es": es_limpio,
            "nota": nota or None,
            "fijado_en": fijado or None,
            "refs": refs,
            "fuente": "glosario",
            "sin_lema": sin_lema,
        })
    return entradas


def verificar(conspectus, normativo, ingles):
    fallos, avisos = [], []

    if not conspectus:
        fallos.append("no hay ninguna entrada del Conspectus")
    if not normativo:
        fallos.append("comun/glosario.md no ha dado ninguna entrada")

    vistos = set()
    for t in conspectus:
        quien = "{0} ({1})".format(t.get("pali", "?"), t.get("epigrafe", "?"))
        for campo in ("pali", "fr", "es", "en", "epigrafe", "pagina"):
            if not t.get(campo):
                fallos.append("{0}: sin «{1}»".format(quien, campo))
        pag = t.get("pagina")
        if isinstance(pag, int) and not PAGINAS[0] <= pag <= PAGINAS[1]:
            fallos.append("{0}: página {1} fuera de {2}-{3}".format(
                quien, pag, *PAGINAS))
        ep = t.get("epigrafe", "")
        if ep != "—" and not re.fullmatch(r"\d+(\.\d+)*", ep):
            fallos.append("{0}: epígrafe con forma rara".format(quien))
        clave = (t.get("pali"), ep)
        if clave in vistos:
            fallos.append("{0}: lema repetido dentro del mismo epígrafe".format(quien))
        vistos.add(clave)

    crudo = json.dumps([conspectus, normativo, ingles], ensure_ascii=False)
    if "�" in crudo:
        fallos.append("hay caracteres sin descifrar (�)")
    if unicodedata.normalize("NFC", crudo) != crudo:
        fallos.append("hay pāḷi que no está en NFC")

    faltan_en = [n["pali"] for n in normativo
                 if not n["sin_lema"] and n["pali"] not in ingles]
    if faltan_en:
        avisos.append("sin propuesta inglesa en glosario-ingles.json: "
                      + ", ".join(faltan_en))

    sobran = [k for k in ingles
              if not k.startswith("[")
              and k not in {n["pali"] for n in normativo}]
    if sobran:
        avisos.append("glosario-ingles.json tiene claves que ya no están en "
                      "comun/glosario.md: " + ", ".join(sobran))

    return fallos, avisos


def claves_nandisena(entradas):
    """La clave de cada entrada del Glosario en ingles.json: el lema tal
    cual, y «lema|N» cuando el mismo lema tiene más de una entrada (los
    homónimos «adhikaraṇa 1 / 2» y el «adhikāra» que sale dos veces sin
    número). N es el ordinal de aparición, de 1 en adelante."""
    cuenta = {}
    for e in entradas:
        cuenta[e["pali"]] = cuenta.get(e["pali"], 0) + 1
    visto = {}
    claves = []
    for e in entradas:
        if cuenta[e["pali"]] > 1:
            visto[e["pali"]] = visto.get(e["pali"], 0) + 1
            claves.append("{0}|{1}".format(e["pali"], visto[e["pali"]]))
        else:
            claves.append(e["pali"])
    return claves


def verificar_ingles_nandisena(entradas, ing):
    """Comprueba el borrador inglés del Glosario de Nandisena entrada por
    entrada contra el español, y devuelve (fallos, avisos, mapa), donde mapa
    va de la clave a la entrada del borrador. No decide si se publica: eso
    lo dice «adjudicado», y lo aplica main()."""
    fallos, avisos = [], []
    borr = ing.get("entradas", {})
    claves = claves_nandisena(entradas)
    por_clave = dict(zip(claves, entradas))

    sobran = [k for k in borr if k not in por_clave]
    if sobran:
        fallos.append("ingles.json tiene claves que no están en nandisena.json: "
                      + ", ".join(sobran[:12]))
    for k, b in borr.items():
        e = por_clave.get(k)
        if e is None:
            continue
        if not isinstance(b, dict) or not (b.get("en") or "").strip():
            fallos.append("{0}: la entrada inglesa está vacía".format(k))
            continue
        if e.get("remite_a"):
            fallos.append("{0}: es una remisión («v. {1}») y no se traduce"
                          .format(k, e["remite_a"]))
        if not e.get("es"):
            fallos.append("{0}: no tiene español que traducir".format(k))
        if not b.get("fuente"):
            avisos.append("{0}: sin «fuente» del término".format(k))
        for campo in ("en", "termino", "fuente", "nota"):
            v = b.get(campo)
            if isinstance(v, str) and unicodedata.normalize("NFC", v) != v:
                fallos.append("{0}: «{1}» no está en NFC".format(k, campo))
        # Lo que el español cita entre comillas —los ejemplos pāḷi— tiene
        # que estar en el inglés: la traducción no quita ejemplos.
        citas_es = re.findall(r'"([^"]{2,})"', e["es"])
        for c in citas_es:
            if re.search(r"[āīūṃṅñṭḍṇḷ]", c) and c not in b["en"]:
                avisos.append("{0}: el inglés no trae el ejemplo «{1}»".format(k, c))
    return fallos, avisos, {k: borr[k] for k in borr if k in por_clave}


def main():
    for ruta in (NORMATIVO, DATOS, INGLES, PLANTILLA):
        if not os.path.exists(ruta):
            print("Falta {0}".format(os.path.relpath(ruta, RAIZ)))
            return 1

    datos = json.load(open(DATOS, encoding="utf-8"))
    ing = json.load(open(INGLES, encoding="utf-8"))

    # una página, un archivo: recursos/glosario/conspectus/pNNNN.json
    conspectus = []
    for nombre in sorted(os.listdir(PAGINAS_DIR)):
        if not re.fullmatch(r"p\d{4}\.json", nombre):
            continue
        conspectus += json.load(
            open(os.path.join(PAGINAS_DIR, nombre), encoding="utf-8"))["terminos"]
    normativo = leer_normativo(NORMATIVO)

    dip = {}
    if os.path.exists(DIPLOMADO):
        dip = json.load(open(DIPLOMADO, encoding="utf-8"))

    nand = {"entradas": [], "fuente": None, "notas_al_pie": []}
    if os.path.exists(NANDISENA):
        nand = json.load(open(NANDISENA, encoding="utf-8"))
    else:
        print("  aviso — falta recursos/glosario/nandisena.json; se publica "
              "sin el Glosario de Nandisena. Se obtiene con "
              "herramientas/extraer_glosario_nandisena.py")

    mapa_en = ing.get("ingles", {})
    for n in normativo:
        clave = "[{0}]".format(n["es"].split(".")[0]) if n["sin_lema"] else n["pali"]
        n["en"] = mapa_en.get(clave)
        n["en_adjudicado"] = bool(ing.get("adjudicado"))

    fallos, avisos = verificar(conspectus, normativo, mapa_en)

    # ---- el inglés del Glosario de Nandisena ---------------------------
    # recursos/glosario/ingles.json. Se comprueba siempre; se INYECTA sólo
    # lo adjudicado, porque son palabras del IEBH. La adjudicación va POR
    # TANDA (sesión 57): cada entrada dice «tanda»: N, y se publica si
    # ing["tanda"][N]["adjudicado"] es true. Una entrada sin «tanda» sigue
    # el «adjudicado» general del archivo. Las demás quedan redactadas y
    # sin publicar: el modo inglés enseña ahí el español y lo dice.
    ing_nand = {"adjudicado": False, "entradas": {}}
    nand_en_total = 0
    nand_en_adjudicadas = 0
    if os.path.exists(INGLES_NANDISENA) and nand["entradas"]:
        ing_nand = json.load(open(INGLES_NANDISENA, encoding="utf-8"))
        f2, a2, borr = verificar_ingles_nandisena(nand["entradas"], ing_nand)
        fallos += f2
        avisos += a2
        nand_en_total = len(borr)
        tandas = ing_nand.get("tanda", {})

        def adjudicada(b):
            t = b.get("tanda")
            if t is None:
                return bool(ing_nand.get("adjudicado"))
            return bool(tandas.get(str(t), {}).get("adjudicado"))

        for clave, e in zip(claves_nandisena(nand["entradas"]), nand["entradas"]):
            if clave in borr and adjudicada(borr[clave]):
                e["en"] = borr[clave]["en"]
                nand_en_adjudicadas += 1

    if fallos:
        print("No se publica. {0} fallo(s):".format(len(fallos)))
        for f in fallos[:40]:
            print("  · " + f)
        if len(fallos) > 40:
            print("  … y {0} más".format(len(fallos) - 40))
        return 1
    for a in avisos:
        print("  aviso — " + a)

    conspectus.sort(key=lambda t: ([int(x) for x in t["epigrafe"].split(".")]
                                   if t["epigrafe"] != "—" else [0],
                                   clave_pali(t["pali"])))
    normativo.sort(key=lambda n: clave_pali(n["pali"]))

    # ---- el cotejo entre las dos fuentes -------------------------------
    # Se casan por lema desnudo: sin diacríticos, sin guiones y sin la marca
    # de homónimo. Nandisena escribe «akkhara-lopa» donde Smith escribe
    # «akkharalopa», y «niggahīta» donde el capítulo escribe «niggahita»;
    # casar por la forma literal perdería justamente los casos interesantes.
    def desnudo(s):
        s = unicodedata.normalize("NFD", (s or "").lower())
        s = "".join(c for c in s if unicodedata.category(c) != "Mn")
        return re.sub(r"[^a-z]", "", s)

    por_lema = {}
    for e in nand["entradas"]:
        por_lema.setdefault(desnudo(e["pali"]), []).append(e)

    en_ambas = 0
    for t in conspectus:
        gemelas = por_lema.get(desnudo(t["pali"]), [])
        if gemelas:
            en_ambas += 1
            t["nandisena"] = [{"pali": g["pali"], "es": g.get("es"),
                               "homonimo": g.get("homonimo"),
                               "refs": g.get("refs", []),
                               "remite_a": g.get("remite_a")}
                              for g in gemelas]

    # ---- la vista alfabética única -------------------------------------
    # Las dos obras y la lista normativa, en un solo orden alfabético pāḷi y
    # UNA FICHA POR LEMA. Se agrupa por el mismo lema desnudo con que se
    # cotejan más arriba, de modo que «akkhara-lopa» y «akkharalopa» caen
    # juntos, y con ellos las 132 parejas cuya grafía no coincide — que son
    # justamente las que conviene ver de una vez.
    #
    # Aquí NO van los datos, sino los ÍNDICES a las tres listas que ya
    # viajan en el JSON: repetir los objetos doblaría el peso de la página.
    # El orden es el del alfabeto pāḷi, no el latino.
    #
    # El lema que se enseña sale por prelación —la lista normativa manda,
    # luego Nandisena, que es la edición base, y por último Smith—, y cuando
    # el grupo trae más de una grafía se enseñan TODAS con su fuente: la
    # divergencia es dato, no ruido.
    # OJO CON LA CLAVE, que es donde estuvo el error. El cotejo entre obras
    # se hace por lema DESNUDO —sin diacríticos—, y para casar a Nandisena
    # con Smith está bien: es lo que encuentra niggahita / niggahīta. Pero
    # como clave de FUSIÓN es demasiado ancha y junta palabras distintas:
    # pada con pāda, karaṇa con kāraṇa, akāra con ākāra, y los cuatro
    # nombres de letra nakāra, ñakāra, ṅakāra y ṇakāra en una sola ficha.
    # Eran 42 grupos, y ahí la tilde no es una variante: es la palabra.
    #
    # De modo que se funde sólo lo que difiere en guiones, paréntesis,
    # apóstrofos o espacios —akkhara-lopa = akkharalopa, suddha(ssara) =
    # suddhassara—, y las grafías que difieren en LETRA O DIACRÍTICO se
    # quedan en fichas aparte, enlazadas entre sí con un «véase también».
    # Decidir si dos de ésas son la misma palabra es del IEBH, no del
    # generador: es justamente lo que la colación viene decidiendo caso por
    # caso.
    def clave_fusion(s):
        s = unicodedata.normalize("NFC", (s or "")).lower()
        return re.sub(r"[^0-9a-zāīūṅñṭḍṇḷṃ]", "", s)

    grupos = {}
    for i, t in enumerate(conspectus):
        grupos.setdefault(clave_fusion(t["pali"]), {"c": [], "n": [], "g": []})["c"].append(i)
    for i, e in enumerate(nand["entradas"]):
        grupos.setdefault(clave_fusion(e["pali"]), {"c": [], "n": [], "g": []})["n"].append(i)
    for i, e in enumerate(normativo):
        if e["sin_lema"]:
            continue
        grupos.setdefault(clave_fusion(e["pali"]), {"c": [], "n": [], "g": []})["g"].append(i)

    agrupado = []
    for clave, ix in grupos.items():
        grafias = []
        for i in ix["g"]:
            grafias.append([normativo[i]["pali"], "norma"])
        for i in ix["n"]:
            grafias.append([nand["entradas"][i]["pali"], "Nandisena"])
        for i in ix["c"]:
            grafias.append([conspectus[i]["pali"], "Smith"])
        vistas, unicas = set(), []
        for p, f in grafias:
            if p not in vistas:
                vistas.add(p)
                unicas.append([p, f])
        entrada = {"id": clave, "p": unicas[0][0],
                   "c": ix["c"], "n": ix["n"], "g": ix["g"]}
        if len(unicas) > 1:
            entrada["gr"] = unicas
        agrupado.append(entrada)
    agrupado.sort(key=lambda e: clave_pali(e["p"]))

    con_varias_grafias = sum(1 for e in agrupado if "gr" in e)

    # «Véase también»: las fichas que sólo se distinguen por un diacrítico o
    # por una letra. Antes se fundían en silencio; ahora se enlazan, que es
    # lo que permite ver a la vez el niggahita de Nandisena y el niggahīta
    # de Smith sin afirmar que son la misma palabra.
    por_desnudo = {}
    for e in agrupado:
        por_desnudo.setdefault(desnudo(e["p"]), []).append(e)
    con_vease = 0
    for hermanas in por_desnudo.values():
        if len(hermanas) < 2:
            continue
        con_vease += len(hermanas)
        for e in hermanas:
            e["v"] = [o["id"] for o in hermanas if o is not e]

    hechas = sorted({t["pagina"] for t in conspectus})
    faltan = PAGINAS[1] - PAGINAS[0] + 1 - len(hechas)
    estado = ("completo" if not faltan else
              "en curso — {0} de {1} páginas".format(
                  len(hechas), PAGINAS[1] - PAGINAS[0] + 1))
    datos["estado"] = estado

    salida = {
        "nota": datos["_nota"],
        "version": datos["version"],
        "estado": estado,
        "fuentes": datos["fuentes"],
        "secciones": datos["secciones"],
        "partes": datos.get("partes", {}),
        "plan": datos["plan_de_smith"],
        "ingles_adjudicado": bool(ing.get("adjudicado")),
        "ingles_adjudicado_por": ing.get("adjudicado_por"),
        "nandisena_en": {
            "adjudicado": bool(ing_nand.get("adjudicado")),
            "adjudicado_por": ing_nand.get("adjudicado_por"),
            "fecha": ing_nand.get("fecha"),
            "redactadas": nand_en_total,
            "adjudicadas": nand_en_adjudicadas,
            "total": len(nand["entradas"]),
        },
        "agrupado": agrupado,
        "conspectus": conspectus,
        "normativo": normativo,
        "nandisena": nand["entradas"],
        "fuente_nandisena": nand.get("fuente"),
        "obras_nandisena": nand.get("obras", {}),
        "notas_nandisena": nand.get("notas_al_pie", []),
        "en_ambas": en_ambas,
        "diplomado": dip,
    }

    plantilla = open(PLANTILLA, encoding="utf-8").read()
    marca = re.search(r"/\*__DATOS__\*/.*?/\*__FIN__\*/", plantilla, re.S)
    if not marca:
        print("La plantilla no tiene el marcador /*__DATOS__*/…/*__FIN__*/")
        return 1
    html = (plantilla[:marca.start()]
            + json.dumps(salida, ensure_ascii=False, separators=(",", ":"))
            + plantilla[marca.end():])

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    open(DESTINO, "w", encoding="utf-8").write(html)

    paginas = sorted({t["pagina"] for t in conspectus})
    conflictos = sum(1 for t in conspectus if t.get("conflicto"))
    dudas = sum(1 for t in conspectus if t.get("duda"))
    total_paginas = PAGINAS[1] - PAGINAS[0] + 1
    print("{0} entradas de Nandisena · {1} términos del Conspectus · "
          "{2} normativos → {3} ({4} KB)".format(
              len(nand["entradas"]), len(conspectus), len(normativo),
              os.path.relpath(DESTINO, RAIZ), len(html) // 1024))
    print("  Conspectus, {0}: {1} páginas de {2} ({3}-{4})".format(
        datos["estado"], len(paginas), total_paginas, paginas[0], paginas[-1]))
    print("  vista alfabética: {0} lemas de las tres fuentes en una sola lista; "
          "{1} traen más de una grafía y {2} llevan «véase también» hacia una "
          "grafía vecina".format(len(agrupado), con_varias_grafias, con_vease))
    if nand["entradas"]:
        pct = 100.0 * en_ambas / len(conspectus)
        print("  en las dos fuentes: {0} de los {1} términos del Conspectus "
              "({2:.0f}%) tienen entrada en Nandisena".format(
                  en_ambas, len(conspectus), pct))
    if conflictos:
        print("  {0} entrada(s) donde Smith y comun/glosario.md no dicen lo "
              "mismo".format(conflictos))
    if dudas:
        print("  {0} entrada(s) con <!-- DUDA -->, por cotejar sobre la "
              "imagen".format(dudas))
    if not salida["ingles_adjudicado"]:
        print("  el inglés de las entradas normativas va SIN adjudicar: la "
              "página lo advierte")
    if nand["entradas"] and nand_en_total:
        print("  inglés del Glosario de Nandisena: {0} de {1} entradas redactadas; "
              "{2} PUBLICADAS (tandas adjudicadas por {3}) y {4} sin adjudicar, "
              "comprobadas y no publicadas (docs/glosario/ingles-por-adjudicar.md)"
              .format(nand_en_total, len(nand["entradas"]), nand_en_adjudicadas,
                      ing_nand.get("adjudicado_por") or "—",
                      nand_en_total - nand_en_adjudicadas))
    return 0


if __name__ == "__main__":
    sys.exit(main())
