# Kaccāyana Pāḷi-Español: Briefing de la Sesión 21

*Complementa a los briefings 05–20. La sesión 21 transcurrió en dos chats a la
vez. En el otro se incorporó el **Nyāsa-Pāḷi** como referencia de segunda capa,
con su escaneo birmano de 1933 —es lo principal de hoy, sección 2—. En éste se
verificó esa incorporación y se escribió este briefing. **No se tocó ni una
forma pāḷi, ni el sitio, ni la paleta.** Lo abierto del briefing 20, §5, sigue
abierto y se repite al final.*

> **Lo primero que tiene que saber el chat nuevo:** el escaneo del Nyāsa **no
> está en el repositorio**, aunque el mensaje del commit diga que sí. Lo
> excluye `.gitignore` con la regla `*.pdf`. Sección 2, «El escaneo».

---

## 1. ESTADO AL CIERRE

HEAD: **`d0acb5f`**. Comprobado **sin ejecutar git**, leyendo
`.git/refs/heads/main` y `.git/logs/HEAD` como texto plano —el método que fijó
el briefing 20 y que evita el `index.lock`—.

Los cinco commits desde el cierre de la sesión 19:

| Hash | Qué |
| ---- | --- |
| `0f6e98c` | glosa a 16px/1.7; briefing 19 |
| `1b7b8dd` | paleta hoja de palma; rompecachés en índices; titulares serif a 400 |
| `1f64337` | CLAUDE.md (pali.css/pali.js/SVG son fuente); briefing sesión 20 |
| `b8b41a4` | **Nyāsa: master, errata y extracción por capítulos** |
| `d0acb5f` | **Nyāsa: transcripción, errata, extracción «y escaneo 1933 comprimido»** ← HEAD |

Dos cosas que conviene tener claras al leer esa tabla:

- **Lo que quedaba pendiente del briefing 20 ya está commiteado** (`1f64337`).
  Esa comprobación queda cerrada.
- **Hay dos commits de Nyāsa y el segundo promete algo que no entregó.** Ver
  abajo.

## 2. NYĀSA-PĀḶI: INCORPORADO

Se incorpora el **Nyāsa-Pāḷi (Mukhamattadīpanī)**, de Vimalabuddhi, como
**referencia de segunda capa, al mismo nivel que Rūpasiddhi**.

**Procedencia:** transcripción `.docx` de la edición Sudhammavatī (Yangon).

### Qué hay en `docs/fuentes/nyasa/`

| Archivo | Qué es | ¿En el repo? |
| ------- | ------ | ------------ |
| `Nyasa_Pali_Mukhamattadipani_master.md` | el master; md5 `df5699b9ae436590e0e36d5361e32707` | sí |
| `Nyasa_errata.md` | registro de correcciones — **leerlo antes de usar nada** | sí |
| `Nyasa-00-prologo-y-matika.md` … `Nyasa-08-unadi.md` | extracción por capítulos | sí |
| `limpiar_nyasa.py`, `dividir_nyasa.py`, `comprimir_nyasa_pdf.py` | los tres scripts | sí |
| `Nyasa_1933_escaneo_bitonal_200dpi.pdf` | escaneo birmano recomprimido, 54 MB | **NO** |

Los nueve extractos llevan cabecera de procedencia y el aviso de **no editar
ahí**: se corrige en el master y se regenera.

### El escaneo: existe, está verificado, y NO está en el repositorio

Esto es lo más importante de la sección, porque el mensaje del commit `d0acb5f`
dice «…y escaneo 1933 comprimido» y **el PDF no entró**. La causa es
`.gitignore`, que trae la regla global `*.pdf`. Comprobado leyendo
`.git/index`: aparecen los nueve `.md` y los tres `.py`, y **no aparece el
PDF**. Coherente con el tamaño: `.git` ocupa 15 MB y el árbol de trabajo 61 MB.

**Consecuencia práctica: el escaneo existe sólo en la máquina de Angel.** Quien
clone el repositorio no lo tendrá, por mucho que este briefing y el mensaje del
commit lo nombren.

**Sin decidir, y hay que decidirlo:**

- **(a) Dejarlo fuera y subirlo como asset de Release**, junto al original de
  357 MB que ya está pendiente de eso. Es lo coherente con `*.pdf` en
  `.gitignore` y con mantener público un repositorio ligero.
- **(b) Meterlo con una excepción** (`!docs/fuentes/nyasa/*.pdf`). Aviso: son
  53,7 MiB y GitHub avisa a partir de 50 MB por archivo; además quedaría en el
  historial para siempre, y sacarlo después obliga a reescribir historia.

La recomendación, si vale: **(a)**. Y **cambiar el mensaje del commit no es
posible sin reescribir**, así que basta con que quede dicho aquí.

**Propiedades verificadas del PDF** (`pdfinfo` + `pdfimages`):

| | |
| --- | --- |
| páginas | 525 |
| resolución | 200 ppi |
| profundidad | 1 bit por píxel — bitonal, como anuncia el nombre |
| tamaño | 56.274.205 bytes (54 MB) |

**La fórmula de paginación, verificada aquí:** *página impresa N = página PDF
N + 38*. Se renderizó la página 60 del PDF, que según la fórmula debe ser la
impresa 22, y su encabezado lleva el numeral birmano **၂၂**. Coincide. Es la
edición Sudhammavatī, contrastada por contenido en la p. 22 por el otro chat
—eso último no se ha vuelto a verificar aquí, porque exige leer birmano—.

### Verificado en esta sesión

No se dio nada por bueno de oídas:

- **md5 del master:** `df5699b9ae436590e0e36d5361e32707` — coincide.
- **Recomposición byte a byte:** se ejecutó `dividir_nyasa.py`, que trae su
  propia comprobación (`assert recomp == t`). Responde
  `recomposición byte a byte: OK`.
- **Aviso para quien repita la comprobación a mano:** concatenar los nueve
  archivos da 1.016.517 bytes frente a los 1.012.387 del master. **No es una
  discrepancia**: son las nueve cabeceras de procedencia (4.130 bytes). La
  comprobación válida es la del script, que las descuenta.
- **Las cinco anclas citadas** —§12, §52, §53, §271, §284— resuelven a los
  archivos que les tocan.
- **La fórmula de páginas del escaneo**, como se ha dicho.
- **`CLAUDE.md` no menciona todavía `docs/fuentes/nyasa/`.** Pendiente real.

### Correcciones

28 correcciones léxicas inequívocas aplicadas, **todas registradas** en
`Nyasa_errata.md` §2. La limpieza mecánica de formato (§1) no altera el texto
pāḷi.

### Zona gris: NO corregido, pendiente de Angel

`Nyasa_errata.md` §3. Lo que hay que saber antes de usar el Nyāsa para algo:

1. **La división Sandhi/Nāma no es la nuestra.** En esta edición **§52
   *Jinavacanayuttaṃ hi* abre el Nāmakappa**, tras el colofón del quinto
   pariccheda del Sandhi. **Cotejar con la división del proyecto antes de citar
   «capítulo» del Nyāsa.**
2. **El Uṇādi reinicia la numeración en (1).** Sus anclas no son § del
   proyecto; hace falta concordancia.
3. **Las anclas no son tipográficamente uniformes**: las hay sin negrita y con
   espacios (`( 570 )`). Cualquier emparejamiento mecánico va a perder casos.
4. **Corrupción de espaciado en los capítulos 4–8** (Samāsa, Taddhita,
   Ākhyāta, Kibbidhāna, Uṇādi): palabras fusionadas y partidas a mitad de
   línea, p. ej. «gadhi iccetasmā ikapaccayohotītiñāpa naṃtthaṃ». Demasiado
   ambigua para arreglo mecánico: **se corrige capítulo por capítulo en el
   punto de uso**. Los capítulos 1–3 están notablemente más limpios.
5. **El capítulo 7 se llama `Kitabbidhāna`** en esta edición, no
   `Kibbidhāna`. Forma consistente de la edición; se conserva.
6. **Colofón duplicado** en el dutiyo pariccheda del Kibbidhāna, con texto
   circundante repetido: duplicación de la transcripción, se conserva tal cual.
7. Dos lecturas dudosas en el comentario a §12: *viggataṃ* donde se esperaría
   *viggahaṃ*, y *kasmī* donde se esperaría *kasmā*. Puede ser errata o puede
   ser la lectura de la edición.

### Regla de uso, igual que Thitzana y Rūpasiddhi

**Todo material tomado del Nyāsa se señala como suyo** antes de incorporarlo,
para que Angel decida y se dé el crédito. Y la transcripción **lleva ruido de
OCR: no se cita textualmente sin verificar**, como avisan las cabeceras de los
propios extractos. El escaneo de 1933 es el árbitro de lecturas.

### En el project knowledge de claude.ai

Subidos allí, para consulta desde chats sin acceso al repositorio: la errata,
`Nyasa-01`, `Nyasa-02`, `Nyasa-03`, y los cortes del PDF 01 y 03.

### Pendientes del Nyāsa

- **Decidir qué se hace con el escaneo** (a/b de arriba) y, en cualquier caso,
  subir el original de 357 MB como asset de Release.
- **Añadir `docs/fuentes/nyasa/` a `CLAUDE.md`.** Se suma al ítem ya abierto
  sobre rutas editables.
- Decidir la zona gris de la errata §3, punto por punto.
- Verificar que la paginación del escaneo cuadra en más puntos que la p. 22
  —la fórmula se comprobó en una sola página—.

## 2 bis. BORRADORES BORRADOS, RECUPERADOS — Y UN HALLAZGO

`docs/borradores/` guardaba trece archivos según el briefing 18; quedaban
cinco. **Los ocho que faltaban se recuperaron de Time Machine** (copia del
18-08 a las 22:09) y están en `~/Desktop/borradores-recuperados/`. Los cinco
supervivientes son idénticos byte a byte a los de la copia, así que el rescate
es fiel.

Los ocho eran: `3-Kāraka-Kappa-revA.md`,
`capitulo-03-karaka-kappa-completo.md`, los tres `sesion-06-suttas-*` y los
tres `sesion-11-suttas-*`. Todos son borradores de capítulos ya publicados: el
borrado fue una limpieza deliberada y **razonable**.

**Se comprobó, uno a uno, que todo lo que afectaba al texto publicado se había
resuelto y aplicado antes del borrado:** diez erratas de Nandisena, los seis
términos del glosario, la fórmula de *avadhāraṇa*, el desglose de una voz de
§239 y la DUDA de §237 —que se resolvió con §174 y que hoy no deja ni un
`<!-- DUDA -->` en el capítulo—. Nada del sitio se apoya en una pregunta sin
responder.

**Pero los borradores llevaban al final una sección `NOTAS DE TRABAJO` que el
capítulo, por ser texto limpio, no podía recoger**, y ahí sí había cosas vivas
—sobre todo diecisiete apartados de Thitzana ofrecidos y no incluidos, marcados
«recuperable si Angel lo quiere», que no constaban en ningún otro sitio—.

Todo eso se ha volcado a **`docs/notas-de-trabajo-nama.md`**, ya en el
repositorio y bajo control de versiones. Los borradores originales pueden
quedarse en el archivo del Escritorio.

### El hallazgo: §10.1 nunca se ejecutó

Al verificar lo anterior salió algo que no venía a cuento y que importa más que
el resto. Los briefings 04 y 05 tienen una sección **§10.1, «Restitución de
referencias bibliográficas (fase HTML)»**: las referencias canónicas se retiran
de la línea española y **se restituyen al pasar a HTML**.

**No se hizo.** `site/kaccayana/nama/index.html` no contiene **ni una sola**
referencia bibliográfica: cero coincidencias con el patrón `Khu./Vin./Abhi./D./
M./A./S. tomo, página`.

No se han perdido —están en los briefings, y las de §204–§270 están tabuladas
en `docs/notas-de-trabajo-nama.md` §1.2—, pero el plan quedó a medias y nadie
volvió a él. **Conviene decidir si se retoma**, y si se retoma, si alcanza a
los tres capítulos publicados o sólo al Nāma.

## 3. LO QUE SIGUE ABIERTO, DEL BRIEFING 20

Se repite entero porque nada de esto se tocó hoy. Orden del briefing 20, §5:

1. **Angel mira la paleta «hoja de palma» en el navegador.** Lo que la
   aritmética no puede decir: si el campo más oscuro cansa en lecturas largas,
   si el degradado radial funciona en páginas de ~35.000 px, y cómo quedan los
   titulares serif a 400 con interletraje −.03em.
2. **La escalera de tamaños serif** (briefing 19, §7 ter) — **decisión
   editorial de Angel, intacta**: el pāḷi queda visiblemente por debajo de su
   traducción; propuesta de +1 px en toda la escalera. **No tocar sin que él lo
   diga.** Falta también la captura de una glosa de dos o tres líneas para ver
   el interlineado 1.7 directamente.
3. **Lo gordo: proponer y verificar las 2379 desinencias** de
   `recursos/paradigmas/paradigmas.json` contra los suttas del Nāma-Kappa.
   Sacaría a la luz las cuatro erratas sin decidir: `mānā`, `gāmanino`,
   `sakkhe`, la coma de `mātūbhi`. Candidato a sesión entera y en limpio.
   **Nota nueva: el Nyāsa es ahora un árbitro más para esa pasada**, con las
   cautelas de la sección 2 —y el Nāma es de los capítulos limpios—.
4. URL más corta (configuración de Cloudflare).
5. `recursos/nombre/`: rediseño con la paleta nueva delante.
6. Las listas «De similar declinación»; los opcionales nunca pedidos.
7. **El permiso de la marca (briefing 19, §8): sigue sin respuesta.** Si
   resultara que el Venerable no lo sabe, `git revert` de `776c81f` y
   `79ba7c3`.
8. **El siguiente capítulo a traducir: sin decidir y hay que preguntarlo.** El
   4 (Samāsa) vive en otro hilo y sus archivos no se tocan. *Y ojo: el
   capítulo 4 del Nyāsa es de los que llevan la corrupción de espaciado.*
9. **`memory.md` del proyecto: RESUELTO el 20-08 por la tarde.** Ya trae el
   texto nuevo —capítulos 1, 2 y 3 publicados, con nota explícita de que lo del
   §203 era falso—. No hay nada que hacer aquí.

   Dos cosas aprendidas por el camino, por si vuelve a pasar: **la memoria no
   está disponible desde Cowork**, así que ningún chat de Cowork puede
   escribirla —hay que hacerlo desde claude.ai web, Desktop o móvil—; y **el
   panel tarda en reflejar los cambios**, de modo que ver el texto viejo no
   significa que la escritura haya fallado. Aquí tardó unas horas.

## 4. RECORDATORIOS QUE NO CAMBIAN

- **Ninguna orden de git desde el sandbox, ni siquiera `status`** — deja un
  `.git/index.lock` que Angel borra a mano. Para saber el estado del
  repositorio: leer `.git/refs/heads/main`, `.git/logs/HEAD` y `.git/index`
  como archivos. Con eso se averigua el hash, el mensaje y qué está indexado,
  que es cuanto hace falta.
- Nada se edita dentro de `site/` salvo `pali.css`, `pali.js` y los SVG de la
  marca.
- Lo tomado de Thitzana, Rūpasiddhi **o Nyāsa** se señala como suyo; la flecha
  de Thitzana va al revés.
- Ante duda, `<!-- DUDA: … -->` y decirlo en voz alta. Nada se añade, quita ni
  cambia respecto de la edición base sin que Angel decida.
- Con Angel se habla en inglés; el producto va en español.
