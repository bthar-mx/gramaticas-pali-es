// Porte fiel de `nuestro/operaciones.py`. Las operaciones de sandhi, hacia
// adelante: UNA POR AFORISMO, con su enunciado arriba, tal como manda el
// proyecto. Estas funciones no deciden: aplican. Quien decide es la
// recomposición. Ninguna operación se agrega sin enunciado.
//
// Convención de pasos (CLAUDE.md §3): el texto primero, los segmentos
// separados por espacios, la cita entre paréntesis al final.

"use strict";

const VOCALES = "aāiīuūeo";
const LARGA = { a: "ā", i: "ī", u: "ū" };
const CORTA = { "ā": "a", "ī": "i", "ū": "u" };

// Las cinco series y su nasal final, «la última consonante del grupo».
const VAGGA = {
    k: "ṅ", kh: "ṅ", g: "ṅ", gh: "ṅ", "ṅ": "ṅ",
    c: "ñ", ch: "ñ", j: "ñ", jh: "ñ", "ñ": "ñ",
    "ṭ": "ṇ", "ṭh": "ṇ", "ḍ": "ṇ", "ḍh": "ṇ", "ṇ": "ṇ",
    t: "n", th: "n", d: "n", dh: "n", n: "n",
    p: "m", ph: "m", b: "m", bh: "m", m: "m",
};
// La segunda y cuarta de cada serie, y la primera y tercera con que se
// duplican (§29).
const SEGUNDA_CUARTA = {
    kh: "k", gh: "g", ch: "c", jh: "j",
    "ṭh": "ṭ", "ḍh": "ḍ", th: "t", dh: "d",
    ph: "p", bh: "b",
};
const DIGRAFOS = Object.keys(SEGUNDA_CUARTA);

// §269, con la ampliación que el propio documento enuncia debajo de la regla.
const CONJUNTAS = { ty: "c", ly: "l", ny: "ñ", dy: "j", sy: "s",
                    thy: "ch", dhy: "jh", "ṇy": "ñ" };

// La lista de la Rūpasiddhi Nāma que fija el grupo de «mana» (§183).
const GRUPO_MANA = new Set(["vaca", "vaya", "teja", "tapa", "ceta", "tama",
    "yasa", "aya", "paya", "sira", "chanda", "sara", "ura", "raha",
    "aha", "mana"]);

function nfc(t) { return t.normalize("NFC"); }

function cot(t) {
    t = nfc(t).replace(/’/g, "").replace(/'/g, "").replace(/-/g, "");
    return t.replace(/\s+/gu, "").toLowerCase().replace(/ṁ/gu, "ṃ");
}

function primeraLetra(t) {
    const dos = t.slice(0, 2);
    return (DIGRAFOS.includes(dos) || dos in VAGGA) ? dos : t.slice(0, 1);
}

function cierre(pasos, unido, atestiguada) {
    // Añade §11 y, si procede, el paso de la edición moderna.
    // `atestiguada === null` es el modo enumeración: no se compara.
    pasos = pasos.concat([`${unido} (§11)`]);
    if (atestiguada === null || atestiguada === undefined) return pasos;
    if (cot(unido) !== cot(atestiguada)) return null;
    if (nfc(atestiguada).trim() !== nfc(unido).trim())
        pasos.push(`${atestiguada} (EM)`);
    return pasos;
}

function sep10(a, b) {
    // §10 sobre la voz anterior: raíz · vocal final · voz siguiente.
    if (!a || !VOCALES.includes(a[a.length - 1]) || a.length < 2) return null;
    return [a.slice(0, -1), a[a.length - 1]];
}

// ── Vocal + vocal ───────────────────────────────────────────────────────

function op14(a, b, F) {
    // §14 — «A veces las vocales "i", "ī" y "u", "ū", cuando siguen a una
    // vocal disímil que ha sido elidida, se convierten en "e" y "o"
    // respectivamente». La disímil es sólo «a» y «ā» (nota 3).
    const s = sep10(a, b);
    if (!s || !b || !"iīuū".includes(b[0]) || !"aā".includes(s[1])) return null;
    const [raiz, v] = s;
    const nuevo = ("iī".includes(b[0]) ? "e" : "o") + b.slice(1);
    return cierre([`${a} ${b}`,
                   `${raiz} ${v} ${b} (§10)`,
                   `${raiz} ${b} (§12)`,
                   `${raiz} ${nuevo} (§14)`], raiz + nuevo, F);
}

function op19(a, b, F) {
    // §19 — «la sílaba "ti" de "ati", "pati" y "iti" se convierte en "c" y
    // ésta se duplica». La duplicación la hace §28.
    if (a.slice(-2) !== "ti" || !["a", "pa", "i"].includes(a.slice(0, -2))
        || !b || !VOCALES.includes(b[0])) return null;
    const raiz = a.slice(0, -2);
    return cierre([`${a} ${b}`,
                   `${raiz}c ${b} (§19)`,
                   `${raiz}cc ${b} (§28)`], raiz + "cc" + b, F);
}

function op20(a, b, F) {
    // §20 — «la sílaba "dha" de "idha", se convierte en "da"».
    if (a !== "idha" || !b || !VOCALES.includes(b[0])) return null;
    return cierre([`${a} ${b}`,
                   `ida ${b} (§20)`], "ida" + b, F);
}

function op22(a, b, F) {
    // §22 — «después de "yathā" y "tathā", la "e" de "eva" se convierte en
    // "ri"».
    if (!["yathā", "tathā"].includes(a) || b !== "eva") return null;
    const corto = a.slice(0, -1) + "a";
    return cierre([`${a} ${b}`,
                   `${a} riva (§22)`,
                   `${corto} riva (§22)`], corto + "riva", F);
}

// ── Vocal + consonante ──────────────────────────────────────────────────

function op25(a, b, F) {
    // §25 — «una vocal, cuando va seguida por una consonante, se alarga».
    if (!a || !(a[a.length - 1] in LARGA) || !b || VOCALES.includes(b[0]))
        return null;
    const largo = a.slice(0, -1) + LARGA[a[a.length - 1]];
    const pasos = [`${a} ${b}`, `${largo} ${b} (§25)`];
    return cierre(pasos.slice(), largo + b, F)
        || cierre(pasos.slice(), largo + " " + b, F);
}

function op26(a, b, F) {
    // §26 — «una vocal, cuando va seguida por una consonante, se acorta».
    if (!a || !(a[a.length - 1] in CORTA) || !b || VOCALES.includes(b[0]))
        return null;
    const corto = a.slice(0, -1) + CORTA[a[a.length - 1]];
    const pasos = [`${a} ${b}`, `${corto} ${b} (§26)`];
    return cierre(pasos.slice(), corto + b, F)
        || cierre(pasos.slice(), corto + " " + b, F);
}

function op27(a, b, F) {
    // §27 — «la "o" de "eta" y "ta", cuando va seguida por una consonante, se
    // elide». El enunciado nombra «eta» y «ta»: las voces son `eso` y `so`.
    if (!["eso", "so"].includes(a) || !b || VOCALES.includes(b[0])) return null;
    const raiz = a.slice(0, -1);
    return cierre([`${a} ${b}`,
                   `${raiz} o ${b} (§10)`,
                   `${raiz} ${b}, ${raiz} a ${b} (§27)`], raiz + "a " + b, F);
}

function op29(a, b, F) {
    // §29 — «la segunda y cuarta consonante de las agrupadas se duplican en
    // la primera y tercera de las agrupadas respectivamente».
    if (!a || !VOCALES.includes(a[a.length - 1])) return null;
    const ini = primeraLetra(b);
    if (!(ini in SEGUNDA_CUARTA)) return null;
    const doble = SEGUNDA_CUARTA[ini] + b;
    return cierre([`${a} ${b}`,
                   `${a} ${doble} (§29)`], a + doble, F);
}

function op36(a, b, F) {
    // §36 — «cuando una consonante sigue, hay insersión de la letra "o"».
    const s = sep10(a, b);
    if (!s || !b || VOCALES.includes(b[0])) return null;
    const [raiz, v] = s;
    return cierre([`${a} ${b}`,
                   `${raiz} ${v} ${b} (§10)`,
                   `${raiz} ${b} (§12)`,
                   `${raiz} o ${b} (§36)`], raiz + "o" + b, F);
}

function op44(a, b, F) {
    // §44 — «el prefijo "abhi" cuando va seguido por una vocal se substituye
    // por "abbh"».
    if (a !== "abhi" || !b || !VOCALES.includes(b[0])) return null;
    return cierre([`${a} ${b}`,
                   `abbh ${b} (§44)`], "abbh" + b, F);
}

function op45(a, b, F) {
    // §45 — «el prefijo "adhi" cuando va seguido por una vocal se substituye
    // por "ajjh"».
    if (a !== "adhi" || !b || !VOCALES.includes(b[0])) return null;
    return cierre([`${a} ${b}`,
                   `ajjh ${b} (§45)`], "ajjh" + b, F);
}

function op48(a, b, F) {
    // §48 — «el prefijo "pati" cuando va seguido por una vocal o una
    // consonante, se convierte en "paṭi"».
    if (a !== "pati") return null;
    return cierre([`${a} ${b}`,
                   `paṭi ${b} (§48)`], "paṭi" + b, F);
}

function op49(a, b, F) {
    // §49 — «cuando va seguida por una consonante, la vocal final de "putha"
    // se convierte en "u"». El paso de duplicación lo hace §28.
    if (a !== "putha" || !b || VOCALES.includes(b[0])) return null;
    const ini = primeraLetra(b);
    const pasos = [`${a} ${b}`,
                   `puth a ${b} (§10)`,
                   `puth u ${b} (§49)`];
    const r = cierre(pasos.slice(), "puthu" + b, F);
    if (r) return r;
    return cierre(pasos.concat([`puth u ${ini}${b} (§28)`]),
                  "puthu" + ini + b, F);
}

function op50(a, b, F) {
    // §50 — «cuando va seguido por una consonante, el prefijo "ava" se
    // convierte en "o"».
    if (a !== "ava" || !b || VOCALES.includes(b[0])) return null;
    return cierre([`${a} ${b}`,
                   `o ${b} (§50)`], "o" + b, F);
}

function op79(a, b, F) {
    // §79 — «la letra "o", la substitución del prefijo "ava", se convierte en
    // "u"». Va después de §50, y §28 duplica.
    if (a !== "ava" || !b || VOCALES.includes(b[0])) return null;
    const ini = primeraLetra(b);
    const pasos = [`${a} ${b}`,
                   `o ${b} (§50)`,
                   `u ${b} (§79)`];
    const r = cierre(pasos.slice(), "u" + b, F);
    if (r) return r;
    return cierre(pasos.concat([`u ${ini}${b} (§28)`]), "u" + ini + b, F);
}

function op183(a, b, F) {
    // §183 — «cuando hay elisión de la inflexión nominal, la vocal final del
    // grupo de "mana" se convierte en "o"». El grupo lo fija la lista de la
    // Rūpasiddhi Nāma.
    if (!GRUPO_MANA.has(a)) return null;
    return cierre([`${a} ${b}`,
                   `${a.slice(0, -1)} ${a[a.length - 1]} ${b} (§10)`,
                   `${a.slice(0, -1)} o ${b} (§183)`],
                  a.slice(0, -1) + "o" + b, F);
}

function op269(a, b, F) {
    // §269 — «las consonantes conjuntas "ty", "ly", "ny", "dy" se convierten
    // en "c", "l", "ñ", "j" respectivamente y después éstas se duplican». El
    // documento amplía debajo a "sy", "thy", "dhy", "ṇy". Va después de §21.
    const s = sep10(a, b);
    if (!s || !b || !VOCALES.includes(b[0])) return null;
    const [raiz, v] = s;
    if (!"iī".includes(v)) return null;
    const conj = primeraLetra(raiz.slice(-1)) + "y";
    if (!(conj in CONJUNTAS)) return null;
    const nueva = CONJUNTAS[conj];
    const base = raiz.slice(0, -1);
    const pasos = [`${a} ${b}`,
                   `${raiz} ${v} ${b} (§10)`,
                   `${raiz} y ${b} (§21)`,
                   `${base + nueva} ${b} (§269)`,
                   `${base + nueva + nueva} ${b} (§28)`];
    return cierre(pasos, base + nueva + nueva + b, F);
}

// ── Niggahīta ───────────────────────────────────────────────────────────

function op31(a, b, F) {
    // §31 — «cuando va seguida por una consonante agrupada, la "niggahīta" se
    // convierte en la última consonante del grupo». Nota 14: k→ṅ, c→ñ, ṭ→ṇ,
    // t→n, p→m.
    if (!a.endsWith("ṃ")) return null;
    const ini = primeraLetra(b);
    if (!(ini in VAGGA)) return null;
    const nuevo = a.slice(0, -1) + VAGGA[ini];
    const pasos = [`${a} ${b}`, `${nuevo} ${b} (§31)`];
    return cierre(pasos.slice(), nuevo + b, F)
        || cierre(pasos.slice(), nuevo + " " + b, F);
}

function op31L(a, b, F) {
    // El «vā» de §31: la niggahīta se vuelve «l» ante «l». Su regla
    // niggahita 2 lo enuncia y §31 no: restringida a «saṃ» y «puma»:
    // `saṃ + lakkhaṇā`, `saṃ + lekho`, `puṃ + liṅgaṃ`.
    if (!["saṃ", "puṃ"].includes(a) || !b.startsWith("l")) return null;
    const nuevo = a.slice(0, -1) + "l";
    const pasos = [`${a} ${b}`,
                   `${nuevo} ${b} (por "vā" en §31)`];
    return cierre(pasos.slice(), nuevo + b, F)
        || cierre(pasos.slice(), nuevo + " " + b, F);
}

function op35L(a, b, F) {
    // La «ḷ» que se inserta después de «cha». §35 no la enumera; la nota 9
    // del documento sí: «Se inserta "ḷ" después de "cha" y numerales.» Se
    // implementa por la nota y se cita por la nota.
    if (a !== "cha" || !b || !VOCALES.includes(b[0])) return null;
    const pasos = [`${a} ${b}`,
                   `${a} ḷ ${b} (§35, nota 9)`];
    return cierre(pasos.slice(), a + "ḷ" + b, F)
        || cierre(pasos.slice(), a + "ḷ " + b, F);
}

function op32(a, b, F) {
    // §32 — «cuando "eva" y "hi" siguen, la "niggahīta" se convierte en "ñ";
    // y ésta se duplica cuando va seguida por "eva"».
    if (!a.endsWith("ṃ") || !["eva", "hi"].includes(b)) return null;
    const base = a.slice(0, -1) + "ñ";
    if (b === "hi") {
        // La forma unida primero (ver el porqué en el Python).
        const pasos = [`${a} ${b}`, `${base} hi (§32)`];
        return cierre(pasos.slice(), base + "hi", F)
            || cierre(pasos.slice(), base + " hi", F);
    }
    const pasos = [`${a} ${b}`,
                   `${base} eva (§32)`,
                   `${base} ñeva (§28)`];
    return cierre(pasos.slice(), base + "ñeva", F)
        || cierre(pasos.slice(), base + " ñeva", F);
}

function op33(a, b, F) {
    // §33 — «cuando "y" sigue, la "niggahīta" junto con "y" se convierte en
    // "ñ"; y ésta se duplica». Sólo "saṃ" y el pronombre "ya" (nota 15).
    if (!a.endsWith("ṃ") || !b.startsWith("y")) return null;
    const base = a.slice(0, -1) + "ñ";
    const resto = b.slice(1);
    const pasos = [`${a} ${b}`,
                   `${base} ñ${resto} (§33)`];
    return cierre(pasos.slice(), base + "ñ" + resto, F)
        || cierre(pasos.slice(), base + " ñ" + resto, F);
}

function op34(a, b, F) {
    // §34 — «cuando una vocal sigue, la "niggahīta" se convierte en "m" y
    // "d"». En "d" sólo después de "ya", "ta" y "eta" (nota 16).
    if (!a.endsWith("ṃ") || !b || !VOCALES.includes(b[0])) return null;
    for (const letra of ["m", "d"]) {
        if (letra === "d" && !["ya", "ta", "eta"].includes(a.slice(0, -1)))
            continue;
        const nuevo = a.slice(0, -1) + letra;
        const r = cierre([`${a} ${b}`,
                          `${nuevo} ${b} (§34)`], nuevo + b, F)
            || cierre([`${a} ${b}`,
                       `${nuevo} ${b} (§34)`], nuevo + " " + b, F);
        if (r) return r;
    }
    return null;
}

function op37(a, b, F) {
    // §37 — «cuando una vocal o una consonante sigue, se inserta la
    // "niggahīta"».
    return cierre([`${a} ${b}`,
                   `${a} ṃ ${b} (§37)`], a + "ṃ" + b, F)
        || cierre([`${a} ${b}`,
                   `${a} ṃ ${b} (§37)`], a + "ṃ " + b, F);
}

function op38(a, b, F) {
    // §38 — «cuando una vocal sigue, la "niggahīta" se elide». La nota 17
    // añade: elidida la niggahīta, se elide la vocal anterior y se alarga la
    // siguiente.
    if (!a.endsWith("ṃ") || !b || !VOCALES.includes(b[0])) return null;
    const sin = a.slice(0, -1);
    const pasos = [`${a} ${b}`, `${sin} ${b} (§38)`];
    const r = cierre(pasos.slice(), sin + b, F)
        || cierre(pasos.slice(), sin + " " + b, F);
    if (r) return r;
    const s = sep10(sin, b);
    if (!s || !(b[0] in LARGA)) return null;
    const [raiz, v] = s;
    const largo = LARGA[b[0]] + b.slice(1);
    return cierre(pasos.concat([`${raiz} ${v} ${b} (§10)`,
                                `${raiz} ${b} (§12)`,
                                `${raiz} ${largo} (§15)`]), raiz + largo, F);
}

function op39(a, b, F) {
    // §39 — «cuando una consonante sigue, la "niggahīta" se elide».
    if (!a.endsWith("ṃ") || !b || VOCALES.includes(b[0])) return null;
    const sin = a.slice(0, -1);
    const pasos = [`${a} ${b}`, `${sin} ${b} (§39)`];
    return cierre(pasos.slice(), sin + b, F)
        || cierre(pasos.slice(), sin + " " + b, F);
}

function op40(a, b, F) {
    // §40 — «la vocal después de la "niggahīta" se elide y la "niggahīta" se
    // convierte en la consonante final del grupo correspondiente».
    if (!a.endsWith("ṃ") || !b || !VOCALES.includes(b[0]) || b.length < 2)
        return null;
    const sinv = b.slice(1);
    const ini = primeraLetra(sinv);
    let pasos = [`${a} ${b}`, `${a} ${sinv} (§40)`];
    if (ini in VAGGA) {
        const nuevo = a.slice(0, -1) + VAGGA[ini];
        pasos = pasos.concat([`${nuevo} ${sinv} (§31)`]);
        return cierre(pasos.slice(), nuevo + sinv, F)
            || cierre(pasos.slice(), nuevo + " " + sinv, F);
    }
    return cierre(pasos.slice(), a + sinv, F)
        || cierre(pasos.slice(), a + " " + sinv, F);
}

function op41(a, b, F) {
    // §41 — «cuando la vocal siguiente a la "niggahīta" se elide, si la
    // consonante siguiente es conjunta, ésta se convierte en no-conjunta».
    if (!a.endsWith("ṃ") || !b || !VOCALES.includes(b[0]) || b.length < 3)
        return null;
    const sinv = b.slice(1);
    if (sinv.length < 2 || sinv[0] !== sinv[1]) return null;
    const simple = sinv.slice(1);
    const pasos = [`${a} ${b}`,
                   `${a} ${sinv} (§40)`,
                   `${a} ${simple} (§41)`];
    return cierre(pasos.slice(), a + simple, F)
        || cierre(pasos.slice(), a + " " + simple, F);
}

function op51(a, b, F) {
    // §51 — «a veces hay transposición de las letras "r", "h", "n"». Se
    // prueban los dos saltos —el contiguo y el de una letra en medio—, que
    // son los que las tres formas del banco atestiguan. Quien decide sigue
    // siendo la recomposición.
    if (!a) return null;
    const salidas = [];
    for (let i = 0; i < a.length; i++) {
        if (!"rhn".includes(a[i])) continue;
        for (const salto of [1, 2]) {
            for (const j of [i - salto, i + salto]) {
                if (!(j >= 0 && j < a.length)) continue;
                const letras = a.split("");
                [letras[i], letras[j]] = [letras[j], letras[i]];
                salidas.push(letras.join(""));
            }
        }
    }
    for (const trans of salidas) {
        const pasos = [`${a} ${b}`.trim(),
                       `${trans} ${b} (§51)`.trim()];
        const r = b
            ? (cierre(pasos.slice(), trans + b, F)
               || cierre(pasos.slice(), trans + " " + b, F))
            : cierre(pasos.slice(), trans, F);
        if (r) return r;
    }
    return null;
}

// ── Cadenas de dos operaciones ──────────────────────────────────────────
// Cada aforismo de sustitución nombra SU vocal y SU letra (enunciados del
// Sandhi-kappa): §17 sólo «e»→y; §18 sólo «o»,«u»→v; §21 sólo «i»,«ī»→y.
const VOCAL_SUST = { 17: "e", 18: "ou", 21: "iī" };
const LETRA_SUST = { 17: "y", 18: "v", 21: "y" };

function _sustitucion(a, b, n) {
    const s = sep10(a, b);
    if (!s || !b || !VOCALES.includes(b[0])) return null;
    const [raiz, v] = s;
    if (!VOCAL_SUST[n].includes(v)) return null;
    return [raiz, v, LETRA_SUST[n]];
}

function licenciaSustitucion(a, b, n) {
    // ¿Licencia el aforismo `n` esta sustitución? Se pregunta ANTES de llamar
    // al derivador del Venerable, que aplica los tres sin mirar la vocal.
    return _sustitucion(a, b, n) !== null;
}

function _cadenaSustAlarga(a, b, F, n) {
    // §17/§18/§21 y después §25. Del banco: «me ayaṃ · m e ayaṃ (§10) ·
    // m y ayaṃ (§17) · m y āyaṃ (§25) · myāyaṃ (§11)».
    const s = _sustitucion(a, b, n);
    if (!s || !(b[0] in LARGA)) return null;
    const [raiz, v, letra] = s;
    const largo = LARGA[b[0]] + b.slice(1);
    return cierre([`${a} ${b}`,
                   `${raiz} ${v} ${b} (§10)`,
                   `${raiz} ${letra} ${b} (§${n})`,
                   `${raiz} ${letra} ${largo} (§25)`],
                  raiz + letra + largo, F);
}

function op1725(a, b, F) { return _cadenaSustAlarga(a, b, F, 17); }
function op1825(a, b, F) { return _cadenaSustAlarga(a, b, F, 18); }
function op2125(a, b, F) { return _cadenaSustAlarga(a, b, F, 21); }

function op3526(a, b, F) {
    // §35 y después §26. Del banco, byañjana 2.2: «yathā idaṃ» da
    // «yatha-y-idaṃ»: §35 inserta la «y» y §26 acorta la «ā».
    if (!a || !(a[a.length - 1] in CORTA)) return null;
    const corto = a.slice(0, -1) + CORTA[a[a.length - 1]];
    for (const letra of "yvmdntrlhg") {
        const r = cierre([`${a} ${b}`,
                          `${a} ${letra} ${b} (§35)`,
                          `${corto} ${letra} ${b} (§26)`],
                         corto + letra + b, F);
        if (r) return r;
    }
    return null;
}

function _cadena38(a, b, F, segunda) {
    // §38 y después §12 o §13. Elidida la niggahīta, las dos voces quedan
    // vocal contra vocal, y ahí §12 y §13 se aplican por su propio enunciado.
    // De «paripucchiṃ ahaṃ»: §38 deja «paripucchi ahaṃ», §12 da
    // «paripucchahaṃ». De «cāriṃ ahaṃ»: §38 y §13 dan «cārihaṃ».
    if (!a.endsWith("ṃ") || !b || !VOCALES.includes(b[0])) return null;
    const sin = a.slice(0, -1);
    const s = sep10(sin, b);
    if (!s) return null;
    const [raiz, v] = s;
    const pasos = [`${a} ${b}`,
                   `${sin} ${b} (§38)`,
                   `${raiz} ${v} ${b} (§10)`];
    if (segunda === 12)
        return cierre(pasos.concat([`${raiz} ${b} (§12)`]), raiz + b, F);
    if (b.length < 2) return null;
    return cierre(pasos.concat([`${raiz} ${v} ${b.slice(1)} (§13)`]),
                  raiz + v + b.slice(1), F);
}

function op3812(a, b, F) { return _cadena38(a, b, F, 12); }
function op3813(a, b, F) { return _cadena38(a, b, F, 13); }

// Claves como en el Python: números para los aforismos, cadenas para las
// combinaciones. Un Map admite las dos sin coerción.
const TODAS = new Map([
    [14, op14], [19, op19], [20, op20], [22, op22], [25, op25], [26, op26],
    [27, op27], [29, op29], [31, op31], [32, op32], [33, op33], [34, op34],
    [36, op36], [37, op37], [38, op38], [39, op39], [40, op40], [41, op41],
    [44, op44], [45, op45], [48, op48], [49, op49], [50, op50], [51, op51],
    [79, op79], [183, op183], [269, op269],
    ["17+25", op1725], ["18+25", op1825], ["21+25", op2125],
    ["35+26", op3526], ["38+12", op3812], ["38+13", op3813],
    ["31vā", op31L], ["35nota9", op35L],
]);

module.exports = {
    VOCALES, LARGA, CORTA, VAGGA, SEGUNDA_CUARTA, CONJUNTAS, GRUPO_MANA,
    VOCAL_SUST, LETRA_SUST, TODAS,
    primeraLetra, licenciaSustitucion, cierre, sep10, cot,
};
