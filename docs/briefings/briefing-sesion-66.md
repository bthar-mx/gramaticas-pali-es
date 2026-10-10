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

## 2. PENDIENTE

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
