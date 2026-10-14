# Siete tratados de la escuela de Kaccāyana, de GRETIL

Bajados el 2026-10-13 del espejo **INDOLOGY/GRETIL-mirror** (GitHub), que
reproduce `gretil.sub.uni-goettingen.de/gretil/2_pali/9_phil/gramm/`. GRETIL
mismo no era accesible desde la sesión; el espejo trae los mismos archivos.

| Archivo | Obra | Archivo GRETIL | Base | Tamaño |
| --- | --- | --- | --- | ---: |
| `Kaccayanasuttaniddesa.md` | Suttaniddesa, Chapaṭa (s. XV) | `chkacsnu.htm` | ed. Medhaṅkara, Colombo 1915; trans. Ruiz Falqués 2013 | 501 KB |
| `Balavatara.md` | Bālāvatāra, Dhammakitti (s. XIV) | `balava_u.htm` | Sri Lanka Tripitaka Project | 95 KB |
| `Karika.md` | Kārikā, Dhammasenāpati (s. XI) | `dhkariku.htm` | ed. birmana 1964; trans. Ruiz Falqués | 62 KB |
| `Saddatthabhedacinta.md` | Saddatthabhedacintā, Saddhammasiri | `saddatbu.htm` | ed. birmana 1964; trans. Ruiz Falqués | 43 KB |
| `Kaccayanabheda.md` | Kaccāyanabheda, Mahāyasa (s. XIV) | `mkacbheu.htm` | ed. birmana 1964; trans. Ruiz Falqués | 21 KB |
| `Kaccayanasara.md` | Kaccāyanasāra, Yasa (s. XIV–XV), sólo el verso | `yaskacsu.htm` | ed. birmana 1964; trans. Ruiz Falqués | 10 KB |
| `Saddabindu.md` | Saddabindu, sin la sanna | `saddab_u.htm` | Sri Lanka Tripitaka Project | 4 KB |

La «ed. birmana 1964» es *Saddā ṅay 15 coṅ pāṭh* («Quince tratados
gramaticales menores»), Rangún, Icchāsaya Piṭaka Press.

## Cómo se hicieron

Conversión mecánica HTML → texto: se quitaron etiquetas y la tabla de
transliteración de GRETIL; el texto pāḷi no se tocó. Se conserva entera la
cabecera de cada archivo GRETIL, con la procedencia y el aviso de su autor.

## Mejoras de presentación (2026-10-14)

Sin tocar el texto pāḷi (comprobado mecánicamente: quitado el marcado
añadido, el texto coincide carácter por carácter con la conversión del 13 de
octubre):

- La cabecera inglesa de GRETIL pasa a un comentario HTML, íntegra.
- **Suttaniddesa:** títulos de kappa como encabezados (los de GRETIL, «II.
  NĀMA»…; los que faltan, entre corchetes: «[Sandhikappa]», «[Samāsakappa]»,
  «[Uṇādikappa]»); cada sutta de Kaccāyana es un encabezado «### Kacc_N.»
  (numeración de Senart/Pind, la misma que la «Kc» de Smith); [#N] → [p. N]
  (páginas de Medhaṅkara 1915; la paginación salta de 236 a 241).
- **Bālāvatāra:** [SL Page N] → [SLTP p. N]; 184 suttas de Kaccāyana citados
  como párrafo propio van en negrita con «[Kc N]». La identificación es
  AUTOMÁTICA (coincidencia de texto con el Suttaniddesa): verificar antes de
  citar; pueden faltar suttas.
- **Kārikā, Saddatthabhedacintā, Kaccāyanabheda, Kaccāyanasāra:** títulos de
  sección como encabezados, colofones en negrita, notas de variantes como
  citas («>»), saltos de línea en los versos; se conservan las referencias de
  GRETIL («// DhKar_11 //», «// Sad_1 //»…) para citar.
- **Saddabindu:** [SL Page N] → [SLTP p. N]; números de estrofa en negrita.

## Cautelas

- **Son transcripciones provisionales.** Ruiz Falqués pide expresamente no
  citar sin cotejar con el impreso. Sirven para BUSCAR, como la Nyāsa; para
  CITAR, al impreso.
- **Licencia: «COPYRIGHT AND TERMS OF USAGE AS FOR SOURCE FILE».** GRETIL no
  da una licencia abierta propia. El IEBH decidió publicarlos (2026-10-14),
  como hace el espejo INDOLOGY en GitHub, con la cabecera y la atribución de
  GRETIL y de cada transcriptor íntegras.

## Escaneo del impreso del Suttaniddesa

`Kaccayanasuttaniddesa-Medhankara-1915.pdf` (281 págs., 92 MB): la ed. de
M. Medhaṅkara, Colombo, Vidyabhusana Press, 1915, en escritura cingalesa, la
misma que transcribió Ruiz Falqués (sus `[#N]` son las páginas de este
impreso). Bajado el 2026-10-13 del Göttinger Digitalisierungszentrum (GDZ,
PPN67018828X), marcado como dominio público; las condiciones de la SUB
Göttingen permiten el uso no comercial para investigación. La copia de la
GRETIL e-library (eDocs, gr_elib-260) está cerrada hasta 2056. No viaja con el
repositorio: `.gitignore` excluye `*.pdf`.
