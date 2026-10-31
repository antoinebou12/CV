/* Progressive page navigation; source content and anchors remain usable without JS. */
(() => {
  const ui = document.getElementById('reader-tools');
  const article = document.querySelector('main article');
  if (!ui || !article) return;
  const dialog = ui.querySelector('dialog');
  const query = ui.querySelector('#reader-query');
  const results = ui.querySelector('#reader-results');
  const count = ui.querySelector('#reader-result-count');
  const actions = ui.querySelector('#reader-actions');
  const feedback = ui.querySelector('#reader-feedback');
  let filter = 'all';
  let timer;
  const entries = [];
  const clean = text => text.replace(/\s+/g, ' ').trim();
  function labelOf(node) {
    if (!node) return '';
    const clone = node.cloneNode(true);
    clone.querySelectorAll('.repo-count, .heading-anchor, [aria-hidden="true"]').forEach(item => item.remove());
    return clean(clone.textContent);
  }
  const normalize = text => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase();
  function index(node, kind, label) {
    if (!label) return;
    if (!node.id) node.id = `reader-${kind}-${entries.length + 1}`;
    entries.push({ node, kind, label });
  }
  article.querySelectorAll('h2, h3').forEach(node => index(node, 'section', labelOf(node)));
  article.querySelectorAll('details').forEach(node => {
    const summary = node.querySelector(':scope > summary');
    if (summary && /diagram|mermaid|uml|c4|layered view|vue en couche/i.test(summary.textContent) && !/source|text version|version textuelle|version texte/i.test(summary.textContent)) {
      const context = labelOf(node.closest('section')?.querySelector('h2, h3, h4'));
      index(node, 'diagram', clean(`${summary.textContent} · ${context}`));
    }
  });
  function render() {
    const terms = normalize(query.value).split(/\s+/).filter(Boolean);
    const found = entries.filter(item => (filter === 'all' || item.kind === filter) && terms.every(term => normalize(item.label).includes(term)));
    const fragment = document.createDocumentFragment();
    for (const item of found) {
      const li = document.createElement('li');
      const link = document.createElement('a');
      link.href = `#${encodeURIComponent(item.node.id)}`;
      const label = document.createElement('span');
      label.textContent = item.label;
      const badge = document.createElement('small');
      badge.textContent = item.kind === 'diagram' ? '◇' : '§';
      badge.setAttribute('aria-hidden', 'true');
      link.append(badge, label);
      link.addEventListener('click', event => {
        event.preventDefault();
        dialog.close();
        for (let parent = item.node.parentElement; parent; parent = parent.parentElement) if (parent.tagName === 'DETAILS') parent.open = true;
        if (item.node.tagName === 'DETAILS') item.node.open = true;
        item.node.scrollIntoView({ block: 'start' });
        history.replaceState(null, '', link.hash);
        if (!item.node.hasAttribute('tabindex')) item.node.setAttribute('tabindex', '-1');
        item.node.focus({ preventScroll: true });
      });
      li.append(link);
      fragment.append(li);
    }
    results.replaceChildren(fragment);
    count.textContent = found.length ? `${found.length} ${ui.dataset.results}` : ui.dataset.empty;
  }
  function closeActions() { if (actions.matches(':popover-open')) actions.hidePopover(); }
  function openSearch() {
    closeActions();
    render();
    dialog.showModal();
    query.focus();
  }
  function notify(message) {
    clearTimeout(timer);
    feedback.textContent = message;
    feedback.hidden = false;
    timer = setTimeout(() => { feedback.hidden = true; }, 4000);
  }
  document.querySelectorAll('[data-reader-search]').forEach(button => button.addEventListener('click', openSearch));
  document.querySelectorAll('[data-reader-copy]').forEach(button => button.addEventListener('click', async () => {
    closeActions();
    try { await navigator.clipboard.writeText(location.href); notify(ui.dataset.copied); }
    catch (_) { notify(ui.dataset.failed); }
  }));
  ui.querySelector('[data-reader-close]').addEventListener('click', () => dialog.close());
  ui.querySelector('[data-reader-clear]').addEventListener('click', () => { query.value = ''; render(); query.focus(); });
  ui.querySelector('[data-reader-top]').addEventListener('click', () => { closeActions(); scrollTo({ top: 0 }); const title = article.querySelector('h1'); if (title) { title.setAttribute('tabindex', '-1'); title.focus({ preventScroll: true }); } });
  query.addEventListener('input', render);
  ui.querySelectorAll('[data-reader-filter]').forEach(button => button.addEventListener('click', () => {
    filter = button.dataset.readerFilter;
    ui.querySelectorAll('[data-reader-filter]').forEach(option => option.setAttribute('aria-pressed', String(option === button)));
    render();
  }));
  const textPanels = [...article.querySelectorAll('.repo-guide-chapter, .article-contents, .repo-language-disclosure')];
  const previous = new Map(textPanels.map(panel => [panel, panel.open]));
  ui.querySelector('#reader-expand').addEventListener('change', event => textPanels.forEach(panel => { panel.open = event.target.checked || previous.get(panel); }));
  if (!textPanels.length) ui.querySelector('#reader-expand').closest('label').hidden = true;
  document.addEventListener('keydown', event => {
    const target = event.target;
    if (event.key === '/' && !event.ctrlKey && !event.metaKey && !event.altKey && !dialog.open && !target.closest('input, textarea, select, [contenteditable="true"], dialog')) { event.preventDefault(); openSearch(); }
  });
  dialog.addEventListener('click', event => {
    const box = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom)) dialog.close();
  });
  article.querySelectorAll('.repo-snapshot-cards a').forEach(link => link.addEventListener('click', () => {
    const target = document.getElementById(link.hash.slice(1));
    if (target?.tagName === 'DETAILS') target.open = true;
  }));
  const launch = ui.querySelector('.reader-launch');
  launch.classList.add('reader-ui');
  const anchor = article.querySelector('.repo-hero-panel, .article-heading') || article.querySelector('.repo-doc-heading');
  if (anchor) anchor.append(launch);
  const progress = ui.querySelector('.reader-progress span');
  let pending = false;
  function updateProgress() {
    const box = article.getBoundingClientRect();
    const distance = Math.max(1, article.offsetHeight - innerHeight);
    progress.style.transform = `scaleX(${Math.min(1, Math.max(0, -box.top / distance))})`;
    pending = false;
  }
  addEventListener('scroll', () => { if (!pending) { pending = true; requestAnimationFrame(updateProgress); } }, { passive: true });
  addEventListener('resize', updateProgress);
  updateProgress();
  ui.hidden = false;
})();
