/* ============================================
   QUARRY ROAD BAND — Shared Scripts
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ---------- Sticky Nav ---------- */
  const nav = document.querySelector('.nav');
  if (nav) {
    const onScroll = () => {
      if (window.scrollY > 40) nav.classList.add('is-scrolled');
      else nav.classList.remove('is-scrolled');
    };
    onScroll();
    window.addEventListener('scroll', onScroll);
  }

  /* ---------- Mobile Menu ---------- */
  const burger = document.querySelector('.nav__burger');
  const mobileMenu = document.querySelector('.mobile-menu');
  if (burger && mobileMenu) {
    burger.addEventListener('click', () => mobileMenu.classList.toggle('is-open'));
    mobileMenu.querySelectorAll('a').forEach(a =>
      a.addEventListener('click', () => mobileMenu.classList.remove('is-open'))
    );
  }

  /* ---------- Dark Mode Toggle ---------- */
  const themeToggle = document.querySelector('.theme-toggle');
  const root = document.documentElement;
  const savedTheme = localStorage.getItem('qrb-theme');
  if (savedTheme === 'dark') {
    root.setAttribute('data-theme', 'dark');
    if (themeToggle) themeToggle.textContent = '☀';
  }
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const isDark = root.getAttribute('data-theme') === 'dark';
      if (isDark) {
        root.removeAttribute('data-theme');
        themeToggle.textContent = '☾';
        localStorage.setItem('qrb-theme', 'light');
      } else {
        root.setAttribute('data-theme', 'dark');
        themeToggle.textContent = '☀';
        localStorage.setItem('qrb-theme', 'dark');
      }
    });
  }

  /* ---------- Hero Carousel ---------- */
  const slides = document.querySelectorAll('.hero__slide');
  const dots = document.querySelectorAll('.hero__dot');
  if (slides.length) {
    let current = 0;
    const showSlide = (i) => {
      slides.forEach(s => s.classList.remove('is-active'));
      dots.forEach(d => d.classList.remove('is-active'));
      slides[i].classList.add('is-active');
      if (dots[i]) dots[i].classList.add('is-active');
      current = i;
    };
    showSlide(0);
    setInterval(() => showSlide((current + 1) % slides.length), 6000);
    dots.forEach((dot, i) => dot.addEventListener('click', () => showSlide(i)));
  }

  /* ---------- Testimonial Slider ---------- */
  const testimonials = document.querySelectorAll('.testimonial');
  const tDots = document.querySelectorAll('.testimonial-dots button');
  if (testimonials.length) {
    let tCurrent = 0;
    const showTestimonial = (i) => {
      testimonials.forEach(t => t.classList.remove('is-active'));
      tDots.forEach(d => d.classList.remove('is-active'));
      testimonials[i].classList.add('is-active');
      if (tDots[i]) tDots[i].classList.add('is-active');
      tCurrent = i;
    };
    showTestimonial(0);
    setInterval(() => showTestimonial((tCurrent + 1) % testimonials.length), 5500);
    tDots.forEach((dot, i) => dot.addEventListener('click', () => showTestimonial(i)));
  }

  /* ---------- Scroll Reveal ---------- */
  const revealEls = document.querySelectorAll('.reveal, .strata');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    revealEls.forEach(el => io.observe(el));
  } else {
    revealEls.forEach(el => el.classList.add('is-visible'));
  }

  /* ---------- Lightbox Gallery ---------- */
  const galleryItems = document.querySelectorAll('.gallery__item img');
  const lightbox = document.querySelector('.lightbox');
  if (galleryItems.length && lightbox) {
    const lightboxImg = lightbox.querySelector('img');
    const closeBtn = lightbox.querySelector('.lightbox__close');
    const prevBtn = lightbox.querySelector('.lightbox__nav--prev');
    const nextBtn = lightbox.querySelector('.lightbox__nav--next');
    let idx = 0;
    const images = Array.from(galleryItems);

    const open = (i) => {
      idx = i;
      lightboxImg.src = images[idx].src;
      lightboxImg.alt = images[idx].alt;
      lightbox.classList.add('is-open');
      document.body.style.overflow = 'hidden';
    };
    const close = () => {
      lightbox.classList.remove('is-open');
      document.body.style.overflow = '';
    };
    const nav = (dir) => {
      idx = (idx + dir + images.length) % images.length;
      lightboxImg.src = images[idx].src;
      lightboxImg.alt = images[idx].alt;
    };

    images.forEach((img, i) => img.addEventListener('click', () => open(i)));
    closeBtn.addEventListener('click', close);
    prevBtn.addEventListener('click', () => nav(-1));
    nextBtn.addEventListener('click', () => nav(1));
    lightbox.addEventListener('click', (e) => { if (e.target === lightbox) close(); });
    document.addEventListener('keydown', (e) => {
      if (!lightbox.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') nav(-1);
      if (e.key === 'ArrowRight') nav(1);
    });
  }

  /* ---------- Contact / Booking / Prayer Forms ---------- */
  document.querySelectorAll('form[data-form]').forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const status = form.querySelector('.form-status');
      const name = form.querySelector('[name="name"]')?.value || 'Friend';
      if (status) {
        status.textContent = `Thank you, ${name}! Your message has been received. We'll be in touch soon.`;
        status.style.color = 'var(--color-gold)';
      }
      form.reset();
    });
  });

  /* ---------- Newsletter ---------- */
  const newsletterForm = document.querySelector('.newsletter-form');
  if (newsletterForm) {
    newsletterForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const status = newsletterForm.querySelector('.form-status');
      if (status) status.textContent = 'Thank you for subscribing!';
      newsletterForm.reset();
    });
  }

  /* ---------- PWA Install Banner ---------- */
  let deferredPrompt;
  const pwaBanner = document.querySelector('.pwa-banner');
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    if (pwaBanner) pwaBanner.classList.add('is-visible');
  });
  if (pwaBanner) {
    pwaBanner.querySelector('.install')?.addEventListener('click', async () => {
      pwaBanner.classList.remove('is-visible');
      if (deferredPrompt) await deferredPrompt.prompt();
    });
    pwaBanner.querySelector('.dismiss')?.addEventListener('click', () => {
      pwaBanner.classList.remove('is-visible');
    });
  }

  /* ---------- Active Nav Link Highlighting ---------- */
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav__links a');
  if (sections.length && navLinks.length) {
    const navObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          navLinks.forEach(link => {
            link.classList.toggle('active', link.getAttribute('href') === `#${entry.target.id}`);
          });
        }
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    sections.forEach(sec => navObserver.observe(sec));
  }

});