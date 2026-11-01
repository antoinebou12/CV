# WebMCP for the CV and Hugo

Run `scripts/dev/start-webmcp.ps1` from PowerShell. It starts the local preview if
needed and opens the CV and Hugo in a separate Chrome profile with native WebMCP
enabled. Use `-Browser Edge` for Edge, `-Build` to rebuild `docs/`, or `-Port 8935`
to use another local port. It does not change your everyday browser profile.

The launcher requires an installed Chrome or Edge, Python managed by `uv`, and a
local `docs/` build. Both installed browsers were tested with native tools on this
PC (Chrome 154 and Edge 157). The preview listens only on `127.0.0.1`; localhost
is a trustworthy context. Public deployments use HTTPS.

The current browser API is `document.modelContext`. The page registers four tools:

| Tool | Purpose |
| --- | --- |
| `website_get_outline` | Read page metadata and heading identifiers. |
| `website_read_section` | Read public text, including collapsed sections. |
| `website_search_page` | Search sections in the current CV, article, or project. |
| `website_show_section` | Open ancestor disclosures and focus a heading. |

The first three tools only read public page content. The last changes the visible
page. Inputs are validated; invalid section IDs return an actionable error.
Tools are unregistered with an AbortSignal on page exit. Browsers without native
WebMCP keep the ordinary page behavior. There is no injected polyfill or backend
MCP endpoint, and no API key is needed.

In the enabled browser, open DevTools and run:

```js
const tools = await document.modelContext.getTools();
console.table(tools.map(tool => ({ name: tool.name, description: tool.description })));
```

A browser agent must support WebMCP to discover these tools. This setup does not
install an AI assistant or grant an extension access to your other tabs.
The in-app preview browser has its own feature settings; use the dedicated
launcher when testing native browser support.

Native tests (from `tools/ux-audit`, with the preview running):

```powershell
$env:E2E_URL = 'http://127.0.0.1:8934'
$env:E2E_PREFIX = '/CV'
$env:PLAYWRIGHT_BROWSERS_PATH = "$env:LOCALAPPDATA/ms-playwright"
node node_modules/@playwright/test/cli.js test --config playwright.e2e.config.ts webmcp.spec.ts
```

References: [Chrome WebMCP guide](https://developer.chrome.com/docs/modern-web-guidance/guides/webmcp/webmcp)
and [imperative API](https://developer.chrome.com/docs/modern-web-guidance/guides/webmcp/agentic-javascript-tools).
