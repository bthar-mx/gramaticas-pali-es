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

   Y dos grupos más, que no son de identidad sino de las dos trampas en que
   ya se cayó el mismo día:

    10-15. EL REPARTO DE RUTAS. Access protege una ruta para TODOS los
           métodos, de modo que dejar (POST /api/veredictos, con identidad) y
           recoger (GET/DELETE /api/cola, con la clave) tienen que vivir
           separados. Si alguien los junta otra vez, quien recoge se queda
           fuera y no se nota hasta que hace falta la cola.
    16-19. ACCESO_EQUIPO ESCRITO DE LAS CUATRO MANERAS RAZONABLES. El panel
           da una URL y el secreto quiere un dominio; pegar «https://…» daba
           «https://https://…» y un fallo mudo. Ahora se admiten las cuatro.

   Nada de esto toca la red: el JWKS se sirve de mentira sustituyendo
   globalThis.fetch, y las claves se generan en el momento. */

import worker from "./index.js";

const EQUIPO = "equipo-de-prueba.cloudflareaccess.com";
const AUD = "aud-de-esta-aplicacion";
const AUD_HEX = "cb27b33c1f8526e9b99a2a2adb4d4a1f56163a72b54a5e6809299bbef1633c32";

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

  /* ---- El reparto de rutas (2026-08-31) ----
     Access protege una ruta entera, todos los métodos. Por eso dejar y
     recoger viven en rutas distintas, y eso hay que sujetarlo con pruebas:
     si alguien volviera a juntarlas, traer_veredictos.py se queda fuera otra
     vez y no se nota hasta que hace falta la cola. */
  {
    const env = conAcceso();
    const t = await firmar(buenas, "kid-bueno",
      { aud: [AUD], email: "revisor@ejemplo.org", exp: dentro });
    await enviar(env, t);   // deja una entrada

    const get = (p) => worker.fetch(
      new Request("https://ejemplo.org" + p), env);

    comprobar("GET /api/veredictos → 405 (dejar no es recoger)",
      (await get("/api/veredictos")).status === 405);

    const mala = await get("/api/cola?clave=noesa");
    comprobar("GET /api/cola con clave mala → 403", mala.status === 403);

    const buena = await get("/api/cola?clave=x");
    const j = buena.status === 200 ? await buena.json() : null;
    comprobar("GET /api/cola con la clave → 200", buena.status === 200,
      "salió " + buena.status);
    comprobar("y trae la entrada con su correo",
      j && j.veredictos.length === 1
        && j.veredictos[0].correo === "revisor@ejemplo.org",
      JSON.stringify(j));

    const del = await worker.fetch(new Request(
      "https://ejemplo.org/api/cola?clave=x&id=" + j.veredictos[0].id,
      { method: "DELETE" }), env);
    comprobar("DELETE /api/cola con la clave → 200 y vacía",
      del.status === 200 && env.VEREDICTOS.datos.size === 0);

    // /api/cola NO pide identidad: es la puerta de quien recoge, y quien
    // recoge no tiene navegador. Si un día pidiera sesión, esto lo canta.
    comprobar("/api/cola no exige sesión de Access",
      (await get("/api/cola?clave=x")).status === 200);
  }

  /* ---- ACCESO_EQUIPO escrito de las maneras razonables (2026-08-31) ----
     El panel da una URL; el secreto quiere un dominio. Pegar la URL entera
     era lo natural y costó una tarde de «no se pudo consultar Access». Que
     las cuatro formas funcionen se sujeta aquí. */
  for (const [comoSeEscribe, valor] of [
    ["dominio pelado", EQUIPO],
    ["con https://", "https://" + EQUIPO],
    ["con https:// y barra", "https://" + EQUIPO + "/"],
    ["con espacios alrededor", "  " + EQUIPO + "  "],
  ]) {

    const env = { VEREDICTOS: kvFalso(), ACCESO_EQUIPO: valor,
                  ACCESO_AUD: AUD, CLAVE_VEREDICTOS: "x" };
    const t = await firmar(buenas, "kid-bueno",
      { aud: [AUD], email: "revisor@ejemplo.org", exp: dentro });
    const r = await enviar(env, t);
    comprobar("ACCESO_EQUIPO " + comoSeEscribe + " → 200",
      r.status === 200, "salió " + r.status);
  }

  /* ---- Los dos secretos cambiados (2026-08-31) ----
     wrangler enmascara lo que se teclea, así que ponerlos al revés no se ve:
     el síntoma fue un 403 pidiendo las claves a un dominio que era el AUD.
     Se distinguen por la forma, y el worker tiene que decirlo con nombre. */
  {
    const env = { VEREDICTOS: kvFalso(), ACCESO_EQUIPO: AUD_HEX,
                  ACCESO_AUD: EQUIPO, CLAVE_VEREDICTOS: "x" };
    const t = await firmar(buenas, "kid-bueno",
      { aud: [AUD], email: "revisor@ejemplo.org", exp: dentro });
    const r = await enviar(env, t);
    const txt = await r.text();
    comprobar("secretos cambiados → 401", r.status === 401, "salió " + r.status);
    comprobar("y el mensaje lo dice con nombre",
      /parece el AUD/.test(txt), txt.slice(0, 120));
  }

  /* ---- /api/entrar, y su variante ?json=1 para el botón (2026-08-31) ---- */
  {
    const env = conAcceso();
    const t = await firmar(buenas, "kid-bueno",
      { aud: [AUD], email: "revisor@ejemplo.org", exp: dentro });
    const pedir = (p, tok) => worker.fetch(new Request("https://ejemplo.org" + p,
      { headers: tok ? { "Cf-Access-Jwt-Assertion": tok } : {} }), env);

    const html = await pedir("/api/entrar", t);
    const cuerpo = await html.text();
    comprobar("/api/entrar saluda por el correo",
      /revisor@ejemplo\.org/.test(cuerpo), cuerpo.slice(0, 90));
    comprobar("y no se cachea (es un diagnóstico)",
      /no-store/.test(html.headers.get("Cache-Control") || ""));

    const j = await (await pedir("/api/entrar?json=1", t)).json();
    comprobar("?json=1 con sesión → el correo",
      j.correo === "revisor@ejemplo.org", JSON.stringify(j));

    const j2 = await (await pedir("/api/entrar?json=1", null)).json();
    comprobar("?json=1 sin token → correo null",
      j2.correo === null, JSON.stringify(j2));
  }

  /* ---- LOS DOS PAPELES (2026-08-31) ----
     Access autentica, el worker autoriza. Lo que se sujeta aquí es que el
     aprendiz NO encola aunque su identidad sea impecable, y que la diferencia
     se diga con 403 y no con 401: son mensajes distintos y mandarían al
     aprendiz a iniciar sesión en bucle si se confundieran. */
  {
    const t = (correo) => firmar(buenas, "kid-bueno",
      { aud: [AUD], email: correo, exp: dentro });
    const conLista = () => ({ VEREDICTOS: kvFalso(), ACCESO_EQUIPO: EQUIPO,
      ACCESO_AUD: AUD, CLAVE_VEREDICTOS: "x",
      REVISORES: "jefe@ejemplo.org, otra@ejemplo.org" });

    const env1 = conLista();
    comprobar("revisor de la lista → 200",
      (await enviar(env1, await t("jefe@ejemplo.org"))).status === 200);

    const env2 = conLista();
    const r2 = await enviar(env2, await t("aprendiz@ejemplo.org"));
    comprobar("aprendiz → 403 (no 401)", r2.status === 403, "salió " + r2.status);
    comprobar("y no deja nada en la cola", env2.VEREDICTOS.datos.size === 0);

    // Mayúsculas y espacios en el repertorio: es una lista escrita a mano.
    const env3 = { ...conLista(), REVISORES: "  JEFE@Ejemplo.ORG \n otra@ejemplo.org " };
    comprobar("el repertorio no distingue mayúsculas ni espacios",
      (await enviar(env3, await t("jefe@ejemplo.org"))).status === 200);

    // Sin REVISORES: como hasta hoy, toda identidad verificada es revisora.
    comprobar("sin REVISORES, cualquiera verificado envía",
      (await enviar(conAcceso(), await t("quien@ejemplo.org"))).status === 200);

    // El papel viaja en el JSON que consulta el botón.
    const env4 = conLista();
    const pedir = (correo) => worker.fetch(new Request(
      "https://ejemplo.org/api/entrar?json=1",
      { headers: { "Cf-Access-Jwt-Assertion": correo } }), env4);
    const jr = await (await pedir(await t("jefe@ejemplo.org"))).json();
    const ja = await (await pedir(await t("aprendiz@ejemplo.org"))).json();
    comprobar("?json=1 dice papel revisor", jr.papel === "revisor", JSON.stringify(jr));
    comprobar("?json=1 dice papel aprendiz", ja.papel === "aprendiz", JSON.stringify(ja));
  }

  /* ---- EL RÓTULO PÚBLICO (2026-08-31, decisión de Angel: nombrar al
     revisor) ---- Lo que se publica es el rótulo, nunca el correo: la
     dirección se quitó de la página esta misma tarde y no vuelve. */
  {
    const env = { VEREDICTOS: kvFalso(), ACCESO_EQUIPO: EQUIPO,
      ACCESO_AUD: AUD, CLAVE_VEREDICTOS: "x",
      REVISORES: "jefe@ejemplo.org = IEBH\nfulano@ejemplo.org = Ven. Fulano\nsinrotulo@ejemplo.org" };
    const t = (c) => firmar(buenas, "kid-bueno",
      { aud: [AUD], email: c, exp: dentro });
    const meta = async (correo) => {
      const e2 = { ...env, VEREDICTOS: kvFalso() };
      await enviar(e2, await t(correo));
      return [...e2.VEREDICTOS.datos.values()][0].meta;
    };
    const a = await meta("jefe@ejemplo.org");
    comprobar("el rótulo del jefe es IEBH", a.rotulo === "IEBH", JSON.stringify(a));
    const b = await meta("fulano@ejemplo.org");
    comprobar("el rótulo con nombre se guarda",
      b.rotulo === "Ven. Fulano", JSON.stringify(b));
    const c = await meta("sinrotulo@ejemplo.org");
    comprobar("sin rótulo → «revisor verificado», NUNCA el correo",
      c.rotulo === "revisor verificado" && !/@/.test(c.rotulo), JSON.stringify(c));
    comprobar("y el correo sigue guardado aparte, para el registro",
      c.correo === "sinrotulo@ejemplo.org");
    comprobar("con rótulo, «=» no rompe el reparto de papeles",
      (await enviar({ ...env, VEREDICTOS: kvFalso() },
        await t("fulano@ejemplo.org"))).status === 200);
    comprobar("y quien no está en el repertorio sigue siendo aprendiz",
      (await enviar({ ...env, VEREDICTOS: kvFalso() },
        await t("nadie@ejemplo.org"))).status === 403);
  }

  /* ---- CÓMO SE ESCRIBE EL REPERTORIO (2026-08-31) ----
     Pasó de verdad: Angel figuraba en REVISORES y la página le decía
     «aprendiz». El parser sólo partía por comas y saltos de línea —para no
     partir los rótulos, que llevan espacios—, de modo que varios correos
     escritos SEGUIDOS quedaban en un solo trozo que no casaba con nadie.
     Se prueban aquí las cinco maneras razonables de escribirlo. */
  for (const [como, valor] of [
    ["separados por espacios", "jefe@ejemplo.org otro@ejemplo.org"],
    ["por comas", "jefe@ejemplo.org, otro@ejemplo.org"],
    ["uno por línea", "jefe@ejemplo.org\notro@ejemplo.org"],
    ["con rótulos por línea", "jefe@ejemplo.org = IEBH\notro@ejemplo.org = Otro"],
    ["mezclando rótulo y sueltos", "jefe@ejemplo.org = IEBH\notro@ejemplo.org tercero@ejemplo.org"],
    // Pegado tal cual desde la documentación, con su «#  → » delante: pasó,
    // y dos veces (2026-08-31). Un repertorio se escribe a mano.
    ["pegado con «#  → » de la documentación", "#  → jefe@ejemplo.org = IEBH\n#    otro@ejemplo.org = Otro"],
    ["con guiones de lista", "- jefe@ejemplo.org = IEBH"],
    ["entre < >", "<jefe@ejemplo.org>"],
  ]) {
    const env = { VEREDICTOS: kvFalso(), ACCESO_EQUIPO: EQUIPO,
      ACCESO_AUD: AUD, CLAVE_VEREDICTOS: "x", REVISORES: valor };
    const t = await firmar(buenas, "kid-bueno",
      { aud: [AUD], email: "jefe@ejemplo.org", exp: dentro });
    comprobar("REVISORES " + como + " → el jefe es revisor",
      (await enviar(env, t)).status === 200);
  }

  console.log("\n" + (hechas - fallos) + "/" + hechas + " comprobaciones");
  if (fallos) { console.log("HAY FALLOS: " + fallos); process.exit(1); }
  console.log("La identidad se sostiene.");
}

main().catch((e) => { console.error(e); process.exit(1); });
