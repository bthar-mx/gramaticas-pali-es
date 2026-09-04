# Briefing de la sesión 57 — LA COLACIÓN TERMINA (44 DE 44), Y LO QUE SE CAE SON LAS OMISIONES

**Fecha:** 2026-09-04. Un frente de trabajo, dos en espera: **la colación del
Conspectus de la p. 1130 a la 1148**, que cierra las 44 páginas; el inglés
del Glosario (tanda 1) y los puntos 17-26 de la revisión siguen esperando
veredicto del IEBH y no se han tocado. Además, el remate de la sustitución
del nombre propio por «IEBH», que la sesión 56 dejó a medias.

Este briefing supone leídos los de las sesiones 46 a 56. El registro de la
colación está en `docs/glosario/revision-de-las-i.md`, **§4 sexies**; los
puntos que esperan decisión, en su §5, ahora **hasta el 34**.

---

## 1. LO PRIMERO, SI SÓLO SE LEE UN PÁRRAFO

**Una duda que decía «comprobado a ×8 sobre el ejemplar del IEBH: punto
redondo» afirmaba lo contrario de lo que el ejemplar imprime.** `aparadipanā`
(p. 1136) es `aparadīpanā`, con ī, y el control está en la línea siguiente
—*purimatthassa* con punto, *dīpanā* con barra—. Es del género de las breves
inventadas de la sesión 55, pero peor, porque ésta se dio por verificada
sobre la misma fuente que la desmiente. De ahí la regla que va al §5.27:
**«comprobado en el ejemplar» sin aumento ni control no vale**. Y de ahí que
su vecina `visesaniya` (p. 1138), con la misma frase, quede en cuarentena:
la hoja no decide y no se afirma.

Lo segundo: **la transcripción tiene huecos de prosa.** Cinco pasajes de
Smith no están en ninguna ficha ni nota; el de la p. 1145 son ocho líneas con
tres casos enteros del cuadro (C) de 7.3.1. Las 25 páginas anteriores no se
miraron con esa clase en la cabeza (§5.34).

---

## 2. La colación: pp. 1130-1148, y con ellas las 44

| pág. | fichas | hallazgos | estado |
| ---: | ---: | ---: | --- |
| 1130 | 49 | 2 | `upānīya` 919,10; `pāḷī` |
| 1131 | 37 | 1 | ⟨Mg⟩ angular (dos fichas) |
| 1132 | 48 | 2 | ⟨5.3 … 5.4.14⟩ angular (dos fichas); `mahāṭīkā` coma confirmada |
| 1133 | 46 | 0 | limpia; omisión «(E)» |
| 1134 | 69 | 0 | limpia |
| 1135 | 36 | 0 | limpia |
| 1136 | 31 | 1 | **`aparadīpanā`**; omisión |
| 1137 | 30 | 0 | limpia |
| 1138 | 35 | 2 | `sarūpānaṃ` ṃ; `visesaniya` en cuarentena; omisión |
| 1139 | 49 | 0 | limpia |
| 1140 | 85 | 1 | `nipphajjəte`, tipo vuelto |
| 1141 | 51 | 0 | limpia |
| 1142 | 75 | 0 | limpia |
| 1143 | 50 | 0 | limpia |
| 1144 | 37 | 0 | limpia; omisión (siete referencias) |
| 1145 | 31 | 0 | limpia; **omisión de ocho líneas** |
| 1146 | 55 | 0 | limpia |
| 1147 | 45 | 0 | limpia |
| 1148 | 16 | 0 | limpia |

**44 de 44. Ningún lema se ha tocado.** Nueve `duda` nuevas, tres ampliadas;
la cuenta que imprime `generar_glosario.py` pasa de 74 a **83**. Todas las
nuevas empiezan por «Colación sobre el ejemplar del IEBH (sesión 57):».

Lo que conviene saber de esta tanda, aparte del §1:

- **Los angulares aplanados suman once** con ⟨Mg⟩ (p. 1131) y ⟨5.3 … 5.4.14⟩
  (p. 1132). El primero es la regla de la sesión 47 §4 en su forma más
  limpia: Smith le pone la marca de Moggallāna hasta a la sigla. El segundo
  abre una comprobación pendiente en el Index A. Los dieciséis angulares
  restantes de estas páginas estaban bien transcritos: en la sección 7 la
  transcripción los miró con más cuidado.
- **`upānīya`**: la ficha dice 919,16 y la plancha 919,10, y **la p. 919 del
  vol. III lo confirma** —línea 10: «tisso kathā: vādo jappo vitaṇḍā ti»—. Es
  el único caso de la tanda en que se pide tocar un campo, y es `ref_smith`.
  De paso, esa página imprime `sādhanīya` con ī tres veces (punto 26).
- **`pāḷī`** (p. 1130) y **`sarūpānaṃ`** (p. 1138): dos lecturas contra la
  ficha, la primera del género de `vīcchā` —Smith con ī, la lengua y
  Nandisena con breve—, la segunda contra una nota que afirma una m.
- **`vīcchā`** con ī por quinta vez (p. 1137).
- **`nipphajjəte`** (p. 1140): errata de imprenta, tipo vuelto; la ficha
  normaliza en silencio. Constancia, nada más.

### El método, lo que ha cambiado

Lo de siempre —hoja = página − 1104, `pdfimages -j`, control en la misma
página— y dos cosas nuevas que salen de esta tanda:

1. **Leer la página entera contra la LISTA de fichas, no sólo los lemas.**
   Así salieron las cinco omisiones. Un guion que imprime «índice | epígrafe |
   pali | fr» de la página y las dos mitades de la hoja a ×0,75 basta.
2. **Cuando una duda dice «comprobado», comprobarla igual.** Dos de las tres
   ampliadas de esta tanda contradicen o ponen en cuarentena lo que decían.

---

## 3. Lo que espera al IEBH, sin tocar

- **El inglés del Glosario, tanda 1** (65 entradas, `recursos/glosario/ingles.json`,
  `"adjudicado": false`): las 14 notas del §3 de
  `docs/glosario/ingles-por-adjudicar.md` siguen sin veredicto. No se ha
  escrito más inglés; la siguiente entrada sigue siendo `apaccattha-taddhita`.
- **Los puntos 17-26** de `revision-de-las-i.md` §5, más los **27-34** de
  esta sesión.

---

## 4. El nombre propio → «IEBH»: lo que la sesión 56 dejó

La sustitución de la sesión 56 fue sensible a mayúsculas y dejó **34
apariciones en versalitas** —«DECISIÓN DE …», «EL EJEMPLAR DE …», en cabeceras
de briefings y en seis `duda` del Conspectus— más la clave
`lo_que_se_ve_en_el_ejemplar_de_…` de `diplomado.json` (nadie la lee por
nombre) y las menciones del propio briefing 56. Hecho ahora, 29 archivos, con
las preposiciones ajustadas («DEL IEBH», «LO QUE EL IEBH DECIDIÓ»). Lo único
que queda es el nombre de archivo `conspectus-ejemplar-angel.pdf`, que no
viaja, y `CLAUDE.md`, que es la excepción declarada.

---

## 5. Lo que el chat que siga tiene que hacer

1. **Esperar el veredicto del IEBH sobre la tanda 1 del inglés** antes de
   escribir más; cuando llegue, aplicarlo a `ingles.json` y seguir por
   `apaccattha-taddhita`, en tandas de ~60, con el mismo patrón y la misma
   prelación (N-EN › IEBH › Ñāṇamoli › propuesta › traducción).
2. **Esperar los veredictos de los puntos 17-34** y aplicarlos; el 32
   (`upānīya` → 919,10) es el único que toca un campo.
3. **Si el IEBH lo aprueba**: (a) el barrido de paréntesis en las pp.
   1105-1122 (§5.23 b), que es rápido; (b) el barrido de omisiones de prosa en
   las pp. 1105-1129 (§5.34), que no lo es tanto; (c) mirar en el Index A qué
   son 5.3-5.4.14 (§5.29).
4. **La colación está hecha.** Lo que sigue del plan del briefing 54 §7 son
   el análisis de las dos fuentes (61 `conflicto`) y las referencias
   `ref_smith` sin verificar.
5. Y al terminar cualquier cosa:

       python3 herramientas/generar_todo.py

   y la comprobación con jsdom: cargar `site/recursos/glosario/index.html`
   con `matchMedia` y `scrollTo` simulados, contar `#out .t` (1.984), pulsar
   `#b-nand` (→ 1.637 → 1.984), `#b-smith` (→ 665 → 1.984), `#b-en`/`#b-es`,
   `#tab-conspectus` (→ 1.878) y leer la consola (0 errores en esta sesión).

### Advertencias operativas que no cambian

- **No ejecutar `git status`** desde el entorno Linux:
  `git --no-optional-locks status --porcelain`. Y tampoco `git checkout --
  archivo`: el montaje no deja desenlazar; para restaurar, `git show
  HEAD:ruta > ruta`.
- Al editar un `pNNNN.json`, `json.load` después. Y **no volcarlo con
  `json.dump`**: los de las pp. 1136-1148 están escritos a mano, con listas
  en una línea, y el volcado los reformatea entero. Insertar la `duda` como
  texto.
- Los tres PDF y `conspectus-ejemplar-angel.pdf` no viajan.

---

## 6. Cifras al cerrar

| | |
| --- | --- |
| **páginas COLACIONADAS contra la plancha** | **44 de 44** |
| términos del Conspectus | 1.878 |
| entradas de Nandisena | 649 · español completo · inglés 65 redactadas, 0 adjudicadas |
| lemas de la vista alfabética | 1.984 |
| fichas con `duda` | **83** (74 al abrir) |
| angulares aplanados encontrados | 11 |
| omisiones de prosa registradas | 5 |
| lemas cambiados en esta sesión | **0** |
| el nombre propio en lo que produce el proyecto | **0** (34 más sustituidas) |
