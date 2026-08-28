# Kaccāyana Pāḷi-Español: Briefing de la Sesión 32

*Complementa a los briefings 05–31. Tema único: **el solucionador publicado y
afinado en vivo con Angel** — el DPD de testigo, los casos y patrones
adjudicados, la regla de la clase vocálica — y **el mapa de lo que sigue**.*

> **Lo primero que tiene que saber el chat nuevo:** el solucionador está
> publicado en `/recursos/solucionador/` (v1.3) y se afinó con Angel
> adjudicando en vivo sobre SN 1.1 y DN 2. Todo confirmado en commits y
> **empujado por Angel** (verificar `git log origin/main..main` por si queda
> algo). Antes de tocar nada: leer este briefing, `nuestro/js/LEEME.txt` y
> los briefings 30–31. Las reglas de siempre: el Python es la referencia; los
> arneses mandan; nada se adjudica sin fuente; toda mejora se mide antes y
> después.

## 1. ESTADO AL CIERRE DE LA SESIÓN 31 (la conversación larga)

Los commits, en orden — cada uno con su porqué completo en el mensaje:

| Commit | Qué |
| --- | --- |
| `23c919e`…`161a52d` | Etapas 1–4 del porte (briefings 30 §6 y 31) |
| `3e2732c` | Tokenizador: la «ṁ» amputada; nacen los CASOS adjudicados |
| `4678602` | UNA lectura por sandhi; la ignorancia dicha en voz alta |
| `86f1d7b` | Lote 1 de adjudicación (250 formas) — **espera veredictos** |
| `4550498` | **El DPD vuelve de TESTIGO SILENCIOSO**: 633/698 y 6.642/7.178 |
| `0131d92` | Crédito: Miguel De Anquín y Bhikkhu Nandisena |
| `0bbf686` | Tarjeta; enlaces al corpus |
| `5112ef3` | **PATRONES adjudicados** (iti, api): base única atestiguada se afirma |
| `ec2eb05` | ceva = ca + eva (grado HABITUAL); la adjudicación asciende la señal |
| `358fcce` | **Regla de la clase vocálica**: hotīti sólo hoti + iti (v1.3) |

Números vigentes (modo solo-canon + `--dpd-filtro`, el de la página): banco
221/251 (88 %); corte 633/698 (90,7 %) y 6.642/7.178 (92,5 %); primera
lectura correcta en el 79 % de los acuerdos de prosa; «seguras» afirmadas en
los corpus de medida: 2.228 formas únicas. Cinco arneses: etapas 1–4 +
`arnes_casos.js` (8/8).

## 2. LAS TRES AUTORIDADES QUE AFIRMAN (y su gramática)

1. **El banco firmado** (reglas.json + Tablas).
2. **Los casos adjudicados** (`recursos/solucionador/casos-reportados.json`),
   con **grado**: *exclusivo* («hotīti es sólo hoti + iti») o *habitual*
   («ceva most of the time is ca eva» — decidir el pasaje pediría leer los
   Comentarios). Un caso no-sandhi APAGA la señal (navo).
3. **Los patrones adjudicados** (mismo archivo, `patrones`): cola enclítica
   con base única atestiguada; regla de la clase vocálica (la vocal ante «ti»
   conserva la clase de la final de la base); desempate breve/larga. El caso
   y el banco mandan sobre el patrón. Todo se atribuye en pantalla.

El DPD es **testigo silencioso** (decisión de Angel 2026-08-28, briefing 31
§5 bis 4; pendiente de confirmación del Venerable): filtro, ordenación,
señal; nunca análisis; atribuido en el pie de la página.

## 3. EL MAPA: QUÉ FALTA PARA QUE SEA AÚN MEJOR

En orden de rendimiento por esfuerzo, con el dueño de cada pieza:

1. **REFRESCAR LAS CIFRAS PUBLICADAS de la señal** *(Claude, una sesión
   corta)*. La página dice «46-56 %» pero eso se midió ANTES de los patrones
   y la regla de la clase vocálica; las «seguras» subieron de ~1.200 a 2.228
   formas únicas. Correr `medir_deteccion_canon.py` en el modo vigente y
   poner los números verdaderos — la honestidad también obliga cuando el
   número mejoró.
2. **Los veredictos del lote 1** *(Angel, un rato con lápiz)*.
   `docs/solucionador/por-adjudicar-lote-1.md`; ahora puede marcar además el
   grado (habitual/exclusivo) escribiéndolo en el veredicto — y generar el
   lote 2 filtrando lo que los patrones ya afirman
   (`generar_por_adjudicar.py` conviene que salte lo ya afirmado).
3. **Más reglas de patrón, firmadas en tanda** *(Angel decide, Claude
   prepara)*. Generar un informe de las familias que siguen en «no sabe»,
   agrupadas por segunda voz candidata (eva, iva, ahaṃ, api residual, ettha…)
   y ordenadas por masa en el canon, para que Angel firme las siguientes 3-5
   reglas de una sentada, como firmó la de «iti».
4. **Las junturas ENTRE palabras escritas** *(Claude, acotado)*. Portar
   `combinar()` y `juntura_declarada`: «vuttanayam eva», «catukkhattun ti»,
   el «ti» suelto. Hoy la página analiza voz por voz y esas junturas ni se
   miran. Es la mitad que falta de la detección en párrafo.
5. **`dpd-descomposiciones.tsv`** *(Angel, en su Mac)*. Bajar `dpd-mobile.db`
   y correr `nuestro/exportar_dpd.py` + `preparar_descomposiciones.py`. Con
   él, la capa de detección del DPD (71-79 % de recall) se vuelve medible en
   modo testigo — la mayor subida de recall disponible sin gramática nueva.
6. **La morfología de Kaccāyana como testigo** *(el salto estructural;
   empezable ya como experimento medido)*. Los 83 paradigmas de
   `/recursos/paradigmas/` permiten des-flexionar: una forma cuyas demás
   casillas del mismo paradigma están atestiguadas es VOZ FLEXIONADA, y esa
   es la señal que mata a los candidatos tipo sāvatthiyaṃ y encoge las
   listas por gramática, no por estadística. Con el capítulo 2 de Kaccāyana
   y Rūpasiddhi (y el Nyāsa) esto se vuelve doctrina del proyecto, no
   heurística. Es lo que Angel señaló: con lo que ya hay, esto ayuda mucho.
7. **El banco de pasajes adjudicados** *(conjunto)*. SN 1.1 y DN 2 ya están
   adjudicados de facto en esta conversación; convertirlos en corpus de
   prueba propio (formas + veredictos + arnés) empieza la ampliación del
   banco más allá de la Therīgāthā que el briefing 30 dejó pendiente — con
   fuente de verdad de Angel, no fabricada.
8. **El nivel del pasaje** *(futuro, del Venerable/Angel)*. Los casos
   habituales (ceva) sólo se deciden por ocurrencia leyendo los Comentarios.
   Cuando haya pasajes leídos, cabe una capa de contexto; sin eso, la página
   afirma lo habitual y muestra el resto — que es lo correcto hoy.
9. **Flecos**: la tarjeta del solucionador en la portada (ofrecido, sin
   respuesta); el rótulo «88 % del banco» (explicado; alternativa ofrecida,
   sin respuesta); el i18n del cromo (no existe en el sitio; briefing 31
   §5); la confirmación del Venerable sobre el DPD-testigo.

## 4. AVISOS AL CHAT NUEVO

- Los arneses tardan; el tope del sandbox son ~170 s por orden. Las
  referencias de señal y detección usan cachés reanudables
  (`SENAL_CACHE`, `DETECCION_CACHE` en `/tmp`). **Bustear la caché** cuando
  cambie la señal, no cuando sólo cambie la presentación.
- Cambió el motor → regenerar TODAS las referencias con `--dpd-filtro` y
  correr los cinco arneses. La etapa 1 va SIN DPD a propósito.
- La herramienta de escritura ha metido dos veces un byte NUL crudo por
  `\\u0000` en literales JS («binary file matches» lo delata).
- Los locks de git del sandbox (briefing 30 §1) se limpian con el permiso
  de borrado.
