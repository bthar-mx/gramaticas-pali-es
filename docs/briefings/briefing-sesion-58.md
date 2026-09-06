# Briefing de la sesión 58 — LOS 67 TÉRMINOS DE LA COSECHA ENTRAN EN LA NORMA, CON SUS SUTTAS

**Fecha:** 2026-09-05. Tres cosas: **los lemas sueltos del texto de Nandisena
enlazan a su ficha**; **los veredictos del IEBH sobre la cosecha de la sesión
57** (67 aceptados, 70 rechazados —los sufijos, todos—) están incorporados a
`comun/glosario.md` y publicados en el glosario; y cada término nuevo lleva
**las referencias por sutta** a Kaccāyana, Rūpasiddhi y Nyāsa, buscadas en
el texto y no propuestas de memoria.

Este briefing supone leídos los de las sesiones 46 a 57. Sigue pendiente
todo lo del briefing 57 §3 bis (tanda 2 del inglés; puntos 17-34 de la
revisión).

---

## 1. Los lemas sueltos enlazan (`plantilla.html`, `enlazaGlosa()`)

Pedido del IEBH: «…en oposición al sandhi interno, **vaṇṇa-sandhi**» tiene
que llevar a la ficha de vaṇṇa-sandhi aunque no lo preceda ningún «V.». Se
hace con estas cautelas, y todas están en el comentario del código:

- la voz existe como lema (IDX); lleva diacrítico o guion, o tiene cuatro
  letras o más («a», «no», «ca», «na», «hi», «tu», «iti» quedan fuera);
- no está entre comillas (lo entrecomillado son ejemplos citados);
- no empieza por mayúscula (Dhamma, Aṭṭhakathā) ni está en `NO_SUELTO`
  (dhamma, buddha, āharati, tiṭṭhati, pavattati);
- no es el propio lema de la ficha; y sólo la **primera** mención de cada
  destino por glosa.
- El guion admite el espacio del impreso («vaṇṇa- sandhi»).

Resultado, medido con jsdom: enlaces en la capa de Nandisena **456 → 637**
(243 → 324 fichas), 0 sin destino, 0 errores. Las notas siguen sin enlazar.

## 2. Los veredictos de la cosecha

`docs/glosario/veredictos-terminos-faltantes.json` (IEBH, 2026-09-05):
**67 acepta** (63 términos + 4 designaciones), **70 rechaza** (los 70
sufijos: el IEBH los dejará para más adelante «de otra manera»). Un término
rechazado; ṇāpaya entra porque la cosecha lo tipó como término y el IEBH lo
aceptó.

`incorporar_terminos_faltantes.py` los puso al final de la tabla de
`comun/glosario.md` (filas 62-128) y en `glosario-ingles.json`. Dos
retoques a mano después:

- **gha, jha, la → `gha-saññā`, `jha-saññā`, `la-saññā`**, que es lo que el
  IEBH escribió en la nota del veredicto; la nota de la fila recupera el
  comentario de la cosecha y lo dice. `ga` fue también **`ga-saññā`**, por
  coherencia, tras preguntarlo el IEBH al buscar «gasaññā».
- **El buscador casa el lema sin guiones ni espacios** (`compacta()`):
  «gasañña» encuentra `ga-saññā`, «vannasandhi» encuentra `vaṇṇa-sandhi`.
- Los ES del IEBH donde los escribió; el propuesto donde no.

Cifras: normativos **53 → 120**; lemas de la vista alfabética **1.984 →
2.049**; 0 errores de consola; pestaña Normativos, 120 fichas.

## 3. Las referencias por sutta (`herramientas/referenciar_terminos.py`)

Nuevo. Parte en suttas lo que el repositorio tiene de las tres obras y
busca el tema:

| obra | de dónde | suttas |
| --- | --- | ---: |
| Kacc. | `kaccayana/01-03`, `docs/borradores/capitulo-04-…`, `docs/5-8 … Kaccāyana.md` | 672 (falta §271) |
| Rū. | `docs/5-7 … Rūpasiddhi.md` (sólo esos tres capítulos están) | 323 |
| Nyāsa | `docs/fuentes/nyasa/Nyasa-01…08` | 555 (huecos del OCR en Taddhita) |

Reglas: se busca el tema **sin la vocal final** (aṅgavikāra casa con
aṅgavikāro) como subcadena en el bloque entero del sutta, sin guiones ni
apóstrofos («pura-sadd’-ūpapade»); las notas al pie vuelven al sutta que
las cita; lo anterior al primer sutta se rotula «(introducción)» —así
sale `kriyālakkhaṇa`, que sólo está en el proemio de la Rūpasiddhi—. Las
designaciones y los temas de menos de cinco letras sólo se buscan como
palabra entera **en la línea del aforismo**, con la vocal final libre
(«gha» casa con «gho» de §60 «Ā gho», y con «gasañño»).

Van en la celda «Fijado en», tras una raya: `cosecha s. 57, IEBH
2026-09-05 — Kacc. §291 · Nyāsa §286, §291`. `generar_glosario.py` las
separa en `refs` y la ficha las enseña en gris tras el sentido, como las
«Sad. ii 78» de Nandisena. Seis suttas por obra y «(y N más)».

**Lo que hay que saber al leerlas:**

- **Ninguna se quedó sin sutta**, pero cuatro son de mirar: las de las
  designaciones (gha, jha, la, ga) salen del aforismo por palabra entera y
  traen ruido (la §35, gha §118…); el IEBH decide cuáles quedan.
- **`saddūpapada` en Kaccāyana sólo está en una nota al pie de §670**: las
  71 apariciones de «Thitz 71» son de Thitzana, no de Nandisena. Las
  cifras `Nyāsa 9 · Thitz 71` del formulario eran APARICIONES, no páginas.
- La Rūpasiddhi está sólo para Taddhita, Ākhyāta y Kibbidhāna; si llegan
  los capítulos 1-4, basta añadirlos a `RU` y volver a correr
  `incorporar_…` sobre una copia limpia, o `referenciar_terminos.py` a mano.

## 3 bis. Una fuente nueva: el Niruttidīpanī de Ledi Sayadaw

El IEBH aportó el *Niruttidīpanīpāṭha* (ed. VRI, 311 pp.), comentario a
Moggallāna. Texto extraído en `docs/fuentes/niruttidipani/Niruttidipani-patha.md`
(páginas «[p. N]»; el PDF no viaja). Barrido de términos contra los 2.049
lemas y la cosecha: **unos 50 candidatos nuevos**, curados y con glosa
propuesta, en `docs/glosario/niruttidipani-terminos-candidatos.md`. Lo
distintivo: las ocho clases de sandhi de Moggallāna (…dvibhāva, vipallāsa),
las tres raíces (pakati-, vikati-, nāma-dhātu), los tres agentes (sayaṃ-,
payojaka-, kamma-kattā), **mahāvutti** (138 veces), los ocho sentidos del
taddhita y los ocho visesavidhāna del compuesto.

**El IEBH los aceptó en la sesión**: 51 lemas (la tabla del documento
menos los siete «paṭhamā-vibhatti…sattamī-vibhatti» y «evuddhi»), con las
glosas propuestas tal cual. Entraron por el mismo camino: filas añadidas a
`terminos-faltantes.json` con `"cosecha": "Niruttidīpanī, s. 58"`,
veredictos en `docs/glosario/veredictos-niruttidipani.json`,
`incorporar_terminos_faltantes.py` (ahora lee el campo `cosecha` para la
celda «Fijado en»). `referenciar_terminos.py` tiene el libro como cuarta
obra, **Nirutti.**, con la numeración de Moggallāna (804 suttas de 810), así
que cada fila nueva lleva sus suttas en las cuatro obras. **Las 67 filas de
la cosecha 57 NO se retocaron** con referencias al Niruttidīpanī: son filas
publicadas, y se hace si el IEBH lo pide (basta volver a calcularlas).

## 4. Lo que el chat que siga tiene que hacer

1. Lo del briefing 57 §5 que no se ha tocado: tanda 2 del inglés, puntos
   17-34, barridos §5.23 b y §5.34.
2. Si el IEBH quita suttas de las designaciones: editar
   la fila en `comun/glosario.md` (y la clave en `glosario-ingles.json` si
   cambia el lema), `generar_todo.py`.
3. Si el IEBH quiere referencias «Nirutti.» también en las 67 filas de la
   cosecha 57: recalcularlas con `referenciar_terminos.py` y reescribir la
   celda «Fijado en» de cada una.
4. Los 70 sufijos: esperar a que el IEBH diga cómo quiere que entren.
5. Comprobación de siempre con jsdom (briefing 57 §5.6); las cuentas ahora
   son **2.100** lemas y **171** normativos.

### Advertencias operativas que no cambian

Las del briefing 57: `git --no-optional-locks status --porcelain`, nada de
`git checkout -- archivo`, los PDF no viajan.

## 5. Cifras al cerrar

| | |
| --- | --- |
| normativos | **171** (53 al abrir: 67 de la cosecha 57 + 51 del Niruttidīpanī) |
| lemas de la vista alfabética | **2.100** |
| enlaces en la capa de Nandisena | **637** en 324 fichas |
| términos nuevos con sutta localizado | 118 de 118 |
| sufijos de la cosecha en la norma | 0 (decisión del IEBH: más adelante) |

## 6. Versión

El glosario pasa de **v0.1 a v1.0** (`recursos/glosario/conspectus.json`,
campo `version`, y las `<meta>` de la plantilla): el Conspectus colacionado
entero, Nandisena completo, 171 normativos con sus suttas, enlaces cruzados.
Lo que viene —el inglés de Nandisena por tandas, los sufijos— son 1.x.

## 7. Numerales en paradigmas, y el barrido de paradigmas en otras fuentes

- **Paradigmas v1.16**: dos fichas nuevas bajo Numerales, **#3 los cardinales**
  y **#4 los ordinales**, con la prosa del documento «Numerales» de Bhikkhu
  Nandisena (Google Doc `1kJVYCgqN51glznKyy-eV3CZvh14THpi5QcvGyDW1MZI`) y las
  listas completas (140 cardinales hasta 10¹⁴⁰; 31 ordinales). Nuevo tipo de
  ficha: `parrafos` (prosa con enlaces `{{CÓDIGO|texto}}` a otras fichas) +
  `lista` ({columnas, filas}); lo pinta `prosa()` y la rama `p.lista` de
  `card()` en `plantilla.html`; búsqueda, copia y barra lateral lo saben.
  Guion: `herramientas/incorporar_numerales.py` (idempotente). Tres erratas
  del documento corregidas con el visto bueno del IEBH y dichas en las notas
  (Aṭthasataṃ, Paṭhamam, «quinta» por cuarta). **Ojo**: `ingles.json` está
  ADJUDICADO en bloque (2026-08-29), así que el inglés de #3 y #4 —borrador
  del traductor— se publica como si estuviera firmado; el IEBH debe leerlo
  (`docs/paradigmas/ingles-por-adjudicar.md` no lo separa).
- **Dos fuentes nuevas en texto**: `docs/fuentes/saddaniti/Saddaniti-padamala.md`
  (VRI, 176 pp.) y el Niruttidīpanī ya dicho. Barrido de tablas de
  declinación en Padamālā, Nyāsa y Niruttidīpanī contra los 84 documentos:
  `docs/paradigmas/paradigmas-en-otras-fuentes.md`. Lo que falta en la
  página: los **monosílabos** (thī, dhī, bhū, kha, go…), **bodhi/nābhi** con
  contracciones, **dhātu** masculino, una ficha de **adjetivo** (dīgha),
  arahanta/mahanta, y notas sobre el compuesto en rāja/sakha/atta. El Nyāsa
  no declina nada. Decide el IEBH.

## 8. Comillas, cursivas y los documentos de cada numeral (2026-09-06)

- **Comillas** (guía de estilo §4: dobles para palabras, simples para letras,
  sílabas, prefijos y sufijos): 28 sustituciones en el español firmado de
  Nandisena (`nandisena.json`) y 5 en su inglés (`ingles.json`): 'a', 'i',
  'u', 'o', 'ā', 'aṃ', 'ga', 'ha', 'da', 'abhi', 'ati', 'ava', 'ku', 'upa',
  'āya', 'ti', 'tvā', 'tuna', 'tvāna', 'tuṃ'. Las partículas (na, ca, vā,
  mā, no, hi), los pronombres (so, sā, te, ya, ta) y las raíces (dā, su, kī,
  i) siguen entre dobles: son palabras. Hecho por pedido del IEBH sobre
  texto firmado. **Pendiente de decidir**: las notas de `/recursos/sandhi/`
  citan formas y letras con «…» (guillemets), una tercera convención.
- **El pāḷi en cursiva**: en el glosario, toda voz pāḷi suelta en las glosas
  (Nandisena, Smith, norma, puente) va en `<i class="pl">`, y enlaza si es
  lema (`claseSuelto()` en `plantilla.html`: diacrítico, o lema de ≥4
  letras; «mata» excluido; mayúsculas y entrecomillados en redonda; las
  marcas «(A)», «(B)» de Smith ya no enlazan al lema «a»). 3.947 cursivas,
  2.509 enlaces, 0 errores. En paradigmas, `hiPali()` hace lo mismo sobre
  párrafos, familias, notas y usos, con las formas de la propia página como
  léxico. **Sin hacer** en sandhi, verbo, raíces, nombre y solucionador:
  hay que mirar cada plantilla; sus textos son sobre todo tablas.
- **Los Google Docs de cada numeral**: el documento «Numerales» enlaza del 1
  al 23 (39 formas) su propio documento de declinación; van en #3 como
  `{f, doc}` en cada forma y la ficha pinta un «↗» tras la forma
  (`DOCS_FORMA` en `incorporar_numerales.py`; `celda()` en la plantilla).
