#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrae el Dhātupāṭha del transcrito de A. Ruiz-Falqués.

    python3 herramientas/extraer_dhatupatha.py ruta/al/dhatupatha.pdf

Escribe recursos/raices/dhatupatha.json.

La fuente es «The Pāli Dhātupāṭha and the Dhātumañjūsā», edición de Dines
Andersen y Helmer Smith (Copenhague, 1921), transcrita por A. Ruiz-Falqués
(Taunggyi, 2019). Este guion lee sólo el Dhātupāṭha: las 639 raíces
numeradas, con su significado, el gaṇa y el signo de conjugación de cada
sección, y las notas críticas al pie, que registran las lecturas de los
manuscritos.

El PDF sí tiene capa de texto —lo compuso Word—, de modo que aquí no hace
falta reconstruir nada; lo que cuesta es la estructura, porque el texto va
en prosa corrida y una entrada puede partirse entre dos páginas.

Requiere pymupdf.
"""
import json
import os
import re
import sys

try:
    import pymupdf
except ImportError:
    sys.exit("Hace falta pymupdf:  pip3 install pymupdf")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, "recursos", "raices", "dhatupatha.json")

# Los nueve grupos de esta edición no son los ocho del Saddanīti: Andersen y
# Smith siguen la ordenación de los Dhātupāṭha sánscritos, y parten el
# primero en «I, a» y «I, b» según lleven o no signo de conjugación. El
# nombre de cada uno lo da la propia edición en su fórmula de cierre.
GRUPOS = {
    "I": "bhuvādayo", "II": "rudhādayo", "III": "divādayo",
    "IV": "tudādayo", "V": "jyādayo", "VI": "kyādayo",
    "VII": "svādayo", "VIII": "tanādayo", "IX": "curādayo",
}

MARCA = '\x01'

GANA  = re.compile(r'^(IX|VIII|VII|VI|IV|V|III|II|I)\s*,?\s*([a-d])?\.\s*$')
LETRA = re.compile(r'^[A-ZĀĪŪṂṄÑṬḌṆḶŚṢ]{1,3}\s*$')
# Las fórmulas de cierre de cada gaṇa. Han de ir ancladas y ser precisas: un
# «.*samatt» suelto casaba con «kammasamattiyaṃ» y se tragaba la línea de las
# entradas 608-609.
CIERRE = re.compile(r'^(?:[A-ZĀ]?[a-zāīūṃṅñṭḍṇḷ]+ādayo\b.*'
                    r'|a anto uccāraṇattho.*'
                    r'|\*?\s*\[?etesaṃ.*'
                    r'|.*dhātupāṭhaṃ samattaṃ.*)$')

def lineas(doc, pno):
    """[(texto, es_nota)] de la página, con las llamadas marcadas."""
    out = []
    for b in doc[pno].get_text('dict')['blocks']:
        for l in b.get('lines', []):
            t, chico, grande = '', 0, 0
            for s in l['spans']:
                txt, sz = s['text'], round(s['size'], 1)
                if sz <= 5.0 and txt.strip().isdigit():
                    t += MARCA + txt.strip()          # llamada de nota
                    continue
                if sz <= 6.6:
                    chico += len(txt.strip())
                else:
                    grande += len(txt.strip())
                t += txt
            # Una línea es nota al pie cuando está casi entera en cuerpo
            # pequeño. Mirar un solo tramo pequeño no vale: los números de
            # entrada con letra —«547a.», «609a.»— llevan la letra en un
            # cuerpo menor, y con la regla ingenua toda la línea, con sus
            # cuatro o cinco raíces, se tomaba por una nota y se perdía.
            if t.strip():
                out.append((t, chico > grande))
    return out

def leer(doc):
    """(cuerpo, notas): el cuerpo como [(pagina, linea)] seguido, y las notas."""
    cuerpo, notas, dentro = [], {}, False
    for pno in range(len(doc)):
        ls = lineas(doc, pno)
        entera = ' '.join(t for t, _ in ls)
        if 'Namo tassa Bhagavato' in entera:
            dentro = True
        if not dentro:
            continue
        for t, esNota in ls:
            t = t.strip()
            if not t:
                continue
            if esNota:
                m = re.match(r'^' + MARCA + r'?(\d{1,3})\s*(.*)$', t)
                if m:
                    notas[(pno, int(m.group(1)))] = m.group(2).strip()
                continue
            if t.startswith('[') or 'Namo tassa' in t or 'sammāsambuddhassa' in t \
               or t.startswith('_') or t.strip('_ ') == '':
                continue
            cuerpo.append((pno, t))
        if 'dhātupāṭhaṃ samattaṃ' in entera:
            break
    return cuerpo, notas

def cortar(texto, paginas, notas, gana, signo, letra, fuera):
    texto = re.sub(r'\s+', ' ', texto).strip()
    if not texto:
        return

    # Las llamadas de nota se quitan ANTES de cortar por entradas: una llamada
    # seguida de coma —«lakkhaṇe¹, 4. saṃkha»— es indistinguible de un número
    # de entrada y se llevaba por delante toda la numeración.
    llamadas, trozos, i = [], [], 0
    for m in re.finditer(MARCA + r'(\d{1,3})', texto):
        trozos.append(texto[i:m.start()])
        llamadas.append((sum(len(x) for x in trozos), int(m.group(1))))
        i = m.end()
    trozos.append(texto[i:])
    texto = ''.join(trozos)

    # El «(?<!\d)» es imprescindible: sin él «11.» casa también empezando por
    # el segundo 1, y la entrada saldría numerada 1.
    # El sufijo de letra —«547a.», «609a.»— numera entradas suplementarias
    # que la edición añade sin correr la numeración.
    CAB = re.compile(r'(?<!\d)(\d{1,3})([a-z])?(?:\s*[—–-]\s*(\d{1,3}))?\s*[.,]\s*')
    hits = list(CAB.finditer(texto))
    for j, m in enumerate(hits):
        n0 = int(m.group(1))
        sufijo = m.group(2) or ''
        n1 = int(m.group(3) or m.group(1))
        if n1 < n0 or n1 - n0 > 12:
            n1 = n0
        ini = m.end()
        fin = hits[j + 1].start() if j + 1 < len(hits) else len(texto)
        resto = texto[ini:fin].strip().rstrip(',;.').strip()
        refs = [n for pos, n in llamadas if ini <= pos <= fin]
        texto_notas = []
        for x in refs:
            for pg in paginas:
                if (pg, x) in notas:
                    texto_notas.append(notas[(pg, x)])
                    break
        toks = [t for t in resto.split() if t.strip(',;.')]
        k = n1 - n0 + 1
        # Sin rango explícito, la propia numeración dice cuántas raíces van
        # en la entrada: si la siguiente es la 354 y ésta la 352, aquí hay
        # dos. Sólo se acepta si el reparto cuadra —tantas raíces como
        # números, y algo que sobre para el significado—; si no, se deja en
        # una y se marca la duda.
        inferido = False
        if k == 1 and not sufijo and j + 1 < len(hits):
            sig = int(hits[j + 1].group(1))
            hueco = sig - n0
            if 1 < hueco <= 12 and len(toks) >= hueco + 1:
                k, n1, inferido = hueco, n0 + hueco - 1, True
        # Un rango puede llevar un significado por raíz, separados por coma:
        # «316—317. kāsa dittiyaṃ, bhāsa vacane ca». Y la segunda mitad puede
        # ser sólo la raíz más «ca» —«562—563. veṭha veṭhane, guṇṭha ca»—, y
        # entonces comparte el significado de la primera.
        pares = None
        if k > 1 and ',' in resto:
            trozos = [t.strip(' ,;.') for t in resto.split(',')]
            trozos = [t for t in trozos if t]
            if len(trozos) == k:
                pares, previa = [], ''
                for t in trozos:
                    tt = [w for w in t.split() if w.strip(',;.')]
                    if not tt:
                        pares = None
                        break
                    r = tt[0]
                    g = ' '.join(w for w in tt[1:] if w != 'ca').strip(' ,;.')
                    if not g:
                        g = previa
                    previa = g
                    pares.append((r, g))
                if pares and not all(g for _, g in pares):
                    pares = None

        dudoso = pares is None and len(toks) < k + 1
        for idx in range(k):
            if pares:
                raiz, glosa = pares[idx]
            elif dudoso:
                # El original no deja separar raíz y significado (p. ej. la
                # entrada 169, «vadhahiṃsāyaṃ», impresa sin espacio). No se
                # inventa el corte: se guarda tal cual y se marca.
                raiz, glosa = (toks[idx] if idx < len(toks) else ''), ''
            else:
                raiz, glosa = toks[idx], ' '.join(toks[k:]).strip(' ,;.')
            fuera.append({'n': n0 + idx, 'sufijo': sufijo,
                          'raiz': raiz.strip(',;.'), 'glosa': glosa,
                          'gana': gana, 'signo': signo, 'letra': letra,
                          'paginas': sorted(set(paginas)),
                          'notas': texto_notas,
                          'dudoso': dudoso, 'inferido': inferido,
                          'pegada': False})

def separar_pegadas(fuera):
    """Rescata las entradas que el original imprime sin espacio.

    La 169 sale «vadhahiṃsāyaṃ», raíz y significado pegados. No se parte a
    ojo: se prueba cada corte y sólo se acepta el que deja un significado ya
    atestiguado en otra entrada del propio Dhātupāṭha y que, recompuesto,
    reproduce exactamente la cadena impresa.
    """
    glosas = {x["glosa"] for x in fuera if x["glosa"]}
    for x in fuera:
        if not x["dudoso"] or not x["raiz"]:
            continue
        w = x["raiz"]
        cortes = [(w[:i], w[i:]) for i in range(2, len(w) - 1)
                  if w[i:] in glosas and w[:i] + w[i:] == w]
        if len(cortes) == 1:
            x["raiz"], x["glosa"] = cortes[0]
            x["dudoso"] = False
            x["pegada"] = True
    return fuera


def parse():
    doc = pymupdf.open(PDF)
    cuerpo, notas = leer(doc)
    fuera = []
    gana = signo = letra = None
    buf, pgs = [], []
    def flush():
        nonlocal buf, pgs
        if buf:
            cortar(' '.join(buf), pgs, notas, gana, signo, letra, fuera)
        buf, pgs = [], []
    for pno, t in cuerpo:
        g = GANA.match(t)
        if g:
            flush(); gana, signo, letra = g.group(1), g.group(2), None; continue
        if LETRA.match(t.replace(MARCA, '')):
            flush(); letra = t.strip(); continue
        if CIERRE.match(t) and not re.match(r'^\d', t):
            flush(); continue
        buf.append(t); pgs.append(pno)
    flush()
    return separar_pegadas(fuera)

CABECERA = {
    "_nota": "El Dhātupāṭha pāḷi, con sus 639 raíces numeradas. Transcrito de "
             "«The Pāli Dhātupāṭha and the Dhātumañjūsā», ed. Dines Andersen y "
             "Helmer Smith, Copenhague 1921, en la transcripción de A. "
             "Ruiz-Falqués (Taunggyi, 2019). El texto es literal. Las notas "
             "son las notas críticas de la edición, que dan las lecturas de "
             "los manuscritos. «dudoso» marca la entrada que el original no "
             "deja separar en raíz y significado; «inferido», aquella cuyo "
             "número de raíces no viene de un rango explícito sino de la "
             "propia numeración de la edición, y sólo cuando el reparto "
             "cuadra exactamente.",
    "fuente": {
        "titulo": "The Pāli Dhātupāṭha and the Dhātumañjūsā",
        "editores": "Dines Andersen y Helmer Smith",
        "lugar": "Copenhague",
        "anyo": 1921,
        "transcripcion": "A. Ruiz-Falqués, Taunggyi, 2019",
    },
    "grupos": GRUPOS,
}


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: python3 herramientas/extraer_dhatupatha.py ruta/al/dhatupatha.pdf")
    global PDF
    PDF = sys.argv[1]
    e = parse()

    nums = sorted({x['n'] for x in e})
    faltan = sorted(set(range(1, max(nums) + 1)) - set(nums))
    if faltan:
        print("  aviso — números sin entrada: {0}".format(faltan))

    datos = dict(CABECERA)
    datos["entradas"] = e
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    json.dump(datos, open(DESTINO, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    sufijos = sum(1 for x in e if x['sufijo'])
    print("{0} entradas · {1} numeradas 1-{2} · {3} suplementarias · "
          "{4} con nota crítica → {5}".format(
              len(e), len(nums), max(nums), sufijos,
              sum(1 for x in e if x['notas']),
              os.path.relpath(DESTINO, RAIZ)))
    dud = [x['n'] for x in e if x['dudoso']]
    if dud:
        print("  sin separar raíz y significado en el original: {0}".format(dud))
    inf = [x['n'] for x in e if x['inferido']]
    if inf:
        print("  reparto deducido de la numeración: {0}".format(inf))
    return 0


if __name__ == '__main__':
    sys.exit(main())
