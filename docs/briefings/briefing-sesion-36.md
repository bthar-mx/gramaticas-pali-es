# Kaccāyana Pāḷi-Español: Briefing de la Sesión 36

*Complementa a los briefings 05–35. Tema de la sesión 36 (2026-08-30, en
vivo con Angel): **la ṁ pegada se corrige a ṃ; el globo de cada marca; el
filete esmeralda; las observaciones del revisor ya no se pierden (v1.10);
y §34 implementado dentro del RÉGIMEN MEDIDO, que es el hallazgo de la
sesión.** Página en v1.11.*

> **Lo primero que tiene que saber el chat nuevo:** verificar
> `git log origin/main..main` (al cierre quedaban CUATRO commits sin
> empujar: v1.9, v1.10, §34 y el gitignore del DPD). Las reglas de
> siempre: el Python es la referencia; los CINCO arneses mandan; nada se
> adjudica sin el visto bueno del IEBH; todo se mide antes y después; la
> atribución pública dice IEBH. Con Angel se habla en inglés; lo del
> proyecto va en español.

## 0. LA CLAVE, TODAVÍA

**Sigue pendiente del briefing 35 §0.** La clave de la cola se escribió en
un chat el 2026-08-29 y al cierre de ESTA sesión tampoco consta rotada.
Es `npx wrangler secret put CLAVE_VEREDICTOS` en la máquina con la sesión
de wrangler, con un valor nuevo que no se escriba en ninguna parte; el
que corre el ciclo pasa a usar el valor nuevo en `VEREDICTOS_CLAVE=…`.
Preguntarlo al abrir, otra vez.

## 1. v1.9 — LA ṁ PEGADA, EL GLOBO DE CADA MARCA, EL FILETE ESMERALDA

Tres pedidos del IEBH, el mismo día:

- **Los pasajes copiados de su lector (buddha-dhamma.net/reader) llegan
  con «ṁ» de punto arriba (U+1E41) aunque el lector muestre «ṃ».** El
  motor ya las identificaba (`cotejo()`); lo que quedaba mal era el texto
  VISIBLE. Ahora la caja se normaliza al pegar y al analizar
  (`normalizarNiggahita`: NFC + ṁ→ṃ + Ṁ→Ṃ), y `CASO_POR_FORMA` usa
  `claveForma` (minúscula + ṁ→ṃ) para que la escalera del IEBH aparezca
  aunque el caso esté guardado con la ṁ con que se pegó (Ekamidāhaṁ,
  khvāhaṁ…).
- **Cada voz marcada del pasaje dice en su globo qué sandhi es** sin
  abrir la tarjeta (`tipMarca`): con señal segura, componentes y rótulo
  —el mismo de la tarjeta, por la misma procedencia—; con posible, la
  cuenta de lecturas SIN elegir ninguna. El globo no asciende nada, como
  «Copiar».
- **El filete de la predicción firme estrena color propio:**
  `--marakata` (esmeralda, #2F6B4A claro / #8FCCA8 oscuro), distinto del
  índigo de lo adjudicado — no sólo más fino. El grueso/fino se conserva
  para no depender del color.

El botón «volver al inicio» que se pidió **ya estaba** (desde v1.7, igual
que en raíces y paradigmas: aparece al pasar de 600 px de scroll); lo que
lo escondía era la caché vieja.

## 2. v1.10 — LAS OBSERVACIONES YA NO SE PIERDEN (era lo urgente del 35)

- **Campo de ESCALERA por voz en el modo revisión** (briefing 35 §6
  quater, opción b): un paso por línea, con su §N. Se guarda al escribir
  SIN re-pintar (re-pintar en cada tecla robaría el foco del área) y
  viaja en el .md como bloque `ESCALERA:` sangrado tras el `VEREDICTO:`.
- **`incorporar_adjudicaciones.py` se rehizo por bloques.** Procesar
  línea a línea era exactamente lo que tiraba la NOTA y la ESCALERA, que
  vienen DESPUÉS del veredicto. Ahora recoge las dos: nota → `nota`
  («Nota del revisor (verbatim): …»), escalera → `escalera_iebh` +
  `escalera_fuente`, rotuladas como del revisor.
- **A un caso YA adjudicado se le AÑADEN escalera y nota si le faltan y
  su veredicto coincide** (cotejo de componentes); si difiere, aviso y
  nada se toca; el veredicto nunca se reescribe. Escalera sin veredicto:
  aviso, no se incorpora sola.
- **Las observaciones generales siguen siendo prosa** y no se vuelven
  datos, pero el incorporador las imprime ENTERAS con un aviso en el
  ciclo: ya no pueden pasar calladas. El placeholder del cuadro dice
  ahora que los datos de UNA voz van en los campos de su tarjeta.
- Probado con lote sintético (los cinco casos raros) y con el circuito
  página→.md en JSDOM. `docs/solucionador/automatizacion.md` al día.

**Decirle al IEBH**: sus escaleras van ahora en el campo de la tarjeta,
no en el cuadro de observaciones — así se incorporan solas.

## 3. §34 IMPLEMENTADO — Y EL RÉGIMEN MEDIDO, QUE ES LA LECCIÓN

La firma era del 2026-08-29 (briefing 35 §6); el mecanismo es de hoy.

- **Clase de patrón nueva** en `casos-reportados.json` (`"clase":
  "niggahita_m"`, con la cita de la firma): los tres patrones vigentes se
  declaran por la SEGUNDA voz; aquí la clase la identifica la «m» de la
  juntura y la licencia es la unicidad de la LECTURA de la clase.
  `_patron_niggahita_m` (Python) / `patronNiggahitaM` (JS), receta
  exactamente la del informe: superficie = base[:-1]+«m»+segunda,
  resguardo por los DOS lados (piso = max(frec(forma), 1)), gemelas de
  vocal inicial → la BREVE, unicidad o silencio.
- **EL HALLAZGO: la receta, aplicada SIN tope, afirmaba en falso fuera
  del alcance de la medición.** El informe midió las 5.000 formas más
  frecuentes; en el corpus de referencia entero (16.366) salían **385**
  afirmaciones, y entre ellas jātimaraṇā (frec 3) como «jātiṃ + araṇā»
  —siendo el compuesto jāti+maraṇa— y vedhamānehi (7) como «vedhaṃ +
  ānehi» —siendo el participio vedhamāna—. Con la forma rara, el piso de
  las candidatas cae y el resguardo se debilita: un régimen que la
  medición nunca cubrió.
- **Decisión de Angel (2026-08-30): el patrón lleva `frec_minima` =
  159** —la frecuencia del puesto 5.000, hasta donde llegó el informe— y
  fuera de ese régimen calla. Quedan **25** afirmaciones (18 antes mudas,
  7 antes posibles), cero falsas conocidas. **El precio:** formas
  correctas bajo el piso también callan (ekamante, 133; tvamasi, 94).
  **Ampliar la licencia es del IEBH** — enseñarle los dos ejemplos
  falsos y el piso.
- **Medido, antes → después** (referencia de señal, 16.366 formas):
  segura 2.266 → **2.291** (+25) · posible 2.197 → **2.190** (−7).
  Banco y página: byte-idénticos (el banco manda sobre el patrón).
  Referencias re-vertidas (señal, corpus ×2, página, banco); CINCO
  arneses en verde con paridad Python/JS en todas las formas.
- La familia de `etadavocuṁ` (briefing 35 §6 quater) queda cubierta por
  el patrón — dentro del régimen.

## 4. EL TESTIGO DEL DPD — a medias, con el camino despejado

- `recursos/lexico/dpd-descomposiciones.tsv` está **gitignorado** (commit
  `cd346c6`), como los PDF: no viaja con el repositorio, y la línea evita
  además que el `git add -A` del ciclo lo cuele en un commit de la cola.
- **El arenal no puede bajar el archivo**: el proxy deja github.com (las
  páginas) pero bloquea los hosts de descarga (release-assets, raw,
  codeload, api). Se le pidió a Angel bajar
  `dpd-mobile-db.zip` (200 MB, release v0.4.20260728, sha256
  `9ce57d36…`) y dejarlo en la carpeta.
- **Cuando esté:** verificar sha256 → extraer en /tmp →
  `python3 nuestro/exportar_dpd.py <dpd-mobile.db>` →
  `python3 nuestro/preparar_descomposiciones.py` → queda sólo el tsv
  final en `recursos/lexico/`. Después: re-correr los dos informes (la
  columna del testigo se llena) y montar el criterio de categoría
  gramatical del IEBH para los proclíticos (briefing 35 §6: «si el
  diccionario da la forma entera como palabra con su categoría, no es
  sandhi proclítico» — para eso está `dpd-pos.tsv`, que exporta el mismo
  guion).

## 5. AVISOS AL CHAT NUEVO

- **El ciclo YA se negó una vez con razón**: Angel lo corrió con el §34 a
  medias en el árbol y el ciclo se detuvo («El árbol tiene cambios sin
  commit»). Es la conducta correcta; no «arreglarla». Coordinarse: nada
  a medias en el árbol cuando él corre el ciclo.
- **Los procesos de fondo del arenal MUEREN al terminar cada llamada de
  bash** (cada llamada es su propio sandbox): un `nohup … &` no
  sobrevive, y `pgrep` engaña porque se encuentra a sí mismo en el
  entorno del proxy. Para lo largo: `volcar_referencia_senal.py` es
  REANUDABLE con `SENAL_CACHE=/tmp/…` — correrlo con `timeout 165` en
  bucle hasta que imprima el total (dos o tres pasadas).
- La caché de señal se descarta sola al tocar `casos-reportados.json`
  (huella): cada cambio de casos o patrones implica la pasada lenta.
- Borrar archivos en la carpeta pide el permiso de Cowork
  (`allow_cowork_file_delete`); ya quedó concedido en esta sesión.
- JSDOM: `npm install jsdom` en /tmp; el botón «✎ revisión» hay que
  PULSARLO en las pruebas (¿revision sólo lo revela).
- El humo de la sesión (`humo_v19.js`, `humo_v110.js`) vive en la
  carpeta de outputs del chat, no en el repositorio: si el chat nuevo
  quiere re-probar la página, los rehace en /tmp.

## 6. LO QUE SIGUE (en orden)

1. **Rotar la clave** (§0 — dos sesiones ya).
2. **Empujar los cuatro commits** si no se ha hecho (o el ciclo de Angel
   los lleva con el próximo lote).
3. **Terminar el testigo del DPD** (§4): zip → tsv → informes con la
   columna llena → criterio de categoría para los proclíticos.
4. **Enseñar al IEBH el régimen medido de §34** (§3): los dos falsos, el
   piso 159, y lo correcto que calla debajo (ekamante, tvamasi). Ampliar
   la licencia es suyo.
5. **La pasada única de dos junturas** (briefing 35 §4): cierra el punto
   4 del mapa 32 (idamavocanti) y haría innecesarias muchas
   `escalera_iebh`.
6. Resto del mapa 33: §23/pakati sistemático, descomposiciones del DPD
   en el motor, des-flexión. **Sin empezar.**
