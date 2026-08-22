/**
 * counters.js — renders the stats strip from HELTZ_DATA.stats and
 * animates each number counting up once it scrolls into view.
 */
(function () {
  "use strict";

  const grid = document.querySelector("[data-stats]");
  if (!grid) return;

  const stats = window.HELTZ_DATA?.stats || [];
  if (!stats.length) return;

  grid.innerHTML = stats
    .map(
      (s) => `
    <div class="stat-card">
      <div class="stat-number"><span data-count="${s.value}">0</span>${s.suffix || ""}</div>
      <div class="stat-label">${s.label}</div>
    </div>`
    )
    .join("");

  const counters = grid.querySelectorAll("[data-count]");

  function animate(el) {
    const target = Number(el.dataset.count);
    const duration = 1400;
    const start = performance.now();

    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(eased * target);
      if (progress < 1) requestAnimationFrame(tick);
      else el.textContent = target;
    }
    requestAnimationFrame(tick);
  }

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animate(entry.target);
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.5 }
    );
    counters.forEach((c) => io.observe(c));
  } else {
    counters.forEach(animate);
  }
})();
