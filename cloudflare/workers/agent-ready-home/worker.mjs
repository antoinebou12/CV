/**
 * Markdown negotiation for site root (Markdown for Agents).
 * Proxies apex /sitemap.xml and /robots.txt to GitHub Pages project-site paths.
 * Requires env.SITE_REPO (e.g. "CV") for GitHub Pages project-site paths.
 */
async function originFetch(request, env, targetUrl) {
  const method = request.method === "HEAD" ? "HEAD" : "GET";
  const req = new Request(targetUrl.toString(), { method, headers: request.headers });
  if (env.ASSETS && typeof env.ASSETS.fetch === "function") {
    return env.ASSETS.fetch(req);
  }
  return fetch(req, { cf: { cacheEverything: true } });
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const repo = (env.SITE_REPO || "CV").replace(/^\/+|\/+$/g, "");

    const discoveryMap = {
      "/sitemap.xml": `/${repo}/sitemap.xml`,
      "/robots.txt": `/${repo}/robots.txt`,
    };
    const underRepo = discoveryMap[url.pathname];
    if (underRepo && (request.method === "GET" || request.method === "HEAD")) {
      const proxied = await originFetch(request, env, new URL(underRepo, url.origin));
      return proxied;
    }

    const accept = request.headers.get("Accept") || "";
    const wantsMarkdown =
      accept.includes("text/markdown") || accept.includes("text/x-markdown");

    if (wantsMarkdown && url.pathname === "/") {
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
