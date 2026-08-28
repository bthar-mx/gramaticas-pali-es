// Porte fiel de `nuestro/normalizar.py` (etapa 1 del porte a JS, sesión 31).
// `cotejo()`: la forma canónica para COMPARAR dos voces pāḷi. Nunca para
// guardar ni para mostrar. Pasos, en este orden (CLAUDE.md §4):
//   1. NFC  2. saca apóstrofos, guiones, comillas y espacios  3. minúscula
//   4. ṁ (U+1E41) → ṃ (U+1E43)  — después de minúscula, para que Ṁ llegue.
// El Python queda como referencia permanente; todo cambio acá se mide contra
// él con `nuestro/js/arnes.js`.

"use strict";

const APOSTROFOS = "’'";
const GUIONES = "-‐‑‒–—−";
// Comillas de cita de la edición (2026-08-28, instrucción del Venerable):
// «oghamatarī”ti» es «oghamatarīti». Igual que en el Python.
const COMILLAS = "“”„\"«»‹›‘";
// El guion se escapa: sin la barra, dentro de la clase formaría un RANGO
// U+0027–U+2010 que se traga todas las letras ASCII.
const BORRAR = new RegExp("[" + (APOSTROFOS + GUIONES + COMILLAS)
    .replace(/[.*+?^${}()|[\]\\-]/g, "\\$&") + "]", "gu");

function cotejo(t) {
    t = t.normalize("NFC");
    t = t.replace(BORRAR, "");
    t = t.replace(/\s+/gu, "");
    t = t.toLowerCase();
    return t.replace(/ṁ/gu, "ṃ");   // ṁ → ṃ
}

function iguales(a, b) { return cotejo(a) === cotejo(b); }

module.exports = { cotejo, iguales };
