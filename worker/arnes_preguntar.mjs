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
        se prefiere a VEREDICTOS
    13. fuentes de fondo (worker/fuentes.js): las claves, el tope y el
        interruptor PREGUNTAR_FUENTES; con «off» la petición es la de antes,
        byte a byte; con «on» van después de la fila, el sistema no cambia,
        los paquetes no vuelven al navegador y la línea «Fuentes
        consultadas» la pone el worker; con_fuentes cambia la advertencia de
        IA de la página; la inferencia propia va rotulada; los «Kac §N» de
        los paquetes son del IEBH; las clases de Kaccāyana de Sīlānanda
        (silananda-kacc) entran igual que las de Rūpasiddhi, y nada limita
        el § a §1–§270
    14. ejercicios sin lista fija: el sistema no enumera §; un ejercicio de
        Nāma (§66) va marcado y sin respuesta sugerida, como §38
    15. visesana suelto (§221): el sistema lo describe como lo da la fila */

import { readFileSync } from "node:fs";
import worker from "./index.js";
import { OBRAS, clavesDe, aplicarTope, fuentesActivas, lineaFuentes, estimarTokens, TOPE_TOKENS } from "./fuentes.js";

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
        content: [{ type: "thinking", thinking: "" }, { type: "text", text: "Respuesta de prueba." }],
        usage: { input_tokens: 300, output_tokens: 120, cache_creation_input_tokens: 0, cache_read_input_tokens: 1400 } });
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
    const registro = [], logOriginal = console.log;
    console.log = (...a) => registro.push(a.join(" "));
    const r = await pedir(e, bueno, P);
    console.log = logOriginal;
    const uso = registro.map((l) => { try { return JSON.parse(l); } catch (x) { return null; } })
      .find((o) => o && o.evento === "preguntar.uso");
    comprobar("registra el uso de la caché (creación y lectura)",
      uso && uso.cache_read_input_tokens === 1400 && uso.cache_creation_input_tokens === 0
        && uso.input_tokens === 300 && uso.output_tokens === 120, JSON.stringify(registro));
    comprobar("y en ese registro no hay correo ni pregunta",
      !registro.join(" ").toLowerCase().includes("lector@ejemplo.org") && !registro.join(" ").includes(P.pregunta));
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
    comprobar("la instrucción trae los ejercicios (por la marca de la fila, sin lista de §) y el «No lo sé»",
      sis.includes("las filas con «ejercicio» verdadero; la fila lo dice") && !/«ejercicio» verdadero: §/.test(sis)
        && sis.includes("«No lo sé»") && sis.includes("«Según la Visuddhāyuṃ (§n)"));
    comprobar("la instrucción describe el visesana suelto como lo da §221",
      sis.includes('§221 [visesana, ca, ""]') && sis.includes("con «visesana» en la primera posición")
        && sis.includes("no digas a qué palabra califica si la fila no lo dice"));
    {
      const f221 = JSON.parse(DATOS).filas["221"].roles.find((x) => x[0] === "visesana");
      comprobar("y la fila §221 de preguntar.json lo trae así", f221 && f221[1] === "ca" && f221[2] === "", JSON.stringify(f221));
    }
    comprobar("la instrucción llama «aṅga» al campo y no da su procedencia",
      sis.includes("«aṅga» (campo anuvatti)") && sis.includes("nunca «anuvatti»") && !sis.includes("vienen de suttas anteriores"));
    comprobar("la instrucción trae el ejemplo de §13 (nimitta «sarasmā», no «asarūpā»)",
      sis.includes("el nimitta es «sarasmā», calificado por «asarūpā»") && sis.includes("no digas lo que una palabra NO es"));
    comprobar("la instrucción pide «usted» y ejemplos sin marcas",
      sis.includes("«usted», nunca de «tú»") && sis.includes("nunca muestres las marcas"));
    comprobar("va el ejemplo llano junto al marcado",
      u.includes('"ejemplo_llano":"ekamidha + ahaṃ → ekamidāhaṃ"') && u.includes("ekami{k|dh}"), u.slice(0, 400));
    comprobar("«No lo sé» termina ahí; sin ofrecer más ayuda",
      sis.includes("TERMINA ahí") && sis.includes("no ofrezcas más ayuda"));
    comprobar("sólo § de otro sutta si está en el material; nada de «el libro dice» sin datos",
      sis.includes("aparece literalmente en el material") && sis.includes("«el libro llama…»"));
    const h = [...new Uint8Array(await crypto.subtle.digest("SHA-256",
      new TextEncoder().encode("lector@ejemplo.org")))].map((b) => b.toString(16).padStart(2, "0")).join("");
    comprobar("el contador va con el hash del correo (en minúsculas)",
      [...e.VEREDICTOS.datos.keys()].some((k) => /^preguntar\/\d{4}-\d\d-\d\d\//.test(k) && k.endsWith("/" + h)));
    const logs = [...e.VEREDICTOS.datos.entries()].filter(([k]) => k.startsWith("preguntar/log/"));
    const reg = logs.length === 1 ? JSON.parse(logs[0][1]) : {};
    comprobar("una entrada de registro con pregunta, §, lengua y fecha",
      reg.pregunta === P.pregunta && reg.sutta === 20 && reg.lang === "es" && /^\d{4}-\d\d-\d\dT/.test(reg.fecha),
      JSON.stringify(logs));
    comprobar("y sólo esos campos (más fuentes y uso)",
      Object.keys(reg).sort().join() === "fecha,fuentes,lang,pregunta,sutta,uso", Object.keys(reg).join());
    comprobar("el registro lleva el uso de tokens y ninguna fuente (interruptor apagado)",
      reg.uso && reg.uso.cache_read_input_tokens === 1400 && reg.uso.output_tokens === 120
        && Array.isArray(reg.fuentes) && reg.fuentes.length === 0, JSON.stringify(reg));
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
  await fuentes(env, pedir, bueno, P, () => llamadas, (v) => { llamadas = v; });
  comprobar("§ inexistente → 404", (await pedir(env(), bueno, { ...P, sutta: 9999 })).status === 404);
  comprobar("pregunta vacía → 400", (await pedir(env(), bueno, { ...P, pregunta: "  " })).status === 400);
  comprobar("pregunta larguísima → 400",
    (await pedir(env(), bueno, { ...P, pregunta: "x".repeat(1501) })).status === 400);

  console.log("\n" + (hechas - fallos) + "/" + hechas + " comprobaciones");
  if (fallos) { console.log("HAY FALLOS."); process.exit(1); }
  console.log("«Preguntar» se sostiene.");
}

/* 13. Las fuentes de fondo. */
async function fuentes(env, pedir, bueno, P, leer, poner) {
  console.log("\n  — fuentes de fondo —");
  comprobar("claves de §2: las cinco obras, en orden de prioridad",
    clavesDe(2).join() === "silananda-kacc/2,silananda-rup/2,rupasiddhi/2,nyasappadipika/2,nyasa/2", clavesDe(2).join());
  {
    const sh = readFileSync(new URL("../herramientas/subir_fuentes.sh", import.meta.url), "utf-8");
    const m = sh.match(/const OBRAS = (\[[^\]]*\]);/);
    const delGuion = m ? JSON.parse(m[1]) : [];
    comprobar("subir_fuentes.sh sube las mismas obras que lee el worker",
      delGuion.join() === OBRAS.map((o) => o.dir).join(), delGuion.join());
  }
  comprobar("claves de §280 (capítulo 3): las mismas obras, sin tope de §",
    clavesDe(280).join() === "silananda-kacc/280,silananda-rup/280,rupasiddhi/280,nyasappadipika/280,nyasa/280", clavesDe(280).join());
  comprobar("interruptor: apagado por omisión",
    !fuentesActivas({ FUENTES: {} }) && !fuentesActivas({ FUENTES: {}, PREGUNTAR_FUENTES: "off" }));
  comprobar("interruptor: «on» enciende (también « ON »), pero no sin el KV",
    fuentesActivas({ FUENTES: {}, PREGUNTAR_FUENTES: "on" }) && fuentesActivas({ FUENTES: {}, PREGUNTAR_FUENTES: " ON " })
      && !fuentesActivas({ PREGUNTAR_FUENTES: "on" }));

  const pq = (dir, chars) => ({ clave: dir + "/2", obra: { dir, nombre: dir, name: dir },
    texto: dir + "; ed.; lugar; ninguno; derechos\n" + "a".repeat(chars) });
  const cuatro = [pq("silananda-rup", 12000), pq("rupasiddhi", 4500), pq("nyasappadipika", 4500), pq("nyasa", 4500)];
  const total = (ps) => ps.reduce((s, p) => s + estimarTokens(p.texto), 0);
  {
    const t = aplicarTope(cuatro, 100000);
    comprobar("tope: lo que cabe pasa entero", t.paquetes.length === 4 && !t.descartadas.length && !t.recortada);
    const t2 = aplicarTope(cuatro, 7000);
    comprobar("tope: se cae primero el Nyāsa, luego la Nyāsappadīpikā",
      t2.descartadas.join() === "nyasa/2,nyasappadipika/2" && t2.paquetes.length === 2, JSON.stringify(t2.descartadas));
    const t3 = aplicarTope(cuatro, 2000);
    comprobar("tope: si ni Sīlānanda cabe sola, se recorta y se dice",
      t3.paquetes.length === 1 && t3.recortada === "silananda-rup/2" && t3.paquetes[0].texto.includes("recortado")
        && total(t3.paquetes) <= 2000, total(t3.paquetes));
    // Tamaños de verdad: Sīlānanda ~7.000 tokens y las otras ~2.000 → 13.000.
    const grandes = [pq("silananda-rup", 21000), pq("rupasiddhi", 6000), pq("nyasappadipika", 6000), pq("nyasa", 6000)];
    // Las dos series juntas: la de Kaccāyana es la última que se cae.
    const pq2 = (dir, chars) => ({ ...pq(dir, chars), clave: dir + "/2" });
    const series = [pq2("silananda-kacc", 15000), pq2("silananda-rup", 15000), pq2("rupasiddhi", 4500)];
    const t5 = aplicarTope(series, 6000);
    comprobar("tope: con las dos series de Sīlānanda, se cae la de Rūpasiddhi y queda la de Kaccāyana",
      t5.descartadas.join() === "rupasiddhi/2,silananda-rup/2" && t5.paquetes.map((p) => p.clave).join() === "silananda-kacc/2",
      JSON.stringify(t5));
    comprobar("y el orden de OBRAS lo dice: silananda-kacc primero, silananda-rup después",
      OBRAS[0].dir === "silananda-kacc" && OBRAS[1].dir === "silananda-rup", OBRAS.map((o) => o.dir).join());
    const t4 = aplicarTope(grandes);
    comprobar("tope por omisión (" + TOPE_TOKENS + "): cae sólo el Nyāsa y el bloque queda por debajo",
      total(t4.paquetes) <= TOPE_TOKENS && t4.descartadas.join() === "nyasa/2", total(t4.paquetes) + " " + t4.descartadas);
  }

  const TEXTOS = {
    "silananda-rup/20": "fuente: U Sīlānanda, Rūpasiddhi classes (clase 3, 12:40); grabación; clase 3; ninguno; uso privado\nIn class he says SECRETO-SILANANDA.",
    "silananda-kacc/20": "fuente: U Sīlānanda, Kaccāyana classes (clase 7, 03:10); transcripción automática, editada; clase 7; ninguno; CC BY-NC-ND 4.0 © IEBH\nIn class he says SECRETO-KACC.",
    "rupasiddhi/20": "**Rūpasiddhi (VRI)**; VRI; §20; texto con ruido de OCR: no citar textualmente; dominio público\nSECRETO-RUPASIDDHI",
    "nyasa/20": "Nyāsa; VRI; p. 1; ninguno; dominio público\nSECRETO-NYASA",
    "nyasa/38": "Nyāsa; VRI; p. 9; ninguno; dominio público\nSECRETO-EJERCICIO",
  };
  const kvF = () => {
    const leidas = [];
    return { leidas, async get(k) { leidas.push(k); return TEXTOS[k] ?? null; } };
  };
  const pedirCon = async (extra, cuerpo = P) => {
    const e = { ...env(), ...extra }; poner([]);
    const registro = [], logOriginal = console.log;
    console.log = (...a) => registro.push(a.join(" "));
    const r = await pedir(e, bueno, cuerpo);
    console.log = logOriginal;
    const c = leer()[0];
    return { e, r, x: await r.json(), c, u: c ? c.body.messages[0].content : "", sis: c ? c.body.system : null, registro };
  };

  const base = await pedirCon({});
  const off = await pedirCon({ FUENTES: kvF(), PREGUNTAR_FUENTES: "off" });
  comprobar("apagado: la petición es idéntica a la de sin FUENTES",
    JSON.stringify(off.c.body) === JSON.stringify(base.c.body));
  comprobar("apagado: no se lee el KV y no hay línea de fuentes",
    off.e.FUENTES.leidas.length === 0 && !off.x.respuesta.includes("Fuentes consultadas"), off.x.respuesta);

  const on = await pedirCon({ FUENTES: kvF(), PREGUNTAR_FUENTES: "on" });
  comprobar("encendido: se piden las cinco claves de §20",
    on.e.FUENTES.leidas.slice().sort().join() === clavesDe(20).slice().sort().join(), on.e.FUENTES.leidas.join());
  comprobar("encendido: el sistema es el mismo (la caché sigue valiendo)",
    JSON.stringify(on.sis) === JSON.stringify(base.c.body.system));
  const iG = on.u.indexOf("</glosario>"), iF = on.u.indexOf("<fuentes>"), iL = on.u.indexOf("<lengua>");
  comprobar("encendido: <fuentes> va después de la fila y el glosario, antes de la pregunta",
    iG > 0 && iF > iG && iL > iF, [iG, iF, iL].join());
  comprobar("encendido: cada paquete con su cabecera; el que falta se salta",
    on.u.includes('<fuente clave="silananda-rup/20">\nfuente: U Sīlānanda, Rūpasiddhi classes (clase 3, 12:40); grabación;')
      && on.u.includes('<fuente clave="silananda-kacc/20">\nfuente: U Sīlānanda, Kaccāyana classes') && on.u.includes("SECRETO-KACC")
      && on.u.includes("texto con ruido de OCR") && on.u.includes("SECRETO-NYASA")
      && !on.u.includes("nyasappadipika/20"), on.u.slice(iF, iF + 400));
  comprobar("encendido: la línea «Fuentes consultadas» la pone el worker, con los nombres fijos y en orden",
    on.x.respuesta === "Respuesta de prueba.\n\nFuentes consultadas: U Sīlānanda, clases de Kaccāyana; U Sīlānanda, clases de Rūpasiddhi; Padarūpasiddhi; Nyāsa.",
    on.x.respuesta);
  comprobar("y sin nada de la cabecera (ni «fuente:», ni clase, ni edición)",
    !/fuente:|clase 3|clase 7|12:40|03:10|VRI|BY-NC|\*\*/.test(on.x.respuesta), on.x.respuesta);
  const alNavegador = JSON.stringify(on.x);
  comprobar("encendido: ningún paquete vuelve al navegador",
    !/SECRETO-|grabación|transcripción automática|dominio público/.test(alNavegador), alNavegador);
  const uso = on.registro.map((l) => { try { return JSON.parse(l); } catch (x) { return null; } })
    .find((o) => o && o.evento === "preguntar.uso");
  comprobar("encendido: el registro del worker lleva las claves y el uso",
    uso && uso.fuentes.join() === "silananda-kacc/20,silananda-rup/20,rupasiddhi/20,nyasa/20" && uso.input_tokens === 300, JSON.stringify(uso));
  const log = [...on.e.VEREDICTOS.datos.entries()].find(([k]) => k.startsWith("preguntar/log/"));
  const reg = log ? JSON.parse(log[1]) : {};
  comprobar("encendido: el registro del KV lleva las claves y no el texto",
    reg.fuentes && reg.fuentes.length === 4 && !/SECRETO-/.test(log[1]), log && log[1]);

  const en = await pedirCon({ FUENTES: kvF(), PREGUNTAR_FUENTES: "on" }, { ...P, lang: "en" });
  comprobar("con fuentes cargadas, con_fuentes es true (y sólo un booleano)",
    on.x.con_fuentes === true && off.x.con_fuentes === false, JSON.stringify([on.x.con_fuentes, off.x.con_fuentes]));
  comprobar("en inglés: «Sources consulted» con los nombres ingleses",
    en.x.respuesta.endsWith("\n\nSources consulted: U Sīlānanda, classes on Kaccāyana; U Sīlānanda, classes on the Rūpasiddhi; Padarūpasiddhi; Nyāsa."), en.x.respuesta);

  const vacio = await pedirCon({ FUENTES: kvF(), PREGUNTAR_FUENTES: "on" }, { ...P, sutta: 13 });
  comprobar("encendido, sin paquetes para el §: ni bloque ni línea",
    !vacio.u.includes("<fuentes>") && vacio.x.respuesta === "Respuesta de prueba." && vacio.x.con_fuentes === false,
    vacio.x.respuesta);

  const roto = await pedirCon({ PREGUNTAR_FUENTES: "on",
    FUENTES: { async get() { throw new Error("KV caído"); } } });
  comprobar("si el KV falla, la pregunta se responde igual y sin fuentes",
    roto.r.status === 200 && !roto.u.includes("<fuentes>"), roto.r.status);

  const ej = await pedirCon({ FUENTES: kvF(), PREGUNTAR_FUENTES: "on" }, { ...P, sutta: 38 });
  comprobar("ejercicio §38 con fuentes: sigue sin la respuesta sugerida",
    ej.u.includes('"ejercicio":true') && !ej.u.includes('["kāriya","lopaṃ","kvaci"]') && ej.u.includes("SECRETO-EJERCICIO"));

  {
    // 14. Un ejercicio de Nāma, que la vieja lista (§38–§50) no nombraba.
    const f66 = JSON.parse(DATOS).filas["66"];
    const ej66 = await pedirCon({}, { ...P, sutta: 66 });
    const resp = JSON.stringify(f66.respuesta);
    comprobar("ejercicio §66 (Nāma): va marcado y sin la respuesta sugerida",
      f66.ejercicio === true && f66.respuesta.length > 0 && ej66.u.includes('"ejercicio":true')
        && !ej66.u.includes(resp.slice(1, -1)) && !ej66.u.includes('"respuesta"'), ej66.u.slice(0, 300));
  }

  {
    // §271 en adelante: las fuentes no tienen tope; lo que falta es la fila.
    const TEXTOS3 = { "silananda-kacc/280": "fuente: U Sīlānanda, Kaccāyana classes; transcripción automática, editada; clase 40; ninguno; CC BY-NC-ND 4.0 © IEBH\nSECRETO-280" };
    const kv3 = { async get(k) { return TEXTOS3[k] ?? null; } };
    const { leerFuentes } = await import("./fuentes.js");
    const l = await leerFuentes({ FUENTES: kv3 }, 280);
    comprobar("§280: leerFuentes trae silananda-kacc/280",
      l.length === 1 && l[0].clave === "silananda-kacc/280" && l[0].obra.nombre === "U Sīlānanda, clases de Kaccāyana", JSON.stringify(l.map((p) => p.clave)));
    const sin = await pedirCon({ FUENTES: kv3, PREGUNTAR_FUENTES: "on" }, { ...P, sutta: 280 });
    comprobar("§280 sin fila en preguntar.json → 404 y la API no se llama (el único límite son los datos de la página)",
      sin.r.status === 404 && !sin.c, sin.r.status);
  }

  const sis = base.c.body.system[0].text;
  comprobar("la instrucción trae las reglas de las fuentes",
    sis.includes("«Según la Rūpasiddhi…»") && sis.includes("(clase N, mm:ss)")
      && sis.includes("nunca atribuyas a la Visuddhāyuṃ la opinión de otra obra")
      && sis.includes("unas 15 palabras") && sis.includes("«texto con ruido de OCR: no citar textualmente»")
      && sis.includes("están en inglés: resúmelas") && sis.includes("«Las fuentes consultadas no tratan este punto»")
      && sis.includes("tampoco se resuelven con las fuentes"));
  comprobar("la instrucción distingue las dos series de clases de Sīlānanda",
    sis.includes("sus clases sobre Kaccāyana (dos series distintas; transcripciones automáticas en inglés, editadas)")
      && sis.includes("«U Sīlānanda explica en sus clases de Kaccāyana (clase N, mm:ss) que…»")
      && sis.includes("No confundas las dos series de clases"));
  comprobar("la inferencia propia va rotulada «(del asistente, no de las fuentes)»",
    sis.includes("«Explicación general (del asistente, no de las fuentes): …»")
      && sis.includes("«General explanation (the assistant's, not from the sources): …»")
      && sis.includes("«(inferencia del asistente)»") && !sis.includes("empieza por «Explicación general: …»"));
  comprobar("los «Kac §N» de los paquetes son del IEBH, no de la obra",
    sis.includes("(«Kac §N», «Kacc. §N» y semejantes) son del IEBH") && sis.includes("no digas que la obra cita ese §"));

  const pagina = readFileSync(new URL("../site/recursos/analisis/index.html", import.meta.url), "utf-8");
  comprobar("la página trae las dos advertencias, con y sin fuentes",
    pagina.includes("sólo a partir de esta fila y del glosario del sitio")
      && pagina.includes("a partir de esta fila, del glosario del sitio y de las fuentes consultadas. No está revisada por el IEBH: cotéjela con las fuentes.")
      && pagina.includes("from this row, the site glossary and the sources consulted. Not reviewed by the IEBH: check it against the sources."));
  comprobar("y la elige por con_fuentes, también al copiar",
    pagina.includes("notaPreg(!!j.con_fuentes)") && pagina.includes("'— '+nota") && pagina.includes("notaPreg(false)"));

  const conf = JSON.parse(readFileSync(new URL("../wrangler.jsonc", import.meta.url), "utf-8")
    .replace(/^\s*\/\/.*$/gm, ""));
  const f = (conf.kv_namespaces || []).find((k) => k.binding === "FUENTES");
  comprobar("wrangler.jsonc enlaza FUENTES con un id real", !!f && /^[0-9a-f]{32}$/.test(f.id), f && f.id);
}

main();
