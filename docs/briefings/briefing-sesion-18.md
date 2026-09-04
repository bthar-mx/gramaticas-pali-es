# Kaccāyana Pāḷi-Español: Briefing de la Sesión 18

*Complementa a los briefings 05–17. La sesión 18 no tocó ni una forma pāḷi:
fue toda de interfaz. Hizo táctil la página de paradigmas, arregló los saltos
largos en todo el sitio, incorporó la marca del IEBH y empezó a unificar la
tipografía. **Lo primero que toca hacer es terminar esa unificación: Gentium
Book Plus en todo el proyecto, sección 6a.** La URL corta sigue abierta.*

---

## 1. ESTADO AL CIERRE

Todo commiteado y empujado. Último commit: `b787aec`. Cinco commits de la
sesión, en este orden:

| Commit | Qué hizo |
| ------ | -------- |
| `bd96c2c` | paradigmas v1.9 — capa táctil |
| `958c857` + `2c5d398` | saltos inmediatos (paradigmas v1.10, sandhi v3.6, capítulos) |
| `776c81f` | marca del IEBH: pie, cabecera parcial, favicon (v1.11 / v3.7) |
| `79ba7c3` | marca en todas las cabeceras; paneles laterales igualados (v1.12 / v3.8) |
| `b787aec` | sandhi: fuera la declaración muerta `max-width:informe` |

Versiones publicadas: **paradigmas v1.12**, **sandhi v3.8**.

Los borradores de `docs/borradores/` siguen sin rastrear —ahora son trece, con
`comparacion-tipografia.html` añadido esta sesión— y `docs/nombres.docx` sigue
excluido en `.git/info/exclude`. Ninguno debe entrar en un commit.

## 2. LO QUE SE HIZO

### Táctil (paradigmas v1.9)

Los tooltips eran de hover y en móvil no aparecían nunca. Ahora el primer
toque abre el tooltip y el segundo sigue el enlace; con ratón no cambia nada.
Afecta a tres cosas: las referencias §N, el caso de cada inflexión (que
conserva su `title` nativo para el ratón y gana `data-caso`/`data-ord` para el
dedo) y la insignia de versión. Las zonas de toque suben a 44 px bajo
`@media (pointer:coarse)`, y los filtros se reparten en filas.

**La distinción es por tipo de puntero, no por ancho de pantalla**: se guarda
el `pointerType` del último `pointerdown`. Detalle que costó encontrar: en
táctil el navegador emula un `mouseover` antes del toque, así que los
manejadores de hover llevan un filtro `conRaton()`; sin él el tooltip se abría
solo y el primer toque ya navegaba.

### Saltos largos (todo el sitio)

Los saltos desde las barras laterales eran `behavior:'smooth'` sobre páginas
de decenas de miles de píxeles —paradigmas mide unos 35.000— y el navegador
animaba todo el recorrido, lo que tardaba segundos. Ahora se anima sólo dentro
de dos pantallas de distancia; más lejos, salta de golpe. Está en tres sitios,
con la misma regla:

- `recursos/paradigmas/plantilla.html` — `saltarA()`
- `recursos/sandhi/plantilla.html` — `saltarA()` y `volverArriba()`
- `site/assets/pali.js` — `saltarA()` y `volverArriba()`, más los 53 botones «↑»
  por capítulo, que `generar_capitulo.py` ahora pinta con `onclick="volverArriba()"`

Se dejaron a propósito los dos `scrollIntoView({block:'nearest'})` de
`pali.js` (líneas 20 y 343): ésos mueven la lista del índice para que se vea
el elemento activo, la distancia es siempre corta y quitar la animación haría
que el panel diera tirones.

### Marca del IEBH

En `site/assets/`, cinco SVG sacados del `.ai` del manual de marca (que es
PDF por dentro: `pdftocairo -svg -f N -l N` da un artboard por página, 16 en
total). Se adelgazaron redondeando coordenadas a dos decimales y cambiando el
`style` repetido por un `fill` corto — **sin reordenar los trazados**, que fue
el primer intento y rompió el dibujo: hay formas claras pintadas encima de
otras oscuras. A 1200 px de ancho difiere el 0,02 % de los píxeles, todo
antialias de bordes.

| Archivo | Qué es | Gzip |
| ------- | ------ | ---- |
| `iebh-imagotipo-granate.svg` | imagotipo completo, tema claro | 27 KB |
| `iebh-imagotipo-blanco.svg` | imagotipo completo, tema oscuro | 27 KB |
| `iebh-arbol-granate.svg` | árbol solo, tema claro | 19 KB |
| `iebh-arbol-blanco.svg` | árbol solo, tema oscuro | 19 KB |
| `favicon.svg` | árbol con los dos colores dentro, por `prefers-color-scheme` | 19 KB |

**Dos archivos por marca, uno por tema, en lugar de teñir uno solo con CSS**:
el imagotipo lleva el punto de la «i» en `#9b2f4e` y aplanarlo a un color
alteraría la marca. Van como `background-image` para que el navegador pida
sólo la del tema en uso. Ambas versiones son las del manual, sin recolorear.

Colocación, en las nueve páginas: **árbol de 26 px en la cabecera** (arriba a
la izquierda, como marca de quien publica) e **imagotipo en el pie**, junto a
la licencia. En los capítulos la cabecera no tiene línea de crédito, así que
el árbol va solo, entre el enlace de vuelta y el título de la obra.

Paleta del manual, por si hace falta: `#47151E` `#ED4263` `#FCE3E8` `#9B2F4E`
`#C63457`. Tipografías de la marca: Patrizia y Poppins.

**Lo que NO se copió al repositorio, y no debe copiarse:**
`Patrizia-Regular.ttf` es una tipografía comercial y el repositorio es
público. Tampoco entraron el manual (7,8 MB), el `.ai` ni los 19 PNG. El zip
original vive fuera del repositorio.

### Tipografía: primer paso

Los dos paneles laterales usaban tipos distintos. Ahora coinciden:

| | antes (capítulos) | ahora |
| --- | --- | --- |
| elementos del índice | Noto Serif 12,5 px | Gentium Book Plus |
| rótulo de kaṇḍa | Inter, gris `#8C8A85`, .07em | JetBrains Mono, `--haritala`, .15em |

`--haritala` ya estaba definido en `pali.css` para los dos temas, así que el
modo oscuro sale gratis (`#EFC14E`). Gentium ya se cargaba en los capítulos
para los titulares: el cambio no añade ninguna petición.

## 3. PERMISO DE LA MARCA — SIN RESOLVER

Se le señaló al IEBH, dos veces, que un logotipo es una marca registrada y que
la licencia CC BY-NC-SA cubre el texto, no la marca; y que un logotipo en la
cabecera se lee como «publicación del IEBH». **el IEBH no ha dicho si el
Venerable lo sabe.** Está publicado. Si la respuesta resultara ser que no, se
deshace con `git revert` de `776c81f` y `79ba7c3`.

## 4. GIT: OJO CON EL SANDBOX

Claude **no puede escribir en `.git`** desde su entorno. Peor: `git status` y
`git add` refrescan el índice y dejan un `.git/index.lock` de cero bytes que
tampoco puede borrar, y entonces los `git commit` del IEBH fallan con «Another
git process seems to be running». Pasó dos veces esta sesión.

**Regla para el chat nuevo: no ejecutar ninguna orden de git desde el sandbox,
ni siquiera `status`.** Sólo `git log` y `git show`, que no tocan el índice.
Los commits los hace IEBH; Claude le entrega las órdenes escritas. Si aparece
el bloqueo: `pgrep -l git` (los `gitstatusd` son del prompt de zsh y no
cuentan) y luego `rm -f .git/index.lock`.

## 5. CÓMO SE COMPRUEBA ESTO

No hay navegador en el sandbox —Chrome no se puede descargar—, así que la
verificación se hizo con **jsdom** (`npm install jsdom` en `/tmp`, y el script
hay que copiarlo a `/tmp` porque desde el directorio montado no resuelve el
módulo). El guion de pruebas de la capa táctil, con 32 aserciones, quedó fuera
del repositorio; se rehace en unos minutos si hace falta. Simula el
`pointerType`, el hover con ratón, el teclado, y comprueba de paso que los
filtros y la búsqueda sin diacríticos siguen funcionando.

Lo que jsdom **no** puede comprobar, porque no maqueta: el umbral de los
saltos (`getBoundingClientRect` devuelve ceros) y cualquier cosa de CSS. Eso
lo mira IEBH en el navegador.

Comprobación que sí conviene repetir tras cualquier cambio de plantilla:

    python3 herramientas/generar_todo.py

y luego cotejar que el `const DATA = {...}` de los HTML generados sigue siendo
idéntico byte a byte al del último commit (53.319 bytes en paradigmas, 131.516
en sandhi). Si cambia sin haber tocado el JSON, algo va mal.

## 6. TIPOGRAFÍA (decidida, sin hacer) Y URL (abierta)

### a) Tipografía — DECIDIDO: Gentium Book Plus

**El IEBH ha decidido unificar todo el proyecto en Gentium Book Plus.** Noto
Serif desaparece del cuerpo de texto. Es trabajo del chat siguiente y aún no
está hecho.

Motivo: SIL dibujó Gentium para lenguas con diacríticos latinos densos, que es
exactamente el pāḷi romanizado (ā ī ū ṃ ṇ ḷ ṅ ñ); ya es la tipografía de las
páginas de recursos y de los titulares de los capítulos, de modo que unificar
no añade ninguna petición y elimina Noto Serif entero —seis pesos más
cursivas— de todas las páginas que lo cargan.

**Salvedad que hay que comprobar al hacerlo:** Gentium tiene la altura de x
más baja que Noto Serif. A los 15 px del cuerpo de los capítulos puede leerse
pequeño y pedir 16. Mirar `docs/borradores/comparacion-tipografia.html`, que
tiene el mismo pasaje (§59 / Kacc. 182) en las dos tipografías a tamaño real,
con botones para aislar cada una.

Dónde está Noto Serif, para no dejarse nada:

| Archivo | Qué hacer |
| ------- | --------- |
| `site/assets/pali.css` línea 20 | `--serif` pasa a Gentium (18 usos cuelgan de esa variable) |
| `site/assets/pali.css` línea 27 | `--display` puede quedarse; su reserva a Noto Serif sobra |
| `herramientas/generar_capitulo.py` | quitar `Noto+Serif` del enlace de Google Fonts |
| `herramientas/generar_indices.py` | ídem |
| `herramientas/generar_recurso.py` | ídem |
| `recursos/nombre/plantilla.html` | cuatro `font-family:"Noto Serif"` sueltos (líneas 202, 226, 318, 445) más el enlace |

No tocar `docs/borradores/comparacion-tipografia.html`: es justamente el
borrador que compara las dos y necesita seguir cargando ambas.

Después: `python3 herramientas/generar_todo.py`, mirar un capítulo en el
navegador a ver si el cuerpo pide 16 px, y comprobar que ninguna página sigue
pidiendo Noto Serif.

### b) URL más corta

Hoy: `gramaticas.buddha-dhamma.net` (33 caracteres). No depende del
repositorio: es configuración de Cloudflare. En el panel del Worker hay una
pestaña **Domains** (nueva desde mayo de 2026); la ruta antigua es
Settings → Domains & Routes → Add → Custom Domain. No se puede enganchar a un
nombre que ya tenga un CNAME.

- Gratis: un subdominio más corto del dominio actual —`pali.` (22) o `g.` (19).
- El tope real: `buddha-dhamma.net` son ya 17 caracteres; para bajar de ahí
  hace falta un dominio nuevo, que cuesta al año.
- Si el sitio responde en dos nombres, uno ha de ser el canónico y el otro un
  301 (Redirect Rule de Cloudflare, sin código), o los buscadores indexan los
  dos y reparten el peso del sitio.

Quedó pendiente que Claude mire qué dominios cortos están libres, si IEBH
quiere ese camino.

## 7. TRABAJO ABIERTO QUE VIENE DE ANTES

Sigue vigente todo lo del briefing 17, sección 7. En particular, y es lo
gordo:

1. **Proponer y verificar** cada desinencia contra los suttas del Nāma-Kappa:
   derivar de base + sutta y conservar sólo lo que reproduce exactamente la
   forma atestiguada. Banco de pruebas: las 2379 formas de
   `recursos/paradigmas/paradigmas.json`. Sacaría a la luz las erratas de la
   sección 4 del briefing 17 (`mānā`, `gāmanino`, `sakkhe`, la coma de
   `mātūbhi`), que **siguen sin decidir**.
2. Incorporar del documento maestro las listas «De similar declinación».
3. Opcionales nunca pedidos: comparar dos paradigmas lado a lado, conmutador
   ordinal ↔ caso latino, casilla «Estudiado».

## 8. RECORDATORIOS QUE NO CAMBIAN

- Nunca se edita nada dentro de `site/`, **salvo `site/assets/pali.css`,
  `site/assets/pali.js` y los SVG de la marca**, que son fuente: ningún
  generador los escribe. `CLAUDE.md` sólo menciona el `.css`; conviene
  corregirlo.
- Lo tomado de Thitzana o Rūpasiddhi se señala como suyo; la flecha de
  Thitzana va al revés.
- Ante duda, `<!-- DUDA: … -->` y decirlo en voz alta.
- Nada se añade, quita ni cambia respecto de la edición base sin avisar y sin
  que IEBH decida.
- Con IEBH se habla en inglés; el producto va en español.
