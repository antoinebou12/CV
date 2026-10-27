(() => {
  const images = [...document.querySelectorAll('.journal-article :is(.article-single-hero, .single-post-content) img')]
    .filter(image => !image.closest('a, button, [data-deck-viewer], .diagram-interactive, .repo-progressive-diagram'));
  if (!images.length) return;
  const fr = document.documentElement.lang.startsWith('fr');
  const dialog = document.createElement('dialog');
  dialog.className = 'article-media-dialog';
  dialog.setAttribute('aria-labelledby', 'media-preview-title');
  const head = document.createElement('div');
  head.className = 'article-media-head';
  const title = document.createElement('h2');
  title.id = 'media-preview-title';
  title.textContent = fr ? 'Aperçu de l’image' : 'Image preview';
  const close = document.createElement('button');
  close.type = 'button';
  close.textContent = fr ? 'Fermer' : 'Close';
  head.append(title, close);
  const preview = document.createElement('img');
  const caption = document.createElement('p');
  const original = document.createElement('a');
  original.textContent = fr ? 'Ouvrir l’image' : 'Open image';
  original.target = '_blank';
  original.rel = 'noopener noreferrer';
  dialog.append(head, preview, caption, original);
  document.body.append(dialog);
  let opener;
  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => opener?.focus({ preventScroll: true }));
  images.forEach(image => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'article-media-open';
    button.setAttribute('aria-label', `${fr ? 'Agrandir l’image' : 'Enlarge image'}: ${image.alt || title.textContent}`);
    image.replaceWith(button);
    button.append(image);
    button.addEventListener('click', () => {
      opener = button;
      preview.src = image.currentSrc || image.src;
      preview.alt = image.alt;
      caption.textContent = image.closest('figure')?.querySelector('figcaption')?.textContent || image.alt;
      original.href = preview.src;
      dialog.showModal();
      close.focus();
    });
  });
})();
