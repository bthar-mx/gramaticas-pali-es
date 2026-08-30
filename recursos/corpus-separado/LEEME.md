# Textos con las junturas separadas — de dónde salen y qué son

Aquí van los textos bilingües del **Instituto de Estudios Buddhistas Hispano
(IEBH)**, editados y traducidos del pāḷi al español por **Bhikkhu
Nandisena**. Imprimen el pāḷi con las junturas de sandhi **abiertas** —«Evam
eva», «yad idaṃ», «Puna c’ aparaṃ», «sato ’va»— donde la edición del Sexto
Concilio las imprime unidas: evameva, yadidaṃ, caparaṃ, satova.

Cada uno de esos espacios es **una juntura etiquetada a mano por el
Venerable**, y eso es justamente lo que al proyecto le faltaba. CLAUDE.md lo
dice sin rodeos: «el cuello de botella es la segmentación, no las reglas —
sin saber que lokaggo es loka + aggo no hay motor de reglas que valga».

## Cómo se usan

    python3 herramientas/extraer_junturas_separadas.py
    python3 herramientas/extraer_junturas_separadas.py --ver-fallos

El guion lee **todos los `.txt` de esta carpeta** (este LEEME es `.md` a
propósito, para que no lo lea), saca las junturas, las une y publica sólo
las que **están atestiguadas en la edición del Sexto Concilio**. Lo que no
está atestiguado no se inventa: se aparta y `--ver-fallos` lo enseña.

Salida: `junturas.json`, en esta misma carpeta.

## Qué hay que hacer con un archivo nuevo: nada

Se deja el `.txt` tal como lo exporta Google Docs («Archivo → Descargar →
Texto sin formato»). El guion descarta solo las líneas españolas, la
portada, los números de página `[232]`, las llamadas de nota y las marcas de
repetición `-pa-`. **No hace falta limpiarlo a mano**, y es mejor no
hacerlo: cuanto menos se toque el documento del Venerable, menos ocasiones
de estropear un diacrítico.

Exportar en **texto sin formato**, no en Markdown: el Markdown de Google
escapa caracteres —`[232]` sale como `\[232\]`— y no aporta nada que este
guion use.

## Y si lo que llega es un PDF

El PDF va **en esta misma carpeta** y se queda quieto: el extractor sólo lee
`.txt`, y `*.pdf` está en `.gitignore`, de modo que no viaja con el
repositorio —como los PDF del Saddanīti y del Abhidhāna—.

**Antes de extraer nada, se diagnostica una página.** Es la regla que este
proyecto aprendió a las malas: el PDF de U Sīlānanda no tenía capa de texto
utilizable —477 subconjuntos tipográficos y el `/ToUnicode` roto— y hubo que
escribir un extractor por el contorno de cada glifo. Si la capa de texto
está limpia, `pdftotext` deja el `.txt` al lado y el extractor lo toma en la
siguiente corrida; si es un escaneo, se dice ANTES de gastar esfuerzo en
OCR, que sobre pāḷi romanizado con diacríticos completos es justamente el
trabajo del que hay que desconfiar.

## Procedencia y licencia

- **Mahāsatipaṭṭhāna-sutta**, versión bilingüe pāḷi-español. Fuente:
  Dīgha-Nikāya ii 231-252. Todas las referencias corresponden a la edición
  del Sexto Concilio. Texto editado y traducido del pāḷi al español por
  Bhikkhu Nandisena; traducción al español editada por Alina Morales
  Troncoso. Copyright © 2013-2025 Buddhismo Theravada México-Hispano AR —
  IEBH. Puede reproducirse para uso personal y distribuirse **sólo de forma
  gratuita**.

Cada texto que se añada aquí lleva su línea en esta lista, con su fuente y
su licencia. Es material del IEBH: se cita como suyo, y la atribución
pública dice IEBH.

## Lo que este corpus NO es

**No adjudica nada.** El corte es del Venerable y vale como tal; los
componentes subyacentes los propone el motor, y donde discrepen es pregunta
para él, no dato que importar. La primera corrida, sobre parte del
Mahāsatipaṭṭhāna, dio 19 junturas —19 atestiguadas, 0 descartadas— y
encontró cuatro formas frecuentes que el motor no veía: panassa (1.731),
caparaṃ (1.548), tamenaṃ (778) y yāvadeva (331).
