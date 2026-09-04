# Briefing de la sesión 50 — el Conspectus, páginas 1135-1138, y un escaneo nuevo que lo cambia todo

**Fecha:** 2026-09-04. **Estado:** 34 de las 44 páginas transcritas (1105-1138).
**Lo que hay que hacer:** seguir por la página 1139.

Este briefing supone leídos los de las sesiones 46, 47, 48 y 49, que siguen
vigentes en todo lo que no se corrija aquí. **Y lo que aquí se corrige no es un
detalle: a mitad de sesión IEBH fotografió su propio ejemplar del Conspectus y
la fuente de imagen ha cambiado. Ver §2, que es lo primero que hay que leer.**

---

## 1. Lo hecho

Cuatro páginas nuevas, 132 términos, de 1.252 a 1.384. El generador publica
limpio.

| pág. | epígrafes | materia |
| --- | --- | --- |
| 1135 | 6.1.1.1, 6.1.1.2, 6.1.1.3 | fin del pada; el sentido de la palabra; **la precisión del sentido** |
| 1136 | 6.1.1.3, 6.1.2.1-6.1.2.3, 6.1.3.1 | el sinónimo; las listas; **empieza la homonimia** |
| 1137 | 6.1.3.1-6.1.3.3, 6.2.1 | la homonimia entera; **empieza el sintagma** |
| 1138 | 6.2.1, 6.2.2, 6.2.3, 6.3 | concordancia, subordinación, elipsis; **empieza el eufemismo** |

La 1138 se corta en «maṅgala(vacana)-»: **la 1139 sigue dentro de 6.3**.

Con esto queda entera la sección 6.1 (la palabra y su sentido) y casi entera la
6.2 (el sintagma). El Conspectus lleva ahora **1.384 términos**.

---

## 2. LA FUENTE DE IMAGEN HA CAMBIADO: EL EJEMPLAR DE ANGEL

`recursos/saddaniti/conspectus-ejemplar-angel.pdf`, 44 fotogramas, las páginas
**1105-1148** completas, una por fotograma y en orden, cortadas justo donde
empieza el Conspectus métrico. Hechas con un iPhone el 2026-09-04.

### Por qué es mejor, y no es por resolución

Medido: el interlineado da **74 px**, contra 72-76 px del
`saddaniti-smith-04.pdf` a 400 dpi. **El muestreo es equivalente.** Lo que
cambia es la procedencia: el PDF de archive.org es el escaneo de una
reproducción mediocre, y esto es la tinta. Los 400 dpi de aquél son nominales.

Un primer intento —una foto de doble página, ~205 dpi por página— quedaba a la
mitad y se descartó; lo que arregló el problema fue **una página por
fotograma**, y es la única indicación que hizo falta.

### Lo que resuelve, con ejemplos de esta misma sesión

| lo que no se leía a 400 dpi | lo que dice el ejemplar |
| --- | --- |
| `As 136,₁₆—139,₁?` (p. 1135) | **139,16**, no 18. La ficha llegó a llevar 18 con duda |
| `685,2?` (p. 1137) | **685,20**, no 685,29 |
| las 12 referencias de 6.1.2.3 (p. 1136) | las doce, limpias, y confirman lo leído |
| las 6 de 6.1.2.2 (p. 1136) | las seis, limpias, y confirman lo leído |
| la ḍ de `āmeṇḍita` (p. 1137) | los dos puntos suscritos, sin duda |
| la mancha tras `uyyāmo :` (p. 1135) | no hay tal signo: era suciedad del papel |

### Lo que NO resuelve, y conviene tenerlo claro

- **Las referencias a la PTS** (`As`, `Dhs`, `M`…) se leen pero **no se pueden
  cotejar**: esos volúmenes no están en el repositorio. Leer bien un subíndice
  no es verificarlo.
- **Los errores de Smith siguen siendo suyos.** Mejor imagen dice qué imprimió,
  no si acertó. La regla de no corregir por cuenta propia no cambia.

### Y NO VIAJA CON EL REPOSITORIO

`.gitignore` excluye `*.pdf` y **esa línea no se ha tocado**. Pero este archivo
no es como los otros: los cinco volúmenes se vuelven a bajar de archive.org, y
éste **sale del ejemplar del IEBH y no existe en ninguna otra parte**. Ahora
mismo vive sólo en su disco. **Es decisión suya** si quiere una excepción en
`.gitignore`. Queda anotado en `recursos/saddaniti/LEEME.md`, con la orden de
extracción:

    # hoja del PDF = página impresa − 1104 (la 1135 es la 31)
    pdfimages -j -f 31 -l 31 recursos/saddaniti/conspectus-ejemplar-angel.pdf /tmp/p

`pdfimages -j` copia el JPEG original y tarda milisegundos; `pdftoppm` sobre
este archivo reescala mal, porque las cajas de página no son uniformes.

---

## 3. LO QUE ANGEL DECIDIÓ, Y LO QUE QUEDA DICHO PARA QUE NO SE PIERDA

### 3.1 `vicchā` se queda con i breve. Y el impreso dice `vīcchā`

Se comprobaron **las cuatro apariciones** sobre el ejemplar: `vīcchāyoge` (4.3,
p. 1120), las dos de 5.2.1 (p. 1124) y la nueva de 6.1.3.1 (p. 1137). **Las
cuatro llevan macrón**, y en la p. 1124 el contraste es interno y decisivo: en
la misma línea, la i de `pariccheda` es un punto redondo y la de `vīcchā` una
barra horizontal, a ×8.

**El IEBH resolvió: `vicchā` es la lectura correcta.** Y tiene la lengua de su
parte —el pāḷi abrevia ante grupo consonántico, de modo que el *vīpsā* sánscrito
da *vicchā*— y también a Nandisena, cuyo lema de cabecera es `vicchā`. Lo más
probable es que Smith arrastre la ī del sánscrito, como hace en `vibhatyanta`,
`vyañjana` y `mukhyavasena`.

**Sólo la ficha nueva de la p. 1137 lo dice.** Las de las pp. 1120 y 1124 llevan
el lema que él fijó y **no se han tocado**, por la regla de no reescribir lo
revisado. Si quiere que también lo digan, es un añadido de dos líneas.

### 3.2 El `ns` está resuelto: es la NISSAYA birmana

Abierto desde la sesión 47 (p. 1120, tras `antojappana`), y la sesión 49 lo dejó
en «una de las siglas de testimonio». **Ahora está cerrado**, y no por la imagen
nueva sino por el cuerpo de la obra:

- En las pp. 32, 37 y 38 del vol. I, `ns` figura en la **cabecera de página**
  junto a `Cᵉ` y `Bᶜᵐ`: «CᵉBᶜᵐns».
- Y el aparato lo cita **en birmano**: «ns: pāṇadadī santī tui kā atthamatta
  nhuik paṭhamā» (p. 32, n. a); «pud eñ phrac kui, ns» (íd., n. c).

Es decir: **ns es la nissaya**, la paráfrasis birmana palabra por palabra que
Smith usa como testimonio — y el *nissaya* como género ya tenía ficha, en
5.3.3.3 (p. 1132). Marcar un término con «(ns)» significa que la voz es de la
nissaya y no de Aggavaṃsa.

Esto explica de una vez el `antojappana, ns` de la p. 1120 y el **`vākyattha
(ns)`** nuevo de la p. 1138. **La ficha de la 1120 no se ha tocado**; la de la
1138 lo cuenta entero. Sigue faltando cotejarlo con la lista de siglas de los
preliminares del vol. I, que nadie ha buscado todavía.

---

## 4. SEIS REFERENCIAS VERIFICADAS ABRIENDO EL PASAJE, Y UNA DE ELLAS CIERRA UNA DUDA DE LA 1134

El método del briefing 49 §3 se aplicó a las referencias a la propia Saddanīti.
**Las seis caen exactamente donde Smith dice.** Ninguna corrección.

| referencia | dónde sale | qué hay en esa línea |
| --- | --- | --- |
| **32,19** | 1135 (padajāti) | «…mānavibhattikan ti pi. **Asamānapadajātikatte** ¹⁵"sayaṃ» |
| **37,12, 13** | 1137 (visesakapadāpekkhaka) | la 12 «na **te saṃ** koṭṭhe openti», la 13 «**satta vo** Licchavi…»: **un subíndice por pareja** |
| **38,26—41,32** | 1137 (ekābaddha) | la p. 38,32-35 trae akkharasannidhāna, padasannidhāna, vicchā y āme(ṇ)ḍita, las cuatro voces del paréntesis |
| **549,15—17** | 1136 (pariyāyasadda) | la 17 remata «mānana-pūjanasaddā hi **pariyāyasaddattā vevacanasaddā eva**» |
| **911,6** | 1137 (vyañjana) | la 6 cierra «Tathā **vyañjanachakke vyañ**-», y la definición está en la 7-8 |
| **918,1—3** | 1137 (dvādhippāyika) | las tres líneas dan ekādhippāyika, **dvādhippāyika**, **adhippāyattayika**, caturādhippāyika, bavhādhippāyika |

### Y aquí está el hallazgo de fondo: `vibhatyanta` es de Smith, no de la obra

La p. 1134 se cerraba con `vibhatyanta : avibhatyanta`, y la sesión 49 lo dejó
con `duda`: una sola t y con y de transición, que es el tratamiento sánscrito de
*vibhakti + anta*, cuando el pāḷi pediría *vibhattyanta* o *vibhattanta*.

**La p. 911 del vol. III lo resuelve.** Aggavaṃsa escribe, en cuerpo de texto y
sin ambigüedad:

- l. 2: «…viya **vibhattiyantaṃ** atthajotakaṃ akkharapiṇḍan ti gahetabbaṃ»
- l. 4: «**vibhattiyanto** pi **avibhattiyanto** pi atthajotako akkharasamūho»

Doble tt y `-iy-` completo. **La forma sanscritizada es de Smith.** Y de propina
las líneas 1-6 de esa página son la fuente de todo 6.1.1.1: allí están también
`akkharapiṇḍa`, `akkharasamūha` y `atthajotaka`, las tres últimas fichas de la
p. 1134.

**La ficha de la 1134 no se ha tocado.** Lo cuenta la de `vyañjana` (6.2.1,
p. 1137). Decidir si la 1134 se anota es del IEBH.

### El «v. cependant» de la p. 1136, explicado

Smith reparte el sinónimo en (A) `pariyāya` y (B) `vevacana`, y añade «v.
cependant 549,15—17». Abrir el pasaje explica el «sin embargo»: **la Saddanīti
identifica lo que él separa** — «por ser pariyāyasadda son sin más
vevacanasadda». No es una remisión de apoyo sino una objeción a sí mismo.

---

## 5. Erratas y rarezas nuevas, ninguna corregida por cuenta propia

Todas comprobadas sobre el ejemplar del IEBH, que es lo que las hace afirmables.

- **`aparadipanā` y `dipanā` con i BREVE (6.1.1.3, p. 1136)**, dos veces en dos
  líneas, donde el pāḷi pide `dīpanā`, de *dīpeti*. A ×8 el signo es un punto
  redondo y contrasta con el macrón de la ā final de la misma palabra; el
  escaneo del repositorio dice lo mismo. **Ojo:** el lema `-dīpana` de 5.3.3.3
  (p. 1132) se transcribió con ī. O son dos grafías de Smith, o una de las dos
  es errata. Va con `duda`.
- **`visesaniya` sin macrón (6.2.1, p. 1138)**, donde el sufijo del participio
  de futuro pasivo es `-anīya` con ī larga —y así lo da Nandisena al enumerar
  los sufijos kicca—. Misma clase de anomalía que la anterior. Va con `duda`.
- **`asamānapavattinimitta` con una sola p (6.1.3.2, p. 1137)**, mientras la
  obra que indiza escribe `asamānappavattinimittā` con dos (p. 32,25). La
  geminación tras `pa-` es la regular. Va con `duda`.
- **`satva` sánscrito entre paréntesis REDONDOS (6.1.1.1, p. 1135)**, no entre
  corchetes. Con `prātiśākhya`, el `vaṃśa-` de la p. 1132, `gamyate` (p. 1134) y
  el `anuprāsa` de la p. 1127, van **cinco sánscritos sin corchete en once
  páginas**. No es que la convención no exista —en estas mismas cuatro páginas
  van entre corchetes `[avyutpanna]`, `[kośa]`, `[śleṣa]`, `[virodhābhāsa]` y
  `[cvi]`—: es que Smith no la sigue siempre. Va con `duda`.
- **`mṭ`, sigla nueva sin desarrollar (6.1.1.3, p. 1136)**, en «mṭ ad As 137,5».
  Lo más probable es *mūlaṭīkā*, pero no consta y no se afirma. Con `ns` ya
  resuelta, van dos siglas suyas identificadas fuera de la lista de
  preliminares, que sigue sin buscarse.
- **El paréntesis de `vākya` abre en ANGULAR y cierra en REDONDO**, a caballo
  entre páginas: «vākya ⟨= pada-» al pie de la 1137 y «samūha);» al abrir la
  1138. Comprobados los dos signos. Si el angular garantiza a Moggallāna
  —sesión 47 §4, matizada en la 48 §3—, aquí lo garantizaría y lo desmentiría a
  la vez. Va con `duda`.
- **`maṅgala` y `avamaṅgala` con ṅ VELAR (6.3, p. 1138)**, contra la norma de
  Smith en toda la sección 6, que escribe `saṃkhāra`, `saṃkhata`, `saṃketa` con
  ṃ. Se transcribe como está impreso.
- **Segunda expresión GRIEGA:** `ἀπὸ κοινοῦ` (6.2.1, p. 1138), tras la
  συνθήκη de 6.0.1 (p. 1133). La ficha de la 1133 la daba por la primera vez que
  echaba mano del griego; ya son dos, y ésta es término técnico de la filología
  clásica, no glosa.
- **`padatthuti` (6.1.1.3, p. 1135)** no es errata aunque lo parezca: *pada* más
  *thuti*, «alabanza por medio de palabras», que es exactamente lo que hace el
  Dhammasaṅgaṇī al amontonar sinónimos. Se repite dos veces en la p. 1136, lo
  que confirma la lectura.

---

## 6. Homónimos: CUATRO nuevos, y el cotejo confirmó mucho más de lo que separó

Se repitió el cotejo con Nandisena sobre los 132 términos nuevos, término a
término y con las dos definiciones a la vista, como pide el briefing 48 §5.
**Casan 29 de los 132.** El guion está en `/tmp` de la sesión y se rehace en
diez líneas.

| término | Smith | Nandisena |
| --- | --- | --- |
| **vibhatti** (6.1.1.3) | la disección, el despliegue analítico | la DESINENCIA, nominal o verbal |
| **sarūpa** (6.1.1.1) | la *suppositio materialis*: la palabra como sonido | «similar», opuesto de asarūpa |
| **nāma** (6.1.2.3) | la lista de denominaciones, un género de obra | el NOMBRE, clase de palabra |
| **pakaraṇa** (6.1.3.1) | el contexto, la situación de discurso | el tratado, el compendio |

**`vibhatti` es el peligroso**, del calibre de `vyañjana` y `sutta`: en una
gramática pāḷi vibhatti es la desinencia y nada más, y aquí no tiene ninguna
relación con la flexión — es el sentido etimológico de reparto, el que está
detrás del título del Vibhaṅga.

**Y `vyañjana` sube a CUATRO acepciones** en cinco páginas: la consonante de
Nandisena, la Expresión frente al Sentido (6.0.3), la variación sufijal
(6.1.1.3) y ahora **el SINTAGMA** (6.2.1). El aviso de la sesión 49 se queda
corto. Lo mismo `kicca`, que va por cuatro.

### Lo que el cotejo CONFIRMÓ, que en esta tanda es lo más

Y conviene recordar el aviso del briefing 46: **las dos fuentes no son testigos
independientes**, porque Nandisena declara que le fue «muy útil» el Conspectus.
Cuando coinciden, eso es filiación, no confirmación cruzada. Coinciden mucho:

- **`vācogadhapada`**: Nandisena da «parte del lenguaje. Hay 4 partes del
  lenguaje: nombre, verbo, prefijo y partícula» — las cuatro de Smith, en el
  mismo orden.
- **`padajāti`**: lo mismo, con «indeclinable» donde Smith dice «partícula».
- **`samānasuti`**: «que tiene el mismo sonido; homónimo». Exacto.
- **`padesapariyosāna`**: «extensión limitada», y **remite a vākya**, como Smith.
- **`tulyādhikaraṇa`**: da la misma pareja, «También samānādhikaraṇa».
- **`anvācaya`**: coincide y añade lo que a Smith le falta aquí — es «una de las
  funciones de la partícula ca».
- **`vākya`**: «oración; frase. Es el opuesto de samāsa».
- **`padasamūha`**, **`dhātu`**, **`paccaya`**, **`abhidhāna`**: coinciden.

### Y una divergencia de FONDO, que no es homonimia

**`dabba` (6.1.1.1).** Los dos dicen «sustancia», pero la TERNA no es la misma:
para Smith, dabba / guṇa / kiriyā son los tres contenidos del `atthaniddesa`;
para Nandisena, dabba es «una de las tres propiedades del tema (liṅgattha)», y
esas tres son **satti, dabba y liṅga**. Misma palabra, dos ternas. Anotado en la
ficha, sin tocar ninguna de las dos definiciones.

---

## 7. Cosas de la transcripción, para seguir

- **Lema partido ENTRE PÁGINAS**, y esta vez dos: `Atthasaddacintā`
  («Atthasadda-» al pie de la 1136, «cintā» al abrir la 1137) y el `vākya ⟨=
  pada-/samūha)` de §5. Como el `lokiyamahājana` de la sesión 49, **la ficha
  vive en la página donde la palabra se completa**.
- **Lemas fundidos por caer dos veces en el mismo epígrafe**, que el generador
  no admite: `padatthuti` (6.1.1.3, entre la 1135 y la 1136; la ficha vive en la
  1135) y `attha` (6.1.3.1, entre la 1136 y la 1137; la ficha vive en la 1136 y
  el segundo valor se explica en la de `kicca` de la 1137).
- **Paréntesis dentro de palabra, que son abreviaturas**: `ekasuti(ka)`
  (p. 1136), `punarutti(dosa)` y `maṅgala(vacana)` (p. 1138). Las formas
  desplegadas van en `variantes`.
- **Expresiones de varias palabras**: `eko a-dutiyo`, `eko yeva attho vyañjanaṃ
  nānaṃ`, `atthato ninnānākaraṇaṃ`, `samānasutikapadānaṃ atthuddharaṇaṃ`,
  `sesaṃ katvā vācaṃ bhaṇati`, `sarūpānam akkharānaṃ ekaseso`.
- **Rótulos LATINOS verbatim en los tres idiomas**, como en 5.1.1.3 y 5.2:
  *definiendum* (p. 1135), *verbum infinitum* (p. 1138).
- **Formas flexionadas como están impresas**: `cattāri vācogadhapadāni`,
  `abhidhānāni`, `pariyāyavacanāni`, `nāmāni`, `aññamañña-vevacanāni` (plurales),
  `vyañjanavasena`, `upasaggavasena`, `atthavasena`, `uttarapadalopena`,
  `samāsabalena` (instrumentales adverbiales), `atthato` (ablativo), `ekaseso`
  (nominativo), `paṭicca` (absolutivo usado como término). El tema va en
  `variantes`.
- **Los ejemplos canónicos NO se lematizan.** Las ristras del Dhammasaṅgaṇī de
  la p. 1135 (phasso, phusanā, ussoḷhi, paññāratanaṃ…) y los homónimos de la
  p. 1137 (devo, santo, samatto, akataññū) son vocabulario, no terminología, y
  van dentro del `fr`/`es`/`en` de la ficha que los trae.
- **Smith numera las acepciones con superíndice**: `³santo`, `¹⁻²samatto`,
  `¹akataññū : ²akataññū`. Se transcriben como están impresos.
- **El ⊃ sigue siendo su «es decir»**, y en estas páginas hace trabajo pesado:
  `attha (⊃: kicca)`, `adhippāya (⊃: analyses)`, y el ⊃ de `aparadipanā` que
  introduce una glosa entera del comentario.

---

## 8. Cómo se sigue, en concreto

    # la página impresa N del ejemplar del IEBH (hoja = N − 1104)
    pdfimages -j -f $((N-1104)) -l $((N-1104)) \
      recursos/saddaniti/conspectus-ejemplar-angel.pdf /tmp/p

    # el cuerpo de la obra, para verificar referencias
    python3 herramientas/pagina_saddaniti.py 911

    python3 herramientas/generar_glosario.py

Lo que funcionó esta sesión:

1. **Leer la página entera en 6-7 bandas horizontales** sobre la imagen nueva,
   a escala 1,5-1,6×. Con el ejemplar del IEBH esto basta para casi todo; con el
   escaneo de archive.org había que bajar además a línea por línea.
2. **Para una cantidad vocálica o un punto suscrito, recortar la palabra sola y
   ampliar ×8**, y —esto es lo que decide— **buscar en la MISMA LÍNEA una letra
   de control**: un i con punto seguro al lado de la i dudosa. Así se resolvió
   `vīcchā` contra `pariccheda`, y `aparadipanā` contra su propia ā.
3. **Verificar las referencias abriendo el pasaje**, que además de confirmar el
   subíndice suele dar la fuente entera de lo que Smith resume: la p. 32 explicó
   6.1.3.1, la p. 911 explicó 6.1.1.1 y de paso resolvió el `vibhatyanta` de la
   1134.
4. **No usar `pdftoppm` sobre el PDF del IEBH**: las cajas de página no son
   uniformes y reescala mal. `pdfimages -j` da el JPEG nativo al instante.

---

## 9. Lo que sigue pendiente, y no se ha tocado

1. **`.gitignore` y el PDF del IEBH.** Es lo más urgente de esta lista, porque
   es lo único irrecuperable: ver §2. Decisión suya.
2. **Rehacer el cotejo con el Diplomado cuando estén las 44 páginas.** Sin
   cambios desde la sesión 46. **No debe correrse hasta el final.**
3. **Repasar las ī de las páginas 1105-1115** —y ahora también las de 1116-1134,
   con el ejemplar del IEBH delante, que es lo que hace la revisión posible—.
   Las 27 fichas con `duda` son el punto de partida y están todas marcadas.
4. **Las tres fichas que la sesión 50 deja SABIENDO más de lo que dicen**, y que
   sólo IEBH puede mandar actualizar: `vicchā` en las pp. 1120 y 1124 (§3.1),
   `antojappana, ns` en la p. 1120 (§3.2) y `vibhatyanta : avibhatyanta` en la
   p. 1134 (§4).
5. **La tarjeta de `/recursos/`**: la página existe y no está enlazada. Falta el
   visto bueno del IEBH (`herramientas/generar_indices.py`, y su copia inglesa).
6. **El guion `herramientas/pagina_saddaniti.py`** sigue a la espera del visto
   bueno, como decía el briefing 49 §2.
7. **Buscar la lista de siglas de Smith** en los preliminares del vol. 01, para
   cerrar `mṭ` y confirmar `ns` documentalmente.
8. Las decisiones del IEBH que siguen abiertas: **lahu** («leve» frente al
   «breve» del Diplomado), **niggahita/niggahīta**, **ensanchar āgama**, el
   `sukkhuccāraṇatthaṃ` de la p. 1108, el `avadhārana` de la p. 1119, el
   `saddhammaniti` de la p. 1131, el `tathāgatādāya` de la p. 1130 —que ahora SÍ
   se puede cotejar contra su ejemplar— y las tres notas de paradigmas que dicen
   «con el visto bueno del IEBH» donde la norma pide «el IEBH».

---

## 10. Cifras al cerrar

| | |
| --- | --- |
| páginas del Conspectus | **34 de 44** (1105-1138) |
| términos del Conspectus | **1.384** (eran 1.252) |
| entradas de Nandisena | 649 |
| normativos de `comun/glosario.md` | 53 |
| en las dos fuentes | 364 (26 %) |
| fichas con `conflicto` | 40 (eran 29) |
| fichas con `duda` | 27 (eran 18) |
| referencias verificadas contra la fuente | 6 nuevas, ninguna corregida |
| lecturas corregidas por el ejemplar del IEBH | 2 (`139,16`, `685,20`) |
| dudas cerradas por el ejemplar del IEBH | 4 |
