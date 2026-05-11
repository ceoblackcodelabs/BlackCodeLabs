/* ============================================
   AngelTech Computers - Main JavaScript
   Includes: Carousel, Chatbot, Cart System (localStorage), Product Filters, Modals
   ============================================ */

// ========== PRELOADER ==========
window.addEventListener('load', () => {
  const preloader = document.getElementById('preloader');
  if (preloader) {
    setTimeout(() => {
      preloader.style.opacity = '0';
      setTimeout(() => {
        preloader.style.display = 'none';
      }, 500);
    }, 500);
  }
  initAOS();
});

// ========== STICKY NAVBAR ==========
const navbar = document.getElementById('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }

    // Back to top button
    const backTop = document.getElementById('backToTop');
    if (backTop) {
      if (window.scrollY > 600) {
        backTop.classList.add('show');
      } else {
        backTop.classList.remove('show');
      }
    }
  });
}

// ========== HAMBURGER MENU ==========
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');
if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('active');
  });

  document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('active');
    });
  });
}

// ========== HERO CAROUSEL ==========
const slides = document.querySelectorAll('.carousel-slide');
if (slides.length > 0) {
  let currentSlide = 0;
  function nextSlide() {
    slides[currentSlide].classList.remove('active');
    currentSlide = (currentSlide + 1) % slides.length;
    slides[currentSlide].classList.add('active');
  }
  setInterval(nextSlide, 5000);
}

// ========== FLOATING PARTICLES ==========
const particlesContainer = document.getElementById('particles');
if (particlesContainer) {
  for (let i = 0; i < 50; i++) {
    const particle = document.createElement('div');
    particle.classList.add('particle');
    const size = Math.random() * 6 + 2;
    particle.style.width = size + 'px';
    particle.style.height = size + 'px';
    particle.style.left = Math.random() * 100 + '%';
    particle.style.top = Math.random() * 100 + '%';
    particle.style.animationDelay = Math.random() * 10 + 's';
    particle.style.animationDuration = 8 + Math.random() * 8 + 's';
    particlesContainer.appendChild(particle);
  }
}

// ========== CONTACT FORM VALIDATION ==========
const contactForm = document.getElementById('contactForm');
if (contactForm) {
  contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = document.getElementById('name')?.value.trim();
    const email = document.getElementById('email')?.value.trim();
    const phone = document.getElementById('phone')?.value.trim();
    const message = document.getElementById('message')?.value.trim();

    if (!name || !email || !phone || !message) {
      alert('Please fill in all fields');
      return;
    }
    if (!/^\S+@\S+\.\S+$/.test(email)) {
      alert('Please enter a valid email address');
      return;
    }
    if (!/^[\d\+\-\(\) ]{10,}$/.test(phone)) {
      alert('Please enter a valid phone number');
      return;
    }

    alert(`Thank you ${name}! We'll get back to you soon.`);
    contactForm.reset();
  });
}

// ========== NEWSLETTER SUBSCRIPTION ==========
const newsBtn = document.getElementById('newsBtn');
if (newsBtn) {
  newsBtn.addEventListener('click', () => {
    const email = document.getElementById('newsEmail')?.value.trim();
    if (email && email.includes('@') && email.includes('.')) {
      alert(`🎉 Subscribed! ${email} will receive tech updates.`);
      document.getElementById('newsEmail').value = '';
    } else {
      alert('Please enter a valid email address');
    }
  });
}

// ========== BACK TO TOP ==========
const backTop = document.getElementById('backToTop');
if (backTop) {
  backTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// ========== WHATSAPP FLOATING BUTTON ==========
const waBtn = document.getElementById('waBtn');
if (waBtn) {
  waBtn.addEventListener('click', () => {
    const message = encodeURIComponent('Hello AngelTech Computers, I would like to inquire about your products.');
    window.open(`https://wa.me/1234567890?text=${message}`, '_blank');
  });
}

// ========== CHATBOT ==========
const chatBtn = document.getElementById('chatBtn');
const chatModal = document.getElementById('chatModal');
const closeChat = document.getElementById('closeChat');
const sendChatMsg = document.getElementById('sendChatMsg');
const chatInput = document.getElementById('chatInput');
const chatBody = document.getElementById('chatBody');

if (chatBtn && chatModal) {
  chatBtn.addEventListener('click', () => {
    chatModal.style.display = 'flex';
  });

  if (closeChat) {
    closeChat.addEventListener('click', () => {
      chatModal.style.display = 'none';
    });
  }

  function addBotMessage(text) {
    const div = document.createElement('div');
    div.className = 'bot-message';
    div.innerHTML = text;
    chatBody.appendChild(div);
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  function addUserMessage(text) {
    const div = document.createElement('div');
    div.className = 'user-message';
    div.innerHTML = text;
    chatBody.appendChild(div);
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  const botResponses = {
    default: "Thanks for reaching out! Our tech team will assist you shortly. For immediate help, call +1 (800) 123-4567.",
    price: "Our products range from $12 for accessories up to $2500 for premium gaming laptops. Check our shop for current deals! 🚀",
    shipping: "We offer free shipping on orders over $99. Standard delivery takes 3-5 business days.",
    warranty: "All products come with a minimum 1-year manufacturer warranty. Extended warranty options available at checkout.",
    return: "You can return items within 30 days of purchase for a full refund. Product must be in original condition."
  };

  function getBotReply(question) {
    const q = question.toLowerCase();
    if (q.includes('price') || q.includes('cost') || q.includes('how much')) return botResponses.price;
    if (q.includes('shipping') || q.includes('delivery')) return botResponses.shipping;
    if (q.includes('warranty')) return botResponses.warranty;
    if (q.includes('return') || q.includes('refund')) return botResponses.return;
    return botResponses.default;
  }

  if (sendChatMsg) {
    sendChatMsg.addEventListener('click', () => {
      const message = chatInput.value.trim();
      if (!message) return;

      addUserMessage(message);
      chatInput.value = '';

      setTimeout(() => {
        const reply = getBotReply(message);
        addBotMessage(reply);
      }, 500);
    });

    chatInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        sendChatMsg.click();
      }
    });
  }
}

// ========== SCROLL REVEAL ANIMATION ==========
function initAOS() {
  const elements = document.querySelectorAll('[data-aos]');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('aos-animate');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  elements.forEach(el => observer.observe(el));
}

// ========== ECOMMERCE PAGE SPECIFIC CODE ==========
if (window.location.pathname.includes('ecommerce.html') || window.location.pathname.endsWith('ecommerce.html')) {

  // Product Database
  const products = [
    { id: 1, name: "Razer Blade 16 Gaming Laptop", price: 1899, desc: "RTX 4070, 32GB RAM, 1TB SSD, 240Hz QHD+", category: "laptop", img: "https://images.pexels.com/photos/7972512/pexels-photo-7972512.jpeg?auto=compress&cs=tinysrgb&w=400" },
    { id: 2, name: "MacBook Pro M3 Max", price: 2499, desc: "16-inch, 36GB RAM, 1TB SSD, Space Black", category: "mac", img: "https://images.pexels.com/photos/18105/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=400" },
    { id: 3, name: "Keychron K2 Pro", price: 129, desc: "Hot-swappable, RGB backlight, Aluminum frame", category: "keyboard", img: "https://images.pexels.com/photos/2115257/pexels-photo-2115257.jpeg?auto=compress&cs=tinysrgb&w=400" },
    { id: 4, name: "Cat6 Ethernet Cable 10ft", price: 12, desc: "High-speed shielded, gold-plated connectors", category: "accessory", img: "https://images.pexels.com/photos/162638/ethernet-cable-network-cable-internet-connection-162638.jpeg?auto=compress&cs=tinysrgb&w=400" },
    { id: 5, name: "Samsung 990 Pro 2TB SSD", price: 179, desc: "NVMe PCIe 4.0, 7450 MB/s read", category: "ssd", img: "https://images.pexels.com/photos/2582937/pexels-photo-2582937.jpeg?auto=compress&cs=tinysrgb&w=400" },
    { id: 6, name: "Corsair Vengeance 32GB DDR5", price: 149, desc: "6000MHz, CL30, RGB lighting", category: "ram", img: "https://images.pexels.com/photos/2582930/pexels-photo-2582930.jpeg?auto=compress&cs=tinysrgb&w=400" },
    { id: 7, name: "ASUS ROG Rapture GT-AX11000", price: 399, desc: "Tri-band WiFi 6 gaming router", category: "router", img: "https://images.pexels.com/photos/2047905/pexels-photo-2047905.jpeg?auto=compress&cs=tinysrgb&w=400" },
    { id: 8, name: "LG UltraGear 27\" 240Hz", price: 399, desc: "QHD, 1ms, G-Sync Compatible", category: "monitor", img: "https://images.pexels.com/photos/2765174/pexels-photo-2765174.jpeg?auto=compress&cs=tinysrgb&w=400" },
    { id: 9, name: "Logitech G Pro X Superlight", price: 149, desc: "Wireless, 63g, Hero 25K sensor", category: "mouse", img: "https://images.pexels.com/photos/1612972/mouse-computer-mouse-wireless-mouse-magic-mouse-1612972.jpeg?auto=compress&cs=tinysrgb&w=400" },
    { id: 10, name: "MSI GeForce RTX 4080", price: 1199, desc: "16GB GDDR6X, DLSS 3, Triple fan", category: "gpu", img: "https://images.pexels.com/photos/2582937/pexels-photo-2582937.jpeg?auto=compress&cs=tinysrgb&w=400" },
    { id: 11, name: "MacBook Air M2", price: 1099, desc: "13.6-inch, 8GB RAM, 256GB SSD", category: "mac", img: "https://images.pexels.com/photos/18105/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=400" },
    { id: 12, name: "WD Black SN850X 1TB", price: 89, desc: "NVMe SSD, up to 7300MB/s", category: "ssd", img: "https://images.pexels.com/photos/2582937/pexels-photo-2582937.jpeg?auto=compress&cs=tinysrgb&w=400" }
  ];

  // Cart Management
  let cart = JSON.parse(localStorage.getItem('angeltech_cart')) || [];

  function saveCart() {
    localStorage.setItem('angeltech_cart', JSON.stringify(cart));
    updateCartUI();
  }

  function updateCartUI() {
    const cartCountElements = document.querySelectorAll('.cart-count');
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCountElements.forEach(el => el.textContent = totalItems);

    // Update cart sidebar if open
    if (document.getElementById('cartItemsContainer')) {
      renderCartSidebar();
    }
  }

  function addToCart(product) {
    const existing = cart.find(item => item.id === product.id);
    if (existing) {
      existing.quantity++;
    } else {
      cart.push({ ...product, quantity: 1 });
    }
    saveCart();
    showNotification(`${product.name} added to cart!`);
  }

  function showNotification(message) {
    // Create temporary notification
    const notif = document.createElement('div');
    notif.className = 'cart-notification';
    notif.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;
    notif.style.cssText = `
      position: fixed;
      bottom: 100px;
      right: 20px;
      background: #2563eb;
      color: white;
      padding: 12px 20px;
      border-radius: 50px;
      z-index: 10000;
      animation: slideIn 0.3s ease;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    document.body.appendChild(notif);
    setTimeout(() => notif.remove(), 2000);
  }

  // Render Products Grid
  function renderProducts(filter = 'all', searchTerm = '') {
    const grid = document.getElementById('productsGrid');
    if (!grid) return;

    let filtered = [...products];
    if (filter !== 'all') {
      filtered = filtered.filter(p => p.category === filter);
    }
    if (searchTerm) {
      filtered = filtered.filter(p =>
        p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        p.desc.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filtered.length === 0) {
      grid.innerHTML = '<div class="no-results">No products found. Try another search!</div>';
      return;
    }

    grid.innerHTML = filtered.map(product => `
      <div class="product-card" data-id="${product.id}">
        <img src="${product.img}" alt="${product.name}" loading="lazy">
        <h4>${product.name}</h4>
        <div class="price">$${product.price}</div>
        <div class="desc-sm">${product.desc.substring(0, 60)}...</div>
        <button class="add-to-cart-btn" data-id="${product.id}">
          Add to Cart <i class="fas fa-cart-plus"></i>
        </button>
      </div>
    `).join('');

    // Attach event listeners to Add to Cart buttons
    document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const id = parseInt(btn.dataset.id);
        const product = products.find(p => p.id === id);
        if (product) addToCart(product);
      });
    });

    // Add click event for product quick view
    document.querySelectorAll('.product-card').forEach(card => {
      card.addEventListener('click', (e) => {
        if (!e.target.classList.contains('add-to-cart-btn')) {
          const id = parseInt(card.dataset.id);
          const product = products.find(p => p.id === id);
          if (product) openProductModal(product);
        }
      });
    });
  }

  // Product Modal
  function openProductModal(product) {
    const modal = document.getElementById('productModal');
    const modalBody = document.getElementById('modalBody');
    if (!modal || !modalBody) return;

    modalBody.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1rem;">
        <img src="${product.img}" alt="${product.name}" style="width: 100%; border-radius: 20px;">
        <h2>${product.name}</h2>
        <p style="font-size: 1.2rem; color: #2563eb; font-weight: 700;">$${product.price}</p>
        <p>${product.desc}</p>
        <div class="quantity-selector" style="display: flex; gap: 1rem; align-items: center; margin: 1rem 0;">
          <label>Quantity:</label>
          <input type="number" id="modalQty" value="1" min="1" max="99" style="width: 70px; padding: 0.5rem; border-radius: 8px; border: 1px solid #e2e8f0;">
        </div>
        <button id="modalAddToCart" class="btn btn-primary" style="width: 100%;">Add to Cart</button>
      </div>
    `;

    modal.style.display = 'flex';

    document.getElementById('modalAddToCart').addEventListener('click', () => {
      const qty = parseInt(document.getElementById('modalQty').value) || 1;
      const existing = cart.find(item => item.id === product.id);
      if (existing) {
        existing.quantity += qty;
      } else {
        cart.push({ ...product, quantity: qty });
      }
      saveCart();
      showNotification(`${qty} × ${product.name} added to cart!`);
      modal.style.display = 'none';
    });
  }

  // Cart Sidebar
  function renderCartSidebar() {
    const container = document.getElementById('cartItemsContainer');
    const totalSpan = document.getElementById('cartTotal');
    if (!container) return;

    if (cart.length === 0) {
      container.innerHTML = '<div style="text-align: center; padding: 2rem;">Your cart is empty 🛒</div>';
      if (totalSpan) totalSpan.textContent = '$0.00';
      return;
    }

    container.innerHTML = cart.map(item => `
      <div class="cart-item" data-id="${item.id}">
        <img src="${item.img}" alt="${item.name}">
        <div class="cart-item-info">
          <h4>${item.name}</h4>
          <p>$${item.price}</p>
        </div>
        <div class="cart-item-actions">
          <input type="number" class="cart-qty-input" data-id="${item.id}" value="${item.quantity}" min="1" style="width: 50px;">
          <button class="remove-item-btn" data-id="${item.id}"><i class="fas fa-trash-alt"></i></button>
        </div>
      </div>
    `).join('');

    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    if (totalSpan) totalSpan.textContent = `$${total.toFixed(2)}`;

    // Quantity change handlers
    document.querySelectorAll('.cart-qty-input').forEach(input => {
      input.addEventListener('change', (e) => {
        const id = parseInt(input.dataset.id);
        const newQty = parseInt(input.value);
        if (newQty > 0) {
          const item = cart.find(i => i.id === id);
          if (item) item.quantity = newQty;
          saveCart();
        }
      });
    });

    // Remove item handlers
    document.querySelectorAll('.remove-item-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = parseInt(btn.dataset.id);
        cart = cart.filter(i => i.id !== id);
        saveCart();
      });
    });
  }

  // Cart Overlay
  const cartOverlay = document.getElementById('cartOverlay');
  const cartIconBtn = document.getElementById('cartIconBtn');

  if (cartIconBtn && cartOverlay) {
    cartIconBtn.addEventListener('click', () => {
      renderCartSidebar();
      cartOverlay.classList.add('active');
    });

    document.querySelectorAll('.close-cart').forEach(btn => {
      btn.addEventListener('click', () => {
        cartOverlay.classList.remove('active');
      });
    });

    cartOverlay.addEventListener('click', (e) => {
      if (e.target === cartOverlay) {
        cartOverlay.classList.remove('active');
      }
    });
  }

  // Checkout
  const checkoutBtn = document.getElementById('checkoutBtn');
  if (checkoutBtn) {
    checkoutBtn.addEventListener('click', () => {
      if (cart.length === 0) {
        alert('Your cart is empty!');
        return;
      }
      alert('Thank you for your order! Our team will contact you shortly for payment and shipping details.');
      cart = [];
      saveCart();
      cartOverlay.classList.remove('active');
    });
  }

  // Filter and Search
  let currentFilter = 'all';
  let currentSearch = '';

  const filterBtns = document.querySelectorAll('.filter-btn');
  const searchInput = document.getElementById('searchInput');

  if (filterBtns.length) {
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentFilter = btn.dataset.filter;
        renderProducts(currentFilter, currentSearch);
      });
    });
  }

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      currentSearch = e.target.value;
      renderProducts(currentFilter, currentSearch);
    });
  }

  // Initialize shop
  renderProducts();
  updateCartUI();

  // Style for no results
  const style = document.createElement('style');
  style.textContent = `
    .no-results { text-align: center; padding: 3rem; font-size: 1.2rem; color: #6b7280; grid-column: 1/-1; }
    .cart-notification { animation: slideIn 0.3s ease; }
    @keyframes slideIn {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
  `;
  document.head.appendChild(style);
}

// Close modals on escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    const modal = document.getElementById('productModal');
    if (modal && modal.style.display === 'flex') modal.style.display = 'none';
    const cartOverlay = document.getElementById('cartOverlay');
    if (cartOverlay && cartOverlay.classList.contains('active')) cartOverlay.classList.remove('active');
    const chatModal = document.getElementById('chatModal');
    if (chatModal && chatModal.style.display === 'flex') chatModal.style.display = 'none';
  }
});