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

### Lo que quedó fuera, y por qué

De las líneas con negrita del Nāma se colocaron 789 tramos y se rechazaron
67 líneas. Casi todas se rechazan porque **la capa de texto del PDF falla
justo donde cambia la fuente**: `yathāsaṅkyaṃ` por *yathāsaṅkhyaṃ*,
`etessa` por *etassa*, `aṃ-āadesā` por *aṃ-ā ādesā*. Emparejarlas con
tolerancia sería invitar a la corrupción silenciosa en pāḷi, así que se
descartan.

Aparte hay 18 líneas con una divergencia de fondo, no de extracción:
Nandisena divide `Saṃ-sāsvī ti kimatthaṃ?` donde el maestro lee
`Saṃ-sāsv iti kimatthaṃ?`.

<!-- DUDA: esa división —«…vī ti» frente a «…v iti»— es sistemática y nadie
     la había registrado. ¿Se conserva la del maestro o se vuelve a la de la
     edición base? Afecta a 18 líneas del Nāma. -->

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
