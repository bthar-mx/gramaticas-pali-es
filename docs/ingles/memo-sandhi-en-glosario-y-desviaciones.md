# Kaccāyana in English — Sandhi-Kappa pilot
## Working glossary and register of deviations from Bhikkhu U Nandisena's English

Draft 1 · 2026-09-03. Sections 1–4 were the proposal; the decisions Angel took the same day are marked inline, and §5 is the register of what the English page actually carries.

Sources compared: Nandisena, *Kaccāyana Byākaraṇaṃ, 1-Sandhi-Kappa* (English, 48 pp., project PDF) — "N-EN"; the published Spanish chapter, `gramaticas.buddha-dhamma.net/kaccayana/sandhi/`, version 1.4 (2026-08-20) — "ES"; the project Markdown draft `1. Sandhi-Kappa.md`; Pind, *Kaccāyana and Kaccāyanavutti* (PTS) for readings and canonical loci; Thitzana Vol. 2 for the word-count breakdowns.

---

## 1. Method (proposed)

1. **Base text = N-EN verbatim.** The English page is a revised edition of the Venerable's own English, not a back-translation of the Spanish. Where N-EN is sound it stands unchanged.
2. **Apparatus overlaid from the Spanish work:** Thitzana word-count breakdowns, the "Extension by *ca*" headers, project footnotes on the functions of *ca*/*vā*, the §-corrections, normalized canonical references, tooltips, cross-reference tips.
3. **Every departure from N-EN wording is registered** in §4 below (and, once we start, flagged sutta by sutta exactly as for the Spanish). Nothing is changed silently.
4. **Same source layout as the Spanish:** one Markdown file per chapter (`sandhi.en.md`), same sutta structure, so the generator can build `/en/kaccayana/sandhi/` from it with the EN/ES button preserving the `#sN` anchor.
5. **Text-critical notes (K, K-PTS) are restored** in the English and — proposal — added back to the Spanish (see §4.6).

---

## 2. English glossary (Sandhi-Kappa scope)

Column "N-EN" = how Nandisena actually renders the term in the Sandhi chapter, with the sutta where attested. Column "EN proposed" = what the English page would use. Where the two differ, the reason is in the last column.

### 2.1 Grammatical terms

| Pāḷi | N-EN (attested) | ES (locked) | EN proposed | Note |
|---|---|---|---|---|
| sandhi | "sandhi" (headers); "joining of words" (§10 vutti) | combinación eufónica | **sandhi**; in running prose "euphonic combination (*sandhi*)" on first appearance per section | Mirrors ES practice. N-EN's "joining of words" in §10 kept as his wording. |
| akkhara | letters (§1–2) | letras | letters | — |
| sara | vowels (§3) | vocales | vowels | — |
| byañjana | consonants (§6) | consonantes | consonants | — |
| rassa | short (§4) | corta | short | — |
| dīgha | long (§5) | larga | long | — |
| lahumattā | light-measured (§4) | de medida leve | light-measured | Keep N-EN's coinage. |
| vagga / vaggā | grouped (§7) | agrupadas | grouped | — |
| ghosa / aghosa | voiced / voiceless (§9) | sonoras / sordas | voiced / voiceless | — |
| niggahita | niggahita (§8) | niggahita (sin traducir) | niggahita | N-EN spells *niggahita*; PTS *niggahīta*. Keep N-EN. |
| lopa | elision; "come(s) to elision" (§12, §38) | elisión; "se elide" | elision; "is elided" | **Deviation:** N-EN alternates "come to elision" / "is elided" / "becomes elided" (§12 vutti vs fn 17). Proposal: "is/are elided" throughout, "elision" as noun. |
| āgama | insertion (§35, §36, §37) | inserción | insertion | — |
| ādesa | substitution; "is substituted by" (§17, §44) | sustitución; "se sustituye por" | substitution; "is substituted by" | — |
| dvebhāva | doubling (§28) | duplicación | doubling | — |
| sarūpa / asarūpa | similar / dissimilar (§13 + fn 19) | similar / disímil | similar / dissimilar | — |
| savaṇṇa / asavaṇṇa | "dissimilar" (§14) | disímil | dissimilar | **Flag:** N-EN uses "dissimilar" for both *asarūpa* (§13) and *asavaṇṇa* (§14). ES does the same. Acceptable, but a one-line footnote distinguishing the two (*asarūpa* = different place of articulation, per N-EN fn 19; *asavaṇṇa* = of a different vowel class) may be worth adding — Angel to decide. |
| pakati | original form(s) (§23–24) | forma original | original form | ES locked list has *pakati* → "natural" for later chapters; Sandhi uses "forma original". Keep N-EN here. |
| ṭhāna / ṭhāne | "in appropriate places" (§28–29, with fn 23 explaining his preference for the plural) | en el lugar apropiado (singular) | **in the appropriate place** (singular, parallel to ES) | Decided by Angel, 2026-09-03: singular in both languages. N-EN fn 23 is kept in both, followed by the sentence that the IEBH edition keeps the Pāḷi singular. Registered deviation. |
| saṃyoga | conjunct consonant (§41) | consonante conjunta | conjunct consonant | — |
| upasagga, nipāta | prefixes and particles (§51) | prefijos y partículas | prefixes and particles | — |
| suttantesu | in the Discourses (§1–2) | en los Discursos | in the Discourses | — |
| vutta-sandhi (§51) | "verse-sandhi" | "de verso" | verse-sandhi | **DUDA:** N-EN renders *vuttasandhīhi* as "verse-sandhi" (reading *vutta* = Skt *vṛtta*, metre). PTS note: K reads *vuttehi sarasandhīhi* ("by the vowel-sandhis that have been stated"). Keep N-EN and add his own fn 42 variant back (it was dropped in ES). |
| kappa | Chapter | capítulo | Chapter | — |
| kaṇḍa | Section | sección | Section | — |
| sutta | sutta | sutta | sutta | — |
| vutti | (not named) | vutti | vutti | — |

### 2.2 Optional-application particles (locked in ES; N-EN is consistent with them)

| Pāḷi | N-EN | ES | EN proposed |
|---|---|---|---|
| kvaci | sometimes (§14 ff.) | a veces | sometimes |
| vā | optionally (§13 ff.) | opcionalmente | optionally |
| navā | occasionally (§21–22) | ocasionalmente | occasionally |
| vibhāsā | — (not in Sandhi) | facultativamente | facultatively *(to confirm when first met in Nāma)* |
| vavatthitavibhāsā | "fixed alternative" (§32 fn 29) | alternativa fija | fixed alternative |

**Erratum found on the way:** the ES page's tooltip for *kvaci* reads "a veces / ocasionalmente", which merges the locked renderings of *kvaci* and *navā*. Should read "a veces" only.

### 2.3 Functions of *ca* (project footnotes; no N-EN equivalent — these are additions from Kaccāyana Bhāsāṭīkā / Kaccāyanavaṇṇanā already in the Spanish)

| Pāḷi | ES | EN proposed |
|---|---|---|
| anukaḍḍhana | arrastre (hacia este sutta / restrictivo) | **dragging** (Nandisena's own term, appendix to ch. 1) |
| sampiṇḍana | recolección | **collecting** ("and") |
| samuccaya | acumulación | **accumulating** ("and also") |
| avadhāraṇa | delimitación | **delimiting** |
| vācāsiliṭṭha | fluidez del habla | **smoothness of speech** |

| caggahaṇena | "By taking 'ca'" (N-EN §20, §35, §37, §41) | por la fuerza de "ca" | **By taking "ca"** (N-EN kept) |
| vāggahaṇena | "By taking 'optionally'" (§31) | por la fuerza de "opcionalmente" | By taking "vā" (optionally) |
| antaggahaṇena | "By taking 'anta'" (§49) | por la fuerza de "anta" | By taking "anta" |
| suttavibhāgena | "By breaking the Sutta (here, making similar suttas)" (§20) | dividiendo el sutta [en reglas similares] | By dividing the sutta [into similar rules] — *deviation, see §4.2* |

*Source for this table: the Venerable's appendix to his chapter 1, supplied by Angel 2026-09-03 and kept verbatim in `docs/fuentes/nandisena-apendice-sandhi-en.md`. It is his text and goes into the EN edition as is (ṁ normalized to ṃ). The `ca` footnotes in the Spanish Sandhi (§16, §20, §22, §27, §37) derive from it.*

### 2.4 Formulae

| Pāḷi | N-EN | ES | EN proposed |
|---|---|---|---|
| Tena kvattho? | What is the benefit of that [calling them "X"]? | ¿Cuál es el beneficio de eso [de llamarlas "X"]? | What is the benefit of that [calling them "X"]? — *Note: the locked ES list has kvattho → "¿Cuál es la utilidad del nombre…?"; Sandhi ES uses "beneficio". One of the two should give way; not an EN issue.* |
| Taṃ yathā? | Which are these? | ¿Cuáles son éstas? | Which are these? |
| Iti X nāma | These are called "X". | Éstas se llaman "X". | These are called "X". |
| X ti kasmā? | Why say "X"? | ¿Por qué se dice "X"? | Why say "X"? |
| [bracketed reason] | [To prevent the operation of this rule in the following:] | [Para evitar la aplicación de esta regla en los siguientes ejemplos] | [To prevent the operation of this rule in the following examples:] |
| Iti sandhi-kappe N kaṇḍo | Thus ends the N section of the chapter on sandhi | Así termina la N sección del capítulo de Sandhi | Thus ends the N section of the chapter on sandhi |
| (ME) | modern edition (§12 fn 18) | (EM) | (ME) |

### 2.5 Invocation and proper names

| Pāḷi | N-EN (verse a–b) | ES (locked) | EN proposed | Note |
|---|---|---|---|---|
| Jina | the Victorious One | el Victorioso | the Victorious One | — |
| Buddha | Buddha | Buddha | Buddha | — |
| Gaṇa | "the noble Sangha" | la noble Orden | **the noble Order** | Decided by Angel, 2026-09-03: "Order", parallel to ES. Deviation from N-EN wording, to be registered in the EN page. |
| Satthu vacana | the Word of the Teacher | la Palabra del Maestro | the Word of the Teacher | — |
| seyya | the best (fn 3: "the nine supramundane states") | lo mejor (fn: nava lokuttaradhammā) | the best | ES fn adds the Pāḷi *nava lokuttaradhammā*; carry into EN fn. |

### 2.6 Page chrome (generator strings)

| ES | EN |
|---|---|
| Ejemplos [con secuencia de formación] | Examples [with formation sequence] |
| Ejemplo | Example |
| Contraejemplos / Contraejemplo | Counter-examples / Counter-example *(N-EN writes "Counter examples")* |
| Secuencia | Sequence |
| Formación de palabras a partir de este sutta y los anteriores. | Formation of words from this and previous suttas. *(N-EN verbatim, §12)* |
| Extensión por "ca" (acumulación) | Extension by "ca" (samuccaya) |
| Extensión por "vā" (opcional) | Extension by "vā" (optional) |
| Extensión por "anta" | Extension by "anta" |
| Extensión por división del sutta (Suttavibhāgena) | Extension by division of the sutta (suttavibhāgena) |
| Explicación de los ejemplos | Explanation of the examples |
| [X + Y = N voces] | [X + Y = N words] *(Thitzana's own form: "[Sarā+sare+lopaṁ. 3 words]")* |
| Mostrar más (formación, etc.) | Show more (formation, etc.) |
| Ir a §… / filtrar | Go to §… / filter |
| Tabla de contenidos | Contents |
| Kaccāyana Sutta / Rūpasiddhi Sutta / Saddanīti-Suttamālā Sutta | same |
| Khuddaka-nikāya · tomo i, página 29 | Khuddaka-nikāya · vol. i, p. 29 |
| Modo oscuro/claro; Volver al inicio; Copiar; Compartir; Leído | Dark/light mode; Back to top; Copy; Share; Read |

---

## 3. Deviations from N-EN by category — Sandhi-Kappa

Each item states what N-EN has, what the English page would carry, and whether the same applies to the Spanish. "ES ok" = Spanish already has it; "ES fix" = Spanish also needs correction.

### 3.1 Reference corrections inside Nandisena's own text (verified against PDF and Pind)

| § | N-EN reads | Correct | ES |
|---|---|---|---|
| §20 | sequence "sā dhu (10); sāhu (20)" — § missing | (§10); (§20) | ES ok |
| §42 | "putha g eva (42)" | (§42) | ES ok |
| §45 | "Ajhāgamā: … ajjh āgamā (45)" | "Ajjhāgamā … (§45)" | ES ok |
| §51 | "Vijjhaggaṃ: vi adhi aggaṃ; vi ajjh aggaṃ (§42)" | **(§45)** — *adhi → ajjh* is §45; §42 is *Go sare puthass' āgamo* | ES ok (already §45) |
| §51 | Pāḷi list "anupaghāto" but sequence "Anūpaghāto" | anūpaghāto (Pind: anūpaghāto [Dhp 185]) | ES ok |
| §41 | "vidhūn' aggam iti" (twice) | **vidūn'** — Pind §38 and §41 both *vidūn' aggaṃ*; N-EN §38 itself has *vidūn'* | **ES fix** (ES copies *vidhūn'* in §41) |
| §19 | counter-example last step "iti 'assa (ME)" | "iti 'ssa (ME)" | ES ok |
| §31 | Pāḷi "Tan niccutaṃ" vs sequence "Tan nicuttaṃ" | niccutaṃ (both places) | ES ok. Decided by Angel 2026-09-03: the Burmese reading *niccutaṃ* (also in the Venerable's appendix), no note on PTS *nibbutaṃ*. |
| §32 | "paccatañ eva (§32)" | paccattañ eva | **ES fix** |
| §31 | "Evaṅ kho: … evaṅkho (§11); evaṅkho (ME)" | last step should be "evaṅ kho (ME)" (cf. every other ME step) | **ES fix** |
| §10 fn 14, §11 fn 16 | "See §13 for formal formation of the word" | **DUDA:** the formation is printed under Kacc. §12 (Rūp. 13). Either "§13" is the Rūpasiddhi number or a slip for §12. ES site has §13, ES draft had §12. Angel to decide; I lean §12. | pending |
| §2 sutta | "Akkharā pādayo" | Akkharā p' ādayo (Pind; ES ok) | ES ok |
| §1 vutti | "Sabbavacanānam attho" | Sabbavacanānaṃ | ES ok |
| §9 | "ga gha ṅ;" | ga gha ṅa | ES ok |
| §14 | "bandusseva (§11)" | bandhusseva | ES ok |
| §18 | "atth kh o assa (§10)" | attha kh o assa | ES ok |
| §36 | "Etha passath 'imaṃ" | passath' imaṃ | ES ok |
| §37 | "Pacesssati"; "naṃ pasaṃ santi" (Pāḷi line) | Pacessati; pasaṃsanti | ES ok |
| §38 | "Etam attthaṃ" | atthaṃ | ES ok |
| §25 | "Munī care / Sequence: / muni care / Sequence: / munī care" | one "Sequence:" | ES ok |
| §49 | "'"putha"" (stray quote) | "putha" | ES ok |
| passim | typos: "fourty-one" (fn 5), "seperately/seperate" (§12), "folowing" (§13), "occassionally" (§21), "consonat", "the the" (fn 16), "consonats" (§51) | corrected silently as typography, listed here once | — |

### 3.2 Wording changes to N-EN (each one to be approved)

1. **Sutta glosses.** N-EN gives deliberately telegraphic glosses that mirror the sūtra ("When a vowel, vowels elision." §12; "Long." §15; "And the previous." §16). ES expands them with brackets ("Las vocales se eliden cuando una vocal [sigue]"). **Decided by Angel, 2026-09-03: (b)** — the English glosses take the same bracketed expansions as the Spanish, for intelligibility; N-EN's words are kept and the additions go in square brackets, so the reader sees what is his and what is ours. Every expanded gloss is a registered deviation. The vutti line below the gloss stays N-EN. **Rule for the brackets (Angel, 2026-09-03; convenciones §1 bis):** a Pāḷi locative in the sutta means "follows" and an ablative means "after"; those words render the case and go **without** brackets ("When a vowel follows", "after a vowel"). Brackets are only for words the sutta does not contain (a supplied noun or verb). The Spanish Sandhi was aligned to this in §12, §31, §39, §46.
2. §20 "By breaking the Sutta (here, making similar suttas)" → "By dividing the sutta [into similar rules]" (ES parallel). Or keep. Angel.
3. §20, §35, §37, §41, §49: ES adds bold headers "Extensión por 'ca' (acumulación)" etc. EN adds the same headers (2.6). Pure apparatus; N-EN text under them unchanged.
4. §12, §23, §25 etc.: N-EN lists "Examples." then bare word lists; ES adds "Ejemplos [con secuencia de formación]" and numbered steps. EN follows ES layout, N-EN steps verbatim.
5. §32 "Tañ ñev' ettha: taṃ evettha" → "taṃ eva ettha" (ES expands the first step; clearer). Angel.
6. §27 N-EN "Sa ve. Same as before." → ES "Sa ve muni jātibhayaṃ adassi: igual que el cuarto." EN: "Sa ve muni jātibhayaṃ adassi: same as the fourth."
7. §29 vutti: N-EN "the first and third letters become the double of the second and fourth letters [voiceless and voiced] respectively" — ES rewrote as "se duplican como [la primera-segunda y la tercera-cuarta letra]" using N-EN fn 24. Keep N-EN sentence + fn 24 in EN; the ES rewrite stays ES-only unless Angel wants them parallel.
8. §41 vutti "if the syllable has a conjunct consonant, it becomes single consonant" → "…it becomes a single consonant" (article only).
9. §12 vutti fn 17 "Vowels become elided because of a vowel" — keep as N-EN's footnote.

### 3.3 Apparatus added (not in N-EN; already in ES; flagged as project/Thitzana/Bhāsāṭīkā material)

| Item | Source | Where |
|---|---|---|
| Word-count breakdowns "[… = N words]" on all 51 suttas | Thitzana Vol. 2 | header line |
| Functions of *ca* footnotes: §16 (anukaḍḍhana, restrictive), §20 (samuccaya), §22 (sampiṇḍana), §27 (sampiṇḍana), §37 (anukaḍḍhana) | **Nandisena's own appendix page** at the end of his chapter 1 (applications of *ca*; *kvaci / vā / navā / vibhāsā*), per Angel 2026-09-03 — not a project addition. The page is absent from the project's PDF slice; the English original is needed for the EN edition. | fn |
| §20 fn "Debido a 'ca' en el sutta" on "también" | project | fn |
| §1 fn: Pāḷi name *nava lokuttaradhammā* added to N-EN fn 3 | project | fn |
| §23 fn 55 "Dh. 72 tiene 'tiṇṇo pāraṅgato jhāyī'" | project textual note | fn |
| Glossary tooltips on Pāḷi terms (23 terms, list in site) | project | tooltip |
| Cross-reference tips on every §N (sutta + gloss) — generated from the gloss, so EN gets English tips automatically | generator | tooltip |
| "Extension by…" headers | project | header |
| Kacc./Rūp./Sadd. number tooltips | project | header |

### 3.4 Omissions in ES relative to N-EN (to restore in EN; Angel to decide for ES)

| § | N-EN content missing in ES |
|---|---|
| §26 | Counter-example "Upanī yati. Here the 'ī' of upanīyati does not become short." **and** N-EN fn 22 "It seems that this is not a satisfactory example." ES stops at "sāvittī chandaso". |
| §1 fn 1 | "Suboddhuṃ (K-PTS)" — variant reading |
| §1 fn 2 | "Vasantilaka Gāthā" — metre identification. Corrected to *vasantatilakā* in both languages (Angel, 2026-09-03; guía §5.1 quinquies). |
| §7 fn 10 | "Pañcapañca-akkharavanto (K)" — variant |
| §35 fn 31 | "Āragge (K)" — variant |
| §51 fn 42 | "Vuttehi sarasandhīhi (K)" — variant |
| §51 fn 43 | "Some teachers separate this as 'paraṃ ayanaṃ'" — **present** in ES (fn 184); listed for completeness |

Proposal: restore all five variant notes in EN as N-EN wrote them; add them to ES as "(K)" notes too — they are the Venerable's, and dropping them is a silent omission under the project's own rules.

### 3.5 Canonical references — two sigla systems, both Nandisena's (corrected 2026-09-03)

N-EN cites the Burmese (Chaṭṭha Saṅgāyana) edition by **volume and page**: "Khu. i, 67", "Khu. i, 13", "Vin. iii, 19". The Spanish Sandhi used a different siglum set — "Dh. 67", "Sn. 306", "J. i 74", "Khp. 6", "Ud. 148", "Vv. 119", "Bv. 322" — which resolves the Khuddaka volume into the specific work **while keeping the Burmese page number**. **Correction to the first draft of this memo:** that by-work system is the Venerable's own, used in his Spanish *Reglas de combinación eufónica* (2013: "tatrāyaṃ · Dh. 67", "anveti · Dh. 13"), so the numbers were never wrong — they are pages in both systems. The residual issue is only that a reader takes "Dh. 67" for a verse number. Checked against Pind:

| Passage | N-EN | ES | Actual |
|---|---|---|---|
| tatrāyam ādi (§10) | Khu. i, 67 | Dh. 67 | Dhp 375 |
| tatrābhiratim iccheyya (§11) | Khu. i, 29 | Dh. 26 *(sic: N-EN 29)* | Dhp 88 |
| yass' indriyāni (§12) | Khu. i, 27 | Dh. 27 | Dhp 94 |
| manopubbaṅgamā (§23) | Khu. i, 13 | Dh. 13 | Dhp 1 |
| pamādo maccuno padaṃ (§23) | Khu. i, 16 | Dh. 16 | Dhp 21 |
| sammā dhammaṃ vipassato (§25) | Khu. i, 67 | Dh. 67 | Dhp 373 |
| sāhu dassanam ariyānaṃ (§20) | Khu. i, 34 | Khu. i, 34 *(left unconverted)* | Dhp 206 |
| saddh' īdha vittaṃ (§15) | Khu. i, 306 | Sn. 306 | Sn 182 |
| na taṃ kammaṃ kataṃ sādhu (§31) | Khu. i, 23 | Khu. i, 23 *(unconverted)* | Dhp 67 |

Some 100 footnotes are affected. Additionally §11 and §31 still show "Khu. i, …" in the Pāḷi line (12 occurrences on the page), so the ES is internally mixed.

**Done (Angel, 2026-09-03):** option (a). The Spanish Sandhi now carries the base edition's citations inline in the Pāḷi block, exactly as Nāma and Kāraka do (guía de estilo §5.1 sexies); the English page inherits the same. Adding verified verse numbers (Dhp 375) to the tooltip remains an open offer — ~110 lookups against Pind, not yet done.

### 3.6 Spanish forms that depart from N-EN and Pind (ES errata, unrelated to EN but found here)

| § | ES | N-EN / Pind | Note |
|---|---|---|---|
| §15 | "Saddhīdha", "Cūbhayaṃ" (Pāḷi line, titles and final "(EM)" step) | "Saddh' īdha", "c' ūbhayaṃ" (N-EN; Pind *saddh' îdha*, *c' ûbhayaṃ*) | ES "Ejemplos" line has "c' ūbhayaṃ" but the Pāḷi line "cūbhayaṃ" — inconsistent; and the (EM) step is identical to the §11 step, so it shows nothing. |
| §16 | "Kiṃ sūdha" (title/Pāḷi) vs "kiṃ sū 'dha (EM)" (sequence) | "Kiṃ sū 'dha" | same inconsistency |
| §41 | vidhūn' | vidūn' | see 3.1 |
| §32 | paccatañ | paccattañ | see 3.1 |
| §31 | evaṅkho (EM) | evaṅ kho (ME) | see 3.1 |
| §10 fn / §11 fn | "Véase §13" | see DUDA in 3.1 | — |
| tooltip | kvaci: "a veces / ocasionalmente" | — | see 2.2 |
| §31, §11 | "(Khu. i, …)" left in Pāḷi lines | — | see 3.5 |

---

## 4. Proposed sequence of work

1. Angel rules on the open decisions: 2.1 *Gaṇa*, *ṭhāne*; 3.2 item 1 (gloss policy) and items 2, 5; 3.4 (restore variant notes in ES?); 3.5 (reference policy); 3.6 fixes to ES.
2. Generator: language parameter, chrome strings (2.6), `hreflang`, EN/ES button on chapter pages preserving `#sN`, `<html lang="en">`.
3. `sandhi.en.md` built from N-EN text + apparatus, one sutta at a time, approval per sutta as for Spanish. Fast where N-EN is sound; the sequences are copy-through.
4. Verification pass: every § in every sequence checked against the sutta it names (as done above for §51 *vijjhaggaṃ*), every ME step compared to the Pāḷi line.
5. Publish EN Sandhi; then Nāma and Kāraka on the same footing.

---

*All § numbers are Kaccāyana numbers. N-EN page references: §12 formation pp. 7–8; fn 22 p. 26; fn 23 p. 28; fn 29 p. 32; fn 42–43 p. 46.*

---

## 5. Register of deviations in `kaccayana/01-sandhi-kappa.en.md` as built (2026-09-03, session 45)

Base: N-EN verbatim. Everything below is where the English page differs from his printed text; each item follows a decision recorded above or the Spanish edition, as Angel instructed ("where the Spanish expanded, follow the Spanish").

**Decided terms.** Verse (a): "the noble Sangha" → "the noble Order". §28–29 and the *ṭhāne* tooltip: "in appropriate places" → "in the appropriate place" (singular); his fn 23 kept as fn 19 with the IEBH sentence. Functions of *ca* named as in his appendix (dragging, collecting, accumulating, delimiting).

**Bracketed glosses (convenciones §1 bis).** §3 "Among them, the eight [letters] ending in ‘o’ are called “vowels”" (N-EN: "Among them there are eight vowels are ending with ‘o’"); §4 "[vowels]"; §7 "The [groups of] five by five, ending in ‘ma’, are grouped"; §9 "[are used]"; §11 "carry [the consonant] to the following [letter]"; §12 "vowels [come to] elision"; §13 "the following [vowel is elided] after a dissimilar [vowel]"; §14 "when [the previous vowel has been] elided, [the following vowel becomes] dissimilar"; §17 "‘Y’ [is] the substitution"; §19 "All [the syllable] ‘ti’ [becomes] ‘c’"; §21 "[becomes]"; §23 "[vowels keep their] original [form]"; §31 "a grouped [consonant]"; §33 "[ṃ]"; §42 "[at the end]"; §43 "[insertion of ‘g’,]"; §46 "they are not [applied]"; §49 "[the end of]". "Follows" and "after" always unbracketed (locative / ablative).

**Wording aligned to the Spanish.** §6–7 vutti: ‘k’, ‘m’ → ‘ka’, ‘ma’. §10: "[With the phrase] “tatr āyam ādi” [the examples begin]" added (N-EN prints the phrase alone). §11: "Example:" line and bracketed answer to *yutte*. §20: "By dividing the sutta [into similar rules]" (N-EN "By breaking the Sutta (here, making similar suttas)"). §27: "Sa ve muni jātibhayaṃ adassi: same as the fourth" (N-EN "Sa ve. Same as before"); "No change." on the last two counter-examples. §31 vutti: "the last letter of the corresponding group". §32: "taṃ eva ettha" (N-EN "taṃ evettha"). §37 *ca*: "there is also ‘pa’ for ‘vi’" (N-EN "there is ‘pa’ of ‘vi’"). §39: "Here the rule does not apply." on both counter-examples. §41: "a single consonant". §42 gloss reordered as ES. §48: "Sometimes ‘paṭi’ for ‘pati’" / "substitution of ‘pati’ by ‘paṭi’" (N-EN has the direction inverted in both lines). §50: "substitution of ‘ava’ by ‘o’" (N-EN "of ‘ava’ for ‘o’"). §51: the examples given twice as in ES (quoted list with "Thus [they are formed] also with vowels / consonants", then "Formation sequences [in case of vowels / consonants]"); *parakkamo* sequence as ES — "par ā kamo (§10); par a kamo (§26)" — where N-EN prints "para kamo (§25)" (shortening is §26, not §25).

**Layout added (apparatus).** Headers "Examples [with formation sequence]:", "Counter-example(s):", "Explanation of the examples:", "Extension by “ca” (accumulating):", "Extension by “vā” (optional):", "Extension by “anta”:", "Extension by division of the sutta (suttavibhāgena):"; numbered sequences; word-count breakdowns "[… = N words]"; tooltips on 23 Pāḷi terms; "(ME)" kept as his.

**Corrections carried over from the Spanish work (guía §5.1 quinquies / sexies).** References inline as Nandisena prints them, with `Vi.` → `Vin.`, `Aṅ.` → `A.`, `khu.` → `Khu.`, and the ten §20 *suttavibhāga* references and `(A. iii, 424)` restored; §41 *vidūn’*; §32 *paccattañ*; §31 "evaṅ kho (ME)"; §15–16 *saddh’ īdha*, *c’ ūbhayaṃ*, *kiṃ sū ’dha* in titles and ME steps; §45 "Ajjhāgamā … (§45)"; §51 *vijjhaggaṃ* (§45) and *anūpaghāto*; §19 "iti ’ssa (ME)"; §9 "ṅa"; §14 "bandhusseva"; §18 "attha kh o assa"; notes 6–7 "See §12"; note 2 *vasantatilakā*. Typos of the PDF (seperately, occassionally, folowing, consonat, fourty) corrected silently.

**Footnotes.** Same 35 as the Spanish, same numbering. 1, 5, 26, 33 are his variant notes (K / K-PTS); 12, 15, 18, 29 are the *ca* notes, from his appendix; 13 and 14 from ES; 16 project (Khu. i, 72 = Dhp 414 reads *jhāyī*); 19 his fn 23 plus the IEBH sentence.

**Not yet in the English page.** The appendix itself (applications of *ca*; *kvaci / vā / navā / vibhāsā*): kept verbatim in `docs/fuentes/nandisena-apendice-sandhi-en.md`, to be published once its place in both editions is decided (the Spanish has it as `comun/terminologia-particulas.md`, not on the chapter page).
