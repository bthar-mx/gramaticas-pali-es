// El arnés de la etapa 4 (briefing sesión 30 §6): LA PÁGINA PUBLICADA da
// secuencias byte-idénticas al Python en las 266 formas del banco.
//
//     node nuestro/js/arnes_pagina.js
//
// No prueba una copia del motor: extrae el <script id="motor"> de
// site/recursos/solucionador/index.html —los mismos bytes que ejecuta el
// navegador—, lo evalúa en Node con un fetch que lee los fragmentos
// publicados, y compara `solucionar()` forma por forma contra la referencia
// del Python:
//
//     python3 nuestro/volcar_referencia_pagina.py

"use strict";

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const RAIZ = path.resolve(__dirname, "..", "..");
const PAGINA = path.join(RAIZ, "site", "recursos", "solucionador",
                         "index.html");
const BASE = path.join(RAIZ, "site", "recursos", "solucionador");

async function main() {
    const html = fs.readFileSync(PAGINA, "utf-8");
    const m = /<script id="motor">([\s\S]*?)<\/script>/.exec(html);
    if (!m) {
        console.log("La página no tiene <script id=\"motor\">.");
        return 1;
    }
    const contexto = {
        __fetchJsonNode: async (url) => JSON.parse(
            fs.readFileSync(path.join(BASE, url), "utf-8")),
        console,
    };
    contexto.globalThis = contexto;
    vm.createContext(contexto);
    vm.runInContext(m[1], contexto, { filename: "pagina#motor" });
    const S = contexto.SOLUCIONADOR;

    const referencia = JSON.parse(fs.readFileSync(
        path.join(RAIZ, "nuestro", "js",
                  "referencia-pagina-solo-canon.json"), "utf-8"));

    // Un solo preparar con todas las formas: el cierre de letras del
    // cargador cubre todo lo que el motor pueda consultar.
    await S.preparar(referencia.filas.map(x => x.f).join(" "));

    let identicas = 0;
    const difieren = [];
    for (const py of referencia.filas) {
        let js;
        try {
            const r = S.solucionar(py.f);
            js = {
                estado: r.estado !== undefined ? r.estado : null,
                senal: r.senal !== undefined ? r.senal : null,
                lecturas: (r.lecturas || []).map(l => ({
                    componentes: l.componentes,
                    pasos: l.pasos,
                    procedencia: l.procedencia,
                    referencia: l.referencia !== undefined
                        ? l.referencia : null,
                })),
            };
        } catch (e) {
            difieren.push({ f: py.f, motivo: "ERROR " + e.message });
            continue;
        }
        const igual = JSON.stringify(js) === JSON.stringify({
            estado: py.estado, senal: py.senal, lecturas: py.lecturas });
        if (igual) { identicas++; continue; }
        difieren.push({ f: py.f, js, py });
    }

    console.log("ARNÉS JS · la página publicada contra el Python");
    console.log(`  formas del banco: ${referencia.filas.length}`
        + ` · byte-idénticas: ${identicas}`);
    if (S.lexico.faltantes)
        console.log(`  AVISO: ${S.lexico.faltantes} consultas a fragmentos`
            + " no precargados — el cierre de letras falló");
    if (difieren.length) {
        console.log(`\n  DIFIEREN (${difieren.length}):`);
        for (const d of difieren.slice(0, 6)) {
            console.log(`   · ${d.f} ${d.motivo || ""}`);
            if (d.js) {
                console.log(`       js: ${JSON.stringify(d.js).slice(0, 220)}`);
                console.log(`       py: ${JSON.stringify(
                    { estado: d.py.estado, senal: d.py.senal,
                      lecturas: d.py.lecturas }).slice(0, 220)}`);
            }
        }
    }
    const pasa = difieren.length === 0 && !S.lexico.faltantes;
    console.log(`\n  PUERTA DE LA ETAPA 4: ${pasa ? "PASA" : "NO PASA"}`
        + "  (las 266 formas byte-idénticas al Python, desde la página"
        + " publicada)");
    return pasa ? 0 : 1;
}

main().then(c => process.exit(c));
