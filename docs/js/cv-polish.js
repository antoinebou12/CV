/* Progressive Motion interactions for public CV content. */
(() => {
  const motion = window.Motion;
  const html = document.documentElement;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const forced = matchMedia('(forced-colors: active)');
  const printing = matchMedia('print');
  const french = html.lang.startsWith('fr');
  const allowed = () => motion?.animate && !reduced.matches && !forced.matches && !printing.matches && html.dataset.motion !== 'paused';
  const active = new Map();
  const refreshers = [];
  function stop(node) {
    const record = active.get(node);
    if (!record) return;
    active.delete(node);
    record.control.cancel();
    record.cleanup?.();
    requestAnimationFrame(() => { if (!active.has(node)) record.cleanup?.(); });
  }
  function animate(node, values, options = {}, cleanup) {
    const previous = active.get(node);
    if (previous) { active.delete(node); previous.control.stop(); }
    if (!allowed()) { cleanup?.(); return; }
    const control = motion.animate(node, values, { duration:.2, ease:[.2,.7,.3,1], ...options });
    active.set(node, { control, cleanup });
    Promise.resolve(control.finished || control).then(() => {
      if (active.get(node)?.control === control) { active.delete(node); cleanup?.(); }
    }, () => {});
  }
  const resetVisual = node => { node.style.removeProperty('transform'); node.style.removeProperty('opacity'); };
  function halt() {
    if (allowed()) return;
    [...active.keys()].forEach(stop);
    refreshers.forEach(refresh => refresh());
  }
  for (const media of [reduced,forced,printing]) media.addEventListener('change', halt);
  new MutationObserver(halt).observe(html, { attributes:true, attributeFilter:['data-motion'] });

  // Commit filter state immediately, then animate the visible items to their new positions.
  window.cvAnimateLayout = (root, mutate) => {
    const items = [...root.querySelectorAll('.expertise-pill')];
    items.forEach(stop);
    const before = new Map(items.filter(node => node.getClientRects().length).map(node => [node,node.getBoundingClientRect()]));
    mutate();
    if (!allowed()) return;
    [...root.querySelectorAll('.expertise-pill')].filter(node => node.getClientRects().length).slice(0,80).forEach((node,i) => {
      const old = before.get(node);
      const box = node.getBoundingClientRect();
      const x = old ? old.left - box.left : 0;
      const y = old ? old.top - box.top : 4;
      if (!old || Math.abs(x) + Math.abs(y) > 1) animate(node, { x:[x,0], y:[y,0], opacity:[old ? 1 : .8,1] }, { duration:.2, delay:Math.min(i,5) * .012 }, () => resetVisual(node));
    });
  };

  function initialize() {
    const rail = document.querySelector('.expertise-domains');
    if (rail) {
      const indicator = document.createElement('span');
      indicator.className = 'cv-skill-indicator';
      indicator.setAttribute('aria-hidden','true');
      rail.prepend(indicator);
      rail.dataset.sliderReady = 'true';
      function update(slide = true) {
        const selected = rail.querySelector('.expertise-domain[aria-selected="true"]');
        if (!selected) return;
        const parent = rail.getBoundingClientRect();
        const box = selected.getBoundingClientRect();
        const target = { x:box.left-parent.left, y:box.top-parent.top, width:box.width, height:box.height };
        if (slide && allowed()) animate(indicator,target,{duration:.2});
        else { stop(indicator); indicator.style.transform = `translate(${target.x}px,${target.y}px)`; indicator.style.width = `${target.width}px`; indicator.style.height = `${target.height}px`; }
      }
      new MutationObserver(() => update()).observe(rail,{subtree:true,attributes:true,attributeFilter:['aria-selected']});
      if ('ResizeObserver' in window) new ResizeObserver(() => update(false)).observe(rail);
      refreshers.push(() => update(false));
      update(false);
    }

    const projects = document.getElementById('projects');
    if (projects) {
      const sectionBody = projects.querySelector(':scope > .cv-section-body');
      const cards = [...projects.querySelectorAll('.project-card')];
      const groups = [...projects.querySelectorAll('details.project-group,details.project-subgroup')];
      const toolbar = document.createElement('div'); toolbar.className='cv-project-search';
      const label=document.createElement('label'); label.htmlFor='cv-project-query'; label.textContent=french?'Rechercher un projet':'Find a project';
      const input=document.createElement('input'); input.type='search';input.id='cv-project-query';input.placeholder=french?'Nom, technologie ou sujet':'Name, technology or topic';input.autocomplete='off';
      const status=document.createElement('p');status.className='cv-project-result-count';status.setAttribute('role','status');
      toolbar.append(label,input,status); sectionBody.prepend(toolbar);
      groups.forEach(group=>{
        const summary=group.querySelector(':scope > summary');
        const count=document.createElement('span');count.className='cv-project-group-count';
        count.textContent=String(group.querySelectorAll('.project-card,.list-group-item').length);summary.append(count);
      });
      let savedState;
      const items=[...projects.querySelectorAll('.project-card,.project-subgroup .list-group-item')];
      const normalize=text=>text.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase();
      const searchable=new Map(items.map(item=>[item,normalize(item.textContent)]));
      function filterProjects() {
        const query=normalize(input.value.trim());
        if(query&&!savedState)savedState=new Map(groups.map(group=>[group,group.open]));
        items.forEach(item=>{item.hidden=!!query&&!searchable.get(item).includes(query);});
        groups.slice().reverse().forEach(group=>{
          const matching=[...group.querySelectorAll('.project-card,.list-group-item')].some(item=>!item.hidden);
          group.hidden=!!query&&!matching;
          if(query&&matching){stop(group);group.open=true;}
          else if(!query&&savedState)group.open=savedState.get(group);
        });
        if(!query)savedState=undefined;
        const count=items.filter(item=>!item.hidden).length;
        status.textContent=query?(count?`${count} ${french?'résultats':'results'}`:(french?'Aucun résultat. Essayez une autre technologie.':'No results. Try another technology.')):`${cards.length} ${french?'projets, regroupés par type de travail':'projects, grouped by type of work'}`;
      }
      input.addEventListener('input',filterProjects);filterProjects();
    }

    // Native summary activation remains the fallback when motion is unavailable.
    document.querySelectorAll('details.cv-job,details.project-group,details.project-subgroup,details.cv-section').forEach(details => {
      const summary = details.querySelector(':scope > summary');
      if (!summary) return;
      details.dataset.motionAccordion = 'true';
      summary.addEventListener('click', event => {
        if (event.target.closest('a,button,input') || !allowed()) return;
        event.preventDefault();
        const opening = details.dataset.motionTarget ? details.dataset.motionTarget !== 'open' : !details.open;
        const start = details.getBoundingClientRect().height;
        stop(details);
        details.style.height = 'auto';
        details.open = opening;
        if (opening) details.querySelectorAll('[data-typewriter]').forEach(node => { node.textContent = node.getAttribute('aria-label') || node.textContent; node.dataset.typed = '1'; node.classList.remove('is-typing'); });
        const end = details.getBoundingClientRect().height;
        details.open = true;
        details.dataset.motionTarget = opening ? 'open' : 'closed';
        details.style.height = `${start}px`;
        summary.setAttribute('aria-expanded',String(opening));
        const finish = () => {
          if (!opening && details.contains(document.activeElement) && !summary.contains(document.activeElement)) summary.focus({preventScroll:true});
          details.open = opening;
          details.style.removeProperty('height');
          delete details.dataset.motionTarget;
          summary.removeAttribute('aria-expanded');
        };
        animate(details,{height:[`${start}px`,`${end}px`]},{duration:.22},finish);
      });
    });

    const toast = document.createElement('div');
    toast.className = 'cv-copy-feedback'; toast.setAttribute('role','status'); toast.setAttribute('aria-live','polite'); toast.hidden = true;
    document.body.append(toast);
    let toastTimer;
    document.querySelectorAll('.contact-item a[href^="mailto:"]').forEach(link => {
      const button = document.createElement('button'); button.type = 'button'; button.className = 'cv-copy-email';
      button.setAttribute('aria-label',french ? 'Copier l’adresse courriel' : 'Copy email address');
      link.closest('.contact-item').classList.add('cv-email-contact');
      const icon = copied => {
        const svg = document.createElementNS('http://www.w3.org/2000/svg','svg');
        svg.setAttribute('viewBox','0 0 20 20');svg.setAttribute('width','18');svg.setAttribute('height','18');svg.setAttribute('fill','none');svg.setAttribute('stroke','currentColor');svg.setAttribute('stroke-width','1.6');svg.setAttribute('aria-hidden','true');
        const path = document.createElementNS('http://www.w3.org/2000/svg','path');
        path.setAttribute('d',copied ? 'M3 10l4 4L17 4' : 'M6 6h11v12H6zM3 14H2V2h11v1');
        svg.append(path);button.replaceChildren(svg);button.dataset.copied=String(copied);
        button.title=copied?(french?'Copié':'Copied'):(french?'Copier l’adresse':'Copy email');
      };
      icon(false);
      link.after(button);
      let resetTimer;
      button.addEventListener('click',async () => {
        clearTimeout(toastTimer); clearTimeout(resetTimer);
        try {
          await navigator.clipboard.writeText(decodeURIComponent(link.getAttribute('href').slice(7).split('?')[0]));
          icon(true);
          toast.textContent = french ? 'Adresse courriel copiée' : 'Email address copied';
          animate(button,{scale:[.96,1]},{duration:.18},()=>resetVisual(button));
          resetTimer = setTimeout(()=>icon(false),1600);
        } catch (_) { toast.textContent = french ? 'Copie indisponible. Sélectionnez l’adresse pour la copier.' : 'Copy unavailable. Select the email address to copy it.'; }
        toast.hidden = false;
        toastTimer = setTimeout(()=>{toast.hidden=true;},3500);
      });
    });

    // Build previews from the authored card, retaining its real images and links.
    const preview = document.createElement('dialog'); preview.id = 'cv-project-preview';
    preview.setAttribute('aria-labelledby','cv-project-preview-title');
    const header = document.createElement('header');
    const title = document.createElement('h2'); title.id = 'cv-project-preview-title';
    const close = document.createElement('button'); close.type='button'; close.className='cv-project-preview-close'; close.textContent='×'; close.setAttribute('aria-label',french?'Fermer':'Close');
    header.append(title,close);
    const body = document.createElement('div'); body.className='cv-project-preview-body';
    preview.append(header,body); document.body.append(preview);
    let previewOpener;
    function dismiss() { preview.close(); }
    close.addEventListener('click',dismiss);
    preview.addEventListener('click',event=>{const box=preview.getBoundingClientRect();if(event.target===preview&&(event.clientX<box.left||event.clientX>box.right||event.clientY<box.top||event.clientY>box.bottom)) dismiss();});
    preview.addEventListener('close',()=>{stop(preview);resetVisual(preview);body.replaceChildren();previewOpener?.focus({preventScroll:true});});
    document.querySelectorAll('.project-card').forEach(card=>{
      const original = card.querySelector('.project-title a');
      if (!original) return;
      const button=document.createElement('button');button.type='button';button.className='cv-project-preview-trigger';
      button.textContent=french?'Aperçu du projet':'Project preview';button.setAttribute('aria-haspopup','dialog');button.setAttribute('aria-label',`${button.textContent}: ${original.textContent.trim()}`);
      let actions=card.querySelector('.project-actions');
      if(!actions) {
        actions=document.createElement('div');actions.className='cv-card-actions';
        card.querySelectorAll('.project-story-link').forEach(link=>{const parent=link.parentElement;actions.append(link);if(parent.tagName==='P'&&!parent.textContent.trim()&&!parent.children.length)parent.remove();});
        (card.querySelector('.project-card-copy')||card).append(actions);
      }
      actions.append(button);
      button.addEventListener('click',()=>{
        previewOpener=button;title.textContent=original.textContent.trim();body.replaceChildren();
        const image=card.querySelector('figure img');
        const svg=card.querySelector('figure svg');
        if(image) {const clone=image.cloneNode();clone.loading='eager';clone.removeAttribute('id');body.append(clone);}
        else if(svg) {const clone=svg.cloneNode(true);clone.setAttribute('xmlns','http://www.w3.org/2000/svg');const img=document.createElement('img');img.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(new XMLSerializer().serializeToString(clone));img.alt=card.querySelector('figcaption')?.textContent.trim() || title.textContent;body.append(img);}
        card.querySelectorAll('.project-context,.project-impact,.project-tags').forEach(node=>{const clone=node.cloneNode(true);clone.querySelectorAll('[id]').forEach(child=>child.removeAttribute('id'));clone.removeAttribute('id');body.append(clone);});
        const links=document.createElement('div');links.className='cv-project-preview-links';
        const source=original.cloneNode(true);source.textContent=french?'Code source ↗':'View source ↗';source.target='_blank';source.rel='noopener noreferrer';links.append(source);
        const seen=new Set([original.href]);card.querySelectorAll('.project-actions a,.project-story-link').forEach(link=>{if(!seen.has(link.href)){seen.add(link.href);links.append(link.cloneNode(true));}});
        body.append(links);preview.showModal();close.focus();
        const from=card.getBoundingClientRect(),to=preview.getBoundingClientRect();
        animate(preview,{opacity:[.95,1],scale:[.9,1],x:[Math.max(-80,Math.min(80,from.left+from.width/2-to.left-to.width/2)),0],y:[Math.max(-60,Math.min(60,from.top+from.height/2-to.top-to.height/2)),0]},{duration:.24},()=>resetVisual(preview));
      });
    });

    const navLinks=[...document.querySelectorAll('.cv-nav-section')];
    let navFrame=0, current;
    function trackSection() {
      navFrame=0;
      const top=document.querySelector('.cv-site-nav')?.getBoundingClientRect().bottom || 0;
      const selected=navLinks.filter(link=>{const section=document.getElementById(link.hash.slice(1));return section&&section.getBoundingClientRect().top<=top+90;}).at(-1);
      if(current===selected) return;
      current=selected;
      navLinks.forEach(link=>{if(link===selected)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current');});
    }
    const scheduleNav=()=>{if(!navFrame)navFrame=requestAnimationFrame(trackSection);};
    addEventListener('scroll',scheduleNav,{passive:true});addEventListener('resize',scheduleNav);trackSection();

    document.querySelectorAll('.cv-live-widgets-panel img').forEach(img=>{
      // Keep the existing parent and next sibling intact for the widget's error fallback.
      const holder=img.parentElement;
      holder.classList.add('cv-widget-media');
      function settle(success,fade=true) {
        holder.dataset.widgetState=success?'ready':'error';holder.removeAttribute('aria-busy');
        if(success&&fade&&img.getClientRects().length)animate(img,{opacity:[.65,1]},{duration:.2},()=>resetVisual(img));
      }
      holder.dataset.widgetState='loading';holder.setAttribute('aria-busy','true');
      img.addEventListener('load',()=>settle(true));img.addEventListener('error',()=>settle(false));
      if(img.complete&&img.naturalWidth)settle(true,false);
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',initialize,{once:true});else initialize();
})();
