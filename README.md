# Gramáticas Pāḷi — Traducciones al español

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21948010.svg)](https://doi.org/10.5281/zenodo.21948010)

Traducciones al español de las gramáticas clásicas de la lengua pāḷi,
con glosario terminológico común y concordancia entre las obras.

Un proyecto del Instituto de Estudios Buddhistas Hispano (IEBH).

## Contenido

| Ruta         | Contenido                                                      |
| ------------ | -------------------------------------------------------------- |
| `kaccayana/` | Kaccāyana-byākaraṇa — texto pāḷi y traducción española          |
| `comun/`     | glosario, convenciones, guía de estilo y concordancia          |
| `site/`      | sitio publicado (HTML) — **salida**, no fuente                 |

Obras previstas: Nyāsa, Padarūpasiddhi, Saddanīti, Nirutti-dīpanī.
Las carpetas se crearán cuando haya texto que colocar en ellas.

El markdown de `kaccayana/` es la fuente de verdad. El HTML de `site/` es la
presentación de ese texto: se corrige en el markdown y se vuelve a generar,
nunca al revés.

## Convenciones

El glosario es normativo: un término pāḷi se traduce siempre igual en todas
las obras de este repositorio. Ver `comun/convenciones.md` antes de traducir.

Los suttas se citan por el número secuencial de Kaccāyana (`§30`), que es
también el ancla permanente de cada sutta en el sitio (`#s30`). Las
concordancias con Padarūpasiddhi y Saddanīti-Suttamālā están en
`comun/concordancia.json`.

## Publicación

El sitio se sirve en <https://gramaticas.buddha-dhamma.net> desde Cloudflare
Workers (assets estáticos), conectado a este repositorio. Cada `git push` a
`main` publica.

La configuración está en `wrangler.jsonc`: se publica únicamente `./site`.
El markdown de `kaccayana/` y los documentos de `comun/` quedan en el
repositorio pero no se sirven.

Sin paso de compilación: los HTML son estáticos y no hay dependencias que
instalar.

Rutas: `/kaccayana/` índice de la obra, `/kaccayana/sandhi/` capítulo 1.
Los estilos y la lógica compartidos están en `site/assets/`; cada capítulo
define sus propios datos en `window.PALI_CAPITULO` antes de cargar `pali.js`.

## Licencia

Copyright © 2026 Instituto de Estudios Buddhistas Hispano (IEBH).

El texto pāḷi, la traducción española y los documentos de este repositorio se
publican bajo [Creative Commons Atribución-NoComercial-SinDerivadas 4.0
Internacional](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.es)
(CC BY-NC-ND 4.0). El texto legal completo está en `LICENSE`.

Este material puede ser reproducido para uso personal y distribuido de forma
gratuita.

Dos precisiones sobre el alcance:

- **Las marcas no van en la licencia.** El logotipo y el nombre del IEBH son
  marca, y la sección 2(b)(2) de la licencia deja fuera los derechos de marca
  y de patente. Reproducir el texto no autoriza a usar la marca.
- **Las obras ajenas conservan la suya.** El Digital Pāḷi Dictionary, que el
  solucionador consulta como testigo de ocurrencia, se publica bajo
  CC BY-NC-SA y no cambia de licencia por aparecer aquí. Lo mismo vale para
  el material tomado de Ven. A. Thitzana, de Rūpasiddhi y del Nyāsa, señalado
  como suyo en cada caso.

## Textos relacionados

Corpus del Sexto Concilio: <https://buddha-dhamma.net\> ·
<https://github.com/bthar-mx/OSBCT\>

