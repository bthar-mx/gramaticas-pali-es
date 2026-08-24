# Kaccāyana Pāḷi-Español: Briefing de la Sesión 29

*Complementa a los briefings 05–28. Tema único: **el recurso nuevo
`/recursos/raices/`**, con las raíces del Saddanīti, el Dhātupāṭha y la
Dhātumañjūsā. No se tocó ningún capítulo, ni el Kaccāyana, ni los
borradores de las sesiones 27 y 28, que siguen esperando la revisión de
Angel en sus propios chats.*

> **Lo primero que tiene que saber el chat nuevo:** el recurso está
> **publicado y en línea** (v1.3), y todo lo de esta sesión está
> confirmado y enviado: `origin/main` y `HEAD` coinciden en
> **`4fb6fe5`**. No queda nada a medias. Lo que sí queda es lo que
> nunca se hizo, y va en el §7.

---

## 1. ESTADO AL CIERRE

HEAD: **`4fb6fe5`** («Sube la versión: Raíces 1.3 y Paradigmas 1.13»).
`git rev-list --left-right --count origin/main...HEAD` → `0 0`. Árbol
limpio.

Seis commits, todos de esta sesión:

| Commit | Qué |
| --- | --- |
| `40061d5` | Añade la referencia de raíces pāḷi en `/recursos/raices/` |
| `005cadc` | Índice propio del Dhātupāṭha, barra lateral plegable, licencia del IEBH |
| `21c2e5d` | Botón «« ocultar» en la propia barra lateral |
| `fda8a1c` | Pestaña «» Índice» en el borde; punto de millar en la insignia |
| `e7f4477` | El índice se abre siempre al llegar; plegarlo ya no se recuerda |
| `4fb6fe5` | Raíces 1.3, Paradigmas 1.13 |

Archivos nuevos: `herramientas/extraer_raices.py`,
`extraer_dhatupatha.py`, `extraer_dhatumanjusa.py`, `generar_raices.py`;
`recursos/raices/` entero (plantilla + cuatro JSON).

**Paradigmas quedó tocado también** (v1.13): barra plegable y, sobre
todo, ya no llama a `matchMedia` a pelo — lo hacía en cinco sitios y en
un entorno sin `matchMedia` eso abortaba el guion entero.

---

## 2. LAS TRES OBRAS, Y QUÉ ES CADA UNA

No son la misma lista de raíces, y confundirlas es el error fácil.

| Pestaña | Obra | Cuántas | Numeración |
| --- | --- | --- | --- |
| Raíces | Saddanīti-dhātumālā | 1.698 | gaṇa (I-VIII) + **página** |
| Significados | índice inverso de la misma | 776 | — |
| Dhātupāṭha | Andersen y Smith 1921 | 643 | 1–639 + cuatro con letra |
| Dhātumañjūsā | Kaccāyana-Dhātumañjūsā | 154 estrofas | propia, hasta 884 |

**La columna sánscrita del Saddanīti es el Pāṇinīya-dhātupāṭha**, y ahí
la cifra **no es una página sino el número de raíz**. Lo dice la
leyenda de la propia edición (p. 46). Yo lo tuve mal un rato.

**Los gaṇas del Dhātupāṭha no son los del Saddanīti**: son nueve, en la
ordenación de los Dhātupāṭha sánscritos, y el primero se parte en I,a e
I,b. La página lo avisa en el globo de cada sección.

---

## 3. LA FUENTE PRINCIPAL, BIEN ATRIBUIDA

**«Pali Roots in Saddanīti»**, del **Venerable U Sīlānanda**
(1927–2005), *editado por* Bhikkhu Nandisena, CMBT 2005. © 2001 U
Sīlānanda.

Durante media sesión lo tuve mal: llamé a la obra «Pali Roots in
Comparison» —que es el título de la **sección** de la p. 57, no del
libro— y di a Nandisena por autor. Angel lo corrigió. Está arreglado en
la página, los metadatos, los JSON y los guiones.

Enlace al libro, en los créditos:
`https://drive.google.com/open?id=16neD1t6MKCsHNkf0zbi0zdG6nt7IamQl`

**Sobre la licencia.** La página de copyright del libro dice «All
rights reserved. Please do not reproduce ... without written permission
from the Publisher». Lo puse en el pie; Angel decidió volver a la nota
habitual del IEBH (CC BY-NC-SA 4.0), que es la que hay ahora. Queda
anotado aquí por si alguna vez hace falta revisarlo. Los créditos a U
Sīlānanda y el enlace sí se mantienen.

---

## 4. POR QUÉ HIZO FALTA UN EXTRACTOR PROPIO

El PDF de U Sīlānanda **no tiene capa de texto utilizable**. Lo compuso
Quartz de Mac OS X 10.5 con **477 subconjuntos tipográficos**, cada uno
con su codificación y el ToUnicode roto: `pdftotext` devuelve basura.

La solución, en `herramientas/extraer_raices.py`: descomponer cada
glifo a su contorno, redondear y hashear. En todo el libro hay **161
contornos distintos**; se identificaron a la vista una vez y ese mapa
—la constante `GLIFOS`— se propaga a los 477 subconjuntos. Las celdas
se recortan con las propias líneas de la tabla del PDF.

Salen los diacríticos íntegros porque se leen del contorno, no de un
OCR. **Si alguna vez cambia el PDF, `GLIFOS` hay que rehacerlo**: el
guion avisa si el número de contornos no es 161.

Los tres PDF **no están en el repositorio**. `generar_todo.py` publica
lo ya extraído; sólo hay que volver a extraer si cambia una fuente.

---

## 5. LAS REGLAS QUE SOSTIENEN LA FIABILIDAD

Las mismas del sandhi: proponer y verificar, nunca afirmar.

- **La concordancia entre obras es por lema y nada más.** Cuando además
  coincide la glosa pāḷi se marca, y ésa es la que puede darse por
  segura: **229 de 675**.
- **La Dhātumañjūsā se enlaza sólo por coincidencia literal** de la
  palabra en el verso, y con lemas de tres letras o más. **No se
  deshace el metro**: en el śloka la raíz y su significado van
  encajados, y separarlos sería interpretar. Por eso va como texto y no
  como tabla.
- **El español del Dhātupāṭha es prestado.** Andersen y Smith no
  traducen. El inglés viene de la hoja de la digitalización (Bodhirasa
  Bhikkhu, 2019), 643/643; el español se reutiliza del Saddanīti cuando
  la glosa pāḷi es idéntica, 430/643, y la entrada lo marca con
  `ES·N`. Los 213 restantes no son un hueco que rellenar: las dos obras
  glosan el mismo sentido con palabras distintas (*gamanatthā* frente a
  *gatyatthe*).
- **Lo dudoso se marca.** La entrada 169 venía impresa `vadhahiṃsāyaṃ`,
  sin espacio; se resolvió probando cada corte y quedándose con el
  único cuyo significado está atestiguado en otra entrada y que
  recompone la cadena exacta. Las 352/353 comparten número impreso y el
  reparto se deduce de la numeración, sólo porque cuadra exactamente.

**La hoja de cálculo pública confirmó el análisis entero**, por su
cuenta: las 643 claves coinciden, incluidas las cuatro suplementarias
(547a, 554a, 563a, 609a) y el corte 352/353.

---

## 6. LOS ERRORES DE ESTA SESIÓN, PARA NO REPETIRLOS

1. **Un `str.replace` de Python sobre un ancla que aparecía dos veces**
   metió 67 líneas de guion **dentro del `<style>`**. Sólo se vio
   porque la página daba 25 errores de CSS donde Paradigmas daba 0.
   *Comprobar siempre `s.count(ancla) == 1` antes de reemplazar.*
2. **Los guiones no eran guiones de corte.** El original es una tabla
   de Word y Word no parte palabras: `-` y `–` son del texto y separan
   los compuestos (`hiṃsā-saṃkleśa–nayoḥ`). Yo los quitaba.
3. **La letra del Dhātupāṭha no es la inicial de la raíz.** La edición
   agrupa por la consonante: bajo «K» van *bhū, ku, aṃka, saṃkha,
   vaka*. Esa cabecera ya venía en los datos y la plantilla la pisaba
   recalculándola; salían 573 cabeceras con 36 identificadores.
4. **Guardar el estado «barra plegada» era una trampa**, no una
   atención: quien la plegaba una vez volvía cada día a una página sin
   navegación. Ahora no se guarda, y se borra lo que hubiera guardado
   una versión anterior.

---

## 7. LO QUE NO SE HIZO

- **Las raíces de la Dhātumañjūsā, una a una.** Hoy va como poema. Sacar
  pares raíz-significado exige deshacer el metro; se puede intentar con
  la regla de proponer y verificar —publicar sólo lo que recomponga el
  verso—, pero es trabajo aparte.
- **Las 152 entradas del Dhātupāṭha cuyo lema no está en el Saddanīti**
  no tienen ficha propia en la pestaña de Raíces; se ven en la suya.
- **El solucionador de sandhis** del CLAUDE.md sigue pendiente. Las
  1.698 raíces con su gaṇa son, ahora, léxico aprovechable para la
  segmentación.
- **Capítulos 5, 6 y 7**: sus borradores siguen esperando revisión, sin
  tocar en esta sesión.

---

## 8. CÓMO SE REHACE

    # sólo si cambia alguno de los PDF (no están en el repositorio)
    python3 herramientas/extraer_raices.py      ruta/dhatu.pdf
    python3 herramientas/extraer_dhatupatha.py  ruta/dhatupatha.pdf
    python3 herramientas/extraer_dhatumanjusa.py ruta/dhatupatha.pdf

    # lo habitual: publicar lo ya extraído
    python3 herramientas/generar_todo.py

`generar_raices.py` **no publica si los datos no cuadran**: comprueba
lemas, referencias, gaṇas dentro de rango, NFC y que no quede ningún
carácter sin descifrar.

Las pruebas de la página se hicieron con jsdom (`npm i jsdom`), montando
el HTML generado y pulsando de verdad las pestañas, el buscador, los
filtros y la barra lateral. No quedaron en el repositorio; conviene
rehacerlas si se toca la plantilla.
