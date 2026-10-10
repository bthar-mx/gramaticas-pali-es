# Dhātvatthasaṅgaha-nissaya — piloto de OCR (sesión 64, 2026-10-10)

Dos hojas, elegidas para cubrir los dos tipos de página que importan:

| hoja PDF | página | qué es | renglones | caracteres |
| ---: | ---: | --- | ---: | ---: |
| 20 | 5 | texto pāḷi solo: versos ၃၈–၄၈ del kaṇḍa de *k-* | 25 | 863 |
| 65 | 51 | nissaya: verso ၃ y las entradas *akka, akkha, agga, agi, aṅga* | 25 | 1.004 |

**La transcripción de control es lectura de Claude sobre la imagen**, no de
un segundo testigo. Donde dudo lo digo abajo (§4); un error mío en el control
cuenta como error del OCR, de modo que las cifras pecan, si acaso, de
pesimistas. Las dos transcripciones están en
`~/Tipitaka/nissaya/ocr/dhatvatthasangaha-nissaya/_work/piloto/NNN.gt.txt`,
**fuera del repositorio**: son texto del libro, y los derechos están por
decidir.

## 1. Resultado

CER = distancia de edición entre el OCR y el control, sin espacios, dividida
por la longitud del control. Las comillas tipográficas se igualan antes.

| método | modelo | hoja 20 (versos) | hoja 65 (nissaya) |
| --- | --- | ---: | ---: |
| página entera, `--psm 6` | myap | 27,2 % | 39,6 % (×0,75) |
| página entera, `--psm 4`, ×0,75, sin renglones de basura | myap | 9,4 % | 25,3 % |
| página entera, `--psm 6`, ×0,75, sin basura | myab | 23,1 % | 48,2 % (×1) |
| **renglón a renglón, `--psm 7`, ×0,75** | **myap** | **4,9 %** | **3,0 %** |
| renglón a renglón, `--psm 7`, ×1 | myap | 6,5 % | — |
| renglón a renglón, `--psm 7`, ×0,75 | myab | 17,3 % | — |

Con el método elegido:

- **renglones**: la segmentación acierta los 25 de cada hoja, sin uno de más
  ni de menos — el problema de la página entera era justamente ése;
- **renglones exactos**: 8 de 25 en la hoja de versos, 14 de 25 en la de nissaya;
- **palabras** (WER, con ’ y espacios contados): 21,4 % y 14,3 %;
- **raíces del margen del nissaya** (lo que más importa para `raices.json`):
  **3 de 5 exactas** — *အဂ’ဂ္ဂါ* sale sin el apóstrofo y *အဂိ* sale *အဝိ*.

El modelo `myap` (el de pndaza, afinado para nissaya) gana en todo. `myab`
(tessdata_best) no aporta; en este libro no sirve ni de segundo voto.

**Por qué renglón a renglón.** Con la página entera, Tesseract toma los
subíndices y las vocales altas de los apilados birmanos por renglones propios y
devuelve líneas como «က ခု) ၁» que no están en la página: de ahí los 20-40
puntos de diferencia entre «bruto» y «sin basura». Cortando antes los renglones
por proyección horizontal, y fundiendo cada banda baja con su vecina, eso
desaparece. Es `herramientas/dhatvatthasangaha/ocr.py`.

## 2. Qué errores quedan

En orden de frecuencia, en las dos hojas:

1. **El apóstrofo de elisión (’) se pierde siempre**: 9 de 9 —
   *lolicchā* por *loli’cchā*, *aggā* por *aga’ggā*, *saṅkhyānaṅkesu* por
   *saṅkhyāna’ṅkesu*—. Es sistemático y, por tanto, reparable: el verso
   repetido en el nissaya y el índice final dan la forma.
2. **Consonantes apiladas**, la segunda causa: *က္က* sale *တ္က*, *တ္တ* o
   *ကတ္က* (seis veces entre las dos hojas); *ဗ္ဗ* → *မ္ဗ*, *ပ္ပ* → *မ္ပ*;
   un *ဋ္ဌ* desaparece.
3. **Confusiones de letra**, pocas: *ဂ/ဝ*, *ဃ/ယ*, *ထ/ယ*.
4. **El número del verso** en grande al principio de renglón se lee mal 2
   veces de 11 (*ဒ၃ု၈* por *၃၈*); la serie es correlativa y se reconstruye.
5. **Signos menores**: *၊* perdido en mitad de renglón, *ု* perdido o
   sobrante, *ံ့* por *ှ*.

Ningún error toca la estructura: renglón de verso, renglón de entrada con su
raíz al margen y nota entre corchetes se distinguen bien por la sangría (las
coordenadas de cada renglón quedan guardadas).

## 3. Qué propongo para el libro entero

**Proponer y verificar, como en el sandhi.** El libro trae cada raíz hasta
**tres veces**, y eso es lo que permite no fiarse de un solo OCR:

1. en el **verso** del texto pāḷi (pp. 1-45);
2. en el **mismo verso repetido** en el nissaya, encima de sus entradas;
3. en la **entrada**, al margen, en negrita.

Una raíz se da por leída cuando los tres testigos coinciden. Si no, va a una
cola de revisión con el recorte de imagen al lado, como se hizo con el
Visuddhāyuṃ ([V] sólo lo visto). Con un 3-5 % de CER, la mayoría de las
raíces debería pasar por coincidencia; el resto es trabajo de ojo, acotado.

El índice alfabético (pp. 405-552) da además, para cada palabra, la página
donde se explica: es un cuarto testigo para la raíz y la llave de la cita.

Coste: unos 15 s por hoja en la VM; el libro entero, ~2 h y media. **No se ha
lanzado**: espera el visto bueno del IEBH al piloto.

## 4. Mis dudas en el control

- Hoja 20, v. ၃၉: *ဇုတေ* (jute) — el ု se ve; ninguno de los dos modelos lo
  lee. Lo dejo.
- Hoja 20, v. ၄၀: *ကဌော* y *ကဋ္ဌိ* — leo ဌ y un apilado bajo el segundo; el
  OCR da *ကဋော* y *ကိ*. No lo aseguro.
- Hoja 20, v. ၄၂: había escrito *ကဎ္ဎော အာကဎ္ဎေ*; el OCR leía *ကဍ္ဎော
  အာကဍ္ဎေ* (kaḍḍha, ḍ + ḍh), que es lo correcto. Corregido en el control antes
  de medir. Es el recordatorio de que el control también se equivoca.
- Hoja 65: *ပင်္ဂနာ-ဟု* — hay un punto bajo la ā que no identifico.

## 5. La corrida completa (misma sesión, con el visto bueno del IEBH)

Decisiones del IEBH al ver el piloto (2026-10-10): **adelante con el libro
entero**; el sitio publicará **raíz, sentido y referencia**, y el texto del
nissaya queda en local; **romanización CST/OSBCT** (la de
`herramientas/nyasappadipika/my2rom.py`); **el sentido, en birmano por ahora**,
y el español en una pasada aparte, firmada.

Hechas las hojas 16-407 (392) con `ocr.py`; `extraer.py` saca versos y
entradas a `docs/fuentes/dhatvatthasangaha/datos.json` (en `.gitignore`).

| | resultado |
| --- | --- |
| versos del texto pāḷi | **445**, numerados; el número leído coincide con la serie en 409 |
| versos repetidos en el nissaya | 432 de 445 (los que faltan, renglón mal leído) |
| entradas (raíces) | **1.614**; el libro declara **1.637** en sus cierres de kaṇḍa |
| kaṇḍa 4 | 177 = 177 |
| kaṇḍa 5 | 265 / 266 |
| kaṇḍa 3 | 161 / 159 |
| kaṇḍas 1-2 | 267 / 277 |
| kaṇḍa 6 | 309 / 316 — **las pp. 262-263 que faltan** |
| kaṇḍa 7 | 435 / 442 |
| tres testigos coinciden | 1.173 |
| tres testigos y la raíz existe en el Saddanīti | 719 |

**Lo que los números no dicen y hay que saber.** Los tres testigos los lee el
mismo OCR, y un mismo glifo impreso se lee mal igual en los tres sitios:
*အဂိ* (agi) sale *အဝိ* en el margen, en el verso del nissaya **y** en el del
pāḷi. Coincidir es necesario, **no suficiente**. Por eso hay un cuarto testigo,
externo: que la raíz exista en el Saddanīti o en el Dhātupāṭha. Pero ése
tampoco basta solo, porque el Dhātvatthasaṅgaha trae raíces que las otras
obras no tienen (*aṅga* de curādi junto a *agi*). **Nada de esto se publica
sin verlo en la imagen**: la cola, en `docs/fuentes/dhatvatthasangaha/revision.md`.

## 6. Verificación en la imagen (sesión 65, 2026-10-10)

Todas las raíces, miradas en la imagen: hojas de contacto de los renglones del
margen (2 × 14 recortes a resolución completa, con la lectura del OCR al lado),
y ampliación de cada caso dudoso. Resultado y tabla en
`docs/fuentes/dhatvatthasangaha/verificacion.md` (local).

| | |
| --- | ---: |
| renglones del margen mirados (hojas 61-407) | 1.915 |
| entradas verificadas `V` | 1.574 |
| entradas que el extractor no había reconocido, `V-nueva` | 22 |
| de la séptima impresión (pp. 262-263 de la sexta), `V-7ª` | 10 |
| dudosas, `?` | 18 |
| **raíces** | **1.637 = el libro**, y cuadran los siete kaṇḍas |

**El OCR del margen se equivocaba en 350 de 1.592 entradas** (22 %), mucho más
que el 3 % de CER del nissaya: el margen va en negrita, más grande, y Tesseract
confunde ahí lo que en el cuerpo lee bien. Confusiones vistas, con la regla
para decidirlas en la imagen:

- ဋ (gancho a la izquierda arriba) / ဍ (arco liso);
- ဂ (abierta abajo a la izquierda) / ဝ (cerrada);
- subíndices: စ redondo y cerrado, ဇ con gancho abierto, ဆ con un bucle más;
  ဗ redondo con muesca arriba, ပ una U, ဖ una U con rizo dentro;
- ဿ más ancha que သ; ီ anillo relleno, ိ anillo abierto;
- **ယ / ဃ: en esta negrita son la misma forma.** No se decide por la imagen;
  se ha dejado la lectura que favorecen el verso, el prayoga y el Dhātupāṭha
  sánscrito, marcada `?`. Son 16 y las decide el IEBH en el papel.

Por qué se le escapaban 22 entradas al extractor: renglones de entrada que no empiezan
por «RAÍZ၊ သည်» —la raíz en acusativo (*လာဘံ ကို … အဗြဝိ*), seguida de «iti
ca» (*ပိဉ္ဆောတိ စ*), de «tu» (*တဖော တု*)— o pegados a la nota anterior.
Una (*ဟိဝိ/ဟီ*, E1594) y un punto (E17) son las otras dos dudas.

**Lo que ya no vale de §5**: las cifras por kaṇḍa de esa tabla (267/277,
161/159…) eran del extractor; las buenas son las de este apartado.
