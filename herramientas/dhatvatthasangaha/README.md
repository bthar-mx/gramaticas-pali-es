# Dhātvatthasaṅgaha-nissaya — herramientas

El escaneo (KBRL 001288) y todo lo que sale de él viven fuera del
repositorio, en `~/Tipitaka/nissaya/ocr/dhatvatthasangaha-nissaya/`
(cambiable con `DHATVATTHA_OCR`). Los modelos, en `~/Tipitaka/nissaya/tessdata`
(`myap`, `myab`; cambiable con `NISSAYA_TESSDATA`).

| guion | qué hace |
| --- | --- |
| `paginar.py` | lee el titulillo de cada hoja y escribe `recursos/raices/dhatvatthasangaha-nissaya.paginas.json` |
| `ocr.py leer N` | OCR renglón a renglón (`myap`, `--psm 7`, ×0,75); `--guardar` escribe `raw/NNN.txt` |
| `ocr.py medir N` | CER contra la transcripción de control `_work/piloto/NNN.gt.txt` |
| `extraer.py` | versos y entradas a `docs/fuentes/dhatvatthasangaha/datos.json` (local) y la cola `revision.md` |

Las imágenes se sacaron una vez con

    pdfimages -png recursos/raices/dhatvatthasangaha-nissaya.pdf img/p

y se renombraron a `img/NNN.png`, con NNN = hoja del PDF (1-567).

Piloto y cifras: `docs/dhatvatthasangaha/piloto-ocr.md`.
