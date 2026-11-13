// Tabbed live demos (shortcodes/demos.html). A frame is created only after the reader
// presses start; switching tabs swaps the running demo, and stop removes the frame so the
// GPU context is released.
(() => {
  const safeUrl = value => {
    try {
      const url = new URL(value, location.href);
      return url.protocol === 'https:' ? url : null;
    } catch {
      return null;
    }
  };

  document.querySelectorAll('[data-live-demos]').forEach(root => {
    const tabs = [...root.querySelectorAll('[role="tab"]')];
    const stage = root.querySelector('[data-stage]');
    const placeholder = root.querySelector('[data-placeholder]');
    const desc = root.querySelector('[data-desc]');
    const open = root.querySelector('[data-open]');
    const start = root.querySelector('[data-start]');
    const stop = root.querySelector('[data-stop]');
    const fullscreen = root.querySelector('[data-fullscreen]');
    if (!tabs.length || !stage || !start) return;
    let current = tabs.find(tab => tab.getAttribute('aria-selected') === 'true') || tabs[0];
    let frame = null;

    const load = () => {
      const url = safeUrl(current.dataset.demoUrl);
      if (!url) return;
      // The sandbox is fixed when a frame is created: start a fresh frame when the origin changes.
      if (frame && frame.dataset.origin !== url.origin) {
        frame.remove();
        frame = null;
      }
      if (!frame) {
        frame = document.createElement('iframe');
        frame.loading = 'eager';
        frame.referrerPolicy = 'no-referrer';
        // allow-same-origin only isolates a demo hosted on another origin.
        const sameOrigin = url.origin === location.origin ? '' : ' allow-same-origin';
        frame.setAttribute('sandbox', `allow-scripts${sameOrigin} allow-popups allow-pointer-lock`);
        frame.setAttribute('allow', 'fullscreen; gamepad');
        frame.setAttribute('allowfullscreen', '');
        frame.dataset.origin = url.origin;
        stage.append(frame);
      }
      frame.title = current.textContent.trim();
      frame.src = url.href;
      placeholder.hidden = true;
      stop.hidden = false;
      if (stage.requestFullscreen) fullscreen.hidden = false;
      root.dataset.running = 'true';
    };

    const select = (tab, focus) => {
      current = tab;
      tabs.forEach(item => {
        const active = item === tab;
        item.setAttribute('aria-selected', String(active));
        item.tabIndex = active ? 0 : -1;
      });
      stage.setAttribute('aria-labelledby', tab.id);
      if (desc) desc.textContent = tab.dataset.demoDesc || '';
      const url = safeUrl(tab.dataset.demoUrl);
      if (open && url) open.href = url.href;
      if (focus) tab.focus();
      if (frame) load();
    };

    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => select(tab, false));
      tab.addEventListener('keydown', event => {
        const step = { ArrowRight: 1, ArrowLeft: -1 }[event.key];
        if (step) {
          event.preventDefault();
          select(tabs[(index + step + tabs.length) % tabs.length], true);
        } else if (event.key === 'Home' || event.key === 'End') {
          event.preventDefault();
          select(tabs[event.key === 'Home' ? 0 : tabs.length - 1], true);
        }
      });
    });

    start.addEventListener('click', load);
    stop.addEventListener('click', () => {
      if (document.fullscreenElement === stage) document.exitFullscreen();
      if (frame) frame.remove();
      frame = null;
      placeholder.hidden = false;
      stop.hidden = true;
      fullscreen.hidden = true;
      delete root.dataset.running;
      start.focus();
    });
    fullscreen.addEventListener('click', () => {
      if (document.fullscreenElement === stage) document.exitFullscreen();
      else stage.requestFullscreen?.();
    });
  });
})();
