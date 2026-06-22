/* shared.js — BlackCodeLabs */
document.addEventListener('DOMContentLoaded', () => {

  /* ── CURSOR (pointer devices only) ── */
  const dot  = document.getElementById('cursor');
  const ring = document.getElementById('cursor-ring');
  if (dot && ring && window.matchMedia('(hover:hover) and (pointer:fine)').matches) {
    let mx = 0, my = 0, rx = 0, ry = 0;
    document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; });
    (function animCursor() {
      rx += (mx - rx) * 0.11;
      ry += (my - ry) * 0.11;
      dot.style.transform  = `translate(${mx - 5}px,${my - 5}px)`;
      ring.style.transform = `translate(${rx - 17}px,${ry - 17}px)`;
      requestAnimationFrame(animCursor);
    })();
    document.querySelectorAll('a,button,.clickable').forEach(el => {
      el.addEventListener('mouseenter', () => { dot.style.transform += ' scale(2)'; ring.style.opacity = '0.3'; });
      el.addEventListener('mouseleave', () => { ring.style.opacity = '1'; });
    });
  }

  /* ── PAGE TRANSITION ── */
  function navigateTo(url) {
    if (!url) return;
    document.body.classList.add('leaving');
    setTimeout(() => { window.location.href = url; }, 440);
  }
  document.querySelectorAll('a[href]').forEach(a => {
    const h = a.getAttribute('href');
    if (!h || h.startsWith('#') || h.startsWith('mailto') || h.startsWith('tel') || a.target === '_blank') return;
    a.addEventListener('click', e => { e.preventDefault(); navigateTo(a.href); });
  });
  window.addEventListener('load', () => {
    document.body.classList.add('entering');
    setTimeout(() => document.body.classList.remove('entering'), 550);
  });

  /* ── SCROLL REVEAL ── */
  const obs = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el    = entry.target;
      const delay = parseInt(el.dataset.delay || 0, 10);
      setTimeout(() => el.classList.add('visible'), delay);
      obs.unobserve(el);
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });
  document.querySelectorAll('.reveal').forEach(el => obs.observe(el));

  /* ── STAGGER CHILDREN ── */
  document.querySelectorAll('[data-stagger]').forEach(parent => {
    parent.querySelectorAll('[data-stagger-item]').forEach((child, i) => {
      child.dataset.delay = i * 100;
      obs.observe(child);
    });
  });

  /* ── NAV SHRINK ── */
  const nav = document.querySelector('nav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.style.background = window.scrollY > 40
        ? 'rgba(5,5,5,0.97)'
        : 'rgba(5,5,5,0.92)';
    }, { passive: true });
  }

  /* ── HAMBURGER ── */
  const burger = document.querySelector('.hamburger');
  const drawer = document.querySelector('.mobile-drawer');
  if (burger && drawer) {
    burger.addEventListener('click', () => {
      const open = drawer.classList.toggle('open');
      burger.classList.toggle('open', open);
      document.body.style.overflow = open ? 'hidden' : '';
    });
    drawer.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        drawer.classList.remove('open');
        burger.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
  }

});