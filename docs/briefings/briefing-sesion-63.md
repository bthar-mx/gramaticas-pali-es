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

## 4. LAS FUGAS DE ESPAÑOL, CERRADAS

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

### 4 bis. `/recursos/raices/`: EL BOTÓN «EN» ERA OTRA COSA

**Su botón «EN» nunca fue un conmutador de idioma.** Lo único que hacía era
**añadir** la glosa inglesa bajo la española (clase `con-en`); el título, el
`h1`, la entradilla, la barra lateral, las pestañas, los filtros, las etiquetas
de fila y el contador se quedaban en español. Era la página que Angel estaba
mirando cuando lo dijo.

**Hecha en esta sesión, y con la decisión de IEBH (2026-09-07): en modo inglés
la glosa española se esconde.** Los dos glosarios se turnan en vez de sumarse,
que es lo que significa un conmutador de lengua y lo que ya hacían paradigmas y
el solucionador. Con ello la glosa inglesa deja de ir en cursiva y más pequeña
—era la secundaria— y se compone como la española: en su modo, cada una es la
principal.

Lo traducido: las **51 cadenas de JavaScript** al diccionario `TXT` con su
`tr()` —globos de gaṇa y de referencia, marcas DP y DM, «sin separar»,
«reparto deducido», las cuatro cajas de búsqueda, las tablas de plural, el
contador— y los **nueve párrafos del pie** en bloques `.i-es`/`.i-en`
(«Fuente», «Cómo leer las referencias», «El Dhātupāṭha», «La Dhātumañjūsā»,
«Los significados del Dhātupāṭha», «Cómo buscar», «Véase también»,
«Créditos» y el de la edición), más la licencia con la fórmula de
`COPYRIGHT_EN`.

**Lo que NO se traduce, y es el criterio de siempre:** las formas pāḷi y
sánscritas, que son el objeto de la página; las glosas pāḷi
(*kuṭilagatiyaṃ*, *gatyatthe*); las referencias (I 12, X 371), que son la
cita; y el español de U Sīlānanda y el inglés de la digitalización, que son
las FUENTES y se enseñan como están.

**Dos errores de oficio que salieron al hacerlo**, y quedan arreglados:

- `botones()` **añadía un oyente en cada llamada**. Como ahora la fila de
  filtros se redibuja al cambiar de lengua, habrían quedado dos escuchando y
  `render()` habría corrido por duplicado. Se pone una sola vez.
- `botones()` **no conservaba el filtro puesto**: al conmutar la lengua los
  filtros volvían a «todas» sin que nadie los tocara. Ahora recibe el valor en
  curso. Comprobado: con «Con sánsc.» puesto, cambiar de lengua pasa de «1517
  de 1698 raíces» a «1517 of 1698 roots» y el botón sigue marcado.

**El inglés nuevo de esta página es PROPUESTA**, y lo adjudica IEBH como el de
`ingles.json`.

### 4 ter. UNA ENTRADA NUEVA BAJO UNA FIRMA QUE NO LA HA VISTO

El pie de `/recursos/verbo/` decía «Notas, cifras y fuentes» también en
inglés. Arreglarlo pedía una cadena nueva, `pie_sum`, en
`recursos/verbo/ingles.json` — y **ese archivo está adjudicado por IEBH**
(`"adjudicado": true`). De modo que, como manda `CLAUDE.md`, se dice: la
cadena **«Notes, numbers and sources»** entra bajo una firma que no la ha
visto. Decide IEBH si vale o si espera adjudicación aparte.

### 4 ter bis. LAS VERSIONES, QUE SE HABÍAN OLVIDADO

Lo vio Angel: la página de raíces cambiaba entera y seguía diciendo v1.5. Y no
era sólo ella — **ninguna de las páginas tocadas se había subido de versión**.
Corregido:

| Página | Versión | Dónde vive el número |
| --- | --- | --- |
| raíces | 1.5 → **1.6** | `<meta>` de la plantilla |
| glosario | 1.1 → **1.2** | `recursos/glosario/conspectus.json`, **no** el `<meta>` |
| solucionador | 2.1 → **2.2** | `VERSION` en `generar_solucionador.py` |
| verbo | 1.4 → **1.5** | `VERSION` en `generar_verbo.py` |
| paradigmas | **1.18**, ya puesta | `const VERSION` dentro de la plantilla |

**Cuidado con el glosario**: su `<meta name="version">` NO es lo que se
publica —lo que manda es `conspectus.json`—, de modo que cambiar el `<meta>` no
hace nada. Se cambian los dos para que no se contradigan.

Y las insignias iban en español pasara lo que pasara. Ahora se repintan con la
lengua:

- **raíces** tenía `toLocaleDateString('es')` fijo, que habría dado el mes en
  español en la página inglesa; se compone a mano con la tabla de meses, como
  en paradigmas. Y estrena `VERSION_NOTE_EN`.
- **glosario** decía «Versión» y el estado «completo» en inglés; ahora
  «Version» y «complete», y «en curso — N de M páginas» → «in progress — N of
  M pages».

**Una trampa de JavaScript, por si se repite:** `aplicarIdioma()` corre al
arrancar ANTES de que se declaren `VERSION` y `VERSION_DATE`, que son `const`,
y tocarlas en su zona muerta lanza — `typeof` tampoco salva de ella. Hace falta
un testigo declarado con `var`, que sí se iza inicializado: `versionLista`.

### 4 ter ter. LA PÁGINA EN BLANCO, Y POR QUÉ NO LA CAZÓ LA PRUEBA

Lo vio Angel: pulsar «EN» en raíces dejaba la **página entera en blanco**.

**La causa, y es un choque de nombres.** La clase de la lengua en el `<body>`
es `en` — la misma que la de la glosa inglesa. De modo que un

    .en{display:none}

suelto no le daba sólo a las glosas: le daba también al propio
`<body class="en">`, y la página desaparecía. `body.en .en{display:block}` no
lo salvaba, porque sólo alcanza a los descendientes, no al elemento que lleva
la clase.

**El arreglo:** las dos glosas se seleccionan siempre dentro de `#out`, que es
donde las pinta el guion, y nunca por la clase a secas. De paso se quitó el
`.en{display:block}` de `@media print`, que forzaba la glosa inglesa en papel
—tenía sentido cuando el botón sólo la AÑADÍA— y que le pegaba al `<body>`
por lo mismo.

**Cuidado si se repite:** en glosario, paradigmas y el solucionador no pasa
porque allí la prosa va en `.i-es`/`.i-en`, que no chocan con la clase del
`body`. Raíces era la única que usaba `.es`/`.en` a secas.

#### Y la prueba estaba mintiendo

Peor que el error: **el arnés de jsdom no lo cazó, y no podía**. Miraba
`textContent`, que no sabe nada de CSS; una página con `display:none` tiene
todo su texto igual. Ahora mira `getComputedStyle(body).display` y la
cantidad de texto, que es lo que distingue una página de una página en blanco.

Y había un segundo fallo, más tonto y más peligroso: el arnés inyectaba su
guion sustituyendo **el primer `<body>` del archivo** — que desde este mismo
commit aparece antes dentro de un comentario del CSS. De modo que
`pali_lang` no se ponía nunca, jsdom dice `en-US`, y **todo lo que creía estar
midiendo en español lo medía en inglés**. Ahora inyecta tras `</head>\n<body>`.

Con las dos correcciones, la prueba encontró **tres fugas más** que la versión
floja daba por limpias: la licencia del glosario, la licencia del verbo y la
nota de versión del solucionador. Las tres, arregladas.

**La lección, que es la del §2 otra vez:** una prueba que pasa no dice que la
página esté bien; dice que la prueba pasa. Conviene preguntarse qué es lo que
NO está mirando.

### 4 quater. LAS COMPROBACIONES

Con jsdom sobre las páginas ya generadas, en los dos idiomas:

- las cinco páginas con conmutador —raíces, glosario, paradigmas,
  solucionador, verbo— **no dejan ni una cadena española a la vista** en modo
  inglés (título, `h1`, entradilla, enlace de vuelta, índice, pestañas,
  filtros, buscador, contador, `summary` del pie y licencia);
- el conmutador de raíces funciona **en caliente**, no sólo al cargar: cambia
  título, clase del `body`, contador, rótulos y filtros, guarda en
  `pali_lang`, y vuelve;
- las 1.698 glosas llevan las dos lenguas en el marcado y las esconde el CSS,
  de modo que no se pierde nada al conmutar;
- `paliLang()` está en **todas** las páginas menos `/recursos/sandhi/` y
  `/recursos/nombre/`, que no tienen conmutador;
- los ocho `window.PALI_CAPITULO` son JSON válido.

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
- `recursos/raices/plantilla.html` — la página entera: `paliLang()`, el
  diccionario `TXT` con `tr()`, el pie y la prosa en `.i-es`/`.i-en`, el
  conmutador de lengua y las dos correcciones de `botones()`
- `recursos/verbo/ingles.json` — cadena nueva `pie_sum`, **bajo firma que no
  la ha visto** (§4 ter)

Más `site/` entero, que lo regenera el hook.

**Ojo:** el commit de la `<meta description>` de la sesión 62 y el de esta
sesión van mezclados en `generar_indices.py`. Si se quieren separados, hay que
partirlo a mano.

---

## 6. POR DÓNDE SEGUIR

1. **Firmar o corregir §268** (§1), que es media hora y cierra seis
   derivaciones.
2. **Adjudicar el inglés nuevo**: la página de raíces entera (§4 bis) y la
   cadena `pie_sum` del verbo (§4 ter).
3. Los candidatos del capítulo 2 que quedan, por orden de señal, tal como los
   dejó el briefing 62 §4: «Puthabyā» (§72), «Itthi» (§85), «Kva»,
   «Daṇḍi», «Catassannaṃ», «Pulliṅgaṃ», «Bāhussaccaṃ».
4. `/recursos/sandhi/` y `/recursos/nombre/` no tienen conmutador ninguno.
   Angel los dejó fuera del encargo de esta sesión, y son las dos únicas
   páginas del sitio que siguen siendo sólo españolas.
5. Los 21 términos ingleses que IEBH pasó para `glosario-ingles.json` quedaron
   a medias: mapeados a sus claves exactas y con la adjudicación por tandas
   decidida, pero **sin escribir**, y con tres glosas por resolver
   —`pañcavassa`, `-gabbha`, `makuṭa`— más `pūḷī` y `hīna`, que no llegaron.
