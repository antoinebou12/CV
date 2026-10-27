(() => {
  const host = document.getElementById('project-particles');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (!host || reduceMotion.matches) return;

  const canvas = document.createElement('canvas');
  const context = canvas.getContext('2d', { alpha: true });
  if (!context) return;

  canvas.setAttribute('aria-hidden', 'true');
  host.appendChild(canvas);

  let width = 0;
  let height = 0;
  let frame = 0;
  let particles = [];

  const palette = () => document.documentElement.classList.contains('dark')
    ? { dot: '111, 219, 208', line: '172, 213, 255' }
    : { dot: '255, 255, 255', line: '224, 242, 237' };

  const makeParticle = () => ({
    x: Math.random() * width,
    y: Math.random() * height,
    radius: 0.8 + Math.random() * 1.5,
    vx: (Math.random() - 0.5) * 0.24,
    vy: (Math.random() - 0.5) * 0.24
  });

  const resize = () => {
    width = window.innerWidth;
    height = window.innerHeight;
    const ratio = Math.min(window.devicePixelRatio || 1, 1.5);
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    const count = Math.max(18, Math.min(54, Math.round((width * height) / 26000)));
    particles = Array.from({ length: count }, makeParticle);
  };

  const draw = () => {
    context.clearRect(0, 0, width, height);
    const colors = palette();

    for (const particle of particles) {
      particle.x += particle.vx;
      particle.y += particle.vy;
      if (particle.x < -8) particle.x = width + 8;
      if (particle.x > width + 8) particle.x = -8;
      if (particle.y < -8) particle.y = height + 8;
      if (particle.y > height + 8) particle.y = -8;
      context.beginPath();
      context.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
      context.fillStyle = `rgba(${colors.dot}, 0.34)`;
      context.fill();
    }

    for (let first = 0; first < particles.length; first += 1) {
      for (let second = first + 1; second < particles.length; second += 1) {
        const dx = particles[first].x - particles[second].x;
        const dy = particles[first].y - particles[second].y;
        const distance = Math.hypot(dx, dy);
        if (distance > 132) continue;
        context.beginPath();
        context.moveTo(particles[first].x, particles[first].y);
        context.lineTo(particles[second].x, particles[second].y);
        context.strokeStyle = `rgba(${colors.line}, ${(1 - distance / 132) * 0.16})`;
        context.lineWidth = 0.7;
        context.stroke();
      }
    }
    frame = window.requestAnimationFrame(draw);
  };

  const stop = () => {
    if (frame) window.cancelAnimationFrame(frame);
    frame = 0;
  };

  const start = () => {
    if (!frame && !document.hidden && !reduceMotion.matches) draw();
  };

  window.addEventListener('resize', resize, { passive: true });
  document.addEventListener('visibilitychange', () => document.hidden ? stop() : start());
  reduceMotion.addEventListener('change', event => {
    if (event.matches) {
      stop();
      host.replaceChildren();
    }
  }, { once: true });

  resize();
  start();
})();
