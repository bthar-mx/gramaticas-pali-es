# Rediseño de la navegación · etapa 1: cabecera común, «Ir a §» y portada

Diseño aprobado por el IEBH el 2026-10-08 (lienzo «Gramáticas Pāḷi —
navigation redesign», mesas de trabajo 1, 3 y 4; la 2, el § hub, es la
etapa 2). Esta nota recoge cómo está hecho y qué se quitó.

## Piezas

| Pieza | Qué es | Fuente o salida |
| --- | --- | --- |
| `herramientas/cabecera.py` | marcado de la barra, tabla `PAGINAS`, `insertar()`, `version_assets()`, comprobación de la paleta | fuente |
| `site/assets/cabecera.css` | estilos de la barra; repite la paleta «hoja de palma» de `pali.css` con prefijo `cab-` | fuente (a mano) |
| `site/assets/cabecera.js` | idioma, tema, menú del teléfono, «Ir a §» | fuente (a mano) |
| `herramientas/generar_secciones.py` | escribe `site/assets/secciones.json` (mapa §N → capítulo) | generador |
| `site/assets/secciones.json` | 405 §§, sólo los que tienen ancla `id="sN"` en el HTML publicado | salida |

`version_assets()` vive ahora en `cabecera.py` y huele los cuatro archivos
(`pali.css`, `pali.js`, `cabecera.css`, `cabecera.js`): un solo `?v=` para
todo el sitio. `generar_capitulo.version_assets()` la llama.

`generar_secciones.py` va en `generar_todo.py` tras los capítulos (lee sus
anclas) y antes de `generar_indices.py` (la portada toma de él los rangos) y
de `generar_seo.py`. Falla si la paleta de `cabecera.css` deja de coincidir
con la de `pali.css`.

## La barra acciona lo que cada página ya tenía

No hay mecanismo nuevo de idioma ni de tema. Los mandos de cada página siguen
en el DOM, ocultos con un `<style>` que pone `insertar()`, y la barra los
pulsa:

| Páginas | Idioma | Tema |
| --- | --- | --- |
| capítulos (ES y EN) | `#lang-btn` (enlace a la otra URL; guarda `pali_lang` y conserva el `#ancla`) | `#dark-btn` → `body.dark` |
| portada, /kaccayana/, /recursos/ | `#lang-btn` → `body.en` | `#dark-btn` → `body.dark` |
| solucionador, paradigmas, raíces | `#en-btn` | `#theme` → `html[data-theme]` |
| glosario | `#b-es` / `#b-en` | `#theme` (clave propia `tema`) |
| verbo | `#langToggle` | `#themeToggle` (sistema si no se eligió) |
| clasificación, análisis, su guía, comentarios | `#lang-btn` | `#theme` |
| sandhi, casos | **Solo en español** | `#theme` |
| nombre | **Solo en español** | `#themeToggle` |
| guía de las clases | **Solo en español** (ya no arranca en inglés) | `#dark-btn` |

Las páginas sólo en español muestran en el sitio del conmutador un rótulo
fijo «Solo en español», no un botón deshabilitado ni nada que dependa de
pasar el ratón.

Desde los capítulos ingleses, Kaccāyana, Recursos, Glosario y la marca
llevan `?lang=en`: la portada, los tres índices y el glosario lo entienden
ahora como lo entendían ya el análisis y la clasificación (manda sobre lo
demás y no se guarda). Era el «←» de esos capítulos, que llevaba a la URL
española.

## «Ir a §»

Un número del 1 al 405 lleva a `/kaccayana/<capítulo>/#sN` (o a `/en/…` si
la página está en inglés y el capítulo tiene edición inglesa). Un número sin
§ publicado da «§406 aún no está publicado» / «§406 is not published yet»,
nunca un enlace muerto. El destino sale de una sola función,
`destinoSutta()` en `cabecera.js`, para que la etapa 2 lo lleve a `/s/N/`.

En la portada, la caja grande usa la misma función. Una palabra no se busca
—no hay todavía búsqueda en todo el sitio— y la caja lo dice: «La búsqueda en
todo el sitio llega en una etapa posterior», con el enlace a los recursos.

## Lo que se quitó (porque la barra lo hace)

- **Capítulos (10 páginas):** el enlace «← Kaccāyana-Byākaraṇaṃ» de la
  cabecera. Ocultos, no quitados: el 🌓 flotante (`#dark-btn`) y el ES|EN de
  la línea de metadatos (`#lang-btn`), que la barra pulsa. La línea de
  metadatos no cambia, de modo que la descripción que saca de ella
  `generar_seo.py` tampoco.
- **/kaccayana/, /recursos/, /guia-clases/:** el enlace «← Gramáticas Pāḷi».
  Ocultos: el ◐ flotante y el ES|EN de la línea de la marca.
- **Portada:** rehecha según la mesa de trabajo 1. Desaparecen la tarjeta
  «Material de apoyo» y las dos tarjetas de clases, sustituidas por los tres
  grupos de recursos y el bloque de clases. El ◐ y el ES|EN, ocultos.
- **Once páginas de recursos** (análisis, casos, clasificación, comentarios,
  glosario, nombre, paradigmas, raíces, sandhi, solucionador, verbo): el
  enlace «← Recursos · Gramáticas Pāḷi». En verbo, además, la línea del guion
  que le ponía el texto. Ocultos: sus botones de tema y de idioma.
- **La guía del análisis** conserva su «← Análisis de los suttas de
  Kaccāyana»: la barra no lleva ahí.
- `generar_recurso.py` (hoy no publica ninguna página): «← Recursos».

Se conservan los encabezados propios de cada página, con la marca del IEBH:
el bloque del título del capítulo, las pastillas de kaṇḍa, los buscadores y
las barras laterales.

## Lo que se movió para que la barra no tape nada

La barra es fija (`position: fixed`, 56 px, `--cabecera-h`), con un hueco
`.cab-hueco` detrás. Fija y no «sticky» porque varias páginas de recursos
dejan sitio a su índice con `padding-left` en el `<body>`, y una barra en el
flujo empezaba a 238 px del borde. Bajan `--cabecera-h`:

- `pali.css`: `#toc`, `.kanda-nav`, `#pbadge`, `#toc-volver` y el globo de
  `.toc-ocultar`;
- plantillas de recursos: `.sidebar`, la `.bar` pegajosa, `#volver-barra`,
  la cabecera fija de la tabla del análisis y los `scroll-padding-top`
  propios (análisis, casos, clasificación, comentarios).

`cabecera.css` pone `scroll-padding-top: var(--cabecera-h)` con
especificidad cero, para que los `#sN` queden bajo la barra donde la página
no tenía el suyo.

## Números que ahora salen de los datos

- Portada: rangos de § de cada capítulo y el total (§1–§405), de
  `comun/concordancia.json`; recuentos de raíces, reglas y formas de sandhi,
  paradigmas del verbo; rangos de la clasificación y del análisis.
- /recursos/: la descripción de los paradigmas decía «83» a mano y la
  insignia contaba 85; ahora las dos dicen el número de los datos (85).
  La insignia del análisis toma capítulos y rango de sus datos, no de la
  «etiqueta» escrita a mano en `meta.json`.
- La tarjeta de Paradigmas de la portada lleva el texto del IEBH del
  2026-10-08: «Declinación nominal y pronominal · *vibhatti-paccaya*,
  sufijos-inflexiones».

## Pendiente o para decidir

- El glosario guarda el tema con su clave propia `tema`, no con `pali_dark`
  (era así antes de esta etapa): la barra lo acciona bien, pero el tema
  elegido allí no viaja al resto del sitio ni al revés.
- Etapa 2: el § hub (`/s/N/`) y llevar allí `destinoSutta()`.
- Etapa 3: la fila de enlaces de cada tarjeta de sutta.
