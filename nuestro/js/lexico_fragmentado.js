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
    const cargados = new Map();          // letra → Map forma → cuenta
    function fragmento(q) {
        if (!q) return null;
        const info = indice.fragmentos[q[0]];
        if (!info) return null;
        let m = cargados.get(q[0]);
        if (!m) {
            // Cada fragmento es una lista de [forma, cuenta]: la cuenta es
            // el árbitro de la señal «posible» (etapa 3) y viaja con el
            // léxico para no pedir un segundo archivo.
            m = new Map(JSON.parse(fs.readFileSync(
                path.join(dir, info.archivo), "utf-8")));
            cargados.set(q[0], m);
        }
        return m;
    }
    return {
        has(q) {
            const m = fragmento(q);
            return m ? m.has(q) : false;
        },
        frecuencia(q) {
            const m = fragmento(q);
            return (m && m.get(q)) || 0;
        },
        total: indice.total,
        fragmentosCargados: () => [...cargados.keys()],
    };
}

module.exports = { lexicoFragmentado };
