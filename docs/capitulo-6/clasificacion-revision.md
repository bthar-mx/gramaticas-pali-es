# Clasificación de los suttas, capítulo 6 (Ākhyāta, §406–§523): lo que hay que revisar

Borrador del 2026-10-12, pedido del IEBH ese día («añadir el capítulo 6 con las
fuentes de antes»). Página: `/recursos/clasificacion/`, v0.8 (borrador).
Datos volcados por `docs/capitulo-6/_clasif_cap6.py` (no volver a ejecutar:
se niega si `datos.json` no está en la v0.7.6). Copia de la v0.7.6:
`docs/clasificacion/datos-v0.7.6-antes-akhyata.json`. Extracto de las fuentes
por sutta: `docs/capitulo-6/_fuentes_clasif_cap6.json`.

## Fuentes y método: los de los capítulos 1–5

- **Rūpasiddhi**: `docs/6. Ākhyāta-Rūpasiddhi.md` (el §432 = Rū 362, en
  `docs/5. Taddhita-Rūpasiddhi.md`). Número de la Rūpasiddhi según
  `comun/concordancia.json`. Cita: la primera frase de la vutti; recortada a
  mano en 43 suttas donde la frase sigue con la derivación.
- **Nyāsa**: `docs/fuentes/nyasa/Nyasa-06-akhyata.md`. El texto OCR va sin
  espacios entre palabras; las citas están **normalizadas por Claude** (fórmula
  «… ti ñāpanatthaṃ»). Como en los capítulos anteriores, son paráfrasis hasta
  cotejarlas con el facsímil.
- **Thitzana** (vol. 2, Introducción, pp. 36–37): línea «Thitzana» en los
  suttas cuya operación se cuenta en la ādesa: §444 (atidesa), §483–§485
  (vuddhi), §488 (vipariyāya).
- **No se ha usado todavía** la Kaccāyanavaṇṇanā, la Bhāsāṭīkā, el Saddanīti
  ni las clases de U Sīlānanda para el capítulo 6: en los capítulos anteriores
  sirvieron para los dudosos. Tampoco la Visuddhāyuṃ (véase abajo).

## Resultado

| Clase | Cuántos | § |
| --- | ---: | --- |
| saññā | 14 | 406–408, 423–431, 457, 459 |
| adhikāra | 1 | 413 (Rū 427: «Ayam adhikāro») |
| paribhāsā | 2 | 409 (Rū 441: «paribhāsam āha»), 432 (Rū 362 y Nyāsa: «paribhāsāsuttaṃ») |
| vidhi | 101 | el resto |

Vidhis: ādesa 43, vibhatti 16, paccaya 15, ādesa + lopa 9, lopa 6, āgama 6,
dīgha 2, rassa 1, lopa + ādesa 1, paccaya + āgama 1 (§446), y §517 con cinco.
Etiquetas: «ādesa: atidesa» §444; «ādesa: vuddhi» §483–§485; «ādesa:
vipariyāya» §488 (etiqueta nueva en la plantilla, en los dos idiomas).
19 notas nuevas.

## Cotejo independiente (2026-10-12)

Un segundo agente, sin ver cómo se hizo, comparó las 118 entradas con los dos
textos (cita por cita, número de la Rūpasiddhi, operación en los dos idiomas).
Halló 13 puntos, todos corregidos antes de generar la página: §498 citaba a
Nyāsa con «kusa», que es la lectura de Rūpasiddhi (Nyāsa lee «kudha»: ahora va
así, con nota); §481 no decía «opcionalmente»; la frase «paribhāsam āha» de
§409 es el cierre de Rū 440, no de Rū 441; un corte sin «…» en §455; una
palabra añadida («hakārassa») en §488 y un ejemplo que ilustraba otra
operación; «a veces» (kvaci) en §516 y §520; y cuatro retoques de grafía
(§444, §446, §496, §521).

## Para que el IEBH decida

1. **La Visuddhāyuṃ (pariśiṣṭa del Ākhyāta, PDF 317) da cuatro paribhāsā:
   §409, §420, §432 y §455.** La página da paribhāsā solo §409 y §432, que son
   los que nombran Rūpasiddhi o Nyāsa; §420 (Māyoge sabbakāle ca) y §455
   (Dhātuppaccayehi vibhattiyo) van como vidhi · vibhatti. Las saññā (14) y la
   adhikāra (§413) coinciden exactamente con el pariśiṣṭa. La lectura del
   pariśiṣṭa es borrador (las dos lecturas coinciden, pero el capítulo no es
   [V]): por la regla de la v0.7 (solo lo que el libro rotula, y con decisión
   del IEBH) no se ha usado. ¿Se sigue al libro en §420 y §455 cuando el
   Ākhyāta de la Visuddhāyuṃ pase a [V]?
2. **§517: «viparīta».** Rū 488 lo glosa «tabbiparīta», «lo contrario de eso»
   (del alargamiento), es decir, acortamiento, y lo ilustra con «Nāmhi rasso
   kiyādīnaṃ». La página lo clasifica así: dīgha + rassa + ādesa + lopa +
   āgama. Pero el capítulo 6 publicado traduce «inversión» («reversal» en
   inglés). ¿Se revisa la traducción del capítulo? Y en el §404 (Taddhita) el
   «viparīta» se contó en la ādesa («ādesa: vuddhi, vikāra, viparīta»).
3. **§410–§412** (la persona del verbo) y **§455**: ninguna fuente nombra la
   clase; van como vidhi · vibhatti, con nota «por revisar».
4. **§458 (reduplicación)**: āgama, como el §28 (dvebhāva); nota «por revisar».
5. **§444 (Tathā kattari ca)**: ādesa con etiqueta atidesa, como §187, §331 y
   §332.
6. **El rótulo del primer kaṇḍa del capítulo 6 dice «PAṬṬHAMA-KAṆḌA»**, con
   ṭṭh, en `docs/6. Ākhyāta-Kappa.md` (línea 4) y en
   `kaccayana/06-akhyata-kappa.en.md`; los demás capítulos dicen
   «PAṬHAMA-KAṆḌA». Por eso la clasificación no reconoce el ordinal y la
   primera sección del Ākhyāta sale sin el rótulo «Primera sección». No se ha
   tocado: el maestro es del IEBH.
