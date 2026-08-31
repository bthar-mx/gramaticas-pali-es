/* Arnés de la identidad de Access — worker/index.js.
   Pedido de Angel, 2026-08-31, al poner login en el modo revisión.

       node worker/arnes_identidad.mjs

   POR QUÉ EXISTE. Esto es código de autenticación, y el código de
   autenticación que no se prueba parece bien hasta el día que importa. El
   principio 1 del proyecto —verificar, no afirmar— vale aquí más que en
   ningún otro sitio: un «if» mal puesto no falla, deja pasar.

   Lo que se comprueba, y cada caso es un modo distinto de colarse:

     1. token bueno                    → 200 y queda el correo
     2. sin token                      → 401
     3. firma de OTRA clave            → 401   (el falsificador evidente)
     4. aud de otra aplicación         → 401   (el descuido clásico: un token
                                                legítimo del mismo equipo pero
                                                emitido para otra aplicación)
     5. caducado                       → 401
     6. cuerpo manipulado, firma vieja → 401   (cambiarse el correo a mano)
     7. algoritmo «none»               → 401
     8. Access sin configurar          → 200 y correo null (la cola sigue
                                                abierta como antes, a propósito)
     9. la galleta CF_Authorization    → 200   (el navegador no manda cabecera)

   Nada de esto toca la red: el JWKS se sirve de mentira sustituyendo
   globalThis.fetch, y las claves se generan en el momento. */

import worker from "./index.js";

const EQUIPO = "equipo-de-prueba.cloudflareaccess.com";
const AUD = "aud-de-esta-aplicacion";

const b64url = (b) => Buffer.from(b).toString("base64")
  .replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");

async function parDeClaves() {
  return crypto.subtle.generateKey(
    { name: "RSASSA-PKCS1-v1_5", modulusLength: 2048,
      publicExponent: new Uint8Array([1, 0, 1]), hash: "SHA-256" },
    true, ["sign", "verify"],
  );
}

async function jwk(par, kid) {
  const j = await crypto.subtle.exportKey("jwk", par.publicKey);
  return { kid, kty: j.kty, n: j.n, e: j.e, alg: "RS256", use: "sig" };
}

async function firmar(par, kid, cuerpo) {
  const cab = b64url(JSON.stringify({ alg: "RS256", kid }));
  const cue = b64url(JSON.stringify(cuerpo));
  const firma = await crypto.subtle.sign(
    "RSASSA-PKCS1-v1_5", par.privateKey,
    new TextEncoder().encode(cab + "." + cue));
  return cab + "." + cue + "." + b64url(new Uint8Array(firma));
}

/* Un KV de mentira: sólo lo que el worker usa de él. */
function kvFalso() {
  const m = new Map();
  return {
    datos: m,
    async put(k, v, o) { m.set(k, { v, meta: o && o.metadata }); },
    async get(k) { return m.has(k) ? m.get(k).v : null; },
    async list() {
      return { list_complete: true,
               keys: [...m.entries()].map(([name, x]) => ({ name, metadata: x.meta })) };
    },
    async delete(k) { m.delete(k); },
  };
}

const MD = "# Veredictos\n\nVEREDICTO: taṃ + ca\n";

async function enviar(env, tok, comoGalleta = false) {
  const h = { "Content-Type": "text/plain" };
  if (tok && comoGalleta) h["Cookie"] = "otra=1; CF_Authorization=" + tok;
  else if (tok) h["Cf-Access-Jwt-Assertion"] = tok;
  return worker.fetch(
    new Request("https://ejemplo.org/api/veredictos", {
      method: "POST", headers: h, body: MD }),
    env);
}

let fallos = 0, hechas = 0;
function comprobar(nombre, cond, detalle) {
  hechas += 1;
  if (cond) { console.log("  ok   " + nombre); }
  else { fallos += 1; console.log("  MAL  " + nombre + (detalle ? " — " + detalle : "")); }
}

async function main() {
  const buenas = await parDeClaves();
  const otras = await parDeClaves();
  const jwks = { keys: [await jwk(buenas, "kid-bueno")] };

  // El JWKS, servido de mentira. Si el worker pidiera otra cosa, salta.
  globalThis.fetch = async (u) => {
    if (String(u) === "https://" + EQUIPO + "/cdn-cgi/access/certs") {
      return new Response(JSON.stringify(jwks),
        { headers: { "Content-Type": "application/json" } });
    }
    throw new Error("el worker pidió una URL inesperada: " + u);
  };

  const dentro = Math.floor(Date.now() / 1000) + 3600;
  const antes = Math.floor(Date.now() / 1000) - 3600;
  const conAcceso = () => ({ VEREDICTOS: kvFalso(), ACCESO_EQUIPO: EQUIPO,
                             ACCESO_AUD: AUD, CLAVE_VEREDICTOS: "x" });

  console.log("Arnés de la identidad de Access\n");

  // 1 — el camino bueno
  {
    const env = conAcceso();
    const t = await firmar(buenas, "kid-bueno",
      { aud: [AUD], email: "revisor@ejemplo.org", exp: dentro });
    const r = await enviar(env, t);
    const j = r.status === 200 ? await r.json() : null;
    comprobar("token bueno → 200", r.status === 200, "salió " + r.status);
    comprobar("y devuelve el correo",
      j && j.correo === "revisor@ejemplo.org", JSON.stringify(j));
    const guardado = [...env.VEREDICTOS.datos.values()][0];
    comprobar("y lo guarda en el metadato del KV",
      guardado && guardado.meta && guardado.meta.correo === "revisor@ejemplo.org",
      JSON.stringify(guardado && guardado.meta));
  }

  // 2 — sin token
  comprobar("sin token → 401", (await enviar(conAcceso(), null)).status === 401);

  // 3 — firmado con otra clave, mismo kid
  {
    const t = await firmar(otras, "kid-bueno",
      { aud: [AUD], email: "intruso@ejemplo.org", exp: dentro });
    comprobar("firma de otra clave → 401",
      (await enviar(conAcceso(), t)).status === 401);
  }

  // 4 — aud de otra aplicación del MISMO equipo
  {
    const t = await firmar(buenas, "kid-bueno",
      { aud: ["otra-aplicacion"], email: "revisor@ejemplo.org", exp: dentro });
    comprobar("aud distinto → 401",
      (await enviar(conAcceso(), t)).status === 401);
  }

  // 5 — caducado
  {
    const t = await firmar(buenas, "kid-bueno",
      { aud: [AUD], email: "revisor@ejemplo.org", exp: antes });
    comprobar("caducado → 401", (await enviar(conAcceso(), t)).status === 401);
  }

  // 6 — cuerpo cambiado a mano, firma legítima de otro cuerpo
  {
    const t = await firmar(buenas, "kid-bueno",
      { aud: [AUD], email: "estudiante@ejemplo.org", exp: dentro });
    const p = t.split(".");
    p[1] = b64url(JSON.stringify(
      { aud: [AUD], email: "angel@ejemplo.org", exp: dentro }));
    comprobar("cuerpo manipulado → 401",
      (await enviar(conAcceso(), p.join("."))).status === 401);
  }

  // 7 — el truco de «alg: none»
  {
    const cab = b64url(JSON.stringify({ alg: "none", kid: "kid-bueno" }));
    const cue = b64url(JSON.stringify(
      { aud: [AUD], email: "intruso@ejemplo.org", exp: dentro }));
    comprobar("alg «none» → 401",
      (await enviar(conAcceso(), cab + "." + cue + ".")).status === 401);
  }

  // 8 — Access sin configurar: la cola sigue abierta, pero marcada
  {
    const env = { VEREDICTOS: kvFalso() };
    const r = await enviar(env, null);
    const guardado = [...env.VEREDICTOS.datos.values()][0];
    comprobar("sin configurar → 200 (no rompe la cola de hoy)", r.status === 200,
      "salió " + r.status);
    comprobar("y la entrada queda con correo null",
      guardado && guardado.meta && guardado.meta.correo === null,
      JSON.stringify(guardado && guardado.meta));
  }

  // 9 — por galleta, que es como llega de un navegador
  {
    const t = await firmar(buenas, "kid-bueno",
      { aud: [AUD], email: "revisor@ejemplo.org", exp: dentro });
    comprobar("galleta CF_Authorization → 200",
      (await enviar(conAcceso(), t, true)).status === 200);
  }

  console.log("\n" + (hechas - fallos) + "/" + hechas + " comprobaciones");
  if (fallos) { console.log("HAY FALLOS: " + fallos); process.exit(1); }
  console.log("La identidad se sostiene.");
}

main().catch((e) => { console.error(e); process.exit(1); });
