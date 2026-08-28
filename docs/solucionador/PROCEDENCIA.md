# Solucionador de sandhis — procedencia

Entrega del 24 de agosto de 2026, encargo de Ven. Bhikkhu Nandisena, recibida
como `solucionador-de-sandhis.zip` e incorporada al árbol el 2026-08-28.

**Autor de la entrega: Miguel De Anquín.** Donde este documento dice «el
colaborador», es él.

## Qué es suyo, qué es nuestro, qué cambió al incorporarse

**De Miguel De Anquín** (todo lo que no se lista abajo): el motor (`nuestro/`),
las mediciones, la pantalla, los datos nuevos de `recursos/sandhi/`,
`recursos/lexico/`, `recursos/corpus/`, `comun/concordancia-sandhi-*.json`,
`comun/concordancia-tres-numeraciones-sandhi.json`, `fuentes-derivadas/`,
`banco.sha256`, y la colación de `recursos/combinacion-eufonica.md` contra el
PDF del Venerable (49/49 enunciados, 22/22 notas; correcciones declaradas en
la cabecera del propio archivo).

**Ya era nuestro y no se tocó**: `recursos/sandhi/reglas.json` (su copia llegó
byte por byte idéntica a la del repositorio) y
`herramientas/derivar_secuencias.py` (el verificador; su copia también llegó
idéntica). `kaccayana/01-sandhi-kappa.md` **no se reemplazó**: la versión del
repositorio es posterior a la instantánea de la entrega (lleva las glosas
`{palabra|glosa}`), y el banco se recongeló sobre la nuestra.

**Cambios hechos al incorporar, nuestros y anotados en el propio código**:

- `nuestro/congelar.py`: la ruta de `listas-cerradas.json` en la lista del
  banco decía `recursos/` donde el motor lee `recursos/sandhi/`; la carpeta
  plana de la entrega enmascaraba la diferencia. Se fijó la ruta del motor.
- `banco.sha256` recongelado tras la colocación (nueva huella de
  `01-sandhi-kappa.md` y la ruta corregida).

## Lo que la entrega declara y sigue pendiente

- `recursos/lexico/dpd-descomposiciones.tsv` (77 MB) no vino; se regenera con
  `nuestro/exportar_dpd.py` + `nuestro/preparar_descomposiciones.py` desde una
  base `dpd-mobile.db`. Sin él, el modo párrafo detecta mucho menos.
- `medir_deteccion.py` importa un módulo `grupos_iniciales` que la entrega no
  trae (sólo vino el JSON). Defecto de la entrega, registrado; no afecta a las
  tres mediciones principales.
- `fuentes-derivadas/concordancia-nandisena-51.json` **no es fuente del
  motor** por decisión del propio colaborador: se extrajo de `sandhi-6.html`
  v1.0 (2026-08-10) y la página viva es v3.8; las diferencias esperan el
  fallo del Venerable.
- Las ocho consultas de `INFORME-AL-VENERABLE.md` esperan respuesta.

## Los datos del DPD

`recursos/lexico/dpd-formas.txt` y el `.tsv` que se regenere proceden del
Digital Pāḷi Dictionary (v0.4.20260728, licencia CC BY-NC-SA). En este
proyecto son **filtro y ordenación, nunca análisis presentado al lector**;
toda descomposición que llegue a mostrarse se atribuye al DPD.
