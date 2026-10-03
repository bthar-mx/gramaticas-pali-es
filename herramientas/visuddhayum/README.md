# Herramientas de recortes — Visuddhāyuṃ

Copia de `~/Tipitaka/nissaya/ocr/visuddhayum-kaccayana-tika/_crops/tools/` (2026-10-03), sin cambios. Sirven para recortar de las imágenes del escaneo las líneas de cada sutta (encabezado, (က), (ခ)) y cotejarlas a ojo. El escaneo y el OCR **no** están en el repositorio (derechos); viven en `~/Tipitaka/nissaya/ocr/visuddhayum-kaccayana-tika/` (`img/p-NNN-*.jpg`, `raw/NNN.txt`, `tessdata/mya.traineddata`).

## Guiones

| Guion | Uso | Qué hace |
|---|---|---|
| `lines.py` | `python3 lines.py N` | Líneas de la página PDF N con su altura (Tesseract `--psm 6`, TSV). Guarda una caché por página. |
| `crop.py` | `python3 crop.py N a b salida.jpg` · `python3 crop.py N y300 y900 salida.jpg` | Recorta de la línea a a la b (índices de `lines.py`), o por píxeles con el prefijo `y`. |
| `mk.py` | `python3 mk.py A B` | Un recorte por sutta entre las páginas A y B: encabezado + 5 líneas + (ခ) + 7 líneas, en `_crops/nama/hNNN-pPPP.jpg`. Falla con los encabezados que el OCR no lee. |
| `loc.py` | `python3 loc.py A B` | Lista los encabezados «(n) … padaṃ», (က) y (ခ) de las páginas A–B. |

Requisitos: Python 3, Pillow, Tesseract 4+ en el PATH. `mk.py` y `loc.py` importan `lines` desde el directorio actual (`sys.path.insert(0,'.')`): ejecutarlos desde esta carpeta.

## Rutas que suponen la VM de Cowork y hay que cambiar en el Mac

Los guiones se escribieron para el shell de Cowork, donde la carpeta conectada se monta en `~/mnt/…` y el área de trabajo es `~/vh`. En el Mac (Claude Code) hay que cambiar:

| Archivo | Línea | Ahora (VM) | En el Mac |
|---|---|---|---|
| `lines.py` | 2 | `B=os.path.expanduser('~/mnt/nissaya/ocr/visuddhayum-kaccayana-tika')` | `~/Tipitaka/nissaya/ocr/visuddhayum-kaccayana-tika` (en la sesión 2 de Cowork, con ~/Tipitaka conectado, era `~/mnt/Tipitaka/nissaya/…`) |
| `lines.py` | 6 | caché `~/vh/tsv/{p}.tsv` (scratch de la VM; se pierde con la sesión) | una carpeta persistente fuera del repo, p. ej. `~/Tipitaka/nissaya/ocr/visuddhayum-kaccayana-tika/_crops/tsv/` (crearla) |
| `crop.py` | 2 | `sys.path.insert(0, os.path.expanduser('~/vh'))` | la carpeta de los guiones: `~/Documents/gramaticas-pali-es/herramientas/visuddhayum` |
| `mk.py` | 5 | salida `B+'/_crops/nama'` | sin cambio (depende de `B`); los recortes quedan fuera del repo, en `~/Tipitaka/…/_crops/` |

`img(p)` busca en `B+'/img'` y `tessdata` en `B+'/tessdata'`: basta con corregir `B`.

Los recortes (`_crops/`) y la caché no deben entrar en el repositorio.

## Notas de trabajo

- `docs/visuddhayum/nama-piloto.md` — tabla de Nāma (§52–§107 cotejados; §108 en adelante, por hacer).
- `docs/visuddhayum/sandhi-piloto.md` — tabla de Sandhi (fuente de `recursos/analisis/datos/01-sandhi.json`).
