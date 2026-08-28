// Los casos adjudicados por lectores, comprobados contra el motor.
//
//     node nuestro/js/arnes_casos.js
//
// Decisión del Venerable (briefing 30 §3.5): cada fallo reportado, un caso
// de prueba permanente. El archivo es
// recursos/solucionador/casos-reportados.json; cada caso lleva su fuente.
// Lo que se exige:
//   sandhi=true  → señal «segura» Y la lectura adjudicada primera
//   sandhi=false → la señal calla (null)

"use strict";

const fs = require("fs");
const path = require("path");

const RAIZ = path.resolve(__dirname, "..", "..");
const motor = require("./motor");
const { cotejo } = require("./normalizar");
const { lexicoFragmentado } = require("./lexico_fragmentado");

function leerJson(...partes) {
    return JSON.parse(fs.readFileSync(path.join(RAIZ, ...partes), "utf-8"));
}

function main() {
    const casos = leerJson("recursos", "solucionador",
                           "casos-reportados.json");
    motor.iniciar({
        lexico: lexicoFragmentado(
            path.join(RAIZ, "site", "recursos", "solucionador", "lexico")),
        reglas: leerJson("recursos", "sandhi", "reglas.json"),
        tablas: leerJson("recursos", "sandhi",
                         "tablas-nandisena-secuencias.json"),
        listas: leerJson("recursos", "sandhi", "listas-cerradas.json"),
        casos,
    });

    console.log("ARNÉS JS · casos adjudicados por lectores");
    let fallos = 0;
    for (const c of casos.casos) {
        const r = motor.solucionar(c.forma);
        const problemas = [];
        if (c.sandhi) {
            if (r.senal !== "segura")
                problemas.push(`señal=${r.senal}, se esperaba «segura»`);
            const objetivo = motor.partirComponentes(c.componentes || "")
                .map(cotejo).join(" + ");
            const primera = r.lecturas.length
                ? r.lecturas[0].componentes.map(cotejo).join(" + ") : "—";
            if (primera !== objetivo)
                problemas.push(`primera lectura «${primera}», se esperaba `
                    + `«${objetivo}»`);
        } else if (r.senal) {
            problemas.push(`señal=${r.senal}, se esperaba silencio`);
        }
        const ok = !problemas.length;
        if (!ok) fallos++;
        console.log(`  ${ok ? "·" : "✗"} ${c.forma}  (${c.fuente})`
            + (ok ? "" : "\n      " + problemas.join("\n      ")));
    }
    console.log(`\n  CASOS: ${casos.casos.length - fallos} de `
        + `${casos.casos.length} ${fallos ? "— HAY FALLOS" : "— todos pasan"}`);
    return fallos ? 1 : 0;
}

process.exit(main());
