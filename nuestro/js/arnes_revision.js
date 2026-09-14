// El MODO REVISIÓN de la página, comprobado sobre la página YA GENERADA.
//
//     node nuestro/js/arnes_revision.js
//
// Los otros cinco arneses miden el motor. Éste mide la parte de la página que
// recoge lo que el revisor decide, y que no medía nadie — que es justamente
// donde han aparecido los dos últimos defectos:
//
//   · 2.1 · una voz registrada a mano Y presente en el pasaje no recibía
//     tarjeta por ningún lado, de modo que no había dónde escribir su
//     secuencia ni su nota. El filtro preguntaba «¿está en el pasaje?»
//     cuando la pregunta era «¿ya tiene tarjeta?».
//   · 2.4 · el .md no decía de qué pasaje salía cada veredicto, y la página
//     lo tenía delante.
//
// No hay navegador aquí, de modo que se extraen las funciones del HTML
// generado y se ejercitan con dobles. Es menos que una prueba de navegador y
// muchísimo más que nada: las dos veces habría cazado el fallo.

"use strict";

const fs = require("fs");
const path = require("path");

const RAIZ = path.resolve(__dirname, "..", "..");
const PAGINA = path.join(RAIZ, "site", "recursos", "solucionador", "index.html");

const html = fs.readFileSync(PAGINA, "utf-8");

// La función tal como quedó en la página publicada, no como está en la
// plantilla: lo que se mide es lo que se sirve.
function extraer(nombre) {
    const i = html.indexOf("function " + nombre + "(");
    if (i < 0) throw new Error("no encuentro «" + nombre + "» en la página");
    let k = html.indexOf("{", i), d = 0;
    for (let j = k; j < html.length; j++) {
        const c = html[j];
        if (c === "{") d++;
        else if (c === "}") { d--; if (d === 0) { k = j + 1; break; } }
    }
    return html.slice(i, k);
}

let fallos = 0, hechas = 0;
function ok(titulo, cierto) {
    hechas++;
    if (!cierto) fallos++;
    console.log((cierto ? "  ok    " : "  FALLA ") + titulo);
}

function montar(REV) {
    const src = ["revPasaje", "revRegistradas", "revMD"].map(extraer).join("\n");
    return new Function("REV", "DATA", "tr", "esc", "tarjeta", "resolver",
        src + "; return { revPasaje, revRegistradas, revMD };")(
        REV, { version: "prueba" },
        k => ({ t_reg: "tip", reg_lbl: "registradas a mano" }[k] || k),
        s => String(s),
        v => `[TARJETA ${v}]`,
        () => ({ lecturas: [] }));
}

console.log("ARNÉS JS · el modo revisión de la página");

// ── La tarjeta de lo registrado a mano (2.1) ────────────────────────────
{
    const REV = { v: new Map(), pasajes: new Map(), obs: "" };
    const f = montar(REV);
    const poner = (voz, d) => REV.v.set(voz, Object.assign(
        { senal: null, primera: "", fecha: "2026-01-01" }, d));

    console.log("\n  la voz registrada a mano recibe tarjeta");
    poner("māhu", { t: "otra", comp: "mā + ahu", falta: true });
    ok("presente en el pasaje y sin señal: la recibe",
        f.revRegistradas(new Set()).includes("[TARJETA māhu]"));
    ok("si el motor ya le dio tarjeta arriba, no se repite",
        !f.revRegistradas(new Set(["māhu"])).includes("[TARJETA"));

    REV.v.clear();
    poner("tenupasaṅkami", { t: "primera", primera: "tena + upasaṅkami" });
    ok("la adjudicada sobre la tarjeta del motor no sale en este bloque",
        !f.revRegistradas(new Set()).includes("[TARJETA"));
}

// ── El pasaje viaja con el veredicto (2.4) ──────────────────────────────
{
    const REV = { v: new Map(), pasajes: new Map(), obs: "" };
    const f = montar(REV);

    console.log("\n  el pasaje viaja con el veredicto");
    const p1 = f.revPasaje("Tassattho. Kiṃ nu taṃ kāraṇaṃ…");
    const p2 = f.revPasaje("Tattha jātassa maraṇaṃ hotī ti…");
    ok("dos textos distintos, dos números", p1 === 1 && p2 === 2);
    ok("el mismo texto no se numera dos veces",
        f.revPasaje("Tassattho. Kiṃ nu taṃ kāraṇaṃ…") === 1);
    ok("el texto vacío no crea pasaje",
        f.revPasaje("   ") === null && REV.pasajes.size === 2);

    REV.v.set("tassattho", { senal: null, primera: "ta + assattho",
        comp: "tassa + attho", t: "otra", falta: true, pasaje: p1,
        esc: "tassa attho\ntass a attho (§10)" });
    REV.v.set("cettha", { senal: "segura", primera: "ca + ettha",
        t: "primera", pasaje: p2 });
    const md = f.revMD();

    ok("el .md lleva la sección de pasajes",
        md.includes("## Pasajes analizados"));
    // Puesta después del primer veredicto, sus líneas sangradas se leerían
    // como pasos de la escalera del último: el orden es la comprobación.
    ok("va ANTES del primer veredicto",
        md.indexOf("## Pasajes analizados") < md.indexOf("## 1."));
    ok("cada veredicto cita el suyo",
        /## 1\. tassattho.*pasaje 1/.test(md) && /## 2\. cettha.*pasaje 2/.test(md));
    ok("el texto del pasaje viaja entero",
        md.includes("Tattha jātassa maraṇaṃ hotī ti…"));
    ok("el pasaje que no usa ningún veredicto no se exporta",
        (f.revPasaje("huérfano"), !f.revMD().includes("huérfano")));

    console.log("\n  lo que el incorporador necesita seguir leyendo");
    ok("la cabecera de cada veredicto", /^## \d+\.\s+(\S+)\s+·/m.test(md));
    ok("la procedencia, que la 2.1 añadió",
        md.includes("registrada a mano por el revisor") &&
        md.includes("revisado en la página"));
    ok("la escalera, sangrada", md.includes("ESCALERA:") &&
        md.includes("    tass a attho (§10)"));
}

console.log("\n  PUERTA DEL MODO REVISIÓN: " + (fallos ? "NO PASA" : "PASA") +
            (fallos
                ? "  (" + fallos + " de " + hechas + " comprobaciones fallan)"
                : "  (" + hechas + " comprobaciones, todas pasan)"));
process.exit(fallos ? 1 : 0);
