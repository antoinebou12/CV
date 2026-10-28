const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(process.argv[2] || 'docs/blog');
const documents = new Map();
function document(file) {
  if(!documents.has(file))documents.set(file,fs.readFileSync(file,'utf8'));
  return documents.get(file);
}
const bad = new Map();
let checked = 0;
function walk(dir) {
  for (const item of fs.readdirSync(dir, {withFileTypes:true})) {
    const file = path.join(dir,item.name);
    if(item.isDirectory()) walk(file);
    else if(item.name.endsWith('.html')) {
      const relative = path.relative(root,file).replaceAll('\\','/');
      const base = new URL(relative.replace(/index\.html$/,''),'https://antoineboucher.info/CV/blog/');
      for(const match of document(file).matchAll(/\bhref=(?:"([^"]*)"|'([^']*)'|([^\s>]+))/g)) {
        let url; try {url=new URL((match[1]??match[2]??match[3]).replaceAll('&amp;','&'),base)}catch{continue}
        if(!['antoineboucher.info','localhost','127.0.0.1','antoinebou12.github.io'].includes(url.hostname))continue;
        let target=url.pathname.replace(/^\/(?:CV\/)?blog\//,'');
        if(!/^(?:fr\/)?(?:posts|projects)\//.test(target))continue;
        checked++;
        let disk=path.join(root,decodeURIComponent(target));
        if(fs.existsSync(disk)&&fs.statSync(disk).isDirectory())disk=path.join(disk,'index.html');
        let reason = !fs.existsSync(disk) ? 'Missing target' : /^(localhost|127\.)/.test(url.hostname) ? 'Local-only URL' : '';
        if(!reason && url.hash && disk.endsWith('.html')) {
          const ids=[...document(disk).matchAll(/\bid=(?:"([^"]*)"|'([^']*)'|([^\s>]+))/g)].map(m=>m[1]??m[2]??m[3]);
          if(!ids.includes(decodeURIComponent(url.hash.slice(1))))reason='Missing anchor';
        }
        if(reason) {
          const key=url.pathname+url.hash;
          const entry=bad.get(key)||{target:key,reason,sources:[]};
          if(entry.sources.length<4)entry.sources.push(relative);
          bad.set(key,entry);
        }
      }
    }
  }
}
walk(root);
console.log(JSON.stringify({checked,broken:[...bad.values()]},null,2));
process.exitCode=bad.size?1:0;
