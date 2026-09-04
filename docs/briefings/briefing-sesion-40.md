# Kaccāyana Pāḷi-Español: Briefing de la Sesión 40

*Complementa a los briefings 05–39. Tema de la sesión 40 (2026-08-30, la misma
noche que la 39): **el barrido del Saddanīti que la 39 dejó pedido**, y una
medida del motor que sale distinta de lo que yo había dicho tres veces. No
entra ninguna regla nueva. Lo que entra es una fuente, una concordancia, un
comparador y cifras.*

> **Lo primero que tiene que saber el chat nuevo:** verificar
> `git log origin/main..main`. Las reglas de siempre: el Python es la
> referencia; los CINCO arneses mandan, y **uno a uno**; nada se adjudica sin
> el visto bueno del IEBH; todo se mide antes y después; la atribución pública
> dice IEBH. Con IEBH se habla en inglés; lo del proyecto va en español.
> **Y el criterio que manda sobre todo, ya en `CLAUDE.md` con las palabras de
> IEBH:** hay formas de sandhi teóricamente plausibles que son inverosímiles
> en el Tipiṭaka. Recomponer no basta. Atestiguar la pieza no atestigua la
> juntura.

## 0. EL ESTADO, EN CIFRAS

| | al abrir la 40 | al cerrarla |
| --- | ---: | ---: |
| textos del corpus separado | 80 | 80 |
| junturas distintas | 2.045 | 2.045 |
| ecuaciones | 141 | 141 |
| casos adjudicados | 195 | 195 |
| señal «segura» / «posible» | 2.300 / 2.185 | 2.300 / 2.185 |

**Ninguna cifra se movió, y está bien que no se moviera:** esta sesión no metió
reglas ni adjudicaciones. Metió fuentes y medidas. Tres commits: `a918ed1`,
`1c7a7e9` y este briefing.

**Y una advertencia para el chat nuevo, porque me pasó dos veces en una noche:
el ciclo empuja solo.** Los dos de la 39 (`20d0301`, `e8e688d`) los empujó a
las 18:58 —queda contestada la pregunta que dejó abierta el briefing 39 §0—, y
`a918ed1` y `1c7a7e9` los empujó a las 19:26, mientras se escribía esto. De
modo que «sin empujar» dura lo que dura: **compruébese `git log
origin/main..main` en el momento, no se dé por bueno lo que diga un briefing.**

## 1. LOS VOLÚMENES DEL SADDANĪTI, EN EL REPOSITORIO

Los cinco de la edición de Helmer Smith están en `recursos/saddaniti/`, movidos
desde la carpeta de descargas y comprobados por md5 antes de borrar los
originales. **Los PDF no viajan** —`.gitignore` excluye `*.pdf`—; sí viajan los
`saddaniti-smith-NN.paginas.json`, que son los que permiten citar por página
impresa. Todo lo demás, en `recursos/saddaniti/LEEME.md`.

La paginación corre continua por los cinco volúmenes, de la pág. 2 a la 1460.
Comprobado contra el dato conocido: la pág. impresa 617 es la 24 del PDF del
vol. 03, como dijo la 39.

## 2. EL BARRIDO — gramsut genera, Smith decide

Era el punto 1 de §9 del briefing 39, y la respuesta corta es que **gramsut no
es la autoridad que parecía**, aunque sirve.

Su concordancia está en `xrefUtil.xrefList`: 803 grupos. **De los 1.347 suttas
del Suttamālā sólo 506 aparecen en alguno.** Y su ausencia no prueba nada: para
los suttas 9 y 10 no da correspondencia y Smith imprime «Kc 605» y «Kc 604».
Donde sí afirma, coincide con Smith en los quince casos cotejados — **y coincide
en el que importaba: el sutta 49 no está en ninguno de los 803 grupos.** Segundo
testimonio de lo que la 39 sostuvo con uno solo.

**La autoridad es el aparato de Smith**, que imprime «|| § 50 Kc 20 ||» al pie.
Lo que no lleva marca no tiene sutta correspondiente. El capítulo de sandhi
queda acotado: **Suttamālā I = Smith XX = págs. 604-642 = págs. 11-49 del PDF
del vol. 03**; el XXI empieza en la 643.

Se lee recortando la franja del aparato y pasándola por tesseract. El pāḷi sale
mal y la cadena «§ N Kc M» sale bien. **El OCR genera; el ojo adjudica.**

**EL HALLAZGO: entre el § 73 y el § 125 no hay ni una marca de Kaccāyana** —
cincuenta y tres suttas seguidos, y son una serie: sustitución de consonante
(73-101, «lo rassa», «jo yassa», «ko gassa») y formación de conjuntos
(104-119, 'tya'→'cca', 'dya'→'jja'). Todo en
`comun/concordancia-sadd-kac-sandhi.json`, con el estado de cada entrada, y en
`docs/solucionador/saddaniti-lo-que-kaccayana-no-tiene.md`.

## 3. Y LA MEDIDA DICE QUE HOY NO HACEN FALTA

De las 2.045 junturas, la lectura del IEBH es la primera del motor en **1.618**;
está pero no primera en **308**; falta en **108**. Son **416 discrepancias, masa
48.439**, y **ninguna** viene de las series del Saddanīti.

En **296 de las 416 —masa 44.998, el 93%—** la segunda voz del texto empieza por
vocal, y lo que el motor hace no es escoger mal la partícula: **corta en otro
sitio**.

    panettha  2.286   pana + ettha    el motor: panetta + ha
    athassa   1.790   atha + assa     el motor: ate + hassa
    panassa   1.731   pana + assa     el motor: pa + anassa
    tenāha    6.018   tena + āha      el motor: tena + iha

**Tres caminos probados, tres caídos:**

| | arregla | rompe |
| --- | ---: | ---: |
| quitar el criterio de nipāta del desempate | 78 | **940** |
| bajar «iha», que es quien gana a «āha» | 1 | 0 |
| premiar que la primera voz esté atestiguada | 7 (masa 170) | premiaría al motor CONTRA el texto en 244 |

El criterio de nipāta **es carga de muro** y no se toca: es lo que pone «taṃ+ca»
delante de «ta+añca». El tercero era hipótesis mía y **queda anotada por caída**,
para que nadie la vuelva a medir: «panetta» y «cetta» SÍ están en la edición, y
las voces del IEBH —«pan», «c», «ath»— no, porque son de superficie.

**En «tenāha» conviven cuatro lecturas que recomponen y están atestiguadas, y
ninguna señal de este repositorio las separa.** De ahí que el §9.8 de la 39
—conectar el texto corrido del OSBCT— deje de ser una mejora entre otras: **es
la única que alcanza a esas 44.998 fichas**, y ahora ese pendiente lleva cifra.

## 4. LO QUE HAY QUE CORREGIR DE MÍ MISMO (principio 5)

1. **Tres medidas seguidas mal, todas por el comparador.** Con `==` a secas:
   2.032 «desacuerdos» donde hay 416 — el IEBH escribe la voz de superficie y
   el motor la subyacente. Aflojando a «una es cola de la otra»: 40, porque
   «imāha» pasaba por «āha». Y con ese mismo comparador flojo, el experimento
   de bajar «iha» dio **«arregla 7, rompe 0»** cuando arregla 1, porque «ha»
   casaba con «āha». **Iba a entregarlo como resultado.**
   Un experimento cuyo criterio de acierto está flojo no mide el cambio: mide
   el criterio. Y un «rompe 0» tenía que haberme dado desconfianza, no alegría.
   De ahí `herramientas/casan_las_voces.py`: escrito una vez, con la razón
   gramatical dicha —la segunda voz puede PERDER su vocal inicial, no ganarla—
   y con catorce pruebas, incluidas las dos que se colaron.
2. **Puse el orden de trabajo antes de la medida.** Propuse medir el grupo de
   los conjuntos «porque es el que más probablemente gane una regla». Era una
   corazonada con cara de pronóstico; de los 416, cero son de conjunto.
3. **Busqué el briefing en el repositorio equivocado.** Empecé por `OSBCT`,
   que es el otro proyecto del IEBH. El briefing vive aquí. Cuesta poco decirlo
   y evita el mismo minuto perdido mañana.

## 5. LO QUE SIGUE (en orden)

**Lo de la sesión, sin cerrar:**

1. **Comprobar a ojo** los huecos del capítulo XX y el tramo 73-125, página por
   página. Son 39 páginas; **van 3** (605, 617, 623). Vale la pena aunque el
   motor no los necesite hoy: el inventario es lo que evita volver a
   encontrarlos de uno en uno, que era el encargo.
2. **Leer los §§ 143-195**, que no se han leído.
3. **La discrepancia del § 34**: el OCR lee «Kc 18» y gramsut da k14.

**Lo que ya venía, y sigue mandando:**

4. **Conectar el texto corrido del OSBCT** (39 §9.8). **Sube al primer lugar de
   los pendientes de fondo**: es lo único que alcanza a las 44.998 fichas del §3.
5. **Que la ficha de caso admita varias lecturas con su discriminante**
   (39 §9.3). Sin eso «tveva» y sus hermanas no se registran bien.
6. **El fallo de la segunda voz** (38 §9.4, 39 §9.2). **Con una DUDA nueva:** en
   la masa de las 416 lo que falla es el PUNTO DE CORTE, y con él las dos voces
   —«panetta+ha» no tiene bien la primera—. Puede que sean dos hilos y no uno.
   No me toca decidirlo.
7. **Enseñar al IEBH lo pendiente del briefing 38**: el diagnóstico de su §1 con
   sus tres testigos, y la decisión del resguardo de su §3 (313 correctas contra
   2 malas).
8. **Las escaleras sin derivar**: la auditoría da 16 casos.
9. **La lista corta de las 69** (37 §3 quater) por el modo revisión.
10. **El `git add -A`** de la línea 172 del ciclo (38 §7 y §9.8; 39 §4). El
    patrón correcto está escrito al lado, en `archivar_cola()`.
11. **La firma de familias** de `docs/solucionador/familias-no-sabe.md`, que
    sigue esperando: «eva» (masa 49.484), «iva» (45.729), «ati» (20.745)…
12. Resto del mapa 33. **Sin empezar.**

## 6. AVISOS AL CHAT NUEVO

Los del briefing 39 §7 siguen todos en pie —los 165 s de bash, los procesos que
no sobreviven, la caché de la señal que no mira `operaciones.py`, los arneses
uno a uno—. Tres añadidos de hoy:

- **El `.git/index.lock` estaba pegado otra vez.** Borrarlo pide permiso de
  borrado sobre la carpeta; se pidió y se borró.
- **El gancho de pre-commit avisa de «referencias §N dejadas sin enlazar».**
  En estos commits **es correcto que avise**: las referencias son al Saddanīti,
  y enlazarlas mandaría al lector al §N de Kaccāyana, que es justo lo que
  arregló `b33d0d5`. Aviso, no fallo.
- **Para medir el motor contra el banco, usar `casan_las_voces.py`.** No
  improvisar la comparación. Es la lección del §4.

## 7. PROCEDENCIA

- La concordancia del capítulo de sandhi **se atribuye al aparato de Helmer
  Smith**, Saddanīti parte III, págs. 604-642.
- El texto romanizado de los enunciados sale de **bhaddacak.github.io**,
  licencia CC BY-NC-ND: se consulta, no se redistribuye. Su concordancia
  (`xrefUtil.xrefList`) se usó **sólo como generador**, y su fallo en los suttas
  9 y 10 queda registrado.
- **Nada se adjudicó en esta sesión.** El inventario del §2 es de candidatos.
