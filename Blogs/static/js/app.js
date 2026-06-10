// ============================================================
// Mobile menu
// ============================================================
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

// Close mobile menu on outside click
document.addEventListener('click', e => {
  const nav = document.querySelector('.nav-links');
  const toggle = document.querySelector('.menu-toggle');
  if (nav?.classList.contains('open') && !nav.contains(e.target) && !toggle?.contains(e.target)) {
    nav.classList.remove('open');
    toggle?.setAttribute('aria-expanded', 'false');
  }
});

// ============================================================
// Nav scroll shadow
// ============================================================
document.addEventListener('scroll', () => {
  const nav = document.querySelector('.nav');
  nav?.classList.toggle('scrolled', window.scrollY > 10);
}, { passive: true });

// ============================================================
// Reply toggles
// ============================================================
document.querySelectorAll('[data-reply]').forEach(btn => {
  btn.addEventListener('click', () => {
    const id = btn.getAttribute('data-reply');
    const form = document.getElementById('reply-' + id);
    const isOpen = form?.classList.contains('open');
    document.querySelectorAll('.reply-form.open').forEach(f => f.classList.remove('open'));
    if (!isOpen) {
      form?.classList.add('open');
      form?.querySelector('textarea')?.focus();
    }
  });
});

// ============================================================
// CSRF helper
// ============================================================
function getCookie(name) {
  const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return m ? m.pop() : '';
}

// ============================================================
// AJAX like (post + comment)
// ============================================================
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

// ============================================================
// Scroll-triggered animations (IntersectionObserver)
// ============================================================
const riseObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.animationPlayState = 'running';
      riseObserver.unobserve(entry.target);
    }
  });
}, { root: null, rootMargin: '0px 0px -50px 0px', threshold: 0.08 });

document.querySelectorAll('.rise').forEach(el => {
  el.style.animationPlayState = 'paused';
  riseObserver.observe(el);
});

// ============================================================
// Smooth scroll for anchor links
// ============================================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ============================================================
// Search input focus effect
// ============================================================
document.querySelector('.search-input')?.addEventListener('focus', function() {
  this.closest('.search')?.classList.add('focused');
});
document.querySelector('.search-input')?.addEventListener('blur', function() {
  this.closest('.search')?.classList.remove('focused');
});

// ============================================================
// Auto-resize textareas
// ============================================================
document.querySelectorAll('textarea').forEach(textarea => {
  textarea.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 300) + 'px';
  });
});

// ============================================================
// FAQ accordion (about page)
// ============================================================
document.querySelectorAll('.faq-item').forEach(item => {
  const question = item.querySelector('.faq-question');
  if (!question) return;

  const toggle = () => {
    const isOpen = item.classList.contains('open');
    // Close all
    document.querySelectorAll('.faq-item.open').forEach(i => {
      i.classList.remove('open');
      i.querySelector('.faq-question')?.setAttribute('aria-expanded', 'false');
    });
    // Open this one if it was closed
    if (!isOpen) {
      item.classList.add('open');
      question.setAttribute('aria-expanded', 'true');
    }
  };

  question.addEventListener('click', toggle);
  question.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
  });
});

// ============================================================
// Contact page: file upload + image preview
// ============================================================
(function initFileUpload() {
  const input = document.getElementById('id_image');
  const label = document.getElementById('uploadLabel');
  const fileName = document.getElementById('fileName');
  const preview = document.getElementById('filePreview');
  const previewImg = document.getElementById('previewImg');
  const removeBtn = document.getElementById('removeFile');
  const wrap = document.getElementById('uploadWrap');

  if (!input || !label) return;

  function handleFile(file) {
    if (!file || !file.type.startsWith('image/')) {
      showUploadError('Please select an image file (PNG, JPG, GIF, WebP).');
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      showUploadError('Image must be under 5 MB.');
      clearFile();
      return;
    }
    if (fileName) fileName.textContent = file.name;
    label.classList.add('has-file');
    const reader = new FileReader();
    reader.onload = e => {
      if (previewImg) previewImg.src = e.target.result;
      preview?.classList.add('visible');
    };
    reader.readAsDataURL(file);
  }

  function clearFile() {
    input.value = '';
    if (fileName) fileName.textContent = '';
    label.classList.remove('has-file');
    preview?.classList.remove('visible');
    if (previewImg) previewImg.src = '';
  }

  function showUploadError(msg) {
    // Use existing flash system if available, else alert
    const container = document.querySelector('.flash-container');
    if (container) {
      const flash = document.createElement('div');
      flash.className = 'flash error';
      flash.innerHTML = `<span class="flash-icon">⚠</span><span>${msg}</span>`;
      container.appendChild(flash);
      setTimeout(() => flash.remove(), 4000);
    } else {
      alert(msg);
    }
  }

  input.addEventListener('change', function() {
    if (this.files && this.files[0]) handleFile(this.files[0]);
  });

  removeBtn?.addEventListener('click', clearFile);

  // Drag and drop
  if (wrap) {
    wrap.addEventListener('dragover', e => {
      e.preventDefault();
      label.style.borderColor = 'var(--navy)';
      label.style.background = '#fff';
    });
    wrap.addEventListener('dragleave', () => {
      label.style.borderColor = '';
      label.style.background = '';
    });
    wrap.addEventListener('drop', e => {
      e.preventDefault();
      label.style.borderColor = '';
      label.style.background = '';
      const file = e.dataTransfer?.files[0];
      if (file) {
        try {
          const dt = new DataTransfer();
          dt.items.add(file);
          input.files = dt.files;
        } catch (_) { /* DataTransfer not supported — preview only */ }
        handleFile(file);
      }
    });
  }
})();

// ============================================================
// Animate counter numbers on the About page stats banner
// ============================================================
(function initCounters() {
  const statNums = document.querySelectorAll('.about-stat-num');
  if (!statNums.length) return;

  const counterObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const suffix = el.querySelector('.about-stat-suffix');
      const suffixText = suffix ? suffix.textContent : '';
      const raw = el.textContent.replace(suffixText, '').trim();
      const target = parseInt(raw.replace(/[^0-9]/g, ''), 10);
      if (isNaN(target)) return;

      counterObserver.unobserve(el);
      let start = 0;
      const duration = 1200;
      const step = timestamp => {
        if (!start) start = timestamp;
        const progress = Math.min((timestamp - start) / duration, 1);
        const ease = 1 - Math.pow(1 - progress, 3); // ease-out cubic
        const current = Math.round(ease * target);
        el.childNodes[0].textContent = current;
        if (progress < 1) requestAnimationFrame(step);
        else el.childNodes[0].textContent = target;
      };
      requestAnimationFrame(step);
    });
  }, { threshold: 0.5 });

  statNums.forEach(el => {
    // Wrap text node so we can replace only the number
    const textNode = el.childNodes[0];
    if (textNode && textNode.nodeType === Node.TEXT_NODE) {
      counterObserver.observe(el);
    }
  });
})();

// ============================================================
// Flash message auto-dismiss
// ============================================================
document.querySelectorAll('.flash').forEach(flash => {
  setTimeout(() => {
    flash.style.transition = 'opacity .4s, transform .4s';
    flash.style.opacity = '0';
    flash.style.transform = 'translateY(-8px)';
    setTimeout(() => flash.remove(), 400);
  }, 5000);
});