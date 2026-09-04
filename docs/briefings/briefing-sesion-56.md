# Briefing de la sesión 56 — EL INGLÉS DEL GLOSARIO ARRANCA, Y LA COLACIÓN ENCUENTRA LOS PARÉNTESIS

**Fecha:** 2026-09-04. Tres frentes: **la primera tanda del inglés del
Glosario de Nandisena** (65 entradas, sin adjudicar), **la colación del
Conspectus** de la p. 1124 a la 1129 (van 25 de 44), y **la sustitución de
«Angel» por «IEBH»** en todo lo que produce el proyecto.

Este briefing supone leídos los de las sesiones 46 a 55. El registro de la
colación, página por página, está en `docs/glosario/revision-de-las-i.md`,
**§4 quinquies**; los puntos que esperan decisión, en su §5, ahora **hasta el
26**.

---

## 1. LO PRIMERO, SI SÓLO SE LEE UN PÁRRAFO

**El escaneo de 400 dpi aplanaba los paréntesis angulares.** En tres páginas
seguidas —1125, 1126, 1127— la plancha imprime **ocho ⟨ ⟩ que la transcripción
dio por ( )**, y en cuatro la nota de la ficha afirma expresamente que son
redondos. Cada angular es una atribución a Moggallāna (sesión 47 §4), y las
ocho se habían perdido: visesana, visessa, saṃkhyādi, vutti yeva, aññatthe,
vītihāre, cattha, sambhama. El patrón: los angulares con texto francés largo
salieron bien; los que encierran una sola voz pāḷi corta salieron redondos.
**Las pp. 1105-1122 no se miraron con esa clase en la cabeza**, y conviene un
barrido sólo de paréntesis (§5.23 de la revisión).

---

## 2. El inglés del Glosario: tanda 1, 65 entradas, SIN adjudicar

| qué | dónde |
| --- | --- |
| el borrador | `recursos/glosario/ingles.json`, `"adjudicado": false` |
| el cotejo lado a lado | `docs/glosario/ingles-por-adjudicar.md` (lo escribe `herramientas/generar_ingles_glosario.py`) |
| la verificación | `generar_glosario.py` comprueba clave, ejemplos citados y NFC; **no inyecta** mientras no esté adjudicado |
| la plantilla | `capaNand()` enseña `t.en` en modo EN cuando el generador lo inyecte; hasta entonces, español |

**Cómo está hecho:**

- **Clave** = lema impreso; los homónimos y el `adhikāra` que sale dos veces
  llevan `|1`, `|2` (`claves_nandisena()` en `generar_glosario.py`). Las
  remisiones («v. akammaka») no tienen entrada.
- **Campos**: `en` (la entrada entera), `termino`, `fuente`, `nota`.
- **Prelación aplicada**, y la cuenta de la tanda: 11 N-EN · 7 IEBH · 7 Ñāṇamoli
  · 1 propuesta (glosario-ingles.json) · **37 traducción** sin término inglés
  en ninguna fuente · 2 remisiones.
- **Fuentes N-EN nuevas respecto al briefing 55**: las traducciones inglesas
  del propio Nandisena de Taddhita, Ākhyāta, Kibbidhāna y Uṇādi (`docs/5 - …`,
  `6 - …`, `7- …`, `8 - …`). De ahí salen «secondary derivative» (taddhita),
  «indicatory letter» (anubandha), «offspring» (apacca), «the Blessed One».

**Las 14 notas del §3 del cotejo piden decisión.** Las de más peso:

1. **ajjhesanā**: el Glosario dice «consentimiento; permiso»; la página del
   verbo, ya adjudicada, dice «Request» y reserva «consent» para anumati.
2. **taddhita**: N-EN «secondary derivative» frente a la propuesta «nominal
   derivative» de `glosario-ingles.json`. Se siguió N-EN.
3. **akkhara-vipatti / apaccattha / anupadiṭṭha**: N-EN traduce «deformity of
   letters», «offspring», «not shown»; el Glosario español dice otra cosa. Se
   siguió al Glosario y se anotó N-EN.
4. **anukaraṇa**: el Glosario dice «preposición» para upasagga; la norma dice
   prefijo.

**Siguiente entrada: `apaccattha-taddhita` (p. 4).** Quedan 582 traducibles.

---

## 3. La colación: pp. 1124-1129

| pág. | fichas | hallazgos | estado |
| ---: | ---: | ---: | --- |
| 1124 | 38 | 3 | tres `duda` |
| 1125 | 39 | 4 | cuatro `duda` |
| 1126 | 33 | 3 | tres `duda` |
| 1127 | 27 | 2 | dos `duda` |
| 1128 | 26 | 0 | limpia |
| 1129 | 50 | 1 | media duda vieja cerrada |

**Van 25 de 44. Ningún lema se ha tocado.** Además de los paréntesis del §1:

- **`vīcchā`**: cuatro apariciones en tres páginas (1120, 1124 ×2, 1127), las
  cuatro con ī en el ejemplar; los cuatro lemas los fijó IEBH breve porque el
  escaneo no decidía. Puntos 18 y 24.
- **`ā̆nupubbī`** (p. 1124): anceps de verdad, y la nota «IMPORTANTE PARA LEER
  LAS BREVES DE SMITH» se apoya en dos breves que la sesión 55 desmintió.
  Punto 25.
- **`upasajjanībhūta`** (variante, p. 1124) y **`sādhanīya-`** (p. 1129): íes
  largas donde la ficha tiene breve; la segunda cierra la mitad de una duda
  vieja. Punto 26.

**Siguiente página a colacionar: la 1130** (ya extraída: hoja 26).

---

## 4. «Angel» → «IEBH», hecho

Pedido de Angel en esta sesión. **779 apariciones en 70 archivos** de
`recursos/`, `comun/`, `docs/` (briefings incluidos) y `herramientas/`, con
las preposiciones ajustadas: «ejemplar del IEBH», «al IEBH», «lo decide IEBH»,
«El IEBH» a principio de frase, «the IEBH» en el inglés. `CLAUDE.md` es la
única excepción y lo dice. El nombre de archivo
`conspectus-ejemplar-angel.pdf` no se ha tocado: está en su disco y no viaja.
Con esto quedan corregidas las tres notas de paradigmas que decían «con el
visto bueno de Angel».

---

## 5. Lo demás de la sesión

- **La tarjeta del glosario en `/recursos/`**, que faltaba. `generar_indices.py`
  la arma con insignia calculada de los datos («649 entradas · 1.878
  términos»), ES/EN.
- **GLOS / CONSP**: Angel los veía no responder. En código conmutan bien
  (jsdom: 1.984 → 1.637 → 1.984; 1.984 → 665 → 1.984). Lo que pasaba es que
  **están desactivados a propósito en las pestañas Conspectus y Norma** y nada
  lo enseñaba. Ahora el desactivado se ve —atenuado y tachado— y el globo dice
  por qué.
- **El globo del botón EN** ya no dice que Nandisena «no tiene inglés», sino
  que se está redactando y lo firma el IEBH.
- **Cuenta de `duda`**: el briefing 55 decía 68 y los datos dan 62 al abrir la
  sesión; al cerrar, **74**. La cifra buena es la que imprime
  `generar_glosario.py`.

---

## 6. Lo que el chat que siga tiene que hacer

1. **Esperar el veredicto de Angel sobre la tanda 1** antes de escribir más
   inglés; cuando llegue, aplicarlo a `ingles.json` y seguir por
   `apaccattha-taddhita`, en tandas de ~60, con el mismo patrón.
2. **Seguir la colación por la p. 1130** hasta la 1148, con la clase nueva en
   la cabeza: **mirar los paréntesis**, no sólo las cantidades. Reglas sin
   cambio: control en la misma página, ningún lema se toca, `duda` a lo que
   baile, anotar en `revision-de-las-i.md` (§4 sexies).
3. Si Angel lo aprueba (§5.23 b), **barrido de paréntesis en las pp. 1105-1122**:
   es rápido, porque sólo se buscan ⟨ ⟩ junto a voces pāḷi cortas.
4. Y al terminar cualquier cosa:

       python3 herramientas/generar_todo.py

   y la comprobación con jsdom de que la página del glosario pinta (la
   sesión 55 lo explica; el guion de esta sesión carga la página con
   `matchMedia` y `scrollTo` simulados, cuenta `#out .t`, pulsa EN/ES y
   GLOS/CONSP y lee la consola).

### Advertencias operativas que no cambian

- **No ejecutar `git status`** desde el entorno Linux: `git --no-optional-locks
  status --porcelain`.
- Al editar un `pNNNN.json`, `json.load` después.
- Los tres PDF y `conspectus-ejemplar-angel.pdf` no viajan.

---

## 7. Cifras al cerrar

| | |
| --- | --- |
| **páginas COLACIONADAS contra la plancha** | **25 de 44** (1105-1129) |
| términos del Conspectus | 1.878 |
| entradas de Nandisena | 649 · español completo · **inglés 65 redactadas, 0 adjudicadas** |
| lemas de la vista alfabética | 1.984 |
| fichas con `duda` | **74** (62 al abrir) |
| lemas cambiados en esta sesión | **0** |
| «Angel» en lo que produce el proyecto | **0** (779 sustituidas) |
