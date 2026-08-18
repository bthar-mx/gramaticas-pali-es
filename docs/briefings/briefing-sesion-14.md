# Kaccāyana Pāḷi-Español: Briefing de la Sesión 14 — PUBLICACIÓN DEL CAPÍTULO 3

*Complementa a los briefings 05–13. Este briefing abre el chat de
**publicación del capítulo 3 (Kāraka-Kappa)**. La revisión del capítulo 4
(Samāsa) es un hilo PARALELO con su propio briefing (el 13): este chat **no
toca** los archivos del capítulo 4 (`sesion-13-*`, `capitulo-04-*`).*

---

## 1. ESTADO: EL CAPÍTULO 3 ESTÁ TERMINADO Y REVISADO

- **Maestro definitivo: `docs/3. Kāraka-Kappa.md`** (§271–§315, 45 suttas,
  un kaṇḍa, **55 notas al pie** numeradas 1–55 en orden de aparición).
  Angel lo revisó entero en la sesión 12; se le aplicaron tres tandas de
  correcciones (A: errores; B: 10 fallos de coherencia; C: 9 consultas),
  todas verificadas por script (notas emparejadas, secuencia continua,
  cero comillas rectas, sin dígitos huérfanos).
- Igual que `docs/2. Nāma-Kappa.md`: **final e intocable sin permiso.**
- Los borradores `sesion-11-*` y `capitulo-03-karaka-kappa-completo.md`
  quedan como registro histórico; sus NOTAS DE TRABAJO conservan las
  tablas de referencias retiradas y las variantes de Pind. La copia
  `borradores/3-Kāraka-Kappa-revA.md` es idéntica al maestro.

## 2. FALLOS DE ANGEL EN LA SESIÓN 12 (ya aplicados; valen como convención)

1. **Los ocho nombres kāraka se TRADUCEN** en la prosa (novedad frente al
   Nāma): apādāna=ablativo, sampadāna=dativo, okāsa=locativo,
   karaṇa=instrumental, kamma=objeto, kattā=sujeto (o agente), hetu=causa,
   sāmī=posesivo (también genitivo). Esquema uniforme: glosa del título con
   el pāḷi; vutti con el español; kvattho «¿Cuál es la utilidad del nombre
   “pāḷi” (español)? Para el uso del nombre “pāḷi” en el sutta “X” (§N).
   [glosa española del sutta citado]». Ocho notas de política con la
   fórmula «A partir de ahora el término “X” se traduce como “Y”.»
2. **«¿Cómo qué?» con tilde** (ojo: el Nāma publicado usa «¿Como qué?» en
   §53 — si Angel quiere retroactividad, es un cambio al maestro del Nāma;
   no se ha pedido).
3. **«Sangha» en el español** (el pāḷi conserva saṃgha-).
4. gāma = «poblado» · appāṇini = «ser no sintiente» · bandhana (§275) =
   «confinamiento» · kimatthaṃ cita «“pāḷi” (español)».
5. **Erratas**: todas las aprobadas están aplicadas; *Sattamīvibhatyatthaṃ*
   (§274) y *asaho* (§272) se CONSERVAN por cotejo de Angel con la edición
   del Sexto Concilio (Pind lee distinto; no corregir).
6. **Notas al pie con prefijo** «Nota al pie:» (de Nandisena) / «Nota del
   traductor:» (nuestras), como el Nāma.
7. **Cierres:** «**Iti nāma-kappe kāraka-kappo chaṭṭho kaṇḍo**» / «**Así
   termina la sexta sección, capítulo de casos gramaticales en el capítulo
   de nombres.**» / «**Kāraka-kappo niṭṭhito**» / «**Fin del capítulo de
   casos gramaticales**». La fórmula española YA casa con `RE_CIERRE_ES`.
8. La nota de referencia «Vin. i 304» se retiró: **las referencias
   canónicas se tratarán todas juntas, más adelante** (decisión de Angel).

## 3. TAREA DE ESTA SESIÓN: PASOS DE PUBLICACIÓN (CLAUDE.md «Capítulo nuevo»)

1. **`kaccayana/03-karaka-kappa.md`** en formato del generador, convertido
   DESDE el maestro con un script (modelo: `herramientas/convertir_nama.py`,
   principio «proponer y verificar»: recomponer byte a byte). Conversiones:
   desglose `\= N voces]` → `, N]`; viñetas `*` → listas numeradas `1.`;
   TRES bloques por sutta (pāḷi `---` español `---` ejemplos: el tercer
   bloque arranca en el primer rótulo «Ejemplos:»); las notas ya son `[^n]`.
   El maestro trae los escapes de exportación (`\.`, `\[`, `\+`, `\=`) como
   el del Nāma: mismo tratamiento.
2. **Regex del encabezado:** `RE_SUTTA` en `generar_capitulo.py` espera UN
   número de Rūpasiddhi; §271 lleva «271\. 88, 308\.». Ampliar el grupo a
   `(\d+(?:,\s*\d+)*)` y revisar qué hace el resto del código con ese campo
   (tooltips, EPUB).
3. **Ojo con dos rasgos del maestro** al convertir: (a) el verso de §277
   va en el bloque pāḷi con pādas línea a línea, pero su 2.ª línea acaba en
   punto — comprobar si dispara o no el modo verso del generador y decidir
   con Angel; (b) los suttas largos (§275, §277) tienen VARIOS bloques
   «Ejemplos:» con rótulos de sección numerados (1)–(22) — verificar cómo
   los digiere el generador antes de publicar.
4. **`CAPITULOS`**: entrada 03 (slug, títulos «Kāraka-Kappa» / «Capítulo de
   casos gramaticales», anterior=nama, siguiente=en preparación), insignia
   de versión con fecha.
5. **`comun/concordancia.json`**: 45 entradas, §271–§315.
6. **`site/kaccayana/index.html`**: tarjeta real en lugar de «en
   preparación».
7. **Avisos del generador esperables:** §438 (capítulo sin traducir) y
   referencias «Rū./Sad./Mog.» de las notas NO deben enlazarse; las citas
   internas §271–§315 y las cruzadas al Sandhi/Nāma sí (vía concordancia).
8. Ejecutar `generar_todo.py`, revisar avisos, verificación visual, commit
   (el hook regenera `site/`), push de Angel.

## 4. PENDIENTES QUE NO SON DE ESTA SESIÓN (no perder)

- **Restitución de referencias canónicas** de los tres capítulos: las del
  Kāraka están tabuladas en las NOTAS DE TRABAJO de
  `borradores/sesion-11-suttas-271-285.md` (§5), `-286-300.md` (§4) y
  `-301-315.md`. Angel dará la orden («Then we will deal with the
  references»).
- **Volcado al glosario** de los términos del capítulo 3 (listas §6/§5 de
  los borradores) con las traducciones FALLADAS (ablativo, dativo, etc.) y
  de los del capítulo 4 cuando se revise.
- Si Angel quiere `<u>` (subrayado) para el kāraka en el sitio en lugar de
  negrita, es cambio del generador (lo pidió una vez; quedó en negrita).
- Revisión del capítulo 4 (hilo propio, briefing-13).
- A plazo: el solucionador de sandhis (CLAUDE.md).

## 5. PARA EL CHAT NUEVO

- Leer primero este briefing; luego `CLAUDE.md` («Cómo se publica» y
  «Capítulo nuevo: qué hace falta»), briefing-08 §2–§3 (cómo se hizo el
  montaje del Nāma: es el modelo exacto) y briefing-05 §11.
- El archivo fuente de todo es **`docs/3. Kāraka-Kappa.md`**; no se edita
  sin permiso — el trabajo de esta sesión produce archivos NUEVOS
  (`herramientas/convertir_karaka.py`, `kaccayana/03-karaka-kappa.md`) y
  toca los cuatro puntos de integración (generador, concordancia, índice).
- Conversación de trabajo en inglés.

---

*Preparado en la sesión 12 al cierre de la revisión del capítulo 3.
La sesión 14 publica el Kāraka-Kappa.*
