/* =========================================================
   WeeDeliver — Application Script
   Vanilla JS only. Sections:
   1. Data (products, categories, testimonials, faq)
   2. State + localStorage persistence
   3. Utility helpers (currency, toast, ripple)
   4. Render functions (products, categories, testimonials, faq)
   5. Cart logic
   6. Wishlist logic
   7. Filters + sorting
   8. Search
   9. Modals (product, checkout)
   10. Overlays (cart, profile, mobile nav)
   11. Misc UI (navbar scroll, reveal, counters, back-to-top, preloader)
========================================================= */

(function () {
  'use strict';

  /* ======================= 1. DATA ======================= */

  const CATEGORIES = [
    { id: 'flowers',      name: 'Flowers',      desc: 'Sun-grown island buds',   icon: 'leaf' },
    { id: 'edibles',      name: 'Edibles',      desc: 'Infused island treats',   icon: 'sparkle' },
    { id: 'oils',         name: 'Oils',         desc: 'Tinctures & concentrates',icon: 'flask' },
    { id: 'vapes',        name: 'Vapes',        desc: 'Discreet, on the go',     icon: 'sparkle' },
    { id: 'prerolls',     name: 'Pre Rolls',    desc: 'Hand-rolled, ready fast', icon: 'leaf' },
    { id: 'accessories',  name: 'Accessories',  desc: 'Gear for the ritual',     icon: 'shield' }
  ];

  const PRODUCTS = [
    { id:'p1',  name:'Island Kush',            cat:'flowers',     price:2400, oldPrice:null, thc:24, cbd:1,  rating:4.8, reviews:142, desc:'A heavy-hitting indica with earthy pine notes and a deep body relaxation.', effects:['Relaxed','Sleepy','Euphoric'], flavor:'Earthy, Pine, Diesel', terpenes:'Myrcene, Caryophyllene', badge:'best', img:'island-kush', popularity:98, date:'2025-11-02' },
    { id:'p2',  name:"Jamaican Lamb's Bread",  cat:'flowers',     price:2600, oldPrice:2900, thc:22, cbd:1,  rating:4.9, reviews:201, desc:'The legendary Jamaican sativa — bright, uplifting and famously smooth.', effects:['Uplifted','Focused','Creative'], flavor:'Herbal, Citrus, Sweet', terpenes:'Limonene, Pinene', badge:'best', img:'lambs-bread', popularity:99, date:'2025-10-18' },
    { id:'p3',  name:'Blue Dream',             cat:'flowers',     price:2200, oldPrice:null, thc:19, cbd:1,  rating:4.7, reviews:167, desc:'Balanced hybrid delivering gentle cerebral invigoration with full-body calm.', effects:['Balanced','Happy','Relaxed'], flavor:'Blueberry, Sweet, Herbal', terpenes:'Myrcene, Pinene', badge:'new', img:'blue-dream', popularity:90, date:'2026-06-01' },
    { id:'p4',  name:'OG Kush',                cat:'flowers',     price:2500, oldPrice:null, thc:23, cbd:1,  rating:4.6, reviews:189, desc:'A West Coast classic with a fuel-forward nose and heavy euphoric effect.', effects:['Euphoric','Relaxed','Hungry'], flavor:'Fuel, Woody, Citrus', terpenes:'Limonene, Myrcene', badge:null, img:'og-kush', popularity:85, date:'2025-09-14' },
    { id:'p5',  name:'Purple Haze',            cat:'flowers',     price:2700, oldPrice:3100, thc:20, cbd:1,  rating:4.5, reviews:98,  desc:'Dreamy sativa with sweet berry tones and an energising, creative lift.', effects:['Energised','Creative','Uplifted'], flavor:'Berry, Sweet, Earthy', terpenes:'Terpinolene, Caryophyllene', badge:null, img:'purple-haze', popularity:78, date:'2025-08-22' },
    { id:'p6',  name:'Pineapple Express',      cat:'prerolls',    price:1200, oldPrice:null, thc:18, cbd:1,  rating:4.6, reviews:134, desc:'Tropical hybrid pre-roll bursting with pineapple sweetness, ready to spark.', effects:['Happy','Energised','Focused'], flavor:'Pineapple, Cedar, Tropical', terpenes:'Caryophyllene, Humulene', badge:'new', img:'pineapple-express', popularity:88, date:'2026-05-20' },
    { id:'p7',  name:'Gorilla Glue',           cat:'flowers',     price:2800, oldPrice:null, thc:26, cbd:1,  rating:4.9, reviews:222, desc:'Potent, sticky hybrid known for its heavy euphoria and pungent aroma.', effects:['Relaxed','Euphoric','Sleepy'], flavor:'Diesel, Chocolate, Earthy', terpenes:'Caryophyllene, Limonene', badge:'best', img:'gorilla-glue', popularity:97, date:'2025-07-11' },
    { id:'p8',  name:'Mango Haze',             cat:'vapes',       price:3200, oldPrice:3600, thc:82, cbd:0,  rating:4.4, reviews:76,  desc:'Full-spectrum vape cartridge with tropical mango sweetness and clear-headed lift.', effects:['Uplifted','Creative','Happy'], flavor:'Mango, Tropical, Sweet', terpenes:'Limonene, Ocimene', badge:null, img:'mango-haze', popularity:70, date:'2025-12-03' },
    { id:'p9',  name:'Wedding Cake',           cat:'flowers',     price:2900, oldPrice:null, thc:25, cbd:1,  rating:4.8, reviews:176, desc:'Rich, tangy hybrid with dense frosty buds and a relaxing, euphoric finish.', effects:['Relaxed','Euphoric','Happy'], flavor:'Vanilla, Earthy, Peppery', terpenes:'Limonene, Caryophyllene', badge:'organic', img:'wedding-cake', popularity:92, date:'2025-06-30' },
    { id:'p10', name:'Gelato',                 cat:'edibles',     price:1500, oldPrice:null, thc:10, cbd:2,  rating:4.5, reviews:112, desc:'Slow-melt infused gummies with a smooth dessert-like onset — 10mg per piece.', effects:['Relaxed','Happy','Calm'], flavor:'Berry, Citrus, Sweet', terpenes:'Linalool, Humulene', badge:'new', img:'gelato', popularity:82, date:'2026-04-15' },
    { id:'p11', name:'White Widow',            cat:'flowers',     price:2300, oldPrice:2600, thc:21, cbd:1,  rating:4.6, reviews:154, desc:'Classic resin-heavy hybrid balancing cerebral buzz with physical ease.', effects:['Euphoric','Creative','Relaxed'], flavor:'Woody, Spicy, Earthy', terpenes:'Myrcene, Pinene', badge:null, img:'white-widow', popularity:80, date:'2025-05-19' },
    { id:'p12', name:'Runtz',                  cat:'oils',        price:3600, oldPrice:null, thc:88, cbd:0,  rating:4.9, reviews:203, desc:'Live-resin tincture with candy-sweet terpenes for precise, fast-acting dosing.', effects:['Euphoric','Relaxed','Happy'], flavor:'Candy, Tropical, Sweet', terpenes:'Limonene, Caryophyllene', badge:'best', img:'runtz', popularity:95, date:'2025-04-02' }
  ];

  const TESTIMONIALS = [
    { name:'Amara Blake',   loc:'Kingston',    text:'The discretion and speed of delivery still amazes me. Island Kush is now my permanent go-to.', rating:5 },
    { name:'Marcus Reid',   loc:'Montego Bay',  text:"Every order has been exactly as described. The lab results actually match what's on the label.", rating:5 },
    { name:'Simone Clarke', loc:'Ocho Rios',    text:'Gelato edibles have the most consistent dosing I have tried anywhere on the island.', rating:4 },
    { name:'Devon Grant',   loc:'Negril',       text:"WeeDeliver's packaging alone feels premium — and the Lamb's Bread lives up to the legend.", rating:5 },
    { name:'Tanya Miller',  loc:'Spanish Town', text:'Rewards points actually add up to something. Great value for a regular customer like me.', rating:4 }
  ];

  const FAQS = [
    { q:'Is WeeDeliver a licensed cannabis retailer?', a:'Yes — WeeDeliver operates under full island cannabis licensing and is audited quarterly for compliance.' },
    { q:'How fast is delivery?', a:'Most orders within Kingston and Montego Bay arrive same-day. Other parishes typically receive orders within 24–48 hours.' },
    { q:'Are your products lab tested?', a:'Every batch is verified by an independent third-party lab for potency, pesticides and contaminants before listing.' },
    { q:'What payment methods do you accept?', a:'This demo supports M-Pesa, card, and cash-on-delivery selections at checkout — no real payments are processed.' },
    { q:'Do I need to verify my age?', a:'In a production version, age verification would be required at signup. This demo does not implement real verification.' },
    { q:'Can I track my order?', a:'Registered members can view order history and status from the Profile panel once logged in.' }
  ];

  const COUPONS = { 'ISLAND10': 0.10, 'GOLD15': 0.15 };
  const TAX_RATE = 0.16;
  const SHIPPING_FLAT = 300;
  const FREE_SHIPPING_THRESHOLD = 5000;

  /* ======================= 2. STATE ======================= */

  const state = {
    cart: loadJSON('wd_cart', []),          // [{id, qty}]
    wishlist: loadJSON('wd_wishlist', []),  // [id,...]
    appliedCoupon: null,
    filters: { category:'all', maxPrice:10000, minThc:0, minCbd:0 },
    sort: 'popularity',
    searchQuery: '',
    checkoutStep: 1,
    loggedIn: false,
    testimonialIndex: 0
  };

  function loadJSON(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) { return fallback; }
  }
  function saveJSON(key, val) {
    try { localStorage.setItem(key, JSON.stringify(val)); } catch (e) {}
  }

  /* ======================= 3. UTILITIES ======================= */

  function formatKSh(n) {
    return 'KSh ' + Math.round(n).toLocaleString('en-KE');
  }

  function findProduct(id) { return PRODUCTS.find(p => p.id === id); }

  function imgUrl(seed, w, h) {
    return `https://picsum.photos/seed/weedeliver-${seed}/${w}/${h}`;
  }

  function showToast(message, type = 'success') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 3200);
  }

  // Ripple effect for .ripple buttons
  document.addEventListener('click', function (e) {
    const btn = e.target.closest('.ripple');
    if (!btn) return;
    const rect = btn.getBoundingClientRect();
    const circle = document.createElement('span');
    const size = Math.max(rect.width, rect.height);
    circle.className = 'ripple-circle';
    circle.style.width = circle.style.height = size + 'px';
    circle.style.left = (e.clientX - rect.left - size / 2) + 'px';
    circle.style.top = (e.clientY - rect.top - size / 2) + 'px';
    btn.appendChild(circle);
    setTimeout(() => circle.remove(), 650);
  });

  function starIcons(rating, size = 14) {
    const full = Math.round(rating);
    let html = '';
    for (let i = 0; i < 5; i++) {
      html += `<svg style="width:${size}px;height:${size}px;opacity:${i < full ? 1 : 0.25}"><use href="#icon-star"></use></svg>`;
    }
    return html;
  }

  function badgeLabel(badge) {
    if (badge === 'new') return '<span class="p-badge new">New</span>';
    if (badge === 'best') return '<span class="p-badge best">Best Seller</span>';
    if (badge === 'organic') return '<span class="p-badge organic">Organic</span>';
    return '';
  }

  /* ======================= 4. RENDER: CATEGORIES ======================= */

  function renderCategories() {
    const grid = document.getElementById('categoryGrid');
    grid.innerHTML = CATEGORIES.map(cat => `
      <div class="category-card reveal" data-cat="${cat.id}">
        <div class="category-icon"><svg><use href="#leaf-icon"></use></svg></div>
        <h3>${cat.name}</h3>
        <p>${cat.desc}</p>
      </div>
    `).join('');

    grid.querySelectorAll('.category-card').forEach(card => {
      card.addEventListener('click', () => {
        document.getElementById('filterCategory').value = card.dataset.cat;
        state.filters.category = card.dataset.cat;
        document.getElementById('shop').scrollIntoView({ behavior: 'smooth' });
        renderProducts();
      });
    });

    observeReveals();
  }

  /* ======================= 4b. RENDER: PRODUCTS ======================= */

  function getCartQty(id) {
    const item = state.cart.find(c => c.id === id);
    return item ? item.qty : 0;
  }

  // Track per-card selector quantity (before adding to cart)
  const pendingQty = {};

  function applyFiltersAndSort(list) {
    const f = state.filters;
    let out = list.filter(p => {
      if (f.category !== 'all' && p.cat !== f.category) return false;
      if (p.price > f.maxPrice) return false;
      if (p.thc < f.minThc) return false;
      if (p.cbd < f.minCbd) return false;
      if (state.searchQuery) {
        const q = state.searchQuery.toLowerCase();
        if (!p.name.toLowerCase().includes(q) && !p.cat.toLowerCase().includes(q)) return false;
      }
      return true;
    });

    switch (state.sort) {
      case 'price-asc':  out.sort((a,b) => a.price - b.price); break;
      case 'price-desc': out.sort((a,b) => b.price - a.price); break;
      case 'rating':     out.sort((a,b) => b.rating - a.rating); break;
      case 'bestselling':out.sort((a,b) => b.reviews - a.reviews); break;
      case 'newest':     out.sort((a,b) => new Date(b.date) - new Date(a.date)); break;
      default:            out.sort((a,b) => b.popularity - a.popularity);
    }
    return out;
  }

  function productCardHTML(p) {
    const isFav = state.wishlist.includes(p.id);
    const qty = pendingQty[p.id] || 1;
    return `
    <article class="product-card reveal in" data-id="${p.id}">
      <div class="product-media" data-action="open-modal">
        <img src="${imgUrl(p.img, 500, 450)}" alt="${p.name}" loading="lazy">
        <div class="product-badges">${badgeLabel(p.badge)}</div>
        ${p.oldPrice ? `<div class="discount-seal"><span>${Math.round(100 - (p.price / p.oldPrice) * 100)}%</span><small>Off</small></div>` : ''}
        <button class="fav-btn ${isFav ? 'active' : ''}" data-action="fav" aria-label="Toggle wishlist">
          <svg><use href="#icon-heart"></use></svg>
        </button>
      </div>
      <div class="product-info">
        <span class="product-cat">${p.cat}</span>
        <h3 class="product-name" data-action="open-modal">${p.name}</h3>
        <div class="product-meta">
          <span class="meta-pill thc">THC ${p.thc}%</span>
          <span class="meta-pill cbd">CBD ${p.cbd}%</span>
        </div>
        <div class="product-rating">${starIcons(p.rating)} <span>${p.rating} (${p.reviews})</span></div>
        <p class="product-desc">${p.desc}</p>
        <div class="product-footer">
          <div class="product-price">${formatKSh(p.price)}${p.oldPrice ? `<span class="old-price">${formatKSh(p.oldPrice)}</span>` : ''}</div>
          <div class="qty-selector" data-qty-for="${p.id}">
            <button data-action="qty-dec"><svg><use href="#icon-minus"></use></svg></button>
            <span class="qty-val">${qty}</span>
            <button data-action="qty-inc"><svg><use href="#icon-plus"></use></svg></button>
          </div>
        </div>
        <button class="add-cart-btn ripple" data-action="add-cart">
          <svg><use href="#icon-cart"></use></svg> Add to Cart
        </button>
      </div>
    </article>`;
  }

  function renderProducts() {
    const grid = document.getElementById('productGrid');
    const empty = document.getElementById('emptyState');
    const list = applyFiltersAndSort(PRODUCTS);

    document.getElementById('resultsCount').textContent = `Showing ${list.length} of ${PRODUCTS.length} products`;

    if (!list.length) {
      grid.innerHTML = '';
      empty.hidden = false;
      return;
    }
    empty.hidden = true;
    grid.innerHTML = list.map(productCardHTML).join('');
  }

  // Delegated events for product grid
  document.addEventListener('click', function (e) {
    const grid = document.getElementById('productGrid');
    if (!grid) return;
    const card = e.target.closest('.product-card');
    if (!card || !grid.contains(card)) return;
    const id = card.dataset.id;
    const action = e.target.closest('[data-action]')?.dataset.action;

    if (action === 'open-modal') openProductModal(id);
    if (action === 'fav') toggleWishlist(id, e.target.closest('.fav-btn'));
    if (action === 'qty-inc') { pendingQty[id] = (pendingQty[id] || 1) + 1; updateQtyDisplay(card, pendingQty[id]); }
    if (action === 'qty-dec') { pendingQty[id] = Math.max(1, (pendingQty[id] || 1) - 1); updateQtyDisplay(card, pendingQty[id]); }
    if (action === 'add-cart') addToCart(id, pendingQty[id] || 1);
  });

  function updateQtyDisplay(card, val) {
    card.querySelector('.qty-val').textContent = val;
  }

  /* ======================= 5. CART LOGIC ======================= */

  function addToCart(id, qty = 1) {
    const existing = state.cart.find(c => c.id === id);
    if (existing) existing.qty += qty;
    else state.cart.push({ id, qty });
    saveJSON('wd_cart', state.cart);
    renderCartBadge();
    renderCart();
    const p = findProduct(id);
    showToast(`${p.name} added to cart`, 'success');
    pulseCartIcon();
  }

  function removeFromCart(id) {
    const p = findProduct(id);
    state.cart = state.cart.filter(c => c.id !== id);
    saveJSON('wd_cart', state.cart);
    renderCartBadge();
    renderCart();
    showToast(`${p.name} removed from cart`, 'info');
  }

  function changeCartQty(id, delta) {
    const item = state.cart.find(c => c.id === id);
    if (!item) return;
    item.qty += delta;
    if (item.qty <= 0) { removeFromCart(id); return; }
    saveJSON('wd_cart', state.cart);
    renderCartBadge();
    renderCart();
  }

  function cartSubtotal() {
    return state.cart.reduce((sum, c) => sum + findProduct(c.id).price * c.qty, 0);
  }

  function pulseCartIcon() {
    const btn = document.getElementById('cartToggle');
    btn.style.transform = 'scale(1.15)';
    setTimeout(() => btn.style.transform = '', 220);
  }

  function renderCartBadge() {
    const count = state.cart.reduce((s, c) => s + c.qty, 0);
    const el = document.getElementById('cartCount');
    el.textContent = count;
    el.classList.toggle('show', count > 0);
  }

  function renderCart() {
    const itemsWrap = document.getElementById('cartItems');
    const empty = document.getElementById('cartEmpty');
    const footer = document.getElementById('cartFooter');
    const label = document.getElementById('cartItemsLabel');

    const totalItems = state.cart.reduce((s, c) => s + c.qty, 0);
    label.textContent = `(${totalItems} item${totalItems !== 1 ? 's' : ''})`;

    if (!state.cart.length) {
      itemsWrap.innerHTML = '';
      empty.style.display = 'flex';
      footer.hidden = true;
      return;
    }
    empty.style.display = 'none';
    footer.hidden = false;

    itemsWrap.innerHTML = state.cart.map(c => {
      const p = findProduct(c.id);
      return `
      <div class="cart-item" data-id="${p.id}">
        <img src="${imgUrl(p.img, 120, 120)}" alt="${p.name}">
        <div class="cart-item-info">
          <span class="cart-item-name">${p.name}</span>
          <span class="cart-item-price">${formatKSh(p.price * c.qty)}</span>
          <div class="cart-item-row">
            <div class="qty-selector">
              <button data-action="cart-dec"><svg><use href="#icon-minus"></use></svg></button>
              <span class="qty-val">${c.qty}</span>
              <button data-action="cart-inc"><svg><use href="#icon-plus"></use></svg></button>
            </div>
            <button class="cart-item-remove" data-action="cart-remove">Remove</button>
          </div>
        </div>
      </div>`;
    }).join('');

    renderSummary();
  }

  function renderSummary() {
    const subtotal = cartSubtotal();
    let discount = 0;
    if (state.appliedCoupon && COUPONS[state.appliedCoupon]) {
      discount = subtotal * COUPONS[state.appliedCoupon];
    }
    const afterDiscount = subtotal - discount;
    const shipping = state.cart.length === 0 ? 0 : (afterDiscount >= FREE_SHIPPING_THRESHOLD ? 0 : SHIPPING_FLAT);
    const tax = afterDiscount * TAX_RATE;
    const total = afterDiscount + shipping + tax;

    document.getElementById('sumSubtotal').textContent = formatKSh(subtotal);
    document.getElementById('sumShipping').textContent = shipping === 0 ? 'Free' : formatKSh(shipping);
    document.getElementById('sumTax').textContent = formatKSh(tax);
    document.getElementById('sumTotal').textContent = formatKSh(total);

    const discRow = document.getElementById('sumDiscountRow');
    if (discount > 0) {
      discRow.hidden = false;
      document.getElementById('sumDiscount').textContent = '-' + formatKSh(discount);
    } else {
      discRow.hidden = true;
    }
    return { subtotal, discount, shipping, tax, total };
  }

  document.getElementById('cartItems').addEventListener('click', function (e) {
    const item = e.target.closest('.cart-item');
    if (!item) return;
    const id = item.dataset.id;
    const action = e.target.closest('[data-action]')?.dataset.action;
    if (action === 'cart-inc') changeCartQty(id, 1);
    if (action === 'cart-dec') changeCartQty(id, -1);
    if (action === 'cart-remove') removeFromCart(id);
  });

  document.getElementById('applyCoupon').addEventListener('click', function () {
    const code = document.getElementById('couponInput').value.trim().toUpperCase();
    const msg = document.getElementById('couponMsg');
    if (COUPONS[code]) {
      state.appliedCoupon = code;
      msg.textContent = `Coupon applied — ${Math.round(COUPONS[code] * 100)}% off!`;
      msg.classList.remove('error');
      showToast('Coupon applied', 'success');
    } else {
      state.appliedCoupon = null;
      msg.textContent = 'Invalid coupon code.';
      msg.classList.add('error');
    }
    renderSummary();
  });

  /* ======================= 6. WISHLIST ======================= */

  function toggleWishlist(id, btnEl) {
    const p = findProduct(id);
    const idx = state.wishlist.indexOf(id);
    if (idx > -1) {
      state.wishlist.splice(idx, 1);
      showToast(`${p.name} removed from wishlist`, 'info');
    } else {
      state.wishlist.push(id);
      showToast(`${p.name} added to wishlist`, 'success');
    }
    saveJSON('wd_wishlist', state.wishlist);
    if (btnEl) btnEl.classList.toggle('active', state.wishlist.includes(id));
    renderWishlistBadge();
  }

  function renderWishlistBadge() {
    const el = document.getElementById('wishlistCount');
    el.textContent = state.wishlist.length;
    el.classList.toggle('show', state.wishlist.length > 0);
    const pw = document.getElementById('profileWishlistCount');
    if (pw) pw.textContent = `${state.wishlist.length} item${state.wishlist.length !== 1 ? 's' : ''} saved`;
  }

  /* ======================= 7. FILTERS + SORT ======================= */

  const filterCategory = document.getElementById('filterCategory');
  const filterPrice = document.getElementById('filterPrice');
  const filterThc = document.getElementById('filterThc');
  const filterCbd = document.getElementById('filterCbd');
  const sortBy = document.getElementById('sortBy');

  filterCategory.addEventListener('change', () => { state.filters.category = filterCategory.value; renderProducts(); });
  filterPrice.addEventListener('input', () => {
    state.filters.maxPrice = Number(filterPrice.value);
    document.getElementById('priceVal').textContent = formatKSh(filterPrice.value);
    renderProducts();
  });
  filterThc.addEventListener('input', () => {
    state.filters.minThc = Number(filterThc.value);
    document.getElementById('thcVal').textContent = filterThc.value + '%';
    renderProducts();
  });
  filterCbd.addEventListener('input', () => {
    state.filters.minCbd = Number(filterCbd.value);
    document.getElementById('cbdVal').textContent = filterCbd.value + '%';
    renderProducts();
  });
  sortBy.addEventListener('change', () => { state.sort = sortBy.value; renderProducts(); });

  document.getElementById('resetFilters').addEventListener('click', () => {
    state.filters = { category:'all', maxPrice:10000, minThc:0, minCbd:0 };
    state.sort = 'popularity';
    state.searchQuery = '';
    filterCategory.value = 'all';
    filterPrice.value = 10000;
    filterThc.value = 0;
    filterCbd.value = 0;
    sortBy.value = 'popularity';
    document.getElementById('priceVal').textContent = 'KSh 10,000';
    document.getElementById('thcVal').textContent = '0%';
    document.getElementById('cbdVal').textContent = '0%';
    renderProducts();
  });

  /* ======================= 8. SEARCH ======================= */

  const searchToggle = document.getElementById('searchToggle');
  const searchBar = document.getElementById('searchBar');
  const searchInput = document.getElementById('searchInput');
  const searchClose = document.getElementById('searchClose');
  const searchResults = document.getElementById('searchResults');

  searchToggle.addEventListener('click', () => {
    searchBar.classList.add('open');
    setTimeout(() => searchInput.focus(), 300);
  });
  searchClose.addEventListener('click', () => searchBar.classList.remove('open'));

  searchInput.addEventListener('input', () => {
    const q = searchInput.value.trim().toLowerCase();
    if (!q) { searchResults.innerHTML = ''; return; }
    const matches = PRODUCTS.filter(p => p.name.toLowerCase().includes(q) || p.cat.toLowerCase().includes(q)).slice(0, 6);
    if (!matches.length) {
      searchResults.innerHTML = `<p class="search-empty">No products match "${searchInput.value}".</p>`;
      return;
    }
    searchResults.innerHTML = matches.map(p => `
      <a class="search-result-item" data-id="${p.id}">
        <img src="${imgUrl(p.img, 100, 100)}" alt="${p.name}">
        <span class="sri-name">${p.name}</span>
        <span class="sri-price">${formatKSh(p.price)}</span>
      </a>
    `).join('');
  });

  searchResults.addEventListener('click', (e) => {
    const item = e.target.closest('.search-result-item');
    if (!item) return;
    searchBar.classList.remove('open');
    openProductModal(item.dataset.id);
  });

  // Also wire the toolbar search into main filter (optional live sync)
  searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      state.searchQuery = searchInput.value.trim();
      searchBar.classList.remove('open');
      document.getElementById('shop').scrollIntoView({ behavior: 'smooth' });
      renderProducts();
    }
  });

  /* ======================= 9. PRODUCT MODAL ======================= */

  const productModal = document.getElementById('productModal');
  const productModalContent = document.getElementById('productModalContent');
  let modalQty = 1;

  const MOCK_REVIEWS = [
    { name:'K. Thompson', rating:5, text:'Exactly as described — potent and smooth. Fast delivery too.' },
    { name:'R. James', rating:4, text:'Great flavor profile, slightly harsher than expected but still excellent.' },
    { name:'A. Campbell', rating:5, text:'My go-to order every time. Consistent quality batch after batch.' }
  ];

  function openProductModal(id) {
    const p = findProduct(id);
    modalQty = 1;
    const isFav = state.wishlist.includes(id);

    productModalContent.innerHTML = `
      <div class="pm-media"><img src="${imgUrl(p.img, 700, 700)}" alt="${p.name}"></div>
      <div class="pm-info">
        <span class="pm-cat">${p.cat}</span>
        <h2 class="pm-name">${p.name}</h2>
        <div class="pm-rating">${starIcons(p.rating, 15)} <span>${p.rating} · ${p.reviews} reviews</span></div>
        <p class="pm-desc">${p.desc}</p>

        <div class="pm-detail-grid">
          <div class="pm-detail"><label>THC</label><span>${p.thc}%</span></div>
          <div class="pm-detail"><label>CBD</label><span>${p.cbd}%</span></div>
          <div class="pm-detail"><label>Effects</label><span>${p.effects.join(', ')}</span></div>
          <div class="pm-detail"><label>Flavor</label><span>${p.flavor}</span></div>
          <div class="pm-detail" style="grid-column:1/-1"><label>Terpenes</label><span>${p.terpenes}</span></div>
        </div>

        <div class="pm-price-row">
          <span class="pm-price">${formatKSh(p.price)}</span>
          <div class="qty-selector" id="modalQtySelector">
            <button data-action="modal-qty-dec"><svg><use href="#icon-minus"></use></svg></button>
            <span class="qty-val" id="modalQtyVal">1</span>
            <button data-action="modal-qty-inc"><svg><use href="#icon-plus"></use></svg></button>
          </div>
        </div>

        <div class="pm-actions">
          <button class="add-cart-btn ripple" style="flex:1" id="modalAddCart"><svg><use href="#icon-cart"></use></svg> Add to Cart</button>
          <button class="fav-btn ${isFav ? 'active' : ''}" id="modalFavBtn" style="position:static"><svg><use href="#icon-heart"></use></svg></button>
        </div>

        <div class="pm-reviews">
          <h4>Customer Reviews</h4>
          ${MOCK_REVIEWS.map(r => `
            <div class="pm-review">
              <div class="pm-review-head"><span>${r.name}</span><span>${starIcons(r.rating, 12)}</span></div>
              <p>${r.text}</p>
            </div>
          `).join('')}
        </div>
      </div>
    `;

    document.getElementById('modalQtyVal').textContent = modalQty;
    productModalContent.querySelector('[data-action="modal-qty-inc"]').addEventListener('click', () => {
      modalQty++; document.getElementById('modalQtyVal').textContent = modalQty;
    });
    productModalContent.querySelector('[data-action="modal-qty-dec"]').addEventListener('click', () => {
      modalQty = Math.max(1, modalQty - 1); document.getElementById('modalQtyVal').textContent = modalQty;
    });
    document.getElementById('modalAddCart').addEventListener('click', () => {
      addToCart(p.id, modalQty);
    });
    document.getElementById('modalFavBtn').addEventListener('click', (e) => {
      toggleWishlist(p.id, e.currentTarget);
    });

    productModal.classList.add('open');
    productModal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeProductModal() {
    productModal.classList.remove('open');
    productModal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }
  document.getElementById('productModalClose').addEventListener('click', closeProductModal);
  productModal.addEventListener('click', (e) => { if (e.target === productModal) closeProductModal(); });

  /* ======================= 10. OVERLAYS: CART / PROFILE / MOBILE NAV ======================= */

  const cartOverlay = document.getElementById('cartOverlay');
  const profileOverlay = document.getElementById('profileOverlay');
  const mobileNav = document.getElementById('mobileNav');
  const backdrop = document.getElementById('overlayBackdrop');
  const mobileNavBackdrop = document.getElementById('mobileNavBackdrop');

  function openOverlay(el) {
    closeAllOverlays();
    el.classList.add('open');
    el.setAttribute('aria-hidden', 'false');
    backdrop.classList.add('show');
    document.body.style.overflow = 'hidden';
  }
  function closeAllOverlays() {
    [cartOverlay, profileOverlay].forEach(el => { el.classList.remove('open'); el.setAttribute('aria-hidden', 'true'); });
    backdrop.classList.remove('show');
    document.body.style.overflow = '';
  }

  document.getElementById('cartToggle').addEventListener('click', () => openOverlay(cartOverlay));
  document.getElementById('cartClose').addEventListener('click', closeAllOverlays);
  document.getElementById('continueShopping').addEventListener('click', closeAllOverlays);
  document.getElementById('cartEmptyShop').addEventListener('click', () => {
    closeAllOverlays();
    document.getElementById('shop').scrollIntoView({ behavior: 'smooth' });
  });

  document.getElementById('profileToggle').addEventListener('click', () => openOverlay(profileOverlay));
  document.getElementById('profileClose').addEventListener('click', closeAllOverlays);

  backdrop.addEventListener('click', closeAllOverlays);

  // Mobile nav
  const hamburger = document.getElementById('hamburger');
  hamburger.addEventListener('click', () => {
    const isOpen = mobileNav.classList.toggle('open');
    hamburger.classList.toggle('active', isOpen);
    mobileNavBackdrop.classList.toggle('show', isOpen);
    document.body.style.overflow = isOpen ? 'hidden' : '';
  });
  mobileNavBackdrop.addEventListener('click', () => {
    mobileNav.classList.remove('open');
    hamburger.classList.remove('active');
    mobileNavBackdrop.classList.remove('show');
    document.body.style.overflow = '';
  });
  mobileNav.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      mobileNav.classList.remove('open');
      hamburger.classList.remove('active');
      mobileNavBackdrop.classList.remove('show');
      document.body.style.overflow = '';
    });
  });

  // Profile: login / register open the auth modal
  const authModal = document.getElementById('authModal');
  const authTabs = document.querySelectorAll('.auth-tab');
  const authPanels = document.querySelectorAll('.auth-panel');

  function openAuthModal(mode) {
    closeAllOverlays();
    setAuthTab(mode);
    authModal.classList.add('open');
    authModal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }
  function closeAuthModal() {
    authModal.classList.remove('open');
    authModal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }
  function setAuthTab(mode) {
    authTabs.forEach(t => t.classList.toggle('active', t.dataset.tab === mode));
    authPanels.forEach(p => p.classList.toggle('active', p.dataset.panel === mode));
  }

  document.getElementById('loginBtn').addEventListener('click', () => openAuthModal('login'));
  document.getElementById('registerBtn').addEventListener('click', () => openAuthModal('register'));
  document.getElementById('authModalClose').addEventListener('click', closeAuthModal);
  authModal.addEventListener('click', (e) => { if (e.target === authModal) closeAuthModal(); });

  authTabs.forEach(tab => tab.addEventListener('click', () => setAuthTab(tab.dataset.tab)));
  document.querySelectorAll('[data-switch]').forEach(link => {
    link.addEventListener('click', (e) => { e.preventDefault(); setAuthTab(link.dataset.switch); });
  });

  document.getElementById('loginForm').addEventListener('submit', (e) => {
    e.preventDefault();
    closeAuthModal();
    mockLogin();
  });
  document.getElementById('registerForm').addEventListener('submit', (e) => {
    e.preventDefault();
    closeAuthModal();
    mockLogin();
    showToast('Account created — welcome to WeeDeliver!', 'success');
  });

  function mockLogin() {
    state.loggedIn = true;
    document.getElementById('profileGuest').hidden = true;
    document.getElementById('profileAccount').hidden = false;
    renderWishlistBadge();
    showToast('Welcome back, Amara!', 'success');
  }
  document.getElementById('logoutBtn').addEventListener('click', () => {
    state.loggedIn = false;
    document.getElementById('profileGuest').hidden = false;
    document.getElementById('profileAccount').hidden = true;
    showToast('Logged out', 'info');
  });
  document.getElementById('settingsBtn').addEventListener('click', () => showToast('Settings — demo only', 'info'));

  /* ======================= 11. CHECKOUT MODAL ======================= */

  const checkoutModal = document.getElementById('checkoutModal');
  const checkoutForm = document.getElementById('checkoutForm');
  const checkoutSuccess = document.getElementById('checkoutSuccess');

  document.getElementById('checkoutBtn').addEventListener('click', () => {
    if (!state.cart.length) return;
    closeAllOverlays();
    openCheckout();
  });

  function openCheckout() {
    state.checkoutStep = 1;
    updateCheckoutStepUI();
    checkoutForm.hidden = false;
    checkoutSuccess.hidden = true;
    checkoutModal.classList.add('open');
    checkoutModal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }
  function closeCheckout() {
    checkoutModal.classList.remove('open');
    checkoutModal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }
  document.getElementById('checkoutModalClose').addEventListener('click', closeCheckout);
  checkoutModal.addEventListener('click', (e) => { if (e.target === checkoutModal) closeCheckout(); });

  function updateCheckoutStepUI() {
    document.querySelectorAll('.checkout-steps .step').forEach(s => {
      s.classList.toggle('active', Number(s.dataset.step) === state.checkoutStep);
    });
    document.querySelectorAll('.checkout-panel').forEach(p => {
      p.hidden = Number(p.dataset.panel) !== state.checkoutStep;
    });
    if (state.checkoutStep === 3) renderCheckoutSummary();
  }

  function renderCheckoutSummary() {
    const { subtotal, discount, shipping, tax, total } = renderSummary();
    const wrap = document.getElementById('checkoutSummary');
    wrap.innerHTML = `
      ${state.cart.map(c => {
        const p = findProduct(c.id);
        return `<div class="summary-row"><span>${p.name} × ${c.qty}</span><span>${formatKSh(p.price * c.qty)}</span></div>`;
      }).join('')}
      <div class="summary-row"><span>Subtotal</span><span>${formatKSh(subtotal)}</span></div>
      ${discount > 0 ? `<div class="summary-row"><span>Discount</span><span>-${formatKSh(discount)}</span></div>` : ''}
      <div class="summary-row"><span>Delivery</span><span>${shipping === 0 ? 'Free' : formatKSh(shipping)}</span></div>
      <div class="summary-row"><span>Tax (16% VAT)</span><span>${formatKSh(tax)}</span></div>
      <div class="summary-row total-row"><span>Total</span><span>${formatKSh(total)}</span></div>
    `;
  }

  document.querySelectorAll('.checkout-next').forEach(btn => {
    btn.addEventListener('click', () => {
      const panel = btn.closest('.checkout-panel');
      const inputs = panel.querySelectorAll('input[required]');
      for (const inp of inputs) { if (!inp.value) { inp.focus(); return; } }
      state.checkoutStep = Math.min(3, state.checkoutStep + 1);
      updateCheckoutStepUI();
    });
  });
  document.querySelectorAll('.checkout-back').forEach(btn => {
    btn.addEventListener('click', () => {
      state.checkoutStep = Math.max(1, state.checkoutStep - 1);
      updateCheckoutStepUI();
    });
  });

  checkoutForm.addEventListener('submit', (e) => {
    e.preventDefault();
    checkoutForm.hidden = true;
    checkoutSuccess.hidden = false;
    state.cart = [];
    state.appliedCoupon = null;
    saveJSON('wd_cart', state.cart);
    renderCartBadge();
    renderCart();
    showToast('Order placed (demo)', 'success');
  });

  document.getElementById('checkoutDone').addEventListener('click', closeCheckout);

  /* ======================= 12. TESTIMONIAL CAROUSEL ======================= */

  function renderTestimonials() {
    const track = document.getElementById('testimonialTrack');
    const dots = document.getElementById('testimonialDots');
    track.innerHTML = TESTIMONIALS.map(t => `
      <div class="testimonial-slide">
        <div class="testimonial-card">
          <div class="testimonial-stars">${starIcons(t.rating, 16)}</div>
          <p class="testimonial-quote">"${t.text}"</p>
          <div class="testimonial-author">
            <div class="testimonial-avatar">${t.name.split(' ').map(n => n[0]).join('')}</div>
            <div>
              <div class="testimonial-author-name">${t.name}</div>
              <div class="testimonial-author-loc">${t.loc}, Jamaica</div>
            </div>
          </div>
        </div>
      </div>
    `).join('');
    dots.innerHTML = TESTIMONIALS.map((_, i) => `<span data-i="${i}" class="${i === 0 ? 'active' : ''}"></span>`).join('');
    updateTestimonialPos();

    dots.querySelectorAll('span').forEach(dot => {
      dot.addEventListener('click', () => { state.testimonialIndex = Number(dot.dataset.i); updateTestimonialPos(); });
    });
  }

  function updateTestimonialPos() {
    const track = document.getElementById('testimonialTrack');
    track.style.transform = `translateX(-${state.testimonialIndex * 100}%)`;
    document.querySelectorAll('#testimonialDots span').forEach((d, i) => d.classList.toggle('active', i === state.testimonialIndex));
  }

  document.getElementById('testimonialNext').addEventListener('click', () => {
    state.testimonialIndex = (state.testimonialIndex + 1) % TESTIMONIALS.length;
    updateTestimonialPos();
  });
  document.getElementById('testimonialPrev').addEventListener('click', () => {
    state.testimonialIndex = (state.testimonialIndex - 1 + TESTIMONIALS.length) % TESTIMONIALS.length;
    updateTestimonialPos();
  });

  // Auto-advance
  setInterval(() => {
    state.testimonialIndex = (state.testimonialIndex + 1) % TESTIMONIALS.length;
    updateTestimonialPos();
  }, 6000);

  /* ======================= 13. FAQ ACCORDION ======================= */

  function renderFAQ() {
    const list = document.getElementById('faqList');
    list.innerHTML = FAQS.map((f, i) => `
      <div class="faq-item reveal" data-i="${i}">
        <button class="faq-question">
          ${f.q}
          <svg><use href="#icon-chevron"></use></svg>
        </button>
        <div class="faq-answer"><div class="faq-answer-inner">${f.a}</div></div>
      </div>
    `).join('');

    list.querySelectorAll('.faq-item').forEach(item => {
      const question = item.querySelector('.faq-question');
      const answer = item.querySelector('.faq-answer');
      question.addEventListener('click', () => {
        const isOpen = item.classList.contains('open');
        list.querySelectorAll('.faq-item').forEach(other => {
          other.classList.remove('open');
          other.querySelector('.faq-answer').style.maxHeight = null;
        });
        if (!isOpen) {
          item.classList.add('open');
          answer.style.maxHeight = answer.scrollHeight + 'px';
        }
      });
    });
    observeReveals();
  }

  /* ======================= 14. NEWSLETTER ======================= */

  document.getElementById('newsletterForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const email = document.getElementById('newsletterEmail').value;
    if (!email) return;
    showToast('Subscribed! Welcome to the inner circle.', 'success');
    e.target.reset();
  });

  /* ======================= 15. NAVBAR SCROLL + ACTIVE LINK ======================= */

  const navbar = document.getElementById('navbar');
  const sections = ['home','shop','categories','about','faq','contact'];

  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 40);

    // back to top
    document.getElementById('backToTop').classList.toggle('show', window.scrollY > 600);

    // active nav link
    let current = 'home';
    sections.forEach(id => {
      const el = document.getElementById(id);
      if (el && window.scrollY >= el.offsetTop - 140) current = id;
    });
    document.querySelectorAll('.nav-link').forEach(link => {
      link.classList.toggle('active', link.getAttribute('href') === '#' + current);
    });
  }, { passive: true });

  document.getElementById('backToTop').addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  /* ======================= 16. SCROLL REVEAL ======================= */

  let revealObserver;
  function observeReveals() {
    if (!revealObserver) {
      revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('in');
            revealObserver.unobserve(entry.target);
          }
        });
      }, { threshold: 0.15 });
    }
    document.querySelectorAll('.reveal:not(.in)').forEach(el => revealObserver.observe(el));
  }

  /* ======================= 17. ANIMATED COUNTERS ======================= */

  function animateCounters() {
    const counters = document.querySelectorAll('.stat-num');
    const counterObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const target = Number(el.dataset.count);
        const duration = 1600;
        const start = performance.now();
        function tick(now) {
          const progress = Math.min((now - start) / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 3);
          el.textContent = Math.round(eased * target).toLocaleString();
          if (progress < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
        counterObserver.unobserve(el);
      });
    }, { threshold: 0.4 });
    counters.forEach(c => counterObserver.observe(c));
  }

  /* ======================= 18. INIT ======================= */

  function init() {
    document.getElementById('year').textContent = new Date().getFullYear();

    renderCategories();
    renderProducts();
    renderTestimonials();
    renderFAQ();
    renderCartBadge();
    renderWishlistBadge();
    renderCart();
    animateCounters();
    observeReveals();

    // Preloader
    window.addEventListener('load', () => {
      setTimeout(() => document.getElementById('preloader').classList.add('hide'), 400);
    });
    // fallback in case load already fired
    setTimeout(() => document.getElementById('preloader').classList.add('hide'), 1800);

    // Escape key closes overlays/modals
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeAllOverlays();
        closeProductModal();
        closeCheckout();
        closeAuthModal();
        searchBar.classList.remove('open');
        mobileNav.classList.remove('open');
        hamburger.classList.remove('active');
        mobileNavBackdrop.classList.remove('show');
      }
    });
  }

  document.addEventListener('DOMContentLoaded', init);
})();
