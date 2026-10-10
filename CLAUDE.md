# Instrucciones del proyecto

Si hay conflicto entre este archivo y `comun/convenciones.md`, manda
`comun/convenciones.md`.

## Qué es este repositorio

Traducciones al español de gramáticas clásicas pāḷi. Público lector:
estudiantes hispanohablantes de pāḷi con formación buddhista.

## Reglas

- **Con el IEBH se habla en inglés. Todo lo que produce el proyecto va en
  español.** El criterio es quién lo lee, no dónde aparece:
  - **Inglés**: todo lo que Claude le dice al IEBH en el chat —la respuesta
    **entera**, incluidas las explicaciones que acompañan a un bloque de
    código o a una orden para copiar.
  - **Español**: el sitio, los briefings, los mensajes de commit, los
    comentarios del código, los `<!-- DUDA: ... -->`. Siguen en español
    **aunque se le pasen al IEBH en el chat para que los copie**: un mensaje
    de commit es contenido del proyecto, no una frase dirigida a él.
- **Nada de verbos ingleses conjugados en español** —«commitear», «pushear»,
  «empujado», «mergear», «testear»—. La tabla y el porqué, en
  `comun/convenciones.md` §0.
- Registro formal y doctrinal; no coloquial.
- **Sin artículo ante títulos de obras** (estilo de la casa, IEBH,
  2026-10-06): «según Visuddhāyuṃ», «de Rūpasiddhi», «cita Mahāṭīkā»,
  «Mugdhabodha-ṭīkā dice»; en inglés, sin «the» («according to Rūpasiddhi»).
  Las colecciones y los textos del canon lo conservan: «el Vinaya», «los
  Jātaka», «el Saṃyutta», «the Vinaya». Los nombres comunes también («la
  ṭīkā», «una Aṭṭhakathā», «su nissaya»): la regla es para el título, no
  para el género de obra.
- Términos técnicos pāḷi sin traducir, con diacríticos completos
  (nibbāna, saṅkhāra, kāraka); cursiva en la primera aparición de cada sección.
- Consultar `comun/glosario.md` antes de fijar la traducción de un término.
  Si no está, proponerlo y añadirlo — no improvisar caso por caso.
- Ante duda gramatical o de lectura, decirlo explícitamente en lugar de
  suponer. Marcar con `<!-- DUDA: ... -->`.
- Dar la referencia (sutta, obra, edición) al afirmar algo sobre el texto.
- No reescribir secciones ya revisadas sin que se pida.
- Nunca añadir, quitar ni cambiar nada más allá de lo que da estrictamente la
  edición base sin avisar explícitamente y dejar que el IEBH decida. Esto incluye
  las expansiones morfológicas (pasos de elisión o sustitución que Nandisena no
  menciona). Lo tomado de Ven. A. Thitzana se señala siempre como suyo.

## EL TIPIṬAKA ES LA FUENTE; KACCĀYANA ES LA AUTORIDAD QUE LO EXPLICA

**Pedido del IEBH, 2026-08-30, y va aquí arriba porque es criterio, no
detalle.** Sí, se entiende, y de este modo:

**Una lectura puede ser impecable por las reglas y no ser una lectura.** Que
una cadena de aforismos recomponga exactamente la forma demuestra que la
gramática PODRÍA producirla; no demuestra que el Tipiṭaka la diga. La
gramática explica el texto: no lo autoriza. Cuando las dos cosas no coinciden,
manda el texto.

De ahí, tres consecuencias que no se negocian:

1. **Recomponer es necesario y no suficiente.** Era el único filtro y no
   alcanza: «tveva» recomponía por siete caminos y el Tipiṭaka dice uno.
2. **Que las voces estén atestiguadas TAMPOCO alcanza.** «tvaṃ» aparece 7.857
   veces en la edición y «tvṃ» una, y aun así «tvaṃ + eva» no es lo que el
   canon lee en «tveva». Atestiguar la PIEZA no atestigua la JUNTURA.
3. **Lo teóricamente posible no se publica como si fuera lo que dice el
   canon.** Antes de enseñar una lectura hay que poder decir dónde la dice el
   Tipiṭaka, o decir que no se sabe.

### DICHO CON SUS PALABRAS, QUE SON MEJORES

**HAY FORMAS DE SANDHI TEÓRICAMENTE PLAUSIBLES QUE SON INVEROSÍMILES EN EL
TIPIṬAKA.** El IEBH, 2026-08-30. Plausible por la gramática y ausente del canon
son cosas distintas, y la segunda manda: **el Tipiṭaka es la fuente; Kaccāyana
—y el Saddanīti— son la autoridad que lo EXPLICA, no la que lo autoriza.**

### Y NO ES CAUTELA: ES EL ESTADO MEDIDO DEL MOTOR (sesión 40)

Sobre las 2.045 junturas del banco, la lectura del IEBH es la primera del motor
en 1.618; en **416 no lo es, y esas 416 pesan 48.439 fichas**. En 296 de ellas
—masa 44.998, el **93%**— lo que el motor hace no es escoger mal la partícula:
es **cortar la palabra en otro sitio**, y todas las candidatas recomponen.

Se probaron tres maneras de separarlas por señal interna. **Las tres se caen**,
y están medidas en `docs/solucionador/saddaniti-lo-que-kaccayana-no-tiene.md`:

| lo que se probó | arregla | rompe |
| --- | ---: | ---: |
| quitar el criterio de nipāta del desempate | 78 | **940** |
| bajar «iha», que es quien gana a «āha» | 1 | 0 |
| premiar que la primera voz esté atestiguada | 7 (masa 170) | premiaría al motor CONTRA el texto en 244 |

En «tenāha» conviven «tena+āha», «tena+iha», «tena+ha» y «tena+aha»: **todas
recomponen, todas están atestiguadas, y ninguna señal de este repositorio las
separa.** Por eso la regla de arriba no es higiene doctrinal sino la razón de
que el trabajo que queda no se pueda terminar con mejores reglas.

<!-- DUDA, y es la que hoy no se puede cerrar aquí: para comprobar que dos
     voces aparecen JUNTAS en el canon hace falta el TEXTO CORRIDO, y este
     repositorio sólo tiene `recursos/corpus/corpus-formas.json` — formas con
     sus cuentas, 681.927 y 8.062.163 fichas, sin contexto—. Con eso se puede
     contar y no leer. El texto corrido lo tiene el proyecto OSBCT, y hasta
     que se conecte, la poda de lecturas inverosímiles se hace a mano y por
     adjudicación, una por una, como se hizo con «tveva» el 2026-08-30.
     2026-08-30, sesión 40: esa DUDA ya tiene precio. Son 44.998 fichas, y
     conectar el OSBCT no es una mejora entre otras: es la única que las
     alcanza. -->

## Gestión de la sesión

Corresponde a Claude —no al IEBH— avisar cuando la conversación se ha alargado
lo bastante como para convenir abrir una nueva. El aviso se da **antes** de que
la calidad se resienta, no después, y no espera a que el IEBH lo pregunte.

Al avisar, Claude entrega lo que el chat nuevo necesita para continuar sin
pérdida:

- el punto exacto donde se dejó el trabajo: último sutta aprobado y siguiente;
- qué archivo debe leer primero el chat nuevo
  (`docs/briefings/briefing-sesion-NN.md`);
- las decisiones, erratas y convenciones acordadas en la sesión que todavía no
  estén recogidas en ese briefing;
- el briefing actualizado, escrito y guardado **antes** de cerrar la sesión, no
  prometido para después.

Un chat nuevo empieza sin memoria de la conversación anterior: lo que no quede
escrito en el briefing se pierde.

## Cuando llegan veredictos: las escaleras, siempre

**Pedido del IEBH, 2026-08-30.** Un veredicto adjudica los COMPONENTES; casi
nunca trae la ESCALERA. Y un caso sin escalera es media respuesta: la página
enseña el corte y calla el cómo, que es justo lo que un lector de gramática
viene a ver.

Así que cada vez que entren veredictos —por la cola, por el modo revisión o
dichos en la sesión—, **sin que el IEBH lo pida**:

    python3 herramientas/auditar_derivacion_casos.py

y para cada caso que quede sin derivar, mirar por qué y proponer la
secuencia. La auditoría ya distingue los tres motivos, y **cada uno pide
una respuesta distinta**:

| lo que dice la auditoría | qué significa | qué hacer |
| --- | --- | --- |
| «el motor corta, pero no ahí» | el motor no propone ese corte | proponer la escalera a mano desde los aforismos |
| «voz no atestiguada en el léxico» | la primera voz no existe suelta en la edición | buscar una forma hermana que el motor SÍ derive y copiar su forma |
| escalera vacía y nada más | no ocurre ninguna operación | es **pakati**, y la escalera de un paso es la respuesta correcta |

Reglas que no se saltan, y son las de siempre:

- **Proponer y verificar, nunca afirmar.** Una secuencia sólo vale si
  `S.combinar(a, b)` la recompone exactamente. `combinar()` devuelve ya la
  escalera con sus §N y el campo `recompone`; si no recompone, no se publica.
- **Nunca inventar un paso para tapar un hueco.** Antes de darla por
  imposible, mirar §51 y el «ca» de §20 (sección «Cómo averiguar qué sutta
  explica una operación», más abajo), y el capítulo de Thitzana.
- **La escalera propuesta es una PROPUESTA.** Se le enseña al IEBH con su
  verificación; firmarla es suya. Lo que él escriba a mano entra como
  `escalera_iebh`, verbatim y rotulada como suya, por
  `incorporar_adjudicaciones.py`.
- Si los componentes firmados esconden la operación —`pātur + ahosi` no deja
  ningún paso que mostrar, mientras que `pātu + ahosi` da «pātu r ahosi
  (§35)»—, **eso se dice**: es pregunta sobre los componentes, no sobre la
  escalera, y la decide él.

## Cómo se publica

El markdown es la fuente; el HTML de `site/` es salida generada. **Nunca se
edita nada dentro de `site/`, con estas excepciones, que son fuente y no salida:
`site/assets/base.css`, `site/assets/recursos.css`, `site/assets/pali.css`,
`site/assets/pali.js`, `site/assets/cabecera.css`, `site/assets/cabecera.js`,
`site/assets/buscar.js`, los SVG de la marca en `site/assets/` y
`site/_headers`** — ningún generador los escribe. Todo lo demás lo reconstruye
entero el hook de pre-commit en cada commit (también
`site/assets/secciones.json`, que es salida), así que un cambio hecho ahí
desaparece sin avisar y sin dejar rastro. Lo que se edita está en
`kaccayana/`, `recursos/`, `comun/` y esos archivos de `site/assets/`.

### La cabecera común (rediseño de la navegación, etapa 1, 2026-10-08)

Las 26 páginas llevan arriba la misma barra: marca → portada; Kaccāyana ·
Recursos · Glosario · Clases; «Ir a §»; ES|EN; tema. **Una sola fuente para
el marcado**: `herramientas/cabecera.py`, que cada generador llama con
`cabecera.insertar(html, clave)` antes de escribir. Su tabla `PAGINAS` dice,
página por página, qué mandos de idioma y de tema ya tenía: la barra **los
acciona** (siguen en el DOM, ocultos), no trae mecanismo propio. Una página
nueva necesita su entrada en `PAGINAS` y la llamada a `insertar`.
`generar_secciones.py` escribe el mapa §N → capítulo para «Ir a §»; el
destino se calcula en una sola función de `cabecera.js` (`destinoSutta`).
Notas de trabajo: `docs/navegacion/etapa-1-cabecera.md`.

**La página de cada sutta** (etapa 2, 2026-10-08): `/s/N/` y `/en/s/N/`, 810
páginas indexadas que escribe `herramientas/generar_hub.py` con el mismo
análisis del markdown que los capítulos. «Ir a §» lleva ahí. **No llevan
nada de los borradores** (clasificación, análisis según Visuddhāyuṃ): sólo
un enlace rotulado «borrador» a cada uno; lo comprueba
`herramientas/comprobar_hub_borradores.py`. Notas:
`docs/navegacion/etapa-2-hub.md`.

**Las tarjetas de los capítulos** (etapa 3, 2026-10-08) llevan una fila de
enlaces —la página del sutta, la clasificación y el análisis (borradores,
sólo el enlace) y «Preguntar»— y, en pantallas táctiles, «Rū N · Sad N» a la
vista. Notas: `docs/navegacion/etapa-3-tarjetas.md`.

**La búsqueda en todo el sitio** (etapa 4a, 2026-10-08): `/buscar/` y
`/en/buscar/`, noindex y fuera del sitemap. La caja «§» de la barra y la de
la portada llevan un número a `/s/N/` y lo demás a `/buscar/?q=…`. El índice
(`site/assets/busqueda-es.json`, `busqueda-en.json`) lo escribe
`herramientas/generar_busqueda.py` con lo ya publicado —suttas, glosario,
raíces, paradigmas y recursos— y **ni una palabra de los borradores**: de
ellos, sólo el título y los § que cubren. Lo carga `site/assets/buscar.js`
sólo al buscar. El glosario guarda el tema en `pali_dark`, como las demás
páginas. Notas: `docs/navegacion/etapa-4a-busqueda.md`.

**Un solo aspecto para los recursos** (etapa 4b, 2026-10-08). La paleta «hoja
de palma», las tres familias de letra, la marca del IEBH y la etiqueta
«borrador» viven **sólo** en `site/assets/base.css`, que `cabecera.insertar`
enlaza en todas las páginas; `cabecera.comprobar_tokens()` falla si un color
de la paleta reaparece en otra hoja o plantilla. El cromo común de las trece
páginas de recursos (bloque del título, índice lateral con un solo ☰, barra de
mandos, pie) está en `site/assets/recursos.css`; el marcado del bloque del
título y del pie lo escribe `herramientas/recursos_comun.py` a partir de las
etiquetas `<rc-titulo>` y `<rc-pie>` de cada plantilla. En una plantilla de
recursos, el `<style>` es sólo para lo que tiene esa herramienta. La portada
ya no lleva caja de búsqueda: la de la barra es la única. Notas:
`docs/navegacion/etapa-4b-recursos.md`.

### Tres capítulos españoles NO se editan en `kaccayana/` (sesión 61)

Los capítulos 2, 3 y 4 en español son **salida**, no fuente: los rehace
`herramientas/convertir_<obra>.py` a partir de su maestro de `docs/`, y el hook
de pre-commit ejecuta **todos** los `convertir_*.py` antes de generar el sitio.
Un cambio hecho en el archivo de `kaccayana/` sobrevive en el disco, sobrevive
a la regeneración del sitio —y lo revierte el hook en el momento del commit, de
modo que el commit sale sin él y sin avisar.

| Capítulo | Se edita aquí | Lo genera |
| --- | --- | --- |
| 2 · Nāma | `docs/2. Nāma-Kappa.md` | `convertir_nama.py` |
| 3 · Kāraka | `docs/3. Kāraka-Kappa.md` | `convertir_karaka.py` |
| 4 · Samāsa | `docs/4. Samāsa-Kappa.md` | `convertir_samasa.py` |

El capítulo 1 (Sandhi) no tiene conversor: `kaccayana/01-sandhi-kappa.md` es su
fuente y se edita ahí. **Los maestros ingleses `NN-nombre.en.md` tampoco tienen
conversor**: los cuatro se editan directamente en `kaccayana/`.

Consecuencia para las notas al pie: en los tres capítulos convertidos **no se
numeran a mano**. En el maestro se escribe la nota en prosa —`… texto. Nota:
…` en la misma línea, o un párrafo propio que empiece por `Nota:`, `Nota al
pie:` o `Nota del traductor…:`— y el conversor coloca el ancla `[^n]` y
renumera todas en orden de aparición. La definición conserva el rótulo
(`[^11]:  Nota: …`); el inglés, que sí se numera a mano, lo acompaña con
`Note: …` para que las dos ediciones digan lo mismo.

Cada `git push` a `main` despliega en
<https://gramaticas.buddha-dhamma.net> (Cloudflare Workers, ver
`wrangler.jsonc`).

    # capítulo de una gramática
    python3 herramientas/generar_capitulo.py kaccayana/02-nama-kappa.md

    # su edición inglesa, si existe el maestro paralelo NN-nombre.en.md
    # (sesión 45: sale en site/en/<obra>/<slug>/, con botón EN/ES y hreflang;
    #  generar_todo.py lo hace solo, y regenera el español después para que
    #  las dos páginas se vean)
    python3 herramientas/generar_capitulo.py kaccayana/01-sandhi-kappa.en.md

    # documento en prosa (reglas, glosarios, tablas)
    python3 herramientas/generar_recurso.py recursos/<archivo>.md

o todo de una vez, que es lo habitual:

    python3 herramientas/generar_todo.py

Un hook de git lo ejecuta en cada commit y añade el HTML regenerado, de modo
que no hace falta acordarse. Los hooks no viajan con el clon: en una copia
nueva del repositorio hay que instalarlo una vez con

    sh herramientas/instalar-hooks.sh

Detalles del formato del markdown y de lo que el generador deduce solo:
`comun/convenciones.md`, secciones 2, 3, 3 bis y 3 ter.

## La edición inglesa (sesión 45)

Con permiso del Venerable Nandisena. **Su inglés donde lo hay; donde no
tradujo, se traduce siguiendo al español; donde el español amplió los
ejemplos, el inglés sigue al español; glosario inglés fijo** (memorando
`docs/ingles/memo-sandhi-en-glosario-y-desviaciones.md`, §2; registro de
desviaciones, §5). Un maestro por capítulo, `kaccayana/NN-nombre.en.md`, con
la misma estructura que el español; las cadenas de la página salen de
`IDIOMAS` en `generar_capitulo.py`. Reglas que no se saltan: la glosa del
sutta lleva corchetes como el español, pero «follows» (locativo) y «after»
(ablativo) van sin corchetes (`comun/convenciones.md` §1 bis); *Gaṇa* = «the
noble Order»; *ṭhāne* en singular; *kvaci / vā / navā* = sometimes /
optionally / occasionally; las funciones de «ca» con los nombres del
Venerable (dragging, collecting, accumulating, delimiting, smoothness of
speech), que están en su apéndice, `docs/fuentes/nandisena-apendice-sandhi-en.md`.

## Estado de recursos/sandhi

La referencia interactiva de sandhi (`/recursos/sandhi/`, v3.5) se arma con
`herramientas/generar_sandhi.py` a partir de tres piezas:
`recursos/sandhi/plantilla.html` (maquetado y lógica),
`recursos/sandhi/reglas.json` (49 reglas y 266 formas) y
`kaccayana/01-sandhi-kappa.md` (los 51 aforismos).

### Procedencia de cada secuencia

Las 266 formas salen del documento de Bhikkhu Nandisena, que da componentes,
resultado y referencia canónica, pero **no** los pasos intermedios. Cada forma
lleva un campo que dice de dónde sale su secuencia:

| Campo        | Formas | De dónde viene |
| ------------ | -----: | -------------- |
| `verificada` |     49 | Copiada de la traducción del Sandhi-kappa |
| `derivada`   |    175 | Calculada y comprobada contra la forma atestiguada |
| `aforismo`   |     42 | Construida a partir del propio aforismo |

La regla que hace fiable lo calculado: se genera una secuencia candidata, se
aplica, y sólo se conserva si reproduce **exactamente** la forma atestiguada
—ignorando apóstrofos, espacios y guiones—. Lo que no cuadra no se publica.
Nunca se inventa un paso para rellenar un hueco.

### Lo que conviene saber antes de tocarlo

- **El Sandhi-kappa está agotado.** Contiene 164 secuencias y las aprovechables
  ya están puestas: son las 49 `verificada`. No vale la pena volver a buscar
  ahí. El resto de las formas de Nandisena son ejemplos canónicos suyos, no de
  Kaccāyana.
- **13 formas tienen un solo paso**, todas de pakati-sandhi. No es que les
  falte la secuencia: es que en pakati no ocurre nada, y ése es el sentido de
  la sección. No hay que «arreglarlas».
- **9 formas llevan `nota`.** Cinco explican qué ilustra la forma; las otras
  cuatro avisan de que los datos de la fuente parecen erróneos —`icc antaṃ`,
  `nicchayo`, `esa ābhogho` y `jamb’ īritā vatena`—. Ésas son para cotejar con
  el PDF, no para corregir a ojo.

### Comprobaciones

    python3 herramientas/auditar_secuencias.py     # coherencia paso ↔ aforismo
    python3 herramientas/reconstruir_sandhi.py     # rehace reglas.json desde el documento

La auditoría sólo comprueba que el aforismo citado haga esa *clase* de
operación. Que un paso la pase no demuestra que la cita sea la correcta.

## Cómo averiguar qué sutta explica una operación

Antes de dar por imposible la secuencia de una forma, hay dos fuentes que
suelen tener la respuesta. Consultarlas **siempre** antes de decir que un paso
no se puede explicar, y nunca inventar una regla para tapar el hueco.

### §51, el sutta comodín

«Anupadiṭṭhānaṃ vuttayogato» —de las formas no mostradas, según las reglas ya
mencionadas— es el cajón de sastre del capítulo, y por eso es la fuente más
rica de patrones: contiene **41 secuencias de formación** ya traducidas, más
que ningún otro sutta. Cuando una forma no encaje en ningún patrón conocido,
mirar ahí primero.

### La partícula «ca»: un sutta hace más de lo que dice

El «ca» de un sutta arrastra funciones que su enunciado no menciona. En las
secuencias se cita como «"ca" en §20», y así aparece en §51:

    Parāyaṇaṃ    … par āyanaṃ (§15); par āyaṇaṃ («ca» en §20)      n → ṇ
    Byaggaṃ      … v y aggaṃ (§21); b y aggaṃ («ca» en §20)        v → b
    Dubbuttaṃ    … du vv uttaṃ (§28); du bb uttaṃ («ca» en §20)    vv → bb

De modo que cuando un paso hace una sustitución que ningún enunciado cubre,
lo probable no es que falte una regla: es que sea el «ca» de alguna, y §20 es
la candidata habitual.

### Las 14 funciones de §20 por suttavibhāga

**Están en el propio capítulo**, en §20, líneas 887-891 de
`kaccayana/01-sandhi-kappa.md`: el pasaje pāḷi *Suttavibhāgena bahudhā siyā …
Icc evamādī yojetabbā* con su traducción y los catorce ejemplos. Thitzana,
vol. 2, pp. 138-140, documenta lo mismo por su lado, de modo que sirve de
cotejo, no de fuente.

Transcritas a `recursos/sandhi/suttavibhaga.json`, listas para el
solucionador, junto con las ocho citas «ca» que el capítulo hace en sus
secuencias (tres a §35, dos a §41, tres a §20).

Las catorce sub-suttas de «Do dhassa ca» (§20):

| Sub-sutta   | Cambio  | Ejemplo |
| ----------- | ------- | ------- |
| To dassa    | d → t   | sugado → sugato |
| Ṭo tassa    | t → ṭ   | dukkataṃ → dukkaṭaṃ |
| Dho tassa   | t → dh  | gantabbo → gandhabbo |
| Tro ttassa  | tt → tr | attajo → atrajo |
| Ko gassa    | g → k   | kulūpago → kulūpako |
| Lo rassa    | r → l   | mahāsāro → mahāsālo |
| Jo yassa    | y → j   | gavayo → gavajo |
| Bbo vvassa  | vv → bb | kuvvato → kubbato |
| Ko yassa    | y → k   | saye → sake |
| Yo jassa    | j → y   | nijaṃputtaṃ → niyaṃputtaṃ |
| Ko tassa    | t → k   | niyato → niyako |
| Cco ttassa  | tt → cc | bhatto → bhacco |
| Pho passa   | p → ph  | nipatti → nipphatti |
| Kho kassa   | k → kh  | nikkamati → nikkhamati |

Aparte de éstas, el propio «ca» de §20 da **dha → ha** (sādhu → sāhu).

**Ojo con la dirección de la flecha.** Nandisena escribe «Sugado > Sugato»,
de la subyacente a la atestiguada, que es la dirección del proyecto. Thitzana
la invierte: imprime «Sugato> Sugado», la atestiguada primero, aunque declare
que `>` significa «se convierte en». Al traer material suyo hay que darle la
vuelta. La convención está fijada en `comun/convenciones.md`.

**Y con dos ejemplos que difieren entre ambos.** En *Pho passa*, Nandisena
escribe «nippatti → nipphatti» y Thitzana «nipatti → nipphatti»; en *Yo
jassa*, Nandisena da «nijaṃ → niyaṃ» y Thitzana «nijaṃputtaṃ →
niyaṃputtaṃ». Manda Nandisena, que es la edición base.

La lista se cierra con *Icceva’mādī yojetabbā* —«y así los demás casos
semejantes»—, que es lo que ampara las sustituciones que §51 cita sin figurar
en la tabla, como v → b y n → ṇ.

### El capítulo de Sandhi de Thitzana entero, no sólo esas páginas

En la conversión de *Kaccāyana Volume 2 (Ven. A. Thitzana)* el capítulo de
Sandhi ocupa aproximadamente las líneas 4029-5890, y ahí están **101 de los
102 bloques `[SM]` de todo el volumen**. Cada ejemplo viene con cuatro
etiquetas:

| Etiqueta | Qué contiene |
| -------- | ------------ |
| `[V]`    | el vutti en pāḷi |
| `[CS]`   | la frase atestiguada, con su referencia y traducción |
| `[SS]`   | la separación en componentes (*sandhi separation*) |
| `[SM]`   | **el método**: qué suttas se aplican y en qué orden, en prosa |

`[SM]` es lo que llevábamos toda la tarde echando en falta: la secuencia
explicada, no la forma sola. Está en inglés y en prosa —«elide the front
vowel a by Sutta 12, then attach…»— pero nombra los suttas.

Dos cosas más que salen de ahí:

- **El «ca» no es exclusivo de §20.** En la línea 5273 aparece «change "m"
  into "p" by means of "ca" in this Sutta». El mecanismo es general; §20 sólo
  es el caso más frecuente.
- **Las formas de §51 están resueltas una a una** en las líneas 5787-5887
  —Pāpanaṃ, Nyāyogo, Nirupadhi, Byaggaṃ, Dubbhikkhaṃ, Sandiṭṭhaṃ…—, de modo
  que sirven para **cotejar** las secuencias del capítulo con una fuente
  independiente, no sólo para rellenar huecos.

Recordatorio de siempre: lo tomado de Thitzana se señala como suyo antes de
incorporarlo, para que el IEBH decida y se le dé el crédito al Venerable.

## Estado de recursos/raices

La referencia de raíces (`/recursos/raices/`, v1.7) reúne **cuatro obras
distintas** en cinco pestañas, y confundirlas es el error fácil:

| Pestaña | Obra | Cuántas | Qué numera |
| --- | --- | --- | --- |
| Raíces | Saddanīti-dhātumālā | 1.698 | gaṇa (I-VIII) + **página** |
| Significados | índice inverso de la misma | 776 | — |
| Dhātupāṭha | Andersen y Smith, 1921 | 643 | 1–639, más cuatro con letra |
| Dhātumañjūsā | Kaccāyana-Dhātumañjūsā | 154 estrofas | la suya, hasta 884 |
| Dhātvatthasaṅgaha | con el nissaya del Mahāvisuddhārāma Sayadaw (KBRL 001288) | 1.637 | la suya, por siete kaṇḍas + **página** |

Se arma con `herramientas/generar_raices.py` a partir de
`recursos/raices/plantilla.html` y cinco JSON: `raices.json`,
`dhatupatha.json`, `dhatupatha-ingles.json`, `dhatumanjusa.json` y
`dhatvatthasangaha.json` (raíz, sentido y página; el texto del nissaya no
se publica; detalle en `recursos/raices/LEEME.md`).

### La fuente principal, y cómo se cita

**«Pali Roots in Saddanīti», del Venerable U Sīlānanda**, editado por
Bhikkhu Nandisena (CMBT, 2005). U Sīlānanda es el **autor**; Nandisena,
el editor y traductor al español. No es «Pali Roots in Comparison»: ése
es el título de la sección de la p. 57, no del libro.

### Dos cifras que no significan lo mismo

Según la leyenda de la propia edición (p. 46): en pāḷi, `I 12` es grupo
y **página** del Saddanīti-dhātumālā; en sánscrito, `X 371` es grupo y
**número de raíz** del Pāṇinīya-dhātupāṭha. Y **los nueve gaṇas del
Dhātupāṭha no son los ocho del Saddanīti**: siguen la ordenación
sánscrita, y el primero se parte en I,a e I,b.

### Por qué hay un extractor propio

El PDF de U Sīlānanda no tiene capa de texto utilizable: Quartz lo
compuso con **477 subconjuntos tipográficos**, cada uno con su
codificación y el ToUnicode roto. `extraer_raices.py` lo reconstruye por
el **contorno** de cada glifo —161 distintos en todo el libro, en la
constante `GLIFOS`— y recorta las celdas con las líneas de la tabla. Si
el PDF cambiara, `GLIFOS` hay que rehacerlo; el guion avisa si el número
de contornos no es 161.

**Los tres PDF no están en el repositorio.** `generar_todo.py` publica lo
ya extraído; sólo hay que volver a extraer si cambia una fuente.

### Lo que conviene saber antes de tocarlo

- **La concordancia entre obras es por lema y nada más.** Cuando además
  coincide la glosa pāḷi se marca, y ésa es la fiable: 229 de 675.
- **La Dhātumañjūsā va como poema, no como tabla.** El enlace con una
  raíz es coincidencia literal de la palabra en el verso, con lemas de
  tres letras o más. No se deshace el metro: en el śloka la raíz y su
  significado van encajados, y separarlos sería interpretar.
- **El español del Dhātupāṭha es prestado**, no traducido aquí: se
  reutiliza el del Saddanīti cuando la glosa pāḷi es idéntica (430 de
  643), y la entrada lo marca con `ES·N`. El inglés viene de la hoja de
  la digitalización (Bodhirasa Bhikkhu, 2019). Los 213 restantes no son
  un hueco que rellenar: las dos obras glosan el mismo sentido con
  palabras distintas —*gamanatthā* frente a *gatyatthe*—.
- **La letra del Dhātupāṭha no es la inicial de la raíz.** La edición
  agrupa por la consonante de la raíz: bajo «K» van *bhū, ku, aṃka,
  saṃkha, vaka*. Esa cabecera viene ya en los datos y **no se
  recalcula**; tomarla por la inicial llena la página de secciones
  repetidas.
- **Los guiones son del texto, no de corte.** El original es una tabla
  de Word, y Word no parte palabras al final de línea: `-` y `–`
  segmentan los compuestos (`hiṃsā-saṃkleśa–nayoḥ`).

### Comprobaciones

`generar_raices.py` no publica si los datos no cuadran: comprueba lemas,
referencias, gaṇas dentro de rango, NFC y que no quede ningún carácter
sin descifrar. La hoja de cálculo pública de la digitalización sirve de
cotejo independiente: sus 643 claves coinciden una a una con las
extraídas del PDF.

## Estado de recursos/casos

La referencia de los usos de las inflexiones (`/recursos/casos/`, v0.3,
**borrador en revisión**, 2026-09-28) se arma con
`herramientas/generar_casos.py` a partir de `recursos/casos/usos.json` (los
datos) y `recursos/casos/plantilla.html` (maquetado y lógica). El generador
verifica los datos —ids únicos, toda cita de la Rūpasiddhi en la concordancia,
Kacc. dentro de §271–§315, fuentes declaradas, NFC— y no publica si algo falla.

- **Orden**: el de la Rūpasiddhi, Kāraka-kaṇḍa (§283–§329, con §70); el botón
  «Kaccāyana» reordena por §271–§315. Rū. §306 no tiene correspondiente en el
  capítulo 3 y va aparte.
- **Base**: un paradigma inglés de los usos (ParadigmCasos.pdf, no está en el
  repositorio), cotejado ejemplo por ejemplo con la Rūpasiddhi; donde no
  coinciden manda la Rūpasiddhi y la corrección va en `correcciones_al_pdf`.
- **El español lleva su fuente** en `es_fuente`: `norma` (`comun/glosario.md`) >
  `cap3` (capítulo 3 publicado) > `glos` (Glosario de Nandisena) > `diap`
  (diapositivas *Casos gramaticales* de Nandisena) > `prop` (propuesta, pendiente
  del IEBH). El modo «Revisión» de la página lo enseña.
- **Nombres de los casos**: fijados por el IEBH el 2026-09-28 (`nombres_de_caso`
  en `usos.json`): caso del sujeto o agente, caso del objeto, caso del
  instrumento, caso del destinatario, caso del punto de partida, caso del lugar;
  el sāmī, que no es kāraka, poseedor. **Sin el caso entre paréntesis** (IEBH
  2026-10-08): un kāraka no equivale a un caso (el kattā va en la primera
  inflexión en la activa y en la tercera en la pasiva, §288). Están en `comun/glosario.md`. El capítulo 3
  usa los papeles desde el 2026-10-08 («apādāna» (punto de partida), etc.;
  kattā: «sujeto» o «agente»); las notas de Nandisena 1, 19, 37, 39 y 46 son
  ahora nota nuestra.
- **Pendiente**: las 17 dudas marcadas en `duda` (lista en
  `docs/casos/usos-revision.md`), y cotejar los ejemplos canónicos con el
  corpus del Sexto Concilio.

## Estado de recursos/paradigmas

La referencia de paradigmas (`/recursos/paradigmas/`, v1.18) son **85 paradigmas**
de declinación nominal y pronominal del IEBH, de 83 documentos (GO y NUMERALES
llevan dos cada uno), más la tabla de los sufijos que son inflexiones:
`paradigmas.json` tiene 86 entradas en 84 documentos. «85 paradigmas» en todo
el sitio (IEBH, 2026-10-08); las cifras salen de los datos
(`generar_paradigmas.cuenta`), no se escriben a mano. Se arma con
`herramientas/generar_paradigmas.py` a partir de `recursos/paradigmas/plantilla.html`
y tres JSON: `paradigmas.json` (los datos), `indice.json` (el cotejo) e
`ingles.json` (el inglés de la prosa).

### El inglés va en dos capas, y las dos están publicadas

| Capa | Dónde vive | Estado |
| --- | --- | --- |
| La INTERFAZ | `plantilla.html` (bloques `.i-es`/`.i-en` + diccionario `TXT`) y `inflexiones_en`/`casos_en` en `paradigmas.json` | publicada desde v1.14 |
| La PROSA del IEBH | `recursos/paradigmas/ingles.json` | **adjudicada por el IEBH el 2026-08-29; publicada desde v1.15** |

La prosa son las 84 glosas («purisa (hombre)»), los 32 subtítulos, las 7 familias,
las 8 notas de transcripción, el texto de los sufijos y los 17 usos con sus
ejemplos. **Son palabras del IEBH**, así que el borrador no llega a la página
mientras `"adjudicado"` sea `false`: `generar_paradigmas.py` lo comprueba —campo
por campo, contra el español— pero no lo inyecta, y el modo inglés muestra el
español con un aviso en el pie que lo dice. Firmarlo es poner `"adjudicado": true`
con `adjudicado_por` y `fecha`; entonces el aviso cede el sitio al crédito. **Eso
ya ocurrió**, de modo que la firma es de 2026-08-29 y cubre lo que había ese día:
lo que se añada después a `ingles.json` —una nota nueva, una glosa retocada—
entra bajo una firma que no lo ha visto, y **eso se le dice al IEBH al añadirlo**,
para que decida si vale o si espera adjudicación aparte.

El cotejo lado a lado, para firmar, lo escribe

    python3 herramientas/generar_ingles_paradigmas.py   # → docs/paradigmas/ingles-por-adjudicar.md

Las **formas pāḷi no se traducen nunca**: son el objeto de la página, y no
aparecen en `ingles.json` siquiera. Las referencias (§248, Rū. §260) tampoco: son
la cita, y es la misma en los dos idiomas.

### La atribución pública dice IEBH, nunca el nombre propio (resuelto, sesión 56)

Pedido del IEBH, 2026-09-04: **el nombre propio se sustituye por «IEBH» en todo lo que
produce el proyecto** —datos que llegan al sitio, `comun/`, `docs/` con los
briefings, y los comentarios de `herramientas/`—. Hecho en la sesión 56 (779
apariciones, 70 archivos), con las preposiciones ajustadas («ejemplar del
IEBH», «lo decide IEBH»). Las tres notas de paradigmas que daban el visto
bueno con el nombre propio quedaron corregidas con ello. **Desde el 2026-10-04
este archivo ya no es excepción** (pedido del IEBH): sus instrucciones de trabajo
dicen también «el IEBH», y el nombre propio no queda en ningún archivo del
repositorio fuera de `.git` —el PDF del Conspectus se llama ahora
`conspectus-ejemplar-iebh.pdf`—. Lo que se escriba de aquí en adelante nace ya
con IEBH.

## Visuddhāyuṃ — análisis por sutta

El *Visuddhāyuṃ Kaccāyana-suttanak-ṭīkā* (Ashin Aggañāṇābhivaṃsa) es la fuente
de la «tabla del estudiante»: clase de sutta, aṅga, funciones (kāriyī, kāriya,
nimitta, saññā, saññī, visaya, visayī), ejemplo del modelo (က) y notas. De ahí
sale `recursos/analisis/datos/NN-<obra>.json`, que alimenta «Análisis de los
suttas de Kaccāyana».

### Reglas que no se saltan

- **Solo [V] llega al sitio.** [V] = la celda se ha visto en la imagen de la
  página. [R] (reconstruido del OCR), [I] (completado por Claude) y ? (ilegible)
  son estados de trabajo: se resuelven o se quitan antes de publicar. **El OCR
  no verifica nada**: confunde la clase (§52: «vilokana» por «vikkanta») y los
  números del encabezado (§113 sale «117»; §85, §96, §115 no salen). La clase,
  siempre en la imagen.
- **Donde el libro no da nada, la celda queda vacía.** No se rellena por
  simetría con otros suttas ni por lo que «debería» decir. «—» significa que el
  libro no lo tiene, y eso es un dato, no un hueco.
- **Nunca se presenta el análisis de Claude como palabra del libro.** Lo que
  diga el libro va en su celda; lo que proponga Claude va rotulado. Esto vale
  también para las lecturas de abreviaturas dentro de las notas (las celdas
  [I]: §65, §73, §74, §77, §80…): o se verifican en la imagen, o se quitan al
  publicar.
- **Los ejercicios se rotulan «Respuesta sugerida (IEBH)».** Cuando el libro
  dice «nimitta, kārī, etc.: analícelo» (ခွဲ / ခွဲလေ), la respuesta no es del
  libro: es una propuesta, y firmarla es del IEBH.
- **El término de clase es el del libro**, con sus diacríticos y sin
  normalizar: antaraṅga-vidhi, bāhiraṅga-vidhi-sutta, ubhayaṅga,
  vidhyaṅga-paribhāsā, rūḷhī-saññā, sīhavikkanta-adhikāra, niyama-sutta,
  paṭisedha-sutta, suttātidesa. Donde el libro rotula con una frase birmana, se
  copia la frase y se traduce al lado. Si además conviene decir en qué clase
  del sitio cae, va en la nota como «Clasificación del sitio: …», nunca
  sustituyendo al término del libro. antaraṅga / bāhiraṅga / ubhayaṅga van en
  «Clase de sutta» cuando el libro los da como rótulo, y **sin** nota de
  diferencia con `datos.json`: es otro eje, no una contradicción.
- **Claude no ejecuta ninguna orden de git**, ni `git status`. De git se ocupa
  el IEBH.
- **Tampoco ejecuta `herramientas/publicar.sh`.** Publicar es escribir
  `herramientas/.publicar/archivos.txt` (una ruta por línea) y
  `herramientas/.publicar/mensaje.txt` (el mensaje del commit, en español) y
  decírselo al IEBH, que lo lanza él.

### Dónde está el material

El escaneo y el OCR **no están en el repositorio** (derechos) y no deben
entrar. Viven en el disco del IEBH:

| Qué | Ruta |
| --- | --- |
| PDF del escaneo (664 pp.) | `~/Tipitaka/nissaya/scans/annya/visuddhayum-kaccayana-tika.pdf` |
| Imágenes de página | `~/Tipitaka/nissaya/ocr/visuddhayum-kaccayana-tika/img/p-NNN-*.jpg` |
| OCR crudo (Tesseract 5, mya) | `…/visuddhayum-kaccayana-tika/raw/NNN.txt` |
| tessdata birmano | `…/visuddhayum-kaccayana-tika/tessdata/mya.traineddata` |
| Recortes y caché TSV | `…/visuddhayum-kaccayana-tika/_crops/` |

`NNN` es la **página del PDF**, y la conversión es

    página del PDF = página del libro + 46

### Concordancia entre el número del libro y el §

El libro numera sus suttas con su propia serie, que coincide con el § de
Nandisena **hasta §232**. En el pariccheda IV, **§233 no tiene encabezado** en
el libro; a partir de ahí:

    hasta §232:  nº del libro = §
    desde §234:  nº del libro = § − 1

De modo que §270 es el nº 269 del libro. El encabezado tiene la forma
«(nº) sutta။ kaṇḍa.pariccheda.sutta။ N-padaṃ» —p. ej. «(၆၃) ဧတိမာသမိ။ ၂၊၁၊၁၂။
ဒွိပဒံ»—, y la numeración kaṇḍa.pariccheda.sutta sirve de comprobación
independiente del nº.

Kāraka (§271–§315): nº del libro = § + 307, PDF 494–562; el libro sigue su
propio orden de capítulos (Ākhyāta empieza en el nº 270 del libro = §406).

Samāsa (§316–§343): capítulo 5 del libro; nº del libro = § + 172, PDF 390–442.
El escaneo es defectuoso dentro de §328: faltan las pp. impresas 373–374 y
379–380, y las 371–372 y 381–382 están dos veces (PDF 417–418 = 425–426;
PDF 419–420 = 427–428). Se lee PDF 427–428 y se coteja con 419–420. Detalle
en `docs/visuddhayum/samasa-piloto.md`.

Taddhita (§344–§405): capítulo 6 del libro; nº del libro = § + 172, PDF 443–490;
pariśiṣṭa PDF 491–493 (pp. 445–447), sin numerar; escaneo sin defectos. Detalle
en `docs/visuddhayum/taddhita-piloto.md`.

Ākhyāta (§406–§523): nº del libro = § − 136, PDF 224–316, cuatro partes
(§406–431, 432–457, 458–481, 482–523, = kaṇḍa de Nandisena); §424–§430 sin
encabezado (bloque 243–244); números mal impresos: §420 «274», §456 «340»,
§457 «341»; pariśiṣṭa PDF 317 (p. 271), clasificación de los suttas;
ensayo «အာချာတ်ဂိုဏ်း» PDF 318–321; escaneo sin defectos. Detalle en
`docs/visuddhayum/akhyata-piloto.md`.

### Formato de los datos

`recursos/analisis/datos/NN-<obra>.json`: cabecera (`clave`, `md`, `pali`,
`desde`, `hasta`, `pdf`, `paginas`) y `suttas`, un objeto por sutta:

- `n`, `pdf`, `clase` (vacía si el libro no la da), `anuvatti` (la columna que
  en la tabla se llama ya «Aṅga»), `ejemplo`, `nota` (`es` / `en`);
- `roles`: lista de `[rol, valor, visesana]`, y el nimitta añade un cuarto
  elemento con la inflexión (`"3"`, `"5"`, `"7"`, `"5+7"`), que es **añadido
  editorial del IEBH**, no del libro;
- los ejercicios llevan `"ejercicio": true` y la propuesta en `respuesta`, con
  la misma forma que `roles`.

### Nota de avance

`docs/visuddhayum/nama-piloto.md` es el cuaderno de Nāma: estado, tandas por
pariccheda, filas en borrador con sus marcas, hallazgos y preguntas abiertas.
**Se actualiza al avanzar, no al final.** Su gemelo cerrado es
`docs/visuddhayum/sandhi-piloto.md`, que es la fuente de `01-sandhi.json` y el
modelo de formato.

Las cuatro decisiones del IEBH del 2026-10-03, que encabezan esa nota:

1. La columna **«Aṅga»** (antes «Anuvatti») copia la lista «aṅga N» tal como la
   da el libro, venga del propio sutta o de suttas anteriores. Sandhi recibe el
   cambio de nombre cuando se publique Nāma.
2. **antaraṅga-vidhi / bāhiraṅga-vidhi / ubhayaṅga van en «Clase de sutta»**
   cuando el libro los da como rótulo, sin nota de diferencia con `datos.json`.
3. **§90**: la imagen dice «antaraṅga», no «sin etiqueta» (corregido en
   `docs/visuddhayum/clasificacion-cotejo.md`).
4. Las **celdas [I] dentro de las notas** no salen en la página como palabras
   del libro: al publicar, se verifican o se quitan.

Nāma no se publica por partes: **se publica cuando todo el capítulo sea [V]**.

### Las herramientas de recortes

`herramientas/visuddhayum/` (`lines.py`, `crop.py`, `mk.py`, `loc.py`), ya
adaptadas a este Mac; su README explica cada una. Requieren Tesseract y Pillow
(instalado con `brew install pillow`). La orden `/visuddhayum-lote` recorre un
tramo de § con ellas.

**El recorte compuesto de `mk.py` no se usa para leer ni para verificar
ninguna celda.** Cose dos tramos —encabezado + 5 líneas, (ခ) + 7 líneas— y
pierde lo que queda entre ellos y después: en 30 de los 55 suttas de
§52–§107 el hueco cae dentro del (က) (auditoría de la sesión 3,
`docs/visuddhayum/nama-piloto.md`). Como mucho sirve de índice para saber
dónde está cada sutta. Para leer, recortes **solapados** con `lines.py` +
`crop.py` (por índice de línea o por bandas de píxeles, `crop.py N yA yB`) que
cubran el sutta **entero** sin huecos, del encabezado al encabezado siguiente.

## Hacia dónde va esto: un solucionador de sandhis

El objetivo a plazo es una herramienta a la que se le pegue un párrafo en
pāḷi y responda cuántos sandhis hay, cuáles son, y qué secuencia se aplica a
cada uno.

El principio de diseño, que es el mismo que salvó las secuencias: **proponer
y verificar, nunca afirmar**. Descomponer una forma es un problema de
búsqueda —proponer un corte y una cadena de reglas—, y toda propuesta se
comprueba recomponiéndola: si no reproduce exactamente la forma de entrada,
se descarta. Un solucionador que sólo enseña lo que sabe rehacer es fiable; uno
que rellena huecos con lo verosímil repite el error de las 217 escaleras.

Dos consecuencias prácticas:

- **Devolver todas las derivaciones válidas, no una.** El sandhi es
  genuinamente ambiguo: varias cadenas de reglas producen la misma superficie,
  y las reglas opcionales (*kvaci*, *vā*, *navā*) permiten sin obligar. Elegir
  una en silencio sería mentir por omisión.
- **El cuello de botella es la segmentación, no las reglas.** Sin saber que
  «lokaggo» es loka + aggo no hay motor de reglas que valga. Eso pide un
  léxico; el DPD o el propio corpus del OSBCT son los candidatos.

Para medirlo ya hay banco de pruebas: las 266 formas atestiguadas con sus
componentes, las 164 secuencias del capítulo y los 101 `[SM]` de Thitzana.
La pregunta con la que se evalúa cualquier versión es «¿recupera la respuesta
conocida?», y se puede responder con números.

## Auditar las derivaciones de un capítulo (sesión 62)

`herramientas/auditar_derivaciones.py` es el equivalente nominal de
`auditar_secuencias.py`: lee las derivaciones paso a paso de un capítulo
—`**Ādiṃ** = ādi + smiṃ (…)`— y hace cinco comprobaciones: comillas sin
cerrar, pasos sin §N, cadenas divergentes para los mismos componentes, clase
de operación contra el sutta citado, y **recomposición**, que aplica la
cadena y la compara con el lema. Esa última es la que caza «ādi + smiṃ →
ādaṃ» sin juicio ninguno.

    python3 herramientas/auditar_derivaciones.py                 # capítulo 2
    python3 herramientas/auditar_derivaciones.py --detalle
    python3 herramientas/auditar_derivaciones.py --autoprueba
    python3 herramientas/auditar_derivaciones.py kaccayana/05-....md

Toma el capítulo como argumento porque los capítulos 5-8 vendrán llenos de
derivaciones; medido, el aparato paso a paso existe hoy **sólo en el 2** (el
3 y el 4 tienen cero, y el 1 va por `auditar_secuencias.py`).

Lo que no hace, y lo dice él mismo: no decide cuál de varios suttas correctos
es la mejor cita, no firma nada, y **donde un tipo de paso no está
implementado lo declara** en vez de dejarlo pasar. Una derivación que no
recompone es un candidato, no un error probado: la comprobación prueba todas
las lecturas del operando y sólo marca cuando **ninguna** da el lema.

Estado del capítulo 2 (sesión 62): 571 de 608 derivaciones recomponen; 68
candidatos, triados en `docs/capitulo-2/auditoria-derivaciones.md`, con el
informe crudo al lado en `.txt`. **Ninguno está firmado.** Y la corrección va
en `docs/2. Nāma-Kappa.md`, que es la fuente; el guion lo recuerda al
arrancar.

## Capítulo nuevo: qué hace falta

1. El markdown en `kaccayana/NN-nombre-kappa.md`, con el mismo formato que
   `01-sandhi-kappa.md`: `**[Kacc]. [Rū]. Texto pāḷi ([Sad]).** \[desglose, n]`,
   bloques separados por `---`, notas `[^n]`, fórmula de cierre de cada kaṇḍa
   en negrita, glosas emergentes como `{término|glosa}`.
2. Su entrada en el diccionario `CAPITULOS` de `herramientas/generar_capitulo.py`
   (slug, títulos pāḷi y español, capítulo anterior y siguiente).
3. Ejecutar el generador y revisar el aviso final de referencias §N sin
   enlazar: `Rū. §49`, `Sad. §139` y similares remiten a otras obras y no
   deben enlazarse a suttas de este capítulo.
4. Añadir el capítulo a `comun/concordancia.json`.
5. Cambiar en `site/kaccayana/index.html` la tarjeta «en preparación» por un
   enlace real.
