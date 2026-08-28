// Porte fiel del núcleo de `nuestro/solucionar_sandhis.py` — etapa 1 del
// porte a JS (briefing sesión 30 §6): `cotejo()`, las operaciones, el bucle
// proponer-verificar y la lógica del verificador.
//
// **Proponer y verificar. Nunca afirmar.** Se propone un corte y una cadena
// de reglas, se aplica la cadena, y tiene que reproducir exactamente la forma
// de entrada. Si no coincide, se descarta. Se devuelven TODAS las lecturas
// válidas, no una.
//
// Modo de esta etapa: **solo-canon** (decisión del Venerable, 2026-08-28).
// El léxico es el corpus convertido del Sexto Concilio; el DPD no interviene
// en ninguna capa. `descomposicion()` devuelve por eso siempre `[]`.
//
// El motor no lee archivos: recibe los datos por `iniciar()`. Así el mismo
// núcleo sirve en Node (el arnés carga JSON del árbol) y en el navegador
// (etapa 4, carga bajo demanda). El Python queda como referencia permanente;
// todo cambio acá se mide contra él con `arnes.js`.

"use strict";

const { cotejo } = require("./normalizar");
const OP = require("./operaciones");
const D = require("./derivar");

const VOCALES = "aāiīuūeo";
const NASALES = "ṅñṇnm";
const MARCAS = "’'-";

// El estado que en Python vive en `_cache`. Se llena con `iniciar()`.
const _cache = { lexico: null, nipata: new Set(), lexicoBanco: new Set() };

function partirComponentes(t) {
    t = (t || "").trim();
    if (!t) return [];
    if (t.includes(" + ")) return t.split(" + ").map(x => x.trim());
    return t.split(/\s+/u).filter(x => x);
}

// ── Iniciar: el léxico del canon y las voces del propio banco ───────────
//
// Réplica de la parte de `cargar()` que la etapa 1 necesita. En solo-canon
// el léxico entero es el corpus del Sexto Concilio (118 volúmenes), más el
// segundo léxico: las voces que el propio banco atestigua como componente
// —`putha`, `vipali`, `ani`, `chayo`…—. Ese añadido hace circular la medida
// del banco, y así está dicho en el informe; el número que vale es el del
// corpus, que estas voces no tocan.
function iniciar({ formasCanon, reglas, tablas, listas }) {
    _cache.lexico = new Set();
    for (const f of formasCanon) _cache.lexico.add(cotejo(f));

    // El banco, sólo para extraer las voces atestiguadas como componente.
    const entradas = [];
    for (const c of reglas.ce) entradas.push(c.comp || "");
    if (tablas) {
        for (const fila of tablas.filas)
            for (const s of (fila.secuencias || []))
                entradas.push(s.forma_inicial || "");
    }
    const extra = new Set();
    for (const comp of entradas) {
        for (const pieza of partirComponentes(comp)) {
            const q = cotejo(pieza);
            // len>=3, alfabética, sin «√» ni «+» — igual que el Python.
            if (q.length >= 3 && /^\p{L}+$/u.test(q)
                && !pieza.includes("√") && !pieza.includes("+"))
                extra.add(q);
        }
    }
    _cache.lexicoBanco = new Set(
        [...extra].filter(q => !_cache.lexico.has(q)));
    for (const q of _cache.lexicoBanco) _cache.lexico.add(q);

    _cache.nipata = new Set((listas ? listas.nipata : []).map(cotejo));
}

function esPalabra(t) { return _cache.lexico.has(cotejo(t)); }

// ── Las descomposiciones del DPD: fuera, por decisión del Venerable ─────
// En el Python, `descomposicion()` bisecta el TSV del DPD si existe. En el
// porte el DPD no interviene: siempre `[]`. (El archivo tampoco vino en la
// entrega; el Python de referencia mide con él ausente.)
function descomposicion(_voz) { return []; }

// ── El vecindario ───────────────────────────────────────────────────────
// Para cada punto de corte se enumeran las voces que, de existir, podrían
// haber producido ese prefijo y ese sufijo. No decide: enumera. Filtra el
// léxico, y decide la recomposición.

function vecinosA(pre) {
    const v = new Set([pre]);
    if (pre) {
        for (const x of VOCALES) {
            v.add(pre + x);                    // se le elidió la vocal final (§12…)
            v.add(pre.slice(0, -1) + x);       // se le sustituyó (y, v, largo, corto)
        }
        v.add(pre + "ṃ");                      // se le elidió la niggahīta (§38, §39)
        for (const x of VOCALES) {
            // §38 y la nota 17: elididas niggahīta Y vocal anterior, el
            // prefijo queda desnudo — de «paripucchiṃ» queda «paripucch».
            v.add(pre + x + "ṃ");
        }
        const ult = pre[pre.length - 1];
        if (NASALES.includes(ult)) v.add(pre.slice(0, -1) + "ṃ");  // §31–§33
        if ("md".includes(ult)) v.add(pre.slice(0, -1) + "ṃ");     // §34
        if (pre.endsWith("abbh")) v.add(pre.slice(0, -4) + "abhi"); // §44
        if (pre.endsWith("ajjh")) v.add(pre.slice(0, -4) + "adhi"); // §45
        if (pre.endsWith("paṭi")) v.add(pre.slice(0, -4) + "pati"); // §48
        if (pre.endsWith("o") || pre.endsWith("u"))
            v.add(pre.slice(0, -1) + "ava");                        // §50, §79
        if ("yvmdntrlhg".includes(ult))
            v.add(pre.slice(0, -1));           // se le insertó una consonante (§35)
        // Devolver la niggahīta: §31 la volvió nasal de serie, §32/§33 «ñ»,
        // el «vā» de §31 «l». Sin esto, de `taññeva` nunca salía `taṃ + eva`.
        if ("ṅñṇnml".includes(ult)) v.add(pre.slice(0, -1) + "ṃ");
        if (pre.endsWith("cc") || pre.endsWith("c"))
            v.add(pre.replace(/c+$/u, "") + "ti");  // §19: «ti» quedó en «c»
        // §51: transposición de r, h, n — los dos saltos que el banco
        // atestigua. Sin esto, de «anabhineyya» nunca se propone «na».
        for (let i = 0; i < pre.length; i++) {
            if (!"rhn".includes(pre[i])) continue;
            for (const salto of [1, 2]) {
                for (const j of [i - salto, i + salto]) {
                    if (j >= 0 && j < pre.length) {
                        const L = pre.split("");
                        [L[i], L[j]] = [L[j], L[i]];
                        v.add(L.join(""));
                    }
                }
            }
        }
    }
    v.delete("");
    return v;
}

function vecinosB(suf) {
    const v = new Set([suf]);
    if (suf) {
        for (const x of VOCALES) {
            v.add(x + suf);                    // se le elidió la vocal inicial (§13)
            v.add(x + suf.slice(1));           // se le sustituyó o alargó (§14, §15…)
        }
        if (suf.length > 1 && suf[0] === suf[1])
            v.add(suf.slice(1));               // se duplicó (§28, §29)
        if (suf.length > 1
            && ["kk", "cc", "ṭṭ", "tt", "pp"].includes(suf.slice(0, 2)))
            v.add(suf.slice(1));
        if ("yvmdntrlhg".includes(suf[0]))
            v.add(suf.slice(1));               // se insertó una consonante (§35)
        if (suf[0] === "ḷ")
            v.add(suf.slice(1));               // la «ḷ» de la nota 9, tras «cha»
        // §32 y §33 dejan una «ñ» al principio de la voz que sigue.
        if (suf[0] === "ñ") {
            v.add(suf.slice(1));               // §32: la «ñ» duplicada
            v.add("y" + suf.slice(1));         // §33: la «y» que se volvió «ñ»
        }
        if (suf.startsWith("riva"))
            v.add("eva" + suf.slice(4));       // §22: la «e» de «eva» dio «ri»
        for (const [dig, simple] of Object.entries(OP.SEGUNDA_CUARTA)) {
            if (suf.startsWith(simple + dig))
                v.add(suf.slice(simple.length));   // §29
        }
    }
    v.delete("");
    return v;
}

// ── El filtro de cadenas, del lado nuestro ──────────────────────────────

function sinAnotacion(paso) {
    // El texto de un paso, sin la anotación final entre paréntesis. Se
    // reconoce CUALQUIER paréntesis final (el contrato del encargo).
    return (paso || "").replace(/\s*\([^)]*\)\s*$/u, "").trim();
}

function pasoQueNoHaceNada(pasos) {
    // ¿Hay un paso cuyo texto es idéntico al anterior? Un aforismo que no
    // cambia una letra no se aplicó; se descarta la cadena entera.
    let prev = null;
    for (const paso of pasos) {
        const texto = sinAnotacion(paso);
        if (prev !== null && texto === prev) return true;
        prev = texto;
    }
    return false;
}

function letraAjena(n, pasos) {
    // ¿El paso de §17/§18/§21 sustituye por la letra que NO es la suya?
    const marca = `(§${n})`;
    const letra = OP.LETRA_SUST[n];
    for (const paso of pasos) {
        if (!paso.trimEnd().endsWith(marca)) continue;
        const solas = sinAnotacion(paso).split(/\s+/u)
            .filter(x => x === "y" || x === "v");
        if (solas.length && !(solas.length === 1 && solas[0] === letra))
            return true;
    }
    return false;
}

function bienFormada(pasos) {
    // El último segmento de cada paso tiene que poder pronunciarse: una voz
    // sin vocal no es una voz. (Red de seguridad; hoy no descarta nada.)
    for (const paso of pasos) {
        const texto = sinAnotacion(paso);
        for (const alternativa of texto.split(",")) {
            const fichas = alternativa.split(/\s+/u).filter(x => x);
            if (fichas.length) {
                const ult = fichas[fichas.length - 1];
                if (![...ult].some(c => VOCALES.includes(c))) return false;
            }
        }
    }
    return true;
}

// ── Aplicar la operación §n ─────────────────────────────────────────────
// Para las nueve que el Venerable implementó, el verificador es el suyo;
// para las demás, el nuestro, con su enunciado.

const NUEVE_DEL_VENERABLE = new Set([12, 13, 15, 16, 17, 18, 21, 28, 35]);

function esVocalSust(n) {
    return typeof n === "number" && Object.prototype.hasOwnProperty
        .call(OP.VOCAL_SUST, n);
}

function forward(n, a, b, F) {
    if (esVocalSust(n) && !OP.licenciaSustitucion(a, b, n)) {
        // §17 sustituye la «e» final, §18 la «o» y la «u», §21 la «i» y la
        // «ī»: no se le pregunta al derivador por un aforismo que no cubre
        // el par.
        return null;
    }
    let pasos;
    if (typeof n === "number" && NUEVE_DEL_VENERABLE.has(n)) {
        pasos = D.derivar(n, a + " " + b, F);
    } else {
        const f = OP.TODAS.get(n);
        pasos = f ? f(a, b, F) : null;
    }
    if (!pasos) return null;
    if (pasoQueNoHaceNada(pasos)) return null;
    if (esVocalSust(n) && letraAjena(n, pasos)) return null;
    return pasos;
}

const ORDEN = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 25, 26, 27, 28, 29,
    31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 44, 45, 48, 49, 50, 51,
    79, 183, 269, "17+25", "18+25", "21+25", "35+26", "38+12", "38+13",
    "31vā", "35nota9"];

// ── Filtros de voces ────────────────────────────────────────────────────

function soloVocal(t) {
    // Una sola vocal no puede ser la voz que sigue: los upasagga son
    // prefijos, van delante, nunca detrás.
    const c = cotejo(t);
    return c.length === 1 && VOCALES.includes(c);
}

function esDesinencia(t) {
    // Una vocal más niggahīta no es una voz: es una desinencia (`aṃ`, `iṃ`,
    // `uṃ`). `taṃ`, `yaṃ`, `kiṃ` sí son voces: tienen consonante.
    const c = cotejo(t);
    return c.length === 2 && VOCALES.includes(c[0]) && c[1] === "ṃ";
}

function compuestoDelLexico(t, piezas = 3) {
    // La voz no está en el léxico, pero es la suma de voces que sí están.
    // No analiza el compuesto —fuera del encargo—: sólo comprueba que lo es.
    const lex = _cache.lexico;
    t = cotejo(t);
    if (t.length < 6) return null;
    if (lex.has(t)) return [t];
    if (piezas < 2) return null;
    for (let i = 3; i < t.length - 2; i++) {
        const a = t.slice(0, i), b = t.slice(i);
        if (!lex.has(a)) continue;
        if (lex.has(b)) return [a, b];
        const resto = compuestoDelLexico(b, piezas - 1);
        if (resto) return [a].concat(resto);
    }
    return null;
}

// ── Comparadores: el orden del Python, exactamente ──────────────────────
// Python ordena por (dpd, nipāta, str(sutta), componentes). Las cadenas se
// comparan por puntos de código; para el pāḷi (BMP) el `<` de JS coincide.

function cmpStr(a, b) { return a < b ? -1 : a > b ? 1 : 0; }

function cmpLista(a, b) {
    const n = Math.min(a.length, b.length);
    for (let i = 0; i < n; i++) {
        const c = cmpStr(a[i], b[i]);
        if (c) return c;
    }
    return a.length - b.length;
}

// ── Proponer: de la forma a los componentes ─────────────────────────────

function proponer(F, unaVoz = true, compuestos = false) {
    // Todas las lecturas que recomponen exactamente F. Ordenadas, sin
    // repetir. `unaVoz` distingue los dos casos del punto D10: dentro de una
    // palabra, una cadena cuya yuxtaposición ya da la forma es un rodeo.
    const lex = _cache.lexico;
    const vistas = new Set();
    const out = [];
    for (let i = 1; i < F.length; i++) {
        const admisible = compuestos
            ? (x => lex.has(cotejo(x)) || Boolean(compuestoDelLexico(x)))
            : (x => lex.has(cotejo(x)));
        const A = [...vecinosA(F.slice(0, i))]
            .filter(x => admisible(x) && !esDesinencia(x));
        if (!A.length) continue;
        const B = [...vecinosB(F.slice(i))]
            .filter(x => lex.has(cotejo(x)) && !soloVocal(x)
                && !esDesinencia(x));
        for (const a of A) {
            for (const b of B) {
                for (const n of ORDEN) {
                    const k = a + " " + b + " " + String(n)
                        + typeof n;
                    if (vistas.has(k)) continue;
                    vistas.add(k);
                    if (unaVoz && cotejo(a) + cotejo(b) === F) {
                        // Elidir algo y volver a ponerlo no es explicar
                        // nada: sin diferencia con la yuxtaposición no hay
                        // operación que citar.
                        continue;
                    }
                    const pasos = forward(n, a, b, F);
                    if (!pasos || !bienFormada(pasos)) continue;
                    out.push({ componentes: [a, b], sutta: n, pasos,
                               reconstruida: F, recompone: true,
                               procedencia: "propuesta automática" });
                }
            }
        }
    }
    // En solo-canon `descomposicion()` calla siempre: el primer criterio del
    // orden (coincidir con el DPD) no mueve nada, y queda el de nipāta.
    const dpd = new Set();
    for (const d of descomposicion(F)) {
        for (let i = 0; i < d.length - 1; i++)
            dpd.add(cotejo(d[i]) + "+" + cotejo(d[i + 1]));
        dpd.add(cotejo(d[0]) + "+" + cotejo(d.slice(1).join("")));
    }
    const nip = _cache.nipata;
    const claveDpd = x => dpd.has(x.componentes.map(cotejo).join("+")) ? 0 : 1;
    const claveNip = x =>
        nip.has(cotejo(x.componentes[x.componentes.length - 1])) ? 0 : 1;
    out.sort((x, y) =>
        (claveDpd(x) - claveDpd(y))
        || (claveNip(x) - claveNip(y))
        || cmpStr(String(x.sutta), String(y.sutta))
        || cmpLista(x.componentes, y.componentes));
    for (const x of out)
        if (dpd.has(x.componentes.map(cotejo).join("+"))) x.dpd = true;
    return out;
}

function proponerEnFrase(escrita) {
    // Una frase tiene varias junturas y el sandhi ocurre en una. Se prueba
    // cada juntura por separado y se deja el resto de la frase intacto.
    const fichas = escrita.split(/\s+/u).filter(x => x);
    if (fichas.length < 2) return [];
    const out = [];
    for (let i = 0; i < fichas.length - 1; i++) {
        for (const l of proponer(cotejo(fichas[i] + fichas[i + 1]), false)) {
            const copia = Object.assign({}, l);
            copia.contexto = { antes: fichas.slice(0, i),
                               despues: fichas.slice(i + 2) };
            copia.reconstruida = fichas.slice(0, i)
                .concat([fichas[i] + fichas[i + 1]])
                .concat(fichas.slice(i + 2)).join(" ");
            out.push(copia);
        }
    }
    return out;
}

function proponerEnMarca(voz) {
    // Cuando el escriba dijo dónde está la juntura —apóstrofo o guion—, se
    // propone ahí y no a ciegas. El guion puede marcar un compuesto sin
    // operación; el apóstrofo marca una elisión.
    const partes = voz.split(new RegExp("[" + MARCAS + "]", "u"));
    if (partes.length !== 2 || !partes.every(x => x)) return [];
    const [aPre, bSuf] = partes;
    const F = cotejo(voz);
    const lex = _cache.lexico;
    if (voz.includes("-") && lex.has(cotejo(aPre)) && lex.has(cotejo(bSuf))
        && cotejo(aPre) + cotejo(bSuf) === F)
        return [{ yuxtaposicion_declarada: [aPre, bSuf] }];
    const vistas = new Set();
    const out = [];
    const A = [...vecinosA(cotejo(aPre))]
        .filter(x => lex.has(cotejo(x)) && !esDesinencia(x));
    const B = [...vecinosB(cotejo(bSuf))]
        .filter(x => lex.has(cotejo(x)) && !soloVocal(x) && !esDesinencia(x));
    for (const a of A) {
        for (const b of B) {
            for (const n of ORDEN) {
                const k = a + " " + b + " " + String(n) + typeof n;
                if (vistas.has(k)) continue;
                vistas.add(k);
                const pasos = forward(n, a, b, F);
                if (!pasos || !bienFormada(pasos)) continue;
                out.push({ componentes: [a, b], sutta: n, pasos,
                           reconstruida: F, recompone: true,
                           procedencia: "propuesta automática",
                           corte_declarado: true });
            }
        }
    }
    const nip = _cache.nipata;
    const claveNip = x =>
        nip.has(cotejo(x.componentes[x.componentes.length - 1])) ? 0 : 1;
    out.sort((x, y) =>
        (claveNip(x) - claveNip(y))
        || cmpStr(String(x.sutta), String(y.sutta))
        || cmpLista(x.componentes, y.componentes));
    return out;
}

function yuxtaposicion(F) {
    // Los cortes que parten la forma en dos voces reales SIN ninguna
    // operación: un compuesto, fuera del encargo.
    const lex = _cache.lexico;
    const out = [];
    for (let i = 2; i < F.length - 1; i++) {
        const a = F.slice(0, i), b = F.slice(i);
        if (lex.has(cotejo(a)) && lex.has(cotejo(b))
            && !esDesinencia(a) && !esDesinencia(b) && !soloVocal(b))
            out.push([a, b]);
    }
    return out;
}

module.exports = {
    iniciar, cotejo, esPalabra, partirComponentes,
    proponer, proponerEnFrase, proponerEnMarca, yuxtaposicion,
    compuestoDelLexico, forward, ORDEN,
    _cache,
};
