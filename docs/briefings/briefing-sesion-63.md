# Briefing de la sesión 63 — LA LENGUA DEL LECTOR

**Fecha:** 2026-09-07. Sesión de sitio, con una propuesta de escalera al
principio. Tres cosas: las **seis derivaciones de §268** quedan propuestas y
verificadas (sin firmar); se caza un **error de sintaxis** que dejaba a las
cuatro páginas inglesas de capítulo sin su configuración de JavaScript; y el
sitio pasa a **abrirse en la lengua del sistema operativo del lector**.

Este briefing supone leído el 62. Lo pendiente de las sesiones 57-58 —tanda 2
del inglés, puntos 17-34 de la revisión del glosario— **sigue sin tocarse**.

---

## 0. LO PRIMERO, PORQUE ESTORBA

Al arrancar quedó un **`.git/index.lock` de cero bytes** —la misma trampa del
§7 del briefing 62— y el entorno de Claude no puede borrarlo:

    rm -f .git/index.lock

Y, **por un error de esta sesión**, hay un `node_modules/` en la raíz del
repositorio: Claude instaló `jsdom` ahí para probar las páginas, en vez de
hacerlo fuera. No está en `.gitignore`, y `ciclo_veredictos.py` hace
`git add -A`, de modo que **se colaría en el primer commit de la cola**. Antes
de nada:

    rm -rf node_modules package.json package-lock.json

Si se va a volver a probar con jsdom, se instala fuera del repositorio.

---

## 1. §268: SEIS DERIVACIONES, UN SOLO PASO QUE FALTA — PROPUESTA, SIN FIRMAR

Las seis de §268 —«guṇiyo», «guṇiṭṭho», «satiyo», «satiṭṭho», «medhiyo»,
«medhiṭṭho»— son un mismo patrón, y les falta **el mismo paso**: tras
sustituirse ‘si’ por ‘o’, la vocal final del tema no se elide, y la cadena
deja *guṇiyao*, *satiyao*, *medhiyao*.

**La evidencia está dentro del capítulo, y es el propio idiom de la edición.**
Las hermanas que hacen exactamente esto lo escriben así:

| Línea | Forma | Cadena |
| ---: | --- | --- |
| 1145 | Himavanto | `… ‘si’ se sustituye por ‘o’ (§104); ‘a’ se elide (§83)` |
| 1431 | Sabbo | `‘si’ se sustituye por ‘o’ (§104); ‘a’ se elide (§83)` |
| 3645 | Gacchanto | `‘si’ se sustituye por ‘o’ (§104); ‘a’ se elide (§83)` |
| 3647 | Mahanto | ídem |
| 3649 | Caranto | ídem |
| 3651 | Khādanto | ídem |

De modo que la propuesta es **añadir el mismo paso, con la misma redacción**,
al final de las seis cadenas:

    ; ‘a’ se elide (§83))

Queda, por ejemplo:

    **Guṇiyo** = guṇavantu + iya + si (“vantu” se elide (§268); ‘a’ se elide
    (§83); ‘si’ se sustituye por ‘o’ (§104); ‘a’ se elide (§83)).

**Verificado, no afirmado.** Aplicado sobre una copia del capítulo,
`auditar_derivaciones.py` deja de marcar las seis y **no rompe ninguna otra**:
los candidatos bajan de **63 a 57**, y la recomposición sube de 577 a **583 de
608**.

**No está escrito en la fuente.** La corrección va en `docs/2. Nāma-Kappa.md`,
líneas 5612-5617, y **la firma es de IEBH**. Dos cosas que decidir con ella:

- **La redacción.** Se propone `‘a’ se elide (§83)` a secas, que es como lo
  escriben *Sabbo* y *Gacchanto* —y «sabba» también tiene dos ‘a’, de modo que
  la edición no desambigua ni cuando podría—. La alternativa sería nombrar el
  alcance, `‘a’ de ‘iya’ se elide (§83)`, como hace *Maghavāno* (línea 2821)
  con `‘a’ de ‘āna’`. **Manda el hábito de la edición**, salvo que IEBH prefiera
  lo contrario.
- **Los dos §83 seguidos.** La cadena queda con §83 dos veces, una por cada
  elisión: la del tema ante el sufijo taddhita y la del final ante ‘o’. Es lo
  que ocurre, y §83 ampara las dos —*paccayādimhi* y *’mādesa*—, pero conviene
  que lo vea.

---

## 2. EL ERROR QUE NO SE VEÍA: UN APÓSTROFO

**Las cuatro páginas inglesas de capítulo tenían el JavaScript roto**, y
llevaban así desde que existe la edición inglesa.

`window.PALI_CAPITULO` se emitía con los valores entre comillas simples, y uno
de ellos es el subtítulo inglés de la obra: **`Kaccāyana's Grammar`**. El
apóstrofo cerraba la cadena, y la consola daba
`SyntaxError: Unexpected identifier 's'`. Consecuencia: el objeto **no llegaba
a existir**, y `pali.js` caía en sus cadenas españolas de reserva. Por eso el
contador de la edición inglesa decía «0 / 219 **estudiados**» —el síntoma
visible— y por eso se perdían además la clave de suttas estudiados, el nombre
del EPUB y el resto de la configuración.

**Arreglado en el origen, no en el síntoma:** el bloque se emite ahora con
`json.dumps`, de modo que ningún carácter de ningún valor puede volver a
romperlo. Comprobado con `JSON.parse` sobre las páginas generadas: las dos
ediciones cuadran, y el contador inglés dice ya «studied».

**La lección de oficio:** el español que se veía en la página inglesa no era
una cadena sin traducir. Era un error de sintaxis a tres capas de distancia.
Conviene mirar la consola antes de dar por sentado que falta una traducción.

---

## 3. LA LENGUA DE ARRANQUE LA PONE EL SISTEMA DEL LECTOR

**Pedido de Angel, 2026-09-07:** «que las páginas se vean en inglés cuando el
sistema operativo del visitante está en inglés, y en español cuando está en
español; y que los conmutadores sigan estando».

Una sola función, **la misma en todo el sitio**, puesta antes de que se pinte
nada:

    function paliLang(){var g=null;
    try{g=localStorage.getItem('pali_lang');}catch(e){}
    if(g==='en'||g==='es')return g;
    var n=(navigator.languages&&navigator.languages[0])||navigator.language||'';
    return /^en\b/i.test(n)?'en':'es';}

El orden de prelación, que es lo que hay que entender:

1. **Si el lector ya eligió**, manda su elección. Pulsar ES|EN la guarda, y a
   partir de ahí el sistema operativo deja de contar. Los conmutadores siguen
   todos donde estaban.
2. **Si no ha elegido**, manda la lengua del navegador, que es la del sistema.
3. **El español es el que queda por defecto**, y a él van a parar las lenguas
   que no son el inglés —el francés, el birmano—. Es la lengua del proyecto.
   Si IEBH prefiere que un lector francófono vea el inglés, es cambiar el
   regreso de la función y nada más.

Se lee del navegador y no del sistema directamente porque **una página web no
ve el sistema operativo**: `navigator.language` es lo más cerca que se puede
estar, y en la práctica es la lengua que el lector tiene puesta en su equipo.

**Probado con 12 casos** —`en-US`, `en`, `en-GB,fr`, `es-ES`, `es`, `fr-FR`,
`my-MM`, la lista vacía, elección guardada que contradice al sistema en los dos
sentidos, basura guardada, y `localStorage` que **lanza** (navegación privada,
cookies bloqueadas)— sobre la función tal como queda publicada, en tres
páginas de clases distintas. Pasan las doce.

En las páginas de capítulo, que son **dos URL distintas**, `paliLang()` decide
además a cuál de las dos se lleva al lector. No hay bucle: la función es
determinista.

### De paso, la elección ya viaja por el sitio

Estaba roto y no se había notado. El comentario de `generar_indices.py` decía
que «pali_lang» era «la misma clave que usan las páginas de recurso», y **no
era verdad**: cada página guardaba en la suya —`pali_paradigmas_en`,
`pali_raices_en`, `pali_solucionador_en`—, el glosario no guardaba nada, y sólo
el verbo usaba `pali_lang`. Elegir inglés en una página no se notaba en la
siguiente.

**Ahora todas guardan en `pali_lang`.** Efecto secundario, y es una sola vez:
a quien tuviera el inglés puesto en paradigmas, raíces o el solucionador se le
olvida esa preferencia la primera vez que entre.

---

## 4. LAS FUGAS DE ESPAÑOL, CERRADAS — MENOS UNA

Auditado el sitio entero en modo inglés, página por página. Estaban limpias la
portada, `/kaccayana/`, `/recursos/` y `/recursos/verbo/`. Lo demás:

| Página | Qué se ha hecho |
| --- | --- |
| capítulos `/en/` | El contador decía «estudiados» — era el §2, no una traducción que faltara |
| `/recursos/glosario/` | Título del navegador, `h1`, rótulo del índice y la nota del alfabeto, en inglés; y la página nace ya en la lengua puesta, que antes no |
| `/recursos/paradigmas/` | Título del navegador y `h1` |
| `/recursos/solucionador/` | El pie entero, con **la fórmula inglesa de licencia que ya usan las páginas de capítulo** (`COPYRIGHT_EN`), no una redactada de nuevo |
| todas | El enlace de vuelta «← Recursos · Gramáticas Pāḷi» → «← Resources · Pāḷi Grammars» |

Comprobado con jsdom sobre las páginas generadas, en los dos idiomas: título,
`lang` del documento, `h1`, enlace de vuelta, rótulo del índice y nota del
alfabeto dicen lo que deben en cada lengua.

**El conmutador ES|EN no es una fuga.** Su globo habla siempre la lengua de
DESTINO —«View in English» en la página española, «Ver este capítulo en
español» en la inglesa—, y es a propósito: es el criterio de la sesión 60 y el
de Wikipedia. Se deja como está.

### 4 bis. LO QUE FALTA: `/recursos/raices/` ENTERA

**Su botón «EN» nunca fue un conmutador de idioma.** Lo único que hace es
**añadir** la glosa inglesa junto a la española (clase `con-en`); el título, el
`h1`, la entradilla, la barra lateral, las pestañas, los filtros, las etiquetas
de fila y el contador **siguen en español**. Es la página que Angel estaba
mirando cuando lo dijo.

**No se ha tocado**, y a propósito: es una página de otro tamaño. Medido, lo
que pide son **51 cadenas distintas en JavaScript** —globos de cada gaṇa, de
cada referencia, las marcas DP y DM, «sin separar», «reparto deducido», las
tablas de plural `['raíz','raíces','ninguna raíz']`, los cuatro buscadores— más
**nueve párrafos de prosa del pie** («Fuente», «Cómo leer las referencias», «El
Dhātupāṭha», «La Dhātumañjūsā», «Los significados del Dhātupāṭha», «Cómo
buscar», «Véase también», «Créditos» y el de la edición). Hacerlo a medias en
una página cuyo valor es la precisión sería peor que no hacerlo.

Lo que sí queda puesto es **el cableado**: `paliLang()` ya está en su plantilla,
lista para cuando se le ponga el diccionario `TXT` y los bloques `.i-es`/`.i-en`,
con el patrón que ya usan paradigmas y el solucionador.

**Y hay una decisión de diseño que tomar antes de escribir nada**, porque hoy
el botón hace otra cosa: cuando «EN» pase a ser lengua, ¿el modo inglés
**esconde** la glosa española —que es lo que significa un conmutador de
lengua, y lo que hacen las demás páginas— o se conserva la vista de las dos a
la vez, que hoy existe y es útil para cotejar? Si se quiere conservar,
hacen falta tres estados y no dos.

**Recordatorio de siempre:** el inglés nuevo que salga de ahí es **propuesta**,
y lo adjudica IEBH, como el de `ingles.json`.

---

## 5. QUÉ ESTÁ TOCADO Y SIN COMMIT

Nada se ha commiteado: **Claude no lanza `git` en este repositorio** (§7 del
briefing 62), y esta vez ya dejó el candado.

Fuentes tocadas:

- `herramientas/generar_capitulo.py` — `paliLang()` en la cabecera, la
  redirección por lengua, y `PALI_CAPITULO` por `json.dumps`
- `herramientas/generar_indices.py` — `paliLang()`, y la `<meta description>`
  inglesa que **venía sin commit de la sesión 62**
- `recursos/glosario/plantilla.html` — `paliLang()`, `pali_lang`, títulos,
  `h1`, `TITULOS`, `NOTA_ABC` y `ROT_BARRA` bilingües, y `ponIdioma(idioma)`
  al arrancar
- `recursos/paradigmas/plantilla.html` — `paliLang()`, `pali_lang`, clave
  `titulo` en `TXT`, `h1` y enlace de vuelta bilingües
- `recursos/solucionador/plantilla.html` — `paliLang()`, `pali_lang`, pie y
  enlace de vuelta bilingües
- `recursos/verbo/plantilla.html` — `paliLang()`
- `recursos/raices/plantilla.html` — sólo `paliLang()`, sin usar todavía

Más `site/` entero, que lo regenera el hook.

**Ojo:** el commit de la `<meta description>` de la sesión 62 y el de esta
sesión van mezclados en `generar_indices.py`. Si se quieren separados, hay que
partirlo a mano.

---

## 6. POR DÓNDE SEGUIR

1. **Firmar o corregir §268** (§1), que es media hora y cierra seis
   derivaciones.
2. **Decidir los tres estados de raíces** (§4 bis) y traducirla.
3. Los candidatos del capítulo 2 que quedan, por orden de señal, tal como los
   dejó el briefing 62 §4: «Puthabyā» (§72), «Itthi» (§85), «Kva»,
   «Daṇḍi», «Catassannaṃ», «Pulliṅgaṃ», «Bāhussaccaṃ».
4. `/recursos/sandhi/` y `/recursos/nombre/` no tienen conmutador ninguno.
   Angel los dejó fuera del encargo de esta sesión.
