/* Arnés de /api/preguntar — worker/preguntar.js (2026-10-03).

       node worker/arnes_preguntar.mjs

   Lo que se comprueba, sin red: el JWKS de Access y la API de Anthropic se
   sirven de mentira sustituyendo globalThis.fetch, y preguntar.json se lee
   del disco (hay que haber corrido antes herramientas/generar_analisis.py).

     1. sin configurar                   → 503, y la API no se llama
     2. sin token                        → 401
     3. token de la OTRA aplicación      → 401 (el aud de «gramaticas» no vale)
     4. GET ?json=1                      → correo y 20 restantes
     5. POST bueno                       → 200; a la API va la fila, sus
                                           términos, la caché en el sistema,
                                           y nada de la «fuente» del glosario
     6. la API falla                     → 502 y no se gasta pregunta
     7. límite alcanzado                 → 429 y la API no se llama
     8. § inexistente / pregunta vacía   → 404 / 400
     9. /api/cola no enseña los contadores ni el registro
    10. el registro: pregunta, §, lengua y fecha; el correo, en ninguna parte
    11. ejercicio (§38): la respuesta sugerida no va al modelo
    12. modelo: Sonnet por omisión, PREGUNTAR_MODELO lo cambia; PREGUNTAS
        se prefiere a VEREDICTOS */

import { readFileSync } from "node:fs";
import worker from "./index.js";

const EQUIPO = "equipo-de-prueba.cloudflareaccess.com";
const AUD = "aud-de-gramaticas";
const AUD_P = "aud-de-gramaticas-preguntar";
const DATOS = readFileSync(new URL("../site/recursos/analisis/preguntar.json", import.meta.url), "utf-8");
const GLOSARIO = readFileSync(new URL("../recursos/terminos/terminos.json", import.meta.url), "utf-8");

const b64url = (b) => Buffer.from(b).toString("base64")
  .replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");

async function firmar(par, cuerpo) {
  const cab = b64url(JSON.stringify({ alg: "RS256", kid: "k" }));
  const cue = b64url(JSON.stringify(cuerpo));
  const firma = await crypto.subtle.sign("RSASSA-PKCS1-v1_5", par.privateKey,
    new TextEncoder().encode(cab + "." + cue));
  return cab + "." + cue + "." + b64url(new Uint8Array(firma));
}

function kvFalso() {
  const m = new Map();
  return {
    datos: m,
    async put(k, v) { m.set(k, v); },
    async get(k) { return m.has(k) ? m.get(k) : null; },
    async list() { return { list_complete: true, keys: [...m.keys()].map((name) => ({ name })) }; },
    async delete(k) { m.delete(k); },
  };
}

const assets = { async fetch(req) {
  return new URL(req.url).pathname === "/recursos/analisis/preguntar.json"
    ? new Response(DATOS) : new Response("no", { status: 404 });
} };

let fallos = 0, hechas = 0;
function comprobar(nombre, cond, detalle) {
  hechas += 1;
  if (cond) console.log("  ok   " + nombre);
  else { fallos += 1; console.log("  MAL  " + nombre + (detalle ? " — " + detalle : "")); }
}

async function main() {
  const par = await crypto.subtle.generateKey(
    { name: "RSASSA-PKCS1-v1_5", modulusLength: 2048,
      publicExponent: new Uint8Array([1, 0, 1]), hash: "SHA-256" }, true, ["sign", "verify"]);
  const j = await crypto.subtle.exportKey("jwk", par.publicKey);
  const jwks = { keys: [{ kid: "k", kty: j.kty, n: j.n, e: j.e, alg: "RS256" }] };

  let llamadas = [], apiStatus = 200;
  globalThis.fetch = async (u, o) => {
    if (String(u) === "https://" + EQUIPO + "/cdn-cgi/access/certs") return Response.json(jwks);
    if (String(u) === "https://api.anthropic.com/v1/messages") {
      llamadas.push({ headers: o.headers, body: JSON.parse(o.body) });
      if (apiStatus !== 200) return new Response("error de prueba", { status: apiStatus });
      return Response.json({ model: "claude-opus-5-5", stop_reason: "end_turn",
        content: [{ type: "thinking", thinking: "" }, { type: "text", text: "Respuesta de prueba." }] });
    }
    throw new Error("URL inesperada: " + u);
  };

  const exp = Math.floor(Date.now() / 1000) + 3600;
  const bueno = await firmar(par, { aud: [AUD_P], email: "Lector@Ejemplo.org", exp });
  const deOtra = await firmar(par, { aud: [AUD], email: "lector@ejemplo.org", exp });
  const env = () => ({ ASSETS: assets, VEREDICTOS: kvFalso(), ACCESO_EQUIPO: EQUIPO,
    ACCESO_AUD: AUD, ACCESO_AUD_PREGUNTAR: AUD_P, ANTHROPIC_API_KEY: "clave-de-prueba",
    CLAVE_VEREDICTOS: "x" });
  const pedir = (e, tok, cuerpo, q = "") => worker.fetch(new Request(
    "https://ejemplo.org/api/preguntar" + q, cuerpo === undefined
      ? { headers: tok ? { "Cf-Access-Jwt-Assertion": tok } : {} }
      : { method: "POST", body: JSON.stringify(cuerpo),
          headers: { "Content-Type": "application/json", ...(tok ? { "Cf-Access-Jwt-Assertion": tok } : {}) } }), e);
  const P = { sutta: 20, pregunta: "¿Por qué «sare» es nimitta?", lang: "es" };

  console.log("Arnés de /api/preguntar\n");

  {
    const e = env(); delete e.ANTHROPIC_API_KEY; llamadas = [];
    const r = await pedir(e, bueno, P);
    comprobar("sin ANTHROPIC_API_KEY → 503", r.status === 503, "salió " + r.status);
    comprobar("y la API no se llama", llamadas.length === 0);
    const e2 = env(); delete e2.ACCESO_AUD_PREGUNTAR;
    comprobar("sin ACCESO_AUD_PREGUNTAR → 503", (await pedir(e2, bueno, P)).status === 503);
  }
  comprobar("sin token → 401", (await pedir(env(), null, P)).status === 401);
  comprobar("token de la aplicación «gramaticas» → 401", (await pedir(env(), deOtra, P)).status === 401);

  {
    const r = await pedir(env(), bueno, undefined, "?json=1");
    const x = await r.json();
    comprobar("GET ?json=1 → correo y 20 restantes",
      r.status === 200 && x.correo === "Lector@Ejemplo.org" && x.restantes === 20, JSON.stringify(x));
    const h = await pedir(env(), bueno, undefined);
    comprobar("GET sin json → página de sesión", h.status === 200
      && (h.headers.get("Content-Type") || "").startsWith("text/html"));
  }

  {
    const e = env(); llamadas = []; apiStatus = 200;
    const r = await pedir(e, bueno, P);
    const x = await r.json();
    comprobar("POST bueno → 200 con la respuesta", r.status === 200 && x.respuesta === "Respuesta de prueba.",
      r.status + " " + JSON.stringify(x));
    comprobar("y quedan 19", x.restantes === 19, JSON.stringify(x));
    const c = llamadas[0] || { headers: {}, body: { system: [{}], messages: [{ content: "" }] } };
    comprobar("la clave va en x-api-key", c.headers["x-api-key"] === "clave-de-prueba");
    comprobar("la parte fija lleva cache_control",
      c.body.system[0].cache_control && c.body.system[0].cache_control.type === "ephemeral");
    const u = c.body.messages[0].content;
    comprobar("va la fila §20", u.includes('"§":20') && u.includes("Do dhassa ca"), u.slice(0, 200));
    comprobar("van sus términos (kāriyī, nimitta)", u.includes('"termino":"kāriyī') && u.includes('"termino":"nimitta'), u);
    comprobar("va la lengua y la pregunta", u.includes("<lengua>es</lengua>") && u.includes(P.pregunta));
    const fuentes = JSON.parse(GLOSARIO).terminos.map((t) => t.fuente).filter((f) => f && f.length > 20);
    comprobar("no va ninguna «fuente» del glosario", !fuentes.some((f) => u.includes(f)));
    comprobar("ni la otra lengua de la nota", !u.includes("The book splits"));
    comprobar("modelo por omisión: claude-sonnet-5-5", c.body.model === "claude-sonnet-5-5", c.body.model);
    const sis = c.body.system[0].text;
    comprobar("la instrucción trae los ejercicios y el «No lo sé»",
      sis.includes("§38, §39, §44 y §50") && sis.includes("«No lo sé»") && sis.includes("«Según la Visuddhāyuṃ (§n)"));
    const h = [...new Uint8Array(await crypto.subtle.digest("SHA-256",
      new TextEncoder().encode("lector@ejemplo.org")))].map((b) => b.toString(16).padStart(2, "0")).join("");
    comprobar("el contador va con el hash del correo (en minúsculas)",
      [...e.VEREDICTOS.datos.keys()].some((k) => /^preguntar\/\d{4}-\d\d-\d\d\//.test(k) && k.endsWith("/" + h)));
    const logs = [...e.VEREDICTOS.datos.entries()].filter(([k]) => k.startsWith("preguntar/log/"));
    const reg = logs.length === 1 ? JSON.parse(logs[0][1]) : {};
    comprobar("una entrada de registro con pregunta, §, lengua y fecha",
      reg.pregunta === P.pregunta && reg.sutta === 20 && reg.lang === "es" && /^\d{4}-\d\d-\d\dT/.test(reg.fecha),
      JSON.stringify(logs));
    comprobar("y sólo esos cuatro campos", Object.keys(reg).sort().join() === "fecha,lang,pregunta,sutta");
    comprobar("el correo no está en ninguna clave ni valor del KV",
      ![...e.VEREDICTOS.datos.entries()].some(([k, v]) => (k + v).toLowerCase().includes("lector@ejemplo.org")));
    const cola = await worker.fetch(new Request("https://ejemplo.org/api/cola?clave=x"), e);
    const lista = (await cola.json()).veredictos || [];
    comprobar("/api/cola no enseña los contadores ni el registro", cola.status === 200 && lista.length === 0, JSON.stringify(lista));

    const en = await pedir(e, bueno, { ...P, lang: "en" });
    const u2 = llamadas[1] ? llamadas[1].body.messages[0].content : "";
    comprobar("en inglés va la nota inglesa", en.status === 200 && u2.includes("The book splits")
      && u2.includes("<lengua>en</lengua>"));

    apiStatus = 500;
    const ko = await pedir(e, bueno, P);
    const k = await ko.json();
    comprobar("la API falla → 502", ko.status === 502, "salió " + ko.status);
    const g = await (await pedir(e, bueno, undefined, "?json=1")).json();
    comprobar("y no se gasta pregunta (siguen 18)", g.restantes === 18, JSON.stringify(g) + " " + JSON.stringify(k));
    apiStatus = 200;

    for (const [kk] of e.VEREDICTOS.datos) e.VEREDICTOS.datos.set(kk, "20");
    llamadas = [];
    const lim = await pedir(e, bueno, P);
    comprobar("con 20 usadas → 429", lim.status === 429, "salió " + lim.status);
    comprobar("y la API no se llama", llamadas.length === 0);
  }

  {
    llamadas = [];
    const r = await pedir(env(), bueno, { ...P, sutta: 38, pregunta: "¿Cuál es la solución?" });
    const u = llamadas[0] ? llamadas[0].body.messages[0].content : "";
    comprobar("ejercicio §38 → 200 y va marcado como ejercicio", r.status === 200 && u.includes('"ejercicio":true'), u.slice(0, 300));
    comprobar("y sin la respuesta sugerida", !u.includes('"respuesta"') && !u.includes('["kāriya","lopaṃ","kvaci"]'), u);
  }
  {
    const e = env(); e.PREGUNTAR_MODELO = "claude-opus-5-5"; e.PREGUNTAS = kvFalso(); llamadas = [];
    await pedir(e, bueno, P);
    comprobar("PREGUNTAR_MODELO cambia el modelo", llamadas[0] && llamadas[0].body.model === "claude-opus-5-5");
    comprobar("con PREGUNTAS enlazado, se escribe ahí y no en VEREDICTOS",
      e.PREGUNTAS.datos.size === 2 && e.VEREDICTOS.datos.size === 0,
      e.PREGUNTAS.datos.size + " / " + e.VEREDICTOS.datos.size);
    const conf = JSON.parse(readFileSync(new URL("../wrangler.jsonc", import.meta.url), "utf-8")
      .replace(/^\s*\/\/.*$/gm, ""));
    comprobar("wrangler.jsonc enlaza PREGUNTAS (producción)",
      (conf.kv_namespaces || []).some((k) => k.binding === "PREGUNTAS" && /^[0-9a-f]{32}$/.test(k.id)));
    comprobar("y no trae valores de secretos",
      !conf.vars && !/sk-ant|ANTHROPIC_API_KEY"\s*:/.test(JSON.stringify(conf)));
  }
  comprobar("§ inexistente → 404", (await pedir(env(), bueno, { ...P, sutta: 9999 })).status === 404);
  comprobar("pregunta vacía → 400", (await pedir(env(), bueno, { ...P, pregunta: "  " })).status === 400);
  comprobar("pregunta larguísima → 400",
    (await pedir(env(), bueno, { ...P, pregunta: "x".repeat(1501) })).status === 400);

  console.log("\n" + (hechas - fallos) + "/" + hechas + " comprobaciones");
  if (fallos) { console.log("HAY FALLOS."); process.exit(1); }
  console.log("«Preguntar» se sostiene.");
}

main();
