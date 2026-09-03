# Kaccāyana Pāḷi-Español: Briefing de la Sesión 45

*Complementa a los briefings 05–44. Tema de la sesión 45 (2026-09-03): **la
edición inglesa de Kaccāyana y, de paso, tres arreglos al Sandhi-Kappa
español**. El Venerable Nandisena ha dado su permiso para la edición inglesa.
Se ha tocado `kaccayana/01-sandhi-kappa.md`, `comun/guia-de-estilo.md` y
`herramientas/generar_capitulo.py`; se ha regenerado `site/` con
`generar_todo.py`. **Nada está confirmado en git:** Angel revisa y confirma.*

> **Lo primero que tiene que saber el chat nuevo: la edición inglesa del
> Sandhi-Kappa ESTÁ ESCRITA Y GENERADA, y no está revisada por Angel.**
> `kaccayana/01-sandhi-kappa.en.md` (51 suttas, 35 notas) →
> `site/en/kaccayana/sandhi/index.html`, con botón EN/ES y `hreflang` en las
> dos páginas. Angel autorizó escribirla entera sin aprobación sutta a sutta
> y revisarla después (2026-09-03, antes de salir). El registro de lo que se
> desvía del inglés impreso de Nandisena está en
> `docs/ingles/memo-sandhi-en-glosario-y-desviaciones.md`, §5. **Nada está
> confirmado en git.** Lo que Angel tiene que hacer al volver: leer la página
> inglesa en `site/en/kaccayana/sandhi/` (o desplegarla), revisar el diff, y
> confirmar o corregir.

## 0. LO QUE CAMBIÓ, EN UNA TABLA

| | antes | después |
| --- | --- | --- |
| citas canónicas del Sandhi | 156 notas al pie con siglas por obra (`Dh. 67`) | **en línea en el bloque pāḷi, como la edición base** (`Khu. i, 67`), igual que Nāma y Kāraka |
| notas al pie del Sandhi | 185 | **35** (las que son texto, no cita) |
| citas que faltaban | — | repuestas: las diez del *suttavibhāga* de §20 y `(A. iii, 424)` en §36 |
| omisiones respecto de Nandisena | 6 | **0**: §26 «upanīyati» + su nota; notas de variante (K / K-PTS) en §1 ×2, §7, §35, §51; nota de Nandisena sobre *ṭhāne* en §28 (estaba vacía) |
| erratas | 6 | **0**: *vidhūn’* → *vidūn’* (§41 ×3); *paccatañ* → *paccattañ* (§32); «evaṅkho (EM)» → «evaṅ kho (EM)» (§31); *Saddhīdha / Cūbhayaṃ / Kiṃ sūdha* → *Saddh’ īdha / C’ ūbhayaṃ / Kiṃ sū ’dha* (§15–16, títulos, pāḷi y paso EM); emergente de *kvaci* «a veces / ocasionalmente» → «a veces» (16 veces) |
| `ABREVIATURAS` | 17 siglas | +`JA`, `VinA`, `AbhiA`, `SuttanipātaA` |
| guía de estilo | — | **§5.1 sexies** documenta lo anterior |

## 1. LA EDICIÓN INGLESA: QUÉ ES Y QUÉ NO ES

Angel lo precisó en la sesión, y conviene dejarlo con sus palabras porque
acota el trabajo:

1. **No es una reescritura.** Donde Nandisena tradujo, su inglés se queda.
2. **Donde Nandisena no tradujo un sutta (o una línea) y el español sí, el
   inglés lo traduce**, siguiendo al español.
3. **Donde el español amplió los ejemplos** (secuencias de formación,
   contraejemplos desglosados, encabezados «Extensión por…»), **el inglés
   sigue al español.**
4. **Hace falta un glosario inglés fijo** para *kvaci / vā / navā / vibhāsā* y
   el resto de términos técnicos, como el español. El borrador está en el
   memorando, §2.
5. **Las notas sobre las funciones de «ca» y sobre las partículas son del
   Venerable:** al final de su capítulo 1 hay una página con las aplicaciones
   de «ca» y de *kvaci, vā, navā, vibhāsā*. `comun/terminologia-particulas.md`
   sale de ahí. **Esa página no está en el PDF que tiene el proyecto** (48
   pp., termina en «End of the Sandhi Chapter»): hace falta el original
   inglés para la edición inglesa. **Pedírselo a Angel.**

Lo técnico, decidido en la conversación previa y sin ejecutar: páginas
paralelas (`/en/kaccayana/sandhi/`) generadas de un markdown paralelo
(`sandhi.en.md`), botón EN/ES que conserve el ancla `#sN`, misma clave
`pali_lang` que ya usan la portada y los recursos, `<html lang="en">`,
`hreflang`. El generador necesita un parámetro de idioma y ~20 cadenas de
interfaz (memorando §2.6).

## 2. LAS CITAS: LO QUE SE HIZO Y LO QUE SE APRENDIÓ

### Lo que se hizo

Se emparejó cada nota al pie del Sandhi con la cita correspondiente del PDF
inglés de Nandisena (alineación automática por la palabra pāḷi que precede a
la cita, 145 de 152 solas; las 7 restantes a mano) y se puso la cita **en el
lugar exacto donde la imprime él** — incluido §17, donde `(A. i, 153)` va
tras «ty āssa» y no al final de la frase (regla de §5.1 bis). Las cuatro
citas que colgaban de líneas españolas (§10, §11, §13) se retiraron, como
manda §5.

### Lo que se aprendió, y corrige el memorando

En el primer borrador del memorando se dijo que los «Dh. 67» del español
eran **una errata sistemática** (página birmana rotulada como si fuera
número de estrofa). **No es así**, y conviene que quede escrito: ese siglum
por obra con número de página es **el del propio Venerable** en sus
*Reglas de combinación eufónica* (2013) — «tatrāyaṃ · Dh. 67», «anveti ·
Dh. 13» — y de ahí lo tomó el Sandhi. Los números eran correctos en los dos
sistemas; lo único que cambia con la unificación es que ahora el capítulo
cita como la edición base y como los capítulos 2 y 3. `recursos/sandhi/
reglas.json` conserva el siglum del documento español, que es su fuente.

**Moraleja de la casa:** una medición que no se ha verificado contra la
fuente es una propuesta, no un hallazgo. Aquí la fuente que faltaba era el
documento español del Venerable, y estaba en el proyecto.

### Lo que NO se hizo

Añadir al emergente el número de estrofa verificado contra Pind (PTS) —
«Dhp 375» junto a «Khu. i, 67». Un intento automático dio ruido; hacerlo
bien son ~110 comprobaciones una a una. Queda como DUDA en la guía §5.1
sexies. Angel decide si vale la pena.

## 3. DECISIONES QUE ESPERAN A ANGEL

Ninguna bloquea lo confirmado; todas afectan a la edición inglesa o a una
nota del español.

| # | Cuestión | Dónde |
| --- | --- | --- |
| 1 | ~~*Gaṇa*~~ **Decidido: «the noble Order»**, paralelo al español (Angel, 2026-09-03). | memorando §2.5 |
| 2 | *ṭhāne*: Nandisena traduce en plural y lo justifica en su nota 23; el español eligió el singular. La nota se ha repuesto en §28 (n. 19) con la frase «Esta traducción conserva el singular del pāḷi». **Decidido: se mantiene el singular** en los dos idiomas (Angel, 2026-09-03); la nota 19 dice ahora «por decisión del IEBH». | §28, n. 19 |
| 3 | **Decidido: §12** en los dos idiomas (Angel, 2026-09-03). Corregido en las notas 6 y 7 y registrado en guía §5.1 quinquies. | §10–11 |
| 4 | **Decidido: *vasantatilakā*** (Angel, 2026-09-03). Registrado en guía §5.1 quinquies como corrección a la edición base. | §1, n. 2 |
| 5 | **Decidido: con corchetes, como el español**, para que se entienda (Angel, 2026-09-03). Las palabras de Nandisena se conservan; lo añadido va entre corchetes. | memorando §3.2 |
| 5 bis | **Regla de los corchetes** (Angel, 2026-09-03): el locativo del sutta significa «sigue» y el ablativo «después»; son el sentido del caso y van **sin** corchetes. Escrita en `comun/convenciones.md` §1 bis; aplicada al español en §12, §31, §39 y §46. | convenciones §1 bis |
| 6 | **Decidido: *niccutaṃ***, la lectura birmana, sin nota (Angel, 2026-09-03). | §31 |
| 7 | **Entregada** por Angel en la sesión y guardada verbatim en `docs/fuentes/nandisena-apendice-sandhi-en.md`. Da los nombres ingleses del Venerable para las funciones de «ca» (*dragging, collecting, accumulating, delimiting, smoothness of speech*), que sustituyen a los propuestos en el memorando §2.3, y la cita *Kaccāyanavaṇṇanā* 31, añadida a `comun/terminologia-particulas.md`. | §1.5 |

## 3 bis. LA PÁGINA INGLESA: CÓMO SE HIZO

Decisiones de Angel antes de salir: capítulo entero de una vez, revisión
después; URL `/en/kaccayana/sandhi/`; crédito «English translation by Bhikkhu
U Nandisena (ITBMU); edition, apparatus and glossary by the IEBH»; generador y
botón EN/ES ahora.

**Generador** (`generar_capitulo.py`): diccionario `IDIOMAS` con todas las
cadenas de la página en las dos lenguas; `L` es la lengua en curso; un maestro
`*.en.md` activa `IDIOMAS["en"]`, sale en `site/en/…` y carga los assets desde
`../../../assets/`. Reconoce los rótulos ingleses (`Sequence`, `Examples…`,
`Counter-examples…`, «Thus ends the…», «End of the … Chapter»). Versión
propia por lengua (`version_en`…). Botón `#lang-btn` (el CSS ya existía en
`pali.css` para la portada) y `hreflang` **sólo si la otra página existe**;
`generar_todo.py` genera el inglés y vuelve a generar el español para que se
vean. `pali.js` lee `CAP.textos` para sus nueve cadenas. Todo el español se
regeneró y se comprobó que no cambia salvo lo previsto.

**Redirección:** una página cuya lengua no es la guardada en `pali_lang`
redirige a la otra (con el ancla). Es lo que hace que la elección de la
portada «viaje». Si molesta, es una línea en `render()`.

**El maestro inglés** se escribió sutta a sutta sobre la estructura del
español: pāḷi, citas, secuencias, desgloses y notas idénticos (cotejo por
guion: 51/51 cabeceras, 51/51 bloques pāḷi, 394 líneas de secuencia, 35
notas en el mismo orden, cero restos de español); prosa de Nandisena donde la
hay, corchetes como el español, «follows/after» sin corchetes, y la prosa que
el español añadió, traducida. §5 del memorando lista cada desviación.

**Hallazgo de paso:** en §51 *parakkamo* Nandisena imprime «para kamo (§25)»
—§25 es *Dīghaṃ*; el acortamiento es §26—; el español ya lo tenía bien y el
inglés lo sigue. Y en §28 la lista de *cātuddasiṃ* del español tenía los
pasos sin numerar; corregido.

**Sandhi español pasa a v1.5** (nota de versión con lo de esta sesión); el
inglés nace en v1.0.

## 4. AVISOS TÉCNICOS

- **Las notas de los versos introductorios (n. 1–3) no aparecen en el
  bloque «Ver notas»**, sólo como emergentes. Es comportamiento previo del
  generador (ya pasaba con la antigua n. 1); no se ha tocado.
- **Un `<!-- DUDA -->` dentro de una nota al pie se publica escapado y
  visible.** Se comprobó y se retiraron los dos que se habían puesto; las
  DUDAs de esta sesión están en la tabla de arriba y en la guía §5.1 sexies,
  no en el maestro.
- `(S. 408)` en §14 no recibe emergente: la edición base no da tomo y el
  generador exige uno. Se deja como lo imprime Nandisena.
- `(Khu. i, 27, 358)` y `(Khu. i, 11, 301)` — dos páginas — reciben el
  emergente genérico «Khuddaka-nikāya», sin tomo ni página. Es el
  comportamiento de `RE_CITA_SIMPLE`; aceptable.
- Se ejecutó `generar_todo.py`; el hook lo repetirá al confirmar.

## 5. CÓMO SEGUIR

0. **Angel revisa la página inglesa entera** y el registro §5 del memorando.
   Lo que corrija, en `01-sandhi-kappa.en.md`; se regenera con
   `generar_todo.py`.

1. Angel revisa el diff de `kaccayana/01-sandhi-kappa.md` (las 156 citas en
   línea, las 6 reposiciones, las 6 erratas) y confirma.
2. Angel resuelve la tabla de §3 y entrega la página del Venerable (§1.5).
3. Con eso: glosario inglés cerrado → `sandhi.en.md`, un sutta cada vez,
   como siempre → generador con idioma → botón EN/ES.

## 6. ARCHIVOS

| Archivo | Qué |
| --- | --- |
| `kaccayana/01-sandhi-kappa.md` | citas en línea, 35 notas, omisiones repuestas, erratas corregidas |
| `comun/guia-de-estilo.md` §5.1 sexies | la regla y su historia |
| `herramientas/generar_capitulo.py` | cuatro siglas más en `ABREVIATURAS` |
| `docs/ingles/memo-sandhi-en-glosario-y-desviaciones.md` | memorando (en inglés) |
| `docs/fuentes/nandisena-apendice-sandhi-en.md` | apéndice del Venerable, verbatim |
| `comun/terminologia-particulas.md` | cita *Kaccāyanavaṇṇanā* 31 |
| `comun/convenciones.md` §1 bis | locativo = «sigue», ablativo = «después», sin corchetes |
| `kaccayana/01-sandhi-kappa.en.md` | **la edición inglesa del Sandhi, entera, sin revisar** |
| `herramientas/generar_capitulo.py` | `IDIOMAS`, `L`, `ruta_salida`, `datos_version`, botón y `hreflang`, versión 1.5 / 1.0 |
| `herramientas/generar_todo.py` | genera el `.en.md` y regenera el español |
| `site/assets/pali.js` | cadenas por `CAP.textos` |
| `comun/guia-de-estilo.md` §9 | la edición inglesa, lo práctico |
| `CLAUDE.md` | «La edición inglesa» y la orden de generación |
| `site/en/kaccayana/sandhi/index.html` | la página inglesa |
| `site/**` | regenerado |
