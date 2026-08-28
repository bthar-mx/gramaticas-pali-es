// El arnés de la etapa 2 (briefing sesión 30 §6): reproduce en Node la
// medida contra el corpus del proyecto `Sandhi` —Therīgāthā y su
// comentario— con el léxico FRAGMENTADO de carga bajo demanda, y compara
// contra el Python forma por forma. La puerta: 551 de 698 y 6.048 de 7.178,
// con la misma categoría y las mismas lecturas que la referencia.
//
//     node nuestro/js/arnes_corpus.js               # los versos
//     node nuestro/js/arnes_corpus.js --comentario  # el aṭṭhakathā
//
// La referencia la vuelca el Python — la fuente de verdad permanente—:
//
//     python3 nuestro/volcar_referencia_corpus.py --solo-canon [--comentario]
//
// El corte de `Sandhi` no es la verdad: es otro proponente, y su partición
// se hizo CON el DPD — la referencia está teñida, briefing 30 §2—. Lo que
// se mide acá no es el mundo sino la identidad JS ↔ Python.

"use strict";

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const RAIZ = path.resolve(__dirname, "..", "..");
const motor = require("./motor");
const { cotejo } = require("./normalizar");
const { lexicoFragmentado } = require("./lexico_fragmentado");

const VOCALES = "aāiīuūeo";

function leerJson(...partes) {
    return JSON.parse(fs.readFileSync(path.join(RAIZ, ...partes), "utf-8"));
}

// La huella del banco, calculada sobre el archivo que se acaba de leer —el
// motor no lee archivos, así que la calcula el cargador y la pasa—.
function huellaBanco() {
    const cuerpo = fs.readFileSync(
        path.join(RAIZ, "recursos", "sandhi", "reglas.json"));
    const calculada = crypto.createHash("sha256").update(cuerpo).digest("hex");
    const d = { "reglas.json": calculada, coincide: null };
    const banco = path.join(RAIZ, "banco.sha256");
    if (fs.existsSync(banco)) {
        for (const l of fs.readFileSync(banco, "utf-8").split("\n")) {
            if (l.trim() && !l.startsWith("#") && l.includes("reglas.json")) {
                d.guardada = l.split("  ")[0];
                d.coincide = d.guardada === calculada;
                break;
            }
        }
    }
    return d;
}

// ── El bucle de medir_contra_corpus.py, portado ─────────────────────────

function normalizarPiezas(p) {
    if (!p || !p.length) return [];
    if (Array.isArray(p[0])) return p.map(c => c.map(cotejo));
    return [p.map(cotejo)];
}

function sinDesinencia(t) {
    t = t.replace(/ṃ+$/u, "");
    return t.replace(/[āīū]$/u, x => ({ "ā": "a", "ī": "i", "ū": "u" }[x]));
}

function esYuxtaposicion(forma, cortes) {
    if (forma.trim().split(/\s+/u).filter(x => x).length > 1) return false;
    const f = cotejo(forma);
    for (const c of cortes) {
        if (c.length < 2) continue;
        const a = c[0], b = c[1];
        const sinVocal = b && VOCALES.includes(b[b.length - 1])
            ? b.slice(0, -1) : b;
        if (f.startsWith(a + sinVocal)) return true;
        if (sinDesinencia(f) === sinDesinencia(c.join(""))) return true;
    }
    return false;
}

function nuestras(r) {
    return (r.lecturas || []).map(
        L => (L.componentes || []).map(cotejo));
}

function medir(archivoCorpus, referencia) {
    const d = leerJson("recursos", "corpus", archivoCorpus);
    const filas = d.palabras.filter(w => w.categoria === "sandhi");

    const cuenta = { acuerdo: 0, corte: 0, desacuerdo: 0, silencio: 0,
                     fuera_de_alcance: 0 };
    const salida = [];
    for (const w of filas) {
        const suyas = normalizarPiezas(w.piezas);
        const fila = { forma: w.forma };
        if (esYuxtaposicion(w.forma, suyas)) {
            fila.categoria = "fuera_de_alcance";
            cuenta.fuera_de_alcance++;
            salida.push(fila);
            continue;
        }
        let r;
        try {
            r = motor.solucionar(w.forma);
        } catch (e) {
            fila.categoria = "desacuerdo";
            fila.error = `${e.name}: ${e.message}`;
            cuenta.desacuerdo++;
            salida.push(fila);
            continue;
        }
        const mias = nuestras(r);
        fila.mias = mias;
        if (!mias.length) {
            fila.categoria = "silencio";
            cuenta.silencio++;
            salida.push(fila);
            continue;
        }
        const clavesSuyas = new Set(suyas.map(s => s.join("\u0000")));
        let hallada = null;
        for (let i = 0; i < mias.length; i++) {
            if (clavesSuyas.has(mias[i].join("\u0000"))) {
                hallada = i + 1;
                break;
            }
        }
        if (hallada) {
            fila.categoria = "acuerdo";
            fila.rango = hallada;
            cuenta.acuerdo++;
        } else {
            const primeras = new Set(
                mias.filter(x => x.length).map(x => x[0]));
            fila.categoria = suyas.some(s => s.length && primeras.has(s[0]))
                ? "corte" : "desacuerdo";
            cuenta[fila.categoria]++;
        }
        salida.push(fila);
    }

    const enAlcance = filas.length - cuenta.fuera_de_alcance;
    const coincide = cuenta.acuerdo + cuenta.corte;
    console.log(`\n  ${archivoCorpus} · ${filas.length} formas «sandhi»`);
    console.log(`  medibles: ${enAlcance} · coincide el corte: ${coincide}`
        + `  (referencia Python: ${referencia.coincide} de `
        + `${referencia.en_alcance})`);

    // ── Comparación forma por forma contra el Python ────────────────────
    let identicas = 0;
    const difieren = [];
    for (let i = 0; i < salida.length; i++) {
        const js = salida[i], py = referencia.filas[i];
        if (!py || js.forma !== py.forma) {
            difieren.push({ i, forma: js.forma,
                            motivo: "desalineada con la referencia" });
            continue;
        }
        const igualCat = js.categoria === py.categoria;
        const igualMias = JSON.stringify(js.mias || null)
            === JSON.stringify(py.mias || null);
        const igualRango = (js.rango || null) === (py.rango || null);
        if (igualCat && igualMias && igualRango) { identicas++; continue; }
        difieren.push({
            i, forma: js.forma,
            motivo: !igualCat
                ? `categoría: js=${js.categoria} py=${py.categoria}`
                : !igualMias ? "difieren las lecturas"
                             : `rango: js=${js.rango} py=${py.rango}`,
            js, py,
        });
    }
    console.log(`  formas idénticas al Python: ${identicas} de `
        + `${salida.length}`);
    if (difieren.length) {
        console.log(`\n  DIFIEREN (${difieren.length}):`);
        for (const x of difieren.slice(0, 8)) {
            console.log(`   · [${x.i}] ${x.forma} — ${x.motivo}`);
            if (x.js && x.js.mias && x.py && x.py.mias) {
                console.log(`       js: ${JSON.stringify(x.js.mias).slice(0, 160)}`);
                console.log(`       py: ${JSON.stringify(x.py.mias).slice(0, 160)}`);
            }
        }
    }
    return {
        pasa: coincide === referencia.coincide
            && enAlcance === referencia.en_alcance
            && difieren.length === 0,
        coincide, enAlcance,
    };
}

function main() {
    const comentario = process.argv.includes("--comentario");
    const todo = !process.argv.slice(2).length
        || process.argv.includes("--todo");

    const reglas = leerJson("recursos", "sandhi", "reglas.json");
    const tablas = leerJson("recursos", "sandhi",
                            "tablas-nandisena-secuencias.json");
    const listas = leerJson("recursos", "sandhi", "listas-cerradas.json");
    const casos = leerJson("recursos", "solucionador",
                           "casos-reportados.json");
    const lexico = lexicoFragmentado(
        path.join(RAIZ, "site", "recursos", "solucionador", "lexico"));

    motor.iniciar({ lexico, reglas, tablas, listas, casos,
                huella: huellaBanco() });

    console.log("ARNÉS JS · corpus en modo solo-canon, léxico fragmentado"
        + ` (${lexico.total} formas, carga bajo demanda)`);

    const resultados = [];
    if (todo || !comentario)
        resultados.push(medir("therigatha_sandhi.json",
            leerJson("nuestro", "js",
                     "referencia-corpus-versos-solo-canon.json")));
    if (todo || comentario)
        resultados.push(medir("therigatha_atthakatha_sandhi.json",
            leerJson("nuestro", "js",
                     "referencia-corpus-comentario-solo-canon.json")));

    console.log(`\n  fragmentos cargados bajo demanda: `
        + `${lexico.fragmentosCargados().sort().join(" ")}`);
    const pasa = resultados.every(r => r.pasa);
    console.log(`\n  PUERTA DE LA ETAPA 2: ${pasa ? "PASA" : "NO PASA"}`
        + "  (se exige 551/698 y 6048/7178, forma por forma idéntico"
        + " al Python)");
    return pasa ? 0 : 1;
}

process.exit(main());
