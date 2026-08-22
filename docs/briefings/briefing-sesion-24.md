# Kaccāyana Pāḷi-Español: Briefing de la Sesión 24

*Complementa a los briefings 05–23. Un solo hilo, el que la 23 dejó a medias:
**la negrita del vutti**. Se cerró casi entero. No se tradujo ni un sutta
nuevo; no se tocó el capítulo 4.*

> **Lo primero que tiene que saber el chat nuevo:** los lemas del Nāma sin
> negrita pasaron de **26 a 2**, y el Kāraka está completo (5 de 5). Lo que
> queda son dos casos concretos —§70 y §92—, cada uno con su camino ya medido
> y ninguno pendiente de trabajo a ciegas.

---

## 1. ESTADO AL CIERRE

HEAD: **`b841dbd`**, publicado en `origin/main`, **árbol limpio**. Comprobado
**sin ejecutar git**, leyendo `.git/refs/heads/main`, `.git/logs/HEAD` y
`.git/refs/remotes/origin/main` como texto plano.

| Hash | Qué |
| ---- | --- |
| `b426955` | negrita: repetida no es ambigua cuando las cuentas cuadran; §66 |
| `08b061f` | división: «Xsv ti» es una «i» perdida; enmienda del briefing 23 |
| `b841dbd` | **negrita: lo que la capa de texto del PDF pierde, en tabla cerrada** ← HEAD |

Los tres commits de las sesiones 23-24 están publicados y el sitio desplegado.
No queda nada por confirmar.

*(Este apartado se escribió primero dando `08b061f` y una lista de archivos sin
confirmar, porque Angel se fue a mediodía y yo no ejecuto git. A su vuelta los
confirmó y los publicó. Se corrige aquí mismo antes de cerrar — que es justo el
fallo que la sesión 23 cometió y que el §8 de abajo manda no repetir.)*

## 2. LA UNIFICACIÓN `Xsv ti` → `Xsv iti` (mañana)

Decisión de Angel, §6.1 de la 23. **Eran doce, no trece**: §222 ya lo había
arreglado `b426955`. Ver la enmienda del briefing 23 para el detalle; lo que
importa aquí es que **desbloqueó siete lemas** por la tarde.

## 3. LA NEGRITA, CON EL PDF DELANTE

Angel subió los PDF del Nāma y del Kāraka. **El Kāraka estaba ya completo**: 0
tramos nuevos, 74 ya puestos, y sus 15 ausentes son compuestos con guion
partidos por el salto de línea físico, nada recuperable. Sirvió toda la tarde
de **control de no-regresión**, y ganó su sueldo: ver §4.

El Nāma fue de **1794 a 1831** tramos en negrita, y de **26 lemas sin negrita a
2**. Cuatro pasos, cada uno cotejado a mano antes de aplicarse:

| | tramos | lemas sin negrita |
| --- | ---: | ---: |
| al abrir la sesión | 1794 | 26 |
| tras la unificación `Xsv iti` | 1801 | 19 |
| tras `VARIANTES` | 1817 | 15 |
| tras bajar `MINIMO` | 1827 | 6 |
| tras arreglar el reconocimiento de citas | 1829 | 4 |
| tras `RE_DEFECTO` | **1831** | **2** |

Una segunda pasada coloca **0**: la operación es idempotente.

### 3.1 `VARIANTES`: lo que la capa de texto pierde

Nueve líneas no encontraban sitio por **un solo carácter**, siempre un
diacrítico que `pdftohtml` no devuelve —`a` por `ā`, `m` por `ṃ`, `n` por `ñ`—.
No son variantes de lectura ni erratas de Nandisena: **el PDF imprime el
diacrítico**, lo que falla es extraerlo. Así que no se corrige nada: se le
enseña al emparejador, como `VARIANTES` en `restituir_citas.py`.

**Es tabla cerrada, no tolerancia.** Ocho entradas para nueve líneas —
`kimattham` → `kimatthaṃ` cubre §76 y §194 a la vez—. Dos condiciones hacen
segura cada una: la forma de la izquierda **no existe en el maestro** (que
escribe `kimatthaṃ` 198 veces y `kimattham` ninguna), y **conserva la
longitud**, porque las marcas de negrita son índices sobre la cadena
normalizada. Un `assert` lo garantiza para quien añada entradas.

Se descartó la alternativa —plegar los diacríticos y aceptar el ancla si el
resultado es único— y conviene saber por qué, porque es el argumento central de
toda la tarde: **en pāḷi la cantidad vocálica significa, y la comprobación de
reconstrucción no detectaría una negrita bien puesta sobre la letra
equivocada.** Sólo demuestra que al quitar el marcado vuelve el maestro
intacto. Por eso cada tramo nuevo se miró con los ojos antes de aplicar.

### 3.2 §190, que parece errata nuestra y no lo es

Es la única de las nueve donde el diacrítico está en el PDF y falta en el
maestro: `evamādīto` frente a `evamādito`. Leído sin más parecería una pérdida
de transcripción por nuestra parte. **No lo es: el propio PDF imprime
`evamādito` cuatro veces y `evamādīto` una**, justo ahí. El maestro sigue a la
mayoría y se queda como está. Singleton de la edición base, de la clase de
`brāhamaṇā` (sesión 23). Decisión de Angel: a `VARIANTES`, sin tocar el pāḷi.

### 3.3 `MINIMO`: un suelo que ya no defendía nada

El suelo de 24 caracteres es de cuando la única regla era «aparece una sola
vez»: entonces una línea corta sí era peligrosa. Se midieron sus 17 capturas en
el Nāma:

| | |
| ---: | --- |
| 10 | únicas en el PDF y en el maestro (1=1) → **legítimas, rechazadas** |
| 6 | ausentes de todos modos (rótulos, inglés, restos de nota) |
| 1 | `honti **aṃ**mhi vibhattimhi` — 2 en el maestro, 1 en el PDF |

La única peligrosa **no la para el suelo: la para la regla de las cuentas** de
la sesión 23. El suelo sólo estaba rechazando lemas cuyo ejemplo es corto
—`**Vā** ti kimatthaṃ? Aggi.`, 19 caracteres—. Bajado a **16**; se conserva un
suelo porque por debajo quedan rótulos y restos de numeración.

### 3.4 Dos errores de verdad en el reconocimiento de citas

`RE_SALTABLE` descarta las citas canónicas antes de comparar. Fallaba en dos
sitios, y ambos son bugs, no criterio:

1. **El orden de las siglas.** La alternación de `re` se queda con la primera
   que case, y `Vin` estaba **antes** que `VinA`: se comía las tres primeras
   letras y dejaba una `A` suelta. `VinA` y `AbhiA` no se reconocían nunca.
   Reordenadas de más larga a más corta.
2. **`( D. ii, 6)`**, con un espacio tras el paréntesis (§93). El patrón exigía
   la sigla pegada, así que la cita se quedaba dentro del ancla y la línea no
   encontraba sitio. Ahora `\(\s*`.

De paso faltaban dos siglas: **`AbhiA`** (sale en el PDF, §94) y **`Rū`** (sale
en los maestros).

### 3.5 `RE_DEFECTO`: dos averías que cambian la longitud

No caben en `VARIANTES`, que necesita conservarla. Se reparan sobre la línea
cruda, antes de normalizar:

    PDF                    maestro              qué pasó
    **Etevī** ti           Etesv iti            's' salió como 'v'
    **Tumha-mhākam** iti   Tumha-amhākaṃ iti    se perdió la 'a' y la 'ṃ'

Cerrada y cotejada igual que `VARIANTES`: las dos formas salen **una vez en el
PDF** y **ninguna en el maestro**. Y el PDF escribe `Etesvī` bien otras cinco
veces, que es lo que confirma que `Etevī` es esa palabra estropeada.

## 4. LO QUE SE MIDIÓ Y NO SE HIZO

### 4.1 Descartar la puntuación: **lo rechazó la herramienta**

`restituir_citas.normalizar` descarta la puntuación desde la sesión 23;
`restituir_negritas.normalizar` no. Igualarlas parecía obvio y habría resuelto
§70. Se probó: **en el Nāma coloca 1 tramo más, y en el Kāraka la
reconstrucción FALLA.**

Es la lección del día y por eso está escrita aquí: **el control del Kāraka es
lo que la cazó.** Una prueba sobre un solo capítulo la habría dado por buena.
Cualquier cambio del emparejador se corre contra los dos.

### 4.2 Colocar de más larga a más corta: propuesta con números

§92 no es ambigüedad, es **contención**: la línea de §92 es un prefijo de la de
§127, de modo que el ancla corta casa dentro de las dos.

    **Etesv** iti kimatthaṃ? Guṇavā. Satimā (M. i, 70).   len=32  hits=1   → §127
    **Etesv** iti kimatthaṃ? Guṇavā.                      len=25  hits=2

Colocando de más larga a más corta y descontando las regiones ya reclamadas,
la corta queda con un solo sitio. Prototipado y medido en el Nāma:

| | ahora | longest-first |
| --- | ---: | ---: |
| colocadas | 443 | **452** |
| ambiguas | 18 | **11** |
| ausentes | 32 | 38 |

**No se ha implementado.** Es un cambio estructural del emparejador, no un
arreglo puntual: gana nueve y crea seis ausentes nuevas, y las nueve habría que
cotejarlas una a una. Angel estaba fuera y esto pide su visto bueno. El
prototipo no tocó el código.

## 5. LOS DOS QUE QUEDAN

- **§70 `Vā`** — el maestro imprime `Pañcah’ aṅgehi (Vin. v, 343), tīhākārehi`
  y el PDF `… (Vin. v, 343) tīhākārehi`: **sobra una coma**. La vía obvia es
  §4.1, que rompe el Kāraka. Alternativa por explorar: descartar la puntuación
  **sólo del lado del PDF**, como se hace con `VARIANTES`.
- **§92 `Etesv`** — es §4.2. Se resuelve con longest-first y con nada más.

## 6. CORRECCIONES AL BRIEFING 23

El 23 se escribió **antes del último commit de su sesión** y quedó desfasado.
Está enmendado en el archivo, con los párrafos reescritos y no borrados. Lo
sustancial: §66 sí se resolvió, el reparo de ambigüedad se levantó, el guion de
`Saṃsāsv` está cerrado, y eran doce divisiones, no trece.

**Y una corrección más, de esta tarde:** el punto 6 de su §6 dice que
`generar_todo.py` no llama a los conversores y que hay que correrlos a mano.
Cierto de `generar_todo.py`, pero **el hook de pre-commit sí los llama** —
recorre `herramientas/convertir_*.py` y aborta el commit si un maestro y su
archivo generado no cuadran—, y lo hace desde el 17 de agosto. En la práctica
un commit normal basta. Se deja dicho para que nadie persiga un fallo que no
existe.

## 7. LO QUE SIGUE ABIERTO

1. **§4.2, longest-first** — decisión de Angel, medida y lista.
2. **§70**, la coma.
3. **32 ausentes y 18 ambiguas** en el Nāma que no son lemas `kimatthaṃ`. Tres
   de las ausentes son prosa inglesa y **deben** seguir ausentes. Quince son
   líneas que el PDF corta a mitad y cuyo prefijo casa de forma única: es la
   otra vía que queda, y pide decidir qué hacer con la negrita que cae más allá
   del corte.
4. **Tres citas canónicas** siguen pendientes (§6.5 de la 23): §81 y §308
   explicadas; **§315 ya está puesta dentro de la nota 30 y se puede cerrar sin
   más**.
5. **Las 2379 desinencias** de `recursos/paradigmas/paradigmas.json`. Candidato
   a sesión entera.
6. El escaneo del Nyāsa; `docs/fuentes/nyasa/` sin constar en `CLAUDE.md`;
   `pañcamī / sattamī` sin llegar al glosario.
7. Los diecisiete apartados de Thitzana; las seis decisiones del §1.4 de
   `docs/notas-de-trabajo-nama.md`; la zona gris de `Nyasa_errata.md` §3.
8. **§10.1 de los briefings 04–05: las referencias bibliográficas del Nāma
   nunca se restituyeron.** Está en `docs/notas-de-trabajo-nama.md` §1.2, con
   la tabla de §204–§270 entera. No se tocó hoy.
9. **El permiso de la marca (briefing 19 §8): sigue sin respuesta.**
10. **El siguiente capítulo a traducir: sin decidir.** Se preguntó por la
    mañana y quedó sin contestar. Es lo único de esta lista que decide para
    qué sirve una sesión, en vez de qué se limpia.
11. `docs/1. Sandhi-Kappa.md`, archivo muerto que diverge; la descripción de
    Zenodo; URL más corta; `recursos/nombre/`.

## 8. RECORDATORIOS QUE NO CAMBIAN

- **Ninguna orden de git desde el sandbox, ni siquiera `status`.** Leer
  `.git/refs/heads/main`, `.git/logs/HEAD` y `.git/index` como archivos.
- **Con Angel se habla en inglés**; el producto —sitio, mensajes de commit,
  comentarios del código, estos briefings— va en español. Una respuesta en el
  chat va en inglés **entera**, también los bloques que se le pasen para
  copiar. En la 24 se le entregó en español el texto para el chat siguiente:
  eso incumple la regla aunque el resto de la respuesta esté en inglés.
- **Nada de verbos ingleses conjugados en español.** «Commitear», «empujado»,
  «pushear», «mergear», «testear». La tabla y el porqué están ahora en
  `comun/convenciones.md` §0, que es donde tenían que haber estado desde el
  principio. **Cuidado con los briefings 10 a 22**: los catorce calcos que
  siguen ahí no son estilo de la casa, son el error que se venía copiando de
  sesión en sesión. No imitarlos.
- **Los PDF no viven en el repositorio** (`.gitignore`: `*.pdf`). Sin ellos no
  se puede repetir la restitución de negritas. Hay que pedírselos a Angel.
- **Todo cambio del emparejador se corre contra los dos capítulos.** Ver §4.1.
- **`reconstrucción: OK` no dice que la negrita esté bien puesta**, sólo que no
  se ha estropeado el texto. Lo primero se comprueba con los ojos.
- Los maestros de los capítulos 2 y 3 están en `docs/`; el Sandhi es la
  excepción, su fuente viva es `kaccayana/01-sandhi-kappa.md`.
- Nada se edita dentro de `site/` salvo `pali.css`, `pali.js` y los SVG.
- Lo tomado de Thitzana se señala como suyo; su flecha va al revés.
- Ante duda, `<!-- DUDA: … -->` y decirlo en voz alta.
- **Proponer y verificar, nunca afirmar.**
- **El briefing se escribe cuando ya no se va a tocar nada más**, no antes del
  último commit. Lo primero que hace un chat nuevo es comprobar `HEAD` contra
  el briefing; si no coinciden, manda el árbol.
