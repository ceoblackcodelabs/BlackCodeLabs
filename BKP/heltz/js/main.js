/**
 * main.js — orchestrates all data-driven rendering that isn't handled
 * by carousel.js / fleet.js / counters.js / gallery.js / forms.js.
 * Every render function first checks its container exists, so this
 * single file can be included on every page safely.
 */
(function () {
  "use strict";

  const D = window.HELTZ_DATA;
  const I = window.ICONS;
  if (!D) return;

  const money = (n) => "KES " + Number(n).toLocaleString("en-KE");

  /* ------------------------------------------------------------
     1. Site-wide dynamic fields (phone/email/social/hours/etc.)
     Populates any element carrying [data-field] with a value
     from the business object — single source of truth.
  ------------------------------------------------------------ */
  function populateFields() {
    const map = {
      phone: D.business.phonePrimary,
      "phone-href": D.business.phonePrimaryHref,
      whatsapp: D.business.whatsapp,
      "whatsapp-href": D.business.whatsappHref,
      email: D.business.email,
      "email-href": "mailto:" + D.business.email,
      address: D.business.address,
      pobox: D.business.poBox,
      "hours-weekday": D.business.hours[0]?.value,
      "hours-saturday": D.business.hours[1]?.value,
      facebook: D.business.social.facebook,
      twitter: D.business.social.twitter,
      instagram: D.business.social.instagram,
      tiktok: D.business.social.tiktok,
      brochure: D.business.brochureUrl,
      mapembed: D.business.mapsEmbed,
      year: new Date().getFullYear(),
    };

    document.querySelectorAll("[data-field]").forEach((el) => {
      const key = el.dataset.field;
      if (!(key in map) || map[key] == null) return;
      if (el.tagName === "A" && key.endsWith("-href")) {
        el.setAttribute("href", map[key]);
      } else if (el.tagName === "A" && (key === "facebook" || key === "twitter" || key === "instagram" || key === "tiktok" || key === "brochure")) {
        el.setAttribute("href", map[key]);
      } else if (el.tagName === "IFRAME") {
        el.setAttribute("src", map[key]);
      } else {
        el.textContent = map[key];
      }
    });
  }

  /* ------------------------------------------------------------
     2. Why Heltz feature grid
  ------------------------------------------------------------ */
  function renderWhy() {
    const grid = document.querySelector("[data-why]");
    if (!grid) return;
    grid.innerHTML = D.whyUs
      .map(
        (f) => `
      <div class="feature-card card" data-animate>
        <div class="feature-icon">${I[toCamel(f.icon)] || I.trophy}</div>
        <h3>${f.title}</h3>
        <p>${f.text}</p>
      </div>`
      )
      .join("");
  }

  function toCamel(str) {
    return str.replace(/-([a-z])/g, (_, c) => c.toUpperCase());
  }

  const ICON_ALIAS = {
    instructor: "instructorIcon",
    trophy: "trophy",
    wallet: "wallet",
    "steering-wheel": "steeringWheel",
    book: "book",
    refresh: "refresh",
    briefcase: "briefcase",
  };

  /* ------------------------------------------------------------
     3. Services grid
  ------------------------------------------------------------ */
  function renderServices() {
    const grid = document.querySelector("[data-services]");
    if (!grid) return;
    grid.innerHTML = D.services
      .map(
        (s) => `
      <div class="service-card card" data-animate>
        <div class="service-icon">${I[ICON_ALIAS[s.icon]] || I.book}</div>
        <h3>${s.title}</h3>
        <p>${s.text}</p>
        <a class="btn-ghost" href="courses.html">Learn more ${I.chevronRight}</a>
      </div>`
      )
      .join("");
  }

  /* ------------------------------------------------------------
     4/5. Courses — preview (Home) and full grid with filter (Courses page)
  ------------------------------------------------------------ */
  function courseCard(group) {
    const lowest = Math.min(...group.items.map((i) => i.price));
    return `
    <div class="course-card card" data-animate data-class="${group.classCode}">
      <div class="course-media">
        <img src="${group.image}" alt="${group.name} — ${group.category}" loading="lazy">
        <span class="plate">Class ${group.classCode}</span>
      </div>
      <div class="course-body">
        <h3>${group.name} — ${group.category}</h3>
        <div class="course-meta">
          <span>${group.transmission}</span>
          <span>${group.items.length} option${group.items.length > 1 ? "s" : ""}</span>
        </div>
        <p class="desc">${group.description}</p>
        <div class="course-foot">
          <div class="course-price">
            <small>From</small>
            ${money(lowest)}
          </div>
          <a class="btn btn-outline" href="register.html">Enroll</a>
        </div>
      </div>
    </div>`;
  }

  function renderCoursesPreview() {
    const grid = document.querySelector("[data-courses-preview]");
    if (!grid) return;
    grid.innerHTML = D.courseGroups
      .filter((g) => g.id !== "vip")
      .map(courseCard)
      .join("");
  }

  function renderCoursesFull() {
    const grid = document.querySelector("[data-courses-full]");
    if (!grid) return;
    grid.innerHTML = D.courseGroups.map(courseCard).join("");

    const filterRow = document.querySelector("[data-course-filter]");
    if (!filterRow) return;
    const classes = ["All", ...D.courseGroups.map((g) => g.classCode)];
    filterRow.innerHTML = classes
      .map((c) => `<button class="filter-chip${c === "All" ? " active" : ""}" data-class="${c}">${c === "All" ? "All Classes" : "Class " + c}</button>`)
      .join("");

    filterRow.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-class]");
      if (!btn) return;
      filterRow.querySelectorAll(".filter-chip").forEach((c) => c.classList.toggle("active", c === btn));
      const cls = btn.dataset.class;
      grid.querySelectorAll(".course-card").forEach((card) => {
        card.style.display = cls === "All" || card.dataset.class === cls ? "" : "none";
      });
    });
  }

  /* ------------------------------------------------------------
     6/7. Branches — preview + full
  ------------------------------------------------------------ */
  function branchCard(b) {
    const q = encodeURIComponent(b.name + " " + b.location + " Nairobi");
    return `
    <div class="branch-card card" data-animate>
      <div class="branch-head">
        <h3>${b.name}</h3>
        ${b.isHQ ? '<span class="branch-hq-tag">Head Office</span>' : ""}
      </div>
      <p>${I.pin}<span>${b.location}</span></p>
      <a class="btn-ghost" href="https://maps.google.com/maps?q=${q}" target="_blank" rel="noopener">Get Directions ${I.chevronRight}</a>
    </div>`;
  }

  function renderBranchesPreview() {
    const grid = document.querySelector("[data-branches-preview]");
    if (!grid) return;
    grid.innerHTML = D.branches.slice(0, 6).map(branchCard).join("");
  }

  function renderBranchesFull() {
    const grid = document.querySelector("[data-branches-full]");
    if (!grid) return;
    grid.innerHTML = D.branches.map(branchCard).join("");
  }

  /* ------------------------------------------------------------
     8. Testimonials — section hides itself when there is no data
  ------------------------------------------------------------ */
  function renderTestimonials() {
    const section = document.querySelector("[data-testimonials-section]");
    const track = document.querySelector("[data-testimonials]");
    if (!section || !track) return;

    if (!D.testimonials.length) {
      section.style.display = "none";
      return;
    }

    track.innerHTML = D.testimonials
      .map(
        (t) => `
      <div class="testimonial-card card">
        <div class="testimonial-stars">${Array(t.rating || 5).fill(I.star).join("")}</div>
        <p class="testimonial-quote">&ldquo;${t.quote}&rdquo;</p>
        <div class="testimonial-person">
          ${t.avatar ? `<img class="testimonial-avatar" src="${t.avatar}" alt="${t.name}">` : ""}
          <div>
            <div class="testimonial-name">${t.name}</div>
            <div class="testimonial-course">${t.course || ""}</div>
          </div>
        </div>
      </div>`
      )
      .join("");
  }

  /* ------------------------------------------------------------
     9. FAQ accordion (+ optional search on faq.html)
  ------------------------------------------------------------ */
  function renderFAQ() {
    const list = document.querySelector("[data-faq]");
    if (!list) return;

    function itemsHtml(items) {
      return items
        .map(
          (f, i) => `
        <div class="faq-item" data-q="${f.q.toLowerCase()}">
          <button class="faq-question" aria-expanded="false" id="faq-q-${i}">
            <span>${f.q}</span>${I.chevronDown}
          </button>
          <div class="faq-answer">
            <div class="faq-answer-inner"><p>${f.a}</p></div>
          </div>
        </div>`
        )
        .join("");
    }

    list.innerHTML = itemsHtml(D.faqs);

    function wireToggles() {
      list.querySelectorAll(".faq-question").forEach((btn) => {
        btn.addEventListener("click", () => {
          const item = btn.closest(".faq-item");
          const answer = item.querySelector(".faq-answer");
          const isOpen = item.classList.toggle("open");
          btn.setAttribute("aria-expanded", String(isOpen));
          answer.style.maxHeight = isOpen ? answer.scrollHeight + "px" : "0";
        });
      });
    }
    wireToggles();

    const search = document.querySelector("[data-faq-search]");
    search?.addEventListener("input", () => {
      const term = search.value.trim().toLowerCase();
      list.querySelectorAll(".faq-item").forEach((item) => {
        const match = item.dataset.q.includes(term) || item.textContent.toLowerCase().includes(term);
        item.style.display = match ? "" : "none";
      });
    });
  }

  /* ------------------------------------------------------------
     10. Student journey / How it works
  ------------------------------------------------------------ */
  function renderJourney() {
    const row = document.querySelector("[data-journey]");
    if (!row) return;
    row.innerHTML = D.journey
      .map(
        (j) => `
      <div class="step-item" data-animate>
        <div class="step-num"></div>
        <h3 style="font-size:1.1rem;margin-bottom:.5rem;">${j.title}</h3>
        <p style="color:var(--c-steel);font-size:.94rem;">${j.text}</p>
      </div>`
      )
      .join("");
  }

  /* ------------------------------------------------------------
     11. Price tables (Prices page / Help Center)
  ------------------------------------------------------------ */
  function renderPriceTables() {
    const wrap = document.querySelector("[data-price-tables]");
    if (!wrap) return;

    const classTables = D.courseGroups
      .map(
        (g) => `
      <div class="price-table-wrap">
        <table class="price-table">
          <caption>Class ${g.classCode} — ${g.category}</caption>
          <thead><tr><th>Details</th><th>Rate</th></tr></thead>
          <tbody>
            ${g.items.map((i) => `<tr><td>${i.details}</td><td class="amount">${money(i.price)}</td></tr>`).join("")}
          </tbody>
        </table>
      </div>`
      )
      .join("");

    const refresherTable = `
      <div class="price-table-wrap">
        <table class="price-table">
          <caption>Refresher Courses — Minimum 5 Lessons</caption>
          <thead><tr><th>Class</th><th>Rate</th></tr></thead>
          <tbody>
            ${D.refresherRates.map((r) => `<tr><td>Class ${r.classCode}</td><td class="amount">${money(r.rate)}/lesson</td></tr>`).join("")}
          </tbody>
        </table>
      </div>`;

    const ntsaTable = `
      <div class="price-table-wrap">
        <table class="price-table">
          <caption>Amounts Payable To NTSA (Not Included Above)</caption>
          <thead><tr><th>Item</th><th>Amount</th></tr></thead>
          <tbody>
            ${D.ntsaFees.map((f) => `<tr><td>${f.item}</td><td class="amount">${money(f.amount)}</td></tr>`).join("")}
          </tbody>
        </table>
      </div>`;

    wrap.innerHTML = classTables + refresherTable + ntsaTable;
  }

  /* ------------------------------------------------------------
     12. Scroll reveal for [data-animate]
  ------------------------------------------------------------ */
  function initScrollReveal() {
    const els = document.querySelectorAll("[data-animate]");
    if (!els.length) return;
    if (!("IntersectionObserver" in window)) {
      els.forEach((el) => el.classList.add("in-view"));
      return;
    }
    const io = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view");
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    els.forEach((el) => io.observe(el));
  }

  /* ------------------------------------------------------------
     Boot — run immediately if the DOM is already parsed (script
     is loaded at the end of body), otherwise wait for the event.
     Guards against any race between script load and DOMContentLoaded.
  ------------------------------------------------------------ */
  function boot() {
    populateFields();
    renderWhy();
    renderServices();
    renderCoursesPreview();
    renderCoursesFull();
    renderBranchesPreview();
    renderBranchesFull();
    renderTestimonials();
    renderFAQ();
    renderJourney();
    renderPriceTables();
    // Give dynamically inserted [data-animate] nodes a tick to exist
    setTimeout(initScrollReveal, 0);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
