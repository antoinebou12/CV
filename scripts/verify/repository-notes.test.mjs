import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const root = fileURLToPath(new URL('../../', import.meta.url));
const read = path => readFileSync(resolve(root, path), 'utf8');
const inventory = JSON.parse(read('hugo/data/github_inventory.json'));
const { notes, reviewed } = JSON.parse(read('hugo/data/repository_notes.json'));
const analysis = JSON.parse(read('hugo/data/repository_analysis.json'));
const handbooks = JSON.parse(read('hugo/data/repository_handbooks.json')).repositories;
const diagramImages = JSON.parse(read('hugo/data/repository_diagram_images.json')).repositories;
const categories = JSON.parse(read('hugo/data/repository_categories.json')).repositories;
const profiles = JSON.parse(read('hugo/data/repository_profiles.json')).repositories;
const apiGuides = JSON.parse(read('hugo/data/repository_api_guides.json')).repositories;
const site = resolve(root, process.env.CV_NOTES_SITE || '_site/blog');
const page = (note, lang) => readFileSync(resolve(site, lang === 'fr' ? 'fr' : '', 'projects/notes', note.slug, 'index.html'), 'utf8');

function expectsMermaid(repo) {
  return notes.some(note => note.repo === repo);
}

test('every public repository has exactly one bilingual architecture note', () => {
  assert.equal(notes.length, inventory.repositories.length);
  assert.equal(new Set(notes.map(note => note.repo)).size, notes.length);
  assert.equal(new Set(notes.map(note => note.slug)).size, notes.length);
  assert.deepEqual(notes.map(note => note.repo).sort(), inventory.repositories.map(repo => repo.name).sort());
});

test('diagram JavaScript parses and uses strict rendering with SVG labels', () => {
  const template = read('hugo/layouts/partials/mermaid.html');
  const script = template.match(/<script type="module">([\s\S]*?)<\/script>/)[1];
  const AsyncFunction = (async () => {}).constructor;
  assert.doesNotThrow(() => new AsyncFunction(script));
  assert.match(script, /securityLevel: 'strict'/);
  assert.match(script, /htmlLabels: false/);
  assert.match(script, /requestAnimationFrame\(\(\) => fit\(\)\)/);
  assert.match(script, /requestFullscreen/);
  assert.match(script, /'Fullscreen'/);
  assert.match(read('hugo/assets/repository-notes.css'), /\.edgeLabel \.labelBkg/);
});

test('automatic documentation covers the inventory with source-pinned exports', () => {
  assert.equal(analysis.schema_version, 1);
  assert.deepEqual(Object.keys(analysis.repositories).sort(), notes.map(note => note.repo).sort());
  for (const note of notes) {
    const data = analysis.repositories[note.repo];
    assert.match(data.commit, /^[0-9a-f]{40}$/);
    assert.equal(data.coverage.failures.length, 0, note.repo);
    assert.equal(data.coverage.read_files, data.coverage.eligible_files, note.repo);
    assert.equal(data.coverage.truncated_tree, false, note.repo);
    assert.equal(data.source_manifest.length, data.coverage.read_files, note.repo);
    assert.equal(data.type_count, data.types.length, note.repo);
    assert.equal(data.language_bytes, data.languages.reduce((sum, lang) => sum + lang.bytes, 0));
    for (const lang of data.languages) {
      assert.ok(lang.bytes > 0);
      assert.ok(Math.abs(lang.percent - lang.bytes / data.language_bytes * 100) < 0.011);
    }
    const paths = new Set(data.source_manifest.map(file => file.path));
    for (const file of data.source_manifest) {
      assert.match(file.blob_sha, /^[0-9a-f]{40}$/);
      assert.ok(file.source_url.includes(`/blob/${data.commit}/`));
    }
    for (const type of data.types) assert.ok(paths.has(type.file), `${note.repo}/${type.file}`);
    for (const file of data.class_files) {
      assert.ok(paths.has(file.path));
      assert.match(read(`hugo/static/${file.download}`), /^classDiagram/);
      assert.ok(existsSync(resolve(site, file.download)));
    }
    assert.ok(existsSync(resolve(site, `repository-docs/${note.slug}/analysis.json`)));
    assert.ok(existsSync(resolve(site, `repository-docs/${note.slug}/files.mmd`)));
    if (data.gitdiagram.source_file) assert.ok(existsSync(resolve(site, data.gitdiagram.source_file)));
    for (const lang of ['en', 'fr']) {
      const html = page(note, lang);
      for (const id of ['installation', 'code-structure']) {
        assert.ok(new RegExp(`id=["']?${id}(?:["' >])`).test(html), `${note.repo}: ${id}`);
      }
      assert.doesNotMatch(html, /id=["']?gitdiagram(?:["' >])|>GitDiagram</);
      assert.ok(html.includes(data.commit.slice(0, 8)));
      assert.doesNotMatch(html, /<video[\s>]|View video options|Voir les options vidéo/);
      if (data.types.length) {
        assert.ok(html.includes(lang === 'fr' ? 'Index des types' : 'Type index'));
      }
    }
  }
});

test('reader guides, Mermaid policy and API sections are present in both languages', () => {
  for (const note of notes) {
    assert.ok(handbooks[note.repo]);
    const showMermaid = expectsMermaid(note.repo);
    for (const lang of ['en', 'fr']) {
      const html = page(note, lang);
      for (const id of ['first-steps', 'reader-guide']) {
        assert.match(html, new RegExp(`id=["']?${id}(?:["' >])`), `${note.repo}/${lang}`);
      }
      assert.ok(existsSync(resolve(site, `repository-docs/${note.slug}/architecture-${lang}.mmd`)));
      if (diagramImages[note.repo]) {
        const hero = diagramImages[note.repo].system || diagramImages[note.repo][`overview_${lang}`];
        if (hero?.path) assert.ok(existsSync(resolve(site, hero.path)));
      }
      const hero = diagramImages[note.repo]?.system || diagramImages[note.repo]?.[`overview_${lang}`];
      if (hero?.path) {
        assert.match(html, /<(?:figure|img)[^>]*(?:repo-static-diagram|data-mermaid-image-fallback)/, `${note.repo} includes a local fallback image`);
        assert.ok(html.includes(hero.path), `${note.repo} uses the recorded fallback image`);
      }
      if (showMermaid) {
        assert.match(html, /<(?:details|div)[^>]*data-mermaid-lazy/, `${note.repo} should lazy-load Mermaid`);
        assert.match(html, /<code[^>]*class=(?:["'][^"']*)?language-mermaid/, `${note.repo} should expose Mermaid source`);
        assert.ok(html.includes(lang === 'fr' ? 'Version texte du diagramme' : 'Text version of the diagram'));
      } else {
        assert.doesNotMatch(html, /<(?:details|div)[^>]*data-mermaid-lazy/, `${note.repo} should stay text-only`);
        assert.doesNotMatch(html, /<code[^>]*class=(?:["'][^"']*)?language-mermaid/, `${note.repo} should omit Mermaid blocks`);
      }
      if (apiGuides[note.repo]) assert.match(html, /id=["']?api-contract(?:["' >])/);
    }
  }
});

for (const note of notes) {
  test(`${note.repo}: evidence, translations and diagram topology`, () => {
    const repo = inventory.repositories.find(repo => repo.name === note.repo);
    assert.equal(note.url, repo.url);
    assert.equal(note.fork, repo.fork);
    assert.equal(note.archived, repo.archived);
    assert.equal(note.reviewed, reviewed);
    assert.match(note.slug, /^[a-z0-9]+(?:-[a-z0-9]+)*$/);
    for (const field of ['topic', 'intro', 'trace', 'limits']) {
      assert.equal(note[field].length, 2);
      for (const text of note[field]) {
        assert.ok(text.trim().length > 15, `${field} needs real content`);
        assert.doesNotMatch(text, /[\u2013\u2014]|TODO|PLACEHOLDER/);
      }
    }
    assert.ok(note.parts.length >= 2);
    for (const part of note.parts) {
      assert.equal(part.length, 4);
      assert.ok(part[2].length > 100 && part[3].length > 100);
    }
    assert.ok(note.nodes.length >= 4);
    const connected = new Set();
    for (const edge of note.edges) {
      assert.equal(edge.length, 2);
      for (const index of edge) {
        assert.ok(Number.isInteger(index) && index >= 0 && index < note.nodes.length);
        connected.add(index);
      }
    }
    assert.equal(connected.size, note.nodes.length, 'no disconnected diagram nodes');
    for (const node of note.nodes) {
      assert.equal(node.length, 2);
      assert.ok(node.every(label => label.length > 0 && !/[<>\n]/.test(label)));
    }
    assert.ok(note.sources.length >= 2);
    for (const source of note.sources) {
      assert.ok(source.url.startsWith(`${repo.url}/blob/`));
      assert.match(source.blob_sha, /^[0-9a-f]{40}$/);
      assert.doesNotMatch(source.path, /(?:^|\/)\.env(?:$|\.)|\.pypirc|dump\.rdb/);
    }
    for (const [i, lang] of ['en', 'fr'].entries()) {
      const path = `hugo/content/projects/notes/${note.slug}/index${lang === 'fr' ? '.fr' : ''}.md`;
      const source = read(path);
      assert.ok(source.includes(`translationKey: repository-note-${note.slug}`));
      assert.ok(source.includes(`repository_note: ${JSON.stringify(note.repo)}`));
      assert.ok(source.includes('{{< repository-note >}}'));
      const html = page(note, lang);
      assert.ok(html.match(/<title>([\s\S]*?)<\/title>/)[1].trim().length <= 70);
      for (const id of ['architecture', 'constraints', 'source-files', 'languages-panel', 'overview', 'features']) {
        assert.ok(new RegExp(`id=["']?${id}(?:["' >])`).test(html), `missing section ${id}`);
      }
      const marker = (id) => {
        const match = new RegExp(`id=(?:"${id}"|'${id}'|${id}(?=[\\s>]))`).exec(html);
        return match ? match.index : -1;
      };
      const titleAt = (() => {
        const m = /id=(?:"single-post-title"|'single-post-title'|single-post-title(?=[\s>]))/.exec(html);
        return m ? m.index : -1;
      })();
      const statusAt = html.indexOf('repo-status-row');
      assert.ok(titleAt > 0 && (statusAt < 0 || titleAt < statusAt), `${note.repo} title precedes status chips`);
      const langAt = marker('languages-panel');
      const installAt = marker('installation');
      const archAt = marker('architecture');
      assert.ok(langAt > 0 && langAt < installAt && installAt < archAt, `${note.repo} opens with languages and getting started`);
      assert.ok(html.includes(note.sources[0].url));
      assert.doesNotMatch(html, /%25!|#L%!/, 'source line links render numeric anchors');
      const hero = diagramImages[note.repo]?.system || diagramImages[note.repo]?.[`overview_${lang}`];
      if (hero?.path) {
        assert.match(html, /data-mermaid-image-fallback/);
        assert.ok(html.includes(hero.path));
      }
      assert.ok(html.includes('repository-notes.min.'));
      if (expectsMermaid(note.repo)) {
        assert.match(html, /<(?:details|div)[^>]*data-mermaid-lazy/);
        assert.match(html, /data-mermaid-fallback/);
        assert.match(html, /<code[^>]*class=(?:["'][^"']*)?language-mermaid/);
        assert.ok(html.includes(lang === 'fr' ? 'Version texte du diagramme' : 'Text version of the diagram'));
      } else {
        assert.doesNotMatch(html, /<(?:details|div)[^>]*data-mermaid-lazy/);
        assert.doesNotMatch(html, /<code[^>]*class=(?:["'][^"']*)?language-mermaid/);
      }
      assert.equal((html.match(/<h1[\s>]/g) || []).length, 1);
      assert.ok(html.includes(note.topic[i].split(' ')[0]));
      const readingOrder = [
        html.indexOf('repo-doc-title'),
        html.indexOf('repo-status-row'),
        html.indexOf('repo-tech-badges'),
        marker('languages-panel'),
        marker('overview'),
        marker('installation'),
        marker('features'),
        marker('architecture'),
      ];
      assert.ok(readingOrder.every(position => position >= 0), 'required project sections are present');
      assert.deepEqual(
        readingOrder,
        [...readingOrder].sort((a, b) => a - b),
        'required project sections keep their reading order',
      );
      const translationPath = `/blog/${lang === 'fr' ? '' : 'fr/'}projects/notes/${note.slug}/`;
      const links = [...html.matchAll(/href=(?:"([^"]+)"|'([^']+)'|([^ >]+))/g)]
        .map(match => new URL(match[1] || match[2] || match[3], 'http://localhost').pathname);
      assert.ok(links.some(path => path.endsWith(translationPath)), 'actual alternate-language link');
    }
  });
}

test('adaptive sections: Compose topology and algorithm when profile data exists', () => {
  for (const lang of ['en', 'fr']) {
    const tch = page({ slug: 'tch099', repo: 'TCH099' }, lang);
    assert.match(tch, /id=["']?deployment(?:["' >])/);
    assert.match(tch, /repo-topology|is-primary-diagram/);
    assert.ok(tch.includes('flowchart LR'));
    assert.ok(tch.includes('data-mermaid-lazy'));
    const ipc = page({ slug: 'ipc-toolkit', repo: 'ipc-toolkit' }, lang);
    assert.match(ipc, /id=["']?algorithm(?:["' >])/);
    assert.ok(ipc.includes('repo-pseudocode') || ipc.includes('repo-algorithm-steps'));
    assert.ok(profiles['ipc-toolkit'].algorithm);
    assert.ok(profiles.TCH099.services.length >= 2);
    assert.ok(expectsMermaid('TCH099'));
    const dots = page({ slug: 'dotfiles', repo: '.dotfiles' }, lang);
    assert.ok(expectsMermaid('.dotfiles'));
    assert.match(dots, /<(?:details|div)[^>]*data-mermaid-lazy/);
    assert.match(dots, /<code[^>]*class=(?:["'][^"']*)?language-mermaid/);
  }
});

test('directory cards link to all local notes, with separate GitHub links', () => {
  for (const lang of ['en', 'fr']) {
    const html = readFileSync(resolve(site, lang === 'fr' ? 'fr' : '', 'projects/index.html'), 'utf8');
    assert.equal((html.match(/class=["']?repo-read-note["' >]/g) || []).length, notes.length);
    for (const note of notes) {
      assert.ok(html.includes(`/projects/notes/${note.slug}/`), note.repo);
      assert.ok(html.includes(note.url), note.repo);
    }
    const search = readFileSync(resolve(site, lang === 'fr' ? 'fr' : '', 'index.json'), 'utf8');
    for (const note of notes) assert.ok(search.includes(`/projects/notes/${note.slug}/`), `${note.repo} is searchable`);
    for (const entry of JSON.parse(search)) {
      assert.doesNotMatch(entry.content, /\uFFFD/, 'search content preserves Unicode');
      assert.ok(Array.from(entry.content).length <= 12000, 'search content stays bounded');
    }
  }
});

test('featured posts retain images and include architecture and related note links', () => {
  for (const [slug, name, image] of [
    ['dimension-rust-math-rendering', 'dimension', 'renderer-architecture'],
    ['dashercontrol-homelab-workspaces', 'dashercontrol', 'dashboard.png'],
    ['bloc-blender-cloud-storage', 'bloc', null],
  ]) {
    for (const lang of ['en', 'fr']) {
      const html = readFileSync(resolve(site, lang === 'fr' ? 'fr' : '', 'posts', slug, 'index.html'), 'utf8');
      assert.ok(html.includes('language-mermaid'));
      assert.ok(html.includes(`/projects/notes/${name}/`));
      if (image) assert.ok(html.includes(image));
    }
  }
  assert.ok(existsSync(resolve(site, 'posts/dashercontrol-homelab-workspaces/demo.gif')));
});

test('repository articles link back to the bilingual technical guides', () => {
  for (const lang of ['en', 'fr']) {
    const html = readFileSync(
      resolve(site, lang === 'fr' ? 'fr' : '', 'posts', 'uml-mcp', 'index.html'),
      'utf8',
    );
    assert.ok(html.includes('repo-article-guides'));
    assert.ok(html.includes(`/projects/notes/uml-mcp/`));
    assert.ok(html.includes(lang === 'fr' ? 'Documentation des projets' : 'Project documentation'));
  }
});
