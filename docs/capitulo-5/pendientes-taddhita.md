# Taddhita (cap. 5): decisiones pendientes de la revisión

*Sesión 25 (continuación del 2026-09-13). El maestro es
`docs/5. Taddhita-Kappa.md`: la revisión del IEBH del 13 de septiembre,
con las correcciones mecánicas aprobadas ese día y las 248 referencias
canónicas reinyectadas desde la fuente (literales, tal como las imprime
Nandisena) y verificadas línea a línea. Lo de abajo es lo que quedó
**sin decidir**; nada de esto impide generar el capítulo, salvo el §6.*

## Decidido el 2026-09-13 (para el registro)

- «Fin del capítulo de derivados **secundarios**» (la fuente del error
  decía «primarios», que es kitaka).
- kāraka = «caso (kāraka)» en la vutti de §391: decisión del IEBH.
- «deviene» unificado al registro de la casa («se sustituye por», «se
  vuelven») en §380, §381, §403.
- Restituida como nota 41 la advertencia de que el título de §401 es el
  único que Nandisena deja sin traducir (su nota se había perdido en la
  exportación: quedaba un «14» suelto).
- Todas las erratas mecánicas de la lista del 13-09 (Vesamitttī→Vesamittī
  ya venía del IEBH; apacaṃ, Kapassa, bhaṇdaṃ ×5, āvuddho ×3, Saṃhassa,
  Sangha ×2, kuṅkumaṃ con viggaha de kasāva, «Bhaddena…» duplicado, el
  «de “sirasa”» duplicado del verso de §352, fecha→flecha, superíndices
  aplanados de §395, etc.).

## 1. Terminología por unificar (glosario)

- **gaṇana** aparece de tres maneras: «numerales» (§389), «conteo»
  (§391), «enumeración» (§389 kimatthaṃ, §393). Elegir una y fijarla en
  `comun/glosario.md`.
- **samūha** «conjunto» frente a **samuccaya** «colección» (heredado de
  la sesión 25; samuccaya ya está fijado por el Samāsa).
- La grafía **saṅkyā / saṅkhyā** vacila en la propia fuente (títulos de
  §373/§381 frente a vuttis de §379/§385/§395). Hoy el maestro conserva
  cada literal. ¿Se unifica? ¿En qué dirección?

## 2. §390, upapada — PROBABLE ERRATA DE TRADUCCIÓN

El título español dice que ‘tu’ se elide de «catu» como «la parte
**siguiente**», pero *upapada* está fijado en el glosario como «miembro
**precedente**», y en cuddasa/catuddasa «catu» precede. Además, la
traducción del ‘ca’ como «parte inicial **de la palabra**» (sin «del
miembro siguiente») coincide con la variante del Rūpasiddhi que registra
la propia nota 30 («Padādicakārassa (Rū)»), no con el texto de Nandisena
(«uttarapadādi-»). Si el IEBH mantiene esa lectura, merece nota que lo
diga; si fue descuido, corregir a «miembro precedente».

## 3. Glosas que son interpretación del IEBH (confirmar)

- §349: **sāmaṇeraṃ** «(familia de la novicia)» y **nāḷikeraṃ**
  «(familia del cocotero)» — Nandisena no glosa el neutro; «familia» no
  tiene fuente que lo respalde.
- §389: «dasadasakā purisā (hombres que tienen diez decenas **[de
  años]**)» — el inglés dice sólo «ten decads».
- §367: el viggaha «Muggā yassa **atthi** … vijjatī» lleva sujeto plural;
  el inglés de Nandisena imprime *santi / vijjanti*.

## 4. Notas de otros tratados: ¿traducirlas?

Propuesta del 13-09: las variantes puras —«Pattaṅgaṃ (Sī)»— quedan en
pāḷi como en el Nāma; las discursivas se dan en pāḷi íntegro seguido de
traducción entre paréntesis (modelo de los borradores del Samāsa).
Candidatas (numeración del maestro de hoy): **12** (Rū, §353), **17**
(Mog, §356), **26** (Rū y juicio editorial, §386), **43** (Rū y Sad,
§402), **49** (lectura cingalesa, §405). Falta el visto bueno del IEBH y
las traducciones mismas.

## 5. Referencias reinyectadas: siglas literales

Se reinyectaron **tal como las imprime la fuente**, incluidas las
anómalas: «a. iii, 101» (§344, minúscula), «V. ii, 11» (§345), «Vin.A.»
con punto interior (§367), «Vin ii, 11» sin punto (§400), «D. i, 82;
DA. i, 220-Sad. sutta 850» y «A. ii, 481-Sad. sutta 854» (§401, con
texto incrustado), «Khu. i, 381-piṭṭhesu pi passitabbaṃ» (§395). La
tabla de erratas de la sesión 25 propone normalizarlas (A., Vin., VinA.);
decide el IEBH. Sea cual sea la decisión, estas siglas faltan en el
`_SIGLAS` del emparejador para cuando se restituya la negrita.

## 6. Nota 34: enlace de Google Docs — RESUELTO EL 2026-09-13

La nota enlazaba a un documento privado de Google, que no puede salir
al sitio. El 13-09 se dejó la frase sin enlace y con «§391» enlazable
(«El sutta anterior, §391, es uno de los cuatro suttas universales de
la gramática de Kaccāyana»). Queda abierto si el documento de los
cuatro suttas universales se trae a `recursos/` para enlazarlo interno.

## 7. §377, el Rūpasiddhi «0»

Nandisena imprime «377. 0.» (sin correspondencia en el Rūpasiddhi).
Decidir cómo lo tratan `generar_capitulo.py`, `comun/concordancia.json`
y la página: ¿«0» literal, guion, omisión del segundo número?

## 8. Registrado, sin acción

- §352: el IEBH puso en mayúscula los nombres de las deidades (la fuente
  imprime «bhaddo, māro…» en minúscula) y añadió punto final a dos
  líneas pāḷi. Cambios deliberados sobre la base impresa; quedan aquí
  anotados por la regla de no cambiar nada sin avisar.
- §344: «Vesamittī» es la corrección del IEBH sobre «Vesamitttī» (la
  sesión 25 había propuesto «Vesāmittī»; manda el inglés de Nandisena,
  que imprime «Vesamittī»).
- La DUDA del verso de §352 quedó resuelta por el IEBH siguiendo el
  inglés de Nandisena («na vade»), con su nota aclaratoria (nota 10).
