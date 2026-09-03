# Convenciones de traducción

Documento normativo. Toda decisión que se repita va aquí.

## 0. Registro del español del proyecto

Vale para **todo** lo que se escribe en español —capítulos, recursos,
briefings, mensajes de commit, comentarios del código—, no sólo para la
traducción.

**No se calcan verbos ingleses.** «Commitear», «pushear», «mergear»,
«deployar», «linkear», «testear», «parchear» y compañía no son español, y
«empujado» por *pushed* es una traducción literal que en español no significa
eso. El sustantivo técnico se deja como es —«el commit», «el hook», «el
push»—; lo que no se hace es conjugarlo.

| En vez de | Se escribe |
| --------- | ---------- |
| commitear, commiteado | confirmar; hacer el commit; «sin confirmar» |
| empujado, pushear | publicado; subido a `origin` |
| mergear | fusionar; integrar |
| deployar | desplegar |
| parchear | corregir; aplicar un parche |
| testear | probar; comprobar |

**Por qué está escrito aquí y no sólo dicho.** Angel lo había advertido en
sesiones anteriores y volvió a salir en la 24. La causa es mecánica: un chat
nuevo no recuerda ninguna conversación, sólo lee el repositorio, y este
documento no lo recogía. Lo que sí leía eran los briefings 10 a 22, donde
«commitear» y «empujado» aparecen veintiuna veces **usados como si fueran la
casa**. De modo que cada sesión no es que olvidara la regla: aprendía el error
del propio registro. Escrito aquí, deja de depender de que alguien lo recuerde.

## 1. Términos pāḷi

- Términos técnicos sin traducir. Unicode NFC, diacríticos completos.
- Equivalencia española entre paréntesis la primera vez:
  *kāraka* (relación sintáctica).

## 1 bis. Locativo y ablativo en la glosa del sutta (sesión 45)

En la glosa de un sutta, **el locativo pāḷi significa «sigue»** (*sare* =
«cuando una vocal sigue») **y el ablativo, «después»** (*saramhā* = «después
de una vocal»). Son el sentido del caso, no un añadido del traductor, y por
eso **van sin corchetes**: «Las vocales se eliden cuando una vocal sigue»,
no «cuando una vocal [sigue]». Los corchetes se reservan para lo que el
sutta no dice —el sustantivo suplido, el verbo suplido—. Decisión de Angel,
2026-09-03; vale para el español y para la edición inglesa («when a vowel
follows», «after a vowel»).

## 2. Numeración de suttas

- Edición base: Kaccāyana-byākaraṇa, ed. y trad. Bhikkhu U Nandisena (ITBMU).
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
