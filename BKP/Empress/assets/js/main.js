/* ============================================
   THE EMPRESS JASMIN — Shared JavaScript
   ============================================ */

'use strict';

// ─── Star Field ───────────────────────────────────
function initStarfield() {
  const canvas = document.getElementById('starfield');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let stars = [];
  let W, H;

  function resize() {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }

  function createStars(n) {
    stars = [];
    for (let i = 0; i < n; i++) {
      stars.push({
        x: Math.random() * W,
        y: Math.random() * H,
        r: Math.random() * 1.4 + 0.2,
        speed: Math.random() * 0.015 + 0.003,
        opacity: Math.random() * 0.7 + 0.1,
        twinkle: Math.random() * Math.PI * 2,
        twinkleSpeed: Math.random() * 0.02 + 0.005,
        color: Math.random() > 0.85 ? '#D4AF37' : Math.random() > 0.7 ? '#9B59F0' : '#ffffff'
      });
    }
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    stars.forEach(s => {
      s.twinkle += s.twinkleSpeed;
      const alpha = s.opacity * (0.6 + 0.4 * Math.sin(s.twinkle));
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fillStyle = s.color.startsWith('#') 
        ? hexToRgba(s.color, alpha)
        : `rgba(255,255,255,${alpha})`;
      ctx.fill();
      s.y -= s.speed;
      if (s.y < -5) { s.y = H + 5; s.x = Math.random() * W; }
    });
    requestAnimationFrame(draw);
  }

  function hexToRgba(hex, alpha) {
    const r = parseInt(hex.slice(1,3),16);
    const g = parseInt(hex.slice(3,5),16);
    const b = parseInt(hex.slice(5,7),16);
    return `rgba(${r},${g},${b},${alpha})`;
  }

  resize();
  createStars(220);
  draw();
  window.addEventListener('resize', () => { resize(); createStars(220); });
}

// ─── Gold Particles ────────────────────────────────
function initParticles(canvasId) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let particles = [];
  let W, H;

  function resize() {
    W = canvas.width  = canvas.offsetWidth;
    H = canvas.height = canvas.offsetHeight;
  }

  function create(n) {
    particles = [];
    for (let i = 0; i < n; i++) {
      particles.push({
        x: Math.random() * W,
        y: Math.random() * H + H,
        vx: (Math.random() - 0.5) * 0.4,
        vy: -(Math.random() * 0.8 + 0.3),
        r: Math.random() * 2.5 + 0.5,
        life: 0,
        maxLife: Math.random() * 200 + 150,
        color: Math.random() > 0.5 ? '#D4AF37' : '#7C3AED'
      });
    }
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    particles.forEach(p => {
      p.life++;
      p.x += p.vx;
      p.y += p.vy;
      const progress = p.life / p.maxLife;
      const alpha = progress < 0.1 ? progress * 10 : 1 - progress;

      const gradient = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 2);
      gradient.addColorStop(0, p.color === '#D4AF37' 
        ? `rgba(212,175,55,${alpha})` 
        : `rgba(124,58,237,${alpha})`);
      gradient.addColorStop(1, 'transparent');

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r * 2, 0, Math.PI * 2);
      ctx.fillStyle = gradient;
      ctx.fill();

      if (p.life >= p.maxLife) {
        p.x = Math.random() * W;
        p.y = H + Math.random() * 50;
        p.life = 0;
        p.maxLife = Math.random() * 200 + 150;
      }
    });
    requestAnimationFrame(draw);
  }

  resize();
  create(60);
  draw();
  window.addEventListener('resize', () => { resize(); create(60); });
}

// ─── Navigation ────────────────────────────────────
function initNav() {
  const navbar    = document.querySelector('.navbar');
  const toggle    = document.querySelector('.nav-toggle');
  const mobileNav = document.querySelector('.nav-mobile');
  const closeBtn  = document.querySelector('.nav-mobile-close');

  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 50);
    });
  }

  if (toggle && mobileNav) {
    toggle.addEventListener('click', () => mobileNav.classList.add('open'));
  }

  if (closeBtn && mobileNav) {
    closeBtn.addEventListener('click', () => mobileNav.classList.remove('open'));
  }

  if (mobileNav) {
    mobileNav.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => mobileNav.classList.remove('open'));
    });
  }

  // Active link
  const path = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a, .nav-mobile a').forEach(a => {
    const href = a.getAttribute('href');
    if (href === path || (path === '' && href === 'index.html')) {
      a.classList.add('active');
    }
  });
}

// ─── Sticky Booking Button ─────────────────────────
function initStickyBook() {
  const btn = document.querySelector('.sticky-book');
  if (!btn) return;
  window.addEventListener('scroll', () => {
    btn.classList.toggle('visible', window.scrollY > 600);
  });
}

// ─── Scroll Reveal ─────────────────────────────────
function initReveal() {
  const els = document.querySelectorAll('.reveal');
  if (!els.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.12 });

  els.forEach(el => observer.observe(el));
}

// ─── Counter Animation ─────────────────────────────
function animateCounter(el, target, suffix, duration) {
  let start = 0;
  const step = target / (duration / 16);
  const timer = setInterval(() => {
    start = Math.min(start + step, target);
    el.textContent = Math.floor(start).toLocaleString() + suffix;
    if (start >= target) clearInterval(timer);
  }, 16);
}

function initCounters() {
  const counters = document.querySelectorAll('[data-count]');
  if (!counters.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const el     = e.target;
        const target = parseFloat(el.dataset.count);
        const suffix = el.dataset.suffix || '';
        animateCounter(el, target, suffix, 2000);
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(c => observer.observe(c));
}

// ─── Testimonial Slider ────────────────────────────
function initTestimonialSlider() {
  const slider = document.querySelector('.testimonial-slider');
  if (!slider) return;

  const cards  = slider.querySelectorAll('.testimonial-card');
  const prev   = document.querySelector('.slider-prev');
  const next   = document.querySelector('.slider-next');
  const dots   = document.querySelectorAll('.slider-dot');
  let current  = 0;
  let interval;

  function show(idx) {
    cards.forEach((c, i) => {
      c.classList.toggle('active', i === idx);
    });
    dots.forEach((d, i) => {
      d.classList.toggle('active', i === idx);
    });
    current = idx;
  }

  function advance() {
    show((current + 1) % cards.length);
  }

  function start() {
    interval = setInterval(advance, 5000);
  }

  function stop() {
    clearInterval(interval);
  }

  if (prev) prev.addEventListener('click', () => { stop(); show((current - 1 + cards.length) % cards.length); start(); });
  if (next) next.addEventListener('click', () => { stop(); advance(); start(); });
  dots.forEach((d, i) => {
    d.addEventListener('click', () => { stop(); show(i); start(); });
  });

  show(0);
  start();
}

// ─── Moon Parallax ─────────────────────────────────
function initParallax() {
  const moon = document.querySelector('.hero-moon');
  if (!moon) return;

  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    moon.style.transform = `translateY(${y * 0.25}px) rotate(${y * 0.03}deg)`;
  }, { passive: true });
}

// ─── Constellation Lines (SVG) ─────────────────────
function initConstellations() {
  const svg = document.getElementById('constellation-svg');
  if (!svg) return;

  const W = svg.clientWidth;
  const H = svg.clientHeight;

  const points = [];
  for (let i = 0; i < 18; i++) {
    points.push({
      x: Math.random() * W,
      y: Math.random() * H,
      vx: (Math.random() - 0.5) * 0.15,
      vy: (Math.random() - 0.5) * 0.15,
    });
  }

  function connectClose(a, b) {
    const dx = a.x - b.x, dy = a.y - b.y;
    return Math.sqrt(dx*dx + dy*dy) < 180;
  }

  function tick() {
    svg.innerHTML = '';
    points.forEach(p => {
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0 || p.x > W) p.vx *= -1;
      if (p.y < 0 || p.y > H) p.vy *= -1;
    });

    for (let i = 0; i < points.length; i++) {
      for (let j = i+1; j < points.length; j++) {
        if (connectClose(points[i], points[j])) {
          const line = document.createElementNS('http://www.w3.org/2000/svg','line');
          line.setAttribute('x1', points[i].x);
          line.setAttribute('y1', points[i].y);
          line.setAttribute('x2', points[j].x);
          line.setAttribute('y2', points[j].y);
          line.setAttribute('stroke','rgba(212,175,55,0.15)');
          line.setAttribute('stroke-width','0.6');
          svg.appendChild(line);
        }
      }
    }

    points.forEach(p => {
      const circle = document.createElementNS('http://www.w3.org/2000/svg','circle');
      circle.setAttribute('cx', p.x);
      circle.setAttribute('cy', p.y);
      circle.setAttribute('r','1.5');
      circle.setAttribute('fill','rgba(212,175,55,0.6)');
      svg.appendChild(circle);
    });

    requestAnimationFrame(tick);
  }

  tick();
}

// ─── Init Everything ───────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initStarfield();
  initNav();
  initStickyBook();
  initReveal();
  initCounters();
  initTestimonialSlider();
  initParallax();
  initConstellations();

  // Init particles for each canvas found
  document.querySelectorAll('[data-particles]').forEach(el => {
    initParticles(el.id);
  });
});
