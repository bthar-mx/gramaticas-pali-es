# Aplica el esquema de ocho vidhis según Thitzana (vol. 2, Introducción, pp. 36–37)
# a recursos/clasificacion/datos.json. 2026-10-01. Ejecutado una vez; no volver a ejecutar.
import json, pathlib
P = pathlib.Path(__file__).resolve().parents[2] / "recursos/clasificacion/datos.json"
d = json.loads(P.read_text(encoding="utf-8"))
S = d["suttas"]
TH_ES = "Thitzana (vol. 2, Introducción, pp. 36–37)"
TH_EN = "Thitzana (vol. 2, Introduction, pp. 36–37)"
Q = "«Vuddhi, Vipariyāya, Pakati, Atidesa and so on, are also included»"
QE = "“Vuddhi, Vipariyāya, Pakati, Atidesa and so on, are also included”"
BASE = {
 "pakati": ("Introducción, pp. 36–37: dentro de la ādesa, " + Q + " (la pakati, en la ādesa).",
            "Introduction, pp. 36–37: under ādesa, " + QE + " (pakati, under ādesa)."),
 "atidesa": ("Introducción, pp. 36–37: dentro de la ādesa, " + Q + " (la atidesa, en la ādesa).",
             "Introduction, pp. 36–37: under ādesa, " + QE + " (atidesa, under ādesa)."),
 "vuddhi": ("Introducción, pp. 36–37: dentro de la ādesa, " + Q + " (la vuddhi, en la ādesa).",
            "Introduction, pp. 36–37: under ādesa, " + QE + " (vuddhi, under ādesa)."),
 "univ": ("Introducción, pp. 36–37: dentro de la ādesa, " + Q + " (vuddhi y vipariyāya, en la ādesa).",
          "Introduction, pp. 36–37: under ādesa, " + QE + " (vuddhi and vipariyāya, under ādesa)."),
 "linga": ("Introducción, pp. 36–37: dentro de la ādesa, " + Q + ". La liṅga-vacana no se nombra; se incluye por «and so on».",
           "Introduction, pp. 36–37: under ādesa, " + QE + ". Liṅga-vacana is not named; included by “and so on”."),
 "nipatana": ("Introducción, pp. 36–37: dentro de la ādesa, " + Q + ". La nipātana no se nombra; se incluye por «and so on».",
              "Introduction, pp. 36–37: under ādesa, " + QE + ". Nipātana is not named; included by “and so on”."),
}
N = {}  # n: (vidhi, grupo, nota_es, nota_en)
N["23"] = ("ādesa", "pakati",
 "La pakati (conservar la forma natural) no figura por su nombre entre las ocho vidhis. " + TH_ES + " la cuenta dentro de la ādesa (" + Q + "), y así se clasifica aquí. La Bhāsāṭīkā, en cambio, llama al sutta hermano §24 paṭisedha-vidhi-sutta, porque impide toda operación. Añade que §23 va primero para que «byañjane» siga por adhikāra en toda la tercera sección. Determinación: vidhi — ādesa (pakati).",
 "Pakati (keeping the natural form) is not named among the eight vidhis. " + TH_EN + " counts it under ādesa (" + QE + "), and it is so classified here. The Bhāsāṭīkā, by contrast, calls the sister sutta §24 a paṭisedha-vidhi-sutta, since it blocks every operation. It adds that §23 is placed first so that “byañjane” runs by adhikāra over the whole third section. Determination: vidhi — ādesa (pakati).")
N["24"] = ("ādesa", "pakati",
 "La Bhāsāṭīkā lo llama paṭisedha-vidhi-sutta (impide las operaciones de todos los suttas vocálicos anteriores). Se sigue a " + TH_ES + ", que cuenta la pakati dentro de la ādesa, como en el §23. Determinación: vidhi — ādesa (pakati).",
 "The Bhāsāṭīkā calls it a paṭisedha-vidhi-sutta (it prevents the operations of all the preceding vowel suttas). " + TH_EN + " is followed, who counts pakati under ādesa, as in §23. Determination: vidhi — ādesa (pakati).")
N["30"] = ("paṭisedha", None,
 "Apavāda (Rū): impide la elisión y la sustitución del niggahita ante consonante. Formalmente «aṃ iti hoti», funcionalmente una interdicción; se clasifica paṭisedha. Podría verse también como una pakati del niggahita, que Thitzana contaría en la ādesa (§23, §24); queda paṭisedha por su función de apavāda, por confirmar. Determinación: vidhi — paṭisedha.",
 "Apavāda (Rū): it blocks the elision and substitution of the niggahita before a consonant. Formally “aṃ iti hoti”, functionally a prohibition; classified paṭisedha. It could also be read as a pakati of the niggahita, which Thitzana would count under ādesa (§23, §24); it stays paṭisedha for its apavāda function, to be confirmed. Determination: vidhi — paṭisedha.")
N["51"] = ("ādesa", "atidesa",
 "La atidesa (extensión) es una clase propia en el esquema de seis citado por la Bhāsāṭīkā (saññā, paribhāsā, vidhi, niyama, atidesa, adhikāra). Rū llama atidesa a este sutta; la Bhāsāṭīkā lo llama suttātidesa y recoge que el Bālāvatāra y otros lo cuentan como vidhi-sutta. En el esquema de ocho vidhis, " + TH_ES + " cuenta la atidesa dentro de la ādesa. Determinación: vidhi — ādesa (atidesa; clase propia en el esquema de seis).",
 "Atidesa (extension) is a kind of its own in the six-fold scheme cited by the Bhāsāṭīkā (saññā, paribhāsā, vidhi, niyama, atidesa, adhikāra). Rū calls this sutta atidesa; the Bhāsāṭīkā calls it a suttātidesa and reports that the Bālāvatāra and others count it a vidhi-sutta. In the eight-fold scheme of vidhis, " + TH_EN + " counts atidesa under ādesa. Determination: vidhi — ādesa (atidesa; a kind of its own in the six-fold scheme).")
N["83"] = ("lopa + ādesa", "pakati",
 "Rū 67: apavāda del §13 («tadapavādena pubbalopam āha»): ante ‘aṃ’, una sustitución, un sufijo, etc., se elide la vocal precedente, no la siguiente. La segunda mitad mantiene natural (pakati) la vocal siguiente; la pakati se cuenta en la ādesa según " + TH_ES + ", como en §23–§24 (la Bhāsāṭīkā sobre el §24 la contaría como paṭisedha). Nyāsa nombra ambas: «pubbasaralopaṃ katvā … pakatibhāvaṃ katvā». Determinación: lopa + ādesa (pakati).",
 "Rū 67: an apavāda of §13 (“tadapavādena pubbalopam āha”): before ‘aṃ’, a substitute, a suffix, etc., the preceding vowel is elided, not the following one. The second half keeps the following vowel natural (pakati); pakati counts under ādesa according to " + TH_EN + ", as in §23–§24 (the Bhāsāṭīkā on §24 would count it as paṭisedha). Nyāsa names both: “pubbasaralopaṃ katvā … pakatibhāvaṃ katvā”. Determination: lopa + ādesa (pakati).")
N["187"] = ("ādesa", "atidesa",
 "Rū 108: «kāriyātideso ’yaṃ»; Nyāsa: «ntum iva katvā». La Bhāsāṭīkā y U Sīlānanda (clase 11) explican que ‘nta’ no se convierte realmente en ‘ntu’: simplemente se le aplican las operaciones prescritas para ‘ntu’. No es, pues, una sustitución en sentido estricto. En el esquema de cuatro es vidhi (la práctica del Bālāvatāra para la atidesa, según la Bhāsāṭīkā sobre el §51); en el de seis, atidesa; en el de ocho vidhis, " + TH_ES + " cuenta la atidesa dentro de la ādesa. Compárese con el §270. Determinación: vidhi — ādesa (atidesa).",
 "Rū 108: “kāriyātideso ’yaṃ”; Nyāsa: “ntum iva katvā”. The Bhāsāṭīkā and U Sīlānanda (class 11) explain that ‘nta’ does not actually become ‘ntu’: the operations prescribed for ‘ntu’ are simply carried out on it. So it is not a substitution in the strict sense. In the four-fold scheme it is a vidhi (the practice of the Bālāvatāra for atidesa, as the Bhāsāṭīkā reports on §51); in the six-fold scheme it is an atidesa; in the eight-fold scheme of vidhis, " + TH_EN + " counts atidesa under ādesa. Contrast §270. Determination: vidhi — ādesa (atidesa).")
N["318"] = ("ādesa", "pakati",
 "Rū 333 lo llama atidesa («ayam atideso»): aunque falte la inflexión, que era la causa, no se quiere que desaparezca su efecto. U Sīlānanda (clase ch4-1, ~13:00–15:00) lo explica como impedimento: «this sutta prevents changes being made». Sea pakati o atidesa, " + TH_ES + " cuenta ambas dentro de la ādesa; la Bhāsāṭīkā al §24 contaría la pakati como paṭisedha. Determinación: vidhi — ādesa (pakati).",
 "Rū 333 calls it an atidesa (“ayam atideso”): even though the inflection, which was the cause, is gone, its effect is not meant to disappear. U Sīlānanda (class ch4-1, ~13:00–15:00) explains it as a prohibition: “this sutta prevents changes being made”. Whether pakati or atidesa, " + TH_EN + " counts both under ādesa; the Bhāsāṭīkā on §24 would count pakati as paṭisedha. Determination: vidhi — ādesa (pakati).")
LING_ES = ("no es una de las ocho vidhis. Se marca «liṅga-vacana» (decisión del IEBH, 2026-10-01). Determinación: vidhi — liṅga-vacana.",
 "no figura por su nombre entre las ocho vidhis. Se cuenta en la ādesa, en la que " + TH_ES + " incluye, además del cambio de una palabra en otra forma, " + Q + " (decisión del IEBH, 2026-10-01). Determinación: vidhi — ādesa (liṅga-vacana).")
LING_EN = ("it is not one of the eight vidhis. Marked “liṅga-vacana” (IEBH decision, 2026-10-01). Determination: vidhi — liṅga-vacana.",
 "it is not named among the eight vidhis. It is counted under ādesa, which " + TH_EN + " extends beyond changing a word into another form: " + QE + " (IEBH decision, 2026-10-01). Determination: vidhi — ādesa (liṅga-vacana).")
ATI_ES = ("Como el §187, ninguna de las ocho vidhis. Determinación: vidhi — atidesa.",
 "Como el §187, en el esquema de ocho se cuenta en la ādesa (" + TH_ES + "). Determinación: vidhi — ādesa (atidesa).")
ATI_EN = ("Like §187, none of the eight vidhis. Determination: vidhi — atidesa.",
 "Like §187, in the eight-fold scheme it counts under ādesa (" + TH_EN + "). Determination: vidhi — ādesa (atidesa).")
NIP = {
 "391": (("Etiqueta «nipātana», no una de las ocho (decisión del IEBH, 2026-10-01). Determinación: vidhi — nipātana.",
          "La nipātana no figura por su nombre entre las ocho vidhis; se cuenta en la ādesa por el «and so on» de " + TH_ES + ", pues fija la forma de una palabra (decisión del IEBH, 2026-10-01). Determinación: vidhi — ādesa (nipātana)."),
         ("Label “nipātana”, not one of the eight (IEBH decision, 2026-10-01). Determination: vidhi — nipātana.",
          "Nipātana is not named among the eight vidhis; it is counted under ādesa by the “and so on” of " + TH_EN + ", since it fixes the form of a word (IEBH decision, 2026-10-01). Determination: vidhi — ādesa (nipātana).")),
 "394": (("No prescribe ninguna de las ocho operaciones: fija cómo se forman los numerales superiores, que se rematan por nipātana (§391). Determinación: vidhi — nipātana (decisión del IEBH, 2026-10-01).",
          "No prescribe por su nombre ninguna de las ocho operaciones: fija cómo se forman los numerales superiores, que se rematan por nipātana (§391). Como el §391, se cuenta en la ādesa (" + TH_ES + "). Determinación: vidhi — ādesa (nipātana)."),
         ("It prescribes none of the eight operations: it fixes how higher numerals are formed, completed by nipātana (§391). Determination: vidhi — nipātana (IEBH decision, 2026-10-01).",
          "It prescribes none of the eight operations by name: it fixes how higher numerals are formed, completed by nipātana (§391). Like §391, it counts under ādesa (" + TH_EN + "). Determination: vidhi — ādesa (nipātana).")),
 "395": (("Determinación: vidhi — nipātana (decisión del IEBH, 2026-10-01).",
          "Como el §391, se cuenta en la ādesa (" + TH_ES + "). Determinación: vidhi — ādesa (nipātana)."),
         ("Determination: vidhi — nipātana (IEBH decision, 2026-10-01).",
          "Like §391, it counts under ādesa (" + TH_EN + "). Determination: vidhi — ādesa (nipātana).")),
}
N["400"] = ("ādesa", "vuddhi",
 "Rūpasiddhi y Nyāsa nombran la vuddhi como operación propia: Nyāsa la nombra como nombra las demás («ādisarassa vuddhiṃ katvā», «akārassa ākāravuddhiṃ katvā»), y Rū la enumera junto a las otras («kāritabyapadesa-ṇalopa-vuddhiyo», Rū 569). Kaccāyana la nombra aparte en §404 y la regula con la paribhāsā §405; Niruttidīpanī la cuenta como clase propia de operación («lopo, dīgho, rasso, vuddhi, ādeso, āgamo, dvibhāvo, vipallāso»). El esquema de ocho vidhis (Glosario de Nandisena; verso mnemónico de la tradición birmana) no la nombra; " + TH_ES + " explica que la ādesa incluye " + Q + ". Se sigue a Thitzana (decisión del IEBH, 2026-10-01). Determinación: vidhi — ādesa (vuddhi).",
 "The Rūpasiddhi and the Nyāsa name vuddhi as an operation of its own: the Nyāsa names it as it names the others (“ādisarassa vuddhiṃ katvā”, “akārassa ākāravuddhiṃ katvā”), and the Rūpasiddhi lists it alongside them (“kāritabyapadesa-ṇalopa-vuddhiyo”, Rū 569). Kaccāyana names it separately in §404 and regulates it with the paribhāsā §405; the Niruttidīpanī counts it as an operation of its own (“lopo, dīgho, rasso, vuddhi, ādeso, āgamo, dvibhāvo, vipallāso”). The eight-fold scheme of vidhis (Nandisena’s Glossary; the mnemonic verse of the Burmese tradition) does not name it; " + TH_EN + " explains that ādesa includes " + QE + ". Thitzana is followed (IEBH decision, 2026-10-01). Determination: vidhi — ādesa (vuddhi).")
N["404"] = ("ādesa + lopa + āgama", "univ",
 "Uno de los cuatro suttas universales de Kaccāyana (nota 36 de la traducción del capítulo; U Sīlānanda los llama «universal suttas» y también «nipātana suttas», clases ch5-7 y ch7-5). Nombra seis operaciones: vuddhi, lopa, āgama, vikāra, viparīta y ādesa. En el esquema de ocho vidhis, " + TH_ES + " cuenta dentro de la ādesa la vuddhi y la vipariyāya (= viparīta), «and so on»; el vikāra (cambio de una letra en otra) se cuenta también en la ādesa. Quedan tres vidhis (decisión del IEBH, 2026-10-01). Determinación: vidhi — ādesa + lopa + āgama.",
 "One of Kaccāyana’s four universal suttas (note 36 of the chapter translation; U Sīlānanda calls them “universal suttas” and also “nipātana suttas”, classes ch5-7 and ch7-5). It names six operations: vuddhi, lopa, āgama, vikāra, viparīta and ādesa. In the eight-fold scheme of vidhis, " + TH_EN + " counts vuddhi and vipariyāya (= viparīta) under ādesa, “and so on”; vikāra (changing one letter into another) also counts under ādesa. Three vidhis remain (IEBH decision, 2026-10-01). Determination: vidhi — ādesa + lopa + āgama.")
BASEKEY = {"23":"pakati","24":"pakati","51":"atidesa","83":"pakati","187":"atidesa","318":"pakati","320":"linga","321":"linga","322":"linga","323":"linga","331":"atidesa","332":"atidesa","391":"nipatana","394":"nipatana","395":"nipatana","400":"vuddhi","404":"univ"}
GRUPO = {"320":"linga","321":"linga","322":"linga","323":"linga","331":"atidesa","332":"atidesa","391":"nipatana","394":"nipatana","395":"nipatana"}
def rep(s, a, b, k):
    assert a in s, (k, a[:40]); return s.replace(a, b)
for k, (v, g, es, en) in N.items():
    e = S[k]; e["vidhi"] = v
    if g: e["grupo"] = g
    e["nota"] = {"es": es, "en": en}
for k in ("320","321","322","323"):
    e = S[k]; e["vidhi"] = "ādesa"
    e["nota"]["es"] = rep(e["nota"]["es"], *LING_ES, k); e["nota"]["en"] = rep(e["nota"]["en"], *LING_EN, k)
for k in ("331","332"):
    e = S[k]; e["vidhi"] = "ādesa"
    e["nota"]["es"] = rep(e["nota"]["es"], *ATI_ES, k); e["nota"]["en"] = rep(e["nota"]["en"], *ATI_EN, k)
for k, (xes, xen) in NIP.items():
    e = S[k]; e["vidhi"] = "ādesa"
    e["nota"]["es"] = rep(e["nota"]["es"], *xes, k); e["nota"]["en"] = rep(e["nota"]["en"], *xen, k)
for k, g in GRUPO.items(): S[k]["grupo"] = g
for k, b in BASEKEY.items():
    es, en = BASE[b]; S[k]["base"]["th"] = {"es": es, "en": en}
for x in ("atidesa","liṅga-vacana","vuddhi","vikāra","viparīta","nipātana"):
    d["vidhis"].pop(x)
d["vidhis"]["ādesa"] = {"es": "sustitución; según Thitzana, incluye también vuddhi, vipariyāya, pakati, atidesa, etc.",
                        "en": "substitution; according to Thitzana, it also includes vuddhi, vipariyāya, pakati, atidesa, etc."}
d["version"] = "0.5"; d["fecha"] = "2026-10-01"
d["nota_version"] = {"es": "Se sigue el esquema de ocho vidhis según Thitzana: vuddhi, pakati, atidesa y demás operaciones sin clase propia pasan a ādesa, con una etiqueta que las nombra.",
                     "en": "The eight-fold scheme of vidhis is followed as Thitzana explains it: vuddhi, pakati, atidesa and the other operations without a class of their own go under ādesa, with a tag that names them."}
eight = set(d["vidhis"])
for k, e in S.items():
    for p in (e.get("vidhi") or "").split("+"):
        assert not p.strip() or p.strip() in eight, (k, p)
P.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", len(S))
