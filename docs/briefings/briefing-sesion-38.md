# Kaccāyana Pāḷi-Español: Briefing de la Sesión 38

*Complementa a los briefings 05–37. Tema de la sesión 38 (2026-08-30, en vivo
con IEBH, la misma tarde que la 37): **el corpus separado deja de ser una
muestra y se vuelve un instrumento** —de 5 textos a 47, de 562 junturas a
1.784— y, al volverse instrumento, empieza a decir cosas sobre el motor que
ninguna otra fuente decía. Al final del día hay UN diagnóstico, no una lista
de fallos sueltos. Y hay tres correcciones a lo que yo mismo había afirmado
horas antes: conviene leerlas, porque las tres eran del tipo «medí mal», no
del tipo «cambió el dato».*

> **Lo primero que tiene que saber el chat nuevo:** verificar
> `git log origin/main..main`. Las reglas de siempre: el Python es la
> referencia; los CINCO arneses mandan; nada se adjudica sin el visto bueno
> del IEBH; todo se mide antes y después; la atribución pública dice IEBH.
> Con IEBH se habla en inglés; lo del proyecto va en español.
> **Y una nueva, en CLAUDE.md**: cuando lleguen veredictos, las escaleras se
> proponen solas, sin que IEBH lo pida.

## 0. EL ESTADO, EN CUATRO CIFRAS

| | al abrir la 38 | al cerrarla |
| --- | ---: | ---: |
| textos del corpus separado | 5 | **47** |
| junturas atestiguadas | 562 | **1.784** |
| ecuaciones | 20 | **101** |
| casos adjudicados | 176 | **193** |

El motor señala **1.270 de 1.784 junturas (71,2 %)**. La cifra BAJA según
crece el corpus —era 77,2 % con cinco textos— y eso es lo esperable, no una
regresión: cada texto nuevo trae junturas que el banco no había visto.

## 1. EL DIAGNÓSTICO DEL DÍA, Y CÓMO SE ESTRECHÓ

Cotejando el corte del Venerable con la lectura del motor en las 1.784
junturas sale **un solo fallo con muchas caras**: el motor reconstruye la
primera voz con **la vocal final equivocada** cuando esa vocal se pierde en
el sandhi. Son **39 formas, masa 1.562**.

    hissa    501   «hi» → «ha»        tayome   139   «tayo» → «taya»
    tissa    265   «ti» → «ta»        yohaṃ     83   «yo»   → «ya»
    yāyaṃ    265   «yā» → «ya»        tatohaṃ   40   «tato» → «tata»

Dos sub-clases claras: los nominativos en «-o» ante «si», «ahaṃ» y «va»
leídos como temas en «-a» (katapuññosi, jātosi, paviṭṭhohaṃ), y los
femeninos en «-ī» leídos breves (lābhinī, vasantī, bhamantī).

**TRES TESTIGOS INDEPENDIENTES, un diagnóstico.** No es una impresión: lo
dicen por su lado el testigo del DPD en el informe de proclíticas (sāpi,
sāyaṃ, yāyaṃ son sā/yā, no so/yo), las ecuaciones de la Therīgāthā (sā,
tassā, purā, duggatā, āsi) y la separación del propio Venerable (yāyaṃ,
hissa, tayome).

**Y AQUÍ ESTÁ LO IMPORTANTE, que llegó al final del día y desmonta la
explicación fácil.** Yo había escrito que «el motor prefiere temas en -a».
Es falso:

    hevaṃ   2.663   →  hi + evaṃ    correcta, y con señal segura
    hetaṃ   1.369   →  hi + etaṃ    correcta, y con señal segura
    hissa     501   →  ha + ...     FALSA
    hānanda    30   →  hānaṃ + uda  FALSA (el IEBH: hi + ānanda)

La misma primera voz, «hi», bien ante «evaṃ» y «etaṃ» y mal ante «assa» y
«ānanda». **El fallo depende de la SEGUNDA voz, no de la primera.** Eso saca
el problema del terreno del léxico y lo mete en el de la derivación, que es
donde el chat nuevo tiene que mirar.

**Cuidado al contarlo, y es la trampa del día.** Otras **24** formas parecen
del mismo grupo y no lo son —natthīti, passāmīti, bhikkhūti—: ahí el IEBH
imprime la vocal ALARGADA ante «ti» (§18) y el motor da la breve subyacente,
que es lo correcto. **El corte del Venerable es de SUPERFICIE y la lectura
del motor es de FONDO.** Confundirlos fabrica 24 fallos que no existen. Yo
los conté mal en la primera pasada.

## 2. EL INGLÉS HABÍA ENTRADO EN EL CORPUS

`es_pali()` sabe descartar el ESPAÑOL y nada más. La Ānāpānassati-kathā de
la Visuddhimagga trae notas del traductor **en inglés**, y en inglés casi
toda palabra acaba en consonante: cada espacio parece una juntura. Estaban
publicadas como dato:

    «it | I»   → iti     8.058
    «at | the» → atthe   1.393     ← desde la PRIMERA corrida de la 37
    «can | do» → cando     299
    «M | A»    → ma         86     de «M.A. ii 94», y con ella T.A. y D.A.

La atestiguación no las atrapa: la forma unida existe en la edición por pura
coincidencia. `basura()` las criba con tres reglas **de PAR, no de línea**, y
ahí está el cuidado: filtrar la LÍNEA por palabras inglesas se probó y
quitaba junturas de verdad —idheva (876), sabbeva (512), yannūnāhaṃ (242)—,
porque estos documentos mezclan pāḷi e inglés en el mismo renglón. Medido:
retira **19 candidatas atestiguadas, las 19 basura**, y no añade ninguna.

Queda sin cribar «ana» (11), de la notación morfológica «’a’ - ’na’».

**Se probó y se DESCARTÓ** apretar el filtro del español para las ~6.500
candidatas descartadas (que son casi todas líneas españolas): tira también
199 líneas de pāḷi de verdad. El resguardo de atestiguación sigue siendo el
único filtro seguro.

## 3. «PAÑCA», Y LO QUE DESBLOQUEA

La regla «ñca = ṃ + ca» **ya estaba firmada** desde el 2026-08-28 (patrón de
§31, *Vaggantaṃ vā vagge*). Lo que faltaba era su excepción, y el IEBH la dio
el 2026-08-30: **pañca no es sandhi**.

`no_sandhi` acepta ahora `formas` (la voz exacta) además de `terminaciones`
(la clase entera, como -tvā/-tvāna). Las dos hacen falta y no son
intercambiables: una terminación «ñca» callaría la familia entera.

Medido sobre las **9.526 voces del canon acabadas en «ñca»** (masa 68.595):
el motor afirma 6.061, deja 1.696 en «posible» y calla 1.769. De las diez
voces con la silueta de pañca —forma frecuente, base rarísima— **las otras
nueve SÍ son sandhi**.

**LA DECISIÓN QUE QUEDA SOBRE LA MESA, y es del IEBH:** quitando a esta
familia el **resguardo de la base residual**, el patrón afirmaría **315
formas más**, y de esas 315 **sólo DOS son malas** —pañca, y
taṃsampayuttakānañca por base residual—. Las otras 313 son correctas y hoy
se silencian: kāmarāgānusayañca (622), paṭighānusayañca (602),
mānānusayañca (445), assādañca (190). Escribir pañca le quita a esa decisión
su riesgo mayor.

## 4. EL SOLUCIONADOR 1.12: LO REGISTRADO A MANO YA SE VE

Pedido del IEBH. Una voz dada de alta por el campo «sandhi no detectado» no
aparecía por ninguna parte: `analizar()` sólo dibuja tarjeta para lo que el
motor señala —`if(!r.senal) continue`— y una voz registrada a mano es, por
definición, una sobre la que el motor calla. Se guardaba y viajaba en el .md
con su veredicto, pero **sin tarjeta no había campo de nota, ni de escalera,
ni botón de borrar**, y el revisor no podía ver lo que acababa de escribir.

Ahora llevan tarjeta, rotuladas aparte y a la vista aunque se analice otro
pasaje. **La escalera importa ahí MÁS que en ninguna otra tarjeta, no
menos**: `escaleraIEBH()` existe para enseñar una escalera de mano cuando la
lectura afirmada no trae la del motor, y éstas nunca traen la del motor.

Y una precisión que IEBH pidió expresamente: **el cuadro de «observaciones»
NO se volvió el campo de escalera**, y a propósito. La escalera es dato de
UNA voz y vive en su tarjeta; las observaciones son prosa sobre MUCHAS y
siguen sin volverse datos. Juntarlas habría convertido prosa en dato, que es
lo único que ese cuadro tiene documentado no hacer.

## 5. LAS ESCALERAS PENDIENTES — lo que IEBH preguntó al cerrar

`auditar_derivacion_casos.py` sobre los 193 casos. Tres del lote del día
quedan sin escalera, **por tres motivos distintos**, y ninguno se resuelve
igual:

- **itiha = iti + ha** — «el motor corta, pero no ahí». No hay pasos porque
  **no ocurre nada**: la 'i' de «iti» no cambia ante la consonante 'h'. Eso
  es **pakati**, y lo cubre **§23 *Sarā pakati byañjane***. La escalera
  correcta es de un paso, como las 13 formas de pakati de
  `recursos/sandhi`. Propuesta, sin firmar.
- **sampakampi = sampakaṃ + api** — «voz no atestiguada: sampakaṃ». La
  escalera existe y está verificada en su hermana **saṅkampi**, que el motor
  sí deriva: `saṅkaṃ api → saṅkaṃ pi (§40) → saṅkam pi (§31) → saṅkampi
  (§11)`. La de sampakampi es idéntica en forma; sólo falta porque
  «sampakaṃ» no está en el léxico. Propuesta, sin firmar.
- **pāturahosi = pātur + ahosi** — **esto no es una pregunta de escalera,
  es de componentes.** Con los componentes firmados no hay ninguna operación
  que enseñar. Con `pātu + ahosi` el motor la deriva y la verifica:
  `pātu ahosi → pātu r ahosi (§35) → pāturahosi (§11)` —§35 es
  *Ya-va-ma-da-na-ta-ra-lā c’ āgamā*, la 'r' insertada ante vocal—. **Lo
  decide el IEBH.**

Y la regla nueva de CLAUDE.md, sección «Cuando llegan veredictos»: esto se
hace **solo**, cada vez que entren veredictos, sin que IEBH lo pida.

## 6. LO QUE HAY QUE CORREGIR DE MÍ MISMO

Principio 5, y son tres en un día:

1. **Dije que `pañca` se salvaba «por los pelos»** y que bajar el piso de §34
   haría leer *cinco* como sandhi 8.192 veces. **Falso por partida doble**:
   no lo calla el piso de §34 sino el **resguardo de la base residual**, y lo
   calla por 1 contra 8.192, que no es por los pelos.
2. **El commit c8843b1 dice «siete textos» y metió NUEVE.** Un
   `git add -- recursos/corpus-separado/` mío barrió **Aggañña-sutta** y
   **Mālukyaputta-sutta**, que IEBH había dejado en la carpeta mientras yo
   trabajaba — el mismo `git add -A` que yo le achacaba al ciclo. Enmendado
   en fb6f788; aportan 126 junturas, las más frecuentes del corpus.
3. **El commit d425df6 dice «los CINCO arneses en verde» y no lo estaban.**
   `arnes_corpus` había dado NO PASA en esa misma corrida y yo commiteé
   igual, porque mi cadena de shell sólo miraba el último arnés. Re-corridos
   después, los cinco pasan; el fallo era una carrera con el ciclo del IEBH,
   que estaba reescribiendo `referencia-senal-solo-canon.json` mientras el
   arnés lo leía. **La afirmación era falsa cuando la hice.**

## 7. EL CICLO Y EL ÁRBOL: UNA CARRERA, NO UNA GUARDA AUSENTE

`ciclo_veredictos.py` **sí** comprueba que el árbol esté limpio, en la línea
82, y funciona: rechazó dos veces al chat por archivos recién dejados. Lo que
falla es que **estadía con `git add -A` en la línea 172**, minutos después
—tras recoger la cola, incorporar, regenerar la página y correr los cinco
arneses—. Todo lo que aparezca en esos minutos está limpio en la comprobación
y barrido en el commit. Así entraron mis archivos en 9ce50c8 y f9ddf33.

**El arreglo es estadiar los archivos que el ciclo posee, no `-A`.** Sin
hacer: es la tubería de la firma y la toca el IEBH.

Efecto secundario a tener presente: **añadir textos y correr el ciclo compiten
por el árbol limpio.** Mientras IEBH deja archivos, el ciclo no corre.

## 8. AVISOS AL CHAT NUEVO

- **El arenal corta cada llamada de bash a los ~165 s**, sea cual sea el
  `timeout_ms`. Una pasada por llamada.
- **`.git/index.lock` se queda pegado** en la carpeta montada; borrarlo pide
  `allow_cowork_file_delete`.
- **Los arneses hay que mirarlos UNO A UNO.** Encadenarlos en un `for` y
  fiarse del código de salida miente: el del bucle es el del último. Ver §6.3.
- **El corpus está SATURADO para el sutta breve.** Los cuatro últimos dieron
  23 junturas entre los cuatro; el Pañhabyākaraṇa, cero. Lo que mueve la
  cifra es texto largo y comentario: Brahmajāla 98, Aggañña 80.
- **Las ecuaciones llevan clavadas en 101 todo el día**, y las 101 salen de
  los documentos de capítulo de la Therīgāthā, que son los únicos con «Lista
  de voces». Son la mejor evidencia —la resolución está DICHA y da los
  componentes SUBYACENTES— y es donde el motor saca **0 de 16**.

## 9. LO QUE SIGUE (en orden)

1. **Más documentos de capítulo de la Therīgāthā**, de los nipātas que
   faltan —Ekaka, Duka, Tika, Catukka, Aṭṭhaka en adelante—. Es la única
   fuente de ECUACIONES, que es la evidencia buena. La carpeta madre en el
   Drive es `1YH-j2nlDNtCGbf5y6PpbRFoDhRERw8IR`; el camino está probado
   (navegador → `data-id` de las filas → descarga por
   `…/export?format=txt`; **la primera llamada de JavaScript tras navegar
   devuelve la página vieja, hay que repetirla**).
2. **Enseñar al IEBH lo del día**: el diagnóstico de §1 con sus tres
   testigos, y la decisión del resguardo de §3 (313 correctas contra 2
   malas). **Ampliar el resguardo y firmar es suyo.**
3. **Las tres escaleras de §5**, para firma.
4. **El fallo de la segunda voz** (§1): mirar la derivación, no el léxico.
   Es el hilo más prometedor del día y está sin tirar.
5. **La lista corta de las 69** (briefing 37 §3 quater) por el modo revisión
   —hoy desbloqueado: las voces registradas a mano ya tienen tarjeta, con
   nota y escalera—. Empezando por la regla de los absolutivos en «-tvā».
6. **Medir el falso «segura» de `jānāti` y `pīti`** (briefing 37 §7).
7. **La pasada única de dos junturas** (briefing 35 §4).
8. **El `git add -A` del ciclo** (§7).
9. Resto del mapa 33. **Sin empezar.**

## 10. PROCEDENCIA: DOS COSAS QUE NO SE PUEDEN PERDER

- **El Ādittapariyāya-sutta lo traduce Rutty Bessoudo Salvo y lo revisa
  Bhikkhu Nandisena.** La traducción es de otra mano; la revisión es suya, de
  modo que el corte entra con la misma autoridad que el resto. Se nombran las
  dos. (En fb6f788 escribí que «el corte no es del Venerable»: enmendado el
  mismo día en 88e7313.)
- **La Ānāpānassati-kathā de la Visuddhimagga no es canon**, sino tratado.
  Está en el corpus y es útil, pero conviene saberlo si alguna vez se pesa el
  corpus por autoridad.
