# Datos de la clasificación, cap. 6 (Ākhyāta, §406–§523). Claude, 2026-10-12.
# Se ejecuta una vez para volcar en recursos/clasificacion/datos.json (v0.7.6 → v0.8).
# Fuentes, las mismas que en los capítulos 1–5: Rūpasiddhi (docs/6. Ākhyāta-Rūpasiddhi.md;
# §432 = Rū 362, en docs/5. Taddhita-Rūpasiddhi.md) y Nyāsa (docs/fuentes/nyasa/Nyasa-06-akhyata.md,
# texto OCR: las citas van normalizadas, con espacios entre palabras); Thitzana (Introducción,
# pp. 36–37) donde la operación se cuenta en la ādesa. Extracto de las dos fuentes por sutta:
# docs/capitulo-6/_fuentes_clasif_cap6.json.
# Se niega a correr si datos.json no está en la v0.7.6 o si ya tiene el capítulo 6.
# Copia de seguridad: docs/clasificacion/datos-v0.7.6-antes-akhyata.json.
import json, re, shutil, unicodedata, sys
N = lambda s: unicodedata.normalize('NFC', s)
P = 'recursos/clasificacion/datos.json'
D = json.load(open(P, encoding='utf-8')); S = D['suttas']
if D['version'] != '0.7.6' or '406' in S:
    sys.exit('datos.json no está en la v0.7.6 o ya tiene el capítulo 6: no se ejecuta.')
F = json.load(open('docs/capitulo-6/_fuentes_clasif_cap6.json', encoding='utf-8'))

def vutti(t):
    """Primera frase de la vutti de la Rūpasiddhi, sin notas ni negritas."""
    t = re.sub(r'\[\^\d+\]', '', t).replace('\\', '')
    t = re.sub(r'^\*\*\d+\. .*?\*\*\s*(\([\d\-, ]+\))?\s*(\[[^\]]*\])?\.?\s*', '', t.strip(), flags=re.S)
    t = re.sub(r'\s+', ' ', t.replace('**', ''))
    return re.split(r'(?<=[a-zāīūṃ])\. ', t)[0].rstrip('.')

# Citas de la Rūpasiddhi recortadas a mano donde la primera frase sigue con la derivación.
RU_CORTE = {
 406: 'Atha taddhitānantaraṃ vuccamānānaṃ sabbāsaṃ vattamānādīnaṃ aṭṭhavidhānaṃ vibhattīnaṃ yāni yāni pubbakāni cha padāni, tāni tāni atthato aṭṭhacattālīsamattāni parassapadasaññāni honti',
 409: 'Sabbesaṃ paṭhama-majjhimānaṃ, paṭham’-uttamānaṃ, majjhim’-uttamānaṃ tiṇṇaṃ vā purisānaṃ ekatobhidhāne kātabbe paro puriso yojetabbo',
 410: 'Tumhāmhasaddavajjite tulyādhikaraṇabhūte sādhakavācake nāmamhi payujjamāne pi appayujjamāne pi dhātūhi paṭhamapuriso hoti',
 411: 'Tulyādhikaraṇabhūte tumhasadde payujjamāne pi appayujjamāne pi dhātūhi majjhimapuriso hoti',
 412: 'Tulyādhikaraṇabhūte amhasadde payujjamāne pi appayujjamāne pi dhātūhi uttamapuriso hoti',
 413: 'Ayam adhikāro. Ito paraṃ tyādivibhattividhāne sabbattha vattate',
 414: 'Paccuppanne kāle gamyamāne vattamānāvibhatti hoti',
 418: 'Hiyyopabhuti atīte kāle paccakkhe vā appaccakkhe vā hiyyattanīvibhatti hoti',
 419: 'Samīpe samīpato paṭhāya ajjappabhuti atīte kāle paccakkhe ca apaccakkhe ca ajjatanīvibhatti hoti',
 423: 'Tyādayo dvādasa vattamānāsaññā honti',
 431: 'Hiyyattanādayo catasso vibhattiyo sabbadhātukasaññā honti',
 432: 'Dhātūhi, liṅgehi ca paccayā parā ’va hontī ti paribhāsato',
 438: 'Sabbehi dhātūhi hetvatthe abhidheyye ṇe ṇaya ṇāpe ṇāpaya icc ete paccayā parā honti, te kāritasaññā ca honti',
 441: 'Tassa bhāva-kammavisayassa yappaccayassa cavagga-yakāra-vakārattaṃ hoti dhātvantena saha yathāsambhavaṃ',
 442: 'Sabbehi dhātūhi tasmiṃ bhāva-kammavisaye yappaccaye pare ivaṇṇāgamo hoti vā',
 443: 'ka-ca-ṭa-pavagga-yakāra-la-santeh’ eva dhātūhi paro yappaccayo pubbarūpam āpajjate vā',
 444: 'Yathā bhāva-kammesu yappaccayass’ ādeso hoti, tathā kattari pi yappaccayassa sadhātvantassa cavagga-yakāra-vakārādeso, pubbarūpañ kātabbānī',
 446: 'Rudha icc evamādito dhātugaṇato appaccayo hoti kattari vibhatti-ppaccayesu niggahītañ ca tato pubbaṃ hutvā āgamo hoti',
 455: 'Dhātvatthe niddiṭṭhehi khādi-kāritantehi paccayehi tyādayo vibhattiyo honti',
 456: 'Kattarikārake abhidheyye sabbadhātūhi parassapadaṃ hoti',
 459: 'Dvebhūtassa dhātussa yo pubbo avayavo, so abbhāsasañño hoti',
 461: 'Abbhāsagatānaṃ dutiya-catutthānaṃ vaggabyañjanānaṃ yathākkamaṃ paṭhama-tatiyā honti',
 462: 'Abbhāse vattamānassa kavaggassa cavaggo hoti',
 463: 'Abbhāsagatānaṃ māna kita icc etesaṃ dhātūnaṃ vakāra-takārattaṃ hoti vā yathākkamaṃ',
 475: 'Brū bhū icc etesaṃ dhātūnaṃ āha bhūva icc ete ādesā honti parokkhāvibhattiyaṃ',
 476: 'Gamu icc etassa dhātuss’ anto makāro ccho hoti vā sabbāsu vibhattīsu, sabbaggahaṇena mān’-anta-yakāritappaccayesu ca',
 482: 'Dā icc etassa dhātussa antassa aṃ hoti vā mi ma icc etesu paresu',
 483: 'Asaṃyogantassa dhātussa kārite pare vuddhi hoti',
 484: 'Ghaṭādīnaṃ dhātūnaṃ asaṃyogantānaṃ vuddhi hoti vā kārite',
 485: 'Kāritato aññesu paccayesu asaṃyogantānaṃ dhātūnaṃ vuddhi hoti. Caggahaṇena ṇuppaccayass’ āpi vuddhi hoti',
 486: 'Guha dusa icc etesaṃ dhātūnaṃ saro dīgham āpajjate kārite pare, vuddhāpavādo ’yaṃ',
 491: 'Kara icc etassa dhātussa sabbass’ eva kāsattaṃ hoti vā ajjatanimhi vibhattimhi pare … “sattam ajjatanimhī” ti yogavibhāgena aññasmā pi dhātuto sāgamo pi sijjhati',
 499: 'Dā icc etassa dhātussa sabbassa dajjādeso hoti vā',
 502: 'Bhāva-kammavisaye yamhi paccaye pare dā dhā mā ṭhā hā pā maha matha icc evamādīnaṃ dhātūnaṃ anto īkāram āpajjate, niccattho ’yam ārambho',
 503: 'Yaja icc etassa dhātussa ādissa yakārassa ikārādeso hoti yappaccaye pare',
 505: 'Jara mara icc etesaṃ dhātūnaṃ jīra-jīyya-mīyyādesā honti vā',
 506: 'Sabattha vibhattippaccayesu ca asa icc etāya dhātuyā ādissa lopo hoti vā',
 508: 'Eyyassa vibhattissa ñā icc etāya dhātuyā parassa iyā ñā icc ete ādesā honti vā',
 509: 'Ñā icc etāya dhātuyā parassa nāpaccayassa lopo hoti vā, yakārattañ ca',
 514: 'Ekārassa dhātvantassa sare pare ayādeso hoti',
 517: 'kvaci dhātūnaṃ, tyādivibhattīnaṃ, dhātuvihitappaccayānañ ca dīgha tabbiparīta ādesa lop’ āgama icc etāni kāriyāni jinavacanānurūpato bhavanti',
 518: 'Attanopadāni kvaci parassapadattam āpajjante, akattari yev’ etaṃ',
 520: 'Brū icc etāya dhātuyā paro īkārāgamo hoti timhi vibhattimhi kvaci',
}

def ru_txt(k):
    r = F[str(k)]['rupasiddhi']
    t = RU_CORTE.get(k) or vutti(F[str(k)]['ru'])
    return (f'Rū {r}: «{t}».', f'Rū {r}: “{t}”.')

TH_ES = 'Introducción, pp. 36–37: dentro de la ādesa, «Vuddhi, Vipariyāya, Pakati, Atidesa and so on, are also included» ({0}).'
TH_EN = 'Introduction, pp. 36–37: under ādesa, “Vuddhi, Vipariyāya, Pakati, Atidesa and so on, are also included” ({0}).'
TH = {444: ('la atidesa, en la ādesa', 'atidesa, under ādesa'),
      483: ('la vuddhi, en la ādesa', 'vuddhi, under ādesa'),
      484: ('la vuddhi, en la ādesa', 'vuddhi, under ādesa'),
      485: ('la vuddhi, en la ādesa', 'vuddhi, under ādesa'),
      488: ('la vipariyāya, en la ādesa', 'vipariyāya, under ādesa')}
GRUPO = {444: 'atidesa', 483: 'vuddhi', 484: 'vuddhi', 485: 'vuddhi', 488: 'vipariyaya'}

# § : (tipo, vidhi, op_es, op_en, Nyāsa (cita normalizada del texto OCR))
R = {
406: ('S', '', 'Las seis primeras formas de cada inflexión reciben el nombre de “parassapada” (voz activa).', 'The first six forms of each inflection are named “parassapada” (active voice).', 'ito paraṃ vuccamānānaṃ vibhattigaṇānaṃ yāni yāni purimāni cha padāni, tāni tāni parassapadasaññāni hontī ti ñāpanatthaṃ'),
407: ('S', '', 'Las seis formas posteriores reciben el nombre de “attanopada” (voz media).', 'The latter six forms are named “attanopada” (middle voice).', 'yāni yāni vibhattīnaṃ parāni cha padāni, tāni tāni attanopadasaññāni hontī ti ñāpanatthaṃ'),
408: ('S', '', 'Los pares de formas reciben los nombres de tercera, segunda y primera persona (paṭhama-, majjhima-, uttamapurisa).', 'The pairs of forms are named third, second and first person (paṭhama-, majjhima-, uttamapurisa).', 'tāsaṃ sabbāsaṃ vibhattīnaṃ dve dve paṭhama-majjhim’-uttamapurisasaññāni hontī ti ñāpanatthaṃ'),
409: ('P', '', 'Regla de interpretación: cuando varias personas se enuncian juntas, se toma la posterior.', 'Interpretive rule: when several persons are mentioned together, the latter is taken.', 'sabbesaṃ paṭhama-majjhim’-uttamapurisānaṃ tulyābhidhāne paro puriso yojetabbo ti ñāpanatthaṃ'),
410: ('V', 'vibhatti', 'Asignación de la tercera persona cuando el sujeto es un nombre con el mismo locus, se emplee o no.', 'Assignment of the third person when the subject is a noun with the same locus, whether used or not.', 'tulyādhikaraṇasaṅkhāte sādhakavācake nāmamhi payujjamāne pi appayujjamāne pi sabbadhātūhi paṭhamapuriso hotī ti ñāpanatthaṃ'),
411: ('V', 'vibhatti', 'Asignación de la segunda persona con “tumha” (tú), se emplee o no.', 'Assignment of the second person with “tumha” (you), whether used or not.', 'tulyādhikaraṇasaṅkhāte tumhe payujjamāne pi appayujjamāne pi majjhimapuriso hotī ti ñāpanatthaṃ'),
412: ('V', 'vibhatti', 'Asignación de la primera persona con “amha” (yo), se emplee o no.', 'Assignment of the first person with “amha” (I), whether used or not.', 'tulyādhikaraṇasaṅkhāte amhasaddamhi payujjamāne pi … appayujjamāne pi uttamapuriso hotī ti ñāpanatthaṃ'),
413: ('A', '', 'Aforismo regulativo: «en tiempo» (kāle) rige las asignaciones de inflexión que siguen.', 'Governing aphorism: “in time” (kāle) governs the assignments of inflection that follow.', 'ye ito paraṃ vakkhāma, te kāle yeva hontī ti ñāpanatthaṃ'),
414: ('V', 'vibhatti', 'Asignación de la inflexión “vattamānā” en el tiempo presente.', 'Assignment of the inflection “vattamānā” in the present time.', 'paccuppanne kāle vattamānāvibhattiyo hontī ti ñāpanatthaṃ'),
415: ('V', 'vibhatti', 'Asignación de la inflexión “pañcamī” en los significados de orden y de bendición, en tiempo no enunciado.', 'Assignment of the inflection “pañcamī” in the meanings of command and blessing, in unstated time.', 'āṇatyatthe ca āsisatthe ca anuttakāle pañcamīvibhattiyo hontī ti ñāpanatthaṃ'),
416: ('V', 'vibhatti', 'Asignación de la inflexión “sattamī” en los significados de consentimiento y de suposición.', 'Assignment of the inflection “sattamī” in the meanings of consent and assumption.', 'anumatyatthe ca parikappatthe ca anuttakāle sattamīvibhattiyo hontī ti ñāpanatthaṃ'),
417: ('V', 'vibhatti', 'Asignación de la inflexión “parokkhā” en el pasado no percibido directamente.', 'Assignment of the inflection “parokkhā” in the past not directly perceived.', 'apaccakkhe atīte kāle parokkhāvibhattiyo hontī ti ñāpanatthaṃ'),
418: ('V', 'vibhatti', 'Asignación de la inflexión “hiyyattanī” en el pasado a partir de ayer, percibido o no.', 'Assignment of the inflection “hiyyattanī” in the past from yesterday on, perceived or not.', 'hiyyopabhuti atīte kāle paccakkhe vā apaccakkhe vā hiyyattanīvibhattiyo hontī ti ñāpanatthaṃ'),
419: ('V', 'vibhatti', 'Asignación de la inflexión “ajjatanī” en el pasado próximo.', 'Assignment of the inflection “ajjatanī” in the recent past.', 'samīpe atīte kāle paccakkhe vā apaccakkhe vā ajjatanīvibhattiyo hontī ti ñāpanatthaṃ'),
420: ('V', 'vibhatti', 'Asignación de “hiyyattanī” y “ajjatanī” (y, por «ca», “pañcamī”) en todo tiempo, en asociación con “mā”.', 'Assignment of “hiyyattanī” and “ajjatanī” (and, by “ca”, “pañcamī”) in all time, in conjunction with “mā”.', 'yadā māyogo, tadā hiyyattanī-ajjatanīvibhattiyo sabbakāle pi hontī ti ñāpanatthaṃ'),
421: ('V', 'vibhatti', 'Asignación de la inflexión “bhavissantī” en el tiempo futuro.', 'Assignment of the inflection “bhavissantī” in the future time.', 'anāgate kāle bhavissantīvibhattiyo hontī ti ñāpanatthaṃ'),
422: ('V', 'vibhatti', 'Asignación de la inflexión “kālātipatti” en el pasado, cuando la acción no llegó a ocurrir.', 'Assignment of the inflection “kālātipatti” in the past, when the action failed to take place.', 'kriyātipannamatte atīte kāle kālātipattivibhattiyo hontī ti ñāpanatthaṃ'),
423: ('S', '', 'Las doce terminaciones ti, anti … e, mhe reciben el nombre de “vattamānā”.', 'The twelve endings ti, anti … e, mhe are named “vattamānā”.', 'tyādayo vattamānasaññā hontī ti ñāpanatthaṃ'),
424: ('S', '', 'Las doce terminaciones tu, antu … e, āmase reciben el nombre de “pañcamī”.', 'The twelve endings tu, antu … e, āmase are named “pañcamī”.', 'tvādayo pañcamīsaññā hontī ti ñāpanatthaṃ'),
425: ('S', '', 'Las doce terminaciones eyya, eyyuṃ … eyyaṃ, eyyāmhe reciben el nombre de “sattamī”.', 'The twelve endings eyya, eyyuṃ … eyyaṃ, eyyāmhe are named “sattamī”.', 'eyyādayo sattamīsaññā hontī ti ñāpanatthaṃ'),
426: ('S', '', 'Las doce terminaciones a, u … iṃ, mhe reciben el nombre de “parokkhā”.', 'The twelve endings a, u … iṃ, mhe are named “parokkhā”.', 'a-ādayo parokkhāsaññā hontī ti ñāpanatthaṃ'),
427: ('S', '', 'Las doce terminaciones ā, ū … iṃ, mhase reciben el nombre de “hiyyattanī”.', 'The twelve endings ā, ū … iṃ, mhase are named “hiyyattanī”.', 'ā-ādayo hiyyattanīsaññā hontī ti ñāpanatthaṃ'),
428: ('S', '', 'Las doce terminaciones ī, uṃ … aṃ, mhe reciben el nombre de “ajjatanī”.', 'The twelve endings ī, uṃ … aṃ, mhe are named “ajjatanī”.', 'ī-ādayo ajjatanīsaññā hontī ti ñāpanatthaṃ'),
429: ('S', '', 'Las doce terminaciones ssati, ssanti … ssaṃ, ssāmhe reciben el nombre de “bhavissantī”.', 'The twelve endings ssati, ssanti … ssaṃ, ssāmhe are named “bhavissantī”.', 'ssatyādayo bhavissantīsaññā hontī ti ñāpanatthaṃ'),
430: ('S', '', 'Las doce terminaciones ssā, ssaṃsu … ssiṃ, ssāmhase reciben el nombre de “kālātipatti”.', 'The twelve endings ssā, ssaṃsu … ssiṃ, ssāmhase are named “kālātipatti”.', 'ssādayo kālātipattisaññā hontī ti ñāpanatthaṃ'),
431: ('S', '', '“Hiyyattanī”, “sattamī”, “pañcamī” y “vattamānā” reciben el nombre de “sabbadhātuka”.', '“Hiyyattanī”, “sattamī”, “pañcamī” and “vattamānā” are named “sabbadhātuka”.', 'hiyyattanādayo catasso sabbadhātukasaññā hontī ti ñāpanatthaṃ'),
432: ('P', '', 'Regla de interpretación: los sufijos se colocan después de las raíces y de los temas nominales.', 'Interpretive rule: suffixes are placed after roots and nominal bases.', 'dhātūhi ca liṅgehi ca paccayā parā va hontī ti ñāpanatthaṃ … paccayaṭṭhānaniyamakaraṇattham idaṃ vuttaṃ … idaṃ pana catūsu suttesu paribhāsāsuttan ti daṭṭhabbaṃ'),
433: ('V', 'paccaya', 'Opcionalmente, aplicación de los sufijos ‘kha’, ‘cha’ y ‘sa’ tras “tija”, “gupa”, “kita” y “māna”.', 'Optionally, application of the suffixes ‘kha’, ‘cha’ and ‘sa’ after “tija”, “gupa”, “kita” and “māna”.', 'tija-gupa-kita-māna icc etehi dhātūhi kha-cha-sa icc ete paccayā honti vikappenā ti ñāpanatthaṃ'),
434: ('V', 'paccaya', 'Opcionalmente, aplicación de los sufijos ‘kha’, ‘cha’ y ‘sa’ tras “bhuja”, “ghasa”, “hara”, “su”, “pā” y otras, en el significado de querer hacer algo (desiderativo).', 'Optionally, application of the suffixes ‘kha’, ‘cha’ and ‘sa’ after “bhuja”, “ghasa”, “hara”, “su”, “pā” and others, in the sense of wanting to do something (desiderative).', 'bhuja-ghasa-hara-su-pā icc evamādīhi tumicchatthesu gamyamānesu kha-cha-sa icc ete paccayā honti vikappenā ti ñāpanatthaṃ'),
435: ('V', 'paccaya', 'Aplicación del sufijo ‘āya’ tras un nombre que sirve de comparación con el agente, en el significado de comportamiento.', 'Application of the suffix ‘āya’ after a noun that serves as comparison for the agent, in the sense of behaviour.', 'kattuno upamānabhūtamhā nāmato āyapaccayo hoti ācāratthe ti ñāpanatthaṃ'),
436: ('V', 'paccaya', 'Aplicación del sufijo ‘īya’ tras un nombre que sirve de comparación, en el significado de comportamiento.', 'Application of the suffix ‘īya’ after a noun that serves as comparison, in the sense of behaviour.', 'upamānasmā nāmato īyapaccayo hoti ācāratthe ti ñāpanatthaṃ'),
437: ('V', 'paccaya', 'Aplicación del sufijo ‘īya’ tras un nombre, en el significado de desear para uno mismo.', 'Application of the suffix ‘īya’ after a noun, in the sense of wanting for oneself.', 'nāmamhā atticchatthe īyapaccayo hotī ti ñāpanatthaṃ'),
438: ('V', 'paccaya', 'Aplicación de los sufijos ‘ṇe’, ‘ṇaya’, ‘ṇāpe’ y ‘ṇāpaya’ tras las raíces en el significado de causa; se llaman “kārita” (causativo).', 'Application of the suffixes ‘ṇe’, ‘ṇaya’, ‘ṇāpe’ and ‘ṇāpaya’ after roots in the sense of cause; they are called “kārita” (causative).', 'sabbadhātūhi hetvatthe gamyamāne ṇe-ṇaya-ṇāpe-ṇāpaya icc ete paccayā honti, te kāritasaññā ca hontī ti ñāpanatthaṃ'),
439: ('V', 'paccaya', 'Aplicación del sufijo ‘ṇaya’ tras un nombre que ha de tomar forma de raíz; se llama también “kārita”.', 'Application of the suffix ‘ṇaya’ after a noun that is to take the form of a root; it is also called “kārita”.', 'dhāturūpe sati nāmasmā ṇayapaccayo hoti, tato kāritasaññā cā ti ñāpanatthaṃ'),
440: ('V', 'paccaya', 'Aplicación del sufijo ‘ya’ en el impersonal (bhāva) y en el pasivo (kamma).', 'Application of the suffix ‘ya’ in the impersonal (bhāva) and the passive (kamma).', 'sabbehi dhātūhi bhāvakammesu yapaccayo hotī ti ñāpanatthaṃ'),
441: ('V', 'ādesa', 'Sustitución del sufijo ‘ya’, junto con el final de la raíz, por una letra del grupo ‘ca’, por ‘y’ o por ‘v’.', 'Substitution of the suffix ‘ya’, together with the end of the root, by a letter of the ‘ca’ group, by ‘y’ or by ‘v’.', 'tassa yapaccayassa dhātvantena saha cavagga-yakāra-vakārattaṃ hotī ti ñāpanatthaṃ'),
442: ('V', 'āgama', 'Opcionalmente, inserción de ‘i’ o ‘ī’ ante el sufijo ‘ya’ del impersonal y del pasivo.', 'Optionally, insertion of ‘i’ or ‘ī’ before the suffix ‘ya’ of the impersonal and the passive.', 'sabbadhātūhi tamhi yapaccaye pare ivaṇṇāgamo hoti vikappenā ti ñāpanatthaṃ'),
443: ('V', 'ādesa', 'Opcionalmente, el sufijo ‘ya’ toma la forma de la consonante anterior (asimilación).', 'Optionally, the suffix ‘ya’ takes the form of the preceding consonant (assimilation).', 'sabbehi dhātūhi yapaccayo pubbarūpam āpajjate vikappenā ti ñāpanatthaṃ'),
444: ('V', 'ādesa', 'Extensión a la voz activa de las sustituciones de ‘ya’ (§441 y §443) (extensión, atidesa).', 'Extension to the active voice of the substitutions of ‘ya’ (§441 and §443) (extension, atidesa).', 'yathā heṭṭhā bhāvakammesu yapaccayass’ ādeso hoti, tathā kattari pi hotī ti ñāpanatthaṃ'),
445: ('V', 'paccaya', 'Aplicación del sufijo ‘a’ tras “bhū” y las demás raíces de su grupo, en la voz activa.', 'Application of the suffix ‘a’ after “bhū” and the other roots of its group, in the active voice.', 'bhū icc evamādito dhātugaṇato apaccayo hoti kattarī ti ñāpanatthaṃ'),
446: ('V', 'paccaya + āgama', 'Aplicación del sufijo ‘a’ tras “rudha” y las demás raíces de su grupo, con inserción de la niggahita delante.', 'Application of the suffix ‘a’ after “rudha” and the other roots of its group, with insertion of the niggahita before it.', 'rudha icc evamādito dhātugaṇato apaccayo hoti kattari, niggahītapubbañ ca hutvā āgamo hotī ti ñāpanatthaṃ'),
447: ('V', 'paccaya', 'Aplicación del sufijo ‘ya’ tras “divu” y las demás raíces de su grupo, en la voz activa.', 'Application of the suffix ‘ya’ after “divu” and the other roots of its group, in the active voice.', 'divādito dhātugaṇato yapaccayo hoti kattarī ti ñāpanatthaṃ'),
448: ('V', 'paccaya', 'Aplicación de los sufijos ‘ṇu’, ‘ṇā’ y ‘uṇā’ tras “su” y las demás raíces de su grupo, en la voz activa.', 'Application of the suffixes ‘ṇu’, ‘ṇā’ and ‘uṇā’ after “su” and the other roots of its group, in the active voice.', 'su icc evamādito dhātugaṇato ṇu-ṇā-uṇā icc ete paccayā honti kattarī ti ñāpanatthaṃ'),
449: ('V', 'paccaya', 'Aplicación del sufijo ‘nā’ tras “kī” y las demás raíces de su grupo, en la voz activa.', 'Application of the suffix ‘nā’ after “kī” and the other roots of its group, in the active voice.', 'kī icc evamādito dhātugaṇato nāpaccayo hoti kattarī ti ñāpanatthaṃ'),
450: ('V', 'paccaya', 'Aplicación de los sufijos ‘ppa’ y ‘ṇhā’ tras “gaha” y otras, en la voz activa.', 'Application of the suffixes ‘ppa’ and ‘ṇhā’ after “gaha” and others, in the active voice.', 'gaha icc evamādito dhātugaṇato ppa-ṇhā icc ete paccayā honti kattarī ti ñāpanatthaṃ'),
451: ('V', 'paccaya', 'Aplicación de los sufijos ‘o’ e ‘yira’ tras “tanu” y las demás raíces de su grupo, en la voz activa.', 'Application of the suffixes ‘o’ and ‘yira’ after “tanu” and the other roots of its group, in the active voice.', 'tanu icc evamādito dhātugaṇato o-yira icc ete paccayā honti kattarī ti ñāpanatthaṃ'),
452: ('V', 'paccaya', 'Aplicación de los sufijos ‘ṇe’ y ‘ṇaya’ tras “cura” y las demás raíces de su grupo; se llaman “kārita”.', 'Application of the suffixes ‘ṇe’ and ‘ṇaya’ after “cura” and the other roots of its group; they are called “kārita”.', 'cura icc evamādito dhātugaṇato ṇe-ṇaya icc ete paccayā honti kattari, kāritasaññā cā ti ñāpanatthaṃ'),
453: ('V', 'vibhatti', 'Asignación de las inflexiones “attanopada” (medias) en el impersonal y en el pasivo.', 'Assignment of the “attanopada” (middle) inflections in the impersonal and the passive.', 'attanopadāni honti bhāve ca kammani cā ti ñāpanatthaṃ'),
454: ('V', 'vibhatti', 'Asignación de las inflexiones “attanopada” también en la voz activa.', 'Assignment of the “attanopada” inflections also in the active voice.', 'kattari ca attanopadāni hontī ti ñāpanatthaṃ'),
455: ('V', 'vibhatti', 'Aplicación de las inflexiones (ti, etc.) tras las raíces derivadas con sufijo (los sufijos de §433–§439).', 'Application of the inflections (ti, etc.) after roots derived with a suffix (the suffixes of §433–§439).', 'dhātvādhikāre vihitānaṃ tyādīnaṃ vibhattīnaṃ adhātumhā sampatte … dhātuppaccayā ti laddhavohārehi … vuttehi khādipaccayehi tyādayo vibhattiyo hontī ti ñāpanatthaṃ'),
456: ('V', 'vibhatti', 'Asignación de las inflexiones “parassapada” en la voz activa.', 'Assignment of the “parassapada” inflections in the active voice.', 'kattarikārake … parassapadaṃ hotī ti ñāpanatthaṃ'),
457: ('S', '', '“Bhū” y las demás palabras que expresan acción reciben el nombre de “dhātu” (raíz).', '“Bhū” and the other words that express action are named “dhātu” (root).', 'bhū icc evamādayo ye saddagaṇā, te dhātusaññā hontī ti ñāpanatthaṃ'),
458: ('V', 'āgama', 'A veces, reduplicación de la sílaba inicial de una sola vocal de la raíz (dvebhāva).', 'Sometimes, reduplication of the initial single-vowel syllable of the root (dvebhāva).', 'ādibhūtānaṃ vaṇṇānaṃ ekassarānaṃ kvaci dvebhāvo hotī ti ñāpanatthaṃ'),
459: ('S', '', 'La parte anterior de la raíz reduplicada recibe el nombre de “abbhāsa”.', 'The former part of the reduplicated root is named “abbhāsa”.', 'dvebhūtassa dhātussa yo pubbo, so abbhāsasañño hotī ti ñāpanatthaṃ'),
460: ('V', 'rassa', 'Acortamiento de la vocal del abbhāsa.', 'Shortening of the vowel of the abbhāsa.', 'abbhāse vattamānassa sarassa rasso hotī ti ñāpanatthaṃ'),
461: ('V', 'ādesa', 'En el abbhāsa, sustitución de la segunda y la cuarta consonante de cada grupo por la primera y la tercera.', 'In the abbhāsa, substitution of the second and fourth consonant of each group by the first and third.', 'abbhāsagatānaṃ dutiya-catutthānaṃ paṭhama-tatiyā hontī ti ñāpanatthaṃ'),
462: ('V', 'ādesa', 'En el abbhāsa, sustitución del grupo ‘ka’ por el grupo ‘ca’.', 'In the abbhāsa, substitution of the ‘ka’ group by the ‘ca’ group.', 'abbhāse vattamānassa kavaggassa cavaggo hotī ti ñāpanatthaṃ'),
463: ('V', 'ādesa', 'Opcionalmente, en el abbhāsa de “māna” y “kita”, sustitución por ‘v’ y por ‘t’ respectivamente.', 'Optionally, in the abbhāsa of “māna” and “kita”, substitution by ‘v’ and by ‘t’ respectively.', 'māna-kita icc etesaṃ dhātūnaṃ abbhāsagatānaṃ vakāra-takārādesā honti vikappenā ti ñāpanatthaṃ'),
464: ('V', 'ādesa', 'En el abbhāsa, sustitución de ‘h’ por ‘j’.', 'In the abbhāsa, substitution of ‘h’ by ‘j’.', 'abbhāse vattamānassa hakārassa jādeso hotī ti ñāpanatthaṃ'),
465: ('V', 'ādesa', 'Opcionalmente, sustitución del final del abbhāsa por ‘i’, ‘ī’ o ‘a’.', 'Optionally, substitution of the end of the abbhāsa by ‘i’, ‘ī’ or ‘a’.', 'abbhāsantassa ivaṇṇo ca akāro ca hoti vikappenā ti ñāpanatthaṃ'),
466: ('V', 'āgama', 'Opcionalmente, inserción de la niggahita al final del abbhāsa.', 'Optionally, insertion of the niggahita at the end of the abbhāsa.', 'abbhāsante niggahītāgamo hoti vikappenā ti ñāpanatthaṃ'),
467: ('V', 'ādesa', 'Tras el abbhāsa, sustitución de “pā” y “māna” por ‘vā’ y ‘maṃ’ cuando sigue el sufijo ‘sa’.', 'After the abbhāsa, substitution of “pā” and “māna” by ‘vā’ and ‘maṃ’ when the suffix ‘sa’ follows.', 'tato abbhāsato paresaṃ pā-mānānaṃ dhātūnaṃ vā-maṃ icc ete ādesā honti sapaccaye pare ti ñāpanatthaṃ'),
468: ('V', 'ādesa', 'Opcionalmente, sustitución de “ṭhā” por ‘tiṭṭha’.', 'Optionally, substitution of “ṭhā” by ‘tiṭṭha’.', 'ṭhā icc etassa dhātussa tiṭṭhādeso hoti vikappenā ti ñāpanatthaṃ'),
469: ('V', 'ādesa', 'Opcionalmente, sustitución de “pā” por ‘piba’ (‘piva’).', 'Optionally, substitution of “pā” by ‘piba’ (‘piva’).', 'pā icc etassa dhātussa pivādeso hoti vikappenā ti ñāpanatthaṃ'),
470: ('V', 'ādesa', 'Opcionalmente, sustitución de “ñā” por ‘jā’, ‘jaṃ’ y ‘nā’.', 'Optionally, substitution of “ñā” by ‘jā’, ‘jaṃ’ and ‘nā’.', 'ñā icc etassa dhātussa jā-jaṃ-nā icc ete ādesā honti vikappenā ti ñāpanatthaṃ'),
471: ('V', 'ādesa', 'Opcionalmente, sustitución de “disa” por ‘passa’, ‘dissa’ y ‘dakkha’.', 'Optionally, substitution of “disa” by ‘passa’, ‘dissa’ and ‘dakkha’.', 'disassa dhātussa passa-dissa-dakkha icc ete ādesā honti vikappenā ti ñāpanatthaṃ'),
472: ('V', 'ādesa', 'Sustitución de la consonante final de la raíz por ‘c’ cuando siguen los sufijos ‘cha’.', 'Substitution of the final consonant of the root by ‘c’ when the suffixes ‘cha’ follow.', 'dhātvantassa byañjanassa cakārādeso hoti chapaccayesu paresū ti ñāpanatthaṃ'),
473: ('V', 'ādesa', 'Sustitución de la consonante final de la raíz por ‘k’ cuando sigue el sufijo ‘kha’.', 'Substitution of the final consonant of the root by ‘k’ when the suffix ‘kha’ follows.', 'dhātvantassa byañjanassa kakārādeso hoti khapaccaye pare ti ñāpanatthaṃ'),
474: ('V', 'ādesa', 'Sustitución de toda la raíz “hara” por ‘gī’ cuando sigue el sufijo ‘sa’.', 'Substitution of the whole root “hara” by ‘gī’ when the suffix ‘sa’ follows.', 'hara icc etassa dhātussa sabbass’ eva gī-ādeso hoti sapaccaye pare ti ñāpanatthaṃ'),
475: ('V', 'ādesa', 'Sustitución de “brū” y “bhū” por ‘āha’ y ‘bhūva’ en la inflexión “parokkhā”.', 'Substitution of “brū” and “bhū” by ‘āha’ and ‘bhūva’ in the “parokkhā” inflection.', 'brū-bhū icc etesaṃ dhātūnaṃ āha-bhūva icc ete ādesā honti parokkhāyaṃ vibhattiyan ti ñāpanatthaṃ'),
476: ('V', 'ādesa', 'Opcionalmente, sustitución del final de “gamu” por ‘ccha’ ante todas las inflexiones.', 'Optionally, substitution of the end of “gamu” by ‘ccha’ before all the inflections.', 'gamu icc etassa dhātussa anto ccho hoti vikappena sabbāsu paccaya-vibhattīsū ti ñāpanatthaṃ'),
477: ('V', 'ādesa', 'Sustitución de la ‘a’ de “vaca” por ‘o’ cuando sigue la inflexión “ajjatanī”.', 'Substitution of the ‘a’ of “vaca” by ‘o’ when the “ajjatanī” inflection follows.', 'vaca icc etassa dhātussa akāro ottam āpajjate ajjatanimhi vibhattimhī ti ñāpanatthaṃ'),
478: ('V', 'dīgha', 'Alargamiento de ‘a’ cuando siguen ‘hi’, ‘mi’ y ‘ma’.', 'Lengthening of ‘a’ when ‘hi’, ‘mi’ and ‘ma’ follow.', 'akāro dīgham āpajjate hi-mi-ma icc etāsu vibhattīsū ti ñāpanatthaṃ'),
479: ('V', 'lopa', 'Opcionalmente, elisión de la inflexión ‘hi’ (tras ‘a’).', 'Optionally, elision of the inflection ‘hi’ (after ‘a’).', 'hivibhatti lopam āpajjate vikappenā ti ñāpanatthaṃ'),
480: ('V', 'ādesa + lopa', 'Sustitución de la vocal de “hū” por ‘eha’, ‘oha’ y ‘e’ ante la inflexión “bhavissantī”, y opcionalmente elisión de ‘ssa’.', 'Substitution of the vowel of “hū” by ‘eha’, ‘oha’ and ‘e’ before the “bhavissantī” inflection, and optionally elision of ‘ssa’.', 'hū icc etassa dhātussa saro eh’-oh’-ettam āpajjate bhavissantimhi vibhattimhi, ssassa ca lopo hoti vikappenā ti ñāpanatthaṃ'),
481: ('V', 'ādesa + lopa', 'Opcionalmente, sustitución de “kara”, junto con su sufijo, por ‘kāha’ ante la inflexión “bhavissantī”, con elisión de ‘ssa’.', 'Optionally, substitution of “kara”, together with its suffix, by ‘kāha’ before the “bhavissantī” inflection, with elision of ‘ssa’.', 'kara icc etassa dhātussa sapaccayassa kāhādeso hoti, sakāradvayassa ca lopo hoti vikappenā ti ñāpanatthaṃ'),
482: ('V', 'ādesa', 'Opcionalmente, sustitución del final de “dā” por ‘aṃ’ cuando siguen ‘mi’ y ‘ma’.', 'Optionally, substitution of the end of “dā” by ‘aṃ’ when ‘mi’ and ‘ma’ follow.', 'dā icc etassa dhātussa antassa aṃ hoti mi-ma icc etesu vibhattīsū ti ñāpanatthaṃ'),
483: ('V', 'ādesa', 'Fortalecimiento (vuddhi) de la vocal de la raíz que no termina en consonante conjunta, cuando sigue un sufijo causativo (kārita).', 'Strengthening (vuddhi) of the vowel of a root that does not end in a conjunct consonant, when a causative (kārita) suffix follows.', 'asaṃyogantassa dhātussa kārite vuddhi hotī ti ñāpanatthaṃ'),
484: ('V', 'ādesa', 'Opcionalmente, fortalecimiento (vuddhi) de “ghaṭa” y otras raíces ante el causativo.', 'Optionally, strengthening (vuddhi) of “ghaṭa” and other roots before the causative.', 'ghaṭādīnaṃ dhātūnaṃ asaṃyogantānaṃ vikappena vuddhi hoti kārite ti ñāpanatthaṃ'),
485: ('V', 'ādesa', 'Fortalecimiento (vuddhi) de la vocal de la raíz ante los demás sufijos (no causativos).', 'Strengthening (vuddhi) of the root vowel before the other (non-causative) suffixes.', 'aññesu ca paccayesu asaṃyogantānaṃ dhātūnaṃ vuddhi hotī ti ñāpanatthaṃ'),
486: ('V', 'dīgha', 'Alargamiento de la vocal de “guha” y “dusa” cuando sigue un sufijo causativo (en lugar de la vuddhi).', 'Lengthening of the vowel of “guha” and “dusa” when a causative suffix follows (instead of vuddhi).', 'guha-dusa icc etesaṃ dhātūnaṃ saro dīgham āpajjate kārite ti ñāpanatthaṃ'),
487: ('V', 'ādesa', 'Sustitución de la ‘v’ de “vaca”, “vasa”, “vaha” y otras por ‘u’ cuando sigue el sufijo ‘ya’.', 'Substitution of the ‘v’ of “vaca”, “vasa”, “vaha” and others by ‘u’ when the suffix ‘ya’ follows.', 'vaca-vasa-vaha icc evamādīnaṃ dhātūnaṃ vakārassa ukāro hoti yapaccaye pare ti ñāpanatthaṃ'),
488: ('V', 'ādesa', 'Inversión (metátesis) de ‘h’ con el sufijo ‘ya’ que sigue, y opcionalmente sustitución de ‘y’ por ‘l’.', 'Inversion (metathesis) of ‘h’ with the following suffix ‘ya’, and optionally substitution of ‘y’ by ‘l’.', 'havipariyāyo hoti yapaccayasmiṃ pare, yakārassa ca lo hoti vikappenā ti ñāpanatthaṃ'),
489: ('V', 'ādesa', 'Sustitución de toda la raíz “gaha” por ‘ghe’ cuando sigue el sufijo ‘ppa’.', 'Substitution of the whole root “gaha” by ‘ghe’ when the suffix ‘ppa’ follows.', 'gaha icc etassa dhātussa ghekāro hoti ppapaccayasmiṃ pare ti ñāpanatthaṃ'),
490: ('V', 'lopa', 'Elisión de la ‘h’ de “gaha” cuando sigue el sufijo ‘ṇhā’.', 'Elision of the ‘h’ of “gaha” when the suffix ‘ṇhā’ follows.', 'gaha icc etassa dhātussa hakārassa lopo hoti ṇhāpaccayasmiṃ pare ti ñāpanatthaṃ'),
491: ('V', 'ādesa', 'Opcionalmente, sustitución de toda la raíz “kara” por ‘kāsa’ cuando sigue la inflexión “ajjatanī”.', 'Optionally, substitution of the whole root “kara” by ‘kāsa’ when the “ajjatanī” inflection follows.', 'kara icc etassa dhātussa kāsattaṃ hoti ajjatanimhi vikappenā ti ñāpanatthaṃ'),
492: ('V', 'ādesa + lopa', 'Tras “asa”, opcionalmente sustitución de ‘mi’ y ‘ma’ por ‘mhi’ y ‘mha’, y elisión del final de la raíz.', 'After “asa”, optionally substitution of ‘mi’ and ‘ma’ by ‘mhi’ and ‘mha’, and elision of the end of the root.', 'asa icc etasmā mi-ma icc etāsaṃ vibhattīnaṃ mhi-mhādesā honti, dhātvantassa ca lopo hoti vikappenā ti ñāpanatthaṃ'),
493: ('V', 'ādesa + lopa', 'Tras “asa”, sustitución de ‘tha’ por ‘ttha’, y elisión del final de la raíz.', 'After “asa”, substitution of ‘tha’ by ‘ttha’, and elision of the end of the root.', 'asa icc etasmā thassa vibhattissa tthattaṃ hoti, dhātvantassa ca lopo hotī ti ñāpanatthaṃ'),
494: ('V', 'ādesa + lopa', 'Tras “asa”, sustitución de ‘ti’ por ‘tthi’, y elisión del final de la raíz.', 'After “asa”, substitution of ‘ti’ by ‘tthi’, and elision of the end of the root.', 'asa icc etasmā tissa vibhattissa tthittaṃ hoti, dhātvantassa ca lopo hotī ti ñāpanatthaṃ'),
495: ('V', 'ādesa + lopa', 'Tras “asa”, sustitución de ‘tu’ por ‘tthu’, y elisión del final de la raíz.', 'After “asa”, substitution of ‘tu’ by ‘tthu’, and elision of the end of the root.', 'asa icc etasmā tussa vibhattissa tthuttaṃ hoti, dhātvantassa ca lopo hotī ti ñāpanatthaṃ'),
496: ('V', 'lopa', 'Elisión del final de “asa” cuando sigue la inflexión ‘si’.', 'Elision of the end of “asa” when the inflection ‘si’ follows.', 'asa icc etass’ eva dhātussa simhi vibhattimhi anto lopo hotī ti ñāpanatthaṃ'),
497: ('V', 'ādesa + lopa', 'Tras “labha”, opcionalmente sustitución de ‘ī’ e ‘iṃ’ por ‘ttha’ y ‘tthaṃ’, y elisión del final de la raíz.', 'After “labha”, optionally substitution of ‘ī’ and ‘iṃ’ by ‘ttha’ and ‘tthaṃ’, and elision of the end of the root.', 'labha icc etasmā ī-iṃnaṃ vibhattīnaṃ ttha-tthaṃ ādesā honti, dhātvantassa ca lopo hotī ti ñāpanatthaṃ'),
498: ('V', 'ādesa + lopa', 'Tras “kusa”, sustitución de ‘ī’ por ‘cchi’, y elisión del final de la raíz.', 'After “kusa”, substitution of ‘ī’ by ‘cchi’, and elision of the end of the root.', 'kudha icc etasmā īvibhattissa cchi-ādeso hoti, dhātvantassa ca lopo hotī ti ñāpanatthaṃ'),
499: ('V', 'ādesa', 'Opcionalmente, sustitución de toda la raíz “dā” por ‘dajja’.', 'Optionally, substitution of the whole root “dā” by ‘dajja’.', 'dā icc etassa dhātussa dajjādeso hoti vikappenā ti ñāpanatthaṃ'),
500: ('V', 'ādesa', 'Opcionalmente, sustitución de toda la raíz “vada” por ‘vajja’.', 'Optionally, substitution of the whole root “vada” by ‘vajja’.', 'vada icc etassa dhātussa vajjādeso hoti vikappenā ti ñāpanatthaṃ'),
501: ('V', 'ādesa', 'Opcionalmente, sustitución de toda la raíz “gamu” por ‘ghamma’.', 'Optionally, substitution of the whole root “gamu” by ‘ghamma’.', 'gamu icc etassa dhātussa ghammādeso hoti vikappenā ti ñāpanatthaṃ'),
502: ('V', 'ādesa', 'Sustitución del final de “dā”, “dhā”, “mā”, “ṭhā”, “hā”, “pā”, “maha”, “matha” y otras por ‘ī’ cuando sigue el sufijo ‘ya’.', 'Substitution of the end of “dā”, “dhā”, “mā”, “ṭhā”, “hā”, “pā”, “maha”, “matha” and others by ‘ī’ when the suffix ‘ya’ follows.', 'yamhi paccaye pare vuttappakārānaṃ dhātūnaṃ anto īkāram āpajjate ti ñāpanatthaṃ'),
503: ('V', 'ādesa', 'Sustitución de la ‘y’ inicial de “yaja” por ‘i’ cuando sigue el sufijo ‘ya’.', 'Substitution of the initial ‘y’ of “yaja” by ‘i’ when the suffix ‘ya’ follows.', 'yaja icc etassa dhātussa ādissa ikārādeso hoti yapaccayasmiṃ pare ti ñāpanatthaṃ'),
504: ('V', 'ādesa', 'Tras todas las raíces, sustitución opcional de ‘uṃ’ por ‘iṃsu’.', 'After all roots, optional substitution of ‘uṃ’ by ‘iṃsu’.', 'sabbehi dhātūhi uṃvibhattissa iṃsvādeso hotī ti ñāpanatthaṃ'),
505: ('V', 'ādesa', 'Opcionalmente, sustitución de “jara” y “mara” por ‘jīra’, ‘jiyya’ y ‘miyya’.', 'Optionally, substitution of “jara” and “mara” by ‘jīra’, ‘jiyya’ and ‘miyya’.', 'jara-marānaṃ jīra-jiyya-miyya icc ete ādesā honti vikappenā ti ñāpanatthaṃ'),
506: ('V', 'lopa', 'Opcionalmente, elisión de la letra inicial de “asa” ante todas las inflexiones y sufijos.', 'Optionally, elision of the initial letter of “asa” before all inflections and suffixes.', 'sabbattha vibhattippaccayesu asa icc etassa dhātussa ādissa lopo hoti vikappenā ti ñāpanatthaṃ'),
507: ('V', 'ādesa', 'Opcionalmente, sustitución de “asa” por ‘bhū’ ante las inflexiones “asabbadhātuka”.', 'Optionally, substitution of “asa” by ‘bhū’ before the “asabbadhātuka” inflections.', 'asa icc etassa dhātussa asabbadhātuke bhū-ādeso hoti vikappenā ti ñāpanatthaṃ'),
508: ('V', 'ādesa', 'Tras “ñā”, sustitución opcional de ‘eyya’ por ‘iyā’ y ‘ñā’.', 'After “ñā”, optional substitution of ‘eyya’ by ‘iyā’ and ‘ñā’.', 'ñā icc etasmā eyyassa vibhattissa iyā-ñā icc ete ādesā honti vikappenā ti ñāpanatthaṃ'),
509: ('V', 'lopa + ādesa', 'Tras “ñā”, opcionalmente elisión del sufijo ‘nā’ o sustitución por ‘y’.', 'After “ñā”, optionally elision of the suffix ‘nā’ or substitution by ‘y’.', 'ñā icc etasmā nāpaccayassa lopo hoti, yakārattañ ca āpajjate vikappenā ti ñāpanatthaṃ'),
510: ('V', 'ādesa + lopa', 'Opcionalmente, sustitución del sufijo ‘a’ por ‘e’, o su elisión.', 'Optionally, substitution of the suffix ‘a’ by ‘e’, or its elision.', 'akārapaccayo ettam āpajjate lopañ ca vikappenā ti ñāpanatthaṃ'),
511: ('V', 'ādesa', 'Opcionalmente, sustitución del sufijo ‘o’ (de “tanu” y su grupo) por ‘u’.', 'Optionally, substitution of the suffix ‘o’ (of “tanu” and its group) by ‘u’.', 'okārapaccayo uttam āpajjate vikappenā ti ñāpanatthaṃ'),
512: ('V', 'ādesa', 'Opcionalmente, sustitución de la ‘a’ de “kara” por ‘u’.', 'Optionally, substitution of the ‘a’ of “kara” by ‘u’.', 'kara icc etassa dhātussa akāro ca uttam āpajjate vikappenā ti ñāpanatthaṃ'),
513: ('V', 'ādesa', 'Sustitución de la ‘o’ final de la raíz por ‘ava’ cuando sigue una vocal.', 'Substitution of the root-final ‘o’ by ‘ava’ when a vowel follows.', 'okārassa dhātvantassa sare pare avādeso hotī ti ñāpanatthaṃ'),
514: ('V', 'ādesa', 'Sustitución de la ‘e’ final de la raíz por ‘aya’ cuando sigue una vocal.', 'Substitution of the root-final ‘e’ by ‘aya’ when a vowel follows.', 'dhātvantassa ekārassa sare pare ayādeso hotī ti ñāpanatthaṃ'),
515: ('V', 'ādesa', 'Sustitución de esas ‘o’ y ‘e’ por ‘āva’ y ‘āya’ ante el causativo.', 'Substitution of those ‘o’ and ‘e’ by ‘āva’ and ‘āya’ before the causative.', 'te o-e icc ete āva-āyādese pāpuṇanti kārite ti ñāpanatthaṃ'),
516: ('V', 'āgama', 'A veces, inserción de ‘i’ ante las inflexiones “asabbadhātuka”.', 'Sometimes, insertion of ‘i’ before the “asabbadhātuka” inflections.', 'ikārāgamo hoti asabbadhātukamhī ti ñāpanatthaṃ'),
517: ('V', 'dīgha + rassa + ādesa + lopa + āgama', 'A veces, alargamiento, lo contrario (acortamiento), sustitución, elisión e inserción en raíces, inflexiones y sufijos, según el uso.', 'Sometimes, lengthening, its opposite (shortening), substitution, elision and insertion in roots, inflections and suffixes, according to usage.', 'kvaci dhātu-vibhatti-paccayānaṃ dīgha-viparīt’-ādesa-lop’-āgamā ca hontī ti ñāpanatthaṃ'),
518: ('V', 'ādesa', 'A veces, las inflexiones “attanopada” pasan a “parassapada”.', 'Sometimes, the “attanopada” inflections become “parassapada”.', 'attanopadāni parassapadattam āpajjante kvacī ti ñāpanatthaṃ'),
519: ('V', 'āgama', 'A veces, inserción de ‘a’ al principio de la raíz ante “hiyyattanī”, “ajjatanī” y “kālātipatti” (aumento).', 'Sometimes, insertion of ‘a’ at the beginning of the root before “hiyyattanī”, “ajjatanī” and “kālātipatti” (augment).', 'kvaci akārāgamo hoti hiyyattanī-ajjatanī-kālātipattīsū ti ñāpanatthaṃ'),
520: ('V', 'āgama', 'Tras “brū”, a veces inserción de ‘ī’ cuando sigue la inflexión ‘ti’.', 'After “brū”, sometimes insertion of ‘ī’ when the inflection ‘ti’ follows.', 'brū icc etāya dhātuyā īkārāgamo hoti timhi vibhattimhī ti ñāpanatthaṃ'),
521: ('V', 'lopa', 'A veces, elisión de la letra final de la raíz de más de una vocal.', 'Sometimes, elision of the final letter of a root of more than one vowel.', 'kvaci anekassarassa dhātussa anto lopo hotī ti ñāpanatthaṃ'),
522: ('V', 'ādesa', 'Opcionalmente, sustitución del final de “isu” y “yamu” por ‘ccha’.', 'Optionally, substitution of the end of “isu” and “yamu” by ‘ccha’.', 'isu-yamu icc etesaṃ anto ccho hoti vikappenā ti ñāpanatthaṃ'),
523: ('V', 'lopa', 'Elisión de la ‘ṇ’ de los sufijos causativos (kārita).', 'Elision of the ‘ṇ’ of the causative (kārita) suffixes.', 'kāritānaṃ paccayānaṃ ṇo lopam āpajjate ti ñāpanatthaṃ'),
}

NOTAS = {
409: ('Rūpasiddhi lo introduce como paribhāsā al cerrar Rū 440 («Paṭhamapurisādīnam ekajjhappavattippasaṅge paribhāsam āha»): no asigna una inflexión, sino que dice cuál de las personas se toma cuando concurren. Nyāsa lo enuncia con «yojetabbo», «se ha de emplear». Determinación: paribhāsā.',
      'The Rūpasiddhi introduces it as a paribhāsā at the close of Rū 440 (“Paṭhamapurisādīnam ekajjhappavattippasaṅge paribhāsam āha”): it does not assign an inflection, but says which person is taken when several concur. The Nyāsa states it with “yojetabbo”, “is to be used”. Determination: paribhāsā.'),
410: ('§410–§412 asignan la persona del verbo (tercera, segunda, primera). Ninguna de las dos fuentes nombra la clase; como las personas son pares de formas de cada inflexión (§408), se cuentan como vidhi · vibhatti, igual que las asignaciones de tiempo de §414–§422. Por revisar.',
      '§410–§412 assign the person of the verb (third, second, first). Neither source names the class; since the persons are pairs of forms of each inflection (§408), they are counted as vidhi · vibhatti, like the tense assignments of §414–§422. To review.'),
413: ('Rū 427: «Ayam adhikāro. Ito paraṃ tyādivibhattividhāne sabbattha vattate»: rige todas las asignaciones de inflexión que siguen. Nyāsa: «lo que diremos de aquí en adelante vale solo en tiempo». Determinación: adhikāra.',
      'Rū 427: “Ayam adhikāro. Ito paraṃ tyādivibhattividhāne sabbattha vattate”: it governs all the assignments of inflection that follow. The Nyāsa: “what we shall say from here on holds only in time”. Determination: adhikāra.'),
420: ('Rū 471: «casaddena pañcamī ca»: el «ca» del sutta añade la “pañcamī” (mā bhavatu).',
      'Rū 471: “casaddena pañcamī ca”: the sutta’s “ca” adds the “pañcamī” (mā bhavatu).'),
432: ('Rūpasiddhi lo cita como paribhāsā («“dhātu-liṅgehi parā paccayā” ti paribhāsato», Rū 362, y otra vez en Rū 428), y Nyāsa lo dice expresamente: fija el lugar del sufijo («paccayaṭṭhānaniyamakaraṇattham idaṃ vuttaṃ») y es «de los cuatro, el paribhāsā-sutta» («idaṃ pana catūsu suttesu paribhāsāsuttan ti daṭṭhabbaṃ»). Rūpasiddhi lo pone en el Taddhita (Rū 362). Determinación: paribhāsā.',
      'The Rūpasiddhi cites it as a paribhāsā (“‘dhātu-liṅgehi parā paccayā’ ti paribhāsato”, Rū 362, and again in Rū 428), and the Nyāsa says so expressly: it fixes the place of the suffix (“paccayaṭṭhānaniyamakaraṇattham idaṃ vuttaṃ”) and is “of the four, the paribhāsā-sutta” (“idaṃ pana catūsu suttesu paribhāsāsuttan ti daṭṭhabbaṃ”). The Rūpasiddhi places it in the Taddhita (Rū 362). Determination: paribhāsā.'),
438: ('Hace dos cosas: aplica los sufijos y les da el nombre “kārita” (Rū 540: «te kāritasaññā ca honti»). Se clasifica por la operación principal, como §439 y §452.',
      'It does two things: it applies the suffixes and gives them the name “kārita” (Rū 540: “te kāritasaññā ca honti”). It is classified by its main operation, like §439 and §452.'),
444: ('Rū 511: «Yathā bhāva-kammesu yappaccayass’ ādeso hoti, tathā kattari pi»: extiende a la voz activa las sustituciones de §441 y §443 (atidesa). La atidesa se cuenta en la ādesa según Thitzana (vol. 2, Introducción, pp. 36–37), como §187, §331 y §332.',
      'Rū 511: “Yathā bhāva-kammesu yappaccayass’ ādeso hoti, tathā kattari pi”: it extends the substitutions of §441 and §443 to the active voice (atidesa). Atidesa is counted under ādesa according to Thitzana (vol. 2, Introduction, pp. 36–37), like §187, §331 and §332.'),
446: ('Dos operaciones: el sufijo ‘a’ (paccaya) y la niggahita que se inserta delante (āgama: «niggahītañ ca tato pubbaṃ hutvā āgamo hoti», Rū 509). Por el «ca», además, los sufijos ‘i’, ‘ī’, ‘e’, ‘o’ (Rū 509: «casaddena i-ī-e-opaccayā ca»).',
      'Two operations: the suffix ‘a’ (paccaya) and the niggahita inserted before it (āgama: “niggahītañ ca tato pubbaṃ hutvā āgamo hoti”, Rū 509). By “ca”, also the suffixes ‘i’, ‘ī’, ‘e’, ‘o’ (Rū 509: “casaddena i-ī-e-opaccayā ca”).'),
455: ('Las inflexiones se dan tras las raíces («dhātūhi»); este sutta las extiende a las bases derivadas con los sufijos de §433–§439, que no son raíces (Nyāsa: «adhātumhā sampatte»). Ninguna de las dos fuentes nombra la clase; se cuenta como vidhi · vibhatti, porque lo que hace es aplicar las inflexiones. Por revisar.',
      'The inflections are given after roots (“dhātūhi”); this sutta extends them to the bases derived with the suffixes of §433–§439, which are not roots (Nyāsa: “adhātumhā sampatte”). Neither source names the class; it is counted as vidhi · vibhatti, because what it does is apply the inflections. To review.'),
458: ('Como en §28, la duplicación (dvebhāva) no está entre las ocho vidhis; se clasifica como āgama, porque se añade una segunda sílaba. Por revisar.',
      'As in §28, doubling (dvebhāva) is not among the eight vidhis; it is classified as āgama, because a second syllable is added. To review.'),
483: ('La vuddhi se cuenta en la ādesa según Thitzana (vol. 2, Introducción, pp. 36–37), como §400. Qué vuddhi corresponde lo fija la paribhāsā §405 (Rū 434: «“A-y-uvaṇṇānañ c’ āyo vuddhī” ti paribhāsato»).',
      'Vuddhi is counted under ādesa according to Thitzana (vol. 2, Introduction, pp. 36–37), like §400. Which vuddhi applies is fixed by the paribhāsā §405 (Rū 434: “‘A-y-uvaṇṇānañ c’ āyo vuddhī’ ti paribhāsato”).'),
484: ('Vuddhi opcional (vā), contada en la ādesa como §483. Rū 542 lee el «vā» como vavatthitavibhāsā: en estas raíces la vuddhi normalmente no se hace (gameti, gamayati).',
      'Optional vuddhi (vā), counted under ādesa like §483. Rū 542 reads the “vā” as vavatthitavibhāsā: in these roots vuddhi is normally not made (gameti, gamayati).'),
485: ('Vuddhi ante los sufijos no causativos, contada en la ādesa como §483; por el «ca», también la del sufijo ‘ṇu’ (Rū 434).',
      'Vuddhi before the non-causative suffixes, counted under ādesa like §483; by “ca”, also that of the suffix ‘ṇu’ (Rū 434).'),
486: ('Rū 543: «vuddhāpavādo ’yaṃ»: excepción (apavāda) a la vuddhi de §483; en vez de fortalecer, alarga.',
      'Rū 543: “vuddhāpavādo ’yaṃ”: an exception (apavāda) to the vuddhi of §483; instead of strengthening, it lengthens.'),
488: ('Dos operaciones: la inversión (vipariyāya) de ‘h’ con la ‘y’ del sufijo (vaha + ya → vayha: vayhati) y la sustitución opcional de esa ‘y’ por ‘l’. La vipariyāya se cuenta en la ādesa según Thitzana (vol. 2, Introducción, pp. 36–37), que la nombra expresamente.',
      'Two operations: the inversion (vipariyāya) of ‘h’ with the ‘y’ of the suffix (vaha + ya → vayha: vayhati) and the optional substitution of that ‘y’ by ‘l’. Vipariyāya is counted under ādesa according to Thitzana (vol. 2, Introduction, pp. 36–37), who names it expressly.'),
491: ('Rū 523 da además una segunda lectura: por yogavibhāga, «sattam ajjatanimhī», inserción de ‘s’ (āgama) también tras otras raíces. Se clasifica por la lectura principal, la sustitución de “kara” por ‘kāsa’.',
      'Rū 523 also gives a second reading: by yogavibhāga, “sattam ajjatanimhī”, insertion of ‘s’ (āgama) after other roots too. It is classified by the main reading, the substitution of “kara” by ‘kāsa’.'),
498: ('Rūpasiddhi lee la raíz «kusa» (Rū 480: «Kusa icc etasmā dhātuto …»), como el enunciado de Nandisena; Nyāsa lee «kudha» («kudha icc etasmā …»; *akkocchi*, de «kudha kope») y explica la ‘d’ del enunciado como de sandhi («kudhasmā īcchī ti vattabbe dakāro sandhivasena»).',
      'The Rūpasiddhi reads the root “kusa” (Rū 480: “Kusa icc etasmā dhātuto …”), as does Nandisena’s wording; the Nyāsa reads “kudha” (“kudha icc etasmā …”; *akkocchi*, from “kudha kope”) and explains the ‘d’ of the wording as due to sandhi (“kudhasmā īcchī ti vattabbe dakāro sandhivasena”).'),
502: ('Rū 493: «niccattho ’yam ārambho»: la sustitución por ‘ī’ es obligatoria, no opcional.',
      'Rū 493: “niccattho ’yam ārambho”: the substitution by ‘ī’ is obligatory, not optional.'),
517: ('Cinco operaciones. Rū 488 glosa «viparīta» como «tabbiparīta», «lo contrario de eso», es decir, del alargamiento: el acortamiento (rassa), y lo ilustra con «Nāmhi rasso kiyādīnaṃ». Rū 488 lo restringe a las formas que las demás reglas no explican («avihitalakkhaṇesu payogesu … jinavacanānurūpato»). Compárese §404 (Taddhita), donde «viparīta» se contó en la ādesa.',
      'Five operations. Rū 488 glosses “viparīta” as “tabbiparīta”, “the opposite of that”, i.e. of lengthening: shortening (rassa), and illustrates it with “Nāmhi rasso kiyādīnaṃ”. Rū 488 restricts it to the forms that the other rules do not account for (“avihitalakkhaṇesu payogesu … jinavacanānurūpato”). Compare §404 (Taddhita), where “viparīta” was counted under ādesa.'),
}

for k, (tipo, vidhi, oe, on, ny) in R.items():
    re_, rn = ru_txt(k)
    e = {'tipo': tipo, 'vidhi': vidhi, 'op': {'es': N(oe), 'en': N(on)},
         'base': {'ru': {'es': N(re_), 'en': N(rn)},
                  'nyasa': {'es': N(f'«{ny}».'), 'en': N(f'“{ny}”.')}}}
    if k in TH:
        e['base']['th'] = {'es': N(TH_ES.format(TH[k][0])), 'en': N(TH_EN.format(TH[k][1]))}
    if k in GRUPO:
        e['grupo'] = GRUPO[k]
    if k in NOTAS:
        e['nota'] = {'es': N(NOTAS[k][0]), 'en': N(NOTAS[k][1])}
    S[str(k)] = e

assert sorted(int(k) for k in R) == list(range(406, 524))
D['capitulos'].append({'clave': 'akhyata', 'md': '06-akhyata-kappa', 'desde': 406, 'hasta': 523, 'pali': 'Ākhyāta-Kappa'})
D['version'] = '0.8'; D['fecha'] = '2026-10-12'
D['nota_version'] = {
 'es': 'v0.8: Ākhyāta-Kappa (§406–§523), los 118 suttas, con las mismas fuentes que los capítulos 1–5: Rūpasiddhi y Nyāsa, y el esquema de las ocho vidhis según Thitzana (vuddhi, vipariyāya y atidesa, en la ādesa). Rūpasiddhi llama paribhāsā a §409 y §432, y adhikāra a §413; Nyāsa llama también paribhāsā a §432. En §517 Rūpasiddhi lee «viparīta» como «tabbiparīta»: acortamiento. ' + D['nota_version']['es'],
 'en': 'v0.8: Ākhyāta-Kappa (§406–§523), all 118 suttas, with the same sources as chapters 1–5: the Rūpasiddhi and the Nyāsa, and the eight-fold scheme of vidhis as Thitzana explains it (vuddhi, vipariyāya and atidesa, under ādesa). The Rūpasiddhi calls §409 and §432 paribhāsā, and §413 adhikāra; the Nyāsa also calls §432 a paribhāsā. At §517 the Rūpasiddhi reads “viparīta” as “tabbiparīta”: shortening. ' + D['nota_version']['en']}
shutil.copy(P, 'docs/clasificacion/datos-v0.7.6-antes-akhyata.json')
json.dump(D, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('v0.8:', len(S), 'suttas;', sum(1 for k in range(406, 524) if 'nota' in S[str(k)]), 'notas nuevas')
