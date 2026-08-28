# Solucionador de sandhis — estado del encargo

*24 de agosto de 2026.*

---

## Lo que el encargo pedía, y dónde está cada cosa

> «Una herramienta que reciba texto pāḷi y responda, para cada punto de sandhi:
> cuántos hay y dónde están; cuáles son los componentes antes de la combinación;
> qué secuencia de suttas de Kaccāyana explica la forma resultante.»
>
> «**Empiece por una sola voz, no por un párrafo.** Dada `lokaggo`, devolver
> `loka + aggo` con la secuencia.»

| | estado |
|---|---|
| **una sola voz → componentes + secuencia** | hecho y medido |
| **el párrafo → dónde hubo sandhi** | señal medida, con precisión conocida |
| los compuestos | fuera, por su instrucción; y ahora el motor lo dice con esas palabras |

---

## La medida

Hasta esta semana el proyecto sólo se medía contra su propio banco: de las 266
formas de `reglas.json`, 251 son medibles y hoy acierta **221 —88 %—**. Ese
número dice qué tan bien reproduce el material del que salió. Un examen que uno
se escribe a sí mismo, y con una circularidad más que conviene declarar: 18 de
las voces que usted usa como componente no están en el DPD —`putha`, `vipali`,
`ani`, `chayo`—, y se agregaron al léxico porque están firmadas por usted. Con
el DPD solo el número es **208 —83 %—**, y el informe lo calcula, no lo recuerda. **El número que vale es el de afuera**, y esas 18
voces no lo mueven en absoluto.

Ahora hay una medida de afuera. Se trajo el corpus del proyecto anterior, que
resolvió la partición de la Therīgāthā entera y su comentario, y se comparó
forma por forma:

| | formas medidas | **coincide el punto de corte** |
|---|---:|---:|
| Therīgāthā (versos) | 698 | **630 · 90,3 %** |
| Therīgāthā-aṭṭhakathā | 7.178 | **6.496 · 90,5 %** |

Las dos medidas son independientes —verso y prosa comentarial, vocabularios muy
distintos, siete mil formas la segunda— y coinciden en un decimal. En el 75 %
de los casos coinciden además **las dos voces**; el resto de la diferencia es de
convención, no de análisis: el otro proyecto cita lemas —`na + abhijānāti`— y
éste cita voces flexionadas —`na + abhijānāmi`—.

**Los compuestos se sacaron del denominador antes de medir**, y el criterio se
validó donde correspondía: sobre las **306 formas firmadas de su banco** marca
cero. No excluye sandhis; excluye compuestos.

---

## Lo que la medida hizo corregir

Medir contra material ajeno encontró en un día dos defectos que 251 formas
propias no habían encontrado en semanas.

**El generador de candidatos nunca restituía vocal y niggahīta a la vez.** De
`paripucchiṃ + ahaṃ`, el §38 elide la niggahīta y el §12 la vocal; en la
superficie queda `paripucch`. El código sabía devolver una o la otra, nunca las
dos, y la voz correcta no se proponía jamás. Son 18 formas sólo en los versos,
casi todas aoristos de primera persona ante `ahaṃ`.

**Faltaban dos cadenas.** `op_38` sólo continuaba por el camino de la nota 17
—§12 y además §15, que alarga—. Pero `paripucchahaṃ` tiene la `a` breve: la
continuación es §12 sola. Y `cārihaṃ`, de `cāriṃ + ahaṃ`, es §38 y después §13.
Ninguna se inventa: §12 y §13 se aplican por su propio enunciado en cuanto §38
dejó dos vocales en contacto.

---

## Dónde detenerse: resuelto, y con una fuente que ya teníamos

Usted escribió en el encargo:

> «El cuello de botella no son las reglas: es la segmentación… Hace falta un
> léxico: el DPD o el corpus del Sexto Concilio que mantiene el IEBH.»

Era el DPD, y más de lo que parecía. Además de las formas flexionadas, el DPD
publica **su propia descomposición** de 852.542 de ellas —2.058.431 en total—.
No es una heurística nuestra: es un segundo testigo, hecho por otra gente con
otro método.

Lo primero fue cotejarlo: **de las 493 formas con sandhi de la Therīgāthā que el
DPD descompone, las 493 coinciden con el corte del corpus.**

| | marca de cada 100 | se ven | de lo marcado tiene juntura |
|---|---:|---:|---:|
| versos | 10,4 | **71 %** | 96 % |
| comentario | 19,2 | **79 %** | 84 % |

En el texto hay 11,8 y 15,6 sandhis cada cien palabras: **se ven siete y ocho de
cada diez.** Con lo que teníamos hace dos días se veían menos de tres.

Y ordena, no sólo marca: la lectura correcta aparece primera en **508 de 630** en
verso y **5.380 de 6.496** en prosa.

**Se probaron nueve criterios y sobrevivieron dos**; los siete descartados van con su cifra —«termina en un nipāta»
acierta una de cada cinco veces; «once letras o más», una de cada cuatro; la
frecuencia en un corpus de un millón de fichas, una de cada tres—. Están medidos
en `LA-DETECCION-medida.md` para que nadie los vuelva a intentar.

**Y el corpus del Sexto Concilio se probó también, y no rinde**: sus cuarenta
volúmenes dan 43.000 formas contra las 443.740 del DPD, y contienen sólo el 30 %
de las piezas necesarias. De paso apareció algo que le va a interesar: **la capa
de texto de esos PDF no trae ni una sola «ṃ»** —todas salieron como «ñ»—, y las
reparamos dejando que el DPD arbitre cada forma.

## Los tres silencios

Decir «sin resolver» a tres cosas distintas hacía parecer que la herramienta
falla todo el tiempo. Ahora son tres, y se dicen distinto:

- **voz entera, sin corte** — está en el léxico y ningún corte la parte en dos
  voces reales. *No hay nada que separar.* Es la respuesta, no una falla.
- **compuesto, fuera del encargo** — se parte en dos voces sin ninguna operación.
- **sin resolver** — con el motivo escrito, y sólo entonces.

---

## Lo que sigue faltando, dicho sin adorno

**El orden de las lecturas.** El motor devuelve todas las que recomponen —trece
por forma— y no elige, que es lo correcto. Ordenarlas por «segunda voz que es
partícula» pone la correcta primera el 61 % de las veces en los versos y el 79 %
en el comentario, contra un 44 % y un 34 % antes. Sigue siendo mucho ruido.

**Los compuestos internos.** Lo que queda mudo son formas de tres o más piezas
—`dhammacakka + pavattana + suttanta + desanā`—. El solucionador parte en dos,
una vez. Ir más adentro es análisis de compuestos, que usted excluyó.

**Ninguna regla de sandhi falta, entre lo medido.** Los 46 desacuerdos de los
versos se verificaron uno por uno contra las lecturas que el motor sí devuelve:
20 coinciden en cuanto se deja de lado la desinencia, 16 son formaciones con
sufijo, 7 piden tres piezas, y de los 10 restantes cuatro son compuestos con
`sat`, tres son formas irregulares, uno es un hueco del léxico —`bhāgamanīyāni`
no está en el DPD— y en uno nuestra lectura parece la mejor. Queda **uno solo**
sin explicar, y va abajo como pregunta.

**§51 ya opera.** Estaba escrito pero fuera del orden de aforismos que el motor
prueba, porque actúa sobre una sola voz y el proponedor razona sobre pares. Al
entrar, el banco pasa de 196 a 198 de 251, y el corpus no se mueve: no agregó
ruido. Con las 18 voces suyas que el DPD no trae, el banco llega a **221**.

---

## Lo que espera su visto bueno

Está todo congelado, sin tocar, hasta que usted decida.

1. **Byañjana 3.1.** El documento trae, en prosa y sin numerar, bajo byañjana 3:
   «Y también a veces, la "o" de "eta", cuando va seguida por una vocal, se
   elide». ¿Va como regla 3.1 con sus dos ejemplos, o como nota de alcance?

2. **Cinco formas de interdicción** de sara 9, 10 y 11 —`atīsigaṇo`,
   `atīritaṃ`, `itīti`, `patīto`, `abhicchitaṃ`— no están en el banco. Si
   entran, el denominador pasa de 266 a 271. (`adhīritaṃ` sí está, en `ce[19]`.)

3. **Tres erratas del PDF original**, con lo que en cada caso parece lo correcto:
   pág. 10 `ati + antaṃ` → `icc antaṃ`; pág. 14 `eso ābhogo` → `esa ābhogho`;
   pág. 16 `ni + cayo` → `nicchayo`.

4. **El signo de sustitución** en las notas 11 y 12 quedó como comilla de
   apertura —`ty “ c`— donde la nota 10 usa `=`. Es errata del impreso, no de
   nuestra conversión: la página impresa muestra la comilla.

5. **Cuatro erratas** en sus Tablas de secuencias.

6. **La versión ampliada corregida** no se autoriza hasta que usted la apruebe.

7. **Las 42 secuencias marcadas `aforismo`** en `reglas.json`: ningún script
   nuestro las produce. ¿Las construyó usted a mano?

8. **La privativa `na`, ante consonante.** Su propio banco la explica ante
   vocal con §51: `na abhineyya` → `an abhineyya` → `anabhineyya`, transposición
   de la «n». Pero `na + laddhā` → `aladdhā` pierde la «n» en vez de
   transponerla, y eso §51 no lo dice. Se buscó enunciado en el capítulo 1, en
   los siete aforismos de fuera que tenemos, en el sandhi-kappa de Thitzana y en
   el de la Rūpasiddhi: no está. ¿Pertenece al compuesto negativo —y queda
   entonces fuera del encargo—, o hay un aforismo que se nos escapó?

---

## Cómo verlo funcionar

    pantalla.bat          la pantalla: se pega una voz o un texto
    probar-corpus.bat     repite las dos medidas contra el corpus
    probar-cobertura.bat  repite la medida contra las 266 del banco

Todas las medidas de este informe se reproducen con esos tres archivos, en la
misma máquina, sin red. En tiempo de consulta no hay modelo: resuelve código
determinista leyendo un banco congelado con huella. La misma voz da la misma
respuesta el martes y el jueves.


---

## Lo añadido el 24 de agosto

**Su `sandhi-6.html`.** Sus 51 aforismos con las tres numeraciones, sus 41 reglas
y sus 261 formas están en `concordancia-nandisena-51.json`, extraídos sin editar
y con la huella del HTML. **No se usan todavía como fuente del motor**, y el
motivo está escrito dentro del archivo: sus documentos difieren entre sí en
algunos puntos, y decidir cuál gobierna es suyo. El día que lo diga, se
incorpora y se vuelve a medir.

Cotejado contra esas 261, el motor propone su corte en **194 de 209 medibles —93 %—**.
De las 15 que no salen, ocho son filas donde dos entradas quedaron pegadas en el
mismo campo —`parakkamo taṇhakkhayo`, `jāty + andhojāc + andho`, `bodhi + aṅgo
bodhy + aṅgo bojh + aṅgo`—, que es de donde sale la diferencia entre sus 261 y
las 266 de `reglas.json`.

**Cuatro cosas que ese cotejo hizo corregir**, todas nuestras:

- el generador de candidatos no sabía **devolver la niggahīta** —de `taññeva`
  nunca se proponía `taṃ + eva`—;
- faltaba el **«vā» de §31** para la «l», que su regla niggahita 2 enuncia:
  `saṃ + lekho`, `saṃ + lakkhaṇā`, `puṃ + liṅgaṃ`;
- faltaba la **«ḷ» de `cha-ḷ-abhiññā`**. §35 enumera ocho consonantes y la «ḷ»
  no está entre ellas, pero **su nota 9 sí la enuncia** —«Se inserta "ḷ" después
  de "cha" y numerales»—: se implementó por la nota y se cita por la nota;
- y una comprobación interna descartaba **en silencio** toda cadena anotada «(por
  "ca" en §41)» o «(por "vā" en §31)», por leer mal el paréntesis.

Con esos cuatro, el banco pasó de 211 a **221 de 251** y sus 261 de 185 a **194
de 209**, sin mover el corpus.

## Una discrepancia entre dos documentos suyos

En `myāyaṃ` y `tyāhaṃ` —los dos únicos ejemplos de §17— la pestaña de las 261
formas cita **§15** donde la pestaña de reglas del mismo archivo y su traducción
del Sandhi-kappa citan **§25**. Los dos aforismos se llaman «Dīghaṃ»: §15 es
sara 3, «cuando la vocal anterior ha sido elidida, la siguiente se alarga»; §25
es byañjana 1, «una vocal seguida de consonante se alarga». Después de §17 la
«e» ya es «y», consonante. El motor sigue a las dos que dicen §25.

## Y dos consultas que se retiran

Íbamos a preguntarle por la **«ḷ»** de `cha-ḷ-abhiññā` y por la **«h» y la «g»**
de §35, que el aforismo no enumera. **Su nota 9 las enuncia las tres**, al pie de
esa misma regla, y la «g» tiene además sus propios aforismos, §42 y §43. No eran
huecos. Se retiran antes de hacerlas.
