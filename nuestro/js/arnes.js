// El arnés de la etapa 1 (briefing sesión 30 §6): reproduce en Node la medida
// del banco en modo solo-canon y compara contra el Python, SECUENCIA POR
// SECUENCIA. La puerta: 218 de 251 medibles, con las mismas lecturas, los
// mismos pasos y el mismo orden que la referencia.
//
//     node nuestro/js/arnes.js
//
// La referencia la vuelca el Python — la fuente de verdad permanente—:
//
//     python3 nuestro/volcar_referencia.py --solo-canon
//
// Si este arnés no da IDÉNTICO, el defecto es del porte, no del Python.

"use strict";

const fs = require("fs");
const path = require("path");

const RAIZ = path.resolve(__dirname, "..", "..");
const motor = require("./motor");
const { cotejo } = require("./normalizar");

function leerJson(...partes) {
    return JSON.parse(fs.readFileSync(path.join(RAIZ, ...partes), "utf-8"));
}

function main() {
    const reglas = leerJson("recursos", "sandhi", "reglas.json");
    const tablas = leerJson("recursos", "sandhi",
                            "tablas-nandisena-secuencias.json");
    const listas = leerJson("recursos", "sandhi", "listas-cerradas.json");
    const corpus = leerJson("recursos", "corpus", "corpus-formas.json");
    const referencia = leerJson("nuestro", "js",
                                "referencia-banco-solo-canon.json");

    motor.iniciar({
        formasCanon: Object.keys(corpus.formas || {}),
        reglas, tablas, listas,
    });

    const PAKATI = new Set([23, 24, 30]);
    const filas = [];
    for (const x of reglas.ce) {
        const comp = motor.partirComponentes(x.comp);
        const escrita = x.f.replace(/’/g, "'").replace(/'/g, "");
        let lect, esperados;
        if (comp.length > 2) {
            lect = motor.proponerEnFrase(escrita);
            const e = new Set();
            for (let j = 0; j < comp.length - 1; j++)
                e.add(cotejo(comp[j] + comp[j + 1]));
            esperados = [...e].sort();
        } else {
            lect = escrita.split(/\s+/u).filter(t => t).length > 1
                ? motor.proponerEnFrase(escrita)
                : motor.proponer(cotejo(x.f));
            esperados = [cotejo(comp.join(""))];
        }
        const acierta = lect.some(
            l => esperados.includes(cotejo(l.componentes.join(""))));
        filas.push({
            f: x.f, kac: x.kac, pakati: PAKATI.has(x.kac), acierta,
            lecturas: lect.map(l => ({ componentes: l.componentes,
                                       sutta: l.sutta, pasos: l.pasos })),
        });
    }

    const medibles = filas.filter(f => !f.pakati);
    const ok = medibles.filter(f => f.acierta).length;
    console.log(`ARNÉS JS · banco en modo solo-canon`);
    console.log(`  acierta: ${ok} de ${medibles.length} medibles`
        + `  (referencia Python: ${referencia.acierta} de ${referencia.medibles})`);

    // ── Comparación secuencia por secuencia contra el Python ────────────
    let identicas = 0;
    const difieren = [];
    for (let i = 0; i < filas.length; i++) {
        const js = filas[i], py = referencia.filas[i];
        if (js.f !== py.f) {
            difieren.push({ i, f: js.f, motivo: "desalineado con la referencia" });
            continue;
        }
        const igualLect = JSON.stringify(js.lecturas)
            === JSON.stringify(py.lecturas);
        if (js.acierta === py.acierta && igualLect) { identicas++; continue; }
        difieren.push({
            i, f: js.f,
            motivo: js.acierta !== py.acierta
                ? `acierta: js=${js.acierta} py=${py.acierta}`
                : `lecturas: js=${js.lecturas.length} py=${py.lecturas.length}`,
            js: js.lecturas, py: py.lecturas,
        });
    }
    console.log(`  formas idénticas al Python, secuencia por secuencia: `
        + `${identicas} de ${filas.length}`);
    if (difieren.length) {
        console.log(`\n  DIFIEREN (${difieren.length}):`);
        for (const d of difieren.slice(0, 10)) {
            console.log(`   · [${d.i}] ${d.f} — ${d.motivo}`);
            if (d.js) {
                const pj = new Set(d.py.map(l => JSON.stringify(l)));
                const jj = new Set(d.js.map(l => JSON.stringify(l)));
                for (const l of d.js.slice(0, 30))
                    if (!pj.has(JSON.stringify(l)))
                        console.log(`       sólo js: ${JSON.stringify(l).slice(0, 200)}`);
                for (const l of d.py.slice(0, 30))
                    if (!jj.has(JSON.stringify(l)))
                        console.log(`       sólo py: ${JSON.stringify(l).slice(0, 200)}`);
            }
        }
    }

    const puerta = ok === referencia.acierta
        && medibles.length === referencia.medibles
        && difieren.length === 0;
    console.log(`\n  PUERTA DE LA ETAPA 1: ${puerta ? "PASA" : "NO PASA"}`
        + `  (se exige ${referencia.acierta}/${referencia.medibles} e identidad`
        + ` de secuencias)`);
    return puerta ? 0 : 1;
}

process.exit(main());
