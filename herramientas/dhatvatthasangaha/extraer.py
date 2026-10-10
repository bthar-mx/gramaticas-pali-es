#!/usr/bin/env python3
"""Versos y entradas del Dhātvatthasaṅgaha-nissaya, a partir del OCR renglón a renglón.

    python3 herramientas/dhatvatthasangaha/extraer.py

Lee raw/NNN.txt (ocr.py) y las imágenes para la sangría de cada renglón.
Escribe, FUERA del sitio y del repositorio (decisión del IEBH, 2026-10-10:
el texto del nissaya no se publica):

    docs/fuentes/dhatvatthasangaha/datos.json    versos y entradas completos
    docs/fuentes/dhatvatthasangaha/revision.md   lo que no pasa la comprobación

La comprobación es la de los tres testigos. Cada raíz sale hasta tres veces:
en el verso del texto pāḷi (pp. 1-45), en el mismo verso repetido en el
nissaya, y al margen de su entrada. Se compara sin apóstrofo de elisión
—el OCR lo pierde siempre— y sin espacios.
"""
import json, os, re, sys, unicodedata
from PIL import Image, ImageOps

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "herramientas", "nyasappadipika"))
from my2rom import translit_word, fix_ocr  # noqa: E402

B = os.environ.get("DHATVATTHA_OCR") or next(
    (p for p in (os.path.expanduser("~/Tipitaka/nissaya/ocr/dhatvatthasangaha-nissaya"),
                 os.path.expanduser("~/mnt/nissaya/ocr/dhatvatthasangaha-nissaya")) if os.path.isdir(p)))
SALIDA = os.path.join(RAIZ, "docs", "fuentes", "dhatvatthasangaha")
DIG = "၀၁၂၃၄၅၆၇၈၉"
PALI, NISSAYA = range(16, 61), range(61, 408)
NUM = re.compile(r"^\s*\S{0,2}?([၀-၉]{1,3})\s*[။၊]")


def paginas():
    d = json.load(open(os.path.join(RAIZ, "recursos", "raices", "dhatvatthasangaha-nissaya.paginas.json"), encoding="utf-8"))
    return {e["hoja"]: e["pageNumber"] for e in d["pages"]}


def renglones(h):
    im = ImageOps.invert(Image.open(os.path.join(B, "img", "%03d.png" % h)).convert("L"))
    w = im.size[0]
    r = []
    for linea in open(os.path.join(B, "raw", "%03d.txt" % h), encoding="utf-8"):
        a, _, t = linea.rstrip("\n").partition("\t")
        y0, y1 = map(int, a.split())
        bb = im.crop((0, y0, w, y1)).point(lambda v: 255 if v > 128 else 0).getbbox()
        r.append({"y0": y0, "y1": y1, "x0": bb[0] if bb else 0, "x1": bb[2] if bb else 0,
                  "t": unicodedata.normalize("NFC", fix_ocr(t)).strip()})
    return w, r


def num(s):
    return int("".join(str(DIG.index(c)) for c in s))


def llano(s):
    """Para comparar testigos: sin apóstrofos, espacios, puntuación ni guiones."""
    return re.sub(r"[\s’'‘\-–—၊။,\.\[\]\|\(\)“”\"]", "", s)


def es_titulillo(i, l, w):
    return i == 0 and (re.search(r"[၀-၉]{1,3}\s*$", l["t"]) or re.match(r"^[၀-၉]{1,3}\s", l["t"])
                       or "ဓာတွတ္ထ" in l["t"])


def cuenta_final(t):
    m = re.search(r"([၀-၉])\s*။?\s*$", t)
    return num(m.group(1)) if m else None


# ------------------------------------------------------------------ texto pāḷi
RESUMEN = re.compile(r"^\s*(ဣတိ|ဣမေ|ဣစ္စေ)")


def versos_pali(pag):
    """Un verso = dos pādas; el primero lleva el número y menos sangría. Los
    renglones «ဣတိ … ဓာတဝေါ … N ။» son el recuento de cada letra y van aparte."""
    versos, actual = [], None
    for h in PALI:
        w, L = renglones(h)
        cuerpo = [l for i, l in enumerate(L) if not es_titulillo(i, l, w)]
        vlike = [l for l in cuerpo if l["x0"] <= 0.35 * w and l["x1"] - l["x0"] >= 0.3 * w]
        if not vlike:
            continue
        x_ini = min(l["x0"] for l in vlike)
        for l in cuerpo:
            t = l["t"]
            if l["x0"] > 0.35 * w or l["x1"] - l["x0"] < 0.3 * w:   # epígrafe centrado: «[က]», título
                continue
            if actual is not None and (RESUMEN.match(t) or (not NUM.match(t) and (
                    re.search(r"ကဏ္ဍော\s*\S*မော", t) or "ဓာတဝေါ။" in t.replace(" ", "")))):
                actual.setdefault("resumen", []).append(t)
                continue
            m = NUM.match(t)
            if actual is None and not m:       # «နမော တဿ …»: antes del verso ၁
                continue
            primero = bool(m) or (l["x0"] < x_ini + 70 and (actual is None or len(actual["lineas"]) >= 2))
            if primero:
                actual = {"leido": num(m.group(1)) if m else None, "lineas": [t],
                          "hoja": h, "pagina": pag.get(h, "")}
                versos.append(actual)
            elif actual is not None:
                actual["lineas"].append(t)
    numerar(versos)
    for v in versos:
        v["cuenta"] = cuenta_final(v["lineas"][-1])
    return versos


def numerar(versos):
    """El número leído manda si sigue la serie (o la salta por poco); si no, el
    correlativo. Los saltos quedan anotados para revisar."""
    prev = 0
    for v in versos:
        le = v["leido"]
        if le is not None and prev < le <= prev + 3:
            if le != prev + 1:
                v["salto"] = le - prev - 1
            v["n"] = le
        else:
            v["n"] = prev + 1
            v["leido_mal"] = le is not None
        prev = v["n"]


# ------------------------------------------------------------------ nissaya
from my2rom import is_burmese_word  # noqa: E402


def es_entrada(t):
    """Renglón de entrada: «RAÍZ၊ သည်။ …» o «RAÍZ သည်။ …», o la raíz y la lista de
    sus ဓာတ် («အဂ’ဂ္ဂါ၊ အဂဓာတ်, အဂ္ဂဓာတ်တို့သည်။»). La raíz es pāḷi, no birmano."""
    toks = t.split()
    if not toks or NUM.match(t):
        return False
    lema = toks[0].rstrip("၊။,")
    if not lema or is_burmese_word(lema) or not re.match(r"[က-ဿ]", lema):
        return False
    cabeza = " ".join(toks[:5])
    return toks[0].endswith("၊") or "သည်" in cabeza


def nissaya(pag):
    versos, entradas = [], []
    verso, ent, en_nota = None, None, False
    for h in NISSAYA:
        w, L = renglones(h)
        cuerpo = [l for i, l in enumerate(L) if not es_titulillo(i, l, w)]
        for l in cuerpo:
            t = l["t"]
            margen = l["x0"] < 0.15 * w
            m = NUM.match(t)
            despues = t[m.end():].split()[:2] if m else []
            if (m and not t.lstrip().startswith("[") and despues
                    and not any(is_burmese_word(x) or re.search(r"[()\"“”]", x) for x in despues)):
                verso = {"leido": num(m.group(1)), "lineas": [t], "hoja": h, "pagina": pag.get(h, "")}
                versos.append(verso)
                ent, en_nota = None, False
                continue
            if verso and len(verso["lineas"]) < 3 and ent is None and not margen and not t.startswith("["):
                verso["lineas"].append(t)        # pādas siguientes
                continue
            if margen and es_entrada(t):
                toks = t.split()
                lema = toks[0].rstrip("၊။,")
                ent = {"lema": lema, "texto": [" ".join(toks[1:])], "notas": [],
                       "verso_idx": len(versos) - 1, "hoja": h, "pagina": pag.get(h, "")}
                entradas.append(ent)
                en_nota = False
                continue
            if ent is None:
                continue
            if t.startswith("[") or en_nota:
                if t.startswith("[") or not ent["notas"]:
                    ent["notas"].append(t)
                else:
                    ent["notas"][-1] += " " + t
                en_nota = "]" not in t
            else:
                ent["texto"].append(t)
    return versos, entradas


def sentido(texto):
    """«PALI၊ BIRMANO၌ ဖြစ်၏» del cuerpo de la entrada: el sentido pāḷi (locativo)
    y su glosa birmana. Sólo lo que la entrada dice; si no cuadra, vacío."""
    t = " ".join(texto)
    for frase in t.split("။"):
        if "၌" in frase and "၊" in frase:
            pali, _, bir = frase.strip().partition("၊")
            pali = pali.strip()
            if " " not in pali and pali:
                return pali, bir.replace("ဖြစ်၏", "").replace("ဖြစ်ကုန်၏", "").strip()
    return "", ""


def gana(texto):
    t = " ".join(texto)
    m = re.search(r"(?:^|။)\s*([^\s၊။]+)၊\s*([^\s။]*တည်း)", t)
    return m.group(1) if m else ""


def rom(w):
    w = re.sub(r"[’'‘“”\"]", "", w).replace("ဥု", "ဦ")
    return translit_word(w)


def candidatos(r):
    """Del nominativo del verso al lema de las otras obras: kako → kaka; agi, kamu
    quedan; el plural de los compuestos (-ā) vuelve a -a."""
    r = r.rstrip(",.")
    c = [r]
    if r[-1:] in ("o", "ā"):
        c.append(r[:-1] + "a")
    if r[-1:] == "ī":
        c.append(r[:-1] + "i")
    if r[-1:] == "ū":
        c.append(r[:-1] + "u")
    return c


def lexico(ents):
    """Cuarto testigo, externo: ¿existe la raíz en el Saddanīti o en el Dhātupāṭha?
    Y si existe en el Saddanīti, ¿coincide además el sentido pāḷi? (como en la
    concordancia de la sesión 29: lema y glosa)."""
    R = json.load(open(os.path.join(RAIZ, "recursos", "raices", "raices.json"), encoding="utf-8"))
    D = json.load(open(os.path.join(RAIZ, "recursos", "raices", "dhatupatha.json"), encoding="utf-8"))
    sad, dp = {}, {}
    for r in R["raices"]:
        for x in r["raices"]:
            sad.setdefault(unicodedata.normalize("NFC", x), []).append(r)
    for x in D["entradas"]:
        dp.setdefault(unicodedata.normalize("NFC", x["raiz"]), []).append(x["n"])
    for e in ents:
        c = candidatos(e["lema_rom"])
        e["sad"] = sorted({r["id"] for k in c for r in sad.get(k, [])})
        e["dp"] = sorted({n for k in c for n in dp.get(k, [])})
        g = e["sentido_rom"][:5]
        e["sad_glosa"] = sorted({r["id"] for k in c for r in sad.get(k, [])
                                 if g and len(g) >= 4 and g in r.get("glosa", "")})


def informe(vp, vn, ents):
    from collections import Counter
    cnt = Counter(e["verso"] for e in ents)
    por_n = {v["n"]: v for v in vp}
    L = ["# Dhātvatthasaṅgaha-nissaya — cola de revisión", "",
         "Generado por `herramientas/dhatvatthasangaha/extraer.py`. **Local: no se publica** "
         "(decisión del IEBH, 2026-10-10).", "",
         "## 1. Versos cuyo número de raíces no cuadra", "",
         "La cifra final del verso dice cuántas raíces trae; aquí, las que no coinciden con "
         "las entradas halladas. Una diferencia puede ser una entrada perdida, una de más o "
         "la cifra mal leída.", "", "| verso | hoja | página | cifra | entradas |", "| ---: | ---: | ---: | ---: | ---: |"]
    for n in range(2, 434):
        v = por_n.get(n)
        if v and v["cuenta"] is not None and v["cuenta"] != cnt[n]:
            L.append("| %d | %d | %s | %d | %d |" % (n, v["hoja"], v["pagina"], v["cuenta"], cnt[n]))
    L += ["", "## 2. Entradas que no pasan los tres testigos", "",
          "| hoja | página | verso | raíz (OCR) | rom. | testigos | Sad. | DP |", "| ---: | ---: | ---: | --- | --- | ---: | --- | --- |"]
    for e in ents:
        if e["coinciden"] < 3:
            L.append("| %d | %s | %s | %s | %s | %d | %s | %s |" % (
                e["hoja"], e["pagina"], e["verso"], e["lema"], e["lema_rom"], e["coinciden"],
                ",".join(map(str, e["sad"])), ",".join(map(str, e["dp"]))))
    open(os.path.join(SALIDA, "revision.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")


def main():
    pag = paginas()
    vp = versos_pali(pag)
    vn, ents = nissaya(pag)
    numerar(vn)
    # Cada entrada cuelga del último verso visto en el nissaya. Si ese verso no se
    # detectó (renglón mal leído), la raíz se busca en los versos vecinos del pāḷi
    # y se reasigna sólo si aparece en uno y nada más, sin volver atrás en la serie.
    por_n = {v["n"]: v for v in vp}
    vn_por_n = {v["n"]: v for v in vn}
    leidos_ok = sum(1 for v in vp if v["leido"] == v["n"])
    plano = {n: llano(" ".join(v["lineas"])) for n, v in por_n.items()}
    ents = [e for e in ents if e["verso_idx"] >= 0 and 2 <= vn[e["verso_idx"]]["n"] <= 433]
    piso = 2
    for e in ents:
        n = max(vn[e["verso_idx"]]["n"], piso)
        L = llano(e["lema"])
        if L and L not in plano.get(n, ""):
            cand = [k for k in (n + 1, n + 2) if L in plano.get(k, "")]
            if len(cand) == 1:
                n = cand[0]
                e["verso_reasignado"] = True
        piso = n
        e["verso"] = n
        vnis, vpal = vn_por_n.get(n), por_n.get(n)
        e["testigos"] = {
            "margen": e["lema"],
            "verso_nissaya": bool(vnis and L and L in llano(" ".join(vnis["lineas"]))),
            "verso_pali": bool(vpal and L and L in plano[n]),
        }
        e["coinciden"] = 1 + e["testigos"]["verso_nissaya"] + e["testigos"]["verso_pali"]
        e["sentido_pali"], e["sentido_my"] = sentido(e["texto"])
        e["gana_my"] = gana(e["texto"])
        e["lema_rom"] = rom(e["lema"])
        e["sentido_rom"] = rom(e["sentido_pali"]) if e["sentido_pali"] else ""
        e.pop("verso_idx")
    lexico(ents)
    os.makedirs(SALIDA, exist_ok=True)
    json.dump({"versos_pali": vp, "versos_nissaya": vn, "entradas": ents},
              open(os.path.join(SALIDA, "datos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    from collections import Counter
    c = Counter(e["coinciden"] for e in ents)
    print("versos pāḷi:", len(vp), "· último nº:", vp[-1]["n"], "· nº leído y en serie:", leidos_ok)
    print("  saltos en la serie:", [(v["n"], v["hoja"]) for v in vp if v.get("salto")])
    print("  versos de 1 o 3+ renglones:", [(v["n"], v["hoja"], len(v["lineas"])) for v in vp if len(v["lineas"]) != 2])
    print("versos en el nissaya:", len(vn))
    print("entradas:", len(ents), "· testigos que coinciden:", dict(sorted(c.items())))
    print("con sentido pāḷi:", sum(1 for e in ents if e["sentido_pali"]))
    # el propio libro da el número de raíces de cada kaṇḍa (renglones de cierre)
    KANDAS = [(1, 2, 73, 277), (3, 74, 109, 159), (4, 110, 150, 177), (5, 151, 217, 266),
              (6, 218, 303, 316), (7, 304, 433, 442)]
    for k, a_, z, libro in KANDAS:
        n_ = sum(1 for e in ents if e["verso"] and a_ <= e["verso"] <= z)
        print("  kaṇḍa", k if k > 1 else "1-2", "versos %d-%d: entradas %d, el libro dice %d" % (a_, z, n_, libro))
    print("  entradas fuera de los versos 2-433:", sum(1 for e in ents if not e["verso"] or not 2 <= e["verso"] <= 433))
    fuerte = [e for e in ents if e["coinciden"] == 3 and e["sad"]]
    print("tres testigos y raíz conocida en el Saddanīti:", len(fuerte),
          "· además con el mismo sentido:", sum(1 for e in fuerte if e["sad_glosa"]))
    print("con algún testigo en el Saddanīti o el Dhātupāṭha:", sum(1 for e in ents if e["sad"] or e["dp"]))
    informe(vp, vn, ents)
    suma = sum(v["cuenta"] or 0 for v in vp)
    print("raíces según los versos (suma de las cifras finales):", suma,
          "· versos sin cifra leída:", sum(1 for v in vp if v["cuenta"] is None))


if __name__ == "__main__":
    main()
