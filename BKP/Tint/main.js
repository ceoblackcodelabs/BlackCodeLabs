/* ============================================
   TINT STUDIO — SHARED JS
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ---- NAVBAR SCROLL ---- */
  const navbar = document.querySelector('.navbar');
  window.addEventListener('scroll', () => {
    navbar && navbar.classList.toggle('scrolled', window.scrollY > 40);
  });

  /* ---- ACTIVE NAV LINK ---- */
  const navLinks = document.querySelectorAll('.navbar-links a, .mobile-nav a');
  const currentPage = window.location.pathname.replace(/\//g, '') || 'index';
  navLinks.forEach(link => {
    const href = link.getAttribute('href').replace(/\//g, '').replace('.html','');
    if (href === currentPage || (currentPage === '' && href === 'index') || (currentPage === 'index' && href === '')) {
      link.classList.add('active');
    }
  });

  /* ---- HAMBURGER ---- */
  const hamburger = document.querySelector('.hamburger');
  const mobileNav = document.querySelector('.mobile-nav');
  hamburger && hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('open');
    mobileNav && mobileNav.classList.toggle('open');
  });

  /* ---- SCROLL REVEAL ---- */
  const reveals = document.querySelectorAll('.reveal');
  if (reveals.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          observer.unobserve(e.target);
        }
      });
    }, { threshold: 0.12 });
    reveals.forEach(el => observer.observe(el));
  }

  /* ---- FAQ ACCORDION ---- */
  const faqs = document.querySelectorAll('.faq-trigger');
  faqs.forEach(trigger => {
    trigger.addEventListener('click', () => {
      const body = trigger.nextElementSibling;
      const isOpen = trigger.classList.contains('open');

      // Close all
      document.querySelectorAll('.faq-trigger.open').forEach(t => {
        t.classList.remove('open');
        t.nextElementSibling.style.maxHeight = null;
      });

      // Open clicked (if wasn't open)
      if (!isOpen) {
        trigger.classList.add('open');
        body.style.maxHeight = body.scrollHeight + 'px';
      }
    });
  });

  /* ---- 3D TILT ---- */
  document.querySelectorAll('.tilt-card').forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      card.style.transform = `perspective(600px) rotateY(${x * 10}deg) rotateX(${-y * 10}deg)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'perspective(600px) rotateY(0deg) rotateX(0deg)';
    });
  });

  /* ---- QUOTE FORM SUBMIT ---- */
  document.querySelectorAll('.quote-form').forEach(form => {
    form.addEventListener('submit', e => {
      e.preventDefault();
      showToast('✦ Message received. We\'ll be in touch shortly.');
      form.reset();
    });
  });

  /* ---- TOAST ---- */
  window.showToast = (msg) => {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<span class="toast-icon">✦</span><span>${msg}</span>`;
    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add('show'), 50);
    setTimeout(() => { toast.classList.remove('show'); setTimeout(() => toast.remove(), 400); }, 4000);
  };

  /* ---- STATS COUNTER ---- */
  const statNums = document.querySelectorAll('.stat-number[data-target]');
  if (statNums.length) {
    const countObserver = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          const el = e.target;
          const target = parseInt(el.dataset.target);
          const suffix = el.dataset.suffix || '';
          let start = 0;
          const step = Math.ceil(target / 60);
          const timer = setInterval(() => {
            start = Math.min(start + step, target);
            el.textContent = start + suffix;
            if (start >= target) clearInterval(timer);
          }, 20);
          countObserver.unobserve(el);
        }
      });
    }, { threshold: 0.5 });
    statNums.forEach(el => countObserver.observe(el));
  }

  /* ---- SMOOTH ANCHOR SCROLL ---- */
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

});