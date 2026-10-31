/* Local particles.js, with an explicit preference and no motion when requested. */
(() => {
  const host = document.getElementById('project-particles');
  const button = document.getElementById('background-motion');
  if (!host || !button || !window.particlesJS) return;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  let paused = false;
  try { paused = localStorage.getItem('background-paused') === 'true'; } catch (_) {}
  function stop() {
    for (const instance of window.pJSDom || []) instance.pJS.fn.vendors.destroypJS();
    window.pJSDom = [];
    host.replaceChildren();
  }
  function sync() {
    stop();
    button.hidden = reduce.matches || !!navigator.connection?.saveData;
    button.textContent = paused ? button.dataset.resume : button.dataset.pause;
    button.setAttribute('aria-pressed', String(!paused));
    if (button.hidden || paused || document.hidden) return;
    window.particlesJS('project-particles', {
      particles: {
        number: { value: 34, density: { enable: true, value_area: 1400 } },
        color: { value: document.documentElement.classList.contains('dark') ? '#70cfc6' : '#426c77' },
        shape: { type: 'circle' }, opacity: { value: 0.35 }, size: { value: 2, random: true },
        line_linked: { enable: true, distance: 140, color: '#639d9a', opacity: 0.15, width: 1 },
        move: { enable: true, speed: 0.3, out_mode: 'out' }
      },
      interactivity: { events: { onhover: { enable: false }, onclick: { enable: false }, resize: true } },
      retina_detect: true
    });
  }
  button.addEventListener('click', () => {
    paused = !paused;
    try { localStorage.setItem('background-paused', String(paused)); } catch (_) {}
    sync();
  });
  reduce.addEventListener('change', sync);
  document.addEventListener('visibilitychange', sync);
  new MutationObserver(sync).observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
  sync();
})();
