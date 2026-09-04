# Kaccāyana Pāḷi-Español: Guía de estilo y formato del proyecto

*Documento de referencia — convenciones establecidas durante la traducción del capítulo 1-Sandhi-Kappa, basado en U Nandisena (ITBMU), con cotejo de Ven. A. Thitzana (Vol. 2) y Rūpasiddhi.*

---

## 1. Idioma de trabajo

- **Conversación/discusión técnica:** inglés (para evitar doble traducción pāli → inglés → español al cotejar con la edición de U Nandisena).
- **Entrega final (la traducción):** español.
- El usuario puede cambiar de idioma libremente; Claude responde en el idioma que mejor convenga al contexto.

---

## 2. Flujo de trabajo

- Traducción **sutta por sutta** (no por bloques grandes), para que el usuario revise y apruebe cada uno antes de continuar.
- Una vez aprobado, el usuario copia el texto a un Google Doc.
- Antes de traducir, Claude debe revisar el documento original (PDF/OCR) para no omitir notas al pie, ejemplos o secuencias de formación de palabras.

---

## 3. Estructura de cada entrada de sutta

**Plantilla de cada entrada:**

> **[Núm. Kaccāyana]. [Núm. Rūpasiddhi]. [Sutta en pāḷi] ([Núm. Saddanīti-Suttamālā, si existe]).** [Desglose estructural en corchetes, N]
>
> [Texto pāḷi de la vutti, sin traducir]
> [Ejemplos en pāḷi, con referencias bibliográficas originales]
> [Pregunta "Kvacī/Navā/Vā ti kasmā?" en pāḷi, si aplica]
>
> ---
>
> *[Traducción al español del gloss/sutta — debe ser tan breve como el original; si el original es una sola palabra ("Long."), la traducción también debe serlo ("Larga.")]*
>
> *[Traducción al español de la vutti — oración completa explicativa]*
>
> *Ejemplos: [traducción o cita de los ejemplos, SIN referencias bibliográficas]*
>
> ---
>
> [Si hay secuencias de formación de palabras, mostrarlas bajo "Ejemplos [con secuencia de formación]:", con "Secuencia:" antes de cada una]
>
> ---
>
> [Si hay contraejemplos, mostrarlos bajo "Contraejemplos:" o "Contraejemplo:"]
>
> ---
>
> [Notas del traductor numeradas, ancladas con superíndice en el texto correspondiente]

### Numeración de referencia (triple numeración)

Formato: **[Núm. Kaccāyana]. [Núm. Rūpasiddhi]. Texto del sutta ([Núm. Saddanīti-Suttamālā]).**

- El primer número es el número de sutta de Kaccāyana (numeración principal y secuencial que usamos para referirnos a los suttas, p. ej. "§14").
- El segundo número es el número correspondiente en Rūpasiddhi.
- El número entre paréntesis (cuando existe) es el número correspondiente en Saddanīti-Suttamālā. No todos los suttas lo tienen.
- **Nota:** en algunos casos (p. ej. sutta §2) el texto fuente de Nandisena presenta dos números entre paréntesis en lugar de uno; esto queda pendiente de verificación contra el Saddanīti-Suttamālā y no debe bloquear el avance de la traducción.

### Desglose estructural [entre corchetes]

Justo después de la línea del sutta, se incluye el desglose en componentes/palabras, siguiendo el modelo de Ven. A. Thitzana, p. ej.:

> **2. 2. Akkharā p' ādayo ekacattālīsaṃ (1, 2).** [Akkharā + api + a-ādayo + ekacattālīsaṃ, 4]

- Los componentes se separan con " + ".
- Se usa un guion para unir elementos que forman parte del mismo segmento por sandhi pero deben mostrarse por separado conceptualmente (p. ej. *a-kāro*, *o-u-dantānaṃ*, *dve-bhāvo*).
- Al final, después de una coma, el número total de componentes (no la palabra "palabras").
- Cuidado especial: verificar que los segmentos del desglose correspondan a los lexemas reales del compuesto (p. ej. "tatrākāro" = *tatra* + *a-kāro*, no *tatra* + *ākāro*, ya que "akāro" es la designación *-kāra* de la letra "a").

---

## 4. Convenciones tipográficas

- **Comillas dobles ("...")**: para palabras completas (p. ej. "evaṃ", "dhammo").
- **Comillas simples ('...')**: para letras, sílabas individuales, y prefijos (p. ej. 'a', 'ṃ', 'ti', 'abhi', 'adhi', 'ava', 'pati', 'anu', etc.). Los prefijos siempre usan comillas simples, no dobles, ya que son unidades sub-léxicas.
- Excepción: cuando 'eva' y 'hi' se citan como palabras desencadenantes de una regla gramatical (p. ej. en §32), se usan comillas simples por su función de partículas/sílabas en ese contexto gramatical.
- Usar comillas tipográficas/inteligentes ("…", '…') en el texto en español. (Nota: pendiente de resolver un problema técnico de copia/pegado hacia Google Docs — el usuario está evaluando usar Buscar y reemplazar con expresiones regulares como solución alternativa.)
- **"EM"** = "edición moderna" (equivalente a "ME" = "Modern Edition" en el original de Nandisena), usado en las secuencias de formación de palabras.

---

## 5. Referencias bibliográficas canónicas

- **En el texto pāḷi:** se conservan las referencias originales (p. ej. *Khu. i, 67*; *Vin. iii, 19*; *M. i, 243*).
- **En las líneas traducidas al español:** estas referencias **se omiten**. Es suficiente con que aparezcan en el texto pāḷi.

### 5.1 Restitución (sesión 22)

Durante la traducción de los capítulos 2 y 3 las referencias se retiraron
también del pāḷi, con el plan —briefings 04 y 05, §10.1— de reponerlas «en la
fase HTML». Nunca se hizo. Se han restituido con
`herramientas/restituir_citas.py`, que las toma de la edición base, las
coloca sólo en el bloque pāḷi y verifica cada inserción por reconstrucción.
Las que no tienen ancla única no se colocan: quedan listadas en
`docs/fuentes/citas-canonicas.json` a la espera de decisión.

El Sandhi-Kappa nunca las perdió: es anterior a aquella decisión.

### 5.1 bis. Dónde va la cita, y cuántas (sesión 23)

Dos reglas, decididas por IEBH sobre el caso de §132, donde Nandisena pone
`(DA. i, 58)` tres veces sobre `Duve samaṇā / Duve brāhmaṇā / Duve janā`:

1. **Se repite la cita en cada ejemplo atestiguado**, aunque sea la misma
   referencia tres veces seguidas. Poner sólo la primera daría a entender
   que los otros dos ejemplos no están atestiguados, lo que sería falso.
2. **La cita va donde la pone la edición base**, que no es siempre el final
   de la frase: cuando lo que la referencia certifica es la voz ilustrada,
   va pegada a esa voz y no al final de la oración.

        §132  Duve (DA. i, 58) samaṇā. Duve (DA. i, 58) brāhmaṇā.
        §130  Amuṃ (M. i, 210) rājānaṃ passasi; asu (D. ii, 162) rājā tiṭṭhati.
        §175  Nāya, tāya; naṃ (Khu. i, 308), taṃ; ne (DhA. i, 6), te; …

   En §175 no hay siquiera frase que cerrar: la lista son formas sueltas.
   Mover la cita al final de la oración habría sido rehacer la edición base,
   que es justo lo que `CLAUDE.md` prohíbe.

### 5.1 ter. Por qué quedaron quince pendientes (sesión 23)

No por ambigüedad, como se creyó en la 22: **por un defecto del
emparejador**. `anclas_candidatas` arma el ancla uniendo voces con un solo
espacio, pero entre esas voces el maestro imprime comas y puntos —«Duve
samaṇā. Duve»—, y `normalizar` comparaba la puntuación al pie de la letra.
De modo que **ningún ancla de más de una voz podía coincidir nunca**: el
emparejador caía siempre al ancla de una sola voz, que casi nunca es única,
y por eso informaba «sin ancla única».

Corregido —se descarta la puntuación al comparar, y también los asteriscos,
que desde `restituir_negritas.py` pueden partir un ancla—, **doce de las
quince se resolvieron solas**, con anclas de hasta seis voces y sin
necesidad de ordenar ocurrencias ni de adivinar nada.

Como la edición base no está en el repositorio, el modo `--pendientes`
reemparejar las que quedaron listadas en `citas-canonicas.json` sin
necesidad de ella, y actualiza el JSON para que la operación sea
idempotente:

    python3 herramientas/restituir_citas.py --pendientes            # prueba
    python3 herramientas/restituir_citas.py --pendientes --aplicar

### 5.1 quater. Erratas de la edición base que el maestro ya traía corregidas

No se corrige nada: se le enseñan al emparejador (`VARIANTES` en
`restituir_citas.py`) para que la cita encuentre su sitio pese a la errata.

| Sutta | Nandisena | El maestro | Sesión |
| ----- | --------- | ---------- | ------ |
| §275 | saṅkha**m**eyya | saṅkameyya | 22 |
| §277 | bhi**kh**ave | bhikkhave | 22 |
| §290 | sam**y**ena | samayena | 22 |
| §132 | brāh**a**maṇā | brāhmaṇā | 23 |

### 5.1 quinquies. Correcciones a la edición base

Distintas de la tabla anterior: allí el maestro ya traía la lectura buena y
sólo había que enseñársela al emparejador. Aquí **se corrige**, por decisión
expresa del IEBH.

| Sutta | Nandisena | Corregido a | Sesión |
| ----- | --------- | ----------- | ------ |
| Kāraka §275 | jātaka | **jātakā** | 23 |
| Sandhi, nota 2 (invocación) | Vasantilaka Gāthā | **estrofa en metro *vasantatilakā*** | 45 |
| Sandhi, notas 6 y 7 (§10, §11) | «See §13 for formal formation of the word» | **Véase §12**: la formación está impresa bajo Kacc. §12 (= Rū. 13) | 45 |

En §275 la lista de los nueve aṅgas aparece dos veces —bajo `Pañhe` y bajo
`Kathane`— y la edición base imprimía *jātakā* en la primera y *jātaka* en
la segunda. Corregida la segunda, **las dos listas son ya idénticas**, de
modo que las dos citas `(Khu. vii, 111; VinA. i, 22; DA. i, 24)` han dejado
de tener ancla única: están puestas y verificadas, pero una pasada futura de
`restituir_citas.py --base` volvería a darlas por pendientes. No es un
error: es el emparejador negándose a elegir, que es lo que debe hacer.

### 5.1 sexies. El Sandhi-Kappa, unificado con los capítulos 2 y 3 (sesión 45)

El Sandhi-Kappa, anterior a la regla de §5, llevaba las citas en **notas al
pie** y con las siglas del documento español del Venerable (*Reglas de
combinación eufónica*, 2013): `Dh. 67`, `Sn. 306`, `Khp. 6`, `J. i 74`,
`Ud. 148`, `Vv. 119`, `Bv. 322`, `Dhk. 1`, `Dhs. 93`, `Ps. 291`, `Vbh.A. 466`.
Son las mismas citas que la edición base imprime como `Khu. i, 67`, etc.:
**el número es en ambos sistemas la página de la edición birmana**, no el
número de estrofa — `Dh. 67` es Dhp 375, no Dhp 67 —, sólo que el siglum
español desata el tomo del Khuddaka en la obra concreta.

Por decisión del IEBH (2026-09-03), el Sandhi-Kappa sigue ahora la misma
regla que Nāma y Kāraka: **la cita va en línea, en el bloque pāḷi, tal como
la imprime la edición base** (`Yass’ indriyāni samathaṅgatāni (Khu. i, 27,
358), …`), y las citas que estaban en líneas españolas se retiran. Se
cotejaron una a una contra el PDF de Nandisena (cap. 1, 48 pp.). Cambios
respecto de lo que había:

- `Vi. iv, 292` (§25, errata de la edición base) → `Vin. iv, 292`.
- `Aṅ. i, 311` (§37) → `A. i, 311`, sigla normalizada.
- `S. 408` (§14) se conserva tal cual: la edición base no da tomo.
- Repuestas las citas que faltaban: las diez del *suttavibhāga* de §20 y
  `(A. iii, 424)` en §36.
- La sigla `khu.` en minúscula de §24 → `Khu.`.

`ABREVIATURAS` gana `JA`, `VinA`, `AbhiA` y `SuttanipātaA`.

Las citas de `recursos/sandhi/reglas.json` proceden del documento español
del Venerable y conservan su siglum (`Dh. 67`); son la misma página birmana.

<!-- DUDA: ¿conviene añadir en el emergente el número de estrofa (Dhp 375)
     verificado contra Pind (PTS)? Exige comprobar ~110 citas una a una; no
     se ha hecho. El IEBH decide si vale la pena. -->

### 5.2 Presentación

No se marcan en el maestro. El generador las reconoce solas —la sigla es un
conjunto cerrado y el tomo va en romanos— y las envuelve en un emergente que
desata la sigla. **La expansión es mecánica, no una identificación de la
edición:** el tomo y la página remiten a la que usa Nandisena, que no consta
en los archivos del proyecto.

<!-- DUDA: ¿qué edición hay detrás de los números de tomo y página de
     Nandisena? Si es la birmana de la Sexta Recitación, conviene decirlo en
     el emergente; mientras no se confirme, no se nombra ninguna. -->

| Sigla | Se desata como |
| ----- | -------------- |
| `D.` | Dīgha-nikāya |
| `M.` | Majjhima-nikāya |
| `S.` | Saṃyutta-nikāya |
| `A.` | Aṅguttara-nikāya |
| `Khu.` | Khuddaka-nikāya |
| `Vin.` | Vinaya-piṭaka |
| `Abhi.` | Abhidhamma-piṭaka |
| `J.` | Jātaka |
| `DA.` `MA.` `SA.` `AA.` | el aṭṭhakathā del nikāya correspondiente |
| `DhA.` | Dhammapada-aṭṭhakathā |
| `UdānaA.` | Udāna-aṭṭhakathā |
| `PetavatthuA.` | Petavatthu-aṭṭhakathā |
| `Sad.` | Saddanīti |
| `Mog.-pañcikā` | Moggallāna-pañcikā |

La tabla vive en `herramientas/generar_capitulo.py` (`ABREVIATURAS`). Las
siglas que no estén ahí no reciben emergente: aparecen tal cual, que es
preferible a desatarlas a ojo.

---

## 5 bis. Negrita dentro del vutti (sesión 22)

Nandisena imprime en negrita, **dentro del vutti**, las letras o sílabas que
el propio sutta nombra. No es adorno: dice qué parte de la explicación
responde a qué palabra del aforismo.

    §237  Itthiyam ato āpaccayo
          Itthiyaṃ vattamānāya **a**kārato **ā**paccayo hoti.

    §238  Nadādito vā ī
          **Nadā**dito vā a**nadā**dito vā … **ī-**paccayo hoti.

Se perdió al convertir el PDF a texto y se ha restituido con
`herramientas/restituir_negritas.py`, que la lee del PDF —allí la negrita es
una fuente aparte, `Times-Bold`— y la coloca sólo donde la línea del PDF
aparece **una sola vez** en los bloques pāḷi del capítulo. Verificación por
reconstrucción: quitadas las marcas, el maestro vuelve byte a byte.

**Alcance: sólo el bloque pāḷi.** El título del sutta va entero en negrita
en el PDF y aquí no la lleva; las líneas españolas tampoco, como en la
edición base.

### Lo hecho

| Capítulo | Tramos | Líneas rechazadas |
| -------- | -----: | ----------------: |
| Sandhi | 100 | 19 |
| Nāma | 801 | 64 |
| Kāraka | 74 —60 ya estaban puestos a mano— | 15 |

El emparejador es ciego a lo que un lado tiene y el otro no: espacios,
asteriscos, glosas emergentes `{akkharā|letras}` y —porque el Sandhi guarda
en notas al pie lo que el PDF imprime entre paréntesis— marcadores `[^22]` y
citas canónicas.

### Lo que quedó fuera, y por qué

Casi todo lo rechazado lo es porque **la capa de texto del PDF falla justo
donde cambia la fuente**: `yathāsaṅkyaṃ` por *yathāsaṅkhyaṃ*, `etessa` por
*etassa*, `aṃ-āadesā` por *aṃ-ā ādesā*. Emparejar con tolerancia sería
invitar a la corrupción silenciosa en pāḷi, así que se descarta.

### La división «…sv iti», fijada

Aparte había 18 líneas del Nāma con una divergencia de fondo, no de
extracción: Nandisena divide `Saṃ-sāsvī ti kimatthaṃ?` donde el maestro lee
`Saṃ-sāsv iti kimatthaṃ?`.

**Manda el maestro: se escribe `Saṃ-sāsv iti`** (el IEBH, sesión 22). Vale
para todas las de su clase —`Ekavacanesv iti`, `Vibhattādesesv iti`— y es
la única divergencia de división registrada frente a la edición base.

El emparejador la conoce: reconoce `…svī ti` del PDF como `…sv iti` del
maestro, de modo que la negrita de esas líneas se coloca sin tocar la
división adoptada.

---

## 6. Notas al pie (notas del traductor)

- Se presentan bajo el encabezado **"Nota(s) del traductor:"**, numeradas.
- El número de nota debe ir **anclado con superíndice** en la palabra o frase específica del texto a la que corresponde — nunca como comentario flotante sin referencia clara.
- Incluyen: aclaraciones gramaticales, explicación de partículas (*ca*, *kvaci*, etc.), variantes textuales, y referencias cruzadas a otros suttas.
- La numeración de notas se reinicia en cada sutta (cada sutta tiene su propia secuencia 1, 2, 3...). Las notas de los versos introductorios también tienen su propia secuencia independiente. Esto es consistente y no genera confusión.

---

## 7. Traducción de moods/formas verbales

- **Optativo (sattamī vibhatti), 3.ª persona singular** (p. ej. *viyojaye*, *pappoti*): se traduce con la construcción impersonal **"se debería + infinitivo"** (p. ej. *"se debería separar..."*), reflejando el carácter genérico/impersonal del precepto gramatical pāḷi.

## 8. Distinción sutta vs. vutti en la traducción

- El **sutta** suele expresar un **estado/cualidad** (p. ej. *assaraṃ* = "desprovista de vocal").
- La **vutti** suele expresar la **acción/procedimiento** (p. ej. *katvā* = "habiendo hecho/desproveyéndola").
- No trasladar el sentido causativo de la vutti a la traducción del sutta mismo; mantener cada uno en su propio registro.
- El gloss/traducción del sutta debe imitar la **brevedad** del original (incluyendo el propio gloss en inglés de Nandisena como referencia): si el sutta es una sola palabra, la traducción española también debe serlo.

---

## 9. Terminología fija del proyecto

| Término pāḷi | Equivalente en español | Notas |
|---|---|---|
| *sandhi* | **combinación eufónica** | Preferido sobre "unión eufónica"; coincide con el título en inglés de Thitzana ("Euphonic Combinations Chapter") |
| *akkhara* | **letra** | Provisional; sujeto a posible reemplazo global más adelante |
| *sara* | **vocal** | |
| *byañjana* | **consonante** | |
| *rassa* | **corta** | No usar "breve" |
| *dīgha* | **larga** | |
| *lahu* (mattā) | **leve** | No usar "liviana" (p. ej. "de medida leve") |
| *vagga* / *vaggā* | **agrupada(s)** | No usar "grupo(s)" como adjetivo; el sutta §7 establece esta convención |
| *ghosa* | **sonora(s)** | |
| *aghosa* | **sorda(s)** | |
| *niggahita* | **niggahita** (sin traducir) | Se deja como término técnico |
| *Gaṇa* (en los versos introductorios) | **Orden** | No "Sangha"; *Gaṇa* y *Saṅgha* son términos pāḷi distintos |
| *kvaci* | **a veces** | |
| *navā* | **ocasionalmente** | Sinónimo funcional de *kvaci*, pero se distingue léxicamente en español |
| *vā* | **opcionalmente** | |
| *vibhāsā* | **facultativamente** | Sinónimo funcional de *vā*, pero se distingue léxicamente en español |

*(Ver el documento separado "Kaccayana_Terminologia_Particulas_Opcionales.md" para el detalle completo de kvaci/vā/navā/vibhāsā y las funciones de 'ca'.)*

---

## 10. Cierre de sección (kaṇḍa) y de capítulo (kappa)

Al final de cada sección, se traduce la fórmula de cierre:

> **Iti [capítulo]-kappe [ordinal] kaṇḍo**
> *Así termina la [ordinal] sección del capítulo de [nombre del capítulo].*

Al final de cada capítulo:

> **[Capítulo]-kappo niṭṭhito**
> *Fin del capítulo de [nombre].*

(Ordinal en pāḷi: *paṭhamo* = primera, *dutiyo* = segunda, *tatiyo* = tercera, *catuttho* = cuarta, *pañcamo* = quinta.)

(Nombres de capítulos: *sandhi* = Sandhi, *nāma* = Nāma, *kāraka* = Kāraka, *samāsa* = Samāsa, *taddhita* = Taddhita, *ākhyāta* = Ākhyāta, *kibbidhāna* = Kibbidhāna.)

---

## 11. Líneas horizontales

- Se usan líneas horizontales (---) para separar el bloque del texto pāḷi del bloque de la traducción española.
- También se usan para separar secciones distintas dentro de una entrada (p. ej. entre la traducción y las secuencias de formación, entre las secuencias y los contraejemplos, etc.).
- En suttas muy cortos sin ejemplos ni secuencias, las líneas horizontales se aplican igualmente para mantener la uniformidad visual.

---

## 12. Título del documento y homenaje inicial

- **Título principal:** KACCĀYANA-BYĀKARAṆAṂ / GRAMÁTICA DE KACCĀYANA
- **Homenaje:** *Namo Tassa Bhagavato Arahato Sammāsambuddhassa* → "Homenaje al Bienaventurado, el Arahant, el Completa y Perfectamente Iluminado"
- *Gaṇa* en los versos introductorios → "la noble Orden" (no "el noble Sangha")
- *Sandhi-Kappa* → "Capítulo de Sandhi" (no "Capítulo sobre Sandhi")

---

## 13. Otros acuerdos generales

- Cuando el usuario hace una corrección, Claude debe aplicar el ajuste de forma consistente hacia adelante (y, si se le pide, retroactivamente a entradas ya traducidas).
- Ante construcciones gramaticales ambiguas o decisiones de traducción no triviales, Claude debe explicar su razonamiento (morfología, análisis de la partícula, comparación con Thitzana/Rūpasiddhi/Pind) antes de proponer una traducción, en lugar de traducir de forma automática.
- Cuando haya discrepancias entre las fuentes (Nandisena, Thitzana, Rūpasiddhi, Pind) sobre numeración o contenido, señalarlas explícitamente al usuario en vez de resolverlas unilateralmente.

---

*Documento de referencia de estilo y formato — Proyecto "Kaccāyana Pāḷi-Español"*

---

## 9. La edición inglesa (sesión 45)

Decidida por IEBH el 2026-09-03 con permiso del Venerable Nandisena. Lo
normativo está en `CLAUDE.md` («La edición inglesa») y en
`comun/convenciones.md` §1 bis; aquí, lo práctico.

- **Maestro paralelo:** `kaccayana/NN-nombre.en.md`, misma estructura que el
  español bloque a bloque —pāḷi, glosa, vutti, secuencias, notas— de modo
  que un guion pueda cotejarlos (el de la sesión 45 comprobó: 51 cabeceras
  iguales, 51 bloques pāḷi iguales, 394 líneas de secuencia iguales salvo
  «(EM)» → «(ME)», 35 notas en el mismo orden).
- **Lo que cambia respecto del español, y sólo eso:** la prosa. El pāḷi, las
  citas, las secuencias y los desgloses son los mismos.
- **Rótulos ingleses** (los reconoce el generador): `Sequence:`,
  `Examples [with formation sequence]:`, `Counter-example(s):`, `(ME)` por
  «(EM)», `Extension by “ca” (accumulating):`, «Thus ends the … section of the
  chapter on sandhi», «End of the Sandhi Chapter».
- **Glosas emergentes** `{término|glosa}` en inglés; los 23 términos del Sandhi
  y su inglés están en el memorando, §2.6 y en el propio maestro.
- **Versión propia:** `version_en`, `version_fecha_en`, `version_nota_en` en
  `CAPITULOS`; la inglesa del Sandhi nace en 1.0.
- **Dónde se publica:** `site/en/kaccayana/sandhi/`. El botón EN/ES de cada
  página lleva a la otra conservando el ancla `#sN`, y guarda la elección en
  `pali_lang`, la misma clave de la portada; una página que encuentra en esa
  clave la otra lengua **redirige** a la otra página. `hreflang` en las dos.
- **Créditos del pie inglés:** «Pāḷi text and English translation by Bhikkhu
  U Nandisena (ITBMU); edition, apparatus and glossary by the IEBH».
- **El apéndice del Venerable** (aplicaciones de «ca»; *kvaci, vā, navā,
  vibhāsā*) está verbatim en `docs/fuentes/nandisena-apendice-sandhi-en.md`
  y todavía no se publica en ninguna de las dos ediciones.

