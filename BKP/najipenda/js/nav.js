/* shared nav helper — injects active class based on current page */
document.addEventListener('DOMContentLoaded',()=>{
  const p=window.location.pathname.split('/').pop()||'index.html';
  document.querySelectorAll('.nav-link').forEach(a=>{
    a.classList.toggle('active', a.getAttribute('href')===p || (p===''&&a.getAttribute('href')==='index.html'));
  });
  document.querySelectorAll('.sb-link').forEach(a=>{
    a.classList.toggle('active', a.getAttribute('href')===p);
  });
  document.querySelectorAll('.bnav-btn').forEach(a=>{
    a.classList.toggle('active', a.getAttribute('href')===p);
  });
});
