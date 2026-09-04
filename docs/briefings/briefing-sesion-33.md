# Kaccāyana Pāḷi-Español: Briefing de la Sesión 33

*Complementa a los briefings 05–32. Tema de la sesión 32 (larguísima, en
vivo con el IEBH): **el solucionador v1.5** — cifras remedidas y
verdaderas, el resguardo de la base residual, el patrón de «ca», la regla
de los absolutivos, el MODO REVISIÓN con su cola automatizada, y una
tanda grande de casos adjudicados sobre pasajes reales.*

> **Lo primero que tiene que saber el chat nuevo:** todo lo de la sesión
> 32 está commiteado; verificar `git log origin/main..main` por si queda
> algo sin empujar. Las reglas de siempre: el Python es la referencia; los
> CINCO arneses mandan (`arnes.js`, `arnes_corpus.js`, `arnes_deteccion.js`,
> `arnes_pagina.js`, `arnes_casos.js`); nada se adjudica sin el visto bueno
> del IEBH; todo se mide antes y después. La atribución pública dice
> **IEBH**, nunca «el IEBH» (pedido del 2026-08-28; los briefings y el git
> conservan la procedencia interna).

## 1. EL MOTOR, AL CIERRE (v1.5)

1. **El resguardo de la base residual** (firmado): una base candidata de
   un patrón debe ser AL MENOS tan frecuente en el canon como la forma
   entera; ni concede ni bloquea la unicidad. Corrigió el defecto por el
   que «ho» (4 apariciones) afirmaba hoti (59.320) como ho + iti — y
   pajānāti, bhaṇati, vadati, karoti…
2. **Tres patrones**: «iti» (con clase vocálica y desempate breve/larga),
   «api», y «ca» (niggahīta §31: tañca, evañca, yañca…, firmado tras el
   informe de familias).
3. **Primera regla negativa** (`no_sandhi` en casos-reportados.json):
   los absolutivos en **-tvā/-tvāna** nunca se señalan
   (`_silenciar_no_sandhi` / `silenciarNoSandhi`, ANTES del caso: el caso
   manda). Quitó ~140 marcas falsas de la prosa sin perder un solo sandhi.
4. **22 casos adjudicados** (arnes_casos 22/22). Nuevos de la sesión 32:
   pajānāti (no), vedanānañca, maggañca, cetā = ca + etā (¡proclítico!),
   phusitva (no; la fuente pegada traía la ā comida), passanto (no),
   idamavoca, idamavocaṃ, idamavocuṃ, **idamavocāyasmā e idamavocanti
   (TRES voces)**, yenāyasmā = yena + āyasmā, dūratova = dūrato + eva
   (confirmado a pregunta expresa), coraṃ (no).
5. **Casos de tres voces**: `_aplicar_caso`/`aplicarCaso` insertan la
   lectura adjudicada PRIMERA, sintética, marcada «pendiente de
   derivación» cuando el motor (de un solo corte) no la produce. Son los
   dos primeros bancos de prueba de `combinar()` (mapa 32 punto 4).

**Cifras vigentes y PUBLICADAS** (modo solo-canon + dpd-filtro): recall
47 % verso · 57 % prosa; «seguro» acierta juntura real 90 % / 95 % («9 de
cada 10» en la página, y es verdad). Señal de referencia: 16.366 formas ·
**2.253 seguras · 2.215 posibles**. Corte 633/698 y 6.642/7.178; banco
218/251 sin DPD (221 con testigo, el número de la página).

## 2. EL MODO REVISIÓN Y LA COLA (nuevo, todo funciona)

- La página con `?revision` (o #revision) muestra el botón ✎; el navegador
  lo recuerda. Es discreción, no candado: el candado es la incorporación
  y la firma.
- Cada tarjeta: ✓ primera lectura / ✗ no es sandhi / otra lectura
  (componentes con «+» O con espacios), más campo de **explicación** que
  viaja con el veredicto. Campo aparte «**sandhi no detectado**»:
  `voz = componentes`, o `voz = no` (también «is not sandhi»); sirve para
  voces fuera del pasaje. Cuadro de **observaciones generales** (de una
  observación así salió la regla de -tvā/-tvāna). Con señal segura la
  tarjeta muestra SÓLO la lectura afirmada (ni «candidatos», ni cuenta,
  ni pliegue). Encabezado: «X sandhis encontrados en Y voces…».
- **Enviar al proyecto** → POST a `/api/veredictos` (worker/index.js +
  KV `VEREDICTOS`, **activo**: id en wrangler.jsonc, clave de lectura en
  el secreto `CLAVE_VEREDICTOS` que sólo el IEBH conoce). Exportar .md es
  el camino manual/repuesto (formato EXACTO de los lotes).
- En la Mac: `VEREDICTOS_CLAVE=… python3 herramientas/traer_veredictos.py`
  (guarda en docs/solucionador/veredictos-recibidos/, incorpora, vacía lo
  incorporado; `--solo-mirar` lista). Después SIEMPRE: generar página,
  arneses, y referencias/medición si la señal cambió. Detalles:
  `docs/solucionador/automatizacion.md`. La automatización COMPLETA
  (veredicto → caso publicado sin Mac) quedó aplazada: pediría CI con los
  cinco arneses; decidir sólo si el uso lo pide.

## 3. LO QUE SIGUE (en orden de valor)

1. **Reglas candidatas detectadas por los casos de hoy, para firmar con
   medición previa**:
   - la familia **§34 con segunda voz corriente** (idamavoca, kimahaṃ =
     kiṃ + ahaṃ…): niggahīta → m ante vocal; hoy sólo la ven los casos;
   - la **regla de primera voz** (proclíticos: cetā = ca + etā, cāyaṃ,
     cassa, cidaṃ… y las gemelas con na-, sv-, yv-): NO existe mecanismo
     de patrón por primera voz; diseñarlo pide firma;
   - las siguientes familias del informe (`docs/solucionador/
     familias-no-sabe.md`, regenerado post-firma): eva (masa 49.484, 43/47
     multi-base — pide grados habituales tipo ceva), iva, atthi (natthi)…
2. **`combinar()` / junturas múltiples** (mapa 32 punto 4): ya hay dos
   casos de tres voces adjudicados como banco de prueba.
3. **Los veredictos del lote 1** siguen esperando
   (`docs/solucionador/por-adjudicar-lote-1.md`) — ahora también pueden
   llegar por la cola.
4. `dpd-descomposiciones.tsv` (Mac del IEBH) y la des-flexión por
   paradigmas (mapa 32 puntos 5–6): sin cambios.
5. **Flecos**: el aviso cosmético «consultas a fragmentos no precargados»
   sale de iniciar() (componentes del banco antes de cargar l/ṭ; arreglo:
   precargar esas letras); ofrecer `_headers` para que el HTML revalide
   siempre (el IEBH sufrió una caché vieja del navegador; ofrecido, sin
   decisión); la tarjeta del solucionador en la portada y el rótulo
   «88 %» (briefing 32 §3.9, sin respuesta).

## 4. AVISOS AL CHAT NUEVO

- Las cachés de /tmp (SENAL_CACHE, DETECCION_CACHE, FAMILIAS_CACHE)
  murieron con el sandbox: primeras corridas lentas, reanudables. Bustear
  sólo cuando cambie la señal; con cambios puntuales basta EVICT de las
  formas afectadas.
- Para probar la página sin navegador: `npm install jsdom` en /tmp y
  evaluar site/…/index.html con JSDOM (runScripts) + fetch simulado; el
  «matchMedia is not defined» es de jsdom, no de la página. La página
  también se prueba en vivo con el navegador integrado.
- `.wrangler/` está en .gitignore (la caché de wrangler coló una vez el
  id de cuenta; limpiado el mismo día).
- Tooltips de aforismo: agrandados en /recursos/sandhi/ Y traídos al
  solucionador (DATA.suttas, extraídos por generar_sandhi.py — una sola
  fuente). Los avisos «secuencias sospechosas» de generar_sandhi.py son
  los de siempre (13 pakati de paso único, documentados).
- El byte NUL y el resto de avisos del briefing 32 §4 siguen vigentes.
