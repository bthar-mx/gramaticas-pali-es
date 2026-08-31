# El capítulo de sandhi del Saddanīti: qué trae que Kaccāyana no tiene

*Sesión 40, 2026-08-30. Responde al punto 1 de §9 del briefing 39: ir a buscar
las otras reglas que Kaccāyana no tiene, en vez de encontrarlas una a una como
fallos. El sutta 49 se halló persiguiendo un fallo; esto es el barrido.*

> **Nada de lo que sigue está adjudicado.** Es un inventario de candidatos con
> su procedencia y su estado de comprobación. Decir qué regla explica qué voz
> es del IEBH, no de este documento.

> **AVISO DE LA SESIÓN 41 (2026-08-31), y hay que leerlo antes que nada.**
> Las 39 páginas del capítulo están ahora **comprobadas a ojo, una a una**, que
> era el encargo del §5.1 del briefing 40. **El barrido por OCR de la sesión 40
> fallaba por los dos lados**, y el hallazgo que encabezaba aquel documento —«§§
> 73-125: cincuenta y tres suttas seguidos sin ni una marca de Kaccāyana»— **no
> se sostiene tal como estaba dicho**: el aparato imprime «‖ § 73—85 Kcv 20 ‖».
> El §3 y el §4 quedan reescritos abajo; el §7 dice el alcance entero de lo que
> hubo que corregir. Lo que NO cambia es el §4 bis y el §4 ter: las 416
> discrepancias del motor están medidas contra el banco, no contra el aparato,
> y ninguna cifra suya se mueve.

---

## 1. Lo primero: gramsut genera, Smith decide

El briefing 39 §6 nombra `/gramsut` como la herramienta para esto. Lo es, pero
**como generador de candidatos, no como autoridad**, y hay dos medidas que lo
dicen.

**Primera: su cobertura.** El buscador guarda su concordancia en
`assets/js/xrefutil.js`, en `xrefUtil.xrefList`: **803 grupos** de suttas
equivalentes, con las obras marcadas por letra (`k` Kaccāyana, `r` Rūpasiddhi,
`m` Moggallāna, `p` Payogasiddhi, `n` Niruttidīpanī, `s` Saddanīti). De los
**1.347** suttas del Suttamālā, sólo **506** aparecen en algún grupo. Los otros
**841** no aparecen en ninguno. Eso no significa que Kaccāyana no los tenga:
significa que la reconstrucción no llega.

**Segunda, y es la que zanja:** el propio editor advierte que la concordancia
está reconstruida a partir de notas de la Niruttidīpanī y «no está bien
comprobada». Se comprobó, y falla por defecto. Para los suttas **9 y 10**
gramsut no da ninguna correspondencia, y el aparato de Smith imprime
«§ 9 Kc 605» y «§ 10 … Kc 604». **La ausencia en gramsut no es ausencia.**

Donde sí sirve, y mucho, es en lo contrario: cuando gramsut *afirma* una
correspondencia, coincide con Smith en todos los casos cotejados
(3↔3, 4↔4, 5↔5, 6↔6, 43↔17, 44↔18, 46↔19, 50↔20, 51↔21, 57↔44, 58↔45,
66↔27, 67↔28, 68↔29).

**Y coincide también en el caso que importaba.** El sutta 49 **no aparece en
ninguno de los 803 grupos**. El aparato de Smith, en la pág. 617, imprime
«§ 50 Kc 20» y «§ 51 Kc 21» y **nada para el 49**. Dos testimonios
independientes de lo mismo, que es lo que la sesión 39 sostuvo con uno solo.

## 2. La autoridad es el aparato de Smith, y es legible

Smith imprime las correspondencias entre dobles barras al pie de cada página,
con esta forma exacta:

    || § 50 Kc 20 ||        || § 51 Kc 21 ||
    || § 3 Kc 3 ||          || § 6 Kc 6, Mmd Ce 14 ||
    || § 8 (Kc 8) ||        || § 25-26 cf. Kc 79 ||

Los paréntesis y el «cf.» marcan correspondencias flojas; la barra sola, la
firme. **Lo que no lleva marca no tiene sutta correspondiente**, y ésa es la
señal que se buscaba.

### El capítulo, acotado — **corregido en la 41**

| | |
| --- | --- |
| obra | Saddanīti Suttamālā, capítulo 1 (= **XX** en la numeración corrida de Smith) |
| suttas | **§§ 1 – 191** |
| páginas impresas | **604 – 641** |
| páginas del PDF, vol. 03 | **11 – 48** |
| el capítulo XXI empieza en | **la pág. impresa 641, la misma**, con el § 192 |

La 40 daba 604-642 y decía que el XXI empezaba en la 643. **Las dos cosas son
falsas, y se ven a ojo.** En la pág. 640 acaba el texto —«Vomissakasandhi-
vidhānaṃ niṭṭhitaṃ» y la estrofa de cierre—; **arriba de la 641 va el colofón**:

    Iti navaṅge sātthakathe piṭakattaye vyappathagatisu viññūnaṃ
    kosallatthāya kate saddanītippakaraṇe sandhikappo nāma vīsatimo paricchedo.

y **debajo, en esa misma página**, «XXI.», la estrofa «Ito paraṃ pavakkhāmi
Nāmakappaṃ hitāvahaṃ…» y el § 192. De donde se sigue una cosa que importa: los
**§§ 192-195, que la 40 metía en su tramo de huecos «150-195», son ya del
Nāmakappa** y no pintan nada aquí.

La correspondencia entre página impresa y página del escaneo sale del
`_page_numbers.json`, y **se comprobó contra el dato conocido**: la sesión 39
dio la pág. impresa 617 como la 24 del PDF, y el mapa da lo mismo. Los cinco
volúmenes corren continuos, de la pág. impresa 2 a la 1460.

### Cómo se leyó, y por qué hubo que volver a leerlo

La 40 recortaba la franja del aparato y la pasaba por tesseract:

    pdftoppm -r 300 -f 11 -l 49 -x 0 -y 1850 -W 1700 -H 820 -png <vol03> a
    tesseract a-024.png - --psm 6

**La 41 lo comprobó a ojo, las 39 páginas**, sobre la imagen a 300 dpi, sin
tesseract de por medio. Ya no queda ninguna entrada en estado «ocr» en
`comun/concordancia-sadd-kac-sandhi.json`.

**Y el OCR fallaba por tres sitios, que conviene dejar dichos porque los tres
son reproducibles:**

1. **El recorte.** `-y 1850` a 300 dpi es el 70,5% de la altura. En las páginas
   donde el cuerpo del texto acaba pronto **el aparato empieza por encima de esa
   línea**, y sus primeras líneas quedaban fuera del recorte. Así se perdió la
   **página 618 entera** —§§ 52, 53, 54, 55, 56—, y con ella el § 64, el
   § 73—85, el § 124, los §§ 145-147 y el § 153.
2. **«Kc» casa dentro de «Kcv».** El aparato distingue las dos obras y el patrón
   no: cinco marcas que Smith da a la **Kcv** se atribuyeron a Kaccāyana
   (§§ 17-18, 55, 72, 73—85, 139).
3. **Y al revés: «Kc» aparece en notas que no son concordancia.** Las págs. 637
   y 638 citan «Kc 139», «Kc 499», «Kcv 2», «Kcv 159» como notas al pie
   corrientes. **Sólo cuenta lo que va entre dobles barras.**

### «Kcv» es obra distinta de «Kc», y qué obra sea es una DUDA

En el aparato, «Kcv N» y «Kc N» son cosas distintas y ambas van por número de
sutta. Lo que apunta a la **Kaccāyana-vutti**: el § 72 imprime «Kcv 20 = Rūp 27
Cᵉ 11⁸ ("ca")», y Rūp 27 es el correspondiente de Kc 20 en la concordancia que
este proyecto ya tiene (`CLAUDE.md`: «Kc 20 = Rūp 27»).

**No se adjudica.** Se buscó la lista de siglas de Smith en el material
preliminar de los vols. 01, 03 y 05 y no apareció. Hasta que aparezca, «Kcv» se
registra como Kcv y **no se cuenta como correspondencia de sutta de
Kaccāyana**.

<!-- DUDA: dónde imprime Smith su lista de siglas. Está en alguna parte de la
     introducción (que va en francés) o en los índices del vol. 04/05, y no se
     halló con el barrido de las primeras y últimas páginas. Mientras tanto,
     «Kcv = Kaccāyana-vutti» es inferencia del § 72, no lectura. -->

**El ojo, además, precisó tres marcas que el OCR daba a medias:** el § 33 es
«Sd 42²¹—43²¹» y no «Sd (reenvío interno)»; el § 44 va **entre paréntesis**,
«(Kc 18)», que la 40 no anotaba; y el § 126 va **sin** paréntesis, que la 40
sí anotaba.

## 3. EL HALLAZGO, RECTIFICADO: la serie está en la VUTTI del § 20

*Lo que sigue reemplaza al §3 de la sesión 40, que decía «entre el § 73 y el
§ 125 el aparato no imprime ni una sola marca de Kaccāyana». Comprobado a ojo,
**no es así**, y el propio tramo lo desmiente en su primera línea.*

**La pág. 622 imprime, y se ha visto a 300 dpi ampliada:**

    ‖ § 73—85 Kcv 20 ‖

y la 621, dos líneas antes de empezar el tramo:

    ‖ § 69 Sd 372⁹ ‖        ‖ § 72 Kcv 20 = Rūp 27 Cᵉ 11⁸ ("ca") ‖

**De modo que la serie de sustitución de consonantes no es materia que
Kaccāyana no tenga: es materia que Smith remite a la vutti del sutta 20** —el
«Do dhassa ca»—, **que es exactamente el suttavibhāga que este proyecto ya
tiene documentado** en `CLAUDE.md` con sus catorce sub-suttas (*To dassa*,
*Ṭo tassa*, *Ko gassa*, *Lo rassa*, *Jo yassa*…). Nandisena lo documenta en
§20 del capítulo, Thitzana lo documenta en su vol. 2, pp. 138-140, y **ahora
Smith lo documenta por tercera vez y por su lado**, al mandar los §§ 72-85 del
Saddanīti a la misma vutti.

Es mejor hallazgo que el que se creyó tener: no es una laguna de Kaccāyana, es
**un tercer testimonio independiente del mecanismo del «ca» de §20**.

### Lo que sí queda, dicho con la cifra correcta

| | la 40 decía | comprobado a ojo |
| --- | --- | --- |
| tramo sin marca de **Kc** | §§ 73-125 (53 suttas) | **§§ 69-125 (57 suttas)** |
| ¿sin ninguna marca? | «ni una sola» | **no**: § 69 Sd, § 72 Kcv, § 73—85 Kcv, § 124 Sd |
| último Kc antes | — | **§ 68 → Kc 29** (pág. 620) |
| primer Kc después | — | **§ 126 → Kc 50** (pág. 626) |

O sea que el tramo **empieza antes** de lo que se dijo y **no está mudo**. Sin
ninguna marca de ninguna clase quedan los **§§ 86-123**, treinta y ocho suttas
seguidos: el final de la sustitución de consonantes y toda la formación de
conjuntos.

Y el contenido del tramo, que es lo que se leyó en la 40, sigue siendo el que
era: **una serie**.

**§§ 73-101 — sustitución de consonante, una por sutta:**

    73. to dassa.          «t» por «d»
    74. ṭo tassa.          «ṭ» por «t»
    76. tro ttassa.        «tr» por «tt»
    77. ko gassa.          «k» por «g»
    78. lo rassa.          «l» por «r»
    79. jo yassa.          «j» por «y»
    80. bo vassa.          «b» por «v»
    81. ko yassa.          82. yo jassa.      83. ko tassa.
    84. co tassa.          85. pho passa.     86. dro dassa.
    87. gho khassa.        88. do jassa.      91. ṇo nassa.
    92. ṇassa ca no.       93. dho dassa.     94. vo yassa.
    96. lassa ḷo.          97. do kassa.      98. po massa.
    100. po vissa vassa ca.                   101. vo passa.

y el sutta que cierra la serie, § 102, que la generaliza:
«vuttāvuttānaṃ byañjanānaṃ aññabyañjanattampi».

**§§ 104-119 — formación de conjuntos**, que es materia de juntura directa:

    104. tayadayānaṃ saññogoccayugajjayugaṃ.   'tya' → 'cca', 'dya' → 'jja'
    106. thayadhayānaṃ cchayugajjhayugaṃ.      'thya' → 'ccha', 'dhya' → 'jjha'
    107. tathānaṃ ṭṭhayugaṃ.                   110. layānaṃ llayugaṃ.
    108. kayānaṃ kkayugaṃ jjayugañca.          111. vayānaṃ bbayugaṃ.
    109. cayajayānaṃ ccayugajjayugaṃ.          112. syo ssayugaṃ.
    113. gyo ggayugaṃ.   114. pyo ppayugaṃ po ca.   115. ghyo ggho.
    116. ṭyo ccayugaṃ.   117. nyo ññayugaṃ ṇyo ca.  118. bhyo bbhayugaṃ.
    119. mmayugaṃ myo.

**§§ 120-125 — reglas sobre el conjunto mismo:** pérdida de la consonante
igual entre tres (120), duplicación (121), contacto y no contacto (122-123),
asimilación en conjunto heterogéneo (124).

**Qué es esto y qué no, dicho con cuidado.** Es una serie que Kaccāyana no
enuncia, y por tanto una serie que un solucionador que sólo sepa Kaccāyana no
puede proponer. **No es, hoy, una carencia del motor**: se midió después de
escribir esto y ninguno de sus fallos reales viene de aquí — véase el §4 bis,
que es lo que manda sobre este párrafo. Lo que vale del hallazgo es el
inventario: saber que existe y dónde está, para no volver a tropezar con estas
reglas de una en una.

## 4. Los otros huecos del capítulo — **la lista de la 40 se cae casi entera**

La 40 daba esta lista de huecos «pendientes de comprobar a ojo». Comprobados,
**la mitad no eran huecos**. Va primero el saldo y después la lista buena.

| lo que la 40 llamaba hueco | comprobado a ojo |
| --- | --- |
| 52-56 | **§ 52 Kc 22, § 53 Kc 42, § 54 Kc 43, § 55 Kcv 49, § 56 Kc 35** — la pág. 618 entera se le había escapado |
| 64 | **§ 64 Kc 25** |
| 143-147 | **§ 145 Kc 34, § 146 Kc 37, § 147 Kc 38 + 39**; quedan sólo el 143 —entre paréntesis con el 142— y el 144 |
| 150-195 | **§ 153 Kc 30**; y §§ 192-195 no son de este capítulo |
| 32, 69, 134 | tienen marca, pero al **Saddanīti mismo**, no a Kaccāyana |
| 37-42, 45, 47, 48, **49**, 70, 71, 127-128, 131, 135, 136 | **confirmados**: sin ninguna marca |

**El § 49 sigue en pie**, que era lo que importaba de la sesión 39: la pág. 617
imprime «‖ § 50 Kc 20 ‖» y «‖ § 51 Kc 21 ‖» y **nada para el 49**, y ahora está
visto dos veces. El **47** —«itissa tisaddabyañjanopi», otra vez «iti»— también
se confirma sin marca.

### Los huecos de verdad, comprobados

Sin **ninguna** marca en el aparato, en todo el capítulo: **96 suttas de 191.**
Por tramos:

    11, 13, 16, 24
    37-42     conjunto previo, elisión ante 'iva', 'ayya/añña/aggha/ussa'
    45, 47-49 'u' de hetu/dhātu; «itissa…»; elisión de la 'i'; y el 49
    70, 71
    86-123    ← el tramo mudo de verdad: 38 suttas seguidos
    125, 127, 128, 131, 135, 136, 143, 144
    150, 151, 154-156, 161-165, 168-191

La tabla entera, entrada por entrada y con su página, en
`comun/concordancia-sadd-kac-sandhi.json`.

## 4 bis. LA MEDIDA, y sale que no — al menos aquí

Antes de proponer nada al motor se midió, que es el orden. Y la medida dice
**que ninguno de estos candidatos hace falta hoy**, en el banco con que se mide
el motor. Conviene que conste, porque la propuesta era mía y la medida la
desmiente.

Sobre las **2.045 junturas** de `recursos/corpus-separado/junturas.json`, con
el comparador de `herramientas/casan_las_voces.py` —que existe por lo que dice
el §7 y pasa sus 14 pruebas—. «Casa» significa que la segunda voz del IEBH y
la del motor son la misma, escritas una de superficie y otra subyacente.

| dónde queda la lectura del IEBH | junturas | masa |
| --- | ---: | ---: |
| **es la PRIMERA que da el motor** | **1.618** | 183.909 |
| está entre las suyas, pero no primera | 308 | 45.398 |
| no está | 108 | 3.041 |

Es decir: **416 junturas (masa 48.439) en las que la primera lectura del motor
no es la del IEBH.** Y ninguna de esas 416 se explica por sustitución de
consonante (§§73-101) ni por formación de conjunto (§§104-119).

### La familia «āha», y por qué no la arregla el orden

La de más masa es una sola: el motor lee «iha» donde el texto tiene «āha».

    tenāha        6.018   el texto: tena + āha      el motor: tena + iha
    ādimāha       3.961   el texto: ādim + āha      el motor: ādimā + iha
    evamāha       1.455   yathāha 1.098   tenevāha 981   sandhāyāha 802
    panāha          103   mamāha 4

**El porqué está localizado**, y no es una regla que falte. En
`solucionar_sandhis.py` las lecturas se ordenan, y el tercer criterio del
desempate premia que la última voz sea **nipāta**. «iha» está en la lista de
nipāta; «āha», que es verbo, no. Bajo `SOLO_CANON` los dos criterios anteriores
—los del DPD— quedan inertes, y decide ése.

Se midieron dos maneras de tocarlo, **sin cambiar nada todavía**:

| | arregla | rompe |
| --- | ---: | ---: |
| quitar el criterio de nipāta | 78 (masa 16.797) | **940 (masa 61.937)** |
| bajar sólo «iha», dejando el criterio | 1 (masa 1.455) | 0 |

**El criterio de nipāta es carga de muro: quitarlo cuesta doce junturas por
cada una que gana.** Es lo que pone «taṃ+ca» delante de «ta+añca» y
«tassa+eva» delante de «ta+asseva». No se toca.

Y bajar «iha» tampoco resuelve la familia: arregla **una** juntura, porque
debajo de «tena+iha» esperan «tena+ha», «tena+aha», «tena+īha» — todas legales
por las reglas, ninguna la del texto. La lectura buena, «tena+āha», está ahí:
está enterrada.

**Que es el §1 de `CLAUDE.md` en estado puro.** Varias lecturas recomponen;
sólo una es la que el texto dice; y nada de lo que el motor ve las separa,
porque para separarlas hace falta la frase. **El arreglo no es de orden ni de
sutta: es el texto corrido del OSBCT** (briefing 39 §9.8), o la ficha de varias
lecturas con su discriminante (§9.3).

**Cautela:** el banco son 2.045 junturas de 84 textos separados, no el canon.
Que aquí no aparezca un candidato no dice que no aparezca. Y el corte del IEBH
no es la verdad —lo dice `medir_contra_corpus.py`—: es otro proponente, de modo
que estas 416 son desacuerdos, no errores demostrados.

## 4 ter. LAS 416, DESPIEZADAS — y una hipótesis mía que no resiste

Deshechas por familias, las 416 no son cuatrocientas cosas: son casi una sola.

**En 296 de 416 —masa 44.998, el 93%— la voz que el texto pone segunda empieza
por vocal.** «āha», «ettha», «assa», «atthaṃ», «attho», «aparaṃ», «ahaṃ»,
«etaṃ», «āyasmā», «ādāya», «akāsi», «avoca». Y lo que el motor pone en su lugar
no es otra partícula: es **otro punto de corte**.

    panettha    2.286   el texto: pana + ettha      el motor: panetta + ha
    cettha      2.140   el texto: ca + ettha        el motor: cetta + ha
    athassa     1.790   el texto: atha + assa       el motor: ate + hassa
    panassa     1.731   el texto: pana + assa       el motor: pa + anassa
    caparaṃ     1.548   el texto: ca + aparaṃ       el motor: capi + araṃ
    tassattho     857   el texto: tassa + attho     el motor: ta + assattho

De ellas, 87 (masa 26.445) son además el caso del nipāta del §4 bis. El resto
no: el motor sencillamente corta en otro sitio.

### La hipótesis, y por qué se cae

Mirando esas primeras voces —«panetta», «cetta», «ate», «capi», «ādimā»— parecen
fragmentos, no palabras. De ahí la hipótesis: **premiar las lecturas cuya
primera voz esté atestiguada en la edición.** Medida sobre las 416:

| ¿está atestiguada la primera voz? | junturas | masa |
| --- | ---: | ---: |
| la del motor sí, la del texto no | 244 | 25.761 |
| las dos sí | 91 | 21.582 |
| ninguna | 74 | 926 |
| **la del motor no y la del texto sí** | **7** | **170** |

**La hipótesis no sirve, y se cae por los dos lados.** Por abajo: sólo 7
junturas —masa 170, el 0%— tienen la primera voz del motor sin atestiguar.
«panetta» y «cetta» ESTÁN en la edición. Por arriba, y es lo que la mata: en
244 casos la voz atestiguada es la del motor y la que NO lo está es la del
texto, porque el IEBH escribe la voz elidida de superficie —«pan», «c», «ath»,
«tass»— y ésas no son formas sueltas de la edición. Premiar la atestiguación
premiaría al motor contra el texto.

Queda anotada porque la siguiente sesión la va a pensar también, y así no la
mide dos veces.

### Lo que sí dice el despiece

Tres caminos probados —quitar el nipāta, bajar «iha», premiar la atestiguación—
y los tres se caen. **No es casualidad ni falta de ingenio: en estas junturas
varias lecturas recomponen, varias están atestiguadas, y ninguna señal interna
las separa.** Separarlas pide la frase.

**El despiece, entonces, es un argumento medido para el §9.8 del briefing 39**
—conectar el texto corrido del OSBCT—: no es una mejora deseable entre otras,
es la única que alcanza a estas 44.998 fichas.

<!-- DUDA, y hay que decirla: el briefing 38 §9.4 llama a esto «el fallo de la
     SEGUNDA voz», y para «nāhaṃ» acierta —«na» está bien y falla «haṃ»—. Pero
     en la masa de estas 416 lo que falla es el PUNTO DE CORTE, y con él las
     dos voces a la vez: «panetta+ha» no tiene bien la primera. Puede que sean
     dos hilos y no uno. No lo decido yo. -->

## 4 quater. LOS §§ 143-191, QUE NO SE HABÍAN LEÍDO

*Era el §5.2 del briefing 40. Leídos en la 41 sobre el propio impreso, págs.
629-640. La 40 pedía «143-195»; el capítulo acaba en el 191, así que son estos.
Los enunciados no se copian de bhaddacak —licencia CC BY-NC-ND— sino que se
leen de la edición de Smith, que es la fuente.*

**No es material menor. Es el tramo donde el Saddanīti hace tres cosas que
Kaccāyana no hace**, y las tres tocan de lleno lo que le falta al motor.

### a) Niggahīta y sandhi corriente (§§ 143-153), casi todo con Kaccāyana

    143 Mo itare                             m ← niggahīta (los otros dos géneros)
    144 Samāse do tiliṅge                    d ← niggahīta en compuesto
    145 Sesato mo do ca sare vyañjane vā     [Kc 34]
    146 Kvaci niggahītāgamo                  [Kc 37]   agama de niggahīta
    147 Lopaṃ                                [Kc 38+39] elisión del niggahīta
    148 Paro saro vā                         [Kc 40]   elisión de la vocal siguiente
    149 Lutte vyañjano visaññogo             [Kc 41]   deshace el conjunto tras elidir
    150 Niggahītaparo ikāro akāraṃ ukārañ ca makāre
    151 Akāro ekāraṃ hakāre                  ke 'haṃ · k'ahaṃ
    152 Sahakassa kassa patimhi niggahītattaṃ    Brahmā Sahampati
    153 Vyañjane niggahītaṃ aṃ               [Kc 30]

### b) Métrica y eufonía (§§ 154-167), y aquí Kaccāyana ya no acompaña

    154 Pariyādīnaṃ ra-yādivaṇṇassa ya-rādihi vipariyāyo
        METÁTESIS: pariyudāhāsi > payirudāhāsi; ariyassa > ayirassa;
        kariyā > kayirā; bahuābādho > bavhābādho; masakā > makasā
    155 Saṃsadde paralope pubbo dīghaṃ       saṃratto > sāratto, sārāgo, sārambho
    156 Vāsiṭṭhass' ikāro ettaṃ pāvacane     Vāseṭṭho
    157 Vaṇṇaniyamo chando, garu-lahuniyamo vutti
    158 Gāthāsu chanda-m-abhedatthaṃ akkharalopo
    159 Vuttānurakkhaṇatthaṃ viparītatā
    160 Sutte sukhuccāraṇatthaṃ akkharalopo viparītatā ca
    161 Appakkharānaṃ bahuttam aññathattañ ca   dve > duve; taṇhā > tasiṇā
    162 Bavhakkharānaṃ appattam aññathattañ ca  ācariyaṃ > āceraṃ
    163 Kvaci sare vyañjane vā odantānaṃ nāmānaṃ akārantattaṃ pakati
    164 Vuttirakkhaṇe māgame               agama 'm': magga-m-atthi, esa-m aggaṃ
    165 Mādese akāro dīghaṃ                paññavatām iva, arahatām iva
    166 Apicass' ilopo passa cattaṃ        api ca > acc  [Kcv]
    167 Aticcassa vā tilopo                aticca > acc
    168 Ṭhānantaragati niggahītassa

**La METÁTESIS del § 154 no tiene equivalente en Kaccāyana**, y es una
operación de otra clase que las del capítulo: no elide, no sustituye, no
inserta — **reordena**. Un motor que sólo componga y elida no la propone nunca.

### c) Las junturas de partícula, que es donde le duele al motor

    175 Akārañ c' ekār' āgame              haññe eva … kocinaṃ
    178 Yathā-tathāto aññato vā evass' ekāro ikāraṃ
        yathā eva > yathar-iva;  tathar-iva;  bhusām iva
    179 Saññoge vāthavāgame dīgho rassaṃ   pa-g eva itarā pajā; samma-d akkhātā
    182 Sakissa iss-ā(kāro) sadāgamena āgāmimhi     saki + d + āgāmi > sakadāgāmī
    183 Patissa pacco saranimittassa vā vyañjananimittassa vā     paccājāto
    191 Suddhassaramhā itissa issa lopo    elisión de la 'i' de «iti» tras vocal pura

**Los §§ 175, 178 y 179 son tres suttas dedicados a «eva»** — que es la familia
sin firmar de más masa de `docs/solucionador/familias-no-sabe.md` (49.484
fichas). **El § 191 es «iti»**, que es lo de la sesión 39. Y el **§ 160**, entre
sus ejemplos, imprime:

    Samantapāsādikā iti eva  ·  "Samantapāsādikā tv eva"

es decir, **«iti eva» dando «tv eva»**, que es la lectura adjudicada de «tveva»
(commit `cb9b56d`). **Testimonio, no adjudicación**: se anota para que el IEBH
decida qué hacer con él, y viene del Saddanīti, no de este documento.

### d) Y LO QUE MÁS IMPORTA: el Saddanīti tiene suttas que PROHÍBEN el sandhi

    185 Yattha sandhite sare na padaṃ sukhuccāraṇīyaṃ, na tattha sarānaṃ sandhi
        donde unir la vocal deja la palabra incómoda de pronunciar, no hay sandhi
    186 Yattha sandhito saro atthaṃ dūseti, na tattha sandhi
        donde la vocal unida ESTROPEA EL SENTIDO, no hay sandhi   («Āyasmā Ānando»)
    187 Dvīsu padesu na vyañjane sarānaṃ sandhi
    189 Na suddhassaralopo ādiss' ākāre sarantare vā

Y en el § 168, de su propia mano, la razón: algunas reglas se enuncian
*aniyamavasena* —sin obligar—, y de ahí *sotūnaṃ sammoho* y *rūpānañ ca
atippasaṅgo*, «confusión del oyente y **exceso de formas**».

**Eso es, dicho en el siglo XII, el problema del §4 ter de este documento.** El
motor propone varias lecturas que recomponen todas y no sabe separarlas; el
Saddanīti sostiene que la juntura se bloquea cuando el resultado no se
pronuncia bien o **cuando estropea el sentido** — y el sentido no está en las
reglas: está en la frase. **Es el argumento del §9.8 del briefing 39 dicho por
la propia autoridad**, y no una analogía forzada: son suttas, no glosa.

Se remata en la pág. 640, cerrando el capítulo, con algo que conviene tener
delante al leer los §§ 157-167: Aggavaṃsa dice que el Bhagavā **no** altera las
palabras por métrica ni por comodidad de pronunciación —*na hi Bhagavā chandañ
ca vuttiñ ca rakkhati*—, que eso es *lokopacāramattavasena*, cosa de autores
que temen la censura ajena. Es decir: **el propio Saddanīti acota hasta dónde
llegan sus reglas de eufonía cuando el texto es Buddhavacana.**

## 5. Lo que falta, en orden

Y el orden cambia por lo que dice el §4 bis.

1. **Las 416 junturas cuya primera lectura no es la del IEBH** (masa 48.439),
   empezando por la familia «āha», que sola pone 14.422. No es un sutta que
   falte y no lo arregla el orden —está medido en el §4 bis—: pide el texto
   corrido del OSBCT (briefing 39 §9.8) o la ficha de varias lecturas con su
   discriminante (§9.3). **Esto pasa delante de todo lo demás.**
2. ~~Comprobar a ojo los huecos del §4 y el tramo 73-125.~~ **HECHO en la 41**:
   las 39 páginas, una a una. Ya no queda estado «ocr» en la concordancia.
3. ~~Leer 143-195.~~ **HECHO en la 41**, y son 143-191: §4 quater.
4. ~~La discrepancia del § 34.~~ **RESUELTA en la 41: «Kc 14».** El aparato lo
   imprime así en la pág. 613. El OCR leía «Kc 18»; **gramsut tenía razón.**
   Y conviene apuntar cómo se equivocó el OCR, porque es instructivo: dos
   páginas más allá, en la 616, el aparato imprime «(Kc 18)» para el § 44.
5. **Nuevo, y sale del §4 quater:** llevarle al IEBH los §§ 185-186 —los suttas
   que PROHÍBEN el sandhi cuando el resultado no se pronuncia bien o estropea
   el sentido— y el § 154, la metátesis, que no tiene equivalente en Kaccāyana.
   No para meterlos en el motor: para que decida si el criterio de `CLAUDE.md`
   quiere citarlos, que es autoridad diciendo lo mismo que él dijo.
6. **Averiguar qué obra es «Kcv»** en las siglas de Smith. Queda como DUDA en
   el §2. Hasta entonces las cinco marcas Kcv no cuentan como Kaccāyana.
7. Sólo después, y con el visto bueno del IEBH, plantear si algo entra en el
   motor. Hoy la medida dice que no hace falta.

## 6. Procedencia

- El texto romanizado de los enunciados sale de **bhaddacak.github.io**
  (`assets/palitext/gram/allheads.gz`, 1.347 suttas del Suttamālā), licencia
  CC BY-NC-ND: se consulta, no se redistribuye. El editor advierte de erratas
  y pide cotejar contra Smith para cita seria — y la sesión 39 comprobó que la
  advertencia es cierta: en el sutta 49 trae un ejemplo donde Smith trae cuatro.
- La concordancia **sale del aparato de Helmer Smith**, ed. del Saddanīti,
  parte III, págs. 604-642, y a él se atribuye.
- La concordancia de gramsut (`xrefUtil.xrefList`) se usó **sólo como
  generador**, y su fallo en los suttas 9 y 10 queda registrado arriba.

## 7 bis. LO QUE LA 41 TUVO QUE CORREGIR DE LA 40 (principio 5)

*Va aparte y va primero porque es de esta sesión, y porque el defecto no está
en una cifra suelta: está en el titular.*

1. **El hallazgo que encabezaba este documento no era cierto como estaba
   dicho.** «Entre el § 73 y el § 125 no hay ni una marca de Kaccāyana» — y el
   aparato imprime «‖ § 73—85 Kcv 20 ‖» en la primera página del tramo. La 40
   había comprobado a ojo la pág. 623 y **no la 622**, que es donde estaba la
   marca. Comprobar una página del tramo y generalizar al tramo es exactamente
   lo que el propio documento decía que no había que hacer.

2. **El alcance, para que se sepa cuánto hay que desconfiar del barrido de la
   40**, sobre 39 páginas:

   | | |
   | --- | ---: |
   | marcas que el OCR **perdió** | **14** |
   | marcas que atribuyó a Kaccāyana siendo de la **Kcv** | **5** |
   | notas de paréntesis mal puestas o mal quitadas | 2 |
   | discrepancias resueltas (§ 34) | 1 |
   | límites del capítulo mal | 604-642 → **604-641** |
   | suttas que no eran del capítulo (§§ 192-195) | 4 |

   Nueve suttas pasan de «hueco» a tener correspondencia de Kaccāyana —52, 53,
   54, 56, 64, 145, 146, 147, 153— y uno a Kcv (el 55).

3. **La causa material está localizada, y era comprobable en la 40 sin leer
   nada:** el recorte empezaba en el 70,5% de la altura de la página y el
   aparato empieza más arriba en cuanto el cuerpo del texto acaba pronto. Una
   sola página completa mirada de arriba abajo —en vez de la franja recortada—
   lo habría enseñado. La 40 escribió «el OCR genera y el ojo adjudica» y luego
   **adjudicó con el recorte del OCR**, que es la misma frase incumplida.

4. **Lo que la 40 hizo bien y conviene no perder de vista:** los §§ 9 y 10 —«Kc
   605» y «Kc 604», donde gramsut calla— están confirmados a ojo, y el § 49
   sigue sin marca. Los dos testimonios de la sesión 39 se sostienen. Y el §4
   bis y el §4 ter, que son las 416 discrepancias del motor, **no dependían del
   aparato y no se mueven**.

## 7. LO QUE HAY QUE CORREGIR DE MÍ MISMO (principio 5)

1. **Propuse medir el grupo de los conjuntos «porque es el que más
   probablemente gane una regla».** Era una corazonada dicha con cara de
   pronóstico, y la medida del §4 bis la desmiente: de los 40 desacuerdos
   reales, cero son de conjunto. Lo que la corazonada tenía de malo no es
   haberse equivocado, sino haber puesto el orden de trabajo antes de la
   medida, que es justo al revés.

2. **Tres medidas seguidas mal, y siempre por lo mismo: el comparador.** Van
   por orden, porque la tercera es la que enseña.

   **La primera, con `==` a secas:** 2.032 «desacuerdos», masa 231.909. No lo
   eran. El IEBH escribe la voz de **superficie**, ya elidida —«vuttan + ti»—,
   y el motor la **subyacente** —«vuttaṃ + iti»—. Mismo análisis, dos
   notaciones; `extraer_junturas_separadas.py` lo dice en un comentario que yo
   no había leído.

   **La segunda, aflojando a «una es cola de la otra»:** 40 desacuerdos reales,
   masa 14.395, y así se escribió aquí. Tampoco: «imāha» pasaba por «āha»,
   «amatthaṃ» por «atthaṃ». Aflojé para no contar de más y conté de menos. El
   número bueno es **416**, masa 48.439.

   **La tercera es la peor, porque ya iba a publicarse como resultado.** Con
   ese mismo comparador flojo medí el experimento de bajar «iha» y salió
   «arregla 7 junturas, masa 13.441, rompe 0». Es falso: las nuevas primeras
   lecturas eran «tena+ha», «yatha+ha», «pana+ha», y «ha» no es «āha» — casaba
   por una cláusula inversa que yo mismo había escrito y que el sandhi no
   admite, porque **la segunda voz puede perder su vocal inicial, no ganarla**.
   Arregla **1**.

   Un experimento cuyo criterio de acierto está flojo no mide el cambio: mide
   el criterio. Y un «rompe 0» debería haberme dado desconfianza en vez de
   contento. El comparador está ahora en `herramientas/casan_las_voces.py`,
   escrito una sola vez, con la regla gramatical dicha y con las catorce
   pruebas que lo sujetan —incluidas «āha»/«iha» y «āha»/«ha», que son las que
   se me colaron—.
