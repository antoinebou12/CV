const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const site=path.resolve(process.argv[2]||'hugo/public');
const {notes}=JSON.parse(fs.readFileSync('hugo/data/repository_notes.json','utf8'));
let pages=0;
let allProjectPages=0;
function checkProjectTree(dir){for(const entry of fs.readdirSync(dir,{withFileTypes:true})){
 const file=path.join(dir,entry.name);
 if(entry.isDirectory())checkProjectTree(file);
 else if(/^index(?:\.fr)?\.md$/.test(entry.name)){
   const folder=path.relative('hugo/content',dir).replaceAll('\\','/').toLowerCase();
   const html=fs.readFileSync(path.join(site,entry.name.includes('.fr.')?'fr':'',folder,'index.html'),'utf8');
   assert.equal((html.match(/id=["']?glossary(?:["' >])/g)||[]).length,1,`${file}: one glossary`);
   allProjectPages++;
 }
}}
checkProjectTree('hugo/content/projects');
let covers=0;
const textOnly = new Set(['ainewstracker-financial-news','mistubavideo-rendered-video','snapchat-lens-creator']);
for(const dir of fs.readdirSync('hugo/content/posts'))for(const lang of ['', 'fr/']){
  const target=path.join(site,lang,'posts',dir,'index.html');
  if(!fs.existsSync(target))continue;
  const html=fs.readFileSync(target,'utf8');
  const meta=(html.split('</head>')[0].match(/<meta[^>]*og:image[^>]*>/)||[''])[0];
  if(textOnly.has(dir)) {
    assert.equal(meta,'',`${dir}/${lang}: no substitute social cover`);
    assert.ok(!html.includes('article-single-hero'),`${dir}/${lang}: no substitute hero`);
  } else assert.ok(meta && !meta.includes('post-kind-'),`${dir}/${lang}: project-specific cover`);
  covers++;
}
for(const note of notes)for(const lang of ['', 'fr/']){
  const html=fs.readFileSync(path.join(site,lang,'projects/notes',note.slug,'index.html'),'utf8');
  assert.equal((html.match(/id=["']?glossary(?:["' >])/g)||[]).length,1,`${note.repo}/${lang}: one glossary`);
  assert.ok((html.match(/data-glossary-entry/g)||[]).length>=3,`${note.repo}: terms`);
  assert.equal((html.match(/class=["']?repo-component(?:["' >])/g)||[]).length,note.nodes.length,`${note.repo}: component explorer`);
  assert.ok(!html.includes('tab-arch-context'),`${note.repo}: no orphaned tab label`);
  pages++;
}
for(const slug of ['ainewstracker','mistubavideo','truemapdata'])for(const lang of ['', 'fr/']){
  const html=fs.readFileSync(path.join(site,lang,'projects/notes',slug,'index.html'),'utf8');
  assert.equal((html.match(/id=["']?glossary(?:["' >])/g)||[]).length,1,`${slug}: manual documentation glossary`);
  pages++;
}
for(const slug of textOnly)for(const lang of ['', 'fr/']){
  const html=fs.readFileSync(path.join(site,lang,'posts',slug,'index.html'),'utf8');
  assert.doesNotMatch(html,/news-archive-concept|rendered-video-concept|ar-lens-concept/);
}
console.log(`${allProjectPages} project pages have one glossary; ${pages} canonical pages/component explorers checked; ${covers} article cover policies checked; no generated cover substitutions.`);
