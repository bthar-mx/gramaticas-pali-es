# Rediseño de la navegación · etapa 4a: búsqueda en todo el sitio y tema del glosario

Pedido del IEBH, 2026-10-08. Etapas anteriores: `etapa-1-cabecera.md`,
`etapa-2-hub.md`, `etapa-3-tarjetas.md`. La etapa 4b (un aspecto común para
las páginas de recursos) va aparte.

## 1. La búsqueda

### Piezas

| Pieza | Qué es | Fuente o salida |
| --- | --- | --- |
| `herramientas/generar_busqueda.py` | escribe el índice y las dos páginas | generador |
| `site/assets/busqueda-es.json`, `busqueda-en.json` | el índice, uno por lengua | salida |
| `site/buscar/index.html`, `site/en/buscar/index.html` | la página: una caja y la lista | salida |
| `site/assets/buscar.js` | la búsqueda en el navegador | fuente (a mano) |
| `.busca*` en `site/assets/pali.css` | estilos de la página | fuente (a mano) |

`generar_busqueda.py` va en `generar_todo.py` después de `generar_hub.py`
(lee sus páginas y el glosario ya publicado) y antes de `generar_indices.py`
y `generar_seo.py`. Tarda alrededor de 1 s. Es determinista.

### Qué entra, y de dónde

Se lee lo YA PUBLICADO, o los datos que la página publica tal cual, para que
la búsqueda no encuentre nada que el sitio no enseñe:

| Grupo | Entradas | De dónde | Dirección |
| --- | ---: | --- | --- |
| Suttas | 405 | las páginas `/s/N/` (`/en/s/N/`): §N, el sutta en pāḷi, la línea de traducción; como claves que no se enseñan, las palabras pāḷi del bloque del sutta (vutti y ejemplos) y de su desglose | `/s/N/` |
| Glosario | 2.122 | las fichas de la vista alfabética del glosario publicado: el lema y su traducción (la lista normativa; si no, Nandisena; si no, Smith; en inglés, lo que la página publica en inglés) | `/recursos/glosario/#g-<id>` |
| Raíces | 1.698 | `recursos/raices/raices.json`: raíz y significado, con la glosa pāḷi como clave | `/recursos/raices/#r<id>` |
| Paradigmas | 86 | `paradigmas.json` (y `ingles.json`, adjudicado): código, nombre y género | `/recursos/paradigmas/#<código>` |
| Recursos | 11 | `generar_indices.recursos_descritos()`: título y línea de cada recurso, los mismos de la portada | `/recursos/<x>/` |

Las anclas ya existían en las tres páginas (`#g-…`, `#r…`, `#<código>`) y
todas llevan a la ficha al cargar; no hubo que añadir ninguna ni tocar lo que
las páginas enseñan. En inglés, las páginas que entienden `?lang=en`
(glosario, análisis, clasificación, comentarios) lo llevan en la dirección.

El texto corto de una ficha del glosario se corta a 110 caracteres; la
definición entera está en la página. No va texto entero de ningún capítulo.

### Borradores

Análisis, clasificación, casos y comentarios: **ni una palabra de su texto**
en el índice. Entran sólo por el título de la página, rotulados «borrador»,
sin su línea descriptiva. La clasificación y el análisis, que tienen una fila
por §, entran además por su número: el índice lleva su título y los § que
cubren (`"borradores"`), y al buscar un número `buscar.js` arma «§N ·
Clasificación de los suttas» y «§N · Análisis según Visuddhāyuṃ», con el
rótulo, detrás de la página del sutta.

### Tamaño

ES 492 KB, EN 501 KB (unos 130 KB comprimidos). Se descarga sólo al buscar.

### Cómo busca

- `norm()` en `buscar.js` y en `generar_busqueda.py`, la misma regla:
  minúsculas, sin diacríticos (ā = a, ṃ = m, ñ = n, ŋ = n…), sin la
  puntuación que quita `plegar()` de `pali.js` («§290» → «290»,
  «Sattamī-atthe» → «sattamiatthe»), y lo demás que no es letra ni cifra a
  espacio. Las claves del índice van ya normalizadas; el título y el texto se
  normalizan en el navegador al cargar el índice.
- Varias palabras: han de estar todas, en cualquier orden.
- Orden dentro de cada grupo: coincidencia exacta con el título (sin §N,
  código ni paréntesis) delante; luego al principio del título, al principio
  de una palabra del título, dentro del título, y por último en el texto o las
  claves. Un poco por delante lo que coincide con los diacríticos tal como se
  escribieron (bhū antes que bhu). Un número pone primero ese §.
- 20 por grupo y «Ver N más». La búsqueda queda en la dirección (`?q=`). Sin
  resultados, lo dice y sugiere probar sin diacríticos o con un número de §.
- Teclado: ↓ de la caja a los resultados, ↑ ↓ entre ellos, Esc a la caja.
  Los resultados son enlaces de verdad.

### La caja de la barra y la de la portada

Un número sigue yendo a `/s/N/` por `destinoSutta()`, sin cambios. Lo demás
va a `/buscar/?q=…` (o `/en/buscar/` si la página está en inglés), con
`destinoBusqueda()` en `cabecera.js`. La caja de la barra ya no pide teclado
numérico (se quitó `inputmode="numeric"`), dice «Buscar…» / «Search…» detrás
del «§», y es un poco más ancha para que quepa. La portada perdió la nota de
que la búsqueda de palabras «llega en una etapa posterior»: su rótulo y su
ejemplo (`290 · kāraka`) dicen ahora que sirve para las dos cosas.

### noindex

Las dos páginas llevan `<meta name="robots" content="noindex"/>`:
`generar_seo.py` no les pone canónica y no entran en `sitemap.xml`, que sigue
con 831 direcciones. En `cabecera.py`, entrada `buscar` de `PAGINAS` (dos
URL, como las páginas de sutta); su ES|EN conserva la búsqueda (`?q=`).

## 2. El tema del glosario

El glosario guardaba el tema con su clave propia `tema` (`dark`/`light`), de
modo que lo elegido allí no viajaba al resto del sitio ni al revés. Ahora lee
y escribe `pali_dark` (`1`/`0`), como paradigmas y raíces. Si al cargar queda
una `tema` vieja, se pasa una vez a `pali_dark` —salvo que el lector ya haya
elegido en otra página, que manda— y se borra. Nada más cambia en el
glosario.
