# Rediseño de la navegación · etapa 4b: un solo aspecto para los recursos

Pedido del IEBH, 2026-10-08. Etapas anteriores: `etapa-1-cabecera.md`,
`etapa-2-hub.md`, `etapa-3-tarjetas.md`, `etapa-4a-busqueda.md`. Es la última
etapa del rediseño. Sólo cambia el ASPECTO y la ESTRUCTURA de las trece páginas
de recursos: ninguna herramienta cambia lo que hace.

Las trece: `/recursos/` (índice), análisis y su guía, clasificación, casos,
comentarios, glosario, raíces, paradigmas, sandhi, solucionador, nombre y
verbo. Hasta aquí usaban tres sistemas de cromo distintos, con el CSS copiado
de plantilla en plantilla.

## Piezas

| Pieza | Qué es | Fuente o salida |
| --- | --- | --- |
| `site/assets/base.css` | la paleta «hoja de palma» (clara, oscura y la del sistema), las tres familias de letra, el fondo, la marca del IEBH y la etiqueta «borrador» | fuente (a mano) |
| `site/assets/recursos.css` | el cromo común de los recursos: bloque del título, índice lateral y su ☰, barra de mandos, botones, filtros, tablas que ruedan, globo, ↑ y pie | fuente (a mano) |
| `herramientas/recursos_comun.py` | escribe el marcado del bloque del título y del pie a partir de `<rc-titulo>` y `<rc-pie>` | herramienta |
| `herramientas/cabecera.py` | enlaza `base.css` en todas las páginas y `recursos.css` en las de recursos; llama a `recursos_comun.componer()` | herramienta |

### Una sola fuente para la paleta y la letra

Los valores de la paleta están **sólo** en `base.css`, con los nombres de
`pali.css` (`--bg`, `--bg2`, `--text`, `--text2`, `--border`, `--accent`,
`--haritala`, `--rakta`…). Se fueron de `pali.css`, de `cabecera.css` (que los
repetía con prefijo `cab-`) y de las doce plantillas, que los repetían con
nombres propios (`--ola`, `--ink`, `--soot`, `--hair`, `--nila`, `--chip-k`):
esos nombres se cambiaron en el CSS de cada plantilla por los comunes.

Los tres mecanismos de tema siguen como estaban: `body.dark` (capítulos,
páginas de sutta, índices, búsqueda), `html[data-theme=dark]` (recursos) y el
del sistema en nombre y verbo mientras el lector no elija (su barra lleva
`data-tema="medio"`). Las claves `pali_dark` y `pali_lang` no cambian.

Las tres familias: Gentium Book Plus, Inter y JetBrains Mono, pedidas una sola
vez por `cabecera.insertar()` para todo el sitio (`FUENTES`). Los generadores
de capítulos, páginas de sutta, índices, búsqueda y prosa ya no piden las
suyas, y las plantillas tampoco. Nombre y verbo dejan Fraunces, Spectral e IBM
Plex Mono; el glosario deja IBM Plex Sans. Sólo el análisis y su guía piden
además Padauk, la letra birmana de las citas del libro.

`cabecera.comprobar_tokens()` (lo llama `generar_secciones.py` en cada
regeneración) falla si un color de la paleta vuelve a aparecer en otra hoja de
`site/assets/` o en el `<style>` de una plantilla de recursos. Excepción: los
bloques `@media print`, cuyos colores no dependen del tema.

`base.css` y `recursos.css` van ANTES de las hojas y estilos de cada página:
lo propio de una página (un tamaño, un margen) las ajusta sin pelear.
`cabecera.css` sigue al final.

### El bloque del título y el pie: una sola fuente para el marcado

En cada plantilla, lo que la página dice queda en unas etiquetas de trabajo
que nunca llegan al sitio:

    <rc-titulo>
      <rc-volver href="../">← …</rc-volver>   (sólo la guía)
      <rc-ceja>…</rc-ceja>                    junto al árbol del IEBH
      <rc-h1>…</rc-h1>
      <rc-sub>…</rc-sub>                      (análisis, glosario, raíces)
      <rc-desc>…</rc-desc>                    la descripción de una línea
      <rc-insignias>…</rc-insignias>          «borrador» y versión
      <rc-lado>…</rc-lado>                    la muestra de la derecha
      <rc-debajo>…</rc-debajo>                leyendas, «Cómo leer…»
    </rc-titulo>

    <rc-pie>
      <rc-notas>…</rc-notas>                  «Notas, cifras y fuentes», plegado
      <rc-licencia>…</rc-licencia>            con el imagotipo del IEBH
      <rc-extra>…</rc-extra>                  lo demás, donde vaya
    </rc-pie>

`recursos_comun.componer()` las cambia por el marcado común
(`header.rc-titulo`, `footer.rc-pie`); los atributos (`id`, `data-t`,
`i-es`/`i-en`) pasan al elemento que las sustituye, de modo que la lógica de
cada página los encuentra donde los buscaba. Una etiqueta de trabajo que se
quede sin componer detiene la generación. `/recursos/` usa las mismas
etiquetas desde `generar_indices.py`.

## El índice lateral: un patrón, un ☰

Las páginas con secciones (análisis, clasificación, casos, comentarios,
glosario, raíces, paradigmas, sandhi, verbo) llevan el mismo índice y el mismo
☰, en el mismo sitio:

- **Pantalla ancha (> 900 px):** el ☰ está en la esquina de arriba a la
  izquierda del índice. Al plegarlo, otro ☰ fijo (`#volver-barra`) queda
  exactamente en ese sitio. El ☰ de la barra de mandos no se ve.
- **Pantalla estrecha:** el índice es un cajón. El ☰ es el primero de la barra
  de mandos, que es pegajosa; con el cajón abierto lo cierran el ☰ de su
  esquina, el velo y Escape.

Cambios de lógica, todos del cromo: análisis, clasificación, casos y
comentarios ganan el `#volver-barra` (antes había que ir al ☰ de la barra);
el glosario pliega con `html.sin-barra` como los demás (antes `body.sin-barra`
y un relleno por bloque) y **gana el cajón en el teléfono**, donde antes el
índice desaparecía; el verbo pasa de `body.sin-indice`/`con-indice` a lo mismo
que los demás, y su ☰ «Índice» de la cabecera pasa a la barra de mandos, que
ahora tiene (con su buscador). «Desplegar / Plegar», donde los había, con un
solo estilo (`.sb-tools`, `.rc-plegar`). La medida de la barra pegajosa se
rehace al cambiar su alto (`ResizeObserver`, como ya hacía el análisis): en
el teléfono un enlace profundo quedaba algún píxel bajo la barra.

Nombre, solucionador y la guía del análisis no tienen secciones: no llevan
índice.

## «borrador», igual en todas partes

Una sola clase, `.borrador` (en `base.css`): en las tarjetas de la portada y
de `/recursos/`, en el bloque del título de análisis, clasificación, casos,
comentarios y la guía, en los resultados de `/buscar/` y en las páginas de
cada sutta (antes `.ini-borrador`, `.badge-b` o la palabra dentro de la
insignia). Donde la insignia de versión decía además «borrador» (análisis,
casos, `/recursos/`), lo dice ahora la etiqueta y la insignia se queda con la
versión.

## La caja de búsqueda de la portada

Pedido del IEBH en esta misma etapa: la portada (`/` y su vista inglesa) ya
no lleva la caja grande de búsqueda; la de la barra común, en todas las
páginas, es la única. Su explicación («Un número lleva a la página de ese
sutta… se busca en los suttas, el glosario, las raíces, los paradigmas y los
recursos») está ahora arriba de `/buscar/` y `/en/buscar/`
(`generar_busqueda.py`, `.busca-intro`), con el número de suttas publicados.

## Diferencias que se ven (las buscadas)

- Mismo bloque del título en todas: ceja con el árbol, h1 de 34–52 px,
  descripción, insignias. Sandhi y solucionador pierden su h1 gigante; el
  glosario, su franja de fondo; raíces lleva las tres obras en el subtítulo
  común.
- Nombre y verbo pasan a la hoja de palma y a las tres familias; el ocre de
  sus acentos es ahora el oropimente (`--haritala`). Nombre gana la línea de
  descripción (la de su `<meta name="description">`) y la insignia de versión.
- El ☰ en el mismo sitio en todas (arriba).
- La insignia de versión, en píldora nīla en todas; el ES|EN y el tema de cada
  página siguen ocultos (los acciona la barra común).
- Los grupos de filtros que no caben en el teléfono se parten en filas en vez
  de salirse.
- La sombra común es `rgba(0,0,0,.06)` (el análisis usaba .08; las demás .05).

## Peso

| Página | Antes | Después | gzip antes → después |
| --- | ---: | ---: | --- |
| glosario | 1.535.131 | 1.526.502 | 389.066 → 386.638 |
| raíces | 1.226.385 | 1.215.160 | 204.622 → 201.828 |
| análisis | 890.770 | 880.623 | 231.234 → 229.224 |
| paradigmas | 177.537 | 163.674 | 50.206 → 46.353 |

`base.css` (7 KB, 2,9 KB gzip) y `recursos.css` (21 KB, 5,7 KB gzip) se piden
una vez y quedan en caché.

## Pendiente o para decidir

- La búsqueda de dentro de `/recursos/verbo/` no encuentra nada, antes y
  después de esta etapa: al armar su índice, `inf.tabla` llega sin definir
  para alguna inflexión y el guion se detiene (`TypeError … reading 'slice'`).
  No es del aspecto; va aparte.
