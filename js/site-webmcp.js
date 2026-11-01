/* Native browser tools shared by the static CV and Hugo. No polyfill or remote service. */
(() => {
  const context = document.modelContext;
  if (!isSecureContext || !context?.registerTool) { document.documentElement.dataset.webmcp = 'unsupported'; return; }
  const root = document.querySelector('main');
  if (!root) return;
  const clean = text => text.replace(/\s+/g, ' ').trim();
  const textOf = node => {
    const clone = node.cloneNode(true);
    clone.querySelectorAll('script,style,iframe,input,textarea,button,noscript,.aeo-agent-only,[aria-hidden="true"],.repo-count').forEach(item => item.remove());
    return clean(clone.textContent);
  };
  function headings() {
    return [...root.querySelectorAll('h1,h2,h3')].filter(node => !node.closest('[hidden],dialog,.aeo-agent-only')).map((node, i) => {
      if (!node.id) {
        let id = `webmcp-section-${i + 1}`;
        while (document.getElementById(id)) id += '-heading';
        node.id = id;
      }
      return { node, id: node.id, title: textOf(node), level: Number(node.tagName.slice(1)) };
    });
  }
  function sectionText(item, outline) {
    const next = outline.slice(outline.indexOf(item) + 1).find(entry => entry.level <= item.level);
    const range = document.createRange();
    range.setStartAfter(item.node);
    if (next) range.setEndBefore(next.node);
    else range.setEnd(root, root.childNodes.length);
    const wrapper = document.createElement('div');
    wrapper.append(range.cloneContents());
    return textOf(wrapper);
  }
  const result = value => ({ content: [{ type: 'text', text: JSON.stringify(value) }] });
  const failure = message => ({ isError: true, content: [{ type: 'text', text: message }] });
  function validate(input, allowed) {
    return input && typeof input === 'object' && !Array.isArray(input) && Object.keys(input).every(key => allowed.includes(key));
  }
  const idSchema = { type: 'object', properties: { section_id: { type: 'string', maxLength: 200, description: 'Section identifier returned by website_get_outline or website_search_page.' } }, required: ['section_id'], additionalProperties: false };
  const tools = [
    {
      name: 'website_get_outline', description: 'Read the current CV, article or project page title and its section headings. Use to choose a section to inspect.',
      inputSchema: { type: 'object', properties: {}, additionalProperties: false },
      execute(input = {}) {
        if (!validate(input, [])) return failure('This tool takes an empty object.');
        return result({ title: document.title, language: document.documentElement.lang, url: location.href, sections: headings().map(({ id, title, level }) => ({ id, title, level })) });
      }, annotations: { readOnlyHint: true }
    },
    {
      name: 'website_read_section', description: 'Read public text from a section of the current page, including text in collapsed disclosures.', inputSchema: idSchema,
      execute(input = {}) {
        if (!validate(input, ['section_id']) || typeof input.section_id !== 'string' || input.section_id.length > 200) return failure('Supply a section_id from website_get_outline.');
        const outline = headings();
        const item = outline.find(entry => entry.id === input.section_id);
        if (!item) return failure('Section not found. Use website_get_outline for current identifiers.');
        const text = sectionText(item, outline);
        return result({ id: item.id, title: item.title, text: text.slice(0, 16000), truncated: text.length > 16000 });
      }, annotations: { readOnlyHint: true }
    },
    {
      name: 'website_search_page', description: 'Search the public text of the current CV, article or project documentation and return matching sections.',
      inputSchema: { type: 'object', properties: { query: { type: 'string', minLength: 1, maxLength: 200, description: 'Words to find on the current page.' } }, required: ['query'], additionalProperties: false },
      execute(input = {}) {
        if (!validate(input, ['query']) || typeof input.query !== 'string' || !input.query.trim() || input.query.length > 200) return failure('Supply a nonempty query of at most 200 characters.');
        const normalize = text => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
        const terms = normalize(input.query).trim().split(/\s+/);
        const outline = headings();
        const found = outline.map(item => ({ id: item.id, title: item.title, text: sectionText(item, outline) })).filter(item => terms.every(term => normalize(item.title + ' ' + item.text).includes(term)));
        return result({ query: input.query, total: found.length, matches: found.slice(0, 20).map(item => ({ id: item.id, title: item.title, excerpt: item.text.slice(0, 400) })) });
      }, annotations: { readOnlyHint: true }
    },
    {
      name: 'website_show_section', description: 'Open the disclosures containing a page section and bring its heading into view.', inputSchema: idSchema,
      execute(input = {}) {
        if (!validate(input, ['section_id']) || typeof input.section_id !== 'string' || input.section_id.length > 200) return failure('Supply a section_id from website_get_outline.');
        const item = headings().find(entry => entry.id === input.section_id);
        if (!item) return failure('Section not found. Use website_get_outline for current identifiers.');
        for (let parent = item.node.parentElement; parent && parent !== root; parent = parent.parentElement) if (parent.tagName === 'DETAILS') parent.open = true;
        item.node.setAttribute('tabindex', '-1');
        item.node.scrollIntoView({ block: 'start', behavior: 'instant' });
        item.node.focus({ preventScroll: true });
        return result({ shown: item.id, title: item.title });
      }, annotations: { readOnlyHint: false }
    }
  ];
  const controller = new AbortController();
  addEventListener('pagehide', event => { if (!event.persisted) controller.abort(); });
  Promise.all(tools.map(tool => context.registerTool(tool, { signal: controller.signal }))).then(() => {
    document.documentElement.dataset.webmcp = 'ready';
  }).catch(() => { controller.abort(); document.documentElement.dataset.webmcp = 'unavailable'; });
})();
