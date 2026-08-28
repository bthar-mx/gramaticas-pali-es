# Kaccāyana Pāḷi-Español: Briefing de la Sesión 30

*Complementa a los briefings 05–29. Tema único: **el solucionador de
sandhis** — la incorporación de la entrega de Miguel De Anquín, el paso al
léxico del canon sin DPD, y el encargo que abre la sesión 31: **portar el
motor a JavaScript** para publicarlo en el sitio.*

> **Lo primero que tiene que saber el chat nuevo:** el solucionador está
> **incorporado, medido y funcionando en local** (`python3
> nuestro/pantalla.py` → `http://127.0.0.1:8731/`). Todo está confirmado en
> commits; **falta el `git push`, que hace Angel desde su Mac** (la caja de
> Claude no tiene llave SSH). El trabajo de la sesión 31 es la **etapa 1 del
> porte a JS** (§6). Antes de tocar nada: leer este briefing entero,
> `docs/solucionador/PROCEDENCIA.md` y `docs/solucionador/INFORME-AL-VENERABLE.md`.

---

## 1. ESTADO AL CIERRE

Siete commits de esta sesión, en orden:

| Commit | Qué |
| --- | --- |
| `f62c526` | CLAUDE.md: precisa el criterio de idioma |
| `925183b` | **Incorpora el solucionador** — entrega de Miguel De Anquín (24-08) |
| `4b210d5` | PROCEDENCIA: el autor de la entrega es Miguel De Anquín |
| `670f88c` | **El canon como léxico, sin DPD**: generador, `--solo-canon`, medición |
| `6f59d54` | Las comillas de cita no son parte de la voz; mensajes con su léxico |

Árbol limpio. **Pendiente de push por Angel.** Dos bloqueos de git
(`index.lock`, `HEAD.lock`) se limpiaron con el permiso de borrado de la
carpeta; si reaparecen, es el mismo caso.

## 2. QUÉ ES CADA COSA (mapa mínimo)

- `nuestro/` — el motor de Miguel: `solucionar_sandhis.py` (entregable 1),
  `pantalla.py` (entregable 2, la pantalla local), `operaciones.py` (una
  función por aforismo, con su enunciado arriba), `normalizar.py`
  (`cotejo()`), mediciones y utilidades. `herramientas/derivar_secuencias.py`
  es el verificador y **ya era nuestro** (llegó idéntico).
- `recursos/sandhi/reglas.json` — el banco: 266 formas con secuencia.
  **Idéntico byte por byte** entre su entrega y el repositorio. Fuente, no
  salida: nunca regenerarlo.
- `recursos/corpus/corpus-formas.json` — **el léxico del canon**: 681.927
  formas de los 118 volúmenes convertidos del OSBCT (canon + aṭṭhakathā +
  ṭīkā), generado por `herramientas/generar_corpus_formas.py`. Sustituye al
  DPD por decisión del Venerable.
- `recursos/corpus/therigatha*.json` — el banco de pruebas de Miguel
  (Therīgāthā y su comentario, particionados por su proyecto anterior CON el
  DPD: **la referencia está teñida de DPD**, tenerlo presente al leer los
  desacuerdos).
- `banco.sha256` — huellas congeladas de todo lo que el motor lee.
  `python3 nuestro/congelar.py` comprueba; `--escribir` recongela.
- `docs/solucionador/` — PROCEDENCIA.md (quién hizo qué),
  INFORME-AL-VENERABLE.md (las **8 consultas** que esperan el fallo de
  Angel), LEEME.txt.

## 3. LAS DECISIONES DEL VENERABLE EN ESTA SESIÓN

1. **El DPD se deja de lado.** La autoridad es Kaccāyana y el texto de la
   edición. El léxico es el corpus convertido del OSBCT. El modo es
   `--solo-canon` (aún no es el default — cambiarlo es decisión pendiente,
   ofrecida y no respondida).
2. **El alcance es el Canon entero con Comentarios y Subcomentarios.** El
   léxico ya lo cumple (118 volúmenes). Lo que sigue siendo Therīgāthā-only
   es el banco de pruebas; ampliarlo es trabajo futuro, no de la etapa 1.
3. **Las comillas de cita se ignoran**: «oghamatarī”ti» = «oghamatarīti».
   Hecho en `cotejo()` (commit `6f59d54`).
4. **La interfaz pública será mínima**: 1 caja donde pegar el pasaje pāḷi;
   2 salida con el número de sandhis, las voces con sandhi, y en cada una un
   desplegable con la secuencia §N de Kaccāyana **exactamente como la
   muestra `/recursos/sandhi/`**. Nada más. La pantalla de Miguel es banco
   de trabajo, no la página del sitio.
5. **Honestidad sobre la precisión**: se publica con su cifra de cobertura a
   la vista; mejora con los fallos que reporten los lectores, cada fallo un
   caso de prueba permanente.

## 4. LOS NÚMEROS (la puerta de aceptación)

| medida | con DPD | solo canon |
| --- | ---: | ---: |
| banco (251 medibles de 266) | 221 (88 %) | 218 (87 %) |
| Therīgāthā (698) | 630 (90,3 %) | 551 (78,9 %) |
| su comentario (7.178) | 6.496 (90,5 %) | 6.048 (84,3 %) |

Se reproducen con `--cobertura`, `nuestro/medir_contra_corpus.py` y
`--comentario`, con y sin `--solo-canon`. **Cualquier cambio al motor debe
dejar estos números iguales o mejores, y toda mejora se mide antes y
después.** La caída del corpus en solo-canon está teñida (§2): cuánto es
error real sólo lo dirá leer los desacuerdos contra la página impresa —
muestreo ofrecido a Angel, sin respuesta aún.

## 5. ERRATAS Y CABOS SUELTOS

- **«cakkhudnriyaṃ», una vez en `22AbhiT01`** (OSBCT): licencia una lectura
  falsa por §51. Cotejar contra la página impresa — errata del impreso o
  defecto de conversión. Es asunto del OSBCT, no de este repo.
- Las **8 consultas** del INFORME esperan el fallo de Angel (byañjana 3.1,
  cinco formas de interdicción, erratas del PDF, la privativa `na`…).
- `medir_deteccion.py` importa un módulo `grupos_iniciales` que la entrega
  no trajo (defecto registrado en PROCEDENCIA; no afecta a nada de arriba).
- `fuentes-derivadas/concordancia-nandisena-51.json` viene de `sandhi-6.html`
  v1.0 (08-10); la página viva es v3.8. **No es fuente del motor** hasta que
  Angel falle las diferencias.
- El modo párrafo detecta menos sin `dpd-descomposiciones.tsv` (77 MB, no
  vino) — pero con el DPD apartado, la detección en párrafo debe rediseñarse
  sobre el canon (etapa 3 del porte, no de la etapa 1).

## 6. EL ENCARGO DE LA SESIÓN 31: PORTE A JS, ETAPA 1

Objetivo final: `/recursos/solucionador/` en el sitio, todo en el navegador,
sin servidor, con la interfaz del §3.4. Etapas con puerta:

1. **Portar el núcleo** — `cotejo()`, las ~35 operaciones de
   `operaciones.py`, el bucle proponer-verificar de `solucionar_sandhis.py`
   y la lógica del verificador. **Puerta: un arnés en Node reproduce 218 de
   251 contra el banco en modo solo-canon, secuencia por secuencia idéntica
   al Python.** El Python queda como referencia permanente; todo cambio del
   JS se mide contra él.
2. **Segmentación con léxico fragmentado** — las 681.927 formas del canon
   partidas por letras iniciales como `names.json`, carga bajo demanda.
   Puerta: reproduce 551/698 y 6.048/7.178.
3. **Detección en párrafo sobre el canon** (rediseño sin DPD) y ampliación
   del banco de pruebas más allá de la Therīgāthā.
4. **La página** — `plantilla` + generador como los demás recursos,
   `pali.css`, `i18n.js` para el cromo, el pāḷi nunca se traduce.
   Puerta: la página publicada da secuencias byte-idénticas al Python en las
   266 del banco.
5. **Publicar** con la cobertura declarada en la propia página.

Reglas que ya costaron caro: proponer y verificar, nunca afirmar; todas las
lecturas, no una; los tres silencios se dicen distinto; nada se incorpora de
Thitzana sin señalarlo como suyo; las secuencias citan §N de Kaccāyana y el
léxico jamás aparece como autoridad en la salida.

## 7. LO QUE NO SE HIZO

- El push (Angel, desde su Mac).
- El default `--solo-canon` (decisión de Angel pendiente).
- La muestra de desacuerdos para adjudicar contra la página impresa.
- Todo el porte a JS (§6).
- La ampliación del banco de pruebas al canon entero.
