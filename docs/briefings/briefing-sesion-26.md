# Kaccāyana Pāḷi-Español: Briefing de la Sesión 26

*Complementa a los briefings 05–25. Tema único: **el capítulo 6, Ākhyāta,
traducido entero en borrador** (§406–§523, seis tandas). No se tocó el
emparejador ni ningún capítulo publicado.*

> **Lo primero que tiene que saber el chat nuevo:** el Ākhyāta está
> traducido en borrador completo —los 118 suttas— y espera la revisión de
> IEBH. El capítulo 5 (Taddhita) sigue esperando la suya, en su propio
> chat. Ninguno de los dos está montado.

---

## 1. ESTADO AL CIERRE

HEAD: **`c13a1ec4`** («taddhita: fuentes del capítulo 5 y borradores de
la sesión 25 (§344–§405); briefing de la sesión»), publicado en
`origin/main`. Comprobado sin ejecutar git, leyendo
`.git/refs/heads/main` y `.git/logs/HEAD` como texto. Con ese commit
quedaron confirmados los cinco archivos que el briefing 25 §1 daba como
pendientes.

**Once archivos nuevos sin confirmar**, todos de esta sesión:

| Archivo | Qué es |
| --- | --- |
| `docs/6 - Ākhyāta-Kaccāyana.md` | Fuente Nandisena, cap. 6. Subida del IEBH al chat; **md5 `5c528464…aee85`, idéntico** al original |
| `docs/6. Ākhyāta-Rūpasiddhi.md` | Rūpasiddhi cap. 6, para cotejo. **md5 `3667daec…64fbe`, idéntico** |
| `docs/borradores/sesion-26-suttas-406-431.md` | Tanda 1 — primera sección entera |
| `docs/borradores/sesion-26-suttas-432-444.md` | Tanda 2 — segunda sección, primera mitad |
| `docs/borradores/sesion-26-suttas-445-457.md` | Tanda 3 — segunda sección, segunda mitad |
| `docs/borradores/sesion-26-suttas-458-481.md` | Tanda 4 — tercera sección entera |
| `docs/borradores/sesion-26-suttas-482-502.md` | Tanda 5 — cuarta sección, primera mitad |
| `docs/borradores/sesion-26-suttas-503-523.md` | Tanda 6 — cuarta sección, segunda mitad, cierre del capítulo |
| `herramientas/verificar_borrador.py` | Verificación mecánica de párrafos pāḷi, en los dos sentidos |
| `herramientas/verificar_estructura.py` | Numeración triple, números del Saddanīti y llamadas de nota |
| `docs/briefings/briefing-sesion-26.md` | Este archivo |

Confirmarlos y publicarlos corresponde al IEBH.

## 2. EL ĀKHYĀTA, TRADUCIDO EN BORRADOR

118 suttas (§406–§523), cuatro kaṇḍas, 71 notas al pie de Nandisena.
Tandas de 26/13/13/24/21/21 **cortadas por las fronteras de kaṇḍa**, de
modo que ninguna fórmula de cierre quedara huérfana y el bloque de los
vikaraṇa (§433–§439) no se partiera. Formato idéntico a los borradores
de la sesión 25.

**Los dos desfases de numeración, comprobados en los 118 suttas:**

- **Pind = Nandisena + 2**, verificado en los dos extremos de cada tanda,
  en los cuatro cierres de kaṇḍa y en las remisiones internas del propio
  Pind (su «[Kacc 455]» donde Nandisena dice §453).
- **Thitzana usa la numeración de Nandisena**, sin desfase. Su Ākhyāta
  empieza en la línea 18725 de `Kaccāyana Volume 2` y termina hacia la
  22030.

**La verificación mecánica, que es lo reutilizable.** Se hizo en los dos
sentidos y se guardó como herramienta:

    python3 herramientas/verificar_borrador.py <borrador.md> <línea_ini> <línea_fin>
    python3 herramientas/verificar_estructura.py <borrador.md> <ini> <fin> <§desde> <§hasta>

**411 párrafos pāḷi comprobados, 411 reproducidos, 0 no encontrados**, y
0 párrafos pāḷi de la fuente ausentes de los borradores. Además, los
**92 pasos de las secuencias de formación** de §433 y §445–§452 se
cotejaron uno a uno, también en los dos sentidos: 92 de 92.

**La verificación cazó un error real:** en la cuarta tanda faltaba el
«Vā ti kimatthaṃ? Ṭhāti» de §468, que estaba en la fuente y se había
perdido al traducir su respuesta. Es la razón de que exista. Dos avisos
más resultaron ser normalizaciones deliberadas y documentadas (§491,
palabras pegadas en la fuente; §513, punto sobrante al retirar la
referencia); el verificador ahora las distingue y las informa aparte en
lugar de darlas por fallo.

## 3. LAS ERRATAS PROPUESTAS

Nueve de lectura pāḷi, todas con al menos dos fuentes independientes
contra Nandisena. **Ninguna se corrigió en el cuerpo**: el borrador
conserva la lectura literal y la propuesta está en las NOTAS DE TRABAJO
de cada tanda.

| Sutta | Imprime | Propuesta | Quién le lleva la contraria |
| --- | --- | --- | --- |
| §420, vutti | māyogā | māyoge | Pind, Rūpasiddhi y su propio título |
| §429, vutti | ssasa ssatha | ssasi ssatha | Pind, Rūpasiddhi y su propio título |
| §431, kvattho | asabbadhātumhi | asabbadhātukamhi | Pind, Rūpasiddhi y su propio inglés |
| §434, ejemplo | bubbhukkhati | bubhukkhati | Pind, Thitzana **y él mismo cuatro veces** en §458, §461, §465 y §473 |
| §438, vutti | bruvīti | bravīti | Pind, y las otras dos apariciones del mismo giro en su propio texto |
| §453, ejemplo | labhante | labbhante | Pind, Thitzana y su propio inglés |
| **§470, título y vutti** | **Ṇāssa / Ṇā** | **Ñāssa / Ñā** | Pind, Thitzana y su propio inglés |
| **§509, vutti** | **Ṇā** | **Ñā** | Pind y su propio inglés |
| §483, vutti | kāriye | kārite | Pind, Thitzana y su propio título |
| §519, vutti | ākārāgamo | akārāgamo | Pind, Thitzana y su propio título |

**Las de §470 y §509 son las de mayor alcance**: son las dos únicas
apariciones de «Ṇā» en el capítulo y las dos dejan el sutta sin raíz a
la que referirse (la raíz es *ñā*, la de *jānāti*).

**Y una que no es de letra sino de número:** §432 lleva **462** como
número de la Rūpasiddhi, y debe ser **362**. La Rūpasiddhi §462 es
«Pubbo ’bbhāso»; su §362 sí es «Dhātu-liṅgehi parā paccayā (905)»,
y está en `docs/5. Taddhita-Rūpasiddhi.md`, línea 19. Thitzana imprime
«432, 362». **Es la única errata del capítulo que obliga a tocar
`comun/concordancia.json`.**

Aparte, unas cuarenta erratas **sólo del inglés** (tipos, glosas
cruzadas, formas pāḷi perdidas entre paréntesis), tabuladas tanda por
tanda. Y un hallazgo curioso: **§408 tiene un fragmento en español
dentro del inglés de Nandisena** —«Pero en "attanopada"»—, marca de su
proceso de trabajo.

## 4. CUATRO PASAJES QUE EL KACCĀYANA-VAṆṆANĀ DECLARA AJENOS AL TEXTO ANTIGUO

Nandisena los imprime en el cuerpo; Pind los relega a aparato en los
cuatro casos, con la misma justificación: los añaden Be, Ce y Ee;
proceden de la Rūpasiddhi o del Ṭīkābyākhyāna; y el Kaccāyana-niddesa o
la Kaccāyana-vaṇṇanā dicen expresamente que no están en el Kaccāyana
antiguo ni los comenta el Nyāsa.

| Sutta | Pasaje |
| --- | --- |
| §438 | «Atthaggahaṇena alapaccayo hoti. Jotalati.» |
| §439 | «Caggahaṇena āra āla icc’ ete paccayā honti…» |
| §446 | «Caggahaṇena i ī e o icc’ ete paccayā honti…» |
| §491 | «Kāsattam iti bhāvaniddesena aññatthā pi sāgamo hoti…» |

**Piden una decisión única**, no cuatro: aviso al lector o silencio. Pind
añade sobre el de §446 una observación datable: la interpolación tuvo
que hacerse entre la Rūpasiddhi y la Saddanīti, porque Sadd §927 ya la
presupone.

## 5. DOS COSAS QUE EL GENERADOR NO SABE HACER

Salieron de este capítulo y no existían en los anteriores:

1. **El tachado de las secuencias de formación.** Nandisena marca la
   letra elidida con tachado —«pac~~a~~», «div~~y~~a»—. `grep '~~'`
   sobre `kaccayana/*.md` da cero y `generar_capitulo.py` no lo trata.
   Doce secuencias lo usan. Hay que enseñárselo al generador o
   convertirlo a la notación del Sandhi, que separa la letra en vez de
   tacharla.
2. **Las «Note» que Nandisena imprime en el cuerpo** (§472 y §473). No
   son notas al pie ni tienen equivalente pāḷi: son párrafos suyos como
   traductor, sin llamada, dentro del texto inglés. El formato no las
   prevé.

## 6. TÉRMINOS PARA EL GLOSARIO

Cada tanda trae su §6 de propuestas. **Ninguna está aún en
`comun/glosario.md`**: entran cuando IEBH las apruebe. Lo que conviene
mirar junto:

- **Tres términos reutilizados con otro referente**, que el lector que
  venga del Nāma o del Kāraka va a confundir: *pañcamī* y *sattamī* (aquí
  tiempos verbales, allí inflexiones nominales quinta y séptima),
  *liṅga* (aquí tema nominal, allí género) y *kamma* (aquí voz pasiva,
  allí acusativo). Los tres piden nota del traductor.
- **La serie ‑āgama, seis casos en cuatro tandas**: *ivaṇṇāgama* (§442),
  *niggahitāgama* (§446), *sāgama* (§491), *ikārāgama* (§516),
  *akārāgama* (§519), *īkārāgama* (§520). Piden una entrada con las
  variantes debajo.
- ***niccaṃ*** (§481) cierra la escala de `terminologia-particulas.md`,
  que ya recoge *kvaci*, *vā*, *navā* y *vibhāsā* y no tiene el extremo
  obligatorio.
- Los **ocho nombres de gaṇa de raíces** (*bhūvādi*, *rudhādi*,
  *divādi*, *svādi*, *kiyādi*, *gahādi*, *tanādi*, *curādi*) y los
  **ocho nombres de tiempo**, que se dejaron sin traducir.
- *abbhāsa*, *vikaraṇa*, *kārita*, *paribhāsa*, *yogavibhāga*,
  *sādhana*, *dhātvanta*, *tulyādhikaraṇa* (ya fijado en la sesión 13).

## 7. DECISIONES QUE ESPERAN A ANGEL

El §8 de cada tanda las lista. Lo gordo, en orden de consecuencia:

1. **Las diez erratas pāḷi** del §3, y en especial las dos «Ṇā» → «Ñā».
2. **El número de la Rūpasiddhi de §432** (462 → 362), que va a
   `concordancia.json`.
3. **Los cuatro pasajes interpolados** del §4: aviso o silencio.
4. **El tachado de las secuencias** y las «Note» del cuerpo (§5).
5. Dejar sin traducir los nombres de las **tres personas** y de los
   **ocho tiempos**, con la equivalencia dada una sola vez en §408.
   **Ojo:** la nota 64 de §507 sí los glosa —«vattamānā (present)»,
   «sattamī (potential)»…—, que es el único sitio donde Nandisena lo
   hace, y puede reabrir la cuestión.
6. El kvattho de §427, que su inglés no traduce aunque su pāḷi lo trae.
7. §413 y §523 **no tienen número del Saddanīti**, y no es omisión: Pind
   tampoco se lo da. Para `concordancia.json`, van sin tercer número.
8. **Siglas nuevas para el repertorio del emparejador:** «JA.», «VinA.»,
   «SnA.», «DAA.», y las formas anómalas «Vin.A.» con punto interior
   (§499), «M.i,» sin espacio (§483), la doble página «M. i, 141, 143»
   (§470) y **la referencia incrustada en mitad del ejemplo de §496**
   («Ko nu tvam asi (S. i, 104) mārisa?»). `RE_SALTABLE` no reconocería
   ninguna.
9. La discrepancia de las notas 61–62 con §450 sobre si ‘ppa’ y ‘ṇhā’
   son del gaṇa *kiyādi* o del *gahādi*. **No es errata**: Kaccāyana y
   la Rūpasiddhi dividen los gaṇas de distinta manera, y las notas siguen
   a la Rūpasiddhi mientras el sutta sigue a Kaccāyana. Merece nota.

## 8. LO QUE SIGUE ABIERTO

Todo el §5 del briefing 25 sigue vigente, sin cambios: §70 y §92 de la
negrita, las 32 ausentes y 18 ambiguas del Nāma, las tres citas
canónicas, las 2379 desinencias de paradigmas, el Nyāsa sin constar en
`CLAUDE.md`, las referencias bibliográficas del Nāma nunca restituidas,
el permiso de la marca, la descripción de Zenodo, `docs/1.
Sandhi-Kappa.md`. Y el emparejador sigue **aprobado y no implementado**
(briefing 25 §4), con las dos observaciones de contabilidad que allí se
anotaron.

**La revisión del capítulo 5 no es asunto de esta sesión ni de la
siguiente:** sigue en el chat de la sesión 25.

## 9. QUÉ NECESITA EL CHAT NUEVO

1. Leer este briefing y `comun/convenciones.md` §0, que es normativo.
2. **Las fuentes del capítulo 6 ya están en `docs/`**, con md5
   comprobado. No hay que pedir nada.
3. **El capítulo 7 (Kibbidhāna) no tiene fuente** ni en `docs/` ni en el
   proyecto de claude.ai —sólo el comentario,
   `docs/fuentes/nyasa/Nyasa-07-kibbidhana.md`—. Si IEBH quiere
   seguir por ahí, hay que pedirle la subida al chat, que es el canal
   byte a byte, y copiarla con md5 como se hizo aquí.
4. Si lo que toca es **montar** el capítulo 6, el paso «Capítulo nuevo:
   qué hace falta» de `CLAUDE.md` está entero por delante, con los dos
   añadidos del §5 de este briefing. Y **depende de que el capítulo 5 se
   monte antes**, porque el «anterior» del 6 en `CAPITULOS` es él.
5. En Thitzana y Pind, los tramos de este capítulo están localizados:
   Thitzana desde la línea 18725, Pind desde la 4863.

## 10. RECORDATORIOS QUE NO CAMBIAN

Los del §7 del briefing 25, íntegros: nada de git desde el sandbox (ni
`status`); con IEBH en inglés, **la respuesta entera, también los
bloques para copiar**; el producto en español; nada de calcos
(«commitear», «empujado») — `comun/convenciones.md` §0; los PDF no viven
en el repositorio; todo cambio del emparejador corre contra los dos
capítulos; `reconstrucción: OK` no dice que la negrita esté bien puesta;
nada se edita en `site/` salvo `pali.css`, `pali.js` y los SVG; lo de
Thitzana se señala como suyo y su flecha va al revés; ante duda,
`<!-- DUDA -->`; **proponer y verificar, nunca afirmar**; el briefing se
escribe cuando ya no se va a tocar nada más.
