# Briefing de la sesión 54 — LA COLACIÓN AVANZA, Y ENCUENTRA UNA SEGUNDA CLASE DE ERROR

**Fecha:** 2026-09-04. **Estado:** la colación va por **13 páginas de 44**,
seguidas de la 1105 a la 1117. El §6 del briefing 53 está en curso y el método
funciona.

Este briefing supone leídos los de las sesiones 46 a 53. El registro detallado,
página por página, está en `docs/glosario/revision-de-las-i.md`, §§4 ter y
siguientes: **ése es el documento que hay que leer antes de tocar nada.**

---

## 1. LO PRIMERO QUE HAY QUE SABER, SI SÓLO SE LEE UN PÁRRAFO

El briefing 53 decía que colacionar encuentra fichas que dan la forma CORRECTA
del pāḷi donde Smith imprime otra cosa. **Eso se confirma —van seis casos— pero
la colación ha sacado además una clase que no estaba prevista: signos que no
dicen cantidad, sino de dónde sale la vocal, y que la transcripción aplana.**

Son el **anceps** —macrón con cazoleta de breve encima— y el **circunflejo** de
contracción. Cuatro perdidos en cinco páginas:

| pág. | plancha | ficha | qué signo |
| ---: | --- | --- | --- |
| 1106 | `ava : o : ū̆` | `ava : o : ū` | anceps |
| 1107 | `vipariyā̆ya` | `vipariyāya` | anceps |
| 1114 | `tassêdaṃ` | `tassedaṃ` | circunflejo |
| 1115 | `nâvisada` | `nāvisada` | circunflejo |

**Y no es criterio, es descuido**, y hay prueba de las dos maneras: en las 1.878
fichas existe UNA sola forma con circunflejo (`tatrâyaṃ gāthā`, p. 1148), de
modo que sí se recoge cuando se ve; y en la p. 1115 **la nota de la ficha vecina
escribe `nâvisada` bien, con circunflejo, mientras el lema lo convierte en
macrón**. El signo se vio al transcribir y se perdió al lematizar.

De ahí **la propuesta que espera decisión de Angel: barrer las 44 páginas
buscando anceps y circunflejos**, en vez de esperar a que la colación llegue a
cada uno. Es un barrido de imagen, no de texto, porque el dato no está en los
datos.

---

## 2. La p. 1110 cierra la duda de lectura del §3 del briefing 53

**Smith imprime `nimantaṇa` y `āmantaṇa`, con Ṇ RETROFLEJA**, y ahora está
verificado en la propia colación, no de paso:

- control interno: `nimantaṇa` tiene tres enes y sólo la última lleva punto;
  `āmantaṇa`, dos y sólo la segunda;
- control externo, misma página y mismo cuerpo: `patthanā` en la línea de
  encima, n dental limpia; `āṇatti` dos líneas arriba, punto de ṇ idéntico;
- comprobado a ×14.

Las dos fichas llevan ya `duda` y los lemas siguen intactos. **Falta la tercera,
el `āmantana` de 5.1.0 (p. 1120)**, que sale al colacionar esa página.

**Lo delicado**: la nota publicada de `āmantana` dice «Smith confirma la lectura
correcta: āmantana», que es lo contrario de lo que imprime. **No se ha
corregido** —corregir lo publicado es de Angel—; queda señalado en la `duda`.

---

## 3. EL FALLO QUE TENÍA LA PÁGINA VACÍA, Y LA LECCIÓN

Del 3 al 4 de septiembre, `/recursos/glosario/` publicó **el armazón sin las
1.878 fichas**. La causa, en `recursos/glosario/plantilla.html`:

    const top = $('#top-btn');

`top` ya existe como propiedad de `window` y no admite redeclaración: es
**SyntaxError en tiempo de análisis**, de modo que no fallaba una función sino
que **no se ejecutaba el guion entero**, y con él la parte que dibuja las
entradas. Introducido en `53b06ad`. Arreglado en `71b58ce` renombrando a
`btnTop`, con el comentario que explica por qué.

**Barrido hecho**: ninguna otra plantilla declara un nombre que choque con
propiedades de `window` (`top`, `self`, `location`, `name`, `length`…).

Dos lecciones que conviene no perder:

1. **Que el dato esté en el HTML desplegado no prueba que la página funcione.**
   Se comprobó lo primero y se dio por buena la publicación; lo que había que
   mirar era si algo se renderizaba. La comprobación correcta es abrir la página
   y contar nodos, o leer la consola.
2. **Comprobar después de cada `push`**, aunque el generador no haya avisado de
   nada. `generar_todo.py` no ejecuta el guion: no puede ver este fallo.

---

## 4. Las trece páginas, y lo que dieron

| pág. | fichas | hallazgos | estado |
| ---: | ---: | ---: | --- |
| 1105 | 22 | 1 | resuelto por Angel |
| 1106 | 50 | 2 + 2 avisos | dos `duda` |
| 1107 | 43 | 1 | una `duda` |
| 1108 | 40 | 1 + 2 avisos | una `duda`; una vieja confirmada |
| 1109 | 46 | 0 | limpia |
| 1110 | 49 | 1 (dos fichas) | dos `duda` |
| 1111 | 43 | 0 | limpia |
| 1112 | 44 | 1 + 2 avisos | una `duda` |
| 1113 | 33 | 0 | limpia |
| 1114 | 49 | 1 | una `duda` |
| 1115 | 38 | 2 | dos `duda` |
| 1116 | 34 | 0 | limpia |
| 1117 | 66 | 1 | resuelto por Angel |

**Proporción real: unos 0,8 hallazgos por página**, cerca de la que el §3.2 de
`revision-de-las-i.md` aventuraba. Cinco páginas de trece salen limpias.

### El hallazgo que más se repite: la ficha se aparta TAMBIÉN de la forma corriente

`īsakaṃ` (pp. 1106 y 1108, dos fichas) y `tassīla` (p. 1112). En los tres casos
Smith imprime el macrón, la ficha da breve, **y la forma con macrón es además la
correcta en pāḷi** —īsakaṃ «un poco»; taṃ + sīla—. No es, por tanto,
normalización callada de una anomalía de Smith, como `samīpa`: es deslizamiento
de transcripción. Conviene distinguir los dos géneros al decidir.

### Y el patrón del `avadhārana`, otra vez

`ārammanabheda` (p. 1115): Smith imprime **n dental**, la ficha da ṇ retrofleja,
y **en la línea siguiente él mismo escribe `puthuārammaṇa` con ṇ**. Igual que el
`avadhārana` de la p. 1119 frente a los tres `avadhāraṇa`. Y, otra vez, el dato
correcto está en la `nota` y la normalización en el lema.

---

## 5. Lo que espera decisión de Angel

Todo está listado en `docs/glosario/revision-de-las-i.md` §5, puntos 7 a 15. En
resumen:

1. **`īsakaṃ`** (pp. 1106 y 1108) y **`tassīla`** (p. 1112) — deslizamientos.
2. **`nimantaṇa` / `āmantaṇa`** (p. 1110) — la ṇ de Smith, y la nota que dice lo
   contrario.
3. **`ārammanabheda`** (p. 1115) — n dental de Smith.
4. **Anceps y circunflejos** — los cuatro, y **si se barren las 44 páginas**.
5. **Cuatro omisiones**: `ekamatta` y `dvimatta` (p. 1106), `chandadīghatā`
   (p. 1108) y **`guṇanāma` de 3.0.2** (p. 1112), que es la de más peso porque
   allí tiene glosa distinta de la de la p. 1111. Más el «(ns)» de `yamaka`
   (p. 1108), que se decide con el `antojappana ns` del §9.3 del briefing 52.
6. **El criterio de lematización de las formas flexionadas**:
   `dūraṭṭhass' ālapane` → `dūraṭṭhassa ālapana` (p. 1106) y ⟨`anvādese`⟩ →
   `anvādesa` (p. 1112), mientras `rassā va vattabbā` se conserva flexionado.
   No es error; es que el criterio no está fijado.

**Ninguna ficha ha cambiado de lema en toda la sesión.**

---

## 6. Lo que el chat que siga tiene que hacer

**Continuar la colación por la p. 1118**, y seguir en orden hasta la 1148
—saltando la 1117, ya hecha—. Van trece.

Cada página, tres cosas, que son las del §6 del briefing 53 y no cambian:

1. colacionar los lemas contra la plancha, **con control en la misma página**;
2. **no tocar ningún lema**: lo que baile se marca con `duda` y se le enseña a
   Angel;
3. anotar el resultado en `docs/glosario/revision-de-las-i.md`.

Y al terminar:

    python3 herramientas/generar_todo.py

### El método, afinado por trece páginas

    pdfimages -j -f N -l N recursos/saddaniti/conspectus-ejemplar-angel.pdf salida

**Hoja = página impresa − 1104.** Lo que se ha aprendido haciéndolo:

- **Leer primero la página entera a media escala.** A la mitad del tamaño
  nativo se detectan ya casi todos los candidatos —`tassīla` y `nâvisada`
  saltaron así—; el aumento sirve para confirmar, no para buscar.
- **Confirmar a ×12–×18, y siempre con un control a la MISMA escala.** El
  macrón es una barra plana ancha que desborda la letra por los dos lados; el
  punto de la i breve es redondo y se apoya en ella; el circunflejo tiene dos
  astas inclinadas; el anceps lleva cazoleta encima de la barra.
- **Cuidado con las motas.** En la p. 1111 el `araha` parece llevar macrón y no
  lo lleva: a ×18 es un grumo estrecho e inclinado. El control decisivo fue
  `pattakāla` en la línea de encima, a la misma escala.
- **Hay hojas que no deciden.** La de la p. 1116 está escaneada más floja que
  las vecinas —1.688 px de ancho frente a 1.908— y la ī de `aṭṭhamī` no se puede
  afirmar desde la imagen. **En ese caso no se afirma**, y se dice por qué.
- **Comprobar el JSON después de cada edición**: `json.load` sobre el archivo.
  Al añadir una `duda` al final de un objeto es fácil comerse el `},`; ha pasado
  dos veces en esta sesión.

### Una advertencia operativa

**No ejecutar `git status` desde el entorno Linux de Claude sobre este
repositorio**: crea `.git/index.lock` y no puede borrarlo por permisos del
montaje, y el siguiente `git commit` de Angel falla. Si hace falta mirar el
estado, `git --no-optional-locks status --porcelain`, que no toma el bloqueo.
`git log` y leer `.git/refs/` son seguros.

---

## 7. Cuánto queda, medido otra vez

| parte | tamaño | estimación |
| --- | --- | --- |
| **colación** | 31 páginas por hacer, a 6-7 por sesión | **≈ 4-5 sesiones** |
| **análisis de las dos fuentes** | 1.608 lemas de Smith, 649 de Nandisena, 284 coincidencias, 61 `conflicto`, 13 casi-coincidencias | **≈ 1-2 sesiones** |
| **las 268 referencias sin verificar** | de 282 `ref_smith`; 14 hechas | **≈ 4-6 sesiones** |

La cuenta del briefing 53 se sostiene: **7-8 sesiones sin las referencias**.

---

## 8. Cifras al cerrar

| | |
| --- | --- |
| páginas del Conspectus | 44 de 44, completo |
| **páginas COLACIONADAS contra la plancha** | **13 de 44** (1105-1117) |
| términos del Conspectus | 1.878 |
| lemas distintos | 1.608 |
| entradas de Nandisena | 649 |
| coincidencias exactas entre las dos fuentes | 284 |
| normativos de `comun/glosario.md` | 53 |
| fichas con `conflicto` | 61 |
| fichas con `duda` | **57** (eran 48 al abrir la sesión 53) |
| referencias verificadas contra la fuente | 14 de 282 |
| lemas cambiados en esta sesión | **0** |
