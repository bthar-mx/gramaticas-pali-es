# Auditoría de las derivaciones del capítulo 2

**Sesión 62.** Encargo del §5 del briefing 61: revisar el Nāma-kappa entero
buscando erratas de la clase de «ādiṃ», y hacerlo con un guion en lugar de
leyendo 219 suttas y afirmando.

    python3 herramientas/auditar_derivaciones.py                 # el informe
    python3 herramientas/auditar_derivaciones.py --detalle       # con cadenas
    python3 herramientas/auditar_derivaciones.py --autoprueba    # el simulador

El informe completo, tal cual lo escupe el guion, está en
`auditoria-derivaciones.txt`, en esta misma carpeta.

**Nada de lo que sigue está firmado.** Son candidatos con su evidencia y una
corrección propuesta; decide IEBH. Y **la corrección va en
`docs/2. Nāma-Kappa.md`**, no en `kaccayana/02-nama-kappa.md`, que es salida
del conversor.

---

## Estado: siete correcciones adjudicadas

Publicadas en v1.4 (es) y v1.2 (en): las tres erratas tipográficas del §1 y las
tres cadenas de §66 del §2.2. En **v1.5 (es)**, una séptima, que no salió del
guion sino del ojo de IEBH:

**«Svāgataṃ» (§71), línea 469 del maestro.** Decía `‘a’ de ‘ya’ se elide
(§83)`, y en `su + āgataṃ` no hay ninguna ‘ya’: la ‘u’ se había sustituido por
‘va’. El ‘ya’ es de «agyāgāraṃ», la derivación de la línea de encima, de la
que se copió el paso. El inglés ya decía ‘va’, de modo que la corrección
acerca las dos ediciones —la inglesa se queda en v1.2, que no cambia—.

**El guion no la cazaba, y ahora sí.** La cadena recomponía igual, porque al
no encontrar ‘ya’ se buscaba la ‘a’ sin alcance y aparecía la de «āgataṃ». De
ahí sale la comprobación **3 bis**: un segmento citado entre comillas SIMPLES
tiene que estar en la forma en ese punto. La distinción entre las dos comillas
es del propio texto —‘ya’ es un segmento, “aggi” es el tema, que puede haberse
transformado ya— y se midió antes de fiarse de ella: en las 608 derivaciones
daba **una** ausencia de segmento, ésta, y ninguna falsa. Queda congelada en
`--autoprueba`.

Con las siete, la recomposición pasa de 571 a **577 de 608**, y quedan 16
cadenas que no dan el lema. El informe `.txt` de al lado está regenerado; las
cifras del apartado siguiente son las de antes, que son las que motivaron cada
propuesta.

---

## El terreno

608 derivaciones, 1.340 pasos, 219 suttas (§52-§270). De la recomposición:

| | |
| --- | ---: |
| la cadena da el lema | 571 |
| la cadena **no** da el lema | 20 |
| ilustrativas (llevan una negación: enseñan lo que NO pasa) | 10 |
| no simulables (el guion lo declara, no las deja pasar) | 7 |

Y de las otras comprobaciones: 3 pasos con comillas sin cerrar, 12 pasos sin
§N, 31 formas con cadenas divergentes, 4 pasos cuya clase no es la del sutta
citado.

---

## 1. Erratas tipográficas (3) — las más seguras

| Línea | Sutta | Dice | Debería decir |
| ---: | --- | --- | --- |
| 278 | §64 · Tissā | `se sustituye por ‘i (§64)` | `‘i’` |
| 702 | §78 · Bhuvi | `ū’ de “bhū”` | `‘ū’` |
| 3685 | §179 · Sabbassaṃ | `‘ā se acorta (§66)` | `‘ā’` |

Las tres rompen además la lectura automática del paso, de modo que arreglarlas
recupera tres derivaciones para la comprobación 4.

## 2. La cadena no da el lema (20)

### 2.1 Falta un paso de elisión (7)

Todas tienen una hermana en el capítulo que sí lo trae, y ésa es la evidencia.

| Línea | Forma | La cadena da | Hermana que sí lo dice |
| ---: | --- | --- | --- |
| 468 | §70 · Vatthuttayaṃ | *vatthuttayaaṃ* | — |
| 670 | §77 · Gavaṃ (go + naṃ) | *gavaaṃ* | línea 596, `‘a’ se elide (§12)` |
| 5052 | §227 · Ko | *kao* | línea 5112, Kaṃ, `‘a’ se elide (§83)` |
| 5111 | §229 · Ko | *kao* | ídem |
| 5988-5993 | §268 · Guṇiyo, Guṇiṭṭho, Satiyo, Satiṭṭho, Medhiyo, Medhiṭṭho | *guṇaiyo* / *guṇiyao*, etc. | — |

Las seis de §268 son un mismo patrón: elidida «vantu» / «mantu» / «vī» y la
vocal del tema, queda todavía la vocal ante ‘si’ → ‘o’, que nadie elide.

### 2.2 Falta el paso de ‘sa’ → ‘sā’ (3)

| Línea | Forma | La cadena da |
| ---: | --- | --- |
| 329 | §66 · Tassā | *tassa* |
| 331 | §66 · Yassā | *yassa* |
| 333 | §66 · Sabbassā | *sabbassa* |

En las tres, `tā + sa` con inserción de ‘s’ y acortamiento da **-assa**, no
**-assā**. La derivación paralela de *Tissā* (línea 278) sí trae
`‘sa’ se sustituye por ‘sā’ (§179)`; las de §66 no. Propuesta: añadirlo.

### 2.3 «Catassannaṃ»: la ‘n’ que falta (2)

Líneas 374 y 1098. Insertar ‘ssa’ en `catu + naṃ` da *catassanaṃ*, con una sola
‘n’. Lo mismo en *Tissannaṃ* (línea 375): da *tissanaṃ*. O el segmento
insertado es otro, o falta un paso de duplicación. **Es pregunta sobre lo que
inserta §67, y la decide IEBH.**

### 2.4 «Puthabyā»: ‘ya’ donde *Matyā* dice ‘y’ (1)

Línea 516. `‘ī’ se sustituye por ‘ya’ (§72)` deja una ‘a’ sobrante: da
*puthabyaā*. La derivación de *Matyā* (línea 396), del mismo §72, escribe
`‘i’ de “mati” se sustituye por ‘y’`. Con ‘y’ recompone. Las dos no pueden
tener razón a la vez.

### 2.5 «Pulliṅgaṃ»: la duplicación parece sobrar (1)

Línea 822. `‘ma’ → ‘ṃ’ (§82); ‘ṃ’ → ‘l’ (§31); ‘l’ se duplica (§28)`: la
sustitución de ‘ṃ’ por ‘l’ ya deja **pul·liṅgaṃ** con las dos eles, de modo
que el tercer paso da *pullliṅgaṃ*. Duda: ¿es §31 quien pone la ‘l’ y §28
sobra, o §31 elide y la geminada la pone §28?

### 2.6 «Bāhussaccaṃ»: falta la inflexión en los componentes (1)

Línea 6022. Los componentes son `bāhussuta + ya`, sin la inflexión ‘aṃ’, de
modo que ninguna cadena puede dar el ‘ṃ’ final del lema.

### 2.7 «Bhuvi» (1)

Línea 702. Arrastra la errata tipográfica de §2.1 y, además, cita el §206
sin ‘§’ dentro del paso (`por “tato” del §206`), que es de los 12 pasos sin
cita legible.

## 3. Mismos componentes, cadenas distintas (31)

La lista entera, con las cadenas enfrentadas, está en el informe. Las que
parecen erratas y no diferencia de enfoque:

- **Itthi**, línea 943 (§85): `‘si’ recibe el nombre de ‘gha’ (§57)`. §57 es
  *Ālapane si gasañño*: el nombre es **‘ga’**, no ‘gha’. Las otras dos
  derivaciones de *Itthi* (líneas 4826 y 5503) dicen ‘ga’.
- **Daṇḍi**, líneas 4828 y 5501: una dice `‘ga’ se elide (§220)` y la otra
  `‘si’ se elide (§220)`. Es la misma operación con dos nombres; conviene
  unificar (y lo mismo en *Itthi*, líneas 4826 vs. 5503).
- **Kva**, líneas 5044 y 5667: la misma elisión de ‘a’ se cita como **§404**
  en un sitio y como **§83** en el otro. §404 cae fuera del capítulo.
- **Ko** y **Kathaṃ**, líneas 5052-5053 vs. 5111-5113: la sustitución de
  «kiṃ» por «ka» se atribuye a `“ca” en §227` y a `§229`. Puede ser correcto
  —son dos suttas—, pero conviene mirarlo junto.
- **Bhikkhavo**, líneas 1299, 1867 y 1960: `‘yo’ se sustituye por ‘vo’` se
  cita como §119 dos veces y como §116 una.
- **Catassannaṃ**, líneas 374 y 1098: además de lo de §2.3, una cadena cita
  §404 y la otra §90 para el mismo `‘u’ → ‘a’`.

## 4. La clase del paso no es la del sutta citado (4)

| Línea | Forma | Paso | Choque |
| ---: | --- | --- | --- |
| 728 | §79 · Uggate | `‘g’ de “gate” se duplica (§20)` | §20 sustituye |
| 793 | §81 · Gunnaṃ | `se inserta ‘n’ (§28)` | §28 duplica |
| 1151 | §92 · Guṇavantesu | `‘a’ se convierte en ‘e’ (§89)` | §89 alarga |
| 3298 | §167 · Dakkhiṇapubbassaṃ | `se inserta ‘s’ (§63)` | §63 sustituye |

Las dos de inserción pueden ser sólo cuestión de palabra —insertar una
consonante que repite la vecina es duplicar—; las de §20 y §89 piden mirada.

## 5. Pasos sin §N (12)

Nueve son glosa («vocativo plural», «por lo tanto este sutta no opera») y no
piden cita. Los tres que sí la piden:

- líneas 374-375, `por “ca” de este sutta se inserta ‘ssa’` → §67;
- línea 468, los dos pasos de *Vatthuttayaṃ* → §70 y §104;
- línea 1098, `se inserta ‘ssa’` → §90;
- línea 702, `por “tato” del §206` (la ‘§’ está, pero fuera del paréntesis de
  cita, y el guion no la ve como tal).

## 6. Lo que el guion declara que no sabe hacer (7)

Está en el informe con su motivo. Tres son las erratas tipográficas de §1;
dos son *Assaṃ* y *Assā* (líneas 3614-3615), donde la cadena dice
`“ima” se convierte en “a”` partiendo de **imā**, no de «ima»; y dos son glosa
pura («vocativo plural», «véase también §214»).

---

## Lo que el guion NO hace

Los mismos dos límites que declara `auditar_secuencias.py`, y uno propio:

1. **No decide cuál de varios suttas correctos es la mejor cita.** Que un paso
   pase la comprobación 3 sólo dice que el aforismo citado hace esa clase de
   cosa.
2. **No firma nada.**
3. **Donde un tipo de paso no está implementado, lo dice** en lugar de dejarlo
   pasar. Los 7 «no simulables» son eso.

Y una consecuencia del diseño que conviene tener presente: la comprobación 4
prueba **todas** las lecturas posibles de cada operando y da la derivación por
buena si **alguna** reproduce el lema. Es deliberado —no inventar cuál de dos
‘a’ se elide—, y significa que la comprobación es conservadora: lo que marca
es que **ninguna** lectura da el lema.
