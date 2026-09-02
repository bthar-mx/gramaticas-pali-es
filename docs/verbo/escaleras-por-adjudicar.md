# Escaleras del documento «Verbo»: cotejo contra las presentaciones

Cotejo del documento «Verbo» (Bhikkhu Nandisena, IEBH, rev. 7-abr-2013,
publicación `20130407-BN-T0021`) contra las trece presentaciones
`GP-T - Verbo-I` … `GP-T - Verbo-XII` exportadas a PDF.

**Nada de lo que sigue está corregido.** Son propuestas y dudas; la firma es
de Angel.

## 0. Resumen

| | |
| --- | ---: |
| Escaleras en el documento | 14 |
| Escaleras en las presentaciones | 17 |
| Escaleras cotejables (las dos fuentes) | 10 |
| Discrepancias de numeración | 1 (adjudicada) |
| Diferencias de convención (no son error) | 14 (adjudicadas) |
| Escaleras que sólo están en las presentaciones | 7 (+2 repetidas) |
| Escaleras que sólo están en el documento | 6 |

Se rehace entero con

    python3 herramientas/extraer_verbo.py
    python3 herramientas/extraer_verbo_diapositivas.py   # necesita los PDF
    python3 herramientas/auditar_verbo.py

## 1. La numeración del documento no es toda de Rūpasiddhi

La nota al pie 1 del documento dice:

> La última columna indica el número de la regla gramatical por medio de la
> cual se realiza esa operación de acuerdo al Padarūpasiddhi (Rū).

**No se cumple en la última fila de las catorce escaleras.** Todas terminan
citando «11», y las presentaciones dan ahí `11/14` —es decir Kacc. §11, Rū 14—.
Leído como Rūpasiddhi, «11» sería Rū 11 = Kacc. §9 *Parasamaññā payoge*, que
trata de los términos técnicos y no tiene nada que ver con formar el verbo. La
regla que sí corresponde es Kacc. §11 *Naye paraṃ yutte*.

De modo que **el «11» final es un número de Kaccāyana en una columna que la
nota declara de Rūpasiddhi**, y ocurre catorce veces. En «bhū» las dos
numeraciones conviven en la misma celda: «67, 11» = Rū 67 (Kacc. §83) más
Kacc. §11 (Rū 14).

Las presentaciones citan siempre el par `Kacc/Rū`, y son coherentes: de los 30
pares distintos que aparecen en las trece —107 citas— **ninguno discrepa** de
la concordancia deducida de `kaccayana/*.md` y `docs/*.md`.

**Decidido por Angel (2026-09-01):** se publica el par `Kacc/Rū`, como hacen
las presentaciones. La numeración normativa del repositorio es la de
Kaccāyana; la de Rūpasiddhi va al lado porque es la que trae el documento.

## 2. Discrepancia de numeración: «suṇāti»

La única discrepancia real entre las dos fuentes.

| | signo | regla citada | qué es esa regla |
| --- | --- | --- | --- |
| Documento, tabla `9-su` (2ª) | ṇā | Rū **513** | Kacc. §449 *Kiyādito nā* |
| Presentación `Verbo-X` | ṇā | 448/**512** | Kacc. §448 *Svādito ṇu-ṇā-uṇā ca* |

`su` pertenece al **svādi-gaṇa**, no al kiyādi-gaṇa; la regla que le da «ṇā» es
Kacc. §448 / Rū 512. Rū 513 es la del grupo de «kī», y es la que el documento
cita —correctamente— en la escalera de `10-vi-kī`.

La primera tabla de `9-su` (ṇu → suṇoti) cita Rū 512, que sí es correcta. El
error afecta sólo a la segunda.

**Adjudicado por Angel (2026-09-01): Kacc. §448 / Rū 512.** Verificado contra
el texto del sutta, no sólo contra la diapositiva. La corrección se señala en
la página: el documento base cita Rū 513, y ahí se dice.

### Sobre el número de Kaccāyana que corresponde a Rū 512

En la sesión se propuso «Kacc. 488». **No cuadra con las fuentes**, y conviene
dejar por escrito por qué, porque los tres números se parecen:

| Sutta | Kacc. | Rū | Qué dice |
| --- | ---: | ---: | --- |
| *Svādito ṇu-ṇā-uṇā ca* | **448** | **512** | el svādi-gaṇa toma ṇu, ṇā, uṇā |
| *Kvaci dhātu-vibhatti-paccayānaṃ dīgha-viparīt'-ādesa-lop'-āgamā ca* | 517 | 488 | alargamiento, sustitución, elisión y aumento |
| *Havipariyayo lo vā* | 488 | 481 | «ha» y «la» |

Comprobado en las dos fuentes por separado: `docs/6 - Ākhyāta-Kaccāyana.md`
línea 691 da «448. 512. Svādito ṇu-ṇā-uṇā ca», y
`docs/6. Ākhyāta-Rūpasiddhi.md` línea 1063 da «512. Svādito ṇu-ṇā-uṇā ca».

De modo que **Rū 488 corresponde a Kacc. §517**, no a Rū 512; y **Kacc. §488
es *Havipariyayo lo vā*** (Rū 481), que no tiene que ver con los signos de
conjugación. El 488 aparece, eso sí, en la escalera vecina de «kī», donde la
diapositiva cita `517/488` para acortar la vocal de la raíz — de ahí es fácil
que se cruce con ésta.

Queda, como cortesía y no como condición, dar cuenta de la corrección a
Bhikkhu Nandisena, por ser suyo el documento.

## 3. Diferencia de convención en los pasos de elisión

No es un error: las dos fuentes muestran lo mismo de dos maneras.

En los pasos que **no** son de elisión, el documento muestra la forma
*resultante* de la regla citada. En los pasos de elisión muestra la forma
*anterior*, y el resultado aparece en la fila siguiente. Las presentaciones
muestran siempre la forma resultante.

    paca, fila 2      documento:  paca   … 425      presentación:  pac   … 521/425
    bhū,  penúltima   documento:  bhava  … 67       presentación:  bhav  … 83/67

Ocurre en las catorce escaleras. Además, el documento **funde en una sola fila
el último paso de elisión y el de formación** del verbo (de ahí las celdas con
dos números: «67, 11», «433, 11», «49, 11»…), mientras que las presentaciones
los separan. Por eso «bhū» tiene 6 filas en el documento y 7 en la diapositiva.

**Decidido por Angel (2026-09-01): una operación por fila**, como en las
diapositivas. Cada fila muestra la forma **resultante** de la regla que se cita
a su lado, de modo que la escalera se puede comprobar línea a línea. Es la
misma convención que ya usan las escaleras de sandhi del repositorio.

Consecuencias, y son dos:

1. En el paso de elisión de la vocal final (Rū 425) la página imprime la forma
   ya elidida —`pac`, no `paca`—, que es lo que hace la diapositiva.
2. En «bhū» la página imprime **`bhav`**, forma intermedia que el documento
   base no imprime nunca. No es una adición ajena: la fila sale de la
   diapositiva de `GP-T - Verbo-I`, del mismo autor, y se rotula como tal.

El porqué del punto 2: tras la fila 5 se tiene `bhava + a + ti`, que concatenado
daría **bhavaati**. Es Kacc. §83 (*Saralopo…*) quien elide la vocal final de
«bhava» y deja `bhav`; sólo entonces Kacc. §11 une `bhav + a + ti` en
*bhavati*. Fundidas las dos reglas en una celda, como hace el documento, se
pierde de vista adónde fue esa «a».

Sobre las trece escaleras restantes la fusión de la última fila no oculta
ninguna forma: la operación fundida ya se ve. «bhū» es el único caso.

## 4. Coinciden sin reservas

Cotejadas paso a paso y regla a regla: `paca`, `bhū`, `rudha`, `divu`,
`10-vi-kī`, `tanu`, `cura` (ṇe) y `cura` (ṇaya). Salvo la convención de §3, no
hay ninguna diferencia.

## 5. Lo que sólo tiene una de las dos fuentes

**Sólo en las presentaciones** (7 escaleras): `gaha` (presente); `anu-bhū` y
`paca` en voz pasiva; `bhū` causativo activo y pasivo; `paca` causativo.

La de `gaha` importa más de lo que parece: en el documento **falta la escalera
de gahādi** y además **la celda de explicación del gahādi-gaṇa está vacía** en
la tabla de los ocho grupos —su contenido se quedó dentro de la fila del
kiyādi, que dice «‘nā, ppa, ṇhā’ se insertan…»—. La presentación `Verbo-XI` da
la escalera completa: `gaha → gah (521/425) → gaha+ti (414/428) → gaha ṇhā ti
(450/517) → ga ṇhā ti (490/518) → gaṇhāti (11/14)`.

Las escaleras de `bhū` y `paca` aparecen dos veces en las diapositivas —en
`Verbo-I` y otra vez en `Verbo-II`—, idénticas. No cuentan como nuevas.

**Sólo en el documento** (6 escaleras): `gamu`, `tuda`, `hū`, `hu`, la de `su`
con ‘ṇu’ (*suṇoti*) y la de `vi-kī` (*vikkiṇāti*). Sin cotejo posible.

De ellas, **`gamu` y `tuda` se separan en dos filas sin inventar nada**: la
operación que el documento funde con la formación del verbo ya deja su forma a
la vista. **`hū` y `hu` no.** En las dos, el documento pasa de `hū + a + ti`
(Rū 487) a `ho + ti` (Rū 434, 11) en una sola fila, de modo que la elisión del
signo de conjugación y el fortalecimiento de la vocal ocurren juntos y sin
forma intermedia impresa. Separarlos obliga a proponer una forma —`hū + ti`—
que ninguna de las dos fuentes imprime.

**Decidido por Angel (2026-09-01): se separan**, imprimiendo «hū + ti», y la
fila añadida se rotula como en «bhū». No es inventar un paso: Rū 487 = Kacc.
§510 *Lopañ c' ettam akāro* elide el signo de conjugación, de modo que de «hū +
a + ti» no puede salir otra cosa que «hū + ti»; después Rū 434 = Kacc. §485
*Aññesu ca* fortalece ū → o. La forma intermedia es aritmética de la regla
citada, no una regla nueva.

**Decidido por Angel (2026-09-01):** se publica tal cual, con nota de que
ninguna segunda fuente la corrobora. Rū 434 = Kacc. §485 *Aññesu ca* es la
regla general de vuddhi y ṇu → ṇo es un fortalecimiento, de modo que la cita
es coherente; sencillamente no hay segundo testigo.

**Decidido por Angel (2026-09-01):** sí se incorpora, **siempre que no esté ya
en el documento «Verbo»**. Es del mismo autor. Cada escalera traída de las
diapositivas se rotula con la presentación de la que sale.

## 6. Pasos no verificables desde las diapositivas

- `9-su` primera tabla: ṇu → ṇo citando Rū 434 (Kacc. §485 *Aññesu ca*).
  Ninguna diapositiva trae la escalera de «suṇoti».
- `10-vi-kī` fila 5: duplicación `ki → kki` citando Rū 27 (Kacc. §20). La
  diapositiva trae «kī» sin prefijo, de modo que ese paso no aparece.

## 7. Otros defectos del documento

El propio colofón advierte que el material «no ha sido editado todavía».

1. Celda de explicación del **gahādi-gaṇa vacía** (§5).
2. Tres entradas siguen **en inglés** en listas por lo demás españolas:
   «Imperative (āṇatti)», «Supposition (parikappa)», «Conditional
   (kālātipatti)» en la lista de los seis tiempos, y «Imperative (pañcamī)» y
   «Conditional (kālātipatti)» en la de las ocho vibhatti.
3. **Tiempos ausentes** en la sección *otros paradigmas*: `3-kara` sin
   perfecto; `5-asa` termina en el imperfecto; `7-vaca` sin presente,
   imperativo ni potencial; `9-disa`, `12-ṭhā`, `13-su`, `14-gaha`, `15-e`,
   `16-hana`, `17-hara`, `18-labha`, `19-upa-pada` y `20-vi-hara`
   incompletos. **Aplazado por Angel (2026-09-01):** no se toca por ahora; los
   paradigmas se publican con los tiempos que traen.
4. El colofón remite a «el siguiente archivo» para la lista de referencias, y
   ese archivo no acompaña al documento. La diapositiva 2 de `Verbo-I` da
   probablemente esa lista: *Kaccāyana* cap. vi, *Rūpasiddhi* cap. vi,
   *Saddanīti-Suttamālā* xv, 811-844.

## 7 bis. Lo que añadió la auditoría automática

`herramientas/auditar_verbo.py` rehace este cotejo desde los datos, de modo
que no hay que creerse el informe. Sobre las **195 citas Kacc/Rū** de las dos
fuentes, **ninguna discrepa** de la concordancia del repositorio. Cuatro cosas
más que salieron al automatizarlo:

1. **La diapositiva de «gaha» retrocede.** El paso 2 elide la vocal final y
   deja «gah»; el paso 3 vuelve a imprimir «gaha». Una de las dos filas está
   mal, y no hay en el documento escalera de gahādi con que cotejarla.
   **Decidido por Angel (2026-09-01):** se publica la escalera con la duda a
   la vista. Kacc. §490 *halopo ṇhāmhi* elide «ha» ante ‘ṇhā’, de modo que en
   el paso 5 la raíz tiene que ser todavía «gaha»: la fila sospechosa es la
   2. Se publica porque es la ÚNICA escalera de gahādi que existe, y porque la
   celda de explicación de ese gaṇa también está vacía (§5): la página gana
   más enseñándola con la pregunta marcada que callándola.
2. **La raíz se llama distinto en cada fuente**: «rudha» en el documento,
   «rudhi» en la diapositiva. La tabla de los ocho grupos del propio documento
   dice «rudhādi-gaṇa» y «grupo que comienza con la raíz "rudhi"», de modo que
   las dos formas están en él.
   **Decidido por Angel (2026-09-01): «rudhi».** Lo zanja el propio
   repositorio: `recursos/raices/raices.json` trae las dos como raíces
   DISTINTAS — «rudhi», gaṇa II, «cerrar; cubrir; prevenir, obstruir», que es
   el rudhādi-gaṇa y justo la glosa del documento; y «rudha», gaṇa III,
   «deseo», que es otra raíz. El documento junta la grafía de una con el
   significado de la otra. Concuerda además con Kacc. §446 *Rudhādito
   niggahitapubbañ ca*.
3. **«vi-kī» y «kī» no son cotejables.** El documento deriva *vikkiṇāti*, con
   prefijo, y la diapositiva *kiṇāti*, sin él. Son palabras distintas, no dos
   versiones de la misma escalera, y la auditoría las empareja por la forma
   final justamente para no confundirlas. La escalera de «kī» entra, pues,
   entre las que sólo están en las diapositivas.
4. **La última fila de «su» escribe «ṇa» donde las anteriores escriben «ṇā».**
   En la diapositiva; el documento pone «ṇā» en las cuatro.
   Queda como errata probable de la diapositiva; se publica «ṇā», que es lo
   que ponen el documento y las tres filas anteriores de la propia
   diapositiva.

## 8. Atribución

Bloque de licencia, idéntico al de las demás páginas de `recursos/`:

> Preparado por Bhikkhu Nandisena
> Este material puede ser reproducido para uso personal y distribuido de forma
> gratuita.
> Copyright © 2026 Instituto de Estudios Buddhistas Hispano (IEBH). Publicado
> bajo licencia CC BY-NC-ND 4.0.

**Decidido por Angel (2026-09-01):** todo paradigma tomado de otra obra lleva
su crédito. La sección *otros paradigmas* —**73 de las 130 tablas**— procede,
según la nota al pie 2 y el colofón, de *The Higher Pali Course for Advanced
Students*, del Venerable Buddhadatta Thera, publicado por The Colombo
Apothecaries' Co., Ltd., Colombo, Sri Lanka, 1951, y así se cita. La misma
regla se aplica a cualquier otro paradigma de procedencia ajena que aparezca al
seguir trabajando.

**Decidido por Angel (2026-09-01):** se hace constar que el material se creó
en 2013 y se editó y mejoró en 2026 al preparar la página. Redacción propuesta
para el pie, a continuación del bloque de licencia:

> Este material fue preparado originalmente en 2013; ha sido editado y
> mejorado en 2026 con motivo de su publicación en esta página.
