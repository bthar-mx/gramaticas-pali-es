import pathlib
P = pathlib.Path(__file__).resolve().parents[2] / "recursos/clasificacion/plantilla.html"
t = P.read_text(encoding="utf-8")
def rep(a, b, n=1):
    global t
    assert t.count(a) == n, (a[:50], t.count(a)); t = t.replace(a, b)
G_ES = """grupo:{otra:['inflexión en el significado de otra','Uno de los suttas que dan una inflexión en el significado de otra inflexión: §306–§309, §311 y §312. El §310 queda fuera: da la séptima en significados de kāraka.'],
   vuddhi:['ādesa: vuddhi','Fortalecimiento (vuddhi). Kaccāyana (§404), Rūpasiddhi, Nyāsa y Niruttidīpanī la nombran como operación propia; en el esquema de ocho vidhis, Thitzana la cuenta dentro de la ādesa.'],
   pakati:['ādesa: pakati','Conservación de la forma natural (pakati). Thitzana la cuenta dentro de la ādesa; la Bhāsāṭīkā (§24) la llama paṭisedha.'],
   atidesa:['ādesa: atidesa','Extensión (atidesa): a una forma se le aplican las operaciones de otra. Clase propia en el esquema de seis tipos de sutta; en el de ocho vidhis, Thitzana la cuenta dentro de la ādesa.'],
   linga:['ādesa: liṅga-vacana','Asignación de género y número al compuesto. No se nombra entre las ocho; se cuenta en la ādesa por el «and so on» de Thitzana (decisión del IEBH).'],
   nipatana:['ādesa: nipātana','Formación por nipātana. No se nombra entre las ocho; se cuenta en la ādesa por el «and so on» de Thitzana (decisión del IEBH).'],
   univ:['ādesa: vuddhi, vikāra, viparīta','El sutta nombra seis operaciones; vuddhi, vikāra y viparīta se cuentan en la ādesa según Thitzana. Quedan ādesa, lopa y āgama.']},"""
G_EN = """grupo:{otra:['inflection in the sense of another','One of the suttas that give an inflection in the sense of another inflection: §306–§309, §311 and §312. §310 is outside the group: it gives the seventh in kāraka senses.'],
   vuddhi:['ādesa: vuddhi','Strengthening (vuddhi). Kaccāyana (§404), the Rūpasiddhi, the Nyāsa and the Niruttidīpanī name it as an operation of its own; in the eight-fold scheme of vidhis, Thitzana counts it under ādesa.'],
   pakati:['ādesa: pakati','Keeping the natural form (pakati). Thitzana counts it under ādesa; the Bhāsāṭīkā (§24) calls it paṭisedha.'],
   atidesa:['ādesa: atidesa','Extension (atidesa): the operations of one form are applied to another. A kind of its own in the six-fold scheme of suttas; in the eight-fold scheme of vidhis, Thitzana counts it under ādesa.'],
   linga:['ādesa: liṅga-vacana','Assignment of gender and number to the compound. Not named among the eight; counted under ādesa by Thitzana’s “and so on” (IEBH decision).'],
   nipatana:['ādesa: nipātana','Formation by nipātana. Not named among the eight; counted under ādesa by Thitzana’s “and so on” (IEBH decision).'],
   univ:['ādesa: vuddhi, vikāra, viparīta','The sutta names six operations; vuddhi, vikāra and viparīta count under ādesa according to Thitzana. Ādesa, lopa and āgama remain.']},"""
a_es = "grupo:{otra:['inflexión en el significado de otra','Uno de los suttas que dan una inflexión en el significado de otra inflexión: §306–§309, §311 y §312. El §310 queda fuera: da la séptima en significados de kāraka.']},"
a_en = "grupo:{otra:['inflection in the sense of another','One of the suttas that give an inflection in the sense of another inflection: §306–§309, §311 and §312. §310 is outside the group: it gives the seventh in kāraka senses.']},"
rep(a_es, G_ES); rep(a_en, G_EN)
rep("<dt>Nyāsa</dt><dd>${esc(e.base.nyasa[lang])}</dd></dl>",
    "<dt>Nyāsa</dt><dd>${esc(e.base.nyasa[lang])}</dd>${e.base.th?`<dt>Thitzana</dt><dd>${esc(e.base.th[lang])}</dd>`:''}</dl>")
OCHO_ES = "<p><strong>Las ocho clases de vidhi.</strong> Las operaciones se clasifican en las ocho clases del <i>Glosario</i> de Nandisena: lopa, dīgha, rassa, ādesa, āgama, paṭisedha, paccaya y vibhatti, que son también las del verso mnemónico de la tradición birmana. Ni <i>Rūpasiddhi</i> ni <i>Nyāsa</i> dan esta lista, y Kaccāyana mismo (§404) nombra aparte la vuddhi, el vikāra y el viparīta. Se sigue la explicación de A. Thitzana (<i>Kaccāyana</i>, vol. 2, Introducción, pp. 36–37): la ādesa abarca, además del cambio de una palabra en otra forma, «Vuddhi, Vipariyāya, Pakati, Atidesa and so on». Esos aforismos llevan la vidhi ādesa y una etiqueta que nombra la operación concreta (p. ej. «ādesa: vuddhi»); su fundamento cita a Thitzana, y la nota recoge cómo la nombran las demás fuentes.</p>\n  <p><strong>Fuentes y cautelas.</strong> <i>Rūpasiddhi</i> se cita"
OCHO_EN = "<p><strong>The eight kinds of vidhi.</strong> Operations are classified by the eight kinds of Nandisena’s <i>Glossary</i>: lopa, dīgha, rassa, ādesa, āgama, paṭisedha, paccaya and vibhatti, which are also those of the mnemonic verse of the Burmese tradition. Neither the <i>Rūpasiddhi</i> nor the <i>Nyāsa</i> gives this list, and Kaccāyana himself (§404) names vuddhi, vikāra and viparīta separately. A. Thitzana’s explanation is followed (<i>Kaccāyana</i>, vol. 2, Introduction, pp. 36–37): besides changing a word into another form, ādesa covers “Vuddhi, Vipariyāya, Pakati, Atidesa and so on”. These aphorisms carry the vidhi ādesa and a tag naming the specific operation (e.g. “ādesa: vuddhi”); their basis cites Thitzana, and the note records how the other sources name it.</p>\n  <p><strong>Sources and caveats.</strong> The <i>Rūpasiddhi</i> is cited"
rep("<p><strong>Fuentes y cautelas.</strong> <i>Rūpasiddhi</i> se cita", OCHO_ES)
rep("<p><strong>Sources and caveats.</strong> The <i>Rūpasiddhi</i> is cited", OCHO_EN)
P.write_text(t, encoding="utf-8"); print("ok")
