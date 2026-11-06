/* Radial skill map (SkillSet-style tree) for hugo/layouts/shortcodes/skill-map.html.
   Data: hugo/data/skill_tree.json, generated from data/cv.yaml by scripts/build/generate_cv.py.
   The root sits in the centre, categories on the inner ring and skills on the outer ring. Every
   visible leaf gets an equal angular slot, so leaf labels never overlap; labels run along the
   radius and flip on the left half so they always read left to right. Clicking (or Enter/Space
   on) a category collapses or expands its branch. The nested list beside it is the text version. */
(() => {
  const NS = 'http://www.w3.org/2000/svg';
  const make = (tag, attrs = {}, parent) => {
    const node = document.createElementNS(NS, tag);
    for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
    if (parent) parent.append(node);
    return node;
  };
  const polar = (angle, radius) => [radius * Math.cos(angle - Math.PI / 2), radius * Math.sin(angle - Math.PI / 2)];
  const degrees = (angle) => (angle * 180) / Math.PI;

  for (const host of document.querySelectorAll('[data-skill-map]')) {
    const data = JSON.parse(host.querySelector('script[type="application/json"]').textContent);
    const fr = document.documentElement.lang.startsWith('fr');
    const stage = host.querySelector('[data-skill-map-stage]');
    const collapsed = new Set();
    const R1 = 190, R2 = 286, LABEL = 8;

    function render() {
      const categories = data.children;
      const slots = categories.reduce((sum, c) => sum + (collapsed.has(c.name) ? 1 : c.children.length), 0);
      const step = (Math.PI * 2) / Math.max(slots, 1);
      // Longest outer label sets the canvas size, so nothing is clipped at the edges.
      const longest = Math.max(...categories.flatMap((c) => (collapsed.has(c.name) ? [0] : c.children.map((s) => s.name.length))));
      const extent = Math.ceil(R2 + LABEL + longest * 7.4 + 16);
      const svg = make('svg', {
        viewBox: `${-extent} ${-extent} ${extent * 2} ${extent * 2}`,
        role: 'group',
        'aria-label': fr ? 'Carte radiale des compétences' : 'Radial skill map',
        class: 'skill-map-svg',
      });
      const links = make('g', { class: 'skill-map-links' }, svg);
      const nodes = make('g', { class: 'skill-map-nodes' }, svg);
      make('circle', { r: 6, class: 'skill-map-root' }, nodes);
      let cursor = 0;
      categories.forEach((category, index) => {
        const isCollapsed = collapsed.has(category.name);
        const span = isCollapsed ? 1 : category.children.length;
        const start = cursor;
        cursor += span;
        const middle = (start + span / 2) * step;
        const [cx, cy] = polar(middle, R1);
        const hue = `var(--skill-hue-${index % 8})`;
        // Root to category: a straight spoke. Category to skill: a radial curve through the ring between them.
        make('path', { d: `M0,0L${cx},${cy}`, class: 'skill-map-link', style: `--hue:${hue}` }, links);
        const branch = make('g', { class: 'skill-map-branch', 'data-category': category.name, style: `--hue:${hue}` }, nodes);
        if (!isCollapsed) {
          category.children.forEach((skill, position) => {
            const angle = (start + position + 0.5) * step;
            const [x, y] = polar(angle, R2);
            const [mx, my] = polar(angle, (R1 + R2) / 2);
            const [px, py] = polar(middle, (R1 + R2) / 2);
            make('path', { d: `M${cx},${cy}C${px},${py} ${mx},${my} ${x},${y}`, class: 'skill-map-link', style: `--hue:${hue}` }, links);
            const flip = angle > Math.PI;
            const rotation = degrees(angle) - 90 + (flip ? 180 : 0);
            const leaf = make('g', { transform: `translate(${x},${y})`, class: `skill-map-leaf${skill.level ? ' is-intermediate' : ''}` }, branch);
            make('circle', { r: 4.5 }, leaf);
            const parent = skill.url ? make('a', { href: skill.url, rel: 'noopener', target: '_blank' }, leaf) : leaf;
            const text = make('text', {
              transform: `rotate(${rotation})`,
              x: flip ? -LABEL : LABEL,
              dy: '0.32em',
              'text-anchor': flip ? 'end' : 'start',
            }, parent);
            text.textContent = skill.name;
            if (skill.level) {
              const title = make('title', {}, parent);
              title.textContent = `${skill.name} (${fr ? 'intermédiaire' : 'intermediate'})`;
            }
          });
        }
        const node = make('g', {
          transform: `translate(${cx},${cy})`,
          class: `skill-map-category${isCollapsed ? ' is-collapsed' : ''}`,
          tabindex: '0',
          role: 'button',
          'aria-expanded': String(!isCollapsed),
          'aria-label': `${category.name}: ${category.children.length} ${fr ? 'compétences' : 'skills'}`,
        }, branch);
        make('circle', { r: 8 }, node);
        // Category labels sit inside the inner ring, pointing at the centre, clear of the leaf curves.
        const flip = middle > Math.PI;
        const text = make('text', {
          transform: `rotate(${degrees(middle) - 90 + (flip ? 180 : 0)})`,
          x: flip ? 14 : -14,
          dy: '0.32em',
          'text-anchor': flip ? 'start' : 'end',
        }, node);
        text.textContent = isCollapsed ? `${category.name} (+${category.children.length})` : category.name;
        const toggle = () => {
          if (collapsed.has(category.name)) collapsed.delete(category.name);
          else collapsed.add(category.name);
          render();
          stage.querySelector(`[data-category="${CSS.escape(category.name)}"] .skill-map-category`)?.focus();
        };
        node.addEventListener('click', toggle);
        node.addEventListener('keydown', (event) => {
          if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); toggle(); }
        });
        node.addEventListener('pointerenter', () => { svg.classList.add('has-focus'); branch.classList.add('is-active'); });
        node.addEventListener('pointerleave', () => { svg.classList.remove('has-focus'); branch.classList.remove('is-active'); });
      });
      stage.replaceChildren(svg);
      // Fit the canvas to what was drawn: measured labels, not an estimate.
      const box = svg.getBBox();
      if (box.width > 0) svg.setAttribute('viewBox', `${box.x - 12} ${box.y - 12} ${box.width + 24} ${box.height + 24}`);
      // On phones the map keeps a readable size and the stage scrolls; start centred on the root.
      if (stage.scrollWidth > stage.clientWidth) stage.scrollLeft = (stage.scrollWidth - stage.clientWidth) / 2;
      host.querySelector('[data-skill-map-reset]').hidden = collapsed.size === 0;
    }

    host.querySelector('[data-skill-map-reset]')?.addEventListener('click', () => { collapsed.clear(); render(); });
    host.querySelector('[data-skill-map-collapse]')?.addEventListener('click', () => {
      data.children.forEach((c) => collapsed.add(c.name));
      render();
    });
    host.classList.add('is-ready');
    render();
  }
})();
