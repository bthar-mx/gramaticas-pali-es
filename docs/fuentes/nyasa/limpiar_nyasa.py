#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Limpieza del Nyāsa-Pāḷi (Mukhamattadīpanī) — pandoc markdown → master limpio.

Fases:
  1. Limpieza mecánica de formato (des-escapes pandoc, marcadores de página,
     cabeceras corrientes de la edición impresa, líneas en blanco).
  2. Correcciones léxicas inequívocas, cada una registrada con recuento.
La fase 2 sólo aplica formas listadas explícitamente en CORRECCIONES.
"""
import re, sys, unicodedata

SRC = "nyasa_raw.md"
DST = "Nyasa_Pali_Mukhamattadipani_master.md"
LOG = "correcciones_aplicadas.tsv"

txt = open(SRC, encoding="utf-8").read()
txt = unicodedata.normalize("NFC", txt)

# ---------- FASE 1: formato ----------

# 1a. Cabeceras corrientes de la edición impresa (running headers):
#     líneas que sólo contienen "Nyāsapāḷi" / variantes (con o sin #, **, >)
runner = re.compile(
    r"^[>\s#*]*Ny[āa][sd]a[- ]?[Pp][āa][ḷl]?[ḷl]?i[*\s]*$"
    r"|^[>\s#*]*Ny[āa]sap[āa][ṭt]ha[*\s]*$",
    re.M)
n_runners = len(runner.findall(txt))
txt = runner.sub("", txt)

# 1b. Marcadores de página → [p. N]  (Page. 22 / Page-124 / ## Page 201 / Page, 12 ...)
pagepat = re.compile(r"^[>\s#*]*Page[\s.,:-]*([0-9]+)\s*p?[*\s]*$", re.M)
n_pages = len(pagepat.findall(txt))
txt = pagepat.sub(r"[p. \1]", txt)
# marcadores incrustados dentro de línea: "Page.22p" pegado
inline_page = re.compile(r"\bPage[\s.,:-]*([0-9]+)\s*p?\b")
n_pages_in = len(inline_page.findall(txt))
txt = inline_page.sub(r"[p. \1]", txt)
# variante abreviada: "P(271).---" / "P.(284)---"
ppat = re.compile(r"^P\.?\(\s*([0-9]+)\s*\)\.?\s*-*\s*$", re.M)
n_pages_in += len(ppat.findall(txt))
txt = ppat.sub(r"[p. \1]", txt)

# 1c. Des-escapes pandoc: \( \) \. \_ \* \' \" \[ \] \-
txt = re.sub(r"\\([().\_*'\"\[\]\-])", r"\1", txt)

# 1d. Líderes de puntos de la mātikā:  "..... ....."  → " — "
txt = re.sub(r"(?:\.{3,}\s*)+", " — ", txt)

# 1e. Cabeceras markdown espurias de pandoc (####### vacíos, niveles absurdos)
txt = re.sub(r"^#{5,}\s*$", "", txt, flags=re.M)
txt = re.sub(r"^(#{5,})\s*", "### ", txt, flags=re.M)

# 1f. Colapsar >2 líneas en blanco
txt = re.sub(r"\n{3,}", "\n\n", txt)

# ---------- FASE 2: correcciones léxicas inequívocas ----------
# (forma errónea, forma correcta, justificación breve)
CORRECCIONES = [
    ("Bhavagato", "Bhagavato", "error de tecleo; genitivo de Bhagavant"),
    ("añññathā", "aññathā", "triple ñ imposible"),
    ("Vibhaṅgaṭṭhkathā", "Vibhaṅgaṭṭhakathā", "sílaba omitida en -aṭṭhakathā"),
    ("Tddhhita", "Taddhita", "error de tecleo en título de capítulo"),
    ("Vatuttho paricchedo", "Catuttho paricchedo", "colofón: sigue a tatiyo; V por C"),
    ("Kitabbidhānaakappe", "Kitabbidhānakappe", "doble a por duplografía"),
    ("Mukhamattadipaniyaṃ", "Mukhamattadīpaniyaṃ", "macrón omitido en dīpanī"),
    ("mukhamattadipaniyaṃ", "mukhamattadīpaniyaṃ", "macrón omitido en dīpanī"),
    ("Samattomukhamattadīpaniyaṃnāmakappe", "Samatto mukhamattadīpaniyaṃ nāmakappe", "colofón sin espacios"),
    ("samattomukhamattadīpaniyaṃnamakappetaddhitakappo", "Samatto mukhamattadīpaniyaṃ nāmakappe taddhitakappo", "colofón sin espacios; namakappe→nāmakappe"),
    ("Samattomukhamattadīpaniyaṃ", "Samatto mukhamattadīpaniyaṃ", "colofón sin espacio"),
    ("samattomukhamattadīpaniyaṃkitabbidhānakappedutiyoparicchedo", "Samatto mukhamattadīpaniyaṃ kitabbidhānakappe dutiyo paricchedo", "colofón sin espacios"),
    ("kitabbidhānakappedutiyo paricchedo", "kitabbidhānakappe dutiyo paricchedo", "colofón sin espacio"),
    ("Samattomukhamattadīpa niyaṃ", "Samatto mukhamattadīpaniyaṃ", "colofón mal partido"),
    ("katabbidhāna kappetatiyoparicchedo", "kitabbidhānakappe tatiyo paricchedo", "colofón sin espacios; katabbidhāna→kitabbidhāna"),
    ("Samattomukhamattadīpaniyaṃnāmakappe", "Samatto mukhamattadīpaniyaṃ nāmakappe", "colofón sin espacios"),
    ("dutiyoparicchedo", "dutiyo paricchedo", "colofón sin espacio"),
    ("Samattomukhamattadīpaniyaṃ nāmakappe tatiyo", "Samatto mukhamattadīpaniyaṃ nāmakappe tatiyo", "sin espacio"),
    ("ākhayā takappe", "ākhyātakappe", "colofón mal partido"),
    ("Kitabbidhāne Uṇādikappo", "Kitabbidhānakappe Uṇādikappo", None),
    ("dīpaniyaṃnāmakappe", "dīpaniyaṃ nāmakappe", "colofón sin espacio"),
    ("mukhamattadīpaniyaṃkitabbidhānakappe", "mukhamattadīpaniyaṃ kitabbidhānakappe", "colofón sin espacio"),
    ("catutthoparicchedo", "catuttho paricchedo", "colofón sin espacio"),
    ("paṭhamoparicchedo", "paṭhamo paricchedo", "colofón sin espacio"),
    ("aṭṭhamoparicchedo", "aṭṭhamo paricchedo", "colofón sin espacio"),
    ("tatiyoparicchedo", "tatiyo paricchedo", "colofón sin espacio"),
    ("Samatta mukhamatta dīpaniyaṃ", "Samatto mukhamattadīpaniyaṃ", "colofón: fórmula fija Samatto; palabra mal partida"),
    ("kitabbidhānakappedutiyo", "kitabbidhānakappe dutiyo", "colofón sin espacio"),
]

log_lines = ["forma_original\tforma_corregida\tocurrencias\tjustificación"]
total = 0
for wrong, right, why in CORRECCIONES:
    n = txt.count(wrong)
    if n:
        txt = txt.replace(wrong, right)
        total += n
        log_lines.append(f"{wrong}\t{right}\t{n}\t{why or ''}")

txt = re.sub(r"\n{3,}", "\n\n", txt).strip() + "\n"

open(DST, "w", encoding="utf-8").write(txt)
open(LOG, "w", encoding="utf-8").write("\n".join(log_lines) + "\n")

print(f"cabeceras corrientes eliminadas: {n_runners}")
print(f"marcadores de página normalizados: {n_pages} (línea) + {n_pages_in} (incrustados)")
print(f"correcciones léxicas aplicadas: {total}")
print(f"master: {DST}  ({len(txt)} chars)")
