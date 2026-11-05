(() => {
  document.querySelectorAll('[data-glossary]').forEach(glossary => {
    const search = glossary.querySelector('[data-glossary-search]');
    const query = glossary.querySelector('[data-glossary-query]');
    const status = glossary.querySelector('[data-glossary-status]');
    const entries = [...glossary.querySelectorAll('[data-glossary-entry]')];
    const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase();
    search.hidden = false;
    query.addEventListener('input', () => {
      const needle = normalize(query.value.trim());
      let count = 0;
      entries.forEach(entry => {
        const match = normalize(entry.textContent).includes(needle);
        entry.hidden = !match;
        if (match) count++;
      });
      status.textContent = count ? `${count} ${status.dataset.count}` : status.dataset.empty;
    });
  });
  function revealFragment() {
    let target;
    try { target = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch { return; }
    if (!target) return;
    for (let node = target; node; node = node.parentElement) {
      if (node.tagName === 'DETAILS') node.open = true;
    }
  }
  window.addEventListener('hashchange', revealFragment);
  revealFragment();

  // Live demo frames load on request only.
  document.querySelectorAll('[data-demo]').forEach(panel => {
    const button = panel.querySelector('[data-demo-load]');
    const host = panel.querySelector('[data-demo-frame]');
    if (!button || !host) return;
    button.addEventListener('click', () => {
      if (host.querySelector('iframe')) { host.hidden = !host.hidden; button.setAttribute('aria-expanded', String(!host.hidden)); return; }
      const frame = document.createElement('iframe');
      frame.src = panel.dataset.demoSrc;
      frame.title = panel.dataset.demoTitle || 'Live demo';
      frame.loading = 'lazy';
      frame.referrerPolicy = 'no-referrer';
      frame.setAttribute('sandbox', 'allow-scripts allow-same-origin allow-popups allow-forms allow-pointer-lock');
      frame.setAttribute('allow', 'fullscreen; gamepad; autoplay');
      frame.setAttribute('allowfullscreen', '');
      host.append(frame);
      host.hidden = false;
      button.setAttribute('aria-expanded', 'true');
      const full = document.createElement('button');
      full.type = 'button'; full.className = 'btn'; full.textContent = document.documentElement.lang.startsWith('fr') ? 'Plein écran' : 'Fullscreen';
      full.addEventListener('click', () => { (host.requestFullscreen ? host.requestFullscreen() : Promise.reject()).catch(() => {}); });
      button.after(full);
    });
  });
  // Repository references: chapters become tabs on wide screens; the disclosures stay for phones and no-JS.
  document.querySelectorAll('.repo-guide-chapters').forEach(group => {
    const chapters = [...group.querySelectorAll(':scope > details.repo-guide-chapter')];
    if (chapters.length < 3) return;
    const wide = matchMedia('(min-width: 900px)');
    const fr = document.documentElement.lang.startsWith('fr');
    const tablist = document.createElement('div');
    tablist.className = 'repo-guide-tabs';
    tablist.setAttribute('role', 'tablist');
    tablist.setAttribute('aria-label', fr ? 'Chapitres du guide' : 'Guide chapters');
    const tabs = chapters.map((chapter, index) => {
      const summary = chapter.querySelector(':scope > summary');
      const tab = document.createElement('button');
      tab.type = 'button'; tab.className = 'repo-guide-tab'; tab.setAttribute('role', 'tab');
      tab.id = `guide-tab-${index + 1}`; tab.textContent = summary.textContent.trim();
      tab.setAttribute('aria-selected', 'false'); tab.tabIndex = -1;
      chapter.setAttribute('aria-labelledby', tab.id);
      tablist.append(tab);
      return tab;
    });
    const select = (index, focus) => {
      chapters.forEach((chapter, k) => { chapter.open = k === index; chapter.classList.toggle('is-active-tab', k === index); });
      tabs.forEach((tab, k) => { tab.setAttribute('aria-selected', String(k === index)); tab.tabIndex = k === index ? 0 : -1; });
      if (focus) tabs[index].focus();
    };
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => select(index, false));
      tab.addEventListener('keydown', event => {
        const delta = event.key === 'ArrowRight' ? 1 : event.key === 'ArrowLeft' ? -1 : event.key === 'Home' ? -index : event.key === 'End' ? tabs.length - 1 - index : 0;
        if (!delta) return; event.preventDefault(); select((index + delta + tabs.length) % tabs.length, true);
      });
    });
    const apply = () => {
      if (wide.matches) {
        if (!tablist.isConnected) group.prepend(tablist);
        group.classList.add('is-tabbed');
        if (!chapters.some(c => c.classList.contains('is-active-tab'))) select(0, false);
      } else {
        tablist.remove();
        group.classList.remove('is-tabbed');
        chapters.forEach(c => { c.classList.remove('is-active-tab'); c.setAttribute('role', 'group'); });
      }
    };
    apply();
    wide.addEventListener('change', apply);
  });
})();