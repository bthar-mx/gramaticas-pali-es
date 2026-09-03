# Kaccāyana Pāḷi-Español: Briefing de la Sesión 44

*Complementa a los briefings 05–43. Tema de la sesión 44 (2026-09-02): **cerrar
lo que dejó abierto la sesión de la licencia**. Se comprueba el enganche de
Zenodo, se hace por fin la revisión visual en un navegador de verdad, se
reescribe la descripción del depósito, el título pasa a
**Kaccāyana-byākaraṇa** y se prepara la versión **2.0.0**. No se ha tocado el
texto de ninguna gramática ni el motor.*

> **Lo primero que tiene que saber el chat nuevo: la 2.0.0 ESTÁ PUBLICADA.**
> Angel etiquetó y publicó la entrega en GitHub, Zenodo la archivó, y el DOI de
> concepto `10.5281/zenodo.21948010` resuelve ya a la versión nueva:
>
> | | |
> | --- | --- |
> | DOI de la 2.0.0 | `10.5281/zenodo.22263057` |
> | título | Kaccāyana-byākaraṇa — traducción española |
> | licencia | **CC BY-NC-ND 4.0** |
> | archivo | `bthar-mx/gramaticas-pali-es-v2.0.0.zip` |
>
> **Queda una cosa por vigilar y está en §7 bis: la pestaña GitHub de Zenodo
> dice «Connect», como si el enlace se hubiera soltado.** No impidió esta
> entrega, pero podría impedir la siguiente.
>
> **Y la regla que gobernó la sesión, que es la de siempre:** proponer y
> verificar, nunca afirmar. Se aplicó a la revisión visual y **cazó dos errores
> míos**, no del sitio. Están en §3.

## 0. LO QUE CAMBIÓ, EN UNA TABLA

| | antes | después |
| --- | --- | --- |
| título del depósito | Kaccāyana-**v**yākaraṇa | **Kaccāyana-byākaraṇa** |
| versión en `.zenodo.json` y `CITATION.cff` | 1.1.0 | **2.0.0** |
| descripción del depósito | los tres capítulos | **+ el aparato de referencia** |
| revisión visual de los pliegues | sin hacer | **hecha, 9 páginas × 3 modos** |
| enganche de Zenodo | sin comprobar | **comprobado, intacto** |
| «vyākaraṇa» en el repositorio | 9 apariciones | **0: todas a «byākaraṇa»** |
| estado | | **`main` desplegado; falta la etiqueta** |

## 1. ZENODO: EL ENGANCHE ESTÁ BIEN, Y SE CIERRA EL PUNTO 2 DEL BRIEFING 43

El miedo del briefing 43 —que el webhook se hubiera quedado en `admin-iebh`
mientras Angel empuja a `bthar-mx`, y que la próxima versión no se archivara—
**no se cumple**. Lo comprobado, con la sesión de Angel abierta:

- En `bthar-mx/gramaticas-pali-es` → Settings → Webhooks hay un hook vivo a
  `https://zenodo.org/api/hooks/receivers/github/events/`, evento `release`,
  con el rótulo **«This hook has never been triggered»**. Nunca se ha disparado
  porque no se ha etiquetado nada desde el traslado.
- En Zenodo → GitHub, **Enabled Repositories** lista
  `bthar-mx/gramaticas-pali-es`, pero su enlace y su interruptor lo direccionan
  por dentro como `admin-iebh/gramaticas-pali-es`. La URL con `bthar-mx` da 404;
  la de `admin-iebh` carga, y **contiene las dos entregas con sus DOI**:

      v1.0.0   10.5281/zenodo.21948011   Published
      v1.1.0   10.5281/zenodo.22037060   Published

**Es UN registro, no dos.** Zenodo siguió el traslado por el id numérico del
repositorio de GitHub y sólo cambió el nombre que muestra. De ahí lo que
importa: **la próxima entrega entra como tercera versión bajo el DOI de
concepto `10.5281/zenodo.21948010`**, y el DOI de `CITATION.cff` sigue
resolviendo. No se acuña un DOI de concepto nuevo.

El segundo portillo —que una organización nueva bloquee el acceso de terceros—
**también está pasado**: Zenodo avisa de que los repositorios de una
organización no aparecen en la lista sin ese permiso, y aparecen los dos de
`bthar-mx` (éste y `OSBCT`).

**Lo que sigue sin demostrarse** es el viaje completo, porque el hook no se ha
disparado nunca. La etiqueta `v2.0.0` es esa prueba. Si falla, falla a la vista
y en el acto.

**Angel sincronizó Zenodo durante la sesión** («Sync now»), de modo que ese paso
está hecho.

## 2. LA REVISIÓN VISUAL: LOS PLIEGUES ESTÁN BIEN

Se cierra el punto 3 del briefing 43. Nueve páginas —las seis de `recursos/` y
los tres índices— en claro, en oscuro y a 375 px, midiendo el contraste por
cómputo y no a ojo.

**Lo que había que comprobar, está bien:**

- **La licencia queda fuera del pliegue en las nueve.** Comprobado por DOM
  (`closest('details')` devuelve nulo), no por inspección visual.
- **Contraste del pie y de los índices:** 5,49–11,75 en oscuro; 4,57–7,08 en
  claro. Todo por encima del 4,5 de la WCAG AA.
- **Ningún pie se desborda a 375 px.**

## 3. DOS ERRORES MÍOS, ANOTADOS COMO MANDA LA CASA

Los dos son del mismo tipo: **medí mal y lo dije como si fuera un fallo del
sitio.** Los dos los cazó el mirar el código antes de tocarlo.

**1. «La portada tiene el inglés en español.»** Falso. Mi sonda leía el
`innerText` del `<p>` padre, que sólo devuelve el tramo **visible** —el
español—, y por eso los dos idiomas salían iguales. Leído el `.i-en` por su
propio `textContent`, dice lo que debe: *«Published under licence CC BY-NC-ND
4.0»*. `generar_indices.py` estaba bien, y las tres páginas generadas son
idénticas entre sí. **No se tocó nada.**

**2. «En paradigmas se desbordan las tablas.»** Falso también. La tabla ya
rodaba sola: `.tbl{display:block;overflow-x:auto}` estaba puesto y funcionaba
(331 px de ancho útil). Quien empujaba la página era **la fila `.meta` de la
cabecera de cada ficha** —«Copiar» y «doc ↗»—, con `flex-wrap:nowrap` y
`white-space:nowrap`, que llegaba a 459 px en una pantalla de 375.

La moraleja es la del proyecto y conviene dejarla escrita: **una medición que
no se ha verificado contra la fuente es una propuesta, no un hallazgo.**

## 4. LOS TRES ARREGLOS, Y CÓMO SE COMPROBARON

Ninguno se hizo a ciegas: se inyectó el CSS exacto en la página **en vivo** y se
volvió a medir. Los tres números son de antes y después reales.

| Página | Qué pasaba | Arreglo | Medido |
| --- | --- | --- | --- |
| verbo | los rótulos `.sb-sec>summary` usaban `--ochre`, que en claro da **3,55** sobre la barra | variable nueva `--ochre-text:#8A5209` sólo en claro | **3,55 → 4,96** |
| raíces | las 4 pestañas + el enlace a `/verbo/` medían 542 px | `.tabs{overflow-x:auto}` a ≤640 px | **542 → 375** |
| paradigmas | la fila `.meta` no se partía | `flex-wrap:wrap;white-space:normal` a ≤640 px | **459 → 375** |

Dos decisiones de forma que conviene conocer:

- **En raíces la tira rueda, no se parte en dos filas.** Partirla dejaría «El
  verbo ↗» debajo de las pestañas, donde parecería la quinta — que es justo lo
  que evita la nota larga del propio `plantilla.html`.
- **En verbo el oscuro no cambia.** Allí `--ochre` ya daba 6,67; `--ochre-text`
  vale lo mismo que `--ochre` en los dos bloques oscuros.

**`nombre` comparte paleta con `verbo` pero no tiene pestañas plegables**, así
que no le hacía falta y no se tocó.

### Lo que se vio y NO se arregló

`.idx-licencia` lleva un filete de `0.5px` con contraste 1,56 en claro y 1,81 en
oscuro. En una pantalla de 1× puede desaparecer del todo. **No se tocó**: es
decisión de diseño, no defecto, y no se pidió.

## 5. EL TÍTULO: «BYĀKARAṆA»

Decisión de Angel. Cambia en `.zenodo.json` y en `CITATION.cff`, título y
primera línea de la descripción.

**La lectura tiene apoyo en las fuentes del propio repositorio**, y conviene
dejarlo dicho para que nadie lo tome por errata: el Nyāsa escribe
*Kaccāyanabyākaraṇassa* (`docs/fuentes/nyasa/Nyasa-00-prologo-y-matika.md`,
línea 25), la Rūpasiddhi trae *Byākaraṇam adhīte veyyākaraṇiko*, y el índice
del sitio ya decía **Kaccāyana-Byākaraṇaṃ**.

### Y NO ERA SÓLO CONSISTENCIA: LAS CITAS ESTABAN MAL

Angel pidió corregirlo en el resto del repositorio. Antes de hacerlo se miró
una cosa que no era obvia: **cinco de las nueve apariciones no eran el nombre
que el proyecto le da a la obra, sino la CITA BIBLIOGRÁFICA de la edición
base** —«Kaccāyana-vyākaraṇa, ed. y trad. Bhikkhu U Nandisena (ITBMU)»—. Una
cita nombra la fuente como la fuente se titula, así que cambiarla habría sido
citar mal a Nandisena… **si su edición dijera «vyākaraṇa».**

No lo dice. **`docs/1. Sandhi-Kappa.md`, línea 1, el documento de la edición
base, abre con `**KACCĀYANA-BYĀKARAṆAṂ**`.** De modo que la cita era la
equivocada desde el principio, y corregirla no es armonizar: es dejar de
atribuirle a la edición base un título que no usa.

Las nueve apariciones, en siete archivos, quedan en «byākaraṇa»:

| Archivo | Qué era |
| --- | --- |
| `comun/convenciones.md:42` | cita de la edición base |
| `comun/concordancia.json:3` | cita de la edición base |
| `recursos/sandhi/suttavibhaga.json:3` | cita de la fuente |
| `herramientas/generar_indices.py:550,553` | «cómo citar», es y en |
| `README.md:14` | tabla de carpetas |
| `recursos/nombre/plantilla.html:723` | pie visible |
| `recursos/verbo/plantilla.html:676` | pie visible |

**Una cosa se hizo de más, y se dice:** en las palabras clave de `.zenodo.json`
y `CITATION.cff` se puso «byākaraṇa» **y se conservó «vyākaraṇa»** junto a
ella. Una palabra clave no nombra la obra, sirve para encontrarla, y la grafía
con *v* es la corriente en la bibliografía occidental. Si Angel prefiere una
sola, se quita.

## 6. LA DESCRIPCIÓN DEL DEPÓSITO

Decía «La versión 1.1.0 comprende los tres primeros capítulos completos, 315
suttas». Era exacta el 21 de agosto. Desde entonces han entrado **243 commits y
352 archivos**, y el texto de la gramática apenas se movió —una enmienda, la
lectura de *saṃ-sāsu ekavacanesu vibhattādesesu*—: lo que creció fue todo lo
que la rodea, y nada de eso se nombraba.

El borrador cotejado está en `docs/zenodo/descripcion-2.0.0-por-adjudicar.md`,
con **una tabla que traza cada cifra al archivo del que sale**. Ya está
incorporado a los dos archivos de metadatos.

**Dos puntos del borrador quedaron sin respuesta expresa de Angel**, y se
publicaron con lo que el borrador proponía por defecto:

1. **El párrafo de lo que el motor NO resuelve** —1.618 de 2.045 junturas— va
   incluido. Es inusual en un registro académico y **queda archivado con DOI y
   sin marcha atrás**.
2. **`upload_type` sigue en `publication` / `book`.** Con un solucionador, un
   léxico y un worker dentro, cabe preguntarse si 2.0.0 no es ya `software` o un
   depósito mixto. **No se tocó**: cambiarlo altera cómo se cita la obra y cómo
   la indexa OpenAIRE.

Si Angel quiere cualquiera de las dos cosas distinta, **hay que cambiarla antes
de empujar la etiqueta**, no después.

## 7. LO QUE FALTA, Y SON DOS ÓRDENES

**`main` ya está empujado y desplegado hasta `1035d7c`.** Angel lo empujó desde
su Mac durante la sesión, y los tres arreglos se comprobaron **en el sitio en
vivo**: `--ochre-text` llega como `#8A5209` y los rótulos del verbo miden 4,96.

Falta el commit `3d62d4b` —el de «byākaraṇa»— y **la etiqueta `v2.0.0`**, que
está anotada y apunta a él. El entorno de Claude no tiene la clave SSH de
Angel; el intento devolvió `Host key verification failed`.

    git push origin main
    git push origin v2.0.0

### DOS COSAS QUE SALIERON MAL, Y LA SEGUNDA ERA UN ERROR MÍO

**1. La etiqueta remota se adelantó.** Angel tiene `push.followTags`, de modo
que su `git push origin main` subió también `v2.0.0` tal como estaba entonces
—apuntando a `1035d7c`—, un commit por detrás. El segundo intento lo rechazó
GitHub con «tag already exists». Se arregló borrando la remota y volviendo a
subirla:

    git push origin :refs/tags/v2.0.0
    git push origin v2.0.0

**2. Empujar la etiqueta NO archiva nada, y yo dije que sí.** El webhook escucha
el evento `release`, y GitHub lo emite cuando se **publica una Release**, no
cuando se empuja una etiqueta. Por eso el hook seguía diciendo «never been
triggered» después del `git push` de la etiqueta. Lo que dispara Zenodo es:

    gh release create v2.0.0 --verify-tag \
      --title "v2.0.0 — La gramática con su aparato de referencia" \
      --notes-file docs/zenodo/notas-release-v2.0.0.md

**Ésa es la orden irreversible**, no el `git push` de la etiqueta.

## 7 bis. CÓMO QUEDÓ, Y LA SEÑAL QUE HAY QUE VIGILAR

Publicada la Release, Zenodo archivó en el acto. Comprobado en el registro
público:

- El DOI de concepto `10.5281/zenodo.21948010` resuelve a la **2.0.0**.
- Las tres versiones cuelgan del mismo registro: 2.0.0 (`22263057`), 1.1.0
  (`22037060`), 1.0.0 (`21948011`). **El traslado a `bthar-mx` no partió la
  serie**, que era el miedo del briefing 43.
- El zip pasa a llamarse **`bthar-mx/gramaticas-pali-es-v2.0.0.zip`** y el campo
  «Repository URL» dice ya `github.com/bthar-mx/gramaticas-pali-es`: se
  corrigieron solos al archivar.
- Licencia **CC BY-NC-ND 4.0** y título con **byākaraṇa**.
- La descripción nueva llegó entera: se comprueban en la página tanto las 1.698
  raíces como el párrafo de las 2.045 junturas.

**Dos señales que NO son fallos:**

- El hook dice «Last delivery was not successful. Invalid HTTP Response: 409».
  GitHub emite más de un evento por Release y Zenodo responde 409 al duplicado.
  **La primera entrega sí funcionó**, y el registro lo demuestra.

**Y una que SÍ hay que mirar antes de la próxima entrega:**

- **La pestaña GitHub de Zenodo muestra «Connect»**, como si la cuenta ya no
  estuviera enlazada, y `/account/settings/github/repository/...` devolvió un
  error 500. La sesión de Zenodo está abierta (`admin@iebh.org`), de modo que no
  es un cierre de sesión. No afectó a esta entrega —el archivado ya había
  ocurrido—, pero **si el enlace está realmente suelto, la 2.1.0 no se
  archivará**. Antes de la próxima: entrar en Zenodo → GitHub, pulsar «Connect»
  si sigue así, y **Sync now**.

Después conviene mirar tres cosas, por este orden:

1. Que el hook deje de decir «never been triggered» en Settings → Webhooks.
2. Que en Zenodo aparezca **v2.0.0** bajo el mismo registro, con licencia
   **CC BY-NC-ND 4.0** y el título nuevo.
3. Que el DOI de concepto `10.5281/zenodo.21948010` resuelva a la 2.0.0.

Si algo de eso no ocurre, el problema es del enganche y **no** de los metadatos:
éstos ya se validaron aquí.

## 8. EL `index.lock`, OTRA VEZ — Y ESTA VEZ SÉ DE DÓNDE SALE

El briefing 43 §7 lo atribuyó a `ciclo_veredictos.py`. **Esta vez fui yo**, y el
mecanismo es distinto y conviene anotarlo: el sistema de archivos montado en el
entorno de Claude **permite crear pero no borrar**. `git add` crea `index.lock`,
termina, e intenta borrarlo — y el borrado falla con `Operation not permitted`,
dejando el lock de 0 bytes que hace fallar el `git add` siguiente.

    warning: unable to unlink '.git/index.lock': Operation not permitted

Se resolvió pidiendo permiso de borrado para la carpeta. **Para la próxima:** un
`index.lock` de 0 bytes justo después de una orden de git de Claude no es un
proceso vivo ni es la cola de veredictos; es esto.

## 9. LO QUE QUEDA ABIERTO

1. **El enlace de GitHub en Zenodo, que dice «Connect».** §7 bis. Es lo único
   que puede impedir que la próxima entrega se archive, y se comprueba en un
   minuto.
2. **`upload_type` sigue en `publication` / `book`**, ya archivado así en la
   2.0.0. Si se cambia, será desde la 2.1.0 en adelante; las versiones
   depositadas no se editan, por la misma razón que no se editó la licencia de
   las anteriores.
3. **La palabra clave doble**, `byākaraṇa` y `vyākaraṇa`. §5, al final: se
   conservaron las dos a propósito, y basta decirlo para dejar una.
4. **Abrir el pliegue cuando la búsqueda cae dentro.** Ofrecido en la 43, sigue
   sin hacer.
5. **El filete de `.idx-licencia` a 0,5 px.** §4, visto y no tocado.
6. Siguen abiertos, de antes: el permiso de marca del briefing 19, la escalera
   de tamaños de la serifa y las 2.379 terminaciones por cotejar.
