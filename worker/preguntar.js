/* /api/preguntar — el botón «Preguntar» de /recursos/analisis/ (2026-10-03).

   El lector pregunta por UNA fila de la tabla y el modelo responde con esa
   fila delante y nada más: los datos de la fila tal como la página los
   enseña, las entradas del glosario que la fila usa (sólo los campos del
   globo; la «fuente» de cada término no sale nunca), la pregunta y la lengua
   de la página. Lo arma generar_analisis.py en site/recursos/analisis/
   preguntar.json, de modo que el contexto es siempre el de la página
   publicada y no lo que mande el navegador.

     POST /api/preguntar   {sutta, pregunta, lang}  → {respuesta, restantes}
     GET  /api/preguntar                             → página «sesión iniciada»
     GET  /api/preguntar?json=1                      → {correo, restantes}

   ---- QUIÉN: Cloudflare Access, como /api/veredictos ----

   La ruta está detrás de la aplicación de Access «gramaticas-preguntar»
   (política «Preguntar»). Se verifica el JWT con la MISMA función que la cola
   —firma, aud y caducidad—, pero contra el AUD de ESA aplicación, que es otro:

     ACCESO_EQUIPO          el mismo de siempre
     ACCESO_AUD_PREGUNTAR   el AUD tag de «gramaticas-preguntar»
     ANTHROPIC_API_KEY      la clave de la API; sólo como secreto del worker

   A diferencia de la cola, AQUÍ SE FALLA CERRADO: sin cualquiera de los tres,
   503. La cola se dejó abierta para no romper lo que ya funcionaba; esto
   cuesta dinero en cada llamada y no hay nada previo que romper.

   El GET existe para iniciar sesión: Access protege la ruta para todos los
   métodos, así que visitarla con el navegador es lo que pide el código de un
   solo uso. La página lo usa también, con ?json=1, para saber si mostrar el
   botón.

   ---- CUÁNTO: 20 preguntas por persona y día (UTC) ----

   El contador vive en el KV de la cola (o en PREGUNTAS, si algún día se crea
   uno propio) bajo el prefijo PREFIJO_PREGUNTAS, que /api/cola excluye. Sólo
   cuenta lo que se respondió: un fallo de la API no gasta pregunta. KV no es
   atómico, así que dos preguntas a la vez podrían contar una; para dos
   personas no merece un Durable Object. No se guarda el texto de las
   preguntas ni de las respuestas. */

export const PREFIJO_PREGUNTAS = "preguntar/";
const LIMITE_DIARIO = 20;
const MAX_PREGUNTA = 1500;          // caracteres
const MODELO = "claude-opus-5-5";   // PREGUNTAR_MODELO lo cambia sin desplegar

/* La parte fija del prompt: va primero y con cache_control, de modo que se
   cobra entera una vez cada cinco minutos y no en cada pregunta. Nada que
   cambie de una llamada a otra (fecha, correo, fila) puede entrar aquí: un
   solo byte distinto invalida la caché. */
const SISTEMA = `Eres el asistente de la página «Análisis de los suttas de Kaccāyana según la Visuddhāyuṃ Kaccāyana-ṭīkā» del sitio Gramáticas Pāḷi del Instituto de Estudios Buddhistas Hispano (IEBH). Los lectores son estudiantes de pāḷi con formación buddhista. Quienes leen tus respuestas ya ven la tabla: no la repitas, explícala.

Cada pregunta trata de UNA fila de la tabla, que recibes en <fila>, junto con las entradas del glosario del sitio que esa fila usa, en <glosario>. Ese material es todo tu contexto.

Qué contiene la fila:
- «sutta»: el texto pāḷi del aforismo (numeración de Kaccāyana, §n), y «tr» su traducción publicada en el sitio.
- «clase»: la clase de sutta que le da la Visuddhāyuṃ (en pāḷi o en birmano, como está impreso).
- «anuvatti»: palabras que vienen de suttas anteriores (el libro las llama aṅga).
- «roles»: la función de cada palabra del sutta, como [función, palabra, visesana, inflexión]. Funciones: kāriyī (aquello a lo que se aplica la operación), kāriya (la operación), nimitta (la causa; la inflexión 7.ª/5.ª/3.ª es un añadido editorial del IEBH, deducido del caso de la palabra, no análisis del libro), saññā/saññī (en los suttas de definición, el nombre técnico y lo que lo recibe), visaya/visayī (en los de inserción y duplicación). El visesana es un calificador de otra palabra.
- «ejercicio»: si es verdadero, el libro deja el análisis al estudiante, y «respuesta» es la respuesta sugerida por el IEBH, no por el libro.
- «ejemplo»: el ejemplo del modelo de derivación del libro, con marcas: {k|…} lo que sufre la operación, {n|…} la causa, {r|…} el resultado, {x|…} lo que se elide; {kx|…} y {nx|…} combinan dos marcas.
- «nota»: notas del IEBH (cotejos, dudas de lectura, la clasificación del sitio).
- «pdf»: la página del PDF del libro.

Cómo responder:
1. Responde en la lengua que indica <lengua> (es = español, en = inglés), en registro formal y claro, en prosa, sin encabezados. Como máximo 300 palabras; menos si basta.
2. Términos técnicos pāḷi sin traducir y con diacríticos completos (kāriyī, nimitta, sattamī, pubbalopa). Usa las definiciones de <glosario> como las del sitio.
3. Básate sólo en la fila y el glosario. Si la respuesta exige algo que no está ahí —otro sutta, la vutti, el comentario completo, otra gramática—, dilo expresamente («la fila no lo dice») en lugar de suponerlo, y puedes indicar dónde habría que mirarlo.
4. No inventes reglas, pasos de derivación, referencias ni citas. Si propones una explicación propia, márcala como tal. Ante una duda de lectura o de gramática, di que es una duda.
5. El Tipiṭaka es la fuente y Kaccāyana la autoridad que lo explica: que una forma sea posible por las reglas no demuestra que el canon la diga. No afirmes que una lectura está atestiguada si no lo dice el material.
6. Lo que es del libro (Visuddhāyuṃ) y lo que es añadido del IEBH (inflexión del nimitta, respuestas de ejercicio, notas) se distingue al citarlo.
7. Si la pregunta no tiene que ver con la fila o con la gramática pāḷi, responde brevemente que este asistente sólo trata de la fila seleccionada.`;

/* preguntar.json, leído una vez por instancia: cambia sólo con un despliegue. */
let DATOS = null;
async function datos(env, url) {
  if (DATOS) return DATOS;
  const r = await env.ASSETS.fetch(new Request(new URL("/recursos/analisis/preguntar.json", url)));
  if (!r.ok) throw new Error("preguntar.json respondió " + r.status);
  DATOS = await r.json();
  return DATOS;
}

function kv(env) {
  return env.PREGUNTAS || env.VEREDICTOS || null;
}

function claveDelDia(correo) {
  return PREFIJO_PREGUNTAS + new Date().toISOString().slice(0, 10) + "/" + correo.toLowerCase();
}

async function usadas(env, correo) {
  return parseInt((await kv(env).get(claveDelDia(correo))) || "0", 10) || 0;
}

const SIN_CACHE = { "Cache-Control": "no-store" };
const json = (cuerpo, status = 200) => Response.json(cuerpo, { status, headers: SIN_CACHE });

export async function preguntar(request, env, url, identidad) {
  // Cerrado mientras falte cualquier pieza: aquí cada llamada se paga.
  const falta = ["ANTHROPIC_API_KEY", "ACCESO_EQUIPO", "ACCESO_AUD_PREGUNTAR"]
    .filter((k) => !env[k]);
  if (!kv(env)) falta.push("KV (VEREDICTOS o PREGUNTAS)");
  if (falta.length) {
    return json({ ok: false, error: "«Preguntar» no está configurado: falta " + falta.join(", ") }, 503);
  }
  const ident = await identidad(request, env, env.ACCESO_AUD_PREGUNTAR);
  if (!ident.correo) {
    return json({ ok: false, error: "hace falta iniciar sesión (" + (ident.por || "sin identidad") + ")" }, 401);
  }

  if (request.method === "GET") {
    const restantes = Math.max(0, LIMITE_DIARIO - await usadas(env, ident.correo));
    if (url.searchParams.get("json")) {
      return json({ ok: true, correo: ident.correo, restantes, limite: LIMITE_DIARIO });
    }
    return new Response(
      "<!doctype html><html lang=es><meta charset=utf-8>"
      + "<meta name=viewport content='width=device-width,initial-scale=1'>"
      + "<title>Preguntar</title>"
      + "<style>body{font:16px/1.6 Georgia,serif;max-width:34em;margin:12vh auto;"
      + "padding:0 1.5em;color:#2b2b2b;background:#faf8f4}a{color:#6b5b2e}</style>"
      + "<h1 style='font-size:1.3em'>Preguntar</h1>"
      + "<p>Sesión iniciada como <strong>" + esc(ident.correo) + "</strong>. "
      + "Le quedan hoy <strong>" + restantes + "</strong> de " + LIMITE_DIARIO + " preguntas.</p>"
      + "<p><a href='/recursos/analisis/'>Volver al análisis de los suttas</a></p>",
      { headers: { "Content-Type": "text/html; charset=utf-8", ...SIN_CACHE } },
    );
  }
  if (request.method !== "POST") return json({ ok: false, error: "sólo GET y POST" }, 405);

  let cuerpo;
  try { cuerpo = await request.json(); } catch (e) {
    return json({ ok: false, error: "el cuerpo no es JSON" }, 400);
  }
  const n = parseInt(String(cuerpo && cuerpo.sutta).replace(/^§/, ""), 10);
  const pregunta = typeof cuerpo.pregunta === "string" ? cuerpo.pregunta.trim() : "";
  const lang = cuerpo.lang === "en" ? "en" : "es";
  if (!pregunta || pregunta.length > MAX_PREGUNTA) {
    return json({ ok: false, error: "la pregunta debe tener entre 1 y " + MAX_PREGUNTA + " caracteres" }, 400);
  }
  let d;
  try { d = await datos(env, url); } catch (e) {
    return json({ ok: false, error: "no se pudieron leer los datos: " + e.message }, 500);
  }
  const fila = d.filas[String(n)];
  if (!fila) return json({ ok: false, error: "no hay fila §" + n + " en el análisis" }, 404);

  const ya = await usadas(env, ident.correo);
  if (ya >= LIMITE_DIARIO) {
    return json({ ok: false, error: "límite diario alcanzado (" + LIMITE_DIARIO + ")", restantes: 0 }, 429);
  }

  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "x-api-key": env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
      "anthropic-beta": "server-side-fallback-2026-07-01",
      "content-type": "application/json",
    },
    body: JSON.stringify(cuerpoDeLaPeticion(env, fila, d.terminos, pregunta, lang)),
  });
  if (!r.ok) {
    // El detalle de la API va al registro del worker, no al navegador.
    console.log("preguntar: la API respondió " + r.status + ": " + (await r.text()).slice(0, 500));
    return json({ ok: false, error: "el modelo no respondió (" + r.status + "); no se ha contado la pregunta" }, 502);
  }
  const m = await r.json();
  if (m.stop_reason === "refusal") {
    return json({ ok: false, error: "el modelo declinó responder; no se ha contado la pregunta" }, 422);
  }
  const respuesta = (m.content || []).filter((b) => b.type === "text").map((b) => b.text).join("").trim();
  if (!respuesta) {
    return json({ ok: false, error: "respuesta vacía; no se ha contado la pregunta" }, 502);
  }
  await kv(env).put(claveDelDia(ident.correo), String(ya + 1), { expirationTtl: 60 * 60 * 48 });
  return json({
    ok: true, respuesta, restantes: LIMITE_DIARIO - ya - 1,
    cortada: m.stop_reason === "max_tokens", modelo: m.model,
  });
}

/* Exportada para el arnés: así se comprueba qué sale hacia la API sin red. */
export function cuerpoDeLaPeticion(env, fila, glosario, pregunta, lang) {
  const de = (o) => (o && typeof o === "object" ? o[lang] || "" : o || "");
  const f = {
    "§": fila.n, sutta: fila.sutta, tr: de(fila.tr), clase: fila.clase, anuvatti: fila.anuvatti,
    roles: fila.roles, ejercicio: fila.ejercicio, respuesta: fila.respuesta,
    ejemplo: fila.ejemplo, nota: de(fila.nota), pdf: fila.pdf,
  };
  const g = fila.terminos.filter((k) => glosario[k]).map((k) => {
    const t = glosario[k], e = t.ejemplo;
    return { termino: t.termino, def: de(t.def),
             ejemplo: e ? { "§": e.n, sutta: e.sutta, nota: de(e.nota), tr: de(e.tr) } : null };
  });
  return {
    model: env.PREGUNTAR_MODELO || MODELO,
    max_tokens: 4000,   // holgura para el razonamiento; el límite de 300 palabras lo pone el prompt
    thinking: { type: "adaptive" },
    output_config: { effort: "low" },
    fallbacks: "default",
    system: [{ type: "text", text: SISTEMA, cache_control: { type: "ephemeral" } }],
    messages: [{
      role: "user",
      content: "<fila>" + JSON.stringify(f) + "</fila>\n<glosario>" + JSON.stringify(g)
        + "</glosario>\n<lengua>" + lang + "</lengua>\n<pregunta>" + pregunta + "</pregunta>",
    }],
  };
}

function esc(s) {
  return String(s).replace(/[&<>"]/g, (c) => (
    { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}
