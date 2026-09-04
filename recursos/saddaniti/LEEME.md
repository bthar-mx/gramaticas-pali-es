# Saddanīti, edición de Helmer Smith — los cinco volúmenes

Traídos de archive.org y guardados aquí el 2026-08-30 (sesión 40), desde la
carpeta de descargas.

## Qué hay y qué no viaja

| archivo | qué es | ¿va al repositorio? |
| --- | --- | --- |
| `saddaniti-smith-NN.pdf` | el escaneo, imagen pura | **no** — `.gitignore` excluye `*.pdf` |
| `saddaniti-smith-NN.paginas.json` | mapa hoja del escaneo → página impresa | **sí** |
| `conspectus-ejemplar-angel.pdf` | el Conspectus fotografiado del ejemplar de Angel | **no** — y esto es un problema, ver abajo |

Los PDF no viajan, como los demás PDF del repositorio. **Si hacen falta en
otra máquina, se vuelven a bajar de archive.org** con los identificadores
`SaddanitiAggavamsasPaliGrammar01` … `05`. Los `.paginas.json` sí viajan, que
es lo que permite citar por página impresa sin tener el escaneo delante.

## EL CONSPECTUS DEL EJEMPLAR DE ANGEL (sesión 50)

`conspectus-ejemplar-angel.pdf`, 44 páginas, las **1105-1148** completas, una
por fotograma y en orden, hechas con un iPhone el 2026-09-04. Es la sección E
del vol. IV, el Conspectus gramatical entero; se corta justo donde empieza el
métrico (sección 8).

**Es mejor que el escaneo de archive.org, y no por resolución sino por
procedencia.** Medido: el interlineado da 74 px, contra 72-76 px del
`saddaniti-smith-04.pdf` a 400 dpi — es decir, muestreo equivalente. Lo que
cambia es que aquélla es la reproducción de una reproducción y ésta es la
tinta. Los subíndices de línea, que a 400 dpi son cuatro manchas grises de
diez píxeles, aquí se leen. Y las cantidades vocálicas también: en la p. 1124
el punto de la i de `pariccheda` y la barra de la i de `vīcchā` se distinguen
en la misma línea.

**PERO NO VIAJA, y a diferencia de los otros no se puede volver a bajar de
ninguna parte**: sale del ejemplar de Angel. `.gitignore` excluye `*.pdf` y
esa línea no se ha tocado —es decisión suya si quiere una excepción para este
archivo—. Mientras tanto, existe sólo en su disco.

    # una página cualquiera, a resolución nativa (la 1135 es la hoja 31)
    pdfimages -j -f 31 -l 31 recursos/saddaniti/conspectus-ejemplar-angel.pdf /tmp/p

**Hoja del PDF = página impresa − 1104.** No hace falta `pagina_saddaniti.py`
para éste; ese guion es para los cinco volúmenes de archive.org.

## La paginación corre continua por los cinco volúmenes

| vol. | páginas del PDF | páginas impresas |
| ---: | ---: | --- |
| 01 | 334 | 2 – 314 |
| 02 | 297 | 316 – 602 |
| 03 | 340 | 604 – 928 |
| 04 | 264 | 930 – 1172 |
| 05 | 314 | 1174 – 1460 |

**Página impresa a página de PDF:** el `.paginas.json` trae `pages[]`, cada
entrada con `leafNum` (base 0) y `pageNumber` (la impresa, cadena vacía en el
material preliminar). La página que pide `pdftoppm` es `leafNum + 1`.

Comprobado contra el dato conocido de la sesión 39: la pág. impresa 617 es la
24 del PDF del vol. 03. Lo es.

En el vol. 03: `impresa = pdf + 593`, mientras no haya láminas intercaladas —
pero **conviene leer el mapa y no fiarse de la resta**, que es justamente para
lo que está el archivo.

## HAY DOS DIGITALIZACIONES EN ARCHIVE.ORG, NO UNA (sesión 41)

Lo comprobado el 2026-08-31, y cambia lo que decía este archivo:

| familia | identificadores | subida | OCR |
| --- | --- | --- | --- |
| la que tenemos | `SaddanitiAggavamsasPaliGrammar01`…`05` | 2016 | **tesseract** |
| la del ASI | `in.gov.ignca.2699`…`2703` | 2017 | **ABBYY FineReader 11** |

**Los PDF de este repositorio son de la primera**: el md5 del vol. 03,
`56034d3c734277ab6062385719d80ee5`, es exactamente el del original de
`SaddanitiAggavamsasPaliGrammar03`.

**Las dos vienen del mismo escaneo físico** —el ejemplar de la Central
Archaeological Library de Nueva Delhi; nuestro vol. 03 lleva estampado su
número de acceso, 2701, que es justo el identificador ASI del vol. 3—, de modo
que **la imagen es la misma y no hay una versión mejor escondida**. Lo que
cambia entre las dos familias es **sólo el OCR**.

Correspondencia: 2699 = vol. 1 (1928), 2700 = vol. 2, **2701 = vol. 3 (1930)**,
2702 = vol. 4, 2703 = vol. 5.

## La resolución es el techo, y es bajo

Cada página es **un solo JPEG de unos 545 × 874 píxeles**, sin capa de texto
(comprobado con `pdfimages -list` y `pdftotext` en los cinco volúmenes). El
`_jp2.zip` de archive.org —295 MB— **es derivado del PDF**, no un maestro: no
contiene ni un píxel más. La ficha del ítem dice `ppi: 600` y **es falso**.

A ~8 píxeles por carácter **no hay OCR que distinga `ṭ` de `t` ni `ā` de `a`**.
El fallo no es de motor: es de píxeles. Se lee a ojo ampliando ×3 o ×10 con
LANCZOS —así se hizo el capítulo XX entero—, pero no se transcribe a máquina.

## Por qué el OCR de cada familia falla, y en qué se distinguen

**La nuestra (tesseract).** La ficha del ítem lo explica del todo:

    ocr_parameters: -l kir+que+Latin+Cyrillic+Arabic
    ocr_detected_lang: ky          ocr_invalid_language: pli

archive.org **rechazó «pli» como idioma**, dedujo que el libro era **kirguís** y
pasó tesseract con modelos cirílico y árabe. De ahí `sakammika` → `ѕакаттіка`:
literalmente estaba leyendo con un modelo cirílico. El briefing 39 §6 lo midió
bien; la causa queda ahora nombrada.

**La del ASI (ABBYY).** No mete cirílico —falla en latín—, pero **pierde todos
los diacríticos** y descuaja los grupos de letras:

    ABBYY:  «bindu niggahitam naraa ti duubabbaip»
    debe decir: «bindu niggahītaṃ nāma ti daṭṭhabbaṃ»

**Tampoco sirve como texto.** Pero sirve para otra cosa, y no es poco:

## El ABBYY SÍ alcanza el aparato, y sirve de segundo testigo

Donde tesseract no dejó nada legible, ABBYY deja las marcas de concordancia
reconocibles a pesar del destrozo, **y corroboran por su cuenta las correcciones
de la sesión 41**:

    ABBYY: «§ J7-IH Kcv Rap n L-e B*-*»        → § 17-18 Kcv 9, Rūp 11
    ABBYY: «§ 72 Ktv 20 = Sop 27 C<^ 11* ("ca")» → § 72 Kcv 20 = Rūp 27 ("ca")
    ABBYY: «§ 73—83 Kcv 20»                     → § 73—85 Kcv 20

Es decir: **una fuente independiente lee «Kcv» donde la sesión 40 había leído
«Kc»**, en los tres sitios que la 41 corrigió a ojo. No adjudica —sigue
adjudicando el ojo— pero es el segundo testimonio que faltaba.

**Y donde discrepa, pierde.** Da «73—83» y el impreso dice **85**: comprobado
sobre la imagen nativa ampliada ×10, el dígito tiene la barra plana y el cuenco
abierto de un 5. Da «23-36» donde el impreso dice **25-26**. De modo que la
regla de siempre: **el OCR genera y el ojo adjudica**, y ahora con dos
generadores en vez de uno.

## Lo que NO se usa, y por qué

De cada volumen se guarda **sólo** el `.pdf` liso y el mapa de páginas. Los
formatos `_djvu.txt`, `_hocr`, `_chocr`, `_abbyy.gz` y `_text.pdf` **no se
incorporan como texto** por lo dicho arriba: ninguna de las dos pasadas produce
pāḷi utilizable. El `_text.pdf` de nuestra familia viene además marcado
`pdf_degraded: invalid-jp2-headers`.

**Sí vale la pena conservar el `2701_djvu.txt` del ASI como GENERADOR de
candidatos del aparato**, que es lo que se acaba de demostrar. No está en el
repositorio; se baja del ítem cuando haga falta.

Sí sirve, y es distinto, pasar tesseract por la **franja del aparato** para
buscar cadenas latinas y numéricas como «§ 50 Kc 20». El pāḷi sale mal; la
concordancia sale. Y aun así genera candidatos, no los adjudica: véase
`docs/solucionador/saddaniti-lo-que-kaccayana-no-tiene.md` §2.

## Cómo se lee una página

    pdftoppm -r 150 -f 24 -l 24 -png recursos/saddaniti/saddaniti-smith-03.pdf pag

El escaneo es excelente y a 150 dpi se lee cómodo. Para el aparato al pie,
recortando y a más resolución:

    pdftoppm -r 300 -f 24 -l 24 -x 0 -y 1850 -W 1700 -H 820 -png <vol> aparato

## Procedencia y permiso

Edición de **Helmer Smith** (Saddanīti, la gramática pāḷi de Aggavaṃsa),
publicada por Gleerup, Lund, 1928-1966, en tres partes que aquí vienen en
cinco volúmenes de escaneo. La introducción de Smith está en **francés**.

La edición está fuera de derechos por antigüedad en la mayoría de
jurisdicciones, pero **eso no se ha comprobado formalmente**; antes de
redistribuir los escaneos hay que verificarlo. Consultarlos y citarlos, sí.

<!-- DUDA: la copia de junio que estaba en descargas con el nombre
     «…Suttamālā.pdf» es, por md5, el mismo archivo que el vol. 03
     (56034d3c734277ab6062385719d80ee5). Se dejó donde estaba; si se quiere,
     se borra, pero borrar archivos de Angel no me toca decidirlo. -->
