# Kaccāyana Pāḷi-Español: Briefing de la Sesión 27

*Complementa a los briefings 05–26. Tema único: **el capítulo 7,
Kibbidhāna, traducido entero en borrador** (§524–§623, cinco tandas). No
se tocó el emparejador ni ningún capítulo publicado ni la revisión de los
capítulos 5 y 6, que sigue en sus propios chats.*

> **Lo primero que tiene que saber el chat nuevo:** el Kibbidhāna está
> traducido en borrador completo —los 100 suttas y los cuatro versos
> iniciales— y espera la revisión de Angel, que revisará las cinco tandas
> juntas. Los capítulos 5 (Taddhita) y 6 (Ākhyāta) siguen esperando la
> suya. Ninguno de los tres está montado.

---

## 1. ESTADO AL CIERRE

HEAD: **`1d89ae2f`** («ākhyāta: fuentes del capítulo 6 y borradores de la
sesión 26 (§406–§523); verificadores de borrador y briefing»). Comprobado
sin ejecutar git, leyendo `.git/refs/heads/main` y `.git/logs/HEAD` como
texto. Con ese commit quedaron confirmados los once archivos que el
briefing 26 §1 daba como pendientes.

**Nueve archivos nuevos o modificados sin confirmar**, todos de esta
sesión:

| Archivo | Qué es |
| --- | --- |
| `docs/7- Kibbidhāna-Kappa-Kaccāyana.md` | Fuente Nandisena, cap. 7. Subida de Angel al chat; **md5 `e79457f262df4db4541960f841d8e4bc`, idéntico** al original |
| `docs/7- Kibbidhāna-Rūpasiddhi.md` | Rūpasiddhi, Kibbidhāna-kaṇḍa (con su Uṇādi y el nigamana), para cotejo. **md5 `a92fe15a8af836ded177df14c0984f15`, idéntico**. Ojo: su nota final 439 avisa en español de que el tramo último «todavía no [ha] sido editado» |
| `docs/borradores/sesion-27-suttas-524-549.md` | Tanda 1 — versos + primera sección entera |
| `docs/borradores/sesion-27-suttas-550-570.md` | Tanda 2 — segunda sección entera |
| `docs/borradores/sesion-27-suttas-571-589.md` | Tanda 3 — tercera sección entera (el sutta comodín §571) |
| `docs/borradores/sesion-27-suttas-590-606.md` | Tanda 4 — cuarta sección entera |
| `docs/borradores/sesion-27-suttas-607-623.md` | Tanda 5 — quinta sección, cierre del capítulo |
| `herramientas/verificar_borrador.py` | **Modificado**: el regex de referencias acepta ahora volumen romano opcional («KhuA. 109») y Ṭ/guion en la sigla («Sārattha-Ṭīkā ii, 329»). Cambio comentado en el propio script |
| `docs/briefings/briefing-sesion-27.md` | Este archivo |

Confirmarlos y publicarlos corresponde a Angel.

## 2. EL KIBBIDHĀNA, TRADUCIDO EN BORRADOR

100 suttas (§524–§623), **cinco kaṇḍas** (no cuatro como el Ākhyāta),
cuatro versos iniciales (K/Kh/G/Gh), 50 notas al pie de Nandisena. Tandas
de 26/21/19/17/17 **cortadas exactamente por las fronteras de kaṇḍa**,
plan aprobado por Angel antes de empezar. Formato idéntico a los
borradores de las sesiones 25 y 26.

**Los dos desfases de numeración, comprobados en los 100 suttas:**

- **Pind = Nandisena + 2** también en este capítulo (§524 = su 526 …
  §623 = su 625), verificado en los dos extremos de cada tanda y en los
  cinco cierres de kaṇḍa. Su edición convertida imprime «|| te kiccā ||
  551 ||» por error de OCR donde su aparato dice 547; no altera el
  desfase. Su Kibbidhāna va de la línea 5795 a la 6800.
- **Thitzana usa la numeración de Nandisena**, sin desfase. Su tramo va
  de la línea 22039 a la 24430 del vol. 2 convertido (texto romanizado
  de los suttas además en 2642–2822).

**La verificación mecánica**, con las herramientas de la sesión 26 y en
los dos sentidos, tanda por tanda:

    python3 herramientas/verificar_borrador.py <borrador> <ini> <fin> "docs/7- Kibbidhāna-Kappa-Kaccāyana.md"
    python3 herramientas/verificar_estructura.py <borrador> <ini> <fin> <§a> <§b> "docs/7- Kibbidhāna-Kappa-Kaccāyana.md"

(Para el capítulo 7 hay que pasar la fuente explícita: los valores por
defecto de ambas herramientas apuntan al capítulo 6.)

**339 párrafos pāḷi comprobados (87+64+74+57+57), 339 reproducidos, 0 no
encontrados.** En sentido inverso, la única línea de la fuente que la
VUELTA lista (tanda 2) es la normalización documentada de §562: el punto
residual de la referencia que sigue al «?» («arahati?. Sakkā»). Numeración
triple idéntica en los 100 suttas, números del Saddanīti sin
discrepancias, llamadas de nota 1–50 idénticas y cubiertas. Dos
normalizaciones deliberadas, documentadas en sus NOTAS DE TRABAJO: §528
(«;,» residual tras referencia) y la citada de §562.

**El cambio del verificador nació de un aviso real:** la primera pasada
de la tanda 1 dio §524 y §544 como no verificables. La causa era el
regex, que exigía volumen romano y no conocía «KhuA. 109» ni
«Sārattha-Ṭīkā». Se amplió el regex (no los datos), y se pasó regresión
sobre las tandas 1 y 6 del capítulo 6: 87/87 y 77/77, con la
normalización conocida de §513 aún informada.

## 3. LAS ERRATAS PROPUESTAS

**Ocho de lectura pāḷi**, cada una con al menos dos testigos
independientes contra Nandisena (o su propio uso interno). **Ninguna se
corrigió en el cuerpo**: el borrador conserva la lectura literal y la
propuesta está en las NOTAS DE TRABAJO de cada tanda.

| Sutta | Imprime | Propuesta | Quién le lleva la contraria |
| --- | --- | --- | --- |
| §538, título | Saṃhan’ **āñ**ñāya | aññāya | Su propia vutti, Pind, el desglose de Thitzana y su propia edición de la Rūpasiddhi (§595) |
| §539, vutti | rakārād**ī** lopo | rakārādi | Pind (Be), la vutti de Thitzana y su propio título («rādi») |
| §548, vutti | icc’ **etasv** atthesu | etesv | Pind, la gramática y su propio §540 |
| §551, título | (**s**1138) | (1138) | Residuo tipográfico; la serie 1137–1139 lo confirma |
| §564, ejemplos | amutr**o** | amutra | Pind, Thitzana y el adverbio canónico |
| §573, vutti | Sakāra**nata** | Sakāranta | Su propio inglés y título, Pind, Thitzana |
| §587, vutti | timh**ī** ca | timhi | Sus §585, §586, §588 y Pind |
| **§592, vutti** | **dhātu**sa | dhātussa | Pind, la vutti de Thitzana y su propio uso en todo el capítulo |
| **§612, kimatthaṃ** | «	 ti kimatthaṃ?» | **Ḍhakāre** ti kimatthaṃ? | Falta el lema; su propio inglés y Pind lo traen. Único kimatthaṃ sin lema del capítulo |

Más las de formato: «?» ausente en §538; «;,» de §528 y «?.» de §562
(normalizadas y documentadas); «26» pegado a kaṭṭhaṃ en §583 (llamada de
nota rota); minúscula de «saḷāyatanaṃ» (§571); «bhavatūti» pegado
(§552); espacio tras guion en la vutti de §601; doble espacio en §618;
negrita partida en el título de §604 (normalizada). Y unas cincuenta
erratas **sólo del inglés**, tabuladas tanda por tanda (typos, glosas
perdidas, «sister» por «daughter» en §568, «ma» por «bha» en §600,
«karitvā» como «should be done» en §605…).

**Cinco lecturas que parecen erratas y no se propusieron**, cada una con
su porqué en las notas: §541 «daṭṭheyyaṃ» (su Rūpasiddhi lo confirma
contra Pind), §544 «garassa» (Thitzana con él), §567 «Pātito» (elección
defendida en su nota 25), §571 «kathinadussaṃ» (Thitzana con él), §600
«āraddha, ārabhitvā» (Thitzana con él; Pind lee «ārādhitvā»), §617
«sakito» (su inglés lo respalda).

## 4. NÚMEROS DE CONCORDANCIA ANÓMALOS (para `comun/concordancia.json`)

El Kibbidhāna es el capítulo con más números fuera de serie del proyecto:

- **Sin número del Saddanīti:** §563 (su nota 21 remite a la página 393
  de la Suttamālā) y §601. Se suman a §413 y §523.
- **Rango en vez de número:** §564 lleva «1150-6» (también en su
  Rūpasiddhi §640).
- **Números prestados de otras partes:** §592 Rū 503; §601 Rū 334; §602
  Rū 6 y Sad 10; §603 Rū 7 y Sad 9 (¡el par en orden inverso en la
  Saddanīti!); §608 Sad 1165; §609 Rū 484; §578 Rū 560; §586 Rū 600.
- **El patrón «matantare»** reaparece: §571 (Sad 1164) y §613 (Sad 1218)
  van como opinión ajena en la Saddanīti según Pind — como el §517 del
  Ākhyāta y el §51 del Sandhi. Los dos son, respectivamente, el sutta
  comodín del capítulo y una regla con «vā».

## 5. LO QUE EL GENERADOR SIGUE SIN SABER HACER

1. **Las «Note» del cuerpo suman cuatro**: §472 y §473 del Ākhyāta
   (briefing 26 §5.2) más **§573** («Note about formation», con
   secuencia) y **§602** («Note:» sobre las moras) de este capítulo.
2. **El tachado (~~) del Ākhyāta no aparece en el Kibbidhāna**: `grep
   '~~'` sobre la fuente del 7 da cero. El problema queda circunscrito
   al capítulo 6.
3. **Los desgloses de nombres propios sin traducir** (§525, §537, §552,
   §571-taddhita): Nandisena imprime «[The following are proper names]»
   y repite el pāḷi. Decidir si llevan nota del traductor.

## 6. SIGLAS Y FORMAS NUEVAS PARA EL REPERTORIO DEL EMPAREJADOR

Tabuladas en el §5 de cada tanda. Lo nuevo de este capítulo:
«Sārattha-Ṭīkā ii, 329» (nombre completo, §536, §554), «AbhA.», «SA.»,
«ApA.», «KhuA.» (también **sin volumen**: «KhuA. 109», «KhuA. 17»),
«MA.», «NdA.», «DA.», «VvA.», «UdA.», «ItA.», «AAA.», «AbhiA.» (en §613
**con doble página**: «i, 94, 295»), «Vism.», «J.» (frente al «JA.»
habitual), la vacilación «Abh./Abhi.», el volumen nuevo «Khu. xi»
(§606), la referencia sin volumen «Khu. 77» (§571; ¿«i» perdida? cotejar
con el PDF) y la referencia pospuesta al signo de interrogación (§562).
El regex del verificador ya las absorbe; `RE_SALTABLE` del emparejador
aún no.

## 7. TÉRMINOS PARA EL GLOSARIO

Cada tanda trae su §6. Ninguno está aún en `comun/glosario.md`. Lo que
conviene mirar junto:

- **El nombre del capítulo**: *kita/kitaka* = «derivado primario» (según
  su inglés) frente a «sufijos primarios» de la tarjeta del sitio.
- ***bhāva*** = «nombre de acción» aquí, frente a «impersonal» en el
  capítulo 6. No es contradicción sino cambio de referente (y el propio
  Nandisena cambia de «impersonal» a «verbal noun»). **Pide decisión
  única con nota.**
- Las **denominaciones**: *kicca*, *kit*, *tekālika*, *kārita* (con
  *vuddhi*), *nipātana*, *sādhana* (remitida a la entrada de la sesión
  26), *tassīla*, *garu* (correlato del *lahu* ya fijado).
- Las **fórmulas**: *ṭhāne* = «cuando corresponde», *sahādibyañjanena* =
  «junto con la consonante inicial», *yathākkamaṃ* = «respectivamente»
  (remitir a *yathāsaṅkhyaṃ*), *yathāgamaṃ* = «según la Palabra del
  Buddha» (¿o el literal?), *payoge sati*, *antalopo*, *viggaha* =
  «resolución».
- *samānakattuka*/*ekakattuka* (§561/§564): fijar si se distinguen.
- La serie **-āgama** suma *ikārāgama* y *yakārāgama* (§605–§606) a la
  entrada única propuesta en la sesión 26 §6.

## 8. DECISIONES QUE ESPERAN A ANGEL

El §8 de cada tanda las lista. Lo gordo, en orden de consecuencia:

1. **Las ocho erratas pāḷi** del §3 y las de formato.
2. **Los números anómalos** del §4 para `concordancia.json`.
3. **El estatuto del Uṇādi**: Pind y Thitzana lo tratan como **sexto
   kaṇḍa del Kibbidhāna**, no como capítulo aparte; Nandisena cierra
   aquí el kappa («Kita-kappo niṭṭhito»). Afecta al índice del sitio y a
   `CAPITULOS` cuando llegue el capítulo 8.
4. **«Bhāva» = «nombre de acción» / «impersonal»** (§7).
5. **El nombre público del capítulo** (§7).
6. **Las «Note» del cuerpo** (§5.1) — bloquean el montaje de los
   capítulos 6 y 7 por igual.
7. Los **viggahas de nombres propios** sin traducir (§5.3).
8. Las **siglas nuevas** del §6.
9. Dos observaciones de Pind por si merecen nota del traductor:
   «goghātako» como derivado de ‘ṇvu’ (§591) y «janitabbaṃ» como error
   antiguo por «jānitabbaṃ» (§605).

## 9. QUÉ NECESITA EL CHAT NUEVO

1. Leer este briefing y `comun/convenciones.md` §0, que es normativo.
2. **Las fuentes del capítulo 7 ya están en `docs/`**, con md5
   comprobado (§1). No hay que pedir nada.
3. **La revisión de las cinco tandas es de Angel** y se hará junta;
   hasta entonces no se montan capítulos ni se tocan los borradores.
4. Si lo que toca es **montar**, el orden es 5 → 6 → 7 (cada `CAPITULOS`
   necesita al anterior), y antes hay que resolver §5.1 (las «Note») y,
   para el 6, el tachado.
5. En las fuentes de cotejo, los tramos del capítulo 7 están
   localizados: Pind líneas 5795–6800; Thitzana líneas 22039–24430 (y
   2642–2822); la Rūpasiddhi entera en
   `docs/7- Kibbidhāna-Rūpasiddhi.md` (su Kibbidhāna acaba en la línea
   1290; siguen su Uṇādi y el nigamana).
6. **El capítulo 8 (Uṇādi, §624–§673) no tiene fuente** en `docs/`. Si
   Angel quiere seguir por ahí, pedirle la subida al chat y copiar con
   md5, como se hizo aquí. Y llegará con la decisión §8.3 pendiente.

## 10. RECORDATORIOS QUE NO CAMBIAN

Los del §10 del briefing 26, íntegros: nada de git desde el sandbox (ni
`status`); con Angel en inglés, **la respuesta entera, también los
bloques para copiar**; el producto en español; nada de calcos —
`comun/convenciones.md` §0; los PDF no viven en el repositorio; todo
cambio del emparejador corre contra los capítulos publicados;
`reconstrucción: OK` no dice que la negrita esté bien puesta; nada se
edita en `site/` salvo `pali.css`, `pali.js` y los SVG; lo de Thitzana se
señala como suyo y su flecha va al revés; ante duda, `<!-- DUDA -->`;
**proponer y verificar, nunca afirmar**; el briefing se escribe cuando ya
no se va a tocar nada más. Y uno nuevo de esta sesión: **para el
capítulo 7, las dos herramientas de verificación necesitan la fuente
como argumento explícito** — sus valores por defecto apuntan al 6.
