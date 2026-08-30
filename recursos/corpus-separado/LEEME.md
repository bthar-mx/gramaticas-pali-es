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

- **Dhammacakkappavattana-sutta**, versión bilingüe pāḷi-español. Puesto el
  2026-08-30.

- **Cinco suttas más**, puestos el 2026-08-30: **Anattalakkhaṇa-sutta**,
  **Pāsarāsi-sutta** (Ariyapariyesana-sutta), **Uppādā-sutta**,
  **Mahā-Taṇhāsaṅkhaya-sutta** y **Sattasūriya-sutta**, este último con su
  Comentario y su Sub-Comentario —la primera vez que el corpus separado
  toca la capa de la Ṭīkā—. Todos editados y traducidos del pāḷi al español
  por Bhikkhu Nandisena.

- **Ānāpānassati**, las tres versiones, puestas el 2026-08-30: el **sutta**
  (M. iii 123-130), la **Kathā del Paṭisambhidāmagga** (Ps. 161-198) y la
  **Kathā de la Visuddhimagga** (Vis. i 258-284). Esta última no es canon
  sino tratado, y además trae notas del traductor en inglés: es la que
  obligó a escribir `basura()` (más abajo).

- **Cuatro más**, el 2026-08-30: **Brahmajāla-sutta**, **Cūḷavedalla-sutta**,
  **Dutiyasaddhammasammosa-sutta** y **Pañhabyākaraṇa-sutta** (A. i 355).
  El Brahmajāla aporta 98 junturas él solo; el Pañhabyākaraṇa, por su
  tamaño, ninguna nueva — y eso también es un dato: el corpus empieza a
  saturarse en los textos cortos.

- **Aggañña-sutta** y **Mālukyaputta-sutta** (con su Comentario y su
  Sub-Comentario), puestos el 2026-08-30. Entre los dos aportan 126
  junturas, y de las más frecuentes de todo el corpus: ceva (8.526),
  evameva (3.475), neva (3.404), etadavoca (3.273), yadidaṃ (1.718).

- **Ādittapariyāya-sutta**, el 2026-08-30: traducido del pāḷi al español por
  **Rutty Bessoudo Salvo** y **revisado por Bhikkhu Nandisena**. La
  traducción es de otra mano, pero la revisión es suya, de modo que el corte
  entra en el corpus con la misma autoridad que el resto. Se anota la
  traductora porque el crédito es suyo y porque este corpus se apoya
  precisamente en de quién es el corte: aquí son dos manos, y las dos se
  nombran. Aporta 12 junturas.

- **Cūḷanikā-sutta**, **Kappa-sutta** (con Comentario), **Lokapañha-sutta**
  y **Moneyya-sutta** (con Comentario), el 2026-08-30. Cuatro textos breves
  que aportan 23 junturas entre los cuatro — pocas, y esperable: el corpus
  está saturado para el sutta corto—. Valen por lo que traen, no por
  cuántas: hevaṃ (2.663), vuttanayeneva (1.908), ayamettha (955).

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

Con el corpus al cierre del 2026-08-30 (**47 textos**): **1.784 junturas**,
las 1.784 atestiguadas; el motor señala 1.270 (**71,2 %**). Y **101
ecuaciones** —16 junturas y 85 ortográficas—, de las que el motor recompone
14 de 16 y **acierta los componentes en 0 de 16**.

Y el cotejo del corte del Venerable contra la lectura del motor da **un solo
fallo con muchas caras**: el motor reconstruye la primera voz con la vocal
final equivocada cuando esa vocal se pierde en el sandhi, y casi siempre la
pone en «-a» —hissa «hi»→«ha» (501), tissa «ti»→«ta» (265), yāyaṃ
«yā»→«ya» (265), tayome «tayo»→«taya» (139), yohaṃ, yadāhaṃ, tatohaṃ—. Son
**39 formas, masa 1.562**, con dos sub-clases: los nominativos en «-o» ante
«si», «ahaṃ» y «va» leídos como temas en «-a» (katapuññosi, jātosi,
paviṭṭhohaṃ), y los femeninos en «-ī» leídos breves (lābhinī, vasantī).

**Cuidado al contarlo**: otras **24** lo parecen y no lo son —natthīti,
passāmīti, bhikkhūti—, porque ahí el IEBH imprime la vocal alargada ante
«ti» (§18) y el motor da la breve subyacente, que es lo correcto. El corte
es de superficie y la lectura es de fondo; confundirlos fabrica fallos que
no existen.

## El inglés entró en el corpus, y la atestiguación no lo paraba

`es_pali()` sabe descartar el ESPAÑOL y nada más. El Ānāpānassati de la
Visuddhimagga trae notas del traductor **en inglés**, y en inglés casi toda
palabra acaba en consonante: cada espacio parece una juntura. Así se
publicaron **«it | I» → *iti* (8.058)**, «at | the» → *atthe* (1.393) y
«can | do» → *cando* (299), más las siglas de referencia «M.A.», «T.A.»,
«D.A.». La atestiguación no las atrapa: la forma unida existe en la edición
por pura coincidencia. La de *atthe* venía desde la primera corrida.

`basura()` las criba desde el 2026-08-30, con tres reglas **de PAR, no de
línea**, y ahí está el punto: filtrar la LÍNEA por palabras inglesas se
probó y quitaba junturas de verdad —idheva (876), sabbeva (512),
yannūnāhaṃ (242)—, porque estos documentos mezclan pāḷi e inglés en el
mismo renglón. Mirando el par no se pierde ninguna.

    (1) una mitad sin letras          «– | ’tiṇṇo»
    (2) las dos de una sola letra     «M | A», de «M.A. ii 94»
    (3) las dos son palabras inglesas «at | the», «can | do»

Medido sobre los 40 textos: retira **19 candidatas atestiguadas, y las 19
son basura**; no añade ninguna. Queda un artefacto conocido sin cribar:
«ana» (11), de la notación morfológica «’a’ - ’na’» de una «Lista de
voces».

Sobre las **4.916 candidatas descartadas**, que asustan al lado de las 78 de
la primera corrida: son casi todas líneas ESPAÑOLAS que se cuelan por
`es_pali()` —«del espejo», «Últimas palabras», «hablan falsedades»—, y las
descarta la exigencia de atestiguación, que es su oficio. Se probó a apretar
el filtro de idioma con «del», «y», «se», «es» y los signos «¿»/«¡»: cae la
basura, pero **también cae pāḷi de verdad** (199 líneas, entre ellas
«Ajjhattaṃ arūpasaññī eko bahiddhā rūpāni passati…»). Medido y descartado:
el resguardo de atestiguación sigue siendo el único filtro seguro.
