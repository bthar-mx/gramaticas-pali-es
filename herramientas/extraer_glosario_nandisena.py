#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrae el «Glosario de términos gramaticales de la lengua pali» de Bhikkhu
Nandisena (IEBH, 2013) a recursos/glosario/nandisena.json.

    python3 herramientas/extraer_glosario_nandisena.py <ruta-al-pdf>

El PDF sí tiene capa de texto —a diferencia del escaneo del Saddanīti—, pero
va a dos columnas, y `pdftotext` sin más las entrelaza. Aquí se recorta cada
columna por su caja y se leen en orden: izquierda entera, luego derecha.

Cada entrada tiene la forma

    lema , definición; definición. Ej., "…". (Rū. §285)

y las líneas de continuación van sangradas. Esa sangría es la única marca
fiable de dónde empieza una entrada y dónde sigue la anterior.

El PDF NO viaja en el repositorio, como los demás PDF de fuentes. Este guion
sólo hay que volver a correrlo si cambia la edición.
"""

import json
import os
import re
import subprocess
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, "recursos", "glosario", "nandisena.json")

PRIMERA = 2      # la 1 es la portada
ULTIMA = 32      # la 33 es la bibliografía
CANAL = 307      # la canal entre las dos columnas, en puntos: la izquierda
                 # acaba hacia x=290 y la derecha empieza hacia x=324
SANGRIA = 6      # a partir de cuántos puntos por dentro del margen una
                 # línea cuenta como continuación y no como lema nuevo

# Las obras que Nandisena cita entre paréntesis al cerrar cada entrada.
OBRAS = {
    "Kac.": "Kaccāyana-byākaraṇa",
    "Rū.": "Padarūpasiddhi",
    "Sad.": "Saddanīti",
    "Nir.": "Niruttidīpanī",
    "Pay.": "Payogasiddhi",
    "KhpA.": "Khuddakapāṭha-aṭṭhakathā",
    "Mogg.": "Moggallāna",
    "IP": "Introduction to Pali (Warder)",
    "PEG": "Pali-English Technical Glossary (Ñāṇamoli)",
    "Monier": "A Sanskrit-English Dictionary",
    "NPC": "New Pali Course (Buddhadatta)",
    "Smith": "Saddanīti, ed. Helmer Smith",
}


def palabras(pdf):
    """Todas las palabras del PDF con su caja, por página.

    Se lee `pdftotext -bbox` en vez de recortar columnas con -x/-W, y la razón
    es concreta: **las notas al pie de Nandisena ocupan el ancho entero de la
    página**, no una columna. Recortando por la canal se partían por la mitad,
    y sus mitades se colaban en el cuerpo como si fueran entradas («erdo con
    Rū. Sublime dijo esto a los bhikkhus»). Con las coordenadas delante, la
    canal y el pie se distinguen sin cortar nada.
    """
    r = subprocess.run(["pdftotext", "-bbox", "-f", str(PRIMERA),
                        "-l", str(ULTIMA), pdf, "-"],
                       capture_output=True, text=True, check=True)
    paginas, actual = [], None
    for m in re.finditer(r'<page[^>]*>|<word xMin="([\d.]+)" yMin="([\d.]+)" '
                         r'xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>',
                         r.stdout, re.S):
        if m.group(0).startswith("<page"):
            actual = []
            paginas.append(actual)
        elif actual is not None:
            actual.append({"x0": float(m.group(1)), "y0": float(m.group(2)),
                           "x1": float(m.group(3)),
                           "t": desescapa(m.group(5))})
    return paginas


def desescapa(s):
    return (s.replace("&amp;", "&").replace("&lt;", "<")
             .replace("&gt;", ">").replace("&quot;", '"')
             .replace("&apos;", "'"))


TOLERANCIA_Y = 3.0   # puntos


def en_lineas(pal):
    """Agrupa palabras en líneas. Se llama por columna, nunca sobre la página
    entera: en una página a dos columnas, la línea izquierda y la derecha
    comparten la y y se fundirían en una sola.

    Las y se agrupan con tolerancia, no por igualdad: **las cursivas se
    asientan un punto más abajo que la redonda de su misma línea**. En
    «atthyattha , v. atthyattha-taddhita» la «v.» cursiva está en y=646,5 y
    las otras dos palabras en 645,75; agrupando por y exacta, la «v.» caía en
    una línea aparte y el lema salía como «atthyattha atthyattha-taddhita».
    """
    salida, ws, y_ref = [], [], None

    def cierra():
        if ws:
            fila = sorted(ws, key=lambda w: w["x0"])
            salida.append({"y": y_ref, "x0": fila[0]["x0"],
                           "texto": " ".join(w["t"] for w in fila)})

    for w in sorted(pal, key=lambda w: w["y0"]):
        if y_ref is None or w["y0"] - y_ref > TOLERANCIA_Y:
            cierra()
            ws, y_ref = [], w["y0"]
        ws.append(w)
    cierra()
    return salida


def donde_empieza_el_pie(pal):
    """La y de la primera línea del pie de página, o None si no hay.

    Lo que delata al pie es que **una sola palabra cruza la canal**: el cuerpo
    va a dos columnas y ninguna de sus palabras puede hacerlo, mientras que
    las notas ocupan el ancho entero. Desde esa línea hacia abajo, todo es pie.
    """
    cruzan = [w["y0"] for w in pal
              if w["x0"] < CANAL < w["x1"] and not es_folio(w)]
    return min(cruzan) - 2 if cruzan else None


def es_folio(w):
    """El número de página va solo, centrado y al pie — y por ir centrado
    cruza la canal, de modo que si no se aparta, se lleva por delante la
    detección del pie."""
    return re.fullmatch(r"\d{1,3}", w["t"].strip()) and w["y0"] > 715


def bloques(pdf):
    """Las columnas del cuerpo, en el orden en que se leen, y las notas al pie."""
    salida, pies = [], []
    for i, pal in enumerate(palabras(pdf)):
        pagina = PRIMERA + i
        corte = donde_empieza_el_pie(pal)
        pal = [w for w in pal if not es_folio(w)]
        cuerpo = [w for w in pal if corte is None or w["y0"] < corte]
        pie = [w for w in pal if corte is not None and w["y0"] >= corte]

        sobras = []
        for lim in ((0, CANAL), (CANAL, 10000)):
            col = [l for l in en_lineas([w for w in cuerpo
                                         if lim[0] <= w["x0"] < lim[1]])
                   if not re.fullmatch(r"\d{1,2}", l["texto"].strip())]
            # Cuando la palabra que cruza la canal cae en la segunda o tercera
            # línea de la nota, el corte por y deja arriba las primeras. Se
            # recogen aquí: una nota abre con su número, y **ninguna palabra
            # pāḷi empieza por un dígito**, así que a partir de esa línea, y
            # hasta el final de la columna, ya no hay cuerpo.
            margen = min((l["x0"] for l in col), default=0)
            corta = next((i for i, l in enumerate(col)
                          if l["x0"] <= margen + SANGRIA
                          and re.match(r"^\d{1,2}\s", l["texto"].strip())), None)
            if corta is not None:
                sobras += col[corta:]
                col = col[:corta]
            salida.append((pagina, col))

        texto_pie = limpia(" ".join(
            l["texto"] for l in sobras + en_lineas(pie)))
        if texto_pie:
            pies.append({"pagina": pagina, "texto": texto_pie})
    return salida, pies


def trocear(bqs):
    """Junta las líneas en entradas.

    Dentro de una columna el lema arranca en el margen y las líneas que lo
    continúan van sangradas. El margen se mide en cada columna, porque la
    izquierda y la derecha no empiezan en la misma x.
    """
    entradas, actual = [], None
    for pagina, lns in bqs:
        if not lns:
            continue
        margen = min(l["x0"] for l in lns)
        for l in lns:
            texto = limpia(l["texto"])
            if not texto:
                continue
            if l["x0"] > margen + SANGRIA:
                if actual is not None:
                    actual["lineas"].append(texto)
                continue
            # las cabeceras de letra van solas: «A», «Ā», «Kh»…
            if len(texto) <= 2 and texto.isupper():
                continue
            # ¿es de veras un lema, o una línea de cuerpo que el maquetado ha
            # dejado pegada al margen? Se mira la parte anterior a la coma:
            # si no está escrita en pāḷi, no abre entrada, continúa la anterior.
            cabeza = re.split(r"\s*[,=]\s*", texto, 1)[0]
            cabeza = re.sub(r"\s+\d$", "", cabeza)          # homónimo
            cabeza = re.sub(r"\s+lit\.$", "", cabeza)       # la errata de p. 6
            if not parece_lema(cabeza):
                if actual is not None:
                    actual["lineas"].append(texto)
                continue
            actual = {"pagina": pagina, "lineas": [texto]}
            entradas.append(actual)
    return entradas


# Un lema es pāḷi, y el pāḷi se escribe con estas letras y nada más. Sirve
# para distinguir un lema de una línea de cuerpo que, por accidente del
# maquetado, ha quedado pegada al margen: «son las siguientes: 1) Perfecto
# (parokkhā)» no es un lema, y «"hetu-kattu"» entrecomillado tampoco.
LETRAS_PALI = set("aāiīuūeokgcjñṭḍṇtdnpbmyrlḷvsh"
                  "AĀIĪUŪEOKGCJÑṬḌṆTDNPBMYRLḶVSH"
                  "ṃṅ ’'-")


# Palabras castellanas de función. Ninguna es pāḷi, y su presencia delata a
# una línea de cuerpo que ha quedado pegada al margen —al saltar de página, la
# continuación de «hetu-kattu» empieza sin sangrar con «hombre haga el
# trabajo, …»— y que si no, se publicaría como si fuera un término.
CASTELLANAS = {"el", "la", "los", "las", "un", "una", "unos", "unas", "de",
               "del", "que", "se", "no", "es", "en", "con", "por", "para",
               "su", "sus", "lo", "al", "como", "más", "este", "esta"}


def parece_lema(s):
    if not s or not all(c in LETRAS_PALI for c in s):
        return False
    return not (set(s.lower().split()) & CASTELLANAS)


def limpia(s):
    s = re.sub(r"\s+", " ", s).strip()
    # pdftotext parte palabras con guion al saltar de línea sólo cuando el
    # guion es del texto; aquí no se une nada, para no fabricar palabras.
    return unicodedata.normalize("NFC", s)


def partir(entrada):
    """De una entrada en bruto saca lema, homónimo, definición y referencias."""
    crudo = limpia(" ".join(entrada["lineas"]))

    # remisión pura: «akamma = akammaka»
    m = re.match(r"^(.+?)\s*=\s*(.+)$", crudo)
    if m and "," not in m.group(1) and len(m.group(1)) < 40:
        return {"pali": limpia(m.group(1)), "remite_a": limpia(m.group(2)),
                "es": None, "refs": [], "pagina": entrada["pagina"]}

    # Erratas de la edición: en «avutta-kattu lit., subjeto no mencionado»
    # falta la coma que separa el lema, de modo que el corte por la primera
    # coma se lleva el «lit.» dentro del lema. Se devuelve a la definición y
    # se deja constancia; no se toca nada más del texto de Nandisena.
    errata = None
    m = re.match(r"^(.+?)\s+(lit\.\s*,.*)$", crudo, re.S)
    if m and parece_lema(m.group(1)):
        crudo = m.group(1) + " , " + m.group(2)
        errata = ("En el impreso falta la coma que separa el lema: dice "
                  "«{0} lit., …». Se restituye la coma; el texto va intacto."
                  .format(m.group(1)))

    m = re.match(r"^(.+?)\s*,\s*(.*)$", crudo, re.S)
    if not m:
        return None
    lema, resto = limpia(m.group(1)), limpia(m.group(2))

    # Un compuesto largo parte de línea por su guion, y al juntar las líneas
    # queda «avadhāraṇapubbapada- kammadhāraya». El guion es del compuesto;
    # el espacio, del salto de línea. Se cierra sólo en el lema: la definición
    # se deja como está, que es prosa de Nandisena.
    lema = re.sub(r"-\s+", "-", lema)

    # los homónimos van numerados: «adhikaraṇa 1», «adhikaraṇa 2»
    homonimo = None
    m2 = re.match(r"^(.+?)\s+(\d)$", lema)
    if m2:
        lema, homonimo = limpia(m2.group(1)), int(m2.group(2))

    refs = []
    for cita in re.findall(r"\(([^()]*(?:§|\bi{1,3}\b|\d)[^()]*)\)$", resto):
        for parte in cita.split(";"):
            refs.append(limpia(parte))
    if refs:
        resto = limpia(re.sub(r"\s*\([^()]*\)$", "", resto))

    # La llamada de nota al pie es un dígito volado que pdftotext entrega
    # como palabra suelta y que queda al frente de la definición
    # («adhikaraṇa 2 ,1 relación; …»). No es texto: es la llamada.
    resto = re.sub(r"^\d{1,2}\s+(?=[a-zñáéíóúü(\"])", "", resto)

    salida = {"pali": lema, "homonimo": homonimo, "es": resto,
              "refs": refs, "pagina": entrada["pagina"]}
    if errata:
        salida["errata"] = errata
    return salida


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip().split("\n\n")[1])
        return 1
    pdf = sys.argv[1]
    if not os.path.exists(pdf):
        print("No está el PDF: " + pdf)
        return 1

    bqs, notas = bloques(pdf)
    entradas = [e for e in (partir(x) for x in trocear(bqs)) if e]

    # el pāḷi de los lemas no debe traer basura de maquetado
    sospechosos = [e["pali"] for e in entradas
                   if len(e["pali"]) > 45 or re.search(r"[.;:\"]", e["pali"])]

    datos = {
        "_nota": "«Glosario de términos gramaticales de la lengua pali», "
                 "material preparado por Bhikkhu Nandisena. El español es SUYO "
                 "y se reproduce literalmente; no se retoca. Extraído de la "
                 "capa de texto del PDF con "
                 "herramientas/extraer_glosario_nandisena.py.",
        "fuente": {
            "titulo": "Glosario de términos gramaticales de la lengua pali",
            "autor": "Bhikkhu Nandisena",
            "editorial": "Dhammodaya Ediciones · Buddhismo Theravada México AR. · "
                         "Instituto de Estudios Buddhistas Hispano (IEBH)",
            "anyo": 2013,
            "revision": "domingo, 7 de abril de 2013",
            "publicacion_iebh": "20130407-BN-T0022",
            "copyright": "© 2013 Dhammodaya Ediciones, Buddhismo Theravada "
                         "México AR., IEBH",
            "licencia": "Puede reproducirse para uso personal; sólo puede "
                        "distribuirse en forma gratuita.",
            "nota": "En su propia lista de referencias, Nandisena declara "
                    "haber consultado los volúmenes de tablas e índices que "
                    "Helmer Smith preparó del Saddanīti y dice que le ha sido "
                    "«muy útil su \"Conspectus Terminorum\", un glosario de "
                    "los términos gramaticales». Las dos fuentes de esta "
                    "página, por tanto, no son independientes: la segunda "
                    "está detrás de la primera.",
        },
        "obras": OBRAS,
        "notas_al_pie": notas,
        "entradas": entradas,
    }

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    json.dump(datos, open(DESTINO, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    from collections import Counter
    repes = [k for k, v in Counter((e["pali"], e.get("homonimo"))
                                   for e in entradas).items() if v > 1]
    cortadas = [e["pali"] for e in entradas
                if e.get("es") and not re.search(r"[.)\]]$", e["es"])]

    con_ref = sum(1 for e in entradas if e["refs"])
    remisiones = sum(1 for e in entradas if e.get("remite_a"))
    print("{0} entradas · {1} con referencia · {2} remisiones → {3}".format(
        len(entradas), con_ref, remisiones, os.path.relpath(DESTINO, RAIZ)))
    if repes:
        print("  {0} lema(s) repetido(s) sin número de homónimo: {1}".format(
            len(repes), ", ".join(sorted(k for k, _ in repes))))
    if cortadas:
        print("  {0} definición(es) que no cierran en punto, por si están "
              "cortadas: {1}".format(len(cortadas), ", ".join(cortadas[:12])))
    if sospechosos:
        print("  {0} lema(s) con pinta de mal cortados, para mirar:".format(
            len(sospechosos)))
        for s in sospechosos[:15]:
            print("    · " + s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
