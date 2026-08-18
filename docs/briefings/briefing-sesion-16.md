# Kaccāyana Pāḷi-Español: Briefing de la Sesión 16

*Complementa a los briefings 05–15. La sesión 16 no tocó traducción: publicó
un recurso nuevo, arregló el modo oscuro de los índices, los pasó a
generarse solos, y dejó abierto el trabajo de los paradigmas de declinación.*

---

## 1. ESTADO AL CIERRE DE LA SESIÓN 16

Todo lo de las secciones 2–5 está **hecho, regenerado y verificado**. Lo de
la sección 6 está **empezado**: existe el índice, faltan los 82 documentos.

Al cerrar quedaban sin commitear los cambios de las secciones 2–5 (Claude no
puede escribir en `.git` desde la sesión). Los cuatro borradores de
`docs/borradores/` siguen sin rastrear y **no** deben entrar en el commit.

## 2. RECURSO NUEVO: `/recursos/nombre/` (formación del nombre · pācako)

Angel trajo un HTML suyo con la derivación de *pācako* en diez pasos. Se
adaptó a las convenciones del sitio y se publicó.

- Fuente: `recursos/nombre/plantilla.html`; generador
  `herramientas/generar_nombre.py` → `site/recursos/nombre/index.html`.
- **Las referencias §N se derivan del markdown, no se copian.**
  `generar_nombre.py` construye el mapa §N → capítulo leyendo los `.md`
  publicados, de modo que §457, §521, §527, §621 y §622 (Kibbidhāna y
  Uṇādi) se enlazarán solas el día que se publiquen esos capítulos. Hoy
  salen como `.xref-pend`, en gris y con `title`.
- Las siete que sí existen se comprobaron una a una contra el maestro:
  §53 *Liṅgañ ca nippajjate*, §54 *Tato ca vibhattiyo*, §56
  *Tadanuparodhena*, §83 *Saralopo…*, §104 *S' o*, y §11 *Naye paraṃ
  yutte* del Sandhi-kappa, que reúne consonante y vocal en el último paso.
- La derivación **cruza tres capítulos** (Kibbidhāna → Nāma → Sandhi). El
  pie de la página lo explica; conviene no describirla como «material del
  capítulo 2» a secas.
- El conmutador de tema escribe en `pali_dark`, la clave compartida, así
  que el modo oscuro viaja entre esta página, sandhi y los capítulos.

## 3. LICENCIA IEBH

Bloque `.licencia` al pie de `/recursos/sandhi/` y `/recursos/nombre/`:
«Preparado por Bhikkhu Nandisena · … · CC BY-NC-SA 4.0». Angel confirmó que
la autoría de la derivación de *pācako* es de Nandisena.

**Ortografía fijada: «Instituto de Estudios Buddhistas Hispano»**, con dos
d. Se corrigió en `README.md`, `site/index.html` (×2) y
`site/kaccayana/index.html`. No queda ninguna «Budistas» en el repositorio.

## 4. BOTÓN «↑» EN SANDHI

`/recursos/sandhi/` tiene ya el botón flotante de volver al inicio, igual
que los capítulos: `#top-btn`, abajo a la derecha, aparece pasados 600 px,
respeta `prefers-reduced-motion` y se oculta al imprimir. No choca con
`#volver`, que va abajo a la izquierda. Editado en
`recursos/sandhi/plantilla.html`, **nunca** en `site/`.

## 5. EL MODO OSCURO DE LOS ÍNDICES, Y LOS ÍNDICES GENERADOS

### El defecto

En los capítulos el fondo lo pone `#main`. Las páginas de índice usan
`.idx` y no tienen `#main`, y **`body` no recibía ni fondo ni color**. En
modo oscuro la página se quedaba blanca mientras `--text` pasaba a casi
blanco: el titular era ilegible. Arreglado con una regla `body { background:
var(--bg); color: var(--text) }` en `site/assets/pali.css`.

El script del tema pasa además **justo detrás de `<body>`**, para que la
clase esté puesta antes de pintar y no haya fogonazo blanco al cargar.

Contraste medido tras el arreglo: todo AA o AA-grande en oscuro. Los dos
valores flojos que quedan son de **modo claro** y son previos —
`.idx-card.pend` lleva además `opacity:.55`—. Angel no pidió tocarlos.

### `herramientas/generar_indices.py` (nuevo)

Genera las tres portadas: `site/index.html`, `site/kaccayana/index.html` y
`site/recursos/index.html`. **Los recuentos se cuentan del markdown**, con
lo que se corrigieron dos cifras rezagadas: «1 de 8 capítulos» → **3 de 8**,
y la insignia de sandhi de 261 → **266 formas**.

Publicar un capítulo ya no exige tocar el índice a mano: basta añadirlo a
`CAPITULOS` en `generar_capitulo.py` y dejar su `.md`. **El paso 5 de la
lista «Capítulo nuevo» de `CLAUDE.md` está obsoleto** y conviene reescribirlo.

Lo único que sigue a mano es el diccionario `DETALLE` del generador, con el
rango de suttas y las kaṇḍas de cada capítulo publicado; si falta, avisa.

### Retirada de `/recursos/combinacion-eufonica/`

La referencia interactiva de sandhi lo reemplaza. Decisión de Angel:
**despublicar la página, conservar el markdown**. `recursos/combinacion-eufonica.md`
sigue donde estaba porque `reconstruir_sandhi.py` lo lee para rehacer
`reglas.json`; se excluye de la generación mediante `SIN_PUBLICAR` en
`generar_todo.py`. El pie de sandhi nombra ahora el documento como fuente
**en texto plano, sin enlace**, para no dejar un 404 ni perder la atribución.

### Sección «Corpus»

`/recursos/` tiene una sección aparte con el Chaṭṭhasaṅgītipiṭaka
(<https://buddha-dhamma.net/>), marcado como externo — borde discontinuo,
flecha `↗`, `target="_blank" rel="noopener"` — para que «Disponible» siga
significando material del IEBH alojado aquí.

## 6. LOS PARADIGMAS DE DECLINACIÓN — TRABAJO ABIERTO

### El hallazgo que lo desbloquea

Los paradigmas son **83 Google Docs públicos**, uno por paradigma, más un
índice. No hace falta conectar Google Drive: **la URL de exportación
funciona y conserva las tablas**.

    https://docs.google.com/document/d/{ID}/export?format=html

Se probó con `purisa` (regular) y con `rāja` (tema consonántico irregular,
cuatro variantes en una celda) y **el grid sale intacto**: diacríticos
correctos, variantes separadas por coma, ocho filas de inflexión.

Los enlaces del índice tienen dos formas —`docs.google.com/document/d/{ID}`
y `drive.google.com/open?id={ID}`— pero **el ID es el mismo**, así que
ambas se convierten a la URL de exportación sin más.

Sobre conectar Drive, por si vuelve a plantearse: **Google no permite
limitar el OAuth a una carpeta**. El conector pide `drive.readonly`, que ve
toda la unidad de la cuenta conectada. Si algún día hiciera falta, la forma
de acotarlo es compartir la carpeta a una cuenta secundaria y conectar ésa,
no la de `admin@iebh.org`.

### Lo que ya existe

`recursos/paradigmas/indice.json` — 84 entradas (83 paradigmas + el
documento *Sufijos-Inflexiones*), 83 documentos únicos: `M-O1` y `F-O`
comparten el de *go*. Cada entrada lleva `codigo`, `paradigma`, `doc` y
`genero`. Reparto: 27 masculinos, 11 femeninos, 10 neutros, 27 pronombres
(9 × M/F/N), 6 pronombres sin género, 2 numerales, 1 de sufijos.

### La estructura de cada documento

Constante en los dos comprobados:

| M-A1—PURISA (hombre) | | |
| --- | --- | --- |
| inflexión | singular | plural |
| primera (paṭhamā) | puriso | purisā |
| vocativo (ālapana) | bho purisa, purisā | bhavanto purisā |
| … | … | … |

Ocho filas —primera, vocativo, segunda … séptima—, y al pie una nota que
mapea inflexión → caso (primera = nominativo, etc.), idéntica en todos.

**La terminología ya casa con el repositorio**: nombra las inflexiones por
ordinal con el pāḷi al lado, no por caso latino, igual que `CLAUDE.md`
(«inflexión», no «inflexión nominal») y que el último paso de la página de
*pācako*, «Primera inflexión, masculino singular».

### Lo que falta

1. **Traer los 82 documentos restantes** (ya están *purisa* y *rāja*).
   Sólo con `mcp__workspace__web_fetch`; las reglas de la herramienta
   prohíben descargar con curl o python.
2. Volcarlos a `recursos/paradigmas/paradigmas.json`, con las variantes de
   cada celda **como lista, no como cadena separada por comas**.
3. **Lo que Angel pidió al cierre: tablas muy cuidadas y un índice o tabla
   de contenidos para navegarlas.** El modelo natural es
   `/recursos/sandhi/`: barra fija, buscador que ignora diacríticos,
   filtros por género y por tema, y `#top-btn`. Página en
   `recursos/paradigmas/plantilla.html` + `herramientas/generar_paradigmas.py`,
   enganchado a `generar_todo.py` y con tarjeta en `/recursos/`.
4. Verificar: 8 inflexiones por paradigma, ninguna celda vacía, diacríticos
   intactos, y cotejo a mano de dos o tres contra el documento original.

### Lo que sería el paso siguiente, no pedido todavía

Ligar cada desinencia al sutta del Nāma-Kappa que la prescribe, con el
mismo principio que salvó las secuencias de sandhi: **proponer y
verificar** — derivar la forma del tema más el sutta, y conservarla sólo si
reproduce exactamente lo que dice el paradigma. Lo que no cuadre se marca,
no se publica. Serviría además para detectar erratas en los documentos.

## 7. RECORDATORIOS QUE NO CAMBIAN

- **Nunca se edita nada dentro de `site/`** salvo las tres portadas, que
  ahora las escribe `generar_indices.py`; lo que se edita está en
  `kaccayana/`, `recursos/` y `comun/`.
- El hook de pre-commit regenera y añade; si falla, detiene el commit.
- Lo tomado de Thitzana se señala como suyo, y su flecha va al revés.
- Ante duda, `<!-- DUDA: … -->`, y decirlo en voz alta en lugar de suponer.
