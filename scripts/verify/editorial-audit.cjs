/* Heuristic review queue, not an automatic prose rewriter or factual validator. */
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve('hugo/content');
const checks = [
  ['staged contrast', /\bnot (?:just|only|merely)\b[^.!?\n]{0,180}\bbut\b/gi],
  ['staged opener', /(?:^|\n)(?:Let's dive|Let's explore|Here's what you need|The real question|At its core)\b[^\n]*/gi],
  ['chat residue', /\b(?:I hope this helps|let me know if|Certainly!|Great question!)\b/gi],
  ['inflated wording', /\b(?:groundbreaking|game.changer|stands as a testament|pivotal moment|delve into)\b/gi],
  ['dash-heavy passage', /[^\n]*(?:—[^\n]*){3,}/g],
  ['document narration', /\b(?:This post walks|This page keeps|This short note keeps|This is the short version|deliberately small)[^.\n]*/gi],
];
const pages=[];
function inspect(file, source) {
  const body=source.replace(/^---[\s\S]*?---\s*/, '').replace(/```[\s\S]*?```/g,'');
  const findings=[];
  for(const [kind, regex] of checks)for(const match of body.matchAll(regex))findings.push({kind,excerpt:match[0]});
  const paragraphs=body.split(/\n\s*\n/).map(x=>x.trim()).filter(x=>x.length>100);
  if(file.includes('/posts/') && /## (?:Running it locally|Getting started|Installation|Exécution locale)/i.test(body))findings.push({kind:'setup in story',excerpt:'Check whether setup belongs in the linked project documentation.'});
  const seen=new Set();for(const text of paragraphs){if(seen.has(text))findings.push({kind:'repeated paragraph',excerpt:text.slice(0,180)});seen.add(text)}
  pages.push({path:file,sha256:crypto.createHash('sha256').update(source).digest('hex'),findings});
}
function walk(dir){for(const entry of fs.readdirSync(dir,{withFileTypes:true})){const file=path.join(dir,entry.name);if(entry.isDirectory())walk(file);else if(entry.name.endsWith('.md'))inspect(path.relative(process.cwd(),file).replaceAll('\\','/'),fs.readFileSync(file,'utf8'));}}
walk(path.join(root,'posts'));walk(path.join(root,'projects'));
const notes=JSON.parse(fs.readFileSync('hugo/data/repository_notes.json','utf8')).notes;
for(const note of notes)inspect(`repository_notes.json#${note.repo}`,JSON.stringify(note));
const report={scope:'All blog/project Markdown and repository-note prose. Findings require human review; quotations and historical writing are not automatically changed.',pagesScanned:pages.length,flagged:pages.filter(p=>p.findings.length),projectNotes:notes.length};
fs.mkdirSync('tmp/editorial-review',{recursive:true});fs.writeFileSync('tmp/editorial-review/audit.json',JSON.stringify({...report,pages},null,2));
console.log(JSON.stringify(report,null,2));
