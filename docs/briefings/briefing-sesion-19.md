# Kaccāyana Pāḷi-Español: Briefing de la Sesión 19

*Complementa a los briefings 05–18. Sesión corta y de una sola cosa: se
terminó la unificación tipográfica que el briefing 18 dejaba decidida y sin
hacer (su sección 6a). Gentium Book Plus queda en todo el proyecto; Noto Serif
no aparece ya en ningún archivo publicable. **Lo primero que debe saber el chat
nuevo: el trabajo está hecho pero SIN COMMITEAR** —ver sección 1—. No se tocó
ni una forma pāḷi.*

---

## 1. ESTADO AL CIERRE — ATENCIÓN: SIN COMMITEAR

El último commit sigue siendo `b787aec`, el del cierre de la sesión 18. Todo lo
de esta sesión está **en el árbol de trabajo, sin añadir ni commitear**. Claude
no ejecutó ninguna orden de git (ver sección 5).

Las órdenes quedaron entregadas a Angel:

    git add site/assets/pali.css herramientas/generar_capitulo.py \
            herramientas/generar_indices.py herramientas/generar_recurso.py \
            recursos/nombre/plantilla.html site/
    git commit -m "tipografía: Gentium Book Plus en todo el proyecto; cuerpo de capítulo a 16px/1.6"

**Si el chat nuevo empieza y `git log` sigue en `b787aec`, lo primero es
preguntar a Angel si quiere commitear antes de seguir.** Si ya está commiteado,
esta sección se puede dar por cerrada.

Versiones publicadas: **paradigmas v1.12**, **sandhi v3.8** —sin cambio, y con
razón: ver sección 3.

Los borradores de `docs/borradores/` siguen sin rastrear (trece) y
`docs/nombres.docx` sigue excluido en `.git/info/exclude`. Ninguno debe entrar
en un commit. `docs/borradores/comparacion-tipografia.html` **no se tocó**, como
pedía el briefing 18: sigue cargando las dos tipografías, que es su función.

## 2. LO QUE SE HIZO

### El cambio, archivo por archivo

| Archivo | Qué se hizo |
| ------- | ----------- |
| `site/assets/pali.css` l. 20 | `--serif` pasa a `'Gentium Book Plus', Georgia, serif` (18 usos cuelgan de ahí) |
| `site/assets/pali.css` l. 27 | `--display` pierde su reserva muerta a Noto Serif |
| `site/assets/pali.css` `.gloss` | cuerpo del capítulo: `15px/1.5` → **`16px/1.7`** (secciones 3 y 7 ter) |
| `herramientas/generar_capitulo.py` | enlace de Google Fonts: fuera Noto Serif |
| `herramientas/generar_indices.py` | ídem |
| `herramientas/generar_recurso.py` | ídem |
| `recursos/nombre/plantilla.html` | el enlace más las cuatro declaraciones sueltas (l. 202, 226, 318, 445) |

Todas las páginas piden ahora exactamente la misma cadena:
`family=Gentium+Book+Plus:ital,wght@0,400;0,700;1,400;1,700`.

### Dos cosas que la tabla del briefing 18 se dejaba

Merece la pena anotarlas porque seguir aquella tabla al pie de la letra habría
roto dos páginas:

1. **`generar_indices.py` pedía Gentium sólo en peso 700**, y
   **`generar_recurso.py` no pedía Gentium en absoluto**. En ambos casos la
   instrucción era «quitar Noto+Serif del enlace», que a secas habría dejado
   esas páginas con `--serif` apuntando a una tipografía que no se carga —es
   decir, cayendo a Georgia—. Hubo que **añadir** Gentium, no sólo quitar Noto.
2. **Los capítulos llevan 74 etiquetas `<i>`**, y no todas están en las notas:
   hay italics dentro de `.gloss` (1), `.vutti` (2), `.rest-para` (9) y
   `.seq-list.seq-ejemplos` (2), que son contextos de `--serif`. El enlace de
   los capítulos pedía Gentium sin cursivas (`wght@400;700`), de modo que la
   cursiva del cuerpo habría pasado a ser oblicua sintética. Por eso ahora
   todas las cadenas incluyen `ital`.

También hay 731 `<strong>` en contextos serif (sobre todo
`.seq-list.seq-ejemplos`, 277), que es lo que justifica seguir pidiendo el 700.

### Páginas afectadas

Nueve en `site/`. Siete cambiaron; dos no.

| Página | De dónde sale |
| ------ | ------------- |
| `site/kaccayana/sandhi/index.html` | `generar_capitulo.py` |
| `site/kaccayana/nama/index.html` | ídem |
| `site/kaccayana/karaka/index.html` | ídem |
| `site/index.html` | `generar_indices.py` |
| `site/kaccayana/index.html` | ídem |
| `site/recursos/index.html` | ídem |
| `site/recursos/nombre/index.html` | `recursos/nombre/plantilla.html` |

`site/recursos/paradigmas/index.html` y `site/recursos/sandhi/index.html`
**no cambiaron ni un byte**: sus plantillas declaran su propio
`--serif:"Gentium Book Plus"` en `:root` y nunca cargaron otra cosa. Ya estaban
donde queríamos llegar. Por eso v1.12 y v3.8 siguen siendo válidas y no hay que
tocar las insignias de versión.

**`generar_recurso.py` hoy no genera ninguna página**: el único markdown de
`recursos/` es `combinacion-eufonica.md` y `generar_todo.py` lo tiene en
`SIN_PUBLICAR`. El arreglo queda hecho para el próximo documento en prosa que
se publique, no para nada que esté vivo ahora.

## 3. EL CUERPO DEL CAPÍTULO: 15 → 16 px, Y POR QUÉ 1.7

El briefing 18 dejaba la pregunta abierta —«a los 15 px puede leerse pequeño y
pedir 16»— y remitía al borrador de comparación. En lugar de juzgarlo a ojo se
midieron las dos tipografías.

**Cómo se midieron, que es lo reutilizable:** Google Fonts **no es accesible**
desde el sandbox (`fonts.googleapis.com` da 000, y el archivo de Ubuntu
devuelve 403 por el proxy). npm **sí** lo es. Los dos tipos se bajaron con

    npm install @fontsource/gentium-book-plus @fontsource/noto-serif

y se leyeron con `fontTools` (`OS/2.sxHeight`, `sCapHeight`, `sTypo*`, más
`hmtx` para el ancho de una línea de muestra). Noto Serif además está instalado
en el sandbox (`fc-list`), Gentium no.

Los números, en em:

| | Noto Serif 400 | Gentium Book Plus 400 |
| --- | ---: | ---: |
| unitsPerEm | 1000 | 2048 |
| altura de x | 0,5360 | **0,4541** |
| altura de mayúscula | 0,7140 | 0,6152 |
| caja de contenido (typo asc − desc) | 1,3620 | **1,4648** |
| ancho de la línea de muestra | 37,447 | 32,708 |

De donde salen las tres conclusiones:

- **La altura de x de Gentium es un 15,3 % menor.** Igualarla exactamente
  pediría 17,7 px, que es un salto demasiado grande. 16 px recupera algo más de
  la mitad de la diferencia.
- **Gentium compone un 12,7 % más estrecho al mismo cuerpo.** A 16 px la línea
  sigue saliendo **un 6,8 % más corta** que la de Noto a 15 px: subir el cuerpo
  no alarga la medida, la sigue acortando. Esto es lo que hace segura la subida.
- **El interlineado importaba más que el cuerpo.** La caja de contenido de
  Gentium es más alta (1,465 em frente a 1,362). A `16px/1.5` el blanco entre
  líneas caía a 0,6 px —apretado de ver—; a `16px/1.6` vuelve a los ~2 px que
  había con `15px/1.5`.

**Corregido al final de la sesión, a la vista del navegador: quedó en `1.7`, no
en `1.6`.** El razonamiento del `1.6` era conservar el interlineado que la
glosa tenía con Noto Serif, y lo conservaba exactamente. Pero al ver una
captura con el `.vutti` a `14px/1.7` justo debajo se vio el error: ese vutti
deja ~3,3 px de aire y la glosa a `1.6` sólo 2,2 px, de modo que **el bloque
más importante de la página iba a ser el más apretado**. Igualar el aire del
vutti a 16 px pide 1,67; se redondeó a `1.7`. Ver sección 7 ter.

Decidido por Angel sobre estos números. **Falta mirarlo en el navegador**: los
demás tamaños que cuelgan de `--serif` (14 px del `.pali-block`, 13,5, 13)
encogen ese mismo 15 % y no se tocaron. Si al verlo el conjunto pide una subida
uniforme, es una decisión de diseño aparte y hay que tomarla entera, no rule a
rule.

## 4. PENDIENTE DECIDIDO A MEDIAS: LOS PESOS 500 Y 600

Gentium Book Plus **sólo tiene 400 y 700**. No hay 500 ni 600. Angel eligió
—expresamente— dejarlo como está y mirarlo en el navegador, sin cambiar nada a
ciegas. Lo que va a pasar al verlo:

| Dónde | Pide | Va a renderizar |
| ----- | ---- | --------------- |
| `pali.css` `.hdr-chapter` | 500 | 400 (más claro que ahora) |
| `pali.css` `.idx h1` | 500 | 400 |
| `pali.css` `.doc h1`, `.doc h2`, `.doc h3` | 500 | 400 |
| `recursos/nombre` `.term .form` | 600 | **700** (más negro que ahora) |

Las tres opciones que había sobre la mesa: dejarlo (elegida), subir los 500 a
700, o escribir 400/700 explícitos —mismo resultado visual que dejarlo, pero el
CSS deja de pedir pesos que la tipografía no tiene—. **Sin decidir.**

## 5. GIT: LA REGLA SE ENDURECIÓ

El briefing 18 permitía `git log` y `git show`. **Angel lo cerró del todo esta
sesión: ninguna orden de git desde el sandbox, ni siquiera `status`.** Deja un
`.git/index.lock` de cero bytes que él tiene que borrar a mano y que hace
fallar sus commits.

Esta sesión se respetó: no se ejecutó git ni una vez. La consecuencia práctica
es que **la verificación no puede apoyarse en `git diff`**, y hay que montarla
de otra manera (sección 6).

Si aparece el bloqueo: `pgrep -l git` (los `gitstatusd` son del prompt de zsh y
no cuentan) y luego `rm -f .git/index.lock`.

## 6. CÓMO SE VERIFICÓ, SIN GIT Y SIN NAVEGADOR

El método que funcionó, por si sirve de patrón:

1. **md5 de las nueve páginas antes y después** de `generar_todo.py`, para ver
   exactamente cuáles cambian y confirmar que no cambia ninguna de más.
2. **Tamaño del bloque `const DATA`** en paradigmas y sandhi antes y después:
   idéntico. (La cifra que mide el script de esta sesión no coincide con la del
   briefing 18 —53.319 / 131.516— porque recorta el bloque con otro criterio;
   lo que importa es la invariancia, no el número absoluto.)
3. **Recuento de suttas** por capítulo tras regenerar: 52 / 219 / 45. Sin
   cambio.
4. **Rastreo de `Noto.Serif`** por todo el repositorio: no queda ninguno fuera
   de `docs/borradores/` y `docs/briefings/`, que es donde debe estar.
5. **Comprobación de que las nueve páginas piden Gentium** y con qué cadena.

Lo que sigue sin poder comprobarse aquí: cualquier cosa de maquetación. No hay
navegador en el sandbox. El cuerpo a 16 px, el interlineado y los pesos los
tiene que mirar Angel.

## 7. LO QUE QUEDA ABIERTO

En orden de tamaño, de menor a mayor:

1. **Los pesos 500/600** de la sección 4: mirar y decidir.
2. **El cuerpo a 16 px** en el navegador, y si los demás tamaños serif piden
   subir con él (sección 3).
3. **URL más corta** — briefing 18, sección 6b, intacta. Hoy
   `gramaticas.buddha-dhamma.net` (33 caracteres). Es configuración de
   Cloudflare, no del repositorio. Gratis: `pali.` (22) o `g.` (19). El tope
   real son los 17 caracteres de `buddha-dhamma.net`; bajar de ahí pide dominio
   nuevo de pago. Si el sitio responde en dos nombres, uno canónico y el otro
   301. **Quedó pendiente que Claude mire qué dominios cortos están libres**, si
   Angel quiere ese camino.
4. **Proponer y verificar las 2379 desinencias** de
   `recursos/paradigmas/paradigmas.json` contra los suttas del Nāma-Kappa:
   derivar de base + sutta y conservar sólo lo que reproduce exactamente la
   forma atestiguada. **Es lo gordo y es lo que sacaría a la luz las cuatro
   erratas** de la sección 4 del briefing 17 —`mānā`, `gāmanino`, `sakkhe`, la
   coma de `mātūbhi`—, que siguen sin decidir.
5. Incorporar del documento maestro las listas «De similar declinación».
6. Opcionales nunca pedidos: comparar dos paradigmas lado a lado, conmutador
   ordinal ↔ caso latino, casilla «Estudiado».

### Sobre el estado de la traducción: corregido

En una primera versión de este briefing se escribió que el Nāma-Kappa estaba
«aprobado hasta §202, sigue §203». **Es falso**, y conviene dejar dicho de
dónde salió el error para que no se repita: de `memory.md` del proyecto, que
sigue congelado en el estado del briefing 05. Ya el briefing 06 registra §203
como aprobado.

Lo que dicen los archivos, que es lo que vale:

| Comprobación | Resultado |
| ------------ | --------- |
| `kaccayana/02-nama-kappa.md` | termina en «Nāmakappo Niṭṭhito / Fin del capítulo de nombres» |
| `site/kaccayana/nama/index.html` | de `id="s52"` a `id="s270"`, 219 fichas |
| `generar_indices.py` | «3 de 8 capítulos · 315 suttas · en preparación: 4, 5, 6, 7, 8» |

Es decir: **capítulos 1, 2 y 3 traducidos y publicados; 4 a 8 sin publicar.**
El Nāma-Kappa está entero, no parado en §203.

**Lo que NO se sabe y hay que preguntar a Angel:** cuál es el siguiente
capítulo a traducir. El 4 (Samāsa) es el que tocaría por orden, pero tanto
`CLAUDE.md` como `memory.md` advierten de que **el capítulo 4 vive en otro hilo
de revisión y no se deben tocar esos archivos**. No se ha inventado aquí una
respuesta.

**Tarea para la próxima sesión: actualizar `memory.md`**, que está dando por
buenas cosas que dejaron de serlo hace catorce briefings.

## 7 bis. MODO CLARO: DECIDIDO, SIN EMPEZAR

**Angel ha decidido llevar los capítulos y los índices a la paleta «hoja de
palma» que ya usan `/recursos/sandhi/` y `/recursos/paradigmas/`.** Se decidió
al final de la sesión 19 y **no se ha tocado ni una línea**. Es el trabajo con
el que debe empezar el chat siguiente.

### De dónde salió

De mirar `wisprflow.ai` —Angel lo guardó completo y se leyó su hoja de estilo
real, no una impresión—. Lo que se sacó de ahí, por si hace falta volver:

| Suyo | Valor |
| ---- | ----- |
| fondo `--base-color--lumen` | `#FFFFEB` (matiz 60°, saturación 100 %) |
| tinta `--base-color--vast` | `#1A1A1A` |
| granate `--base-color--pulse` | `#7F1C34` — a 3° del granate del IEBH |
| borde primario | negro al **30 %** (el nuestro está al 11 %) |
| titulares | **todos `font-weight:400`**, con `letter-spacing:-.03em` |
| serif de titulares | EB Garamond (misma familia de formas que Gentium) |

Pero **la conclusión no fue copiar a Wispr.** Al medir nuestras propias
páginas apareció esto:

| Paleta | Páginas | Fondo | Matiz / saturación |
| ------ | ------: | ----- | ------------------ |
| `pali.css` | 6 | `#FAFAF8` / `#F3F2EE` | 45–60°, **17 %** |
| hoja de palma | 2 | `#F0EDE4` / `#E7E3D6` | 45°, **28 %** |
| `nombre` | 1 | `#F4F5F0` / `#E9EBE4` | 72–77°, 15–20 % |

Es decir: **el proyecto ya había tomado esta decisión** —hoja de palma, tinta
de humo, oropimente, bermellón, índigo— y `pali.css` es una versión
desvaída de la misma idea. Wispr sólo confirma que la dirección funciona. El
token `--haritala` (`#5C4008`) ya es **idéntico** en las dos paletas: el
puente ya existe.

### Las dos cosas que no son obvias

1. **El modelo de superficies se invierte.** En la página de sandhi el `body`
   va sobre `--ola` (`#E7E3D6`, el tono *más oscuro*) y las tarjetas y paneles
   sobre `--ola-2` (`#F0EDE4`, el *más claro*). En los capítulos es al revés:
   la página es lo más claro y los paneles se oscurecen. **No basta con cambiar
   el `:root`**: hay que auditar los 20 usos de `--bg` y los 22 de `--bg2`.
2. **La página lleva un degradado que `pali.css` no tiene:**
   `radial-gradient(circle at 12% 8%, rgba(255,255,255,.55), transparent 55%)`
   en el `body`. Una luz suave arriba a la izquierda, como la que cae sobre una
   hoja de palma. Es probablemente la mitad de por qué esa página «se ve muy
   bien» y no simplemente beige.

### Accesibilidad: la paleta nueva arregla un fallo que tenemos

Hoja de palma cumple AA en todo: ink 14,10:1 · soot 7,08:1 · nīla 8,37:1 ·
rakta 7,10:1 · haritāla 7,46:1. **Y no tiene un tercer tono de texto flojo.**
Donde los capítulos usan `--text3` (`#8C8A85`, **3,30:1, suspende AA** y
carga las descripciones de tarjeta, `.sutta-ref`, `.sutta-breakdown` y los
pies), la página de sandhi usa `--soot` a 7,08:1. Adoptar la paleta **corrige
el problema por estructura**, no parcheando un hexadecimal.

### Correspondencia propuesta (conservando los nombres de `pali.css`)

Se conservan los nombres para no tocar los 242 usos repartidos por el archivo.

| `pali.css` | pasa a | Nota |
| ---------- | ------ | ---- |
| `--bg` | `#E7E3D6` (ola) | **campo de página — ahora el más oscuro** |
| `--bg2` | `#F0EDE4` (ola-2) | superficies elevadas — ahora el más claro |
| `--bg3` | *sin decidir* | hoja de palma sólo tiene dos tonos (ver abajo) |
| `--text` | `#171612` (ink) | 14,10:1 |
| `--text2` | `#4E4839` (soot) | 7,08:1 |
| `--text3` | `#6B6455` | **4,57:1 — pasa AA**; hoy 3,30:1 |
| `--border` | `#BFB7A0` (hair) | sólido, no alfa |
| `--border2` | *sin decidir* | hace falta un filete más marcado |
| `--accent` | `#27414F` (nīla) | 8,37:1 · **desaparece el violeta `#534AB7`** |
| `--accent-bg` | `rgba(39,65,79,.10)` (chip-k) | |
| `--accent-mid` | *sin decidir* | filete de `.gloss` |
| `--green` / `--green-bg` | *sin decidir* | sólo los usa `.idx-badge` |
| `--haritala` | `#5C4008` | **ya idéntico, no se toca** |

**Cuatro decisiones menores sin tomar**, señaladas arriba. Candidatos medidos
para `--bg3`: `#F6F4EC` (ink encima 16,44:1), `#EFEBDE` (15,18:1), `#DCD7C7`
(12,58:1).

### Trampas contadas antes de empezar

- `pali.css` son **932 líneas** y **242 usos** de estos tokens.
- **24 reglas `body.dark`.** El oscuro de hoja de palma **ya existe y está
  probado** (`--ola:#1A1917; --ink:#F4F1E8; --nila:#B6D8EE; --rakta:#F09A88`…),
  así que se copia, no se inventa.
- **Dos mecanismos de tema distintos**, y esto está comprobado y **funciona
  bien**: `pali.css` usa la clase `body.dark`; paradigmas y sandhi usan
  `html[data-theme=dark]`. Los dos leen la misma clave `pali_dark` con valores
  `'1'`/`'0'`, y la página de sandhi los traduce con reserva a su clave antigua
  `sandhi-theme`. **No hay desincronización; no hay que «arreglarlo».**
- Quedan ~20 hexadecimales literales en `pali.css` (algunos son estilos de
  impresión: `#f7f7f5`, `#f5f5f0`). Hay que repasarlos aparte de los tokens.
- **LA TRAMPA GORDA, descubierta al cambiar el interlineado: los índices no
  llevan rompecachés.** Los capítulos enlazan
  `pali.css?v=<hash md5>` —`version_assets()` en `generar_capitulo.py`, línea
  796— y el generador lo rehace solo. **Las tres páginas de índice enlazan
  `pali.css` a secas**, sin `?v=`:

  | Página | Enlace |
  | ------ | ------ |
  | los 3 capítulos | `pali.css?v=43815aef` · `pali.js?v=43815aef` |
  | `site/index.html` | `pali.css` |
  | `site/kaccayana/index.html` | `pali.css` |
  | `site/recursos/index.html` | `pali.css` |

  Consecuencia para la pasada de la paleta: `pali.css` va a cambiar de arriba
  abajo y **tres de las seis páginas afectadas no se lo van a decir al
  navegador**. Se verán los capítulos con la paleta nueva y los índices con la
  vieja, según lo que tenga cacheado cada visitante y la caché de Cloudflare —
  y al depurar parecerá un error de CSS cuando no lo es.

  **Arreglarlo antes de empezar con la paleta**: llevar `version_assets()` a
  `generar_indices.py` y usar `pali.css?v={assets_v}` en su plantilla, igual
  que los capítulos. Es un cambio pequeño y ahorra una tarde de desconcierto.

### Alcance

**Siete páginas**, todas por `pali.css`, salvo que ya estén:

- por `pali.css`: los 3 capítulos y los 3 índices → **es donde está el trabajo**
- `/recursos/sandhi/` y `/recursos/paradigmas/`: **ya están** — a lo sumo el
  grosor del filete y el interletraje de los titulares
- `/recursos/nombre/`: **fuera de esta pasada, por decisión de Angel.** Es
  página publicada y viva (ficha normal en el índice de recursos, la genera
  `generar_nombre.py`), pero es autónoma, no carga `pali.css`, está a 25° en
  los verdes con tinta azulada `#1D2430` y lleva tipografías propias
  (Fraunces, Spectral) y tres bloques de oscuro. Se ve después, ya con la
  paleta nueva delante.

### Cómo se comprueba

Igual que la tipografía (sección 6), porque sigue sin haber navegador:
md5 de las nueve páginas antes y después, invariancia del bloque `const DATA`,
recuento de suttas, y **contraste calculado de cada par nuevo**. Lo que no se
puede comprobar aquí y tiene que mirar Angel: si el campo más oscuro cansa en
lecturas largas, y si el degradado radial funciona en páginas de 35.000 px.

**Y una consecuencia gratis:** la sección 4 de este briefing —los pesos 500 y
600 que Gentium no tiene— se resuelve sola si se adopta el criterio de Wispr,
que no usa el peso como recurso en los titulares: `font-weight:400` y
`letter-spacing:-.03em`. Conviene decidirlo a la vez que la paleta.

## 7 ter. LO QUE SE VIO EN EL NAVEGADOR AL CIERRE

Angel miró el capítulo de Sandhi ya con Gentium y mandó dos capturas: la página
plegada y §12–§13 desplegados. Es la única comprobación visual que existe de
todo lo de hoy, así que conviene no perderla.

### Confirmado, funciona

- **Gentium carga en todas partes**; no se ve ninguna caída a Georgia. Los
  diacríticos del pāḷi se ven correctos y los del titular, en oropimente,
  quedan bien.
- **El cuerpo a 16 px acierta.** La glosa es claramente la línea principal y
  manda sobre el vutti sin gritar. La jerarquía se lee bien.
- La barra lateral, con Gentium y los rótulos de kaṇḍa en mono dorado (cambio
  de la sesión 18), hace juego con el cuerpo.

### DECISIÓN NUEVA, SIN TOMAR: la escalera de tamaños de la serif

Esto salió de mirar la captura y **no estaba previsto**. Al pasar a Gentium
**todos** los tamaños en serif perdieron el mismo 15 % de tamaño aparente, pero
esta mañana sólo se compensó `.gloss` (15 → 16 px). Resultado: la distancia
entre la traducción española y el texto pāḷi se ha abierto por partida doble, y
**el pāḷi —que es la fuente— queda visiblemente por debajo de su traducción.**

Devolver al `.pali-block` su tamaño aparente anterior pediría 16,5 px, que
adelantaría a la glosa. O sea que no es la solución. La pregunta real es si
subir toda la escalera ese mismo 7 %:

| Regla | Ahora | Propuesta |
| ----- | ----: | --------: |
| `.pali-block` | 14 | 15 |
| `.vutti` | 14 | 15 |
| `.seq-list.seq-ejemplos` | 13 | 14 |
| `.sutta-pali-title` | 16 | 17 |
| `.intro-pali` | 14 | 15 |
| `.intro-trans` | 13,5 | 14,5 |

**Es una decisión editorial, no tipográfica** —cuál de los dos textos manda en
la página—, y por eso se deja para Angel. No tocarla sin que él lo diga.

### El interlineado: corregido a 1.7, y todavía sin ver del todo

En las tres capturas **todas las glosas ocupan una sola línea**, de modo que
el interlineado de `.gloss` no se ha visto nunca directamente. Lo que sí se vio,
en la tercera, fue el primer bloque en serif de dos líneas —el párrafo «¿Por
qué se dice “opcionalmente” (vā)?»— a `14px/1.7`, y de ahí salió la corrección:

| Bloque | Tamaño | Caja de Gentium | Aire entre líneas |
| ------ | ------ | --------------- | ----------------- |
| ese párrafo | 14px/1.7 = 23,8 px | 20,5 px | **3,3 px** — se ve cómodo |
| `.gloss` con 1.6 | 16px/1.6 = 25,6 px | 23,4 px | **2,2 px** |
| `.gloss` con 1.7 | 16px/1.7 = 27,2 px | 23,4 px | **3,8 px** |

Con `1.6` la glosa —el bloque más grande y más importante— habría quedado más
apretada que el párrafo de debajo. **Se cambió a `1.7` y está aplicado.**

**Sigue faltando la comprobación directa:** una captura de un sutta cuya
traducción ocupe dos o tres líneas. La aritmética es firme, pero no sustituye a
verlo.

### La captura confirma el diagnóstico de la paleta

Tres cosas que en la sección 7 bis eran números y ahora se ven:

1. **Las tarjetas no se separan del fondo.** Filete al 11 % y superficies al
   17 % de saturación: «Versos introductorios» y las fichas de sutta flotan
   casi al mismo valor que la página.
2. **`--text3` no se lee.** «Capítulo anterior / Introducción» parece
   desactivado sin estarlo, y «0 / 51 estudiados» y el campo `§...` pelean con
   el fondo. Es el 3,30:1 en la práctica.
3. **El violeta está en el peor sitio posible.** No es sólo la insignia de
   versión: es **el fondo de la glosa** —el elemento más importante de la
   página, dos veces por sutta—, más las llamadas de nota y el elemento activo
   de la barra lateral. Es el único color frío sobre papel cálido.

De donde sale una consecuencia práctica para ordenar el trabajo: **cambiar
`--accent` es lo que más se va a notar de toda la paleta.** Si hubiera que
hacer una sola cosa, es ésa.

## 8. SIGUE SIN RESOLVER: EL PERMISO DE LA MARCA

Se arrastra desde la sesión 18 y no se tocó hoy. Se le señaló a Angel, dos
veces, que un logotipo es marca registrada, que la licencia CC BY-NC-SA cubre
el texto y no la marca, y que un logotipo en la cabecera se lee como
«publicación del IEBH». **Angel no ha dicho si el Venerable lo sabe.** Está
publicado. Si la respuesta resultara ser que no, se deshace con `git revert` de
`776c81f` y `79ba7c3`.

## 9. RECORDATORIOS QUE NO CAMBIAN

- Nunca se edita nada dentro de `site/`, **salvo `site/assets/pali.css`,
  `site/assets/pali.js` y los SVG de la marca**, que son fuente: ningún
  generador los escribe. `CLAUDE.md` sólo menciona el `.css`; **sigue
  conviniendo corregirlo** (venía ya del briefing 18).
- Lo tomado de Thitzana o Rūpasiddhi se señala como suyo; la flecha de Thitzana
  va al revés.
- Ante duda, `<!-- DUDA: … -->` y decirlo en voz alta.
- Nada se añade, quita ni cambia respecto de la edición base sin avisar y sin
  que Angel decida.
- Con Angel se habla en inglés; el producto va en español.
