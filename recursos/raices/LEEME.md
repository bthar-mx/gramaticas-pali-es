# Dhātvatthasaṅgaha con su nissaya — el escaneo de la KBRL

Bajado de la biblioteca electrónica del Ministerio de Asuntos Religiosos de
Myanmar (KBRL / DPPS e-Library) y guardado aquí el 2026-10-10.

## Qué hay y qué no viaja

| archivo | qué es | ¿va al repositorio? |
| --- | --- | --- |
| `dhatvatthasangaha-nissaya.pdf` | el escaneo, imagen pura, 567 páginas | **no** — `.gitignore` excluye `*.pdf` |

El PDF no viaja, como los demás PDF del repositorio. **Si hace falta en otra
máquina, se vuelve a bajar de la KBRL**, ítem `001288`:

- ficha: <http://www.kbrl.gov.mm/book/details/001288?categoryId=54>
- descarga: <https://www.kbrl.gov.mm/old/book/download/001288>

md5 de la copia de aquí: `94ac160678dcd90be6fcb93b75895ca4`.

Hay una segunda copia en la lista «Shwegyin» de New Masoeyein e-library
(n.º 20, alojada en MediaFire,
<https://msy-elibrary.blogspot.com/2020/12/blog-post_31.html>). No se ha
comprobado si es el mismo archivo.

## La obra

**ဓာတွတ္ထသင်္ဂဟပါဌ်နိဿယ** (*Dhātvatthasaṅgahapāṭh-nissaya*), del
**Mahāvisuddhārāma Sayadaw**, Bhaddanta Visuddhācāra, segundo
Thathanabaing de la Shwegyin Nikāya (1894–1916). La portada le da los
títulos ဝိသုဒ္ဓါစာရ ကဝိဓဇ … မဟာဓမ္မရာဇဂုရု, အဂ္ဂမဟာပဏ္ဍိတ y
ရွှေကျင်နိကာယ ဓမ္မသေနာပတိ.

Esta impresión es la de portada verde: la portada trae un número de impresión
(ဆဋ္ဌအကြိမ်) y dos fechas al pie. Según la portada, añade un índice
alfabético de las palabras que conviene memorizar
(မှတ်သားဖွယ်ရာ ပုဒ်တို့၏အစဉ် အက္ခရာဝလိ). La reimpresión la costearon
donantes encabezados por Bhaddanta Nandavaṃsābhivaṃsa (Hinthada).

**Las dos fechas del pie de la portada** (hoja 1; repetidas en la portadilla,
hoja 4) son **၁၃၆၉** y **၂၀၀၈**: año birmano 1369 y año 2008 de la era común
(el 1369 birmano va de abril de 2007 a abril de 2008, de modo que las dos
cuadran). Leído en la imagen en la sesión 64; seguridad alta, no total: en la
portada el escaneo es gris y la tinta está gastada.

El IEBH tiene en papel **otra impresión** (portada amarilla, librería
မိဘဂုဏ်ရောင် ပိဋကတ်စာအုပ်ဆိုင်, U Lu Maung y Daw Mi Mi, Zegyo, Mandalay,
impresa con permiso del grupo ဂဏဝါစက de Visuddhāyuṃ), que encuaderna con
el Dhātvatthasaṅgaha otras obras breves (ကစ္စည်းပကာသအကောက်,
နေတ္တိဟာရတ္ထဒီပနီသစ်, …). Sirve de segundo testigo. Su portada dice
**သတ္တမအကြိမ်**: es la **séptima** impresión, posterior a la del escaneo
(sexta). **No pagina como la sexta** (comprobado en la sesión 65 con 22
páginas fotografiadas por el IEBH): está recompuesta, con otra caja, y lleva
el número de cada verso como encabezado («(၂၈၄)»). Lo que en la sexta son las
pp. 262-263 es en la séptima pp. 201-203. Una página de la séptima, por tanto,
no se cita como si fuera de la sexta.

## Cómo está hecho el libro

Visto hoja por hoja en la sesión 64 (hojas del PDF; páginas, las impresas):

| hojas | páginas | qué es |
| --- | --- | --- |
| 1 | — | cubierta (verde) |
| 2-15 | [က]…, sin cifras | preliminares: dedicatoria, portadillas, registro del dhammadāna (ဓမ္မဒါနမှတ်တမ်း), **mātikā** (hojas 10-11), nidāna |
| 16-60 | 1-45 | **el pāḷi solo**, en ocho kaṇḍas: 1 paṇāma y vocales (p. 1), 2 *k-* (5), 3 *kh-* y las tres letras siguientes (8), 4 ca- y ṭa-vagga (12), 5 ta-vagga (16), 6 pa-vagga (23), 7 a-vagga, *y-* a *ḷ-* (32), 8 nigamana (44) |
| 61-407 | 47-395 | **el nissaya**: 1 paṇāma y vocales (p. 47), 2 *k-* (79), 3 *kh-* (104), 4 *g-* (115), 5 *c-* (131), 6 *t-* (160), 7 *p-* (211), 8 a-vagga (278) |
| 408-415 | 396-403 | lista de donantes (ဓမ္မဒါန အလှူရှင်စာရင်း) |
| 416-564 | 404-552 | **índice alfabético** (အက္ခရာဝလိ): palabra → página, a dos columnas |
| 565 | 553 | colofón |
| 566-567 | — | contracubierta |

Las páginas de comienzo de cada parte son las de la **mātikā** (hojas 10-11),
y cuadran con el mapa de páginas en todas las que se han cotejado (47, 79,
104, 396, 405). Las del pāḷi están vistas en la imagen de la hoja 10; las del nissaya
(hoja 11), leídas por OCR y vistas las cinco primeras.

- **El verso.** Numeración corrida (၃၈။ …), y al final de cada verso **el
  número de raíces que contiene** (… ၇ ။ = siete raíces). Cada raíz va en
  nominativo (*kako, kaki*) seguida de su sentido en locativo y, a menudo,
  de la marca de gaṇa: ဘူ (bhūvādi), စု (curādi), ဒိ (divādi), …
- **La entrada del nissaya.** El verso se repite y luego viene una entrada por
  raíz: la raíz **en negrita al margen**, su sentido en birmano palabra por
  palabra y, entre corchetes, formas conjugadas, derivados y citas
  (Moggallāna, Dhātumañjūsā, Kavikappadduma, …).
- El **titulillo** de las páginas del nissaya da además la primera y la
  última raíz de la página (*အက ----- အင်္ဂ*), como un diccionario.

## El escaneo

Cada página es **una imagen bitonal JBIG2 de unos 2400 × 3400 píxeles**
(la portada, JPEG en color), **sin capa de texto** (comprobado con
`pdfimages -list` y `pdftotext`). El PDF lo hizo Acrobat 11 y lo comprimió
«Advanced PDF Compressor» el 2015-09-02. La resolución es buena: muy por
encima del techo de los escaneos del Saddanīti.

### El mapa de páginas: `dhatvatthasangaha-nissaya.paginas.json`

**Para citar una página, se mira ahí; la resta no vale.** El desfase hoja −
página no es constante:

| hojas | desfase | por qué cambia |
| --- | ---: | --- |
| 16-60 | 15 | — |
| 61-275 | 14 | **falta la p. 46** (entre el fin del pāḷi y la portadilla del nissaya; casi seguro un verso en blanco) |
| 276-565 | 12 | **faltan las pp. 262-263** (la 261 acaba en la entrada *မဒေါ*; la 264 abre con el verso ၂၈၆) |

Las pp. 262-263 caen en las raíces en *m-* del kaṇḍa de *p-* (ma es de la
pa-vagga): **su contenido no está en este escaneo**. Se ha leído en el
ejemplar en papel del IEBH (séptima impresión, pp. 201-203, fotos de la
sesión 65): versos ၂၈၃-၂၈၅ con **diez raíces**, *madi, maddo, madhu, mano,
mabbo, mabbho, mayo, maro, malo, mallo*. Con ellas el kaṇḍa 6 da los 316 del
libro. La p. 46, en cambio, no esconde texto: el pāḷi acaba en la 45 y el
nissaya empieza en la 47 sin que falte ningún verso; es un hueco de la
compaginación, no del contenido.

El mapa lo hace `herramientas/dhatvatthasangaha/paginar.py`: lee el
titulillo de cada hoja con OCR, saca el número y vota el desfase. 368 hojas se
leen directamente; 178 se interpolan **sólo** entre dos lecturas del mismo
desfase; 4 se han visto en la imagen (16, 61, 62, 565); 17 no llevan número
(cubiertas y preliminares). Formato como el de los `.paginas.json` del
Saddanīti (`leafNum` desde 0), con `fuente` por página y los `huecos` con su
nota.

    # una página cualquiera, a resolución nativa
    pdfimages -f 200 -l 200 -png recursos/raices/dhatvatthasangaha-nissaya.pdf /tmp/p

### Imágenes y OCR

Fuera del repositorio, como las del Visuddhāyuṃ, en
`~/Tipitaka/nissaya/ocr/dhatvatthasangaha-nissaya/` (`img/NNN.png`, NNN = hoja
del PDF). Piloto de OCR: `docs/dhatvatthasangaha/piloto-ocr.md` — con el
modelo `myap` renglón a renglón, **CER 4,9 % en versos y 3,0 % en nissaya**.
Corrida completa (hojas 16-407) y extracción: §5 de ese documento. **El libro
declara 1.637 raíces** (renglones de cierre de cada kaṇḍa: 277 en los dos
primeros, 159, 177, 266, 316 y 442) y **445 versos**.

**Verificación en la imagen (sesión 65): las 1.637, kaṇḍa por kaṇḍa.**
1.625 renglones de entrada vistos uno a uno en la imagen (varios valen por dos
o tres raíces unidas con ’); 22 que el extractor no había reconocido; las diez
de las pp. 262-263, de la séptima impresión. Quedan **18 lecturas dudosas**,
16 de ellas ယ/ဃ: en la negrita del margen las dos letras tienen la misma
forma, y lo decide el IEBH en el papel. Tabla y datos, en local:
`docs/fuentes/dhatvatthasangaha/verificacion.md` y `.json`.

### Qué se publica (decisión del IEBH, 2026-10-10)

- En el sitio: **la raíz, su sentido y la referencia** (verso, página).
- **En local, no se publica**: el texto del nissaya, con sus notas.
  `docs/fuentes/dhatvatthasangaha/` está en `.gitignore`, bajo «Fuentes no
  publicadas».
- La romanización, la de CST/OSBCT (`herramientas/nyasappadipika/my2rom.py`).
- El sentido va **en birmano** por ahora; el español, en una pasada aparte que
  firma el IEBH.

### Publicado: la quinta pestaña (sesión 66, 2026-10-10, v1.7 de la página)

`recursos/raices/dhatvatthasangaha.json` (1.625 entradas, 1.637 raíces), que
`generar_raices.py` carga como `datos.dhatvattha` y cruza con el Saddanīti por
lema (`concordar_dv`: la forma de cita del margen con -o/-ā final se compara
también con -a). Cada entrada: `raiz_my` (el margen), `raiz` y `nombres`
(romanización CST), `n` y `cuantas` (el número de raíz del libro), `kanda`,
`pagina` e `impresion` (6 o 7), `estado` (`V` / `?`, con `duda`), `sentidos`
(`pali_my`, `pali`, `my`), `sentido_estado` y `sentido_duda`, `con` (cuando el
libro da el sentido con la raíz siguiente: «သည်၎င်း»).

**El sentido está cotejado con la imagen** (sesión 66): 1.566 entradas vistas
`V`, 49 `?` con su motivo, y las diez de la séptima impresión `sin-imagen`. El
registro de cada corrección (809 entradas corregidas desde la imagen) está
fuera del repositorio, en `~/Tipitaka/nissaya/ocr/dhatvatthasangaha-nissaya/_work/sesion66/cotejo-sentidos.py`.
Comprobación independiente: el primer sentido pāḷi aparece en el verso en
1.325 de 1.528 entradas (87 %).

**Traducción** (sesión 66): `generar_raices.py` (`traducir_dv`) pone a cada
sentido el español de Nandisena y el inglés de su edición cuando el pāḷi
coincide con una glosa del Saddanīti (rótulo «Sad»); si no, la glosa birmana
frase por frase con `dhatvatthasangaha-glosas.json`, **sólo cuando el IEBH lo
haya firmado** (`"adjudicado": true`). Lo que se añada al glosario después de
la firma entra bajo una firma que no lo ha visto, y eso se le dice al IEBH.

**No se publica todavía el número de verso**: la asignación del extractor está
corrida en algunos versos (briefing 65, §3). La referencia publicada es la
página.

## Procedencia y permiso

Publicación difundida por un ministerio de Myanmar, en descarga libre.
**Los derechos de redistribución no se han comprobado.** Consultarla y
citarla, sí. Publicar en el sitio la raíz, su sentido y la referencia parece
razonable; publicar el texto del nissaya entero queda **pendiente de
decisión**, como las demás «fuentes no publicadas» del `.gitignore`.
