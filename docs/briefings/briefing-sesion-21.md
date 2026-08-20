# Kaccāyana Pāḷi-Español: Briefing de la Sesión 21

*Complementa a los briefings 05–20. La sesión 21 transcurrió en dos chats a la
vez. En el otro se incorporó el **Nyāsa-Pāḷi** como referencia de segunda capa
—es lo principal de hoy y está en la sección 2—. En éste sólo se verificó esa
incorporación y se escribió este briefing. **No se tocó ni una forma pāḷi, ni
el sitio, ni la paleta.** Todo lo que quedó abierto en el briefing 20, §5,
sigue abierto y se repite aquí al final.*

---

## 1. ESTADO AL CIERRE

**Sin commitear al escribir esto:** el árbol `docs/fuentes/nyasa/` entero y
este briefing. Órdenes para Angel:

    git add docs/fuentes/nyasa/ docs/briefings/briefing-sesion-21.md
    git commit -m "fuentes: Nyāsa-Pāḷi (Mukhamattadīpanī) como referencia de segunda capa; briefing sesión 21"
    git push

Antes de ejecutarlas conviene decidir una cosa: **el master pesa 1,01 MB y los
nueve extractos otro 1,01 MB**, de modo que el repositorio —que es público—
crece ~2 MB de una vez. Si se prefiere no duplicar, la extracción es
reproducible con `dividir_nyasa.py` a partir del master y podría quedarse
fuera; pero entonces hay que decirlo en `CLAUDE.md`, porque el que clone no
tendrá los capítulos. **Sin decidir.**

Del briefing 20 quedaba pendiente de commitear la corrección de `CLAUDE.md` y
el propio briefing 20 (`git add CLAUDE.md docs/briefings/briefing-sesion-20.md`).
**Comprobar si eso llegó a hacerse** antes de encadenar el commit de hoy.

## 2. NYĀSA-PĀḶI: INCORPORADO

Se incorpora el **Nyāsa-Pāḷi (Mukhamattadīpanī)**, de Vimalabuddhi, como
**referencia de segunda capa, al mismo nivel que Rūpasiddhi**.

**Procedencia:** transcripción `.docx` de la edición Sudhammavatī (Yangon).

### Qué hay y dónde

`docs/fuentes/nyasa/`:

| Archivo | Qué es |
| ------- | ------ |
| `Nyasa_Pali_Mukhamattadipani_master.md` | el master; md5 `df5699b9ae436590e0e36d5361e32707` |
| `Nyasa_errata.md` | registro de correcciones — **leerlo antes de usar nada** |
| `Nyasa-00-prologo-y-matika.md` … `Nyasa-08-unadi.md` | extracción por capítulos |
| `limpiar_nyasa.py`, `dividir_nyasa.py` | los dos scripts |

Los nueve extractos llevan cabecera de procedencia y el aviso de **no editar
ahí**: se corrige en el master y se regenera.

### Verificado en esta sesión

No se dio nada por bueno de oídas:

- **md5 del master:** `df5699b9ae436590e0e36d5361e32707` — coincide.
- **Recomposición byte a byte:** se ejecutó `dividir_nyasa.py`, que trae su
  propia comprobación (`assert recomp == t`). Responde
  `recomposición byte a byte: OK`.
- **Aviso para el que repita la comprobación a mano:** concatenar los nueve
  archivos da 1.016.517 bytes frente a los 1.012.387 del master. **No es una
  discrepancia**: son las nueve cabeceras de procedencia añadidas (4.130
  bytes). La comprobación válida es la del script, que las descuenta.
- **Las cinco anclas citadas** —§12, §52, §53, §271, §284— resuelven a los
  archivos que les tocan.
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
4. **Corrupción de espaciado extensa en los capítulos 4–8** (Samāsa, Taddhita,
   Ākhyāta, Kibbidhāna, Uṇādi): palabras fusionadas y partidas a mitad de
   línea, p. ej. «gadhi iccetasmā ikapaccayohotītiñāpa naṃtthaṃ». Demasiado
   ambigua para arreglo mecánico: **se corrige capítulo por capítulo en el
   punto de uso**, cuando cada capítulo entre en traducción. Los capítulos 1–3
   están notablemente más limpios.
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
OCR: no se cita textualmente sin verificar**, como avisan las propias cabeceras
de los extractos.

### Pendientes del Nyāsa

- **Escaneo en birmano como árbitro de lecturas**, verificando que la
  paginación coincide con los marcadores `[p. N]`.
- **Añadir `docs/fuentes/nyasa/` a `CLAUDE.md`**, junto a las demás fuentes.
- Decidir la zona gris de la errata §3, punto por punto.
- Decidir si los nueve extractos entran al repositorio o se regeneran (§1).

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
   cautelas de la sección 2.
4. URL más corta (configuración de Cloudflare).
5. `recursos/nombre/`: rediseño con la paleta nueva delante.
6. Las listas «De similar declinación»; los opcionales nunca pedidos.
7. **El permiso de la marca (briefing 19, §8): sigue sin respuesta.** Si
   resultara que el Venerable no lo sabe, `git revert` de `776c81f` y
   `79ba7c3`.
8. **El siguiente capítulo a traducir: sin decidir y hay que preguntarlo.** El
   4 (Samāsa) vive en otro hilo y sus archivos no se tocan. *Y ojo: el
   capítulo 4 del Nyāsa es de los que llevan la corrupción de espaciado.*
9. **`memory.md` del proyecto:** el briefing 20 dejó redactada la versión al
   día y se la entregó a Angel para pegarla en claude.ai, porque el archivo es
   de sólo lectura desde Cowork. **Comprobar si ya está pegado.** Si no, el
   viejo sigue diciendo que el Nāma-Kappa está parado en §203, que es falso —
   los capítulos 1–3 están completos y publicados.

## 4. RECORDATORIOS QUE NO CAMBIAN

- **Ninguna orden de git desde el sandbox, ni siquiera `status`** — deja un
  `.git/index.lock` que Angel borra a mano. Para saber el estado del
  repositorio: leer `.git/refs/heads/main` y `.git/logs/HEAD` como texto.
- Nada se edita dentro de `site/` salvo `pali.css`, `pali.js` y los SVG de la
  marca.
- Lo tomado de Thitzana, Rūpasiddhi **o Nyāsa** se señala como suyo; la flecha
  de Thitzana va al revés.
- Ante duda, `<!-- DUDA: … -->` y decirlo en voz alta. Nada se añade, quita ni
  cambia respecto de la edición base sin que Angel decida.
- Con Angel se habla en inglés; el producto va en español.
