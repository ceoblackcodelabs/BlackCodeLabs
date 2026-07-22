/* ==========================================================================
   DATALINK GROUP — SCRIPT.JS
   Vanilla JS only. Organized by feature. Each section is self-guarding
   (checks the element exists) so this one file can be shared by every page.
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {

  /* ------------------------------------------------------------------ */
  /* 0. PRODUCT DATA — single source of truth for shop + product page   */
  /* ------------------------------------------------------------------ */
  const PRODUCTS = [
    { id: 1,  name: 'DL-4MP Dome Camera Pro',      category: 'cctv',        categoryLabel: 'CCTV Cameras',   price: 8500,  stock: 'in-stock',  desc: 'High-resolution dome camera with 30m night vision, built for continuous indoor and outdoor monitoring.' },
    { id: 2,  name: 'DL-Bullet Cam Outdoor 5MP',   category: 'cctv',        categoryLabel: 'CCTV Cameras',   price: 9200,  stock: 'in-stock',  desc: 'Weatherproof bullet camera with long-range infrared, ideal for perimeter and gate monitoring.' },
    { id: 3,  name: 'DL-PTZ Speed Dome',           category: 'cctv',        categoryLabel: 'CCTV Cameras',   price: 24500, stock: 'pre-order', desc: 'Pan-tilt-zoom camera with 360° coverage and auto-tracking for large open areas.' },
    { id: 4,  name: 'DL-Mini WiFi Cam',            category: 'cctv',        categoryLabel: 'CCTV Cameras',   price: 4200,  stock: 'in-stock',  desc: 'Compact wireless camera for indoor monitoring with two-way audio and mobile alerts.' },
    { id: 5,  name: 'DL-8CH NVR System',           category: 'dvr',         categoryLabel: 'DVR/NVR',        price: 15800, stock: 'in-stock',  desc: '8-channel network video recorder with 2TB storage, supports remote playback.' },
    { id: 6,  name: 'DL-16CH DVR Recorder',        category: 'dvr',         categoryLabel: 'DVR/NVR',        price: 21000, stock: 'in-stock',  desc: '16-channel DVR built for medium to large sites needing extended recording capacity.' },
    { id: 7,  name: 'DL-Solar Backup Kit 300W',    category: 'solar',       categoryLabel: 'Solar Equipment',price: 32500, stock: 'in-stock',  desc: 'Complete solar backup kit that keeps cameras and gates powered through outages.' },
    { id: 8,  name: 'DL-Solar Panel 150W Mono',    category: 'solar',       categoryLabel: 'Solar Equipment',price: 11500, stock: 'pre-order', desc: 'High-efficiency monocrystalline panel suited for small security installations.' },
    { id: 9,  name: 'DL-PoE Network Switch 8-Port',category: 'networking',  categoryLabel: 'Networking',     price: 6800,  stock: 'in-stock',  desc: 'Managed 8-port PoE switch that powers cameras and access points over a single cable run.' },
    { id: 10, name: 'DL-Outdoor WiFi Access Point',category: 'networking',  categoryLabel: 'Networking',     price: 7400,  stock: 'in-stock',  desc: 'Weatherproof access point for extending Wi-Fi coverage across large compounds.' },
    { id: 11, name: 'DL-CAT6 Cable Bundle (100m)', category: 'accessories', categoryLabel: 'Accessories',    price: 3200,  stock: 'in-stock',  desc: 'Shielded CAT6 cable bundle for reliable long-run camera and network installs.' },
    { id: 12, name: 'DL-Smart Video Doorbell',     category: 'smart',       categoryLabel: 'Smart Security', price: 5600,  stock: 'in-stock',  desc: 'Smart doorbell with HD video, motion alerts and remote two-way talk via mobile app.' },
  ];

  const formatKES = (n) => 'KSh ' + n.toLocaleString('en-KE');

  /* ------------------------------------------------------------------ */
  /* 1. YEAR STAMP (footer)                                              */
  /* ------------------------------------------------------------------ */
  document.querySelectorAll('#year').forEach(el => el.textContent = new Date().getFullYear());

  /* ------------------------------------------------------------------ */
  /* 2. STICKY NAVBAR + ACTIVE LINK HIGHLIGHT ON SCROLL                  */
  /* ------------------------------------------------------------------ */
  const navbar = document.getElementById('navbar');
  const onScrollNav = () => {
    if (!navbar) return;
    navbar.classList.toggle('scrolled', window.scrollY > 40);
  };
  window.addEventListener('scroll', onScrollNav);
  onScrollNav();

  // Highlight nav link matching current scroll section (home page sections)
  const sections = ['about', 'services', 'testimonials'].map(id => document.getElementById(id)).filter(Boolean);
  const navLinkEls = document.querySelectorAll('.nav-links a, .mobile-menu a');
  if (sections.length) {
    window.addEventListener('scroll', () => {
      let current = 'home';
      sections.forEach(sec => {
        const rect = sec.getBoundingClientRect();
        if (rect.top <= 120 && rect.bottom >= 120) current = sec.id;
      });
      navLinkEls.forEach(a => {
        const href = a.getAttribute('href') || '';
        const isMatch = href === `index.html#${current}` || (current === 'home' && href === 'index.html');
        a.classList.toggle('active', isMatch && href.includes('#') || (current === 'home' && (href === 'index.html')));
      });
    });
  }

  /* ------------------------------------------------------------------ */
  /* 3. MOBILE HAMBURGER MENU                                            */
  /* ------------------------------------------------------------------ */
  const hamburger = document.getElementById('hamburger');
  const mobileMenu = document.getElementById('mobileMenu');
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('active');
      mobileMenu.classList.toggle('open');
      document.body.style.overflow = mobileMenu.classList.contains('open') ? 'hidden' : '';
    });
    mobileMenu.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        hamburger.classList.remove('active');
        mobileMenu.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
  }

  /* ------------------------------------------------------------------ */
  /* 4. HERO IMAGE CAROUSEL (auto + arrows + dots)                       */
  /* ------------------------------------------------------------------ */
  const heroSlides = document.querySelectorAll('.hero-slide');
  const heroDotsWrap = document.getElementById('heroDots');
  if (heroSlides.length) {
    let heroIndex = 0;
    let heroTimer = null;

    // Build dots dynamically
    heroSlides.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.className = 'hero-dot' + (i === 0 ? ' active' : '');
      dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
      dot.addEventListener('click', () => goToHeroSlide(i));
      heroDotsWrap.appendChild(dot);
    });
    const heroDots = heroDotsWrap.querySelectorAll('.hero-dot');

    function showHeroSlide(i) {
      heroSlides.forEach(s => s.classList.remove('active'));
      heroDots.forEach(d => d.classList.remove('active'));
      heroSlides[i].classList.add('active');
      heroDots[i].classList.add('active');
    }
    function goToHeroSlide(i) {
      heroIndex = (i + heroSlides.length) % heroSlides.length;
      showHeroSlide(heroIndex);
      resetHeroTimer();
    }
    function nextHeroSlide() { goToHeroSlide(heroIndex + 1); }
    function prevHeroSlide() { goToHeroSlide(heroIndex - 1); }
    function resetHeroTimer() {
      clearInterval(heroTimer);
      heroTimer = setInterval(nextHeroSlide, 5000);
    }

    document.getElementById('heroNext')?.addEventListener('click', nextHeroSlide);
    document.getElementById('heroPrev')?.addEventListener('click', prevHeroSlide);

    resetHeroTimer();
  }

  /* ------------------------------------------------------------------ */
  /* 5. TESTIMONIAL CAROUSEL (auto + arrows)                             */
  /* ------------------------------------------------------------------ */
  const testTrack = document.getElementById('testimonialSlides');
  if (testTrack) {
    const testCards = testTrack.querySelectorAll('.testimonial-card');
    let testIndex = 0;
    let testTimer = null;

    function showTestSlide(i) {
      testIndex = (i + testCards.length) % testCards.length;
      testTrack.style.transform = `translateX(-${testIndex * 100}%)`;
    }
    function resetTestTimer() {
      clearInterval(testTimer);
      testTimer = setInterval(() => showTestSlide(testIndex + 1), 6000);
    }

    document.getElementById('testNext')?.addEventListener('click', () => { showTestSlide(testIndex + 1); resetTestTimer(); });
    document.getElementById('testPrev')?.addEventListener('click', () => { showTestSlide(testIndex - 1); resetTestTimer(); });

    resetTestTimer();
  }

  /* ------------------------------------------------------------------ */
  /* 6. SCROLL-REVEAL ANIMATIONS                                         */
  /* ------------------------------------------------------------------ */
  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length && 'IntersectionObserver' in window) {
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

  /* ------------------------------------------------------------------ */
  /* 7. SMOOTH SCROLL FOR ANCHOR LINKS                                   */
  /* ------------------------------------------------------------------ */
  document.querySelectorAll('a[href*="#"]').forEach(link => {
    const href = link.getAttribute('href');
    const hashIndex = href.indexOf('#');
    if (hashIndex === -1) return;
    const targetId = href.slice(hashIndex + 1);
    const samePage = href.slice(0, hashIndex) === '' || href.slice(0, hashIndex) === window.location.pathname.split('/').pop();
    if (!samePage || !targetId) return;
    link.addEventListener('click', (e) => {
      const target = document.getElementById(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  /* ------------------------------------------------------------------ */
  /* 8. BACK TO TOP BUTTON                                               */
  /* ------------------------------------------------------------------ */
  const backToTop = document.getElementById('backToTop');
  if (backToTop) {
    window.addEventListener('scroll', () => {
      backToTop.classList.toggle('visible', window.scrollY > 500);
    });
    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ------------------------------------------------------------------ */
  /* 9. PRODUCT GRID — RENDER, SEARCH, FILTER, SORT (ecommerce.html)     */
  /* ------------------------------------------------------------------ */
  const productGrid = document.getElementById('productGrid');
  if (productGrid) {

    const PRODUCTS_PER_PAGE = 6;
    let currentPage = 1;

    function renderProducts(list) {
      productGrid.innerHTML = '';
      if (!list.length) {
        productGrid.innerHTML = `
          <div class="no-results">
            <i class="fa-solid fa-magnifying-glass"></i>
            <p>No products match your filters. Try resetting them.</p>
          </div>`;
        return;
      }
      list.forEach(p => {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
          <div class="product-media">
            <span class="product-badge">${p.categoryLabel}</span>
            <span>${p.name.replace(/\s+/g, '-').toLowerCase()}.jpg</span>
          </div>
          <div class="product-body">
            <h3>${p.name}</h3>
            <p>${p.desc}</p>
            <div class="product-price">${formatKES(p.price)}</div>
            <a class="btn btn-solid" href="product-details.html?id=${p.id}">View Details</a>
          </div>`;
        productGrid.appendChild(card);
      });
    }

    function getFilteredProducts() {
      const searchTerm = (document.getElementById('productSearch')?.value || '').toLowerCase().trim();
      const activeCats = Array.from(document.querySelectorAll('.cat-filter:checked')).map(c => c.value);
      const maxPrice = parseInt(document.getElementById('priceRange')?.value || '60000', 10);
      const availability = document.querySelector('input[name="availability"]:checked')?.value || 'all';
      const sortBy = document.getElementById('sortSelect')?.value || 'default';

      let list = PRODUCTS.filter(p => {
        const matchesSearch = !searchTerm || p.name.toLowerCase().includes(searchTerm) || p.categoryLabel.toLowerCase().includes(searchTerm);
        const matchesCat = !activeCats.length || activeCats.includes(p.category);
        const matchesPrice = p.price <= maxPrice;
        const matchesAvail = availability === 'all' || p.stock === availability;
        return matchesSearch && matchesCat && matchesPrice && matchesAvail;
      });

      if (sortBy === 'price-asc') list.sort((a, b) => a.price - b.price);
      if (sortBy === 'price-desc') list.sort((a, b) => b.price - a.price);
      if (sortBy === 'name-asc') list.sort((a, b) => a.name.localeCompare(b.name));

      return list;
    }

    function renderPagination(totalItems) {
      const pagination = document.getElementById('pagination');
      if (!pagination) return;
      const totalPages = Math.ceil(totalItems / PRODUCTS_PER_PAGE);

      if (totalPages <= 1) {
        pagination.innerHTML = '';
        return;
      }

      // Build a compact page list with ellipses for larger catalogs, e.g. 1 2 3 ... 8
      const pages = [];
      const addPage = (n) => { if (!pages.includes(n)) pages.push(n); };
      addPage(1);
      addPage(totalPages);
      for (let n = currentPage - 1; n <= currentPage + 1; n++) {
        if (n > 1 && n < totalPages) addPage(n);
      }
      pages.sort((a, b) => a - b);

      let html = `<button data-page="prev" ${currentPage === 1 ? 'disabled' : ''} aria-label="Previous page"><i class="fa-solid fa-chevron-left"></i></button>`;
      let lastPage = 0;
      pages.forEach(p => {
        if (p - lastPage > 1) html += `<span class="pagination-ellipsis">&hellip;</span>`;
        html += `<button data-page="${p}" class="${p === currentPage ? 'active' : ''}">${p}</button>`;
        lastPage = p;
      });
      html += `<button data-page="next" ${currentPage === totalPages ? 'disabled' : ''} aria-label="Next page"><i class="fa-solid fa-chevron-right"></i></button>`;

      pagination.innerHTML = html;

      pagination.querySelectorAll('button[data-page]').forEach(btn => {
        btn.addEventListener('click', () => {
          const val = btn.getAttribute('data-page');
          if (val === 'prev') currentPage = Math.max(1, currentPage - 1);
          else if (val === 'next') currentPage = Math.min(totalPages, currentPage + 1);
          else currentPage = parseInt(val, 10);
          refresh(false);
          productGrid.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
      });
    }

    function refresh(resetPage = true) {
      if (resetPage) currentPage = 1;
      const list = getFilteredProducts();
      const totalPages = Math.max(1, Math.ceil(list.length / PRODUCTS_PER_PAGE));
      currentPage = Math.min(currentPage, totalPages);
      const start = (currentPage - 1) * PRODUCTS_PER_PAGE;
      const pageItems = list.slice(start, start + PRODUCTS_PER_PAGE);

      renderProducts(pageItems);
      renderPagination(list.length);

      const countEl = document.getElementById('resultsCount');
      if (countEl) countEl.textContent = list.length;
    }

    document.getElementById('productSearch')?.addEventListener('input', () => refresh(true));
    document.querySelectorAll('.cat-filter').forEach(cb => cb.addEventListener('change', () => refresh(true)));
    document.querySelectorAll('input[name="availability"]').forEach(rb => rb.addEventListener('change', () => refresh(true)));
    document.getElementById('sortSelect')?.addEventListener('change', () => refresh(true));

    const priceRange = document.getElementById('priceRange');
    const priceRangeValue = document.getElementById('priceRangeValue');
    priceRange?.addEventListener('input', () => {
      priceRangeValue.textContent = formatKES(parseInt(priceRange.value, 10));
      refresh(true);
    });

    document.getElementById('resetFilters')?.addEventListener('click', () => {
      document.getElementById('productSearch').value = '';
      document.querySelectorAll('.cat-filter').forEach(cb => cb.checked = false);
      document.querySelector('input[name="availability"][value="all"]').checked = true;
      priceRange.value = 60000;
      priceRangeValue.textContent = formatKES(60000);
      document.getElementById('sortSelect').value = 'default';
      refresh(true);
    });

    refresh(true);
  }

  /* ------------------------------------------------------------------ */
  /* 10. PRODUCT DETAILS PAGE — populate from URL ?id=                  */
  /* ------------------------------------------------------------------ */
  const pdName = document.getElementById('pdName');
  if (pdName) {
    const params = new URLSearchParams(window.location.search);
    const id = parseInt(params.get('id'), 10) || 1;
    const product = PRODUCTS.find(p => p.id === id) || PRODUCTS[0];

    document.getElementById('pageTitle').textContent = `${product.name} | Datalink Group`;
    document.getElementById('pageHeading').textContent = product.name;
    document.getElementById('breadcrumbProduct').textContent = product.name;
    document.getElementById('pdCategory').textContent = product.categoryLabel;
    pdName.textContent = product.name;
    document.getElementById('pdPrice').textContent = formatKES(product.price);
    document.getElementById('pdMainImageLabel').textContent = product.name.replace(/\s+/g, '-').toLowerCase() + '-main.jpg';
    const descEl = document.querySelector('.pd-desc');
    if (descEl) descEl.textContent = product.desc;

    const availEl = document.getElementById('pdAvailability');
    if (availEl) {
      const isInStock = product.stock === 'in-stock';
      availEl.innerHTML = `<i class="fa-solid fa-circle"></i> ${isInStock ? 'In Stock' : 'Pre-Order'}`;
      availEl.style.color = isInStock ? '#1a9c56' : 'var(--color-accent-dark)';
      availEl.style.background = isInStock ? 'rgba(26,156,86,0.08)' : 'rgba(245,180,0,0.12)';
    }

    // Thumbnail switching — clicking a thumb relabels the main image
    document.querySelectorAll('.pd-thumb').forEach(thumb => {
      thumb.addEventListener('click', () => {
        document.querySelectorAll('.pd-thumb').forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');
        const num = thumb.getAttribute('data-thumb');
        document.getElementById('pdMainImageLabel').textContent =
          `${product.name.replace(/\s+/g, '-').toLowerCase()}-view-${num}.jpg`;
      });
    });

    // WhatsApp purchase link — auto-generated with the product name
    const whatsappBtn = document.getElementById('whatsappBtn');
    if (whatsappBtn) {
      const message = `Hello Datalink Group, I am interested in the ${product.name}`;
      whatsappBtn.href = `https://wa.me/254700000000?text=${encodeURIComponent(message)}`;
    }

    // Downloadable datasheet — placeholder file. Upload the real PDF into this
    // folder using this exact filename (or edit DOWNLOAD_FILE_PATH below) and
    // it will become downloadable automatically, per product.
    const slug = product.name.replace(/\s+/g, '-').toLowerCase();
    const DOWNLOAD_FILE_PATH = `downloads/${slug}-datasheet.pdf`;
    const downloadResource = document.getElementById('downloadResource');
    const downloadFileName = document.getElementById('downloadFileName');
    if (downloadResource) {
      downloadResource.href = DOWNLOAD_FILE_PATH;
      downloadResource.setAttribute('download', `${slug}-datasheet.pdf`);
      if (downloadFileName) downloadFileName.textContent = `${slug}-datasheet.pdf`;
    }

    // External resource link — points to another site (e.g. the manufacturer's
    // page for this product). Replace EXTERNAL_RESOURCE_URL per product as needed.
    const EXTERNAL_RESOURCE_URL = `https://example.com/products/${slug}`;
    const externalResource = document.getElementById('externalResource');
    if (externalResource) externalResource.href = EXTERNAL_RESOURCE_URL;

    // Related products — same category, excluding current
    const relatedGrid = document.getElementById('relatedGrid');
    if (relatedGrid) {
      const related = PRODUCTS.filter(p => p.category === product.category && p.id !== product.id).slice(0, 4);
      const fallback = related.length ? related : PRODUCTS.filter(p => p.id !== product.id).slice(0, 4);
      relatedGrid.innerHTML = fallback.map(p => `
        <div class="product-card">
          <div class="product-media">
            <span class="product-badge">${p.categoryLabel}</span>
            <span>${p.name.replace(/\s+/g, '-').toLowerCase()}.jpg</span>
          </div>
          <div class="product-body">
            <h3>${p.name}</h3>
            <p>${p.desc}</p>
            <div class="product-price">${formatKES(p.price)}</div>
            <a class="btn btn-solid" href="product-details.html?id=${p.id}">View Details</a>
          </div>
        </div>
      `).join('');
    }
  }

  /* ------------------------------------------------------------------ */
  /* 11. CONTACT FORM — client-side handling                             */
  /* ------------------------------------------------------------------ */
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!contactForm.checkValidity()) {
        contactForm.reportValidity();
        return;
      }
      const status = document.getElementById('formStatus');
      status.classList.add('visible');
      contactForm.reset();
      setTimeout(() => status.classList.remove('visible'), 6000);
    });
  }

});