/* Progressive table enhancement for articles and project notes.
   Every data table with a header row becomes sortable (click or Enter/Space on a header,
   aria-sort announces the order). Tables with more than eight rows also get a filter field
   and a live row count. Static markup stays the source of truth: without JavaScript the
   table is unchanged, and the enhancement skips tables that merge cells. */
(() => {
  const fr = document.documentElement.lang.startsWith('fr');
  const t = {
    sort: fr ? 'Trier par' : 'Sort by',
    asc: fr ? 'ordre croissant' : 'ascending',
    desc: fr ? 'ordre décroissant' : 'descending',
    none: fr ? 'non trié' : 'not sorted',
    filter: fr ? 'Filtrer les lignes' : 'Filter rows',
    placeholder: fr ? 'Tapez pour filtrer…' : 'Type to filter…',
    rows: fr ? 'lignes affichées' : 'rows shown',
    of: fr ? 'sur' : 'of',
    empty: fr ? 'Aucune ligne ne correspond.' : 'No rows match.',
    reset: fr ? 'Effacer' : 'Clear',
  };
  const collator = new Intl.Collator(fr ? 'fr' : 'en', { numeric: true, sensitivity: 'base' });
  const numberOf = (text) => {
    const cleaned = text.replace(/[\s,%$€£]/g, '').replace(/−/g, '-');
    if (!cleaned || !/^[-+]?\d*\.?\d+(e[-+]?\d+)?$/i.test(cleaned)) return NaN;
    return Number(cleaned);
  };
  const cellText = (cell) => (cell?.dataset.sortValue ?? cell?.textContent ?? '').trim();
  const selector = '.single-post-content table, .repo-doc table, .journal-article table';
  const tables = [...document.querySelectorAll(selector)].filter((table) => {
    if (table.dataset.enhanced || table.closest('.terminal, .article-contents') || table.hasAttribute('data-static')) return false;
    const head = table.tHead?.rows[0];
    if (!head || table.tBodies.length !== 1) return false;
    if (table.querySelector('[rowspan], [colspan]')) return false;
    return table.tBodies[0].rows.length > 1 && [...head.cells].every((cell) => cell.tagName === 'TH');
  });
  let seq = 0;
  for (const table of tables) {
    table.dataset.enhanced = 'true';
    table.classList.add('is-dynamic');
    const body = table.tBodies[0];
    const rows = [...body.rows];
    const original = rows.slice();
    const heads = [...table.tHead.rows[0].cells];
    const live = document.createElement('p');
    live.className = 'table-status';
    live.setAttribute('role', 'status');
    live.setAttribute('aria-live', 'polite');
    const id = `dyn-table-${++seq}`;
    table.id ||= id;

    // Sorting -----------------------------------------------------------------
    const numericColumn = heads.map((_, index) => original.length > 0 && original.every((row) => !Number.isNaN(numberOf(cellText(row.cells[index])))));
    const applySort = (index, direction) => {
      heads.forEach((cell, i) => {
        cell.setAttribute('aria-sort', i === index ? (direction === 'asc' ? 'ascending' : direction === 'desc' ? 'descending' : 'none') : 'none');
      });
      let ordered = original.slice();
      if (direction !== 'none') {
        const sign = direction === 'asc' ? 1 : -1;
        ordered.sort((a, b) => {
          const ta = cellText(a.cells[index]);
          const tb = cellText(b.cells[index]);
          if (numericColumn[index]) return (numberOf(ta) - numberOf(tb)) * sign;
          return collator.compare(ta, tb) * sign;
        });
      }
      body.append(...ordered);
      live.textContent = direction === 'none'
        ? `${heads[index].textContent.trim()}: ${t.none}`
        : `${t.sort} ${heads[index].textContent.trim()}, ${direction === 'asc' ? t.asc : t.desc}`;
    };
    heads.forEach((cell, index) => {
      if (!cell.textContent.trim()) return;
      cell.setAttribute('aria-sort', 'none');
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'table-sort';
      button.setAttribute('aria-label', `${t.sort} ${cell.textContent.trim()}`);
      while (cell.firstChild) button.append(cell.firstChild);
      cell.append(button);
      button.addEventListener('click', () => {
        const current = cell.getAttribute('aria-sort');
        applySort(index, current === 'none' ? 'asc' : current === 'ascending' ? 'desc' : 'none');
      });
    });

    // Filtering ---------------------------------------------------------------
    const host = table.closest('.post-table-scroll') || table;
    if (original.length > 8) {
      const bar = document.createElement('div');
      bar.className = 'table-tools';
      const label = document.createElement('label');
      label.setAttribute('for', `${table.id}-filter`);
      label.textContent = t.filter;
      const input = document.createElement('input');
      input.type = 'search';
      input.id = `${table.id}-filter`;
      input.placeholder = t.placeholder;
      input.autocomplete = 'off';
      input.setAttribute('aria-controls', table.id);
      const count = document.createElement('output');
      count.setAttribute('for', input.id);
      const paint = () => {
        const needle = input.value.trim().toLocaleLowerCase();
        let shown = 0;
        for (const row of original) {
          const hit = !needle || row.textContent.toLocaleLowerCase().includes(needle);
          row.hidden = !hit;
          if (hit) shown += 1;
        }
        count.textContent = shown ? `${shown} ${t.of} ${original.length} ${t.rows}` : t.empty;
      };
      input.addEventListener('input', paint);
      bar.append(label, input, count);
      host.before(bar);
      paint();
    }
    host.after(live);
  }
})();
