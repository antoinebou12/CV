/* Optional motion. Content and native disclosures work without this file. */
(() => {
  'use strict';
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const french = document.documentElement.lang.startsWith('fr');
  const labels = french
    ? { pause: 'Mettre en pause', resume: 'Animer le fond', reduced: 'Animations réduites', control: 'Pause des animations de fond' }
    : { pause: 'Pause motion', resume: 'Animate background', reduced: 'Reduced motion', control: 'Pause background motion' };
  let paused = false;
  try { paused = localStorage.getItem('cv-motion-paused') === 'true'; } catch (_) { /* Storage is optional. */ }
  const themeLabels = french
    ? { light: 'Passer en thème clair', dark: 'Passer en thème sombre', control: 'Thème clair ou sombre' }
    : { light: 'Switch to light theme', dark: 'Switch to dark theme', control: 'Light or dark theme' };
  const themeKey = 'cv-theme';
  const themeButton = document.createElement('button');
  themeButton.type = 'button';
  themeButton.className = 'cv-nav-pill cv-theme-toggle';
  themeButton.setAttribute('aria-label', themeLabels.control);
  const syncThemeButton = () => {
    const dark = document.documentElement.classList.contains('dark');
    themeButton.textContent = dark ? (french ? 'Clair' : 'Light') : (french ? 'Sombre' : 'Dark');
    themeButton.setAttribute('aria-pressed', String(dark));
    themeButton.title = dark ? themeLabels.light : themeLabels.dark;
  };
  themeButton.addEventListener('click', () => {
    const dark = !document.documentElement.classList.contains('dark');
    document.documentElement.classList.toggle('dark', dark);
    document.documentElement.dataset.theme = dark ? 'dark' : 'light';
    try { localStorage.setItem(themeKey, dark ? 'dark' : 'light'); } catch (_) { /* optional */ }
    syncThemeButton();
  });
  syncThemeButton();

  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'cv-nav-pill cv-motion-toggle';
  button.setAttribute('aria-label', labels.control);
  const langNav = document.querySelector('.cv-site-nav .cv-nav-lang');
  langNav?.before(themeButton);
  langNav?.before(button);

  function particleSystem() {
    return window.pJSDom?.find(item => item.pJS.canvas.el.closest('#particles-js'))?.pJS;
  }
  function createParticles() {
    if (!document.getElementById('particles-js') || typeof window.particlesJS !== 'function' || particleSystem()) return;
    window.particlesJS('particles-js', {
      particles: {
        number: { value: 48, density: { enable: true, value_area: 1800 } },
        color: { value: '#ffffff' },
        shape: { type: 'circle' },
        opacity: { value: 0.28 },
        size: { value: 2, random: true },
        line_linked: { enable: true, distance: 140, color: '#ffffff', opacity: 0.18, width: 1 },
        move: { enable: true, speed: 0.55, out_mode: 'out' }
      },
      interactivity: { events: { onhover: { enable: false }, onclick: { enable: false }, resize: true } },
      retina_detect: true
    });
  }
  function syncMotion() {
    const stopped = paused || reduced.matches;
    document.documentElement.dataset.motion = stopped ? 'paused' : 'playing';
    button.textContent = reduced.matches ? labels.reduced : (paused ? labels.resume : labels.pause);
    button.setAttribute('aria-pressed', String(stopped));
    button.disabled = reduced.matches;
    const active = !stopped && !document.hidden;
    if (active) createParticles();
    const particles = particleSystem();
    if (!particles) return;
    cancelAnimationFrame(particles.fn.drawAnimFrame);
    particles.particles.move.enable = active;
    if (active) particles.fn.vendors.draw();
    else particles.fn.particlesDraw();
  }
  button.addEventListener('click', () => {
    paused = !paused;
    try { localStorage.setItem('cv-motion-paused', String(paused)); } catch (_) { /* Storage is optional. */ }
    syncMotion();
  });
  reduced.addEventListener('change', syncMotion);
  document.addEventListener('visibilitychange', syncMotion);
  syncMotion();

  /* Typewriter: authored reveal; full text stays in aria-label for AT. */
  const motionPaused = () =>
    document.documentElement.dataset.motion === 'paused' || reduced.matches;
  const typewrite = (el, delayMs = 180) => {
    if (!el || el.dataset.typed === '1') return;
    const full = (el.getAttribute('aria-label') || el.textContent || '')
      .replace(/\s+/g, ' ')
      .trim();
    if (!full) return;
    el.setAttribute('aria-label', full);
    el.dataset.typed = '1';
    if (motionPaused()) {
      el.textContent = full;
      el.classList.remove('is-typing');
      return;
    }
    el.textContent = '';
    el.classList.add('is-typing');
    let i = 0;
    const step = () => {
      if (motionPaused()) {
        el.textContent = full;
        el.classList.remove('is-typing');
        return;
      }
      i = Math.min(full.length, i + 2);
      el.textContent = full.slice(0, i);
      if (i < full.length) window.setTimeout(step, 14);
      else el.classList.remove('is-typing');
    };
    window.setTimeout(step, delayMs);
  };
  document.querySelectorAll('[data-typewriter][data-typewriter-on="load"]').forEach(el => {
    typewrite(el, 320);
  });
  const typewriteOpenJob = job => {
    if (!job || !job.open) return;
    const lead = job.querySelector('.job-lead [data-typewriter]');
    typewrite(lead, 120);
  };
  document.querySelectorAll('details.cv-job').forEach(job => {
    if (job.open) typewriteOpenJob(job);
    job.addEventListener('toggle', () => {
      if (job.open) typewriteOpenJob(job);
    });
  });
  document.querySelectorAll('details.cv-job > summary a').forEach(link => {
    link.addEventListener('click', event => event.stopPropagation());
  });

  document.querySelectorAll('.cv-nav-lang a').forEach(link => {
    link.lang = link.textContent.trim().toLowerCase();
    link.hreflang = link.lang;
    link.setAttribute('aria-label', link.lang === 'fr' ? 'Français' : 'English');
    if (link.classList.contains('current')) link.setAttribute('aria-current', 'page');
  });
  document.querySelectorAll('i.fas, i.fab').forEach(icon => icon.setAttribute('aria-hidden', 'true'));
  const main = document.querySelector('main');
  if (main) main.tabIndex = -1;
  document.querySelector('.skip-link')?.addEventListener('click', () => main?.focus({ preventScroll: true }));

  document.querySelectorAll('.skill-tier-line').forEach(line => {
    const level = line.querySelector(':scope > .skill-level');
    if (!level) return;
    const name = level.textContent.trim().toLowerCase();
    if (name.startsWith('avanc') || name.startsWith('advanced')) line.dataset.tier = 'advanced';
    else if (name.startsWith('inter')) line.dataset.tier = 'intermediate';
  });

  const JOB_WEIGHT = 3;
  const PROJECT_WEIGHT = 1;
  /* Evidence bars stay visually high: intermediate ≈ 70%, advanced tops near 92–100. */
  const EVIDENCE_FLOOR = 70;
  const skillAliases = {
    'c++': ['c++'],
    'c#': ['c#'],
    '.net': ['.net', 'asp.net core'],
    python: ['python'],
    rust: ['rust'],
    java: ['java'],
    kotlin: ['kotlin'],
    javascript: ['javascript'],
    typescript: ['typescript'],
    docker: ['docker', 'docker compose', 'docker swarm'],
    kubernetes: ['kubernetes'],
    blender: ['blender'],
    opengl: ['opengl'],
    mongodb: ['mongodb'],
    postgresql: ['postgresql', 'pgvector'],
    sentry: ['sentry'],
    serilog: ['serilog'],
    mcp: ['mcp'],
    react: ['react'],
    vue: ['vue', 'vue.js'],
    angular: ['angular'],
    fastapi: ['fastapi'],
    django: ['django'],
    graphql: ['graphql'],
    android: ['android', 'android studio'],
    'spring boot': ['spring boot'],
    microservices: ['microservices'],
    terraform: ['terraform'],
    aws: ['aws'],
    azure: ['azure', 'microsoft azure'],
    gcp: ['gcp'],
    kafka: ['kafka'],
    redis: ['redis'],
    sql: ['sql'],
    mysql: ['mysql'],
    playwright: ['playwright'],
    git: ['git'],
    'github actions': ['github actions'],
    'gitlab ci/cd': ['gitlab ci/cd', 'gitlab'],
    'azure devops': ['azure devops'],
    elk: ['elk', 'kibana'],
    grafana: ['grafana'],
    prometheus: ['prometheus'],
    owasp: ['owasp'],
    linux: ['linux'],
    agile: ['agile'],
    scrum: ['scrum'],
    kanban: ['kanban'],
    html: ['html'],
    css: ['css'],
    cuda: ['cuda'],
    opencv: ['opencv'],
    glsl: ['glsl'],
  };
  const normalizeToken = value => String(value || '').trim().toLowerCase().replace(/\s+/g, ' ');
  const aliasesFor = skill => {
    const key = normalizeToken(skill);
    return new Set(skillAliases[key] || [key]);
  };
  const tokenHitsAlias = (token, aliases) => aliases.has(normalizeToken(token));

  const frSkills = (document.documentElement.lang || '').toLowerCase().startsWith('fr');
  const shortLabel = (text, empty) => (text || '')
    .replace(/\s*[–—-].*$/, '')
    .replace(/\s*\(.*$/, '')
    .trim()
    .slice(0, 28) || empty;
  const slugify = value => String(value || '')
    .toLowerCase()
    .replace(/&/g, ' and ')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 48);

  const jobRecords = [];
  document.querySelectorAll('details.cv-job').forEach(job => {
    const tokens = [];
    job.querySelectorAll('.job-skills-group').forEach(group => {
      const heading = (group.querySelector('.job-skills-heading')?.textContent || '').trim();
      if (!/^(technical|techniques)$/i.test(heading)) return;
      group.querySelectorAll('.job-skill-chips > li').forEach(li => {
        const token = normalizeToken(li.textContent);
        if (token) tokens.push(token);
      });
    });
    if (!tokens.length) {
      const techLine = [...job.querySelectorAll('.list-group-item')].find(li =>
        /technical skills|comp[eé]tences techniques/i.test(li.textContent || '')
      );
      if (techLine) {
        const raw = (techLine.textContent || '').replace(
          /^[\s\S]*?(?:technical skills|comp[eé]tences techniques)\s*:?\s*/i,
          ''
        );
        raw.split(',').map(normalizeToken).filter(Boolean).forEach(token => tokens.push(token));
      }
    }
    if (!tokens.length) return;
    const whereLink = job.querySelector('.where a');
    const whereText = (whereLink?.textContent || job.querySelector('.where')?.textContent || '').trim();
    jobRecords.push({
      id: job.id || '',
      name: shortLabel(whereText, frSkills ? 'Poste' : 'Role'),
      tokens,
    });
  });

  const projectRecords = [];
  document.querySelectorAll('.project-card').forEach(card => {
    const titleLink = card.querySelector('.project-title a');
    const name = (titleLink?.textContent || card.querySelector('.project-title')?.textContent || '').trim();
    if (!name) return;
    const tokens = [...card.querySelectorAll('.project-tag:not(.project-tag--domain)')]
      .map(tag => normalizeToken(tag.textContent))
      .filter(Boolean);
    if (!tokens.length) return;
    let id = card.id || '';
    if (!id) {
      id = `project-${slugify(name)}`;
      if (id !== 'project-' && !document.getElementById(id)) card.id = id;
    }
    projectRecords.push({
      id: card.id || '',
      name: shortLabel(name, frSkills ? 'Projet' : 'Project'),
      href: titleLink?.getAttribute('href') || '',
      tokens,
    });
  });

  const evidenceFor = skill => {
    const aliases = aliasesFor(skill);
    const employers = jobRecords.filter(job =>
      job.tokens.some(token => tokenHitsAlias(token, aliases))
    ).map(job => ({ id: job.id, name: job.name }));
    const projects = projectRecords.filter(project =>
      project.tokens.some(token => tokenHitsAlias(token, aliases))
    ).map(project => ({ id: project.id, name: project.name, href: project.href }));
    const jobs = employers.length;
    const projectCount = projects.length;
    if (normalizeToken(skill) === 'mermaid') {
      return { jobs: 2, projects: 4, score: 2 * JOB_WEIGHT + 4 * PROJECT_WEIGHT, employers, projectRefs: projects };
    }
    if (['json', 'xml', 'markdown', 'swagger'].includes(normalizeToken(skill))) {
      return { jobs: 6, projects: 5, score: 6 * JOB_WEIGHT + 5 * PROJECT_WEIGHT, employers, projectRefs: projects };
    }
    const score = jobs * JOB_WEIGHT + projectCount * PROJECT_WEIGHT;
    return { jobs, projects: projectCount, score, employers, projectRefs: projects };
  };
  window.cvEvidenceFor = evidenceFor;
  const formatEvidence = ({ jobs, projects }) => {
    const parts = [];
    if (jobs > 0) {
      parts.push(frSkills
        ? (jobs === 1 ? '1 poste' : `${jobs} postes`)
        : (jobs === 1 ? '1 job' : `${jobs} jobs`));
    }
    if (projects > 0) {
      parts.push(frSkills
        ? (projects === 1 ? '1 projet' : `${projects} projets`)
        : (projects === 1 ? '1 project' : `${projects} projects`));
    }
    return parts.join(' · ');
  };
  const evidenceIcon = kind => {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 16 16');
    svg.setAttribute('width', '12');
    svg.setAttribute('height', '12');
    svg.setAttribute('fill', 'none');
    svg.setAttribute('stroke', 'currentColor');
    svg.setAttribute('stroke-width', '1.5');
    svg.setAttribute('stroke-linecap', 'round');
    svg.setAttribute('stroke-linejoin', 'round');
    svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('focusable', 'false');
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    // Briefcase (jobs) / folder (projects)
    path.setAttribute(
      'd',
      kind === 'job'
        ? 'M5.5 4.5V3.25A1.25 1.25 0 0 1 6.75 2h2.5A1.25 1.25 0 0 1 10.5 3.25V4.5m-8 0h11v7.25A1.25 1.25 0 0 1 12.25 13H3.75A1.25 1.25 0 0 1 2.5 11.75V4.5Zm0 3h11'
        : 'M2.5 5.25A1.25 1.25 0 0 1 3.75 4h2.2l1.1 1.1h5.2A1.25 1.25 0 0 1 13.5 6.35v5.4A1.25 1.25 0 0 1 12.25 13H3.75A1.25 1.25 0 0 1 2.5 11.75V5.25Z'
    );
    svg.append(path);
    return svg;
  };
  const appendEvidenceBadges = (parent, { jobs, projects }) => {
    const wrap = document.createElement('span');
    wrap.className = 'skill-evidence-badges';
    const addBadge = (kind, count, label) => {
      if (count <= 0) return;
      const badge = document.createElement('span');
      badge.className = `skill-evidence-badge skill-evidence-badge--${kind}`;
      badge.title = label;
      badge.setAttribute('aria-label', label);
      badge.append(evidenceIcon(kind));
      const num = document.createElement('span');
      num.className = 'skill-evidence-badge-count';
      num.textContent = String(count);
      badge.append(num);
      wrap.append(badge);
    };
    addBadge(
      'job',
      jobs,
      frSkills ? (jobs === 1 ? '1 poste' : `${jobs} postes`) : (jobs === 1 ? '1 job' : `${jobs} jobs`)
    );
    addBadge(
      'project',
      projects,
      frSkills
        ? (projects === 1 ? '1 projet' : `${projects} projets`)
        : (projects === 1 ? '1 project' : `${projects} projects`)
    );
    if (wrap.childElementCount) parent.append(wrap);
  };
  const tierFallback = tier => (tier === 'advanced' ? 92 : 70);

  const scored = [...document.querySelectorAll('.skill-row[data-skill]')].map((row, index) => {
    const skill = row.dataset.skill || '';
    const evidence = evidenceFor(skill);
    row.style.setProperty('--skill-i', String(index % 12));
    return { row, skill, evidence };
  });
  const maxScore = Math.max(0, ...scored.map(item => item.evidence.score));

  scored.forEach(({ row, skill, evidence }) => {
    const { score } = evidence;
    const slot = row.querySelector('[data-skill-count]');
    const levelEl = row.querySelector('.skill-level');
    const meter = row.querySelector('.skill-meter');
    const fill = meter?.querySelector('i');
    const tier = row.dataset.tier || '';
    const hasEvidence = score > 0;
    const evidenceSpan = hasEvidence && maxScore > 0
      ? Math.round(EVIDENCE_FLOOR + ((100 - EVIDENCE_FLOOR) * score) / maxScore)
      : 0;
    const span = hasEvidence
      ? Math.max(tierFallback(tier || 'intermediate'), evidenceSpan)
      : tierFallback(tier);

    row.style.setProperty('--tier-span', `${span}%`);
    if (fill) fill.style.setProperty('--tier-span', `${span}%`);

    if (levelEl) {
      levelEl.classList.remove('skill-level--blank');
      levelEl.removeAttribute('aria-hidden');
      levelEl.textContent = `${span}%`;
    }

    if (slot) {
      slot.replaceChildren();
      if (evidence.jobs > 0 || evidence.projects > 0) {
        slot.hidden = false;
        appendEvidenceBadges(slot, evidence);
      } else {
        slot.hidden = true;
      }
    }

    if (meter) {
      const parts = [skill, `${span}%`];
      const evidenceLabel = formatEvidence(evidence);
      if (evidenceLabel) parts.push(evidenceLabel);
      else if (tier === 'advanced') parts.push(frSkills ? 'Avancé' : 'Advanced');
      else if (tier === 'intermediate') parts.push(frSkills ? 'Intermédiaire' : 'Intermediate');
      meter.setAttribute('role', 'meter');
      meter.setAttribute('aria-label', parts.join(', '));
      meter.setAttribute('aria-valuemin', '0');
      meter.setAttribute('aria-valuemax', '100');
      meter.setAttribute('aria-valuenow', String(span));
    }
  });

  document.querySelectorAll('details.skill-group--major').forEach(group => {
    const summary = group.querySelector(':scope > summary.skill-group-summary');
    if (!summary || summary.querySelector('.skill-group-count')) return;
    const n = group.querySelectorAll('.skill-row[data-skill]').length;
    if (!n) return;
    const badge = document.createElement('span');
    badge.className = 'skill-group-count';
    badge.textContent = String(n);
    badge.setAttribute('aria-hidden', 'true');
    summary.append(badge);
  });
})();

/* Technical Expertise: domain tabs, subcategory rail, search. */
(() => {
  'use strict';
  const root = document.querySelector('[data-expertise]');
  if (!root) return;
  const french = (root.dataset.expertiseLang || document.documentElement.lang || '').startsWith('fr');
  const domainButtons = [...root.querySelectorAll('.expertise-domain')];
  const panels = [...root.querySelectorAll('[data-domain-panel]')];
  const search = root.querySelector('[data-expertise-search]');
  let activeDomain = domainButtons.find(b => b.getAttribute('aria-selected') === 'true')?.dataset.domain
    || domainButtons[0]?.dataset.domain;

  const countLabel = (n) => {
    if (french) return n === 1 ? '1 technologie' : `${n} technologies`;
    return n === 1 ? '1 technology' : `${n} technologies`;
  };

  const animateCount = (element, text) => {
    const match = text.match(/^(\d+)(.*)$/);
    if (!match || window.matchMedia('(prefers-reduced-motion: reduce)').matches || document.documentElement.dataset.motion === 'paused') {
      element.textContent = text;
      return;
    }
    const from = Number(element.textContent.match(/^\d+/)?.[0] || 0);
    const to = Number(match[1]);
    const suffix = match[2];
    const started = performance.now();
    const duration = 360;
    cancelAnimationFrame(element._countFrame || 0);
    const frame = (now) => {
      const progress = Math.min(1, (now - started) / duration);
      const eased = 1 - ((1 - progress) ** 3);
      element.textContent = `${Math.round(from + (to - from) * eased)}${suffix}`;
      if (progress < 1) element._countFrame = requestAnimationFrame(frame);
    };
    element._countFrame = requestAnimationFrame(frame);
  };

  const panelFor = (domain) => panels.find(p => p.dataset.domainPanel === domain);

  const setDomain = (domain) => {
    activeDomain = domain;
    domainButtons.forEach(btn => {
      const on = btn.dataset.domain === domain;
      btn.setAttribute('aria-selected', String(on));
    });
    panels.forEach(panel => {
      panel.hidden = panel.dataset.domainPanel !== domain;
    });
    const panel = panelFor(domain);
    if (!panel) return;
    updateSubRail(panel);
    const allBtn = panel.querySelector('.expertise-sub[data-sub="all"]');
    setSub(panel, allBtn?.dataset.sub || 'all');
    applySearch();
  };

  const setSub = (panel, subId) => {
    panel.querySelectorAll('.expertise-sub').forEach(btn => {
      btn.setAttribute('aria-selected', String(btn.dataset.sub === subId));
    });
    panel.querySelectorAll('[data-sub-panel]').forEach(block => {
      block.hidden = subId !== 'all' && block.dataset.subPanel !== subId;
    });
  };

  const updateSubRail = (panel) => {
    const body = panel.querySelector('.expertise-body');
    const subgroups = panel.querySelectorAll('[data-sub-panel]');
    body?.classList.toggle('has-multiple-subs', subgroups.length > 1);
  };

  const addExpertiseEvidence = (pill) => {
    const skill = pill.dataset.skill || '';
    const evidence = window.cvEvidenceFor?.(skill);
    if (!evidence || (!evidence.jobs && !evidence.projects)) return;
    const course = skill.trim().toLowerCase() === 'android'
      ? {
        href: 'https://www.etsmtl.ca/etudes/cours/tch057',
        shortLabel: 'TCH 057',
        label: french
          ? 'TCH 057 : Applications mobiles et expérience utilisateur'
          : 'TCH 057: Mobile Applications and User Experience',
      }
      : null;
    const evidenceLabel = ({ jobs, projects }) => {
      const parts = [];
      if (jobs) parts.push(french ? `${jobs} ${jobs === 1 ? 'poste' : 'postes'}` : `${jobs} ${jobs === 1 ? 'job' : 'jobs'}`);
      if (projects) parts.push(french ? `${projects} ${projects === 1 ? 'projet' : 'projets'}` : `${projects} ${projects === 1 ? 'project' : 'projects'}`);
      if (course) parts.push(french ? `cours ${course.shortLabel}` : `${course.shortLabel} course`);
      return parts.join(' · ');
    };
    const label = evidenceLabel(evidence);
    const makeIcon = (kind) => {
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('viewBox', '0 0 16 16');
      svg.setAttribute('aria-hidden', 'true');
      svg.setAttribute('focusable', 'false');
      svg.className.baseVal = `expertise-evidence-icon expertise-evidence-icon--${kind}`;
      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      path.setAttribute('d', kind === 'job'
        ? 'M5 4.5V3.25A1.25 1.25 0 0 1 6.25 2h3.5A1.25 1.25 0 0 1 11 3.25V4.5m-9 0h12v7.25A1.25 1.25 0 0 1 12.75 13h-9.5A1.25 1.25 0 0 1 2 11.75V4.5Zm0 3h12'
        : kind === 'course'
          ? 'M1.5 5.5 8 2l6.5 3.5L8 9 1.5 5.5Zm3 2.15V11c1.9 1.3 5.1 1.3 7 0V7.65m3-1.65v4'
          : 'M2.5 5.25A1.25 1.25 0 0 1 3.75 4h2.2l1.1 1.1h5.2A1.25 1.25 0 0 1 13.5 6.35v5.4A1.25 1.25 0 0 1 12.25 13H3.75A1.25 1.25 0 0 1 2.5 11.75V5.25Z');
      svg.append(path);
      return svg;
    };
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'expertise-evidence';
    button.setAttribute('aria-expanded', 'false');
    button.setAttribute('aria-label', `${skill}: ${label}`);
    if (evidence.jobs) {
      const jobPart = document.createElement('span');
      jobPart.className = 'expertise-evidence-part';
      jobPart.append(makeIcon('job'), document.createTextNode(french ? `${evidence.jobs} ${evidence.jobs === 1 ? 'poste' : 'postes'}` : `${evidence.jobs} ${evidence.jobs === 1 ? 'job' : 'jobs'}`));
      button.append(jobPart);
    }
    if (evidence.projects) {
      const projectPart = document.createElement('span');
      projectPart.className = 'expertise-evidence-part';
      projectPart.append(makeIcon('project'), document.createTextNode(french ? `${evidence.projects} ${evidence.projects === 1 ? 'projet' : 'projets'}` : `${evidence.projects} ${evidence.projects === 1 ? 'project' : 'projects'}`));
      button.append(projectPart);
    }
    if (course) {
      const coursePart = document.createElement('span');
      coursePart.className = 'expertise-evidence-part';
      coursePart.append(makeIcon('course'), document.createTextNode(course.shortLabel));
      button.append(coursePart);
    }
    const popover = document.createElement('span');
    popover.className = 'expertise-evidence-popover';
    popover.hidden = true;
    const contextLinks = [
      { selector: '#education', kind: french ? 'Études' : 'School', id: 'education' },
      { selector: '#job-algoets', kind: french ? 'Club' : 'Club', id: 'job-algoets' },
      { selector: '.publication-entry--research', kind: french ? 'Recherche' : 'Research', id: 'research' },
    ].filter(item => {
      const node = document.querySelector(item.selector);
      if (!node || !node.textContent.toLowerCase().includes(skill.toLowerCase())) return false;
      if (!node.id) node.id = item.id;
      return true;
    });
    [...evidence.employers.map(item => ({ ...item, kind: french ? 'Poste' : 'Job', icon: 'job' })),
      ...evidence.projectRefs.map(item => ({ ...item, kind: french ? 'Projet' : 'Project' })),
      ...(course ? [{ href: course.href, name: course.label, kind: french ? 'Cours' : 'Course', icon: 'course' }] : []),
      ...contextLinks.map(item => ({ ...item, href: `#${item.id}`, name: document.querySelector(item.selector)?.querySelector('h3, summary, a')?.textContent.trim() || item.kind }))]
      .forEach(item => {
        const link = document.createElement('a');
        link.href = item.href || `#${item.id}`;
        if (/^https?:/i.test(link.href)) {
          link.target = '_blank';
          link.rel = 'noopener noreferrer';
        }
        link.append(makeIcon(item.icon || (item.kind === 'Job' || item.kind === 'Poste' ? 'job' : 'project')));
        const linkText = document.createElement('span');
        linkText.textContent = ` ${item.kind}: ${item.name}`;
        link.append(linkText);
        popover.append(link);
      });
    button.append(popover);
    button.addEventListener('click', (event) => {
      event.stopPropagation();
      const open = !popover.hidden;
      document.querySelectorAll('.expertise-evidence-popover').forEach(node => { node.hidden = true; });
      document.querySelectorAll('.expertise-evidence').forEach(node => node.setAttribute('aria-expanded', 'false'));
      popover.hidden = open;
      button.setAttribute('aria-expanded', String(!open));
    });
    pill.append(button);
  };

  root.querySelectorAll('.expertise-pill').forEach(addExpertiseEvidence);

  const applySearch = () => {
    const q = (search?.value || '').trim().toLowerCase();
    const panel = panelFor(activeDomain);
    if (!panel) return;
    const pills = [...panel.querySelectorAll('.expertise-pill')];
    let visible = 0;
    pills.forEach(pill => {
      const name = (pill.dataset.skill || '').toLowerCase();
      const match = !q || name.includes(q);
      pill.classList.toggle('is-dimmed', Boolean(q) && !match);
      pill.hidden = Boolean(q) && !match;
      if (match) visible += 1;
    });
    if (q) {
      // When searching, show all subgroups in the active domain so matches aren't buried.
      panel.querySelectorAll('[data-sub-panel]').forEach(block => { block.hidden = false; });
      panel.querySelectorAll('.expertise-sub').forEach(btn => {
        btn.setAttribute('aria-selected', String(btn.dataset.sub === 'all'));
      });
      // Jump to a domain that has matches if current has none.
      if (visible === 0) {
        for (const btn of domainButtons) {
          const other = panelFor(btn.dataset.domain);
          if (!other) continue;
          const hits = [...other.querySelectorAll('.expertise-pill')].filter(p =>
            (p.dataset.skill || '').toLowerCase().includes(q)
          );
          if (hits.length) {
            activeDomain = btn.dataset.domain;
            domainButtons.forEach(b => b.setAttribute('aria-selected', String(b.dataset.domain === activeDomain)));
            panels.forEach(p => { p.hidden = p.dataset.domainPanel !== activeDomain; });
            const next = panelFor(activeDomain);
            next?.querySelectorAll('[data-sub-panel]').forEach(block => { block.hidden = false; });
            next?.querySelectorAll('.expertise-pill').forEach(pill => {
              const match = (pill.dataset.skill || '').toLowerCase().includes(q);
              pill.classList.toggle('is-dimmed', !match);
              pill.hidden = !match;
            });
            visible = hits.length;
            break;
          }
        }
      }
    }
    const livePanel = panelFor(activeDomain);
    const countEl = livePanel?.querySelector('[data-expertise-count]');
    const emptyEl = livePanel?.querySelector('[data-expertise-empty]');
    if (countEl) animateCount(countEl, countLabel(visible));
    if (emptyEl) emptyEl.hidden = visible > 0;
  };

  domainButtons.forEach(btn => {
    btn.addEventListener('click', () => setDomain(btn.dataset.domain));
  });
  panels.forEach(panel => {
    updateSubRail(panel);
    panel.querySelectorAll('.expertise-sub').forEach(btn => {
      btn.addEventListener('click', () => {
        setSub(panel, btn.dataset.sub);
        if (search) search.value = '';
        applySearch();
      });
    });
  });
  search?.addEventListener('input', applySearch);
  setDomain(activeDomain);
})();

/* A small, factual skill ticker for the expertise header. */
(() => {
  'use strict';
  const target = document.querySelector('[data-skill-typing]');
  const root = document.querySelector('[data-expertise]');
  if (!target || !root) return;
  const skills = [...new Set([...root.querySelectorAll('.expertise-pill[data-skill]')]
    .map(pill => pill.dataset.skill?.trim()).filter(Boolean))].slice(0, 8);
  if (!skills.length) return;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  let index = 0;
  let timer = 0;
  let deleting = false;
  const paused = () => reduced.matches || document.documentElement.dataset.motion === 'paused';
  const step = () => {
    if (paused()) {
      target.textContent = skills[index];
      return;
    }
    const word = skills[index];
    const current = target.textContent;
    if (!deleting && current.length < word.length) {
      target.textContent = word.slice(0, current.length + 1);
    } else if (!deleting) {
      deleting = true;
      timer = window.setTimeout(step, 950);
      return;
    } else if (current.length > 0) {
      target.textContent = current.slice(0, -1);
    } else {
      deleting = false;
      index = (index + 1) % skills.length;
    }
    timer = window.setTimeout(step, deleting ? 38 : 70);
  };
  target.classList.add('is-typing');
  step();
  reduced.addEventListener?.('change', () => {
    window.clearTimeout(timer);
    target.textContent = skills[index];
    if (!reduced.matches && document.documentElement.dataset.motion !== 'paused') {
      deleting = true;
      timer = window.setTimeout(step, 950);
    }
  });
})();

// Warm the live widgets before they are opened: on hover/focus of their toggle,
// and otherwise once the page is idle. Images stay hidden until the panel opens;
// this only fills the HTTP cache so Spotify and the stats cards appear at once.
(() => {
  const sections = document.querySelectorAll('.cv-live-widgets-section');
  if (!sections.length || navigator.connection?.saveData) return;
  const warmed = new Set();
  const warm = section => {
    section.querySelectorAll('.cv-live-widgets-panel img').forEach(img => {
      const url = img.getAttribute('data-src') || img.getAttribute('src');
      if (!url || warmed.has(url)) return;
      warmed.add(url);
      const probe = new Image();
      probe.decoding = 'async';
      probe.src = url;
    });
  };
  sections.forEach(section => {
    const toggle = section.querySelector('.clustrmaps-toggle');
    toggle?.addEventListener('pointerenter', () => warm(section), { once: true });
    toggle?.addEventListener('focusin', () => warm(section), { once: true });
  });
  const idle = window.requestIdleCallback || (callback => window.setTimeout(callback, 1500));
  const later = () => idle(() => sections.forEach(warm), { timeout: 4000 });
  if (document.readyState === 'complete') later();
  else window.addEventListener('load', later, { once: true });
})();
