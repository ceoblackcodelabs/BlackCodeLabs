/* ===== KitchenHub app.js ===== */

/* ── IMAGE MAP ─────────────────────────────────────── */
const IMG = {
  cookware:[
    'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1585515320310-259814833e62?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1565538810643-b5bdb714032a?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1610701596007-11502861dcfa?w=400&h=400&fit=crop',
  ],
  knives:[
    'https://images.unsplash.com/photo-1593618998160-e34014e67546?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1566454825481-9c31a8d3c4f7?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1588168333986-5078d3ae3976?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1617816254555-aa2b5d9b26b7?w=400&h=400&fit=crop',
  ],
  baking:[
    'https://images.unsplash.com/photo-1486887396153-fa416526c108?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1621303837174-89787a7d4729?w=400&h=400&fit=crop',
  ],
  utensils:[
    'https://images.unsplash.com/photo-1590794056226-79ef3a8147e1?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1606923829579-0cb981a83e2e?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1556909172-54557c7e4fb7?w=400&h=400&fit=crop',
  ],
  dining:[
    'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1464500542410-1396074bf230?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1619566636858-adf3ef46400b?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1594732832278-abd644401426?w=400&h=400&fit=crop',
  ],
  coffee:[
    'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1459755486867-b55449bb39ff?w=400&h=400&fit=crop',
    'https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?w=400&h=400&fit=crop',
  ],
  hero:[
    'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=300&fit=crop',
    'https://images.unsplash.com/photo-1593618998160-e34014e67546?w=300&h=300&fit=crop',
    'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300&h=300&fit=crop',
    'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=300&h=300&fit=crop',
  ],
  banner:{
    cookware:'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=1200&h=380&fit=crop',
    knives:  'https://images.unsplash.com/photo-1593618998160-e34014e67546?w=1200&h=380&fit=crop',
    baking:  'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=1200&h=380&fit=crop',
    dining:  'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=1200&h=380&fit=crop',
    coffee:  'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1200&h=380&fit=crop',
    utensils:'https://images.unsplash.com/photo-1590794056226-79ef3a8147e1?w=1200&h=380&fit=crop',
  },
  cat:{
    cookware:'https://images.unsplash.com/photo-1565538810643-b5bdb714032a?w=400&h=250&fit=crop',
    knives:  'https://images.unsplash.com/photo-1588168333986-5078d3ae3976?w=400&h=250&fit=crop',
    utensils:'https://images.unsplash.com/photo-1590794056226-79ef3a8147e1?w=400&h=250&fit=crop',
    dining:  'https://images.unsplash.com/photo-1464500542410-1396074bf230?w=400&h=250&fit=crop',
    baking:  'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=250&fit=crop',
    coffee:  'https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?w=400&h=250&fit=crop',
    pots:    'https://images.unsplash.com/photo-1610701596007-11502861dcfa?w=400&h=250&fit=crop',
    storage: 'https://images.unsplash.com/photo-1619566636858-adf3ef46400b?w=400&h=250&fit=crop',
  }
};

/* ── PRODUCTS ──────────────────────────────────────── */
const products = [
  {id:1, name:"ProChef 5-Piece Non-Stick Cookware Set",     brand:"ProChef",       price:8499,  oldPrice:11999, cat:"cookware", rating:4.8, reviews:2341, emoji:"🍳", img:IMG.cookware[0], stock:15, isNew:false, isBest:true,  disc:29, colors:["Black","Red","Charcoal"], sizes:[]},
  {id:2, name:"Cast Iron Skillet 12-inch Pre-Seasoned",     brand:"IronMaster",    price:3299,  oldPrice:4499,  cat:"cookware", rating:4.9, reviews:1876, emoji:"🥘", img:IMG.cookware[1], stock:8,  isNew:false, isBest:true,  disc:27, colors:["Black"],               sizes:['10"','12"','14"']},
  {id:3, name:"Stainless Steel 7-Piece Pot Set",            brand:"SteelChef",     price:6799,  oldPrice:8999,  cat:"cookware", rating:4.7, reviews:943,  emoji:"🫕", img:IMG.cookware[2], stock:22, isNew:true,  isBest:false, disc:24, colors:["Silver","Gold"],       sizes:[]},
  {id:4, name:"Ceramic Coated Dutch Oven 6Qt",              brand:"CeramaCook",    price:4599,  oldPrice:5999,  cat:"cookware", rating:4.6, reviews:712,  emoji:"🍲", img:IMG.cookware[3], stock:5,  isNew:false, isBest:false, disc:23, colors:["Red","Blue","Cream"],  sizes:[]},
  {id:5, name:'Professional 8" Chef\'s Knife German Steel', brand:"BladeElite",    price:2999,  oldPrice:3999,  cat:"knives",   rating:4.9, reviews:3102, emoji:"🔪", img:IMG.knives[0],   stock:30, isNew:false, isBest:true,  disc:25, colors:[],                     sizes:['6"','8"','10"']},
  {id:6, name:"8-Piece Knife Block Set with Sharpener",     brand:"BladeElite",    price:7499,  oldPrice:9999,  cat:"knives",   rating:4.8, reviews:1543, emoji:"🗡️", img:IMG.knives[1],   stock:12, isNew:false, isBest:true,  disc:25, colors:["Black","Walnut"],      sizes:[]},
  {id:7, name:'Bread Knife Serrated 10" Stainless',         brand:"SliceRight",    price:1599,  oldPrice:1999,  cat:"knives",   rating:4.5, reviews:567,  emoji:"🔪", img:IMG.knives[2],   stock:45, isNew:true,  isBest:false, disc:20, colors:[],                     sizes:[]},
  {id:8, name:'Santoku Knife Japanese Style 7"',            brand:"ZenBlade",      price:2199,  oldPrice:2999,  cat:"knives",   rating:4.7, reviews:892,  emoji:"🔪", img:IMG.knives[3],   stock:19, isNew:true,  isBest:false, disc:27, colors:[],                     sizes:['5"','7"','9"']},
  {id:9, name:"12-Piece Baking Set Silicone Non-Stick",     brand:"BakeMaster",    price:3499,  oldPrice:4999,  cat:"baking",   rating:4.8, reviews:2087, emoji:"🧁", img:IMG.baking[0],   stock:28, isNew:false, isBest:true,  disc:30, colors:["Red","Blue","Gray"],   sizes:[]},
  {id:10,name:"Stand Mixer 5Qt Professional 800W",          brand:"MixPro",        price:12999, oldPrice:17999, cat:"baking",   rating:4.9, reviews:3654, emoji:"🥧", img:IMG.baking[1],   stock:7,  isNew:false, isBest:true,  disc:28, colors:["White","Red","Silver","Black"], sizes:[]},
  {id:11,name:"Springform Pan Set 3-Piece Nonstick",        brand:"BakeMaster",    price:1899,  oldPrice:2499,  cat:"baking",   rating:4.6, reviews:445,  emoji:"🎂", img:IMG.baking[2],   stock:60, isNew:false, isBest:false, disc:24, colors:[],                     sizes:[]},
  {id:12,name:"Digital Kitchen Scale Precision 5kg",        brand:"PrecisionPro",  price:1299,  oldPrice:1799,  cat:"baking",   rating:4.7, reviews:1230, emoji:"⚖️", img:IMG.baking[3],   stock:42, isNew:true,  isBest:false, disc:28, colors:["Black","White"],      sizes:[]},
  {id:13,name:"Silicone Kitchen Utensil Set 10-Piece",      brand:"FlexiCook",     price:1799,  oldPrice:2499,  cat:"utensils", rating:4.7, reviews:2341, emoji:"🥄", img:IMG.utensils[0], stock:89, isNew:false, isBest:true,  disc:28, colors:["Black","Red","Teal"],  sizes:[]},
  {id:14,name:"Wooden Spoon Set 5-Piece Bamboo",            brand:"NaturalKitchen",price:899,   oldPrice:1299,  cat:"utensils", rating:4.5, reviews:1876, emoji:"🥄", img:IMG.utensils[1], stock:120,isNew:false, isBest:false, disc:31, colors:[],                     sizes:[]},
  {id:15,name:"Stainless Steel Tong Set 2-Piece",           brand:"GrillMaster",   price:699,   oldPrice:999,   cat:"utensils", rating:4.6, reviews:943,  emoji:"🥢", img:IMG.utensils[2], stock:78, isNew:true,  isBest:false, disc:30, colors:[],                     sizes:[]},
  {id:16,name:"Adjustable Rolling Pin with Rings",          brand:"BakeMaster",    price:1199,  oldPrice:1599,  cat:"utensils", rating:4.4, reviews:567,  emoji:"🪄", img:IMG.utensils[3], stock:34, isNew:false, isBest:false, disc:25, colors:["Natural","Black"],    sizes:[]},
  {id:17,name:"16-Piece Porcelain Dinner Set for 4",        brand:"DineElegant",   price:5999,  oldPrice:7999,  cat:"dining",   rating:4.8, reviews:1234, emoji:"🍽️", img:IMG.dining[0],   stock:14, isNew:false, isBest:true,  disc:25, colors:["White","Cream","Blue"],sizes:[]},
  {id:18,name:"Stainless Steel Cutlery Set 24-Piece",       brand:"SilverTable",   price:3299,  oldPrice:4499,  cat:"dining",   rating:4.7, reviews:892,  emoji:"🍴", img:IMG.dining[1],   stock:31, isNew:false, isBest:false, disc:27, colors:["Silver","Gold","Rose Gold"], sizes:[]},
  {id:19,name:"Glass Water Pitcher 2L with Lid",            brand:"CrystalClear",  price:1499,  oldPrice:1999,  cat:"dining",   rating:4.6, reviews:445,  emoji:"🫙", img:IMG.dining[2],   stock:56, isNew:true,  isBest:false, disc:25, colors:[],                     sizes:[]},
  {id:20,name:"Bamboo Serving Tray with Handles",           brand:"NaturalKitchen",price:1299,  oldPrice:1799,  cat:"dining",   rating:4.5, reviews:712,  emoji:"🍱", img:IMG.dining[3],   stock:43, isNew:true,  isBest:false, disc:28, colors:[],                     sizes:[]},
  {id:21,name:"Pour Over Coffee Maker Set with Stand",      brand:"BrewMaster",    price:2499,  oldPrice:3499,  cat:"coffee",   rating:4.9, reviews:3102, emoji:"☕", img:IMG.coffee[0],   stock:22, isNew:false, isBest:true,  disc:29, colors:["Black","Copper","Silver"],sizes:[]},
  {id:22,name:"French Press Borosilicate Glass 1L",         brand:"BrewMaster",    price:1699,  oldPrice:2299,  cat:"coffee",   rating:4.8, reviews:1543, emoji:"☕", img:IMG.coffee[1],   stock:47, isNew:false, isBest:true,  disc:26, colors:["Black","Chrome"],     sizes:["350ml","600ml","1L"]},
  {id:23,name:"Moka Pot Stovetop Espresso Maker 6-Cup",     brand:"EspressoArt",   price:1999,  oldPrice:2799,  cat:"coffee",   rating:4.7, reviews:987,  emoji:"🫗", img:IMG.coffee[2],   stock:33, isNew:false, isBest:false, disc:29, colors:["Aluminum","Black"],   sizes:[]},
  {id:24,name:"Electric Milk Frother Handheld",             brand:"FrothPro",      price:799,   oldPrice:1199,  cat:"coffee",   rating:4.5, reviews:2341, emoji:"🥛", img:IMG.coffee[3],   stock:95, isNew:true,  isBest:false, disc:33, colors:["Black","White","Rose Gold"], sizes:[]},
];

/* ── STATE ─────────────────────────────────────────── */
let cart     = JSON.parse(localStorage.getItem('kh_cart')    ) || [];
let wishlist = JSON.parse(localStorage.getItem('kh_wishlist')) || [];
const saveCart     = () => localStorage.setItem('kh_cart',     JSON.stringify(cart));
const saveWishlist = () => localStorage.setItem('kh_wishlist', JSON.stringify(wishlist));

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
  const saved=localStorage.getItem('kh_theme')||'dark';
  document.documentElement.setAttribute('data-theme',saved);
  setThemeIcons(saved);
  document.querySelectorAll('.theme-btn').forEach(btn=>{
    btn.addEventListener('click',()=>{
      const cur=document.documentElement.getAttribute('data-theme');
      const nxt=cur==='dark'?'light':'dark';
      document.documentElement.setAttribute('data-theme',nxt);
      localStorage.setItem('kh_theme',nxt); setThemeIcons(nxt);
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
    el.innerHTML=`<div class="empty-state"><div class="empty-icon">🛒</div><h3>Your cart is empty</h3><p>Discover amazing kitchen products</p><a href="ecommerce.html" class="btn btn-primary">Start Shopping</a></div>`;
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
