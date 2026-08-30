# El criterio de categoría gramatical del IEBH, mecanizado y medido

*Generado por `herramientas/generar_informe_criterio_pos.py` — modo de la página (solo-canon + dpd-filtro), sobre las 5.000 formas más frecuentes del canon. Este informe PREPARA la firma; no adjudica nada: firmar el criterio es del IEBH.*

## El criterio y lo que hacía falta

Palabras del IEBH (briefing 35 §6): *«sattānaṃ is a noun, caranto is a present participle, cittaṃ is a noun. I can almost with 100 % confidence say that never caranto = ca + anto.»* De ahí: **si el diccionario da la forma entera como palabra con su categoría gramatical, no es sandhi proclítico.** En la sesión 35 no se pudo computar —el léxico de la carpeta era una lista de formas desnuda—. Ya se puede: `dpd-pos.tsv` trae 457.628 formas con categoría, y entre las categorías del DPD hay una que dice **«sandhi»**: 1.522 formas.

## Las dos formulaciones, que no son equivalentes

| | formulación |
| --- | --- |
| **(a) positiva** | afirmar sólo si el DPD registra la forma como «sandhi» |
| **(b) negativa** | descartar si la forma tiene cualquier categoría ajena |

Medidas sobre las **86 formas que el mecanismo espejo afirmaría**, con el testigo DPD de árbitro:

| criterio | conserva de las 14 correctas | deja pasar de las 9 falsas | de las 63 mudas | precisión |
| --- | ---: | ---: | ---: | ---: |
| (a) positiva | 14 | 4 | 1 | 77.8 % |
| (b) negativa | 6 | 1 | 0 | 85.7 % |
| **(a) + el testigo** | 14 | 0 | 1 | 100.0 % |

**La (b), que es la literal del enunciado, es la peor**: tira lecturas correctas porque una forma de sandhi corriente aparece además como otra cosa (cetaṃ es *masc* y *nt* aparte de *sandhi*). La (a) las conserva todas.

## El hallazgo: el criterio y el testigo son complementarios

Ni uno ni otro basta solo. Estas lecturas falsas el DPD **sí** las marca «sandhi» — reconoce que hay sandhi y descompone distinto:

| forma | frec. | la receta diría | el DPD (testigo) | categorías |
| --- | ---: | --- | --- | --- |
| yeva | 1.275 | yo + eva | y + eva | sandhi |
| sāpi | 538 | so + api | sā + api | adj, letter, masc, pron, sandhi |
| sāyaṃ | 410 | so + ayaṃ | sā + ayaṃ | adj, aor, ind, nt, pron, prp, sandhi |
| yāyaṃ | 265 | yo + ayaṃ | yā + ayaṃ | aor, pron, prp, sandhi |

La categoría no las puede cortar; la descomposición sí. **Juntas cortan las 9 falsas y conservan las 14 correctas.**

## El límite, que es serio: la etiqueta tiene 50 % de recall

Sobre las 18 respuestas YA adjudicadas de la clase, el DPD etiqueta «sandhi» sólo 9.

| forma | conocida | de dónde | ¿la etiqueta el DPD? | categorías |
| --- | --- | --- | --- | --- |
| anabhineyya | na + abhineyya | banco | **no** | ger, pr |
| cesā | ca + esā | caso adjudicado | **no** | — |
| cetā | ca + etā | caso adjudicado | sí | masc, nt, sandhi |
| ceva | ca + eva | caso adjudicado | sí | ind, letter, sandhi |
| cāti | ca + iti | caso adjudicado | **no** | ind, letter |
| cāyaṃ | ca + ayaṃ | caso adjudicado | sí | sandhi |
| cūbhayaṃ | ca + ubhayaṃ | banco | sí | sandhi |
| nayidaṃ | na + idaṃ | banco | sí | ind, sandhi |
| nayimassa | na + imassa | banco | **no** | — |
| netaṃ | na + etaṃ | caso adjudicado | **no** | pr, pron, prp |
| nopeti | na + upeti | banco | **no** | pr |
| nātivattati | na + ativattati | caso adjudicado | **no** | pr |
| sohaṃ | so + ahaṃ | banco | sí | sandhi |
| soyeva | so + eva | banco | **no** | adj, ind, letter, pron, suffix |
| svassa | so + assa | banco | **no** | — |
| sveva | so + eva | banco | sí | adj, ind, letter, pron, sandhi, suffix |
| svāyaṃ | so + ayaṃ | caso adjudicado | sí | sandhi |
| yvāyaṃ | yo + ayaṃ | banco | sí | sandhi |

Deja fuera netaṃ, cāti y nātivattati —adjudicadas por el propio IEBH—. De modo que la etiqueta sirve de **licencia** (lo que marca, casi seguro es sandhi) y **no de prueba de verdad** (lo que no marca puede serlo igualmente). Usarla como puerta única silenciaría sandhis reales, y por eso el informe no la propone como tal.

## Lo que el criterio combinado dejaría pasar

| forma | frec. | lectura | el testigo | categorías |
| --- | ---: | --- | --- | --- |
| neva | 3.404 | na + eva | coincide | ind, masc, prefix, sandhi |
| cettha | 2.140 | ca + ettha | coincide | sandhi |
| cassa | 1.544 | ca + assa | coincide | letter, sandhi |
| nāhaṃ | 1.231 | na + ahaṃ | coincide | sandhi |
| cetaṃ | 1.038 | ca + etaṃ | coincide | masc, nt, sandhi |
| nāpi | 688 | na + api | coincide | ind, masc, prefix, sandhi |
| cāpi | 683 | ca + api | coincide | ind, letter, sandhi |
| nāyaṃ | 529 | na + ayaṃ | coincide | pron, sandhi |
| cito | 453 | ca + ito | calla | pp, sandhi |
| napi | 417 | na + api | coincide | ind, masc, prefix, sandhi |
| nāssa | 344 | na + assa | coincide | opt, sandhi |
| cāhaṃ | 237 | ca + ahaṃ | coincide | sandhi |
| svāhaṃ | 183 | so + ahaṃ | coincide | sandhi |
| cesa | 162 | ca + esa | coincide | sandhi |
| caññe | 159 | ca + aññe | coincide | sandhi |

