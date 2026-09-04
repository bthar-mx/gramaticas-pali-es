# Kaccāyana Pāḷi-Español: Briefing de la Sesión 22

*Complementa a los briefings 05–21. La sesión 22 tuvo un solo hilo y fue de
**restitución**: se devolvió al texto publicado lo que la traducción y la
conversión a texto habían perdido por el camino. No se tradujo ni un sutta
nuevo; no se tocó el capítulo 4.*

> **Lo primero que tiene que saber el chat nuevo:** §10.1 —el pendiente que
> venía de los briefings 04 y 05 y que el 21 sacó a la luz— **está hecho**.
> Y se hizo también algo que no estaba previsto: recuperar del PDF la
> negrita del vutti. Los tres capítulos son hoy bastante más fieles a la
> edición base que ayer.

---

## 1. ESTADO AL CIERRE

HEAD: **`b613d81`**, más un cambio de redacción sin commitear (la
descripción del Nyāsa en el índice). Comprobado **sin ejecutar git**,
leyendo `.git/refs/heads/main`, `.git/logs/HEAD` y
`.git/refs/remotes/origin/main` como texto plano.

Publicado en Zenodo: **v1.1.0**, DOI de versión
`10.5281/zenodo.22037060`, 21 de agosto. Etiqueta `v1.1.0` en el
repositorio.

Los commits desde el cierre de la 21:

| Hash | Qué |
| ---- | --- |
| `b7983fc`/`454d16c` | índice: fuera Moggallāna-vyākaraṇa, dentro Nirutti-dīpanī |
| `054df79` | pāḷi a 16 px y tinta plena |
| `3e96409` | **§10.1: referencias canónicas del Nāma y el Kāraka** |
| `7f1abfc` | citas: tolerar las erratas de la base y las mayúsculas |
| `8c9734c` | **negrita del vutti (Nāma y Kāraka)** |
| `7ef346a` | negrita del vutti en los tres capítulos |
| `f71b34d`/`f8a865e` | división «Saṃ-sāsv iti»; peso del tipo en oscuro |
| `2328d53` | v1.1.0: versiones de capítulo, CITATION.cff, .zenodo.json |
| `66a447c` | DOI de concepto en el pie, el README y CITATION.cff |
| `b00f7d9`/`b613d81` | índice: el Nyāsa entre las obras previstas ← HEAD |

(Hay cuatro pares de commits con el mismo mensaje. No es un error: son
reintentos del hook, que regenera y añade `site/`.)

## 2. §10.1: LAS REFERENCIAS CANÓNICAS, RESTITUIDAS

Los briefings 04 y 05 mandaban reponer «en la fase HTML» las referencias
—`(Khu. i, 336)`— que la traducción había retirado. Nunca se hizo.

**Hecho.** `herramientas/restituir_citas.py`, que las saca de la edición
base y las coloca **sólo donde hay ancla única dentro del bloque pāḷi** del
sutta que les toca.

| | detectadas | colocadas | pendientes |
| --- | ---: | ---: | ---: |
| Nāma | 129 | 118 | 11 |
| Kāraka | 99 | 95 | 4 |

Los tres capítulos muestran hoy **222 citas** (el Sandhi nunca perdió las
suyas: es anterior a aquella decisión).

**Tres correcciones al planteamiento del briefing 21, por si vuelve a
citarse:**

1. **No era un agujero de tres capítulos.** El Sandhi las conserva; el
   Kāraka tenía siete, todas dentro de una nota al pie de Nandisena.
2. **«Restituir en la fase HTML» ya no es ejecutable.** El maestro también
   las había perdido, y `site/` se regenera en cada commit: lo escrito ahí
   desaparece. La restitución va a los maestros de `docs/`.
3. **Las tablas de los briefings son un registro parcial** —unas 34 de las
   228—. La fuente real es el archivo de Nandisena.

**Presentación:** no se marcan en el maestro. El generador las reconoce
solas (la sigla es un conjunto cerrado, el tomo va en romanos) y las envuelve
en un emergente que desata la sigla: *Khu. i, 336* → «Khuddaka-nikāya · tomo
i, página 336». Tabla de siglas en `comun/guia-de-estilo.md` §5.2 y en
`ABREVIATURAS` de `generar_capitulo.py`. Gracias a la autodetección, las seis
del Sandhi ganaron emergente **sin tocar su texto**.

**Verificado por tres vías:** reconstrucción sutta a sutta (deshechas las
inserciones por posición, el bloque vuelve idéntico); las 222 están dentro
del bloque pāḷi y ninguna en línea española (guía de estilo §5); y el cotejo
con la tabulación a mano de los briefings 04 y 07 da **13 de 13**.

### Erratas de la edición base descubiertas al hacerlo

El emparejador se negó a colocar tres citas porque la palabra no existía en
el español. No existía porque **el español ya había corregido a Nandisena**:

| Sutta | Nandisena | El maestro |
| ----- | --------- | ---------- |
| §275 | saṅkha**m**eyya | saṅkameyya |
| §277 | bhi**kh**ave | bhikkhave |
| §290 | sam**y**ena | samayena |

El IEBH confirmó las tres lecturas del maestro. **No se corrigió nada**: se le
enseñaron al emparejador (`VARIANTES` en `restituir_citas.py`).

## 3. LA NEGRITA DEL VUTTI (no estaba previsto)

El IEBH se fijó en que Nandisena imprime en negrita, **dentro del vutti**, las
letras o sílabas que el propio sutta nombra:

    §237  Itthiyam ato āpaccayo
          Itthiyaṃ vattamānāya **a**kārato **ā**paccayo hoti.

No es adorno: dice qué parte de la explicación responde a qué palabra del
aforismo. **Se había perdido entera**: los `.md` de Nandisena no tienen ni
una marca. Sobrevive sólo en los PDF, donde la negrita es una fuente aparte
(`Times-Bold`) y `pdftohtml -xml` la devuelve etiquetada.

`herramientas/restituir_negritas.py`. El IEBH subió los tres PDF.

| Capítulo | Tramos | Líneas rechazadas |
| -------- | -----: | ----------------: |
| Sandhi | 100 | 19 |
| Nāma | 806 | 57 |
| Kāraka | 74 —60 ya estaban a mano— | 15 |

**990 tramos** en total. El sitio no necesitó nada: `enfasis()` ya convertía
`**x**` en `<strong>`.

**Lo que costó afinarlo**, por si hay que repetirlo con otro capítulo:

- Los diacríticos vienen de otra fuente, así que las palabras llegan
  partidas y el espacio entre tramos es a veces posición y no carácter
  (`si gasañño` → `sigasañño`). Se compara **sin espacios**.
- El PDF parte en líneas físicas lo que el maestro guarda como párrafo. Se
  busca **por subcadena**, no por igualdad.
- El maestro tiene cosas que el PDF no: glosas `{akkharā|letras}`,
  marcadores `[^22]`, y las citas que el Sandhi guarda en nota al pie
  mientras el PDF las imprime entre paréntesis. El emparejador es ciego a
  todo eso.
- **El Sandhi no tiene `convertir_sandhi.py`.** Su fuente viva es
  `kaccayana/01-sandhi-kappa.md`; `docs/1. Sandhi-Kappa.md` es sólo archivo,
  y ya diverge.

**Lo rechazado lo es casi todo porque la capa de texto del PDF falla justo
donde cambia la fuente** —`yathāsaṅkyaṃ` por *yathāsaṅkhyaṃ*, `etessa` por
*etassa*—. Emparejar con tolerancia sería invitar a la corrupción silenciosa
en pāḷi. Se informa, no se coloca a ojo.

## 4. LO QUE ANGEL DECIDIÓ HOY

- **`Saṃ-sāsv iti`**: manda el maestro, no la división `Saṃ-sāsvī ti` de
  Nandisena. Vale para toda su clase. Es la única divergencia de división
  registrada. Guía de estilo §5 bis; el emparejador la conoce.
- **saṅkameyya, bhikkhave, samayena**: lecturas correctas, ya en el maestro.
- **La escalera serif**: manda el pāḷi. `.pali-block` de 14 px atenuado a
  **16 px y tinta plena**, a la par de `.gloss`. Se descartó el +1 px de
  toda la escalera: escalaba sin cerrar la diferencia.
- **Modo oscuro**: la negrita del vutti se marca **también con oropimente**.
  Sobre fondo oscuro las formas claras se ven más gruesas de lo que son y
  Gentium no tiene peso intermedio; el tono no lo altera ese efecto.
- **Índice**: fuera el Moggallāna-vyākaraṇa; dentro la **Nirutti-dīpanī** de
  Ledi Sayadaw y el **Nyāsa**.
- **Release v1.1.0**, no 2.0.0.

## 5. DOS ITEMS DEL §1.4 CERRADOS, DE PASO

Estaban marcados «por cotejar con el PDF» en
`docs/notas-de-trabajo-nama.md` §1.4. Con el PDF delante:

- **§238, nota 77**: dice de verdad que «anadādi» son palabras «en ‘u’ y
  ‘o’». La lectura rara es de Nandisena, no del OCR.
- **§269, nota 83**: imprime «musa-paṇacāge» y «§638» tal cual. El `[sic]`
  estaba bien puesto.

**Quedan seis de los ocho.**

## 6. LO QUE SIGUE ABIERTO

### Nuevo de esta sesión

1. **15 citas sin ancla única.** §132 tiene tres `(DA. i, 58)` sobre `Duve
   samaṇā / Duve brāhamaṇā / Duve janā`: **decidir si van las tres o sólo la
   primera fija el criterio de las demás.** Las otras: §68, §81, §130 ×2,
   §132 ×3, §173, §175 ×2, §275 ×2, §308, §315 —éstas dos últimas, ya
   presentes o irrelevantes—. Lista en `docs/fuentes/citas-canonicas.json`.
2. **57 + 15 + 19 líneas de negrita rechazadas**, casi todas por defectos de
   la capa de texto del PDF.
3. **El maestro del Nāma escribe `Saṃsāsv iti` (sin guion) y el título de
   §62 `Saṃ-sāsv`.** Unificarlo desbloquearía alguna línea más de negrita.
4. **`docs/1. Sandhi-Kappa.md` es un archivo muerto que diverge** de la
   fuente viva. Decidir si se resincroniza o se retira.
5. **La descripción de Zenodo y `.zenodo.json` difieren en redacción** (no
   en cifras). Se arregla solo en la próxima entrega.

### Heredado, y sin tocar

6. **Lo gordo: proponer y verificar las 2379 desinencias** de
   `recursos/paradigmas/paradigmas.json` contra los suttas del Nāma.
   Sacaría las cuatro erratas sin decidir: `mānā`, `gāmanino`, `sakkhe`, la
   coma de `mātūbhi`. **Candidato a sesión entera y en limpio.**
7. **El escaneo del Nyāsa (54 MB)**: el IEBH se inclina por Release, no repo.
   Sigue sin hacerse, y el original de 357 MB también.
8. **`docs/fuentes/nyasa/` no está en `CLAUDE.md`.** Sigue pendiente.
9. **`pañcamī / sattamī` no llegó a `comun/glosario.md`.**
10. **Los diecisiete apartados de Thitzana** de `notas-de-trabajo-nama.md`
    §1.1, ofrecidos y nunca decididos.
11. **Seis decisiones del §1.4** aplicadas al texto y nunca confirmadas.
12. **La zona gris de `Nyasa_errata.md` §3**, punto por punto.
13. **El permiso de la marca (briefing 19 §8): sigue sin respuesta.** Si el
    Venerable no lo sabe, `git revert` de `776c81f` y `79ba7c3`.
14. **El siguiente capítulo a traducir: sin decidir. Hay que preguntarlo.**
    El 4 vive en otro hilo y sus archivos no se tocan.
15. URL más corta; `recursos/nombre/` con la paleta nueva; las listas «De
    similar declinación».

### Cerrado, para no volver a abrirlo

- La paleta «hoja de palma» **está revisada y aprobada**. El degradado
  radial no llega más allá de la primera pantalla en páginas de 35 000 px:
  se deja como está, porque uno que siguiera al lector llamaría la atención
  sobre sí mismo.
- `memory.md`: resuelto en la 21.

## 7. RECORDATORIOS QUE NO CAMBIAN

- **Ninguna orden de git desde el sandbox, ni siquiera `status`.** Leer
  `.git/refs/heads/main`, `.git/logs/HEAD` y `.git/index` como archivos.
- **Tras tocar `pali.css` hay que regenerar**: la huella del CSS va dentro
  de cada página. Sin eso el navegador sirve el estilo viejo. Pasó hoy.
- **Y el HTML no lleva huella**: al comprobar algo en el sitio, recargar con
  Cmd+Shift+R. Hoy costó un rato entender por qué «no se veían» las citas.
- Nada se edita dentro de `site/` salvo `pali.css`, `pali.js` y los SVG.
- Lo tomado de Thitzana, Rūpasiddhi o Nyāsa se señala como suyo; la flecha
  de Thitzana va al revés.
- Ante duda, `<!-- DUDA: … -->` y decirlo en voz alta.
- **El DOI del pie y de `CITATION.cff` es el de concepto** (`21948010`), no
  el de una versión. Resuelve siempre a la más reciente. No «corregirlo».
- Con IEBH se habla en inglés; el producto va en español.
