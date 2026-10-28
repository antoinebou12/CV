/* Browser checks for the shared CV/Hugo theme. Run against local preview servers. */
const { createRequire } = require('node:module');
const { mkdirSync, writeFileSync } = require('node:fs');
const { resolve } = require('node:path');
const runtime = process.env.CODEX_NODE_MODULES;
const { chromium } = runtime ? createRequire(resolve(runtime, 'package.json'))('playwright') : require('playwright');
const out = resolve(process.env.AUDIT_OUT || 'tmp/portfolio-theme-audit');
const base = process.env.HUGO_PREVIEW || 'http://localhost:1313/blog';
const cvBase = process.env.CV_PREVIEW || 'http://127.0.0.1:8877';
const routes = process.env.AUDIT_BASELINE ? ['cv', 'posts/', 'projects/', 'projects/notes/nova-backtest/'] :
  ['cv', 'cv-fr', '', 'posts/', 'fr/posts/', 'projects/', 'fr/projects/', 'projects/notes/nova-backtest/', 'fr/projects/notes/nova-backtest/', 'projects/notes/serilog-sinks-sentrysdk/', 'tags/conference/', 'search/'];
(async () => {
  mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ headless: true, channel: 'chrome' });
  const report = [];
  for (const theme of ['light', 'dark']) for (const width of (process.env.AUDIT_BASELINE ? [1440] : [390, 768, 1440])) {
    const context = await browser.newContext({ viewport: { width, height: 960 }, colorScheme: theme, reducedMotion: 'reduce' });
    await context.addInitScript(t => { localStorage.setItem('cv-theme',t); localStorage.setItem('dark',String(t==='dark')); }, theme);
    for (const route of routes) {
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', e => errors.push(e.message));
      const url = route==='cv' ? `${cvBase}/index-en.html` : route==='cv-fr' ? `${cvBase}/index-fr.html` : `${base}/${route}`;
      try {
        const response = await page.goto(url, {waitUntil:'domcontentloaded',timeout:15000});
        await page.evaluate(() => document.fonts.ready);
        const metrics = await page.evaluate(() => {
          const main=document.querySelector('main');
          const h1=document.querySelector('h1');
          const style=e=>e?{color:getComputedStyle(e).color,background:getComputedStyle(e).backgroundColor,font:getComputedStyle(e).fontFamily}:null;
          return {overflow:document.documentElement.scrollWidth>innerWidth+1,renderedTheme:document.documentElement.classList.contains('dark')?'dark':'light',h1:document.querySelectorAll('h1').length,title:document.title,body:style(document.body),main:style(main),heading:style(h1)};
        });
        const image=`${theme}-${width}-${route.replaceAll('/','-')||'home'}.png`;
        await page.screenshot({path:resolve(out,image)});
        report.push({route,theme,width,status:response.status(),errors,image,...metrics});
      } catch(e) {report.push({route,theme,width,error:e.message});}
      await page.close();
    }
    await context.close();
  }
  await browser.close();
  writeFileSync(resolve(out,'report.json'),JSON.stringify(report,null,2));
  const failures=report.filter(x=>x.error||x.status!==200||x.overflow||x.h1!==1||x.errors.length||x.theme!==x.renderedTheme);
  console.log(JSON.stringify({states:report.length,failures},null,2));
  if(failures.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;});
