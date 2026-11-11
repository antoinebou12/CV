// Audio story player (partials/podcast-player.html): a playback-speed button that remembers
// the reader's choice. The native audio controls do the rest.
(() => {
  const speeds = [1, 1.25, 1.5, 0.85];
  let saved = 1;
  try { saved = Number(localStorage.getItem('podcast-speed')) || 1; } catch { /* storage unavailable */ }
  if (!speeds.includes(saved)) saved = 1;

  document.querySelectorAll('.podcast-player').forEach(player => {
    const audio = player.querySelector('audio');
    const button = player.querySelector('[data-podcast-speed]');
    if (!audio || !button) return;
    const apply = rate => {
      audio.defaultPlaybackRate = rate;
      audio.playbackRate = rate;
      button.textContent = `${String(rate).replace('.', button.lang === 'fr' ? ',' : '.')}×`;
    };
    button.lang = document.documentElement.lang || 'en';
    button.hidden = false;
    apply(saved);
    button.addEventListener('click', () => {
      const next = speeds[(speeds.indexOf(audio.playbackRate) + 1) % speeds.length] || 1;
      apply(next);
      try { localStorage.setItem('podcast-speed', String(next)); } catch { /* storage unavailable */ }
    });
  });
})();
