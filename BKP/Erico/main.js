/* ===== AZZIAD — MAIN.JS ===== */

/* ---- CUSTOM CURSOR ---- */
const cursor = document.getElementById('cursor');
const follower = document.getElementById('cursorFollower');
let mx = 0, my = 0, fx = 0, fy = 0;
document.addEventListener('mousemove', e => {
  mx = e.clientX; my = e.clientY;
  if (cursor) { cursor.style.left = mx + 'px'; cursor.style.top = my + 'px'; }
});
function animFollower() {
  fx += (mx - fx) * 0.12;
  fy += (my - fy) * 0.12;
  if (follower) { follower.style.left = fx + 'px'; follower.style.top = fy + 'px'; }
  requestAnimationFrame(animFollower);
}
animFollower();

/* ---- LOADER ---- */
const loader = document.getElementById('loader');
const fill = document.getElementById('loaderFill');
const ltxt = document.getElementById('loaderText');
const msgs = ['Initializing…','Loading assets…','Almost there…','Welcome ✦'];
let prog = 0;
const iv = setInterval(() => {
  prog += Math.random() * 18 + 5;
  if (prog >= 100) prog = 100;
  if (fill) fill.style.width = prog + '%';
  if (ltxt) ltxt.textContent = msgs[Math.floor(prog / 26)] || msgs[3];
  if (prog === 100) {
    clearInterval(iv);
    setTimeout(() => {
      if (loader) loader.classList.add('done');
      document.body.style.overflow = '';
    }, 400);
  }
}, 100);
document.body.style.overflow = 'hidden';

/* ---- NAVBAR SCROLL ---- */
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  if (navbar) navbar.classList.toggle('scrolled', window.scrollY > 50);
}, { passive: true });

/* ---- MOBILE MENU ---- */
const toggle = document.getElementById('navToggle');
const mMenu = document.getElementById('mobileMenu');
let menuOpen = false;
if (toggle && mMenu) {
  toggle.addEventListener('click', () => {
    menuOpen = !menuOpen;
    toggle.classList.toggle('open', menuOpen);
    mMenu.classList.toggle('open', menuOpen);
  });
  mMenu.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      menuOpen = false;
      toggle.classList.remove('open');
      mMenu.classList.remove('open');
    });
  });
}

/* ---- REVEAL ON SCROLL ---- */
const revealEls = document.querySelectorAll('.reveal-up, .reveal-left, .reveal-right');
const revealObs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('in');
      revealObs.unobserve(e.target);
    }
  });
}, { threshold: 0.1 });
revealEls.forEach(el => revealObs.observe(el));

/* ---- COUNTER ANIMATION ---- */
const counts = document.querySelectorAll('.count');
let counted = false;
function runCounters() {
  if (counted) return;
  counted = true;
  counts.forEach(el => {
    const target = parseInt(el.dataset.target);
    const dur = 1800;
    const step = target / (dur / 16);
    let cur = 0;
    const t = setInterval(() => {
      cur += step;
      if (cur >= target) { el.textContent = target; clearInterval(t); }
      else el.textContent = Math.floor(cur);
    }, 16);
  });
}
const heroObs = new IntersectionObserver(e => { if (e[0].isIntersecting) runCounters(); }, { threshold: 0.3 });
const hs = document.querySelector('.hero-stats-row');
if (hs) heroObs.observe(hs);

/* ---- PARALLAX ENGINE ---- */
function lerp(a, b, t) { return a + (b - a) * t; }
let scrollY = 0;
let tScrollY = 0;

window.addEventListener('scroll', () => { tScrollY = window.pageYOffset; }, { passive: true });

// Elements with data-parallax-speed attribute
const pxEls = document.querySelectorAll('[data-parallax-speed]');

// Hero background parallax
const heroBg = document.getElementById('heroBg');
const qbBg = document.getElementById('qbBg');
const nbParallax = document.querySelector('.nb-parallax');
const qbText = document.querySelector('.qb-text');

function rafLoop() {
  scrollY = lerp(scrollY, tScrollY, 0.08);

  // Hero background
  if (heroBg) {
    const progress = scrollY * 0.25;
    heroBg.style.transform = `translateY(${progress}px)`;
  }

  // Quote band BG
  if (qbBg) {
    const qbSection = qbBg.closest('.quote-band');
    if (qbSection) {
      const rect = qbSection.getBoundingClientRect();
      const progress = (window.innerHeight - rect.top) / (window.innerHeight + rect.height);
      qbBg.style.transform = `translateY(${(progress - 0.5) * -60}px)`;
    }
  }

  // Quote text subtle
  if (qbText) {
    const sect = qbText.closest('.quote-band');
    if (sect) {
      const rect = sect.getBoundingClientRect();
      const p = (window.innerHeight - rect.top) / (window.innerHeight + rect.height);
      qbText.style.transform = `translateY(${(p - 0.5) * -30}px)`;
    }
  }

  // Numbers band
  if (nbParallax) {
    const sect = nbParallax.closest('.numbers-band');
    if (sect) {
      const rect = sect.getBoundingClientRect();
      const p = (window.innerHeight - rect.top) / (window.innerHeight + rect.height);
      nbParallax.style.transform = `translateY(${(p - 0.5) * -40}px)`;
    }
  }

  // About background text
  const aboutBgTxt = document.querySelector('.about-bg-text');
  if (aboutBgTxt) {
    const sect = aboutBgTxt.closest('.about');
    if (sect) {
      const rect = sect.getBoundingClientRect();
      const p = (window.innerHeight - rect.top) / (window.innerHeight + rect.height);
      aboutBgTxt.style.transform = `translate(-50%, calc(-50% + ${(p - 0.5) * -50}px))`;
    }
  }

  // Floating pills
  document.querySelectorAll('.fpill[data-depth]').forEach(pill => {
    const depth = parseFloat(pill.dataset.depth);
    const rect = pill.closest('.hero-center')?.getBoundingClientRect();
    if (rect) {
      const p = (window.innerHeight / 2 - rect.top) * depth;
      pill.style.transform = `translateY(${p}px)`;
    }
  });

  requestAnimationFrame(rafLoop);
}
rafLoop();

/* ---- 3D TILT CARDS ---- */
document.querySelectorAll('.service-card, .testi-card, .tc, .brand-item').forEach(card => {
  card.addEventListener('mousemove', e => {
    const r = card.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - 0.5;
    const y = (e.clientY - r.top) / r.height - 0.5;
    card.style.transform = `translateY(-6px) perspective(800px) rotateX(${-y * 6}deg) rotateY(${x * 6}deg)`;
  });
  card.addEventListener('mouseleave', () => { card.style.transform = ''; });
});

/* ---- SERVICE ROW HOVER ---- */
document.querySelectorAll('.sv-row').forEach(row => {
  row.addEventListener('click', () => {
    document.querySelector('#contact')?.scrollIntoView({ behavior: 'smooth' });
  });
});

/* ---- GALLERY IMAGE HOVER SCALE ---- */
// Already handled in CSS

/* ---- CONTACT FORM ---- */
const form = document.getElementById('contactForm');
const cfSuccess = document.getElementById('cfSuccess');
if (form) {
  form.addEventListener('submit', e => {
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    const lbl = btn.querySelector('.cta-label');
    btn.disabled = true;
    if (lbl) lbl.textContent = 'Sending…';
    setTimeout(() => {
      if (lbl) lbl.textContent = 'Send Booking Request';
      btn.disabled = false;
      if (cfSuccess) { cfSuccess.style.display = 'block'; }
      form.reset();
      setTimeout(() => { if (cfSuccess) cfSuccess.style.display = 'none'; }, 5000);
    }, 1600);
  });
}

/* ---- ACTIVE NAV HIGHLIGHT ---- */
const sections = document.querySelectorAll('section[id]');
const navAs = document.querySelectorAll('.nav-links a[href^="#"]');
window.addEventListener('scroll', () => {
  let cur = '';
  sections.forEach(s => { if (window.scrollY >= s.offsetTop - 140) cur = s.id; });
  navAs.forEach(a => {
    const isActive = a.getAttribute('href') === '#' + cur;
    a.style.color = isActive ? 'var(--gold)' : '';
  });
}, { passive: true });

/* ---- SMOOTH SCROLL ---- */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

/* ---- HERO IMG PARALLAX ON MOUSE MOVE ---- */
const heroImgContainer = document.getElementById('heroImgContainer');
document.addEventListener('mousemove', e => {
  if (!heroImgContainer) return;
  const cx = window.innerWidth / 2;
  const cy = window.innerHeight / 2;
  const dx = (e.clientX - cx) / cx;
  const dy = (e.clientY - cy) / cy;
  heroImgContainer.style.transform = `perspective(1000px) rotateY(${dx * 5}deg) rotateX(${-dy * 3}deg) translateZ(10px)`;
});

/* ---- NUMBERS BAND — COUNT UP ON ENTER ---- */
const nbObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.querySelectorAll('[data-target]').forEach(el => {
        const target = parseInt(el.dataset.target);
        let cur = 0;
        const step = target / 60;
        const t = setInterval(() => {
          cur += step;
          if (cur >= target) { el.textContent = target; clearInterval(t); }
          else el.textContent = Math.floor(cur);
        }, 24);
      });
      nbObs.unobserve(e.target);
    }
  });
}, { threshold: 0.3 });
const nb = document.querySelector('.numbers-band');
if (nb) nbObs.observe(nb);