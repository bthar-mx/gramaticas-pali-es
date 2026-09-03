# Descripción del depósito 2.0.0 — POR ADJUDICAR

*Borrador para la sesión 44. **No está incorporado a `.zenodo.json` ni a
`CITATION.cff`.** Lo firma Angel; hasta entonces, los dos archivos siguen
diciendo lo que decían.*

## 0. Por qué se reescribe

La descripción depositada describe la versión 1.1.0: «los tres primeros
capítulos completos, 315 suttas». Era exacta el 21 de agosto de 2026. Desde
entonces el texto de la gramática apenas se ha movido —una sola enmienda, la
lectura de *saṃ-sāsu ekavacanesu vibhattādesesu* en el Nāma-kappa—, pero el
repositorio ha crecido en 243 commits y 352 archivos con **material que la
descripción no menciona**: dos obras de referencia completas, un solucionador
de sandhis, el barrido del Saddanīti y el servicio que recoge los veredictos.

Depositar 2.0.0 con la descripción de 1.1.0 archivaría una licencia correcta
sobre una descripción que cubre menos de la quinta parte de lo depositado. La
descripción es, además, lo que un lector ve en la página del registro.

## 1. Lo que se propone decir

> Traducción española del **Kaccāyana-vyākaraṇa**, la gramática clásica más
> antigua de la lengua pāḷi, con el texto pāḷi completo, análisis morfológico de
> los ejemplos, notas, glosario terminológico y concordancia con el
> Padarūpasiddhi y el Saddanīti-Suttamālā.
>
> **La gramática.** Los tres primeros capítulos completos, 315 suttas:
> **Sandhi-kappa** (§1–§51, combinación eufónica), **Nāma-kappa** (§52–§270,
> morfología nominal) y **Kāraka-kappa** (§271–§315, los casos gramaticales).
> Conservan las **222 referencias canónicas** y los **990 tramos de negrita**
> con que Nandisena señala, dentro del vutti, las letras que cada sutta nombra,
> restituidos desde la edición base y verificados por reconstrucción.
>
> **El aparato de referencia**, que es lo que distingue a esta versión de la
> anterior. Seis obras auxiliares, todas navegables y enlazadas al texto:
>
> - **Raíces pāḷi** — las 1.698 raíces del *Saddanīti-dhātumālā* en la edición
>   del Venerable U Sīlānanda, con su índice inverso de 776 significados, las
>   643 entradas del *Dhātupāṭha* de Andersen y Smith y las 154 estrofas de la
>   *Kaccāyana-Dhātumañjūsā*. La concordancia entre obras se establece por lema;
>   cuando además coincide la glosa pāḷi, se marca, y sólo esa es firme.
> - **Paradigmas** — 84 paradigmas de declinación nominal y pronominal en los
>   ocho casos.
> - **Combinación eufónica** — las 49 reglas del Sandhi-kappa y 266 formas
>   atestiguadas con su secuencia de formación. De ellas, 49 están copiadas de
>   la traducción del capítulo, 175 calculadas y comprobadas contra la forma
>   atestiguada, y 42 construidas a partir del propio aforismo. Ninguna
>   secuencia se publica si no reproduce exactamente la forma atestiguada.
> - **El verbo · ākhyāta** — las ocho inflexiones, los nueve gaṇas, 105
>   paradigmas y 14 escaleras de formación.
> - **Formación del nombre** — la derivación de *pācako*, paso a paso.
> - **Solucionador de sandhis** — dado un pasaje en pāḷi, propone los cortes y
>   la cadena de aforismos que los explica, y **verifica cada propuesta
>   recomponiéndola**: lo que no reproduce la forma de entrada se descarta.
>   Incluye 262 casos adjudicados por el IEBH.
>
> **Lo que la herramienta todavía no puede hacer, dicho con números.** Sobre las
> 2.045 junturas del banco de pruebas, la lectura del IEBH es la primera
> propuesta del motor en 1.618. En las 416 restantes no lo es, y en 296 de ellas
> lo que falla no es la elección de la partícula sino el punto del corte, con
> todas las candidatas recomponiendo por igual. Se documenta así, y no como
> porcentaje de acierto, porque **el Tipiṭaka es la fuente y Kaccāyana la
> autoridad que lo explica, no la que lo autoriza**: una lectura impecable por
> las reglas no es todavía una lectura del canon.
>
> **Edición base:** la traducción de Bhikkhu Nandisena (ITBMU), seguida al pie
> de la letra; los desgloses estructurales y material complementario proceden de
> la edición de Ven. A. Thitzana; el texto pāḷi se coteja con la edición de la
> PTS (Pind) y con el Nyāsa-Pāḷi (Mukhamattadīpanī). Las expansiones
> morfológicas propias y toda desviación de la edición base están señaladas como
> tales.
>
> **Las obras ajenas conservan su propia licencia**, y el *Digital Pāḷi
> Dictionary* —empleado como testigo, no como fuente— la suya, CC BY-NC-SA.
>
> El markdown del repositorio es la fuente; el sitio publicado, con navegación
> por sutta, referencias cruzadas enlazadas y exportación EPUB, se sirve en
> <https://gramaticas.buddha-dhamma.net>.
>
> Un proyecto del Instituto de Estudios Buddhistas Hispano (IEBH). Obras
> previstas en el mismo repositorio: Nyāsa, Padarūpasiddhi, Saddanīti y
> Nirutti-dīpanī.

## 2. Las cifras, y de dónde sale cada una

| Cifra | Origen | Comprobada |
| --- | --- | --- |
| 315 suttas, §1–§315 | descripción de 1.1.0 | sí, sin cambio |
| 222 referencias, 990 tramos | descripción de 1.1.0 | sí, sin cambio |
| 1.698 raíces · 776 significados | `raices.json` | sí |
| 643 entradas del Dhātupāṭha | `dhatupatha.json` | sí |
| 154 estrofas | `dhatumanjusa.json` | sí |
| 84 paradigmas · 8 casos | `paradigmas.json` | sí |
| 49 reglas · 266 formas | `reglas.json` | sí |
| 49 / 175 / 42 por procedencia | `CLAUDE.md`, §«Estado de recursos/sandhi» | sí |
| 8 inflexiones · 9 gaṇas · 105 paradigmas · 14 escaleras | `verbo.json` | sí |
| 262 casos adjudicados | `casos-reportados.json` | sí |
| 2.045 junturas · 1.618 · 416 · 296 | `CLAUDE.md`, §«el estado medido del motor» | sí |

## 3. Tres decisiones que son de Angel, no mías

1. **El título.** El depósito se llama *«Kaccāyana-vyākaraṇa — traducción
   española»*. Sigue siendo exacto —la traducción es la espina dorsal y el DOI
   de concepto lleva ese nombre—, pero ya no describe todo el contenido. Mi
   recomendación es **dejarlo**, y que el crecimiento se cuente en la
   descripción; conviene que sea una decisión tomada, no una omisión.

2. **El párrafo de los números del motor.** Es inusual publicar en un registro
   académico lo que la herramienta NO resuelve. Va porque es la regla del
   proyecto, pero es material que queda archivado con DOI y sin marcha atrás.

3. **`upload_type`.** El depósito está declarado como `publication` /
   `publication_type: book`. Con un solucionador, un léxico y un worker dentro,
   cabe preguntarse si 2.0.0 no es ya `software` o un depósito mixto. **No lo
   he tocado**: cambiarlo altera cómo se cita la obra y cómo la indexa OpenAIRE.

## 4. Lo que falta para publicar la versión

1. Firmar esta descripción (o corregirla).
2. `version` a `2.0.0` en `.zenodo.json` y en `CITATION.cff`; `date-released`
   al día.
3. **Sync now** en la pestaña GitHub de Zenodo — el registro se sincronizó por
   última vez hace una semana.
4. Etiquetar `v2.0.0` y empujar. El webhook está puesto en
   `bthar-mx/gramaticas-pali-es` y **no se ha disparado nunca**: esta será la
   primera prueba de punta a punta.
