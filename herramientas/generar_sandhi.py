#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la referencia interactiva de sandhi.

    python3 herramientas/generar_sandhi.py

Junta tres cosas:

  kaccayana/01-sandhi-kappa.md   los 51 aforismos — se derivan del markdown,
                                 nunca se copian: corregir el markdown corrige
                                 también esta página
  recursos/sandhi/reglas.json    las reglas de combinación eufónica y las
                                 formas trabajadas — obra propia, se editan ahí
  recursos/sandhi/plantilla.html el maquetado y la lógica

y escribe site/recursos/sandhi/index.html.
"""

import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "herramientas"))

from generar_capitulo import parsear, partir_bloques, desescapar  # noqa: E402

MD = os.path.join(RAIZ, "kaccayana", "01-sandhi-kappa.md")
REGLAS = os.path.join(RAIZ, "recursos", "sandhi", "reglas.json")
PLANTILLA = os.path.join(RAIZ, "recursos", "sandhi", "plantilla.html")
DESTINO = os.path.join(RAIZ, "site", "recursos", "sandhi", "index.html")

RE_TITULO = re.compile(r'^\*\*(.+?)\*\*$')
RE_ITEM = re.compile(r'^\d+\.\s+(.*)$')
RE_CONTRA = re.compile(r'^Contraejemplos?\b', re.I)
RE_EJEMPLO = re.compile(r'^Ejemplos?\b', re.I)
# Encabezados que el documento pone en negrita pero que no son formas.
RE_ENCABEZADO = re.compile(r'^(Extensión por|Formación de palabras|Nota)', re.I)


def limpiar(t):
    """Quita marcadores de nota, glosas emergentes y escapes."""
    t = re.sub(r'\[\^\d+\]', '', t)
    t = re.sub(r'\{([^|{}]+)\|[^{}]*\}', r'\1', t)
    t = desescapar(t)
    return re.sub(r'\s+', ' ', t).strip()


# El markdown usa dos convenciones para las secuencias de formación:
#   hasta §30   **Título** / «Secuencia:» / lista numerada
#   desde §31   **Título**: paso; paso; paso.
RE_INLINE = re.compile(r'^\*\*(.+)$')


def secuencia_en_linea(t):
    """Devuelve (título, pasos) si la línea trae la forma compacta."""
    if not t.startswith("**"):
        return None
    plano = t.replace("**", "")
    if ":" not in plano:
        return None
    titulo, resto = plano.split(":", 1)
    if RE_ENCABEZADO.match(titulo.strip()):
        return None
    partes = [x.strip(" .") for x in resto.split(";") if x.strip(" .")]
    if len(partes) < 2 or len(titulo) > 60:
        return None
    return limpiar(titulo), [limpiar(x) for x in partes]


def secuencias(bloques):
    """Extrae las secuencias de formación en cualquiera de las dos formas.

    «Secuencia», no «derivación»: en gramática pāḷi la derivación es la
    formación de palabras (taddhita, kita), no la cadena de operaciones
    de sandhi que estas escaleras muestran.
    """
    salida, contra = [], False
    for bloque in bloques:
        titulo, pasos, ultima_negrita = None, [], None

        def cerrar():
            if titulo and pasos and not RE_ENCABEZADO.match(titulo):
                salida.append({"f": limpiar(titulo), "s": list(pasos), "ce": contra})

        for linea in bloque:
            t = linea.strip()
            if not t:
                continue
            if RE_CONTRA.match(t):
                cerrar(); titulo, pasos = None, []
                contra = True
                continue
            if RE_EJEMPLO.match(t):
                cerrar(); titulo, pasos = None, []
                contra = False
                continue
            if t.startswith("Secuencia"):
                # el título es la negrita más cercana por encima
                if ultima_negrita:
                    cerrar(); titulo, pasos = ultima_negrita, []
                continue
            enlinea = secuencia_en_linea(t)
            if enlinea:
                cerrar(); titulo, pasos = None, []
                salida.append({"f": enlinea[0], "s": enlinea[1], "ce": contra})
                continue
            negritas = re.findall(r'\*\*(.+?)\*\*', t)
            if negritas:
                ultima_negrita = negritas[-1].strip(" .:*")
            mt = RE_TITULO.match(t)
            if mt:
                cerrar(); titulo, pasos = mt.group(1), []
                continue
            mi = RE_ITEM.match(t)
            if mi and titulo:
                pasos.append(limpiar(mi.group(1)))
                continue
        cerrar()
    return salida


def suttas_desde_markdown():
    cap = parsear(MD)
    fuera = []
    for s in cap["suttas"]:
        bloques = partir_bloques(s["cuerpo"])
        es = glosa = ""
        if len(bloques) > 1:
            lineas = [x.strip() for x in bloques[1] if x.strip()]
            if lineas:
                es = limpiar(lineas[0])
            # el vutti ampliado: la primera línea que no sea la lista de ejemplos
            for extra in lineas[1:]:
                if not RE_EJEMPLO.match(extra.strip()):
                    glosa = limpiar(extra)
                    break
        split = ""
        if s["desglose"]:
            split = "{0}, {1}".format(desescapar(s["desglose"]), s["voces"])
        fuera.append({
            "kac": s["n"],
            # `rup` es cadena desde la sesión 14 (admite «88, 308»); en el
            # Sandhi siempre es un número, y se conserva como tal.
            "ru": int(s["rup"]) if s["rup"].isdigit() else s["rup"],
            "sad": ", ".join(s["sadd"]) if s["sadd"] else None,
            "pali": limpiar(s["pali"]),
            "split": split,
            "es": es,
            "gloss": glosa,
            "ex": secuencias(bloques[2:]),
        })
    return fuera


def main():
    suttas = suttas_desde_markdown()
    reglas = json.load(open(REGLAS, encoding="utf-8"))
    datos = {"suttas": suttas, "rules": reglas["rules"], "ce": reglas["ce"]}

    plantilla = open(PLANTILLA, encoding="utf-8").read()
    marca = re.search(r'/\*__DATOS__\*/.*?/\*__FIN__\*/', plantilla, re.S)
    if not marca:
        print("La plantilla no tiene el marcador /*__DATOS__*/…/*__FIN__*/")
        return 1
    html = (plantilla[:marca.start()]
            + json.dumps(datos, ensure_ascii=False, separators=(",", ":"))
            + plantilla[marca.end():])

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    open(DESTINO, "w", encoding="utf-8").write(html)

    # ── auditoría de las secuencias ──────────────────────────────────
    # §10 separa la consonante de su vocal, §11 vuelve a unirlas. Si un paso
    # cita §10 y no separa, o §11 y no une, la anotación está mal. Y en
    # pakati-sandhi, donde por definición no ocurre nada, un paso único no
    # puede llevar referencia a ningún aforismo.
    def _texto(paso):
        return re.sub(r'\s*\(([^)]*)\)\s*$', '', paso).strip()

    def _refs(paso):
        m = re.search(r'\(([^)]*)\)\s*$', paso)
        return m.group(1) if m else ""

    fallos = []
    for c in reglas["ce"]:
        etiqueta = "{0} {1} · {2}".format(c["sec"], c["rule"], c["f"])
        if c["sec"] == "pakati" and len(c["s"]) == 1 and "§" in c["s"][0]:
            fallos.append("{0}: paso único con referencia en pakati".format(etiqueta))
        for a, b in zip(c["s"], c["s"][1:]):
            ta, tb, r = _texto(a), _texto(b), _refs(b)
            if not r:
                continue
            if ta == tb:
                fallos.append("{0}: «{1}» no cambia pero cita {2}".format(etiqueta, tb, r))
            if "§10" in r and tb.count(" ") <= ta.count(" "):
                fallos.append("{0}: cita §10 pero no separa".format(etiqueta))
            if "§11" in r and tb.count(" ") >= ta.count(" "):
                fallos.append("{0}: cita §11 pero no une".format(etiqueta))

    # avisos útiles
    sin_glosa = [s["kac"] for s in suttas if not s["es"]]
    sin_split = [s["kac"] for s in suttas if not s["split"]]
    existen = {(r["sec"], str(r["n"])) for r in reglas["rules"]}
    huerf = [c for c in reglas["ce"] if (c["sec"], str(c["rule"])) not in existen]
    sin_ej = [(r["sec"], r["n"]) for r in reglas["rules"]
              if not r.get("sub") and not any(
                  c["sec"] == r["sec"] and str(c["rule"]) == str(r["n"])
                  for c in reglas["ce"])
              and not any(x.get("parent") == str(r["n"]) and x["sec"] == r["sec"]
                          for x in reglas["rules"])]

    print("{0} aforismos · {1} con secuencia · {2} reglas · {3} formas → {4}".format(
        len(suttas), sum(1 for s in suttas if s["ex"]),
        len(reglas["rules"]), len(reglas["ce"]),
        os.path.relpath(DESTINO, RAIZ)))
    if fallos:
        print("\n  SECUENCIAS SOSPECHOSAS:")
        for f in fallos[:12]:
            print("    ✗", f)
        if len(fallos) > 12:
            print("    … y {0} más".format(len(fallos) - 12))

    for etiqueta, lista in (("sin glosa española", sin_glosa),
                            ("sin desglose", sin_split),
                            ("formas huérfanas", huerf),
                            ("reglas sin ejemplo ni subreglas", sin_ej)):
        if lista:
            print("  aviso — {0}: {1}".format(etiqueta, lista[:8]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
