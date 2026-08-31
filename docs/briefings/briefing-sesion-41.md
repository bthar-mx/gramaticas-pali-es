# Kaccāyana Pāḷi-Español: Briefing de la Sesión 41

*Complementa a los briefings 05–40. Tema de la sesión 41 (2026-08-31): **el
§5.1–5.3 de la 40**, o sea comprobar a ojo el capítulo XX del Saddanīti, leer
los §§ 143-195 y resolver el § 34. Las tres cosas están hechas. Y las tres
dieron algo distinto de lo que la 40 había dicho, **incluido su hallazgo
principal**. No entra ninguna regla nueva. Lo que entra es un aparato leído
entero, un tramo del Suttamālā leído por primera vez, y un titular rectificado.*

> **Lo primero que tiene que saber el chat nuevo:** verificar
> `git log origin/main..main` **en el momento** — el ciclo empuja solo. Las
> reglas de siempre: el Python es la referencia; los CINCO arneses mandan, y
> **uno a uno**; nada se adjudica sin el visto bueno del IEBH; todo se mide
> antes y después; la atribución pública dice IEBH. Con Angel se habla en
> inglés; lo del proyecto va en español.
> **Y el criterio que manda sobre todo**, ya en `CLAUDE.md` con las palabras de
> Angel: hay formas de sandhi teóricamente plausibles que son inverosímiles en
> el Tipiṭaka. Recomponer no basta. Atestiguar la pieza no atestigua la juntura.
> **Esta sesión le encontró respaldo textual** — véase §4 —, pero *respaldo* no
> es *adjudicación*, y quien adjudica es él.

## 0. EL ESTADO, EN CIFRAS

| | al abrir la 41 | al cerrarla |
| --- | ---: | ---: |
| textos del corpus separado | 80 | 80 |
| junturas distintas | 2.045 | 2.045 |
| ecuaciones | 141 | 141 |
| casos adjudicados | 195 | 195 |
| señal «segura» / «posible» | 2.300 / 2.185 | 2.300 / 2.185 |

**Ninguna cifra del motor se movió, y está bien que no se moviera:** esta
sesión no tocó el motor. Tocó una fuente que estaba mal leída.

Lo que sí se movió es la concordancia del Saddanīti:

| | la 40 | la 41 |
| --- | ---: | ---: |
| páginas comprobadas **a ojo** | 3 de 39 | **39 de 39** |
| entradas en estado «ocr» | 44 | **0** |
| suttas con correspondencia de Kaccāyana | 47 | **53** |
| marcas identificadas como **Kcv**, no Kc | 0 | **5** |
| suttas del capítulo | 1-195 (mal) | **1-191** |
| páginas del capítulo | 604-642 (mal) | **604-641** |

## 1. LO QUE SE PIDIÓ Y LO QUE SALIÓ

Las tres tareas del §5 de la 40, por orden:

1. **Comprobar a ojo las 36 páginas que faltaban.** Hechas, y además re-leída
   la 605 (que la 40 daba por vista) porque el error de Kc/Kcv la afectaba en
   principio. No la afectaba: sus cuatro marcas son Kc de verdad.
2. **Leer los §§ 143-195.** Leídos — y son **143-191**, porque el capítulo
   acaba en el 191.
3. **La discrepancia del § 34.** Resuelta: **«Kc 14»**. gramsut tenía razón y
   el OCR se equivocaba.

## 2. EL HALLAZGO DE LA 40 NO ERA LO QUE PARECÍA, Y LO QUE ES ES MEJOR

La 40 encabezaba su documento con esto: «entre el § 73 y el § 125 no hay ni una
marca de Kaccāyana — cincuenta y tres suttas seguidos». **La pág. 622 imprime:**

    ‖ § 73—85 Kcv 20 ‖

y la 621, justo antes: `‖ § 72 Kcv 20 = Rūp 27 Cᵉ 11⁸ ("ca") ‖`.

De modo que **Smith remite la serie entera de sustitución de consonantes a la
vutti del sutta 20 de Kaccāyana**, el «Do dhassa ca» — que es **exactamente el
suttavibhāga que el proyecto ya tiene documentado en `CLAUDE.md`** con sus
catorce sub-suttas. No es materia que Kaccāyana no tenga: es materia que
Kaccāyana tiene **en la vutti**.

**Y así el hallazgo es mejor que el que se creyó tener**: Nandisena lo
documenta en §20, Thitzana en su vol. 2 pp. 138-140, y ahora **Smith por
tercera vez y por su lado**. Tercer testimonio independiente del mecanismo del
«ca» de §20, que es una de las piezas de las que cuelga el capítulo.

**La cifra correcta del tramo**, ya que se cita: sin marca de **Kc** van del
**§ 69 al § 125, cincuenta y siete** —el último Kc antes es el § 68 → Kc 29, y
el primero después el § 126 → Kc 50—, pero el tramo **no está mudo**. Sin
ninguna marca de ninguna clase quedan los **§§ 86-123**, treinta y ocho.

## 3. POR QUÉ FALLÓ EL OCR — tres mecanismos, los tres reproducibles

Conviene que quede escrito, porque no es mala suerte:

1. **El recorte.** `-y 1850 -H 820` a 300 dpi empieza en el 70,5% de la altura.
   Donde el cuerpo del texto acaba pronto, **el aparato empieza más arriba** y
   sus primeras líneas caían fuera. Así se perdió la **página 618 entera**
   (§§ 52-56) y con ella el § 64, el § 73—85, el § 124, los §§ 145-147 y el
   § 153. **Catorce marcas perdidas.**
2. **«Kc» casa dentro de «Kcv».** Cinco marcas que Smith da a la Kcv se
   atribuyeron a Kaccāyana: §§ 17-18, 55, 72, 73—85 y 139.
3. **Y al revés.** Las págs. 637 y 638 citan «Kc 139», «Kc 499», «Kcv 2» como
   notas al pie corrientes. **Sólo cuenta lo que va entre dobles barras.**

**«Kcv» queda como DUDA.** Es obra distinta de «Kc» en el aparato y se cita
también por número de sutta; el § 72 («Kcv 20 = Rūp 27») apunta a la
**Kaccāyana-vutti**, porque Rūp 27 es el correspondiente de Kc 20 en la
concordancia del proyecto. **No está adjudicado**: se buscó la lista de siglas
de Smith en el material preliminar de los vols. 01, 03 y 05 y no apareció.
Hasta que aparezca, las cinco marcas Kcv **no cuentan** como Kaccāyana.

## 4. LOS §§ 143-191, LEÍDOS — y tres cosas que tocan al motor

El detalle está en `docs/solucionador/saddaniti-lo-que-kaccayana-no-tiene.md`
§4 quater. Lo que hay que saber:

**a) La metátesis del § 154** —*pariyudāhāsi > payirudāhāsi*, *ariyassa >
ayirassa*, *kariyā > kayirā*, *masakā > makasā*— **no tiene equivalente en
Kaccāyana**, y es operación de otra clase: no elide, no sustituye, no inserta;
**reordena**. Un motor que sólo componga y elida no la propone nunca.

**b) Tres suttas dedicados a «eva»** —§§ 175, 178, 179—, que es la familia sin
firmar de más masa de `docs/solucionador/familias-no-sabe.md` (49.484 fichas):
*yathā eva > yathar-iva*, *pa-g eva*, *haññe eva*. Y el **§ 191 es «iti»**, lo
de la sesión 39. Y el **§ 160**, entre sus ejemplos, imprime **«Samantapāsādikā
iti eva · Samantapāsādikā tv eva»** — la lectura adjudicada de «tveva»
(`cb9b56d`), **dicha por el Saddanīti**. Testimonio, no adjudicación: se anota
y lo decide el IEBH.

**c) Y lo que más importa: el Saddanīti tiene suttas que PROHÍBEN el sandhi.**

    185  donde unir la vocal deja la palabra incómoda de pronunciar, no hay sandhi
    186  donde la vocal unida ESTROPEA EL SENTIDO, no hay sandhi  («Āyasmā Ānando»)
    187  en dos padas, no hay sandhi de vocales ante consonante

y en el § 168, de su propia mano, la razón de que algunas reglas se enuncien
*aniyamavasena*: *sotūnaṃ sammoho* y ***rūpānañ ca atippasaṅgo***, «confusión
del oyente y **exceso de formas**».

**Eso es el §4 ter del documento dicho en el siglo XII.** El motor propone
varias lecturas que recomponen todas y no sabe separarlas; el Saddanīti
sostiene que la juntura **se bloquea cuando estropea el sentido** — y el
sentido no está en las reglas, está en la frase. Es el argumento del §9.8 del
briefing 39 **dicho por la autoridad, y en forma de sutta, no de glosa**.

Se remata en la pág. 640, cerrando el capítulo: Aggavaṃsa dice que el Bhagavā
**no** altera las palabras por métrica ni por comodidad —*na hi Bhagavā chandañ
ca vuttiñ ca rakkhati*—, que eso es *lokopacāramattavasena*. El propio
Saddanīti acota hasta dónde llegan sus reglas de eufonía cuando el texto es
Buddhavacana.

## 5. LO QUE HAY QUE CORREGIR DE MÍ MISMO (principio 5)

1. **El titular de la 40 era falso, y la 40 tenía cómo saberlo.** Había
   comprobado a ojo la pág. 623 —que en efecto no lleva marcas— y **no la 622**,
   que es donde estaba «§ 73—85 Kcv 20». Comprobar una página de un tramo y
   afirmar el tramo entero es lo que su propio documento decía que no se hace.
2. **Escribió «el OCR genera y el ojo adjudica» y luego adjudicó con el recorte
   del OCR.** Mirar UNA página entera, de arriba abajo, en vez de la franja,
   habría enseñado que el aparato empieza más arriba de lo que el recorte
   suponía. La frase estaba bien; no se cumplió.
3. **Alcance de lo corregido, para que se sepa cuánto desconfiar:** 14 marcas
   perdidas, 5 mal atribuidas, 2 notas de paréntesis mal, 1 discrepancia, los
   límites del capítulo y 4 suttas que no eran del capítulo. Nueve suttas pasan
   de «hueco» a tener Kaccāyana.
4. **Lo que la 40 hizo bien y no hay que perder:** los §§ 9 y 10 —«Kc 605» y
   «Kc 604», donde gramsut calla— están **confirmados a ojo**, y el § 49 sigue
   sin marca, visto ya dos veces. Los dos testimonios de la 39 se sostienen. Y
   el §4 bis y el §4 ter —las 416 discrepancias del motor— **no dependían del
   aparato y no se mueven**.

## 6. LO QUE SIGUE (en orden)

**Lo de fondo, que sigue mandando y no lo cambia esta sesión:**

1. **Conectar el texto corrido del OSBCT** (39 §9.8; 40 §3). **Primero de
   todo**: es lo único que alcanza a las 44.998 fichas de las 296 junturas donde
   el motor corta en otro sitio. Y ahora, además, tiene respaldo en la propia
   autoridad: los §§ 185-186 del Saddanīti dicen que la juntura se decide por el
   sentido, no por las reglas.
2. **Que la ficha de caso admita varias lecturas con su discriminante**
   (39 §9.3). Sin eso «tveva» y sus hermanas no se registran bien.
3. **El fallo de la segunda voz** (38 §9.4, 39 §9.2), con la DUDA de la 40: en
   la masa de las 416 lo que falla es el PUNTO DE CORTE y con él las dos voces.
   Puede que sean dos hilos y no uno. **No me toca decidirlo.**

**Lo que abre esta sesión, y es para el IEBH:**

4. **Enseñarle los §§ 185-186 y el § 154.** Los primeros porque son autoridad
   diciendo lo que él dijo en `CLAUDE.md`, y quizá quiera citarlos; el segundo
   —la metátesis— porque es una clase de operación que el capítulo no tiene.
5. **Enseñarle el § 160 del Saddanīti** con su «Samantapāsādikā iti eva · tv
   eva», por lo que toca a la adjudicación de «tveva».
6. **Averiguar qué obra es «Kcv»** en las siglas de Smith. Mientras tanto, las
   cinco marcas Kcv no cuentan como Kaccāyana.

**Lo que ya venía y sigue en su sitio:**

7. **Enseñar al IEBH lo pendiente del briefing 38**: el diagnóstico de su §1 con
   sus tres testigos, y la decisión del resguardo de su §3 (313 correctas contra
   2 malas).
8. **Las escaleras sin derivar**: la auditoría da 16 casos.
9. **La lista corta de las 69** (37 §3 quater) por el modo revisión.
10. **El `git add -A`** de la línea 172 del ciclo (38 §7 y §9.8; 39 §4). El
    patrón correcto está escrito al lado, en `archivar_cola()`.
11. **La firma de familias** de `docs/solucionador/familias-no-sabe.md`: «eva»
    (masa 49.484), «iva» (45.729), «ati» (20.745)… **Y ahora «eva» tiene tres
    suttas del Saddanīti que la tratan** (§§ 175, 178, 179), que es material
    para esa firma.
12. Resto del mapa 33. **Sin empezar.**

## 7. AVISOS AL CHAT NUEVO

Los del briefing 39 §7 y 40 §6 siguen todos en pie —los 165 s de bash, los
procesos que no sobreviven entre llamadas, la caché de la señal que no mira
`operaciones.py`, los arneses uno a uno, el `.git/index.lock` que se pega, el
aviso de «referencias §N sin enlazar» del gancho de pre-commit (que con
referencias al Saddanīti **es correcto que avise**), y usar
`herramientas/casan_las_voces.py` para medir el motor contra el banco—. Tres
añadidos de hoy:

- **Para leer el aparato de Smith, NO recortar por fracción fija.** El aparato
  empieza donde acaba el cuerpo, y eso varía de página en página. Lo que
  funciona es recortar **del 60% para abajo** y mirar la imagen entera; la
  detección automática de la regla de nota no es de fiar (la línea más larga de
  la mitad baja resultó ser un defecto del escaneo, no la regla).
- **Y leerlo a ojo, no por tesseract.** A 300 dpi con el recorte ancho se lee
  cómodo. El OCR sirve para generar candidatos y ya se ha visto lo que cuesta
  confundirlo con la lectura.
- **Los PDF del Saddanīti no viajan** (`.gitignore` excluye `*.pdf`). Si hacen
  falta en otra máquina se rebajan de archive.org con los identificadores que
  dice `recursos/saddaniti/LEEME.md`. Los `.paginas.json` sí viajan, y son los
  que dan la equivalencia página impresa ↔ hoja del PDF.

## 8. PROCEDENCIA

- La concordancia del capítulo de sandhi **se atribuye al aparato de Helmer
  Smith**, Saddanīti parte III, págs. 604-641, y está ahora **leída a ojo** por
  entero sobre el escaneo.
- Los enunciados de los §§ 143-191 del §4 quater se leen **de la edición de
  Smith**, no de bhaddacak.github.io, cuya licencia CC BY-NC-ND permite
  consultar y no redistribuir. Su concordancia (`xrefUtil.xrefList`) se usó
  **sólo como generador**, y en el § 34 acertó donde falló el OCR.
- **Nada se adjudicó en esta sesión.** El inventario del §2 y el del §4 son de
  candidatos y de testimonios; quien adjudica es el IEBH.
