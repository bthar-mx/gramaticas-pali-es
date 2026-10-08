# Rediseño de la navegación · etapa 3: las tarjetas apuntan a las páginas de sutta

Diseño aprobado por el IEBH el 2026-10-08 (lienzo «Gramáticas Pāḷi —
navigation redesign», mesa de trabajo 3), más tres arreglos pedidos el mismo
día. Etapas anteriores: `etapa-1-cabecera.md`, `etapa-2-hub.md`.

## 1. Fila de enlaces en cada tarjeta

En las diez páginas de capítulo (ES y EN), dentro del cuerpo de cada tarjeta y
justo encima de su pie («Estudiado · Enlace · Copiar §»):

| Enlace | Destino |
| --- | --- |
| Todo sobre §N | `../../s/N/` (en inglés, `/en/s/N/`) |
| Clasificación (borrador) | `/recursos/clasificacion/#sN` (`?lang=en` en inglés) |
| Visuddhāyuṃ (borrador) | `/recursos/analisis/#sN` (ídem) |
| Preguntar | `/recursos/analisis/?preguntar=N#sN` (`&lang=en` en inglés) |

Enlaces llanos, sin texto de los borradores. Sólo salen los de las filas que
existen: `generar_capitulo.filas_borrador()` lee los § de
`recursos/clasificacion/datos.json` y de `recursos/analisis/datos/`; hoy los
dos cubren §1–§405. La fila la arma `generar_capitulo.fila_enlaces()`.

Dianas de 44 px con el dedo y a ancho de teléfono (32 px con ratón, para que
la tarjeta siga siendo compacta); la fila se parte. `pali.js` la deja fuera
de la búsqueda del capítulo (`textoBuscable`): si no, «preguntar» encontraría
todas las tarjetas. La copia del sutta y el EPUB no la ven (leen sus propios
bloques). No toca la línea «hdr-meta», de la que `generar_seo.py` saca la
descripción de los capítulos.

## 2. Rū y Sad legibles sin pasar el ratón

Los números de Rūpasiddhi y de Saddanīti de la cabecera de la tarjeta sólo se
explicaban con un globo, y con el dedo los globos no se abren
(`@media (hover: none)` en `pali.css`). Ahora cada tarjeta lleva una línea
`.sutta-concord` («Rū 298 · Sad 602») que sólo se ve en pantallas sin ratón;
con ratón quedan los globos. No son enlaces: no hay todavía página de
Rūpasiddhi ni de Saddanīti.

## 3. «Kāraka-Kappa», sin el número delante

En las páginas de sutta (migas, números, descripción y «Dónde se cita») y en
el título del índice lateral de los capítulos sale el nombre sin el número
del archivo («Kāraka-Kappa», no «3-Kāraka-Kappa»): el número ya está en
«capítulo 3 de 8». No cambian archivos, anclas, `<title>` ni la cabecera del
capítulo.

## 4. «85 paradigmas» en todo el sitio

`paradigmas.json` tiene 86 entradas en 84 documentos: 85 paradigmas de
declinación y la tabla de los sufijos que son inflexiones; dos documentos
llevan dos paradigmas cada uno (GO: *go* masculino y femenino; NUMERALES:
cardinales y ordinales), de modo que los 85 paradigmas proceden de 83
documentos. `generar_paradigmas.cuenta()` saca las dos cifras de los datos y
las pone en la página (descripción y «Fuente», ES y EN); la portada y
/recursos/ usan la misma función.

Quedan las cifras viejas en tres briefings fechados (sesiones 16, 17 y 32),
que registran lo que había entonces; no se han tocado.
