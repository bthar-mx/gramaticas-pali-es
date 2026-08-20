# Nyāsa-Pāḷi (Mukhamattadīpanī) — Registro de correcciones

Fuente: transcripción .docx de la edición Sudhammavatī (Yangon). Master limpio:
`Nyasa_Pali_Mukhamattadipani_master.md` (md5 `df5699b9ae436590e0e36d5361e32707`).
Scripts: `limpiar_nyasa.py` (limpieza + correcciones), `dividir_nyasa.py` (extracción
por capítulos, verificada byte a byte contra el master).

## 1. Limpieza mecánica de formato (no altera el texto pāḷi)

- 24 cabeceras corrientes de la edición impresa eliminadas («Nyāsapāḷi», «Nyāsapāṭha» y variantes, incluida la errata «Nyādapāḷi»).
- 370 marcadores de página normalizados a `[p. N]` (formas originales: `Page. 22`, `Page-124`, `Page, 12`, `Page.22p`, `P(271).---`, etc.). Remiten a la paginación de la edición impresa.
- Des-escapes de pandoc (`\(`, `\.`, `\_`, etc.); líderes de puntos de la mātikā (`.....`) → «—»; niveles de cabecera markdown espurios reducidos; líneas en blanco colapsadas.

## 2. Correcciones léxicas aplicadas (inequívocas) — 28 ocurrencias

| Original | Corregido | N | Justificación |
|---|---|---|---|
| Bhavagato | Bhagavato | 1 | error de tecleo; genitivo de Bhagavant |
| añññathā | aññathā | 1 | triple ñ imposible |
| Vibhaṅgaṭṭhkathā | Vibhaṅgaṭṭhakathā | 1 | sílaba omitida en -aṭṭhakathā |
| Tddhhita | Taddhita | 1 | error de tecleo en título de capítulo |
| Vatuttho paricchedo | Catuttho paricchedo | 1 | colofón: sigue a tatiyo; V por C |
| Kitabbidhānaakappe | Kitabbidhānakappe | 1 | duplografía de a |
| Mukhamattadipaniyaṃ / mukhamattadipaniyaṃ | °dīpaniyaṃ | 2 | macrón omitido en dīpanī |
| Samatta mukhamatta dīpaniyaṃ | Samatto mukhamattadīpaniyaṃ | 1 | fórmula fija del colofón; palabra mal partida |
| ākhayā takappe | ākhyātakappe | 1 | colofón mal partido |
| Colofones fusionados (Samattomukhamatta°, °kappedutiyo, dutiyoparicchedo, catutthoparicchedo, paṭhamoparicchedo, tatiyoparicchedo, aṭṭhamoparicchedo, dīpaniyaṃnāmakappe, °kitabbidhānakappe°, namakappe→nāmakappe, katabbidhāna→kitabbidhāna) | separados / normalizados | 18 | espaciado de colofones; sólo fórmulas fijas |

## 3. Zona gris — NO corregido; pendiente de decisión de Angel

- **§12 (comentario):** «a ca ā ca i ca ī ca e cā ti *viggataṃ* katvā» — se esperaría *viggahaṃ* (análisis del compuesto). Posible errata; posible lectura de la edición.
- **§12 (comentario):** «kasmī sarā ti vuttan?» — se esperaría *kasmā*.
- Colofones con variantes menores conservadas: «Mukhamattadīpaniyam» (m final por ṃ, 2×), «mukhamattadīpanīyaṃ» (ī larga en °nīyaṃ, 1×).
- «Kitabbidhāna» como nombre del capítulo 7 (frente a «Kibbidhāna» de otras ediciones): forma consistente de esta edición; se conserva.
- **Colofón duplicado** del dutiyo pariccheda del Kibbidhāna (aparece dos veces con texto circundante repetido): duplicación de la transcripción; se conserva tal cual.
- **Corrupción de espaciado extensa** en Samāsa, Taddhita, Ākhyāta, Kibbidhāna y Uṇādi (palabras fusionadas y partidas en medio de línea, p. ej. «gadhi iccetasmā ikapaccayohotītiñāpa naṃtthaṃ»). Demasiado extensa y ambigua para corrección mecánica: corregir capítulo por capítulo en el punto de uso, cuando cada capítulo entre en traducción. Los capítulos 1–3 (Sandhi, Nāma, Kāraka) están notablemente más limpios.
- **Anclas de sutta:** en Sandhi–Kāraka los números `(N)` coinciden con los § del proyecto (verificado: §12, §52, §53, §271, §284). No todos los suttas llevan ancla tipográficamente uniforme (algunos sin negrita o con espacios: `( 570 )`). El **Uṇādi reinicia la numeración** en (1): no usar sus anclas como § sin concordancia.
- **Límite Sandhi/Nāma en esta edición:** §52 *Jinavacanayuttaṃ hi* abre el Nāmakappa aquí (tras el colofón del quinto pariccheda del Sandhi). Cotejar con la división que usa el proyecto antes de citar «capítulo» del Nyāsa.
