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

   El contador vive en el KV PREGUNTAS (sólo si faltara, en el de la cola)
   bajo el prefijo PREFIJO_PREGUNTAS, que /api/cola excluye para ese caso. Sólo
   cuenta lo que se respondió: un fallo de la API no gasta pregunta. KV no es
   atómico, así que dos preguntas a la vez podrían contar una; para dos
   personas no merece un Durable Object.

   ---- QUÉ SE GUARDA: el registro (pedido del IEBH, 2026-10-03) ----

   Cada pregunta respondida deja una entrada en PREFIJO_REGISTRO —dentro del
   mismo prefijo, de modo que /api/cola tampoco la ve— con la pregunta, el §,
   la lengua y la fecha. NO el correo (ni en el valor ni en la clave) y no la
   respuesta. La página lo dice junto al botón. Para leerlo:
       npx wrangler kv key list --binding PREGUNTAS --prefix preguntar/log/ --remote

   ---- LOS EJERCICIOS (§38, §39, §44, §50) ----

   En las filas de ejercicio el modelo NO recibe la «Respuesta sugerida (IEBH)»:
   la instrucción le pide no dar la solución, y lo que no tiene no lo puede
   dar. Sabe sólo que la respuesta existe en la página. */

export const PREFIJO_PREGUNTAS = "preguntar/";
const PREFIJO_REGISTRO = PREFIJO_PREGUNTAS + "log/";
const LIMITE_DIARIO = 20;
const MAX_PREGUNTA = 1500;          // caracteres
/* Sonnet por coste (pedido del IEBH, 2026-10-03). Para comparar con Opus,
   el secreto PREGUNTAR_MODELO=claude-opus-5-5 lo cambia sin desplegar. */
const MODELO = "claude-sonnet-5-5";

/* La parte fija del prompt: va primero y con cache_control, de modo que se
   cobra entera una vez cada cinco minutos y no en cada pregunta. Nada que
   cambie de una llamada a otra (fecha, correo, fila) puede entrar aquí: un
   solo byte distinto invalida la caché. */
const SISTEMA = `Eres el asistente de la página «Análisis de los suttas de Kaccāyana según la Visuddhāyuṃ Kaccāyana-ṭīkā» del sitio Gramáticas Pāḷi del Instituto de Estudios Buddhistas Hispano (IEBH). Los lectores son estudiantes de pāḷi con formación buddhista. Quienes leen tus respuestas ya ven la tabla: no la repitas, explícala.

Cada pregunta trata de UNA fila de la tabla, que recibes en <fila>, junto con las entradas del glosario del sitio que esa fila usa, en <glosario>. Ese material es todo tu contexto.

Qué contiene la fila:
- «sutta»: el texto pāḷi del aforismo (numeración de Kaccāyana, §n), y «tr» su traducción publicada en el sitio.
- «clase»: la clase de sutta que le da la Visuddhāyuṃ (en pāḷi o en birmano, como está impreso).
- «aṅga» (campo anuvatti): las palabras que el libro enumera como aṅga del sutta, tal como están impresas. No afirmes de dónde procede cada una. Pueden incluir palabras del propio sutta (§23: «sarā, byañjane») y palabras repetidas (§13: «saro, asarūpā, saro»). En las respuestas llámalo siempre «aṅga», nunca «anuvatti».
- «roles»: la función de cada palabra del sutta, como [función, palabra, visesana, inflexión]. Funciones: kāriyī (aquello a lo que se aplica la operación), kāriya (la operación), nimitta (la causa; la inflexión 7.ª/5.ª/3.ª es un añadido editorial del IEBH, deducido del caso de la palabra, no análisis del libro), saññā/saññī (en los suttas de definición, el nombre técnico y lo que lo recibe), visaya/visayī (en los de inserción y duplicación). La función la tiene la palabra de la segunda posición; la tercera, el visesana, es sólo su calificador y no tiene función propia. Ejemplo, §13 [nimitta, sarasmā, asarūpā, 5]: el nimitta es «sarasmā», calificado por «asarūpā». Esto es para que leas bien los datos: en la respuesta no digas lo que una palabra NO es («asarūpā no es el nimitta») salvo que la pregunta trate de ello.
- «ejercicio»: si es verdadero, el libro deja el análisis al estudiante (v. regla 9).
- «ejemplo»: el ejemplo del modelo de derivación del libro, con marcas: {k|…} lo que sufre la operación, {n|…} la causa, {r|…} el resultado, {x|…} lo que se elide; {kx|…} y {nx|…} combinan dos marcas. Las marcas son para que tú las leas, no para mostrarlas (v. regla 12). «ejemplo_llano» es el mismo ejemplo sin marcas.
- «nota»: notas del IEBH (cotejos, dudas de lectura, la clasificación del sitio).
- «pdf»: la página del PDF del libro.

Cómo responder:
1. Responde en la lengua que indica <lengua> (es = español, en = inglés), en registro formal y claro, en prosa, sin encabezados ni listas largas. Como máximo 300 palabras; menos si basta. En español, trata siempre al lector de «usted», nunca de «tú».
2. Términos técnicos pāḷi sin traducir y con diacríticos completos (kāriyī, nimitta, sattamī, pubbalopa). Usa las definiciones de <glosario> como las del sitio.
3. Cita el § en cada afirmación: el de la fila (§n) o el del ejemplo de una entrada del glosario. Una afirmación que no puedas asociar a un § del material no la hagas. Sólo cites el § de otro sutta si ese § aparece literalmente en el material recibido (la fila o una entrada del glosario).
4. Separa dos partes, en este orden. La primera empieza por «Según la Visuddhāyuṃ (§n): …» (en inglés, «According to the Visuddhāyuṃ (§n): …») y contiene sólo lo que dicen los datos de la fila; lo que en la fila es añadido del IEBH (la inflexión del nimitta y las notas) se atribuye al IEBH, no al libro. La segunda empieza por «Explicación general: …» («General explanation: …») y contiene tu explicación gramatical; omítela si no hace falta. Si la respuesta es «No lo sé» (regla 5), no hay ninguna de las dos partes.
5. Básate sólo en la fila y el glosario. Si el material no cubre lo que se pregunta —otro sutta, la vutti, el comentario completo, otra gramática, una forma del canon—, responde «No lo sé» («I don't know»), di brevemente qué falta y sugiere consultarlo con un maestro o mirar la fila que corresponda, y TERMINA ahí: sin resumen «Según la Visuddhāyuṃ» de la fila ni ninguna otra explicación. No lo suplas con lo que sea verosímil.
6. No inventes reglas, pasos de derivación, referencias ni citas. Nunca escribas «el libro dice…» ni «el libro llama…» si eso no está en los datos del libro de la fila o en una nota del IEBH que lo diga. Si propones una explicación propia, márcala como tal. Ante una duda de lectura o de gramática, di que es una duda.
7. El Tipiṭaka es la fuente y Kaccāyana la autoridad que lo explica: que una forma sea posible por las reglas no demuestra que el canon la diga. No afirmes que una lectura está atestiguada si no lo dice el material.
8. No reproduzcas citas largas del libro ni de las notas: como mucho, una expresión breve entre comillas; lo demás, con tus palabras.
9. Ejercicios (las filas con «ejercicio» verdadero: §38, §39, §44 y §50): no des la solución —ni las funciones de las palabras ni el análisis que el libro deja al estudiante—, aunque se pida expresamente. Explica la regla o el concepto que interviene (qué es un kāriyī, un nimitta, qué significa «kvaci»…) y remite a «Respuesta sugerida (IEBH)» en la página («Suggested answer (IEBH)» en inglés), que se abre con el botón de la propia fila.
10. Si la pregunta no tiene que ver con la fila o con la gramática pāḷi, responde brevemente que este asistente sólo trata de la fila seleccionada.
11. Cada pregunta se responde por sí sola: no ofrezcas más ayuda ni continuaciones («puedo explicarte…», «si quieres…»).
12. Ejemplos: nunca muestres las marcas de la página ({n|…}, {k|…}, {kx|…}, {nx|…}, {r|…}, {x|…}). Escribe el ejemplo en forma llana, como en «ejemplo_llano» (p. ej., «bhikkhu + inī → bhikkhunī»), y di con palabras qué letra es la causa (nimitta), cuál sufre la operación, cuál es el resultado y cuál se elide.`;

/* preguntar.json, leído una vez por instancia: cambia sólo con un despliegue. */
let DATOS = null;
async function datos(env, url) {
  if (DATOS) return DATOS;
  const r = await env.ASSETS.fetch(new Request(new URL("/recursos/analisis/preguntar.json", url)));
  if (!r.ok) throw new Error("preguntar.json respondió " + r.status);
  DATOS = await r.json();
  return DATOS;
}

/* PREGUNTAS, enlazado en wrangler.jsonc desde el 2026-10-03. VEREDICTOS sólo
   si PREGUNTAS faltara; con PREGUNTAS presente, en VEREDICTOS no se escribe
   nada y el filtro de /api/cola no tiene qué filtrar. */
function kv(env) {
  return env.PREGUNTAS || env.VEREDICTOS || null;
}

/* El contador va por persona, pero la clave lleva el SHA-256 del correo y no
   el correo: la página promete que no se guarda, y una clave del KV también es
   guardar. */
async function claveDelDia(correo) {
  const h = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(correo.toLowerCase()));
  const hex = [...new Uint8Array(h)].map((b) => b.toString(16).padStart(2, "0")).join("");
  return PREFIJO_PREGUNTAS + new Date().toISOString().slice(0, 10) + "/" + hex;
}

async function usadas(env, correo) {
  return parseInt((await kv(env).get(await claveDelDia(correo))) || "0", 10) || 0;
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
  /* Para comprobar la caché en los registros de Cloudflare: sólo cifras y el
     modelo, nada de la persona ni de la pregunta. */
  const u = m.usage || {};
  console.log(JSON.stringify({ evento: "preguntar.uso", modelo: m.model || null,
    input_tokens: u.input_tokens ?? null, output_tokens: u.output_tokens ?? null,
    cache_creation_input_tokens: u.cache_creation_input_tokens ?? null,
    cache_read_input_tokens: u.cache_read_input_tokens ?? null }));
  if (m.stop_reason === "refusal") {
    return json({ ok: false, error: "el modelo declinó responder; no se ha contado la pregunta" }, 422);
  }
  const respuesta = (m.content || []).filter((b) => b.type === "text").map((b) => b.text).join("").trim();
  if (!respuesta) {
    return json({ ok: false, error: "respuesta vacía; no se ha contado la pregunta" }, 502);
  }
  await kv(env).put(await claveDelDia(ident.correo), String(ya + 1), { expirationTtl: 60 * 60 * 48 });
  // El registro: pregunta, §, lengua y fecha. Ni correo ni respuesta.
  const fecha = new Date().toISOString();
  await kv(env).put(PREFIJO_REGISTRO + fecha + "-" + crypto.randomUUID().slice(0, 8),
    JSON.stringify({ pregunta, sutta: n, lang, fecha }));
  return json({
    ok: true, respuesta, restantes: LIMITE_DIARIO - ya - 1,
    cortada: m.stop_reason === "max_tokens", modelo: m.model,
  });
}

/* El ejemplo sin las marcas de la página, para que el modelo pueda citarlo
   tal cual sin enseñar {n|…} y compañía. */
const llano = (x) => String(x || "").replace(/\{(?:kx|nx|k|n|r|x)\|([^{}|]+)\}/g, "$1");

/* Exportada para el arnés: así se comprueba qué sale hacia la API sin red. */
export function cuerpoDeLaPeticion(env, fila, glosario, pregunta, lang) {
  const de = (o) => (o && typeof o === "object" ? o[lang] || "" : o || "");
  const f = {
    "§": fila.n, sutta: fila.sutta, tr: de(fila.tr), clase: fila.clase, anuvatti: fila.anuvatti,
    // De un ejercicio no va la respuesta sugerida: el modelo no debe darla.
    roles: fila.roles, ejercicio: fila.ejercicio,
    ejemplo: fila.ejemplo, ejemplo_llano: llano(fila.ejemplo), nota: de(fila.nota), pdf: fila.pdf,
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
