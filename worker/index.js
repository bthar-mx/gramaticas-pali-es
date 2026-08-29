/* El worker del sitio: sirve site/ tal cual, y añade UNA cosa — la cola de
   veredictos del modo revisión (automatización de grado medio, decisión del
   IEBH, 2026-08-28).

   POST /api/veredictos          el navegador del revisor deja el .md exportado
                                 en la cola (KV). Sin clave: la cola sólo se
                                 LEE con la clave, y nada entra al proyecto
                                 sin pasar por herramientas/traer_veredictos.py,
                                 el incorporador, los arneses y la firma.
   GET  /api/veredictos?clave=…  lista la cola (sólo con la clave).
   DELETE …?clave=…&id=…         borra una entrada ya incorporada.

   La clave vive como secreto del worker (CLAVE_VEREDICTOS); la cola, en el
   KV VEREDICTOS. Cómo crearlos: docs/solucionador/automatizacion.md. */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/veredictos") {
      return veredictos(request, env, url);
    }
    return env.ASSETS.fetch(request);
  },
};

async function veredictos(request, env, url) {
  if (!env.VEREDICTOS) {
    return new Response("la cola no está configurada", { status: 503 });
  }
  if (request.method === "POST") {
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
    // 90 días de vida: la cola es un buzón, no un archivo. Lo incorporado
    // vive en casos-reportados.json; lo no recogido en 90 días caduca.
    await env.VEREDICTOS.put(id, md, { expirationTtl: 60 * 60 * 24 * 90 });
    return Response.json({ ok: true, id });
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
    const lista = await env.VEREDICTOS.list();
    const out = [];
    for (const k of lista.keys) {
      out.push({ id: k.name, md: await env.VEREDICTOS.get(k.name) });
    }
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
