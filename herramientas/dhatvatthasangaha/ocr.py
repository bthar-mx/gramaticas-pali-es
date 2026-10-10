#!/usr/bin/env python3
"""OCR del Dhātvatthasaṅgaha-nissaya (KBRL 001288), renglón a renglón.

Por qué renglón a renglón (piloto de la sesión 64): con la página entera
(--psm 4/6) Tesseract parte los apilados birmanos en renglones falsos
—subíndices, vocales altas— y saca líneas de basura; el CER filtrado del
mejor modelo era 9,4 % en una página de versos y 25 % en una de nissaya.
Segmentando antes por proyección horizontal y leyendo cada renglón con
--psm 7, el mismo modelo da 4,9 % y 3,0 %. Detalle en
docs/dhatvatthasangaha/piloto-ocr.md.

    python3 herramientas/dhatvatthasangaha/ocr.py leer 20            # imprime los renglones
    python3 herramientas/dhatvatthasangaha/ocr.py leer 20-60 --guardar  # raw/NNN.txt
    python3 herramientas/dhatvatthasangaha/ocr.py medir 20,65        # CER contra piloto/NNN.gt.txt

Imágenes, salida y transcripciones de control viven FUERA del repositorio
(derechos pendientes), en $DHATVATTHA_OCR:
    img/NNN.png          hoja NNN del PDF (pdfimages -png, renombradas)
    raw/NNN.txt          OCR, un renglón por línea: «y0 y1<TAB>texto»
    _work/piloto/NNN.gt.txt   transcripción de control (lectura de Claude)
"""
import argparse, os, statistics, subprocess, sys, unicodedata

B = os.environ.get("DHATVATTHA_OCR") or next(
    (p for p in (os.path.expanduser("~/Tipitaka/nissaya/ocr/dhatvatthasangaha-nissaya"),
                 os.path.expanduser("~/mnt/nissaya/ocr/dhatvatthasangaha-nissaya")) if os.path.isdir(p)),
    os.path.expanduser("~/Tipitaka/nissaya/ocr/dhatvatthasangaha-nissaya"))
TESSDATA = os.environ.get("NISSAYA_TESSDATA") or os.path.join(os.path.dirname(os.path.dirname(B)), "tessdata")
MODELO, ESCALA = "myap", 0.75   # los mejores del piloto; myab queda muy por detrás


def bandas(im):
    """Renglones por proyección horizontal. Una banda baja (subíndice, vocal alta,
    marca) se funde con la vecina más próxima; así no hay renglones de basura."""
    w, h = im.size
    px = im.load()
    prof = [sum(1 for x in range(0, w, 2) if px[x, y] < 128) for y in range(h)]
    b, y = [], 0
    while y < h:
        if prof[y]:
            y0 = y
            while y < h and prof[y]:
                y += 1
            b.append([y0, y])
        y += 1
    alt = statistics.median([b1 - b0 for b0, b1 in b if b1 - b0 > 10] or [40])
    cambio = True
    while cambio:
        cambio = False
        for i, (b0, b1) in enumerate(b):
            if b1 - b0 < 0.55 * alt and len(b) > 1:
                arriba = b0 - b[i - 1][1] if i > 0 else 10 ** 9
                abajo = b[i + 1][0] - b1 if i + 1 < len(b) else 10 ** 9
                j = i - 1 if arriba <= abajo else i + 1
                if min(arriba, abajo) < 0.6 * alt:
                    b[min(i, j)] = [min(b[i][0], b[j][0]), max(b[i][1], b[j][1])]
                    del b[max(i, j)]
                    cambio = True
                    break
    return [x for x in b if x[1] - x[0] >= 0.3 * alt]


def leer(hoja, modelo=MODELO, escala=ESCALA):
    from PIL import Image
    im = Image.open(os.path.join(B, "img", "%03d.png" % hoja)).convert("L")
    out = []
    for k, (y0, y1) in enumerate(bandas(im)):
        c = im.crop((0, max(0, y0 - 12), im.size[0], min(im.size[1], y1 + 12)))
        if escala != 1:
            c = c.resize((int(c.size[0] * escala), int(c.size[1] * escala)), Image.LANCZOS)
        f = "/tmp/dvs-%03d-%d.png" % (hoja, k)
        c.save(f)
        r = subprocess.run(["tesseract", f, "stdout", "--tessdata-dir", TESSDATA, "-l", modelo, "--psm", "7"],
                           capture_output=True, text=True, env=dict(os.environ, OMP_THREAD_LIMIT="1"))
        os.remove(f)
        if r.returncode:
            sys.exit("tesseract falló en la hoja %d: %s" % (hoja, r.stderr[:300]))
        out.append((y0, y1, r.stdout.strip()))
    return out


def norm(s):
    s = unicodedata.normalize("NFC", s)
    for a, z in (("'", "’"), ("‘", "’"), ("“", '"'), ("”", '"'), ("|", "]"), ("---", "-"), ("--", "-")):
        s = s.replace(a, z)
    return "".join(c for c in s if not c.isspace())


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
        prev = cur
    return prev[-1]


def hojas(spec):
    r = []
    for parte in spec.split(","):
        a, _, z = parte.partition("-")
        r += range(int(a), int(z or a) + 1)
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("orden", choices=["leer", "medir"])
    ap.add_argument("hojas")
    ap.add_argument("--guardar", action="store_true")
    ap.add_argument("--modelo", default=MODELO)
    ap.add_argument("--escala", type=float, default=ESCALA)
    a = ap.parse_args()
    for h in hojas(a.hojas):
        sal = os.path.join(B, "raw", "%03d.txt" % h)
        if a.orden == "leer" and a.guardar and os.path.exists(sal):
            continue
        L = leer(h, a.modelo, a.escala)
        if a.orden == "leer":
            txt = "".join("%d %d\t%s\n" % x for x in L)
            if a.guardar:
                os.makedirs(os.path.dirname(sal), exist_ok=True)
                open(sal, "w", encoding="utf-8").write(txt)
                print("hoja", h, len(L), "renglones", flush=True)
            else:
                sys.stdout.write(txt)
        else:
            gt = norm(open(os.path.join(B, "_work", "piloto", "%03d.gt.txt" % h), encoding="utf-8").read())
            o = norm("".join(t for _, _, t in L))
            print("hoja %d  %s ×%s  CER %.1f %%  (%d caracteres)" % (h, a.modelo, a.escala, 100 * lev(o, gt) / len(gt), len(gt)))


if __name__ == "__main__":
    main()
