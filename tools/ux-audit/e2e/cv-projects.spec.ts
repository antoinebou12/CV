import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
const prefix=process.env.E2E_PREFIX||'';
for(const width of [320,390,1033,1440]) for(const lang of ['en','fr']) for(const theme of ['light','dark']) test(`project hierarchy ${width} ${lang} ${theme}`,async({page},info)=>{
  await page.setViewportSize({width,height:950});
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.addInitScript(theme=>localStorage.setItem('cv-theme',theme),theme);
  await page.goto(`${prefix}/index-${lang}.html`);
  const projects=page.locator('#projects');
  await projects.evaluate((node:HTMLDetailsElement)=>node.open=true);
  await projects.scrollIntoViewIfNeeded();
  const groups=projects.locator('details.project-group');
  await expect(groups).toHaveCount(2);
  for(const group of await groups.all()) await expect(group).not.toHaveAttribute('open');
  await projects.screenshot({path:info.outputPath('project-groups.png')});
  const input=page.locator('#cv-project-query');
  await input.fill('DasherControl');
  await expect(projects.locator('.project-card:visible')).toHaveCount(1);
  await expect(projects.locator('.project-card:visible .project-title')).toContainText('DasherControl');
  await projects.screenshot({path:info.outputPath('project-search.png')});
  await input.fill('this-project-does-not-exist');
  await expect(projects.locator('.project-card:visible')).toHaveCount(0);
  await expect(page.locator('.cv-project-result-count')).toContainText(lang==='fr'?'Aucun':'No results');
  await input.fill('');
  for(const group of await groups.all()) await expect(group).not.toHaveAttribute('open');
  for(const id of ['project-uml-mcp','project-ipc-toolkit']) {
    const card=page.locator('#'+id);
    await card.evaluate(node=>{for(let parent=node.parentElement;parent;parent=parent.parentElement)if(parent.tagName==='DETAILS')(parent as HTMLDetailsElement).open=true;});
    await card.scrollIntoViewIfNeeded();
    await expect(card).toHaveCSS('border-radius','10px');
    await card.screenshot({path:info.outputPath(id+'.png')});
    expect(await card.evaluate(node=>node.scrollWidth<=node.clientWidth+1)).toBe(true);
  }
  const graphics=page.locator('.expertise-domain[data-domain="graphics-3d"]');
  await graphics.click();
  const sub=page.locator('.expertise-panel:visible .expertise-sub').first();
  await expect(sub).toHaveCSS('font-size','11px');
  await expect(sub).toHaveCSS('border-radius','5px');
  await page.locator('.expertise').screenshot({path:info.outputPath('skill-subcategories.png')});
  const certs=page.locator('#certifications');
  await certs.evaluate(node=>{if(node.tagName==='DETAILS')(node as HTMLDetailsElement).open=true;});
  const logos=certs.locator('.cv-credential-logo');
  expect(await logos.count()).toBe(11);
  for(const logo of await logos.all()) {
    await logo.scrollIntoViewIfNeeded();
    await expect.poll(()=>logo.evaluate((img:HTMLImageElement)=>img.complete&&img.naturalWidth>0)).toBe(true);
    expect(await logo.getAttribute('src')).toMatch(/^images\//);
  }
  await certs.screenshot({path:info.outputPath('credentials.png')});
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);
});
test('project controls support keyboard and accessible search',async({page})=>{
  await page.goto(`${prefix}/index-en.html`);
  await page.locator('#projects').evaluate((node:HTMLDetailsElement)=>node.open=true);
  const summary=page.locator('#projects details.project-group > summary').first();
  await summary.focus();await page.keyboard.press('Enter');
  await expect(page.locator('#projects details.project-group').first()).toHaveAttribute('open');
  await expect(page.locator('#projects details.project-group').first()).not.toHaveAttribute('data-motion-target');
  const audit=await new AxeBuilder({page}).include('#projects').withTags(['wcag2a','wcag2aa']).analyze();
  expect(audit.violations).toEqual([]);
});

for(const lang of ['en','fr']) for(const theme of ['light','dark']) test(`credential contrast ${lang} ${theme}`,async({page})=>{
  await page.setViewportSize({width:320,height:950});
  await page.addInitScript(theme=>localStorage.setItem('cv-theme',theme),theme);
  await page.goto(`${prefix}/index-${lang}.html`);
  const certs=page.locator('#certifications');
  await certs.scrollIntoViewIfNeeded();
  const row=certs.locator('.certification-badge').first();
  await expect(row).toHaveCSS('border-radius','0px');
  const audit=await new AxeBuilder({page}).include('#certifications').withTags(['wcag2a','wcag2aa']).analyze();
  expect(audit.violations).toEqual([]);
});
