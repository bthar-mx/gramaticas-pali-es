#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera `recursos/corpus/corpus-formas.json`: el léxico del canon.

    python3 herramientas/generar_corpus_formas.py /ruta/al/repo/OSBCT

Lee los volúmenes convertidos y verificados del corpus del Sexto Concilio
(OSBCT, `site/*.json`) y produce la lista de formas atestiguadas, para que el
solucionador proponga cortes con las palabras de la propia edición en lugar
del DPD (decisión del Venerable, 2026-08-28: el DPD se deja de lado; la
autoridad es Kaccāyana y el texto de la edición).

Esto reemplaza al `corpus-formas.json` que la entrega de Miguel De Anquín
probó el 23-24 de agosto: aquél salió de la capa de texto CRUDA de 40 PDF,
que no trae ni una «ṃ» (defecto VZTimes, resuelto hace tiempo en la
conversión del OSBCT), y dio 22.485 formas. Éste sale del corpus convertido
y verificado, con el texto correcto.

Higiene, según el DICTIONARY_ROADMAP del OSBCT, apéndice A.1:

- se quitan los marcadores de aparato: el dígito pegado a la palabra
  (`malyadhare1`);
- se excluyen los seis párrafos que traen un índice de palabras impreso
  dentro del cuerpo;
- una ficha es una racha máxima de letras pāḷi más el apóstrofo de elisión;
  el apóstrofo se conserva DENTRO de la ficha para no partir `te’tādiso` en
  fragmentos de elisión que licenciarían cortes falsos — después `cotejo()`
  lo quita al comparar;
- «ṁ» de la edición y «ṃ» moderna se identifican, como hace `cotejo()`.
"""

import json
import os
import re
import sys
import unicodedata
from collections import Counter

# Letras del alfabeto pāḷi en romanización, más el apóstrofo de elisión.
LETRA = "aāiīuūeokgcjñṭḍṇtdnpbmyrlvshḷṅṃṁ"
FICHA = re.compile("[" + LETRA + LETRA.upper() + "’']+")
DIGITO_PEGADO = re.compile(r"(?<=[a-zāīūṁṃṅñṭḍṇḷ])\d{1,2}\b")

# HANDOFF OSBCT 2026-07-29q: índices de palabras impresos dentro del cuerpo.
INDICES_IMPRESOS = {
    ("03Vin03", 489), ("24Khu07", 210), ("24Khu07", 211),
    ("34KhuA15", 944), ("38KhuA19", 855), ("51Vism01", 363),
}


def cotejo(t):
    t = unicodedata.normalize("NFC", t)
    t = t.replace("’", "").replace("'", "").replace("-", "")
    return t.lower().replace("ṁ", "ṃ")


def main():
    if len(sys.argv) != 2 or not os.path.isdir(os.path.join(sys.argv[1], "site")):
        print("Uso: generar_corpus_formas.py /ruta/al/repo/OSBCT")
        return 1
    osbct = sys.argv[1]
    vols = sorted(f for f in os.listdir(os.path.join(osbct, "site"))
                  if re.fullmatch(r"\d{2}[A-Za-z0-9]+\.json", f))
    formas = Counter()
    nvol = 0
    for f in vols:
        try:
            d = json.load(open(os.path.join(osbct, "site", f), encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if not isinstance(d, dict) or "paragraphs" not in d:
            continue
        vol = f[:-5]
        nvol += 1
        for i, p in enumerate(d["paragraphs"]):
            if (vol, i) in INDICES_IMPRESOS:
                continue
            t = DIGITO_PEGADO.sub("", p.get("text") or "")
            for m in FICHA.findall(t):
                q = cotejo(m)
                if len(q) >= 2:
                    formas[q] += 1
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    destino = os.path.join(raiz, "recursos", "corpus", "corpus-formas.json")
    salida = {
        "_meta": {
            "que_es": "Formas atestiguadas del corpus convertido del Sexto Concilio, para proponer cortes con las palabras de la propia edición.",
            "fuente": "OSBCT site/*.json (corpus convertido y verificado), {0} volúmenes".format(nvol),
            "higiene": "aparato quitado; 6 índices impresos excluidos; apóstrofo conservado dentro de la ficha; ṁ=ṃ",
            "formas": len(formas),
            "fichas": sum(formas.values()),
        },
        "formas": dict(formas.most_common()),
    }
    json.dump(salida, open(destino, "w", encoding="utf-8"), ensure_ascii=False)
    print("{0} volúmenes · {1:,} formas distintas · {2:,} fichas → {3}".format(
        nvol, len(formas), sum(formas.values()), os.path.relpath(destino, raiz)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
