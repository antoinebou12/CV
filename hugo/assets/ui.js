// Shared UI behaviour (assets/ui.css). Counts a [data-count] number up once, when it scrolls
// into view. The real number is already in the HTML, so nothing depends on this script, and
// readers who ask for reduced motion keep the static number.
(() => {
  const nodes = [...document.querySelectorAll('[data-count]')];
  if (!nodes.length || !('IntersectionObserver' in window)) return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const run = (node) => {
    const target = Number(node.dataset.count);
    if (!Number.isFinite(target) || target < 2) return;
    const duration = 900;
    const start = performance.now();
    const step = (now) => {
      // The frame timestamp can be slightly earlier than `start`, so clamp both ends.
      const t = Math.max(0, Math.min(1, (now - start) / duration));
      const eased = 1 - Math.pow(1 - t, 4);
      node.textContent = String(Math.round(target * eased));
      if (t < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      observer.unobserve(entry.target);
      run(entry.target);
    }
  }, { threshold: 0.6 });
  nodes.forEach((node) => observer.observe(node));
})();
