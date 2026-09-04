# Kaccāyana Pāḷi-Español: Briefing de la Sesión 17

*Complementa a los briefings 05–16. La sesión 17 ejecutó el trabajo abierto de
la sesión 16: trajo los 83 documentos de paradigmas, construyó
`paradigmas.json`, publicó `/recursos/paradigmas/` (v1.0 → v1.8 en la misma
sesión, con la revisión del IEBH en vivo), cotejó todo contra el documento
maestro de Nandisena y resolvió varias erratas y una duda de fuentes.*

---

## 1. ESTADO AL CIERRE

Todo lo de esta sesión está **hecho, verificado, regenerado y commiteado**.
Al cierre quedaban commits sin `git push`; el push despliega en
<https://gramaticas.buddha-dhamma.net>.

- `recursos/paradigmas/indice.json` — 84 entradas (sesión 16), con la
  corrección «asaddhā» → «assaddhā» de esta sesión.
- `recursos/paradigmas/paradigmas.json` — **84 entradas, 82 tablas, 2379
  formas**, variantes de cada celda como lista; desviaciones del origen
  siempre en `notas`.
- `recursos/paradigmas/plantilla.html` + `herramientas/generar_paradigmas.py`
  → `site/recursos/paradigmas/index.html` (**v1.8**). Enganchado en
  `generar_todo.py`; tarjeta con insignia «83 paradigmas» en `/recursos/`
  (vía `generar_indices.py`).
- Los cuatro borradores de `docs/borradores/` siguen sin rastrear y **no**
  deben entrar en ningún commit.

### docs/nombres.docx — ¡leer esto!

El IEBH facilitó su **documento maestro completo** de los paradigmas (el origen
de los Google Docs, última revisión 2014, licencia CC BY-NC-**ND**). Está en
`docs/nombres.docx` y **NO debe entrar en el repositorio público** — decisión
explícita del IEBH. Está excluido en `.git/info/exclude` (exclusión local:
un clon nuevo no la hereda; rehacerla con
`echo "docs/nombres.docx" >> .git/info/exclude`).

## 2. LA PÁGINA `/recursos/paradigmas/` (v1.8)

Modelo `/recursos/sandhi/`: barra pegajosa con buscador que ignora
diacríticos, filtros por género (con pestaña **Sufijos**) y por tema
(a ā i ī u ū o), barra lateral con secciones **plegables** que **acompañan
al filtro de género**, botón «↑», tema oscuro compartido (`pali_dark`).
Cada tarjeta lleva botones **«Enlace»** (copia el enlace directo) y
**«Copiar»** (la tabla en texto plano alineado), como los suttas de los
capítulos, y un enlace `doc ↗` al Google Doc de origen. Las referencias §N
de la tabla de sufijos llevan el **tooltip grande** de sandhi con el sutta
entero, que `generar_paradigmas.py` extrae del Nāma-Kappa publicado.

Decisiones de estilo del IEBH (permanentes):

- **Formas de las tablas en redonda**; cursiva sólo para lemas y pāḷi
  corrido. Lemas en **cursiva minúscula** (convención académica).
- **No segmentar las desinencias** (nada de purisa·ssa): se presenta al
  modo tradicional, la vibhatti unida a su base.
- La comunicación con Claude es **en inglés**; el producto, en español
  (nada de «commiteado» en los mensajes al IEBH).

## 3. CORRECCIONES APROBADAS POR IEBH EN ESTA SESIÓN

| Dónde | Antes | Después |
| ----- | ----- | ------- |
| #1 pañca, quinta | pañacahi | **pañcahi** |
| Sufijo ‘tha’, ejemplo | sabbatha | **sabbattha** (§28) |
| Índice y N-Ā1, lema | asaddhā | **assaddhā** |
| N-Ā1, primera plural | assadhā | **assaddhā** |

Cada una tiene su nota en `paradigmas.json` con el visto bueno registrado.

## 4. ERRATAS DEL ORIGEN AÚN SIN DECISIÓN (transcritas tal cual)

- M-A2 *mana*, vocativo plural: «bhavanto **mānā**» (¿manā?).
- M-Ī2 *gāmaṇī*: «**gāmanino**, **gāmanissa**» (cuarta sg.), «**gāmanīhi**»
  (quinta pl.), «**gāmāṇimhi**» (séptima sg.) — vacilación ṇ/n y ā.
- M-A12 *sakha*, séptima sg.: «**sakkhe**» (¿sakhe?).
- F-U2 *mātu*, quinta plural: el origen termina en coma
  («…mātūhi, mātūbhi,») — probablemente truncada frente a la tercera.

## 5. FUENTES: LO AVERIGUADO ESTA SESIÓN

- **Los tres usos de ‘to’**: Kaccāyana sólo da la quinta (§248). La séptima
  (ādito, majjhato…) y la tercera (aniccato, dukkhato…) las obtiene
  **Rūpasiddhi por yogavibhāga** de «Kvaci to», en el vutti que sigue a su
  §265 (Imass’ i thaṃ-dāni-ha-to-dhesu ca). El documento de Nandisena
  las recoge igual.
- **La tabla de vibhatti-paccaya** (imagen en el Google Doc) se transcribió
  del documento maestro: quince sufijos con uso, ejemplos, glosas españolas
  del propio Nandisena y doble numeración (§N Kaccāyana enlazado; Rū. §N sin
  enlazar). Su columna «ref.» usa numeración de Rūpasiddhi.
- **Origen de assaddhā (N-Ā1)**: es el ejemplo de **Rūpasiddhi** para el
  neutro en -ā («Ākāranto napuṃsakaliṅgo assaddhāsaddo», sección del
  napuṃsakaliṅga, entre Rū. §198 y §199): bahubbīhi «assaddhaṃ kulaṃ»,
  acortado por *Saro rasso napuṃsake* (Kacc. §342 = Rū. §337) y declinado
  como *citta*. El verso de cierre de esa sección («Cittaṃ kammañ ca
  assaddham ath’ aṭṭhi sukhakāri ca, āyu gotrabhū dhammaññū, cittagū ti
  napuṃsake») es exactamente la serie N de Nandisena. Saddanīti no trae el
  paradigma; Thitzana reproduce la lista con «Asaddhā» (una sola s).

## 6. COTEJO CONTRA EL DOCUMENTO MAESTRO

Cotejo automático (python-docx) de las 82 tablas del JSON contra
`docs/nombres.docx`: **80/82 emparejadas, 1251 celdas idénticas, cero
errores de transcripción**. Las 13 diferencias, todas explicadas:
«purisāya» en la cuarta sg. de M-A1 es **adición de la revisión** de los
Google Docs (no está en el maestro de 2014); «-bhi» expandido en satthu y
kattu (con nota); comas finales; tres mayúsculas accidentales del docx;
«pañacahi» (errata también en el maestro). **F-Ā1A (ammā) y M+1 (addha) no
existen en el maestro de 2014**: son adiciones posteriores de los Google
Docs. El script del cotejo fue efímero (no quedó guardado); si vuelve a
hacer falta, se rehace en unos minutos con python-docx.

Del maestro puede sacarse más, aún no incorporado: **listas «De similar
declinación»** para los nombres (los Google Docs sólo las tienen en
pronombres y pañca) y las **partículas vocativas en negrita**.

## 7. TRABAJO ABIERTO

1. **Proponer y verificar** (el paso grande): derivar cada desinencia de
   base + sutta del Nāma-Kappa y conservar sólo lo que reproduce la forma
   atestiguada; lo que no cuadre se marca, no se publica. Banco de pruebas:
   las 2379 formas. Detectaría además las erratas de la sección 4.
2. **Táctil**: los tooltips (suttas, insignia de versión, casos en las
   filas) son de hover y **no funcionan en móvil/tablet**; los botones de
   filtro quedan pequeños para el dedo. Ver sección 8.
3. Opcionales sugeridos y no pedidos: comparación de dos paradigmas lado a
   lado, salto a la celda que coincide al buscar, conmutador ordinal ↔ caso
   latino, casilla «Estudiado» como en los capítulos.
4. Incorporar del maestro las listas «De similar declinación» (si IEBH
   quiere).

## 8. MÓVIL Y TABLET — estado honesto

La página es **responsive** (rejilla y tablas con desplazamiento horizontal,
barra lateral convertida en cajón con «☰», tipografía reducida a ≤640 px),
pero **no es plenamente táctil**: todo lo que depende de hover —tooltips de
§N, título de las filas con el caso, insignia de versión— no aparece al
tocar, y los botones de filtro (10px) quedan por debajo del tamaño de pulsación
recomendado. Arreglo natural: primer toque muestra el tooltip, segundo
navega; y agrandar las zonas de toque en pantallas estrechas. Pendiente.

## 9. RECORDATORIOS QUE NO CAMBIAN

- Nunca se edita nada dentro de `site/` (salvo `site/assets/pali.css`, que
  es fuente); el hook de pre-commit regenera y añade.
- Lo tomado de Thitzana o Rūpasiddhi se señala como suyo; la flecha de
  Thitzana va al revés.
- Ante duda, `<!-- DUDA: … -->` y decirlo en voz alta.
- Nada se añade, quita ni cambia respecto de la edición base sin avisar y
  sin que IEBH decida.
