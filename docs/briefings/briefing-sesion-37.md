# Kaccāyana Pāḷi-Español: Briefing de la Sesión 37

*Complementa a los briefings 05–36. Tema de la sesión 37 (2026-08-30, en
vivo con Angel): **el testigo del DPD deja de estar vacío y se pone a
trabajar. Los dos informes re-corridos; un informe nuevo del sub-piso de
§34 que encuentra que lo falso tiene firma y no es la frecuencia; y el
criterio de categoría del IEBH mecanizado por fin, con su límite medido.
Nada adjudicado: los tres informes preparan, y firmar es del IEBH.***

> **Lo primero que tiene que saber el chat nuevo:** verificar
> `git log origin/main..main` (al cierre quedaban CUATRO commits sin empujar:
> los dos informes con el testigo, el informe del sub-piso, el del criterio,
> y la cabecera en inglés con este briefing). Las reglas de siempre: el Python es la referencia; los CINCO
> arneses mandan; nada se adjudica sin el visto bueno del IEBH; todo se
> mide antes y después; la atribución pública dice IEBH. Con Angel se habla
> en inglés; lo del proyecto va en español.

## 0. LA CLAVE — Angel dijo que la rotaba en esta sesión

**Pendiente desde el briefing 35 §0 y arrastrada por el 36.** Angel eligió
en esta sesión «rotarla ahora»; **al cerrar no consta la confirmación**, así
que se pregunta otra vez al abrir. Es
`npx wrangler secret put CLAVE_VEREDICTOS` en la máquina con la sesión de
wrangler, con un valor nuevo que no se escriba en ninguna parte; el que
corre el ciclo pasa a usar el valor nuevo en `VEREDICTOS_CLAVE=…`. Para
comprobar que prendió: correr el ciclo con el valor nuevo, o pedir
`/api/veredictos?clave=<el viejo>` y ver un 403.

Contexto que ayuda a decidir, y que en dos briefings no se había dicho: si
la clave se filtra, **lo peor posible es que alguien lea o vacíe la cola**.
No puede publicar ni adjudicar: eso sigue pidiendo la Mac, los arneses y la
firma. Enviar a la cola es abierto a propósito.

## 1. LA TRAMPA DE LA POBLACIÓN — lo primero que hay que interiorizar

**Las «16.366 formas» significan dos cosas distintas en este proyecto, y
confundirlas invalida una medición entera.** Pasó en esta sesión.

| «16.366» | qué es | hasta dónde baja |
| --- | --- | --- |
| referencia de señal | las formas ÚNICAS de los dos corpus de Sandhi (`nuestro/js/referencia-senal-solo-canon.json`) | frecuencia **0** |
| `--n 16366` | las 16.366 formas MÁS FRECUENTES del canon | frecuencia **45** |

No es un matiz. **jātimaraṇā (frec 3) ocupa el puesto 167.330 y vedhamānehi
(7) el 86.261**, de modo que un `--n 16366` de los informes **no contiene
ninguna de las dos** — siendo exactamente las dos que motivaron el piso de
§34. El briefing 36 §3 dice «el corpus de referencia entero (16.366)»
queriendo decir la primera; un `--n 16366` da la segunda. La primera medición
de esta sesión se hizo sobre la población equivocada y hubo que rehacerla.

**Regla para el chat nuevo:** cuando algo se mida «sobre la referencia», la
población es el JSON de la referencia, no un corte por frecuencia. El informe
nuevo del §3 lo hace bien y lo dice en su cabecera.

## 2. LOS DOS INFORMES, CON EL TESTIGO LLENO (§6.3 del 36 — hecho)

Con `recursos/lexico/dpd-descomposiciones.tsv` en la carpeta, `hay_testigo()`
da True y la columna deja de estar vacía. Re-corridos sin tocar su código.

### informe-procliticas: el espejo no se sostiene, y el testigo dice por qué

De las **86** formas que el mecanismo espejo afirmaría: **coincide 14 ·
difiere 9 · calla 63**. Acuerdo en una de cada seis. Y las nueve
discrepancias **no son ruido, sino cuatro clases**:

| forma | la receta diría | el DPD | qué es de verdad |
| --- | --- | --- | --- |
| nakusalaṃ, nakusalo | na + akusalaṃ/-o | na + kusalaṃ/-o | segunda voz equivocada |
| nuppajjittha | na + uppajjittha | nu + pajjittha | partícula equivocada |
| sāpi, sāyaṃ, yāyaṃ | so/yo + … | **sā/yā** + … | **el femenino, no el masculino** |
| sacakkhukānaṃ | so + acakkhukānaṃ | **sa-** + cakkhukānaṃ | prefijo, no pronombre |
| yeva | yo + eva | y + eva | — |
| anupādinnupādāniyo | na + … | anupādinna + upādāniyo | compuesto, no proclítico |

Cuatro de las nueve son de **categoría gramatical**, que es precisamente lo
que el §4 mecaniza. El informe existía para decir qué condición extra pide la
primera voz; el testigo la nombró.

La medición previa sigue en pie: **afirmaría 16 de las 18 conocidas, con 16
aciertos de 16**. Callan anabhineyya y nātivattati.

Las cuentas bajan de 335 a 324 formas **por §34, no por el testigo**: el
patrón embarcado en la 36 ya reclama con autoridad las que antes entraban.

### informe-niggahita-m: se ha vaciado, y por construcción

De 153 formas a **99, y CERO afirmables** (testigo 0 · 0 · 0). No es un
fallo. **La ventana del informe son las 5.000 formas más frecuentes, y el
puesto 5.000 tiene frecuencia 159 — el mismo número que `frec_minima`.**
Ventana y régimen medido son la misma frontera: todo lo que el informe
alcanza a ver ya lo afirma el patrón. Para que vuelva a informar hay que
correrlo **por debajo** del piso, que es lo que hace el informe nuevo.

## 3. INFORME NUEVO DEL SUB-PISO: LO FALSO TIENE FIRMA, Y NO ES LA FRECUENCIA

`herramientas/generar_informe_subpiso_34.py` →
`docs/solucionador/informe-subpiso-34.md`. Sobre **la referencia de señal**
(§1), con la receta embarcada y el piso quitado.

- **449 afirmaciones sin piso**: 30 dentro del régimen, **419 calladas**.
- El testigo sobre esas 419: **coincide 199 · difiere 62 · calla 158**. El
  piso suprime del orden de **tres lecturas correctas por cada falsa**, y las
  falsas confirmadas son **62**, no las dos que se conocían.
- **TRES FIRMAS separan lo falso mucho mejor que la frecuencia:**

| condición | falsas que corta | correctas que pierde |
| --- | ---: | ---: |
| la base es «saṃ» o «maṃ» | 23 | **0** |
| forma en «-ti» con segunda voz en «-ti» | 26 | 2 |
| segunda voz acabada en partícula ajena | 29 | 4 |
| **las tres juntas** | **62 → 18** | **199 → 195** |

  Precisión sobre lo adjudicable: **76,2 % → 91,5 %**. «saṃ-» es preverbo y
  samāgama es compuesto; «maṃ» es el acusativo donde la lectura verdadera
  lleva «mama»; y el grupo de «-ti» es §34 quitándole formas al patrón de
  «iti», que ya está firmado (satimantoti es satimanto + iti).

**DOS LÍMITES, declarados en el propio informe y que no hay que perder:**

1. **El DPD CALLA sobre jātimaraṇā y sobre vedhamānehi.** El testigo no
   adjudica los dos casos que fijaron el piso; los adjudicó el juicio de
   Angel y sigue haciendo falta. De las dos correctas que el piso silencia,
   confirma tvamasi y calla sobre ekamante.
2. **La cuenta no cuadra con el briefing 36 §3**: 385 allí, 441 aquí sin las
   conocidas. **SIN RECONCILIAR.** Causa probable: la precedencia entre
   patrones —dentro de `senal()` otro patrón reclama la forma antes y a §34
   no se le pregunta—, que la receta suelta del informe no modela. **Es una
   tarea concreta para el chat nuevo.**

De paso, medido y no supuesto: el artefacto «m»/«ṃ» del cotejo con el DPD
(«sabbam + idaṃ» frente a «sabbaṃ + idaṃ») es de **un caso en 419**.

## 4. EL CRITERIO DEL IEBH, MECANIZADO POR FIN — con su límite

`herramientas/generar_informe_criterio_pos.py` →
`docs/solucionador/informe-criterio-pos.md`. Lo que faltaba en la 35 era la
categoría gramatical; `dpd-pos.tsv` la trae —457.628 formas—, y entre las
categorías del DPD hay una que dice **«sandhi»**: 1.522 formas.

| criterio | conserva de 14 correctas | deja pasar de 9 falsas | precisión |
| --- | ---: | ---: | ---: |
| (a) positiva — el DPD la marca «sandhi» | 14 | 4 | 77,8 % |
| (b) negativa — sin categoría ajena | 6 | 1 | 85,7 % |
| **(a) + el testigo** | **14** | **0** | **100 %** |

- **La (b) es la literal del enunciado y es la peor**: tira ocho correctas,
  porque una forma de sandhi corriente figura además como otra cosa (cetaṃ es
  *masc* y *nt* aparte de *sandhi*).
- **El criterio y el testigo son complementarios.** Cuatro de las nueve
  falsas —yeva, sāpi, sāyaṃ, yāyaṃ— el DPD **sí** las marca «sandhi»:
  reconoce que hay sandhi y descompone distinto, con el femenino sā/yā donde
  la receta pone el masculino so/yo. La categoría no las corta; la
  descomposición sí.
- **EL LÍMITE, Y ES SERIO: la etiqueta tiene 50 % de recall.** De las 18
  respuestas ya adjudicadas de la clase el DPD sólo etiqueta 9, y deja fuera
  **netaṃ, cāti y nātivattati — adjudicadas por el propio IEBH**, más cesā,
  nayimassa, nopeti, anabhineyya, soyeva y svassa. Sirve de **licencia**, no
  de **prueba de verdad**. Como puerta única silenciaría sandhis reales.

## 4 bis. LA CABECERA EN INGLÉS — pedido del IEBH, hecho

En modo inglés el título decía «Solucionador de sandhis» y el sobretítulo
«Kaccāyana · Sandhi-Kappa · Canon del Sexto Concilio»: los dos en español
dentro de una interfaz que ya estaba traducida. Ahora van con los mismos
`.i-es`/`.i-en` que el resto:

- **`Sandhi Solver`**, con la letra en color (`.dia`) conservada sobre la
  «i» de *Sandhi*, como el español la tiene sobre la de *sandhis*;
- **`Kaccāyana · Sandhi-Kappa · Sixth Council Canon`**;
- y el `<title>` de la pestaña, que también se queda en español al cambiar
  de idioma: ahora es una clave más de `TXT` (`titulo_doc`) y el bloque del
  idioma lo pone con `tr()`. Es lo primero que se lee al compartir el enlace.

Se toca **la plantilla**, `recursos/solucionador/plantilla.html`, nunca el
HTML de `site/`. Los CINCO arneses, en verde después del cambio.

## 5. AVISOS AL CHAT NUEVO

- **NADA DE ESTA SESIÓN SE HA APLICADO AL MOTOR.** Las tres firmas del §3 y
  el criterio del §4 son candidatas medidas. Ampliar la licencia de §34 y
  firmar el criterio **son del IEBH**. Decisión de Angel en esta sesión:
  «evidence only».
- **El arenal corta cada llamada de bash a los ~165-180 s**, sea cual sea el
  `timeout_ms` que se pida: un bucle de tres pasadas en una sola llamada se
  queda a medias. Una pasada por llamada, con `timeout 150`. Los procesos de
  fondo mueren igual (briefing 36 §5).
- **`.git/index.lock` se queda pegado** en la carpeta montada: un `git status`
  puede dejarlo y entonces todo git falla con «File exists». Borrarlo pide el
  permiso de Cowork (`allow_cowork_file_delete`); concedido en esta sesión.
- Las cachés de cómputo de los informes son compartibles apuntándolas al
  mismo archivo (`PROCLITICAS_CACHE`, `NIGGAHITA_CACHE`) — pero **la del
  sub-piso NO** (`SUBPISO_CACHE`), porque guarda otra cosa: el par de la
  receta, no la señal.
- Los tres informes se re-generaron dos y tres veces y salieron
  byte-idénticos; cero U+FFFD; NFC. Los CINCO arneses, en verde, con paridad
  16.366 de 16.366.

## 6. LO QUE SIGUE (en orden)

1. **Rotar la clave** si no consta (§0 — tres sesiones ya).
2. **Empujar los tres commits** si no se ha hecho (o el ciclo los lleva con
   el próximo lote).
3. **Enseñar al IEBH los dos informes nuevos** (§3 y §4): las tres firmas del
   sub-piso, con «saṃ»/«maṃ» que corta 23 falsas a coste cero; y el criterio
   suyo mecanizado, con el aviso de que su forma literal es la peor de las
   dos y de que la etiqueta tiene 50 % de recall. **Ampliar la licencia y
   firmar el criterio son suyos.**
4. **Reconciliar 385 contra 441** (§3, límite 2): probar si la precedencia
   entre patrones lo explica. Es acotado y deja el número limpio.
5. **La pasada única de dos junturas** (briefing 35 §4): cierra el punto 4 del
   mapa 32 (idamavocanti) y haría innecesarias muchas `escalera_iebh`.
6. Resto del mapa 33: §23/pakati sistemático, descomposiciones del DPD en el
   motor, des-flexión. **Sin empezar.**
