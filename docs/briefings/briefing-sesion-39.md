# Kaccāyana Pāḷi-Español: Briefing de la Sesión 39

*Complementa a los briefings 05–38. Tema de la sesión 39 (2026-08-30, en vivo
con IEBH, la misma tarde que la 37 y la 38): **el Saddanīti entra en el
proyecto**. Empezó como un trabajo mecánico —traer los documentos de capítulo
de la Therīgāthā— y terminó con la primera operación no kaccayaniana del
motor, una fuente nueva, y un criterio que IEBH pidió poner por escrito y que
manda sobre todo lo demás.*

> **Lo primero que tiene que saber el chat nuevo:** verificar
> `git log origin/main..main`. Las reglas de siempre: el Python es la
> referencia; los CINCO arneses mandan; nada se adjudica sin el visto bueno
> del IEBH; todo se mide antes y después; la atribución pública dice IEBH.
> Con IEBH se habla en inglés; lo del proyecto va en español.
> **Y la nueva de esta sesión, ya en CLAUDE.md**: el Tipiṭaka es la fuente y
> Kaccāyana la autoridad que lo explica. Recomponer no basta.

## 0. EL ESTADO, EN CIFRAS

| | al abrir la 39 | al cerrarla |
| --- | ---: | ---: |
| textos del corpus separado | 47 | **80** |
| junturas distintas | 1.784 | **2.045** |
| ecuaciones | 101 | **141** |
| casos adjudicados | 193 | **195** |
| señal «segura» / «posible» | 2.300 / 2.182 | **2.300 / 2.185** |

Once commits, de `804fff4` a `b33d0d5`. **Ninguno empujado por este chat**;
comprobar si el ciclo los empujó.

## 1. EL CRITERIO QUE MANDA SOBRE TODO — pedido del IEBH

Está en `CLAUDE.md`, en su propia sección, y no es un detalle de esta sesión:
es cómo se decide de aquí en adelante.

**Una lectura puede ser impecable por las reglas y no ser una lectura.** Que
una cadena de aforismos recomponga la forma demuestra que la gramática PODRÍA
producirla, no que el Tipiṭaka la diga.

1. **Recomponer es necesario y no suficiente.** «tveva» recomponía por siete
   caminos y el canon dice uno.
2. **Que las voces estén atestiguadas TAMPOCO alcanza.** «tvaṃ» aparece 7.857
   veces y «tvṃ» una, y «tvaṃ + eva» sigue sin ser lo que el canon lee en
   «tveva». **Atestiguar la pieza no atestigua la juntura.**
3. Lo teóricamente posible no se publica como si fuera lo que dice el canon.

**Lo que hoy NO se puede hacer, y es el trabajo grande que esto abre:**
comprobar que dos voces van JUNTAS pide el TEXTO CORRIDO, y aquí sólo hay
formas con cuentas (`recursos/corpus/corpus-formas.json`, 681.927 formas,
8.062.163 fichas, sin contexto). Se puede contar, no leer. El texto corrido lo
tiene el OSBCT. **Conectar los dos proyectos es lo que convertiría este
criterio en un filtro automático en vez de una poda a mano.**

## 2. SADDANĪTI SUTTAMĀLĀ 49 — la primera operación no kaccayaniana

El IEBH observó que «tveva» significa a veces «iti eva» y a veces «tu eva»:
citativo en «sabbe kāmā ‘kāmā’ tveva saṅkhaṃ gacchanti» y en «“Aññāsikoṇḍañño”
tveva» del Dhammacakkappavattana; «tu eva» en «avijjāya tveva». Para el
segundo hay Kaccāyana §18; para el primero no encontraba autoridad. **La hay:**

> **49. Evass’ ekāre itiss’ aññassa c’ issa vo.** Evasaddassa ekāre pare
> itisaddassa aññassa ca saddassa issa vakāro hoti kvaci: «itv eva coro asim
> āvudhañ ca; vilapatv eva so dijo; Isigili tv eva; Samantapāsādikā tv eva».
> Kvacī ti kiṃ: icc eva.

Y el sutta anterior dice por qué no sale con ‘y’: «itisaddassa ikārena saddhiṃ
tyakārasaññogassa asamāgamo» — el conjunto ‘ty’ no se junta con la ‘i’ de
«iti»—. La edición lo confirma sola: **«tyeva» es CERO en 118 volúmenes**,
mientras «tyāhaṃ», «tyassa» y «tyajja» sí se imprimen. La cuenta se hizo antes
de dar con el sutta.

**Dónde NO está**, comprobado sobre el texto entero: Kaccāyana + Rūpasiddhi dan
`itveva` 0 · `tveva` 0 · `tyeva` 0 · `icceva` 193. **Kaccāyana §51 tampoco**:
es sutta de upasagga y nipāta, y sus secuencias mandan 'i' a 'y' (Nyāyogo,
§21) y 'u' a 'v' (Dvālayo, §18); no hay ningún paso 'y' → 'v'. El Nyāsa no
está callado —12 «tveva», 6 «tyeva»— pero son todos «bhavatu/hotu + eva» y
«bhavati + eva»: el par mínimo de §18 contra §21, nunca con «iti».

**Cotejado contra Helmer Smith** (Saddanīti III, p. 617 = pág. 24 del PDF):
Smith trae **cuatro** ejemplos donde el texto romanizado de Bhaddacak trae
uno, y dos de los que faltaban son los que deciden —«Isigili tv eva» y
«Samantapāsādikā tv eva», la fórmula del nombre—. Su aparato da «Kc» para los
suttas 50 y 51 y **ninguno para el 49**: testimonio suyo de que Kaccāyana no
tiene sutta correspondiente.

### Cómo quedó implementada

`op_S49` en `nuestro/operaciones.py` **y** `opS49` en
`nuestro/js/operaciones.js` (porte a mano, sin transpilador), más `"S49"` en
el `ORDEN` de los dos motores. La clave es `S49` y no `49` porque **el 49 del
motor es el de Kaccāyana y está tomado**.

**El alcance se estrechó, y es restricción NUESTRA, no del sutta.** Se exige
que la primera voz acabe en «-ti». El sutta dice «issa» y «aññassa ca
saddassa», que es más ancho; pero sus cuatro ejemplos son unánimemente «-ti».
Medido sobre las 681.927 formas:

| | formas | masa |
| --- | ---: | ---: |
| como lo dice el sutta (cualquier 'i' final) | 248 | 1.821 |
| estrechado a «-ti» | **234** | **1.276** |

Las 14 que caen son todas falsas —la regla ancha proponía «si + eva» para
«sveva», «di + eva» para «dveva», «esi + eva» para «esveva»— y se apoyan en
voces que la edición trae una o dos veces («si» 2, «di» 1, «esi» 14).

**Las lecturas verdaderas de esas formas las adjudicó IEBH el 2026-08-30**, y
se anotan aquí porque el chat que venga las va a necesitar:

    sveva   = so + eva    (§18)
    dveva   = dvi + eva   (§12)
    esveva  = eso + eva   (§18)

<!-- ENMIENDA del mismo día, y es de las que hay que declarar. La lista de
     lecturas falsas era correcta —es lo que la regla ancha generaba de más—,
     pero en la primera redacción añadí de mi cosecha «cuando es dve + eva» y
     «dvevassasahassāyukā, que es dve vassasahassāyukā». Eso no era una medida
     ni una cita: era una glosa mía sin autoridad, escrita el mismo día en que
     IEBH pidió dejar por escrito que lo teóricamente posible no se publica
     como si fuera lo que dice el canon. La corrigió él: es «dvi + eva» por
     §12. Enumerar lo que el motor propone de más es una cosa; decir lo que la
     voz ES, otra, y la segunda no me toca. -->

**Sin la restricción, `arnes.js` se detenía**:
la forma `sv eva` del banco salía con una octava lectura falsa. Queda un
`<!-- DUDA -->` en el código: estrechar el enunciado lo decide el IEBH.

Lo que SÍ entra son los citativos, que es lo que se buscaba: `subhantveva`
(subhanti + eva), `rūpantveva`, `dhammakathikotveva`, `samaṇotveva`,
`aṅgantveva` — la fórmula del nombre y de la cuenta.

## 3. «tveva»: TRES decisiones en un día, y las tres son del IEBH

| | qué | commit |
| --- | --- | --- |
| mañana | adjudicado «tu + eva» | (sesión 38) |
| tarde | **retirada** la adjudicación: 7 lecturas, ninguna afirmada | `b272eee` |
| noche | adjudicado **«ti + eva»**, la citativa | `cb9b56d` |

Queda la última. Y con ella, **`avijjāyatveva` = «tu + eva»** (Kacc. §18) bajo
la voz unida —14 veces en la edición—, para que esa voz dé la respuesta
correcta cuando aparezca. Mismo recurso que `aññāsikoṇḍaññotveva` = «iti +
eva», que entró antes.

**La limitación de fondo, que sigue en pie:** la ficha admite UNA lectura por
forma y el motor analiza **una voz por vez, sin ver la vecina**
—`_aplicar_caso(r)` busca por `r["cotejo"]` y ese registro no trae la frase—.
Por eso no se puede adjudicar «iti + eva» en el primer discurso y «tu + eva»
en «avijjāya tveva»: no hay dónde escribir «aquí sí, allí no». Que la ficha
admita varias lecturas con su discriminante es cambio de esquema, de análisis
y de `arnes_casos` a la vez, **y es el pendiente más claro que deja esta
sesión**.

Todo el asunto, con las cuentas y las citas, en
`docs/solucionador/tveva-dos-lecturas.md`.

## 4. LA COLA YA NO SE ATASCA A SÍ MISMA — y ahora dice qué pasó

**El atasco**, que costó media tarde: cuando el incorporador declina un lote,
no hay casos nuevos y `ciclo_veredictos.py` salía por `return 0` SIN commitear
lo que `traer_veredictos.py` acababa de archivar. Ese archivo quedaba suelto y
**la comprobación de árbol limpio de la corrida SIGUIENTE se negaba a
correr**. Pasó en `92281b1` y otra vez hoy. Arreglado con `archivar_cola()`,
que commitea el archivo del lote y nada más, estadiando por nombre —nunca
`git add -A`—.

**Y declinar NO es un error**: el incorporador devuelve 0 igual, así que
`traer_veredictos` borraba de la cola lo declinado y el veredicto se gastaba
en silencio. Ahora hay **RESUMEN** al final: qué le pasó a cada veredicto
—incorporado, enriquecido, ya adjudicada, DECLINADO, ILEGIBLE, SIN
VEREDICTO—, con el porqué y una línea que nombra los que no entraron.

**Y un ensayo para verlo antes de gastar la cola:**

    python3 herramientas/incorporar_adjudicaciones.py <lote> --sin-tocar
    VEREDICTOS_CLAVE=… python3 herramientas/traer_veredictos.py --ensayo

El segundo baja la cola de verdad, la pasa por el incorporador en modo ensayo
con archivos temporales, y NO archiva, NO incorpora y NO vacía la cola. Hace
falta porque **la corrida buena es irreversible**: la cola se vacía al
incorporar y el archivo no se vuelve a leer. La orden del IEBH no cambia
—`ciclo_veredictos.py` sigue siendo la misma—; el ensayo es opcional.

**Sigue sin hacer**, y es de la misma familia: el `git add -A` de la línea 172
en el camino normal (briefing 38 §7 y §9.8). El patrón correcto está escrito
al lado, en `archivar_cola()`. Y un caso hermano: si falla un arnés, el lote
archivado también queda suelto; ahí el árbol se deja a propósito para
diagnosticar, de modo que el arreglo no es el mismo.

## 5. THERĪGĀTHĀ I-IV, y dos correcciones al mapa del briefing 38

Entraron los 32 documentos de capítulo de Ekaka, Duka, Tika y Catukka —versos
1 a 66— más el Mahānidāna-sutta que aportó IEBH. Los 32 traen «Lista de
voces», que es lo que los hace fuente de ecuaciones.

**Las ecuaciones nuevas caen sobre el diagnóstico del briefing 38 §1** y son
testimonio independiente, porque estos nipātas se tradujeron antes de que
existiera el motor:

    tassāhaṃ      tassā + ahaṃ        el motor: tassa + haṃ
    sāhaṃ         sā + ahaṃ           el motor: sa + haṃ
    duggatāhaṃ    duggatā + ahaṃ      el motor: duggata + haṃ
    purāyaṃ       purā + ayaṃ         el motor: pura + āyaṃ
    māhu          mā + ahu            el motor: ma + āhu
    āsūpasampadā  āsi + upasampadā    el motor: āsa + upasampadā

Y una que afina el hallazgo tardío del §1: en **«nāhaṃ = na + ahaṃ» el motor
responde «na + haṃ»**. La primera voz está BIEN; falla la segunda. Es el hilo
de 38 §9.4, sigue sin tirarse, y ahora tiene un ejemplar limpio.

**Dos correcciones al briefing 38 §9.1**, las dos «el mapa estaba viejo»:

1. **No hay Aṭṭhakanipāta ni nada posterior.** El Drive tiene siete carpetas
   de nipāta, de Ekaka a Sattaka. «Aṭṭhaka en adelante» no tiene nada detrás.
2. **El Sattaka ya estaba completo**: son tres documentos y los tres estaban.
   Sīsūpacālā (196-203) no falta del corpus — falta de traducir.

**Y el camino del Drive cambió:** el `data-id` de las filas ya no se puede
leer con `querySelectorAll('[data-id]')` porque la página trae un `<script
data-id>` con 28 KB de JSON de sesión y devolverlo hace saltar la guarda del
navegador. **Filtrar a `tr[data-id]` pasa.** El resto del camino sigue igual.

`therigatha-I-IV.txt` quedó **redundante**: su cabecera dice PARCIAL, versos
1-66, que es justo lo que cubren los 32 documentos nuevos, con menos. No
estorba —las junturas se deduplican— pero está superado.

## 6. FUENTES NUEVAS, registradas en `comun/fuentes-externas.md`

**bhaddacak.github.io/grammarbooks** (lo encontró IEBH). Trae el **Saddanīti
entero** —Suttamālā con sus 1.347 suttas, Dhātumālā, Padamālā—, Moggallāna,
Payogasiddhi, Niruttidīpanī, Rūpasiddhi y un buscador de suttas entre obras.
Es lo que resolvió la pregunta del día. **Dos advertencias que no son
menores:** el editor avisa de erratas y pide cotejar contra Helmer Smith para
cita seria —y se comprobó cierta el mismo día: en el sutta 49 trae un ejemplo
donde Smith trae cuatro—; y la licencia es CC BY-NC-ND, de modo que consultar
sí y redistribuir no.

**El Smith en PDF.** Imagen pura, sin capa de texto, pero **escaneo excelente y
legible a 150 dpi** con `pdftoppm`. Sirve para COTEJAR PÁGINA A PÁGINA y para
leer el aparato, que trae las concordancias Kc/Rūp/Mmd y la referencia
canónica de cada ejemplo. La página impresa no coincide con la del PDF: la 617
impresa es la 24 del PDF, porque la paginación de Smith corre continua a
través de las tres partes.

**El OCR de archive.org NO sirve**, y está medido: mete letras CIRÍLICAS en
palabras pāḷi (`sakammika` → `ѕакаттіка`), pone diéresis por macrón (`ādīsu` →
`ädisu`), confunde `t` con `l` sistemáticamente (`bhavati` → `bhavali`) y
pierde los puntos suscritos. **De cada volumen conviene bajar sólo el `.pdf`
liso y el `_page_numbers.json`** —que mapea índice de escaneo a página impresa
y ahorra la búsqueda a tientas—; los formatos `_djvu.txt`, `_hocr`, `_chocr` y
`_text.pdf` salen todos de la misma pasada de OCR. La introducción de Smith
está en **francés**.

## 7. AVISOS AL CHAT NUEVO — los de siempre y tres nuevos

- **El arenal corta cada llamada de bash a los ~165 s.** Una pasada por
  llamada.
- **Los procesos en segundo plano NO sobreviven entre llamadas de bash.**
  Lanzar algo con `&` y volver a mirarlo en la llamada siguiente es mirar un
  fantasma: `pgrep -f` casa con `bwrap`, el envoltorio del arenal, y contesta
  «corriendo» de algo que ya murió. Se perdieron varios minutos así. Lo que
  tarde más de 165 s hay que correrlo en trozos, en primer plano.
- **La caché de la señal NO mira `operaciones.py`.** Se invalida por huella de
  `casos-reportados.json` y `reglas.json`; al cambiar una operación hay que
  borrar `~/.cache/gramaticas-pali-senal.json` a mano o sirve datos rancios en
  silencio. Con la caché fría tarda unos cinco minutos, en dos o tres trozos.
- **Añadir una regla cuesta un ciclo de re-vertido entero**: la regla se
  escribe DOS veces (Python y JS) y hay que re-vertir las referencias de señal
  y de corpus (verso y prosa) y regenerar la página. Diez líneas de regla,
  media hora de tubería.
- **Los arneses, UNO A UNO.** Encadenarlos y fiarse del código de salida
  miente.
- **`.git/index.lock` se queda pegado**; borrarlo pide
  `allow_cowork_file_delete`.

## 8. LO QUE HAY QUE CORREGIR DE MÍ MISMO (principio 5)

1. **Propuse la clave unida como «el arreglo» sin comprobar el token del
   pasaje.** Registré `aññāsikoṇḍaññotveva` y dije que resolvía el
   Dhammacakkappavattana. No podía: ahí el texto imprime el nombre y la
   partícula SEPARADOS, de modo que el token es «tveva» y esa clave no dispara
   nunca. Comprobé que la forma unida estuviera atestiguada, que es otra
   pregunta.
2. **Llamé a `subhantveva` «la forma que decide»** la lectura citativa. No
   decide nada: puede ser «subhaṃ + tu + eva». Lo que decide es el sutta 49,
   que nombra «iti» y trae su propio ejemplo. La conclusión era buena y el
   argumento no.
3. **Vigilé un proceso muerto durante varios minutos** con un `pgrep` que
   casaba con el envoltorio del arenal. La comprobación no podía fallar, que
   es la definición de comprobación inútil — briefing 38 §6.3, otra vez.
4. **Glosé de mi cosecha lo que unas voces «son»** —«dveva … cuando es dve +
   eva», «dvevassasahassāyukā, que es dve vassasahassāyukā»— dentro de una
   lista que sí estaba medida. El IEBH lo corrigió: es **«dvi + eva» por §12**.
   El fallo no fue la medida sino el resbalón de «esto es lo que el motor
   propone de más» a «y esto es lo que la voz es», que es adjudicar, y no me
   toca. Y ocurrió el mismo día en que él pidió poner por escrito justamente
   eso. Corregido en `nuestro/operaciones.py` y en §2 de aquí.

## 9. LO QUE SIGUE (en orden)

1. **Trabajar con el Saddanīti**, que es donde se quedó la sesión. El IEBH iba a
   traer los volúmenes de archive.org (5 de 6, en varios formatos): el `.pdf`
   liso y el `_page_numbers.json` de cada uno. Con la Suttamālā buscable en
   bhaddacak y el Smith para cotejar, **lo que se abre es buscar las OTRAS
   reglas que Kaccāyana no tiene**, en vez de esperar a que cada una aparezca
   como un fallo. El buscador de suttas entre obras (`/gramsut`) es la
   herramienta para eso.
2. **El fallo de la segunda voz** (briefing 38 §1 y §9.4): mirar la
   derivación, no el léxico. Sigue sin tirarse, y las ecuaciones nuevas le dan
   más masa. **Es el hilo más prometedor que queda.**
3. **Que la ficha de caso admita varias lecturas con su discriminante** (§3).
   Sin eso, «tveva» y sus hermanas no se pueden registrar bien.
4. **Enseñar al IEBH lo pendiente del briefing 38**: el diagnóstico de su §1
   con sus tres testigos, y la decisión del resguardo de su §3 (313 correctas
   contra 2 malas).
5. **Las escaleras sin derivar**: la auditoría da 16 casos, con los tres del
   briefing 38 §5 entre ellos.
6. **La lista corta de las 69** (briefing 37 §3 quater) por el modo revisión.
7. **El `git add -A` del ciclo** (briefing 38 §7 y §9.8; §4 de aquí).
8. **Conectar el texto corrido del OSBCT** — lo que convertiría el criterio de
   §1 en filtro automático. Es el trabajo grande.
9. Resto del mapa 33. **Sin empezar.**

## 10. PROCEDENCIA — lo que no se puede perder

- **El sutta 49 y su cita se atribuyen al Saddanīti Suttamālā de Aggavaṃsa**,
  cotejado contra la edición de Helmer Smith. En la página se imprime
  «Saddanīti Suttamālā §49» **sin enlace**, porque el sitio no tiene página de
  esa obra: enlazarlo mandaba al lector al §49 de Kaccāyana, que trata de la
  vocal final de «putha». Lo vio IEBH y está arreglado en `b33d0d5`; cuando
  haya página del Saddanīti, el enlace se pone en `refHTML()`.
- **Las tres decisiones sobre «tveva» son del IEBH**, del mismo día, y las
  tres están escritas con su fecha. La retirada de la adjudicación de la
  mañana no fue una corrección de un error suyo: «tu + eva» es correcta para
  «avijjāya tveva», y por eso volvió, bajo la voz unida.
