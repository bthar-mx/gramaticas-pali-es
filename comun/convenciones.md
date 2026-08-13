# Convenciones de traducción

Documento normativo. Toda decisión que se repita va aquí.

## 1. Términos pāḷi

- Términos técnicos sin traducir. Unicode NFC, diacríticos completos.
- Equivalencia española entre paréntesis la primera vez:
  *kāraka* (relación sintáctica).

## 2. Numeración de suttas

- Edición base: Kaccāyana-vyākaraṇa, ed. y trad. Bhikkhu U Nandisena (ITBMU).
  La numeración de suttas de este repositorio sigue esta edición.
  <!-- PENDIENTE: precisar año / versión exacta que se está usando -->
- **Numeración triple**, tal como la presenta Nandisena:
  `**[Núm. Kaccāyana]. [Núm. Rūpasiddhi]. Texto del sutta ([Núm. Saddanīti-Suttamālā]).**`
  Ejemplo: `**30. 58. Aṃ byañjane niggahitaṃ (153).**`
- El **primer número** (Kaccāyana, secuencial) es el normativo. Se cita `§30`
  y fija el ancla del sutta: `id="s30"`, es decir la URL pública
  `…/kaccayana/sandhi/#s30`. **Las anclas no se cambian una vez publicadas.**
- El segundo número (Rūpasiddhi) y el número entre paréntesis
  (Saddanīti-Suttamālā, ausente en algunos suttas) son concordancias, no anclas.
- No renumerar.
- `comun/concordancia.json` registra los tres números de cada sutta, para quien
  llegue desde otra edición. Se actualiza al cerrar cada capítulo.

## 3. Estructura de los archivos

- Un archivo por kappa (capítulo), no uno por kaṇḍa ni por sutta:
  `kaccayana/01-sandhi-kappa.md` contiene las cinco kaṇḍas del capítulo.
  <!-- Corregido: la regla anterior decía "un archivo por kaṇḍa"; el texto ya
       traducido está organizado por kappa. -->
- Orden dentro de cada sutta: texto pāḷi, traducción, vutti, nota.

## 3 bis. Sitio publicado

- `site/` es lo único que se publica; ver `wrangler.jsonc` en la raíz.
- El HTML de `site/` es **salida generada**; la fuente es el markdown de
  `kaccayana/`. No editar el HTML a mano: se pierde al regenerar.
- Dominio: `gramaticas.buddha-dhamma.net`. Un solo sitio, obras y capítulos
  en rutas: `/kaccayana/sandhi/`, `/kaccayana/nama/`, `/recursos/`.

## 3 ter. Generación del HTML

    python3 herramientas/generar_capitulo.py kaccayana/01-sandhi-kappa.md

Los metadatos de cada capítulo (slug, título pāḷi y español, capítulo
anterior y siguiente) están en el diccionario `CAPITULOS` al principio del
script. Añadir una entrada antes de generar un capítulo nuevo.

Lo que el generador deduce solo del markdown:

- tarjeta y ancla de cada sutta (`#sN`), con la numeración triple
- desglose y número de voces
- bloque pāḷi, glosa y vutti
- secuencias de formación, ejemplos, contraejemplos y preguntas
- notas al pie: superíndice con nota emergente y bloque «Ver notas»
- referencias cruzadas §N → enlace al sutta
- secciones de kaṇḍa y su fórmula de cierre, tomada literal del markdown
- versos introductorios, tabla de contenidos y pastillas de navegación

### Referencias a otras obras

`Rū. §49`, `Sad. §139`, `Bā. §41` remiten a Rūpasiddhi, Saddanīti y
Bālāvatāra, **no** a suttas de este capítulo. El generador no las enlaza y
las lista al terminar, para poder revisarlas. Un §N que apunte a un sutta
inexistente en el capítulo tampoco se enlaza y aparece en ese aviso.

### La flecha de derivación

Entre dos formas se escribe **→**, nunca `>`:

    sugado → sugato
    dukkataṃ → dukkaṭaṃ

La flecha va siempre de la forma subyacente a la atestiguada, en el sentido
en que ocurre la operación.

Dos motivos para no usar `>`: en markdown, un `>` al principio de línea abre
una cita, y además el `>` de Thitzana lleva la dirección contraria. Él
imprime «Sugato> Sugado» —primero la forma atestiguada— aunque su propia nota
diga que el signo significa «se convierte en». Al incorporar material suyo hay
que invertir el orden, y sólo se deja su `>` tal cual cuando se le cita
literalmente.

### Glosas emergentes

Para glosar una palabra pāḷi dentro del texto:

    {akkharakosallaṃ|habilidad con las letras}

Se escriben en el cuerpo del sutta, nunca en la línea de cabecera: el título
pāḷi se reutiliza en el índice lateral y en las pastillas, donde no cabe una
glosa emergente.

## 4. Citas del canon

- Enlazar a https://buddha-dhamma.net en lugar de reproducir el pasaje.

## 5. Marcas de trabajo

- `<!-- DUDA: ... -->`      cuestión sin resolver
- `<!-- REVISAR: ... -->`   traducción provisional
