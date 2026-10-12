# Kaccāyana in English — Sandhi-Kappa pilot
## Working glossary and register of deviations from Bhikkhu U Nandisena's English

Draft 1 · 2026-09-03. Sections 1–4 were the proposal; the decisions IEBH took the same day are marked inline, and §5 is the register of what the English page actually carries.

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
| savaṇṇa / asavaṇṇa | "dissimilar" (§14) | disímil | dissimilar | **Flag:** N-EN uses "dissimilar" for both *asarūpa* (§13) and *asavaṇṇa* (§14). ES does the same. Acceptable, but a one-line footnote distinguishing the two (*asarūpa* = different place of articulation, per N-EN fn 19; *asavaṇṇa* = of a different vowel class) may be worth adding — the IEBH to decide. |
| pakati | original form(s) (§23–24) | forma original | original form | ES locked list has *pakati* → "natural" for later chapters; Sandhi uses "forma original". Keep N-EN here. |
| ṭhāna / ṭhāne | "in appropriate places" (§28–29, with fn 23 explaining his preference for the plural) | en el lugar apropiado (singular) | **in the appropriate place** (singular, parallel to ES) | Decided by the IEBH, 2026-09-03: singular in both languages. N-EN fn 23 is kept in both, followed by the sentence that the IEBH edition keeps the Pāḷi singular. Registered deviation. |
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

*Source for this table: the Venerable's appendix to his chapter 1, supplied by the IEBH 2026-09-03 and kept verbatim in `docs/fuentes/nandisena-apendice-sandhi-en.md`. It is his text and goes into the EN edition as is (ṁ normalized to ṃ). The `ca` footnotes in the Spanish Sandhi (§16, §20, §22, §27, §37) derive from it.*

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
| Gaṇa | "the noble Sangha" | la noble Orden | **the noble Order** | Decided by the IEBH, 2026-09-03: "Order", parallel to ES. Deviation from N-EN wording, to be registered in the EN page. |
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
| §31 | Pāḷi "Tan niccutaṃ" vs sequence "Tan nicuttaṃ" | niccutaṃ (both places) | ES ok. Decided by the IEBH 2026-09-03: the Burmese reading *niccutaṃ* (also in the Venerable's appendix), no note on PTS *nibbutaṃ*. |
| §32 | "paccatañ eva (§32)" | paccattañ eva | **ES fix** |
| §31 | "Evaṅ kho: … evaṅkho (§11); evaṅkho (ME)" | last step should be "evaṅ kho (ME)" (cf. every other ME step) | **ES fix** |
| §10 fn 14, §11 fn 16 | "See §13 for formal formation of the word" | **DUDA:** the formation is printed under Kacc. §12 (Rūp. 13). Either "§13" is the Rūpasiddhi number or a slip for §12. ES site has §13, ES draft had §12. the IEBH to decide; I lean §12. | pending |
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

1. **Sutta glosses.** N-EN gives deliberately telegraphic glosses that mirror the sūtra ("When a vowel, vowels elision." §12; "Long." §15; "And the previous." §16). ES expands them with brackets ("Las vocales se eliden cuando una vocal [sigue]"). **Decided by the IEBH, 2026-09-03: (b)** — the English glosses take the same bracketed expansions as the Spanish, for intelligibility; N-EN's words are kept and the additions go in square brackets, so the reader sees what is his and what is ours. Every expanded gloss is a registered deviation. The vutti line below the gloss stays N-EN. **Rule for the brackets (el IEBH, 2026-09-03; convenciones §1 bis):** a Pāḷi locative in the sutta means "follows" and an ablative means "after"; those words render the case and go **without** brackets ("When a vowel follows", "after a vowel"). Brackets are only for words the sutta does not contain (a supplied noun or verb). The Spanish Sandhi was aligned to this in §12, §31, §39, §46.
2. §20 "By breaking the Sutta (here, making similar suttas)" → "By dividing the sutta [into similar rules]" (ES parallel). Or keep. El IEBH.
3. §20, §35, §37, §41, §49: ES adds bold headers "Extensión por 'ca' (acumulación)" etc. EN adds the same headers (2.6). Pure apparatus; N-EN text under them unchanged.
4. §12, §23, §25 etc.: N-EN lists "Examples." then bare word lists; ES adds "Ejemplos [con secuencia de formación]" and numbered steps. EN follows ES layout, N-EN steps verbatim.
5. §32 "Tañ ñev' ettha: taṃ evettha" → "taṃ eva ettha" (ES expands the first step; clearer). El IEBH.
6. §27 N-EN "Sa ve. Same as before." → ES "Sa ve muni jātibhayaṃ adassi: igual que el cuarto." EN: "Sa ve muni jātibhayaṃ adassi: same as the fourth."
7. §29 vutti: N-EN "the first and third letters become the double of the second and fourth letters [voiceless and voiced] respectively" — ES rewrote as "se duplican como [la primera-segunda y la tercera-cuarta letra]" using N-EN fn 24. Keep N-EN sentence + fn 24 in EN; the ES rewrite stays ES-only unless the IEBH wants them parallel.
8. §41 vutti "if the syllable has a conjunct consonant, it becomes single consonant" → "…it becomes a single consonant" (article only).
9. §12 vutti fn 17 "Vowels become elided because of a vowel" — keep as N-EN's footnote.

### 3.3 Apparatus added (not in N-EN; already in ES; flagged as project/Thitzana/Bhāsāṭīkā material)

| Item | Source | Where |
|---|---|---|
| Word-count breakdowns "[… = N words]" on all 51 suttas | Thitzana Vol. 2 | header line |
| Functions of *ca* footnotes: §16 (anukaḍḍhana, restrictive), §20 (samuccaya), §22 (sampiṇḍana), §27 (sampiṇḍana), §37 (anukaḍḍhana) | **Nandisena's own appendix page** at the end of his chapter 1 (applications of *ca*; *kvaci / vā / navā / vibhāsā*), per IEBH 2026-09-03 — not a project addition. The page is absent from the project's PDF slice; the English original is needed for the EN edition. | fn |
| §20 fn "Debido a 'ca' en el sutta" on "también" | project | fn |
| §1 fn: Pāḷi name *nava lokuttaradhammā* added to N-EN fn 3 | project | fn |
| §23 fn 55 "Dh. 72 tiene 'tiṇṇo pāraṅgato jhāyī'" | project textual note | fn |
| Glossary tooltips on Pāḷi terms (23 terms, list in site) | project | tooltip |
| Cross-reference tips on every §N (sutta + gloss) — generated from the gloss, so EN gets English tips automatically | generator | tooltip |
| "Extension by…" headers | project | header |
| Kacc./Rūp./Sadd. number tooltips | project | header |

### 3.4 Omissions in ES relative to N-EN (to restore in EN; the IEBH to decide for ES)

| § | N-EN content missing in ES |
|---|---|
| §26 | Counter-example "Upanī yati. Here the 'ī' of upanīyati does not become short." **and** N-EN fn 22 "It seems that this is not a satisfactory example." ES stops at "sāvittī chandaso". |
| §1 fn 1 | "Suboddhuṃ (K-PTS)" — variant reading |
| §1 fn 2 | "Vasantilaka Gāthā" — metre identification. Corrected to *vasantatilakā* in both languages (el IEBH, 2026-09-03; guía §5.1 quinquies). |
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

**Done (el IEBH, 2026-09-03):** option (a). The Spanish Sandhi now carries the base edition's citations inline in the Pāḷi block, exactly as Nāma and Kāraka do (guía de estilo §5.1 sexies); the English page inherits the same. Adding verified verse numbers (Dhp 375) to the tooltip remains an open offer — ~110 lookups against Pind, not yet done.

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

1. El IEBH rules on the open decisions: 2.1 *Gaṇa*, *ṭhāne*; 3.2 item 1 (gloss policy) and items 2, 5; 3.4 (restore variant notes in ES?); 3.5 (reference policy); 3.6 fixes to ES.
2. Generator: language parameter, chrome strings (2.6), `hreflang`, EN/ES button on chapter pages preserving `#sN`, `<html lang="en">`.
3. `sandhi.en.md` built from N-EN text + apparatus, one sutta at a time, approval per sutta as for Spanish. Fast where N-EN is sound; the sequences are copy-through.
4. Verification pass: every § in every sequence checked against the sutta it names (as done above for §51 *vijjhaggaṃ*), every ME step compared to the Pāḷi line.
5. Publish EN Sandhi; then Nāma and Kāraka on the same footing.

---

*All § numbers are Kaccāyana numbers. N-EN page references: §12 formation pp. 7–8; fn 22 p. 26; fn 23 p. 28; fn 29 p. 32; fn 42–43 p. 46.*

---

## 5. Register of deviations in `kaccayana/01-sandhi-kappa.en.md` as built (2026-09-03, session 45)

Base: N-EN verbatim. Everything below is where the English page differs from his printed text; each item follows a decision recorded above or the Spanish edition, as IEBH instructed ("where the Spanish expanded, follow the Spanish").

**Decided terms.** Verse (a): "the noble Sangha" → "the noble Order". §28–29 and the *ṭhāne* tooltip: "in appropriate places" → "in the appropriate place" (singular); his fn 23 kept as fn 19 with the IEBH sentence. Functions of *ca* named as in his appendix (dragging, collecting, accumulating, delimiting).

**Bracketed glosses (convenciones §1 bis).** §3 "Among them, the eight [letters] ending in ‘o’ are called “vowels”" (N-EN: "Among them there are eight vowels are ending with ‘o’"); §4 "[vowels]"; §7 "The [groups of] five by five, ending in ‘ma’, are grouped"; §9 "[are used]"; §11 "carry [the consonant] to the following [letter]"; §12 "vowels [come to] elision"; §13 "the following [vowel is elided] after a dissimilar [vowel]"; §14 "when [the previous vowel has been] elided, [the following vowel becomes] dissimilar"; §17 "‘Y’ [is] the substitution"; §19 "All [the syllable] ‘ti’ [becomes] ‘c’"; §21 "[becomes]"; §23 "[vowels keep their] original [form]"; §31 "a grouped [consonant]"; §33 "[ṃ]"; §42 "[at the end]"; §43 "[insertion of ‘g’,]"; §46 "they are not [applied]"; §49 "[the end of]". "Follows" and "after" always unbracketed (locative / ablative).

**Wording aligned to the Spanish.** §6–7 vutti: ‘k’, ‘m’ → ‘ka’, ‘ma’. §10: "[With the phrase] “tatr āyam ādi” [the examples begin]" added (N-EN prints the phrase alone). §11: "Example:" line and bracketed answer to *yutte*. §20: "By dividing the sutta [into similar rules]" (N-EN "By breaking the Sutta (here, making similar suttas)"). §27: "Sa ve muni jātibhayaṃ adassi: same as the fourth" (N-EN "Sa ve. Same as before"); "No change." on the last two counter-examples. §31 vutti: "the last letter of the corresponding group". §32: "taṃ eva ettha" (N-EN "taṃ evettha"). §37 *ca*: "there is also ‘pa’ for ‘vi’" (N-EN "there is ‘pa’ of ‘vi’"). §39: "Here the rule does not apply." on both counter-examples. §41: "a single consonant". §42 gloss reordered as ES. §48: "Sometimes ‘paṭi’ for ‘pati’" / "substitution of ‘pati’ by ‘paṭi’" (N-EN has the direction inverted in both lines). §50: "substitution of ‘ava’ by ‘o’" (N-EN "of ‘ava’ for ‘o’"). §51: the examples given twice as in ES (quoted list with "Thus [they are formed] also with vowels / consonants", then "Formation sequences [in case of vowels / consonants]"); *parakkamo* sequence as ES — "par ā kamo (§10); par a kamo (§26)" — where N-EN prints "para kamo (§25)" (shortening is §26, not §25).

**Layout added (apparatus).** Headers "Examples [with formation sequence]:", "Counter-example(s):", "Explanation of the examples:", "Extension by “ca” (accumulating):", "Extension by “vā” (optional):", "Extension by “anta”:", "Extension by division of the sutta (suttavibhāgena):"; numbered sequences; word-count breakdowns "[… = N words]"; tooltips on 23 Pāḷi terms; "(ME)" kept as his.

**Corrections carried over from the Spanish work (guía §5.1 quinquies / sexies).** References inline as Nandisena prints them, with `Vi.` → `Vin.`, `Aṅ.` → `A.`, `khu.` → `Khu.`, and the ten §20 *suttavibhāga* references and `(A. iii, 424)` restored; §41 *vidūn’*; §32 *paccattañ*; §31 "evaṅ kho (ME)"; §15–16 *saddh’ īdha*, *c’ ūbhayaṃ*, *kiṃ sū ’dha* in titles and ME steps; §45 "Ajjhāgamā … (§45)"; §51 *vijjhaggaṃ* (§45) and *anūpaghāto*; §19 "iti ’ssa (ME)"; §9 "ṅa"; §14 "bandhusseva"; §18 "attha kh o assa"; notes 6–7 "See §12"; note 2 *vasantatilakā*. Typos of the PDF (seperately, occassionally, folowing, consonat, fourty) corrected silently.

**Footnotes.** Same 35 as the Spanish, same numbering. 1, 5, 26, 33 are his variant notes (K / K-PTS); 12, 15, 18, 29 are the *ca* notes, from his appendix; 13 and 14 from ES; 16 project (Khu. i, 72 = Dhp 414 reads *jhāyī*); 19 his fn 23 plus the IEBH sentence.

**Not yet in the English page.** The appendix itself (applications of *ca*; *kvaci / vā / navā / vibhāsā*): kept verbatim in `docs/fuentes/nandisena-apendice-sandhi-en.md`, to be published once its place in both editions is decided (the Spanish has it as `comun/terminologia-particulas.md`, not on the chapter page).

## 6. Register of deviations in `02-nama-kappa.en.md` and `03-karaka-kappa.en.md` as built (2026-09-03, session 45, second part)

Same base and same rule as §5: N-EN verbatim; the Spanish master gives the structure; where the Spanish translated what N-EN left untranslated, or expanded, the English follows the Spanish. Both chapters were written whole, without sutta-by-sutta approval, as IEBH authorised; **neither is reviewed**.

### 6.1 Nāma-Kappa (219 suttas, 75 notes)

**Terms made uniform (glossary §2).** N-EN says "is changed to / changed into" (290 places) and "is substituted" (62) for the same operation, *ādesa*; the English page says **"is substituted by"** throughout (511 places), as the Spanish says «se sustituye por». *Kimatthaṃ*: N-EN "Why it is said …?" (185) → **"What is the purpose of saying …?"** (197), the form fixed for Sandhi. *Kvattho* → "What is the use of the name …?". *Vibhāsā* (§140, first occurrence in the work) → **facultatively**, as proposed in §2.2 and now applied; the Spanish has «facultativamente». *Liṅga* → base; *vibhatti* → inflection; *adhikāra* → governing aphorism (notes 1, 5, 13, 18).

**Structure from the Spanish.** Every sutta carries the Thitzana word-count breakdown, the numbered examples with the word under study in bold, the §N at every step of every formation and the counter-examples with the bracketed answer ("[This sutta does not apply when …, as in:]"). N-EN gives the examples in running prose with no §N; the numbering and the §N are the Spanish edition's.

**Where the English is not Nandisena's.** (a) §185: the two stanzas (*santo have sabbhi pavedayanti …*) have no English in his PDF; the English translation is the IEBH's, from the Spanish. (b) Note 42 (§57, *he brahme*) and note 75 (§263, the *ṇya* abstracts, after Ven. A. Thitzana) are IEBH notes, translated from the Spanish and labelled "Translator's note". (c) Note 7 (two ‘si’ inflections) says, as the Spanish does, that the explanation is Thitzana's. (d) The glosses of the sutta headings use brackets for supplied words, as the Spanish; "follows" / "after" unbracketed (convenciones §1 bis). (e) The functions of *ca* in the notes use his appendix names (note 11: *sampiṇḍana*, collecting).

**Corrections carried over from the Spanish work.** The citations are inline as he prints them; the errata already fixed in the Spanish (briefings 04–05, §10.1) are not reintroduced.

### 6.2 Kāraka-Kappa (45 suttas, 55 notes)

**Terms.** N-EN keeps the Pāḷi names of the cases in the vutti ("that case has the name “apādāna”"); the Spanish, from the first occurrence, gives the grammatical name and a translator's note («A partir de ahora … se traduce como …»). The English follows the Spanish: **"has the name “ablative / dative / locative / instrumental / object / subject / cause / possessive”"** in the vutti of §271, 276, 278–283, with the eight translator's notes (1, 19, 37, 39, 40, 42, 43, 46). *Yoga / payoge*: N-EN "in conjunction with" (11) and "in connection with" (5) → **"in connection with"** throughout. *Kvattho* (§271, 276, 278–283) → "What is the use of the name …?", and the answer completed with the cited sutta's own gloss as the Spanish does ("In the ablative, the fifth [inflection]"). *Kimatthaṃ* → "What is the purpose of saying …?", with the bracketed answer of the Spanish ("[This sutta does not apply when …, as in:]"; §308 "[To show exceptions to this sutta, as in:]").

**Structure from the Spanish.** The twenty meanings of §275, the twenty-two of §277 and the four of §278 are numbered "(1) **In the meaning of far**:" etc., with "Examples:" and numbered lines, as the Spanish; N-EN runs them as paragraphs. §277 (9): the analytic paragraph on *akathitakamma / kathitakamma* and the stanza ("The one who speaks, that is the “subject” (kattā)…") follow his English; the stanza is set as in the Spanish (three lines).

**Where the English is not Nandisena's.** (a) §314: his PDF gives no gloss for the sutta *Upa-’dhyādhik’-issaravacane*; the gloss is the IEBH's, from the Spanish, and note 53 says so ("Nandisena does not translate the title of this sutta; the translation is ours"). (b) Fourteen notes are IEBH notes ("Translator's note"), translated from the Spanish: the eight case-name notes above plus 8, 13, 47, 53, 54, 55. (c) The Pāḷi notes of the base edition (20, 22–23, 25–26, 30–31, 33, 45, 48–49) carry, in parentheses, the English of the Spanish edition's gloss, which the Spanish added and N-EN does not have. (d) Footnote labels: the Spanish distinguishes «Nota al pie:» (his) from «Nota del traductor:» (IEBH); the English says "Footnote:" and "Translator's note:" (41 + 14 = 55). (e) Typos of the PDF corrected silently (jeoulous, dreaful, imprisioned, helful, expresion, conjunciton, adhiraraṇa, "the the"). Spelling kept American (honor, skillful, color), which is Nandisena's own and what the Sandhi page already uses.

**Small wording aligned to the Spanish.** §272 (1) "the adherents of other teachers were defeated by the Buddha" is his; §272 *ādi* (1) "fifteen days from now" is his; §275 (2) "Antikaṃ gāmā (near the village)…" split in three as the Spanish; §275 (5) "[a word ending in] ‘tvā’" as the Spanish (N-EN "(a word ending in)"); §277 (14) "one wrestler is a match for another wrestler; one wrestler is worthy of another wrestler" (the Spanish gives both; N-EN one); §285 "vocative" for his "addressing"; §291 "blind in one eye, crippled in one hand, lame in one foot" (N-EN "blind by eye, cripple by hand…"; the Spanish «ciego de un ojo»); §299 "the one gone forth [the Bodhisatta]" (N-EN "the recluse"); §303 "heir" (N-EN "inheritor"); §309 (1) "they are the ones who say to him" (N-EN "they are sayers to him").

**Not touched.** Nandisena's canonical references, inline, exactly as in the Spanish; the Sī / K / Rū variant notes verbatim.

## 7. Register of deviations in `04-samasa-kappa.en.md` as built (2026-09-06, session 60)

Same base and same rule as §5–§6: N-EN verbatim; the Spanish master (`docs/4. Samāsa-Kappa.md`, revised by the IEBH in session 59) gives the structure; where the Spanish translated what N-EN left untranslated, or expanded, the English follows the Spanish. Written whole, as chapters 2–3 were; **not reviewed**.

**Terms (glossary).** The names of the compounds follow the kāraka model of the Spanish: the Pāḷi name with the gloss in parentheses at the first occurrence and in every vutti — "has the name “samāsa” (compound)", "“abyayībhāva” (adverbial compound)", "“kammadhāraya” (adjectival compound)", "“digu” (numerical compound)", "“tappurisa” (determinative compound)", "“dvanda” (copulative compound)", "“bahubbīhi” (relative compound)". The glosses are N-EN's own (his "adjectival compound", "numerical compound", etc.); only the model of presentation is the Spanish edition's (N-EN says "is (called) a compound (samāsa)"). *Taddhita / kitaka* → "secondary / primary derivatives" (N-EN §317). *Tulyādhikaraṇa* mirrors N-EN in each passage, as the Spanish does: "referring to the same thing" (§324), "the same location" (§328), "the same locus" (§330–§332). *Kimatthaṃ* → "What is the purpose of saying …?"; *kvattho* → "What is the use of the name …?", completed with the cited sutta's gloss ("Sometimes there is ‘a’ of the end vowel…"; "Also in an adjectival compound"; "Optionally, in a copulative compound"; "Also in a relative compound"), as the Spanish. "is substituted by" for *ādesa* (§330, §334), "facultatively" for *vibhāsā* (§323), "sometimes" for *kvaci*, "optionally" for *vā*. Brackets for supplied words; "(called)" of N-EN becomes "[is called]" / "[are called]" in the analyses of §328, as the Spanish «[se llama]».

**Structure from the Spanish.** Numbered examples with the compound in bold; the seven groups of §322 each with its "Thus in the meaning of…"; the seventeen analyses of §328 under formation titles (`**Nigrodhassa parimaṇḍalo nigrodhaparimaṇḍalo**:`), one paragraph per step with its "[dvanda-samāsa]" label, where N-EN runs them as a block with `\[Dvanda-samāsa\]`; the bracketed answers to *kimatthaṃ* of §335 and §341 ("[This sutta does not apply when…]", "[To allow exceptions to this sutta, as in:]"); the second and third "Examples:" blocks of §317, §330 and §337.

**Where the English is not Nandisena's.** (a) §322, small creatures: the Pāḷi (*Ḍaṃsā ca makasā ca ḍaṃsamakasaṃ…*) is the IEBH's restoration (session 59); the English glosses are N-EN's ("fly and mosquito", etc.). (b) The *viggaha* completed by the IEBH in the Spanish examples (§322 *ādi*, §330 *mahabbalaṃ, mahaddhanaṃ, mahabbhayaṃ*, §331, §333, §334, §338) carry the Pāḷi of the Spanish, with N-EN's gloss. (c) §328: "(ambudharo, the rain-cloud)" and "[tappurisa-samāsa]" on the first step follow the Spanish; N-EN has "What is it? (ko so?) A rain-cloud (ambudharo). [Tappurisa-samāsa]". (d) Note 9 (the Sinhalese books) and note 14 ("This example should be examined") are bilingual as in the Spanish: Nandisena's Pāḷi followed by the English of the Spanish edition's gloss. (e) §331 example 1 glossed as the Spanish ("the legs of that [man] are long; he is “dīghajaṅgho”…"); examples 2–3 as "[one who has] a good wife / much wisdom". (f) §337 *kāra*: "[why does it say “akāranto” instead of “a-anto”]" is N-EN's own bracket, kept. (g) §340: "the bow of that one is jointed; he is “gāṇḍīvadhanvā” [one who has a bow with many joints]", after the Spanish (N-EN: "Jointed (gāṇḍīvo) bow (dhanu) of this (yassa), he is (called)…").

**Small wording aligned to the Spanish.** §316 kvattho and §319 kvattho completed with the gloss of the cited sutta; §320 "It has the neuter gender" (N-EN, kept); §323 "goat and wild goat" (N-EN); §324 "noble girl" for *khattiyakaññā* (N-EN "*Khattiya* girl"; the Spanish «muchacha noble» by the IEBH's ruling khattiya = noble, and §332 "noble maiden" likewise); §326 "not five bundles" for *apañcapūlī* (N-EN "not five packages"; Spanish «manojos»); §327 "fear or danger from thieves" (N-EN "fear/danger"); §329 "Yama (the king of Death)" (N-EN); §330 "great fear or danger"; §334 "(not a horse, a mule)" (N-EN); §338 examples glossed as the Spanish ("there are many rivers in this; this is [a place which has] many rivers"). Typos of the PDF corrected silently (daugther, monsatery, sustitutions, immensurable, Immesurable, Embellisehd, "which which", "in its", "tha has", "did not indicated"). Spelling kept American (color, honor), as in the other chapters.

**Not touched.** The canonical references, inline, exactly as in the Spanish (99, restored in session 60 from the base edition, with "Khi. iii, 373" → "Khu." by the IEBH's ruling); the Sī / K / Sad. / Sā variant notes verbatim; N-EN's "[This chapter deals with the different types of compounds.]" kept in the master (the generator does not show it, as in Spanish).

## 8. Register of deviations in `05-taddhita-kappa.en.md` as built (2026-09-13, session 25 continued)

Same base and same rule as §5–§7: N-EN verbatim; the Spanish master (`docs/5. Taddhita-Kappa.md`, revised by the IEBH on 2026-09-13) gives the structure; where the Spanish translated what N-EN left untranslated, or expanded, the English follows the Spanish. Built by substitution over the published Spanish chapter file, so the Pāḷi blocks, headings, breakdowns and the 248 inline references are byte-identical with the Spanish edition (verified: identical Pāḷi token multiset per sutta, 52 note anchors paired). Written whole, as chapters 2–4 were; **not reviewed**.

**Terms (glossary).** "is substituted by" for *ādesa*; "What is the purpose of saying …?" / "What is the use of the name …?"; *kvaci* sometimes, *vā* optionally, *navā* occasionally; brackets for supplied words, "follows" / "after" unbracketed (convenciones §1 bis); "offspring" (apacca), "groups of clans" (gottagaṇa), "skill / merchandise / livelihood" (§351), "collection" (samūha), "state" (bhāva), "distinction" (visesa), "completion" (pūraṇa), "one only remains" (ekasesa), "expression of manner" (pakāravacana) — all N-EN's own words. The §404 set is rendered strengthening / elision / insertion / change / **reversal** / substitution (N-EN "reversing"; noun form for the list). *Nipātana* untranslated, as N-EN.

**Where the English follows the Spanish against N-EN's wording (each traceable to the Spanish master).** (a) The optional "vā" that N-EN omits in the glosses and vuttis of §344–§346 and §351 is supplied ("Optionally, …"), from the Pāḷi, as the Spanish does. (b) §347, §350: N-EN "“Vā” has the meaning of extending" → "has the meaning of “alternative” (vikappana)", the locked rendering. (c) §349: the glosses of the neuter forms ("the family of the female novice / of the coconut tree") are the Spanish edition's (IEBH interpretation; pending confirmation, `docs/capitulo-5/pendientes-taddhita.md` §3). (d) §352, the verse: the IEBH's resolved reading of "na vade", with note 10. (e) §389: N-EN "these are accomplished somehow" → "are accomplished again" (pacchā puna nippajjante), from the Pāḷi, as the Spanish. (f) §390: rewritten by the IEBH on 2026-09-13 in both editions — “catu” as the **preceding member** and the ‘ca’ “at the beginning of the following member”, i.e. N-EN's own reading (uttarapadādi-), with the Rūpasiddhi variant in note 30; “member” (not N-EN's “word”) for consistency with §387 and the locked upapada = «miembro precedente». (g) §391: "case (kāraka)" — the IEBH's ruling of 2026-09-13 — and N-EN's own "example" for *payoga*. (h) §394–§395: the powers of ten restored as superscripts (10¹⁴ … 10¹⁴⁰). (i) §401: N-EN prints "[Sutta has not been translated]"; the English gloss follows the Spanish edition's, with translator note 41 saying so. (j) §404, *viparīta* examples: N-EN "goes down / when the sun goes down" → "rises / when the sun has risen" (ud + gam), from the Pāḷi, as the Spanish.

**Corrections of N-EN's English against his own Pāḷi (silent in the page, listed here once).** §353 "kappino" → kappimo; §369 rucimā glossed via "(juti)" → ruci; §372 "made by lac" repeated for brick / iron / clay / wood → each material; §376 vutti "'sa' of “cha”" → 'so' (his own title and Pāḷi); §381 "twelve faculties" for *dvādasāyatanāni* → "the twelve spheres". *Samūha* rendered **aggregation** (N-EN "collection"; 2026-09-13), so that samūha and samuccaya do not share one word, mirroring the Spanish agregación / colección pair. *Gaṇana* unified to **enumeration** in both editions (2026-09-13; N-EN varies between "counting" and "numbers"), with a translator's note at its first occurrence in the work (§389, note 29; notes 29–52 renumbered 30–53). The spelling saṅkyā/saṅkhyā, which wavers in the base edition, unified to **saṅkhyā** by the IEBH (2026-09-13) in both editions (titles of §373/§381 included). Typos of the PDF corrected silently (Vesamitttī, "tree" for three, "(rattho)", "Vāsitho", "reversiong", "onw", "nineth", "clasification").

**Notes.** Same 52 as the Spanish, same numbering. The Sī / K / Rū / Mog. / Sad. variant notes verbatim in Pāḷi; notes 1 and 27 are N-EN's own English; notes 8, 9 (Thitzana attribution), 10, 21, 22, 32, 34 (the four universal suttas; the private link removed as in the Spanish) and 41 are the IEBH's, translated from the Spanish.

**Addendum, same day (later).** A translator's note on the §349 neuter (it refers to *kula*, family) entered as note 2, renumbering 2–53 → 3–54 in both editions; the note numbers earlier in this §8 are as of their writing. The five discursive treatise notes carry, after the Pāḷi kept verbatim, a translation in parentheses — Spanish in the Spanish edition, English in the English one — as the Samāsa notes 9 and 14 already did. **Scope fixed by the IEBH the same day: the passages quoted from other treatises are rendered, the variant readings are not.** Notes 13 (Rū) and 18 (Mog) are wholly treatise passages and are translated entire; notes 27, 45 and 51 are mixed, so their parenthesis is labelled ("Translation of the Rūpasiddhi passage…") and the (K), (Sī, K) and Sinhalese-book readings inside them stay untranslated. The pure variant notes stay in Pāḷi. Chapter note total: 54.

## 9. Register of deviations in `06-akhyata-kappa.en.md` as built (2026-10-12)

Same base and rule as §5–§8: N-EN verbatim (ṁ → ṃ); the Spanish master (`docs/6. Ākhyāta-Kappa.md`, revised by the IEBH, with the 188 canonical references of the base edition restored by `restituir_citas.py`) gives the structure; where the Spanish translated what N-EN left untranslated, or expanded, the English follows the Spanish. The corrections to N-EN listed in §2 of the working notes of each session-26 draft («Divergencias del inglés resueltas desde el pāḷi») were accepted by the IEBH on 2026-10-12 and are applied. Built by substitution over the converted Spanish chapter, in five ranges, so the Pāḷi blocks, headings, breakdowns, canonical references and the 113 note anchors are byte-identical with the Spanish edition. **Not reviewed.**

**Notes.** Same 113 as the Spanish, same numbering: N-EN's 71 (his English verbatim; the Sī / K / Rū variant notes in Pāḷi), the 41 added in the IEBH's revision (translated from the Spanish, unlabelled, as the IEBH decided on 2026-10-12), and one by Ven. A. Thitzana (note 69, §458, from *Kaccāyana Pāli Vyākaraṇaṁ* vol. 2, p. 645, n. 42). Note 62 (§445) also carries, after the IEBH's text, Thitzana's explanation of the vikaraṇa (vol. 2, p. 637, n. 36). Both Thitzana texts: his English edited for clarity and attributed to him.

**Terms.** *vikaraṇa* conjugational sign; *kārita* causative; *kattari* in the active voice; *parassapada* / *attanopada* active / middle voice; *paṭhama-* / *majjhima-* / *uttamapurisa* third / second / first person (N-EN «middle person» for the second; follows the Spanish and its note 4); *dvebhāva* reduplication; *abbhāsa* untranslated; *vipariyaya* and *viparīta* both **reversal** (N-EN «reversion» in §488; unified on assembly); the eight tense names untranslated.

**Update, same day.** The IEBH ruled that the Spanish takes every accepted correction (2026-10-12): §422 (‑matta), §433 «gupa (sentir aversión)», §434 «querer [hacer algo]», §439 «la noche es clara», §442 «la ivaṇṇa», §461–§465 «en lugar de», §486 «hace ocultar / hace corromper», §515 «llegan a», §521 «que no es de una sola vocal». The English now carries them all (clear, in place of, causes to hide / to corrupt, reach, does not have only one vowel); where the range registers below say a correction was not applied because the Spanish lacked it, that is superseded.

The five range registers follow as written.

### Range 1 (§406–§431, with chapter opening): register of deviations in `tramo1.en.md`

Base: N-EN (Nandisena's English) verbatim, ṃ normalized. Built by substituting the Spanish lines of `tramo1-406-431.es.md` one at a time. All other lines, including Pāḷi blocks, headings, verses, kaṇḍa Pāḷi lines, separators and Pāḷi variant notes, are byte-identical with the Spanish, trailing spaces included. The `<!-- NOTAS DEL TRAMO -->` marker is kept unchanged so that assembly can find the notes.

#### (a) Departures from N-EN wording

##### Formatting and conventions applied throughout
- Glosses, explanations and examples are laid out as in the Spanish: blocks separated by `---`, numbered examples, and "Examples:" / "Which are these?" labels. N-EN runs the examples as prose with word-by-word parentheses ("He (so) goes (gacchati)"). The English now uses the Spanish model: the Pāḷi phrase in bold followed by its English in parentheses. The English inside the parentheses is N-EN's wherever he gives one.
- *Kvattho*: N-EN "Why it is said “X”? For the use of the word “X” …" is replaced by "What is the use of the name “X”? For the use of the name “X” …" (fixed formula, Spanish «nombre»). *Kimatthaṃ*: N-EN "Why it is said …?" is replaced by "What is the purpose of saying …?", and the quoted Pāḷi word is now the sutta's own locative “tulyādhikaraṇe” (N-EN: “tulyādhikaraṇa”), as in the Spanish.
- In the gloss lines, square brackets `\[…\]` appear exactly where the Spanish has them. Where N-EN marked a supplied word with round brackets, those became square brackets ("(should be taken)" → "\[should be taken\]", "(a knowledge that has)" → "\[a knowledge that has\]").
- Body brackets are written escaped (`\[…\]`) as INSTRUCCIONES §2 says. **Note:** the published `05-taddhita-kappa.en.md` carries them *unescaped* in the body (`[there is]`). That file also drops the trailing double spaces after `**…-KAPPA**`, after `**…-KAṆḌA**` and on list items. I followed the instruction to stay byte-identical with the Spanish. If the 05 convention is wanted, removing the escapes and trailing spaces is a mechanical step.

##### Divergencias applied (sesion-26-suttas-406-431)
1. **§408 gloss** (div. 1): "The pairs \[are\] third person, second person and first person." This replaces N-EN's "A group of two is called person (purisa), third person …".
2. **§427 kvattho** (div. 2): "What is the use of the name “hiyyattanī”? …(§418)." N-EN does not have this sentence. It is supplied from the Pāḷi and the Spanish, by parallel with §423–§430. The divergencia says the IEBH decides whether it stays, but the Spanish file carries **no** `<!-- DUDA -->` marker, so none was added in the English either (see (c)).
3. **§410** (div. 3): "the first (person)" / "the first person" → "the third \[person\]" / "the third person".
4. **§420 vutti** (div. 4): "When \[they are\] in conjunction with “mā”, the inflections “hiyyattanī” and “ajjatanī” are also \[employed\] in all time." N-EN reads "When in conjunction with “mā” and in all time, there are the inflections …".
5. **§422 vutti** (div. 5, *-matta*): "In the past time, in what consists only of an action that has passed without happening,[^13] there is …". **Applied although the Spanish vutti does NOT carry it** (it reads «en una acción no ocurrida,[^13]»). See (b) and (c).
6. **Verse (K)** (div. 6): "force" is kept, following N-EN and his note 1 (*raya*). The Spanish «corriente» renders the same word.

##### Following the Spanish (expansions or terminology)
- **§406** gloss and vutti: N-EN "(word for another)" → "(active voice)". The Spanish moved the literal sense into note 3, which the English now carries as "Literally “word for another”." The vutti also gets "(active voice)", as the Spanish does.
- **§407** gloss: N-EN "(word for itself)" → "(middle voice)", as the Spanish. The Spanish has no literal-sense note here, so N-EN's "word for itself" disappears (see (b)).
- **§408–§412**: *majjhimapurisa* is "second person" where N-EN has "middle person", following the Spanish and its note 4. This also applies in §409, where N-EN's vutti read "first person, middle person and highest person" and was recast as "Where all three –third person, second person and first person– are mentioned together …".
- **§408** examples: N-EN's stray Spanish «Pero en "attanopada"» → "Also in the “attanopada”:" (Pāḷi *pi*). The Pāḷi labels (paṭhamapurisā …) were added in parentheses, as in the Spanish. The kvattho answer quotes three suttas separately, as in the Spanish. N-EN joins them into one quoted sutta.
- **§408** vutti: the Pāḷi in parentheses is written *paṭhamapurisa / majjhimapurisa / uttamapurisa* without hyphens, as in the Spanish. N-EN hyphenates them.
- **§410** "Also when \[the name is\] not used:" (Spanish «\[el nombre\]»).
- **§411–§412** vutti: "that have the same locus" → "with the same locus", following the Spanish «con el mismo locus», because N-EN's clause is ungrammatical. "(you)" / "(I)" were added after “tumha” / “amha”, as in the Spanish.
- **§411** examples: N-EN "goes (yāsi)" → "(\[you\] go)", following the Spanish.
- **§413**: “kāla” (time) → “kāle” (in time), and "\[from 413 to 422\]" added, as in the Spanish.
- **§414, §419, §421**: "\[time\]" supplied where the Spanish has «\[tiempo\]». For §419 this gives "In proximate \[time\]" in place of N-EN's "In proximity", in both the gloss and the vutti (wording change; see (b)).
- **§415** gloss recast on the Spanish model: "In the meaning of command and blessing, and in time that is not said, \[there is\] the “pañcamī”." N-EN: "In command, blessing and time that is not said, there is the “pañcamī”."
- **§417, §418** gloss: "In \[that which is\] not seen / seen" for N-EN "In that which is …", with brackets as in the Spanish «En \[aquello\]».
- **§422** gloss: "(without taking place)" became plain text, because the Spanish has no bracket there.
- **§423–§430** vutti: inside the Pāḷi lists, N-EN's semicolon is replaced by the Spanish comma.
- **§431** example: N-EN "(He) came (agamā)" → "(\[he\] went)", and "go (gacchatu)" → "let \[him\] go", following the Spanish «fue», «que \[él\] vaya» and §418–§419 "went".
- **Verse (Kh)**: "grammar of verbs" → "\[grammar of\] verbs", as in the Spanish.
- **Verse (G)**: "exists in (these meanings)" → "exists \[in these meanings\]".
- **Closing**: "**Thus \[ends\] the first section in the chapter of verbs**" uses N-EN's words with the Spanish bracket «\[termina\]».
- **Notes 2, 6 and 13** exist only in the Spanish (editor's notes). They are translated into English and carry no label.
- **Note 4**: N-EN's fn 2 is followed by the Spanish additions, translated (the second- and first-person explanation).
- **Note 5**: N-EN fn 3 verbatim. The bold on the Pāḷi suffixes comes from the Spanish.

##### Typos and slips of N-EN corrected
"knowlege" → knowledge (K); "who possess" → who possesses (Kh); "nipphannna" → nipphanna (G); "undestood" → understood (§413); "that have the same locus" → "that has" (§410); "Let he do" → let him do (§415); "the Ancient (porānā)" → the ancients (§417); "hiyyatanī" → hiyyattanī (§431); "asabbadhātumhi" → asabbadhātukamhi (§431 kvattho, matching the Pāḷi block). N-EN's Pāḷi typos ("Ākyātasāgaram", "ssasa", "Ti, anti") do not enter, because the Spanish Pāḷi is used.

#### (b) Places where I am unsure

1. **§422 vutti, *-matta***. The divergencia says the Spanish was translated «en aquello que consiste sólo en una acción que ha quedado sin realizarse», but the Spanish file has «en una acción no ocurrida». I applied the divergencia ("in what consists only of an action that has passed without happening"), so on this line the English is *not* parallel with the Spanish. Either the Spanish file is behind the divergencia, or the divergencia was later withdrawn. The IEBH should decide.
2. **"second person" for *majjhimapurisa*** (§408–§412, note 4). This follows the Spanish and its note 4, which explicitly says «aquí se traduce como “segunda persona”». N-EN consistently says "middle person". I chose the Spanish so that the English note stays true, but this is a terminology decision.
3. **§406/§407 "(active voice)" / "(middle voice)"** in place of N-EN's literal "(word for another)" / "(word for itself)". For §407 the literal sense is lost entirely, because the Spanish has no note there. The IEBH may want a parallel note ("Literally “word for itself”"), but I did not invent one.
4. **§410 gloss and vutti "When used \[or not used\] in a name that has the same locus"**: this is N-EN's wording, kept. The Pāḷi is a locative absolute ("when a name … is used"), which the Spanish renders more accurately («cuando se emplea un nombre»). I did not rewrite it, because no divergencia covers it.
5. **§419 "In proximate \[time\]"**: this rewords N-EN's "In proximity" to carry the Spanish bracket. The alternative is to keep "In proximity" with no bracket.
6. **§407 "The latest \[six\]"**: kept from N-EN, although "latter" or "last" is the natural English. It is not an obvious typo, so I left it.
7. **Number in the English glosses**: "you" renders both *tvaṃ* and *tumhe* (§409, §411), so singular and plural are not distinguished (the Spanish has tú / vosotros). I kept N-EN's plain "you".
8. **Verse (Kh) "the Buddha"**: N-EN's word is kept for *sambuddham*. The Spanish has «el Perfectamente Iluminado».
9. **Note 6**: "vasāma … tadā" is rendered "lived" (past), as the Spanish «vivimos» with «en ese entonces» implies.

#### (c) Problems noticed in the Spanish (reported only, not changed)

1. **§422 vutti** does not reflect divergencia 5 (*-matta*): see (b)1.
2. **§427**: divergencia 2 says the supplied kvattho line is "marcado con `<!-- DUDA -->` en el cuerpo", but there is no such marker in `tramo1-406-431.es.md`.
3. **§411 vutti**: «hay la la segunda persona» has a duplicated article.
4. **§431 kvattho**: «“Ikārāgamo asabbadhātumkamhi”» is a typo for *asabbadhātukamhi*, the form in the sutta's own Pāḷi block.
5. **§416 vutti** line ends with a stray tab character.
6. **§418 Pāḷi vutti**: «“hiyyattanī”[^11] vibhatti» uses quotes and a space, where every parallel sutta and N-EN have **…**vibhatti in bold, compounded (N-EN: `**hiyyattanī[^8]**vibhatti`). The line was kept byte-identical.
7. **Header breakdowns** have stray spaces: §408 «paṭhama-majjhima- uttama-purisā» and §431 «Hiyyattanī- sattamī-pañcamī-vattamānā». Kept byte-identical.
8. **Note 19 (§427 vutti, aṃ mhā)**: the Spanish reads «Amha (Sī).», but N-EN's corresponding note 15 reads «Amhā (Sī).», as does note 18 on the heading. The Spanish may have dropped the macron. Kept as in the Spanish.
9. **§431 Pāḷi example line**: N-EN gives a reference «(M. i, 326)» after «Agamā, gaccheyya, gacchatu, gacchati», and the Spanish block omits it. This may be intentional, but it is not registered.
10. **Note 6** ends with trailing spaces (not carried into the English).
11. **§416 example**: the Spanish «tú irías» (conditional) does not match N-EN's "you may go" (permissive *sattamī*, consent). The English keeps N-EN. The Spanish might better read «puedes ir» / «que vayas»; this is for the IEBH to judge.

### Range 2 (§432–§457): register of deviations from N-EN

Base: Nandisena's English (N-EN) verbatim, ṁ → ṃ. The file was built by substitution over `tramo2-432-457.es.md`. Pāḷi blocks, sutta headings, formation steps, Pāḷi notes, the closing Pāḷi formula and the `<!-- NOTAS DEL TRAMO -->` marker are byte-identical, and so is the Markdown escaping (`\[ \] \+ \=`, trailing double spaces). The escaping follows INSTRUCCIONES §2 (`\[…\]`). 05-taddhita-kappa.en.md uses unescaped `[…]` in its glosses and no trailing double spaces. Both forms render the same; the generator/IEBH may want to normalise.

#### (a) Departures from N-EN wording

**Fixed terms and formulae (whole range).** *vā* → "optionally" (N-EN "sometimes": §433 gloss, vutti and *kimatthaṃ*; §434 vutti and *kimatthaṃ*; §442; §443). "Why it is said …?" → "What is the purpose of saying …?". Root names, and the names *niggahita* and *kārita*, in curly quotes, as the Spanish has them (N-EN uses single quotes on root names). Brackets are placed where the Spanish has them, including N-EN's own parentheses "(which are called)", "(a verb signifying)", "(inflection)" and "(insertion of the)". Example glosses drop N-EN's interlinear "(word)" annotations and take the form of the Spanish examples (Pāḷi = **word** (gloss)). "Formation of" → "Sequence of". "Thus" (list header) → "Likewise:" (05 convention).

**Accepted divergencias applied.**
- §433: "gupa, disgusting" → "“gupa” (feeling aversion)", and in the examples (§433, §455) "is disgusted" → "feels aversion" (div. 1). I kept N-EN's gerunds for tija/kita/māna ("enduring", "curing", "investigating"). In English, "curing" already gives the root meaning, which is what div. 1 asks for. See (b).
- §434: "in the meanings of wanting and to do" → "in the meanings of wanting \[to do something\]" in the gloss, the vutti and the *kimatthaṃ* (div. 2). See (c): the Spanish file does not carry this change.
- §439: "(it) is pure as the night" → "(the night is pure)" (div. 3, subject restored). I kept N-EN's word "pure", which is also the final Spanish «pura». The divergencia says «clara». See (b).
- §439: *daḷhayati* "makes the effort firm" and *upakkamālati* "undertakes" (div. 4).
- §440, §442, §443, §453: the *bhāva* member is given as an action noun ("knowing, or it is known"), which is N-EN's own pattern (div. 5). §440 *labbhate* "obtaining and it is obtained" → "or" (typo). §453 "obtaining (they) are obtained" → "obtaining or they are obtained".
- §441 vutti: "–as the case may be–" added for *yathāsambhavaṃ* (div. 7). The vutti otherwise follows the Spanish structure, with "changes … to the state of the letters of the ‘ca’ group, of ‘y’ and of ‘v’". N-EN has "there is the substitution of ‘ca’ group …".
- §442 gloss and vutti: "insertion of ivaṇṇa \[‘i’ or ‘ī’\]" (div. 6). See (c): the Spanish file does not carry this either.
- §446 gloss: "Also after “rudha” and others, \[there is\] the “niggahita” in front" (div. 1 of 445–457).
- §451: imperatives marked as "stretch \[you\]!", "do \[you\]!" (div. 2). The Spanish has «extiende \[tú\]», with no exclamation mark. I added "!" because English cannot otherwise tell the imperative from the present.
- §454 *jāyate*: "arises" → "is born" (div. 4). Div. 3 (*rocate*/*socate*) leaves N-EN's "shines"/"grieves" unchanged.
- §455 vutti: from the Pāḷi, as div. 5: "After the roots with the suffixes that indicate their meaning –those beginning with ‘kha’ and ending with “kārita”–, there are inflections."
- §457: gloss without "(called)"; vutti "are called “dhātu” (root)" (div. 6).
- §447 *dibbati*: both values kept (div. 7, no change).

**Following the Spanish where it expands or reorders N-EN.**
- §438 gloss and vutti: "“kārita” (causative)".
- §439 gloss: "after a noun" added (*nāmasmā*, omitted by N-EN). Vutti: "after that noun" (*tasmā*).
- §440 and §444: order "impersonal … and passive" (Pāḷi *bhāva-kamma*), with "\[sense\]". N-EN has "passive and impersonal".
- §443 gloss: "And \[reaches\] the previous form" (N-EN "And the previous form"; "reaches" is his vutti word). Examples: *sakkate* added, which N-EN omits, glossed as the Spanish has it, "it is honored". See (b).
- §444 gloss: "Likewise also in the active voice" (*tathā*; N-EN "Also in the active voice").
- §447 gloss: ‘ya’ (N-EN ‘yo’, the nominative of the sutta).
- §452 vutti: ", and they are called “kārita”" (in the Pāḷi; N-EN omits it). *manteti* "deliberates/consults" (N-EN "consults").
- §453–§454: "“attanopada” (middle)" and §456 "“parassapada”", with the brackets as in the Spanish.
- Closing: "Thus \[ends\] the second section in the verb chapter" (bracket as in the Spanish). "**THIRD SECTION**" (N-EN "**Third Section**"; 05 casing).
- Glosses where N-EN and the Spanish differ only in wording keep N-EN's: *paṭhati* "reads" (Spanish «recita»), *lunāti* "cuts" («siega»), *saṃvuṇoti* "restrains" («contiene»), *yujjate* "engaged" in §441/§453 ("yoked" in §440, as N-EN), *cicciṭāyati* "acts like “ci-ci”" («chisporrotea»), *vuḍḍhate* "it is increased" («crece»), *phallate* "splitting" («se parte»). *kujjhate* "he is angry" in §441 (N-EN there "it is angry"; his own §453 "he is angry").

**Typos of N-EN corrected.** mountarin; Sometines; "there is there is suffix"; comparision; "such in the" (§437); "they are know" (§441); "there insertion" (§446); "Those group of words" (§457); "and it is obtained" → "or" (§440); "following examples" → "example" (§434, single example); "desire of oneself" → "desire for oneself" (§437 vutti and *kimatthaṃ*, to agree with his own gloss); stray comma in note 68 ("“dhātuppaccaya”, means").

**Notes.** 27–30, 33–48, 50, 52–55, 58–60 and 64 are identical to the Spanish (Pāḷi variants or formulas). 31, 49 and 68 are N-EN verbatim (his 27, 44, 52). In 57 and 63 (his 47 and 50, Pāḷi in the base edition), I kept the Pāḷi verbatim and added the English in parentheses, following memo §8 addendum. The Spanish gives only a Spanish translation and drops the Pāḷi (see (c)). 32, 51, 56, 61, 62 (first part), 65, 66 and 67 are editor's notes, translated from the Spanish. In 62 I used "dragged" for «se arrastra», Nandisena's *anukaḍḍhana* term. 62 ends with the Thitzana text exactly as given in INSTRUCCIONES.

#### (b) Places where I am unsure

1. **§439 *visuddhayati*.** Div. 3 says the Spanish was rendered «la noche es clara», but the final Spanish says «pura». I used "the night is pure" (N-EN's word, final Spanish). Change to "clear" if the divergencia wording is meant to prevail.
2. **§433 root glosses.** I changed only "disgusting". If IEBH wants div. 1 read literally, change "kita (curing)" to "(to cure)" and put the other three in the infinitive too.
3. **§443 *sakkate* "it is honored".** I copied this from the Spanish, but I doubt it. In the grammatical tradition *sakkate* under *pubbarūpa* is usually taken from √*sak* "to be able" (*sak* + *ya* → *sakk-*), so "it is possible / one is able". "Honored" would point to *sakkaroti* (sa + √kar), which does not fit this rule. I have not checked this against Rūpasiddhi or Saddanīti in this session. Please verify.
4. **§434 and §442.** I applied div. 2 and div. 6, but the final Spanish does not reflect them (see (c)). If the Spanish is deliberately final and the divergencias are outdated, these four lines should go back to "in the meanings of wanting and to do" and "insertion of ‘i’ or ‘ī’".
5. **§451 "stretch \[you\]!".** The bracket placement and the "!" are my rendering of the divergencia.
6. **Note 61.** Its content is questionable: "That is, ‘ya’ becomes the previous form". §444 extends to the active voice *all* the substitutions of ‘ya’ of §441–§443 ("yathā heṭṭhā … ādeso"). Its own examples *bujjhati*, *vijjhati* and *maññati* are §441 (cavagga) cases, not *pubbarūpa*. I translated it faithfully but flag it.
7. **Note 65.** The Spanish dash placement is broken (see (c)). I translated what I take to be the intended sense: "the letter ‘ṇ’ –which prescribes the strengthening of the root vowel and is part of the true causative suffixes (§438)– is elided by §523".
8. **`<!-- NOTAS DEL TRAMO -->`.** I kept the marker unchanged in case a script splits on it. Rename it if not needed.

#### (c) Problems noticed in the Spanish (reported only, not changed)

1. **Formation sequences, §433.** Step 2 reads "tij (§521)" in all four sequences. It is right only for *titikkhati*. For *jigucchati*, *tikicchati* and *vīmaṃsati* it should be "gup (§521)", "kit (§521)" and "mān (§521)". Copied unchanged into the English, so the error is in both.
2. **§434, divergencia 2 not applied.** The gloss, vutti and *kimatthaṃ* still say «en los significados de querer y hacer», which is the reading div. 2 rejects.
3. **§442, divergencia 6 not applied.** The gloss and vutti say «inserción de ‘i’ o ‘ī’», with no «ivaṇṇa».
4. **§433.** Div. 1 says «gupa (sentir aversión)», but the vutti has «“gupa” (disgustar)». The examples have «siente aversión», so the vutti and the examples are not consistent.
5. **§439.** Div. 3 says «la noche es clara», but the example has «la noche es pura».
6. **§440 example 1.** «**Ṭhīyate** ( estar en pie, la acción de estar en pie)» has a stray space and a duplicated gloss, apparently an unfinished edit. In the same line, «la acción e uncir» should be «de uncir».
7. **§434 header.** «\[Bhuja-ghasa-hara-su- pā-ādīhi …» has a stray space after "su-".
8. **Note 58** gives «√vaḍha + ya + te = vaḍḍhate», but the example it is attached to is *vuḍḍhate*. Either the note or the example form needs aligning.
9. **Note 65.** The opening dash closes in the wrong place: «–que prescribe el fortalecimiento de la vocal de la raíz es parte de los verdaderos sufijos causativos (§438)–». It needs «raíz y es parte…» or the dash moved.
10. **Notes 57 and 63.** The Spanish replaces Nandisena's Pāḷi notes (his 47, 50) with a Spanish translation only, so the Pāḷi of the base edition is lost. Elsewhere (memo §8 addendum) the Pāḷi is kept and the translation added.
11. **Note 68** (and N-EN 52) reads "nāpe" for ‘ṇāpe’. Copied unchanged.
12. **Note 61** content: see (b) 6.
13. **Inline canonical references.** None of N-EN's inline references appear in the Pāḷi lines of this range, for example (Vin. iii, 320), (Khu. i, 59), (M. ii, 87), (VinA. i, 6). Chapters 1–5 carry them inline (memo §5, §7, §8). The English inherits the omission because the Pāḷi blocks are byte-identical.
14. **§432 header.** «432\. 362\.» differs from N-EN's «432. 462.». The Spanish note 32 («Rū. §362») agrees with 362, which looks like a deliberate correction (in Rūpasiddhi this sutta opens the Taddhita section). Noted only.
15. **Minor.** Note 49 has three spaces after the colon (the English has two). §449 sequence step 5 has three trailing spaces.

### Range 3 (§458–§481): register of deviations from Nandisena's English

Base: N-EN verbatim (ṁ → ṃ). The file was built by substitution over `tramo3-458-481.es.md`, so the Pāḷi blocks, headings, kaṇḍa Pāḷi lines and the 13 note anchors (69–81) are byte-identical with the Spanish. All the items below are places where the English departs from N-EN.

#### (a) Departures from N-EN and the reason for each

**Applied in every sutta (convention).** *vā* → "optionally". N-EN writes "Sometimes" for *vā* in the glosses, vuttis and *kimatthaṃ* answers of §463, §465–§466, §468–§471, §476, §479–§481. "Why it is said “X”?" → "What is the purpose of saying “X”?". N-EN's parenthesised supplied words, e.g. "(syllable)", "(he)", "(inflections)", become `\[…\]` wherever the Spanish brackets them. Where the Spanish has no bracket, the parentheses are dropped and the words are kept. Root names take the Spanish's double quotes ("“māna”"; N-EN has ‘māna’). "(abbhāsa)" is placed after "the previous syllable" as the Spanish places it. N-EN's own forms here are "“abbhāsa” (previous reduplicated syllables)" and "“abbhāsa” (reduplicate syllable)". Example glosses are N-EN's own and go after the bold word, as the Spanish layout has them. The plural "examples" follows the Spanish wherever two counter-examples are given (§458, §466).

**Divergencias applied (sesion-26-suttas-458-481).**
- No. 2, §463 vutti: "Optionally, …". N-EN drops the *vā* here.
- No. 3, §465 title and vutti: "‘i’, ‘ī’ **or** the letter ‘a’", not N-EN's "and ‘a’".
- No. 4, §464: *juhvati, juhoti* glossed "(\[he\] offers)" (Spanish «ofrenda»). N-EN has "(he) sacrifices".
- No. 5, §476: *gacchamāno, gacchanto* "(going)". This is N-EN's own word, kept together as the Spanish does.
- No. 6, §478: *gacchāma, gacchāmhe* "(we go)". No distinction was added, as the divergencia directs.
- No. 7, §481: "the inflection of the “bhavissantī” **has the substitutions** ‘khāmi’…". N-EN's "is changed to" inverted the operation.
- No. 8, §481: "and others" added for *icc’ ādayo*.
- **No. 1 was NOT applied** ("in place of" for §461, §462, §464 and §465). See (b)1.

**Follows the Spanish, which expands or recasts N-EN.**
- §459 vutti: the stray "it" is removed ("of the reduplicated root ~~it~~ is called").
- §460 vutti: "previous syllable (abbhāsa)". N-EN has "previous (syllable)".
- §461 title: "Of the second and fourth, the first and third." (N-EN "First and third of second and fourth."). §461 vutti is recast to the Spanish order: "Of the second and fourth \[consonants\] in the previous syllable (abbhāsa), there are the first and third."
- §462 title and vutti are recast the same way: "Of the ‘ka’ group, the ‘ca’ group." and "Of the ‘ka’ group in the previous syllable (abbhāsa), there is the ‘ca’ group."
- §463 title: "\[there is\] the state of ‘va’ and ‘ta’" (Spanish «el estado de», from *-ttaṃ*). The vutti follows the Spanish whole: "the previous syllable (abbhāsa) of the roots … is changed to the state of the letter ‘va’ and of the letter ‘ta’ respectively". N-EN has "There are ‘va’ and ‘ta’ of the “abbhāsa” of the roots…".
- §466 title: "And \[there is\] the niggahita." This follows the Spanish and the Pāḷi *ca*. N-EN has "Sometimes there is the “niggahita”", and the title has no *vā*. "niggahita" is left unquoted, as in the Spanish.
- §467 title: "After that, \[there are\] … when ‘sa’ follows" (N-EN "After that (abbhāsa) there are…").
- §468 and §469 titles: "\[is substituted by\]" (N-EN "becomes"), following the Spanish «\[se sustituye por\]» and the ādesa convention.
- §470 and §471 titles: "\[There are\] … of “ñā”" and "… of “disa”". The words "of “disa”" are added for §471; N-EN's title omits them.
- §472: "suffixes" is plural in the title and the vutti, following the Spanish and the Pāḷi *chapaccayesu*. N-EN has "suffix". "And" is added to the title for *ca*. "follow" is left unbracketed (locative); see (c)3.
- §473 and §474 titles: "\[there is\]" bracketed as in the Spanish. For §474, "when ‘sa’ follows" replaces N-EN's "when there is ‘sa’".
- §475: "\[there are\]" is bracketed. The question reads "“parokkhāyaṃ”" as in the Spanish (N-EN "“parokkhā”").
- §476 title: "\[is substituted by\]" (N-EN "becomes"), followed by "when all \[the inflections\] follow". In the vutti, "all suffixes and inflections" follows the Spanish and the Pāḷi *paccayavibhattīsu* (N-EN "inflections and suffixes"). "(to go)" replaces N-EN's appositive "going", and "is substituted by" replaces "becomes". Example 3 reads "(let \[him\] go)" (Spanish «que \[él\] vaya»; N-EN "Go").
- §477 title: "When “ajjatanī” follows … \[becomes\]". The vutti reads "changes to the state of ‘o’" (Spanish «cambia al estado de», Pāḷi *ottam āpajjate*); N-EN has "When there is … becomes ‘o’".
- §478 title: "follow … \[becomes\] long" (N-EN "When there are … becomes long").
- §480 title is recast to the Spanish: "There are ‘eha’, ‘oha’ and ‘e’ of the vowel of “hū” when \[the inflection\] “bhavissantī” follows, and \[there is elision\] of ‘ssa’". N-EN's own wording, "(future)", is dropped there, as in the Spanish. In the vutti, "\[the inflection\]" is added.
- §481: "its suffix" (N-EN "the suffix"). In the vutti, "when the inflection “bhavissantī” follows" replaces "when there is".
- Closing formula: "**Thus \[ends\] the third section in the verb chapter**". This is N-EN's wording with the Spanish bracket on «termina».
- Notes 75 and 80–81: "Kac" → "Kacc." in note 75, as in the Spanish. Notes 71, 72, 80 and 81 exist only in the Spanish and are translated without a label.

**Errors in N-EN corrected (typos, or a gloss that contradicts his own Pāḷi or the Spanish).**
- §458: "an exception **of** the rule" → "to the rule".
- §466: "walks up **an** down" → "and".
- §466 counter-example: *pivāsati* "(he) wishes to **eat**" → "to drink", as in his §458 and §465.
- §468: "(he) stands" lacks its word (*tiṭṭhati*). "(let he) stand" → "let \[him\] stand"; the same fix is made in §469 and §476.
- §471 counter-example: "(adassa)" → *addasa* (his own Pāḷi).
- §472: *jighacchati* lacks its parenthesis in N-EN ("(he) wishes to eat."). The word is supplied as in the Spanish.
- §475 counter-example: *abravuṃ* "(they) **were**" → "(\[they\] said)", as in the Spanish.
- §478: "does not **becomes** long" → "become".
- §480: N-EN's second list has "hohissati" among the plurals. It is not carried into the English, because the Spanish list (*hohissanti*) is used.

#### (b) Places I am unsure about

1. **Divergencia No. 1 does not match the Spanish.** The divergencias file says §461 (and §462, §464, §465) were translated as a genitive of substitution, «*en lugar de* la segunda y la cuarta…». The final Spanish file has no «en lugar de» in any of these suttas: §461 reads «De la segunda y la cuarta, la primera y la tercera.» I followed the Spanish so that the two editions stay parallel ("Of the second and fourth, the first and third."). If the editor wants "In place of…", both the Spanish and the English need it.
2. **Example glosses where N-EN varies.** N-EN uses different English for the same verb in different suttas, and I kept his gloss in each place as the instruction says:
   - *jahāti*: "renounces" in §458, "abandons" in §460 and §464.
   - *jigucchati*: "is disgusted" in §458, §462 and §472, but "reproaches" in §465.
   - *vīmaṃsati*: "investigates" in §458, §465 and §467, but "thinks" in §463.
   - *jaṅgamati*: "goes" in §462, "goes about" in §466 (Spanish «anda de acá para allá» in both).
   - *jigīsati*: "wants to carry" in §462, "wishes to carry" in §474.
   - *dadhāti*: "holds" in §459, where the Spanish gives two senses («lleva/sostiene»).

   The Spanish is uniform in each case. If uniform English is wanted, these are the places to change.
3. **Imperatives in §478–§479.** *gacchāhi* (Spanish «ve tú»), *gaccha / gama* and *gamaya* «haz ir tú» are given as "(you go)" and "(you cause to go)", following N-EN's "(You) go". The English does not show that these are imperatives as the Spanish does. I avoided "go [you]" because it would add brackets the Spanish does not have.
4. **§476 example 8.** *agacchissā* is given as "(\[if he\] would go)", N-EN's wording. The Spanish «\[si él\] hubiera ido» is past conditional ("would have gone"). I kept N-EN.
5. **Note 71: "√mā".** I translated the Spanish literally. The sutta §467 names the root as *māna*, not *mā*; see (c)5.
6. **Note 80.** It says *abravuṃ* is in the ajjatanī. I did not verify this. The ending *-uṃ* occurs in both the ajjatanī and the hiyyattanī 3rd plural, so the editor may wish to confirm it.

#### (c) Problems noticed in the Spanish (report only; nothing changed)

1. **§458:** the title gloss and the vutti gloss are identical sentences (lines 11 and 13). N-EN's two differ only in "which" and "that".
2. **§472 title:** «‘ca’de» lacks a space («‘ca’ de»).
3. **§472 title:** «cuando \[siguen\] los sufijos ‘cha’» brackets the locative "follow". Under convenciones §1 bis, «siguen» should be unbracketed. The English leaves it unbracketed.
4. **§463 example:** the note anchors are inconsistent with each other. One sits outside the bold: «**Vīmaṃsati**[^71]». The other sits inside it: «**tikicchati[^72]**». Both are copied byte-identically.
5. **Note 71:** «√mā se sustituye por ‘maṃ’ por §467». §467 substitutes ‘maṃ’ for the root **māna**, so the note might better say "māna". I don't know whether the note means the root in its dictionary form *mā(n)*.
6. **Sutta headings, Rūpasiddhi numbers:** §468 and §469 both carry "(949)", and the sequence then skips 955 (§474 = 954, §475 = 956). N-EN has the same. This may be in the source edition. I have not verified it.
7. **§464 example:** *juhvati* has no gloss of its own («**juhvati**, **juhoti** (\[él\] ofrenda)»). This is not wrong; I mention it only because N-EN groups the two the same way.
8. **Trailing spaces** at the end of note definitions 75, 76, 77 and 81. They are harmless. The English keeps the one on the Pāḷi note 77 and drops the others.
9. **§465 heading** has «ivaṇṇākāro» where N-EN has «ivaṇṇ’ ākāro». The Spanish Pāḷi was kept as is. I mention it only in case the apostrophe form is intended.

### Range 4 (§482–§502) — register of deviations from Nandisena's English

Built by line substitution over `tramo4-482-502.es.md`: every heading, Pāḷi block, `---`, the §488 formation steps and all `[^n]` anchors are byte-identical with the Spanish. Notes 82–88, Spanish numbering. Supplied words in escaped brackets `\[…\]` exactly where the Spanish has them (05-taddhita-kappa.en.md writes them unescaped in body text; they render the same). The `<!-- NOTAS DEL TRAMO -->` marker is kept as in the Spanish file.

#### (a) Departures from N-EN wording

**Conventions applied throughout (not repeated per sutta).** ‘x’ for letters/suffixes/inflections and “x” for roots and words, as the Spanish (N-EN uses ‘…’ for roots). Locative "When there is ‘x’" → "When ‘x’ follows", unbracketed (convenciones §1 bis): §482, §485, §487, §489, §490, §491, §496, §502. Ablative → "after": §492 vutti ("after the root “asa”", N "of the root"), §497 and §498 gloss and vutti ("after “labha”/“kusa”", N "of"). *Vā* → "optionally" where N has "sometimes": §484, §488, §491, §492, §499, §500, §501 (incl. "What is the purpose of saying “vā” (optionally)?", N "(sometimes)"). "Why it is said …?" → "What is the purpose of saying …?" (§483, §484, §501). N's "(he) does X (form)" prose → numbered examples with the form in bold and the gloss in parentheses; N's "(he)/(they)" → `\[he\]`/`\[they\]` where the Spanish brackets «\[él\]/\[ellos\]», and unbracketed where the Spanish has an explicit pronoun or none ("I give", "we are", "it is said").

**Divergencias applied** (`sesion-26-suttas-482-502.divergencias-ingles.md`):
- §484 (div. 1): short gloss "Optionally, \[also\] of “ghaṭa” and others." (N "Sometimes of ‘ghaṭa’ and others."); vutti restructured after the Spanish: "Optionally, in the causative, there is strengthening of the roots “ghaṭa” and others that do not end in a conjunct consonant." (N "…of (the vowel of) the root that does not end in a conjunct consonant, of roots ‘ghaṭa’ and others").
- §487 (div. 3): *vussati* "(it is inhabited)" (N "(he) causes to live").
- §491 (div. 4): "By indicating the state with “kāsatta”, also in other cases there is insertion of ‘s’:" (N "By showing state in “kāsatta”, also when there are other (inflections), there is insertion of ’s’.").
- §493–§495 (div. 5): *attha* "(you all are)" — plural, see (b); *atthi* "(\[he\] is)"; *atthu* "(let it be)" (N's own words, brackets removed as in the Spanish).
- §496 (div. 6): N's "Who are you Sir?" kept as "(who are you, Sir?)" — the Spanish keeps «señor»; the divergencia leaves *mārisa* ("friend", Thitzana) to the IEBH.
- §499–§500 (div. 7): grouping by person kept as N and the Spanish: "(I give) … (\[he\] should give)". The Pāḷi order is "dajjāmi, dajjeyya; dadāmi, dadeyya"; Thitzana treats *dadāmi/dadeyya* as counter-examples of *vā*.
- **§486 (div. 2) NOT applied — see (b).**

**Follows the Spanish (expansion or correction of N):**
- §482 gloss: "\[there is\]" bracketed (Spanish «\[hay\]»).
- §483 gloss: "(vuddhi)" added and "\[the vowel of the root\]" (N "(vowel of the root that)"); counter-examples "such as in the following examples" (plural; N "example", two forms follow).
- §485 vutti: "\[other than the causative\]", "\[of the vowel\]" as the Spanish brackets; *ca* extension set as a header line with a numbered example.
- §488: "of the suffix ‘ya’" (N "of ‘ya’"); sequence label "Sequence of **vuyhati**, which comes from the root ‘vaha’ (carrying):" (N "Formation of “vuyhati”. It comes from the root ‘vaha’, carrying."). Steps copied from the Spanish byte for byte (see (c) on step 2).
- §489: "there is the letter ‘ghe’" (Spanish «la letra»; N "there is ‘ghe’").
- §491 gloss: "When \[the inflection\] “ajjatanī” follows, \[there is\] ‘kāsa’ of “kara”." (N "In the “ajjatanī” there is…").
- §492 gloss: "\[of the root\]" bracket (N "(consonant of the root)").
- §496 vutti: "When the inflection ‘si’ follows" (N "When there is ‘si’").
- §497: "There are the substitutions" (article added, as Spanish «las sustituciones»).
- §499: "there is the substitution" (article, as N's own §500–§501).
- §500: *vajjeyya, vadeyya* "(\[he\] should say)" — N "(I) should say"; Spanish «\[él\] debería decir» (3rd sg optative, parallel to N's own §499 "(he) should give").
- §501: *ghammatu/gacchatu* "(let \[him\] go)", *ghammāhi/gacchāhi* "(go!)", *ghammāmi/gacchāmi* "(I go)" — N groups "(Let it) go (ghammatu, ghammāhi)"; the Spanish separates 3rd sg imperative / 2nd sg imperative / 1st sg.
- §502: vutti "the end \[vowel\] … and others becomes the letter ‘ī’" (Spanish «la \[vocal\] final … y otras … la letra ‘ī’»; N "the end of the roots … becomes ‘ī’", without *evamādīnaṃ*); "and “matha”" for N's list comma; *ṭhīyati* "(one stands)" — N "standing", Spanish «se está en pie» (impersonal passive), see (b).
- Kept N against the Spanish's different word (no divergencia): §483 *mantayati* "consults" (ES «delibera»); §484 "causes to try" (ES «hace esforzarse»); §487 *vuyhati* "he is carried away", §488 "it is carried" (N's own two wordings); §502 *dhīyati* "it is contained" (ES «es sostenido»).

**Typos of N-EN corrected:** "strengthning" (§483), "roots that does not" → "do not" (§485), "inflection follow" → "follows" (§491), "elision of end" → "of the end" (§493), "elsion" (§497), "Sir" comma (§496). N's "adasi"/"uccati" in his prose glosses disappear because the forms are now the bold Pāḷi of the Spanish.

**Notes.** 86, 87: N's 61, 62 verbatim. 82, 83, 84, 85, 88: editor's notes, translated from the Spanish, unlabelled.

#### (b) Uncertain — the IEBH to decide

1. **§486, *gūhayati / dūsayati* (div. 2).** The divergencia says the Spanish was translated «hace ocultar» / «hace corromper», but the final Spanish has «hace proteger» with note 85 «Oculta.» and «hace perecer». Since the Spanish master did not take the divergencia and note 85 only makes sense against "protect", I kept N verbatim — "(\[he\] causes to protect),[^85] … (\[he\] causes to injure, spoil)" — and note 85 as "Hides." (I read «Oculta» as the verb, glossing *guha*; it could also be read as an adjective.) If div. 2 stands: "causes to hide" / "causes to corrupt" and note 85 becomes redundant. *Dūsayati*: the Spanish «perecer» is neither N's "injure, spoil" nor the divergencia's «corromper»; I did not follow it.
2. **§493 *attha* "(you all are)".** The Spanish «vosotros sois» has no brackets; English has no unbracketed plural "you". Alternatives: "(you \[pl.\] are)", "(ye are)".
3. **§502 *ṭhīyati* "(one stands)".** Rendering of the Spanish impersonal «se está en pie»; N "standing". Possible alternative "(it is stood)".
4. **§501 *ghammāhi* "(go!)"** for «ve tú»; alternative "(go \[you\])".
5. **Note 88** «La letra ‘i’ es indicativa de √gamu» rendered literally "The letter ‘i’ is indicative of √gamu" (i.e. *gami-* in the sutta stands for *gamu*). Wording may want smoothing.
6. **Fourth-section heading.** The brief says the range begins with the heading of the fourth section, but `tramo4-482-502.es.md` begins at §482: «CATUTTHA-KAṆḌA / CUARTA SECCIÓN» is at the end of `tramo3-458-481.es.md` (lines 566–567). I did not add it here (it would break line-for-line parity with the Spanish range); whoever builds range 3 should render it "**CATUTTHA-KAṆḌA**  / **FOURTH SECTION**".

#### (c) Problems noticed in the Spanish (reported, not changed)

1. **§483 Pāḷi vutti: "kāriyte"** — should be *kārite* (N-EN prints "kāriye", also wrong). Pāḷi left byte-identical.
2. **§486 Pāḷi vutti: "dhātunaṃ"** — expected *dhātūnaṃ* (N-EN has the same).
3. **§486: divergencia 2 not reflected** in the Spanish (see (b) 1).
4. **§488 sequence step 2: "vah (§521)"** — N-EN has "vah**~~a~~** (§521)" (the elided ‘a’ shown struck through). The Spanish drops the strikethrough; copied as in the Spanish.
5. **§488 vutti:** double space in «del sufijo  ‘ya’».
6. **§491 vutti:** missing space in «‘kāsa’de».
7. **§492 breakdown:** «mi-mā-naṃ» vs. the sutta «mi-mānaṃ» (hyphenation differs; possibly intentional split mi-mā + naṃ).
8. **§487 examples:** Pāḷi has *uccate* (attanopada); N-EN's prose gloss reads "uccati" — no issue in the Spanish, noted only because the two sources differ.
9. **Note 83:** trailing space after «‘aya’.» (dropped in the English).

### Range 5 (§503–§523, closing verse and formulas): deviations from Nandisena's English

Base: N-EN verbatim (ṃ throughout). The Spanish range file gives the structure. Pāḷi blocks, headings, the verse in Pāḷi, the Pāḷi closing formulas and the Pāḷi variant notes (89, 98, 99, 101, 106) are byte-identical with the Spanish.

#### (a) Where the English departs from N-EN's wording

**Fixed terms and formulae, applied throughout.**
- *vā*: N-EN "Sometimes" → **"Optionally"** in §505, §506, §507, §508, §511, §512, §522 (glosses and vuttis), and "“vā” (sometimes)" → "“vā” (optionally)" in every *kimatthaṃ*. The Spanish says «opcionalmente» in all of them.
- *kimatthaṃ*: N-EN "Why it is said “X”?" → "What is the purpose of saying “X”?" (12 places).
- "To allow an exception **of** this rule" (§506, §507, §509, §519) → "**to** this rule", which is N-EN's own wording in §518, §521 and §522. "such in" → "such as in" (§519, §521).
- Supplied words in square brackets wherever the Spanish has them ("\[There is\]", "\[there are\]", "\[roots\]", "\[syllable\]", "\[letter\]", "\[inflections\]", "\[inflections called\]", "\[become\]", "\[becomes\]", "\[reach\]", "\[suffixes\]", "\[chapter of the\]", "\[on it\]"). In the example glosses N-EN's "(He) …" / "(they) …" → "(\[he\] …)" / "(\[they\] …)". "follows" (locative) and "after" (ablative) are unbracketed.
- Roots in double quotes and letters/suffixes/inflections in single quotes, as the Spanish (N-EN uses single quotes for roots).
- Where N-EN gives one gloss for a list of words, the gloss sits in the Spanish position (e.g. §505, two numbered lines).

**Accepted divergencias (sesion-26-suttas-503-523), applied.**
- Div. 2, §517: the five operations in the order of the Pāḷi, "lengthening, reversal, substitution, elision and insertion", and "of the roots, of the inflections and of the suffixes" (N-EN: "insertion, elision, substitution, reversion, lengthening of suffixes, inflections, roots"). "reversal" rather than N-EN's "reversion", as in the §404 set in Taddhita (memo §8).
- Div. 3, §515 vutti: "those \[letters\] ‘o’ and ‘e’" (N-EN "those ‘e’ and ‘o’"). The gloss has no list of letters, as in the Spanish, so N-EN's "(‘e’ and ‘o’)" there is dropped.
- Div. 5, §515: *lāveti* "causes to reap" (N-EN "causes to cut").
- Div. 6, §510: the two pairs kept with a semicolon, "**Vajjemi**, **vademi**; **vajjāmi**, **vadāmi** (I speak)", as in the Spanish.
- Div. 7, §517: *vakkhetha* / *dakkhetha* "you would speak" / "you would see" (N-EN "(you) speak", "(you) see").
- Div. 8, verse: "let the sagacious ones reflect" (N-EN "let the wise ones think again and again"). "Wise" is avoided because it renders *dhīra* in the opening verse (K) of the chapter.
- Div. 1 (§521) and div. 4 (§515) could not be applied as written. See (b).

**Following the Spanish (structure or expansion).**
- §503: "the initial \[syllable\]" (N-EN "the beginning"), from the Spanish «la \[sílaba\] inicial». Typo "og" → "of".
- §506: the gloss begins "And everywhere" (*ca*), as the Spanish; "the initial \[letter\]" (N-EN "the beginning").
- §507: the gloss and vutti say "the \[inflections\] / \[inflections called\] “asabbadhātuka”" (N-EN "the “asabbadhātuka”").
- §508: N-EN gives no English for the *kimatthaṃ*. The answer is translated from the Spanish: "To allow an exception … **jāneyya** (\[he\] may know)".
- §509: gloss "or the state of ‘ya’" (N-EN "or ‘ya’"); vutti "the suffix ‘nā’ that follows the root “ñā”" (N-EN "of the root").
- §510: gloss "the letter ‘a’"; vutti "or **optionally** it is changed to ‘e’" (the Spanish «u opcionalmente»; N-EN has no "optionally").
- §511: gloss "\[There is\] the state of ‘u’ of the letter ‘o’" (N-EN "There is ‘u’ of letter ‘o’").
- §512: vutti "of the root “kara”"; the counter-example sentence says "examples" (plural, two words), as the Spanish. N-EN has a double space there, now removed.
- §513: gloss "When a vowel follows, \[there is\] ‘ava’ in place of ‘o’" (N-EN "When there is a vowel, there is ‘ava’ of ‘o’"). The Spanish has «en lugar de».
- §515: "By dividing the sutta, also in another case there is the substitution ‘āya’ of the letter ‘e’:" (N-EN "also when other follow"), with the examples as a numbered line, as the Spanish.
- §516: gloss "When the \[inflections\] “asabbadhātuka” follow" and vutti "When all the \[inflections called\] “asabbadhātuka” follow, there is insertion of ‘i’" (N-EN "There is insertion of ‘i’ in all “asabbadhātuka”"). In the *kimatthaṃ* the Spanish gloss of the word is placed in parentheses after it: "“asabbadhātukamhi” (when the \[inflections\] “asabbadhātuka” follow)". See (c). Typo "operaratio" → "operation".
- §517: "formations" for *sādhana* (N-EN "examples") in the vutti and in "Thus also the other formations should be formed", as the Spanish «formaciones» (cf. note 107). "the Victorious One" for *jina* (N-EN "the Conqueror"), the glossary term (memo §2.5) and the Spanish «el Victorioso». "have not been show" → "shown"; "according the Word" → "according to the Word". The operations are set between en dashes, as the Spanish. *Jāniyā* "\[he\] may know" (N-EN "should know") and *siyā* "may be" (N-EN "(he) would be"), as in §506 and §508 and the Spanish «podría». N-EN leaves *kareyya* unglossed ("(he) should do," with no word); the gloss is given. *Jāyati* "arises" (N-EN "(It) is arisen", ungrammatical); see (b).
- §518: gloss "The \[inflections\] “attanopada” \[reach\] the state of “parassapada”" and vutti "reach the state of" (N-EN "are changed (to)"). This follows the Spanish «alcanzan (al/el) estado», which renders *-ttaṃ* and *āpajjante*. N-EN's vutti "changed “parassapada”" is missing "to". N-EN's example gloss "(it) is cooked (paccate)" → *paccati*, the word in his own Pāḷi line.
- §519: "when … follow" for N-EN "in the" / "when there are the inflections of the" (locative). "The is insertion" → "\[There is\] insertion".
- §520: "when ‘ti’ follows" / "when the inflection ‘ti’ follows" (N-EN "when there is"); "there insertion" → "there is insertion".
- §521: "the final \[letter\]" in the gloss and vutti (N-EN "the end" / "the end (consonant)"). His "(consonant)" contradicts his own note 70 (= 110), where the elided letter is the vowel ‘u’. The *kimatthaṃ* gloss is "(which has various vowels)" (N-EN "(of many vowels)"), and the counter-example reads "when the root has only one vowel" (N-EN "only one syllable"), as the Spanish. *Pāti* is glossed "(\[he\] protects)"; N-EN has "(he) protects" with no word in parentheses. *Mahīyati* / *mathīyati* are glossed as passives, "is honored" / "is churned" (N-EN active "(he) honors", "(he) churns"), as the Spanish «es honrado», «es batido». They are *ya*-passives (cf. note 111). "Whty" → "What".
- §523: gloss "of the \[suffixes\] “kārita”" (N-EN "of the causative"). The Spanish keeps "kārita" in the gloss; the vutti says "causative suffixes", as both.
- Verse: one paragraph, as the Spanish. "the \[chapter of the\] verb has been shown by me in brief" (N-EN "it has been shown by me this verb chapter in brief"). The word order is corrected and the brackets follow the Spanish. "By their own special knowledge" (N-EN "By one’s special knowledge"; *sakaṃ*, Spanish «su propio»). "\[on it\]" from the Spanish.
- Closing formulas: N-EN verbatim, bold as in the Spanish: "**Thus ends the fourth section in the verb chapter**", "**End of the Verb Chapter**".

**Notes.**
- 89, 98, 99, 101, 106: Pāḷi variants, identical.
- 91 (= N-EN 64), 95 (= 65), 110 (= 70), 111 (= 71): N-EN verbatim, with curly quotes as in the Spanish. Typo in 111: "there end vowel" → "the end vowel".
- 90, 92, 93, 94, 96, 97, 100, 102, 103, 104, 105, 107, 108, 109, 112, 113: editor's notes, translated from the Spanish and unlabelled. «Después» → "Then".
- No Thitzana note falls in this range.

#### (b) Places where I am unsure

1. **Div. 4 (§515, *pāpuṇanti* «llegan a») is not in the final Spanish.** The final Spanish says «se convierten en», both bracketed in the gloss and plain in the vutti. I followed the final Spanish, "\[become\]" / "become", which also replaces N-EN's "are changed to". If the IEBH wants div. 4 as described, the vutti should read "those \[letters\] ‘o’ and ‘e’ reach ‘āva’ and ‘āya’", and the gloss should become "Those \[reach\] …". The Spanish would need the same change.
2. **Div. 1 (§521, *anekasara* «que no es de una sola vocal») is not in the final Spanish either.** The Spanish keeps «que tiene varias vocales» in the gloss, the vutti and the *kimatthaṃ*. Only the counter-example was changed, to «cuando la raíz tiene una sola vocal». I followed the Spanish: "which has various vowels" (N-EN), with "only one vowel" in the counter-example. If div. 1 is applied, the three places would read "which is not of a single vowel".
3. **Unbracketed glosses without a subject.** The Spanish glosses some words without a subject and without brackets: *siyā* «podría ser», *jāyati* «nace», *ahosi* «fue», and the passives of §518 and §521. I gave bare English, "may be", "arises", "was", "is said", following the bracket rule. For *vakkhetha* / *dakkhetha* (Spanish «diríais», «veríais») English needs a pronoun to show the person. I wrote "you would speak" / "you would see" **unbracketed**, like *asi* "you are" (Spanish «tú eres») and *vadāmi* "I speak" («yo digo»). Someone should check whether "you" ought to be bracketed. For *jāyati* I kept N-EN's verb ("arises", from his "is arisen"). The Spanish has «nace» ("is born"), and either reading is defensible.
4. **§519 *agamissā* / *gamissā*:** I kept N-EN's "should have gone". The Spanish has «habría ido» ("would have gone"), and divergencia 7 moved the sattamī forms of §517 to "would". I did not change this one because no divergencia covers it. Someone should check it.
5. **§522:** I kept N-EN's two different glosses, *niyacchati* "regulates" and *niyamati* "determines". The Spanish uses «controla» for both. They could be unified.
6. **Verse, *vicakkhaṇā* → "the sagacious ones":** the Spanish has «sagaces». I avoided "discerning" because the Spanish «discernimiento» renders *buddhi* in the same line. This is my choice of word; the IEBH may prefer another.
7. **Note 105:** the Spanish «No obstante que aquí no hay sufijo causativo ‘e’ → ‘āya’» has no comma. I read it as "Although there is no causative suffix here, ‘e’ → ‘āya’", where ‘e’ is the root-final of *ge*. The alternative reading "no causative suffix ‘e’" also makes sense, and I cannot tell which the editor meant.
8. **The `<!-- NOTAS DEL TRAMO -->` marker** is kept as it is so that the assembler can split body and notes. Remove it if the assembled master should carry no Spanish marker.

#### (c) Problems noticed in the Spanish (reported only, not changed)

1. **§519, word breakdown:** «\[Akāra-āgamo \+ hiyyattanī, ajjatanī-kālātipattīsu, 2\]» has a comma inside the compound. It should be «hiyyattanī-ajjatanī-kālātipattīsu». The comma is copied in the English heading, which has to be byte-identical.
2. **§509, vutti:** the Pāḷi has «lopo hoti **vā**» and the Pāḷi line has a *Vā ti kimatthaṃ?*, but neither the gloss nor the vutti in Spanish says «opcionalmente». N-EN also lacks it. The English follows them.
3. **§518, gloss:** «\[alcanzan\] **al** estado de “parassapada”» should be «el estado», as in the vutti.
4. **§516, *kimatthaṃ*:** «¿Con qué fin se dice cuando siguen las \[inflexiones\] “asabbadhātukamhi”?» is garbled. The Pāḷi word is quoted inside its own gloss, and the inflections are named in the locative. A parallel form would be «¿Con qué fin se dice “asabbadhātukamhi” (cuando siguen las \[inflexiones\] “asabbadhātuka”)?»
5. **Divergencias 1 and 4 vs the final Spanish:** see (b) 1–2. The divergencias file says «se tradujo» for wordings that the Spanish file does not carry.
6. **Note 91:** «hiyyatanī» (single *t*), copied from N-EN fn 64. Everywhere else, including §519, the spelling is «hiyyattanī». It was kept in the English because the note is N-EN verbatim.
7. **Inconsistent subject brackets in §517:** «**jāyati** (nace)», «**siyā** (podría ser)» and «**ahosi** (fue)» have no «\[él\]», while every other singular in the list has one. The same holds for §506 *siyā*.
8. **The section-closing formula is phrased differently from range 1:** range 1 has «Así \[termina\] la primera sección del capítulo de los verbos»; this range has «Así termina la cuarta sección en el capítulo del verbo» (no bracket, «en», «del verbo»). N-EN also varies ("in the chapter of verbs" / "in the verb chapter").
9. **Note 108:** double space after «“pajjunnagatika”,». Notes 90, 103, 107 and 111 end with a trailing space. These are typographic only.
10. **Note 109 (*bravīti*):** «√brū \+ a \+ ti. Después ‘ū’ → ‘o’ → ‘ava’» does not mention the ‘ī’ insertion of this very sutta, or what happens to the vikaraṇa ‘a’. It is not wrong as far as it goes, but it is incomplete. I am not sure how the editor intends the derivation.
