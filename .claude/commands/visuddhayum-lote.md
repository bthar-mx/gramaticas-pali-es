---
description: Analiza una tanda de suttas del Visuddhāyuṃ y escribe sus filas en la nota de trabajo
argument-hint: "§108-§119  (o «108 119», o «108-119 nama»)"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(python3 herramientas/visuddhayum/*), Bash(ls:*), Bash(mkdir:*), Agent
---

# Tanda del Visuddhāyuṃ: $ARGUMENTS

Antes de nada, lee la sección «Visuddhāyuṃ — análisis por sutta» de
`CLAUDE.md` y el encabezado de `docs/visuddhayum/nama-piloto.md` (estado,
decisiones del IEBH, marcas). Mandan sobre esta orden.

**No ejecutes ninguna orden de git, ni `git status`. No ejecutes
`herramientas/publicar.sh`.** De git se ocupa el IEBH.

## 0. Preparar

1. Interpreta el rango. Si no se da ninguno, toma el siguiente tramo pendiente
   según el estado de la nota y **dilo antes de empezar**.
2. Convierte cada § al número del libro:
   - hasta §232: nº del libro = §;
   - desde §234: nº del libro = § − 1 (§233 no tiene encabezado).
3. Sitúa el tramo en el PDF (página del PDF = página del libro + 46). La
   tabla de tandas de la nota da la horquilla; afínala con

       python3 herramientas/visuddhayum/loc.py A B

   que lista los encabezados «(n) … padaṃ», los (က) y los (ခ). Comprueba la
   numeración `kaṇḍa.pariccheda.sutta` del encabezado: es la verificación
   independiente del nº, y el OCR se equivoca con los números.
4. Si el OCR no lee un encabezado (le pasa a §85, §96, §113, §115), localiza
   el sutta a mano con `lines.py` y recorta con `crop.py`.

## 1. Por cada sutta

1. **Recorta el sutta entero en bandas solapadas**, del encabezado al
   encabezado siguiente, sin huecos:

       python3 herramientas/visuddhayum/lines.py N                    # líneas y alturas de la página
       python3 herramientas/visuddhayum/crop.py N a b salida.jpg      # por índice de línea
       python3 herramientas/visuddhayum/crop.py N yA yB salida.jpg    # por píxeles (y en los dos extremos)

   Bandas de unos 500 px con al menos 100 px de solape, y cruzando el salto de
   página cuando el sutta sigue en la siguiente. **No uses `mk.py`**: su
   recorte compuesto cose dos tramos y pierde las líneas de en medio (véase
   `CLAUDE.md`, «Las herramientas de recortes»). Donde `lines.py` no aísla
   bien los renglones (p. ej. PDF 148 y 150), recorta por píxeles.

   **El modo por píxeles exige la «y» en los dos extremos**
   (`crop.py 152 y1620 y2140 salida.jpg`). Sin ella, `crop.py` toma los
   números como índices de línea y falla con IndexError (sesión 5). Díselo
   también a los subagentes al pasarles la orden de ampliar.

   Los recortes van a `~/Tipitaka/…/_crops/nama/` — **fuera del repositorio**.
   Si el recorte corta una frase, amplía con `crop.py` en vez de adivinar.
2. **Lee el recorte** con el subagente `lector-sutta`, uno por sutta. Pásale el
   §, el nº del libro, la página del PDF y las rutas de los recortes; te
   devuelve la fila.
3. **Verifica** tres celdas —la clase de sutta, las funciones y el **ejemplo
   (က)**, este último con su forma y su segmentación— con el subagente
   `verificador`, que lee **recortes frescos sin ver el borrador**. Una celda
   es **[V]** solo si las dos lecturas coinciden. Si no coinciden, la celda no
   es [V]: se anota la discrepancia con las dos lecturas y se le lleva al IEBH.
4. **Como mucho 3 subagentes a la vez.** Lanza los de un grupo en un solo
   mensaje y espera a que terminen antes del siguiente.

## 2. La fila

Las columnas de la nota: `§ | PDF | Clase de sutta | Aṅga | Funciones |
Ejemplo (က) | Notas`. Y, sin excepción:

- **Marcas**: [V] visto en la imagen · [R] reconstruido del OCR · [I]
  completado por Claude · ? ilegible · — el libro no lo tiene. **Nada llega a
  la página sin [V].**
- **Celda vacía donde el libro no da nada.** No la rellenes por simetría con
  otro sutta. Que el libro calle es un dato.
- **El término de clase, el del libro**, con sus diacríticos. Si rotula con una
  frase birmana, cópiala y tradúcela al lado. antaraṅga / bāhiraṅga /
  ubhayaṅga van aquí cuando el libro los da como rótulo, sin nota de
  diferencia con `datos.json`.
- **Nunca presentes tu análisis como palabra del libro.** Cuando el libro pide
  analizar (ခွဲ / ခွဲလေ), la fila dice **ejercicio** y la propuesta va rotulada
  «Respuesta sugerida (IEBH)».
- La etiqueta de inflexión del nimitta (7.ª, 5.ª…) es añadido editorial del
  IEBH: mantenla como tal.
- Las lecturas de abreviaturas de caso («စ၊ ဆ», «ပ၊ ဒု», «သ၊ တ၊ မိ») van
  marcadas [I] dentro de la nota.

## 3. Guardar

**Cada 5 suttas**, escribe las filas en `docs/visuddhayum/nama-piloto.md`
—en la tabla de la tanda que corresponda— y actualiza la línea de estado del
encabezado (último § cotejado, siguiente §). No esperes al final: lo que no
quede escrito se pierde.

## 4. Informe final (al IEBH, en inglés)

1. **Filas**: cuántos suttas, de § a §, y cuántas celdas quedaron [V].
2. **Correcciones**: lo que esta tanda corrige de la nota o de lo ya escrito
   (números de encabezado, páginas, suttas que sí tienen (ခ) aunque `mk.py`
   dijera que no…).
3. **Celdas vacías, y por qué**: distinguiendo «el libro no lo da» de «no se
   pudo leer» y de «hay discrepancia entre lector y verificador».
4. **Términos nuevos para el glosario**: los que no estén en
   `comun/glosario.md` ni en `recursos/terminos/terminos.json`, con la cita del
   sutta donde salen. Propuestos, no añadidos.
5. **Preguntas** para el IEBH: abreviaturas sin resolver, rótulos dudosos,
   decisiones de formato.

## 5. Mientras el capítulo esté a medias, no se prepara publicación

**No escribas `herramientas/.publicar/archivos.txt` ni
`herramientas/.publicar/mensaje.txt`.** Una tanda no es un capítulo: lo único
que se toca es `docs/visuddhayum/nama-piloto.md`. Los archivos de publicación
se preparan **solo cuando el IEBH pide publicar un capítulo entero**, y entonces
los escribe él o se escriben a petición suya; publicar lo hace él.
