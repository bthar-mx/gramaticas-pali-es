# Herramientas de recortes — Visuddhāyuṃ

Recortan de las imágenes del escaneo las líneas de cada sutta (encabezado,
(က), (ခ)) para cotejarlas a ojo. El escaneo y el OCR **no** están en el
repositorio (derechos); viven en
`~/Tipitaka/nissaya/ocr/visuddhayum-kaccayana-tika/` (`img/p-NNN-*.jpg`,
`raw/NNN.txt`, `tessdata/mya.traineddata`). `NNN` es la página del PDF, y
**página del PDF = página del libro + 46**.

Kāraka (§271–§315): nº del libro = § + 307, PDF 494–562; el libro sigue su
propio orden de capítulos (Ākhyāta empieza en el nº 270 del libro = §406).

Samāsa (§316–§343): capítulo 5 del libro; nº del libro = § + 172, PDF 390–442.
El escaneo es defectuoso dentro de §328: faltan las pp. impresas 373–374 y
379–380, y las 371–372 y 381–382 están dos veces (PDF 417–418 = 425–426;
PDF 419–420 = 427–428). Se lee PDF 427–428 y se coteja con 419–420. Detalle
en `docs/visuddhayum/samasa-piloto.md`.

Taddhita (§344–§405): capítulo 6 del libro; nº del libro = § + 172, PDF 443–490;
pariśiṣṭa PDF 491–493 (pp. 445–447), sin numerar; escaneo sin defectos. Detalle
en `docs/visuddhayum/taddhita-piloto.md`.

Ākhyāta (§406–§523): nº del libro = § − 136, PDF 224–316, cuatro partes
(§406–431, 432–457, 458–481, 482–523, = kaṇḍa de Nandisena); §424–§430 sin
encabezado (bloque 243–244); números mal impresos: §420 «274», §456 «340»,
§457 «341»; pariśiṣṭa PDF 317 (p. 271), clasificación de los suttas;
ensayo «အာချာတ်ဂိုဏ်း» PDF 318–321; escaneo sin defectos. Detalle en
`docs/visuddhayum/akhyata-piloto.md`.

Adaptadas al Mac el 2026-10-03 (antes suponían la VM de Cowork, con `~/mnt/…`
y `~/vh`). Lo que cambió:

| Antes (VM) | Ahora (Mac) |
|---|---|
| `B = ~/mnt/nissaya/ocr/visuddhayum-kaccayana-tika` | `B = ~/Tipitaka/nissaya/ocr/visuddhayum-kaccayana-tika`, cambiable con la variable de entorno `VISUDDHAYUM_OCR` |
| caché TSV en `~/vh/tsv/` (scratch, se perdía con la sesión) | `_crops/tsv/` junto al OCR; persiste, y se crea sola |
| `sys.path` a `~/vh` o al directorio actual | la carpeta del propio guion: se pueden ejecutar desde cualquier sitio |
| `mk.py` escribía siempre en `_crops/nama` | tercer argumento opcional con la carpeta; `nama` por defecto |

Además, los cuatro guiones avisan con un mensaje claro si falta el escaneo,
si Tesseract no devuelve TSV o si falta Pillow, en vez de fallar con una
traza.

## Guiones

| Guion | Uso | Qué hace |
|---|---|---|
| `lines.py` | `python3 lines.py N` | Líneas de la página N del PDF con su altura (Tesseract `--psm 6`, TSV). Guarda caché por página. |
| `crop.py` | `python3 crop.py N a b salida.jpg` · `python3 crop.py N y300 y900 salida.jpg` | Recorta de la línea a a la b (índices de `lines.py`), o por píxeles con el prefijo `y`. |
| `mk.py` | `python3 mk.py A B [carpeta]` | Un recorte por sutta entre las páginas A y B: encabezado + 5 líneas + (ခ) + 7 líneas, en `_crops/<carpeta>/hNNN-pPPP.jpg`. Omite los encabezados que el OCR no lee. |
| `loc.py` | `python3 loc.py A B` | Lista los encabezados «(n) … padaṃ», los (က) y los (ခ) de las páginas A–B. |

## Requisitos en este Mac

- **Tesseract 5.5.3** (`/opt/homebrew/bin/tesseract`). El birmano no está en
  el tessdata de Homebrew: los guiones usan el `mya.traineddata` de la carpeta
  del OCR con `--tessdata-dir`.
- **Pillow 12.3.0**, instalado con `brew install pillow` (2026-10-03). El
  `python3` de Homebrew está «externally managed» (PEP 668), de modo que
  `pip install` no es la vía aquí.
- Con `OMP_THREAD_LIMIT=1`, que los guiones fijan solos, el OCR de una página
  tarda ~3 s; después queda en caché.

`sips`, el recortador de macOS, **no sirve** de sustituto de Pillow: su
`--cropOffset` ignora unos desplazamientos y con otros devuelve una imagen
negra (comprobado el 2026-10-03).

Los recortes (`_crops/`) y la caché no deben entrar en el repositorio.

## Notas de trabajo

- `docs/visuddhayum/nama-piloto.md` — tabla de Nāma (§52–§107 cotejados;
  §108 en adelante, por hacer).
- `docs/visuddhayum/karaka-piloto.md` — tabla de Kāraka (§271–§315; por
  hacer).
- `docs/visuddhayum/samasa-piloto.md` — tabla de Samāsa (§316–§343;
  preparada, por hacer).
- `docs/visuddhayum/taddhita-piloto.md` — tabla de Taddhita (§344–§405;
  preparada, por hacer).
- `docs/visuddhayum/akhyata-piloto.md` — tabla de Ākhyāta (§406–§523;
  preparada, por hacer).
- `docs/visuddhayum/sandhi-piloto.md` — tabla de Sandhi (fuente de
  `recursos/analisis/datos/01-sandhi.json`).
- `docs/visuddhayum/clasificacion-cotejo.md` — cotejo de clasificación.

Las reglas de trabajo (qué llega al sitio, cómo se rotula lo que no es del
libro, la concordancia nº del libro ↔ §) están en `CLAUDE.md`, sección
«Visuddhāyuṃ — análisis por sutta». La orden `/visuddhayum-lote` recorre un
tramo de § con estos guiones.
