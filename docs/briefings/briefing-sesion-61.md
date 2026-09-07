# Briefing de la sesión 61 — «ĀDI», Y LA TRAMPA DEL CONVERSOR

**Fecha:** 2026-09-07. Sesión corta de correcciones que destapó dos cosas de
distinto tamaño: unas erratas de derivación en el capítulo 2 —de las que la de
«ādiṃ» es el ejemplar— y, sobre todo, **que el maestro español del capítulo 2
no es `kaccayana/02-nama-kappa.md`**, de modo que dos commits salieron sin los
cambios que creíamos hechos. Publicado: capítulo 2 en **v1.3** (es) y **v1.1**
(en), paradigmas en **v1.18**.

Este briefing supone leído el 60 (publicación del capítulo 4). Lo pendiente de
las sesiones 57-58 —tanda 2 del inglés, puntos 17-34 de la revisión del
glosario— no se ha tocado.

---

## 1. LO PRIMERO QUE HAY QUE SABER: TRES CAPÍTULOS NO SE EDITAN EN `kaccayana/`

Está ya en `CLAUDE.md` («Cómo se publica»), y se repite aquí porque costó dos
commits perdidos y una hora:

**Los capítulos 2, 3 y 4 en español son salida, no fuente.** Los rehace
`herramientas/convertir_<obra>.py` desde su maestro de `docs/`, y el hook de
pre-commit ejecuta **todos** los `convertir_*.py` antes de generar el sitio.

| Capítulo | Se edita aquí | Lo genera |
| --- | --- | --- |
| 2 · Nāma | `docs/2. Nāma-Kappa.md` | `convertir_nama.py` |
| 3 · Kāraka | `docs/3. Kāraka-Kappa.md` | `convertir_karaka.py` |
| 4 · Samāsa | `docs/4. Samāsa-Kappa.md` | `convertir_samasa.py` |

El capítulo 1 no tiene conversor, y los maestros ingleses `.en.md` tampoco:
ésos sí se editan en `kaccayana/`.

**Por qué engaña.** Un cambio hecho en el archivo de `kaccayana/` se guarda
bien, sobrevive a `generar_capitulo.py` y se ve en el HTML regenerado. Lo
revierte el hook **en el momento del commit**, cuando ya nadie está mirando: el
commit sale sin el cambio, sin error y sin aviso. Así se perdieron dos veces
las correcciones de §70 y §72; el inglés, que no tiene conversor, sí entró, de
modo que el repositorio quedó un rato con las dos ediciones diciendo cosas
distintas.

**Consecuencia para las notas al pie:** en los tres capítulos convertidos no se
numeran a mano. En el maestro se escribe `… texto. Nota: …` en la misma línea
(o un párrafo propio que empiece por `Nota:`, `Nota al pie:` o `Nota del
traductor…:`) y el conversor pone el ancla `[^n]` y renumera todas en orden de
aparición. La definición conserva el rótulo (`[^11]:  Nota: …`); el inglés, que
sí se numera a mano, lleva `Note: …` para que las dos ediciones digan lo mismo.

---

## 2. «ĀDI»: NO LE FALTA PARADIGMA, LE FALTABA LA NOTA

Pregunta del IEBH: la página de paradigmas no tiene ficha de «ādi». Cotejadas
las dos fuentes de segunda capa que hay en `docs/fuentes/`:

- **Niruttidīpanī** (ikārantapulliṅgarāsi, ed. VRI): enumera «ādi» y «upādi»
  entre los masculinos en ‘i’ que siguen a *aggi / muni*, y añade una entrada
  propia —«Ādisadde –»— con la única particularidad del vocablo: séptima
  `ādismiṃ, ādimhi, ādo` (por *Ratthyādīhi ṭo smiṃno*), más `gāthādo, pādādo`;
  y advierte que `ādiṃ, gāthādiṃ, pādādiṃ` son **acusativo en sentido de
  locativo** (*ādhāratthe dutiyā*), como *imaṃ rattiṃ*. En su §95, sobre los
  femeninos en ‘i’, aclara además **ādisaddo pana pulliṅgoyeva**: el vocablo es
  sólo masculino, y figura allí únicamente porque comparte la regla de ‘ṭo’ con
  *ratti*.
- **Saddanīti Padamālā** (VRI, `docs/fuentes/saddaniti/`): **no le da
  padamālā**. Su lista en verso de masculinos en ‘i’ (tipo *dhanabhūti /
  aggi*, [p. 106]) termina en «…samādhi jaladhi**ccādī**, dhanabhūtisamā matā»,
  de modo que «ādi» cae bajo el «etcétera». Aviso: sólo tenemos la Padamālā;
  la Suttamālā (donde están Sad. 218-219) no está en el repositorio.

**Resultado:** ficha M-I1 (*aggi*) con una `notas` nueva que dice que «ādi» no
tiene paradigma propio, se declina como *aggi*, y su particularidad es la
séptima —`ādiṃ, ādo` por Kacc. §69, junto a `ādismiṃ, ādimhi`—. Va rotulada
«Nota de esta edición, no del documento del IEBH». Su contraparte inglesa se
añadió a `ingles.json`, **que está firmado desde el 2026-08-29**: la nota entra
bajo una firma que no la ha visto, y así se le dijo al IEBH (queda anotado en
`CLAUDE.md`, «Estado de recursos/paradigmas»).

---

## 3. CAPÍTULO 2: CUATRO DERIVACIONES CORREGIDAS Y UNA ERRATA DE LECTURA

Todo en `docs/2. Nāma-Kappa.md` y en el maestro inglés.

**§69 «Ādito o ca».** La derivación decía `ādi + smiṃ (‘smiṃ’ → ‘aṃ’ (§69);
‘i’ de “ādi” se elide (§83))`, que da **ādaṃ**, no *ādiṃ*. §83 elide la vocal
del TEMA (*purisa + aṃ → purisaṃ*); los temas en ‘i’, ‘ī’, ‘u’, ‘ū’ —‘jha’,
‘la’, ‘pa’— van por **§82 «Aṃ-mo niggahitaṃ jha-la-pehi»**, que convierte ‘aṃ’
en ‘ṃ’ sin elidir nada. El propio §82 trae *ādiṃ*, *aggiṃ*, *isiṃ*, *rattiṃ*,
*itthiṃ* entre sus ejemplos. Reparto limpio: temas en ‘a’ por §83, temas
jha/la/pa por §82.

| Forma | Antes | Ahora |
| --- | --- | --- |
| **Ādiṃ** (§69) | ‘i’ se elide (§83) | nombre ‘jha’ (§58); ‘aṃ’ → ‘ṃ’ (§82) |
| **Ratto** (§69) | ‘i’ de “ratti” se elide *(sin sutta)* | ‘i’ se elide (**§83**), como *divā* |
| **Bārāṇasiṃ** (§69) | ‘a’ de ‘aṃ’ se elide *(sin sutta)* | ‘ī’ se acorta (§84); ‘aṃ’ → ‘ṃ’ (§82) |
| **Itthiṃ** (§223) | ‘ī’ se acorta (§84); ‘a’ de ‘aṃ’ se elide (§13) | igual que la de §84: §84 + §82 |

La de §223 explicaba la misma forma de dos maneras distintas en dos sitios; ya
son idénticas.

**§72 «Pasaññassa ca».** El español glosaba «la vocal \[‘a’\] que es la
sustitución de la inflexión \[‘smā’\]». Lo que sustituye a ‘smā’ es **‘ā’**
(§68), como dicen las derivaciones de *matyā* y *puthabyā*. El inglés ya decía
‘ā’, de modo que las dos ediciones divergían sin que constara en el registro de
desviaciones. Corregido el español.

Queda dicho, y **sin resolver**, que los corchetes estrechan el vutti: éste
dice sólo *vibhattādese sare pare* —cualquier vocal que sea sustitución de una
inflexión—, y §68 enseña *matyaṃ* = mati + smiṃ → ‘aṃ’ con §72. Si algún día se
quiere, la salida es quitar los dos corchetes y pasar el detalle a nota.

**§70 «Jha-lānam iy’-uvā sare vā».** La correspondencia que iba suelta al final
del párrafo —«i ī — iya u ū — uva»— pasa a nota al pie, con flecha: `Nota: i ī
→ iya; u ū → uva`. Es la nota 11 en las dos ediciones.

---

## 4. VERSIONES PUBLICADAS

| Página | Versión | Dónde se toca |
| --- | --- | --- |
| Nāma-kappa (es) | 1.2 → **1.3** (2026-09-07) | `CAPITULOS` en `generar_capitulo.py` |
| Nāma-kappa (en) | 1.0 → **1.1** (2026-09-07) | ídem, campos `*_en` |
| Paradigmas | 1.17 → **1.18** (2026-09-07) | `VERSION`/`VERSION_NOTE(_EN)` en `recursos/paradigmas/plantilla.html` |

La nota de versión de paradigmas encadena la anterior con «Antes, en la versión
1.17: …»; la de los capítulos se sustituye entera, que es como está diseñado.
La nota inglesa del capítulo no menciona §72 porque el inglés no tenía esa
errata.

`CLAUDE.md` decía además que paradigmas iba por v1.14 y que `ingles.json`
estaba «SIN adjudicar»: las dos cosas eran falsas desde hacía semanas y quedan
corregidas.

---

## 5. LO QUE VIENE: UN AUDITOR DE DERIVACIONES PARA EL CAPÍTULO 2

Encargo del IEBH: revisar el capítulo 2 entero buscando erratas de la clase de
«ādiṃ». **No se hace leyendo 219 suttas y afirmando**; se hace con un guion,
que es la regla de siempre —proponer y verificar—. Sería el equivalente nominal
de `auditar_secuencias.py`.

**El terreno, medido.** En `kaccayana/02-nama-kappa.md`: **594 derivaciones**
con **1.304 pasos** y unas 1.300 citas §N. De ahí salen ya tres señales:

- **9 pasos no citan ningún sutta** (la clase de *Bārāṇasiṃ*).
- **74 formas se derivan en más de un sitio con cadenas distintas** (la clase
  de *itthiṃ*). No todas serán erratas —dos suttas pueden ilustrar aspectos
  distintos de la misma forma—, pero cada una hay que mirarla.
- **Ninguna cita cae fuera de §1-§675**: no hay referencias rotas.

**Las cuatro comprobaciones**, de menor a mayor coste:

1. Pasos sin §N. Puro patrón.
2. Misma forma, cadenas divergentes. Puro patrón; el juicio es después.
3. **Clase de operación contra el sutta citado**: ¿el vutti de §N hace de veras
   esa clase de cosa —*lopa*, *ādesa*, *rassa*, *dīgha*, niggahita, *saññā*—?
   Es lo que `auditar_secuencias.py` hace para sandhi. Caza «se elide (§82)» y
   «se convierte en ‘ṃ’ (§83)».
4. **Aplicar la cadena y comparar con el lema.** La que caza *ādaṃ* sola, sin
   juicio ninguno. Implementable para los tipos de paso frecuentes —elisión de
   la vocal final, ‘aṃ’ → ‘ṃ’, acortamiento y alargamiento, «X se sustituye por
   Y», y los pasos de nombre, que no cambian nada—. **Donde un tipo de paso no
   esté implementado, el guion lo dice**; no lo deja pasar en silencio.

**Dos límites que hay que declarar en el propio guion**, como los declara el de
sandhi: no decide cuál de varios suttas correctos es la mejor cita, y no firma
nada. Da candidatos; cada uno se le enseña al IEBH con su evidencia y su
corrección propuesta, y firma él.

**¿Sirve para los otros capítulos?** Medido: el aparato de derivación paso a
paso **existe sólo en el capítulo 2**. El 3 y el 4 no tienen cadenas (0
derivaciones: el kāraka trata del uso de los casos y el samāsa da análisis, no
pasos), y el 1 tiene secuencias en prosa, que ya están cubiertas por
`auditar_secuencias.py` y por `S.combinar()`. De modo que el guion se escribe
para el 2 — pero **tomando el capítulo como argumento**, porque los capítulos
5-8 (taddhita, ākhyāta, kibbidhāna, uṇādi) vendrán llenos de derivaciones y
conviene que ya esté hecho cuando lleguen.

Nombre propuesto: `herramientas/auditar_derivaciones.py`.

---

## 6. ESTADO Y COMMITS

Publicado en dos commits (`487208a` y `5223376`) más los anteriores de la
sesión. Tocado: `docs/2. Nāma-Kappa.md`, `kaccayana/02-nama-kappa.en.md` y su
salida convertida, `recursos/paradigmas/paradigmas.json`, `ingles.json`,
`plantilla.html`, `herramientas/generar_capitulo.py`, `CLAUDE.md` y el HTML
regenerado.

Lo que **no** se ha tocado, y sigue esperando: la tanda 2 del inglés y los
puntos 17-34 de la revisión del glosario (sesiones 57-58).
