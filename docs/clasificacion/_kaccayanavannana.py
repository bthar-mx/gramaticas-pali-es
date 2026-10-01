#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v0.6 de la clasificación: cotejo con la Kaccāyanavaṇṇanā (Mahāvijitāvī;
Rangún, 1916; facsímil de Internet Archive, ~/Tipitaka/nissaya/scans/annya/
kaccayanavannana-1916.pdf). Se ejecuta UNA vez (2026-10-01). No volver a
ejecutar: comprueba que la versión sea 0.5 y, si no, no hace nada.

- Añade base.kv (Kaccāyanavaṇṇanā) a §30, §285, §296, §400, §404, §405.
- §30: paṭisedha → ādesa (la Kaccāyanavaṇṇanā lo presenta como sustitución).
- Notas de §30, §285, §296, §400, §405 ampliadas.
- Plantilla: fila «Kaccāyanavaṇṇanā» en el fundamento, búsqueda y pie.
- Versión 0.6.
"""
import json, os, sys, unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATOS = os.path.join(RAIZ, "recursos", "clasificacion", "datos.json")
PLANT = os.path.join(RAIZ, "recursos", "clasificacion", "plantilla.html")
COPIA = os.path.join(RAIZ, "docs", "clasificacion", "datos-v0.5-antes-kaccayanavannana.json")

N = lambda s: unicodedata.normalize("NFC", s)

KV = {
 "30": {
  "es": "Facsímil de 1916, p. 32 del PDF: «idāni niggahitādesaṃ vidhātuṃ “aṃ byañjane niggahitan” ti vuttaṃ»; «byañjane niggahitassa amādeso pi hotī ti dassetuṃ»; en los ejemplos, «aṃ-ādesaṃ katvā»; y «… vidhisuttan ti veditabbaṃ».",
  "en": "1916 facsimile, PDF p. 32: “idāni niggahitādesaṃ vidhātuṃ ‘aṃ byañjane niggahitan’ ti vuttaṃ”; “byañjane niggahitassa amādeso pi hotī ti dassetuṃ”; in the examples, “aṃ-ādesaṃ katvā”; and “… vidhisuttan ti veditabbaṃ”."},
 "285": {
  "es": "Facsímil de 1916, p. 117 del PDF: sale del §284 («“liṅgatthe paṭhamā” ti suttato nikkhantaṃ») y se enuncia «ālapanatthādike liṅgatthe pi paṭhamāvibhatti hotī ti dassetuṃ»; no lo llama niyama.",
  "en": "1916 facsimile, PDF p. 117: it derives from §284 (“‘liṅgatthe paṭhamā’ ti suttato nikkhantaṃ”) and is stated “ālapanatthādike liṅgatthe pi paṭhamāvibhatti hotī ti dassetuṃ”; it does not call it a niyama."},
 "296": {
  "es": "Facsímil de 1916, p. 119 del PDF: «iminā hetvatthe tatiyāvibhattiṃ vikappeti».",
  "en": "1916 facsimile, PDF p. 119: “iminā hetvatthe tatiyāvibhattiṃ vikappeti”."},
 "400": {
  "es": "Facsímil de 1916, p. 145 del PDF: sale de los suttas que dan los sufijos con ‘ṇ’ indicativa («vā ṇapacce» y otros) y explica la vuddhi de la vocal inicial ante esos sufijos; nombra la operación vuddhi, sin asignarle clase.",
  "en": "1916 facsimile, PDF p. 145: it derives from the suttas that give the suffixes with indicatory ‘ṇ’ (“vā ṇapacce” and others) and explains the vuddhi of the initial vowel before those suffixes; it names the operation vuddhi without assigning it a class."},
 "404": {
  "es": "Facsímil de 1916, pp. 146–147 del PDF: enumera las seis operaciones (vuddhi, lopa, āgama, vikāra, viparīta, ādesa) y glosa lopa como «adassana»; no asigna clase.",
  "en": "1916 facsimile, PDF pp. 146–147: it lists the six operations (vuddhi, lopa, āgama, vikāra, viparīta, ādesa) and glosses lopa as “adassana”; it assigns no class."},
 "405": {
  "es": "Facsímil de 1916, p. 147 del PDF: «niyamena pana akārayuvaṇṇānaṃ yeva vuddhi hotī ti dassetuṃ»; y «paribhāsāsuttaṃ».",
  "en": "1916 facsimile, PDF p. 147: “niyamena pana akārayuvaṇṇānaṃ yeva vuddhi hotī ti dassetuṃ”; and “paribhāsāsuttaṃ”."},
}

def main():
    d = json.load(open(DATOS, encoding="utf-8"))
    if d["version"] != "0.5":
        print("datos.json no está en v0.5 ({0}); no se hace nada.".format(d["version"]))
        return 1
    json.dump(d, open(COPIA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    s = d["suttas"]

    for n, t in KV.items():
        s[n]["base"]["kv"] = {k: N(v) for k, v in t.items()}

    # §30: paṭisedha → ādesa
    e = s["30"]
    e["vidhi"] = "ādesa"
    e["op"] = {
     "es": "Cuando sigue una consonante, al niggahita le corresponde ‘aṃ’ (en lugar de elidirse).",
     "en": "When a consonant follows, the niggahita takes ‘aṃ’ (instead of being elided)."}
    e["nota"] = {
     "es": "Apavāda (Rū 58): impide la elisión y las demás sustituciones del niggahita ante consonante; formalmente «aṃ iti hoti». La Kaccāyanavaṇṇanā lo presenta como sustitución («niggahitādesaṃ vidhātuṃ», «amādeso pi hotī ti dassetuṃ») y lo llama vidhisutta. Hasta la v0.5 se clasificaba paṭisedha por su función de apavāda; ahora se sigue a la Kaccāyanavaṇṇanā, lo que concuerda con Thitzana, que cuenta la pakati dentro de la ādesa (§23, §24) (decisión del IEBH, 2026-10-01). Determinación: vidhi — ādesa.",
     "en": "Apavāda (Rū 58): it blocks the elision and the other substitutions of the niggahita before a consonant; formally “aṃ iti hoti”. The Kaccāyanavaṇṇanā presents it as a substitution (“niggahitādesaṃ vidhātuṃ”, “amādeso pi hotī ti dassetuṃ”) and calls it a vidhisutta. Up to v0.5 it was classified paṭisedha for its apavāda function; the Kaccāyanavaṇṇanā is now followed, which agrees with Thitzana, who counts pakati under ādesa (§23, §24) (IEBH decision, 2026-10-01). Determination: vidhi — ādesa."}

    def inserta(n, ancla_es, frase_es, ancla_en, frase_en):
        nota = s[n]["nota"]
        assert ancla_es in nota["es"] and ancla_en in nota["en"], n
        nota["es"] = nota["es"].replace(ancla_es, frase_es + " " + ancla_es, 1)
        nota["en"] = nota["en"].replace(ancla_en, frase_en + " " + ancla_en, 1)

    inserta("285", "Se clasifica por la forma.",
            "La Kaccāyanavaṇṇanā lo explica también como extensión al vocativo («… liṅgatthe pi paṭhamāvibhatti hotī ti dassetuṃ»), sin llamarlo niyama.",
            "Classified by form.",
            "The Kaccāyanavaṇṇanā also explains it as an extension to the vocative (“… liṅgatthe pi paṭhamāvibhatti hotī ti dassetuṃ”), without calling it a niyama.")
    inserta("296", "Determinación:",
            "La Kaccāyanavaṇṇanā lo dice expresamente: «iminā hetvatthe tatiyāvibhattiṃ vikappeti».",
            "Determination:",
            "The Kaccāyanavaṇṇanā says so expressly: “iminā hetvatthe tatiyāvibhattiṃ vikappeti”.")
    inserta("400", "Se sigue a Thitzana",
            "La Kaccāyanavaṇṇanā también la llama vuddhi, sin asignarle clase.",
            "Thitzana is followed",
            "The Kaccāyanavaṇṇanā also calls it vuddhi, without assigning it a class.")

    n405 = s["405"]["nota"]
    a_es, a_en = "Se sigue a los dos tratados, que lo dicen expresamente.", "The two treatises, which say so expressly, are followed."
    assert a_es in n405["es"] and a_en in n405["en"]
    n405["es"] = n405["es"].replace("En contra, la vutti",
        "La Kaccāyanavaṇṇanā lo llama también «paribhāsāsuttaṃ», con función de niyama («niyamena pana akārayuvaṇṇānaṃ yeva vuddhi hotī ti dassetuṃ»). En contra, la vutti", 1)
    n405["en"] = n405["en"].replace("Against this, the vutti",
        "The Kaccāyanavaṇṇanā also calls it “paribhāsāsuttaṃ”, with a niyama function (“niyamena pana akārayuvaṇṇānaṃ yeva vuddhi hotī ti dassetuṃ”). Against this, the vutti", 1)
    n405["es"] = n405["es"].replace(a_es, "Se sigue a las tres obras, que lo dicen expresamente.")
    n405["en"] = n405["en"].replace(a_en, "The three works, which say so expressly, are followed.")
    s["405"]["base"]["ru"]  # sin cambios

    for n in ("30", "285", "296", "400", "405"):
        for k in ("es", "en"):
            s[n]["nota"][k] = N(s[n]["nota"][k])

    d["version"] = "0.6"
    d["fecha"] = "2026-10-01"
    d["nota_version"] = {
     "es": "v0.6: cotejo con la Kaccāyanavaṇṇanā (Rangún, 1916) en §30, §285, §296, §400, §404 y §405; el §30 pasa de paṭisedha a ādesa. " + d["nota_version"]["es"],
     "en": "v0.6: checked against the Kaccāyanavaṇṇanā (Rangoon, 1916) at §30, §285, §296, §400, §404 and §405; §30 moves from paṭisedha to ādesa. " + d["nota_version"]["en"]}
    json.dump(d, open(DATOS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # Plantilla
    p = open(PLANT, encoding="utf-8").read()
    cambios = [
     ("${e.base.th?`<dt>Thitzana</dt><dd>${esc(e.base.th[lang])}</dd>`:''}",
      "${e.base.th?`<dt>Thitzana</dt><dd>${esc(e.base.th[lang])}</dd>`:''}${e.base.kv?`<dt>Kaccāyanavaṇṇanā</dt><dd>${esc(e.base.kv[lang])}</dd>`:''}"),
     ("e.base.ru.en,e.base.nyasa.en,", "e.base.ru.en,e.base.nyasa.en,e.base.kv?e.base.kv.en:'',"),
     ("Los dudosos se han contrastado con la <i>Kaccāyana Bhāsāṭīkā</i>, el <i>Saddanīti</i>",
      "Los dudosos se han contrastado con la <i>Kaccāyana Bhāsāṭīkā</i>, la <i>Kaccāyanavaṇṇanā</i>, el <i>Saddanīti</i>"),
     ("Doubtful cases were checked against the <i>Kaccāyana Bhāsāṭīkā</i>, the <i>Saddanīti</i>",
      "Doubtful cases were checked against the <i>Kaccāyana Bhāsāṭīkā</i>, the <i>Kaccāyanavaṇṇanā</i>, the <i>Saddanīti</i>"),
     ("unas y otras citas son paráfrasis hasta cotejarlas con el facsímil.",
      "unas y otras citas son paráfrasis hasta cotejarlas con el facsímil. La <i>Kaccāyanavaṇṇanā</i> (Mahāvijitāvī; Rangún, 1916) se cita por lectura directa del facsímil en escritura birmana, transliterada; por cotejar."),
     ("both are paraphrases until checked against the facsimile.",
      "both are paraphrases until checked against the facsimile. The <i>Kaccāyanavaṇṇanā</i> (Mahāvijitāvī; Rangoon, 1916) is cited from a direct reading of the Burmese-script facsimile, transliterated; to be checked."),
    ]
    for viejo, nuevo in cambios:
        assert p.count(viejo) == 1, viejo
        p = p.replace(viejo, nuevo)
    open(PLANT, "w", encoding="utf-8").write(p)
    print("Hecho: datos.json v0.6, plantilla actualizada; copia en", os.path.relpath(COPIA, RAIZ))
    return 0

if __name__ == "__main__":
    sys.exit(main())
