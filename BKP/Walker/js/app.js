/* ===== Walkers Variety Vault app.js ===== */

/* ── IMAGE MAP ─────────────────────────────────────── */
const IMG = {
  beauty:[
    'https://images.unsplash.com/photo-1522336572468-97b06e8ef143?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1583241809340-6e65fbdcb915?w=400&h=400&fit=crop',
  ],
  apparel:[
    'https://images.unsplash.com/photo-1532453288672-3a27e9be9efd?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1483985988355-763728e1935b?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1445205170230-053b83016050?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=400&h=400&fit=crop',
  ],
  electronics:[
    'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1550009158-9ebf69173e03?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1521931961826-fe48677230a5?w=400&h=400&fit=crop',
  ],
  wellness:[
    'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1545205597-3d9d02c29597?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1601042879364-f3947d3f9c16?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=400&fit=crop',
  ],
  home:[
    'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1619566636858-adf3ef46400b?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?w=400&h=400&fit=crop',
  ],
  lifestyle:[
    'https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1558618666-fcd25c85f2df?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1542296332-2e4473faf563?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1526178613552-2a45e6c9d097?w=400&h=400&fit=crop',
  ],
  hero:[
    'https://images.unsplash.com/photo-1522336572468-97b06e8ef143?w=300&h=300&fit=crop',
    'https://images.unsplash.com/photo-1532453288672-3a27e9be9efd?w=300&h=300&fit=crop',
    'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&h=300&fit=crop',
    'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=300&h=300&fit=crop',
  ],
  banner:{
    beauty:'https://images.unsplash.com/photo-1522336572468-97b06e8ef143?w=1200&h=380&fit=crop',
    apparel:'https://images.unsplash.com/photo-1532453288672-3a27e9be9efd?w=1200&h=380&fit=crop',
    electronics:'https://images.unsplash.com/photo-1550009158-9ebf69173e03?w=1200&h=380&fit=crop',
    wellness:'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=1200&h=380&fit=crop',
    home:'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=1200&h=380&fit=crop',
    lifestyle:'https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=1200&h=380&fit=crop',
  },
  cat:{
    beauty:'https://images.unsplash.com/photo-1522336572468-97b06e8ef143?w=400&h=250&fit=crop',
    apparel:'https://images.unsplash.com/photo-1532453288672-3a27e9be9efd?w=400&h=250&fit=crop',
    electronics:'https://images.unsplash.com/photo-1550009158-9ebf69173e03?w=400&h=250&fit=crop',
    wellness:'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=250&fit=crop',
    home:'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=250&fit=crop',
    lifestyle:'https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=400&h=250&fit=crop',
    fashion:'https://images.unsplash.com/photo-1532453288672-3a27e9be9efd?w=400&h=250&fit=crop',
    gifts:'https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=400&h=250&fit=crop',
  }
};

/* ── PRODUCTS ──────────────────────────────────────── */
const products = [
  {id:1, name:"GlowEssence Radiant Skincare Set 5-Piece",     brand:"GlowEssence",   price:8499,  oldPrice:11999, cat:"beauty", rating:4.8, reviews:2341, emoji:"💄", img:IMG.beauty[0], stock:15, isNew:false, isBest:true,  disc:29, colors:["Gold","Rose","Charcoal"], sizes:[]},
  {id:2, name:"Vitamin C Brightening Serum 30ml",             brand:"GlowEssence",   price:3299,  oldPrice:4499,  cat:"beauty", rating:4.9, reviews:1876, emoji:"✨", img:IMG.beauty[1], stock:8,  isNew:false, isBest:true,  disc:27, colors:[],               sizes:['15ml','30ml','50ml']},
  {id:3, name:"Hydrating Face Mask Set 3-Piece",              brand:"PureSkin",      price:6799,  oldPrice:8999,  cat:"beauty", rating:4.7, reviews:943,  emoji:"🧖", img:IMG.beauty[2], stock:22, isNew:true,  isBest:false, disc:24, colors:[],       sizes:[]},
  {id:4, name:"Natural Lip Care Collection 6-Pack",           brand:"PureSkin",      price:4599,  oldPrice:5999,  cat:"beauty", rating:4.6, reviews:712,  emoji:"💋", img:IMG.beauty[3], stock:5,  isNew:false, isBest:false, disc:23, colors:["Red","Pink","Nude"],  sizes:[]},
  {id:5, name:'StyleCraft Casual Comfort Top',                brand:"StyleCraft",    price:2999,  oldPrice:3999,  cat:"apparel", rating:4.9, reviews:3102, emoji:"👗", img:IMG.apparel[0], stock:30, isNew:false, isBest:true,  disc:25, colors:["Black","White","Navy","Red"], sizes:['S','M','L','XL']},
  {id:6, name:"Urban Chic Denim Jacket",                      brand:"StyleCraft",    price:7499,  oldPrice:9999,  cat:"apparel", rating:4.8, reviews:1543, emoji:"🧥", img:IMG.apparel[1], stock:12, isNew:false, isBest:true,  disc:25, colors:["Blue","Black","Wash"], sizes:['S','M','L','XL']},
  {id:7, name:'Essential Basic Tee 3-Pack',                   brand:"ComfortWear",   price:1599,  oldPrice:1999,  cat:"apparel", rating:4.5, reviews:567,  emoji:"👕", img:IMG.apparel[2], stock:45, isNew:true,  isBest:false, disc:20, colors:["Black","White","Gray","Navy"], sizes:['S','M','L','XL']},
  {id:8, name:'Elegant Evening Dress',                        brand:"StyleCraft",    price:2199,  oldPrice:2999,  cat:"apparel", rating:4.7, reviews:892,  emoji:"👗", img:IMG.apparel[3], stock:19, isNew:true,  isBest:false, disc:27, colors:["Red","Black","Gold"], sizes:['S','M','L']},
  {id:9, name:"TechWave Wireless Headphones Pro",             brand:"TechWave",      price:3499,  oldPrice:4999,  cat:"electronics", rating:4.8, reviews:2087, emoji:"🎧", img:IMG.electronics[0], stock:28, isNew:false, isBest:true,  disc:30, colors:["Black","White","Rose"],   sizes:[]},
  {id:10,name:"Smart Fitness Tracker Elite",                  brand:"TechWave",      price:12999, oldPrice:17999, cat:"electronics", rating:4.9, reviews:3654, emoji:"⌚", img:IMG.electronics[1], stock:7,  isNew:false, isBest:true,  disc:28, colors:["Black","Silver","Gold","Navy"], sizes:[]},
  {id:11,name:"Portable Bluetooth Speaker",                   brand:"SoundPulse",    price:1899,  oldPrice:2499,  cat:"electronics", rating:4.6, reviews:445,  emoji:"🔊", img:IMG.electronics[2], stock:60, isNew:false, isBest:false, disc:24, colors:["Black","Blue","Red"], sizes:[]},
  {id:12,name:"Fast Charging Power Bank 20000mAh",            brand:"PowerMax",      price:1299,  oldPrice:1799,  cat:"electronics", rating:4.7, reviews:1230, emoji:"🔋", img:IMG.electronics[3], stock:42, isNew:true,  isBest:false, disc:28, colors:["Black","White","Blue"], sizes:[]},
  {id:13,name:"PureLife Aromatherapy Essential Oil Set",      brand:"PureLife",      price:1799,  oldPrice:2499,  cat:"wellness", rating:4.7, reviews:2341, emoji:"🌿", img:IMG.wellness[0], stock:89, isNew:false, isBest:true,  disc:28, colors:[],  sizes:[]},
  {id:14,name:"Yoga Mat Premium Non-Slip 6mm",                brand:"PureLife",      price:899,   oldPrice:1299,  cat:"wellness", rating:4.5, reviews:1876, emoji:"🧘", img:IMG.wellness[1], stock:120,isNew:false, isBest:false, disc:31, colors:["Purple","Blue","Green","Gray"], sizes:[]},
  {id:15,name:"Meditation Cushion Set",                       brand:"ZenSpace",      price:699,   oldPrice:999,   cat:"wellness", rating:4.6, reviews:943,  emoji:"🪷", img:IMG.wellness[2], stock:78, isNew:true,  isBest:false, disc:30, colors:["Burgundy","Blue","Gray"], sizes:[]},
  {id:16,name:"Self-Care Wellness Kit",                       brand:"PureLife",      price:1199,  oldPrice:1599,  cat:"wellness", rating:4.4, reviews:567,  emoji:"🧴", img:IMG.wellness[3], stock:34, isNew:false, isBest:false, disc:25, colors:[],    sizes:[]},
  {id:17,name:"HomeComfort Cozy Throw Blanket",               brand:"HomeComfort",   price:5999,  oldPrice:7999,  cat:"home",   rating:4.8, reviews:1234, emoji:"🛋️", img:IMG.home[0],   stock:14, isNew:false, isBest:true,  disc:25, colors:["Gray","Beige","Navy","Burgundy"],sizes:[]},
  {id:18,name:"Kitchen Storage Organizer Set 5-Piece",        brand:"HomeComfort",   price:3299,  oldPrice:4499,  cat:"home",   rating:4.7, reviews:892,  emoji:"🗄️", img:IMG.home[1],   stock:31, isNew:false, isBest:false, disc:27, colors:["White","Black","Wood"], sizes:[]},
  {id:19,name:"Decorative Candle Set 3-Piece",                brand:"HomeComfort",   price:1499,  oldPrice:1999,  cat:"home",   rating:4.6, reviews:445,  emoji:"🕯️", img:IMG.home[2],   stock:56, isNew:true,  isBest:false, disc:25, colors:["Vanilla","Lavender","Citrus"], sizes:[]},
  {id:20,name:"Wall Art Décor Set Modern",                    brand:"ArtSpace",      price:1299,  oldPrice:1799,  cat:"home",   rating:4.5, reviews:712,  emoji:"🖼️", img:IMG.home[3],   stock:43, isNew:true,  isBest:false, disc:28, colors:["Black","Gold","Natural"], sizes:[]},
  {id:21,name:"Luxury Gift Box Set",                          brand:"GiftCraft",     price:2499,  oldPrice:3499,  cat:"lifestyle", rating:4.9, reviews:3102, emoji:"🎁", img:IMG.lifestyle[0], stock:22, isNew:false, isBest:true,  disc:29, colors:["Gold","Rose","Silver"],sizes:[]},
  {id:22,name:"Premium Leather Journal",                      brand:"CraftWorks",    price:1699,  oldPrice:2299,  cat:"lifestyle", rating:4.8, reviews:1543, emoji:"📓", img:IMG.lifestyle[1], stock:47, isNew:false, isBest:true,  disc:26, colors:["Brown","Black","Tan"],     sizes:["A5","A4","Pocket"]},
  {id:23,name:"Scented Candle Gift Set 6-Pack",               brand:"AromaGlow",     price:1999,  oldPrice:2799,  cat:"lifestyle", rating:4.7, reviews:987,  emoji:"🕯️", img:IMG.lifestyle[2], stock:33, isNew:false, isBest:false, disc:29, colors:[],   sizes:[]},
  {id:24,name:"Fashion Accessory Set",                        brand:"StyleCraft",    price:799,   oldPrice:1199,  cat:"lifestyle", rating:4.5, reviews:2341, emoji:"💍", img:IMG.lifestyle[3], stock:95, isNew:true,  isBest:false, disc:33, colors:["Gold","Silver","Rose"], sizes:[]},
];

/* ── STATE ─────────────────────────────────────────── */
let cart     = JSON.parse(localStorage.getItem('wvv_cart')    ) || [];
let wishlist = JSON.parse(localStorage.getItem('wvv_wishlist')) || [];
const saveCart     = () => localStorage.setItem('wvv_cart',     JSON.stringify(cart));
const saveWishlist = () => localStorage.setItem('wvv_wishlist', JSON.stringify(wishlist));

/* ── CART ──────────────────────────────────────────── */
function addToCart(id, qty=1){
  const p = products.find(x=>x.id===id); if(!p) return;
  const ex = cart.find(x=>x.id===id);
  if(ex) ex.qty = Math.min(ex.qty+qty, p.stock);
  else cart.push({id, qty, name:p.name, price:p.price, emoji:p.emoji, img:p.img});
  saveCart(); updateCartCount(); animCart();
  toast(`${p.name.slice(0,30)}… added to cart 🛒`,'success');
}
function removeFromCart(id){ cart=cart.filter(x=>x.id!==id); saveCart(); updateCartCount(); renderCartItems(); }
function updateQty(id, delta){
  const item=cart.find(x=>x.id===id); const p=products.find(x=>x.id===id); if(!item) return;
  item.qty=Math.max(1,Math.min(item.qty+delta, p?.stock||99));
  saveCart(); renderCartItems();
}
function getCartTotal(){ return cart.reduce((s,i)=>{ const p=products.find(x=>x.id===i.id); return s+(p?.price||i.price)*i.qty; },0); }
function getCartCount(){ return cart.reduce((s,i)=>s+i.qty,0); }
function updateCartCount(){
  const n=getCartCount();
  document.querySelectorAll('.cart-count').forEach(el=>{ el.textContent=n; el.style.display=n>0?'flex':'none'; });
}
function animCart(){ document.querySelectorAll('[data-cart]').forEach(el=>{ el.style.transform='scale(1.3)'; setTimeout(()=>el.style.transform='',300); }); }

/* ── WISHLIST ──────────────────────────────────────── */
function toggleWishlist(id){
  const i=wishlist.indexOf(id);
  if(i===-1){ wishlist.push(id); toast('Added to wishlist ❤️','info'); }
  else { wishlist.splice(i,1); toast('Removed from wishlist','info'); }
  saveWishlist(); syncWishlistUI();
}
function syncWishlistUI(){
  document.querySelectorAll('[data-wid]').forEach(btn=>{
    const id=parseInt(btn.dataset.wid); const on=wishlist.includes(id);
    btn.classList.toggle('fav',on); btn.innerHTML=on?'❤️':'🤍';
    btn.title=on?'Remove from wishlist':'Add to wishlist';
  });
  const n=wishlist.length;
  document.querySelectorAll('.wish-count').forEach(el=>{ el.textContent=n; el.style.display=n>0?'flex':'none'; });
}

/* ── TOAST ─────────────────────────────────────────── */
function toast(msg, type='info', dur=3200){
  let wrap=document.querySelector('.toast-wrap');
  if(!wrap){ wrap=document.createElement('div'); wrap.className='toast-wrap'; document.body.appendChild(wrap); }
  const el=document.createElement('div'); el.className=`toast ${type}`;
  const ico=type==='success'?'✓':type==='error'?'✕':'ℹ';
  el.innerHTML=`<span class="toast-ico">${ico}</span><span>${msg}</span>`;
  wrap.appendChild(el);
  setTimeout(()=>{ el.classList.add('toast-out'); setTimeout(()=>el.remove(),320); },dur);
}

/* ── PRODUCT CARD ──────────────────────────────────── */
function renderCard(p){
  const fav=wishlist.includes(p.id);
  const save=p.oldPrice-p.price;
  return `<div class="pcard" data-id="${p.id}">
    <div class="pcard-img" onclick="openQV(${p.id})">
      <div class="pcard-badges">
        ${p.isNew?'<span class="badge badge-acc" style="font-size:.60rem">NEW</span>':''}
        ${p.isBest?'<span class="badge badge-pri" style="font-size:.60rem">BEST</span>':''}
        ${p.disc?`<span class="badge badge-dark" style="font-size:.60rem">-${p.disc}%</span>`:''}
      </div>
      <div class="pcard-acts">
        <button class="pact-btn ${fav?'fav':''}" data-wid="${p.id}" onclick="event.stopPropagation();toggleWishlist(${p.id})">${fav?'❤️':'🤍'}</button>
        <button class="pact-btn" onclick="event.stopPropagation();openQV(${p.id})" title="Quick view">👁</button>
      </div>
      <img src="${p.img}" alt="${p.name}" loading="lazy" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
      <span class="emoji-fb" style="display:none">${p.emoji}</span>
    </div>
    <div class="pcard-body">
      <div class="pcard-brand">${p.brand}</div>
      <div class="pcard-name">${p.name}</div>
      <div class="pcard-stars">
        <span class="stars">${'★'.repeat(Math.floor(p.rating))}${'☆'.repeat(5-Math.floor(p.rating))}</span>
        <span class="rcount">${p.rating} (${p.reviews.toLocaleString()})</span>
      </div>
      ${p.stock<=5?`<div class="stock-low">⚠ Only ${p.stock} left</div>`:'<div class="stock-ok">✓ In Stock</div>'}
      <div class="pcard-price">
        <span class="p-now">KSh ${p.price.toLocaleString()}</span>
        ${p.oldPrice?`<span class="p-old">KSh ${p.oldPrice.toLocaleString()}</span>`:''}
        ${save>0?`<span class="p-save">-KSh ${save.toLocaleString()}</span>`:''}
      </div>
      <div class="pcard-foot">
        <button class="btn-atc" onclick="addToCart(${p.id})">🛒 Add to Cart</button>
        <button class="btn-buy-s" onclick="buyNow(${p.id})">Buy</button>
      </div>
    </div>
  </div>`;
}

/* ── QUICK VIEW ────────────────────────────────────── */
function openQV(id){
  const p=products.find(x=>x.id===id); if(!p) return;
  const ov=document.getElementById('qvModal'); if(!ov) return;
  const save=p.oldPrice-p.price;
  ov.querySelector('.modal').innerHTML=`
    <button class="modal-x" onclick="closeQV()">✕</button>
    <div class="modal-grid">
      <div>
        <div class="gal-main"><img src="${p.img.replace('w=400&h=400','w=600&h=600')}" alt="${p.name}" onerror="this.outerHTML='<span style=font-size:6rem>${p.emoji}</span>'"></div>
        <div class="gal-thumbs">
          <div class="g-thumb active"><img src="${p.img.replace('w=400&h=400','w=130&h=130')}" alt="" onerror="this.outerHTML='<span style=font-size:1.6rem>${p.emoji}</span>'"></div>
          <div class="g-thumb"><span style="font-size:1.6rem">📦</span></div>
          <div class="g-thumb"><span style="font-size:1.6rem">✨</span></div>
          <div class="g-thumb"><span style="font-size:1.6rem">🎁</span></div>
        </div>
      </div>
      <div>
        <div class="prod-brand">${p.brand}</div>
        <div class="prod-title">${p.name}</div>
        <div class="pcard-stars" style="margin-bottom:12px">
          <span class="stars">${'★'.repeat(Math.floor(p.rating))}${'☆'.repeat(5-Math.floor(p.rating))}</span>
          <span class="rcount">${p.rating} · ${p.reviews.toLocaleString()} reviews</span>
          ${p.isBest?'<span class="badge badge-pri">BESTSELLER</span>':''}
        </div>
        <div style="margin-bottom:18px">
          <span class="prod-price-main">KSh ${p.price.toLocaleString()}</span>
          ${p.oldPrice?`<span class="prod-price-old">KSh ${p.oldPrice.toLocaleString()}</span>`:''}
          ${save>0?`<div class="prod-save">Save KSh ${save.toLocaleString()} (${p.disc}% OFF)</div>`:''}
        </div>
        ${p.colors.length?`<div class="var-label">Color</div><div class="var-row">${p.colors.map((c,i)=>`<button class="var-btn ${i===0?'active':''}" onclick="this.parentNode.querySelectorAll('.var-btn').forEach(b=>b.classList.remove('active'));this.classList.add('active')">${c}</button>`).join('')}</div>`:''}
        ${p.sizes.length?`<div class="var-label">Size</div><div class="var-row">${p.sizes.map((s,i)=>`<button class="var-btn ${i===0?'active':''}" onclick="this.parentNode.querySelectorAll('.var-btn').forEach(b=>b.classList.remove('active'));this.classList.add('active')">${s}</button>`).join('')}</div>`:''}
        <div class="qty-row">
          <div class="qty-ctrl">
            <button class="qb" onclick="this.nextElementSibling.value=Math.max(1,+this.nextElementSibling.value-1)">−</button>
            <input class="qi" type="number" value="1" min="1" max="${p.stock}" id="qv-qty">
            <button class="qb" onclick="this.previousElementSibling.value=Math.min(${p.stock},+this.previousElementSibling.value+1)">+</button>
          </div>
          <span class="${p.stock<=5?'stock-low':'stock-ok'}">${p.stock<=5?`⚠ Only ${p.stock} left`:`✓ ${p.stock} in stock`}</span>
        </div>
        <div class="prod-acts">
          <button class="btn-atc" onclick="addToCart(${p.id},+document.getElementById('qv-qty').value);closeQV()">🛒 Add to Cart</button>
          <button class="btn-wish" onclick="buyNow(${p.id})">Buy Now</button>
        </div>
        <a href="product.html?id=${p.id}" style="font-size:.82rem;color:var(--primary);font-weight:600;display:block;margin-top:6px">View Full Details →</a>
      </div>
    </div>`;
  ov.classList.add('open'); document.body.style.overflow='hidden';
}
function closeQV(){ const ov=document.getElementById('qvModal'); if(ov){ov.classList.remove('open');document.body.style.overflow='';} }
function buyNow(id){ addToCart(id); window.location.href='cart.html'; }

/* ── SEARCH ────────────────────────────────────────── */
function initSearch(){
  document.querySelectorAll('.nav-search').forEach(wrap=>{
    const inp=wrap.querySelector('input'); const drop=wrap.querySelector('.search-drop'); if(!inp||!drop) return;
    inp.addEventListener('input',()=>{
      const v=inp.value.toLowerCase().trim(); if(!v){drop.classList.remove('open');return;}
      const matches=products.filter(p=>p.name.toLowerCase().includes(v)||p.brand.toLowerCase().includes(v)).slice(0,6);
      if(!matches.length){drop.classList.remove('open');return;}
      drop.innerHTML=matches.map(p=>`<div class="search-item" onclick="openQV(${p.id})"><span>${p.emoji}</span><span>${p.name}</span><span class="search-item-price">KSh ${p.price.toLocaleString()}</span></div>`).join('');
      drop.classList.add('open');
    });
    document.addEventListener('click',e=>{if(!wrap.contains(e.target)) drop.classList.remove('open');});
  });
}

/* ── NAVBAR ────────────────────────────────────────── */
function initNavbar(){
  const nav=document.querySelector('.navbar'); if(!nav) return;
  window.addEventListener('scroll',()=>nav.classList.toggle('scrolled',window.scrollY>20),{passive:true});
}

/* ── SIDEBAR ───────────────────────────────────────── */
function initSidebar(){
  const ham=document.querySelector('.hamburger'),ov=document.querySelector('.sb-overlay'),sb=document.querySelector('.sidebar'),cl=document.querySelector('.sb-close');
  if(!ham) return;
  const open=()=>{sb?.classList.add('open');ov?.classList.add('open');document.body.style.overflow='hidden';};
  const close=()=>{sb?.classList.remove('open');ov?.classList.remove('open');document.body.style.overflow='';};
  ham.addEventListener('click',open); cl?.addEventListener('click',close); ov?.addEventListener('click',close);
}

/* ── DARK MODE ─────────────────────────────────────── */
function initTheme(){
  const saved=localStorage.getItem('wvv_theme')||'dark';
  document.documentElement.setAttribute('data-theme',saved);
  setThemeIcons(saved);
  document.querySelectorAll('.theme-btn').forEach(btn=>{
    btn.addEventListener('click',()=>{
      const cur=document.documentElement.getAttribute('data-theme');
      const nxt=cur==='dark'?'light':'dark';
      document.documentElement.setAttribute('data-theme',nxt);
      localStorage.setItem('wvv_theme',nxt); setThemeIcons(nxt);
    });
  });
}
function setThemeIcons(t){
  document.querySelectorAll('.theme-btn').forEach(b=>{ b.innerHTML=t==='dark'?'☀️':'🌙'; b.title=t==='dark'?'Light mode':'Dark mode'; });
}

/* ── COUNTERS ──────────────────────────────────────── */
function initCounters(){
  const els=document.querySelectorAll('[data-count]'); if(!els.length) return;
  const obs=new IntersectionObserver(entries=>{
    entries.forEach(e=>{
      if(!e.isIntersecting) return;
      const el=e.target,target=parseInt(el.dataset.count),suf=el.dataset.suffix||'',dur=1800,start=performance.now();
      const anim=now=>{const prog=Math.min((now-start)/dur,1),ease=1-Math.pow(1-prog,3);el.textContent=Math.round(ease*target).toLocaleString()+suf;if(prog<1)requestAnimationFrame(anim);};
      requestAnimationFrame(anim); obs.unobserve(el);
    });
  },{threshold:.5});
  els.forEach(el=>obs.observe(el));
}

/* ── COUNTDOWN ─────────────────────────────────────── */
function initCountdown(){
  const containers=document.querySelectorAll('.countdown'); if(!containers.length) return;
  const end=Date.now()+6*3600000;
  const tick=()=>{
    const r=Math.max(0,end-Date.now()),h=Math.floor(r/3600000),m=Math.floor((r%3600000)/60000),s=Math.floor((r%60000)/1000);
    containers.forEach(c=>{
      const ns=c.querySelectorAll('.cu-n');
      if(ns[0])ns[0].textContent=String(h).padStart(2,'0');
      if(ns[1])ns[1].textContent=String(m).padStart(2,'0');
      if(ns[2])ns[2].textContent=String(s).padStart(2,'0');
    });
  };
  tick(); setInterval(tick,1000);
}

/* ── SCROLL REVEAL ─────────────────────────────────── */
function initReveal(){
  const els=document.querySelectorAll('.pcard,.cat-card,.feat-card,.testi-card,.reveal');
  const obs=new IntersectionObserver(entries=>{
    entries.forEach((e,i)=>{
      if(!e.isIntersecting) return;
      setTimeout(()=>{e.target.style.opacity='1';e.target.style.transform='translateY(0)';},( (i%4)*55));
      obs.unobserve(e.target);
    });
  },{threshold:.1,rootMargin:'0px 0px -28px 0px'});
  els.forEach((el,i)=>{ el.style.opacity='0';el.style.transform='translateY(18px)';el.style.transition='opacity .5s ease,transform .5s ease';obs.observe(el); });
}

/* ── HORIZONTAL SCROLL ─────────────────────────────── */
function initHScroll(){
  document.querySelectorAll('.pscroll-wrap').forEach(wrap=>{
    const track=wrap.querySelector('.pscroll'); if(!track) return;
    const prev=wrap.querySelector('.sarrow-prev'),next=wrap.querySelector('.sarrow-next');
    const scroll=dir=>track.scrollBy({left:dir*(track.offsetWidth*0.75),behavior:'smooth'});
    prev?.addEventListener('click',()=>scroll(-1)); next?.addEventListener('click',()=>scroll(1));
    track.addEventListener('scroll',()=>{
      if(prev) prev.disabled=track.scrollLeft<10;
      if(next) next.disabled=track.scrollLeft+track.clientWidth>=track.scrollWidth-10;
    },{passive:true});
    if(prev) prev.disabled=true;
  });
}

/* ── CART PAGE ─────────────────────────────────────── */
function renderCartItems(){
  const el=document.getElementById('cartItems'); if(!el) return;
  if(!cart.length){
    el.innerHTML=`<div class="empty-state"><div class="empty-icon">🛒</div><h3>Your cart is empty</h3><p>Discover amazing products you'll love</p><a href="ecommerce.html" class="btn btn-primary">Start Shopping</a></div>`;
    updateSummary(); return;
  }
  el.innerHTML=cart.map(item=>{
    const p=products.find(x=>x.id===item.id); if(!p) return '';
    return `<div class="cart-item">
      <div class="ci-img">${p.img?`<img src="${p.img}" alt="${p.name}" onerror="this.style.display='none'">`:''}${p.emoji}</div>
      <div class="ci-info">
        <div class="ci-name">${p.name}</div>
        <div class="ci-meta">${p.brand} · ${p.stock>0?'✓ In Stock':'Out of Stock'}</div>
        <div class="ci-qty">
          <button class="qty-b" onclick="updateQty(${item.id},-1)">−</button>
          <span class="qty-n" id="cq-${item.id}">${item.qty}</span>
          <button class="qty-b" onclick="updateQty(${item.id},1)">+</button>
        </div>
      </div>
      <div class="ci-price">
        <div class="ci-total">KSh ${(p.price*item.qty).toLocaleString()}</div>
        <div class="ci-each">KSh ${p.price.toLocaleString()} each</div>
        <button class="ci-remove" onclick="removeFromCart(${item.id})">🗑 Remove</button>
      </div>
    </div>`;
  }).join('');
  updateSummary();
}
function updateSummary(){
  const sub=getCartTotal(),ship=sub>5000?0:299,tax=Math.round(sub*.16),total=sub+ship+tax;
  const s=(id,v)=>{const el=document.getElementById(id);if(el)el.textContent=v;};
  s('sum-sub',`KSh ${sub.toLocaleString()}`);
  s('sum-ship',ship===0?'FREE 🎉':`KSh ${ship}`);
  s('sum-tax',`KSh ${tax.toLocaleString()}`);
  s('sum-total',`KSh ${total.toLocaleString()}`);
  s('sum-count',`${getCartCount()} item${getCartCount()!==1?'s':''}`);
}

/* ── SHOP PAGE ─────────────────────────────────────── */
let shopFilter='all', shopSort='popular';
function renderShop(){
  const el=document.getElementById('shopGrid'); if(!el) return;
  let list=shopFilter==='all'?products:products.filter(p=>p.cat===shopFilter);
  if(shopSort==='price-lo') list=[...list].sort((a,b)=>a.price-b.price);
  else if(shopSort==='price-hi') list=[...list].sort((a,b)=>b.price-a.price);
  else if(shopSort==='rating') list=[...list].sort((a,b)=>b.rating-a.rating);
  else if(shopSort==='new') list=[...list].sort((a,b)=>b.isNew-a.isNew);
  else list=[...list].sort((a,b)=>b.reviews-a.reviews);
  el.innerHTML=list.map(p=>renderCard(p)).join('');
  const cnt=document.getElementById('shopCount'); if(cnt) cnt.textContent=`Showing ${list.length} products`;
  syncWishlistUI(); setTimeout(initReveal,80);
}
function initShop(){
  const sortEl=document.getElementById('sortSel');
  sortEl?.addEventListener('change',()=>{shopSort=sortEl.value;renderShop();});
  document.querySelectorAll('[data-filter]').forEach(btn=>{
    btn.addEventListener('click',()=>{
      shopFilter=btn.dataset.filter;
      document.querySelectorAll('[data-filter]').forEach(b=>b.classList.remove('active'));
      btn.classList.add('active'); renderShop();
    });
  });
  // mobile filter panel
  const mfBtn=document.querySelector('.mob-filter-btn'),sidebar=document.querySelector('.shop-sidebar'),sideClose=document.querySelector('.sb-filters-close');
  mfBtn?.addEventListener('click',()=>sidebar?.classList.add('mob-open'));
  sideClose?.addEventListener('click',()=>sidebar?.classList.remove('mob-open'));
  // url param
  const cat=new URLSearchParams(window.location.search).get('cat');
  if(cat){ shopFilter=cat; document.querySelectorAll('[data-filter]').forEach(b=>b.classList.toggle('active',b.dataset.filter===cat)); }
  renderShop();
}

/* ── TABS ──────────────────────────────────────────── */
function initTabs(){
  document.querySelectorAll('.tab-b').forEach(btn=>{
    btn.addEventListener('click',()=>{
      const target=btn.dataset.tab;
      btn.closest('.tabs-bar').querySelectorAll('.tab-b').forEach(b=>b.classList.remove('active'));
      btn.classList.add('active');
      const panels=btn.closest('section,main,.card-tabs')?.querySelectorAll('.tab-panel');
      panels?.forEach(p=>p.classList.toggle('active',p.id===target));
    });
  });
}

/* ── PAYMENT OPTIONS ───────────────────────────────── */
function initPayOpts(){
  document.querySelectorAll('.pay-opt').forEach(opt=>{
    opt.addEventListener('click',()=>{
      opt.closest('.pay-opts').querySelectorAll('.pay-opt').forEach(o=>o.classList.remove('sel'));
      opt.classList.add('sel'); const r=opt.querySelector('input[type=radio]'); if(r) r.checked=true;
    });
  });
}

/* ── INIT ──────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded',()=>{
  initNavbar(); initSidebar(); initSearch(); initTheme(); initCounters(); initCountdown(); initTabs(); initPayOpts(); initHScroll();
  updateCartCount(); syncWishlistUI();
  if(document.getElementById('cartItems')) renderCartItems();
  if(document.getElementById('shopGrid')) initShop();
  document.getElementById('qvModal')?.addEventListener('click',e=>{if(e.target===e.currentTarget)closeQV();});
  document.querySelectorAll('.g-thumb').forEach(t=>{t.addEventListener('click',()=>{t.parentNode.querySelectorAll('.g-thumb').forEach(x=>x.classList.remove('active'));t.classList.add('active');});});
  setTimeout(initReveal,160);
});