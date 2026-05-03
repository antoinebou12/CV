/**
 * Markdown negotiation for site root (Markdown for Agents).
 * Requires env.SITE_REPO (e.g. "CV") for GitHub Pages project-site paths.
 */
async function originFetch(request, env, targetUrl) {
  const req = new Request(targetUrl.toString(), { method: "GET", headers: request.headers });
  if (env.ASSETS && typeof env.ASSETS.fetch === "function") {
    return env.ASSETS.fetch(req);
  }
  return fetch(req, { cf: { cacheEverything: true } });
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const accept = request.headers.get("Accept") || "";
    const wantsMarkdown =
      accept.includes("text/markdown") || accept.includes("text/x-markdown");

    if (wantsMarkdown && url.pathname === "/") {
      const repo = (env.SITE_REPO || "CV").replace(/^\/+|\/+$/g, "");
      const candidates = [
        new URL(`/${repo}/blog/agent/home.md`, url.origin),
        new URL("/blog/agent/home.md", url.origin),
      ];

      for (const target of candidates) {
        const mdRes = await originFetch(request, env, target);
        if (mdRes.ok) {
          const body = await mdRes.text();
          return new Response(body, {
            status: 200,
            headers: {
              "Content-Type": "text/markdown; charset=utf-8",
              "Cache-Control": "public, max-age=300",
            },
          });
        }
      }
    }

    // Pages: bind the static deployment as `ASSETS`. Otherwise forward to the origin fetch().
    if (env.ASSETS && typeof env.ASSETS.fetch === "function") {
      return env.ASSETS.fetch(request);
    }
    return fetch(request);
  },
};
