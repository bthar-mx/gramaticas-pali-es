# -*- coding: utf-8 -*-
# Términos gramaticales pāḷi que NO están entre los 1.984 lemas del glosario
# (Nandisena + Smith + normativos, variantes incluidas), cosechados de
# Kaccāyana (8 capítulos, trad. Nandisena), Rūpasiddhi (7 capítulos), Nyāsa
# (texto pāḷi completo, OCR) y Kaccāyana vol. 2 de Ven. A. Thitzana (cuerpo e
# índice). Las cifras son apariciones del tema en cada fuente. ES/EN son
# PROPUESTAS; decide el IEBH. Sesión 57.
import json, sys
A = json.load(open('/sessions/gallant-lucid-bell/mnt/outputs/tanda2/atestig.json'))
R = []
def t(termino, es, en, com='', tipo='término', ref='', fuentes=None):
    R.append({'id': termino, 'termino': termino, 'tipo': tipo, 'es': es, 'en': en,
              'comentario': com, 'ref': ref, 'fuentes': fuentes if fuentes is not None else A.get(termino, {})})

# ---- 1. Términos de la doctrina ------------------------------------------
t('sādhana', 'sādhana; modo de formación (de un derivado primario, según el kāraka que expresa)',
  'sādhana; mode of derivation (of a primary derivative)',
  'Thitzana lo usa 379 veces y le dedica un apéndice («Kāraka & Sādhana»): kattu-, kamma-, bhāva-, karaṇa-, sampadāna-, apādāna-, adhikaraṇa-sādhana. Ñāṇamoli p. 12 traduce bhāvasādhana «definition by way of state». Nandisena tiene bhāva-sādhana dentro de assapada-viggaha pero no sādhana suelto.',
  ref='Kacc. §… Kibbidhāna; Thitzana, Appendix «Kāraka & Sādhana»')
t('saralopa', 'elisión de vocal', 'vowel elision',
  'La operación más frecuente de la Rūpasiddhi y del Nyāsa («saralopo», 509 apariciones). lopa → «elision» es N-EN.', ref='Rū. §… ; Kacc. §12')
t('savibhatti', 'con (su) inflexión; con la desinencia', 'with its inflection',
  'Fórmula de la Rūpasiddhi y del Nyāsa: «savibhattissa» = de la voz junto con su desinencia. vibhatti → «inflection» es la norma.', ref='Rū. passim')
t('avibhatti', 'sin inflexión', 'without inflection', 'Pareja de savibhatti. Nandisena tiene avibhattiyutta, no avibhatti.', ref='Rū.; Nyāsa')
t('asaṃyoganta', 'que no termina en consonante conjunta', 'not ending in a conjunct consonant',
  'N-EN, Kibbidhāna §973: «of not a conjunct consonant» (asaṃyogantassa). Condición de la vuddhi.', ref='Kacc. §… (asaṃyogantassa vuddhi kārite)')
t('saṃyoganta', 'que termina en consonante conjunta', 'ending in a conjunct consonant', 'Pareja de la anterior.', ref='Kacc.; Rū.')
t('dhātvanta', 'final de la raíz', 'root-final (letter)',
  '391 apariciones; «dhātvantassa» abre decenas de reglas de sustitución.', ref='Kacc. Ākhyāta y Kibbidhāna, passim')
t('dhātvantalopa', 'elisión de la final de la raíz', 'elision of the root-final', 'Compuesto de la anterior con lopa; 74 apariciones.', ref='Kacc.; Rū.')
t('pakatibhāva', 'estado natural; forma original (no alterada)', 'natural state; original form',
  'N-EN traduce pakati «original form» en Sandhi §23-24. En el Nyāsa, «saralopa-pakatibhāvādi» es la fórmula de las operaciones que no ocurren.', ref='Nyāsa, passim')
t('pubbasara', 'vocal precedente', 'preceding vowel', 'Pareja de parasara. Nandisena tiene pubba y para sueltos como partes de compuestos, no estos dos.', ref='Kacc. Sandhi; Nyāsa')
t('parasara', 'vocal siguiente', 'following vowel', '', ref='Kacc. Sandhi; Nyāsa')
t('parakkhara', 'letra siguiente', 'following letter', 'Nyāsa 39. Pareja pubbakkhara (4).', ref='Nyāsa')
t('napuṃsaka', 'neutro; (género) neutro', 'neuter', 'Ñāṇamoli p. 6 da napuṃsakaliṅga «neuter gender»; el glosario tiene napuṃsakaliṅga como parte de compuestos de Smith, no napuṃsaka suelto, que es como lo escribe Kaccāyana (§…, «napuṃsake»).', ref='Kacc. Nāma')
t('adhikicca', 'tomando como regla regente; bajo el adhikāra de', 'governed by (the adhikāra of); having taken as governing rule',
  'Fórmula de la Rūpasiddhi y del Nyāsa: «“X” ti adhikicca …» = rigiendo la regla X. Es el absolutivo de adhi-kar; va con la entrada adhikāra de Nandisena.', ref='Rū. passim')
t('anuvatti', 'continuación (de una regla anterior)', 'continuation (of a previous rule)',
  'Nandisena tiene el verbo (anuvattati) y anuvattana-vutti, no el sustantivo, que es el que usan Rūpasiddhi y Nyāsa (40).', ref='Rū.; Nyāsa')
t('antalopa', 'elisión de la final', 'elision of the final', '', ref='Kacc.; Rū.')
t('appayoga', 'falta de uso; no empleo (de una forma)', 'non-use; absence of use', 'Kacc. 8, Rū. 15: «nāmappayoge», «vuttatthānam appayogo» (fórmula de la Rūpasiddhi: lo ya dicho no se vuelve a emplear).', ref='Rū. passim')
t('niddiṭṭha', 'indicado; especificado', 'indicated; specified', 'Thitzana: «dhātu-niddiṭṭha affixes» (los sufijos indicados junto a la raíz).', ref='Nyāsa; Thitzana')
t('byākaraṇa', 'gramática', 'grammar', 'Título mismo de la obra (Kaccāyanabyākaraṇaṃ). El glosario tiene veyyākaraṇa (gramático) por Smith, no byākaraṇa.', ref='Kacc., título')
t('guṇavacana', 'palabra que expresa una cualidad; adjetivo', 'word expressing a quality; adjective', 'Kacc. 5, Rū. 5, Thitzana 3. Distinto de guṇa (fortalecimiento).', ref='Kacc. Nāma / Taddhita')
t('ādivuddhi', 'fortalecimiento de la (vocal) inicial', 'strengthening of the initial vowel', 'vuddhi → «strengthening» es N-EN.', ref='Kacc. Taddhita')
t('suttavibhāga', 'división del aforismo', 'splitting of a sutta', 'Kacc. §20 «suttavibhāgena»; Thitzana, índice: «Split-Sutta procedure» (también «yogavibhāga», que sí está).', ref='Kacc. §20')
t('akatarassa', '(vocal) no acortada; breve por naturaleza', 'not shortened; naturally short (vowel)', 'La norma tiene katarassa «que ha sido acortada» (Nāma §225); falta su contrario. Thitzana, índice: «Natural short vowel».', ref='Kacc. Nāma')
t('jinavacanayutta', 'conforme a la palabra del Jina', 'in accordance with the word of the Victorious One', 'Kacc. §52 «Jinavacanayuttaṃ hi». Jina → «the Victorious One» ya está propuesto en glosario-ingles.json.', ref='Kacc. §52')
t('kāranta', 'que termina en la letra … (akāranta: terminado en «a»)', 'ending in the letter … (a-ending)', '120 apariciones; se lematiza el segundo miembro porque el primero varía (akāranta, ikāranta, ukāranta…).', ref='Kacc. Nāma; Rū.')
t('tabbiparīta', 'lo contrario de eso; el caso inverso', 'the reverse of that', 'Thitzana, índice: «reversal procedure». Fórmula de la Rūpasiddhi.', ref='Rū.; Thitzana')
t('aññapadattha', 'el significado de otra palabra (en el bahubbīhi)', 'the meaning of another word (in a bahubbīhi)', 'Nandisena tiene aññapada y aññapadattha-padhāna, no aññapadattha solo, que es el que Thitzana usa (26).', ref='Kacc. Samāsa; Thitzana')
t('aṅgavikāra', 'modificación de un miembro del cuerpo (instrumental)', 'alteration of a limb (instrumental of bodily defect)', 'Kacc. Kāraka: «aṅgavikāre» (akkhinā kāṇo). Thitzana, índice: «Defective body part».', ref='Kacc. §… (tatiyā)')
t('tappakati', 'hecho de eso; cuya materia es eso', 'made of that', 'Taddhita: sufijo maya en el sentido «tappakatavacane». Thitzana: «made up of, crafted with».', ref='Kacc. Taddhita')
t('dhātupaccaya', 'sufijo de raíz (sufijo que se añade a la raíz: kārita, etc.)', 'root-affix', 'Thitzana, índice: «Dhātu-paccaya, also Dhātu niddiṭṭha affixes». Nyāsa 16.', ref='Nyāsa; Thitzana')
t('manogaṇa', 'el grupo «mano» (temas en -o del tipo manas)', 'the «mano» group', 'glosario-ingles.json ya tiene «manogaṇādito → after the “mano” group and others», de modo que el inglés está medio fijado y el lema no existe.', ref='Kacc. Nāma')
t('ghaṭādi', 'las raíces del grupo «ghaṭa» (etc.)', 'the «ghaṭa» group of roots', 'Kacc. Ākhyāta: «ghaṭādīnaṃ vā» (vuddhi opcional).', ref='Kacc. Ākhyāta')
t('tunādi', 'los sufijos tuna, etc. (tuna, tvāna, tvā)', 'the «tuna» group of suffixes (absolutive)', 'Kacc. Kibbidhāna «sabbehi tunādīnaṃ yo». Ñāṇamoli: «gerund or absolutive affixes».', ref='Kacc. Kibbidhāna')
t('tvādi', 'los sufijos tvā, etc.', 'the «tvā» group of suffixes', 'Nandisena lo cita dentro de abyaya («tvādi-paccayanta-pada») sin entrada propia.', ref='Kacc.; Nyāsa')
t('saddūpapada', 'con una palabra (no un kāraka) como upapada', 'having a word as upapada', 'Thitzana 71, Nyāsa 65: los derivados primarios cuyo upapada es un sadda y no un kāraka. La norma tiene upapada «miembro precedente».', ref='Kacc. Kibbidhāna; Thitzana')
t('yoganta', 'final del aforismo; (que va) al final de la regla', 'end of the rule', 'Nyāsa 122, Thitzana 17, sobre todo en «yogantaṃ» / «asaṃyoganta» (cuidado: no confundir). SENTIDO POR CONFIRMAR sobre los pasajes.', ref='Nyāsa; Thitzana')
t('sambandhī', 'el término de la relación; lo relacionado (genitivo)', 'the related term; correlate', 'Rū. 15, Nyāsa 33: pareja de sambandha, que sí está.', ref='Rū. Kāraka')
t('hetvattha', 'en el sentido de causa', 'in the sense of cause', 'Kacc. 15 (instrumental y ablativo de causa).', ref='Kacc. Kāraka')
t('karaṇattha', 'en el sentido de instrumento', 'in the sense of instrument', '', ref='Kacc. Kāraka')
t('byāpika', '(locativo) que abarca; de extensión', 'pervading (locative)', 'Kacc. 4, Rū. 4: uno de los tres adhikaraṇa con opasilesika y vesayika, que sí están.', ref='Kacc. §… (adhikaraṇa)')
t('ubhayattha', 'en ambos sentidos; en los dos casos', 'in both senses', 'Rū. 5.', ref='Rū.')
t('bhāvakamma', '(en) el impersonal y el pasivo', '(in) the impersonal and the passive', 'Kacc. «bhāvakammesu»: la condición de la voz pasiva e impersonal. Nyāsa 73, Thitzana 13.', ref='Kacc. Ākhyāta')
t('tija-gupa-kita-māna', 'las raíces tija, gupa, kita y māna (desiderativo con kha, cha, sa)', 'the roots tija, gupa, kita and māna', 'Kacc. §433 «Tijagupakitamānehi kha cha sā vā». Nyāsa 6.', ref='Kacc. §433')
t('catukka', 'tétrada; grupo de cuatro (niddhāraṇa-catukka, anādara-catukka)', 'tetrad; group of four', 'Thitzana, índice: «Niddhāraṇa-Catukka», «Anā’dara-Catukka». Kacc. 10.', ref='Thitzana')
t('sabbattha', 'en todos los casos (fórmula «evaṃ sabbattha»)', 'everywhere; in all cases', 'glosario-ingles.json ya propone «evaṃ sabbattha → So everywhere». 186 apariciones.', ref='Kacc. passim')
t('ikārāgama', 'inserción de la letra «i»', 'insertion of the letter «i»', 'āgama → «insertion» es N-EN. Nyāsa 61. Van también sāgama (38), māgama (9), rāgama (8), okārāgama (6) y vāgama (3): decidir si entran una a una o como patrón «-āgama».', ref='Kacc. Ākhyāta; Nyāsa')
t('sāgama', 'inserción de la letra «s»', 'insertion of the letter «s»', 'Kacc. Ākhyāta (aoristo).', ref='Kacc.')
t('māgama', 'inserción de la letra «m»', 'insertion of the letter «m»', '', ref='Kacc.; Nyāsa')
t('rāgama', 'inserción de la letra «r»', 'insertion of the letter «r»', '', ref='Kacc.; Nyāsa')
t('okārāgama', 'inserción de la letra «o»', 'insertion of the letter «o»', '', ref='Nyāsa')
t('ṇāpaya', 'el sufijo causativo ṇāpaya', 'the causative suffix ṇāpaya', 'Con ṇe, ṇaya, ṇāpe (Kacc. §438 «Dhātūhi ṇe ṇaya ṇāpe ṇāpayā kāritāni hetvatthe»). Ninguno de los cuatro está como lema; kārita sí.', ref='Kacc. §438')
t('gha (saññā)', 'la designación «gha» (los temas femeninos en -ā)', 'the designation «gha» (feminine ā-stems)', 'Kacc. §… «Ā gho». La norma tiene pasañña «llamada pa»; faltan gha, jha, la, ga. Nyāsa 18.', ref='Kacc. §…', tipo='designación', fuentes={'Nyāsa': 18, 'Thitz': 1})
t('jha (saññā)', 'la designación «jha» (temas masculinos y neutros en -i, -ī, -u, -ū)', 'the designation «jha»', 'Kacc. «I-vaṇṇ-uvaṇṇā jha-lā». Nyāsa 19.', ref='Kacc.', tipo='designación', fuentes={'Nyāsa': 19})
t('la (saññā)', 'la designación «la» (temas femeninos en -i, -ī, -u, -ū)', 'the designation «la»', 'Nyāsa 30.', ref='Kacc.', tipo='designación', fuentes={'Nyāsa': 30, 'Rūp': 1, 'Thitz': 1})
t('ga (saññā)', 'la designación «ga» (el vocativo singular)', 'the designation «ga» (vocative singular)', 'Kacc. «Ālapane si gasañño». 62 en el Nyāsa, 4 en Kacc.', ref='Kacc. §…', tipo='designación', fuentes={'Kacc': 4, 'Rūp': 4, 'Nyāsa': 62, 'Thitz': 5})

# ---- 2. Sufijos (paccaya) sin lema ---------------------------------------
S = json.load(open('/sessions/gallant-lucid-bell/mnt/outputs/tanda2/sufijos_ctx.json'))
have = set(json.load(open('/sessions/gallant-lucid-bell/mnt/outputs/tanda2/lemas_existentes.json')))
GLOSA = {  # sentido según el vutti donde se introduce; lo demás lo dice el «ref»
 'ṇa':'linaje (tass’ āpaccaṃ) y otros', 'ṇeyya':'linaje', 'ṇi':'linaje', 'ṇava':'linaje', 'ṇera':'linaje',
 'ṇika':'«relacionado con» (saṃsaṭṭha, tarati, carati, vahati…)', 'tā':'colectivo (samūha)', 'iya':'«lugar de eso» (tad assa ṭhānaṃ)',
 'la':'«lugar de eso»; dependencia', 'kaṇ':'abstracto (tassa bhāvo)', 'vī':'posesión (tad ass’ atthi)', 'so':'posesión', 'ttana':'abstracto',
 'vantu':'posesión', 'mantu':'posesión', 'ī':'posesión', 'sī':'posesión', 'ra':'posesión; agente', 'ma':'ordinal / posesión', 'tiya':'ordinal',
 'thaṃ':'adverbio de modo', 'thā':'adverbio de modo', 'dhā':'distributivo', 'maya':'«hecho de» (tappakati)', 'ka':'diminutivo; posesión; varios',
 'ta':'participio pasado (kita)', 'ya':'vikaraṇa de divādi; kicca', 'ntu':'participio presente; posesión', 'tuṃ':'infinitivo',
 'yu':'agente / nombre de acción (ana)', 'ṇya':'kicca; abstracto', 'ala':'uṇādi', 'i':'agente (uṇādi)', 'ina':'agente (kita)',
 'kha':'desiderativo', 'kta':'uṇādi', 'nā':'vikaraṇa de kiyādi', 'ritu':'agente (kita: -tar)', 'rū':'agente (kita)', 'sa':'desiderativo',
 'va':'posesión', 'ā':'femenino; vikaraṇa', 'īya':'denominativo', 'ama':'uṇādi', 'cha':'desiderativo', 'ika':'kita', 'kvi':'agente sin resto (kita)',
 'kāra':'«que hace» (kita)', 'man':'uṇādi', 'ppa':'vikaraṇa', 'ramma':'kita', 'ratthu':'agente (kita: -tar)', 'ricca':'kita', 'ririya':'kita',
 'rātu':'agente (kita)', 'teyya':'kicca', 'tha':'uṇādi', 'to':'ablativo adverbial', 'tu':'agente (-tar)', 'tuka':'kita', 'ye':'', 'āni':'uṇādi',
 'āya':'denominativo', 'īvara':'uṇādi', 'ūra':'uṇādi', 'ṇaya':'causativo', 'ṇu':'vikaraṇa de svādi', 'ṇuka':'kita', 'ṇī':'uṇādi', 'ṇitta':'uṇādi', 'ṭha':'uṇādi',
}
for w, d in S.items():
    if w in have: continue
    ch = ', '.join(d['capitulos'])
    ctx = d['ctx']
    ref = (ctx[0] + ': «' + ctx[2] + '»') if ctx else ch
    g = GLOSA.get(w, '')
    t('sufijo ' + w, 'el sufijo ' + w + (' — ' + g if g else ''), 'the suffix ' + w + (' — ' + g if g else ''),
      'Capítulo(s): ' + ch + '. El sentido de la columna sale del vutti donde se introduce; conviene confirmarlo.',
      tipo='sufijo', ref=ref, fuentes={k: v for k, v in d['capitulos'].items()})

json.dump(R, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(R), sum(1 for r in R if r['tipo']=='término'), sum(1 for r in R if r['tipo']=='sufijo'), sum(1 for r in R if r['tipo']=='designación'))
