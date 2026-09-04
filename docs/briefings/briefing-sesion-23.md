# Kaccāyana Pāḷi-Español: Briefing de la Sesión 23

*Complementa a los briefings 05–22. La sesión 23 tuvo un solo hilo, heredado
del §6 de la 22: **las quince citas pendientes**. Resultó que no estaban
pendientes por ambigüedad sino por un defecto del emparejador. De paso salió
un segundo hilo, la negrita del vutti, que quedó a medias. No se tradujo ni un
sutta nuevo; no se tocó el capítulo 4.*

> **Lo primero que tiene que saber el chat nuevo:** doce de las quince citas
> están puestas y verificadas, y §66 —lo que IEBH preguntaba— quedó resuelto.
> Lo que queda abierto es **la negrita de los 26 lemas restantes**, que ya no
> depende de ninguna decisión sino de volver a tener delante el PDF del Nāma.

> **Enmienda del 21 de agosto (sesión 24).** Este briefing se escribió *antes*
> del último commit de la sesión y quedó desfasado en tres puntos: daba §66 por
> no resuelto, el reparo de ambigüedad por revertido y las divisiones `Xsv ti`
> por trece. Las secciones §1, §5 y §6 están corregidas abajo; los párrafos
> tachados por los hechos se han reescrito, no borrado, y se dice en cada caso
> qué decía antes. **Moraleja de procedimiento: el briefing se escribe al
> cerrar, no antes del último commit.**

---

## 1. ESTADO AL CIERRE

HEAD: **`b426955`**, publicado en `origin/main`. Comprobado **sin ejecutar
git**, leyendo `.git/refs/heads/main`, `.git/logs/HEAD` y
`.git/refs/remotes/origin/main` como texto plano.

Dos commits de contenido:

| Hash | Qué |
| ---- | --- |
| `c06d2e8`/`4e3f72e` | reintentos del hook sobre el commit de la 22 |
| `4aeead1` | citas, §275 y negrita |
| `b426955` | **repetida no es ambigua cuando las cuentas cuadran; §66** ← HEAD |

*(Este apartado decía `4aeead1` y «un solo commit». Se escribió antes de que
`b426955` existiera. Es el commit que resuelve §66 y levanta el reparo de
ambigüedad, y sin él las secciones §5 y §6 de abajo no se entienden.)*

## 2. LAS CITAS: NO ERAN AMBIGUAS, EL EMPAREJADOR ESTABA ROTO

El briefing 22 las dio por «sin ancla única». No lo estaban.

`anclas_candidatas` arma el ancla uniendo voces con **un solo espacio**,
pero entre esas voces el maestro imprime comas y puntos —«Duve samaṇā.
Duve»— y `normalizar` comparaba la puntuación al pie de la letra. De modo
que **ningún ancla de más de una voz podía coincidir jamás**: el
emparejador caía siempre al ancla de una sola voz, que casi nunca es única.
Llevaba así desde la sesión 22, también para las 213 que sí colocó.

Corregido —se descarta la puntuación, y también los asteriscos, que desde
`restituir_negritas.py` pueden partir un ancla—, **doce de las quince se
resolvieron solas**, con anclas de hasta seis voces. No hizo falta ordenar
ocurrencias ni adivinar nada.

| | antes | ahora |
| --- | ---: | ---: |
| Nāma | 118 | **128** |
| Kāraka | 95 | **97** |
| Sitio (los tres capítulos) | 222 | **234** |

**Verificado por tres vías:** la reconstrucción del propio script en ambos
capítulos; una segunda pasada resuelve 0, de modo que la operación es
idempotente; y la salida del conversor difiere de los `kaccayana/` previos
**exactamente en esas doce líneas y en nada más**, lo que de paso demuestra
que `kaccayana/` estaba en sincronía con `docs/`.

### Modo `--pendientes`

La edición base no vive en el repositorio, así que sin ella no se puede
repetir la extracción. Pero `citas-canonicas.json` guarda de cada pendiente
su sutta, su cita y las sesenta últimas letras del texto previo, y eso basta:
el ancla nunca pasa de seis voces.

    python3 herramientas/restituir_citas.py --pendientes            # prueba
    python3 herramientas/restituir_citas.py --pendientes --aplicar

Actualiza el JSON al aplicar. Sin eso la operación no sería idempotente: las
resueltas seguirían figurando como pendientes y una segunda pasada las
insertaría por duplicado.

## 3. LO QUE ANGEL DECIDIÓ

- **§132, y con él el criterio de las demás.** Las tres `(DA. i, 58)` sobre
  `Duve samaṇā / Duve brāhmaṇā / Duve janā` van **las tres**: poner sólo la
  primera daría a entender que las otras dos no están atestiguadas.
- **La cita va donde la pone la edición base**, que no es siempre el final de
  la frase. Cuando lo que certifica es la voz ilustrada, va pegada a ella:
  `Duve (DA. i, 58) samaṇā`. Se le ofreció primero la colocación a final de
  frase por un error mío —dije que era lo consistente sin comprobarlo— y él
  la descartó al ver que el maestro ya publicaba tres citas a media frase
  (§130 `Amuṃ (M. i, 210) rājānaṃ passasi`, §173 dos veces). Guía §5.1 bis.
- **Kāraka §275: `jātaka` → `jātakā`.** Corrección a la base, no variante.
- **La negrita acaba en el locativo, no dentro de «iti»**: `**Yosv** iti`,
  nunca `**Yosv i**ti`.

## 4. UNA CUARTA ERRATA DE LA BASE, Y UNA CORRECCIÓN

`brāhamaṇā` (Nandisena) / `brāhmaṇā` (el maestro) bloqueaba la tercera cita
de §132. Se suma a las tres de la 22 en `VARIANTES`. **No se corrige nada**:
se le enseña al emparejador. Guía §5.1 quater.

Distinta es §275, donde **sí se corrige** por decisión expresa. Consecuencia
que conviene no olvidar: la lista de los nueve aṅgas aparece dos veces en
§275 y la base imprimía `jātakā` en una y `jātaka` en la otra —era eso, y
sólo eso, lo que daba ancla única a sus dos citas—. Corregida, **las dos
listas son idénticas** y las dos citas han perdido el ancla. Están puestas y
verificadas, pero una pasada futura de `--base` volverá a darlas por
pendientes. No es un error: es el emparejador negándose a elegir.

## 5. LA NEGRITA DEL VUTTI: HILO ABIERTO

El IEBH vio que en §66 `Saṃsāsv` y `Ekavacanesv` no van en negrita y pidió
mirar cuántas más había. La fórmula `X (i)ti kimatthaṃ` sale **194 veces**:
189 en el Nāma, 5 en el Kāraka, 0 en el Sandhi. **Treinta y cuatro no
llevaban negrita, todas en el Nāma.**

No es distinción de Nandisena: el mismo lema sale de las dos maneras
(`Vā`, `Se`, `Ato`, `Ekavacanesv`, `Saṃ-sāsv`).

### La causa, con el PDF delante

El PDF imprime **siempre** el locativo contraído:

    PDF       **Yosvī** ti kimatthaṃ?      **Sesesū** ti kimatthaṃ?
    maestro     Yosv iti kimatthaṃ?          Sesesv iti kimatthaṃ?

Es la divergencia de división que IEBH ya había decidido en la 22 («manda
el maestro… vale para toda su clase»), y por eso esas líneas no encontraban
sitio. Se añadió a `restituir_negritas.py` un `redividir()` que reescribe la
línea del PDF a la división del maestro.

**Ojo con la dirección de la 'ī'.** La `ī` de `Yosvī` **es** la `i` de `iti`
absorbida por la contracción: al deshacerla, esa letra vuelve a `iti` y sale
de la negrita. Lo que el sutta nombra es `yosu`, no `yosv i`. Se hizo mal
primero —`**Yosv i**ti`— y IEBH lo corrigió.

### Lo que se arregló

- **Cuatro lemas restituidos** del PDF: §169, §187, §198, §222.
- **Diez tramos con la negrita mal cerrada**, que se comían la `i` de `iti`.
  Sólo cuatro eran de esta sesión; **cinco eran anteriores** —`Saṃ-sāsv`,
  `Vibhattādesesv`, `Ekavacanesv`, `Ekavacanayosv`, `Aññesv`—, heredados de
  la fase de traducción y nunca vistos.
- **§176**, que iba como `**Etesv ī**ti`: mal el tramo y mal la división.
  Además hacía **fallar la reconstrucción** de `restituir_negritas.py`, que
  quedó otra vez en OK al corregirlo.

### §66, que es lo que IEBH preguntaba: **resuelto** en `b426955`

*(Este apartado se titulaba «Lo que NO se arregló: §66» y daba 30 lemas
pendientes y dos bloqueos vivos. Lo escribí antes del último commit. Lo que
sigue es lo que de verdad pasó.)*

Los dos bloqueos cayeron, y por la misma vía:

1. **`Saṃsāsv` (§63, §66)** — el maestro lo escribía sin guion frente al
   `Saṃ-sāsv` del PDF y de §62. **Cerrado**: hoy no queda ni una aparición sin
   guion y hay cuatro con él. Con eso muere también el punto 3 del §6 de la 22.
2. **`Ekavacanesv` (§62, §66)** — la línea del PDF es idéntica en los dos
   suttas y el script la descartaba por ambigua. **Reparo levantado.**

**La regla que lo hizo seguro: repetida no es ambigua cuando las cuentas
cuadran.** «Ekavacanesv iti kimatthaṃ? Tāsaṃ, sabbāsaṃ.» sale dos veces en el
PDF y dos veces en el maestro, §62 y §66. No hay nada que adivinar: es una
correspondencia uno a uno que se resuelve por orden.

El primer intento —colocar la línea repetida en *todas* sus apariciones— sí
falló, y es lo que este briefing dio por definitivo: las líneas que se repiten
son las genéricas, salen en muchos más sitios de los que el PDF tiene, el
marcado se entrelaza con la negrita ya puesta y la reconstrucción deja de
reproducir el maestro. **Exigir que las cuentas coincidan descarta esas solas.**
Hicieron falta además dos cosas:

- `restituir_negritas.py` líneas 281-302: la condición `len(hits) ==
  veces_pdf[norm]`, con el porqué comentado en el código.
- Líneas 331-342: descartar el tramo que **pisa a medias** una negrita
  existente. Antes sólo se miraba la coincidencia exacta, de modo que un tramo
  que empezara dentro de una negrita y acabara fuera producía marcado
  entrelazado —`**a**b**c**`— que `pelar` ya no sabe deshacer. Era eso, y no la
  ambigüedad, lo que hacía fallar la reconstrucción.

**Estado real al cierre: 26 lemas sin negrita**, no 30. También se restituyó
**§222** (`**Liṅgādīsv** iti`), que este briefing seguía contando como
pendiente.

## 6. LO QUE SIGUE ABIERTO

### ~~La decisión que desbloquea más~~ · resuelta el 21 de agosto

1. **Unificar `Xsv ti` → `Xsv iti`: HECHO.** Eran **doce**, no trece —§88 ×2,
   §89, §92, §93, §96, §97, §127, §132, §133, §147, §155—; §222 ya lo había
   arreglado `b426955`. El IEBH lo decidió al abrir la sesión 24.

   El maestro tenía ahí una forma que no es ni la de Nandisena (`Yosvī ti`) ni
   la decidida (`Yosv iti`): le falta la `i` entera, y así **no se puede leer**
   —sin esa vocal no queda ningún `iti` que valga—. Es la pérdida de un macrón
   en la capa de texto, la misma avería del punto 4 de abajo, no una variante.

   **La prueba de que no era distinción del maestro: `Etesv`.** Lo imprimía de
   las dos maneras en el mismo capítulo, `Etesv ti` cinco veces y `Etesv iti`
   dos. Igual `Yosv` (5/0), `Katanikāralopesv` (1/0) y `Ve-vosv` (1/0).

   **Cómo se verificó**, ya que cambia el pāḷi: la única diferencia admitida
   entre el maestro de antes y el de después son doce inserciones de `i`. Tres
   comprobaciones lineales, y el script no escribe si alguna falla —la
   diferencia de longitud es exactamente 12; los dos textos son **idénticos al
   quitarles toda la `i`**; y no queda ningún `Xsv ti`—. Las doce líneas
   tocadas coinciden una a una con las doce localizadas antes de tocar nada.

   Ojo: esto **no pone negrita por sí solo**. Prepara el terreno. Los 26 lemas
   siguen en 26 hasta que se vuelva a pasar `restituir_negritas.py`, y para eso
   hace falta el PDF del Nāma, que no vive en el repositorio.
2. ~~**El guion de `Saṃsāsv`** (§63, §66)~~ — **cerrado** en `b426955`, ver §5.
3. ~~**El reparo de ambigüedad**~~ — **levantado** en `b426955`, ver §5.
4. **53 líneas ausentes** en el informe de negritas, casi todas por defectos
   de la capa de texto del PDF (macrones que se pierden, `s`→`v`). El informe
   ya las lista enteras. **Es lo único que sigue vivo de este hilo**, junto con
   los 26 lemas, y ambas cosas piden el PDF delante.

### Nuevo de esta sesión

5. **Tres citas siguen pendientes**, y ninguna es cuestión de colocación:
   **§81** `(Khu. vi, 46, 51)` vive en una nota al pie de Nandisena y
   «Gavaṃ ce» no está en el §81 español; **§308** `(D. ii, 126-7. Piṭṭhesu
   passitabbaṃ)` no es una referencia simple y la base lee `paññato` frente
   al `paññatto` del maestro; **§315** `(Mog.-pañcikā ii, 25)` **ya está
   puesta**, dentro de la nota 30 — ésa se puede cerrar sin más.
6. **`generar_todo.py` no llama a los conversores.** Un cambio en `docs/` no
   llega al sitio hasta correr `convertir_nama.py` / `convertir_karaka.py` a
   mano. Estuvo a punto de costar un despiste serio: los maestros de los
   capítulos 2 y 3 son los de `docs/`, y `kaccayana/` es salida.

### Heredado de la 22, sin tocar

7. **Las 2379 desinencias** de `recursos/paradigmas/paradigmas.json`.
   Candidato a sesión entera.
8. El escaneo del Nyāsa; `docs/fuentes/nyasa/` sin constar en `CLAUDE.md`;
   `pañcamī / sattamī` sin llegar al glosario.
9. Los diecisiete apartados de Thitzana; las seis decisiones del §1.4; la
   zona gris de `Nyasa_errata.md` §3.
10. **El permiso de la marca (briefing 19 §8): sigue sin respuesta.**
11. **El siguiente capítulo a traducir: sin decidir.** Hay que preguntarlo.
12. `docs/1. Sandhi-Kappa.md`, archivo muerto que diverge; la descripción de
    Zenodo; URL más corta; `recursos/nombre/`.

### Cerrado

- Las quince citas del §6.1 de la 22: doce puestas, tres explicadas arriba.
- **El color de la negrita de los ejemplos**: el IEBH preguntó si convenía
  darles también oropimente. **No.** El amarillo entró por un problema
  óptico concreto —irradiación, Gentium sin peso intermedio, y lo marcado
  suele ser una sola letra—, y en las listas de ejemplos la negrita son
  palabras enteras, donde el peso solo se ve. Además el oropimente significa
  hoy una cosa: *esto es la parte del aforismo a la que responde el vutti*.
  Pintar las dos lo dejaría en «negrita en oscuro». Si alguna vez se ve
  floja, la palanca es el contraste, no el tono.

## 7. RECORDATORIOS QUE NO CAMBIAN

- **Ninguna orden de git desde el sandbox, ni siquiera `status`.** Leer
  `.git/refs/heads/main`, `.git/logs/HEAD` y `.git/index` como archivos.
- **Con IEBH se habla en inglés**; el producto —sitio, mensajes de commit,
  comentarios del código, estos briefings— va en español. Se me olvidó a
  mitad de la sesión y tuvo que recordármelo.
- **Los maestros de los capítulos 2 y 3 están en `docs/`**, no en
  `kaccayana/`. El Sandhi es la excepción: su fuente viva es
  `kaccayana/01-sandhi-kappa.md`.
- Tras tocar `pali.css` hay que regenerar; el HTML no lleva huella, así que
  recargar con Cmd+Shift+R.
- Nada se edita dentro de `site/` salvo `pali.css`, `pali.js` y los SVG.
- Lo tomado de Thitzana se señala como suyo; su flecha va al revés.
- Ante duda, `<!-- DUDA: … -->` y decirlo en voz alta.
- **Proponer y verificar, nunca afirmar.** Las dos veces que esta sesión se
  salió de ahí —la colocación a final de frase, la negrita comiéndose la
  `i`— las cazó IEBH, no la máquina.
- **El briefing se escribe cuando ya no se va a tocar nada más.** `CLAUDE.md`
  pide que esté escrito y guardado antes de cerrar; éste lo estuvo *demasiado*
  antes, y dio por abierto lo que el commit siguiente cerró. Un briefing que
  adelanta el cierre manda a la sesión próxima a rehacer trabajo hecho. **Lo
  primero que hace un chat nuevo es comprobar `HEAD` contra el briefing**; si
  no coinciden, manda el árbol.
