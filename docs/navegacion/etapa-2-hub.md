# Rediseño de la navegación · etapa 2: la página de cada sutta (§ hub)

Diseño aprobado por el IEBH el 2026-10-08 (lienzo «Gramáticas Pāḷi —
navigation redesign», mesas de trabajo 2 y 4), con sus decisiones del mismo
día. Etapa 1: `etapa-1-cabecera.md`.

## Qué hay

Una página por § con tarjeta publicada: `/s/N/` (español) y `/en/s/N/`
(inglés), N = 1–405. 810 páginas, todas indexadas y en `sitemap.xml`. Las
escribe `herramientas/generar_hub.py`, que va en `generar_todo.py` después de
los capítulos y de los recursos y antes de los índices y de `generar_seo.py`
(que les pone la canónica y la pareja hreflang). Tarda unos 1,7 s; el
`generar_todo.py` entero, unos 7 s.

Dos URL por sutta, como los capítulos: la misma redirección por
`pali_lang`, y el ES|EN de la cabecera común pasa de una a otra con su
`#ancla` (entrada `hub` de `PAGINAS` en `cabecera.py`, modo «enlace»).

## De arriba abajo

1. Migas (Inicio › Kaccāyana › capítulo › kaṇḍa › §N) y § anterior y
   siguiente, con su título pāḷi; cruzan de capítulo (§51 → §52) y no hay
   anterior a §1 ni siguiente a §405.
2. §N, el sutta en pāḷi (`pali` de `comun/concordancia.json`) y la línea de
   traducción del capítulo.
3. Los números, en texto (la etapa 3 los enlazará): Kaccāyana, Rūpasiddhi,
   Saddanīti si lo hay, capítulo y kaṇḍa.
4. «Texto y traducción»: lo que enseña la tarjeta del capítulo, con las
   MISMAS funciones de `generar_capitulo.py` (`parsear`, `bloque_pali`,
   `parrafos`, `inline`), todo desplegado. Diferencias, y por qué:
   - **sin las notas al pie** (lo dice la propia página): en la tarjeta son
     un globo y un bloque plegable que maneja `pali.js`, y aquí no se carga;
   - las glosas emergentes `{término|glosa}` van a la vista, entre
     paréntesis: sin `pali.js` no se abrirían con el dedo;
   - los §N del texto llevan a la página de ese sutta (`../N/`), no al ancla
     del capítulo;
   - las citas canónicas conservan la sigla desatada como `title`.
   Y «Leer en el capítulo →» lleva a `/kaccayana/<capítulo>/#sN`.
5. «Dónde se cita»: generado. Cuenta un enlace de una página publicada a la
   tarjeta `/kaccayana/<capítulo>/#sN` (o `/en/…`), fuera de la página de ese
   capítulo. Se encuentran de dos maneras:
   - en el HTML publicado, todo `<a href>` que resuelva ahí, y las direcciones
     ya hechas que una página lleva en sus datos (`"href": "…#s83"` del
     verbo). En un capítulo, la cita se nombra por la tarjeta que la contiene
     y lleva a la página de ese sutta;
   - las páginas que arman el enlace en el navegador se leen con la misma
     regla que su guion, sobre los mismos datos: sandhi (secuencias
     `verificada`, `kac_seq`), paradigmas (referencias «§N» de los sufijos) y
     casos (los aforismos de cada uso por la concordancia de la página).
   De cada página sólo se toma el título y el texto visible del enlace. No
   entran el solucionador (sus enlaces dependen del pasaje que pegue el
   lector) ni los globos de términos, que sólo viven en páginas de borrador.
   Si un § no tiene ninguna, la sección no sale. Hoy la tienen 102.
6. Los dos borradores, **sólo como enlace**, con su rótulo: «Clasificación
   del sutta (borrador) →» a `/recursos/clasificacion/#sN` y «Análisis según
   Visuddhāyuṃ (borrador) →» a `/recursos/analisis/#sN`. Nada de su texto
   (decisión del IEBH: el contenido de borrador se queda en las páginas de
   borrador). `herramientas/comprobar_hub_borradores.py` lo comprueba.
7. «Preguntar sobre §N»: véase abajo.

## «Preguntar»: enlace al diálogo del análisis, no una copia

El diálogo vive dentro del guion del análisis y depende de su estado (las
cadenas `T`, la fila `F` del §, `render()` y la lengua de la página), y el
worker responde con la fila del análisis —un borrador— como contexto. Sacarlo
a un archivo común obligaba a rehacer el guion de una página de borrador, y
enseñar la respuesta aquí era enseñar, en una página indexada, algo basado
en esa fila sin la fila delante. Así que:

- la página del sutta hace la MISMA sonda (`GET /api/preguntar?json=1`,
  `redirect:'manual'`) y dice si hay sesión («Le quedan hoy N preguntas») o
  ofrece iniciarla (`/api/preguntar`);
- el botón lleva a `/recursos/analisis/?preguntar=N#sN` (con `&lang=en` en
  inglés), y el análisis, si la sonda dice que hay sesión, abre esa fila y el
  diálogo de ese §. El POST es el de siempre, `{sutta, pregunta, lang}`; el
  worker no cambia.

## «Ir a §»

`destinoSutta()` (`cabecera.js`) devuelve ahora `/s/N/` o `/en/s/N/`. La caja
grande de la portada usa la misma función. §406 en adelante sigue diciendo
«aún no está publicado». Los capítulos no cambian: conservan sus anclas
`#sN` y todos sus enlaces.
