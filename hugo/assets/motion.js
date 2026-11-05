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
  document.addEventListener('visibilitychange', () => { if (document.hidden) return; });
  // Opening a disclosure reveals what it contains without waiting for a scroll.
  document.addEventListener('toggle', (event) => {
    if (event.target.open) event.target.querySelectorAll('[data-reveal]').forEach((node) => node.classList.add('is-visible'));
  }, true);
  root.dataset.revealReady = 'true';
})();
