# Instrucciones del proyecto

Si hay conflicto entre este archivo y `comun/convenciones.md`, manda
`comun/convenciones.md`.

## Qué es este repositorio

Traducciones al español de gramáticas clásicas pāḷi. Público lector:
estudiantes hispanohablantes de pāḷi con formación budista.

## Reglas

- **Con Angel se habla en inglés. Todo lo demás va en español**: el sitio, los
  briefings, los mensajes de commit, los comentarios del código. Una respuesta
  en el chat es para Angel y va en inglés **entera**, también los bloques que
  le pases para copiar.
- **Nada de verbos ingleses conjugados en español** —«commitear», «pushear»,
  «empujado», «mergear», «testear»—. La tabla y el porqué, en
  `comun/convenciones.md` §0.
- Registro formal y doctrinal; no coloquial.
- Términos técnicos pāḷi sin traducir, con diacríticos completos
  (nibbāna, saṅkhāra, kāraka); cursiva en la primera aparición de cada sección.
- Consultar `comun/glosario.md` antes de fijar la traducción de un término.
  Si no está, proponerlo y añadirlo — no improvisar caso por caso.
- Ante duda gramatical o de lectura, decirlo explícitamente en lugar de
  suponer. Marcar con `<!-- DUDA: ... -->`.
- Dar la referencia (sutta, obra, edición) al afirmar algo sobre el texto.
- No reescribir secciones ya revisadas sin que se pida.
- Nunca añadir, quitar ni cambiar nada más allá de lo que da estrictamente la
  edición base sin avisar explícitamente y dejar que Angel decida. Esto incluye
  las expansiones morfológicas (pasos de elisión o sustitución que Nandisena no
  menciona). Lo tomado de Ven. A. Thitzana se señala siempre como suyo.

## Gestión de la sesión

Corresponde a Claude —no a Angel— avisar cuando la conversación se ha alargado
lo bastante como para convenir abrir una nueva. El aviso se da **antes** de que
la calidad se resienta, no después, y no espera a que Angel lo pregunte.

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

## Cómo se publica

El markdown es la fuente; el HTML de `site/` es salida generada. **Nunca se
edita nada dentro de `site/`, con tres excepciones que son fuente y no salida:
`site/assets/pali.css`, `site/assets/pali.js` y los SVG de la marca en
`site/assets/`** — ningún generador los escribe. Todo lo demás lo reconstruye
entero el hook de pre-commit en cada commit, así que un cambio hecho ahí
desaparece sin avisar y sin dejar rastro. Lo que se edita está en
`kaccayana/`, `recursos/`, `comun/` y esos tres archivos de `site/assets/`.

Cada `git push` a `main` despliega en
<https://gramaticas.buddha-dhamma.net> (Cloudflare Workers, ver
`wrangler.jsonc`).

    # capítulo de una gramática
    python3 herramientas/generar_capitulo.py kaccayana/02-nama-kappa.md

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
incorporarlo, para que Angel decida y se le dé el crédito al Venerable.

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
