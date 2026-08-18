# Kaccāyana Pāḷi-Español: Briefing de la Sesión 15

*Complementa a los briefings 05–14. La sesión 14 publicó el capítulo 3
(Kāraka-Kappa) y, de paso, arregló cinco defectos de maquetación que
afectaban a los tres capítulos. La revisión del capítulo 4 (Samāsa) sigue
siendo un hilo PARALELO con su propio briefing (el 13).*

---

## 1. ESTADO AL CIERRE DE LA SESIÓN 14

- **`kaccayana/03-karaka-kappa.md` existe y genera limpio**: 45 suttas
  (§271–§315), 1 kaṇḍa, 55 notas → `site/kaccayana/karaka/index.html`.
- `comun/concordancia.json` tiene ya el capítulo 3 (45 entradas,
  continuidad §271–§315 verificada). La tarjeta de
  `site/kaccayana/index.html` enlaza a `karaka/`. Insignia de versión 1.0
  (2026-08-17).
- El único aviso del generador es **§438** (capítulo sin traducir), como
  anticipaba el briefing-14. `revisar.py` no da errores.
- **Pendiente al cerrar: el commit y el push.** El árbol de trabajo tiene
  todo hecho y regenerado; falta lanzarlo (Claude no puede escribir en
  `.git` desde la sesión).

## 2. LA CONVERSIÓN (herramientas/convertir_karaka.py)

Mismo principio que el Nāma: **proponer y verificar** — recompone el
maestro desde el archivo convertido y exige igualdad byte a byte antes de
escribir. Transformaciones:

1. Desglose `\= N voces]` → `, N]` (45).
2. Tercer bloque: `---` antes del bloque de ejemplos (45 suttas; ninguno
   se queda sin él).
3. Viñetas `*` → listas numeradas (100 listas, 296 ítems).

**Diferencia con el Nāma:** el maestro del Kāraka **no** tiene notas en
prosa. Las 55 ya vienen como `[^n]` numeradas 1–55 en orden de aparición,
así que el script no las convierte ni renumera: sólo comprueba que anclas
y definiciones casen, y aborta si aparece una nota en prosa inesperada.

**El corte del tercer bloque retrocede al rótulo de entrada** (decisión de
Angel, sesión 14). Regla: se corta en el primer «Ejemplos:», y se
retrocede un párrafo si el anterior acaba en «:» o es «¿Cómo qué?». Afecta
a cinco suttas —§271, §272 («¿Cómo qué?»), §275, §277, §278 («Primero,
(1) …:»)— y deja el bloque español en glosa + vutti en todo el capítulo.
Los otros 40 salen igual que con la regla del Nāma.

## 3. CAMBIOS AL GENERADOR

- **`RE_SUTTA` admite número de Rūpasiddhi doble**: §271 lleva
  «271. 88, 308.». El grupo es `(\d+(?:,\s*\d+)*)` y `rup` pasa a ser
  cadena normalizada; el tooltip pluraliza a «Rūpasiddhi Suttas».
  Mismo cambio en `revisar.py`; `generar_sandhi.py` lo devuelve a entero
  para no alterar su JSON.
- **El nombre del kaṇḍa se lee del markdown**, no del número correlativo.
  El Kāraka es el `CHAṬṬHA-KAṆḌA` aunque sea el primer (y único) kaṇḍa de
  su archivo, y antes habría salido «Paṭhama-Kaṇḍa · Primera sección».
  El Sandhi y el Nāma empiezan en PAṬHAMA, así que su salida no cambia.
- **Plural del encabezado**: «1 sección», no «1 secciones» (el Kāraka es
  el primer capítulo de un solo kaṇḍa).
- `CAPITULOS["03-karaka-kappa"]`: slug `karaka`, anterior `2-Nāma-Kappa`,
  siguiente `4-Samāsa-Kappa` (botón inactivo mientras no exista).
- **El hook de pre-commit ejecuta todos los `convertir_*.py`** y añade
  todo `kaccayana/`, no sólo el Nāma. **Ojo: los hooks no viajan con el
  clon**; en una copia nueva hay que volver a ejecutar
  `sh herramientas/instalar-hooks.sh`.

## 4. CINCO ARREGLOS DE MAQUETACIÓN QUE AFECTAN A LOS TRES CAPÍTULOS

Salieron de la revisión visual de Angel sobre el capítulo nuevo, pero
ninguno era exclusivo de él. Ninguno toca el texto traducido.

| Arreglo | Sandhi | Nāma | Kāraka |
| ------- | -----: | ---: | -----: |
| Bloques pāḷi con sus párrafos | 50 | 212 | 45 |
| `<strong>` con negrita real | 224 | 731 | 516 |
| Listas de ejemplos en la serif | — | 244 | 100 |
| Listas separadas de lo que sigue | 54 | 169 | 71 |
| Traducción de verso sin cursiva | — | 2 | — |

1. **Los bloques pāḷi recuperan sus párrafos.** `bloque_pali()` sólo
   respetaba los párrafos cuando detectaba un verso; si no, unía el bloque
   entero en un párrafo corrido y se perdían las separaciones entre
   explicaciones («**Dūratthe** tāva: …», «**Antikatthe**: …»). §275 tiene
   22 párrafos en el maestro y salía como uno solo.
2. **La negrita nunca fue de verdad.** Las páginas cargaban JetBrains Mono
   sólo en peso 400, y Noto Serif e Inter en 400/500: ningún `<strong>`
   tenía cara real y el navegador la sintetizaba. Añadidos los pesos 700
   en `generar_capitulo.py` y `generar_recurso.py`. (La referencia de
   sandhi ya cargaba `wght@400;500;700`; por eso allí sí se veía.)
3. **Las listas de «Ejemplos» van en la serif**, no en mono. El criterio es
   **el rótulo, no el capítulo**: «Ejemplos» → serif 13px; «Secuencia» →
   mono, que es lo que piden los pasos de derivación. Sale limpio porque
   el Sandhi es 63/63 «Secuencia» (ítems de 18 caracteres de media) y el
   Nāma y el Kāraka son 100 % «Ejemplos» (99 y 88 caracteres de media:
   prosa, no código). Marca: `<ol class="seq-list seq-ejemplos">`.
4. **Las listas se separan de lo que sigue.** El reset `* { margin: 0 }`
   dejaba la lista pegada al «(2) …» siguiente, al kimatthaṃ o al título
   en negrita. `.seq-list { margin-bottom: .85rem }`, y `:last-child` a
   cero para no dejar hueco al cerrar el bloque.
5. **`.pali-verse-trans` sin cursiva** (las traducciones de los versos de
   §185).

## 5. ERRATA APLICADA AL MAESTRO DEL KĀRAKA

§277, segundo pāda del verso: `Vuttaṃ ‘kamman ti vuccati.` →
**`Vuttaṃ ‘kamman’ ti vuccati.`** La comilla de apertura no cerraba,
frente a `sa ‘kattā’ ti` del primer pāda y `‘sampadānaṃ’ vijāniyā` del
cuarto. Autorizado por Angel; `revisar.py` queda limpio.

**El verso de §277 sigue sin modo verso** (decisión de Angel): su segundo
pāda acaba en punto y el criterio del generador pide coma en todas las
líneas menos la última. Ahora al menos es un párrafo aparte, gracias al
arreglo 4.1. Si se quisiera pāda a pāda, hay que relajar el criterio y
poner un guardia para que «icc evamādi.» no se tome por la traducción.

## 6. PENDIENTES

- **Commit y push** (lo primero de la sesión 15 si no se hizo).
- **Revisión visual en vivo** de los tres capítulos tras el despliegue.
- **Restitución de referencias canónicas** de los tres capítulos: las del
  Kāraka están tabuladas en las NOTAS DE TRABAJO de
  `borradores/sesion-11-suttas-271-285.md` (§5), `-286-300.md` (§4) y
  `-301-315.md`. Angel dará la orden.
- **Volcado al glosario** de los términos del capítulo 3 con las
  traducciones falladas (ablativo, dativo, okāsa=locativo, karaṇa=
  instrumental, kamma=objeto, kattā=sujeto/agente, hetu=causa,
  sāmī=posesivo) y de los del 4 cuando se revise.
- «¿Como qué?» sin tilde en §53 del Nāma publicado, frente a «¿Cómo qué?»
  del Kāraka: si Angel quiere retroactividad, es un cambio al maestro del
  Nāma (no se ha pedido).
- Si Angel quiere `<u>` para el kāraka en lugar de negrita, es cambio del
  generador.
- Revisión del capítulo 4 (hilo propio, briefing-13).
- A plazo: el solucionador de sandhis (CLAUDE.md).

## 7. PARA EL CHAT NUEVO

- Leer primero este briefing; el 14 da el detalle del capítulo 3 y el 05
  §11 el formato del generador.
- Los maestros de `docs/` son **finales e intocables sin permiso**. Los
  archivos del generador se rehacen desde ellos con
  `convertir_nama.py` / `convertir_karaka.py` (verifican solos).
- `python3 herramientas/generar_todo.py` regenera el sitio. Avisos
  esperados: Kāraka §438; Nāma §25, §45 ×2, §404 ×4, §638; Sandhi §49 y
  §139; las «secuencias sospechosas» de generar_sandhi son las conocidas
  (CLAUDE.md, «Estado de recursos/sandhi»).
- Conversación de trabajo en inglés.

---

*Preparado al cierre de la sesión 14, con el capítulo 3 listo para
desplegar.*
