/**
 * fleet.js — right-to-left infinite auto-scrolling vehicle showcase.
 * Duplicates the track once so the CSS keyframe (-50%) loops seamlessly.
 */
(function () {
  "use strict";

  const viewport = document.querySelector("[data-fleet]");
  if (!viewport) return;

  const fleet = window.HELTZ_DATA?.fleet || [];
  if (!fleet.length) return;

  const track = viewport.querySelector(".fleet-track");

  function card(v) {
    return `
    <div class="fleet-card">
      <div class="fleet-media"><img src="${v.image}" alt="${v.name}" loading="lazy"></div>
      <div class="fleet-body">
        <h3>${v.name}</h3>
        <p class="mono" style="font-size:.78rem;color:var(--c-steel);text-transform:uppercase;">${v.category}</p>
        <div class="fleet-tags">
          <span>${v.transmission}</span>
        </div>
      </div>
    </div>`;
  }

  const cardsHtml = fleet.map(card).join("");
  // Duplicate so translateX(-50%) creates a seamless infinite loop
  track.innerHTML = cardsHtml + cardsHtml;

  /* Pause on manual scroll/touch, resume after a pause */
  let resumeTimer = null;
  function pause() {
    track.classList.add("paused");
    clearTimeout(resumeTimer);
  }
  function scheduleResume() {
    clearTimeout(resumeTimer);
    resumeTimer = setTimeout(() => track.classList.remove("paused"), 2200);
  }

  viewport.addEventListener("touchstart", pause, { passive: true });
  viewport.addEventListener("touchend", scheduleResume, { passive: true });
  viewport.addEventListener("wheel", () => {
    pause();
    scheduleResume();
  }, { passive: true });
})();
