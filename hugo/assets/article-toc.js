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
  // Position-based spy: the current section is the last heading above the reading line
  // (35% down the viewport); at the end of the page the last section wins.
  let frame = 0;
  const spy = () => {
    frame = 0;
    const line = innerHeight * 0.35;
    let current = headings[0];
    for (const item of headings) if (item.target.getBoundingClientRect().top <= line) current = item;
    if (scrollY + innerHeight >= document.documentElement.scrollHeight - 2) current = headings[headings.length - 1];
    setCurrent(current.target.id);
  };
  const schedule = () => { if (!frame) frame = requestAnimationFrame(spy); };
  addEventListener('scroll', schedule, { passive: true });
  addEventListener('resize', schedule);
  spy();
  for (const { link, target } of headings) {
    link.addEventListener('click', () => {
      setCurrent(target.id);
      if (!wide.matches) toc.open = false;
    });
  }
})();
