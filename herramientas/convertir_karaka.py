#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convierte el maestro `docs/3. Kāraka-Kappa.md` al formato del generador
(`kaccayana/03-karaka-kappa.md`), según briefing-05 §11 y briefing-14 §3.
Modelo: `herramientas/convertir_nama.py` (sesión 08).

  1. Desglose del encabezado: `\\[A \\+ B \\= N voces\\]` → `\\[A \\+ B, N\\]`.
  2. TRES bloques por sutta: se inserta un `---` antes del bloque de
     ejemplos. El corte va en el primer rótulo «Ejemplo(s)…:» (o primera
     viñeta), y se retrocede un párrafo si el inmediatamente anterior es
     un rótulo de entrada —acaba en «:» o es «¿Cómo qué?»—, de modo que
     el rótulo viaje con sus propios ejemplos (decisión de Angel,
     sesión 14; afecta a §271, §272, §275, §277 y §278). El bloque
     español queda así siempre en glosa + vutti.
     Todo lo que sigue al corte (kimatthaṃ incluido) va al tercer bloque,
     en el orden del maestro.
  3. Ejemplos con asterisco → lista numerada `1.`, `2.`, …

A diferencia del Nāma, el maestro del Kāraka **no** tiene notas en prosa:
las 55 notas ya vienen como `[^n]`, numeradas 1–55 en orden de aparición.
El script no las toca; sólo comprueba que anclas y definiciones casen.

Principio del proyecto: proponer y verificar, nunca afirmar. El script
recompone el maestro a partir del archivo convertido (transformaciones
inversas) y exige igualdad byte a byte; si no la hay, no escribe nada.
"""

import re
import sys

SRC = "docs/3. Kāraka-Kappa.md"
DST = "kaccayana/03-karaka-kappa.md"

RE_HDR = re.compile(r'^\*\*(\d+)\\\. ')
RE_DEF = re.compile(r'^\[\^(\d+)\]:\s(.*)$')
RE_DESGLOSE = re.compile(r'^(.*?) \\= (\d+) (voces|voz)(\\\])(\s*)$')
RE_LABEL = re.compile(r'^Ejemplos?\b[^:]*:$')
RE_BULLET = re.compile(r'^\* ')
RE_NUM = re.compile(r'^\d+\. ')
RE_NOTA = re.compile(r'^Nota(?: al pie| del traductor[^:]*)?: ')
RE_ANCLA = re.compile(r'\[\^(\d+)\]')

registro = {"suttas_divididos": [], "suttas_sin_tercer_bloque": [],
            "listas_convertidas": 0, "items": 0, "desgloses": 0,
            "retrocesos": []}


def leer(path):
    return open(path, encoding="utf-8").read()


def segmentar(lines):
    """preámbulo + [(n, líneas_del_sutta)] + defs verbatim."""
    fn_start = next(i for i, l in enumerate(lines) if RE_DEF.match(l))
    hdrs = [i for i, l in enumerate(lines[:fn_start]) if RE_HDR.match(l)]
    pre = lines[:hdrs[0]]
    segs = []
    for k, i in enumerate(hdrs):
        j = hdrs[k + 1] if k + 1 < len(hdrs) else fn_start
        segs.append([int(RE_HDR.match(lines[i]).group(1)), lines[i:j]])
    return pre, segs, lines[fn_start:]


# ── Transformaciones directas (por sutta) ──────────────────────────────

def tr_header(seg, meta):
    m = RE_DESGLOSE.match(seg[0])
    if m:
        seg[0] = "{0}, {1}{2}{3}".format(m.group(1), m.group(2),
                                         m.group(4), m.group(5))
        meta["voz"] = m.group(3)
        registro["desgloses"] += 1
    return seg


def indices_sep(seg):
    return [k for k, l in enumerate(seg) if l.strip() == "---"]


def inicio_parrafo(seg, k):
    """Índice de la primera línea del párrafo al que pertenece seg[k]."""
    p = k
    while p > 0 and seg[p - 1].strip():
        p -= 1
    return p


def retroceder(seg, corte, ini):
    """Si el párrafo anterior al corte es un rótulo de entrada («…:» o
    «¿Cómo qué?»), el corte pasa a incluirlo."""
    p = corte - 1
    while p > ini and not seg[p].strip():
        p -= 1
    if p <= ini or not seg[p].strip():
        return corte, None
    fin_parr = p
    ini_parr = inicio_parrafo(seg, p)
    texto = seg[fin_parr].strip()
    if not (texto.endswith(":") or texto == "¿Cómo qué?"):
        return corte, None
    return ini_parr, seg[ini_parr:fin_parr + 1]


def tr_split(n, seg, meta):
    """Inserta --- antes del bloque de ejemplos, dentro del bloque español."""
    seps = indices_sep(seg)
    assert seps, "sutta %d sin separador" % n
    ini = seps[0] + 1                      # blanco tras el ---
    fin = seps[1] if len(seps) > 1 else len(seg)
    corte = None
    for k in range(ini + 1, fin):
        t = seg[k].strip()
        if RE_LABEL.match(t) or RE_BULLET.match(seg[k]) or RE_NUM.match(seg[k]):
            corte = k
            break
    if corte is None:
        registro["suttas_sin_tercer_bloque"].append(n)
        return seg
    nuevo, rotulo = retroceder(seg, corte, ini)
    if rotulo is not None:
        registro["retrocesos"].append((n, rotulo[-1].strip()[:70]))
        corte = nuevo
    assert seg[corte - 1].strip() == "", \
        "sutta %d: corte sin línea en blanco" % n
    seg[corte:corte] = ["---", ""]
    meta["corte"] = corte
    registro["suttas_divididos"].append(n)
    return seg


def tr_bullets(n, seg, meta):
    if "corte" not in meta:
        return seg
    seps = indices_sep(seg)
    ini = meta["corte"] + 2
    fin = seps[2] if len(seps) > 2 else len(seg)
    grupos, k = [], ini
    while k < fin:
        if RE_BULLET.match(seg[k]):
            g0 = k
            while k < fin and RE_BULLET.match(seg[k]):
                k += 1
            grupos.append((g0, k))
        else:
            k += 1
    for g0, g1 in grupos:
        for idx, x in enumerate(range(g0, g1), start=1):
            seg[x] = "{0}. ".format(idx) + seg[x][2:]
        registro["listas_convertidas"] += 1
        registro["items"] += g1 - g0
    meta["grupos"] = grupos
    return seg


def comprobar_notas(cuerpo, defs_txt):
    """El maestro ya trae las notas como [^n]: sólo se verifican."""
    orden = []
    for l in cuerpo:
        for m in RE_ANCLA.finditer(l):
            orden.append(m.group(1))
    assert len(orden) == len(set(orden)), "anclas repetidas"
    assert set(orden) == set(defs_txt), \
        "anclas ≠ definiciones: %s" % (set(orden) ^ set(defs_txt))
    assert orden == [str(i) for i in range(1, len(orden) + 1)], \
        "las notas no van numeradas 1..N en orden de aparición"
    return orden


def buscar_notas_en_prosa(lines):
    """El Kāraka no debería tener ninguna; si aparece, hay que avisar."""
    sueltas = []
    for i, l in enumerate(lines):
        t = l.strip()
        if RE_NOTA.match(t) and not RE_HDR.match(l) and not RE_DEF.match(l):
            sueltas.append((i + 1, t[:70]))
        elif " Nota: " in l and not RE_HDR.match(l):
            sueltas.append((i + 1, "(en línea) " + t[:60]))
    return sueltas


def convertir(texto):
    lines = texto.split("\n")
    sueltas = buscar_notas_en_prosa(lines)
    assert not sueltas, "notas en prosa inesperadas: %s" % sueltas

    pre, segs, defs = segmentar(lines)
    defs_txt = {}
    for l in defs:
        m = RE_DEF.match(l)
        if m:
            defs_txt[m.group(1)] = m.group(2)

    metas = {}
    cuerpo = list(pre)
    for n, seg in segs:
        meta = {}
        seg = tr_header(seg, meta)
        seg = tr_split(n, seg, meta)
        seg = tr_bullets(n, seg, meta)
        metas[n] = meta
        cuerpo.extend(seg)

    orden = comprobar_notas(cuerpo, defs_txt)
    convertido = "\n".join(cuerpo + defs) + "\n"
    return convertido, metas, defs, orden


# ── Recomposición (inversa) ────────────────────────────────────────────

def recomponer(convertido, metas, defs_originales):
    lines = convertido.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    fn_start = next(i for i, l in enumerate(lines) if RE_DEF.match(l))
    cuerpo = lines[:fn_start]

    hdrs = [i for i, l in enumerate(cuerpo) if RE_HDR.match(l)]
    out = list(cuerpo[:hdrs[0]])
    for k, i in enumerate(hdrs):
        j = hdrs[k + 1] if k + 1 < len(hdrs) else len(cuerpo)
        n = int(RE_HDR.match(cuerpo[i]).group(1))
        seg = list(cuerpo[i:j])
        meta = metas[n]

        # 3) listas numeradas → viñetas
        for g0, g1 in meta.get("grupos", []):
            for x in range(g0, g1):
                seg[x] = "* " + re.sub(r'^\d+\. ', '', seg[x], count=1)

        # 2) corte del tercer bloque
        if "corte" in meta:
            c = meta["corte"]
            assert seg[c] == "---" and seg[c + 1] == "", \
                "§%d: el corte no está donde se anotó" % n
            del seg[c:c + 2]

        # 1) encabezado
        if "voz" in meta:
            m = re.match(r'^(.*?), (\d+)(\\\])(\s*)$', seg[0])
            seg[0] = "{0} \\= {1} {2}{3}{4}".format(
                m.group(1), m.group(2), meta["voz"], m.group(3), m.group(4))

        out.extend(seg)

    return "\n".join(out + defs_originales)


def main():
    texto = leer(SRC)
    convertido, metas, defs_orig, orden = convertir(texto)
    rehecho = recomponer(convertido, metas, defs_orig)
    if rehecho != texto:
        import difflib
        d = list(difflib.unified_diff(texto.split("\n"), rehecho.split("\n"),
                                      lineterm="", n=1))
        print("LA RECOMPOSICIÓN NO REPRODUCE EL MAESTRO — no se escribe nada.")
        print("\n".join(d[:80]))
        return 1
    with open(DST, "w", encoding="utf-8") as f:
        f.write(convertido)
    print("Recomposición byte a byte: OK → escrito", DST)
    print("Suttas:", len(metas), "· notas verificadas:", len(orden))
    print("Desgloses reescritos:", registro["desgloses"])
    print("Suttas con tercer bloque:", len(registro["suttas_divididos"]))
    print("Suttas SIN tercer bloque:", registro["suttas_sin_tercer_bloque"])
    print("Listas convertidas:", registro["listas_convertidas"],
          "· items:", registro["items"])
    print("Cortes retrocedidos al rótulo de entrada "
          "({0}):".format(len(registro["retrocesos"])))
    for n, r in registro["retrocesos"]:
        print("  §{0}  {1}".format(n, r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
