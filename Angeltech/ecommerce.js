const products = [
  { id:1, name:"ROG Zephyrus G14", price:1499, desc:"Gaming laptop RTX 4060", img:"https://images.pexels.com/photos/18105/pexels-photo.jpg?w=300", category:"laptop" },
  { id:2, name:"MacBook Pro M3", price:1999, desc:"Apple Silicon power", img:"https://images.pexels.com/photos/18105/pexels-photo.jpg?w=300", category:"laptop" },
  { id:3, name:"Keychron K2", price:89, desc:"Mechanical keyboard", img:"https://images.pexels.com/photos/2115257/pexels-photo-2115257.jpeg?w=300", category:"accessory" },
  { id:4, name:"Cat6 Ethernet 10ft", price:12, desc:"High speed cable", img:"https://images.pexels.com/photos/162140/ethernet-cable-close-up-connect-162140.jpeg?w=300", category:"networking" },
  { id:5, name:"Samsung 990 Pro 1TB", price:129, desc:"NVMe SSD", img:"https://images.pexels.com/photos/2582937/pexels-photo-2582937.jpeg?w=300", category:"accessory" },
  { id:6, name:"Corsair Vengeance 32GB", price:109, desc:"DDR5 RAM", img:"https://images.pexels.com/photos/2582937/pexels-photo-2582937.jpeg?w=300", category:"accessory" },
  { id:7, name:"TP-Link AX6000", price:199, desc:"Gaming router", img:"https://images.pexels.com/photos/2047905/pexels-photo-2047905.jpeg?w=300", category:"networking" },
  { id:8, name:"LG UltraGear 27\"", price:329, desc:"144Hz Monitor", img:"https://images.pexels.com/photos/2582928/pexels-photo-2582928.jpeg?w=300", category:"accessory" },
  { id:9, name:"Razer DeathAdder V3", price:69, desc:"Gaming mouse", img:"https://images.pexels.com/photos/2115257/pexels-photo-2115257.jpeg?w=300", category:"accessory" },
];
let cart = JSON.parse(localStorage.getItem('cart')) || [];
let currentFilter = 'all';
let searchTerm = '';

function renderProducts() {
  let filtered = products.filter(p => (currentFilter==='all' || p.category===currentFilter) && p.name.toLowerCase().includes(searchTerm));
  const grid = document.getElementById('productGrid');
  grid.innerHTML = filtered.map(p => `<div class="product-card" onclick="openModal(${p.id})"><div class="product-img" style="background-image:url('${p.img}')"></div><div class="product-info"><h4>${p.name}</h4><p>$${p.price}</p><button class="btn btn-primary" onclick="event.stopPropagation(); addToCart(${p.id})">Add to Cart</button></div></div>`).join('');
}
function addToCart(id) {
  const product = products.find(p=>p.id===id);
  const existing = cart.find(i=>i.id===id);
  if(existing) existing.qty++;
  else cart.push({...product, qty:1});
  updateCartUI();
  localStorage.setItem('cart', JSON.stringify(cart));
}
function updateCartUI() {
  document.getElementById('cartCount').innerText = cart.reduce((s,i)=>s+i.qty,0);
  const cartDiv = document.getElementById('cartItems');
  if(cartDiv) cartDiv.innerHTML = cart.map(item => `<div style="margin:1rem 0; border-bottom:1px solid #ddd"><span>${item.name} x${item.qty}</span> <span>$${item.price*item.qty}</span> <button onclick="removeItem(${item.id})">Remove</button></div>`).join('');
  const total = cart.reduce((s,i)=>s+i.price*i.qty,0);
  document.getElementById('cartTotal').innerHTML = `<h4>Total: $${total}</h4>`;
}
function removeItem(id) { cart = cart.filter(i=>i.id!==id); updateCartUI(); localStorage.setItem('cart', JSON.stringify(cart)); }
function openModal(id) {
  const p = products.find(p=>p.id===id);
  document.getElementById('modalContent').innerHTML = `<div style="padding:2rem"><img src="${p.img}" width="100%"><h2>${p.name}</h2><p>${p.desc}</p><p><strong>$${p.price}</strong></p><input type="number" id="modalQty" value="1" min="1"><button onclick="addToCartWithQty(${p.id})">Add to Cart</button></div>`;
  document.getElementById('productModal').classList.add('open');
}
function addToCartWithQty(id) { const qty = parseInt(document.getElementById('modalQty').value); const product = products.find(p=>p.id===id); const existing = cart.find(i=>i.id===id); if(existing) existing.qty+=qty; else cart.push({...product, qty}); updateCartUI(); localStorage.setItem('cart', JSON.stringify(cart)); document.getElementById('productModal').classList.remove('open'); }
document.getElementById('closeModal')?.addEventListener('click',()=>document.getElementById('productModal').classList.remove('open'));
document.getElementById('cartIcon')?.addEventListener('click',()=>{document.getElementById('cartOverlay').classList.add('open'); document.getElementById('cartOverlayBg').style.display='block';});
document.getElementById('closeCart')?.addEventListener('click',()=>{document.getElementById('cartOverlay').classList.remove('open'); document.getElementById('cartOverlayBg').style.display='none';});
document.getElementById('checkoutBtn')?.addEventListener('click',()=>{alert('Order placed! Thank you.'); cart=[]; updateCartUI(); localStorage.setItem('cart','[]'); document.getElementById('cartOverlay').classList.remove('open');});
document.getElementById('searchInput')?.addEventListener('input',(e)=>{searchTerm=e.target.value.toLowerCase(); renderProducts();});
document.querySelectorAll('[data-cat]').forEach(btn=>{btn.addEventListener('click',()=>{currentFilter=btn.dataset.cat; renderProducts(); document.querySelectorAll('[data-cat]').forEach(b=>b.classList.remove('active')); btn.classList.add('active');});});
renderProducts(); updateCartUI();