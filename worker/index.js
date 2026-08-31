/* El worker del sitio: sirve site/ tal cual, y añade UNA cosa — la cola de
   veredictos del modo revisión (automatización de grado medio, decisión del
   IEBH, 2026-08-28).

   POST /api/veredictos          el navegador del revisor deja el .md exportado
                                 en la cola (KV). EXIGE IDENTIDAD si Access
                                 está configurado (v. abajo); si no lo está,
                                 sigue abierta como hasta el 2026-08-31 y la
                                 entrada queda marcada «sin identidad».
   GET  /api/veredictos?clave=…  lista la cola (sólo con la clave).
   GET  …&resumen=1              id, cuenta e identidad, SIN los .md.
   DELETE …?clave=…&id=…         borra una entrada ya incorporada.

   La clave de LECTURA vive como secreto del worker (CLAVE_VEREDICTOS); la
   cola, en el KV VEREDICTOS. Cómo crearlos: docs/solucionador/automatizacion.md.

   ---- QUIÉN ESCRIBE: Cloudflare Access (pedido de Angel, 2026-08-31) ----

   Hasta hoy la cola era un buzón ANÓNIMO: cualquiera podía dejar un .md y no
   quedaba constancia de quién. Peor que eso, el .md exportado trae ya escrita
   la orden de incorporación con «--fuente "IEBH, …"», de modo que lo de un
   desconocido entraba al proyecto rotulado como del IEBH. Eso rompe el
   principio 4 —atribuir la procedencia— en silencio, que es la peor manera.

   Ahora el POST pide el JWT que Cloudflare Access pone en la cabecera
   «Cf-Access-Jwt-Assertion» (o en la galleta CF_Authorization). El worker
   verifica la FIRMA contra las claves públicas del equipo, comprueba el «aud»
   de la aplicación y la caducidad, y guarda el correo verificado junto a la
   entrada. Quien firma ve entonces de quién es cada veredicto, y traer_
   veredictos.py saca de ahí el «--fuente» en vez de suponerlo.

   Dos variables lo gobiernan, y MIENTRAS NO ESTÉN PUESTAS TODO SIGUE IGUAL
   —a propósito: desplegar esto no debe romper la cola que ya funciona—:

     ACCESO_EQUIPO   p. ej. «mi-equipo.cloudflareaccess.com»
     ACCESO_AUD      el Application Audience (AUD) tag de la aplicación

   El repertorio de quién puede entrar NO vive aquí: vive en la política de
   Access, que se edita en el panel sin tocar código ni volver a desplegar.
   Es la diferencia con una contraseña compartida: se revoca a uno solo. */

/* ---- POR QUÉ HAY DOS RUTAS Y NO UNA (2026-08-31, la misma tarde) ----

   Access protege una RUTA, y la protege para TODOS los métodos. Se puso
   delante de /api/veredictos pensando sólo en el POST del navegador, y con
   ello quedó fuera también el GET — es decir, traer_veredictos.py, que corre
   en la Mac sin sesión de navegador y recibía el HTML del login en vez del
   JSON de la cola. Con una sola ruta no hay manera: Access no distingue
   métodos.

   De modo que la puerta del navegador y la puerta de quien recoge se separan,
   y cada una lleva la cerradura que le toca:

     POST   /api/veredictos   ← Access delante: IDENTIDAD (quién deja algo)
     GET    /api/cola?clave=  ← sin Access: la CLAVE de siempre (quién recoge)
     DELETE /api/cola?clave=  ← ídem
     GET    /api/entrar       ← Access delante: sólo sirve para iniciar sesión

   No es un apaño: es la separación correcta. Al buzón se echa una carta
   diciendo quién eres; el buzón se abre con llave. Son dos cosas distintas y
   nunca fueron la misma.

   /api/entrar existe porque la sesión de Access se obtiene visitando una ruta
   protegida, y la página del solucionador NO lo está —ni debe estarlo: el
   estudiante entra sin cuenta—. Sin ella, el revisor tendría que visitar a
   mano el endpoint del POST para que le pidieran la contraseña.

   OJO: /api/entrar tiene que estar en la MISMA aplicación de Access que
   /api/veredictos, como segundo «destination». La galleta de Access vale por
   aplicación: si fuera otra aplicación, iniciar sesión ahí no abriría el POST. */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/veredictos") {
      return veredictos(request, env, url);
    }
    if (url.pathname === "/api/cola") {
      return cola(request, env, url);
    }
    if (url.pathname === "/api/entrar") {
      return entrar(request, env);
    }
    return env.ASSETS.fetch(request);
  },
};

/* La página de «ya está» tras el login. Si se ve, Access dejó pasar: eso es
   todo lo que tiene que decir, y lo dice en español como el resto del sitio. */
async function entrar(request, env) {
  const ident = await identidad(request, env);
  /* «?json=1» para que la página pregunte si hay sesión sin sacar al lector
     de donde está. Va en ESTA ruta y no en otra a propósito: Access protege
     rutas, de modo que compartirla es compartir la protección — sin sesión,
     Cloudflare responde con su redirección antes de que el worker exista, y
     eso mismo es la respuesta que la página necesita. */
  if (new URL(request.url).searchParams.get("json")) {
    return Response.json(
      { correo: ident.correo || null, configurado: ident.configurado },
      { headers: { "Cache-Control": "no-store" } },
    );
  }
  const quien = ident.correo
    ? "Sesión iniciada como <strong>" + esc(ident.correo) + "</strong>."
    : (ident.configurado
      ? "No se pudo leer la identidad (" + esc(ident.por || "") + ")."
      : "Access no está configurado: la cola sigue abierta.");
  return new Response(
    "<!doctype html><html lang=es><meta charset=utf-8>"
    + "<meta name=viewport content='width=device-width,initial-scale=1'>"
    + "<title>Sesión de revisión</title>"
    + "<style>body{font:16px/1.6 Georgia,serif;max-width:34em;margin:12vh auto;"
    + "padding:0 1.5em;color:#2b2b2b;background:#faf8f4}"
    + "a{color:#6b5b2e}code{background:#efece5;padding:.1em .3em}</style>"
    + "<h1 style='font-size:1.3em'>Sesión de revisión</h1><p>" + quien + "</p>"
    + "<p>Ya puede volver al solucionador y pulsar «Enviar». "
    + "La sesión dura lo que diga la aplicación de Access (24 horas).</p>"
    + "<p><a href='/recursos/solucionador/'>Volver al solucionador</a></p>",
    { headers: {
      "Content-Type": "text/html; charset=utf-8",
      // Esta página es un DIAGNÓSTICO: dice el estado de ahora mismo. Sin
      // esto el navegador la cachea con su heurística y enseña el estado de
      // hace un rato — que al depurar es peor que no enseñar nada, porque
      // parece que un arreglo no ha servido cuando sí ha servido.
      "Cache-Control": "no-store, must-revalidate",
    } },
  );
}

function esc(s) {
  return String(s).replace(/[&<>"]/g, (c) => (
    { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

async function veredictos(request, env, url) {
  if (!env.VEREDICTOS) {
    return new Response("la cola no está configurada", { status: 503 });
  }
  if (request.method === "POST") {
    // QUIÉN, antes que QUÉ: si Access está configurado, sin identidad
    // verificada no se encola nada. El 401 lleva un cuerpo que la página
    // sabe leer para decir «inicie sesión» en vez de «no hay red».
    const ident = await identidad(request, env);
    if (ident.configurado && !ident.correo) {
      return new Response("hace falta iniciar sesión (" + ident.por + ")", {
        status: 401,
      });
    }
    const md = await request.text();
    if (!md || md.length > 65536) {
      return new Response("tamaño fuera de rango", { status: 400 });
    }
    // Cordura mínima: tiene que parecer una exportación del modo revisión.
    if (!md.includes("VEREDICTO:") && !md.includes("## Observaciones del revisor")) {
      return new Response("no parece una exportación de veredictos", { status: 400 });
    }
    const id = new Date().toISOString().replace(/[:.]/g, "-")
      + "-" + crypto.randomUUID().slice(0, 8);
    // La cuenta de veredictos va como METADATO del propio KV, para que
    // «--solo-mirar» pueda responder con list() a secas, sin leer ni un
    // .md (2026-08-30). list() la devuelve junto con la clave.
    const n = (md.match(/VEREDICTO:/g) || []).length;
    // 90 días de vida: la cola es un buzón, no un archivo. Lo incorporado
    // vive en casos-reportados.json; lo no recogido en 90 días caduca.
    await env.VEREDICTOS.put(id, md, {
      expirationTtl: 60 * 60 * 24 * 90,
      // «correo: null» dice «esta entrada es anónima», y se distingue de las
      // anteriores al 2026-08-31, que no traen el campo en absoluto.
      metadata: { n, correo: ident.correo || null, cuando: new Date().toISOString() },
    });
    return Response.json({ ok: true, id, correo: ident.correo || null });
  }
  // Aquí sólo se DEJA. Leer y vaciar es /api/cola, y por la razón dicha
  // arriba: Access no distingue métodos y dejaría fuera a quien recoge.
  return new Response("sólo POST: para leer la cola, /api/cola", {
    status: 405,
  });
}

/* Leer y vaciar la cola. SIN Access delante, a propósito: quien recoge es un
   guion que corre en la Mac, no un navegador, y no tiene con qué iniciar
   sesión. La cerradura aquí es la de siempre, CLAVE_VEREDICTOS, que es
   exactamente la que protegía esto antes del login y no ha cambiado. */
async function cola(request, env, url) {
  if (!env.VEREDICTOS) {
    return new Response("la cola no está configurada", { status: 503 });
  }
  const clave = url.searchParams.get("clave") || "";
  // Dos fallos distintos, dos respuestas distintas (2026-08-29: un 403
  // indistinguible costó una tarde). Decir «no hay clave configurada» no
  // regala nada a nadie: sin la clave igual no se puede leer ni borrar.
  if (!env.CLAVE_VEREDICTOS) {
    return new Response(
      "el worker desplegado no tiene CLAVE_VEREDICTOS configurada", {
        status: 503 });
  }
  if (clave !== env.CLAVE_VEREDICTOS) {
    return new Response("la clave no coincide", { status: 403 });
  }
  if (request.method === "GET") {
    // list() pagina de 1.000 en 1.000: con cursor se recorre entera. La cola
    // nunca ha llegado ahí, pero una cola sin vaciar durante meses sí podría,
    // y media cola sería peor que una cola lenta.
    const claves = [];
    let cursor;
    for (;;) {
      const lista = await env.VEREDICTOS.list(cursor ? { cursor } : {});
      claves.push(...lista.keys);
      if (lista.list_complete) break;
      cursor = lista.cursor;
    }
    // El resumen no lee NINGÚN valor: la cuenta viaja como metadato desde
    // que se encoló. Las entradas anteriores al 2026-08-30 no lo llevan, y
    // ésas —y sólo ésas— hay que leerlas para contarlas.
    if (url.searchParams.get("resumen")) {
      const viejas = claves.filter((k) => !k.metadata || k.metadata.n === undefined);
      const contadas = new Map(
        (await Promise.all(viejas.map(async (k) => [
          k.name,
          ((await env.VEREDICTOS.get(k.name)) || "").split("VEREDICTO:").length - 1,
        ]))),
      );
      return Response.json({
        ok: true,
        resumen: true,
        veredictos: claves.map((k) => ({
          id: k.name,
          n: k.metadata && k.metadata.n !== undefined
            ? k.metadata.n : contadas.get(k.name),
          // undefined = entrada anterior a la identidad; null = anónima.
          correo: k.metadata ? (k.metadata.correo ?? undefined) : undefined,
        })),
      });
    }
    // Y el listado completo, en PARALELO. Estaba dentro de un for con await,
    // de modo que el tiempo era la suma de todas las lecturas del KV, una
    // detrás de otra (2026-08-30, pedido de Angel: «¿hay manera de que
    // termine antes?»). Con Promise.all es el de la más lenta, no la suma.
    const out = await Promise.all(claves.map(async (k) => ({
      id: k.name,
      correo: k.metadata ? (k.metadata.correo ?? undefined) : undefined,
      md: await env.VEREDICTOS.get(k.name),
    })));
    return Response.json({ ok: true, veredictos: out });
  }
  if (request.method === "DELETE") {
    const id = url.searchParams.get("id");
    if (!id) return new Response("falta id", { status: 400 });
    await env.VEREDICTOS.delete(id);
    return Response.json({ ok: true, id });
  }
  return new Response("método", { status: 405 });
}

/* ---------------- La identidad de Cloudflare Access ----------------

   Verificar un JWT es comprobar tres cosas, y las tres hacen falta:
   la FIRMA (que lo emitió el equipo y no un cualquiera), el AUD (que es para
   ESTA aplicación y no para otra del mismo equipo) y la CADUCIDAD. Saltarse
   el aud es el descuido clásico: un token legítimo de otra aplicación del
   mismo Access valdría aquí. */

/* La caché va POR DOMINIO, no en una variable suelta. Si ACCESO_EQUIPO
   cambia, las claves del anterior no valen, y una caché sin llave las serviría
   igual — con lo cual un dominio mal escrito «funcionaría» mientras durase la
   hora, que es la peor forma de fallar: la intermitente. */
const CLAVES = new Map();   // dominio → { keys, cuando }

/* El valor de ACCESO_EQUIPO se escribe a mano en un «wrangler secret put», y
   lo que sale del panel de Cloudflare es una URL. Pegar
   «https://holy-term-49b9.cloudflareaccess.com» era lo natural y daba
   «https://https://…», que falla sin decir por qué (pasó el 2026-08-31).
   Se admite el dominio con esquema, sin esquema, con barra final o con
   espacios: es un dominio, y exigir una forma exacta de escribirlo no protege
   nada — sólo cuesta una tarde. */
function dominioDelEquipo(v) {
  return String(v).trim()
    .replace(/^https?:\/\//i, "")
    .replace(/\/.*$/, "");
}

async function clavesDelEquipo(equipo) {
  const dom = dominioDelEquipo(equipo);
  // Una hora de caché: Access rota las claves, y pedirlas en cada POST sería
  // una llamada de red por veredicto.
  const y = CLAVES.get(dom);
  if (y && Date.now() - y.cuando < 3600e3) return y.keys;
  const r = await fetch("https://" + dom + "/cdn-cgi/access/certs");
  if (!r.ok) {
    throw new Error("las claves de " + dom + " respondieron " + r.status);
  }
  const keys = (await r.json()).keys || [];
  CLAVES.set(dom, { keys, cuando: Date.now() });
  return keys;
}

function deB64Url(s) {
  const t = s.replace(/-/g, "+").replace(/_/g, "/");
  const bin = atob(t + "=".repeat((4 - (t.length % 4)) % 4));
  return Uint8Array.from(bin, (c) => c.charCodeAt(0));
}

function jsonDeB64Url(s) {
  return JSON.parse(new TextDecoder().decode(deB64Url(s)));
}

function galleta(request, nombre) {
  const c = request.headers.get("Cookie") || "";
  const m = c.match(new RegExp("(?:^|;\\s*)" + nombre + "=([^;]+)"));
  return m ? m[1] : null;
}

async function identidad(request, env) {
  const equipo = env.ACCESO_EQUIPO, aud = env.ACCESO_AUD;
  // Sin configurar: la cola sigue como estaba. Es deliberado — desplegar
  // este worker no debe cerrar la puerta antes de que exista la llave.
  if (!equipo || !aud) return { configurado: false, correo: null };
  /* Los dos secretos se escriben a ciegas —wrangler enmascara lo que se
     teclea— y se pusieron cambiados el 2026-08-31: el AUD en ACCESO_EQUIPO.
     El síntoma era un 403 al pedir las claves, que no dice lo que pasa. Se
     distinguen por la forma y no cuesta nada mirarla: el equipo es un nombre
     de máquina, con puntos; el AUD son 64 dígitos hexadecimales y ninguno. */
  const dom = dominioDelEquipo(equipo);
  if (!dom.includes(".")) {
    return { configurado: true, correo: null,
             por: /^[0-9a-f]{32,}$/i.test(dom)
               ? "ACCESO_EQUIPO tiene lo que parece el AUD; se esperaba el "
                 + "dominio del equipo (algo.cloudflareaccess.com). "
                 + "¿Están cambiados los dos secretos?"
               : "ACCESO_EQUIPO no parece un dominio: «" + dom + "»" };
  }
  const tok = request.headers.get("Cf-Access-Jwt-Assertion")
    || galleta(request, "CF_Authorization");
  if (!tok) return { configurado: true, correo: null, por: "sin token" };
  const p = tok.split(".");
  if (p.length !== 3) return { configurado: true, correo: null, por: "token mal formado" };
  let cab, cuerpo;
  try {
    cab = jsonDeB64Url(p[0]);
    cuerpo = jsonDeB64Url(p[1]);
  } catch (e) {
    return { configurado: true, correo: null, por: "token ilegible" };
  }
  let jwk;
  try {
    jwk = (await clavesDelEquipo(equipo)).find((k) => k.kid === cab.kid);
  } catch (e) {
    // Con el motivo DENTRO: un «no se pudo» a secas manda a adivinar, y lo
    // que se adivina mal cuesta más que lo que se lee. Esto sólo lo ve quien
    // ya pasó por Access, de modo que decirlo no regala nada.
    return { configurado: true, correo: null,
             por: "no se pudo consultar Access — " + (e && e.message ? e.message : e) };
  }
  if (!jwk) return { configurado: true, correo: null, por: "kid desconocido" };
  const clave = await crypto.subtle.importKey(
    "jwk",
    { kty: jwk.kty, n: jwk.n, e: jwk.e, alg: "RS256", ext: true },
    { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" },
    false,
    ["verify"],
  );
  const ok = await crypto.subtle.verify(
    "RSASSA-PKCS1-v1_5",
    clave,
    deB64Url(p[2]),
    new TextEncoder().encode(p[0] + "." + p[1]),
  );
  if (!ok) return { configurado: true, correo: null, por: "firma inválida" };
  const auds = Array.isArray(cuerpo.aud) ? cuerpo.aud : [cuerpo.aud];
  if (!auds.includes(aud)) return { configurado: true, correo: null, por: "aud distinto" };
  if (!cuerpo.exp || cuerpo.exp * 1000 < Date.now()) {
    return { configurado: true, correo: null, por: "caducado" };
  }
  return { configurado: true, correo: cuerpo.email || cuerpo.sub || "(sin correo)" };
}
