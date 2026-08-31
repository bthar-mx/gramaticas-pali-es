# Saddanīti, edición de Helmer Smith — los cinco volúmenes

Traídos de archive.org y guardados aquí el 2026-08-30 (sesión 40), desde la
carpeta de descargas.

## Qué hay y qué no viaja

| archivo | qué es | ¿va al repositorio? |
| --- | --- | --- |
| `saddaniti-smith-NN.pdf` | el escaneo, imagen pura | **no** — `.gitignore` excluye `*.pdf` |
| `saddaniti-smith-NN.paginas.json` | mapa hoja del escaneo → página impresa | **sí** |

Los PDF no viajan, como los demás PDF del repositorio. **Si hacen falta en
otra máquina, se vuelven a bajar de archive.org** con los identificadores
`SaddanitiAggavamsasPaliGrammar01` … `05`. Los `.paginas.json` sí viajan, que
es lo que permite citar por página impresa sin tener el escaneo delante.

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

## Lo que NO se usa, y por qué

**El OCR de archive.org no sirve.** Está medido en el briefing 39 §6: mete
letras cirílicas dentro de palabras pāḷi (`sakammika` → `ѕакаттіка`), pone
diéresis por macrón, confunde `t` con `l` de manera sistemática y pierde los
puntos suscritos. Por eso de cada volumen se guarda **sólo** el `.pdf` liso y
el mapa de páginas; los formatos `_djvu.txt`, `_hocr`, `_chocr` y `_text.pdf`
salen todos de la misma pasada y arrastran los mismos defectos.

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
