// Serves the library index from R2.
//
// Cache policy follows the playground's hard-won rule: only a name that carries
// a fingerprint may be cached, and index.json carries none -- it is rewritten in
// place on every regeneration. Caching it would hand people a catalogue that
// disagrees with what pip can actually install, with no error to show for it.
//
// CORS is open because the catalogue page and the IDE plugins read this from a
// different origin, and the file is public data with no credentials attached.

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
  "Access-Control-Max-Age": "86400",
};

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: CORS });
    }
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method not allowed", { status: 405, headers: CORS });
    }

    const url = new URL(request.url);
    const key = url.pathname === "/" ? "index.json" : url.pathname.slice(1);

    const object = await env.BUCKET.get(key);
    if (object === null) {
      return new Response("Not found", { status: 404, headers: CORS });
    }

    const headers = new Headers(CORS);
    object.writeHttpMetadata(headers);
    headers.set("etag", object.httpEtag);
    headers.set("cache-control", "no-cache");
    if (!headers.has("content-type")) {
      headers.set("content-type", "application/json; charset=utf-8");
    }

    return new Response(request.method === "HEAD" ? null : object.body, { headers });
  },
};
