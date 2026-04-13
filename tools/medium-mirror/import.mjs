/**
 * Medium → Hugo page bundles. See README.md.
 */
import * as fs from "node:fs/promises";
import * as path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";
import * as cheerio from "cheerio";
import TurndownService from "turndown";
import { gfm } from "turndown-plugin-gfm";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const ROOT = path.resolve(__dirname, "..", "..");
const POSTS_DIR = path.join(ROOT, "hugo", "content", "posts");
const URLS_PATH = path.join(__dirname, "urls.json");

const USER_AGENT =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36";

const CT_EXT = {
  "image/jpeg": ".jpg",
  "image/jpg": ".jpg",
  "image/png": ".png",
  "image/webp": ".webp",
  "image/gif": ".gif",
  "image/svg+xml": ".svg",
};

function pickSrcsetUrl(srcset) {
  if (!srcset || typeof srcset !== "string") return null;
  const parts = srcset.split(",").map((s) => s.trim().split(/\s+/));
  let best = null;
  let bestW = 0;
  for (const chunk of parts) {
    const url = chunk[0];
    const w = chunk[1];
    const m = w?.match(/(\d+)w/);
    const width = m ? parseInt(m[1], 10) : 0;
    if (url && width >= bestW) {
      bestW = width;
      best = url;
    }
  }
  return best;
}

function resolveUrl(base, href) {
  try {
    return new URL(href, base).href;
  } catch {
    return null;
  }
}

function extFromUrl(u) {
  try {
    const p = new URL(u).pathname;
    const base = path.basename(p).split("?")[0];
    const m = base.match(/\.(webp|jpe?g|png|gif|svg)(\b|$)/i);
    return m ? `.${m[1].toLowerCase().replace("jpeg", "jpg")}` : ".bin";
  } catch {
    return ".bin";
  }
}

function stripNoise($, $root) {
  $root.find("script, style, noscript").remove();
  $root.find("aside").remove();
  $root.find("iframe").remove();
  $root.find("button").remove();
  $root.find('[data-testid="upgradeButtonLock"]').parent().remove();
  $root.find("a[href*='medium.com/membership']").closest("div").remove();
  $root.find('a[href*="/m/signin"]').remove();
  $root.find('a[href*="medium.com/plans"]').remove();
  $root.find("a[href*='source=post_page---byline']").remove();
  $root.find("a[href*='clap_footer'], a[href*='bookmark_footer']").remove();
}

function yamlEscape(s) {
  if (/[:#\n"|']/.test(s)) return JSON.stringify(s);
  return s;
}

/**
 * Prefer real story blocks (paragraphs, code, figures) inside <article> to avoid Medium chrome.
 */
async function extractArticleHtml(page, pageUrl) {
  await page.goto(pageUrl, {
    waitUntil: "domcontentloaded",
    timeout: 90_000,
  });
  await page.waitForTimeout(2500);
  await page.evaluate(() => {
    window.scrollTo(0, document.body.scrollHeight);
  });
  await page.waitForTimeout(1500);

  const html = await page.evaluate(() => {
    const article = document.querySelector("article");
    const root = article || document.body;

    const blockSel = [
      "p[data-selectable-paragraph]",
      "p.pw-post-body-paragraph",
      "pre",
      "figure",
      "h2",
      "h3",
      "h4",
      "ul",
      "ol",
      "blockquote",
      "hr",
      "table",
    ].join(", ");

    const nodes = root.querySelectorAll(blockSel);
    const wrap = document.createElement("div");

    nodes.forEach((el) => {
      if (el.closest("figure") && el.tagName.toLowerCase() !== "figure") {
        return;
      }
      const t = (el.innerText || "").trim();
      if (
        el.tagName.toLowerCase() === "p" &&
        t.length < 2 &&
        !el.querySelector("img")
      ) {
        return;
      }
      wrap.appendChild(el.cloneNode(true));
    });

    if (wrap.children.length >= 3) {
      return wrap.innerHTML;
    }

    /* Fallback: largest section inside article */
    let best = null;
    let bestScore = 0;
    const sections = root.querySelectorAll("section, div");
    sections.forEach((node) => {
      const score = (node.innerText || "").trim().length;
      if (score > bestScore) {
        bestScore = score;
        best = node;
      }
    });
    return best?.innerHTML || article?.innerHTML || null;
  });

  return html;
}

async function downloadImage(request, absoluteUrl) {
  const res = await request.get(absoluteUrl, {
    headers: { "User-Agent": USER_AGENT },
    timeout: 60_000,
  });
  if (!res.ok()) {
    console.warn(`  skip image ${absoluteUrl} status ${res.status()}`);
    return { ok: false, body: null, ext: null };
  }
  const ct = (res.headers()["content-type"] || "").split(";")[0].trim();
  const ext = CT_EXT[ct] || extFromUrl(absoluteUrl);
  const body = await res.body();
  return { ok: true, body, ext };
}

async function cleanBundleImages(bundleDir) {
  const names = await fs.readdir(bundleDir).catch(() => []);
  await Promise.all(
    names
      .filter((n) => n.startsWith("img-"))
      .map((n) => fs.unlink(path.join(bundleDir, n)).catch(() => {})),
  );
}

async function processEntry(browser, entry) {
  const { slug, url, title, date, tags, indexFile, lang } = entry;
  const bundleDir = path.join(POSTS_DIR, slug);
  await fs.mkdir(bundleDir, { recursive: true });
  await cleanBundleImages(bundleDir);

  const context = await browser.newContext({
    userAgent: USER_AGENT,
    locale: lang === "fr" ? "fr-FR" : "en-US",
  });
  try {
    const page = await context.newPage();
    const request = context.request;

    console.log(`Fetching: ${slug}`);
    const rawHtml = await extractArticleHtml(page, url);

    if (!rawHtml || rawHtml.length < 200) {
      throw new Error(
        `Empty or tiny article HTML for ${slug}. Update extractArticleHtml() in import.mjs.`,
      );
    }

    const $ = cheerio.load(`<div id="root-import">${rawHtml}</div>`);
    const $root = $("#root-import");
    stripNoise($, $root);

    let imgIndex = 0;
    const tasks = [];

    $root.find("img").each((_, el) => {
      const $img = $(el);
      const srcset = $img.attr("srcset");
      const src = $img.attr("src");
      const fromSet = pickSrcsetUrl(srcset);
      const absolute = resolveUrl(url, fromSet || src || "");
      if (!absolute || !absolute.startsWith("http")) {
        $img.remove();
        return;
      }
      imgIndex += 1;
      const base = `img-${String(imgIndex).padStart(3, "0")}`;
      tasks.push(
        downloadImage(request, absolute).then(({ ok, body, ext }) => {
          if (!ok || !body) {
            $img.remove();
            return;
          }
          const filename = `${base}${ext}`;
          const destPath = path.join(bundleDir, filename);
          return fs.writeFile(destPath, body).then(() => {
            $img.attr("src", `./${filename}`);
            $img.removeAttr("srcset");
          });
        }),
      );
    });

    await Promise.all(tasks);

    const turndown = new TurndownService({
      headingStyle: "atx",
      codeBlockStyle: "fenced",
    });
    turndown.use(gfm);

    let markdown = turndown.turndown($root.html() || "");
    markdown = markdown
      .replace(/\n{3,}/g, "\n\n")
      .replace(/^\[\s*\]\([^)]*\)\s*$/gm, "")
      .replace(/\n{3,}/g, "\n\n")
      .trim();

    const mediumLine =
      lang === "fr"
        ? `\n\n---\n\n*Publié originalement sur [Medium](${url}).*`
        : `\n\n---\n\n*Originally published on [Medium](${url}).*`;

    markdown += mediumLine;

    const tagsYaml = tags.map((t) => `    - ${yamlEscape(t)}`).join("\n");
    const fm = `---
title: ${yamlEscape(title)}
date: ${date}
tags:
${tagsYaml}
canonicalURL: ${JSON.stringify(url)}
---

`;

    const outPath = path.join(bundleDir, indexFile);
    await fs.writeFile(outPath, fm + markdown + "\n", "utf8");
    console.log(`  wrote ${path.relative(ROOT, outPath)} (${markdown.length} chars)`);
  } finally {
    await context.close();
  }
}

async function main() {
  const raw = await fs.readFile(URLS_PATH, "utf8");
  const entries = JSON.parse(raw);
  const browser = await chromium.launch({ headless: true });

  try {
    for (const entry of entries) {
      await processEntry(browser, entry);
    }
  } finally {
    await browser.close();
  }

  console.log("Done.");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
