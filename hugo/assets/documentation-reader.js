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
})();
