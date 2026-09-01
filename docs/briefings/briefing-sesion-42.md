# Kaccāyana Pāḷi-Español: Briefing de la Sesión 42

*Complementa a los briefings 05–41. Tema de la sesión 42 (2026-09-01): **abrir
un recurso nuevo, `/recursos/verbo/`**, a partir del documento «Verbo» de
Bhikkhu Nandisena y de trece presentaciones de clase suyas. No se ha tocado el
solucionador ni el corpus. Al cerrar, **la página está hecha y publicada en el
árbol** —datos, maquetado, generador y borrador inglés—, sin commit.*

> **Lo primero que tiene que saber el chat nuevo:** leer
> `docs/verbo/escaleras-por-adjudicar.md` **antes que nada**. Es el informe de
> cotejo, y lleva las NUEVE decisiones que Angel firmó el 1 de septiembre.
> No queda en él ninguna duda abierta; lo único a medias es el inglés. Las reglas de siempre: nada se adjudica sin
> el visto bueno del IEBH; la atribución pública dice IEBH; con Angel se habla
> en inglés y lo del proyecto va en español.
>
> **Y el criterio de esta sesión, que es el de siempre con otra ropa:** una
> escalera que recompone no es todavía una escalera atestiguada. Aquí el
> problema no ha sido el motor sino **dos fuentes del mismo autor que no dicen
> lo mismo**, y la respuesta ha sido la de siempre: cotejar, medir, y dejar la
> firma a Angel.

## 0. EL ESTADO, EN CIFRAS

| | al abrir la 42 | al cerrarla |
| --- | ---: | ---: |
| recursos publicados | 5 | **6** |
| escaleras verbales extraídas | 0 | **31** (14 + 17) |
| paradigmas verbales extraídos | 0 | **105** |
| citas Kacc/Rū comprobadas | — | **195, ninguna discrepa** |

## 1. QUÉ ENTRÓ

Fuentes, ninguna de las dos en el repositorio salvo la primera:

- `docs/fuentes/verbo.docx` — «Verbo (ākhyāta)», Bhikkhu Nandisena, IEBH,
  rev. 7-abr-2013, publicación `20130407-BN-T0021`. 130 tablas.
- `docs/fuentes/verbo-diapositivas/*.pdf` — trece presentaciones `GP-T -
  Verbo-I … XII` (son trece: `VII` y `VII-Voz Pasiva`). **Están en
  `.gitignore`**, como los tres PDF del Saddanīti: viaja el JSON extraído.

Guiones nuevos:

| Guion | Qué hace |
| --- | --- |
| `herramientas/extraer_verbo.py` | docx → `recursos/verbo/verbo.json` |
| `herramientas/extraer_verbo_diapositivas.py` | PDF → `recursos/verbo/diapositivas.json` |
| `herramientas/auditar_verbo.py` | coteja los dos y no corrige nada |

Y el informe: `docs/verbo/escaleras-por-adjudicar.md`.

## 2. EL HALLAZGO DE LA SESIÓN

**La columna de autoridad del documento no es toda de Rūpasiddhi, aunque su
nota al pie lo diga.** Las catorce escaleras terminan citando «11», que es
Kacc. §11 *Naye paraṃ yutte* (= Rū 14). Leído como Rūpasiddhi sería Kacc. §9
*Parasamaññā payoge*, que trata de los términos técnicos y no forma ningún
verbo. En «bhū» las dos numeraciones conviven en una celda: «67, 11».

Se descubrió porque las presentaciones citan siempre el par `Kacc/Rū`. De los
30 pares distintos —107 citas— ninguno discrepa de la concordancia deducida de
`kaccayana/*.md` y `docs/*.md`. **Si esos números se hubieran enlazado como
Kaccāyana, las 87 citas del documento habrían apuntado a suttas sin relación**
(Rū 424 → Kacc §457, no §424).

## 3. LA ERRATA

`9-su`, segunda tabla (*suṇāti*), cita **Rū 513** para el signo ‘ṇā’. Rū 513 es
Kacc. §449 *Kiyādito nā*, la regla del grupo de «kī». `su` es svādi: le
corresponde **Kacc. §448 / Rū 512** *Svādito ṇu-ṇā-uṇā ca*, que es lo que dice
la diapositiva. Comprobado contra el texto del sutta en las dos fuentes.

**Adjudicado por Angel: Kacc. §448 / Rū 512**, señalando en la página que el
documento base lee Rū 513. Queda dar cuenta a Bhikkhu Nandisena, por cortesía,
no como condición.

## 4. LAS CINCO DECISIONES DE ANGEL (2026-09-01)

1. **Se publica el par `Kacc/Rū`**, como hacen las presentaciones.
2. **`suṇāti` se corrige** a Kacc. §448 / Rū 512, con la nota.
3. **Una operación por fila**, como en las diapositivas: cada fila muestra la
   forma RESULTANTE de la regla que se cita a su lado. Consecuencia visible:
   en «bhū» la página imprime `bhav`, forma que el documento no imprime nunca
   —sin ella se pierde de vista adónde fue la «a» de `bhava + a + ti`—. Se
   rotula como venida de la diapositiva.
4. **Entra el material que sólo está en las diapositivas**, siempre que no
   esté ya en el documento, rotulado con su presentación de origen.
5. **Se hace constar que el material se creó en 2013** y se editó y mejoró en
   2026 al preparar la página.

Atribución, idéntica a la de las demás páginas de `recursos/`, más el crédito
que Angel pidió: **todo paradigma tomado de otra obra lleva el suyo**. Los 73
de *otros paradigmas* son de *The Higher Pali Course for Advanced Students*,
Ven. Buddhadatta Thera, Colombo Apothecaries', 1951.

## 5. LAS CUATRO DECISIONES DE LA TARDE

Salieron al automatizar el cotejo, y Angel las firmó el mismo día. **El
informe no tiene ya ningún `<!-- DUDA -->` abierto.**

1. **«hū» y «hu»: se separan**, imprimiendo la forma intermedia. No es
   inventar un paso: Rū 487 = Kacc. §510 *Lopañ c' ettam akāro* elide el signo
   de conjugación, y de `hū + a + ti` no puede salir otra cosa que `hū + ti`.
   Al aplicar la regla resultó que en «hū» esa forma ya está impresa en su
   propio paso 2, de modo que sólo quedan marcadas tres filas en toda la
   página: `gamu` 2, `tuda` 2 y `hu` 6.
2. **«gaha» se publica con la duda a la vista.** Kacc. §490 *halopo ṇhāmhi*
   elide «ha» ante ‘ṇhā’, luego en el paso 5 la raíz tiene que ser todavía
   «gaha»: la fila sospechosa es la 2. Se publica porque es la única escalera
   de gahādi que existe y la celda de ese gaṇa está vacía.
3. **«rudhi», no «rudha».** Lo zanja el propio repositorio:
   `recursos/raices/raices.json` trae las dos como raíces distintas —«rudhi»,
   gaṇa II, «obstruir», que es el rudhādi-gaṇa; «rudha», gaṇa III, «deseo»—.
   El documento junta la grafía de una con el significado de la otra.
4. **«su» con ‘ṇu’ se publica tal cual**, con nota de que ninguna segunda
   fuente lo corrobora.

Aplazado, y lo pidió él: los tiempos ausentes de *otros paradigmas*. Siguen
en pie, como defectos del documento base y no como huecos que rellenar, las
tres entradas en inglés dentro de listas españolas, la celda vacía del
gahādi-gaṇa y el archivo de referencias que el colofón promete y no acompaña
(la diapositiva 2 de `Verbo-I` da probablemente esa lista).

## 6. LA PÁGINA

`/recursos/verbo/`, v1.0, con **barra lateral de índice** —54 entradas, una
por inflexión, escalera y grupo de paradigmas, plegable con el ☰—, **insignia
de versión** con su nota, y cuatro pestañas: Introducción, Inflexiones,
Formación, Paradigmas. Al modo de `/recursos/paradigmas/`.

**Ojo con la tipografía.** Fraunces no lleva las combinadas del pāḷi y componía
«ākhyāta» con el macron descolocado. Todo lo que es pāḷi va ahora en
`<span class="pali">`, que es Gentium Book Plus. Vale para el h1, los
encabezados de grupo, las cabeceras de pada y los subtítulos.

Cada inflexión lleva su **nombre pāḷi junto al castellano** —«presente
indicativo · vattamānā vibhatti»— y, cuando el documento la trae, su nota
(«inserción de ‘a’ es opcional», en imperfecto, aoristo y condicional). Sale
del propio docx: el párrafo que va entre el encabezado y la tabla. Los
títulos del índice van en ocre, como los de `/recursos/paradigmas/`.

| Pieza | Qué es |
| --- | --- |
| `recursos/verbo/plantilla.html` | maquetado y lógica |
| `recursos/verbo/verbo.json` | el documento, verbatim |
| `recursos/verbo/diapositivas.json` | las 17 escaleras de las presentaciones |
| `recursos/verbo/ingles.json` | el borrador inglés, **sin adjudicar** |
| `herramientas/escaleras_verbo.py` | las cinco decisiones, en un solo sitio |
| `herramientas/generar_verbo.py` | valida y publica |

**21 escaleras publicables** (15 de las diapositivas, 6 del documento), **105
paradigmas**, **3 filas marcadas «propuesta»** —`gamu` 2, `tuda` 2, `hu` 6—.
De los §N, **29 enlazan** y **105 no**, porque el Ākhyāta-kappa no está
publicado; salen en texto plano con un `title` que lo explica y se enlazarán
solos el día que entre `kaccayana/06-akhyata-kappa.md`.

### El inglés, entero y publicado

Dos capas, como en `/recursos/paradigmas/`: **interfaz** y **prosa del IEBH**.
La diferencia es que aquí la prosa **está adjudicada y se publica** —Angel lo
pidió el 1-sep-2026—, de modo que el botón EN cambia la página entera y el pie
dice «English translation approved by IEBH».

Volver atrás es un booleano: `"adjudicado": false` en
`recursos/verbo/ingles.json` y la página en inglés vuelve a mostrar la prosa
española con su aviso. No hay que tocar nada más.

La cobertura se comprueba en cada publicación —71 cadenas, ninguna sin
traducir, ninguna sobrante—: si el español cambia, `generar_verbo.py` avisa y
retiene la prosa en vez de publicar una traducción incompleta.

La terminología no se inventó: sale de la traducción inglesa que el propio
Nandisena hizo del Ākhyāta-kappa (`docs/6 - Ākhyāta-Kaccāyana.md`). De ahí
que las vibhatti se queden en pāḷi entre comillas, que «root», «person» y
«conjugational sign» sean sus palabras, y que *sattamī* sea **potential** y
no «optative».

El cotejo para firmar, con los cinco puntos que quedan por decidir:
`docs/verbo/ingles-por-adjudicar.md`.

## 7. POR DÓNDE SIGUE LA 43

1. **Leer el inglés con calma.** Está publicado, pero la traducción se hizo en
   una tarde; `docs/verbo/ingles-por-adjudicar.md` guarda el cotejo lado a
   lado y los cinco puntos donde el inglés se aparta o podría discutirse
   —«potential» por *sattamī*, la glosa de *parassapada/attanopada*, *kāraka*
   por «voz»—.
2. Un **buscador o filtro** para los 105 paradigmas, como el de
   `/recursos/paradigmas/`. El índice de la izquierda ayuda, pero no busca.
3. Las escaleras del documento **no traen explicación** —el docx no tiene esa
   columna—, de modo que 6 de las 21 enseñan el paso y la autoridad y callan
   el porqué. Las diapositivas sí la traen, y la misma regla se explica
   siempre igual: se podría rellenar desde ellas. **Es decisión de Angel**, no
   se ha hecho.

**Nada se ha empujado.** El trabajo está en el árbol, sin commit, para que
Angel lo revise antes.
