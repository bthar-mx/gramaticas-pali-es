#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Busca un término pāḷi en las tres obras que el repositorio tiene por sutta y
devuelve los aforismos donde aparece, para ponerlos de referencia en el
glosario normativo.

    python3 herramientas/referenciar_terminos.py saddūpapada napuṃsaka …

Obras y de dónde salen:

  Kacc.   los ocho capítulos de Kaccāyana (trad. Nandisena): 1-3 en
          kaccayana/, 4 en docs/borradores/, 5-8 en docs/. Cabecera de sutta
          «**NNN. RRR. …**»: el primer número es el de Kaccāyana.
  Rū.     la Rūpasiddhi, capítulos 5-7 (docs/). Cabecera «**NNN. …**».
  Nyāsa   el texto pāḷi completo (docs/fuentes/nyasa/), cabecera «( NNN )».

Se busca el TEMA (sin desinencia) como subcadena, sin distinguir mayúsculas,
en todo el bloque del sutta —aforismo, vutti, ejemplos y traducción—; los
temas de menos de cinco letras y las designaciones (gha, jha, la, ga) sólo se
buscan como palabra entera en la línea del aforismo, porque sueltos casan
con cualquier cosa. El OCR del Nyāsa pega palabras, y por eso la subcadena
es lo único que allí funciona. Nada se inventa: lo que no se encuentra
queda sin referencia y se dice.
"""
import glob, os, re, sys, unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KACC = [
    ("kaccayana/01-sandhi-kappa.md"),
    ("kaccayana/02-nama-kappa.md"),
    ("kaccayana/03-karaka-kappa.md"),
    ("docs/borradores/capitulo-04-samasa-kappa-completo.md"),
    ("docs/5 - Taddhita-Kaccāyana.md"),
    ("docs/6 - Ākhyāta-Kaccāyana.md"),
    ("docs/7- Kibbidhāna-Kappa-Kaccāyana.md"),
    ("docs/8 - Uṇādi-Kappa-Kaccāyana.md"),
]
RU = [
    ("docs/5. Taddhita-Rūpasiddhi.md"),
    ("docs/6. Ākhyāta-Rūpasiddhi.md"),
    ("docs/7- Kibbidhāna-Rūpasiddhi.md"),
]
NYASA = sorted(glob.glob(os.path.join(RAIZ, "docs", "fuentes", "nyasa", "Nyasa-0[1-8]-*.md")))

RE_KACC = re.compile(r"^\s*\**(\d{1,3})\\?\.\s*\d{1,3}\\?\.\s*\**\s*\S")
RE_RU = re.compile(r"^\s*\**(\d{3})\**\\?\.\s*\**\s*\S")
RE_NYASA = re.compile(r"^\s*\(\s*\**(\d{1,3})\**\s*\)")

# Kaccāyana: el número de sutta crece a lo largo de la obra; una cabecera
# cuyo número no sea el siguiente (o cercano) al anterior es una cita, no
# un sutta nuevo.
RE_NOTA = re.compile(r"^\[\^(\d+)\]:")

def _capitulo(ruta):
    """El nombre del capítulo a partir del archivo: «Ākhyāta», «Kibbidhāna»."""
    m = re.search(r"(Sandhi|Nāma|Kāraka|Samāsa|Taddhita|Ākhyāta|Kibbidhāna|Uṇādi|sandhi|nama|karaka|samasa|taddhita|akhyata|kibbidhana|unadi)", os.path.basename(ruta))
    return m.group(1).capitalize() if m else os.path.basename(ruta)


def _bloques(ruta, re_cab, monotono=True):
    """Parte el archivo en suttas: {número: texto}. Lo que va ANTES del primer
    sutta (la introducción de la Rūpasiddhi, el preámbulo del capítulo) se
    guarda bajo la clave «intro:<capítulo>». Las notas al pie, que la
    edición pone al final del archivo, se devuelven al sutta que las cita."""
    bloques, actual, num, ultimo, notas = {}, [], "intro:" + _capitulo(ruta), 0, {}
    for linea in open(ruta, encoding="utf-8"):
        mn = RE_NOTA.match(linea)
        if mn:
            notas[mn.group(1)] = linea
            continue
        m = re_cab.match(linea)
        if m:
            n = int(m.group(1))
            if not monotono or (ultimo < n <= ultimo + 12) or ultimo == 0:
                bloques.setdefault(num, []).extend(actual)
                num, actual, ultimo = n, [], n
        actual.append(linea)
    bloques.setdefault(num, []).extend(actual)
    salida = {k: "".join(v) for k, v in bloques.items()}
    for k, nota in notas.items():
        marca = "[^" + k + "]"
        for n, t in salida.items():
            if marca in t:
                salida[n] += nota
                break
    return salida


def _nfc(s):
    """Minúsculas, NFC y sin los guiones ni apóstrofos con que la edición
    parte los compuestos («pura-saddūpapade», «dhātv’-anta»)."""
    return re.sub(r"[-‑’'`]", "", unicodedata.normalize("NFC", s).lower())


_CORPUS = None
def corpus():
    global _CORPUS
    if _CORPUS is None:
        _CORPUS = {"Kacc.": {}, "Rū.": {}, "Nyāsa": {}}
        for r in KACC:
            _CORPUS["Kacc."].update(_bloques(os.path.join(RAIZ, r), RE_KACC))
        for r in RU:
            _CORPUS["Rū."].update(_bloques(os.path.join(RAIZ, r), RE_RU))
        for r in NYASA:
            _CORPUS["Nyāsa"].update(_bloques(r, RE_NYASA))
        # De cada sutta se guardan el aforismo (primera línea, con los
        # guiones vueltos espacios: «jha-lā» son dos designaciones) y el
        # bloque entero sin guiones, para la subcadena.
        for obra in _CORPUS:
            _CORPUS[obra] = {n: {"cab": re.sub(r"[-‑’'`]", " ", unicodedata.normalize("NFC", t.split("\n", 1)[0]).lower()),
                                 "txt": _nfc(t)}
                             for n, t in _CORPUS[obra].items()}
    return _CORPUS


def tema(termino):
    """Lo que se busca: sin «(saññā)», sin paréntesis, sin guion inicial;
    de un compuesto con guiones (tija-gupa-kita-māna) se toma entero sin
    los guiones, y si no casa, su primer miembro."""
    t = termino.replace(" (saññā)", "").strip()
    t = re.sub(r"\s*\(.*\)$", "", t).strip().lstrip("-")
    return _nfc(t)


VOCAL = "aāiīuūeo"
LETRA = "a-zāīūṅñṭḍṇḷṃ"


def raiz(cand):
    """El tema sin su vocal final, que es la que flexiona: «aṅgavikāra»
    casa así con «aṅgavikāro», «suttavibhāga» con «suttavibhāgena»."""
    return cand[:-1] if len(cand) > 4 and cand[-1] in VOCAL else cand


def buscar(termino, tipo="término"):
    """Devuelve {obra: [números de sutta]} donde aparece el tema."""
    t = tema(termino)
    corto = len(t.replace("-", "")) < 5 or tipo == "designación"
    candidatos = [t.replace("-", "")]
    if "-" in t:
        candidatos.append(t.split("-")[0])
    hallado = {}
    for obra, bloques in corpus().items():
        for cand in candidatos:
            nums = []
            if corto:
                # palabra entera en la línea del aforismo, con la vocal final
                # libre: «gha» casa con «gho» (§58 «Ā gho»), «la» con «lā»
                # libre: «gha» casa con «gho» (§60 «Ā gho»), «la» con «lā»,
                # y también con el compuesto «gasañño» (§57).
                base = re.escape(cand[:-1] if cand[-1] in VOCAL else cand)
                re_cab = re.compile("(?<![{0}])".format(LETRA) + base
                                    + "(?:[{0}]?(?![{1}])|asañ)".format(VOCAL, LETRA))
            for n, bloque in sorted(bloques.items(), key=lambda kv: (isinstance(kv[0], str), kv[0] if isinstance(kv[0], int) else 0, str(kv[0]))):
                if corto:
                    if re_cab.search(bloque["cab"]):
                        nums.append(n)
                elif raiz(cand) in bloque["txt"]:
                    nums.append(n)
            if nums:
                hallado[obra] = nums
                break
    return hallado


def formatear(hallado, maximo=6):
    """«Kacc. §525, §526 · Nyāsa §525, §526, §540 (y 6 más)»."""
    partes = []
    for obra in ("Kacc.", "Rū.", "Nyāsa"):
        nums = hallado.get(obra)
        if not nums:
            continue
        intros = [n.split(":", 1)[1] + " (introducción)" for n in nums if isinstance(n, str)]
        nums = [n for n in nums if isinstance(n, int)]
        lista = ", ".join("§{0}".format(n) for n in nums[:maximo])
        if len(nums) > maximo:
            lista += " (y {0} más)".format(len(nums) - maximo)
        lista = ", ".join([x for x in [lista] + intros if x])
        partes.append("{0} {1}".format(obra, lista))
    return " · ".join(partes)


if __name__ == "__main__":
    for term in sys.argv[1:]:
        h = buscar(term)
        print("{0}: {1}".format(term, formatear(h) or "— no se encuentra —"))
