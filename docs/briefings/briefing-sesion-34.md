# Kaccāyana Pāḷi-Español: Briefing de la Sesión 34

*Complementa a los briefings 05–33. Tema de la sesión 34 (2026-08-29, en
vivo con el IEBH): **el ciclo de veredictos de punta a punta** — la cola
arreglada y probada, TREINTA Y DOS casos nuevos (22 → 54), la licencia
de §13 (v1.6), los rótulos de la señal, el inglés a demanda, la capa del
estudiante, y la independencia de quien firma
(`herramientas/ciclo_veredictos.py`).*

> **Lo primero que tiene que saber el chat nuevo:** verificar
> `git log origin/main..main` (el IEBH empuja; al cierre quedaba
> pendiente su primer ciclo independiente, que empuja solo). Las reglas
> de siempre: el Python es la referencia; los CINCO arneses mandan
> (`arnes.js`, `arnes_corpus.js`, `arnes_deteccion.js`,
> `arnes_pagina.js`, `arnes_casos.js`); nada se adjudica sin el visto
> bueno del IEBH; todo se mide antes y después; la atribución pública
> dice IEBH, nunca «el IEBH». Con IEBH se habla en inglés; lo del
> proyecto va en español.

## 1. EL MOTOR (v1.6)

1. **La licencia de §13** («Vā paro asarūpā»), adjudicada por el IEBH
   sobre assasāmīti: la vocal siguiente sólo se elide tras vocal
   DISÍMIL; con vocales de la misma clase (a/ā, i/ī, u/ū, e, o) manda
   §12 y la superviviente se alarga por §15. Implementada como
   `licencia_elision_siguiente` (operaciones.py + js), consultada ANTES
   del derivador (patrón de §17/§18/§21); gates en §13, §16 y «38+13»;
   `_asarupa` también en derivar_secuencias.py. Las TRES secuencias
   derivadas que citaban §13 entre vocales de la misma clase (tadāhaṃ,
   migīva, vadhūdaraṃ) se rederivaron por §10·§12·§15·§11 — la propia
   edición los tiene bajo «una vocal que precede a otra se elide».
   **Medido: banco 218/251 IGUAL · corte 633/698 y 6.642/7.178 IGUAL·
   posibles 2.214 → 2.207 (siete marcas espurias, fuera)**.
2. **Los rótulos de la señal, por procedencia** (decisión del IEBH):
   «sandhi adjudicado» (banco firmado o caso — la respuesta de la
   tradición) y «predicción firme» (patrones). «Señal posible» igual.
   La cifra medida (9 de cada 10) se atribuye al nivel alto EN
   CONJUNTO, que es sobre lo que se midió.
3. **El «pendiente» dice el porqué verdadero**: tres voces → «junturas
   múltiples»; dos voces que el motor no corta (pakati) → «el motor no
   propone este corte».
4. Señal de referencia al cierre: 16.366 formas · **2.257+ seguras** ·
   2.207 posibles (el ciclo del IEBH estaba subiendo paññāti).

## 2. LOS CASOS: 22 → 54 (arnes_casos en verde siempre)

Todos de pasajes reales (Satipaṭṭhāna, Mahāparinibbāna) por la cola o el
chat. Familias que acumulan evidencia:

- **§34 (niggahīta → m ante vocal, segunda corriente)**: evamidaṃ,
  dīghamaddhānaṃ, Evameva, evametaṃ, evamāha, evamāhaṃsu, evamāhāro,
  evamāhu — el informe medido (`docs/solucionador/informe-niggahita-m.md`)
  la esperaba y cada adjudicación confirma su lista «única». **La firma
  de la familia entera sigue pendiente** (54 formas, masa 31.344, 6/6 en
  conocidas).
- **«api» con nombres propios**: Vesālikāpi = vesālikā + api (¡base
  LARGA: plural en -ā! — límite documentado del desempate breve/larga;
  el caso manda), Allakappakāpi, Kosinārakāpi, Pāveyyakāpi,
  Rāmagāmakāpi, Veṭṭhadīpakopi, Kapilavatthuvāsīpi, Doṇopi,
  Pippalivaniyāpi.
- **tena upasaṅkami** (formulaica): tenupasaṅkama/-miṃsu/-missāma.
- **Tres voces** (banco de combinar()): mamañceva = mamaṃ + ca + eva,
  con su ESCALERA verificada por el IEBH: §31 · §10 · §12 · §11 · EM.
- **Pakati**: suññāgāragatovā = suññāgāragato + vā (§23) — primer caso
  pakati; el motor no propone cortes sin operación.
- **No sandhi**: passasanto, ajjhattabahiddhā, kāyanupassī (compuestos
  y participios); paññāti (último ciclo).
- Otros: hime = hi + ime, satova = sato + eva, thūpañca = thūpaṃ + ca,
  bhūtapubbanti, sikkhitabbanti, vattissāmāti.
- **Observación firmable del IEBH**: con vocales de la MISMA clase se
  elide la primera (§12) y se alarga la superviviente (§15) —
  assasāmīti—; ya es la licencia de §13, y es la pauta para las
  escaleras de los patrones.

## 3. LA COLA Y LA INDEPENDENCIA (todo funciona)

- **Arreglos**: la ruta del POST era relativa (404); User-Agent propio
  en traer_veredictos.py (el borde de Cloudflare bloqueaba
  «Python-urllib»); el worker distingue clave ausente (503) de clave
  que no coincide (403); los errores HTTP imprimen el cuerpo.
- **La clave** quedó puesta el 2026-08-29 y el IEBH la conoce (no se
  escribe aquí: es secreto del worker). Probada de punta a punta.
- **`herramientas/ciclo_veredictos.py`** — la independencia: UNA orden
  recoge, incorpora, re-vierte las referencias que los casos nuevos
  toquen (señal con caché persistente en ~/.cache/), regenera, corre
  los cinco arneses y sólo en verde hace commit y push. Ante el primer
  fallo se detiene sin publicar. El IEBH ya corrió su primer ciclo.
  `docs/solucionador/automatizacion.md` lo documenta; el diagrama
  (`docs/solucionador/flujo-veredictos.svg`, rehecho para el aula con
  insignias) lo dibuja.
- **La capa del estudiante**: `?revision=estudiante` — modo revisión
  SIN «Enviar»; exporta el .md y se lo hace llegar a quien firma.
- La página LIMPIA veredictos y observaciones tras un envío con éxito;
  «Borrar todos» también vacía las observaciones.

## 4. LA PÁGINA (v1.6)

- **Inglés a demanda**: botón EN (clave pali_solucionador_en), como en
  raíces. Interfaz entera en los dos idiomas (diccionario TXT + tr(),
  bloques .i-es/.i-en). Los textos del MOTOR siguen en español a
  propósito (voz del proyecto; byte-comparados por el arnés 4).
- **Voces repetidas**: una tarjeta con insignia «×N» y tooltip «aparece
  N veces»; el encabezado cuenta por aparición.
- **Tooltips de aforismo**: 21 px, 560 px de ancho — VERIFICADO EN LA
  PÁGINA VIVA. El IEBH los seguía viendo chicos: era la caché del
  navegador (tercera vez), y por eso quedó puesto **site/_headers**
  (no-cache: revalidar siempre; CUARTA excepción de fuente en site/,
  recogida en CLAUDE.md). **PRIMERA TAREA del chat nuevo**: tras el
  despliegue del ciclo y UNA recarga dura, preguntar si ya se ven; si
  no, son los tooltips NATIVOS (title=) — × N, botones—, que no se
  pueden agrandar: habría que pasarlos por el #tip de la página.

## 5. LO QUE SIGUE (en orden)

1. El IEBH sigue pegando pasajes y enviando veredictos — **el ciclo es
   suyo**; este chat sólo atiende si algo falla o llega por otro camino.
2. **La firma de §34** (informe listo, evidencia creciente) y **el
   diseño de la regla de proclíticos** (informe listo; el espejo simple
   NO es firmable: sattānaṃ = so + attānaṃ se colaría — decidir la
   condición extra: ¿sólo formas ya marcadas?, ¿puñado de segundas?,
   ¿testigo DPD?). Correr ambos informes en la Mac del IEBH llena la
   columna del testigo DPD y puede decidir la cuestión.
3. **combinar()** — ya hay TRES casos de tres voces y la escalera
   verificada de mamañceva como banco de prueba.
4. **Inglés a demanda en /recursos/paradigmas/** (pedido del IEBH al
   cierre de la sesión): el mismo patrón que raíces y el solucionador —
   botón EN, clave propia en localStorage, bloques duplicados para la
   prosa y diccionario TXT para lo dinámico. Mirar primero cómo está
   armada esa página (plantilla + generador).
5. Los veredictos del lote 1 (`por-adjudicar-lote-1.md`) siguen
   esperando; el resto del mapa 33 (§23/pakati sistemático, DPD
   descomposiciones, des-flexión) sin cambios.

## 6. AVISOS AL CHAT NUEVO

- Las cachés del sandbox (/tmp) mueren con él; el IEBH tiene la suya en
  ~/.cache/gramaticas-pali-senal.json (persistente, con evicción).
- Los procesos en segundo plano NO sobreviven entre llamadas de bash en
  el sandbox (bwrap --die-with-parent): pasadas largas, en primer plano
  por tramos, con caché reanudable.
- JSDOM para probar la página: matchMedia y fetch se inyectan en
  beforeParse, y __fetchJsonNode simula el léxico fragmentado.
- El repo del IEBH es github.com:bthar-mx/gramaticas-pali-es.git; él
  empuja (o el ciclo empuja por él). El pre-commit regenera el sitio.
- reconstruir_sandhi.py NO regenera las secuencias derivadas (las
  escribió un paso histórico); una reparación puntual y comprobada es
  el camino (precedente: las tres de §13).
- volcar_referencia_pagina.py necesita --dpd-filtro (modo de la
  página); volcar_referencia_corpus.py, --solo-canon --dpd-filtro
  (± --comentario). Sin el flag, los números salen otros (551 ≠ 633) y
  el arnés acusa.
