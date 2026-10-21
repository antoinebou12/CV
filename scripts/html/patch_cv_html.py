"""Apply accessibility and performance patches to index-en.html and index-fr.html."""

from __future__ import annotations

import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from _repo import REPO_ROOT as ROOT

CLUSTRMAPS_JS = r"""
    (function () {
      document.querySelectorAll('.clustrmaps-toggle').forEach(function (btn) {
        var panel = document.getElementById(btn.getAttribute('aria-controls'));
        var mount = panel && panel.querySelector('[data-clustrmaps-src]');
        if (!mount) return;
        var fr = document.documentElement.lang.indexOf('fr') === 0;
        var status = mount.querySelector('.clustrmaps-placeholder');
        var mapUrl = 'https://mapmyvisitors.com/map.png?d=SALlTdL7CuZX05Y8yrOrB64GOo5l9xEv4HbMaHu2Znc&cl=ffffff';
        var link = document.createElement('a');
        link.href = 'https://mapmyvisitors.com/web/1c8zo';
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.textContent = fr ? 'Carte et statistiques sur MapMyVisitors' : 'Map and statistics on MapMyVisitors';
        panel.appendChild(link);
        var timer;
        var image;
        function failed() {
          clearTimeout(timer);
          mount.dataset.state = 'error';
          mount.classList.remove('clustrmaps-mount--ready');
          if (image) image.hidden = true;
          if (status) {
            status.hidden = false;
            status.textContent = fr ? 'La carte est indisponible. Réessayez ou ouvrez le lien ci-dessous.' : 'The map is unavailable. Retry or open the link below.';
          }
          if (!mount.querySelector('.map-retry')) {
            var retry = document.createElement('button');
            retry.type = 'button';
            retry.className = 'map-retry';
            retry.textContent = fr ? 'Réessayer' : 'Retry';
            retry.addEventListener('click', loadMap);
            mount.appendChild(retry);
          }
        }
        function loadMap() {
          clearTimeout(timer);
          mount.dataset.state = 'loading';
          var retry = mount.querySelector('.map-retry');
          if (retry) retry.remove();
          if (image) { image.onload = null; image.onerror = null; image.remove(); }
          if (status) { status.hidden = false; status.textContent = fr ? 'Chargement de la carte…' : 'Loading map…'; }
          image = new Image();
          image.alt = fr ? 'Répartition géographique des visiteurs, par MapMyVisitors' : 'Visitor locations provided by MapMyVisitors';
          image.width = 300;
          image.style.maxWidth = '100%';
          image.style.height = 'auto';
          image.referrerPolicy = 'no-referrer-when-downgrade';
          image.onload = function () {
            if (mount.dataset.state !== 'loading') return;
            clearTimeout(timer);
            mount.dataset.state = 'ready';
            mount.classList.add('clustrmaps-mount--ready');
            if (status) status.hidden = true;
          };
          image.onerror = failed;
          timer = setTimeout(failed, 10000);
          mount.appendChild(image);
          image.src = mapUrl;
        }
        btn.addEventListener('click', function () {
          var open = btn.getAttribute('aria-expanded') === 'true';
          btn.setAttribute('aria-expanded', String(!open));
          panel.hidden = open;
          if (!open && !mount.dataset.state) loadMap();
        });
      });
    })();
"""

PARTICLES_INIT = r"""
    (function () {
      function initParticles() {
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
        if (typeof particlesJS !== 'function') return;
        particlesJS('particles-js', {
        particles: {
          number: { value: 200, density: { enable: true, value_area: 2400 } },
          color: { value: "#ffffff" },
          shape: { type: "circle", stroke: { width: 1, color: "#000000" }, polygon: { nb_sides: 6 } },
          opacity: { value: 0.5, random: false, anim: { enable: false, speed: 1, opacity_min: 0.1, sync: false } },
          size: { value: 3, random: true, anim: { enable: false, speed: 40, size_min: 0.1, sync: false } },
          line_linked: { enable: true, distance: 150, color: "#ffffff", opacity: 0.4, width: 1 },
          move: { enable: true, speed: 6, direction: "none", random: false, straight: false, out_mode: "out", bounce: false, attract: { enable: false, rotateX: 600, rotateY: 1200 } }
        },
        interactivity: {
          detect_on: "canvas",
          events: { onhover: { enable: true, mode: "repulse" }, onclick: { enable: true, mode: "push" }, resize: true },
          modes: {
            grab: { distance: 140, line_linked: { opacity: 1 } },
            bubble: { distance: 400, size: 40, duration: 2, opacity: 8, speed: 3 },
            repulse: { distance: 200, duration: 0.4 },
            push: { particles_nb: 4 },
            remove: { particles_nb: 2 }
          }
        },
        retina_detect: true
      });
      }
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initParticles);
      } else {
        initParticles();
      }
    })();
"""


def wrap_section_summaries(html: str) -> str:
    def repl(match: re.Match[str]) -> str:
        inner = match.group(1).strip()
        if inner.startswith("<h2"):
            return match.group(0)
        return f'<summary class="cv-section-summary"><h2 class="cv-section-heading">{inner}</h2></summary>'

    return re.sub(
        r'<summary class="cv-section-summary">(.*?)</summary>',
        repl,
        html,
        flags=re.DOTALL,
    )


def patch_file(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    is_fr = "fr" in path.name

    html = html.replace(
        '  <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>\n',
        "",
        1,
    )

    if is_fr:
        if 'href="#main"' not in html:
            html = html.replace("<body>\n", '<body>\n  <a class="skip-link" href="#main">Aller au contenu principal</a>\n', 1)
        old = """          <h3 class="clustrmaps-section-title"><i class="fas fa-globe-americas ico"></i> Carte des visiteurs</h3>
          <div class="clustrmaps-embed">
            <script type="text/javascript" id="clustrmaps" src="https://cdn.clustrmaps.com/map_v2.js?cl=ffffff&amp;w=a&amp;t=tt&amp;d=5r6lAAh3W_opreqW2Zi-o-UhGvrv12PSDzwfKIyaVoA"></script>
          </div>"""
        new = """          <h2 class="clustrmaps-section-title"><i class="fas fa-globe-americas ico"></i> Carte des visiteurs</h2>
          <button type="button" class="btn btn-default btn-sm clustrmaps-toggle" id="clustrmaps-toggle-fr" aria-expanded="false" aria-controls="clustrmaps-panel-fr">
            Afficher la carte des visiteurs
          </button>
          <div id="clustrmaps-panel-fr" class="clustrmaps-embed clustrmaps-embed-collapsed" hidden>
            <div id="clustrmaps-mount-fr" data-clustrmaps-src="https://cdn.clustrmaps.com/map_v2.js?cl=ffffff&amp;w=a&amp;t=tt&amp;d=5r6lAAh3W_opreqW2Zi-o-UhGvrv12PSDzwfKIyaVoA"></div>
          </div>"""
    else:
        if 'href="#main"' not in html:
            html = html.replace("<body>\n", '<body>\n  <a class="skip-link" href="#main">Skip to main content</a>\n', 1)
        old = """          <h3 class="clustrmaps-section-title"><i class="fas fa-globe-americas ico"></i> Visitor map</h3>
          <div class="clustrmaps-embed">
            <script type="text/javascript" id="clustrmaps" src="https://cdn.clustrmaps.com/map_v2.js?cl=ffffff&amp;w=a&amp;t=tt&amp;d=5r6lAAh3W_opreqW2Zi-o-UhGvrv12PSDzwfKIyaVoA"></script>
          </div>"""
        new = """          <h2 class="clustrmaps-section-title"><i class="fas fa-globe-americas ico"></i> Visitor map</h2>
          <button type="button" class="btn btn-default btn-sm clustrmaps-toggle" id="clustrmaps-toggle-en" aria-expanded="false" aria-controls="clustrmaps-panel-en">
            Show visitor map
          </button>
          <div id="clustrmaps-panel-en" class="clustrmaps-embed clustrmaps-embed-collapsed" hidden>
            <div id="clustrmaps-mount-en" data-clustrmaps-src="https://cdn.clustrmaps.com/map_v2.js?cl=ffffff&amp;w=a&amp;t=tt&amp;d=5r6lAAh3W_opreqW2Zi-o-UhGvrv12PSDzwfKIyaVoA"></div>
          </div>"""
    html = html.replace(old, new)

    html = html.replace(
        '<img src="antoine.png" alt="Antoine Boucher">',
        '<img src="antoine-320.jpg" srcset="antoine-320.jpg 320w, antoine.jpeg 800w" sizes="160px" alt="Antoine Boucher" width="160" height="160" fetchpriority="high" decoding="async">',
    )
    if '<main id="main"' not in html:
        html = html.replace('<div class="container">', '<main id="main" class="container">', 1)
        html = html.replace("</body>", "  </main>\n</body>", 1)

    html = wrap_section_summaries(html)
    html = html.replace(' role="img" aria-hidden="true" aria-labelledby="uml-mcp-flow-caption"', ' role="img" aria-labelledby="uml-mcp-flow-caption"')

    html = re.sub(
        r"</body>\s*<script>\s*\n\s*particlesJS\('particles-js'.*?</script>\s*</html>",
        "</body>\n</html>",
        html,
        flags=re.DOTALL,
        count=1,
    )
    if PARTICLES_INIT.strip() not in html:
        inject = (
            '  <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js" defer></script>\n'
            f"  <script>{PARTICLES_INIT}</script>\n"
            f"  <script>{CLUSTRMAPS_JS}</script>\n"
        )
        html = html.replace("</body>\n</html>", inject + "</body>\n</html>", 1)

    path.write_text(html, encoding="utf-8", newline="\n")
    print(f"Patched {path.name}")


def main() -> int:
    for name in ("index-en.html", "index-fr.html"):
        path = ROOT / name
        if not path.is_file():
            print(f"Missing {path}")
            return 1
        patch_file(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
