// Porte fiel de `herramientas/derivar_secuencias.py` — EL VERIFICADOR del
// Venerable. Quien propone (motor.js) y quien verifica son distintos, a
// propósito; este archivo no se «mejora»: se transcribe. La regla de oro: una
// secuencia sólo se emite si, al aplicarla, se llega exactamente a la forma
// atestiguada. Si no coincide, no se emite nada.
//
// OJO: el `cotejo()` de este archivo NO es el de normalizar.js. El del
// verificador sólo hace NFC, saca ’ ' - y espacios; no baja a minúscula ni
// lleva ṁ a ṃ. Así está en el Python y así se porta.

"use strict";

const VOCALES = "aāiīuūeo";
// LARGA mapea e→e y o→o a propósito: es el original del Venerable. El paso
// calcado que eso produce lo descarta el motor (`pasoQueNoHaceNada`), no éste.
const LARGA = { a: "ā", i: "ī", u: "ū", e: "e", o: "o" };

function nfc(t) { return t.normalize("NFC"); }

function cotejo(t) {
    t = nfc(t).replace(/’/g, "").replace(/'/g, "").replace(/-/g, "");
    return t.replace(/\s+/gu, "");
}

function dosVoces(comp) {
    const partes = comp.trim().split(/\s*\+\s*|\s+/u).filter(x => x);
    return partes.length === 2 ? partes : null;
}

function cierre(pasos, unido, atestiguada) {
    pasos.push(unido + " (§11)");
    if (cotejo(unido) !== cotejo(atestiguada)) return null;
    if (nfc(atestiguada).trim() !== nfc(unido).trim())
        pasos.push(atestiguada + " (EM)");
    return pasos;
}

// ── Un derivador por aforismo ───────────────────────────────────────────

function dElideAnterior(a, b, atestiguada, n) {
    // §12: se separa la vocal final de la primera voz y se elide.
    if (!a || !VOCALES.includes(a[a.length - 1])) return null;
    const raiz = a.slice(0, -1), v = a[a.length - 1];
    if (!raiz) return null;
    return cierre([`${a} ${b}`,
                   `${raiz} ${v} ${b} (§10)`,
                   `${raiz} ${b} (§${n})`],
                  raiz + b, atestiguada);
}

function dElideSiguiente(a, b, atestiguada, n) {
    // §13: se elide la vocal inicial de la segunda voz.
    if (!a || !VOCALES.includes(a[a.length - 1]) || !b || !VOCALES.includes(b[0]))
        return null;
    const raiz = a.slice(0, -1), v = a[a.length - 1];
    if (!raiz || b.length < 2) return null;
    return cierre([`${a} ${b}`,
                   `${raiz} ${v} ${b} (§10)`,
                   `${raiz} ${v} ${b.slice(1)} (§${n})`],
                  raiz + v + b.slice(1), atestiguada);
}

function dElideYAlarga(a, b, atestiguada, n) {
    // §15: elidida la anterior, la siguiente se alarga.
    if (!a || !VOCALES.includes(a[a.length - 1]) || !b || !VOCALES.includes(b[0]))
        return null;
    const raiz = a.slice(0, -1), v = a[a.length - 1];
    if (!raiz || !(b[0] in LARGA)) return null;
    const largo = LARGA[b[0]] + b.slice(1);
    return cierre([`${a} ${b}`,
                   `${raiz} ${v} ${b} (§10)`,
                   `${raiz} ${b} (§12)`,
                   `${raiz} ${largo} (§${n})`],
                  raiz + largo, atestiguada);
}

function dAlargaAnterior(a, b, atestiguada, n) {
    // §16: elidida la siguiente, la anterior se alarga.
    if (!a || !VOCALES.includes(a[a.length - 1]) || !b || !VOCALES.includes(b[0]))
        return null;
    const raiz = a.slice(0, -1), v = a[a.length - 1];
    if (!raiz || !(v in LARGA) || b.length < 2) return null;
    return cierre([`${a} ${b}`,
                   `${raiz} ${v} ${b} (§10)`,
                   `${raiz} ${v} ${b.slice(1)} (§13)`,
                   `${raiz} ${LARGA[v]} ${b.slice(1)} (§${n})`],
                  raiz + LARGA[v] + b.slice(1), atestiguada);
}

function dSustituyeAnterior(a, b, atestiguada, n, destino) {
    // §17 (e→y), §18 (o,u→v), §21 (i,ī→y): cambia la vocal final.
    if (!a || !VOCALES.includes(a[a.length - 1])) return null;
    const raiz = a.slice(0, -1), v = a[a.length - 1];
    if (!raiz) return null;
    return cierre([`${a} ${b}`,
                   `${raiz} ${v} ${b} (§10)`,
                   `${raiz} ${destino} ${b} (§${n})`],
                  raiz + destino + b, atestiguada);
}

function dDuplica(a, b, atestiguada, n) {
    // §28: se duplica la consonante inicial de la segunda voz.
    if (!b || VOCALES.includes(b[0])) return null;
    const doble = b[0] + b;
    return cierre([`${a} ${b}`,
                   `${a} ${doble} (§${n})`],
                  a + doble, atestiguada);
}

function dInserta(a, b, atestiguada, n, letra) {
    // §35: se inserta una consonante entre las dos voces.
    return cierre([`${a} ${b}`,
                   `${a} ${letra} ${b} (§${n})`],
                  a + letra + b, atestiguada);
}

function derivar(kac, comp, atestiguada) {
    const par = dosVoces(comp);
    if (!par) return null;
    const [a, b] = par;
    const intentos = [];
    if (kac === 12) intentos.push(() => dElideAnterior(a, b, atestiguada, 12));
    else if (kac === 13) intentos.push(() => dElideSiguiente(a, b, atestiguada, 13));
    else if (kac === 15) intentos.push(() => dElideYAlarga(a, b, atestiguada, 15));
    else if (kac === 16) intentos.push(() => dAlargaAnterior(a, b, atestiguada, 16));
    else if (kac === 17 || kac === 18 || kac === 21) {
        for (const destino of ["y", "v"])
            intentos.push(() => dSustituyeAnterior(a, b, atestiguada, kac, destino));
    } else if (kac === 28) intentos.push(() => dDuplica(a, b, atestiguada, 28));
    else if (kac === 35) {
        for (const letra of "yvmdntrlhg")
            intentos.push(() => dInserta(a, b, atestiguada, 35, letra));
    }
    for (const f of intentos) {
        const r = f();
        if (r) return r;
    }
    return null;
}

module.exports = { derivar };
