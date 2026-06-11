// Theme
(function(){
  const saved = localStorage.getItem('sv-theme');
  if(saved) document.documentElement.setAttribute('data-theme', saved);
})();
document.addEventListener('DOMContentLoaded', () => {
  // Theme toggle
  const tt = document.querySelector('.theme-toggle');
  if(tt) tt.addEventListener('click', () => {
    const cur = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', cur);
    localStorage.setItem('sv-theme', cur);
  });

  // Mobile menu
  const mt = document.querySelector('.menu-toggle');
  const nl = document.querySelector('.nav-links');
  if(mt && nl) mt.addEventListener('click', () => {
    const open = nl.classList.toggle('open');
    mt.setAttribute('aria-expanded', open);
  });

  // Sticky nav shadow + scroll progress
  const nav = document.querySelector('.nav');
  const bar = document.querySelector('.scroll-progress');
  const onScroll = () => {
    if(nav) nav.classList.toggle('scrolled', window.scrollY > 12);
    if(bar){
      const h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (h>0 ? (window.scrollY / h * 100) : 0) + '%';
    }
  };
  window.addEventListener('scroll', onScroll, {passive:true});
  onScroll();

  // Share button
  document.querySelectorAll('.share-btn').forEach(b => {
    b.addEventListener('click', async () => {
      try{ await navigator.clipboard.writeText(window.location.href); }catch(e){}
      b.classList.add('copied');
      setTimeout(()=>b.classList.remove('copied'), 1800);
    });
  });

  // File upload preview
  const fi = document.querySelector('.file-upload-input');
  const fl = document.querySelector('.file-upload-label');
  const fn = document.querySelector('.file-upload-name');
  if(fi && fl){
    fi.addEventListener('change', () => {
      if(fi.files && fi.files[0]){
        fl.classList.add('has-file');
        if(fn) fn.textContent = fi.files[0].name;
      } else {
        fl.classList.remove('has-file');
      }
    });
  }

  // TOC scrollspy
  const links = document.querySelectorAll('.toc a');
  if(links.length){
    const headings = [...links].map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if(e.isIntersecting){
          links.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#'+e.target.id));
        }
      });
    }, {rootMargin: '-30% 0px -60% 0px'});
    headings.forEach(h => io.observe(h));
  }
});
