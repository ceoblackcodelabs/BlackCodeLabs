/**
 * carousel.js — database-driven hero carousel.
 * Reads HELTZ_DATA.heroSlides; each slide's `type` ("image" | "video")
 * decides whether an <img> or a <video> is rendered — nothing is
 * hardcoded to image-only.
 */
(function () {
  "use strict";

  const root = document.querySelector("[data-hero]");
  if (!root) return;

  const slides = window.HELTZ_DATA?.heroSlides || [];
  if (!slides.length) return;

  const track = root.querySelector(".hero-track");
  const dotsWrap = root.querySelector(".hero-dots");
  const prevBtn = root.querySelector(".hero-arrow.prev");
  const nextBtn = root.querySelector(".hero-arrow.next");
  const AUTOPLAY_MS = 6500;

  let current = 0;
  let timer = null;

  function mediaEl(slide) {
    if (slide.type === "video") {
      return `<video src="${slide.media}" autoplay muted loop playsinline preload="none" aria-hidden="true"></video>`;
    }
    return `<img src="${slide.media}" alt="${slide.title || "Heltz Driving Academy"}" loading="${slides.indexOf(slide) === 0 ? "eager" : "lazy"}" fetchpriority="${slides.indexOf(slide) === 0 ? "high" : "auto"}">`;
  }

  track.innerHTML = slides
    .map(
      (slide, i) => `
    <div class="hero-slide${i === 0 ? " active" : ""}" data-index="${i}" data-media-type="${slide.type}">
      ${mediaEl(slide)}
      <div class="hero-content">
        <div class="container">
          <div class="hero-copy">
            ${slide.tag ? `<span class="plate">${slide.tag}</span>` : ""}
            <h1 style="margin-top:1rem;">${slide.title}</h1>
            <p>${slide.description || ""}</p>
            <div class="hero-cta-row">
              ${slide.ctaText ? `<a class="btn btn-amber" href="${slide.ctaUrl || "#"}">${slide.ctaText}</a>` : ""}
              <a class="btn btn-outline" style="color:#fff;" href="${window.HELTZ_DATA.business.whatsappHref}" target="_blank" rel="noopener">Chat On WhatsApp</a>
            </div>
          </div>
        </div>
      </div>
    </div>`
    )
    .join("");

  if (dotsWrap) {
    dotsWrap.innerHTML = slides
      .map((_, i) => `<button class="hero-dot${i === 0 ? " active" : ""}" data-goto="${i}" aria-label="Go to slide ${i + 1}"></button>`)
      .join("");
  }

  const slideEls = () => track.querySelectorAll(".hero-slide");
  const dotEls = () => dotsWrap ? dotsWrap.querySelectorAll(".hero-dot") : [];

  function playVisibleVideo() {
    slideEls().forEach((el) => {
      const v = el.querySelector("video");
      if (!v) return;
      if (el.classList.contains("active")) {
        v.play().catch(() => {});
      } else {
        v.pause();
      }
    });
  }

  function goTo(index) {
    const els = slideEls();
    const dots = dotEls();
    current = (index + slides.length) % slides.length;
    els.forEach((el, i) => el.classList.toggle("active", i === current));
    dots.forEach((d, i) => d.classList.toggle("active", i === current));
    playVisibleVideo();
    resetAutoplay();
  }

  function next() {
    goTo(current + 1);
  }
  function prev() {
    goTo(current - 1);
  }

  function resetAutoplay() {
    clearInterval(timer);
    timer = setInterval(next, AUTOPLAY_MS);
  }

  prevBtn?.addEventListener("click", prev);
  nextBtn?.addEventListener("click", next);
  dotsWrap?.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-goto]");
    if (btn) goTo(Number(btn.dataset.goto));
  });

  /* Pause autoplay when tab hidden or hero out of viewport */
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) clearInterval(timer);
    else resetAutoplay();
  });

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) resetAutoplay();
          else clearInterval(timer);
        });
      },
      { threshold: 0.2 }
    );
    io.observe(root);
  } else {
    resetAutoplay();
  }

  /* Touch / swipe */
  let touchStartX = 0;
  track.addEventListener(
    "touchstart",
    (e) => {
      touchStartX = e.touches[0].clientX;
    },
    { passive: true }
  );
  track.addEventListener(
    "touchend",
    (e) => {
      const dx = e.changedTouches[0].clientX - touchStartX;
      if (Math.abs(dx) > 40) (dx < 0 ? next() : prev());
    },
    { passive: true }
  );

  playVisibleVideo();
})();
