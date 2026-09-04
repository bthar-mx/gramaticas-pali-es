# Briefing de la sesión 49 — el Conspectus, páginas 1132-1134

**Fecha:** 2026-09-03. **Estado:** 30 de las 44 páginas transcritas (1105-1134).
**Lo que hay que hacer:** seguir por la página 1135.

Este briefing supone leídos los de las sesiones 46, 47 y 48, que siguen
vigentes en todo lo que no se corrija aquí. **Y aquí se corrige una cosa del
48 que cuesta una hoja mal sacada: la tabla de desfases de los PDF. Ver §2.**

---

## 1. Lo hecho

Tres páginas nuevas, 163 términos, de 1.089 a 1.252. El generador publica
limpio.

| pág. | epígrafes | materia |
| --- | --- | --- |
| 1132 | 5.3.3.2, 5.3.3.3 | fin de la lengua del canon; **empieza la exégesis** |
| 1133 | 5.3.3.3, 6.0.1 | los autores, los poetas; **empieza la semántica** |
| 1134 | 6.0.2, 6.0.3, 6.1.1.1 | las cinco categorías; significante y significado; el pada |

La 1134 se corta en «vibhatyanta : avibhatyanta,»: **la 1135 sigue dentro de
6.1.1.1**.

Son tres páginas y no siete porque la 1134 sola trae 69 términos —es la más
densa de las treinta transcritas— y porque la verificación de referencias de §3
se llevó lo suyo. La 1133 y la 1134 son, además, el punto en que Smith deja la
filología y entra en la teoría del significado: **de aquí en adelante el
Conspectus es un tratado de semántica**, y las fichas piden más nota.

---

## 2. CORRECCIÓN AL BRIEFING 48: LA TABLA DE DESFASES ESTABA MAL, Y AHORA HAY GUION

El briefing 48 §2 da esta tabla, «hoja = impresa − N», con N = 14, 307, 593,
921, 1166. **Para los vols. 03, 04 y 05 funciona; para el 01 y el 02, no**, y
el fallo no es de redondeo:

- Los números de esa tabla son `leafNum`, que **empieza en 0**, mientras que
  `pdftoppm -f` **empieza en 1**. Hay una unidad de desfase en todos.
- En el **vol. 01 el signo está invertido**: la hoja del PDF es MAYOR que la
  página impresa, porque van delante las portadas y el prefacio. Pedir la hoja
  `127 − 14 = 113` no da la p. 127 sino la 98. La buena es la 142.
- **Un volumen puede tener más de un tramo.** El 04 usa un desfase para las
  pp. 930-941 y otro a partir de la 946.

La correspondencia real, leída de los propios `.paginas.json`:

| vol. | páginas impresas | hoja del PDF = impresa + |
| --- | --- | ---: |
| 01 | 2 - 314 | **+15** |
| 02 | 316 - 392 | −306 |
| 02 | 395 - 602 | −308 |
| 03 | 604 - 928 | −593 |
| 04 | 930 - 941 | −919 |
| 04 | 946 - 1172 | **−921** |
| 05 | 1174 - 1460 | −1165 |

**Para no volver a calcularlo a mano hay guion nuevo**, y es lo único que se ha
añadido al repositorio fuera de las tres páginas:

    python3 herramientas/pagina_saddaniti.py 755        # una página
    python3 herramientas/pagina_saddaniti.py 127 691    # varias
    python3 herramientas/pagina_saddaniti.py --tabla    # los tramos

No calcula nada: lee la correspondencia del escaneo y escribe la orden de
`pdftoppm` lista para copiar. **Si Angel prefiere no tenerlo en
`herramientas/`, se quita y no se pierde nada**: la tabla de arriba basta.

---

## 3. SEIS REFERENCIAS VERIFICADAS, Y EL MÉTODO DA MÁS DE LO QUE PROMETÍA

El método del briefing 48 §2 —abrir la página citada y contar líneas— se
aplicó a las seis referencias a la propia Saddanīti de estas tres páginas.
**Las seis caen exactamente donde Smith dice.** Ninguna corrección.

| referencia | dónde sale | qué hay en esa línea |
| --- | --- | --- |
| **127,33—129,6** | 1132 (saddabheda) y 1134 (attha) | 127,33 es la ÚLTIMA línea de la página, «…jānitabbā. Buddhavacanasmiṃ»; cierra en 129,6, «garatare nibbānatitthūpage” ti» |
| **35,3** | 1133 (tabbisayaṃ buddhiṃ uppādeti) | «sutisāmaññato tabbisayaṃ buddhiṃ n' uppādeti vinā…» |
| **37,15—22** | 1133 (íd.) | contiene gahitapubbasaṃketa (l. 19) y la estrofa de visayattaṃ (l. 21-22) |
| **37,21—22** | 1133 (adaptaciones del sánscrito) | la estrofa entera, con su original sánscrito en nota al pie |
| **289,25, 26** | 1133 (íd.) | las dos citas del **Kāvyādāsa**, que es justo «un passage sanskrit» |
| **604,28—605,6** | 1134 (akkhara) | 604,28 abre «ime pana vaṇṇā saṃ-», y 605,6 cierra «…na khīyantī ti attho ti» |
| **691,29—32** | 1134 (asantaṃ santaṃ va kappīyati) | 691,29 **es el sutta 549 entero**, y 30-32 su vutti con los cinco ejemplos |

### Y esto es lo que no se esperaba: la página citada resuelve la LECTURA, no sólo la referencia

**El caso de `lokanīti-vidhura` (5.3.3.2, p. 1132) es el que hay que retener.**
La ī del Conspectus no se decide a 400 dpi —regla de la sesión 47—, y en vez de
forzar la imagen se abrió la página que Smith cita. La voz está allí, en
**129,4**: «yebhuyyena hi **lokanītividhurā** pāṭhe nayā vijjare», en cuerpo de
texto, donde el macrón contrasta limpiamente con las i breves de la misma
palabra. **Lema resuelto: lokanīti, con ī.**

De modo que la regla de la sesión 47 gana una salida que no tenía:

> Donde la imagen del Conspectus no decide una cantidad vocálica y Smith cita
> un pasaje, **hay que mirar el pasaje antes de marcar `duda`**. El cuerpo de
> texto es legible donde el Conspectus no lo es.

**Esto toca de refilón la `duda` de `saddhammaniti` (5.3.3.2, p. 1131)**, que
quedó abierta en la sesión 48 por la misma razón. Allí Smith no da referencia,
así que la salida no sirve; pero **la 1132 imprime `lokanīti` con macrón claro
en su cita**, lo que es un argumento más —no una prueba— a favor de
`saddhammanīti`. **La ficha de la 1131 no se ha tocado.** Es decisión de Angel.

Las demás referencias de estas páginas —a la PTS (Kva, M, As, Ppa, Sp, Vin) o
sin cotejar (105,33; 907,7—13; 910,18—24; 325,19; p. 1016)— van leídas de la
imagen, y las fichas no afirman nada sobre ellas.

---

## 4. Erratas y rarezas nuevas, ninguna corregida por cuenta propia

- **`Mahābodhivaṃśaparikathā` con Ś PALATAL (5.3.3.3, p. 1132), y la 1133 la
  desmiente.** A diez líneas de distancia, en la p. 1133, Smith escribe
  **`Mahābodhivaṃsa` con s normal**. Comprobadas las dos a 400 dpi: el acento
  de la ś se ve limpio. La misma obra, dos grafías. Va con `duda` en la ficha
  de la 1132, y la de la 1133 lo dice.
- **La convención de los corchetes no es firme.** Smith declaró en 4.1 que los
  corchetes traen el sánscrito, y en estas tres páginas hay **tres sánscritos
  sin corchete**: `prātiśākhya` (p. 1132), el `vaṃśa-` de arriba y `gamyate`
  (p. 1134, pasivo en -yate que el pāḷi hace -īyati). Con el `anuprāsa` de la
  p. 1127 son cuatro en ocho páginas. Los tres nuevos van con `duda`. **No es
  que la convención no exista** —en las mismas páginas van entre corchetes
  `[vyavahārasatya]`, `[saṃvṛti]`, `[a-lakṣaṇa]`, `[atyantābhāva]` y
  `[sphoṭa]`—, es que Smith no la sigue siempre.
- **`vibhatyanta : avibhatyanta` (6.1.1.1, p. 1134)**, con **una sola t** y con
  y de transición, que es el tratamiento sánscrito de *vibhakti + anta*; el
  pāḷi pediría `vibhattyanta` o `vibhattanta`. Comprobado a 400 dpi en las dos
  voces. Van con `duda`. Encaja con que en esa misma página Smith escriba
  `vyañjana`, `vyappatha` y `mukhyavasena` sanscritizando.
- **`ib` sin punto (5.3.3.3, p. 1132)**, en «(ib 2.6; 4.1.1)», mientras las
  demás remisiones de la página llevan «ib.». Se transcribe como está impreso.
- **La coma de las remisiones al Index A.** Smith escribe `1.1,1`, `3.7,1`,
  `1.2,11`, `3.1,11`: la **coma** introduce la capa comentarial dentro de la
  obra, y el punto los demás escalones. En `mahāṭīkā (ib. 2.8.1,1)` el tercer
  separador no se decide sobre la imagen —a 400 dpi coma y punto dan la misma
  mancha—; se transcribió con coma por coherencia con la serie, y va con
  `duda`.
- **El signo `×` de `[sammati × saṃvṛti]` (6.0.1, p. 1133)** no está explicado.
  Queda registrado sin interpretar, como el `‖` de la p. 1129.
- **Smith glosa `saṃketa` con una palabra GRIEGA**, συνθήκη (6.0.1, p. 1133).
  Es la primera vez que echa mano del griego en lo transcrito. Va verbatim.

### Dos misterios viejos que esta sesión deja MÁS CERCA, sin cerrarlos

Los dos salieron de mirar páginas del cuerpo de la obra para verificar
referencias, no de las páginas del Conspectus:

- **El `ns` de 5.1.0 (p. 1120)**, que la sesión 47 dejó «sin interpretar». En
  las pp. 98, 289 y 604 del cuerpo, `ns` aparece **en el aparato crítico y en
  la cabecera de página**, junto a `Ce` y `Bm`: «CeBemns». **Es una de las
  siglas de testimonio de Smith**, y sale también en cuerpo de nota, «¹ ns:
  yān' asmāsu na vijjanti…». Falta cotejarlo con la lista de siglas de los
  preliminares, que no se ha buscado. Como pista es sólida; como conclusión,
  todavía no.
- **El `‖` de 5.3.2.3 (p. 1129).** En el aparato de las pp. 289 y 691 el `‖`
  separa entradas y delimita el texto de un sutta: «‖ Abhinipphādanalakkhaṇaṃ
  kattukārakaṃ ‖.» Mismo signo, otro contexto. **No se ha tocado la ficha de la
  1129.**

---

## 5. Homónimos nuevos: NUEVE, y el cotejo también CONFIRMÓ cosas

Se repitió el cotejo con Nandisena sobre los 163 términos nuevos, término a
término y con las dos definiciones a la vista, como pide el briefing 48 §5. El
guion está en `/tmp` de la sesión y se rehace en diez líneas: casa por
`desnudo()` e imprime las dos definiciones recortadas.

| término | Smith | Nandisena |
| --- | --- | --- |
| **saddabheda** (5.3.3.2) | el corte entre pāḷi y no-pāḷi | la tripartición interna de la variación de la palabra |
| **nissaya** (5.3.3.3) | el género birmano de paráfrasis | «las vocales son nissaya» — el apoyo fonético |
| **garū** (5.3.3.3) | los maestros de autoridad | la sílaba PESADA |
| **vikāra** (6.0.2) | categoría de lo cognoscible, lo derivado | la alteración fonética |
| **abhidheyya** (6.0.3) | el Significado, sin más | «el significado de un compuesto relativo (bahubbīhi)» |
| **bhāva** (6.0.3) | la intención del hablante | el nombre abstracto, el impersonal |
| **vyañjana** (6.0.3) | la Expresión, la letra | la CONSONANTE |
| **vacana** (6.0.3) | la palabra, el decir | y además, en otra entrada, el NÚMERO |
| **satti** (6.0.3) | la potencia significativa (la śakti) | «una de las tres propiedades del tema (liṅgattha)» |

**`vyañjana` es el peligroso**, del calibre de `sutta` y `vagga`: en una
gramática pāḷi byañjana es la consonante y nada más, y aquí Smith lo usa nueve
veces seguidas por «la letra frente al espíritu».

### Lo que el cotejo confirmó, que también vale

- **`akkhara` son 41 en las tres fuentes.** Smith dice «les 41 akkhara»,
  Sad. 604,24 dice «ekacattālīsa saddā akkharā» y Nandisena «hay 41 letras en
  el alfabeto pali». Las tres coinciden.
- **`rūḷhi` (6.0.1)**: Nandisena dice lo mismo que Smith y encima da la
  oposición técnica que a él le falta, «opuesto de yoga y anvattha». Ojo con la
  grafía: su lema de cabecera es **`ruḷhī`**, con u breve e ī larga, y Smith
  imprime `rūḷhi`. No se corrige ninguna.
- **`veyyākaraṇa`**: Nandisena registra los dos valores, «gramático;
  explicación», de modo que la ambigüedad con el aṅga de la p. 1131 es del
  término y no de la transcripción.

### Y una divergencia de FONDO, que no es homonimia

**`pada` (6.1.1.1).** Nandisena lo define por la desinencia —«aquellos que
terminan con inflexión (vibhatti) se denominan pada»—, de modo que sin vibhatti
no hay pada. Smith admite las dos cosas, «à désinence… ou sans désinence», y
por eso su definición necesita el par `vibhatyanta : avibhatyanta`. **Los dos
describen la misma unidad y no le ponen la misma frontera.** Anotado en la
ficha, sin tocar ninguna de las dos definiciones.

### Un aviso sobre el cotejo automático

En `samaññā` (6.0.1) la página engancha **dos** entradas de Nandisena, `samaññā`
y `sāmañña`, porque `desnudo()` quita los macrones. La segunda es otra palabra.
La ficha lo advierte. No se ha tocado `desnudo()`.

---

## 6. Cosas de la transcripción, para seguir

- **Primer lema con GUIÓN INICIAL**: `-dīpana` (5.3.3.3, p. 1132), de
  «līnattha-pakāsana, -dīpana». Es el mismo procedimiento de las series de
  5.1.1.3 y 5.2.3 pero al revés: allí Smith abrevia el segundo miembro y el
  guión queda a la derecha; aquí abrevia el primero. **Se transcribe abreviado,
  como está impreso**, y el generador lo admite: comprobado.
- **Los paréntesis dentro de palabra siguen siendo abreviaturas**, y esta tanda
  trae nueve: `(sammukha)sāvaka`, `(saddhamma)neruttika`, `(porāṇ)aṭṭhakathā`,
  `attha(saṃ)vaṇṇanā`, `(abhi)navaṭīkā`, `(porāṇa)kaviracanā`,
  `payoga(racanā)`, `sammuti(attha)`, `(attha)bodhaka`, `(attha)pakāsaka`,
  `(atthavisesa)jotaka`. Las formas desplegadas van en `variantes`.
- **Expresiones de varias palabras**: `sakkaṭabhāsāto nayaṃ gahetvā vuttāni`,
  `tantinayānukūlā bhāsā`, `vohārūpagā saddā`, `vattum icchā`, `asantaṃ santaṃ
  va kappīyati`, `visayattaṃ āpannā`, `tabbisayaṃ buddhiṃ uppādeti`.
- **`visayattaṃ āpannā` va en POSITIVO y la fuente en negativo.** El verso de
  37,21 dice «visayattaṃ **an**āpannā saddā n' ev' atthabodhakā»; Smith enuncia
  la condición, no cita. La forma negada está en `variantes`, y la ficha lo
  explica. Lo mismo pasa con `tabbisayaṃ buddhiṃ uppādeti` frente a 35,3, que
  lleva `n'`.
- **Smith cita en TEMA y marca el final en cursiva.** En `vācin` la n va en
  cursiva dentro de la palabra redonda, y lo mismo la t de `atthavat`. Es la
  costumbre de `kattar` (5.1.1.1) y `sotar` (5.3.3.3), ahora con marca
  tipográfica.
- **`saṃkhāra`, `saṃkhata`, `saṃketa` con ṃ, no con ṅ.** Es su norma en toda la
  sección 6 y se transcribe como está impreso.
- **Formas flexionadas como están impresas**: `porāṇā`, `ācariyā`, `garū`
  (plurales), `sotūnaṃ`, `viññūnaṃ`, `āgamikānaṃ` (genitivos plurales),
  `kosallajananatthaṃ`, `buddhivijambhanatthaṃ` (acusativos adverbiales),
  `mukhyavasena`, `upacāravasena` (instrumentales), `atthato`, `vyañjanato`,
  `ganthato`, `pariyattito`, `dhammato` (ablativos adverbiales),
  `padavyañjanāni` (plural neutro). El tema va en `variantes`.
- **Palabras que NO son pāḷi y van igual**: `gæṭapada` y `sannaya` (singalés),
  `nissaya` (birmano por el género), y los sánscritos ya dichos.
- **Un lema partido ENTRE PÁGINAS**: `lokiyamahājana`, «lokiyama-» al pie de la
  1131 y «hājana» al abrir la 1132. La ficha vive en la 1132.
- **Ningún lema repetido dentro del mismo epígrafe en estas tres páginas**, y
  eso que hay repeticiones a mansalva entre epígrafes: `akkhara` y `paññatti`
  dos veces en la 1134, `saddalakkhaṇa` dos en la 1132, `atthajotaka` dos en la
  1134, `vohāra` cuatro veces en cuatro páginas y con cuatro valores.
- **Los paréntesis angulares siguen garantizando a Moggallāna**: `⟨vivacchā⟩`
  (6.0.2, p. 1134). Y siguen sin garantizar lo contrario, según el briefing 48
  §3.

---

## 7. Cómo se sigue, en concreto

    # la hoja del PDF que toca, sin calcularla a mano
    python3 herramientas/pagina_saddaniti.py 1135

    python3 herramientas/generar_glosario.py

Lo que funcionó esta sesión, y conviene repetir:

1. **Cortar la página en bandas horizontales de unos 620 px a 0,8 de escala**
   para leerla entera y situar los epígrafes. Cinco o seis bandas por página.
2. **Después, recortar CADA LÍNEA en dos mitades a 1,5×** y leer sólo las que
   llevan pāḷi. Es lo que decide las ṇ, las ṭ y las ś. Calcular las rachas de
   tinta y recortar **en el mismo guion**, como avisa el briefing 48 §7.
3. **Ojo con el detector de líneas en páginas densas.** En la 1133 el umbral
   de `rows > 3` fundía las líneas de dos en dos; con `rows > 30` sobre la
   franja `[:,160:2250]` salen las 34 limpias. Conviene comprobar que el número
   de rachas cuadra con las líneas que se ven en las bandas antes de fiarse.
4. **No subir de 400 dpi.** A 3× sobre 400 dpi ya se ve el grano del escaneo,
   no más letra.

---

## 8. Lo que sigue pendiente, y no se ha tocado

1. **Rehacer el cotejo con el Diplomado cuando estén las 44 páginas.** Sin
   cambios desde la sesión 46. **No debe correrse hasta el final.**
2. **Repasar las ī de las páginas 1105-1115** con el criterio de la sesión 47
   —y ahora también con la salida de §3: mirar la página citada—. Sigue
   pendiente.
3. **La tarjeta de `/recursos/`**: la página existe y no está enlazada. Falta
   el visto bueno de Angel (`herramientas/generar_indices.py`, y su copia
   inglesa).
4. **El guion `herramientas/pagina_saddaniti.py` es nuevo** y está a la espera
   del visto bueno de Angel, como se dice en §2.
5. **Buscar la lista de siglas de Smith** en los preliminares del vol. 01, para
   cerrar el `ns` de §4.
6. Las decisiones de Angel que siguen abiertas: **lahu** («leve» frente al
   «breve» del Diplomado), **niggahita/niggahīta**, **ensanchar āgama** —y esta
   sesión da un tercer argumento: el `āgamikānaṃ` de 5.3.3.3 (p. 1133) es «los
   versados en la tradición», no un fonema—, el `sukkhuccāraṇatthaṃ` de la
   p. 1108, el `avadhārana` de la p. 1119, el `saddhammaniti` de la p. 1131
   (ver §3), y las tres notas de paradigmas que dicen «con el visto bueno de
   Angel» donde la norma pide «el IEBH».

---

## 9. Cifras al cerrar

| | |
| --- | --- |
| páginas del Conspectus | **30 de 44** (1105-1134) |
| términos del Conspectus | **1.252** (eran 1.089) |
| entradas de Nandisena | 649 |
| normativos de `comun/glosario.md` | 53 |
| en las dos fuentes | 335 (27 %) |
| fichas con `conflicto` | 29 (eran 20) |
| fichas con `duda` | 18 (eran 12) |
| referencias verificadas contra la fuente | 6 nuevas, ninguna corregida |
