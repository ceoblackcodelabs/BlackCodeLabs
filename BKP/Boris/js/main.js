/* ============================================================
   LUXURY REAL ESTATE — KENYA | main.js
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

  /* ---------- PAGE LOADER ---------- */
  const loader = document.getElementById('page-loader');
  if (loader) {
    window.addEventListener('load', () => {
      setTimeout(() => loader.classList.add('hidden'), 400);
    });
    // fallback in case load already fired
    setTimeout(() => loader.classList.add('hidden'), 1800);
  }

  /* ---------- STICKY HEADER ---------- */
  const header = document.getElementById('header');
  function onScrollHeader() {
    if (!header) return;
    if (window.scrollY > 40) header.classList.add('scrolled');
    else header.classList.remove('scrolled');
  }
  window.addEventListener('scroll', onScrollHeader);
  onScrollHeader();

  /* ---------- MOBILE NAV ---------- */
  const hamburger = document.getElementById('hamburger');
  const mobileNav = document.getElementById('mobile-nav');
  const mobileNavClose = document.getElementById('mobile-nav-close');

  function openMobileNav() {
    hamburger.classList.add('open');
    mobileNav.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function closeMobileNav() {
    hamburger.classList.remove('open');
    mobileNav.classList.remove('open');
    document.body.style.overflow = '';
  }
  if (hamburger && mobileNav) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.contains('open') ? closeMobileNav() : openMobileNav();
    });
  }
  if (mobileNavClose) mobileNavClose.addEventListener('click', closeMobileNav);
  if (mobileNav) {
    mobileNav.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMobileNav));
  }

  /* ---------- SCROLL TO TOP ---------- */
  const scrollTopBtn = document.getElementById('scroll-top');
  if (scrollTopBtn) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 500) scrollTopBtn.classList.add('show');
      else scrollTopBtn.classList.remove('show');
    });
    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ---------- SMOOTH SCROLL FOR ANCHOR LINKS ---------- */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId.length > 1) {
        const target = document.querySelector(targetId);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    });
  });

  /* ---------- FADE UP ON SCROLL (Intersection Observer) ---------- */
  const fadeEls = document.querySelectorAll('.fade-up');
  if (fadeEls.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    fadeEls.forEach(el => observer.observe(el));
  }

  /* ---------- HERO SLIDER ---------- */
  const heroSlides = document.querySelectorAll('.hero-slide');
  const heroDots = document.querySelectorAll('.hero-dot');
  let heroIndex = 0;
  let heroInterval;

  function showHeroSlide(i) {
    heroSlides.forEach(s => s.classList.remove('active'));
    heroDots.forEach(d => d.classList.remove('active'));
    if (heroSlides[i]) heroSlides[i].classList.add('active');
    if (heroDots[i]) heroDots[i].classList.add('active');
    heroIndex = i;
  }
  function nextHeroSlide() {
    showHeroSlide((heroIndex + 1) % heroSlides.length);
  }
  if (heroSlides.length) {
    showHeroSlide(0);
    heroInterval = setInterval(nextHeroSlide, 5500);
    heroDots.forEach((dot, i) => {
      dot.addEventListener('click', () => {
        showHeroSlide(i);
        clearInterval(heroInterval);
        heroInterval = setInterval(nextHeroSlide, 5500);
      });
    });
  }

  /* ---------- ANIMATED COUNTERS ---------- */
  const counters = document.querySelectorAll('.stat-number[data-target]');
  if (counters.length) {
    const counterObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          counterObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    counters.forEach(c => counterObserver.observe(c));
  }
  function animateCounter(el) {
    const target = parseInt(el.getAttribute('data-target'), 10);
    const suffix = el.getAttribute('data-suffix') || '';
    const duration = 1600;
    const start = performance.now();
    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const value = Math.floor(eased * target);
      el.textContent = value.toLocaleString() + suffix;
      if (progress < 1) requestAnimationFrame(tick);
      else el.textContent = target.toLocaleString() + suffix;
    }
    requestAnimationFrame(tick);
  }

  /* ---------- TESTIMONIALS CAROUSEL ---------- */
  const testimonialInner = document.querySelector('.testimonial-inner');
  const testimonialSlides = document.querySelectorAll('.testimonial-slide');
  const tDots = document.querySelectorAll('.t-dot');
  const tPrev = document.querySelector('.testimonial-btn.prev');
  const tNext = document.querySelector('.testimonial-btn.next');
  let tIndex = 0;

  function showTestimonial(i) {
    if (!testimonialInner) return;
    tIndex = (i + testimonialSlides.length) % testimonialSlides.length;
    testimonialInner.style.transform = `translateX(-${tIndex * 100}%)`;
    tDots.forEach(d => d.classList.remove('active'));
    if (tDots[tIndex]) tDots[tIndex].classList.add('active');
  }
  if (testimonialInner && testimonialSlides.length) {
    showTestimonial(0);
    let tInterval = setInterval(() => showTestimonial(tIndex + 1), 6000);
    if (tPrev) tPrev.addEventListener('click', () => { showTestimonial(tIndex - 1); clearInterval(tInterval); tInterval = setInterval(() => showTestimonial(tIndex + 1), 6000); });
    if (tNext) tNext.addEventListener('click', () => { showTestimonial(tIndex + 1); clearInterval(tInterval); tInterval = setInterval(() => showTestimonial(tIndex + 1), 6000); });
    tDots.forEach((dot, i) => dot.addEventListener('click', () => { showTestimonial(i); clearInterval(tInterval); tInterval = setInterval(() => showTestimonial(tIndex + 1), 6000); }));
  }

  /* ---------- PROPERTY GALLERY SLIDER (Detail Page) ---------- */
  const galleryMainImg = document.querySelector('.gallery-main-placeholder');
  const galleryThumbs = document.querySelectorAll('.gallery-thumb');
  if (galleryThumbs.length && galleryMainImg) {
    galleryThumbs.forEach((thumb) => {
      thumb.addEventListener('click', () => {
        galleryThumbs.forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');
        const bgClass = thumb.getAttribute('data-bg');
        galleryMainImg.className = 'gallery-main-placeholder ' + bgClass;
      });
    });
  }

  /* ---------- FAQ ACCORDION ---------- */
  document.querySelectorAll('.faq-q').forEach(q => {
    q.addEventListener('click', () => {
      const item = q.closest('.faq-item');
      const wasOpen = item.classList.contains('open');
      item.parentElement.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
      if (!wasOpen) item.classList.add('open');
    });
  });

  /* ---------- CARD FAVORITE TOGGLE ---------- */
  document.querySelectorAll('.card-fav').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      btn.classList.toggle('active');
      btn.textContent = btn.classList.contains('active') ? '♥' : '♡';
    });
  });

  /* ---------- NEWSLETTER FORM VALIDATION ---------- */
  document.querySelectorAll('.newsletter-form').forEach(form => {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const input = form.querySelector('input[type="email"]');
      const msg = form.parentElement.querySelector('.form-msg');
      if (input && validateEmail(input.value)) {
        showFormMessage(msg, 'Thanks for subscribing! Check your inbox to confirm.', true);
        input.value = '';
      } else {
        showFormMessage(msg, 'Please enter a valid email address.', false);
      }
    });
  });

  function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
  function showFormMessage(el, text, success) {
    if (!el) return;
    el.textContent = text;
    el.style.display = 'block';
    el.style.color = success ? '#4ade80' : '#f87171';
    el.style.fontSize = '0.82rem';
    el.style.marginTop = '10px';
    setTimeout(() => { el.style.display = 'none'; }, 4000);
  }

  /* ---------- GENERIC CONTACT / VIEWING / APPLICATION FORM VALIDATION ---------- */
  document.querySelectorAll('form[data-validate]').forEach(form => {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      let valid = true;
      form.querySelectorAll('[required]').forEach(field => {
        const errorEl = field.parentElement.querySelector('.field-error');
        if (!field.value.trim()) {
          valid = false;
          field.style.borderColor = '#f87171';
          if (errorEl) errorEl.style.display = 'block';
        } else if (field.type === 'email' && !validateEmail(field.value)) {
          valid = false;
          field.style.borderColor = '#f87171';
          if (errorEl) errorEl.style.display = 'block';
        } else {
          field.style.borderColor = '';
          if (errorEl) errorEl.style.display = 'none';
        }
      });
      const successMsg = form.querySelector('.form-success');
      if (valid) {
        if (successMsg) {
          successMsg.style.display = 'block';
          setTimeout(() => { successMsg.style.display = 'none'; }, 5000);
        }
        form.reset();
      }
    });
  });

  /* ---------- MORTGAGE CALCULATOR ---------- */
  const mortgageForm = document.getElementById('mortgage-calc-form');
  if (mortgageForm) {
    mortgageForm.addEventListener('submit', function (e) {
      e.preventDefault();
      calculateMortgage();
    });
    mortgageForm.addEventListener('input', calculateMortgage);
    calculateMortgage();
  }
  function calculateMortgage() {
    const price = parseFloat(document.getElementById('mc-price')?.value) || 0;
    const downPct = parseFloat(document.getElementById('mc-down')?.value) || 0;
    const rate = parseFloat(document.getElementById('mc-rate')?.value) || 0;
    const years = parseFloat(document.getElementById('mc-years')?.value) || 1;

    const downAmount = price * (downPct / 100);
    const principal = price - downAmount;
    const monthlyRate = (rate / 100) / 12;
    const n = years * 12;

    let monthly = 0;
    if (monthlyRate > 0 && n > 0) {
      monthly = principal * (monthlyRate * Math.pow(1 + monthlyRate, n)) / (Math.pow(1 + monthlyRate, n) - 1);
    } else if (n > 0) {
      monthly = principal / n;
    }
    const totalPay = monthly * n;
    const totalInterest = totalPay - principal;

    setText('mc-monthly', formatKES(monthly));
    setText('mc-total-interest', formatKES(totalInterest));
    setText('mc-total-pay', formatKES(totalPay + downAmount));
  }
  function setText(id, val) {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
  }
  function formatKES(num) {
    if (isNaN(num) || !isFinite(num)) num = 0;
    return 'KES ' + Math.round(num).toLocaleString();
  }

  /* ---------- ROI CALCULATOR (Investments page) ---------- */
  const roiForm = document.getElementById('roi-calc-form');
  if (roiForm) {
    roiForm.addEventListener('submit', (e) => { e.preventDefault(); calculateROI(); });
    roiForm.addEventListener('input', calculateROI);
    calculateROI();
  }
  function calculateROI() {
    const investment = parseFloat(document.getElementById('roi-investment')?.value) || 0;
    const monthlyIncome = parseFloat(document.getElementById('roi-income')?.value) || 0;
    const expenses = parseFloat(document.getElementById('roi-expenses')?.value) || 0;
    const appreciation = parseFloat(document.getElementById('roi-appreciation')?.value) || 0;

    const annualIncome = (monthlyIncome - expenses) * 12;
    const cashOnCashROI = investment > 0 ? (annualIncome / investment) * 100 : 0;
    const appreciationValue = investment * (appreciation / 100);
    const totalAnnualReturn = annualIncome + appreciationValue;
    const totalROI = investment > 0 ? (totalAnnualReturn / investment) * 100 : 0;

    setText('roi-annual-income', formatKES(annualIncome));
    setText('roi-cashflow-pct', cashOnCashROI.toFixed(2) + '%');
    setText('roi-total-return', formatKES(totalAnnualReturn));
    setText('roi-total-pct', totalROI.toFixed(2) + '%');
  }

  /* ---------- PROPERTY FILTERING (Properties page) ---------- */
  const filterForm = document.getElementById('property-filters');
  const propertyCards = document.querySelectorAll('.props-grid .property-card');
  const propsCountEl = document.getElementById('props-count-num');

  function applyFilters() {
    if (!filterForm) return;
    const type = document.getElementById('filter-type')?.value || '';
    const location = document.getElementById('filter-location')?.value || '';
    const beds = document.getElementById('filter-beds')?.value || '';
    const maxPrice = parseFloat(document.getElementById('filter-max-price')?.value) || Infinity;
    const keyword = (document.getElementById('filter-search')?.value || '').toLowerCase();

    let visibleCount = 0;
    propertyCards.forEach(card => {
      const cardType = card.getAttribute('data-type') || '';
      const cardLocation = card.getAttribute('data-location') || '';
      const cardBeds = card.getAttribute('data-beds') || '';
      const cardPrice = parseFloat(card.getAttribute('data-price')) || 0;
      const cardTitle = (card.getAttribute('data-title') || '').toLowerCase();

      const matchType = !type || cardType === type;
      const matchLocation = !location || cardLocation === location;
      const matchBeds = !beds || cardBeds === beds || (beds === '4' && parseInt(cardBeds) >= 4);
      const matchPrice = cardPrice <= maxPrice;
      const matchKeyword = !keyword || cardTitle.includes(keyword) || cardLocation.toLowerCase().includes(keyword);

      const show = matchType && matchLocation && matchBeds && matchPrice && matchKeyword;
      card.style.display = show ? '' : 'none';
      if (show) visibleCount++;
    });
    if (propsCountEl) propsCountEl.textContent = visibleCount;
  }
  if (filterForm) {
    filterForm.querySelectorAll('select, input').forEach(field => {
      field.addEventListener('input', applyFilters);
      field.addEventListener('change', applyFilters);
    });
    document.getElementById('filter-reset')?.addEventListener('click', () => {
      filterForm.reset();
      applyFilters();
    });
  }

  /* ---------- SORT PROPERTIES ---------- */
  const sortSelect = document.getElementById('props-sort-select');
  const propsGrid = document.querySelector('.props-grid');
  if (sortSelect && propsGrid) {
    sortSelect.addEventListener('change', () => {
      const cards = Array.from(propsGrid.querySelectorAll('.property-card'));
      const val = sortSelect.value;
      cards.sort((a, b) => {
        const priceA = parseFloat(a.getAttribute('data-price')) || 0;
        const priceB = parseFloat(b.getAttribute('data-price')) || 0;
        if (val === 'price-asc') return priceA - priceB;
        if (val === 'price-desc') return priceB - priceA;
        return 0;
      });
      cards.forEach(card => propsGrid.appendChild(card));
    });
  }

  /* ---------- BLOG CATEGORY FILTER ---------- */
  const catBtns = document.querySelectorAll('.cat-btn');
  const blogCards = document.querySelectorAll('.blog-grid .blog-card');
  if (catBtns.length) {
    catBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        catBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const cat = btn.getAttribute('data-cat');
        blogCards.forEach(card => {
          const cardCat = card.getAttribute('data-cat');
          card.style.display = (cat === 'all' || cardCat === cat) ? '' : 'none';
        });
      });
    });
  }

  /* ---------- RENTAL TABS ---------- */
  const rentalTabs = document.querySelectorAll('.rental-tab');
  const rentalPanels = document.querySelectorAll('.rental-panel');
  if (rentalTabs.length) {
    rentalTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        rentalTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        const target = tab.getAttribute('data-tab');
        rentalPanels.forEach(panel => {
          panel.style.display = panel.getAttribute('data-panel') === target ? '' : 'none';
        });
      });
    });
  }

  /* ---------- LAZY LOAD IMAGES (real <img data-src>) ---------- */
  const lazyImages = document.querySelectorAll('img[data-src]');
  if (lazyImages.length) {
    const lazyObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.getAttribute('data-src');
          img.removeAttribute('data-src');
          lazyObserver.unobserve(img);
        }
      });
    });
    lazyImages.forEach(img => lazyObserver.observe(img));
  }

  /* ---------- SEARCH FORM (Index hero) -> redirect to properties.html with query ---------- */
  const heroSearchForm = document.getElementById('hero-search-form');
  if (heroSearchForm) {
    heroSearchForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const params = new URLSearchParams();
      ['hs-location', 'hs-type', 'hs-price', 'hs-beds'].forEach(id => {
        const el = document.getElementById(id);
        if (el && el.value) params.append(id, el.value);
      });
      window.location.href = 'properties.html?' + params.toString();
    });
  }

  /* ---------- ACTIVE NAV LINK BASED ON CURRENT PAGE ---------- */
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('nav a, .mobile-nav a').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPage) link.classList.add('active');
  });

});
