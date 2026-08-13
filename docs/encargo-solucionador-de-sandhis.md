# Encargo: solucionador de sandhis

Documento para entregar a quien vaya a construirlo.

## Antes de nada: compruebe que lo tiene todo

Este encargo da por supuesto que tiene a mano, en su proyecto, los archivos
del trabajo sobre el Sandhi-kappa. Compruebe que están éstos:

**Datos y herramientas**

- `recursos/sandhi/reglas.json` — 49 reglas y 266 formas
- `kaccayana/01-sandhi-kappa.md` — los 51 aforismos traducidos
- `recursos/combinacion-eufonica.md` — el documento de Bhikkhu Nandisena
- `comun/concordancia.json` — numeración Kaccāyana / Rūpasiddhi / Saddanīti
- la carpeta `herramientas/` y el archivo `CLAUDE.md`

**Fuentes de consulta**

- **Kaccāyana Volume 2 (Ven. A. Thitzana)**, en markdown. Es imprescindible:
  sin él no podrá seguir las referencias por número de línea que da este
  encargo, y se quedará sin los 101 métodos `[SM]`, que son la fuente más rica.
- **Kaccāyana 2 – Nāma-Kappa (U Nandisena)** y la edición PTS
  (*Kaccāyana-Kaccāyanavutti*, Pind), para cotejos.

Si le falta alguno, y en particular el volumen de Thitzana, pídalo antes de
empezar.

## Qué se pide

Una herramienta que reciba texto pāḷi y responda, para cada punto de sandhi:

- cuántos hay y dónde están;
- cuáles son los componentes antes de la combinación;
- qué secuencia de suttas de Kaccāyana explica la forma resultante.

**Empiece por una sola voz, no por un párrafo.** Dada `lokaggo`, devolver
`loka + aggo` con la secuencia. El párrafo exige además detectar *dónde* hubo
sandhi, que es un problema distinto y más difícil (ver «El cuello de botella»).
Una herramienta que resuelva una voz ya es útil para un estudiante.

## La regla que no se negocia

**Proponer y verificar. Nunca afirmar.**

Descomponer es un problema de búsqueda: se propone un corte y una cadena de
reglas, se aplica esa cadena, y se comprueba que reproduce **exactamente** la
forma de entrada —ignorando apóstrofos, espacios y guiones—. Si no coincide,
se descarta. No se publica ni se muestra nada que no haya pasado esa prueba.

Esto no es una preferencia de estilo. Este proyecto ya tuvo 217 secuencias
generadas por un modelo de lenguaje sin comprobar, y contenían cuatro clases
distintas de error: reglas citadas que no pueden producir el cambio, formas
archivadas bajo la regla equivocada, reglas mal numeradas y pasos que aplicaban
mal las reglas mecánicas. Hubo que tirarlas y rehacerlo todo. La verificación
por recomposición es lo que permitió recuperar 185 secuencias sin inventar
ninguna.

**Devolver todas las derivaciones válidas, no una.** El sandhi es
genuinamente ambiguo: varias cadenas producen la misma superficie, y las
reglas opcionales (*kvaci*, *vā*, *navā*) permiten sin obligar. Elegir una en
silencio es mentir por omisión. Devolverlas ordenadas, con su cadena de
suttas, y que el lector juzgue.

## Los datos que ya existen

| Dónde | Qué |
| ----- | --- |
| `recursos/sandhi/reglas.json` | 49 reglas y 266 formas atestiguadas con componentes, resultado, referencia canónica y secuencia |
| `kaccayana/01-sandhi-kappa.md` | los 51 aforismos traducidos, con 164 secuencias de formación |
| `recursos/combinacion-eufonica.md` | el documento de Nandisena: reglas y tablas de formas |
| `comun/concordancia.json` | numeración Kaccāyana / Rūpasiddhi / Saddanīti |
| `recursos/sandhi/suttavibhaga.json` | las 14 sub-suttas de §20 por *suttavibhāga* y las 8 citas «ca» atestiguadas |
| Thitzana vol. 2, capítulo de Sandhi | ~101 bloques `[SM]` con el método en prosa |

En `reglas.json` cada forma dice de dónde sale su secuencia: `verificada` (49,
copiadas de la traducción), `derivada` (175, calculadas y comprobadas),
`aforismo` (42, construidas desde el aforismo). Nueve llevan `nota`; cuatro de
ellas señalan erratas probables de la fuente.

En el volumen de Thitzana cada ejemplo trae `[V]` el vutti, `[CS]` la frase
atestiguada, `[SS]` la separación en componentes y **`[SM]` el método**: qué
suttas se aplican y en qué orden, en prosa inglesa. Es la fuente más rica para
saber qué secuencia corresponde a qué forma.

### La forma de los datos

Una forma de `reglas.json`, con todos sus campos:

```json
{
 "f": "lokaggo",              // la forma atestiguada
 "comp": "loka + aggo",       // componentes, como los da el documento
 "ref": "Ap. i 166",          // referencia canónica
 "sec": "sara",               // sara | byanjana | niggahita | pakati
 "rule": "1",                 // número de regla DENTRO de esa sección
 "title": "Una vocal que precede a otra vocal se elide",
 "kac": 12,                   // aforismo de Kaccāyana de esa regla
 "s": ["loka aggo",
       "lok a aggo (§10)",
       "lok aggo (§12)",
       "lokaggo (§11)"],      // la secuencia
 "full": true,
 "derivada": true             // procedencia: verificada | derivada | aforismo
}
```

**Convención de los pasos**, que es el contrato de análisis: el texto va
primero, con los segmentos separados por espacios, y la anotación entre
paréntesis al final. `(§10)` cita un aforismo; `(«ca» en §20)` cita el «ca» de
uno; `(EM)` marca la forma de la edición moderna, con apóstrofo. Un paso puede
citar dos aforismos: `(§35, §23)`.

Al comparar formas, normalice: los apóstrofos (`’`), los espacios y los
guiones no cuentan. `yassindriyāni` y `yass’ indriyāni` son la misma forma.

### Aproveche lo que ya está escrito

`herramientas/derivar_secuencias.py` ya tiene un derivador por aforismo —§12,
§13, §15, §16, §17/§18/§21, §28, §35—, cada uno escrito a partir de una
secuencia verificada del capítulo, y todos con la comprobación por
recomposición ya montada. **El solucionador es en buena medida ese archivo del
revés**: donde aquél va de componentes a forma, éste va de forma a componentes.
Conviene leerlo antes de escribir nada.

`herramientas/auditar_secuencias.py` tiene además la tabla `OPERACIONES`, que
dice qué clase de operación hace cada aforismo —elisión, alargamiento,
sustitución…—. Sirve para podar el árbol de búsqueda.

## El banco de pruebas

Existe, y es lo que hace medible el proyecto: **266 formas atestiguadas con
sus componentes, 164 secuencias del capítulo y ~101 métodos `[SM]`**.

La pregunta con la que se evalúa cualquier versión es: *dada la forma
atestiguada, ¿recupera el solucionador los componentes y la secuencia conocidos?*
Se responde con un número. Cualquier cambio en el motor debe informar de si ese
número sube o baja.

## Lo que hay que saber de la gramática antes de empezar

Se aprendió por las malas; ahorra semanas.

**§10 y §11 son el andamiaje.** §10 separa la consonante final sin vocal de la
voz **anterior** (`yassa` → `yass a`); §11 vuelve a unir al final. Casi toda
secuencia empieza por §10 y termina por §11. §10 **nunca** opera sobre la voz
siguiente.

**El «ca» de un sutta hace más de lo que dice su enunciado.** Cuando un paso
hace una sustitución que ningún enunciado cubre, lo probable no es que falte
una regla: es el «ca» de alguna. Se cita como «"ca" en §20». Thitzana
documenta el mecanismo —*suttavibhāga*, la división del sutta—. Las catorce
sub-suttas de §20 están en el propio capítulo (§20) y transcritas en
`recursos/sandhi/suttavibhaga.json`, que es donde conviene leerlas.

**§51 es el sutta comodín** y por eso el más rico en patrones: reúne 41
secuencias ya traducidas. Conviene mirar ahí antes de dar una forma por inexplicable.

**Pakati-sandhi es la ausencia de operación.** Sus formas no llevan secuencia
porque no ocurre nada; no son datos incompletos y no hay que «arreglarlas».

## El cuello de botella

No son las reglas: es la segmentación. Sin saber que `lokaggo` es
`loka + aggo`, ningún motor de reglas sirve. Hace falta un léxico: el DPD
(Digital Pāḷi Dictionary) o el corpus del Sexto Concilio que mantiene el IEBH.
Conviene pedir acceso a uno de los dos y resolver esto antes de invertir en
sofisticar el motor de reglas, que es la mitad fácil.

## Lo que no se debe hacer

- **No inventar pasos** para completar una secuencia que no verifica.
- **No elegir una derivación** entre varias válidas sin decir que hay más.
- **No editar nada dentro de `site/`**: es salida generada, se reconstruye
  entera y cualquier cambio hecho ahí desaparece sin avisar.
- **No dar por buenos los datos heredados** sin cotejarlos con el documento
  fuente. Ese fue el error que costó una tarde entera.

## Qué no es sandhi

Conviene no contar de más. El sandhi es la combinación eufónica de letras al
juntarse dos voces. **No** es sandhi la formación de palabras —*taddhita*,
*kita*—, aunque el resultado se le parezca. El propio Thitzana lo advierte al
presentar las funciones por *yogavibhāga*: «these examples are not Sandhi but a
kind of word-form changes only».

Por la misma razón, en este proyecto la cadena de pasos se llama **secuencia**
y nunca «derivación»: en gramática pāḷi la derivación es la formación de
palabras, y usar la misma palabra para las dos cosas confunde al lector. Está
fijado en `comun/glosario.md`, que es normativo.

## Entregables sugeridos

1. `herramientas/solucionar_sandhis.py` — dada una voz, devuelve las derivaciones
   válidas con su cadena de suttas.
2. Un informe de cobertura contra el banco de pruebas: cuántas de las 266
   recupera, cuántas falla, y por qué.
3. Sólo después: segmentación y modo párrafo.

### Cuándo está terminada la primera etapa

Cuando, dada cualquiera de las 266 formas atestiguadas, la herramienta
devuelva sus componentes y al menos una cadena de suttas que los recomponga
exactamente; cuando informe con un número de cuántas recupera y cuántas no; y
cuando de las que no, diga por qué falló en lugar de callarlo.

No hace falta que acierte las 266. Hace falta que se sepa cuántas acierta.
