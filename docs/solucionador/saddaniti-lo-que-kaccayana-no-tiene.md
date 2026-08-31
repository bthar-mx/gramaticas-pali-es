# El capítulo de sandhi del Saddanīti: qué trae que Kaccāyana no tiene

*Sesión 40, 2026-08-30. Responde al punto 1 de §9 del briefing 39: ir a buscar
las otras reglas que Kaccāyana no tiene, en vez de encontrarlas una a una como
fallos. El sutta 49 se halló persiguiendo un fallo; esto es el barrido.*

> **Nada de lo que sigue está adjudicado.** Es un inventario de candidatos con
> su procedencia y su estado de comprobación. Decir qué regla explica qué voz
> es del IEBH, no de este documento.

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

### El capítulo, acotado

| | |
| --- | --- |
| obra | Saddanīti Suttamālā, capítulo 1 (= **XX** en la numeración corrida de Smith) |
| páginas impresas | **604 – 642** |
| páginas del PDF, vol. 03 | **11 – 49** |
| el capítulo XXI empieza en | pág. impresa 643 = pág. 50 del PDF |

La correspondencia entre página impresa y página del escaneo sale del
`_page_numbers.json`, y **se comprobó contra el dato conocido**: la sesión 39
dio la pág. impresa 617 como la 24 del PDF, y el mapa da lo mismo. Los cinco
volúmenes corren continuos, de la pág. impresa 2 a la 1460.

### Cómo se leyó

Las páginas son imagen pura. Se recorta la franja del aparato y se pasa por
tesseract:

    pdftoppm -r 300 -f 11 -l 49 -x 0 -y 1850 -W 1700 -H 820 -png <vol03> a
    tesseract a-024.png - --psm 6

El OCR confunde letras pāḷi, pero **la cadena «§ N Kc M» es dígitos y latín**,
y sale. Aun así: **el OCR genera y el ojo adjudica.** Comprobadas a ojo sobre
la imagen: pág. 605 (§§ 3-6), pág. 617 (§§ 50-51, y el hueco del 49), pág. 623
(sin ninguna marca). La tabla entera, con el estado de cada entrada, en
`comun/concordancia-sadd-kac-sandhi.json`.

## 3. EL HALLAZGO: cincuenta y tres suttas seguidos sin Kaccāyana

Entre el **§ 73 y el § 125** —páginas impresas 621 a 626— el aparato de Smith
no imprime **ni una sola** marca de Kaccāyana. La pág. 623 se comprobó a ojo y
en efecto su aparato es todo citas canónicas y variantes, sin concordancia.

Y no es un tramo cualquiera. Leídos los enunciados, es **una serie**:

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

## 4. Los otros huecos del capítulo

Dentro del tramo de sandhi propiamente dicho, sin marca de Kaccāyana en el
aparato, y **pendientes de comprobar a ojo**:

| suttas | de qué van |
| --- | --- |
| 37-39 | conjunto previo y elisión ante 'iva' |
| 40-42 | «hoti kesañci matena»; 'ayya/añña/aggha/ussa'; 'temepabbatyādīnaṃ' |
| 45, 47, 48 | 'u' de hetu/dhātu; «itissa tisaddabyañjanopi»; elisión de la 'i' |
| **49** | **«evassekāre itissaññassa cissa vo»** — comprobado a ojo, sesión 39 |
| 52-56 | 'eva'→'ri'; 'putha' + agama 'g'; 'pā'; «ossu»; «yavamadanataralahā vā» |
| 64, 69-71 | alargamiento ante consonante; elisión ante 'y m n r'; «animittopi vā» |
| 127-128, 131, 134-136 | 'viya'→'byā'; 'vācā'→'byo'; niggahīta en gāthā; conjunto y no conjunto |
| 143-147, 150-195 | sin leer todavía |

El **47** merece nombrarse aparte: «itissa tisaddabyañjanopi» es otra vez el
comportamiento de «iti», que es lo que ocupó la sesión 39.

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

## 5. Lo que falta, en orden

Y el orden cambia por lo que dice el §4 bis.

1. **Las 416 junturas cuya primera lectura no es la del IEBH** (masa 48.439),
   empezando por la familia «āha», que sola pone 14.422. No es un sutta que
   falte y no lo arregla el orden —está medido en el §4 bis—: pide el texto
   corrido del OSBCT (briefing 39 §9.8) o la ficha de varias lecturas con su
   discriminante (§9.3). **Esto pasa delante de todo lo demás.**
2. **Comprobar a ojo** los huecos del §4 y el tramo 73-125 página por página.
   Son 39 páginas; van 3 comprobadas. Sigue valiendo la pena aunque el motor
   no los necesite hoy: el inventario es lo que evita volver a encontrarlos de
   uno en uno.
3. **Leer 143-195**, que no se ha hecho.
4. **Resolver la discrepancia del § 34**: el OCR lee «Kc 18» y gramsut da k14.
5. Sólo después, y con el visto bueno del IEBH, plantear si algo entra en el
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
