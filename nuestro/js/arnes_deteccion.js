// El arnés de la etapa 3 (briefing sesión 30 §6): la señal de detección en
// modo solo-canon, palabra por palabra idéntica al Python. Recorre todas
// las formas únicas de los dos corpus de `Sandhi` y compara señal y motivo
// contra la referencia.
//
//     node nuestro/js/arnes_deteccion.js
//
// La referencia la vuelca el Python — la fuente de verdad permanente—:
//
//     python3 nuestro/volcar_referencia_senal.py
//
// Los números de la señal (qué marca, con qué precisión y qué recall) no se
// miden acá: los mide `python3 nuestro/medir_deteccion_canon.py`, y están
// escritos en `_ascender_senal` del Python. Este arnés mide una sola cosa:
// que el JS diga EXACTAMENTE lo que dice el Python.

"use strict";

const fs = require("fs");
const path = require("path");

const RAIZ = path.resolve(__dirname, "..", "..");
const motor = require("./motor");
const { lexicoFragmentado } = require("./lexico_fragmentado");

function leerJson(...partes) {
    return JSON.parse(fs.readFileSync(path.join(RAIZ, ...partes), "utf-8"));
}

function main() {
    const reglas = leerJson("recursos", "sandhi", "reglas.json");
    const tablas = leerJson("recursos", "sandhi",
                            "tablas-nandisena-secuencias.json");
    const listas = leerJson("recursos", "sandhi", "listas-cerradas.json");
    const lexico = lexicoFragmentado(
        path.join(RAIZ, "recursos", "solucionador", "lexico"));
    const referencia = leerJson("nuestro", "js",
                                "referencia-senal-solo-canon.json");

    motor.iniciar({ lexico, reglas, tablas, listas });

    console.log("ARNÉS JS · señal de detección en modo solo-canon");
    const cuenta = { segura: 0, posible: 0, nada: 0 };
    let identicas = 0;
    const difieren = [];
    for (const fila of referencia.filas) {
        let s = null, m = null;
        try {
            const r = motor.solucionar(fila.forma);
            s = r.senal || null;
            m = r.senal_motivo !== undefined ? r.senal_motivo : null;
        } catch (e) {
            s = null;
            m = `ERROR ${e.message}`;
        }
        cuenta[s === "segura" ? "segura" : s === "posible" ? "posible"
               : "nada"]++;
        const ps = fila.senal || null;
        const pm = fila.motivo !== undefined ? fila.motivo : null;
        if (s === ps && m === pm) { identicas++; continue; }
        difieren.push({ forma: fila.forma, js: [s, m], py: [ps, pm] });
    }
    console.log(`  formas únicas: ${referencia.filas.length}`
        + ` · segura ${cuenta.segura} (py ${referencia.segura})`
        + ` · posible ${cuenta.posible} (py ${referencia.posible})`);
    console.log(`  idénticas al Python, señal y motivo: ${identicas} de `
        + `${referencia.filas.length}`);
    if (difieren.length) {
        console.log(`\n  DIFIEREN (${difieren.length}):`);
        for (const d of difieren.slice(0, 10)) {
            console.log(`   · ${d.forma}`);
            console.log(`       js: ${JSON.stringify(d.js)}`);
            console.log(`       py: ${JSON.stringify(d.py)}`);
        }
    }
    const pasa = difieren.length === 0
        && cuenta.segura === referencia.segura
        && cuenta.posible === referencia.posible;
    console.log(`\n  PUERTA DE LA ETAPA 3 (paridad): ${pasa ? "PASA" : "NO PASA"}`
        + "  (señal y motivo idénticos al Python en todas las formas)");
    return pasa ? 0 : 1;
}

process.exit(main());
