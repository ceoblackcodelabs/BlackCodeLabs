/* ============================================
   BOLLINGTON TRAINING INSTITUTE — SCRIPTS
============================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ---------- Footer year ---------- */
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---------- Sticky header on scroll + back to top ---------- */
  const header = document.getElementById('site-header');
  const backToTop = document.getElementById('backToTop');

  const onScroll = () => {
    if (window.scrollY > 40) header.classList.add('scrolled');
    else header.classList.remove('scrolled');

    // Back to top button
    if (window.scrollY > 600) backToTop.classList.add('show');
    else backToTop.classList.remove('show');
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile nav toggle ---------- */
  const navToggle = document.getElementById('navToggle');
  const mainNav = document.getElementById('main-nav');

  navToggle.addEventListener('click', () => {
    const isOpen = mainNav.classList.toggle('open');
    navToggle.classList.toggle('active');
    navToggle.setAttribute('aria-expanded', isOpen);
  });

  // Mobile dropdown toggle
  document.querySelectorAll('.has-dropdown > a').forEach(link => {
    link.addEventListener('click', (e) => {
      if (window.innerWidth <= 920) {
        e.preventDefault();
        link.parentElement.classList.toggle('open');
      }
    });
  });

  // Close mobile menu when a link is clicked
  document.querySelectorAll('.main-nav a:not(.has-dropdown > a)').forEach(link => {
    link.addEventListener('click', () => {
      mainNav.classList.remove('open');
      navToggle.classList.remove('active');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });

  /* ---------- Scroll reveal animations (progressive enhancement) ---------- */
  const revealEls = document.querySelectorAll('[data-aos]');
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

  revealEls.forEach(el => {
    el.classList.add('js-aos');
    revealObserver.observe(el);
  });

  /* ---------- Animated stat counters ---------- */
  const statEls = document.querySelectorAll('.stat-big');
  const animateCount = (el) => {
    const target = parseInt(el.dataset.count, 10);
    const suffix = el.dataset.suffix || '';
    const duration = 1400;
    const start = performance.now();

    const step = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      const value = Math.floor(eased * target);
      el.textContent = value.toLocaleString() + suffix;
      if (progress < 1) requestAnimationFrame(step);
      else el.textContent = target.toLocaleString() + suffix;
    };
    requestAnimationFrame(step);
  };

  const statObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCount(entry.target);
        statObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.4 });
  statEls.forEach(el => statObserver.observe(el));

  /* ---------- Course filtering (tabs + dropdown links) ---------- */
  const courseGrid = document.getElementById('courseGrid');
  const courseCards = courseGrid ? Array.from(courseGrid.querySelectorAll('.course-card')) : [];
  const tabs = document.querySelectorAll('.tab');
  const searchInput = document.getElementById('courseSearch');
  const noResults = document.getElementById('noResults');
  let activeFilter = 'all';

  const applyFilters = () => {
    const query = (searchInput.value || '').trim().toLowerCase();
    let visibleCount = 0;

    courseCards.forEach(card => {
      const matchesCategory = activeFilter === 'all' || card.dataset.cat === activeFilter;
      const title = card.querySelector('h3').textContent.toLowerCase();
      const desc = card.querySelector('p').textContent.toLowerCase();
      const matchesSearch = !query || title.includes(query) || desc.includes(query);

      const visible = matchesCategory && matchesSearch;
      card.classList.toggle('hidden', !visible);
      if (visible) visibleCount++;
    });

    noResults.hidden = visibleCount !== 0;
  };

  const setActiveTab = (filter) => {
    activeFilter = filter;
    tabs.forEach(tab => {
      const isActive = tab.dataset.filter === filter;
      tab.classList.toggle('active', isActive);
      tab.setAttribute('aria-selected', isActive);
    });
    applyFilters();
  };

  tabs.forEach(tab => {
    tab.addEventListener('click', () => setActiveTab(tab.dataset.filter));
  });

  if (searchInput) {
    searchInput.addEventListener('input', applyFilters);
  }

  // Links elsewhere (nav dropdown, footer) that pre-filter the course grid
  document.querySelectorAll('a[data-filter]').forEach(link => {
    link.addEventListener('click', (e) => {
      const filter = link.dataset.filter;
      if (!filter) return;
      // allow normal anchor jump, then apply filter
      setTimeout(() => setActiveTab(filter), 300);
    });
  });

  /* ---------- Application form submission ---------- */
  const appForm = document.getElementById('applicationFormEl');
  const appFormNote = document.getElementById('appFormNote');

  if (appForm) {
    appForm.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!appForm.checkValidity()) {
        appFormNote.textContent = 'Please fill in all required fields.';
        appFormNote.classList.remove('success');
        return;
      }
      const name = document.getElementById('appName').value.trim();
      appFormNote.textContent = `Thank you, ${name}! Your application has been received. Our admissions team will contact you within 48 hours.`;
      appFormNote.classList.add('success');
      appForm.reset();
    });
  }

  /* ---------- Contact form submission ---------- */
  const contactForm = document.getElementById('contactFormEl');
  const contactFormNote = document.getElementById('contactFormNote');

  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!contactForm.checkValidity()) {
        contactFormNote.textContent = 'Please fill in all required fields.';
        contactFormNote.classList.remove('success');
        return;
      }
      contactFormNote.textContent = 'Thank you for reaching out! We will get back to you shortly.';
      contactFormNote.classList.add('success');
      contactForm.reset();
    });
  }

  /* ---------- Newsletter subscription ---------- */
  const newsletterForm = document.getElementById('newsletterForm');
  const newsletterNote = document.getElementById('newsletterNote');

  if (newsletterForm) {
    newsletterForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const emailInput = document.getElementById('newsletterEmail');
      if (!emailInput.checkValidity()) {
        newsletterNote.textContent = 'Please enter a valid email address.';
        return;
      }
      newsletterNote.textContent = `Thanks! ${emailInput.value} has been subscribed to Bollington updates.`;
      newsletterForm.reset();
    });
  }

  /* ---------- Back to top button click ---------- */
  backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

});