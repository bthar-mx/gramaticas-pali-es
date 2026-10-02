#!/usr/bin/env python3
# Decisión C (Angel, 2026-10-03): seguir las etiquetas de la Visuddhāyuṃ
# solo donde el libro las da. Se ejecuta una vez; se niega si datos.json no es v0.6.
import json, os, re, sys
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(R, "recursos", "clasificacion", "datos.json")
d = json.load(open(P, encoding="utf-8"))
if d["version"] != "0.6":
    sys.exit("datos.json no es v0.6; no se aplica")
S = d["suttas"]
DEC_ES, DEC_EN = "(Decisión del IEBH, 2026.)", "(IEBH decision, 2026.)"

def nueva_det(n, es, en, det_es, det_en):
    e = S[str(n)]["nota"]
    for k, add, det, lab in (("es", es, det_es, "Determinación"), ("en", en, det_en, "Determination")):
        t = e[k]
        m = re.search(r"\s*%s:[\s\S]*$" % lab, t)
        base = t[:m.start()] if m else t
        e[k] = "{0} {1} {2}: {3}".format(base.rstrip(), add, lab, det)

def add_sent(n, es, en):
    e = S[str(n)]["nota"]
    e["es"] = e["es"].rstrip() + " " + es
    e["en"] = e["en"].rstrip() + " " + en

# etiquetas
S["1"]["tipo"], S["1"]["vidhi"] = "P", ""
for n in ("24", "30"):
    S[n]["tipo"], S[n]["vidhi"] = "V", "paṭisedha"
S["51"]["vidhi"] = "atidesa"
S["320"]["vidhi"] = "liṅga-vacana"
for n in ("24", "51", "320"):
    S[n].pop("grupo", None)

nueva_det(1,
  "Clasificación según la Visuddhāyuṃ Kaccāyana-ṭīkā (PDF 52): de las tres clases de paribhāsā (saññaṅga, anaṅga, vidhyaṅga), «anaṅga»; y paribhāsā, no upari-bhāsā. Antes: pubbavākya (fuera de las cuatro clases) según Rūpasiddhi y la Bhāsāṭīkā. " + DEC_ES,
  "Classification following the Visuddhāyuṃ Kaccāyana-ṭīkā (PDF 52): of the three kinds of paribhāsā (saññaṅga, anaṅga, vidhyaṅga), “anaṅga”; and a paribhāsā, not an upari-bhāsā. Before: pubbavākya (outside the four kinds) following the Rūpasiddhi and the Bhāsāṭīkā. " + DEC_EN,
  "paribhāsā (anaṅga-paribhāsā).", "paribhāsā (anaṅga-paribhāsā).")
nueva_det(24,
  "Clasificación según la Visuddhāyuṃ Kaccāyana-ṭīkā (PDF 80): «sutta que impide todo el segundo pariccheda». Antes: ādesa (pakati) según Thitzana; la Bhāsāṭīkā ya lo llamaba paṭisedha-vidhi-sutta. " + DEC_ES,
  "Classification following the Visuddhāyuṃ Kaccāyana-ṭīkā (PDF 80): “sutta that blocks the whole second pariccheda”. Before: ādesa (pakati) following Thitzana; the Bhāsāṭīkā already called it a paṭisedha-vidhi-sutta. " + DEC_EN,
  "vidhi — paṭisedha.", "vidhi — paṭisedha.")
nueva_det(30,
  "Clasificación según la Visuddhāyuṃ Kaccāyana-ṭīkā (PDF 79–80 y 89): «paṭisedha (pakati) vidhi»; impide §31–§33 y §39. Antes: ādesa según la Kaccāyanavaṇṇanā y Thitzana (v0.6); paṭisedha hasta la v0.5 por Rū 58 (apavāda). " + DEC_ES,
  "Classification following the Visuddhāyuṃ Kaccāyana-ṭīkā (PDF 79–80 and 89): “paṭisedha (pakati) vidhi”; it blocks §31–§33 and §39. Before: ādesa following the Kaccāyanavaṇṇanā and Thitzana (v0.6); paṭisedha up to v0.5 on Rū 58 (apavāda). " + DEC_EN,
  "vidhi — paṭisedha.", "vidhi — paṭisedha.")
nueva_det(51,
  "Clasificación según la Visuddhāyuṃ Kaccāyana-ṭīkā (PDF 111): «suttātidesa», remisión a los suttas ya enunciados. Antes: ādesa (atidesa) según Thitzana. " + DEC_ES,
  "Classification following the Visuddhāyuṃ Kaccāyana-ṭīkā (PDF 111): “suttātidesa”, a reference back to the suttas already stated. Before: ādesa (atidesa) following Thitzana. " + DEC_EN,
  "vidhi — atidesa (clase propia).", "vidhi — atidesa (a class of its own).")
nueva_det(320,
  "Clasificación según la Visuddhāyuṃ Kaccāyana-ṭīkā (PDF 398): «no es kāriyātidesa; es vidhi del singular y del género neutro». Antes: ādesa (liṅga-vacana) por el «and so on» de Thitzana; Nyāsa lo llama atidesa. " + DEC_ES,
  "Classification following the Visuddhāyuṃ Kaccāyana-ṭīkā (PDF 398): “not a kāriyātidesa; a vidhi of singular number and neuter gender”. Before: ādesa (liṅga-vacana) by Thitzana’s “and so on”; the Nyāsa calls it atidesa. " + DEC_EN,
  "vidhi — liṅga-vacana (número y género; no atidesa).", "vidhi — liṅga-vacana (number and gender; not atidesa).")
add_sent(23, "La Visuddhāyuṃ no da clase a este sutta; su sutta hermano §24 se clasifica paṭisedha según ese libro.",
  "The Visuddhāyuṃ gives this sutta no class; its sibling sutta §24 is classified paṭisedha following that book.")
for n in (321, 322, 323):
    add_sent(n, "La Visuddhāyuṃ clasifica el §320 como vidhi de número y género (no atidesa); para este sutta no da clase.",
      "The Visuddhāyuṃ classifies §320 as a vidhi of number and gender (not atidesa); for this sutta it gives no class.")

# leyenda
d["vidhis"]["atidesa"] = {"es": "extensión (atidesa); clase propia según la Visuddhāyuṃ, fuera de las ocho", "en": "extension (atidesa); a class of its own according to the Visuddhāyuṃ, outside the eight", "fuera": True}
d["vidhis"]["liṅga-vacana"] = {"es": "número y género (liṅga-vacana); clase propia según la Visuddhāyuṃ, fuera de las ocho", "en": "number and gender (liṅga-vacana); a class of its own according to the Visuddhāyuṃ, outside the eight", "fuera": True}
if not any(e["tipo"] == "X" for e in S.values()):
    d["tipos"].pop("X", None)

d["version"], d["fecha"] = "0.7", "2026-10-03"
d["nota_version"]["es"] = "v0.7: los aforismos que la Visuddhāyuṃ Kaccāyana-ṭīkā clasifica expresamente siguen ese libro: §1 paribhāsā; §24 y §30 paṭisedha; §51 atidesa y §320 liṅga-vacana, con clase propia. " + d["nota_version"]["es"]
d["nota_version"]["en"] = "v0.7: the aphorisms that the Visuddhāyuṃ Kaccāyana-ṭīkā classifies explicitly follow that book: §1 paribhāsā; §24 and §30 paṭisedha; §51 atidesa and §320 liṅga-vacana, each a class of its own. " + d["nota_version"]["en"]
open(P, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))
print("v0.7 aplicada")
