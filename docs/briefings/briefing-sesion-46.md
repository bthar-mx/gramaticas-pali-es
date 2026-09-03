# Briefing de la sesión 46 — el glosario de terminología gramatical

**Fecha:** 2026-09-03. **Lo que se empezó:** una obra nueva del repositorio,
`/recursos/glosario/`, que reúne la terminología con que las gramáticas
clásicas hablan de sí mismas. **Estado:** en curso, 11 de 44 páginas del
Conspectus transcritas. **Lo que hay que hacer:** seguir por la página 1116.

---

## 1. Qué es esto y de dónde sale

Angel pidió reunir los términos gramaticales pāḷi de dos obras y traducirlos
al español y al inglés, tomando como base el glosario que ya existía, y
cotejarlos después con el Diplomado del IEBH. Las fuentes son **dos, y las dos
son principales** —esto lo corrigió él expresamente, porque el primer intento
daba a Smith el papel principal y relegaba a Nandisena—:

| clave | obra | qué aporta | dónde vive |
| --- | --- | --- | --- |
| `nandisena` | **Glosario de términos gramaticales de la lengua pali**, Bhikkhu Nandisena, IEBH / Dhammodaya, 2013, rev. 7-IV-2013, publicación 20130407-BN-T0022 | 649 entradas con definición **en español** y referencia a Kac., Rū., Sad., Nir. | `recursos/glosario/nandisena.json` |
| `conspectus` | **Conspectus Terminorum** (saññāmātikā), sección E del vol. IV de la edición de **Helmer Smith** del Saddanīti, pp. 1105-1148 (Lund, Gleerup, 1949) | definición **en francés**, dentro de una terminología ordenada por materias | `recursos/glosario/conspectus/pNNNN.json` |
| `glosario` | `comun/glosario.md` | la lista **normativa interna**: qué castellano se ha fijado. No es obra de nadie. | ya existía |
| `diplomado` | **Diplomado en Lengua Pāḷi I** del IEBH (Moodle, curso 4), instructor **Dr. Aleix Ruiz Falqués** | tercera voz: términos nuevos y equivalencias divergentes | `recursos/glosario/diplomado.json` |

### LAS DOS FUENTES NO SON TESTIGOS INDEPENDIENTES

En su propia bibliografía, **Nandisena declara que le fue «muy útil» el
Conspectus de Smith.** Por tanto, cuando las dos coinciden **eso no es
confirmación cruzada: es filiación**. Donde difieren es donde hay algo que
mirar. La página lo dice en su aviso de cabecera y en el pie, y no debe
presentarse de otro modo.

---

## 2. Dónde está el trabajo

    recursos/glosario/
      conspectus.json          metadatos del Conspectus (fuentes, secciones, plan de Smith)
      conspectus/p1105.json … p1115.json   una página, un archivo
      nandisena.json           las 649 entradas, extraídas del PDF
      glosario-ingles.json     propuesta inglesa para comun/glosario.md — SIN adjudicar
      diplomado.json           la cosecha del curso del IEBH
      plantilla.html           maquetado y lógica (FUENTE, se edita)
    herramientas/
      extraer_glosario_nandisena.py   del PDF de Nandisena a nandisena.json
      generar_glosario.py             lo junta todo → site/recursos/glosario/index.html

Está enganchado a `generar_todo.py`, de modo que el hook de pre-commit lo
regenera solo.

**Una página, un archivo**: son 44 páginas y unas 2.000 entradas; con un solo
JSON había que reescribirlo entero para añadir una página. `generar_glosario.py`
recorre `conspectus/p*.json` y calcula solo el estado («en curso — N de 44»).

---

## 3. Por dónde se sigue

**Transcritas: 1105-1115. La siguiente es la 1116.** El reparto de Smith,
que él mismo declara en la p. 1105:

| epígrafes | materia | estado |
| --- | --- | --- |
| 1.1 – 1.3 | fonética, sandhi, prosodia y métrica | hecho (1105-1108) |
| 2.1 – 2.3 | el verbo | hecho (1109-1111) |
| 3.0 – 3.3 | el nombre: kita, taddhita, flexión | **a medias** — va por 3.3.3, casos |
| 4.1 – 4.3 | los indeclinables (upasagga, nipāta) | pendiente |
| 5.1 – 5.3 | sintaxis: kāraka, samāsa, la frase | pendiente |
| 6.1 – 6.3 | semántica, tropos y figuras | pendiente |
| 7.1 – 7.3 | instrumental filológico | pendiente |
| 8.1 – 8.9 | **Conspectus Terminorum (Metricorum)**, pp. 1149-1172 | **fuera de alcance por ahora** |

Angel decidió: **el gramatical primero (1105-1148), el métrico después**, como
pieza aparte.

### Cómo se transcribe

El escaneo **no tiene capa de texto y ningún OCR lo lee** (ver
`recursos/saddaniti/LEEME.md`). Se lee a ojo. Lo que funciona:

    pdftoppm -r 170 -f $((PAGINA-921)) -l $((PAGINA-921)) -png -singlefile \
      recursos/saddaniti/saddaniti-smith-04.pdf /ruta/pNNNN

**La página impresa N es la N-921 del PDF del vol. 04.** A 170 dpi se lee
cómodo; para una duda concreta, 400 dpi y recorte con `convert -crop … -resize`.

Cada entrada lleva: `pali`, `fr` (**verbatim de Smith**), `es` y `en`
(**propuesta**), `epigrafe`, `pagina`, `fuente`, y cuando toca `variantes`,
`nota`, `conflicto`, `duda`, `ref_smith`, `ref_interna`.

---

## 4. Decisiones tomadas en esta sesión, que no se vuelven a discutir

1. **El español de Nandisena es suyo y va literal.** No se retoca.
2. **El francés de Smith va literal**, con su cursiva deshecha.
3. **El español y el inglés que añadimos son PROPUESTA**, no adjudicados por
   el IEBH, y la página lo dice en la cabecera y en cada ficha. Angel eligió
   publicar con el aviso visible, no esperar a la firma.
4. **`comun/glosario.md` manda** sobre cualquier propuesta. Donde Smith no
   coincide, la ficha lo marca «difiere de la norma».
5. **Una página, un archivo**; el estado lo calcula el generador.
6. La tarjeta de `/recursos/` **todavía no se ha puesto**: la página existe
   pero no está enlazada. Ponerla cuando Angel dé el visto bueno
   (`herramientas/generar_indices.py`, lista de tarjetas, y también su copia
   inglesa).

---

## 5. Lo que hay que enseñarle a Angel para que decida

### 5.1 Choques terminológicos vivos

| término | `comun/glosario.md` | Nandisena | Smith | Diplomado |
| --- | --- | --- | --- | --- |
| **lahu** | leve | «leve. Igual que rassa, corta.» | *une tranche légère* | **breve** |
| **garu** | — | «(sílaba) fuerte» | *une tranche lourde* | — |
| **guṇa** | — | «fortalecimiento de la vocal» | *renforcement apophonique : 1er degré* | **grado pleno** |
| **vuddhi** | — | «incremento; vocal fortalecida» | *2ème degré* | **grado aumentado** |
| **āgama** | — | «inserción… aumento» | *le phonème de transition* | **aumento; consonante epentética** |
| **upasagga** | **prefijo** (Nāma §221) | — | *préverbe* | **preverbio** |
| **niggahīta** | *niggahita*, sin macrón | registra las dos, remite a niggahīta | niggahīta | niggahīta |

- **lahu es el más serio**: la norma del repositorio fija «leve» y **prohíbe
  expresamente «breve»** (la prohibición se puso para *rassa*), y el Diplomado
  llama «Breves» a las vocales lahu. Nandisena está con la norma.
- **āgama**: la propuesta hecha desde Smith («el fonema de transición») es más
  estrecha que Nandisena y que el Diplomado. **Hay que ensancharla.**
- **niggahita/niggahīta**: conviene unificar en el repositorio. Es decisión suya.

### 5.2 Erratas detectadas, ninguna corregida por cuenta propia

- **Smith, p. 1108**: imprime `sukkhuccāraṇatthaṃ`, con **kkh**, contra
  *sukha-* y contra el *sukhuccāraṇīya* de la línea anterior. Comprobado a
  ×2,3 sobre la imagen nativa: el impreso dice eso. Va tal cual, marcado
  «por cotejar».
- **Nandisena, p. 6**: `avutta-kattu lit., subjeto no mencionado` — le falta
  la coma que separa el lema (y dice «subjeto»). Se restituye la coma y se
  deja constancia en el campo `errata`.
- **Nandisena, p. 31**: `suti-sāmañña` **no tiene definición** en el impreso,
  sólo la referencia (Sad. i 167). No es fallo del extractor.
- **Diplomado, Clase 19**: imprime `āmaṇtanā` y `nimantaṇā`, con **ṇ**, que no
  es forma pāḷi posible tras *ma*. Smith confirma las lecturas correctas:
  **āmantana** y **nimantana** (p. 1110).

### 5.3 Un defecto conocido en la extracción de Nandisena

La **última** entrada del libro (`hetu-kattu`, p. 31-32) continúa a la página
siguiente **sin sangrar**, y el trozo final acaba publicándose como un
`suddha-kattu` duplicado. Un caso en 649. Está reportado por el propio guion
(«lema(s) repetido(s)»), no escondido.

---

## 6. El Diplomado del IEBH: qué se hizo y qué queda

Se recorrieron **los 30 PDF** del curso (28 dossieres + Currículum +
Vocabulario) extrayendo su capa de texto **con pdf.js dentro del navegador**,
en la sesión de Angel. **No se descargó nada** ni se guarda el contenido: sólo
términos y la línea de contexto. Las 22 Presentaciones no se recorrieron
—repiten los dossieres en diapositivas—.

Dos apuntes técnicos por si hay que repetirlo:
- Moodle no sirve pdf.js, y la CSP no deja cargarlo de cdnjs **desde el mundo
  aislado de la extensión**; sí desde el mundo de la página, inyectando un
  `<script>` y **escondiendo `define.amd`** mientras carga, porque si no el
  RequireJS de Moodle se traga el UMD y no define el global.
- El puente entre los dos mundos es un nodo del DOM (`#__puente`).

**Lo que queda, y es importante:** la comparación se hizo contra un Conspectus
**incompleto** (4 páginas). Ya se vio el efecto: tres términos que se dieron
por «ausentes de Smith» —*ajjhiṭṭha*, *nimantana*, *āmantana*— estaban en la
p. 1110, sin transcribir todavía. **Cuando esté completo el Conspectus hay que
rehacer el cotejo entero**, y `diplomado.json` lleva ya corregida esa parte.

---

## 7. Cifras al cerrar la sesión

| | |
| --- | --- |
| entradas de Nandisena | 649 |
| términos del Conspectus | 457 (11 páginas de 44) |
| normativos de `comun/glosario.md` | 53 |
| **únicos, sin repetir lema** | **986** |
| de ellos, sólo en el Conspectus | 344 |
| proyección al terminar las 44 páginas | ~1.600-1.700 únicos |

Se comprueba con:

    python3 herramientas/generar_glosario.py

que **no publica** si hay pāḷi fuera de NFC, una entrada del Conspectus sin
glosa francesa, una página fuera de 1105-1148, un epígrafe con forma rara o un
lema repetido dentro del mismo epígrafe.
