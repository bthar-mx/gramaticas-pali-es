# Briefing de la sesión 65 — EL DHĀTVATTHASAṄGAHA, LAS 1.637 RAÍCES VISTAS

**Fecha:** 2026-10-10. Tema único: verificar en la imagen las raíces del
*Dhātvatthasaṅgahapāṭh-nissaya* (KBRL 001288). **`site/` no cambia.**

Leer antes el 64 y `recursos/raices/LEEME.md` (al día).

---

## 1. LO HECHO

1. **Todas las raíces vistas en la imagen.** 1.915 renglones del margen
   (hojas 61-407) en hojas de contacto, y ampliación de cada duda. Resultado:
   **1.637 raíces, las que declara el libro, y cuadran los siete kaṇḍas**
   (147 · 130 · 159 · 177 · 266 · 316 · 442).
2. **22 entradas que el extractor no había tomado por tales** (`V-nueva`):
   renglones que no empiezan por «RAÍZ၊ သည်» —*လာဘံ ကို … အဗြဝိ*,
   *ပိဉ္ဆောတိ စ*, *တဖော တု*— o pegados a la nota anterior.
3. **Las pp. 262-263 que faltan en el escaneo**, leídas en las fotos del
   ejemplar del IEBH: **la séptima impresión no pagina como la sexta**
   (recompuesta; encabezado «(၂၈၄)» por verso); ahí son las pp. 201-203.
   Diez raíces, versos ၂၈၃-၂၈၅: *madi, maddo, madhu, mano, mabbo, mabbho,
   mayo, maro, malo, mallo* (`V-7ª`). La p. 46 no esconde texto.
4. **El OCR del margen fallaba en 350 de 1.592 entradas**; corregidas. Las
   reglas para distinguir las letras confundidas, en
   `docs/dhatvatthasangaha/piloto-ocr.md` §6.
5. Salida, **local** (`.gitignore`):
   `docs/fuentes/dhatvatthasangaha/verificacion.md` (resumen, dudas, tabla
   completa) y `verificacion.json` (por raíz: hoja, página, y0/y1, estado,
   lectura, OCR, nota, verso, kaṇḍa, acumulado).
6. Herramientas de trabajo (hojas de contacto, ampliación, registro) y sus
   datos, en `~/Tipitaka/nissaya/ocr/dhatvatthasangaha-nissaya/_work/sesion65/`,
   fuera del repositorio.

## 2. PENDIENTE DEL IEBH: 18 DUDAS, EN EL PAPEL

Lista con la evidencia en `verificacion.md`, «Para decidir en el papel».

- **16 son ယ / ဃ.** En la negrita del margen las dos letras tienen la misma
  forma (E1283 y E1284, juntas, iguales; el OCR leyó una ယ y otra ဃ). Se ha
  dejado la lectura que favorecen el verso, el prayoga y el Dhātupāṭha
  sánscrito. **Claude se equivocó aquí una vez en la sesión** (corrigió E7/E9
  a ဃ, luego a ယ por la forma): por eso van todas como duda. Quizá la
  séptima impresión, con otra letra, las distinga: una foto de una de ellas
  (p. ej. *လဃော / လဃိ*, verso ၃၃၀) lo diría.
- E17: punto redondo sobre ဇ, ¿mancha o niggahīta?
- E1594: *ဟိဝိ* o *ဟီ…*, la vocal.

## 3. POR DÓNDE SEGUIR

1. Con las 18 resueltas: la obra nueva en `raices.json` (`obras`), su
   pestaña en `plantilla.html`, la concordancia con el Saddanīti en
   `generar_raices.py`. Raíz y página salen de `verificacion.json`; el
   **sentido** todavía no está verificado (es OCR de `datos.json`): es la
   siguiente pasada, con el mismo método.
2. **El verso de cada raíz**: `verso` en `verificacion.json` es la
   asignación del extractor, y en algunos versos está corrida una raíz
   (p. ej. ၃၃၀/၃၃၁, ၃၉၀/၃၉၁). Antes de publicar «verso N» hay que
   reasignar contra el texto del verso.
3. Las diez de la séptima impresión se citan con su página (201-203) y su
   impresión, hasta que haya otra cosa.

## 4. ERRORES Y AVISOS DE ESTA SESIÓN

- El vaivén ယ/ဃ de E7 y E9 (arriba).
- En la carpeta del OCR quedó **`_work/sesion65-copia.tar` (35 MB)**, una
  copia de `raw/` e `img/` para trabajar en la nube; no se pudo borrar
  (permiso de borrado no pedido). Se puede tirar.
- `extraer.py` del repositorio **no se ha tocado**; la copia de trabajo
  guardaba además y0/y1 de entradas y versos.

## 5. QUÉ HAY SIN COMMIT

En `herramientas/.publicar/` (lo lanza el IEBH): los de la sesión 64 (si no
se lanzaron ya), más

- `recursos/raices/LEEME.md` — séptima impresión, pp. 262-263, verificación
- `docs/dhatvatthasangaha/piloto-ocr.md` — §6
- `docs/briefings/briefing-sesion-65.md`

`verificacion.md` y `.json` no entran: están bajo `.gitignore`.
