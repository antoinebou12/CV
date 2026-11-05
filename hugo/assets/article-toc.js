/* Article table of contents: on wide screens the disclosure becomes a sticky side rail
   that follows the reader (aria-current marks the section in view); on phones it stays a
   collapsible block above the text. The markup is Hugo's TableOfContents, unchanged. */
(() => {
  const toc = document.querySelector('[data-article-toc]');
  const article = document.querySelector('.journal-article');
  const content = document.querySelector('.single-post-content');
  if (!toc || !article || !content) return;
  const links = [...toc.querySelectorAll('a[href^="#"]')];
  const headings = links
    .map((link) => ({ link, target: document.getElementById(decodeURIComponent(link.hash.slice(1))) }))
    .filter((item) => item.target);
  if (!headings.length) return;
  const wide = matchMedia('(min-width: 1100px)');
  const rail = document.createElement('aside');
  rail.className = 'article-toc-rail';
  const place = () => {
    if (wide.matches) {
      if (toc.parentElement !== rail) { rail.append(toc); article.prepend(rail); article.classList.add('has-toc-rail'); }
      toc.open = true;
    } else if (toc.parentElement === rail) {
      content.parentElement.prepend(toc);
      rail.remove();
      article.classList.remove('has-toc-rail');
      toc.open = false;
    }
  };
  place();
  wide.addEventListener('change', place);
  const setCurrent = (id) => {
    for (const { link, target } of headings) {
      const on = target.id === id;
      link.classList.toggle('is-current', on);
      if (on) link.setAttribute('aria-current', 'true'); else link.removeAttribute('aria-current');
    }
  };
  if ('IntersectionObserver' in window) {
    const visible = new Map();
    const observer = new IntersectionObserver((entries) => {
      for (const entry of entries) visible.set(entry.target, entry.isIntersecting);
      const first = headings.find(({ target }) => visible.get(target));
      if (first) setCurrent(first.target.id);
    }, { rootMargin: '-72px 0px -60% 0px', threshold: [0, 1] });
    headings.forEach(({ target }) => observer.observe(target));
  }
  for (const { link, target } of headings) {
    link.addEventListener('click', () => {
      setCurrent(target.id);
      if (!wide.matches) toc.open = false;
    });
  }
})();
