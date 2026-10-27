document.querySelectorAll('[data-deck-viewer]').forEach(viewer => {
  const slides = [...viewer.querySelectorAll('[data-deck-slide]')];
  if (!slides.length) return;
  const previous = viewer.querySelector('[data-deck-prev]');
  const next = viewer.querySelector('[data-deck-next]');
  const select = viewer.querySelector('[data-deck-select]');
  const status = viewer.querySelector('[data-deck-status]');
  let active = 0;
  function show(index) {
    active = Math.max(0, Math.min(slides.length - 1, index));
    slides.forEach((slide, i) => { slide.hidden = i !== active; });
    select.value = String(active);
    previous.disabled = active === 0;
    next.disabled = active === slides.length - 1;
    status.textContent = select.selectedOptions[0].textContent;
  }
  previous.addEventListener('click', () => show(active - 1));
  next.addEventListener('click', () => show(active + 1));
  select.addEventListener('change', () => show(Number(select.value)));
  viewer.querySelector('.deck-slides').addEventListener('keydown', event => {
    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
      event.preventDefault();
      show(active + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  viewer.classList.add('is-enhanced');
  viewer.querySelector('.deck-controls').hidden = false;
  show(0);
});
