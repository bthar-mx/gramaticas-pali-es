# Briefing de la sesión 48 — el Conspectus, páginas 1125-1131

**Fecha:** 2026-09-03. **Estado:** 27 de las 44 páginas transcritas (1105-1131).
**Lo que hay que hacer:** seguir por la página 1132.

Este briefing supone leídos los de las sesiones 46 y 47, que siguen vigentes en
todo lo que no se corrija aquí: qué es la obra, las cuatro fuentes, el reparto
de Smith por materias, cómo se transcribe y las decisiones ya cerradas.

---

## 1. Lo hecho

Siete páginas nuevas, 261 términos, de 828 a 1.089. El generador publica limpio.

| pág. | epígrafes | materia |
| --- | --- | --- |
| 1125 | 5.2.2.2-5.2.3 | kammadhāraya, digu, upapadasamāsa; empieza el bahubbīhi |
| 1126 | 5.2.3, 5.2.4, 5.2.5 | fin del bahubbīhi; el dvanda; la reiteración |
| 1127 | 5.2.5, 5.3.1 | fin de la reiteración; **empieza la frase** |
| 1128 | 5.3.2.1, 5.3.2.2 | los marcos del texto; la pregunta |
| 1129 | 5.3.2.2, 5.3.2.3 | las dos seises de la desanā; **el debate y la lógica** |
| 1130 | 5.3.2.3, 5.3.3.1 | fin de las 32 tantiyutti y de las tres kathā; **la transmisión** |
| 1131 | 5.3.3.1, 5.3.3.2 | las divisiones del canon; **la lengua del canon** |

La 1131 se corta en «au courant de l'usage vohāra du monde lokiyama-»: **la
1132 sigue dentro de 5.3.3.2**.

---

## 2. LO PRINCIPAL DE ESTA SESIÓN: LAS REFERENCIAS SE PUEDEN VERIFICAR

Y conviene hacerlo, porque **los subíndices de línea no se leen con seguridad a
400 dpi**. Son cifras de cuerpo pequeñísimo y el escaneo no da para más; el 3 y
el 5, o el 0 y el 6, se confunden.

**El remedio es que la referencia apunta a un sitio que tenemos.** Las páginas
que Smith cita —744, 750, 755, 758, 761, 766, 777, 780, 844— están en los
mismos PDF del repositorio, y basta abrir la página y contar las líneas del
margen para saber si el número es el que se leyó.

    # la p. N del vol. III es la hoja N-593
    pdftoppm -r 300 -f $((N-593)) -l $((N-593)) -png -singlefile \
      recursos/saddaniti/saddaniti-smith-03.pdf /ruta/sN

Los volúmenes y sus desfases, medidos con los `.paginas.json`:

| vol. | páginas impresas | hoja = impresa − |
| --- | --- | --- |
| 01 | 2-314 | 14 |
| 02 | 316-602 | 307 |
| 03 | 604-928 | **593** |
| 04 | 930-1172 | **921** |
| 05 | 1174-1460 | 1166 |

### Cuatro referencias verificadas así, y una corregida

- **755,11—15** (nicca, 5.2.2.4). El subíndice se leía «13 o 15» y no había
  manera. La p. 755 lo resuelve: la línea 11 empieza «evamādi. Upapadasamāse
  niccam eva samāsavidhi na vākyaṃ» y el pasaje se cierra en la 15, «dhammacārī
  icc ādi, dutiyātappuriso 'yaṃ». **Es 11—15.**
- **761,11—16** (tipadabahubbīhi, 5.2.3). La p. 761 abre la línea 11 con
  «Tipado yathā:» y los ejemplos llegan a la 16.
- **766,7—20 y 766,21—767,6** (dukkaramagga y durājānamagga, 5.2.3). En la
  p. 766, la línea 7 empieza «Chando jāto yassa so 'yaṃ chandajāto», con «ayaṃ
  dukkaramaggo nāma bahubbīhi» en las líneas 15-16 y el cierre en la 20; la
  línea 21 empieza «Ahaṃ dīpo etesan ti maṃdīpā, ayaṃ durājānamaggo nāma
  bahubbīhi». Las dos referencias caen exactamente donde Smith dice.
- **750,16—751,11** (la serie de los siete conjuntos del samāhāra, 5.2.4). La
  línea 16 de la p. 750 es el sutta 700 entero: «Dvande
  pāṇituriyayoggasenaṅga-khuddajantuka-vividhaviruddhavisabhāgatthādinañ ca».
  De propina, confirma **una a una** las siete voces del Conspectus
  —pāṇiyaṅga, turiyaṅga, yoggaṅga, senaṅga, khuddajantuka, vividhaviruddha,
  vividhavisabhāga—, que allí salen con sus ejemplos.

**Las fichas afectadas lo dicen** («VERIFICADO CONTRA LA FUENTE»), con la cita
de la línea. Las demás referencias de estas siete páginas van leídas de la
imagen, y no se han cotejado: **quien las necesite, que las compruebe así**.

---

## 3. Los paréntesis: la distinción ⟨ ⟩ / ( ) NO es la que parecía

La sesión 47 anotó que los paréntesis angulares traen a Moggallāna. **Sigue
siendo cierto, pero no al revés**: hay terminología moggallánica que Smith
imprime entre paréntesis REDONDOS.

Comprobado a 400 dpi, comparando la forma del signo con la del paréntesis
vecino:

| dónde | qué | signo |
| --- | --- | --- |
| 5.2.2.3, p. 1125 | saṃkhyādi (el digu de Moggallāna) | **redondo** |
| 5.2.3, p. 1125 | aññatthe (el bahubbīhi de Moggallāna) | **redondo** |
| 5.2.2.4, p. 1125 | vutti yeva III 10 | **redondo** |
| 5.2.3, p. 1126 | vyadhikaraṇa- | **ANGULAR** |
| 5.2.4, p. 1126 | ennemis naturels niccaverin | **ANGULAR** |

De modo que **el paréntesis angular garantiza que es Moggallāna, pero el
redondo no garantiza que no lo sea**. En estas páginas la marca fiable de
Moggallāna es la CITA por libro y sutta —III 10, I 54, y el ⟨casaddattha III,
23⟩ de páginas anteriores—, y ésa va indistintamente entre unos u otros.

---

## 4. Erratas y rarezas nuevas, ninguna corregida por cuenta propia

- **`avadhāraṇapubbapada` con ṇ (5.2.2.2, p. 1125), y descarga a la p. 1119.**
  Aquí el punto suscrito se ve limpio a 400 dpi. En 4.2.3.2 (p. 1119) Smith
  imprimía `avadhārana` con n dental, contra la regla de la ṇ tras r, y aquella
  ficha lo dejó con `duda`. **Esta página es cotejo interno a favor de que la de
  la 1119 sea errata de la edición.** Corregirla sigue siendo decisión de Angel;
  la ficha de 1119 no se ha tocado. Es el mismo tipo de hallazgo que el
  `asukhuccāraṇa` de la sesión 47.
- **`sogatamata` con o (5.3.3.1, p. 1130)**, en la misma serie y una línea
  después de `sugatasāsana` con u. Comprobado a 400 dpi. Puede ser deliberado
  —sogata sería el derivado con vuddhi, como el saugata sánscrito— o errata. Va
  con `duda`.
- **`tathāgatādāya` (5.3.3.1, p. 1130).** Leído letra por letra a 400 dpi. Un
  `-ādāya` en una serie de sinónimos de «la palabra del Buddha» no se explica;
  cabría esperar `tathāgatādesa`, `tathāgatavacana` o `tathāgatādayo`. Va con
  `duda`, **para cotejar con otro ejemplar del impreso**.
- **`anuprāsa` sin corchetes (5.3.1, p. 1127).** Es forma SÁNSCRITA —el grupo
  `pr` no existe en pāḷi, cuya forma sería `anuppāsa`—, y Smith declara en 4.1
  que los corchetes traen el sánscrito, como hace con `[āmreḍitasamāsa]`,
  `[udātta]` y `[śāstra]`. Aquí no los pone. Va con `duda`.
- **`saddhammaniti` (5.3.3.2, p. 1131)**, donde cabría esperar `saddhammanīti`,
  con el mismo `-nīti` de la obra que se está indizando. Va con `duda`, por la
  regla de la ī.
- **El signo ‖ (5.3.2.3, p. 1129)**, que Smith pone tras `hāra` y tras `naya`,
  no está explicado en lo transcrito. Queda registrado sin interpretar, como el
  `ns` de 5.1.0 (p. 1120).
- **`Magadha(vohāra)` sin macrón (5.3.3.2, p. 1131)**, y `Māgadhikā bhāsā` con
  él en la línea siguiente. Comprobado a 400 dpi. No es descuido: el primero es
  el país, el segundo el adjetivo.

### Y una cosa que Smith distingue tipográficamente y conviene no borrar

En 5.3.3.1 (p. 1130) escribe `pāḷi`, con diacríticos, para el TEXTO canónico
frente al comentario; en 5.3.3.2 (p. 1131) escribe «Pali», entre comillas y sin
diacríticos, a la europea, para la LENGUA. Son dos usos y él los separa.

---

## 5. Homónimos nuevos, y cómo salieron

Se corrió el cotejo con Nandisena sobre los 261 términos nuevos, término a
término, mirando las dos definiciones lado a lado. **Salieron siete trampas**,
todas marcadas con `conflicto`:

| término | Smith | Nandisena |
| --- | --- | --- |
| **sutta** (5.3.2.1, 5.3.3.1) | el sermón del canon | «aforismo; regla gramatical» |
| **vagga** (5.3.3.1) | la sección de un nikāya | «las consonantes agrupadas», los cinco grupos |
| **nipāta** (5.3.3.1) | la sección numérica del Aṅguttara | la partícula |
| **yoga** (5.3.2.3) | la combinación de dos enunciados | «regla gramatical; aforismo» |
| **adhikaraṇa** (5.3.2.3) | la delimitación del problema | el caso locativo; la concordancia |
| **kicca-** (5.3.2.2) | la pregunta por el fin | los sufijos kicca de la morfología |
| **sarūpa-** (5.3.2.2) | la pregunta por la definición | «similar», opuesto a asarūpa |
| **jāti** (5.3.2.3) | el argumento especioso de la lógica | «especie; categoría; clase» |
| **ākāra** (5.3.2.2) | el fraccionamiento | «la letra ā» — y es ya el TERCER sentido |

**`sutta` y `vagga` son los serios**, porque los dos sentidos son de manual en
un libro de gramática y el lector desprevenido tomará el que no es.

**El cotejo también confirmó algo, y eso también vale.** Nandisena define
`pubbapadatthapadhāna` como «tipo de compuesto adverbial (abyayībhāva) donde el
primer miembro es predominante»: es decir, que Smith se lo aplique al digu es
una anomalía real, y por eso él le pone un «(!)». La ficha lo recoge.

Merece la pena **repetir este cotejo al cerrar cada tanda de páginas**. El
guion está en la sesión: casa por `desnudo()` e imprime las dos definiciones
recortadas, y las trampas saltan a la vista.

---

## 6. Cosas de la transcripción, para seguir

- **Los paréntesis DENTRO de una palabra son abreviaturas de Smith**, y se
  transcriben como están impresos: `acchar(iy)a` (5.2.5, p. 1127) recoge
  acchara y acchariya; `(paṭhama-)paññatti` (5.3.2.1, p. 1128), paññatti y
  paṭhamapaññatti; `upanaya(na)` (5.3.2.3, p. 1129); `Magadha(vohāra)`
  (5.3.3.2, p. 1131). Las formas desplegadas van en `variantes`. El generador
  admite el paréntesis en el lema: comprobado.
- **Las formas flexionadas van como están impresas**, siguiendo lo que ya se
  hizo con `păpuṇīyate` y con `kattar`: `guṇavācakassa` y `kiriyāpadassa` en
  genitivo, `dviruttavasena` en instrumental, `atthantarābhāve` en locativo,
  `khuddakāni` en plural. El tema va en `variantes`.
- **Y las expresiones de varias palabras, también**: `siliṭṭhaṃ vacanaṃ`,
  `pañcāvayavaṃ vākyaṃ`, `battiṃsa tantiyuttiyo`, `tisso kathā`, `āhacca
  bhāsitaṃ`, `tepiṭakaṃ buddhavacanaṃ`, `satthu sāsanaṃ`, `tantiṃ āropeti`,
  `Māgadhikā bhāsā`, `adiṭṭhajotanā pucchā`. Smith compone unas y deja sueltas
  otras, a veces en la misma línea, y la diferencia se conserva.
- **El mismo lema dos veces en un epígrafe no lo admite el generador**, y esta
  vez pasó cuatro veces; las cuatro se resolvieron fundiendo las apariciones en
  una ficha que lo advierte: `padabhājanīya` (5.3.2.1), `nigamana` (5.3.2.3),
  `chala` (5.3.2.3) y `paṭikkhepa` (5.3.2.3, **y a caballo entre la p. 1129 y la
  1130** — la ficha vive en la 1129).
- **Smith sigue abreviando el segundo miembro de las series** con guión, y se
  transcribe abreviado: `kicca-`, `sarūpa-`, `vatthu-` por -pucchā (5.3.2.2);
  `tappurisagabbha-`, `kammadhārayagabbha-` y los demás por -bahubbīhi
  (5.2.3); `-sāsana` por pariyattisāsana (5.3.3.1). Una ficha cabecera lo
  explica en cada serie.
- **Los corchetes siguen trayendo el sánscrito**: `[āmreḍitasamāsa]`,
  `[udātta]` (5.2.5, p. 1126), `[śāstra]` (5.3.2.3, p. 1129) — salvo el
  `Dhs [6.1.1.3]` de la p. 1127, que es remisión interna, y salvo el `anuprāsa`
  de §4.
- **El ⊃ de Smith reaparece** en 5.3.3.2 (p. 1131), y esta vez con dos puntos:
  «chandaso (⊃: vācanāmaggaṃ) āropetuṃ».
- **La p. 1127 es sobre todo prosa francesa** sobre el orden de palabras, con
  muchas referencias al canon (M I 68, J VI 532, CPD, Sp, Dhs, Vibh, Nidd) y
  pocos términos pāḷi. No es un fallo de la transcripción: la página es así.
- **La ī de `vicchā` se dejó ver.** En 5.2.5 (p. 1127), en la línea «la valeur
  distributive vicchā», el signo sobre la i es un cuadrado corto y el de la ā
  final una regla que desborda la letra, y a 400 dpi se ven uno al lado del
  otro. Confirma lo que Angel fijó en la sesión 47. **Pero la regla general no
  cambia:** donde la imagen no decide, decide la lengua, y se dice.

---

## 7. Cómo se sigue, en concreto

    # imagen de la página impresa N (la N-921 del PDF del vol. 04)
    pdftoppm -r 400 -f $((N-921)) -l $((N-921)) -png -singlefile \
      recursos/saddaniti/saddaniti-smith-04.pdf /ruta/pNNNN

    python3 herramientas/generar_glosario.py

Lo que ahorró más tiempo esta sesión: **recortar la página en cinco bandas
horizontales de unos 600 px a 0,8 de escala** y leerlas seguidas, en vez de
tantear coordenadas; y, para una duda concreta, localizar la línea por perfil
de tinta y recortarla entera.

    rows=(np.array(img.convert('L'))<140).sum(axis=1)   # rachas > 8 px = líneas

**Ojo:** los índices de esas rachas y las bandas visuales **no se corresponden
uno a uno**, y esta sesión se perdieron varios recortes por darlo por supuesto.
Conviene calcular las rachas y recortar **en el mismo guion**, nunca fiándose de
una lista impresa antes.

---

## 8. Lo que sigue pendiente, y no se ha tocado

1. **Rehacer el cotejo con el Diplomado cuando estén las 44 páginas.** Sin
   cambios desde la sesión 46: se hizo contra 4 páginas y ya falló una vez. **No
   se ha vuelto a correr**, y no debe correrse hasta el final.
2. **Repasar las ī de las páginas 1105-1115** con el criterio de la sesión 47.
   Sigue pendiente.
3. **La tarjeta de `/recursos/`**: la página existe y no está enlazada. Falta el
   visto bueno de Angel (`herramientas/generar_indices.py`, y su copia inglesa).
4. **`conspectus.json`: hecho.** El campo `"estado"` decía «piloto — pp.
   1105-1108» y ahora dice «en curso — pp. 1105-1131». (El generador lo calcula
   y lo sobreescribe en la salida de todos modos.)
5. Las decisiones de Angel que siguen abiertas: **lahu** («leve» frente al
   «breve» del Diplomado), **niggahita/niggahīta**, **ensanchar āgama** —y esta
   sesión da un argumento más: en 5.3.3.1 (p. 1130) āgama es la tradición
   transmitida, no un fonema—, el `sukkhuccāraṇatthaṃ` de la p. 1108, el
   `avadhārana` de la p. 1119, y las tres notas de paradigmas que dicen «con el
   visto bueno de Angel» donde la norma pide «el IEBH».

---

## 9. Cifras al cerrar

| | |
| --- | --- |
| páginas del Conspectus | **27 de 44** (1105-1131) |
| términos del Conspectus | **1.089** (eran 828) |
| entradas de Nandisena | 649 |
| normativos de `comun/glosario.md` | 53 |
| en las dos fuentes | 307 (28 %) |
| fichas con `conflicto` | 20 (eran 11) |
| fichas con `duda` | 12 (eran 6) |
