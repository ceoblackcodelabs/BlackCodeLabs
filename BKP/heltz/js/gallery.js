/**
 * gallery.js — renders gallery grids from HELTZ_DATA.gallery.
 * data-gallery="preview" -> small fixed grid, no filter (used on Home)
 * data-gallery="full"    -> filterable + paginated grid (Gallery page)
 * Both share a lightbox with prev/next + keyboard support.
 */
(function () {
  "use strict";

  const allItems = window.HELTZ_DATA?.gallery || [];

  function layoutClass(i) {
    // simple varied-size masonry-ish pattern for visual interest
    const pattern = i % 8;
    if (pattern === 0) return "wide";
    if (pattern === 3) return "tall";
    return "";
  }

  function itemMarkup(item, globalIndex) {
    const isVideo = item.type === "video";
    return `
    <div class="gallery-item ${layoutClass(globalIndex)}" data-index="${globalIndex}" role="button" tabindex="0" aria-label="Open ${isVideo ? "video" : "photo"}: ${item.alt}">
      ${
        isVideo
          ? `<video src="${item.src}" muted loop preload="none" poster="${item.poster || ""}"></video>
             <div class="play-badge"><span>${window.ICONS.play}</span></div>`
          : `<img src="${item.src}" alt="${item.alt}" loading="lazy">`
      }
    </div>`;
  }

  function buildLightbox() {
    if (document.querySelector(".lightbox")) return;
    const lb = document.createElement("div");
    lb.className = "lightbox";
    lb.innerHTML = `
      <button class="lightbox-close" aria-label="Close">${window.ICONS.close}</button>
      <button class="lightbox-arrow prev" aria-label="Previous">${window.ICONS.arrowLeft}</button>
      <div class="lightbox-content"></div>
      <button class="lightbox-arrow next" aria-label="Next">${window.ICONS.arrowRight}</button>
    `;
    document.body.appendChild(lb);
  }

  function initGalleryBlock(container) {
    const mode = container.dataset.gallery;
    const filterWrap = document.querySelector("[data-gallery-filter]");
    const loadMoreBtn = document.querySelector("[data-gallery-more]");

    let activeCategory = "All";
    let visibleCount = mode === "preview" ? 8 : 12;
    const PAGE_SIZE = 12;

    function filteredItems() {
      if (activeCategory === "All") return allItems;
      return allItems.filter((i) => i.category === activeCategory);
    }

    function render() {
      const items = filteredItems().slice(0, visibleCount);
      container.innerHTML = items.map((item, i) => itemMarkup(item, allItems.indexOf(item))).join("");
      if (loadMoreBtn) {
        loadMoreBtn.style.display = visibleCount >= filteredItems().length ? "none" : "inline-flex";
      }
    }

    if (filterWrap && mode === "full") {
      const categories = ["All", ...new Set(allItems.map((i) => i.category))];
      filterWrap.innerHTML = categories
        .map((c) => `<button class="filter-chip${c === "All" ? " active" : ""}" data-cat="${c}">${c}</button>`)
        .join("");
      filterWrap.addEventListener("click", (e) => {
        const btn = e.target.closest("[data-cat]");
        if (!btn) return;
        activeCategory = btn.dataset.cat;
        visibleCount = PAGE_SIZE;
        filterWrap.querySelectorAll(".filter-chip").forEach((c) => c.classList.toggle("active", c === btn));
        render();
      });
    }

    loadMoreBtn?.addEventListener("click", () => {
      visibleCount += PAGE_SIZE;
      render();
    });

    render();

    /* Lightbox open handler (delegated) */
    container.addEventListener("click", (e) => {
      const item = e.target.closest(".gallery-item");
      if (item) openLightbox(Number(item.dataset.index));
    });
    container.addEventListener("keydown", (e) => {
      if (e.key !== "Enter" && e.key !== " ") return;
      const item = e.target.closest(".gallery-item");
      if (item) {
        e.preventDefault();
        openLightbox(Number(item.dataset.index));
      }
    });
  }

  let lightboxIndex = 0;
  function openLightbox(index) {
    buildLightbox();
    lightboxIndex = index;
    renderLightbox();
    document.querySelector(".lightbox").classList.add("open");
    document.body.style.overflow = "hidden";
  }

  function closeLightbox() {
    const lb = document.querySelector(".lightbox");
    if (!lb) return;
    lb.classList.remove("open");
    document.body.style.overflow = "";
    lb.querySelector("video")?.pause();
  }

  function renderLightbox() {
    const lb = document.querySelector(".lightbox");
    if (!lb) return;
    const item = allItems[lightboxIndex];
    const content = lb.querySelector(".lightbox-content");
    content.innerHTML =
      item.type === "video"
        ? `<video src="${item.src}" controls autoplay playsinline></video>`
        : `<img src="${item.src}" alt="${item.alt}">`;
  }

  document.addEventListener("click", (e) => {
    if (e.target.closest(".lightbox-close") || e.target.classList.contains("lightbox")) closeLightbox();
    if (e.target.closest(".lightbox-arrow.next")) {
      lightboxIndex = (lightboxIndex + 1) % allItems.length;
      renderLightbox();
    }
    if (e.target.closest(".lightbox-arrow.prev")) {
      lightboxIndex = (lightboxIndex - 1 + allItems.length) % allItems.length;
      renderLightbox();
    }
  });

  document.addEventListener("keydown", (e) => {
    const lb = document.querySelector(".lightbox.open");
    if (!lb) return;
    if (e.key === "Escape") closeLightbox();
    if (e.key === "ArrowRight") {
      lightboxIndex = (lightboxIndex + 1) % allItems.length;
      renderLightbox();
    }
    if (e.key === "ArrowLeft") {
      lightboxIndex = (lightboxIndex - 1 + allItems.length) % allItems.length;
      renderLightbox();
    }
  });

  document.querySelectorAll("[data-gallery]").forEach(initGalleryBlock);
})();
