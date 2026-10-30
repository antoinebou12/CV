/**
 * Markdown negotiation for site root (Markdown for Agents).
 * Proxies apex /sitemap.xml and /robots.txt to GitHub Pages project-site paths.
 * Attaches baseline security headers on responses (forces CSP; fills gaps otherwise).
 * Requires env.SITE_REPO (e.g. "CV") for GitHub Pages project-site paths.
 */

/** Always set — production currently lacks CSP. Keep in sync with hugo/static/_headers. */
const FORCE_SECURITY_HEADERS = {
  "Content-Security-Policy":
    "default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; form-action 'self'; upgrade-insecure-requests; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://maxcdn.bootstrapcdn.com https://cdnjs.cloudflare.com; font-src 'self' data: https://fonts.gstatic.com https://cdnjs.cloudflare.com https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; media-src 'self' https:; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://graphquon.github.io https://lens.snap.com; connect-src 'self' https://static.cloudflareinsights.com https://mapmyvisitors.com https://cdn.clustrmaps.com; worker-src 'self' blob:",
};

/** Set only when the origin/CDN did not already send them. */
const FILL_SECURITY_HEADERS = {
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "DENY",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Permissions-Policy":
    "geolocation=(), microphone=(), camera=(), payment=(), usb=(), interest-cohort=()",
  "Cross-Origin-Opener-Policy": "same-origin-allow-popups",
};

function withSecurityHeaders(response) {
  const headers = new Headers(response.headers);
  for (const [key, value] of Object.entries(FORCE_SECURITY_HEADERS)) {
    headers.set(key, value);
  }
  for (const [key, value] of Object.entries(FILL_SECURITY_HEADERS)) {
    if (!headers.has(key)) headers.set(key, value);
  }
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}

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
      return withSecurityHeaders(proxied);
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
          const headers = new Headers({
            "Content-Type": "text/markdown; charset=utf-8",
            "Cache-Control": "public, max-age=300",
          });
          for (const [key, value] of Object.entries(FORCE_SECURITY_HEADERS)) {
            headers.set(key, value);
          }
          for (const [key, value] of Object.entries(FILL_SECURITY_HEADERS)) {
            headers.set(key, value);
          }
          return new Response(body, { status: 200, headers });
        }
      }
    }

    // Pages: bind the static deployment as `ASSETS`. Otherwise forward to the origin fetch().
    if (env.ASSETS && typeof env.ASSETS.fetch === "function") {
      return withSecurityHeaders(await env.ASSETS.fetch(request));
    }
    return withSecurityHeaders(await fetch(request));
  },
};
