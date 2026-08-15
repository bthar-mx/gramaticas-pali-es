#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convierte el maestro `docs/2. Nāma-Kappa.md` al formato del generador
(`kaccayana/02-nama-kappa.md`), según briefing-05 §11 y briefing-07 §6:

  1. Desglose del encabezado: `\\[A \\+ B \\= N voces\\]` → `\\[A \\+ B, N\\]`.
  2. TRES bloques por sutta: se inserta un `---` antes del bloque de
     ejemplos (primer rótulo «Ejemplo(s)…:» exento, primera viñeta, o rótulo
     «Ejemplos:» pegado al final de la vutti, que pasa a línea propia).
     Todo lo que sigue (kimatthaṃ incluido) queda en el tercer bloque,
     en el orden del maestro (decisión de Angel, sesión 08).
  3. Ejemplos con asterisco → lista numerada `1.`, `2.`, …
  4. Notas en prosa («Nota:», «Nota al pie:», «Nota del traductor…:») →
     notas al pie `[^n]` ancladas + definición al final; renumeración
     global de todas las notas en orden de aparición.

Principio del proyecto: proponer y verificar, nunca afirmar. El script
recompone el maestro a partir del archivo convertido (transformaciones
inversas) y exige igualdad byte a byte; si no la hay, no escribe nada.
"""

import re
import sys

SRC = "docs/2. Nāma-Kappa.md"
DST = "kaccayana/02-nama-kappa.md"

RE_HDR = re.compile(r'^\*\*(\d+)\\\. (\d+)\\\. ')
RE_DEF = re.compile(r'^\[\^(\d+)\]:\s{2}(.*)$')
RE_DESGLOSE = re.compile(r'^(.*?) \\= (\d+) (voces|voz)(\\\])(\s*)$')
RE_LABEL = re.compile(r'^Ejemplos?\b[^:]*:$')             # rótulo exento
RE_INLINE_LABEL = re.compile(r'^(.*\S)\s+Ejemplos:\s*$')  # pegado a la vutti
RE_BULLET = re.compile(r'^\* ')
RE_NUM = re.compile(r'^\d+\. ')
RE_NOTA = re.compile(r'^Nota(?: al pie| del traductor[^:]*)?: ')
RE_ANCLA = re.compile(r'\[\^([0-9]+|X\d+)\]')

registro = {"suttas_divididos": [], "suttas_sin_tercer_bloque": [],
            "listas_convertidas": 0, "items": 0, "notas": [],
            "desgloses": 0, "sep77": False}


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


def tr_sep77(n, seg, meta):
    """§77 carece del --- entre pāḷi y español; se inserta y se avisa."""
    if n != 77:
        return seg
    i = next(k for k, l in enumerate(seg) if l.startswith("Después de este"))
    assert seg[i - 1].strip() == "" and "---" not in [x.strip() for x in seg[:i]]
    seg[i:i] = ["---", ""]
    meta["sep77"] = i
    registro["sep77"] = True
    return seg


def indices_sep(seg):
    return [k for k, l in enumerate(seg) if l.strip() == "---"]


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
        m = RE_INLINE_LABEL.match(seg[k])
        if m and not RE_NOTA.match(t):
            meta["rotulo_inline"] = (k, seg[k])
            seg[k] = m.group(1)
            seg[k + 1:k + 1] = ["", "Ejemplos:"]
            corte = k + 2                  # la línea "Ejemplos:" insertada
            break
    if corte is None:
        registro["suttas_sin_tercer_bloque"].append(n)
        return seg
    assert seg[corte - 1].strip() == "", "sutta %d: corte sin línea en blanco" % n
    seg[corte:corte] = ["---", ""]
    meta["corte"] = corte
    registro["suttas_divididos"].append(n)
    # rótulos «Ejemplos:» pegados a la prosa DENTRO del tercer bloque
    # (§227, §229): pasan a línea propia para que el generador los formatee
    seps = indices_sep(seg)
    fin3 = seps[2] if len(seps) > 2 else len(seg)
    rotulos3, k = [], corte + 2
    while k < fin3:
        m = RE_INLINE_LABEL.match(seg[k])
        if m and not RE_NOTA.match(seg[k].strip()):
            rotulos3.append((k, seg[k]))
            seg[k] = m.group(1)
            seg[k + 1:k + 1] = ["", "Ejemplos:"]
            fin3 += 2
            k += 2
        k += 1
    if rotulos3:
        meta["rotulos3"] = rotulos3
        registro.setdefault("rotulos3", []).append((n, len(rotulos3)))
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


def tr_notas(n, seg, meta, nuevas):
    """Notas en prosa → ancla [^Xk] + texto registrado."""
    conv = []
    k = 0
    while k < len(seg):
        l = seg[k]
        t = l.strip()
        if RE_NOTA.match(t) and not RE_HDR.match(l):
            # nota exenta (párrafo propio)
            pid = "X%d" % (len(nuevas) + 1)
            p = k - 1
            while p >= 0 and not seg[p].strip():
                p -= 1
            assert k - p == 2, "§%d: nota exenta no precedida de un blanco" % n
            assert k + 1 < len(seg) and seg[k + 1].strip() == "", \
                "§%d: nota exenta sin blanco posterior" % n
            cuerpo = seg[p].rstrip()
            cola = seg[p][len(cuerpo):]
            seg[p] = cuerpo + "[^%s]" % pid + cola
            conv.append({"tipo": "exenta", "pos_parrafo": p, "linea": l,
                         "id": pid})
            nuevas[pid] = t
            del seg[k:k + 2]               # la nota y el blanco que le sigue
            continue
        if " Nota: " in l and not RE_HDR.match(l):
            pid = "X%d" % (len(nuevas) + 1)
            cuerpo, nota = l.split(" Nota: ", 1)
            seg[k] = cuerpo + "[^%s]" % pid + nota[len(nota.rstrip()):]
            conv.append({"tipo": "inline", "pos": k, "linea": l, "id": pid})
            nuevas[pid] = "Nota: " + nota.rstrip()
        k += 1
    meta["notas"] = conv
    registro["notas"].extend(dict(sutta=n, **c) for c in conv)
    return seg


def convertir(texto):
    lines = texto.split("\n")
    pre, segs, defs = segmentar(lines)

    defs_txt = {}
    for l in defs:
        m = RE_DEF.match(l)
        if m:
            defs_txt[m.group(1)] = m.group(2)

    nuevas, metas = {}, {}
    cuerpo = list(pre)
    for n, seg in segs:
        meta = {}
        seg = tr_header(seg, meta)
        seg = tr_sep77(n, seg, meta)
        seg = tr_split(n, seg, meta)
        seg = tr_bullets(n, seg, meta)
        seg = tr_notas(n, seg, meta, nuevas)
        metas[n] = meta
        cuerpo.extend(seg)

    # renumeración global en orden de aparición
    orden = []
    for l in cuerpo:
        for m in RE_ANCLA.finditer(l):
            orden.append(m.group(1))
    assert len(orden) == len(set(orden)), "anclas repetidas"
    assert set(orden) == set(defs_txt) | set(nuevas), "anclas ≠ definiciones"
    mapa = {old: str(i) for i, old in enumerate(orden, start=1)}
    cuerpo = [RE_ANCLA.sub(lambda m: "[^%s]" % mapa[m.group(1)], l)
              for l in cuerpo]

    defs_nuevas = []
    for old in orden:
        txt = defs_txt[old] if old in defs_txt else nuevas[old]
        defs_nuevas.append("[^{0}]:  {1}".format(mapa[old], txt))
        defs_nuevas.append("")
    if defs_nuevas:
        defs_nuevas.pop()

    convertido = "\n".join(cuerpo + defs_nuevas) + "\n"
    return convertido, metas, mapa, defs, nuevas


# ── Recomposición (inversa) ────────────────────────────────────────────

def recomponer(convertido, metas, mapa, defs_originales):
    lines = convertido.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    fn_start = next(i for i, l in enumerate(lines)
                    if re.match(r'^\[\^\d+\]:', l))
    cuerpo = lines[:fn_start]

    inv = {v: k for k, v in mapa.items()}
    cuerpo = [re.sub(r'\[\^(\d+)\]', lambda m: "[^%s]" % inv[m.group(1)], l)
              for l in cuerpo]

    hdrs = [i for i, l in enumerate(cuerpo) if RE_HDR.match(l)]
    out = list(cuerpo[:hdrs[0]])
    for k, i in enumerate(hdrs):
        j = hdrs[k + 1] if k + 1 < len(hdrs) else len(cuerpo)
        n = int(RE_HDR.match(cuerpo[i]).group(1))
        seg = list(cuerpo[i:j])
        meta = metas[n]

        # 5) notas, en orden inverso
        for c in reversed(meta.get("notas", [])):
            pid = "[^%s]" % c["id"]
            if c["tipo"] == "inline":
                seg[c["pos"]] = c["linea"]
            else:
                p = c["pos_parrafo"]
                assert pid in seg[p], "§%d: ancla %s no está" % (n, pid)
                seg[p] = seg[p].replace(pid, "", 1)
                seg[p + 2:p + 2] = [c["linea"], ""]

        # 4) listas numeradas → viñetas
        for g0, g1 in meta.get("grupos", []):
            for x in range(g0, g1):
                seg[x] = "* " + re.sub(r'^\d+\. ', '', seg[x], count=1)

        # 3 bis) rótulos «Ejemplos:» del tercer bloque, a su forma pegada
        for k3, orig in reversed(meta.get("rotulos3", [])):
            assert seg[k3 + 2].strip() == "Ejemplos:"
            del seg[k3 + 1:k3 + 3]
            seg[k3] = orig

        # 3) corte del tercer bloque
        if "corte" in meta:
            c = meta["corte"]
            assert seg[c] == "---" and seg[c + 1] == ""
            del seg[c:c + 2]
            if "rotulo_inline" in meta:
                ki, orig = meta["rotulo_inline"]
                assert seg[ki + 2].strip() == "Ejemplos:"
                del seg[ki + 1:ki + 3]
                seg[ki] = orig

        # 2) §77
        if "sep77" in meta:
            s = meta["sep77"]
            assert seg[s] == "---" and seg[s + 1] == ""
            del seg[s:s + 2]

        # 1) encabezado
        if "voz" in meta:
            m = re.match(r'^(.*?), (\d+)(\\\])(\s*)$', seg[0])
            seg[0] = "{0} \\= {1} {2}{3}{4}".format(
                m.group(1), m.group(2), meta["voz"], m.group(3), m.group(4))

        out.extend(seg)

    return "\n".join(out + defs_originales)


def main():
    texto = leer(SRC)
    convertido, metas, mapa, defs_orig, nuevas = convertir(texto)
    rehecho = recomponer(convertido, metas, mapa, defs_orig)
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
    print("Desgloses reescritos:", registro["desgloses"])
    print("Suttas con tercer bloque:", len(registro["suttas_divididos"]))
    print("Suttas SIN tercer bloque:", registro["suttas_sin_tercer_bloque"])
    print("Listas convertidas:", registro["listas_convertidas"],
          "· items:", registro["items"])
    print("Separador §77 insertado:", registro["sep77"])
    print("Notas convertidas ({0}):".format(len(registro["notas"])))
    for c in registro["notas"]:
        print("  §{0} [{1}] → [^{2}]  {3}".format(
            c["sutta"], c["tipo"], mapa[c["id"]], nuevas[c["id"]][:72]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
