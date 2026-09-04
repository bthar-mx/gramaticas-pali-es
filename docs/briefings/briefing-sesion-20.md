# Kaccāyana Pāḷi-Español: Briefing de la Sesión 20

*Complementa a los briefings 05–19. Sesión de una sola cosa: se hizo entera la
sección 7 bis del briefing 19 —la paleta «hoja de palma» en los tres capítulos
y las tres páginas de índice—, con las cinco decisiones que estaban sin tomar,
ya tomadas por IEBH. No se tocó ni una forma pāḷi ni ningún tamaño de la
escalera serif (7 ter del briefing 19, que sigue abierta).*

---

## 1. ESTADO AL CIERRE

Commiteado y desplegado:

- `1b7b8dd` — «paleta: hoja de palma en capítulos e índices; rompecachés en
  los índices; titulares serif a 400». 8 archivos: `site/assets/pali.css`,
  `herramientas/generar_indices.py` y las seis páginas regeneradas.

**Sin commitear al escribir esto:** la corrección de `CLAUDE.md` (sección 5) y
este briefing. Las órdenes entregadas al IEBH:

    git add CLAUDE.md docs/briefings/briefing-sesion-20.md
    git commit -m "CLAUDE.md: pali.css, pali.js y SVG de la marca son fuente; briefing sesión 20"
    git push

La sección 1 del briefing 19 quedó cerrada al empezar: el trabajo tipográfico
estaba commiteado (`0f6e98ce`). Se comprobó **sin ejecutar git**: leyendo
`.git/refs/heads/main` y `.git/logs/HEAD` como archivos de texto. Ese es el
método para saber el estado del repositorio sin riesgo del `index.lock`.

Versiones publicadas: **paradigmas v1.12, sandhi v3.8** — sin cambio, sus
páginas no se movieron ni un byte (ya estaban en hoja de palma).

## 2. LAS CINCO DECISIONES, TOMADAS POR IEBH

Las cuatro «sin decidir» de 7 bis más los pesos de la sección 4 del
briefing 19. Quedan así, con el contraste medido:

| Token | Valor | Nota |
| ----- | ----- | ---- |
| `--bg3` | `#F6F4EC` | más claro que `--bg2`: en el modelo invertido el hover de lo ya elevado sigue aclarando, como el `--hover` de sandhi. Ink 16,44:1 |
| `--border2` | `#A89C7F` sólido | hair oscurecido; sólido como `--border`, siguiendo el criterio «sólido, no alfa» |
| `--accent-mid` | `#517488` | nīla medio; 3,89:1 sobre `--bg` — solo usos no textuales en claro (filete de `.gloss`, focos, barra de progreso) |
| `--green` / `--green-bg` | `#55611E` / `rgba(85,97,30,.12)` | oliva cálido ajustado a la paleta; 5,25:1 sobre `--bg` |
| Pesos serif 500 | **400 + `letter-spacing:-.03em`** | el criterio de Wispr; aplicado a `.hdr-chapter`, `.idx h1`, `.doc h1/h2/h3`. El 600 de `recursos/nombre` queda para su propia pasada |

## 3. LO QUE SE HIZO, EN ORDEN

### a. El rompecachés de los índices, ANTES de la paleta

Como mandaba 7 bis («arreglarlo antes de empezar»). En
`herramientas/generar_indices.py`: se importa `version_assets` de
`generar_capitulo.py` y la plantilla enlaza `pali.css?v={assets_v}`. Las tres
llamadas a `PAGINA.format` pasan `assets_v=version_assets()`. Resultado: las
seis páginas por `pali.css` piden hoy la misma huella (`?v=9c6246a4`).

### b. Los tokens de `:root` y el oscuro

Correspondencia de 7 bis aplicada entera, conservando los nombres (los 242
usos no se tocan): `--bg #E7E3D6` (ola — **el campo de página es ahora el tono
más oscuro**), `--bg2 #F0EDE4`, `--text #171612` (ink), `--text2 #4E4839`
(soot), `--text3 #6B6455` (4,57:1 — el `#8C8A85` que suspendía AA,
desaparecido), `--border #BFB7A0` (hair, sólido), `--accent #27414F` (nīla —
**el violeta `#534AB7` ya no existe en el archivo**), `--accent-bg
rgba(39,65,79,.10)` (chip-k), más los cinco de la sección 2. `--haritala`
intacto.

El `body.dark` se copió del oscuro probado de sandhi
(`html[data-theme=dark]`), no se inventó: `#1A1917 / #232220 / #F4F1E8 /
#BDB5A2 / #494438 / #B6D8EE / EFC14E`. Lo que sandhi no tiene se derivó y se
midió: `--bg3 #2C2A26`, `--text3 #978F80` (4,96:1 sobre `--bg2`),
`--border2 #5C564A`, `--accent-mid #8FB6CE`, `--green #A5D178` /
`--green-bg rgba(165,209,120,.14)`.

### c. La inversión de superficies: los ~42 usos, auditados

La trampa anunciada. Regla aplicada, la misma que rige en la página de sandhi:
el campo y la barra pegajosa en `--bg` (ola); lo elevado —barra lateral,
tarjetas de índice, paneles, botones flotantes, tooltips, campos de
búsqueda— en `--bg2` (ola-2); el hover de lo elevado, un paso más de luz
(`--bg3`).

Cambios concretos de token (no de valor): `#toc`, `#pbadge`, `#dark-btn`,
`#top-btn`, `.toc-burger`, `.kanda-nav-btn`, `.kanda-jump`, `.search-input`,
`.done-cb` y las cinco cajas de tooltip pasan de `--bg` a `--bg2`; los hovers
`.toc-item`, `.kanda-nav-btn`, `#top-btn`, `.toc-burger` y
`.chapter-nav-btn` pasan a `--bg3`; `.toc-jump` (dentro del TOC, ya en bg2) a
`--bg3`.

**Lo que NO se cambió, adrede:** `.sutta-card` sigue en `--bg` — la ficha
queda al tono del campo, definida por su borde, exactamente como las tarjetas
de sandhi; su cabecera en `--bg2` se lee ahora como elevada y su hover en
`--bg3` aclara. `.kanda-nav` sigue en `--bg`, como la `.bar` de sandhi.
`.pali-block`, `.vutti`, `.footer-box`, `.chapter-nav`, `.idx-card` ya
estaban en `--bg2` y con la inversión quedan bien solos.

### d. El degradado radial

En el `body`:
`radial-gradient(circle at 12% 8%, rgba(255,255,255,.55), transparent 55%)`,
apagado en oscuro (`body.dark{background-image:none}`), igual que sandhi.
**`#main` pasó de `background:var(--bg)` a `transparent`** — si no, tapaba el
degradado en los capítulos. El color de campo lo pone el body (regla de la
línea ~41, que ya existía para los índices).

### e. Tres decisiones menores que tomó Claude y conviene conocer

Se avisaron en la sesión; se dejan escritas:

1. **Los grises duros del oscuro** (`#C8C6C0`, `#D0CEC8`, `#C0BEB8` en
   `body.dark .kanda-end`, `.sutta-ref`, etc.) se corrieron a sus
   equivalentes cálidos (`#C9C2B0`, `#D2CBB8`, `#C1BAA7`) para que no
   quedaran neutros sobre el oscuro cálido nuevo.
2. **El violeta de impresión**: el `@media print` de `.gloss` llevaba
   `border-left #7F77DD` y fondo `#eeeefa`; pasó a `#517488` / `#ecf1f3`.
   El resto de los hexadecimales de impresión (grises neutros) se dejó.
3. **`--green`/`--green-bg` en oscuro no existían** (el oscuro viejo nunca
   los definió); se añadieron, y `body.dark .idx-badge` dejó sus hexadecimales
   duros (`#24331a`/`#a5d178`) por `var(--green-bg)`/`var(--green)`.

También: `body.dark .fn-sup` y `.sutta-xref` llevaban el violeta duro
`#A09AE4`; ahora `var(--accent)`.

### f. `CLAUDE.md`, corregido

La sección «Cómo se publica» decía que nunca se edita nada dentro de `site/`,
sin excepciones. Ahora nombra las tres que son fuente: `pali.css`, `pali.js`
y los SVG de la marca. Venía arrastrándose desde el briefing 18.

## 4. CÓMO SE VERIFICÓ (mismo patrón, sin git y sin navegador)

1. md5 de las nueve páginas antes y después de `generar_todo.py`: cambian
   exactamente las seis de `pali.css`; **sandhi, paradigmas y nombre,
   idénticas al byte**.
2. Bloque `const DATA`: 131.530 / 53.333 — invariante.
3. Recuento de suttas: 52 / 219 / 45 — sin cambio.
4. Contraste calculado de **cada** par nuevo, claro y oscuro (script de
   luminancia WCAG en el sandbox): todos los textos ≥ 4,5:1 sobre todas sus
   superficies; `--accent-mid` claro sólo se usa en trazos no textuales.
5. Rastreo de violeta (`534AB7`, `7F77DD`, `A09AE4`, `EEEDFE`, `26224A`,
   `A9A2F0`): no queda ninguno fuera de comentarios.
6. Llaves y paréntesis del CSS balanceados; ninguna `var(--x)` sin definir.

## 5. LO QUE QUEDA ABIERTO (para mañana)

Lo primero de la próxima sesión, **en este orden**:

1. **el IEBH mira la paleta en el navegador.** Las tres cosas que la aritmética
   no puede decir: si el campo más oscuro cansa en lecturas largas, si el
   degradado radial funciona en páginas de ~35.000 px, y cómo quedan los
   titulares serif a 400 con interletraje −.03em. Lo que chirríe, se ajusta.
2. **La escalera de tamaños serif** (7 ter del briefing 19) — decisión
   editorial del IEBH, intacta: el pāḷi queda visiblemente por debajo de su
   traducción; propuesta +1 px en toda la escalera. **No tocar sin que él lo
   diga.** Falta también la captura de una glosa de dos o tres líneas para
   ver el 1.7 directamente.
3. **Lo gordo: proponer y verificar las 2379 desinencias** de
   `recursos/paradigmas/paradigmas.json` contra los suttas del Nāma-Kappa
   (briefing 19, §7.4). Es lo que sacaría a la luz las cuatro erratas sin
   decidir: `mānā`, `gāmanino`, `sakkhe`, la coma de `mātūbhi`. Candidato a
   sesión entera y en limpio.
4. URL más corta (configuración de Cloudflare; Claude puede mirar dominios
   libres si IEBH quiere).
5. `recursos/nombre/`: rediseño con la paleta nueva delante — fuera de la
   pasada de hoy por decisión del IEBH.
6. Las listas «De similar declinación»; los opcionales nunca pedidos.
7. **El permiso de la marca (briefing 19, §8): sigue sin respuesta.** Si
   resultara que el Venerable no lo sabe, `git revert` de `776c81f` y
   `79ba7c3`.
8. **El siguiente capítulo a traducir: sin decidir y hay que preguntarlo.**
   El 4 (Samāsa) vive en otro hilo y sus archivos no se tocan.

### memory.md del proyecto

Se redactó la versión puesta al día (14 briefings de atraso: capítulos 1–3
completos y publicados, tipografía, paleta, reglas duras, pendientes). El
archivo del proyecto es de sólo lectura desde Cowork, así que se le entregó a
El IEBH como archivo para pegarlo en el proyecto de claude.ai. **Comprobar en
la próxima sesión si ya está pegado**; si no, el memory.md viejo sigue
diciendo que el Nāma-Kappa está parado en §203, que es falso.

## 6. RECORDATORIOS QUE NO CAMBIAN

- **Ninguna orden de git desde el sandbox, ni siquiera `status`** — deja un
  `.git/index.lock` que IEBH borra a mano. Estado del repo: leer
  `.git/refs/heads/main` y `.git/logs/HEAD` como texto.
- Nada se edita dentro de `site/` salvo `pali.css`, `pali.js` y los SVG de la
  marca (ya lo dice `CLAUDE.md` desde hoy).
- Lo tomado de Thitzana o Rūpasiddhi se señala como suyo; la flecha de
  Thitzana va al revés.
- Ante duda, `<!-- DUDA: … -->` y decirlo en voz alta. Nada se añade, quita
  ni cambia respecto de la edición base sin que IEBH decida.
- Con IEBH se habla en inglés; el producto va en español.
