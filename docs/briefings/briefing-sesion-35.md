# Kaccāyana Pāḷi-Español: Briefing de la Sesión 35

*Complementa a los briefings 05–34. Tema de la sesión 35 (2026-08-29, en
vivo con el IEBH): **los globos al tamaño justo, el inglés de los
paradigmas de punta a punta —interfaz y prosa, esta última adjudicada—,
los dos botones del solucionador, y `combinar_varias()` para las formas
de tres voces**.*

> **Lo primero que tiene que saber el chat nuevo:** verificar
> `git log origin/main..main` (el IEBH empuja, o su ciclo empuja por él).
> Las reglas de siempre: el Python es la referencia; los CINCO arneses
> mandan (`arnes.js`, `arnes_corpus.js`, `arnes_deteccion.js`,
> `arnes_pagina.js`, `arnes_casos.js`); nada se adjudica sin el visto
> bueno del IEBH; todo se mide antes y después; la atribución pública
> dice IEBH, nunca «Angel». Con Angel se habla en inglés; lo del proyecto
> va en español.

## 0. AVISO QUE NO PUEDE ESPERAR

**La clave de la cola se escribió en el chat.** El IEBH pegó
`VEREDICTOS_CLAVE=…` en un mensaje para preguntar por la salida del ciclo.
Se le avisó de que hay que **rotarla en el worker**; al cierre de la sesión
no consta que se haya hecho. Preguntarlo, y no volver a escribirla en
ninguna parte: es secreto del worker, y el briefing 34 §3 ya lo decía.

## 1. LOS GLOBOS, RESUELTOS DE VERDAD (v1.7 del solucionador)

La primera tarea del briefing 34 §4 tenía media respuesta escrita de
antemano, y la mitad estaba al revés. Con la caché ya arreglada
(`site/_headers`, cuarta excepción de fuente en `site/`), el IEBH VIO la
página por fin, y lo que vio corrigió las dos suposiciones:

- **El aforismo estaba DEMASIADO grande.** El agrandado del 2026-08-29
  (560 px · 21 px) se había pedido contra una página vieja que nunca llegó
  a mostrarse. Vuelve al tamaño del 2026-08-28 —460 px · 18 px—, que es
  **el mismo de `/recursos/sandhi/`**: las dos páginas coinciden otra vez,
  y eso es lo comprobable.
- **Los que se veían chicos eran los NATIVOS** (`title=`), como el briefing
  34 anticipaba. Los NUEVE del solucionador y los CUATRO de paradigmas
  pasan ahora por el `#tip` de cada página, en una variante **llana** de
  15 px. Las dos insignias de versión, que tenían globo propio de CSS
  (`::after`), se pliegan al mismo motor.

**Queda una sola clase de globo por página, y un solo tamaño que ajustar.**
Si vuelve a pedirse un cambio de tamaño, es `#tip` y `#tip.llano`, y nada
más. En paradigmas, además, el globo del caso de cada inflexión —que sólo
salía con el dedo— sale ya también con el ratón.

Cuidado aprendido: en táctil, el primer toque tiene que seguir obedeciendo
a los botones. Sólo el caso de la inflexión y la insignia de versión abren
globo al tocarlos; un globo no vale un botón que no responde.

## 2. `/recursos/paradigmas/` EN INGLÉS, ENTERO (v1.15)

Iba en dos capas y las dos están publicadas.

| Capa | Dónde | Estado |
| --- | --- | --- |
| INTERFAZ | `plantilla.html` (`.i-es`/`.i-en` + `TXT`), `inflexiones_en`/`casos_en` | publicada |
| PROSA del IEBH | `recursos/paradigmas/ingles.json` | **ADJUDICADA** por el IEBH, 2026-08-29 |

La prosa son las 84 glosas, 32 subtítulos, 7 familias, 8 notas, el texto de
los sufijos y los 17 usos con sus ejemplos. **La puerta sigue montada y hay
que dejarla montada**: `generar_paradigmas.py` comprueba el borrador SIEMPRE
—campo por campo contra el español— pero sólo lo inyecta si
`"adjudicado": true`. Se probó en las dos posiciones antes de firmar. Firmar
fueron tres campos; el aviso del pie cedió el sitio al crédito.

Cotejo lado a lado: `docs/paradigmas/ingles-por-adjudicar.md`, que lo escribe
`herramientas/generar_ingles_paradigmas.py` desde el propio JSON y **sabe si
está firmado** (cambia la cabecera). CLAUDE.md tiene ya su sección
«Estado de recursos/paradigmas».

**Lo que no se traduce, y es deliberado:** las formas pāḷi (son el objeto de
la página) y las referencias (§248, Rū. §260: son la cita, y es la misma).
El buscador indexa los dos idiomas — «girl» y «niña» encuentran kaññā.

### Pendiente, y es del IEBH

**Tres notas publicadas dicen «con el visto bueno de Angel»** — N-Ā1, #1 y la
segunda de Sufijos-Inflexiones. La regla del proyecto es que la atribución
pública dice IEBH. El inglés ya pone «with the approval of the IEBH»; el
español está **sin tocar a propósito**, porque corregir la edición es
decisión suya. Se le ofreció y no la tomó todavía. §7 del cotejo.

## 3. EL SOLUCIONADOR: «ENLACE» Y «COPIAR» EN CADA VOZ (v1.7)

Los mismos dos botones de raíces y paradigmas, en el cuerpo de cada tarjeta
(no en el `<summary>`: un clic ahí la plegaría).

- **Enlace** copia `…/solucionador/?voz=lokaggo`, y esa dirección **llega
  analizada**. Vale porque el motor es determinista y porque una voz sola
  entra por la rama del «análisis completo».
- **Copiar** da el análisis en texto llano: voz, señal **con su
  procedencia**, estado, componentes, escalera con el aforismo de cada paso,
  referencia; y las otras lecturas si la señal no es segura. Crédito y
  enlace al pie.

**El rótulo copiado es el mismo que el de la tarjeta y por la misma prueba.**
Copiar no asciende una conjetura a afirmación.

El bloque de `?voz=` va DESPUÉS del bloque del idioma: aquél reanaliza al
cambiar de idioma y si no, el análisis se haría dos veces.

## 4. `combinar_varias()` — TRES VOCES (mapa 32, punto 4)

Pliega `combinar()`: primera con segunda, se verifica por recomposición, el
superviviente con la tercera, y otra vez a verificar. Con dos voces devuelve
lo mismo que `combinar()`.

**DOS de las tres salen, con escalera completa** — `idamavocāyasmā` y
`mamañceva`.

**La tercera no, y el porqué es el hallazgo.** `idamavocanti` = idaṃ +
avocaṃ + iti pide como intermedio `idamavocaṃ`, que **no está en el léxico**:
es producto de un sandhi, no una palabra que un diccionario liste. Y
`solucionar()` sólo corta cuando las dos mitades son voces atestiguadas. De
modo que **el plegado funciona exactamente cuando el intermedio resulta estar
atestiguado** —`mamañca` lo está, `idamavoca` lo está—. No falta una regla:
la puerta pide dos palabras y aquí una es un intermedio. **Levantar ese techo
pide una derivación de UNA pasada sobre las dos junturas, no un plegado.**
Ése es el trabajo siguiente si se quiere cerrar el punto 4 del mapa 32.

**Segunda advertencia, en la docstring:** la escalera del plegado es UNA
derivación válida, no la que firmó el IEBH. El plegado cierra la primera
juntura (§11) antes de abrir la segunda; la verificada de `mamañceva`
—§31 · §10 · §12 · §11 · EM— trata las dos a la vez.

### El termómetro nuevo

`herramientas/auditar_derivacion_casos.py` — para cada caso adjudicado, ¿sabe
el motor **derivar** esa lectura? No es lo que comprueba `arnes_casos`
(aquél exige que se **afirme**), y **no es una puerta**: no detiene nada.
Separa los motivos, que es lo que convierte una lista en trabajo.

De 62 casos con sandhi: **54 derivan de un corte, 2 plegando, 6 no**. Y de
esos 6, **sólo DOS interrogan a las reglas** — `idamavocanti` y
`atikkamiyeva` (atikkami + yeva) —; `suññāgāragatovā` es pakati (no hay
operación, y el motor hace bien en callar) y **tres son lemas que faltan en
el léxico**: `upādinnakasantāne`, `anupādinnakasantāne`, `kenacid`. Eso no es
falta de regla: es falta de palabra, y se arregla en otro sitio.

## 5. EL LOTE 1 NO ESTÁ RANCIO

Se comprobó regenerándolo contra el estado de hoy: de sus 250 formas,
**237 siguen pendientes**. Sólo 13 se resolvieron (9 como caso adjudicado:
ceva, cāti, evameva, mano, natthi, pajānāti, passanto, sotaṃ, teneva; el
resto por banco, patrón o la licencia de §13). El lote regenerado se
descartó por redundante.

**El cuello de botella del lote 1 no es el archivo: son los 250 veredictos,
y son del IEBH.** No hay nada que un chat pueda adelantar ahí.

## 6. LAS ADJUDICACIONES DEL CIERRE (2026-08-29, en el chat)

### §34 — APROBADO. Falta implementarlo.

Palabras del IEBH: **«§34 is approved since anytime you find the niggahita
changed to 'm' before a vowel, it means this rule applies.»**

**La aprobación está dada y el mecanismo NO está escrito.** Es la primera
tarea del chat siguiente, y no es pequeña, porque §34 **no encaja en el
mecanismo de patrones que hay**: los tres patrones vigentes (`iti`, `api`,
`ca`) se declaran por la SEGUNDA voz, y en §34 la segunda voz es cualquiera
— lo que identifica la clase es **la «m» de la juntura**. Hace falta una
clase de patrón nueva.

La receta, tal como la simuló `generar_informe_niggahita_m.py` (que es lo
que se midió y por tanto lo que se firmó):

- candidatas: `base` acabada en ṃ y `seg` tales que
  `base[:-1] + "m" + seg == forma`, las dos atestiguadas;
- **el resguardo de siempre**: las dos voces al menos tan frecuentes como la
  forma entera (`piso = max(frec(forma), 1)`);
- gemelas (misma base, segundas que sólo difieren en la cantidad de la
  vocal inicial) → la de inicial BREVE;
- si queda EXACTAMENTE UNA, se afirma; si no, calla.

Medido antes de firmar: **54 formas afirmables, masa 31.344, y 37 de ellas
hoy sin señal ninguna** — recall nuevo, no sólo «no sabe» resuelto.

**Cómo se hace el cambio, que es lo que no hay que improvisar:** los arneses
no llevan cifras a mano, comparan el JS contra una **referencia volcada del
Python** (`nuestro/js/referencia-*.json`). Así que: cambiar el Python →
volver a volcar las referencias → espejar el cambio en `nuestro/js/motor.js`
→ los cinco arneses. Las cifras de `arnes_deteccion` **tienen que moverse**:
ése es el efecto buscado, y el antes/después es la medición.

### Proclíticos — NO hay regla general, y el IEBH lo zanjó

Palabras del IEBH: **«there is no way to define a general rule»**. Lo que sí
dio, y queda como caso adjudicado:

- **`svāyaṃ` = so + ayaṃ, SIEMPRE** → caso, grado exclusivo. Ya puesto.
- **`netaṃ` = na + etaṃ, mayormente** → caso, grado habitual. Ya puesto.
- **`cetā` = ca + etā, mayormente** → ya era caso desde el 2026-08-28.

Y dio el **criterio** para lo demás: *«sattānaṃ is a noun, caranto is a
present participle, cittaṃ is a noun. I can almost with 100 % confidence say
that never caranto = ca + anto.»* Es decir: **si el diccionario da la forma
entera como palabra con su categoría gramatical, no es sandhi proclítico.**

**Se probó, y el criterio no se puede computar con lo que hay en la
carpeta.** `es_palabra()` dice «sí» tanto de `sattānaṃ`, `caranto` y
`cittaṃ` como de `cetā`, `netaṃ` y `svāyaṃ`: el léxico
(`recursos/lexico/dpd-formas.txt`, 443.740 líneas) es una **lista de formas
desnuda, sin categoría**, y las formas de sandhi también están atestiguadas
en él. Lo que el criterio pide es la **categoría gramatical**, y eso vive en
`dpd-descomposiciones.tsv`, **que no está en la carpeta**.

De modo que la conclusión es limpia y de una sola pieza: **el criterio del
IEBH es el correcto y es mecanizable, y lo único que le falta es ese
archivo.** Confirma de paso su instinto: el informe da hoy veredicto «única»
tanto a `caranto` como a `sattānaṃ` — las dos que él nombró como
disparates—, que es exactamente lo que su filtro frenaría.

### Las notas de «Angel» — hechas

«Replace Angel with IEBH wherever it appears in all the webpages.» Las tres
notas de `paradigmas.json` (N-Ā1, #1, Sufijos-Inflexiones) dicen ya «con el
visto bueno del IEBH». **`site/` no contiene ya ninguna aparición de
«Angel»** — comprobado con `grep -rl` sobre todo el directorio.

Queda «Angel» en sitios que **no son páginas** y que no se tocaron: los
comentarios de `nuestro/*.py`, las cabeceras de los tres informes de
`docs/solucionador/` («los firma Angel»), `comun/guia-de-estilo.md`,
`comun/convenciones.md` y los borradores de sesión. Si también han de decir
IEBH, es otra orden y es fácil; no se hizo porque no son páginas.

## 7. LO QUE SIGUE (en orden)

1. **Rotar la clave** (§0).
2. **Implementar §34** (§6). Aprobado, medido, con la receta escrita.
3. **Traer `dpd-descomposiciones.tsv` a `recursos/lexico/`**: desbloquea la
   columna del testigo en los dos informes Y el criterio de categoría
   gramatical que el IEBH dio para los proclíticos.
4. **La pasada única de dos junturas** (§4), que cierra el punto 4 del mapa 32.
5. Resto del mapa 33: §23/pakati sistemático, descomposiciones del DPD,
   des-flexión. **Sin empezar.**

## 7. AVISOS AL CHAT NUEVO

- **`ciclo_veredictos.py` hace `git add -A`.** Cualquier cosa sin
  confirmar en el árbol se lleva a un commit «Casos de la cola» con el
  mensaje equivocado. **Confirmar antes de que el IEBH corra el ciclo**, y
  mirar `git status` si se sospecha que acaba de correrlo. Pasó tres veces
  esta sesión y no llegó a estropear nada por poco.
- El IEBH corrió el ciclo **cinco veces** durante la sesión: los casos
  pasaron de 54 a 82 mientras se trabajaba. Las cifras de un arnés pueden
  cambiar entre dos llamadas sin que nadie haya tocado nada.
- JSDOM no está instalado en el arenal; `npm install jsdom` en `/tmp`
  funciona. `matchMedia` y `fetch` se inyectan en `beforeParse`; para el
  solucionador, `fetch` se sirve desde `site/recursos/solucionador/`.
  `scrollIntoView` no existe en JSDOM y salta en `sincronizarBarra`: es
  cosa de JSDOM, no de la página.
- Las cachés del arenal (`/tmp`) mueren con él; la del IEBH está en
  `~/.cache/gramaticas-pali-senal.json`.
- `volcar_referencia_pagina.py` necesita `--dpd-filtro`;
  `volcar_referencia_corpus.py`, `--solo-canon --dpd-filtro`.
- El repo del IEBH es `github.com:bthar-mx/gramaticas-pali-es.git`; desde el
  arenal no hay acceso a `origin` (ni `fetch` ni `push`): **empuja él**.
