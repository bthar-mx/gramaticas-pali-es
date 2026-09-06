#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mete en la referencia de paradigmas las dos fichas de numerales —#3, los
cardinales; #4, los ordinales— a partir del documento «Numerales» de Bhikkhu
Nandisena (Google Doc 1kJVYCgqN51glznKyy-eV3CZvh14THpi5QcvGyDW1MZI, última
revisión 3 de junio de 2021). Sesión 58.

Las dos fichas no son tablas de casos sino PROSA más una LISTA:
  · «parrafos»: la prosa del documento, con enlaces {{CÓDIGO|texto}} a los
    paradigmas que nombra (eka, dvi, ti, catu, pañca, ratti, citta, āyu…);
  · «lista»: {columnas, filas}, cada fila [rótulo, [formas], …].
generar_paradigmas.py las deja pasar (no tienen «filas» de casos) y
plantilla.html las pinta con su propio renderizador.

Tres erratas del documento se corrigen con el visto bueno del IEBH y quedan
dichas en las notas de la ficha: «Aṭthasataṃ» → aṭṭhasataṃ, «Paṭhamam» →
paṭhamaṃ, «catutthaṃ jhānaṃ, quinta jhāna» → cuarta. Las potencias de diez
que el documento imprime sin superíndice (107, 1014) se restituyen.

Idempotente: si #3 y #4 ya están, no hace nada.
"""
import json, os, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(RAIZ, "recursos", "paradigmas")
DOC = "1kJVYCgqN51glznKyy-eV3CZvh14THpi5QcvGyDW1MZI"

SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
def pot(n):
    return "10" + str(n).translate(SUP)

CARDINALES = [
 ("1", "Eka"), ("2", "Dvi"), ("3", "Ti"), ("4", "Catu"), ("5", "Pañca"), ("6", "Cha"),
 ("7", "Satta"), ("8", "Aṭṭha"), ("9", "Nava"), ("10", "Dasa"),
 ("11", "Ekādasa, ekārasa"), ("12", "Dvādasa, bārasa"), ("13", "Terasa, teḷasa"),
 ("14", "Cuddasa, catuddasa, coddasa"), ("15", "Pannarasa, paṇṇarasa, pañcadasa"),
 ("16", "Soḷasa"), ("17", "Sattarasa, sattadasa"), ("18", "Aṭṭhārasa, aṭṭhādasa"),
 ("19", "Ekūnavīsati, ekūnavīsaṃ"), ("20", "Vīsati, vīsaṃ"), ("21", "Ekavīsati, ekavīsaṃ"),
 ("22", "Dvāvīsati, dvāvīsaṃ, bāvīsati, bāvīsaṃ"), ("23", "Tevīsati, tevīsaṃ"),
 ("24", "Catuvīsati, catuvīsaṃ"), ("25", "Pañcavīsati, pañcavīsaṃ, paṇṇavīsati, paṇṇavīsaṃ"),
 ("26", "Chabbīsati, chabbīsaṃ"), ("27", "Sattavīsati, sattavīsaṃ"), ("28", "Aṭṭhavīsati, aṭṭhavīsaṃ"),
 ("29", "Ekūnatiṃsati, ekūnatiṃsaṃ"), ("30", "Tiṃsati, tiṃsaṃ"), ("31", "Ekatiṃsati, ekatiṃsaṃ"),
 ("32", "Dvattiṃsati, dvattiṃsaṃ, bāttiṃsaṃ"), ("33", "Tettiṃsati, tettiṃsaṃ"),
 ("34", "Catutiṃsaṃ, catuttiṃsaṃ"), ("35", "Pañcatiṃsati, pañcatiṃsaṃ"),
 ("36", "Chattiṃsati, chattiṃsaṃ"), ("37", "Sattatiṃsati, sattatiṃsaṃ, sattattiṃsaṃ"),
 ("38", "Aṭṭhatiṃsati, aṭṭhatiṃsaṃ, aṭṭhattiṃsaṃ"),
 ("39", "Ekūnacattālīsaṃ"),
 ("40", "Cattārīsaṃ, cattārīsā, cattālīsaṃ, tālīsaṃ, cuttālīsaṃ, cottālīsaṃ"),
 ("41", "Ekacattārīsa, ekacattārīsā, ekacattālīsaṃ"), ("42", "Dvācattālīsaṃ, bācattālīsaṃ"),
 ("43", "Tecattālīsaṃ"), ("44", "Catucattālīsaṃ, catucattārīsaṃ"), ("45", "Pañcacattālīsaṃ"),
 ("46", "Chacattālīsaṃ, chacattārīsaṃ"), ("47", "Sattacattālīsaṃ"),
 ("48", "Aṭṭhacattālīsaṃ, aṭṭhacattārīsaṃ"),
 ("49", "Ekūnapaññāsaṃ, ekūnapaṇṇāsaṃ"), ("50", "Paññāsaṃ, paṇṇāsaṃ"),
 ("51", "Ekapaññāsaṃ, ekapaṇṇāsaṃ"), ("52", "Dvāpaññāsaṃ, dvipaññāsaṃ, dvepaññāsaṃ, dvepaṇṇāsaṃ"),
 ("53", "Tepaññāsaṃ, tepaṇṇāsaṃ"), ("54", "Catupaññāsaṃ, catupaṇṇāsaṃ"),
 ("55", "Pañcapaññāsaṃ, pañcapaṇṇāsaṃ"), ("56", "Chapaññāsaṃ, chapaṇṇāsaṃ, chappaññāsaṃ"),
 ("57", "Sattapaññāsaṃ, sattapaṇṇāsaṃ"), ("58", "Aṭṭhapaññāsaṃ, aṭṭhapaṇṇāsaṃ"),
 ("59", "Ekūnasaṭṭhi"), ("60", "Saṭṭhi"), ("61", "Ekasaṭṭhi"),
 ("62", "Dvāsaṭṭhi, dvesaṭṭhi, dvisaṭṭhi, bāsaṭṭhi"), ("63", "Tesaṭṭhi, tisaṭṭhi"),
 ("64", "Catusaṭṭhi"), ("65", "Pañcasaṭṭhi"), ("66", "Chasaṭṭhi"), ("67", "Sattasaṭṭhi"),
 ("68", "Aṭṭhasaṭṭhi"),
 ("69", "Ekūnasattati"), ("70", "Sattati, sattari"), ("71", "Ekasattati"),
 ("72", "Dvāsattati, dvesattati, dvāsattari, dvisattari, disattati"), ("73", "Tesattati, tisattati"),
 ("74", "Catusattati"), ("75", "Pañcasattati"), ("76", "Chasattati"), ("77", "Sattasattati"),
 ("78", "Aṭṭhasattati"),
 ("79", "Ekūnāsīti"), ("80", "Asīti"), ("81", "Ekāsīti"), ("82", "Dvāsīti, dve-asīti"),
 ("83", "Te-asīti"), ("84", "Caturāsīti"), ("85", "Pañcāsīti"), ("86", "Cha-asīti"),
 ("87", "Sattāsīti"), ("88", "Aṭṭhāsīti"),
 ("89", "Ekūnanavuti"), ("90", "Navuti"), ("91", "Ekanavuti"), ("92", "Dvānavuti, dvenavuti, dvinavuti"),
 ("93", "Tenavuti, tinavuti"), ("94", "Catunavuti"), ("95", "Pañcanavuti"),
 ("96", "Channavuti, chanavuti"), ("97", "Sattanavuti"), ("98", "Aṭṭhanavuti"),
 ("99", "Ekūnasataṃ, navanavuti"),
 ("100", "Sataṃ"), ("200", "Dvisataṃ"), ("300", "Tisataṃ"), ("400", "Catusataṃ"),
 ("500", "Pañcasataṃ"), ("600", "Chasataṃ"), ("700", "Sattasataṃ"), ("800", "Aṭṭhasataṃ"),
 ("900", "Navasataṃ"),
 ("1.000", "Sahassaṃ"), ("2.000", "Dvisahassaṃ"), ("3.000", "Tisahassaṃ"), ("4.000", "Catusahassaṃ"),
 ("5.000", "Pañcasahassaṃ"), ("6.000", "Chasahassaṃ"), ("7.000", "Sattasahassaṃ"),
 ("8.000", "Aṭṭhasahassaṃ"), ("9.000", "Navasahassaṃ"), ("10.000", "Dasasahassaṃ, nahutaṃ"),
 ("100.000", "Satasahassaṃ, lakkhaṃ"), ("1.000.000", "Dasasatasahassaṃ"),
 (pot(7) + " (10.000.000)", "Koṭi"), (pot(14), "Pakoṭi"), (pot(21), "Koṭippakoṭi"),
 (pot(28), "Nahuta"), (pot(35), "Ninnahuta"), (pot(42), "Akkhobhiṇī"), (pot(49), "Bindu"),
 (pot(56), "Abbuda"), (pot(63), "Nirabbuda"), (pot(70), "Ahaha"), (pot(77), "Ababa"),
 (pot(84), "Aṭaṭa"), (pot(91), "Sogandhika"), (pot(98), "Uppala"), (pot(105), "Kumuda"),
 (pot(112), "Puṇḍarīka"), (pot(119), "Paduma"), (pot(126), "Kathāna"),
 (pot(133), "Mahākathāna"), (pot(140), "Asaṅkheyya"),
]

ORDINALES = [
 ("1.º", "Paṭhamo", "Paṭhamā", "Paṭhamaṃ"), ("2.º", "Dutiyo", "dutiyā", "dutiyaṃ"),
 ("3.º", "Tatiyo", "tatiyā", "tatiyaṃ"), ("4.º", "Catuttho", "catutthā, catutthī", "catutthaṃ"),
 ("5.º", "Pañcamo", "pañcamā, pañcamī", "pañcamaṃ"), ("6.º", "Chaṭṭho", "chaṭṭhī, chaṭṭhā", "chaṭṭhaṃ"),
 ("7.º", "Sattamo", "sattamī, sattamā", "sattamaṃ"), ("8.º", "Aṭṭhamo", "aṭṭhamī, aṭṭhamā", "aṭṭhamaṃ"),
 ("9.º", "Navamo", "navamī, navamā", "navamaṃ"), ("10.º", "Dasamo", "dasamī, dasamā", "dasamaṃ"),
 ("11.º", "Ekādasamo", "ekādasamā, ekādasamī", "ekādasamaṃ"),
 ("12.º", "Bārasamo, dvādasamo", "dvādasamā, dvādasamī", "dvādasamaṃ"),
 ("13.º", "Terasamo", "terasamā, terasamī, terasī", "terasamaṃ"),
 ("14.º", "Cuddasamo, catuddasamo", "catuddasī, cātuddasī", "cuddasamaṃ"),
 ("15.º", "Pannarasamo, pañcadasamo", "pannarasamā, pannarasī, pañcadasī", "pannarasamaṃ, pañcadasamaṃ"),
 ("16.º", "Soḷasamo", "soḷasī, soḷasamā", "soḷasamaṃ"),
 ("17.º", "Sattarasamo, sattadasamo", "", "sattarasamaṃ"),
 ("18.º", "Aṭṭhārasamo", "aṭṭhārasamā", "aṭṭhārasamaṃ"),
 ("19.º", "Ekūnavīsatimo", "", "ekūnavīsatimaṃ"), ("20.º", "Vīsatimo", "vīsatimā", "vīsatimaṃ"),
 ("21.º", "Ekavīsatimo", "ekavīsatimā", "ekavīsatimaṃ"),
 ("22.º", "Bāvīsatimo, dvāvīsatimo", "dvāvīsatimā", "bāvīsatimaṃ, dvāvīsatimaṃ"),
 ("23.º", "Tevīsatimo", "", ""), ("24.º", "Catuvīsatimo", "", ""),
 ("25.º", "Paṇṇavīsatimo, pañcavīsatimo", "", ""), ("26.º", "Chabbīsatimo", "", ""),
 ("27.º", "Sattavīsatimo", "", ""), ("28.º", "Aṭṭhavīsatimo", "", ""),
 ("29.º", "Ekūnatiṃsatimo", "", ""), ("30.º", "Tiṃsatimo", "", ""), ("40.º", "Cattālīsamo", "", ""),
]


def como_cardinal(n, fs):
    """Con qué paradigma se declina cada cardinal, según el documento:
    enlace {{CÓDIGO|voz}} a la ficha. Devuelve una cadena para la columna
    «se declina como»."""
    try:
        v = int(n.replace(".", ""))
    except ValueError:
        v = None
    if v == 1:
        return "{{PM9|eka}} (m.), {{PF9|eka}} (f.), {{PN9|eka}} (n.)"
    if v == 2:
        return "{{P11|dvi}}"
    if v == 3:
        return "{{P12|ti}}"
    if v == 4:
        return "{{P13|catu}}"
    if v is not None and 5 <= v <= 18:
        return "{{#1|pañca}}"
    if v is not None and 19 <= v <= 99:
        partes = []
        if any(f.endswith("i") for f in fs):
            partes.append("en «i»: {{F-I1|ratti}} (como vīsati)")
        if any(f.endswith("aṃ") or f.endswith("ā") or f.endswith("a") for f in fs):
            partes.append("las demás: como vīsaṃ (el documento no remite a ficha)")
        return "; ".join(partes)
    if v is not None and 100 <= v <= 1000000:
        return "{{N-A1|citta}} (como sata)"
    # potencias de diez
    if fs and fs[0] in ("koṭi", "pakoṭi", "koṭippakoṭi", "akkhobhiṇī"):
        return "{{F-I1|ratti}} (como vīsati)"
    if fs and fs[0] == "bindu":
        return "{{N-U1|āyu}} (como cakkhu), sólo singular y sin vocativo"
    return "{{N-A1|citta}} (como sata)"


COMO_ORDINAL = "m. {{M-A1|purisa}}; f. en «ā» {{F-Ā1|kaññā}}, en «ī» {{F-Ī1|itthī}}; n. {{N-A1|citta}}"


def formas(s):
    """«Ekādasa, ekārasa» → ['ekādasa', 'ekārasa'] (la mayúscula es del
    documento, que numera la lista; el paradigma va en minúscula)."""
    if not s:
        return []
    return [v.strip()[0].lower() + v.strip()[1:] for v in s.split(",")]


ES_3 = [
 "El número (saṅkhyā) es de cinco clases: (1) número mixto (missaka-saṅkhyā), que se obtiene por adición: ekādasa, once, dvādasa, doce; (2) número multiplicativo (guṇita-saṅkhyā), que se obtiene por multiplicación: dvisataṃ, doscientos; (3) número agregativo (sambandha-saṅkhyā): aṭṭhasaṭṭhi-satasahassaṃ, 168.000, donde aṭṭhasaṭṭhi, 68, es un número mixto y satasahassaṃ, 100.000, uno multiplicativo —saṭṭhi, 60, y aṭṭha, 8, se multiplican por sahassaṃ, 1.000, y los totales se suman a satasahassaṃ: 100.000 + 60.000 + 8.000—; (4) número simbólico (saṅketa-saṅkhyā): la voz canda, luna, puede significar el número uno porque hay una sola luna en el mundo; la voz māsa, mes, el número doce porque hay doce meses en el año; (5) número múltiple (aneka-saṅkhyā): sahassaraṃsi, que tiene miles de (muchos) rayos, el sol; sahassa, mil, en este compuesto significa muchos.",
 "Según el género y el número (Kacc. §571): desde dvi (2) hasta aṭṭhārasa (18) tienen los tres géneros y son plurales; desde vīsati (20) hasta navuti (90) son femeninos singulares; desde sataṃ (100) hasta sahassaṃ (1.000) son neutros singulares; desde koṭi (10⁷) hasta akkhobhiṇī (10⁴²) son femeninos singulares; el resto, hasta asaṅkheyyaṃ (10¹⁴⁰), son neutros singulares.",
 "Declinación. Los numerales {{PM9|eka}} (1), {{P11|dvi}} (2), {{P12|ti}} (3), {{P13|catu}} (4) y {{#1|pañca}} (5) tienen su propio paradigma. Eka, que se declina en los tres géneros en singular y plural, cuando significa número es solamente singular; además del numeral uno, significa «solo(a)», «particular», etc. Dvi tiene un mismo paradigma para los tres géneros; ti y catu, uno distinto para cada género. Desde cha (6) hasta aṭṭhādasa (18) tienen un mismo paradigma para los tres géneros y se declinan como {{#1|pañca}}. Desde ekūnavīsati (19) hasta navanavuti (99) son femeninos singulares: los terminados en «i» se declinan como vīsati ({{F-I1|ratti}}); los terminados en «aṃ», como vīsaṃ. Desde sata (100) hasta sahassa (1.000), y todos los intermedios, se declinan como sata ({{N-A1|citta}}). Koṭi (10⁷), pakoṭi (10¹⁴), koṭippakoṭi (10²¹) y akkhobhiṇī (10⁴²) se declinan como vīsati; bindu (10⁴⁹) se declina como cakkhu ({{N-U1|āyu}}) solamente en singular y sin vocativo; el resto, desde abbuda (10⁵⁶), como sata.",
 "Hay dos maneras de representar el numeral: (1) el conteo (saṅkhyāna): bhikkhūnaṃ ekūnavīsati tiṭṭhati, diecinueve de los bhikkhus están de pie —ekūnavīsati, el sujeto, es singular, y el verbo va en singular, tiṭṭhati; el español pide el plural—; (2) aquello que se cuenta (saṅkhyeyya): ekūnavīsati bhikkhavo tiṭṭhanti, diecinueve bhikkhus están de pie.",
 "Aunque los numerales a partir de veinte son singulares, cuando hay división en grupos se usa el plural: dve vīsatiyo, dos veintes (40); dve satāni, dos cientos (200); bahūni satāni, muchos cientos; dve sahassāni, dos miles (2.000); bahūni sahassāni, muchos miles.",
]
EN_3 = [
 "Number (saṅkhyā) is of five kinds: (1) mixed number (missaka-saṅkhyā), obtained by addition: ekādasa, eleven, dvādasa, twelve; (2) multiplicative number (guṇita-saṅkhyā), obtained by multiplication: dvisataṃ, two hundred; (3) aggregative number (sambandha-saṅkhyā): aṭṭhasaṭṭhi-satasahassaṃ, 168,000, where aṭṭhasaṭṭhi, 68, is a mixed number and satasahassaṃ, 100,000, a multiplicative one —saṭṭhi, 60, and aṭṭha, 8, are multiplied by sahassaṃ, 1,000, and the totals are added to satasahassaṃ: 100,000 + 60,000 + 8,000—; (4) symbolic number (saṅketa-saṅkhyā): the word canda, moon, can mean the number one because there is only one moon in the world; the word māsa, month, the number twelve because there are twelve months in the year; (5) multiple number (aneka-saṅkhyā): sahassaraṃsi, having thousands of (many) rays, the sun; sahassa, a thousand, means many in this compound.",
 "By gender and number (Kacc. §571): from dvi (2) to aṭṭhārasa (18) they have the three genders and are plural; from vīsati (20) to navuti (90) they are feminine singular; from sataṃ (100) to sahassaṃ (1,000), neuter singular; from koṭi (10⁷) to akkhobhiṇī (10⁴²), feminine singular; the rest, up to asaṅkheyyaṃ (10¹⁴⁰), neuter singular.",
 "Declension. The numerals {{PM9|eka}} (1), {{P11|dvi}} (2), {{P12|ti}} (3), {{P13|catu}} (4) and {{#1|pañca}} (5) have their own paradigm. Eka, declined in the three genders in singular and plural, is singular only when it means the number; besides the numeral one it means «alone», «a certain», etc. Dvi has one paradigm for the three genders; ti and catu, a different one for each gender. From cha (6) to aṭṭhādasa (18) they have one paradigm for the three genders and are declined like {{#1|pañca}}. From ekūnavīsati (19) to navanavuti (99) they are feminine singular: those ending in «i» are declined like vīsati ({{F-I1|ratti}}); those ending in «aṃ», like vīsaṃ. From sata (100) to sahassa (1,000), and all the numerals in between, are declined like sata ({{N-A1|citta}}). Koṭi (10⁷), pakoṭi (10¹⁴), koṭippakoṭi (10²¹) and akkhobhiṇī (10⁴²) are declined like vīsati; bindu (10⁴⁹) is declined like cakkhu ({{N-U1|āyu}}) in the singular only and without vocative; the rest, from abbuda (10⁵⁶), like sata.",
 "There are two ways of representing the numeral: (1) the counting (saṅkhyāna): bhikkhūnaṃ ekūnavīsati tiṭṭhati, nineteen of the bhikkhus are standing —ekūnavīsati, the subject, is singular and the verb is singular, tiṭṭhati; Spanish requires the plural—; (2) what is counted (saṅkhyeyya): ekūnavīsati bhikkhavo tiṭṭhanti, nineteen bhikkhus are standing.",
 "Although the numerals from twenty on are singular, when there is division into groups the plural is used: dve vīsatiyo, two twenties (40); dve satāni, two hundreds (200); bahūni satāni, many hundreds; dve sahassāni, two thousands (2,000); bahūni sahassāni, many thousands.",
]
NOTAS_3 = [
 "Material preparado por Bhikkhu Nandisena sobre los capítulos II y V de Kaccāyana, II y V de la Rūpasiddhi y XXIV del Saddanīti-Suttamālā; no editado todavía (última revisión, 3 de junio de 2021; publicación IEBH 20160331-BN-T0052). El documento escribe «Aṭthasataṃ» (800); errata por «aṭṭhasataṃ», corregida aquí con el visto bueno del IEBH (sesión 58). Las potencias de diez, que el documento imprime sin superíndice (107, 1014…), se restituyen.",
 "Nahutaṃ (10.000) también puede significar 10²⁸.",
]
NOTAS_3_EN = [
 "Material prepared by Bhikkhu Nandisena on chapters II and V of Kaccāyana, II and V of the Rūpasiddhi and XXIV of the Saddanīti-Suttamālā; not yet edited (last revision, 3 June 2021; IEBH publication 20160331-BN-T0052). The document writes «Aṭthasataṃ» (800); a slip for «aṭṭhasataṃ», corrected here with the approval of the IEBH (session 58). The powers of ten, printed without superscript in the document (107, 1014…), are restored.",
 "Nahutaṃ (10,000) can also mean 10²⁸.",
]
ES_4 = [
 "Los ordinales se declinan en los tres géneros. Se forman agregando el sufijo «ma» a los cardinales: pañcamo, quinto; el femenino, con las inflexiones «ā» e «ī»: pañcamā, pañcamī, quinta; el neutro, con «ṃ»: pañcamaṃ jhānaṃ, quinta jhāna.",
 "Tras dvi (2) y ti (3) se coloca el sufijo «tiya»: dutiyo, segundo; tatiyo, tercero; femenino dutiyā, tatiyā; neutro dutiyaṃ, tatiyaṃ. Tras catu (4) y cha (6), el sufijo «ṭha»: catuttho, cuarto; chaṭṭho, sexto (también chaṭṭhamo); femenino catutthī, catutthā; chaṭṭhī, chaṭṭhā; neutro catutthaṃ jhānaṃ, cuarta jhāna; chaṭṭhaṃ.",
 "Los ordinales masculinos se declinan como {{M-A1|purisa}}; los femeninos en «ā», como {{F-Ā1|kaññā}}, y los terminados en «ī», como {{F-Ī1|itthī}}; los neutros, como {{N-A1|citta}}.",
]
EN_4 = [
 "The ordinals are declined in the three genders. They are formed by adding the suffix «ma» to the cardinals: pañcamo, fifth; the feminine, with the inflections «ā» and «ī»: pañcamā, pañcamī, fifth; the neuter, with «ṃ»: pañcamaṃ jhānaṃ, fifth jhāna.",
 "After dvi (2) and ti (3) the suffix «tiya» is added: dutiyo, second; tatiyo, third; feminine dutiyā, tatiyā; neuter dutiyaṃ, tatiyaṃ. After catu (4) and cha (6), the suffix «ṭha»: catuttho, fourth; chaṭṭho, sixth (also chaṭṭhamo); feminine catutthī, catutthā; chaṭṭhī, chaṭṭhā; neuter catutthaṃ jhānaṃ, fourth jhāna; chaṭṭhaṃ.",
 "Masculine ordinals are declined like {{M-A1|purisa}}; feminines in «ā», like {{F-Ā1|kaññā}}, and those ending in «ī», like {{F-Ī1|itthī}}; neuters, like {{N-A1|citta}}.",
]
NOTAS_4 = [
 "Del mismo documento «Numerales» de Bhikkhu Nandisena. El documento escribe «Paṭhamam (n)» —errata por «paṭhamaṃ»— y «catutthaṃ jhānaṃ, quinta jhāna» —por «cuarta»—; ambas corregidas aquí con el visto bueno del IEBH (sesión 58). Las casillas vacías son las que el documento no da; a partir del 23.º sólo trae el masculino.",
]
NOTAS_4_EN = [
 "From the same «Numerales» document by Bhikkhu Nandisena. The document writes «Paṭhamam (n)» —a slip for «paṭhamaṃ»— and «catutthaṃ jhānaṃ, quinta jhāna» —for «cuarta»—; both corrected here with the approval of the IEBH (session 58). Empty cells are those the document does not give; from the 23rd on it gives only the masculine.",
]


def cargar(nombre):
    return json.load(open(os.path.join(P, nombre), encoding="utf-8"))

def guardar(nombre, datos):
    ruta = os.path.join(P, nombre)
    json.dump(datos, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(ruta, "a", encoding="utf-8").write("\n")


def main():
    d = cargar("paradigmas.json")
    if any(p["codigo"] in ("#3", "#4") for p in d["paradigmas"]):
        if "--rehacer" not in sys.argv:
            print("#3 y #4 ya están; nada que hacer (--rehacer para reescribirlas).")
            return 0
        d["paradigmas"] = [p for p in d["paradigmas"] if p["codigo"] not in ("#3", "#4")]
        ix = cargar("indice.json")
        ix["entradas"] = [e for e in ix["entradas"] if e["codigo"] not in ("#3", "#4")]
        guardar("indice.json", ix)
    e3 = {"codigo": "#3", "paradigma": "los numerales cardinales (saṅkhyā)", "genero": "numeral",
          "doc": DOC, "titulo_doc": "NUMERALES",
          "subtitulo": "clases, género y número, declinación, lista",
          "parrafos": ES_3,
          "lista": {"columnas": ["número", "formas", "se declina como"],
                    "filas": [[n, formas(f), como_cardinal(n, formas(f))] for n, f in CARDINALES]},
          "notas": NOTAS_3}
    e4 = {"codigo": "#4", "paradigma": "los numerales ordinales", "genero": "numeral",
          "doc": DOC, "titulo_doc": "NUMERALES",
          "subtitulo": "formación, declinación, lista",
          "parrafos": ES_4,
          "lista": {"columnas": ["ordinal", "masculino", "femenino", "neutro", "se declina como"],
                    "filas": [[n, formas(m), formas(f), formas(x), COMO_ORDINAL] for n, m, f, x in ORDINALES]},
          "notas": NOTAS_4}
    i = next(k for k, p in enumerate(d["paradigmas"]) if p["codigo"] == "#2")
    d["paradigmas"][i + 1:i + 1] = [e3, e4]
    guardar("paradigmas.json", d)

    ix = cargar("indice.json")
    j = next(k for k, e in enumerate(ix["entradas"]) if e["codigo"] == "#2")
    ix["entradas"][j + 1:j + 1] = [
        {"codigo": "#3", "paradigma": e3["paradigma"], "doc": DOC, "genero": "numeral"},
        {"codigo": "#4", "paradigma": e4["paradigma"], "doc": DOC, "genero": "numeral"}]
    guardar("indice.json", ix)

    en = cargar("ingles.json")
    en["paradigmas"]["#3"] = {"paradigma": "the cardinal numerals (saṅkhyā)",
                              "subtitulo": "classes, gender and number, declension, list",
                              "parrafos": EN_3, "notas": NOTAS_3_EN}
    en["paradigmas"]["#4"] = {"paradigma": "the ordinal numerals",
                              "subtitulo": "formation, declension, list",
                              "parrafos": EN_4, "notas": NOTAS_4_EN}
    guardar("ingles.json", en)
    print("Incorporados #3 ({0} cardinales) y #4 ({1} ordinales). Ahora: generar_todo.py".format(
        len(CARDINALES), len(ORDINALES)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
