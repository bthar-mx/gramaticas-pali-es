# Kaccāyana Pāḷi-Español: Briefing de la Sesión 37

*Complementa a los briefings 05–36. Tema de la sesión 37 (2026-08-30, en
vivo con IEBH): **el testigo del DPD deja de estar vacío y se pone a
trabajar; y al final del día aparece un testigo mejor, que es el Venerable
mismo.** Los dos informes re-corridos; un informe nuevo del sub-piso de §34
que encuentra que lo falso tiene firma y no es la frecuencia; el criterio de
categoría del IEBH mecanizado por fin, con su límite medido; y **el CORPUS
SEPARADO (§4 ter), que es lo más importante del día**: los textos bilingües
del IEBH traen las junturas abiertas y las ecuaciones de sandhi escritas, y
ya delatan lecturas FALSAS del motor, no sólo silencios. Nada adjudicado:
todo prepara, y firmar es del IEBH.*

> **Lo primero que tiene que saber el chat nuevo:** verificar
> `git log origin/main..main`. Las reglas de siempre: el Python es la referencia; los CINCO
> arneses mandan; nada se adjudica sin el visto bueno del IEBH; todo se
> mide antes y después; la atribución pública dice IEBH. Con IEBH se habla
> en inglés; lo del proyecto va en español.

## 0. LA CLAVE — ROTADA. Cerrado, y por qué tardó tres sesiones

**HECHO el 2026-08-30.** IEBH la rotó con `npx wrangler secret put
CLAVE_VEREDICTOS` («Success! Uploaded secret»), y quedó comprobada: con el
valor nuevo, `traer_veredictos.py --solo-mirar` lista la cola. **No hay que
volver a preguntarlo.**

**Por qué se arrastró desde el briefing 35, que es la lección:** el §0 decía
«rotar con un valor nuevo que no se escriba en ninguna parte» sin decir
NUNCA qué descalificaba al viejo. Y lo que lo descalificaba es que **el valor
original lo generó Claude en un chat durante la instalación** — no un
descuido del IEBH, que se limitó a usar la clave que se le dio. Un aviso que
no dice su razón se lee como una manía y se pospone. El valor nuevo lo
generó IEBH en su Mac con `secrets.token_urlsafe(24)` y no ha pasado por
ningún chat.

**Regla que queda:** Claude no es fuente de secretos. Si hace falta uno, se
genera en la máquina de quien lo usa y se pega directo en el `prompt` de
wrangler, que lo enmascara.

Contexto que en dos briefings no se había dicho, y que dimensiona el asunto:
si la clave se filtra, **lo peor posible es que alguien lea o vacíe la
cola**. No puede publicar ni adjudicar: eso sigue pidiendo la Mac, los
arneses y la firma. Enviar a la cola es abierto a propósito.

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

  Precisión sobre lo adjudicable: **76,2 % → 91,5 %**. Las dos primeras
  voces se descartan por razones DISTINTAS (precisiones del IEBH,
  2026-08-30): «saṃ-» es un **prefijo, y se antepone a nombres y a verbos**
  —antes se decía «preverbo», que es más estrecho—, de modo que samāgama es
  compuesto; «maṃ» **no es prefijo, es el ACUSATIVO del pronombre «amha»**, y
  **«mama» es dativo y genitivo de ese mismo pronombre** — las dos son del
  paradigma de amha, no piezas que se antepongan a nada. El grupo de «-ti»
  es §34 quitándole formas al patrón de «iti», que ya está firmado
  (satimantoti es satimanto + iti).

**DOS LÍMITES, declarados en el propio informe y que no hay que perder:**

1. **El DPD CALLA sobre jātimaraṇā y sobre vedhamānehi.** El testigo no
   adjudica los dos casos que fijaron el piso; los adjudicó el juicio de
   IEBH y sigue haciendo falta. La correcta que el piso silencia y el
   testigo confirma es **tvamasi = tvaṃ + asi**.

   **ENMIENDA DEL IEBH (2026-08-30), y toca tres archivos:** *jāti + maraṇā*
   lleva ā; *vedhamāna* es **compuesto**, no participio; y **ekamante, que
   se citaba desde el briefing 36 §3 como la segunda correcta silenciada por
   el piso, es COMPUESTA** — de modo que ahí el piso acierta y el ejemplo
   estaba mal elegido. **Ninguna cifra se mueve**: el testigo callaba sobre
   ekamante y por eso nunca entró en las 199 confirmadas. Pero quita un
   argumento a favor de bajar el piso, y así se le ha dicho. Corregido en
   `solucionar_sandhis.py`, en `generar_informe_subpiso_34.py` y en el
   informe al Venerable; el briefing 36 se deja como quedó, que es el
   registro de lo que se creía entonces.
2. ~~La cuenta no cuadra con el briefing 36 §3.~~ **RECONCILIADA EXACTAMENTE
   el mismo día — ver §3 bis.**

De paso, medido y no supuesto: el artefacto «m»/«ṃ» del cotejo con el DPD
(«sabbam + idaṃ» frente a «sabbaṃ + idaṃ») es de **un caso en 419**.

## 3 bis. 385 CONTRA 441: RECONCILIADO, Y NO QUEDA NADA SIN EXPLICAR

La hipótesis del §3 era la precedencia, y era la correcta. Corriendo el
camino REAL de `senal()` con `frec_minima` = 0 sobre la referencia:

| | hoy | en el commit de la sesión 36 |
| --- | ---: | ---: |
| la receta suelta afirma | 449 | 449 |
| `senal()` afirma | **384** | **385** |
| bloqueadas, todas atribuidas | 65 | 64 |

Las 65 se reparten así: **57 las reclama antes otro patrón** (54 el de
«iti», 3 el del verso), **7 son lecturas ya adjudicadas** y **1 la manda el
banco**. Ninguna queda sin explicar, y tampoco al revés: no hay ni una forma
que `senal()` afirme y la receta no.

**La única forma que separa 384 de 385 es `evamayaṃ`**, que no era caso
cuando se midió en la sesión 36 y sí lo es desde la cola del 2026-08-30. El
385 del briefing 36 §3 era correcto cuando se tomó.

Medido en un `git worktree` desechable sobre `94bac5e~1`, sin tocar el árbol
—y allí el testigo del DPD no está, que es justamente el estado de la máquina
que midió el 385—.

## 3 ter. EL CICLO SE CERRABA CONTRA UN ARCHIVO RANCIO, Y LA COLA IBA DE UNA EN UNA

Dos defectos que salieron del uso real, no de una revisión:

- **`ciclo_veredictos.py` no re-vertía la referencia de la PÁGINA.** El lote
  de 22 adjudicaciones del 2026-08-30 se detuvo en la etapa 4: el caso nuevo
  «iccassa» cambia la forma del banco «icc assa» —`cotejo()` pliega las dos
  a la misma clave—, la página lo reflejaba y la referencia, del 2026-08-29,
  no. Re-vertía la de señal y las dos del corpus: **tres de cuatro**. Ya son
  cuatro. Al re-verterla cambió UNA entrada de 266.
- **El worker leía el KV de una en una.** El GET tenía el `await` DENTRO del
  bucle, así que el tiempo era la SUMA de las lecturas. Con `Promise.all` es
  el de la más lenta. Y `--solo-mirar` descargaba todos los `.md` sólo para
  contar «VEREDICTO:»: la cuenta viaja ya como METADATO del KV y
  `?resumen=1` la da con `list()` a secas, sin leer un solo valor. De paso,
  `list()` pagina de 1.000 y el bucle no seguía el cursor — una cola sin
  vaciar en meses habría devuelto media cola en silencio.

**Pendiente de la misma familia:** la referencia del BANCO podría quedarse
rancia igual. No se tocó porque no se demostró — la etapa 1 pasó con 266 de
266—, y este proyecto no arregla por sospecha.

## 3 quater. EL LOTE 1 NO SON 231, SON 69

`por-adjudicar-lote-1.md` se generó el 2026-08-28, antes de que se firmaran
los patrones y §34. Re-medido contra el motor de hoy, de sus 231 voces sin
caso:

| | formas | |
| --- | ---: | --- |
| ya las afirma un patrón firmado | 144 | el motor las responde solo |
| señal segura por otra vía | 14 | ver el aviso de abajo |
| **siguen «posible» — el atasco real** | **69** | masa 52.273 |
| sin señal ninguna | 4 | dassetvā, kathetvā, uppādetvā, bhāvetvā |

Encabezan las 69: nava (7.423), neva (3.404), tava (2.420), nanu (2.352),
tatheva (1.962). Las cuatro en «-tvā» son la regla de los absolutivos que el
propio `traer_veredictos.py` nombra en su cabecera: **una firma cubriría la
clase entera**, en vez de cuatro casos.

**No hay que rellenar el archivo de 3.852 líneas.** Lo que corresponde es una
lista corta de esas 69 por el modo revisión de la página, donde los
veredictos llegan con escalera y por la cola.

**AVISO, y es de los que importan:** de las 14 «segura por otra vía», varias
son palabras corrientes, no sandhis — `jānāti` (3.916) sale como «jānā +
iti» y `pīti` (821) como «pa + iti», por la regla de vocal larga ante «ti».
Es el nivel de PREDICCIÓN FIRME acertando mal, que es justo lo que el IEBH
señaló con caranto y sattānaṃ. Puede ser el 5-10 % de error ya medido, pero
es también exactamente lo que cortaría el criterio de categoría del §4. Sin
medir todavía.

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

## 4 ter. EL CORPUS SEPARADO — lo más importante del día, y lo más nuevo

El IEBH trajo los textos bilingües del IEBH (Bhikkhu Nandisena), y con ellos el
proyecto tiene por primera vez **segmentación de mano del Venerable**, que es
el dato que CLAUDE.md declara como cuello de botella: «sin saber que lokaggo
es loka + aggo no hay motor de reglas que valga».

### Dos maneras de leerlos, y la segunda es mejor

**1. Junturas por separación** (`herramientas/extraer_junturas_separadas.py`
→ `recursos/corpus-separado/junturas.json`). Los textos imprimen el pāḷi con
las junturas ABIERTAS —«Evam eva», «yad idaṃ», «Puna c’ aparaṃ», «sato ’va»—
donde la edición las imprime unidas. Unir es literal: fuera el espacio y el
apóstrofo.

Cómo se distingue de un espacio corriente, que el documento usa igual para
las dos cosas: el **apóstrofo** es inequívoco; y una palabra pāḷi acaba en
vocal o en «ṃ», así que una acabada en consonante —evam, yad, kathañ, imam,
tam, tañ, yāvad, muttan— está a media operación y abre juntura.

**2. Ecuaciones de la «Lista de voces»**
(`herramientas/extraer_ecuaciones_sandhi.py` → `ecuaciones.json`). Los
documentos de capítulo de la Therīgāthā traen las formas de sandhi
**resueltas con un signo igual**: «Nāccharāsaṅghātamattam = na
accharāsaṅghātamattaṃ». Es mejor evidencia por dos razones: la resolución
está DICHA y no inferida, y da los componentes **subyacentes** —cittassa +
upasamaṃ— y no sólo el corte de superficie. Eso es lo que un caso necesita.

### Cómo se verifica cada uno, y NO es lo mismo

- **Junturas**: se publica sólo si la forma UNIDA está atestiguada en la
  edición. Sobre el Mahāsatipaṭṭhāna dio 474 de 474 y descartó 0, que es la
  mejor señal de que el método es sano.
- **Ecuaciones**: la primera versión exigía lo mismo de la forma de la
  IZQUIERDA y **descartaba todo**, con razón —«Nāccharāsaṅghātamattam» acaba
  en «m» porque le sigue «pi» y en la edición existe unida a ella—. La
  izquierda es un fragmento a media operación. Lo correcto: que las voces de
  la DERECHA estén atestiguadas, y comprobar aparte si el motor RECOMPONE,
  tolerando la «m» final por «ṃ».

### Lo que lleva encontrado (5 textos, al cierre)

**562 junturas**, las 562 atestiguadas, 78 candidatas descartadas. El motor
señala 434 (77,2 %) y **no ve 116**. Y 20 ecuaciones, 4 de juntura.

Las que no ve no son menudencias: tenāha (6.018), ādimāha (3.961), cettha
(2.140), vuttanayeneva (1.908), athassa (1.790), panassa (1.731), caparaṃ
(1.548), cassa (1.544), cetaṃ (1.038).

**Y hay errores, no sólo silencios:**

| el Venerable | el motor | |
| --- | --- | --- |
| caparaṃ = c \| aparaṃ | capi + araṃ | falso |
| nāhaṃ = na + ahaṃ | na + **haṃ** | segunda voz inexistente, y sin señal |
| sājja = sā + ajja | **sa** + ajja | vocal breve por larga |
| tvamasi = tvam \| asi | ta + vamasi | falso |
| cittassūpasam’ = cittassa + upasamaṃ | — | no lo recompone |

`tvamasi` importa aparte: es una de las dos formas que el informe cita como
CORRECTAS silenciadas por el piso de §34, y resulta que el motor no sólo la
calla, la lee mal.

### Lo que esto le hace a las dos decisiones

Las dos del §3 y §4 se apoyaban en el testigo del DPD, que **callaba sobre
158 de 419**. El texto del Venerable no calla. Separa «c | ettha», «c |
assa», «c | etaṃ», «c | esa» —las cuatro proclíticas que el mecanismo
afirmaría y la página no señala— y trae 89 junturas de §34 de las que el
motor no ve 26, entre ellas dos que **lee bien y calla por el resguardo**
(vuttanayameva 571, pattacīvaramādāya 467). Todo eso está ya en el informe
al Venerable.

### Estado y lo que falta

En `recursos/corpus-separado/`: el Mahāsatipaṭṭhāna y su Vaṇṇanā (completos,
los puso IEBH), la Therīgāthā I-IV, y de Pañcakanipāta los versos 67-71 y
72-81. El `LEEME.md` de la carpeta explica procedencia, licencia y qué hacer
con un archivo nuevo (nada: se deja el `.txt` crudo).

**Faltan 19 documentos** de los tres capítulos que pidió IEBH: Pañcaka 12
—van 4—, Chakka 8, Sattaka 3. Se recogen del Drive del proyecto abriendo la
carpeta con el navegador y sacando los `data-id` de las filas, y luego
`https://docs.google.com/document/d/<id>/export?format=txt`. **Ojo con el
navegador: la primera llamada de JavaScript tras navegar devuelve la página
vieja; hay que repetirla.** Los identificadores de los tres capítulos:
Pañcaka `1TNamf2nmBkvgC2gvrZXWuXvai5btJTLh`, Chakka
`1ClowIWWdbZuQT0qlhaN1Ij02ExpX6UGj`, Sattaka
`1hkEsXxKBz3y21RIkPwd-e6ufkTp0btV8`.

**Sin usar todavía**, y está en esos mismos documentos: las citas de
Kaccāyana atadas a formas concretas (Kac. §45, Rū. 470, Kac. §517), las
raíces en la convención del proyecto (√gamu, √labha, √visa, √ñā, √disī), el
análisis morfológico con el nombre del paradigma —que es lo que
`recursos/paradigmas` cubre— y el aparato de variantes de las notas al pie
(PTS, Sī, Syā, Ka).

**El PDF del Mahāparinibbāna** está en la carpeta y **diagnostica limpio**:
122 páginas con capa de texto de verdad y diacríticos correctos, de modo que
NO hace falta OCR. Sin extraer.

## 5. AVISOS AL CHAT NUEVO

- **NADA DE ESTA SESIÓN SE HA APLICADO AL MOTOR.** Las tres firmas del §3 y
  el criterio del §4 son candidatas medidas. Ampliar la licencia de §34 y
  firmar el criterio **son del IEBH**. Decisión del IEBH en esta sesión:
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

1. ~~Rotar la clave.~~ **HECHA** (§0).
2. ~~Reconciliar 385 contra 441.~~ **HECHA** (§3 bis).
3. **Enseñar al IEBH los dos informes nuevos** (§3 y §4): las tres firmas del
   sub-piso, con «saṃ»/«maṃ» que corta 23 falsas a coste cero; y el criterio
   suyo mecanizado, con el aviso de que su forma literal es la peor de las
   dos y de que la etiqueta tiene 50 % de recall. **Ampliar la licencia y
   firmar el criterio son suyos.**
4. **Terminar el corpus separado** (§4 ter): los 19 documentos que faltan de
   Pañcaka, Chakka y Sattaka, y extraer el PDF del Mahāparinibbāna, que
   diagnostica limpio. Es trabajo mecánico y bien definido.
5. **Los siete arreglos que el corpus ya delata** —caparaṃ, panassa,
   tamenaṃ, yāvadeva, nāhaṃ, sājja y la familia de `mhī`—: están medidos y
   **sin registrar**, porque convertirlos en casos es adjudicar.
6. **La lista corta de las 69** (§3 quater) por el modo revisión, en vez del
   archivo de 3.852 líneas. Empezando por la regla de los absolutivos en
   «-tvā», que es UNA firma para cuatro voces.
7. **Medir el falso «segura» de `jānāti` y `pīti`** (§3 quater): cuánto
   dispara la regla de vocal larga ante «ti» sobre palabras corrientes, y si
   el criterio de categoría del §4 lo cortaría. Evidencia, no aplicación.
8. **La pasada única de dos junturas** (briefing 35 §4): cierra el punto 4 del
   mapa 32 (idamavocanti) y haría innecesarias muchas `escalera_iebh`.
9. Resto del mapa 33: §23/pakati sistemático, descomposiciones del DPD en el
   motor, des-flexión. **Sin empezar.**

**Lo que el corpus separado desbloquea a plazo**, y conviene no perderlo de
vista: es la primera vez que se puede medir el recall sobre TEXTO CORRIDO y
no sobre un banco, y es el material que el solucionador de párrafos
necesitaba para el problema que CLAUDE.md declara insoluble sin él.
