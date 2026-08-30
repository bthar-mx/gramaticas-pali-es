/* El worker del sitio: sirve site/ tal cual, y añade UNA cosa — la cola de
   veredictos del modo revisión (automatización de grado medio, decisión del
   IEBH, 2026-08-28).

   POST /api/veredictos          el navegador del revisor deja el .md exportado
                                 en la cola (KV). Sin clave: la cola sólo se
                                 LEE con la clave, y nada entra al proyecto
                                 sin pasar por herramientas/traer_veredictos.py,
                                 el incorporador, los arneses y la firma.
   GET  /api/veredictos?clave=…  lista la cola (sólo con la clave).
   GET  …&resumen=1              id y cuenta de veredictos, SIN los .md.
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
    // La cuenta de veredictos va como METADATO del propio KV, para que
    // «--solo-mirar» pueda responder con list() a secas, sin leer ni un
    // .md (2026-08-30). list() la devuelve junto con la clave.
    const n = (md.match(/VEREDICTO:/g) || []).length;
    // 90 días de vida: la cola es un buzón, no un archivo. Lo incorporado
    // vive en casos-reportados.json; lo no recogido en 90 días caduca.
    await env.VEREDICTOS.put(id, md, {
      expirationTtl: 60 * 60 * 24 * 90,
      metadata: { n },
    });
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
        })),
      });
    }
    // Y el listado completo, en PARALELO. Estaba dentro de un for con await,
    // de modo que el tiempo era la suma de todas las lecturas del KV, una
    // detrás de otra (2026-08-30, pedido de Angel: «¿hay manera de que
    // termine antes?»). Con Promise.all es el de la más lenta, no la suma.
    const out = await Promise.all(claves.map(async (k) => ({
      id: k.name,
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
