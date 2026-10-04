/* Las fuentes de fondo de /api/preguntar (2026-10-04).

   Junto a la fila, el modelo puede recibir textos de otras obras sobre el
   mismo sutta: las clases de U Sīlānanda sobre la Rūpasiddhi, la propia
   Rūpasiddhi, la Nyāsappadīpikā y el Nyāsa. NO están en el repositorio —que
   es público— ni en el sitio: viven en el KV privado FUENTES, con una clave
   por obra y § de Kaccāyana:

       silananda-rup/2   rupasiddhi/2   nyasappadipika/2   nyasa/2

   Cada valor es el Markdown del paquete tal cual, y su primera línea es la
   cabecera «fuente; edición/origen; ubicación; aviso; derechos». Los sube
   herramientas/subir_fuentes.sh desde el Mac del IEBH.

   Reglas que no se saltan:
   - Los paquetes van SÓLO a la API. Nunca al navegador: lo único que sale de
     aquí hacia la página es la línea «Fuentes consultadas», con los nombres.
   - El interruptor es PREGUNTAR_FUENTES («on»/«off»; por omisión, «off»).
     Con «off», o sin el enlace FUENTES, la petición es la de siempre, byte a
     byte.
   - Tope duro para el bloque entero (TOPE_TOKENS). Si no cabe, se cae primero
     el Nyāsa, luego la Nyāsappadīpikā, luego la Rūpasiddhi; si ni la primera
     cabe sola, se recorta por el final y se dice. */

/* En orden de prioridad: la primera es la que más pesa y la última que se
   cae. «nombre» y «name» son lo que dice la línea «Fuentes consultadas»:
   fijos, y no sacados de la cabecera del paquete, para que en la línea no
   aparezcan rótulos («fuente: …»), ediciones ni números de clase. */
export const OBRAS = [
  { dir: "silananda-rup", nombre: "U Sīlānanda, clases de Rūpasiddhi",
    name: "U Sīlānanda, classes on the Rūpasiddhi" },
  { dir: "rupasiddhi", nombre: "Padarūpasiddhi", name: "Padarūpasiddhi" },
  { dir: "nyasappadipika", nombre: "Nyāsappadīpikā", name: "Nyāsappadīpikā" },
  { dir: "nyasa", nombre: "Nyāsa", name: "Nyāsa" },
];

export const TOPE_TOKENS = 12000;

/* Sin tokenizador en el worker: se estima por lo alto. Pāḷi con diacríticos
   y español salen a unos 3,5 caracteres por token; con 3 el tope se queda
   corto antes que largo. */
export const estimarTokens = (s) => Math.ceil(String(s).length / 3);

export function fuentesActivas(env) {
  return String(env.PREGUNTAR_FUENTES || "off").trim().toLowerCase() === "on" && !!env.FUENTES;
}

export function clavesDe(n) {
  return OBRAS.map((o) => o.dir + "/" + n);
}

/* Las cuatro a la vez; la que falta (o falla) se salta sin más. */
export async function leerFuentes(env, n) {
  const claves = clavesDe(n);
  const valores = await Promise.all(claves.map((k) =>
    env.FUENTES.get(k).catch((e) => {
      console.log("preguntar: FUENTES no dio " + k + ": " + e.message);
      return null;
    })));
  return claves.map((clave, i) => ({ clave, obra: OBRAS[i], texto: valores[i] }))
    .filter((p) => typeof p.texto === "string" && p.texto.trim());
}

const MARCA_RECORTE = "\n[… paquete recortado por el tope de extensión …]";

/* Deja los paquetes dentro del tope: quita de la cola (la menor prioridad)
   mientras no quepan; si queda uno solo y aún no cabe, lo recorta. Devuelve
   {paquetes, descartadas, recortada}. */
export function aplicarTope(paquetes, tope = TOPE_TOKENS) {
  const p = paquetes.slice();
  const descartadas = [];
  const total = () => p.reduce((s, x) => s + estimarTokens(envolver(x)), 0);
  while (p.length > 1 && total() > tope) descartadas.push(p.pop().clave);
  let recortada = null;
  if (p.length === 1 && total() > tope) {
    const sobra = estimarTokens(envolver({ ...p[0], texto: "" }) + MARCA_RECORTE);
    const caben = Math.max(0, (tope - sobra) * 3);
    p[0] = { ...p[0], texto: p[0].texto.slice(0, caben) + MARCA_RECORTE };
    recortada = p[0].clave;
  }
  return { paquetes: p, descartadas, recortada };
}

/* Un paquete no puede cerrar la etiqueta que lo contiene. */
const limpio = (s) => String(s).replace(/<\/?fuentes?\b/gi, (m) => m.replace("<", "‹"));

function envolver(p) {
  return '<fuente clave="' + p.clave + '">\n' + limpio(p.texto).trim() + "\n</fuente>";
}

export function bloqueDeFuentes(paquetes) {
  return "<fuentes>\n" + paquetes.map(envolver).join("\n") + "\n</fuentes>";
}

/* La línea que el worker añade a la respuesta: la escribe él, no el modelo. */
export function lineaFuentes(paquetes, lang) {
  if (!paquetes.length) return "";
  return (lang === "en" ? "Sources consulted: " : "Fuentes consultadas: ")
    + paquetes.map((p) => (lang === "en" ? p.obra.name : p.obra.nombre)).join("; ") + ".";
}
