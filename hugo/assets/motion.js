/* Entrance reveals for cards and document sections (see motion.css).
   Reduced motion, Save-Data and the paused-motion preference reveal everything at once. */
(() => {
  const root = document.documentElement;
  const targets = [...document.querySelectorAll('[data-reveal]')];
  if (!targets.length) return;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const showAll = () => targets.forEach((node) => node.classList.add('is-visible'));
  if (reduce.matches || navigator.connection?.saveData || !('IntersectionObserver' in window)) { showAll(); return; }
  // Stagger siblings inside a group; cap the delay so long lists do not lag.
  for (const group of document.querySelectorAll('[data-reveal-group]')) {
    [...group.querySelectorAll(':scope > [data-reveal], :scope > * > [data-reveal]')].forEach((node, index) => {
      node.style.setProperty('--reveal-index', String(Math.min(index, 6)));
    });
  }
  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    }
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  targets.forEach((node) => {
    const box = node.getBoundingClientRect();
    // Content already on screen at load paints immediately.
    if (box.top < innerHeight && box.bottom > 0) node.classList.add('is-visible');
    else observer.observe(node);
  });
  reduce.addEventListener('change', () => { if (reduce.matches) { observer.disconnect(); showAll(); } });
  addEventListener('beforeprint', showAll);
  // Opening a disclosure reveals what it contains without waiting for a scroll.
  document.addEventListener('toggle', (event) => {
    if (event.target.open) event.target.querySelectorAll('[data-reveal]').forEach((node) => node.classList.add('is-visible'));
  }, true);
  root.dataset.revealReady = 'true';
})();
/* Navigation progress: a thin bar at the top while the next same-origin page loads. */
(() => {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const root = document.documentElement;
  const bar = document.createElement('div');
  bar.className = 'nav-progress'; bar.setAttribute('aria-hidden', 'true');
  bar.append(document.createElement('span'));
  document.body.append(bar);
  let timer = 0;
  const start = () => { clearTimeout(timer); root.classList.remove('nav-progress-done'); root.classList.add('is-navigating'); };
  const finish = () => { root.classList.add('nav-progress-done'); timer = setTimeout(() => root.classList.remove('is-navigating', 'nav-progress-done'), 260); };
  document.addEventListener('click', (event) => {
    const link = event.target.closest('a[href]');
    if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    if (link.target && link.target !== '_self') return;
    const url = new URL(link.href, location.href);
    if (url.origin !== location.origin || link.hasAttribute('download')) return;
    if (url.pathname === location.pathname && url.search === location.search && url.hash) return;
    start();
  });
  addEventListener('pagehide', finish);
  addEventListener('pageshow', () => { root.classList.remove('is-navigating', 'nav-progress-done'); });
  // Lazy demo frames show a spinner until their document loads.
  document.addEventListener('click', (event) => {
    const button = event.target.closest('[data-demo-load]');
    if (!button) return;
    const host = button.closest('[data-demo]')?.querySelector('[data-demo-frame]');
    if (!host || host.querySelector('iframe')) return;
    host.classList.add('is-loading');
    const watch = new MutationObserver(() => {
      const frame = host.querySelector('iframe');
      if (!frame) return;
      watch.disconnect();
      frame.addEventListener('load', () => host.classList.remove('is-loading'), { once: true });
      setTimeout(() => host.classList.remove('is-loading'), 15000);
    });
    watch.observe(host, { childList: true });
  }, true);
})();