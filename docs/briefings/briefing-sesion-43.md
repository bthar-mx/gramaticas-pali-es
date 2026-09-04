# Kaccāyana Pāḷi-Español: Briefing de la Sesión 43

*Complementa a los briefings 05–42. Tema de la sesión 43 (2026-09-02): **la
licencia**. Se cambia la atribución de CC BY-NC-SA 4.0 a **CC BY-NC-ND 4.0** en
todo lo que el proyecto publica, se pliega el pie de las cinco páginas de
`recursos/` que aún no lo tenían, se da atribución a los tres índices, que no la
llevaban, y se añade el `LICENSE` que faltaba. No se ha tocado el texto de
ninguna gramática, ni el motor, ni el corpus.*

> **Lo primero que tiene que saber el chat nuevo:** el cambio de licencia está
> **cerrado y publicado**, en cuatro commits que llegan hasta `8669411`. Lo que
> queda abierto son tres cosas, y ninguna es de traducción: el número de versión,
> el enganche de Zenodo con GitHub y la comprobación visual de los pliegues.
>
> **Y la regla que gobernó la sesión:** una licencia no se cambia hacia atrás.
> Las versiones ya depositadas se quedan como constancia de lo que se publicó
> bajo ellas. Vale también para lo demás: los briefings viejos no se reescriben
> y las obras ajenas conservan su licencia.

## 0. LO QUE CAMBIÓ, EN UNA TABLA

| | antes | después |
| --- | --- | --- |
| licencia de las páginas | CC BY-NC-SA 4.0 | **CC BY-NC-ND 4.0** |
| páginas con atribución | 9 | **12** |
| páginas de `recursos/` con pie plegado | 1 | **6** |
| `LICENSE` en el repositorio | no existía | **texto legal íntegro** |
| licencia declarada en GitHub | ninguna | **CC BY-NC-ND 4.0** |

## 1. LOS CUATRO COMMITS

| Commit | Qué lleva |
| --- | --- |
| `02242f7` | Licencia CC BY-NC-ND 4.0 y veredictos del 2026-09-02 |
| `eef6fdb` | Pie plegado en las cinco páginas de recursos |
| `bffb713` | Atribución en los índices |
| `8669411` | `LICENSE` y sección de licencia en el `README` |

## 2. DÓNDE SE CAMBIÓ LA LICENCIA

En la fuente, nunca en `site/`:

- las seis plantillas de `recursos/` —sandhi, raíces, paradigmas, nombre, verbo,
  solucionador—;
- `herramientas/generar_capitulo.py`, que escribe el pie de los tres capítulos;
- `herramientas/generar_indices.py`, que ahora escribe además la atribución de
  los índices;
- `.zenodo.json` (`cc-by-nc-nd-4.0`) y `CITATION.cff` (`CC-BY-NC-ND-4.0`);
- `docs/verbo/escaleras-por-adjudicar.md` §8, el bloque de la página del verbo,
  que aún no existe.

### Lo que NO se tocó, y por qué

**Tres menciones al Digital Pāḷi Dictionary** —dos en
`recursos/solucionador/plantilla.html`, una en `docs/solucionador/PROCEDENCIA.md`—
siguen diciendo CC BY-NC-SA. **No es un descuido: es la licencia del DPD**, obra
ajena, y no cambia por aparecer aquí. Lo mismo vale para el material de
Ven. A. Thitzana, de Rūpasiddhi y del Nyāsa.

**Cinco briefings** —09, 16, 18, 19 y 29— nombran la licencia vieja. Se quedan
como están: dejan constancia de lo que se decidió entonces, y reescribirlos sería
falsear el rastro. El 29 es el que hay que corregir hacia adelante, en éste, no
editando aquél.

## 3. EL PIE PLEGADO

El solucionador estrenó el pliegue el 2026-08-29, a petición del IEBH. Ahora lo
llevan las seis páginas de `recursos/`. A la vista queda **el árbol del IEBH y su
crédito**, que es lo que el pie de una página del instituto tiene que decir sin
que nadie pulse nada; las notas, las cifras y la nota de versión van bajo
**«Notas, cifras y fuentes»**.

| Página | Qué se plegó |
| --- | --- |
| verbo | `#pie-fuente` y la nota de versión |
| nombre | los tres párrafos de notas |
| sandhi | nota de versión, Fuentes, Véase también, Cómo leer |
| paradigmas | nota de versión y los dos bloques de idioma |
| raíces | nota de versión y toda la tirada de notas y créditos |

Dos cosas que conviene saber antes de tocarlo:

- **El texto no se quita del documento.** Sigue donde estaba y el buscador lo
  encuentra igual, porque un `<details>` cerrado conserva su contenido en el DOM.
  Lo que **no** ocurre todavía: si un resultado de búsqueda cae dentro de un
  pliegue cerrado, el pliegue no se abre solo. Está ofrecido y sin hacer.
- **La licencia queda SIEMPRE fuera del pliegue**, en las seis páginas. Se
  comprobó una a una.

**En verbo, además, la medida del pie pasó de `66ch` a `104ch`.** Era el origen
de la queja: dejaba en blanco media página mientras la nota de fuente se estiraba
hacia abajo. Las otras cuatro ya iban al ancho de la columna; su problema era
sólo el largo, y lo resuelve el pliegue.

Hay dos familias de paleta y el CSS del pliegue va distinto en cada una:
paradigmas, raíces, sandhi y solucionador usan `--soot`, `--haritala` y `--mono`;
verbo y nombre usan `--ink-soft`, `--ochre` y una pila mono literal, porque no
tienen `--mono`.

## 4. LA ATRIBUCIÓN DE LOS ÍNDICES

La portada, `/kaccayana/` y `/recursos/` llevaban la marca del IEBH y el enlace
al repositorio, pero **no decían bajo qué licencia se publican**. Ahora sí, en
`generar_indices.py`, de modo que la lleve también todo índice que se genere en
adelante. El estilo es `.idx-licencia`, en `site/assets/pali.css`, que es fuente
y no salida.

**No se nombra a Bhikkhu Nandisena en esas tres páginas.** Decisión del IEBH: son
navegación escrita por el instituto —recuentos, descripciones, texto de las
tarjetas—, no su traducción. Dicen sólo:

> Copyright © 2026 Instituto de Estudios Buddhistas Hispano (IEBH). Publicado
> bajo licencia CC BY-NC-ND 4.0.

## 5. EL `LICENSE` Y EL `README`

El repositorio publicaba bajo licencia en doce páginas y no traía el texto legal:
**GitHub no declaraba licencia alguna**. Se añade `LICENSE` con el texto íntegro
de CC BY-NC-ND 4.0, tomado de creativecommons.org y **verbatim**, sin encabezado
propio, para que el detector de GitHub lo reconozca.

El `README` gana una sección «Licencia» que hace constar lo que la licencia deja
fuera, y son dos cosas que conviene no perder de vista:

1. **Las marcas no van en la licencia.** La sección 2(b)(2) excluye los derechos
   de marca y de patente. Reproducir el texto no autoriza a usar el logotipo del
   IEBH. Esto toca de cerca el punto abierto del briefing 19 sobre el permiso de
   marca, que **sigue sin resolverse**.
2. **Las obras ajenas conservan la suya**, con el DPD nombrado explícitamente.

## 6. ZENODO: SE DECIDIÓ NO TOCARLO

El registro `10.5281/zenodo.21948010` es el DOI de concepto y no tiene campo de
licencia propio. Debajo hay dos versiones, **cada una con el suyo**, y las dos
dicen todavía *Attribution Non Commercial Share Alike 4.0*:

| Versión | DOI | Fecha |
| --- | --- | --- |
| 1.1.0 | `10.5281/zenodo.22037060` | 21-ago-2026 |
| 1.0.0 | `10.5281/zenodo.21948011` | 15-ago-2026 |

**Adjudicado por IEBH: no se editan.** El razonamiento, que conviene no volver a
discutir desde cero: **una licencia CC es irrevocable**. Quien obtuvo la 1.0.0 o
la 1.1.0 bajo CC BY-NC-SA conserva esos derechos para siempre, y editar los
metadatos de Zenodo no se los quita — sólo haría que el registro dijera que se
publicó algo que no se publicó. La licencia nueva **rige desde la versión
siguiente**, que `.zenodo.json` ya lleva.

## 7. EL `index.lock` Y DE DÓNDE SALIÓ

A media sesión, `git add` falló con `index.lock: File exists`. **No era un
proceso vivo.** Lo que había en `ps` era `gitstatusd`, el demonio del prompt de
zsh, que es de sólo lectura y nunca toma el lock; en esa máquina saldrá siempre,
de modo que `ps | grep git` no sirve de señal.

El origen está anotado en el propio `.gitignore`: **`ciclo_veredictos.py` hace
`git add -A`**. La cola trajo veredictos a las 16:29:59, `incorporar_adjudicaciones.py`
escribió `casos-reportados.json` a las 16:30, y el lock quedó fechado a las 16:32,
en medio de esa cadena. Se borró a mano y no hubo daño.

**Para la próxima:** un lock de 0 bytes y varios minutos de antigüedad, sin un
`git` con subcomando en `ps`, es basura de un proceso muerto.

## 8. LOS VEREDICTOS DE LA SESIÓN

Entraron dos por la cola, del 2026-09-02, firmados por el IEBH:

- `kumbhiyanti` = *kumbhiyaṃ + iti*
- `abhāsitthāti` = *abhāsittha + iti*

Ya estaban incorporados cuando empezó la sesión. Se corrió la auditoría, como
manda `CLAUDE.md` cada vez que entran veredictos:

    211 casos con sandhi · 181 derivados de un corte · 9 plegando combinar() · 21 sin derivar

**Ninguno de los dos cae en las listas de problemas: los dos derivan solos.** No
hay escalera que proponer a mano de este lote.

## 9. UN ERROR MÍO, ANOTADO PARA QUE NO SE REPITA

Dije que `CITATION.cff` apuntaba al repositorio equivocado, por leer `syncs.json`
y el registro de Zenodo sin comprobar `.git/config`. **Es falso.** El remoto real
es `git@github.com:bthar-mx/gramaticas-pali-es.git`, y los briefings 34 y 35 ya lo
decían. **`bthar-mx` es correcto en todas partes**: en `CITATION.cff`, en el
`README` y en el pie de los tres índices. No hay nada que corregir ahí.

## 10. LO QUE QUEDA ABIERTO

1. **El número de versión.** `.zenodo.json` y `CITATION.cff` dicen `1.1.0`, que es
   justamente la versión publicada bajo la licencia **vieja**. Tal como están,
   atribuyen CC BY-NC-ND a una entrega que no salió con ella. Hay que subirlo
   cuando esto se publique como versión. **Lo decide IEBH.**
2. **El enganche de Zenodo con GitHub.** El zip depositado se llama
   `admin-iebh/gramaticas-pali-es-v1.1.0.zip` y el registro da como repositorio
   `github.com/admin-iebh/gramaticas-pali-es`, pero IEBH empuja a `bthar-mx`. O
   son dos repositorios, o hubo un traslado y el webhook se quedó en el viejo. **Si
   el enganche está en `admin-iebh` y la publicación sale de `bthar-mx`, la próxima
   versión puede no archivarse, y la licencia nueva no llegaría nunca a Zenodo.**
   Sin comprobar.
3. **La comprobación visual de los pliegues.** No se ha hecho y **no puede
   afirmarse**: no hay navegador en el entorno. Falta mirarlos en claro y en
   oscuro y en móvil; en los índices, lo que hay que mirar es `--text3` sobre el
   filete de `.idx-licencia`.
4. **Abrir el pliegue cuando la búsqueda cae dentro.** Ofrecido, no hecho.
5. Siguen abiertos, de antes: el permiso de marca del briefing 19, la escalera de
   tamaños de la serifa y las 2.379 terminaciones por cotejar.
