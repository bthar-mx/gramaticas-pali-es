# Kaccāyana Pāḷi-Español: Briefing de la Sesión 23

*Complementa a los briefings 05–22. La sesión 23 tuvo un solo hilo, heredado
del §6 de la 22: **las quince citas pendientes**. Resultó que no estaban
pendientes por ambigüedad sino por un defecto del emparejador. De paso salió
un segundo hilo, la negrita del vutti, que sigue abierto. No se tradujo ni un
sutta nuevo; no se tocó el capítulo 4.*

> **Lo primero que tiene que saber el chat nuevo:** doce de las quince citas
> están puestas y verificadas. Lo que queda abierto es **la negrita**, y en
> concreto una decisión de Angel que bloquea trece líneas: unificar la
> división `Xsv ti` → `Xsv iti`.

---

## 1. ESTADO AL CIERRE

HEAD: **`4aeead1`**, empujado (`origin/main` igual). Comprobado **sin
ejecutar git**, leyendo `.git/refs/heads/main`, `.git/logs/HEAD` y
`.git/refs/remotes/origin/main` como texto plano.

Un solo commit de contenido en toda la sesión:

| Hash | Qué |
| ---- | --- |
| `c06d2e8`/`4e3f72e` | reintentos del hook sobre el commit de la 22 |
| `4aeead1` | **citas, §275 y negrita** ← HEAD |

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

Angel vio que en §66 `Saṃsāsv` y `Ekavacanesv` no van en negrita y pidió
mirar cuántas más había. La fórmula `X (i)ti kimatthaṃ` sale **194 veces**:
189 en el Nāma, 5 en el Kāraka, 0 en el Sandhi. **Treinta y cuatro no
llevaban negrita, todas en el Nāma.**

No es distinción de Nandisena: el mismo lema sale de las dos maneras
(`Vā`, `Se`, `Ato`, `Ekavacanesv`, `Saṃ-sāsv`).

### La causa, con el PDF delante

El PDF imprime **siempre** el locativo contraído:

    PDF       **Yosvī** ti kimatthaṃ?      **Sesesū** ti kimatthaṃ?
    maestro     Yosv iti kimatthaṃ?          Sesesv iti kimatthaṃ?

Es la divergencia de división que Angel ya había decidido en la 22 («manda
el maestro… vale para toda su clase»), y por eso esas líneas no encontraban
sitio. Se añadió a `restituir_negritas.py` un `redividir()` que reescribe la
línea del PDF a la división del maestro.

**Ojo con la dirección de la 'ī'.** La `ī` de `Yosvī` **es** la `i` de `iti`
absorbida por la contracción: al deshacerla, esa letra vuelve a `iti` y sale
de la negrita. Lo que el sutta nombra es `yosu`, no `yosv i`. Se hizo mal
primero —`**Yosv i**ti`— y Angel lo corrigió.

### Lo que se arregló

- **Cuatro lemas restituidos** del PDF: §169, §187, §198, §222.
- **Diez tramos con la negrita mal cerrada**, que se comían la `i` de `iti`.
  Sólo cuatro eran de esta sesión; **cinco eran anteriores** —`Saṃ-sāsv`,
  `Vibhattādesesv`, `Ekavacanesv`, `Ekavacanayosv`, `Aññesv`—, heredados de
  la fase de traducción y nunca vistos.
- **§176**, que iba como `**Etesv ī**ti`: mal el tramo y mal la división.
  Además hacía **fallar la reconstrucción** de `restituir_negritas.py`, que
  quedó otra vez en OK al corregirlo.

### Lo que NO se arregló: §66, que es lo que Angel preguntaba

**Quedan 30 lemas sin negrita.** Dos bloqueos distintos:

1. **`Saṃsāsv` (§63, §66)**: el maestro lo escribe sin guion; el PDF y §62
   traen `Saṃ-sāsv`. Es el punto 3 del §6 de la 22, todavía abierto.
2. **`Ekavacanesv` (§62, §66)**: la línea del PDF es idéntica en los dos
   suttas y el script la descarta por ambigua.

**Se intentó levantar ese reparo y no sale.** Las líneas que se repiten son
las genéricas, aparecen en muchos suttas a la vez, el marcado nuevo se
entrelaza con la negrita que ya está y **la reconstrucción deja de reproducir
el maestro**. Se dio marcha atrás y quedó nota en el código para que nadie lo
reintente igual. Hacerlo bien pide emparejar por contexto de cada aparición,
no «ponerlo en todas».

## 6. LO QUE SIGUE ABIERTO

### La decisión que desbloquea más

1. **Unificar `Xsv ti` → `Xsv iti` en trece sitios** —§88 ×2, §89, §92, §93,
   §96, §97, §127, §132, §133, §147, §155, §222—. El maestro tiene ahí una
   tercera forma que no es ni la de Nandisena (`Yosvī ti`) ni la decidida
   (`Yosv iti`): le falta la `i` entera. Unificarla les devolvería la negrita
   desde el PDF. **Cambia el pāḷi, así que no se tocó.** Se le planteó a
   Angel y no llegó a contestarlo.
2. **El guion de `Saṃsāsv`** (§63, §66) — punto 3 del §6 de la 22.
3. **El reparo de ambigüedad**, si se quiere §66 entero.
4. **53 líneas ausentes** en el informe de negritas, casi todas por defectos
   de la capa de texto del PDF (macrones que se pierden, `s`→`v`). El informe
   ya las lista enteras.

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
- **El color de la negrita de los ejemplos**: Angel preguntó si convenía
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
- **Con Angel se habla en inglés**; el producto —sitio, mensajes de commit,
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
  `i`— las cazó Angel, no la máquina.
