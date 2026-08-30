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

**Pero un PDF no se deja como sale, y ésta es la única excepción a la regla
de no tocar nada.** La razón es medible, no estética:

    python3 herramientas/preparar_pdf_corpus_separado.py <archivo.pdf> --medir
    python3 herramientas/preparar_pdf_corpus_separado.py <archivo.pdf> --salida <archivo.txt>

Google Docs exporta **un párrafo por línea** —la mediana del Mahāsatipaṭṭhāna
es una línea de 1.693 caracteres—; `pdftotext` corta por el ancho de la caja,
con una mediana de 93. Y `extraer_junturas_separadas.py` trabaja línea a
línea: una juntura que caiga en un corte de línea desaparece. El guion une
las líneas pāḷi seguidas —el corte de idioma lo decide `es_pali()` importado
del propio extractor— y quita las llamadas de nota que el PDF deja **pegadas
a la voz** («ekam idāhaṃ8»), que el `.txt` de Google trae como «[8]» y el
extractor ya sabía descartar. En el Mahāparinibbāna: 100 llamadas pegadas y
**48 junturas** que sin el re-flujo no se veían.

## Procedencia y licencia

- **Mahāsatipaṭṭhāna-sutta**, versión bilingüe pāḷi-español. Fuente:
  Dīgha-Nikāya ii 231-252. Todas las referencias corresponden a la edición
  del Sexto Concilio. Texto editado y traducido del pāḷi al español por
  Bhikkhu Nandisena; traducción al español editada por Alina Morales
  Troncoso. Copyright © 2013-2025 Buddhismo Theravada México-Hispano AR —
  IEBH. Puede reproducirse para uso personal y distribuirse **sólo de forma
  gratuita**.

- **Mahāparinibbāna-sutta**, versión bilingüe pāḷi-español. Fuente:
  Dīgha-nikāya ii 61. Todas las referencias corresponden a la edición del
  Sexto Concilio. Texto editado y traducido del pāḷi al español por Bhikkhu
  Nandisena; edición por Alina Morales Troncoso. Llegó como PDF de 122
  páginas con capa de texto limpia —cero U+FFFD, NFC, diacríticos
  correctos—, de modo que **no hizo falta OCR**; el `.txt` se preparó con
  `preparar_pdf_corpus_separado.py` (arriba).

- **Therīgāthā-aṭṭhakathā, 23 documentos de capítulo** —Pañcakanipāta
  (versos 67-126, 12 documentos), Chakkanipāta (127-174, 8) y Sattakanipāta
  (175-195, 3)—, con los versos, su vaṇṇanā, la «Lista de voces» y las notas.
  Traducción, análisis y comentario del pāḷi al español por Bhikkhu
  Nandisena. Recogidos del Drive del proyecto el 2026-08-30, en texto sin
  formato, uno por documento y con el nombre que les da el Venerable.

Cada texto que se añada aquí lleva su línea en esta lista, con su fuente y
su licencia. Es material del IEBH: se cita como suyo, y la atribución
pública dice IEBH.

## Dos avisos que salieron de los 23 documentos completos

**Los anclajes de comentario de Google Docs.** El export trae, además de las
llamadas de nota `[1]`, los anclajes de comentario en LETRA: `[a]`, `[b]`,
`[ab]`. En los 23 capítulos son **1.281**, y estorban más que los numéricos
porque caen justo donde interesa —la voz anotada es la que tiene sandhi:
«cittassūpasam[b][c][d][e][f]’ ajjhagaṃ»—. `limpiar()` los quita desde el
2026-08-30; sin eso la juntura se une con basura dentro y no atestigua.

**Las dos MUESTRAS se retiraron.** `therigatha-V-67-71.txt` y
`therigatha-V-72-81.txt` eran recortes a mano de tres de estos documentos,
guardados cuando aún no se tenían enteros. Al llegar los completos
duplicaban texto, y además eran derivados editados a mano de la obra del
Venerable, que es lo que este LEEME desaconseja. Se quitaron, y **se perdió
exactamente una forma atestiguada**: `aṅguliphoṭanamattampi`, frecuencia 1.
Queda dicho para que nadie lo descubra como una merma inexplicada.

## Lo que este corpus NO es

**No adjudica nada.** El corte es del Venerable y vale como tal; los
componentes subyacentes los propone el motor, y donde discrepen es pregunta
para él, no dato que importar. La primera corrida, sobre parte del
Mahāsatipaṭṭhāna, dio 19 junturas —19 atestiguadas, 0 descartadas— y
encontró cuatro formas frecuentes que el motor no veía: panassa (1.731),
caparaṃ (1.548), tamenaṃ (778) y yāvadeva (331).

Con el corpus completo (27 textos, 2026-08-30): **1.180 junturas**, las 1.180
atestiguadas; el motor señala 865 (**73,3 %**) y no ve 315. Y **101
ecuaciones** —16 junturas y 85 ortográficas—, de las que el motor recompone
14 de 16 y **acierta los componentes en 0 de 16**.

Sobre las **4.916 candidatas descartadas**, que asustan al lado de las 78 de
la primera corrida: son casi todas líneas ESPAÑOLAS que se cuelan por
`es_pali()` —«del espejo», «Últimas palabras», «hablan falsedades»—, y las
descarta la exigencia de atestiguación, que es su oficio. Se probó a apretar
el filtro de idioma con «del», «y», «se», «es» y los signos «¿»/«¡»: cae la
basura, pero **también cae pāḷi de verdad** (199 líneas, entre ellas
«Ajjhattaṃ arūpasaññī eko bahiddhā rūpāni passati…»). Medido y descartado:
el resguardo de atestiguación sigue siendo el único filtro seguro.
