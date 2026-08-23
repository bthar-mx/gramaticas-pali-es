# -*- coding: utf-8 -*-
"""Verificación mecánica de un borrador de traducción contra su fuente.

Uso:
    python3 herramientas/verificar_borrador.py <borrador.md> <ini> <fin> [fuente.md]

<ini> y <fin> son las líneas de la fuente que cubre el borrador. Si no se da
la fuente, se deduce del nombre del borrador leyendo el número de capítulo.

Comprueba en los dos sentidos: que todo párrafo pāḷi del borrador está en la
fuente, y que todo párrafo pāḷi de la fuente está en el borrador. Normaliza
espacios, comillas, negritas, escapes de markdown y llamadas de nota, y
descuenta las referencias canónicas retiradas del cuerpo.

Informa **aparte** de los párrafos que sólo coinciden tras normalizar el
espaciado o la puntuación: ésas son normalizaciones deliberadas del borrador
—palabras pegadas en la fuente, puntuación sobrante al retirar una
referencia— y cada una debe estar documentada en sus NOTAS DE TRABAJO. No son
fallos, pero tampoco se dan por buenas en silencio.

Escrito en la sesión 26 para el Ākhyāta; sirve para cualquier capítulo.
"""
import os, re, sys, unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(RAIZ, "docs")

def fuente_por_defecto(borrador):
    """Deduce la fuente a partir del nombre del borrador (…-suttas-NNN-NNN.md)."""
    import glob
    m = re.search(r"sesion-\d+-suttas-(\d+)-", os.path.basename(borrador))
    if not m:
        return None
    n = int(m.group(1))
    cap = {1: 1, 52: 2, 271: 3, 316: 4, 344: 5, 406: 6, 524: 7}
    inicio = max(k for k in cap if k <= n)
    patron = os.path.join(DOCS, "%d*Kacc*.md" % cap[inicio])
    hits = sorted(glob.glob(patron))
    return hits[0] if hits else None

def norm(s):
    s = unicodedata.normalize("NFC", s)
    s = s.replace("**", "").replace("*", "")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    for a, b in (("\\.", "."), ("\\[", "["), ("\\]", "]"), ("\\-", "-"),
                 ("\\=", "="), ("\\+", "+"), ("\\_", "_"),
                 ("\\(", "("), ("\\)", ")"), ("\\*", "*")):
        s = s.replace(a, b)
    s = re.sub(r"\[\^\d+\]", "", s)
    # referencias canónicas: (Vin. iii, 320), (A. ii, 468; Khu. i, 59), (DhA. i, 30)…
    s = re.sub(r"\s*\((?:[A-ZĀ][A-Za-zĀāĪīŪūṂṃṆṇ]*\.?(?:[A-Z][a-z]*\.)?\s*[ivxlcdm]+,\s*\d+(?:,\s*\d+)*\s*;?\s*)+\)", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def parrafos_pali_borrador(bor):
    cuerpo = re.split(r"^## NOTAS DE NANDISENA", bor, flags=re.M)[0]
    out = []
    for b in cuerpo.split("\n---\n"):
        m = re.match(r"\s*\*\*(\d+)\. \d+\.", b)
        if not m:
            continue
        n = m.group(1)
        for p in b.strip().split("\n\n"):
            p = p.strip()
            if p and not p.startswith("<!--"):
                out.append((n, p))
    return out

def main(path, ini, fin, fuente=None):
    fuente = fuente or fuente_por_defecto(path)
    if not fuente or not os.path.exists(fuente):
        sys.exit("No encuentro la fuente. Pásala como cuarto argumento.")
    print(f"fuente: {os.path.basename(fuente)}  líneas {ini}–{fin}")
    src = "\n".join(open(fuente, encoding="utf-8").read().split("\n")[ini - 1:fin])
    bor = open(path, encoding="utf-8").read()
    NSRC = norm(src)

    ok = 0; fallos = []; espaciado = []; puntuacion = []
    for n, p in parrafos_pali_borrador(bor):
        q = norm(re.sub(r"\[[^\]]*=\s*\d+ (voces|voz)\]", "", p))
        if q and q in NSRC:
            ok += 1
        elif q and q.replace(" ", "") in NSRC.replace(" ", ""):
            ok += 1
            espaciado.append((n, q))
        elif q and re.sub(r"[ .,;]", "", q) in re.sub(r"[ .,;]", "", NSRC):
            ok += 1
            puntuacion.append((n, q))
        else:
            fallos.append((n, q))
    print(f"IDA   párrafos pāḷi del borrador: {ok + len(fallos)} | reproducidos: {ok} | no encontrados: {len(fallos)}")
    if puntuacion:
        print(f"      de ellos, {len(puntuacion)} sólo tras normalizar la puntuación (residuo de la referencia retirada):")
        for n, q in puntuacion:
            print(f"      ~ §{n}: {q[:120]}")
    if espaciado:
        print(f"      de ellos, {len(espaciado)} sólo tras normalizar el espaciado (palabras pegadas en la fuente):")
        for n, q in espaciado:
            print(f"      ~ §{n}: {q[:120]}")
    for n, q in fallos:
        print(f"  !! §{n}: {q[:180]}")

    cuerpo = re.split(r"^## NOTAS DE NANDISENA", bor, flags=re.M)[0]
    NBOR = norm(re.sub(r"\[[^\]]*=\s*\d+ (voces|voz)\]", "", cuerpo))
    marcas = r"(honti|hoti|icc'|Taṃ yathā|kvattho|vibhatti|veditabbaṃ|gahetabbo|yojetabbā|yojetabbo|kimatthaṃ|padānaṃ|paccayo|paccayā|āpajjate|kātabbo|icchati)"
    ingles = r"\b(is|are|the|of|in|for|when|there|after|why|thus|also|sometimes|wishes|treats|acts|causes)\b|\((?:He|he|She|she|They|they|It|it)\)"
    ausentes = []
    for line in src.split("\n"):
        t = line.strip()
        if not t or re.match(r"^\[\^\d+\]:", t):
            continue
        if re.search(marcas, t) and not re.search(ingles, t):
            q = norm(t)
            if q and q not in NBOR and q.replace(" ", "") not in NBOR.replace(" ", ""):
                ausentes.append(q)
    print(f"VUELTA párrafos pāḷi de la fuente ausentes del borrador: {len(ausentes)}")
    for a in ausentes[:20]:
        print("  -", a[:180])

if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]),
         sys.argv[4] if len(sys.argv) > 4 else None)
