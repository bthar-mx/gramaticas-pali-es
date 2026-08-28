// El léxico del canon partido por letra inicial, con carga bajo demanda
// (etapa 2, briefing sesión 30 §6). Los fragmentos los escribe
// `herramientas/generar_lexico_solucionador.py` en
// `recursos/solucionador/lexico/`; la tabla letra → archivo está en
// `indice.json` — el nombre no se deduce, se lee.
//
// Esta versión es la de Node (fs síncrono). En el navegador (etapa 4) la
// carga es un fetch con la misma tabla; el contrato del motor no cambia:
// un objeto con `.has()` sobre formas ya en forma de cotejo.

"use strict";

const fs = require("fs");
const path = require("path");

function lexicoFragmentado(dir) {
    const indice = JSON.parse(
        fs.readFileSync(path.join(dir, "indice.json"), "utf-8"));
    const cargados = new Map();          // letra → Set de formas
    return {
        has(q) {
            if (!q) return false;
            const info = indice.fragmentos[q[0]];
            if (!info) return false;
            let s = cargados.get(q[0]);
            if (!s) {
                s = new Set(JSON.parse(fs.readFileSync(
                    path.join(dir, info.archivo), "utf-8")));
                cargados.set(q[0], s);
            }
            return s.has(q);
        },
        total: indice.total,
        fragmentosCargados: () => [...cargados.keys()],
    };
}

module.exports = { lexicoFragmentado };
