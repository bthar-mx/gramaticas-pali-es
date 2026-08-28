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
const _cache = { lexico: null, nipata: new Set(), lexicoBanco: new Set(),
                 banco: new Map(), canon: new Set(), huella: null };

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
function iniciar({ formasCanon, lexico, reglas, tablas, listas, huella }) {
    // El léxico base: o una lista de formas crudas (`formasCanon`, se cotejan
    // acá), o un objeto con `.has()` sobre formas YA cotejadas — el léxico
    // fragmentado con carga bajo demanda de la etapa 2.
    let base;
    if (formasCanon) {
        base = new Set();
        for (const f of formasCanon) base.add(cotejo(f));
    } else {
        base = lexico;
    }

    // El índice del banco: cotejo(f) → [{dato, archivo, clave}], en el orden
    // del Python — primero reglas.json, después las Tablas.
    _cache.banco = new Map();
    const meter = (f, entrada) => {
        const k = cotejo(f);
        if (!_cache.banco.has(k)) _cache.banco.set(k, []);
        _cache.banco.get(k).push(entrada);
    };
    reglas.ce.forEach((c, i) => meter(c.f, {
        dato: c, archivo: "recursos/sandhi/reglas.json",
        clave: `ce[${i}]` }));
    if (tablas) {
        tablas.filas.forEach((fila, i) => {
            (fila.secuencias || []).forEach((s, j) => {
                const f = s.em || s.forma_inicial;
                if (f) meter(f, {
                    dato: s,
                    archivo: "recursos/sandhi/tablas-nandisena-secuencias.json",
                    clave: `filas[${i}].secuencias[${j}]` });
            });
        });
    }

    // El segundo léxico: las voces que el propio banco atestigua como
    // componente y el corpus no trae. Hace circular la medida del banco (así
    // está dicho en el informe); el número que vale es el del corpus.
    const entradas = [];
    for (const lista of _cache.banco.values()) {
        for (const { dato } of lista) {
            entradas.push("s" in dato ? (dato.comp || "")
                                      : (dato.forma_inicial || ""));
        }
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
        [...extra].filter(q => !base.has(q)));
    const lb = _cache.lexicoBanco;
    _cache.lexico = { has: q => base.has(q) || lb.has(q) };

    // La capa `--canon` del modo DPD queda apagada y vacía: este porte es
    // solo-canon por decisión del Venerable (2026-08-28).
    _cache.canon = new Set();
    _cache.nipata = new Set((listas ? listas.nipata : []).map(cotejo));
    _cache.huella = huella === undefined ? null : huella;
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
                    const k = a + "\u0000" + b + "\u0000" + String(n)
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
                const k = a + "\u0000" + b + "\u0000" + String(n) + typeof n;
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

// ── Resolver: el porte de `solucionar()` ────────────────────────────────

// Pakati es la ausencia de operación: no hay corte que buscar.
const PAKATI = new Set([23, 24, 30]);
const N_OP = ORDEN.filter(n => typeof n === "number").length;

function nombreLexico() {
    // El porte es solo-canon: el DPD no interviene y no se nombra.
    return "del canon (Sexto Concilio)";
}

function huellaBanco() {
    // En Python se calcula acá, leyendo el archivo. El motor JS no lee
    // archivos: la huella la calcula quien carga (el arnés en Node, el
    // cargador en el navegador) y la pasa por `iniciar()`.
    return _cache.huella;
}

function juntarIguales(lecturas) {
    // Dos fuentes pueden traer la misma lectura: se muestra una vez, con las
    // dos procedencias. La clave incluye la cadena, no sólo los componentes
    // —si difieren en un paso o un aforismo son DOS lecturas y salen las
    // dos—. El paso «(EM)» no distingue: es la edición moderna, no un
    // aforismo. Los espacios tampoco.
    const fusion = new Map();
    for (const x of lecturas) {
        const pasosClave = x.pasos.map(
            p => p.split(/\s+/u).filter(t => t).join(" "));
        while (pasosClave.length
               && pasosClave[pasosClave.length - 1].trimEnd().endsWith("(EM)"))
            pasosClave.pop();
        const k = cotejo(x.componentes.join(""))
            + "\u0000" + pasosClave.join("\u0000");
        if (fusion.has(k)) {
            const y = fusion.get(k);
            if (x.origen) {
                if (!y.tambien_en) y.tambien_en = [];
                y.tambien_en.push(x.origen);
            }
            if (x.procedencia === "firmada") y.procedencia = "firmada";
        } else {
            fusion.set(k, x);
        }
    }
    return [...fusion.values()];
}

function compuestoAparente(c) {
    // La forma se parte, sin operación, en dos voces del léxico de las que
    // la segunda NO es una partícula: un compuesto junta dos nombres.
    const nip = _cache.nipata;
    for (const [, b] of yuxtaposicion(c)) {
        const cb = cotejo(b);
        if (!nip.has(cb) && cb.length >= 3) return true;
    }
    return false;
}

function senal(voz) {
    // ¿Hay motivo para SOSPECHAR sandhi en esta voz, antes de proponer nada?
    // Dos señales, las dos medidas. (La del DPD calla en solo-canon.)
    const c = cotejo(voz);
    if (descomposicion(voz).length)
        return ["segura",
                "el DPD publica su propia descomposición de esta voz"];
    if (c.endsWith("ti") && c.length > 3 && "āīū".includes(c[c.length - 3]))
        return ["segura", "cola de «iti»: vocal larga antes de «ti»"];
    if (!esPalabra(voz) && !compuestoAparente(c))
        return ["segura", "la voz no está en el léxico " + nombreLexico()
                + ", y tampoco se parte en dos voces del léxico sin operación"];
    return [null, ""];
}

function paresDelLexico(F) {
    // Los cortes que parten la voz en dos voces que el léxico reconoce.
    // Filtra exactamente igual que `proponer()`, y por la misma razón.
    const lex = _cache.lexico;
    const out = [];
    for (let i = 1; i < F.length; i++) {
        const A = [...vecinosA(F.slice(0, i))]
            .filter(x => lex.has(cotejo(x)) && !esDesinencia(x));
        if (!A.length) continue;
        for (const b of [...vecinosB(F.slice(i))]
            .filter(x => lex.has(cotejo(x)) && !soloVocal(x)
                && !esDesinencia(x))) {
            for (const a of A) out.push([a, b]);
        }
    }
    return out;
}

function porQueNo(voz, k) {
    // Por qué no se resolvió, dicho en el orden en que sirve. No se propone
    // una corrección de lo escrito: se informa qué se comprobó.
    const entera = esPalabra(voz);
    const pares = paresDelLexico(k);
    const d = {
        la_voz_esta_en_el_lexico: entera,
        cortes_en_dos_voces_del_lexico: pares.length,
        ejemplos_de_corte: pares.slice(0, 6).map(p => p.join(" + ")),
        aforismos_probados: ORDEN.filter(n => typeof n === "number"),
    };
    if (!entera && !pares.length)
        return ["la voz NO está en el léxico " + nombreLexico()
            + ", y ningún corte la parte en dos voces que el léxico "
            + "reconozca. O la forma está mal escrita, o alguna de sus "
            + "piezas falta en el léxico.", d];
    if (!entera)
        return ["la voz NO está en el léxico " + nombreLexico()
            + `. Hay ${pares.length} corte(s) en dos voces reales, pero `
            + `ninguna de las ${N_OP} operaciones enunciadas los lleva a `
            + "esta forma. Conviene revisar cómo está escrita antes de "
            + "buscarle una regla.", d];
    if (!pares.length)
        return ["la voz está en el léxico como palabra entera, pero ningún "
            + "corte la parte en dos voces que el léxico reconozca.", d];
    return [`hay ${pares.length} corte(s) en dos voces del léxico, pero `
        + `ninguna de las ${N_OP} operaciones enunciadas los lleva a esta `
        + "forma. Puede que la operación no esté enunciada en el capítulo 1, "
        + "o que el análisis necesite más de dos piezas.", d];
}

function solucionar(voz) {
    const k = cotejo(voz);
    const r = { escrita: voz, cotejo: k, estado: null, motivo: null,
                lecturas: [], banco: huellaBanco() };
    const fichas = voz.trim().split(/\s+/u).filter(t => t);
    if (fichas.length === 1) {
        const [s, m] = senal(voz);
        r.senal = s; r.senal_motivo = m;
    } else {
        r.senal = null; r.senal_motivo = "";
    }

    if (_cache.banco.has(k)) {
        for (const { dato, archivo, clave } of _cache.banco.get(k)) {
            let pasos, comp, primerPasoDe, proc, ref, sinOp;
            if ("s" in dato) {                                // reglas.json
                pasos = dato.s.slice();
                comp = partirComponentes(dato.comp || "");
                primerPasoDe = null;
                // La etiqueta tiene que ser cierta: «firmada» sólo con la
                // marca `verificada` del banco.
                proc = dato.verificada ? "firmada"
                                       : "del banco, sin comprobar";
                ref = dato.ref !== undefined ? dato.ref : null;
                sinOp = Boolean(dato.sin_cambio) || dato.sec === "pakati";
            } else {                                          // las Tablas
                pasos = (dato.pasos || []).map(p =>
                    p.texto + (p.citas && p.citas.length
                        ? "  (" + p.citas.join(", ") + ")" : ""));
                const inicial = dato.forma_inicial || "";
                // La forma de partida es el primer paso; las Tablas la
                // guardan aparte y arrancan en §10. Sin unificar, la misma
                // cadena salía dos veces.
                if (inicial && (!pasos.length
                    || pasos[0].trimEnd().endsWith(")")))
                    pasos = [inicial].concat(pasos);
                comp = partirComponentes(inicial);
                const p0 = (dato.pasos && dato.pasos.length
                    ? dato.pasos : [{}])[0];
                primerPasoDe = p0.forma_de_partida !== undefined
                    ? p0.forma_de_partida : null;
                proc = "firmada";
                ref = dato.referencia !== undefined ? dato.referencia : null;
                sinOp = !(dato.suttas_que_operan
                          && dato.suttas_que_operan.length);
            }
            // «Sin operación» sólo si ninguna opera: si la cadena cita un
            // aforismo que no es pakati ni andamiaje (§10, §11), opera.
            const citados = new Set();
            for (const m of pasos.join(" ").matchAll(/§\s*(\d+)/gu))
                citados.add(parseInt(m[1], 10));
            for (const excl of [...PAKATI, 10, 11]) citados.delete(excl);
            if (citados.size) sinOp = false;
            const ultimo = pasos.length
                ? sinAnotacion(pasos[pasos.length - 1]) : "";
            let recompone = Boolean(ultimo) && cotejo(ultimo) === k;
            if (recompone && proc === "del banco, sin comprobar")
                proc = "del banco, último paso comprobado";
            r.lecturas.push({
                componentes: comp, pasos,
                reconstruida: pasos.length ? pasos[pasos.length - 1] : voz,
                recompone, procedencia: proc,
                origen: { archivo, clave }, referencia: ref,
                sin_operacion: sinOp, primer_paso_de: primerPasoDe,
            });
        }
        r.lecturas = juntarIguales(r.lecturas);

        // Las filas de las Tablas que quedaron mal partidas: al paso pegado
        // le falta `forma_de_partida`, y una fila pakati legítima tiene un
        // solo paso — se exige más de uno.
        for (const x of r.lecturas) {
            if (!(((x.origen && x.origen.archivo) || "").includes("tablas")))
                continue;
            if (x.pasos.length > 1 && !x.primer_paso_de)
                x.fila_mal_partida = true;
        }
        r.banco_mal_partido = r.lecturas
            .filter(x => x.fila_mal_partida)
            .map(x => ({ componentes: x.componentes, pasos: x.pasos,
                         origen: x.origen }));
        r.lecturas = r.lecturas.filter(x => !x.fila_mal_partida);

        // Lo que no recompone no se publica; se anota aparte para que el
        // defecto del banco se vea en vez de taparse.
        r.banco_no_recompone = r.lecturas
            .filter(x => !x.recompone)
            .map(x => ({ componentes: x.componentes, pasos: x.pasos,
                         origen: x.origen }));
        r.lecturas = r.lecturas.filter(x => x.recompone);

        // Y lo que el motor encuentra además no se esconde: la firmada va
        // primera, con su procedencia; las demás detrás.
        const firmadas = r.lecturas.length;
        r.lecturas = juntarIguales(r.lecturas.concat(proponer(k)));
        r.lecturas.sort((x, y) => (x.origen ? 0 : 1) - (y.origen ? 0 : 1));
        r.del_banco = firmadas;

        if (!r.lecturas.length) {
            r.estado = "no_resuelto";
            r.motivo = "el banco trae esta forma pero su cadena no la "
                + "reproduce, y el motor no propone otra";
        } else if (r.lecturas.every(x => x.sin_operacion)) {
            r.estado = "sin_sandhi_por_regla";
        } else if (r.lecturas.length === 1
                   && r.lecturas[0].procedencia === "firmada") {
            r.estado = "firmada";
        } else {
            r.estado = "candidatos";
        }
        return r;
    }

    if (fichas.length > 1) {
        r.lecturas = proponerEnFrase(
            voz.replace(/’/g, "'").replace(/'/g, ""));
    } else {
        // La capa `--canon` del modo DPD no existe en este porte: es
        // solo-canon y `_cache.canon` queda vacío a propósito.
        const marcadas = [...MARCAS].some(m => voz.includes(m))
            ? proponerEnMarca(voz) : [];
        if (marcadas.length && "yuxtaposicion_declarada" in marcadas[0]) {
            r.estado = "fuera_del_alcance";
            r.entera = esPalabra(voz);
            const [a, b] = marcadas[0].yuxtaposicion_declarada;
            r.motivo = "la marca de la edición separa dos voces del léxico "
                + `sin ninguna operación —${a} + ${b}—: es un compuesto, `
                + "y los compuestos están fuera del encargo.";
            return r;
        }
        r.lecturas = marcadas.length ? marcadas : proponer(k);
        if (!r.lecturas.length) {
            // Segunda pasada, sólo si la primera no dijo nada: la voz
            // anterior puede ser un compuesto que el léxico no lista.
            r.lecturas = proponer(k, true, true);
        }
    }
    r.entera = esPalabra(voz);
    if (r.lecturas.length) {
        // «Resuelto» pide un segundo testigo: una sola lectura sin origen
        // ni testigo no es una resolución, es que no se encontró más.
        const una = r.lecturas.length === 1 ? r.lecturas[0] : null;
        r.estado = (una && (una.origen || una.dpd)) ? "resuelto"
                                                    : "candidatos";
        return r;
    }

    // Sin lecturas: los tres silencios, y no se dicen igual.
    const yux = fichas.length === 1 ? yuxtaposicion(k) : [];
    if (r.entera) {
        r.estado = "sin_sandhi";
        r.motivo = "la voz está entera en el léxico y ninguna de las "
            + `${N_OP} operaciones enunciadas encuentra un corte que la `
            + "explique: no hay nada que separar.";
        return r;
    }
    if (yux.length) {
        r.estado = "fuera_del_alcance";
        r.motivo = "la forma se parte en dos voces **sin ninguna operación** "
            + `—${yux[0].join(" + ")}—: es un compuesto, y los compuestos `
            + "están fuera del encargo.";
        r.diagnostico = {
            yuxtaposiciones: yux.slice(0, 6).map(x => x.join(" + ")) };
        return r;
    }
    r.estado = "no_resuelto";
    const [motivo, diagnostico] = porQueNo(voz, k);
    r.motivo = motivo;
    r.diagnostico = diagnostico;
    return r;
}

module.exports = {
    iniciar, cotejo, esPalabra, partirComponentes,
    proponer, proponerEnFrase, proponerEnMarca, yuxtaposicion,
    compuestoDelLexico, forward, ORDEN,
    solucionar, juntarIguales, senal, paresDelLexico, porQueNo,
    PAKATI,
    _cache,
};
