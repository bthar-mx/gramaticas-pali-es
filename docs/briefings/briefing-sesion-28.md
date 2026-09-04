# Kaccāyana Pāḷi-Español: Briefing de la Sesión 28

*Complementa a los briefings 05–27. Tema único: **el capítulo 8, el
Uṇādi-kappa, traducido entero en borrador** (§624–§673, cuatro tandas).
Con él quedan traducidos en borrador **los ocho capítulos de la obra**.
No se tocó el emparejador ni ningún capítulo publicado ni las revisiones
pendientes (capítulos 5, 6 y 7, que siguen en sus propios chats).*

> **Lo primero que tiene que saber el chat nuevo:** el Uṇādi está
> traducido en borrador completo —los 50 suttas, la cabecera y las tres
> fórmulas de cierre (kaṇḍa, kappa y tratado)— y espera la revisión de
> IEBH, que revisará las cuatro tandas juntas. Las cinco tandas del
> capítulo 7 (sesión 27) también esperan la suya. Nada de esto está
> montado.

---

## 1. ESTADO AL CIERRE

HEAD: **`69673a6a`** («kibbidhāna: fuentes del capítulo 7 y borradores
de la sesión 27 (§524–§623); regex de referencias del verificador;
briefing de la sesión»). Comprobado sin ejecutar git, leyendo
`.git/refs/heads/main` y `.git/logs/HEAD` como texto. Con ese commit
El IEBH confirmó los nueve archivos del briefing 27 §1.

**Seis archivos nuevos sin confirmar**, todos de esta sesión:

| Archivo | Qué es |
| --- | --- |
| `docs/8 - Uṇādi-Kappa-Kaccāyana.md` | Fuente Nandisena, cap. 8. Subida del IEBH al chat; **md5 `bcee096f4f5390e0799331a3fa8a9601`, idéntico** al original. 769 líneas, 50 suttas, 49 notas |
| `docs/borradores/sesion-28-suttas-624-638.md` | Tanda 1 — cabecera del capítulo + §624–§638 |
| `docs/borradores/sesion-28-suttas-639-649.md` | Tanda 2 — §639–§649 |
| `docs/borradores/sesion-28-suttas-650-661.md` | Tanda 3 — §650–§661 (el grupo temporal del futuro) |
| `docs/borradores/sesion-28-suttas-662-673.md` | Tanda 4 — §662–§673, cierre del capítulo y de la obra |
| `docs/briefings/briefing-sesion-28.md` | Este archivo |

Confirmarlos y publicarlos corresponde al IEBH.

## 2. EL UṆĀDI, TRADUCIDO EN BORRADOR

50 suttas (§624–§673), **sin kaṇḍas internos** (el capítulo entero es,
según su propio cierre, un solo kaṇḍo — el sexto del Kibbidhāna), 49
notas al pie de Nandisena. Tandas de **15/11/12/12**, cortadas por peso
(los suttas-lista §638, §641, §643, §656, §663, §665 y §673 son
enormes) y manteniendo junto el grupo del futuro (§650–§655); plan
aprobado por IEBH antes de empezar. Formato idéntico a los borradores
de la sesión 27.

**Los dos desfases de numeración, comprobados en los 50 suttas:**

- **Pind = Nandisena + 2** también aquí (§624 = su 626 … §673 = su
  675), verificado en los dos extremos de cada tanda y en el cierre.
  Pind abre «IV.6» justo antes de su 626: para él el Uṇādi es el sexto
  kaṇḍa del Kibbidhānakappa (aunque sus cabeceras de página sigan
  diciendo «IV.5», sic). Su tramo: líneas 6781–7496 de su edición
  convertida. **Con esto queda comprobado el +2 en toda la obra.**
- **Thitzana usa la numeración de Nandisena** sin desfase. Su
  tratamiento en prosa: líneas 24442–26586 del vol. 2 convertido
  (romanizado además en 2763–2821). También cierra «Iti
  kibbidhānakappe uṇā’dikappo chaṭṭho kaṇḍo».
- **La Rūpasiddhi** (en `docs/7- Kibbidhāna-Rūpasiddhi.md`) reparte los
  paralelos entre su cuerpo del Kibbidhāna y su sección
  «Uṇādippaccayanta-naya» (líneas 1048–1285, la del aviso de su nota
  final 439). Cierra con un sutta que Kaccāyana no tiene (su 684,
  «Akkharehi kāra»).

**La verificación mecánica**, con las herramientas de la sesión 26, en
los dos sentidos y tanda por tanda (fuente explícita obligatoria):

    python3 herramientas/verificar_borrador.py <borrador> <ini> <fin> "docs/8 - Uṇādi-Kappa-Kaccāyana.md"
    python3 herramientas/verificar_estructura.py <borrador> <ini> <fin> <§a> <§b> "docs/8 - Uṇādi-Kappa-Kaccāyana.md"

Rangos de línea: tanda 1 = 1–216; tanda 2 = 217–376; tanda 3 =
377–516; tanda 4 = 517–671.

**162 párrafos pāḷi comprobados (49+41+36+36), 162 reproducidos, 0 no
encontrados; VUELTA 0 en las cuatro tandas.** Numeración triple
idéntica en los 50 suttas, números del Saddanīti sin discrepancias,
llamadas de nota 1–49 idénticas y cubiertas. Tres artefactos del
verificador, documentados en las notas de cada tanda: la línea
«**8\. Uṇādi Chapter**» de la fuente se traga el número de §624 en el
lado fuente (benigno; el borrador evita el mismo efecto titulando
«8-CAPÍTULO» con guion); §648 sin número del Saddanīti hace que el
verificador liste «649» (simétrico, comprobado a mano); y el escape
«(1299, 1300\)» de §659 impide leer ese número en el lado fuente.

## 3. LAS ERRATAS PROPUESTAS

**Dieciocho propuestas pāḷi/formato**, cada una con al menos dos
testigos (o el uso interno del propio Nandisena). **Ninguna se corrigió
en el cuerpo**: lectura literal en el cuerpo, propuesta en las NOTAS DE
TRABAJO de su tanda.

| Sutta | Imprime | Propuesta | Quién le lleva la contraria |
| --- | --- | --- | --- |
| §626, ejemplos | devadatto (minúscula ×3) | Devadatto | Su primer ejemplo y Pind. Formato |
| §628, ejemplos | nivārenti **etanā** ti | etenā | Su inglés y el patrón «etenā ti» del capítulo |
| §633, título | Yāṇa-lāṇ**a** | Yāṇa-lāṇā | Pind, su Rūpasiddhi (§657) y Thitzana |
| §635, ejemplos | ajjhey**a**ṃ | ajjheyyaṃ | Su primer ejemplo, Pind, su Rūpasiddhi (§560) |
| §639, ejemplos | khanatī␣␣saṅkho | khanatī **ti** saṅkho | Su inglés («so (ti)»); el doble espacio delata la caída |
| §640 y §641, vuttis | yatha­saṅkhyaṃ (×2) | yathāsaṅkhyaṃ | Pind y Thitzana en ambos; su propio uso |
| §643, referencia | «pūjito **((**Vin. i, 115)» | un paréntesis | Formato. Única referencia conservada en el cuerpo |
| §645, ejemplos | akarāṇ**ī** | akarāṇi | Pind, Thitzana; su «agamāni» (Rū: akarāni) |
| §647, ejemplos | suṇ**a**tī ti soṇo | suṇātī | Su segundo viggaha, Thitzana, Ce(1)Be de Pind |
| §651, título | ṇī gh**in** | ghiṇ | Su propia vutti, Pind, Thitzana |
| §651, ejemplos | passāv**i**, paṭṭhāy**i** | passāvī, paṭṭhāyī | Sus gāmī/bhājī, Pind, Thitzana; el sufijo ṇī |
| §652, título y vutti | K**r**iyāyaṃ | Kiriyāyaṃ | Pind, Thitzana, su «kiriyā» (§638). Ojo: consecuente, quizá deliberada |
| §661, ejemplos | vacitab**bb**an | vacitabban | Triple b; su inglés |
| §665, ejemplos | aggaḷ**h**aṃ | aggaḷaṃ / aggalaṃ | Pind, su Rūpasiddhi, la K de su nota 39, Thitzana |
| §669, vutti | **yatha** | yata | Su viggaha («yatati»), Pind, Thitzana, su Rūpasiddhi (§679) |
| §670, ejemplos | himsatī | hiṃsatī | Falta la niggahita. Formato |
| §671, vutti | ve dhe **dha** | dhā | Pind, Thitzana; su propio «dhāretī ti dhātu» |
| §673, ejemplos | kucchi**k**abban | kucchitabban | Su inglés y Thitzana |

Más unas cuarenta erratas **sólo del inglés**, tabuladas tanda por
tanda («grief (viveko)» por soko en §640, «I will go» por «I will do»
en §652, «root (hetu)» por «cause» en §671, «she is to be heard» por
«bothered» en §673, glosas ausentes, typos…). Dos conservadas literales
por interpretativas y elevadas a decisión: **«gem (mahāli)» y «famous
(bhaddāli)»** (§669), que son con toda probabilidad los nombres propios
Mahāli y Bhaddāli.

**Dudas registradas sin propuesta** (testigos en desacuerdo): §642
«dusa/disa» (Nandisena+Pind contra su propia Rūpasiddhi y Thitzana, que
lo tiene por corrupción de copista); §658 «element (dhāti)» (¿confusión
dhāti/dhātu?); §673 «manti» (Thitzana manati, Rū manate). Cotejar con
el PDF.

## 4. NÚMEROS DE CONCORDANCIA ANÓMALOS (para `comun/concordancia.json`)

- **Rūpasiddhi «0» — primera vez en el proyecto**: §637 y §640 no
  tienen sutta propio en la Rūpasiddhi (Thitzana tampoco les imprime
  segundo número).
- **Sin número del Saddanīti**: §648 (se suma a §413, §523, §563,
  §601).
- **Préstamo**: §653 lleva Rū 306, del capítulo del Kāraka de la
  Rūpasiddhi.
- **Rangos del Saddanīti**: §644 «1271-3», §646 «1282-4», §647
  «1285-6», §656 «1295-6», §659 «1299, 1300» (doble explícito), §664
  «1306-7»; y §666 imprime «1309» donde Pind remite a «Sadd §§
  1309–12».
- **El patrón «matantare» se dispara**: cuatro nuevos según Pind —
  §646 (Sadd 1284), §659 (1299–1300), §662 (1304), §664 (1307)—, que
  se suman a §51, §517, §571 y §613. Ocho en total en la obra.

## 5. LO QUE EL GENERADOR SIGUE SIN SABER HACER (y datos nuevos)

1. **Las «Note» del cuerpo** (briefing 27 §5.1) no crecen: el capítulo
   8 no trae ninguna. Siguen siendo cuatro (§472, §473, §573, §602).
2. **Bloques nuevos del capítulo 8**: «Sufijos diferentes» (§624, siete
   formaciones kara + ṇu = kāru…) y «Ejemplo de formación» (§627, khī +
   man → khema) — material de la propia fuente, no de Thitzana. El
   generador de capítulos tendrá que reconocerlos.
3. **La nota [^3] (§624) remite a §546 del capítulo 7**: primera
   referencia cruzada entre capítulos dentro de una nota; cómo
   enlazarla depende de la decisión §8.3.
4. **La cabecera del capítulo** sólo existe en inglés («Sixth
   Section»): no hay línea pāḷi de apertura de kaṇḍa.
5. **`fuente_por_defecto` de `verificar_borrador.py` no conoce el
   capítulo 8**: su diccionario acaba en `524: 7`, de modo que un
   borrador `sesion-NN-suttas-624-…` caería en la fuente del 7. No se
   tocó el script (todo se corrió con fuente explícita); añadir
   `624: 8` queda propuesto para IEBH.

## 6. SIGLAS Y FORMAS NUEVAS PARA EL REPERTORIO DEL EMPAREJADOR

Tabuladas en el §5 de cada tanda. Lo nuevo del capítulo 8:
«**Vin.A.** iii, 105» (con punto interior, §628), «**CpA.** 17» (§638,
sin volumen), «**ItA.** 278» y «**MndA.** 231» (sin volumen; MndA. es
sigla nueva frente al NdA. del capítulo 7), «**Vin. v**, 41» (volumen
nuevo, §650), «**Ṇvādivutti**, 97» y «**Nyā.**» (en la nota 45), la
vacilación **Abh./Abhi. dentro del mismo sutta** (§656, «i, 157» las
dos), las referencias **triples** «Vin. iii, 4; Khu. v, 100, 152»
(§642) y «Vin. iii, 2; D. ii, 208, 255» (§673), las dobles páginas
«Khu. v, 4, 167», «D. i, 3, 80», «Khu. vi, 34, 361», «JA. i, 16, 17»,
«Khu. i, 58; DhA. i, 193», y «A. i, 553» (§669; página altísima,
cotejar). El regex del verificador ya las absorbe; `RE_SALTABLE` del
emparejador aún no.

## 7. TÉRMINOS PARA EL GLOSARIO

Cada tanda trae su §6. Lo que conviene mirar junto:

- ***uṇādi*** = sin traducir (¿nombre público del capítulo?).
- ***bhāva***: el inglés del capítulo 8 **vuelve a «impersonal»**
  (§625, §641) tras el «verbal noun» del 7 — dato nuevo para la
  decisión pendiente del briefing 27 §7.
- ***pāṭipadika*** = «base» provisional — el término más frecuente del
  capítulo sin entrada; **colisiona con *liṅga* = «base»**.
- ***upadhā*** = «penúltima [letra]» (§629).
- *pesa / atisagga / pattakāla* (§635); *avassaka / adhamiṇa* (§636);
  *sesa* = «lo inacabado» (§655, pide decisión); *bhāvavāci* (§653);
  *gaṇa* = «colección» (§657); *nibbatta* (§644); *guṇa* = «refuerzo»
  (§642, único lugar de la obra); *nippajjante* = «se forman»;
  *yathāsambhavaṃ* = «según corresponda»; *kiriyā* (ligada a la errata
  Kriyā); ***mettā*** = «amor benevolente» (§656; término doctrinal
  mayor, conviene fijarlo).
- *payoge sati* reapareció (§637) con el valor ya fijado en §604.

## 8. DECISIONES QUE ESPERAN A ANGEL

1. **Las dieciocho erratas pāḷi/formato del §3** y las del inglés
   (mahāli/bhaddāli en particular).
2. **El estatuto del Uṇādi** (briefing 27 §8.3) — la sesión aporta los
   datos que faltaban, todos en la misma dirección: la propia fuente
   rotula «Sixth Section» y cierra «Iti **kibbidhāna-kappe**
   uṇādi-kappo **chaṭṭho kaṇḍo**», aunque numere el capítulo como 8 y
   despida «Uṇādi-kappo niṭṭhito»; Pind lo edita como IV.6; Thitzana
   como sexto kaṇḍo. Afecta al slug, al índice del sitio y a
   `CAPITULOS`.
3. **Los números anómalos del §4** para `concordancia.json`.
4. **Las siglas nuevas del §6.**
5. **Los términos del §7**, con el dato nuevo de *bhāva*.
6. **Seis observaciones de Pind** candidatas a nota del traductor:
   ‘āni’ como mala lectura del sandhi «namh’ âni» (§645); la
   atribución de nibbatte a los nombres en ‘thu’ (§644); «gaṇe» por
   «karaṇe» (§657); «uḍḍho» por «uṭṭho» y daḍḍha desde «daha» (§659);
   su análisis de ṇī/ghiṇ (§651, con la nota 21 de Nandisena y la
   cuestión ssaṃ/ssantu de §655); y el verso final de Senart/Mahābodhi
   que Pind imprime y Thitzana documenta (nota 57), con el «sandhikappo
   niṭṭhito» (sic) del cierre de Pind.
7. **Los nombres propios con viggaha** (§663 Isiṇḍa, §669
   Mahāli/Bhaddāli, §673 Illiso) — reabren el §5.3 del briefing 27.
8. **Añadir `624: 8` a `fuente_por_defecto`** del verificador (§5.5).

## 9. QUÉ NECESITA EL CHAT NUEVO

1. Leer este briefing y `comun/convenciones.md` §0, que es normativo.
2. **Las fuentes del capítulo 8 ya están en `docs/`** con md5
   comprobado (§1). No hay que pedir nada.
3. **La revisión de las cuatro tandas es del IEBH** y se hará junta;
   también sigue pendiente la de las cinco tandas de la sesión 27.
   Hasta entonces no se montan capítulos ni se tocan los borradores.
4. Si lo que toca es **montar**, el orden es 5 → 6 → 7 → 8 (cada
   `CAPITULOS` necesita al anterior), y antes hay que resolver las
   «Note» del cuerpo (briefing 26 §5.2/27 §5.1), el tachado del 6 y la
   decisión §8.2 de este briefing.
5. Tramos localizados en las fuentes de cotejo: **Pind** líneas
   6781–7496 (sus 626–675 + cierre); **Thitzana** líneas 24442–26586
   (prosa) y 2763–2821 (romanizado); **Rūpasiddhi** sección Uṇādi en
   líneas 1048–1285 de `docs/7- Kibbidhāna-Rūpasiddhi.md` (ojo a su
   nota 439: el tramo final no está editado).
6. **La obra está entera en borrador.** Lo que sigue es revisión y
   montaje, no traducción.

## 10. RECORDATORIOS QUE NO CAMBIAN

Los del §10 del briefing 27, íntegros: nada de git desde el sandbox (ni
`status`); con IEBH en inglés, **la respuesta entera, también los
bloques para copiar**; el producto en español; nada de calcos —
`comun/convenciones.md` §0; los PDF no viven en el repositorio; todo
cambio del emparejador corre contra los capítulos publicados; nada se
edita en `site/` salvo `pali.css`, `pali.js` y los SVG; lo de Thitzana
se señala como suyo y su flecha va al revés; ante duda, `<!-- DUDA -->`;
**proponer y verificar, nunca afirmar**; el briefing se escribe cuando
ya no se va a tocar nada más. Y los dos de esta sesión: **para los
capítulos 7 y 8, las herramientas de verificación necesitan la fuente
como argumento explícito** (los valores por defecto apuntan al 6, y el
diccionario no conoce el 8); y las erratas del inglés se corrigen en la
traducción sólo cuando el desliz es evidente — las interpretativas se
conservan literales y se registran.
