# Kaccāyana Pāḷi-Español: Briefing de la Sesión 11

*Complementa a `briefing-sesion-05.md` (reglas y terminología), `-06`, `-07`,
`-08`, `-09` y `-10`. El chat nuevo debe leer los SIETE briefings; para
traducción siguen mandando el 05 y el 07. Esta sesión empezó el capítulo 3
(Kāraka-Kappa) y dejó traducidos en borrador §271–§300. La sesión 12
continúa con §301–§315.*

---

## 1. ESTADO AL CIERRE DE LA SESIÓN 11

- **Capítulo 3 (Kāraka-Kappa): §271–§315, 45 suttas, un solo kaṇḍa** (el
  *sexto* del Nāma: cierra con «Iti nāma-kappe kāraka-kappo chaṭṭho kaṇḍo»
  y «Kāraka-kappo niṭṭhito»). 37 notas al pie en la fuente.
- **Borradores entregados** (formato de trabajo, comillas tipográficas):
  - `docs/borradores/sesion-11-suttas-271-285.md` (tanda 1)
  - `docs/borradores/sesion-11-suttas-286-300.md` (tanda 2)
- **FALTA la tanda 3: §301–§315.** Ésa es la primera tarea de la sesión 12.
- **el IEBH revisará el español AL FINAL del capítulo**, cuando se le entregue
  el .md completo — NO sutta a sutta. Las decisiones pendientes (ver §6)
  esperan a esa revisión; mientras tanto se presentan lecturas literales.
- Los pasos de publicación de `CLAUDE.md` («Capítulo nuevo: qué hace falta»)
  se ejecutan solo cuando el capítulo esté completo y revisado.

## 2. FUENTES Y LOCALIZACIONES EXACTAS

- **Base:** `3 - Kāraka-Kappa–Kaccāyana.md` (carpeta de conocimiento).
  Empieza en §271. **§301–§315 = líneas 682–966** (§301 en 682; notas al pie
  del archivo al final). Formato: encabezados `**NNN\. RR\. Título** (Sad)`,
  pāḷi primero, después su inglés.
- **Rūpasiddhi Kāraka:** `3 - Kāraka–Rūpasiddhi.md` (secundaria, pāḷi).
- **Pind:** su numeración va +2 en este capítulo (nuestro §271 = su 273;
  nuestro §301 = su 303). **§301–§315 = sus 303–317, líneas ~3200–3400** del
  archivo. Ya se leyó hasta su 310 en esta sesión (variantes registradas en
  los borradores).
- **Thitzana:** lista de títulos con doble número en líneas 2315 ss.;
  entradas con desglose desde la línea 11995 (§271). Los desgloses [N voces]
  SIEMPRE se cotejan ahí.
- **El archivo del Saddanīti en la carpeta de conocimiento está vacío**
  (678 líneas en blanco): los números Sad solo se cotejan vía Pind.

## 3. DECISIONES DE ANGEL EN ESTA SESIÓN

1. **bhayaṃ** = «peligro o temor», espejando el orden de Nandisena en cada
   aparición («danger or fear» / «fear/danger»).
2. **sikkhā** = «entrenamiento».
3. **Kvattho:** «¿Cuál es la utilidad del nombre "X"? Para el uso del nombre
   "X" en el sutta "Título" (§N).» **+ traducción del sutta citado** a
   continuación (p. ej. «En el apādāna, la quinta [inflexión].»).
4. **saññā** = «recibe el nombre» (también se admite «se denomina»).
5. **Números de Saddanīti según Nandisena** (§271 imprime «(555, 557)»
   aunque Pind dé 555–56).
6. **Bloque «Ejemplos:» en cada sutta** (petición expresa): lista con
   asterisco, **el kāraka del ejemplo en negrita**, traducción española
   entre paréntesis inmediatamente después. El IEBH pidió «subrayado»; se usa
   negrita porque el subrayado no sobrevive la exportación a markdown — si
   lo quiere en el sitio, habrá que añadir `<u>` al generador (fase HTML).
7. La división del trabajo del capítulo: **tres tandas de 15** (271–285,
   286–300, 301–315).

## 4. CONVENCIONES NUEVAS FIJADAS EN LA PRÁCTICA (tandas 1 y 2)

- **Encabezado con doble número de Rūpasiddhi:** §271 se imprime tal cual
  Nandisena: «**271. 88, 308. Yasmād apeti…**». Verificado: la regla
  aparece dos veces en el Rūpasiddhi (en su Nāma-kaṇḍa y como su 308 en el
  Kāraka-kaṇḍa); Thitzana también imprime «271, 88, 308». Es el ÚNICO sutta
  del capítulo con dos números. **Consecuencia:** `RE_SUTTA` de
  `generar_capitulo.py` no casa «88, 308» — ampliar la regex a
  `(\d+(?:,\s*\d+)*)` en la fase de publicación.
- **Comillas tipográficas** desde el origen: “…” palabras, ‘…’ letras y
  raíces, ’ para TODA elisión pāḷi (Yo ’dhāro, Yato ’haṃ…) normalizada a
  comilla derecha (el OCR de Nandisena mezcla ‘ y ’). En las notas del
  traductor, «…» para citar su inglés o texto editorial.
- **Kāraka en negrita solo dentro del bloque «Ejemplos:»**; los rótulos en
  negrita de Nandisena (**Dūratthe**, **Pihappayoge**…) se conservan en el
  bloque pāḷi.
- «Taṃ yathā?» = «¿Como qué?» (precedente del Nāma §53); cuando no hay
  «Taṃ yathā?», el rótulo «Ejemplos:» va solo.
- Glosas inglesas de los nombres kāraka entre paréntesis en los kvattho,
  según Nandisena: kamma (objeto), kattu (sujeto), karaṇa (instrumento),
  hetu (causa), sāmī (poseedor), okāsa (receptáculo), sampadāna (dativo),
  apādāna (ablativo).
- Nandisena traduce Bhagavā como «the Blessed One» → «el Bienaventurado»
  (precedente del Nāma §251/§220); samaṇa → «asceta»; cīvara → «túnica»;
  kappa → «eón»; Sugata → «el Que ha Ido Rectamente» (su inglés).
- Paréntesis suyos con palabras suplidas → corchetes […]; paréntesis suyos
  explicativos → se conservan como paréntesis.
- Las series de alternancias de caso que él no traduce («rahitā mātujaṃ,
  rahitā mātujena vā») se dejan en pāḷi también en el bloque español.
- **Notas al pie:** conservan la numeración de Nandisena donde se puede
  (tanda 1: 1–28 suyas + 34, 35, 41 del traductor + 36–40 = sus 29–33
  renumeradas; tanda 2: sus 34 y 35 tal cual). **Para la tanda 3 quedan sus
  [^36] («“Sāmā” can mean both golden complexion or dark complexion», en
  §303) y [^37] («It means that he disregarded the crying of his son…», en
  §305).** Numerarlas con cuidado de no chocar.
- Referencias bibliográficas: retiradas de ambos bloques y tabuladas en las
  NOTAS DE TRABAJO de cada borrador (fase HTML las restituye).

## 5. HALLAZGOS TEXTUALES YA REGISTRADOS (en los borradores)

- **Erratas propuestas** (cuerpo literal): tanda 1 — §274 *vibhatyatthaṃ*,
  §275 *Vibhatthe*, *saṅkhameyya*, *kammādhikaranesu*, §277 *bhikhave*,
  §280 *ratthaṃ*→*rathaṃ*, §283 *bhikhuno*, §285 *liṅgathā-*; tanda 2 —
  §287 *gaggena*, §290 *samyena*, §299 *kittissaddo*, §300 *sayādinaṃ*.
  §272 *asaho* NO es errata (Thitzana también lo lee; Pind *asayho*).
- **§277, sección Tadatthe: el pāḷi falta en la fuente** (OCR); el inglés
  existe. Restauración desde Pind/Be propuesta en la nota 35 del borrador 1.
- **§282: mojibake «���e» restituido como ṇe** (corrupción del archivo, no
  lectura); **§277 título:** guion+espacio del OCR unido.
- **§277: Nandisena no traduce el título** («Here I did not translate the
  sutta»); la glosa española es nuestra, marcada en nota 34 del borrador 1.
- DUDAs abiertas listadas en las notas de trabajo de cada borrador (§3 en
  ambos): «me agrada el rey», «la tormenta destruye los países», las
  interjecciones de §284, tiṭṭhati «existe» (§278), la vutti de «vā» en
  §276, el mapeo inglés de §296, «kāṇaṃ passati nettena» (§291, que Pind
  marca sin sentido), «vā» opcional omitido en el inglés de §300, dāna =
  «dádiva».

## 6. PENDIENTES

1. **Tanda 3: §301–§315** (sesión 12). Suttas §303–§315 son de tamaño
   medio; §303 y §306 tienen listas dobles (chaṭṭhī ca sattamī ca), §307 el
   espacio raro «( 589)» a normalizar/flagear, §308–§315 mezclan casos.
2. **Al terminar la tanda 3:** montar el capítulo completo en un solo .md
   de trabajo y entregarlo al IEBH, que hará ENTONCES su revisión del
   español y fallará las erratas, las DUDAs y los cuatro grupos de
   decisiones pendientes (erratas / Tadatthe / DUDAs / glosa de §277).
3. Tras la revisión: pasos de publicación de `CLAUDE.md` (markdown en
   `kaccayana/03-karaka-kappa.md`, entrada en `CAPITULOS`, regex del
   generador para «88, 308», concordancia.json, tarjeta del índice).
   Fórmulas de cierre del capítulo por decidir con IEBH (es «sexto kaṇḍo
   del nāma-kappa» y a la vez fin del Kāraka-kappa).
4. Glosario: volcar los términos propuestos en las notas de trabajo de los
   borradores (§6 tanda 1, §5 tanda 2) cuando IEBH los apruebe.
5. Siguen vivos los pendientes heredados del briefing-10 §7 (push/revisión
   visual si quedara algo, y a plazo el solucionador de sandhis).

## 7. PARA EL CHAT NUEVO

- Leer primero este briefing y los borradores
  `sesion-11-suttas-271-285.md` y `-286-300.md` (sus NOTAS DE TRABAJO son
  vinculantes para mantener uniformidad), más briefing-05 §3 (flujo) y §7
  (formato).
- Continuar con **§301** («Sāmismiṃ chaṭṭhī», línea 682 de la fuente) en el
  MISMO formato de las tandas 1 y 2, tercera tanda en
  `docs/borradores/sesion-11-suttas-301-315.md` (o sesion-12; da igual el
  nombre, que quede junto a los otros).
- Presentar lecturas literales; erratas y DUDAs a las notas de trabajo; no
  esperar aprobaciones sutta a sutta (el IEBH revisa al final).
- La conversación de trabajo, en inglés; la traducción, en español formal.

---

*Preparado al cierre de la sesión 11. La sesión 12 empieza con §301–§315.*
