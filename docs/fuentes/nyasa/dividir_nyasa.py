#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Divide el master del Nyāsa en 8 archivos por capítulo del proyecto.
El corte se hace por colofones (no por números de línea), y se verifica
que la concatenación de todas las partes reproduzca el master byte a byte."""
import re, hashlib

t = open("Nyasa_Pali_Mukhamattadipani_master.md", encoding="utf-8").read()

def pos_after(pattern, start=0):
    m = re.search(pattern, t[start:], re.S)
    if not m:
        raise SystemExit(f"marcador no hallado: {pattern}")
    return start + m.end()

# límites
i_matika  = t.index("### Kaccayanasuttapāṭha")          # fin del prólogo
i_sandhi  = t.index("Nyāsa Pāṭha")                      # inicio comentario sandhi
e_sandhi  = pos_after(r"pañcamo paricchedo\.", i_sandhi)
e_nama    = pos_after(r"nāmakappe pañcamo paricchedo\.", e_sandhi)
e_karaka  = pos_after(r"Kārakakappo chaṭṭho paricchedo", e_nama)
e_samasa  = pos_after(r"samāsakappo.*?Sattamo paricchedo\.", e_karaka)
e_taddh   = pos_after(r"taddhitakappo.*?aṭṭhamo paricchedo\.", e_samasa)
e_akhyata = pos_after(r"ākhyātakappe.*?Catuttho paricchedo\.", e_taddh)
e_kita    = pos_after(r"kitabbidhānakappe.*?Pañcamo paricchedo", e_akhyata)
# uṇādi = resto hasta EOF

partes = [
    ("00", "prologo-y-matika", 0, i_sandhi),
    ("01", "sandhi",   i_sandhi, e_sandhi),
    ("02", "nama",     e_sandhi, e_nama),
    ("03", "karaka",   e_nama,   e_karaka),
    ("04", "samasa",   e_karaka, e_samasa),
    ("05", "taddhita", e_samasa, e_taddh),
    ("06", "akhyata",  e_taddh,  e_akhyata),
    ("07", "kibbidhana", e_akhyata, e_kita),
    ("08", "unadi",    e_kita,   len(t)),
]

NOMBRES = {"00":"Prólogo y Kaccāyanasuttapāṭha (mātikā)","01":"Sandhi-Kappa (§1–§51 en esta edición)",
"02":"Nāma-Kappa (§52–§270 en esta edición: §52 Jinavacanayuttaṃ hi abre el Nāmakappa aquí)","03":"Kāraka-Kappa (§271–§315)","04":"Samāsa-Kappa",
"05":"Taddhita-Kappa","06":"Ākhyāta-Kappa","07":"Kibbidhāna-Kappa",
"08":"Uṇādi-Kappa (numeración propia de la edición: reinicia)"}

cab = ("<!-- Nyāsa-Pāḷi (Mukhamattadīpanī), Vimalabuddhi — edición Sudhammavatī, Yangon.\n"
"     Extracción mecánica del master Nyasa_Pali_Mukhamattadipani_master.md; NO editar aquí:\n"
"     corregir en el master y regenerar con dividir_nyasa.py.\n"
"     Referencia de segunda capa. Transcripción con ruido de OCR: no citar textualmente\n"
"     sin verificación. Correcciones aplicadas: ver Nyasa_errata.md. -->\n\n")

recomp = ""
for num, slug, a, b in partes:
    seg = t[a:b]
    recomp += seg
    fn = f"Nyasa-{num}-{slug}.md"
    open(fn, "w", encoding="utf-8").write(cab + f"# Nyāsa — {NOMBRES[num]}\n\n" + seg.strip() + "\n")
    print(f"{fn}: {len(seg)} chars")

assert recomp == t, "¡la recomposición NO es byte a byte!"
print("recomposición byte a byte: OK")
print("md5 master:", hashlib.md5(t.encode()).hexdigest())
