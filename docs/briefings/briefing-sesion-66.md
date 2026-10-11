# Briefing de la sesión 66 — EL DHĀTVATTHASAṄGAHA, PUBLICADO

**Fecha:** 2026-10-10. Tema único: la quinta pestaña de `/recursos/raices/`
(v1.7). Leer antes el 65 y `recursos/raices/LEEME.md` (al día).

---

## 1. LO HECHO

1. **El sentido, cotejado con la imagen.** 138 hojas de contacto (renglones
   del cuerpo desde la raíz hasta «…၌ ဖြစ်၏», con lo extraído al lado), miradas
   todas. 809 entradas corregidas desde la imagen; 49 quedan `?` con su motivo
   (`sentido_duda`); las diez de la séptima impresión, `sin-imagen`. Reglas:
   el OCR lee «ေ၊» como «ေါ» al final del sentido pāḷi; se quitan los pares
   que son condición de prefijo o de gaṇa («…ရှေ့ရှိမူ», «…ဖြစ်မူ»).
   Registro: `~/Tipitaka/nissaya/ocr/dhatvatthasangaha-nissaya/_work/sesion66/cotejo-sentidos.py`.
2. **Testigos**: el primer sentido pāḷi está en el verso en 1.325 de 1.528
   (87 %); los demás son compuestos que el metro corta de otro modo u OCR del
   verso. Cruce con el Saddanīti con la misma glosa: 143 → 179.
3. **Publicado** (por lanzar): `recursos/raices/dhatvatthasangaha.json`,
   `concordar_dv` en `generar_raices.py`, pestaña e índice por kaṇḍas y marca
   «DV» en `plantilla.html` (v1.7, nota de versión ES/EN), tarjeta y portada
   en `generar_indices.py`. El IEBH vio un piloto antes de publicar.
4. Decisión del IEBH: primero publicar con el birmano; la traducción, en una
   pasada aparte (propuesta: glosario de frases, ~1.300 distintas, que firma
   el IEBH y se aplica en todas las entradas; rótulo ES/EN como el `ES·N` del
   Dhātupāṭha).

5. **Traducción** (pedido del IEBH: adoptar el Saddanīti donde se pueda).
   `traducir_dv` en `generar_raices.py`: si el sentido pāḷi coincide con una
   glosa del Saddanīti (como en el Dhātupāṭha: sin «ca/pi» final, consonante
   doble inicial simplificada), español de Nandisena e inglés de esa edición,
   rótulo «Sad»: **543 de 2.016 sentidos, ya en la página**. El resto, el
   glosario de frases birmanas `recursos/raices/dhatvatthasangaha-glosas.json`
   (1.098 frases; seguridad A 951 · B 109 · C 38), **sin firmar**: no se
   inyecta hasta `"adjudicado": true`. Firmado, cubre 1.365 sentidos más;
   quedan 109 sin birmano y sin Saddanīti. Tabla para adjudicar, las C y B
   primero: `docs/dhatvatthasangaha/glosas-por-adjudicar.md`.

6. **Segunda parte de la sesión (v1.8, sin commit)**, con el IEBH fuera:
   - **Los 445 versos**, cotejados en 65 hojas de contacto (verso 1-109 leídos
     enteros, 110-445 por corrección del OCR); registro en
     `_work/sesion66/cotejo-versos.py`. Vista «Versos» en la pestaña; cada raíz
     con su verso (campo `verso`, `verso_como`).
   - **«La obra y guía»**: tercera vista de la pestaña (no una página aparte:
     no necesita entrada en `cabecera.PAGINAS`). Se basa en la portada, los
     vv. 1, 434-436 y la nota de los editores (hojas 6-9 y 13-14, leídas por
     OCR `mya` en la nube; el registro de dhammadāna se resume, no se traduce).
   - **Globos de los kaṇḍas** (`kandas_info`, `orden_es/en` en el JSON).
   - **Glosario**: tabla `pali` con los 39 sentidos sin glosa birmana.
   - **Aviso de derechos** de los editores (hoja 14): nadie puede reimprimir
     sin permiso del grupo Visuddhāruṃ Gaṇavācaka. Se publican los versos por
     decisión del IEBH tomada antes de leerlo; se le avisa.

7. **Tercera parte (v1.9, sin commit)**, con el IEBH:
   - Traducción en borrador publicada, rotulada («publicar_borrador»).
   - «sentido» → «significado» en los textos en español de la pestaña.
   - Cabecera fija de columnas con globos.
   - Lo del Saddanīti ya no dice «Sad»: si la raíz del Saddanīti con esa
     glosa está en la tercera columna, la traducción va allí (campo
     `en_col`, 187); si no, rótulo «según Saddanīti» (356).
   - Buscador del sitio: tipos `dhatupatha`, `dhatvattha`,
     `dhatvattha_versos` en `generar_busqueda.py` (sin borradores); anclas
     `#dpN`, `#dvN`, `#dvvN` en la plantilla (`abrirAncla`).
   - **Marcas de gaṇa en los versos**: bhū, cu, di, ru, svā, kī, gaha, to/tā
     (tanādi; «tā» plural, ver nissaya «တာ၊ တနာဒိဂဏိကတို့တည်း»), y además
     «tu» (cutu 32×, bhūtu, dirutu): ¿tudādi? Sin confirmar. El nissaya nombra
     el gaṇa (ဘူဝါဒိ 72, စုရာဒိ 100, ဒိဝါဒိ 35… en el OCR de `raw/`).

## 2. PENDIENTE

- **Enlazar las raíces dentro del texto de los versos** (recomendado al
  IEBH): 1.514 de 1.625 salen como palabra entera; ~100 en sandhi (’ki = aki).
- **Gaṇa: hecho** (v1.9). `gana.py` + `gana_aplicar.py` en `_work/sesion66/`.
  Pendiente: cotejo con la imagen de las 26 que discrepan del Saddanīti y de
  las «según el significado». «tu» = partícula «pero» (resuelto).
- **Versión interna con el nissaya: hecha (opción 1)**, fuera del repositorio:
  `~/Tipitaka/nissaya/ocr/dhatvatthasangaha-nissaya/interno/` (index.html,
  nissaya.js, recortes/, paginas/; ~60 MB; se abre con doble clic). Se rehace
  con `_work/interno/construir.py`. Opción 2 (repo privado + Cloudflare
  Access) cuando haga falta. Pedir permiso al grupo Visuddhāruṃ Gaṇavācaka.
- **OCR del kaṇḍa 1 corregido contra la imagen** (hojas 64-93, 304 líneas):
  `_work/interno/corr-k1.json`; `aplicar_corr.py` genera `raw_corr/` sin
  tocar `raw/`. `construir.py` lee `raw_corr/` y ya no corta una entrada en
  una cita numerada («၂။ ၁၈၇)») ni en un verso sin raíces propias (v. 16 de
  *avo*). Traducción ES/EN puesta al día; quedan 15 «[?]», ningún «[OCR …]».
  Correcciones al sitio público: E16 añcho, E8 mūlye, E37 pāṇajīvane.
- **Kaṇḍa 2 (Kakārādika)**: OCR corregido (hojas 93-118, `corr-k2.json`) y
  traducido ES/EN (`traduccion-k2.json`, 127 entradas). Las correcciones de
  consonante de los kaṇḍas 1-2 se cotejaron por segunda vez, línea contra
  imagen: deshizo cuatro correcciones mías erróneas (kaḷo, kūḍo, ကေသောသိ,
  သောကော). E37: el verso dice pāṇajīvane; el cuerpo, ပါဏဇီဝဏေ.
- **Traducción del nissaya (piloto)**: kaṇḍa 1 (Sarādika, 138 entradas)
  traducida al español, borrador sobre el OCR, en
  `_work/interno/traduccion-k1.json`; se ve en la versión interna. Espera la
  revisión del IEBH antes de seguir con los kaṇḍas 2-7 (`traduccion-kN.json`,
  `construir.py` los recoge todos).
- **Kaṇḍas 3-7 (noche del 10 al 11-X)**: OCR corregido contra la imagen por
  agentes en paralelo (hojas 119-399, 2.874 líneas; segunda pasada de cada
  bloque con `verif2.py`), `corr-k3…k7.json`; `raw_corr/` regenerado (3.524
  líneas en total). Traducidos ES/EN por agentes (`traduccion-k3…k7.json`,
  1.350 entradas; 332 con algún «[?]»). La versión interna tiene ya las 1.615
  entradas con nissaya traducidas. BORRADOR SIN REVISIÓN HUMANA.
  Lista de lo que hay que cotejar y de lo que afecta a los datos publicados
  (lemas y sentidos distintos, totales de grupo, ဃ/ယ): 
  `_work/interno/revision-pendiente-k3-7.md` (privado, contiene birmano).
  Cotejada luego con Saddanīti, Dhātupāṭha, Dhātumañjūsā y cognado
  sánscrito (agentes, `rev-k3-4/k5-6/k7.json`, privados): aplicadas a
  `dhatvatthasangaha.json` 115 entradas y 73 versos, cada una con
  `nota_correccion`; «?» pasa de 18 a 5 (aghi, aja, cagha, dhāgha, lagha).
  Diferido: gaṇa de E617/E758/E797 y los sentidos con prefijo de E758/E797;
  E1283 laya/lagha, E1293 yāte/ghāte, E1575 āyāte/āghāte, E640 tiya/tigha,
  E980/E1041 vuddhyaṃ/vuḍḍhyaṃ, verso 364 gatibhūkhana/sukhana: papel de la
  7.ª impresión. Siete significados nuevos sin traducción todavía.

- **Decidir, a la vista del aviso de derechos**, si los versos pāḷi siguen
  publicados.

- **Adjudicar el glosario de frases birmanas** (arriba). Las «C» son sobre
  todo fragmentos de sentidos múltiples y remisiones a otras raíces.

- **Las 18 lecturas dudosas del margen** (briefing 65 §2), y las 49 del
  sentido: en el papel.
- **El contador** dice «1.625 entradas» y la pestaña «1.637» (raíces). ¿Que
  cuenten las dos raíces? Pregunta abierta al IEBH.
- **El número de verso** no se publica hasta reasignarlo contra el texto
  (briefing 65 §3).
- Las diez de la séptima impresión: sentido sin cotejar (no hay OCR de las
  fotos).
- La traducción de la glosa birmana (arriba).
- Aviso viejo, no de esta sesión: `generar_raices.py` cuenta 181 raíces sin
  cognado sánscrito; la nota del pie dice 180.

## 3. QUÉ HAY SIN COMMIT

`herramientas/.publicar/` lleva lo de las sesiones 64 y 65 (si no se
lanzaron) y lo de ésta. El piloto y las hojas de contacto quedan fuera del
repositorio, en `_work/sesion66/`.
