# Visuddhāyuṃ ↔ clasificación del sitio: cotejo de la clase de sutta (2026-10-03)

**Alcance.** Solo lectura: no se ha tocado `recursos/clasificacion/`.

**Corrección del 2026-10-03 (sesión 2 de Nāma):** en §90 la (ခ) dice «အန္တရင်» (antaraṅga); la fila decía «sin etiqueta». Decisión del IEBH: antaraṅga / bāhiraṅga / ubhayaṅga van en «Clase de sutta» cuando el libro los da como rótulo, sin nota de diferencia con datos.json (es otro eje, no una contradicción).

**Método.**

- Para cada sutta se recortó en la imagen el encabezado y la apertura de (ခ), o la línea que da la clase.
- «datos.json ahora» se toma del `recursos/clasificacion/datos.json` actual (v0.6), no de los antiguos `claude/clasificacion_cap*_data.py.txt`.
- **Marcas:** [V] = leído en la imagen; ? = no confirmado.
- **Comparación:** «sin etiqueta» = el libro no da clase en las líneas leídas; «coincide» / «difiere» compara lo que dice el libro con datos.json.
- Este cotejo no recomienda cambios: pendiente de revisión del IEBH.

## Sandhi

| § | N.º libro | PDF | Texto del libro (tal como está impreso) | Traducción literal | datos.json ahora | Resultado |
|---|---|---|---|---|---|---|
| 1 | 1 | 52 | «…ဟူသော ပရိဘာသာသုံးမျိုးတို့တွင် အနင်္ဂါတည်း။ (သညင်၊ အနင်၊ ဝိဓိယင်၊ သုံးအင်ပရိဘာ)။ ဥပရိဘာသာ(မြစ်) ပရိဘာသာ (မမြစ်) နှစ်မျိုးတွင် ပရိဘာသာတည်း။» [V] | «Among the three kinds of paribhāsā … it is anaṅga (saññaṅga, anaṅga, vidhyaṅga: the three-aṅga paribhāsā). Of the two kinds, upari-bhāsā (blocking) and paribhāsā (not blocking), it is paribhāsā.» | X (fuera de las cuatro clases; Rū: abhidheyyappayojanavākya) | **difiere** |
| 23 | 23 | 79 | Apertura de (ခ): «(၁) သရာ၊ (၂) ဗျဉ္ဇနေ-အင်္ဂါနှစ်ပါး။ ဗျဉ္ဇနေ ကား ဗျည်းကြောင့်ဟု ပေးသောကြောင့် ပကတိ၏ နိမိတ်…» [V] | «(1) sarā, (2) byañjane: two aṅga. Because byañjane gives "because of a consonant", it is the nimitta of the pakati…» | V · ādesa (grupo pakati) | sin etiqueta |
| 24 | 24 | 80 | «…ဒုတိယပိုင်း တစ်ပိုင်းလုံးကို မြစ်သောသုတ် ဖြစ်၍…» [V] (v0.2) | «…being the sutta that blocks the whole second part…» | V · ādesa (grupo pakati); nota: la Bhāsāṭīkā lo llama paṭisedha-vidhi-sutta | **difiere** (ādesa frente a «sutta que impide»); coincide con la nota de la Bhāsāṭīkā |
| 28 | 28 | 85 | «ဤသုတ်သည် သဒိသာသဒိသဒွေဘော် ၂-မျိုးလုံးကို စီရင်သောသုတ်တည်း။ အနန္တရသုတ်ကား- ဈလပါရဿံ ကဲ့သို့ နိယမသုတ်တည်း။» [V] | «This sutta is the sutta that arranges both kinds of doubling, like and unlike. The next sutta is a niyama sutta, like "jhalapā rassaṃ".» | V · āgama (nota: dvebhāva no está entre las ocho vidhis) | sin conflicto: el libro no da la clase de vidhi; describe la función. Para §29 el libro dice niyama, como la nota de datos.json |
| 30 | 30 | 89 | «ဤသုတ်သည်-ဝဂ္ဂန္တံ ဝါ ဝဂ္ဂေ၊ ဧဟေဉံ (တစိတ်)၊ သယေစ၊ ဗျဉ္ဇနေစတို့ကို မြစ်သောသုတ်တည်း။ ဧဟေဉံ (တစိတ်) မဒါသရေ-တို့ကို 'အံ နိဂ္ဂဟီတံ' ဟူသော ဒွိဓာကရဏသုတ်ဖြင့်မြစ်။» [V] | «This sutta is the sutta that blocks vagganta vā vagge, ehe ñaṃ (in part), saye ca and byañjane ca. Ehe ñaṃ (in part) and madā sare are blocked by the split-off sutta "aṃ niggahītaṃ".» | V · ādesa (v0.6, a partir de la Kaccāyanavaṇṇanā; nota: apavāda, Rū 58) | **⚑ difiere: ver abajo** |
| 51 | 51 | 111 | «ဤသည် သုတ္တာတိဒေသတည်း။ သုတ္တာတိဒေသ ဟူသည် ဆိုအပ်ပြီးသော သုတ်များကို ပြန်၍ညွှန်းသည်။» [V] | «This is a suttātidesa. Suttātidesa means referring back to suttas already stated.» | V · ādesa (grupo atidesa; nota: la atidesa es clase propia en el esquema de seis) | **difiere** en la etiqueta de vidhi; coincide con el grupo atidesa |

### ⚑ §30

**El libro (PDF 89):**

- Lo presenta como el sutta que impide §31 (vagganta vā vagge), §32 en parte (ehe ñaṃ), §33 (sa ye ca) y §39 (byañjane ca).
- Añade que «ehe ñaṃ» (en parte) y §34 (madā sare) quedan impedidos por la forma separada «aṃ niggahītaṃ» del mismo sutta.

**El libro (PDF 79–80), dentro de la explicación de §23:**

- Texto: «…ဒီဃံ၊ ရဿံ၊ လောပဉ္စ တတြာကာရော-တို့၌ (စတုတ္ထပိုင်းဆိုင်ရာ နိဂ္ဂဟီတသန္ဓိ၌ 'အံဗျဉ္ဇနေ နိဂ္ဂဟီတံ' ဟူသော ပတိသေဓ (ပကတိ)ဝိဓိ ရှိသေးသည်ကို သတိရစေ)…» [V]
- Traducción literal: «…in dīghaṃ, rassaṃ, lopañca tatrākāro (and, in the niggahīta-sandhi of the fourth part, remember that there is also the paṭisedha (pakati) vidhi "aṃ byañjane niggahītaṃ")…».
- **La frase «ပတိသေဓ (ပကတိ)ဝိဓိ» se refiere a §30, no a §24.** El libro mismo une pakati y paṭisedha, y lo hace a propósito de §30.

**datos.json v0.6:** V · ādesa, con nota de apavāda (Rū 58).

Se registran las dos posiciones, sin veredicto. La página del análisis lleva ahora en §30 la nota «Clasificación del sitio: vidhi (ādesa)» (v0.2.2).

## Decisión A pospuesta: liṅga-vacana y nipātana

**Números del libro confirmados en la imagen por sus encabezados.** La concordancia inferida por recuentos (Samāsa −172, Taddhita −172) se cumple en los siete casos.

**§320** se leyó en sus líneas de apertura, que ya dan la clase. Las secciones de **§321, §322, §391, §394 y §395** se leyeron enteras en la imagen. **§323** es larga (PDF 400–402): se leyeron en la imagen todos los pasajes en que el OCR encuentra un término de clase, y el resto solo se cribó por OCR.

| § | N.º libro | PDF | Encabezado / apertura de (ခ) | Traducción literal | datos.json ahora | Resultado |
|---|---|---|---|---|---|---|
| 320 | 492 | 398 | «(၄၉၂) သော နပုံသကလိင်္ဂေါ။ ဒွိပဒံ။» — (ခ): «ဤသုတ်အစီအရင်သည် ကာရိယာတိဒေသ မဟုတ်။ ဧကတ္တ နပုံသက လိင်ကာရိယ (ဝိဓိ) တည်း။» [V] | «The procedure of this sutta is not a kāriyātidesa. It is the operation (vidhi) of singular and neuter gender.» | V · ādesa (grupo liṅga; nota: Nyāsa lo llama atidesa) | sin conflicto con ādesa-como-vidhi; **contradice expresamente la lectura de Nyāsa** (atidesa) que cita la nota |
| 321 | 493 | 398–399 | «(၄၉၃) ဒိဂုဿေကတ္တံ။ ဒွိပဒံ။» — sección leída entera: sentido de digu, samāhāra (singular) frente a asamāhāra (plural) [V] | — | V · ādesa (liṅga) | sin etiqueta en toda la sección |
| 322 | 494 | 399–400 | «(၄၉၄) တထာ ဒွန္ဒေ ပါဏိတူရိယ--။ စတုပ္ပဒံ။» — sección leída entera: gāthā mnemónica, significados de las clases de dvanda, Moggallāna [V] | — | V · ādesa (liṅga) | sin etiqueta en toda la sección |
| 323 | 495 | 400–402 | «(၄၉၅) ဝိဘာသာ ရုက္ခ တိဏ ပသု-။ တိပဒံ။» — sección revisada por los pasajes que el OCR marca con «နိယမ»; en ninguno es la clase del sutta: «…ရှေ့သုတ်လာ ဒွန်တို့၌လည်း နပုံသကေကတ္တနိယမသည် ဧကန္တ မဟုတ်ပေ။» y «ဤ၌ ဒွန်ပုဒ်တို့၏ ပုဗ္ဗာပရ နိယမကို ဆိုကြ၏။» [V] | «…so even in the dvandas of the previous sutta the restriction to neuter singular is not absolute.» / «Here they speak of the restriction (niyama) on the order of the dvanda members.» | V · ādesa (liṅga) | sin etiqueta de clase; «niyama» = restricción de género y número, y del orden de los miembros. Resto de la sección: cribado por OCR, no leído en la imagen |
| 391 | 563 | 487 | «(၅၆၃) ယဒနုပပန္နာ နိပါတနာ သိဇ္ဈန္တိ။ စတုပ္ပဒံ။» — sección leída entera (10 líneas): ejemplos (hatthikā …); formas «que no tienen uso, regla ni instrucción en la Pāḷi, las aṭṭhakathā y las ṭīkā» [V] | — | V · ādesa (grupo nipātana; uno de los cuatro suttas universales) | sin etiqueta en toda la sección |
| 394 | 566 | 488 | «(၅၆၆) ယာဝ တဒုတ္တရိ ဒသဂုဏိတဉ္စ။ တိပဒံ။» — la sección entera es: «အဓိပ္ပါယ်ကို စာကိုယ်၌ အကျယ်ပြအပ်ပြီ။» [V] | «The meaning has already been shown at length in the text itself.» | V · ādesa (nipātana) | sin etiqueta en toda la sección |
| 395 | 567 | 488 | «(၅၆၇) သကနာမေဟိ။ ဧကပဒံ။» — no hay comentario; sigue (၅၆၈) [V] | — | V · ādesa (nipātana) | sin (ခ) |

## Nāma (11 suttas marcados en las notas de datos.json)

**Método:**

- Número del libro = § hasta §232; = § − 1 desde §234.
- Cada número se confirmó en la imagen por su encabezado.
- (ခ) se leyó solo hasta la frase de clase, o entera cuando es corta.

| § | N.º libro | PDF | Texto del libro (tal como está impreso) | Traducción literal | datos.json ahora | Resultado |
|---|---|---|---|---|---|---|
| 65 | 65 | 123 | «(၆၅) တတော သဿ ဿာယ။ … တိပဒံ။» — (ခ): solo aṅga y funciones (tato: nimitta; sassa: kārī; ssāya: kāriya; vā: su visesana) [V] | — | V · ādesa (nota: Nyāsa lo llama apavāda del §179) | sin etiqueta (la sesión 2 de Nāma lee al final de la lista de rasgos «ဗဟိရင်ဝိဓိ», bāhiraṅga-vidhi: otro eje, véase la corrección arriba) |
| 83 | 83 | 133 | «(၈၃) သရလောပေါ မာဒေသ-။ … ပဉ္စပဒံ။» — (ခ): «ဥဘယင် (လောပ-အန္တရင်၊ ပကတိ-ဗာဟိယင်)။ အင်္ဂါ ၂-ပါး။ အမာဒေသပစ္စယာဒိမှိ-နိမိတ်။ သရ-ကာရီ။ လောပေါ-ကာရိယ။» [V] | «Ubhayaṅga (the lopa is antaraṅga, the pakati bāhiraṅga). Two aṅga. "aṃ-ādesa-paccayādimhi": nimitta. "sara": kārī. "lopo": kāriya.» | V · lopa + ādesa (grupo pakati; nota: Rū 67, apavāda del §13) | sin etiqueta de apavāda; **ubhayaṅga** va en «Clase de sutta» (decisión del IEBH, 2026-10-03), sin nota de diferencia |
| 85 | 85 | 135 | «(၈၅) န သိသ္မိံ မနပုံသကာနိ။ … တိပဒံ။» — (ခ): «အဃောရဿ-၌ ပတိသေဓအပိအရ သရုပ်ပြ၍ နေရာချသော နိယမသုတ်တည်း။» [V] | «It is a niyama-sutta that, showing in its own form the "api" of prohibition in "agho rassaṃ…" (§84), assigns it its place.» | V · paṭisedha (nota: niyama según Rū 150, Nyāsa, Bhāsāṭīkā, U Sīlānanda) | **coincide con la nota** (niyama); la vidhi «paṭisedha» no se contradice |
| 90 | 90 | 137–138 | «(၉၀) ပဉ္စာဒီနမတ္တံ။ … ဒွိပဒံ။» — (ခ): «သုနံဟိသုစ ဖြင့် နံကြောင့်ဒီဃ၊ သုဟိသွ-ဖြင့် သုဟိကြောင့် ဧပြုကိုပြသည်။ အန္တရင်။ နိမိတ်စသည်ခွဲ။ တိလိင်။ သချာ ၁၁-ပုဒ်။ သဗ္ဗနာမ်ဂိုဏ်း။» [V] | «…shows the lengthening before naṃ (by "sunaṃhisu ca") and the e before su, hi (by "suhisv a"). Antaraṅga. Analyse the nimitta, etc. Three genders. Numerals: 11 words. Sabbanāma group.» | V · ādesa (nota: apavāda, Rū 252) | **antaraṅga** (corregido el 2026-10-03; antes «sin etiqueta en las líneas leídas»); otro eje, no contradice ādesa |
| 134 | 134 | 156 | «(၁၃၄) ပဉ္စာဒီနမကာရော။ … ဒွိပဒံ။» — (ခ), entero: sobre qué numerales son «pañcādi» [V] | — | V · ādesa (nota: apavāda del §107) | sin etiqueta |
| 187 | 187 | 180 | «(၁၈၇) သေသေသု န္တုဝ။ … တိပဒံ။» — (ခ): «ဂုဏဝါဒိကိုဏ်း အစီအရင်ရောက်ရန် န္တုကို နှုပြုသည်။ သေသေသုဆိုသော်လည်း န္တော၊ တော၊ တိ၊ တာ၊ တံ-စသော ဝိသေသဝိဓိ မရှိသည့်အရာ ဥကို အ-ပြန်ပြုရဦးမည့်အရာတို့၌ နှုမင့်ပဲထားသည်က သာ၍ကောင်း၏။» [V; la palabra «နှု» es ?] | «So that it follows the procedure of the guṇavant group, it makes [nta] (like?) ntu. Although it says "sesesu", where there is no special vidhi such as nto, to, ti, tā, taṃ, and where the u would have to be turned back into a, it is better to leave it [as nta].» | V · ādesa (grupo atidesa; nota: Rū 108 kāriyātidesa) | sin término de clase; describe el efecto «como ntu», compatible con la nota de atidesa |
| 203 | 203 | 184 | «(၂၀၃) ဥ သသ္မိံ သလောပေါ စ။ … စတုပ္ပဒံ။» — solo el modelo (က); no hay (ခ) [V] | — | V · ādesa + lopa (nota: apavāda del §200) | sin (ခ) |
| 227 | 227 | 196 | «(၂၂၇) ကိဿ က ဝေ စ။ … စတုပ္ပဒံ။» — solo el modelo (က); no hay (ခ) [V] | — | V · ādesa (nota: Nyāsa llama niyama a «ve») | sin (ခ) |
| 229 | 229 | 197 | «(၂၂၉) သေသေသု စ။ … ဒွိပဒံ။» — (ခ), entero: una cita pāḷi («ettha ca kissa ka ve cāti sutte …») y «ကစ္စည်းဝုတ္တိသို့ မလိုက်။» [V] | «…does not follow the Kaccāyana-vutti.» | V · ādesa (nota: niyama según Nyāsa) | sin etiqueta |
| 245 | 244 | 205 | «(၂၄၄) ဈလပါ ရဿံ။ … ဒွိပဒံ။» — (ခ): «…ရဿံဖြင့် ကာရီ၌ အ၊ ဥ မပါဟု သိရ၏။ အဃောရဿ-ဖြင့် ဂနောင်းရာ ပြုရမည့် ကာရီများကို နိယမပြုသည်။» [V] | «…By "rassaṃ" we know that a and u are not among the kārī. It makes a niyama of the kārī that must be [shortened] where ga follows, by "agho rassaṃ…".» | V · rassa (nota: niyama, en el sentido de especificar) | **coincide con la nota** (niyama); la vidhi «rassa» no se contradice |
| 270 | 269 | 212 | «(၂၆၉) အမှ၊ တုမှ၊ န္တု၊ ရာဇ-- … စတုပ္ပဒံ။» — solo el modelo (က); luego «ပဉ္စမပိုင်းပြီး၏။» [V] | «…The fifth part is finished.» | V · ādesa (nota: dos lecturas, atidesa o ādesa) | sin (ခ) |

**Resumen Nāma:**

- El libro usa término de clase en **§85** y **§245** («နိယမ», niyama), en los dos casos de acuerdo con las notas de datos.json.
- En **§90** rotula el sutta «antaraṅga» (corregido el 2026-10-03), y en **§83** «ubhayaṅga» (lopa antaraṅga, pakati bāhiraṅga): otro eje, sin contradicción con datos.json; ninguno dice apavāda.
- En **§187** describe un efecto «como ntu», sin dar término.
- **§203, §227 y §270** no tienen (ခ).
- En ninguno de los 11 aparece «apavāda» ni «atidesa» en las líneas leídas.
- Nada de esto afecta a la página del análisis (solo Sandhi), que sigue en v0.2.2.

## Pakati: resumen de fuentes (para el IEBH)

- **El sitio (datos.json v0.6):**
  - Sigue a Thitzana, que pone la pakati dentro de la ādesa: §23 y §24 = V · ādesa, grupo pakati.
  - Referencia: nota de §23 en datos.json (Thitzana, vol. 2, introducción). Véase también `claude/vuddhi-y-las-ocho-vidhis.md`.
- **La Visuddhāyuṃ:**
  - Llama a §30 «ပတိသေဓ (ပကတိ)ဝိဓိ» (PDF 79–80, dentro de la explicación de §23), y a §30 «sutta que impide» §31–§33 y §39 (PDF 89).
  - Describe §24 como «sutta que impide todo el segundo pariccheda» (PDF 80).
- **La Bhāsāṭīkā:** llama a §24 «paṭisedha-vidhi-sutta» (citada en la nota de §24 de datos.json).
