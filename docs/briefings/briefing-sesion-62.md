# Briefing de la sesión 62 — EL AUDITOR DE DERIVACIONES

**Fecha:** 2026-09-07. Sesión de herramienta: se escribió
`herramientas/auditar_derivaciones.py`, el encargo del §5 del briefing 61, y se
pasó sobre el capítulo 2. De sus avisos salieron seis correcciones; una séptima
la vio IEBH a ojo, y de ella salió una comprobación más en el guion. Publicado:
capítulo 2 en **v1.5** (es) y **v1.2** (en). Además, la portada inglesa dejó de
titularse en español y el nombre del Venerable quedó unificado.

Este briefing supone leído el 61. Lo pendiente de las sesiones 57-58 —tanda 2
del inglés, puntos 17-34 de la revisión del glosario— **sigue sin tocarse**.

---

## 1. EL GUION: `auditar_derivaciones.py`

Equivalente nominal de `auditar_secuencias.py`. Lee las derivaciones paso a
paso de un capítulo —`**Ādiṃ** = ādi + smiṃ (…)`— y hace **seis**
comprobaciones:

| # | Qué mira |
| --- | --- |
| 0 | comillas simples o dobles sin cerrar dentro de un paso |
| 1 | pasos que no citan ningún §N |
| 2 | misma forma y mismos componentes, cadenas distintas |
| 3 | la clase de operación del paso contra la del sutta citado |
| 3 bis | el paso nombra un segmento que no está en la forma |
| 4 | **recomposición**: aplica la cadena y la compara con el lema |

    python3 herramientas/auditar_derivaciones.py                 # capítulo 2
    python3 herramientas/auditar_derivaciones.py --detalle
    python3 herramientas/auditar_derivaciones.py --autoprueba
    python3 herramientas/auditar_derivaciones.py kaccayana/05-....md

**Toma el capítulo como argumento**, pensando en los capítulos 5-8. Medido: el
aparato paso a paso existe hoy sólo en el 2; el 3 y el 4 dan cero derivaciones
y el 1 va por `auditar_secuencias.py`.

### Las decisiones de diseño que hay que conocer antes de tocarlo

- **La comprobación 4 es conservadora a propósito.** Prueba **todas** las
  lecturas posibles de cada operando ambiguo y da la cadena por buena si
  **alguna** reproduce el lema. Así no inventa cuál de dos ‘a’ se elide. Lo que
  marca, por tanto, es que **ninguna** lectura da el lema.
- **La clase de cada sutta se lee de su propia traducción castellana**, en el
  mismo archivo, con el mismo vocabulario que usan los pasos. La palabra que
  costó descubrir es **«deviene»**: es como esta edición dice *ādesa*, y sin
  ella se quedaban sin clasificar tres docenas de suttas. Para §1-§51 se
  importa la tabla revisada a mano de `auditar_secuencias.py`.
- **La comprobación 2 compara lo que la cadena HACE, no cómo está redactada.**
  Quedan fuera la comilla elegida, el verbo («se sustituye por» / «se convierte
  en»), el orden de los pasos, las glosas que no tocan la forma y los pasos
  negados. Sin eso daba 78 avisos, casi todos de redacción; con eso da 31.
- **Un cambio de cantidad —a ↔ ā— vale como alargamiento y como sustitución**,
  porque la edición lo dice de las dos maneras. Sin esa tolerancia la
  comprobación 3 daba 16 avisos; con ella, 4.
- **`--autoprueba` congela ocho casos**, entre ellos la errata de «ādiṃ» tal
  como estaba antes de la sesión 61 (que da *ādaṃ*) y la de «svāgataṃ» de esta
  sesión. Si se toca el simulador, eso dice si sigue cazando lo que ya cazaba.

### Lo que el guion declara que no hace

Los dos límites del guion de sandhi, y uno propio: no decide cuál de varios
suttas correctos es la mejor cita; **no firma nada**; y donde un tipo de paso
no está implementado **lo dice** —bucket «no simulable»— en vez de dejarlo
pasar.

---

## 2. LA COMPROBACIÓN QUE NACIÓ DE UN FALLO DEL GUION

Vale la pena contarlo entero, porque es el método del proyecto en pequeño.

IEBH vio a ojo que **«Svāgataṃ» (§71)** decía `‘a’ de ‘ya’ se elide (§83)`, y
en `su + āgataṃ` no hay ninguna ‘ya’: la ‘u’ se había sustituido por ‘va’. El
‘ya’ es de «agyāgāraṃ», la derivación de la línea de encima, de la que se copió
el paso.

**El guion lo dejaba pasar**, y por una decisión que parecía razonable: cuando
no encontraba el alcance nombrado, buscaba el operando sin él. Así halló la ‘a’
de «āgataṃ», la cadena recomponía, y no decía nada.

La salida está en el propio texto: **la edición distingue con las comillas.**
‘ya’ entre simples es un SEGMENTO y tiene que estar; “aggi” entre dobles es el
TEMA, que puede haberse transformado ya. Antes de fiarse se midió: sobre las
608 derivaciones, un segmento ausente aparece **una vez** —ésta— y ninguna
falsa; los dos temas ausentes son los benignos que se esperaban. De ahí la
comprobación **3 bis**.

**La lección, que es la de siempre:** recomponer es necesario y no suficiente.
Una cadena puede recomponer y aun así no ser la derivación que el texto
enseña.

---

## 3. LAS SIETE CORRECCIONES, TODAS ADJUDICADAS

Todas en `docs/2. Nāma-Kappa.md`, que es la fuente; el inglés, en
`kaccayana/02-nama-kappa.en.md`.

**v1.4 (es) y v1.2 (en).** Tres comillas simples sin cerrar, **sólo en el
español** —«tissā» (§64), «bhuvi» (§78), «sabbassaṃ» (§179)—: el inglés ya las
traía bien, de modo que corregirlas acerca las ediciones y no abre desviación.
Y las tres cadenas de **§66** —«tassā», «yassā», «sabbassā»—, que no mostraban
el paso por el cual ‘sa’ se sustituye por ‘sā’ (§179) y daban *tassa* en vez de
*tassā*. Tres cosas lo respaldaban, todas dentro de la edición: el propio §179
lo dice, sus hermanas «tassaṃ», «yassaṃ» y «sabbassaṃ» ya citaban §179, y
«tissā» (§64) también. Esa omisión sí estaba en las dos ediciones.

**v1.5 (es).** «Svāgataṃ» (§71): la vocal que elide §83 es la de ‘va’, no la de
‘ya’. Sólo español; el inglés ya decía ‘va’, y por eso se queda en v1.2.

Con las siete, la recomposición pasa de 571 a **577 de 608**.

---

## 4. LO QUE QUEDA DEL CAPÍTULO 2: 63 CANDIDATOS

Triados en **`docs/capitulo-2/auditoria-derivaciones.md`**, con el informe
crudo al lado en `.txt`. **Ninguno está firmado.**

| Comprobación | Candidatos |
| --- | ---: |
| 1 · pasos sin §N | 12 (sólo 4 piden cita de veras) |
| 2 · cadenas divergentes | 31 |
| 3 · clase contra el sutta | 4 |
| 4 · la cadena no da el lema | 16 |
| 4 ter · no simulable (declarado) | 5 |

**Por dónde seguir, y era la propuesta al cerrar:** las **seis de §268**
—«guṇiyo», «guṇiṭṭho», «satiyo», «satiṭṭho», «medhiyo», «medhiṭṭho»— son un
mismo patrón, de modo que es una decisión que cubre seis derivaciones. Elidida
«vantu» / «mantu» / «vī» y la vocal del tema, queda todavía la vocal ante ‘si’
→ ‘o’, que ningún paso elide.

Después, las de más señal:

- **«Puthabyā» (§72)** escribe `‘ī’ → ‘ya’` donde **«Matyā»**, del mismo §72,
  escribe `‘y’`. Con ‘y’ recompone; con ‘ya’ no. Las dos no pueden tener razón.
- **«Itthi» (§85)** dice `‘si’ recibe el nombre de ‘gha’ (§57)`. §57 es
  *Ālapane si gasañño*: es **‘ga’**, y las otras dos derivaciones de la misma
  forma lo dicen.
- **«Kva»** cita **§404** para una elisión que en el otro sitio cita §83; §404
  cae fuera del capítulo.
- **«Daṇḍi»** elide ‘ga’ en un sitio y ‘si’ en otro para el mismo paso.
- **«Catassannaṃ»** ×2: insertar ‘ssa’ da *catassanaṃ*, con una sola ‘n’.
- **«Pulliṅgaṃ»**: la sustitución de ‘ṃ’ por ‘l’ ya deja las dos eles, de modo
  que el paso de duplicación parece sobrar.
- **«Bāhussaccaṃ»**: los componentes no incluyen la inflexión, de modo que
  ninguna cadena puede dar el ‘ṃ’ final.

---

## 5. EL SITIO: TÍTULO, ENTRADILLA Y EL NOMBRE DEL VENERABLE

- **La portada inglesa se titulaba en español.** El `h1` era una cadena fija y
  no pasaba por `bi()`, de modo que el botón de idioma no lo cambiaba: la
  edición inglesa se encabezaba «Gramáticas Pāḷi en español». Ahora dice
  **«Pāḷi Grammars in English»**, y con él el título de la pestaña en las tres
  páginas de índice, que decía «in Spanish».
- **La entradilla inglesa** dice ya «English translations of the classical Pāḷi
  grammars…». El español no cambia.
- **El nombre queda «Bhikkhu Nandisena»**, sin «U» y sin «(ITBMU)», en los seis
  sitios en que llega al lector y en las cuatro fuentes normativas
  (`comun/convenciones.md`, `comun/guia-de-estilo.md` ×3,
  `comun/concordancia.json`, `recursos/sandhi/suttavibhaga.json`). El copyright
  español ya lo decía así; el inglés era el que iba suelto.
  **No se toca** «Kaccāyana 2 - Nāma-Kappa (U Nandisena).md» en
  `restituir_citas.py`, que es el nombre de un archivo; ni los briefings ni las
  notas de Zenodo, que son registro de lo publicado.
- **La `<meta name="description">`** tiene ya versión inglesa, que el botón
  pone junto con el título. **Con un límite que conviene saber:** las tres
  páginas de índice son **una sola URL** con las dos lenguas dentro, de modo
  que lo que se sirve en el HTML —y lo que ven los rastreadores y las vistas
  previas de los enlaces, que no ejecutan JavaScript— es el español. El cambio
  arregla lo que ve el lector en el navegador, no lo que indexa un buscador. Es
  exactamente la misma limitación que ya tenía el `<title>`.

---

## 6. UNA TRAMPA NUEVA, HERMANA DE LA DE LA SESIÓN 61

**`generar_todo.py` NO ejecuta los `convertir_*.py`.** Sólo lo hace el hook de
pre-commit. De modo que, entre editar un maestro de `docs/` y hacer el commit,
`kaccayana/02-nama-kappa.md` puede enseñar texto viejo aunque se haya
regenerado el sitio entero. El orden seguro cuando se quiere ver el resultado
antes de commit es:

    python3 herramientas/convertir_nama.py
    python3 herramientas/generar_todo.py

No es un error del hook —al hacer el commit todo cuadra—, pero sí engaña al
comprobar a mano, que es justo lo que costó dos commits en la sesión 61.

---

## 7. OTRO AVISO DE OFICIO: EL CANDADO DE GIT

Durante la sesión, un `git status` lanzado desde el entorno de Claude dejó un
`.git/index.lock` de cero bytes que ese entorno no pudo borrar, y los dos
commits siguientes fallaron con «Another git process seems to be running». Se
resolvió con `rm -f .git/index.lock`.

**A partir de aquí, Claude no lanza `git` en este repositorio**: prepara los
cambios y entrega los comandos para que los ejecute Angel.

---

## 8. ESTADO

Al cerrar la sesión quedaban **tres commits preparados y sin hacer** en el
árbol de trabajo, cada uno con su mensaje redactado, sobre archivos distintos:

1. «Nāma-kappa v1.5 (es): «svāgataṃ» elide la ‘a’ de ‘va’, no la de ‘ya’» —
   `auditar_derivaciones.py`, `docs/2. Nāma-Kappa.md`, su salida convertida,
   `generar_capitulo.py`, `docs/capitulo-2/`, `site/`.
2. «La portada inglesa se titula «Pāḷi Grammars in English»» —
   `generar_indices.py`, `generar_capitulo.py`, `site/`.
3. «La cita de la edición base dice «Bhikkhu Nandisena»» — `comun/` (tres
   archivos), `recursos/sandhi/suttavibhaga.json`, `site/`.

**Lo primero que debe hacer el chat nuevo es comprobar si se hicieron**
(`git log --oneline -6`) antes de suponer nada.

Ya en `main` de esta sesión: `0fcc8c4` (el auditor) y `11dbeb6` (v1.4 / v1.2).
