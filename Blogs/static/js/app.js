// Mobile menu
document.querySelector('.menu-toggle')?.addEventListener('click', function() {
  const nav = document.querySelector('.nav-links');
  const expanded = this.getAttribute('aria-expanded') === 'true';
  this.setAttribute('aria-expanded', !expanded);
  nav?.classList.toggle('open');
});

// Close mobile menu on link click
document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', () => {
    const toggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('.nav-links');
    if (toggle) toggle.setAttribute('aria-expanded', 'false');
    nav?.classList.remove('open');
  });
});

// Nav scroll shadow
document.addEventListener('scroll', () => {
  const nav = document.querySelector('.nav');
  if (window.scrollY > 10) {
    nav?.classList.add('scrolled');
  } else {
    nav?.classList.remove('scrolled');
  }
});

// Reply toggles
document.querySelectorAll('[data-reply]').forEach(btn => {
  btn.addEventListener('click', () => {
    const id = btn.getAttribute('data-reply');
    const form = document.getElementById('reply-' + id);
    const isOpen = form?.classList.contains('open');
    // Close all other reply forms
    document.querySelectorAll('.reply-form.open').forEach(f => f.classList.remove('open'));
    if (!isOpen) {
      form?.classList.add('open');
      form?.querySelector('textarea')?.focus();
    }
  });
});

// CSRF helper
function getCookie(name) {
  const m = document.cookie.match('(^|;)\s*' + name + '\s*=\s*([^;]+)');
  return m ? m.pop() : '';
}

// AJAX like (post + comment)
document.querySelectorAll('.like-form, form.inline').forEach(form => {
  form.addEventListener('submit', async e => {
    if (!form.action.includes('/like/')) return;
    e.preventDefault();
    const btn = form.querySelector('.like-btn');
    btn.style.pointerEvents = 'none';
    try {
      const res = await fetch(form.action, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest'
        },
      });
      if (!res.ok) throw new Error();
      const data = await res.json();
      const count = btn.querySelector('span');
      const svg = btn.querySelector('svg');
      btn.classList.toggle('liked', data.liked);
      if (svg) svg.setAttribute('fill', data.liked ? 'currentColor' : 'none');
      if (count) {
        count.style.transition = 'transform 0.2s';
        count.style.transform = 'scale(1.3)';
        count.textContent = data.count;
        setTimeout(() => { count.style.transform = 'scale(1)'; }, 200);
      }
    } catch {
      form.submit();
    } finally {
      btn.style.pointerEvents = '';
    }
  });
});

// Intersection Observer for scroll animations
const observerOptions = {
  root: null,
  rootMargin: '0px 0px -50px 0px',
  threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.animationPlayState = 'running';
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

document.querySelectorAll('.rise').forEach(el => {
  el.style.animationPlayState = 'paused';
  observer.observe(el);
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// Search input focus effect
document.querySelector('.search-input')?.addEventListener('focus', function() {
  this.closest('.search')?.classList.add('focused');
});
document.querySelector('.search-input')?.addEventListener('blur', function() {
  this.closest('.search')?.classList.remove('focused');
});

// Auto-resize textareas
document.querySelectorAll('textarea').forEach(textarea => {
  textarea.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 300) + 'px';
  });
});