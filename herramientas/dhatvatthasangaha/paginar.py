#!/usr/bin/env python3
"""Mapa hoja del PDF -> página impresa del Dhātvatthasaṅgaha-nissaya (KBRL 001288).

Lee el titulillo de cada hoja (franja superior, 7,5 % de la altura) con el
modelo birmano `myab`, saca los números birmanos que abren o cierran una línea
y vota el desfase hoja − página. El mapa se arma con los tramos de desfase
constante; una hoja sin lectura recibe el desfase del tramo que la rodea SÓLO
si las dos lecturas vecinas dan el mismo desfase. Donde cambia el desfase hay
un hueco o una hoja de más, y eso se dice en `huecos`, no se tapa.

    python3 herramientas/dhatvatthasangaha/paginar.py           # OCR (con caché) + mapa
    python3 herramientas/dhatvatthasangaha/paginar.py --solo-mapa

Imágenes y caché fuera del repositorio, en $DHATVATTHA_OCR
(por defecto ~/Tipitaka/nissaya/ocr/dhatvatthasangaha-nissaya):
img/NNN.png (NNN = hoja del PDF) y _work/heads/NNN.txt.
Salida: recursos/raices/dhatvatthasangaha-nissaya.paginas.json
"""
import json, os, re, subprocess, sys
from collections import Counter

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
B = os.environ.get("DHATVATTHA_OCR") or next(
    (p for p in (os.path.expanduser("~/Tipitaka/nissaya/ocr/dhatvatthasangaha-nissaya"),
                 os.path.expanduser("~/mnt/nissaya/ocr/dhatvatthasangaha-nissaya")) if os.path.isdir(p)),
    os.path.expanduser("~/Tipitaka/nissaya/ocr/dhatvatthasangaha-nissaya"))
TESSDATA = os.environ.get("NISSAYA_TESSDATA") or os.path.join(os.path.dirname(os.path.dirname(B)), "tessdata")
HOJAS = 567
SALIDA = os.path.join(RAIZ, "recursos", "raices", "dhatvatthasangaha-nissaya.paginas.json")
DIG = "၀၁၂၃၄၅၆၇၈၉"

# Lo que no sale del titulillo y se ha visto en la imagen (sesión 64).
PARTES = [  # (desde hoja, hasta hoja, parte)
    (1, 1, "cubierta"), (2, 15, "preliminares"), (16, 60, "pali"),
    (61, 407, "nissaya"), (408, 415, "apendices"), (416, 564, "indice"),
    (565, 565, "colofon"), (566, 567, "cubierta"),
]


# Vistas en la imagen, sesión 64: la hoja 16 abre el texto pāḷi (p. 1 según la
# mātikā; la 17 lleva «၂»); la hoja 61 es la portadilla del nissaya, sin
# número (la mātikā, hoja 11, da la p. 47 como comienzo de la parte); la 62
# lleva «၄၈» y la 565, el colofón, «၅၅၃», que el OCR no lee.
VISTAS = {16: "1", 61: "47", 62: "48", 565: "553"}


def ocr(p):
    out = os.path.join(B, "_work", "heads", "%03d.txt" % p)
    if os.path.exists(out):
        return open(out, encoding="utf-8").read()
    from PIL import Image
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im = Image.open(os.path.join(B, "img", "%03d.png" % p)).convert("L")
    w, h = im.size
    tmp = "/tmp/dvs-head-%03d.png" % p
    im.crop((0, 0, w, int(h * 0.075))).save(tmp)
    r = subprocess.run(["tesseract", tmp, "stdout", "--tessdata-dir", TESSDATA, "-l", "myab", "--psm", "6"],
                       capture_output=True, text=True, env=dict(os.environ, OMP_THREAD_LIMIT="1"))
    os.remove(tmp)
    if r.returncode:
        sys.exit("tesseract falló en la hoja %d: %s" % (p, r.stderr[:300]))
    open(out, "w", encoding="utf-8").write(r.stdout)
    return r.stdout


def numeros(txt):
    c = []
    for linea in txt.splitlines():
        t = linea.split()
        for tok in (t[:1] + t[-1:]) if t else []:
            m = re.fullmatch(r"[\(\[]?([၀-၉]{1,3})[\)\]]?", tok)
            if m:
                c.append(int("".join(str(DIG.index(ch)) for ch in m.group(1))))
    return c


def parte(p):
    return next(x for a, b, x in PARTES if a <= p <= b)


def main():
    leidos = {}
    for p in range(1, HOJAS + 1):
        if parte(p) in ("cubierta", "preliminares"):
            continue
        votos = [p - n for n in numeros(ocr(p)) if 0 <= p - n <= 30]
        if votos:
            leidos[p] = (Counter(votos).most_common(1)[0][0], p - (Counter(votos).most_common(1)[0][0]))
    # Tramos: una lectura aislada que contradice a sus dos vecinas es mala lectura.
    hs = sorted(leidos)
    buenos = {}
    for i, p in enumerate(hs):
        d = leidos[p][0]
        vec = [leidos[hs[j]][0] for j in (i - 1, i + 1) if 0 <= j < len(hs)]
        if d in vec or not vec:
            buenos[p] = d
    paginas, huecos, malas = [], [], sorted(set(leidos) - set(buenos))
    hb = sorted(buenos)
    for p in range(1, HOJAS + 1):
        e = {"leafNum": p - 1, "hoja": p, "parte": parte(p), "pageNumber": "", "fuente": "sin numerar"}
        if p in VISTAS:
            e.update(pageNumber=VISTAS[p], fuente="vista")
        elif p in buenos:
            e.update(pageNumber=str(p - buenos[p]), fuente="titulillo")
        elif e["parte"] not in ("cubierta", "preliminares"):
            antes = [q for q in hb if q < p]
            despues = [q for q in hb if q > p]
            if antes and despues and buenos[antes[-1]] == buenos[despues[0]]:
                e.update(pageNumber=str(p - buenos[antes[-1]]), fuente="interpolada")
            elif antes and not despues:
                e.update(pageNumber=str(p - buenos[antes[-1]]), fuente="extrapolada")
        paginas.append(e)
    num = [(e["hoja"], int(e["pageNumber"])) for e in paginas if e["pageNumber"]]
    for (a, pa), (b, pb) in zip(num, num[1:]):
        if pb - pa != b - a:
            huecos.append({"entre_hojas": [a, b], "entre_paginas": [pa, pb],
                           "faltan": list(range(pa + 1, pb)) if b == a + 1 else "revisar",
                           "nota": ""})
    datos = {
        "obra": "Dhātvatthasaṅgahapāṭh-nissaya (ဓာတွတ္ထသင်္ဂဟပါဌ်နိဿယ), Mahāvisuddhārāma Sayadaw",
        "escaneo": "KBRL 001288, md5 94ac160678dcd90be6fcb93b75895ca4, 567 hojas",
        "nota": ("leafNum empieza en 0, como en los .paginas.json del Saddanīti; hoja = leafNum + 1 "
                 "= la página del visor y de pdftoppm -f. fuente: titulillo (leído y coherente con "
                 "sus vecinas), interpolada (sin lectura, entre dos lecturas del mismo desfase), "
                 "extrapolada (tras la última lectura), sin numerar."),
        "generado_por": "herramientas/dhatvatthasangaha/paginar.py",
        "huecos": huecos,
        "lecturas_descartadas": [{"hoja": p, "leido": leidos[p][1]} for p in malas],
        "pages": paginas,
    }
    if os.path.exists(SALIDA):  # conservar las notas escritas a mano en los huecos
        viejo = json.load(open(SALIDA, encoding="utf-8"))
        notas = {tuple(h["entre_hojas"]): h.get("nota", "") for h in viejo.get("huecos", [])}
        for h in huecos:
            h["nota"] = notas.get(tuple(h["entre_hojas"]), "")
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)
        f.write("\n")
    cuenta = Counter(e["fuente"] for e in paginas)
    print("hojas:", HOJAS, dict(cuenta))
    for h in huecos:
        print("hueco: hojas %s -> pp. %s; faltan %s" % (h["entre_hojas"], h["entre_paginas"], h["faltan"]))
    print("lecturas descartadas:", [(d["hoja"], d["leido"]) for d in datos["lecturas_descartadas"]])
    print("->", os.path.relpath(SALIDA, RAIZ))


if __name__ == "__main__":
    main()
