/* =========================================================
   POCKET OF PARADISE — site behaviour (vanilla JS)
   ========================================================= */
(function(){
'use strict';
var $=function(s,r){return (r||document).querySelector(s)};
var $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var WA='254115167384';                       // main WhatsApp line (+254 115 167 384)
var EMAIL='info@pocketofparadise.com';
var ROOT=(document.documentElement.getAttribute('data-root')||'');
var kes=function(n){return 'KES '+Math.round(n).toLocaleString('en-KE')};
document.documentElement.classList.remove('no-js');

function toast(msg){var t=$('#toast');if(!t)return;t.textContent=msg;t.classList.add('show');clearTimeout(toast._t);toast._t=setTimeout(function(){t.classList.remove('show')},3200)}
function waLink(text){return 'https://wa.me/'+WA+'?text='+encodeURIComponent(text)}

/* ---------- header, drawer, back-to-top ---------- */
var header=$('.site-header');
function onScroll(){
  if(header)header.classList.toggle('scrolled',window.scrollY>10);
  var t=$('#top');if(t)t.classList.toggle('show',window.scrollY>700);
}
window.addEventListener('scroll',onScroll,{passive:true});onScroll();
var drawer=$('#drawer'),burger=$('#burger');
function setDrawer(o){if(!drawer)return;drawer.classList.toggle('open',o);burger.setAttribute('aria-expanded',o);document.body.style.overflow=o?'hidden':''}
if(burger){burger.addEventListener('click',function(){setDrawer(true)});
  drawer.addEventListener('click',function(e){if(e.target===drawer||e.target.closest('[data-close]')||e.target.closest('a'))setDrawer(false)});}
document.addEventListener('keydown',function(e){if(e.key==='Escape'){setDrawer(false);closeLB();var f=$('.wa-fab');if(f)f.classList.remove('open')}});
var top_=$('#top');if(top_)top_.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'})});

/* ---------- reveal on scroll ---------- */
if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -40px 0px'});
  $$('.reveal').forEach(function(el){io.observe(el)});
}else{$$('.reveal').forEach(function(el){el.classList.add('in')})}

/* ---------- counters ---------- */
var cio=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(en){
  if(!en.isIntersecting)return;cio.unobserve(en.target);
  var el=en.target,to=+el.dataset.count,suf=el.dataset.suffix||'',t0=performance.now(),d=1800;
  (function step(t){var p=Math.min((t-t0)/d,1),v=to*(1-Math.pow(1-p,3));el.textContent=Math.round(v).toLocaleString('en-KE')+suf;if(p<1)requestAnimationFrame(step)})(t0);
})},{threshold:.5}):null;
$$('[data-count]').forEach(function(el){if(cio)cio.observe(el);else el.textContent=(+el.dataset.count).toLocaleString('en-KE')+(el.dataset.suffix||'')});

/* ---------- seasonal pill + calendar highlight (UI version of the "seasonal engine") ---------- */
var SEASON=[
 ['Calving season &amp; festive getaways','packages/index.html'],['Valentine’s &amp; couples escapes','packages/couples/index.html'],
 ['Calving season value','destinations/kenya/index.html'],['Green season — value rates','packages/index.html'],
 ['Green season — value rates','packages/index.html'],['Migration is just around the corner','destinations/kenya/great-migration-safari/index.html'],
 ['Great Migration season','destinations/kenya/great-migration-safari/index.html'],['Great Migration season','destinations/kenya/great-migration-safari/index.html'],
 ['Great Migration season','destinations/kenya/great-migration-safari/index.html'],['Great Migration season','destinations/kenya/great-migration-safari/index.html'],
 ['Plan your festive escape','packages/index.html'],['Christmas &amp; New Year in the bush','packages/index.html']];
var m=new Date().getMonth();
$$('[data-season-pill]').forEach(function(el){el.innerHTML='● '+SEASON[m][0];el.setAttribute('href',ROOT+SEASON[m][1])});
$$('.mo').forEach(function(el,i){if(i===m)el.classList.add('now')});

/* ---------- hero slider ---------- */
var hs=$$('.hero-slide');
if(hs.length){
  var cur=0,dotsWrap=$('.hero-dots');
  hs.forEach(function(_,i){var b=document.createElement('button');b.setAttribute('aria-label','Slide '+(i+1));b.addEventListener('click',function(){go(i);restart()});if(dotsWrap)dotsWrap.appendChild(b)});
  var go=function(i){hs[cur].classList.remove('on');cur=(i+hs.length)%hs.length;hs[cur].classList.add('on');$$('.hero-dots button').forEach(function(b,k){b.classList.toggle('on',k===cur)})};
  var tm;var restart=function(){clearInterval(tm);tm=setInterval(function(){go(cur+1)},6500)};
  go(0);restart();
}

/* ---------- finder widget ---------- */
var finder=$('#finder');
if(finder)finder.addEventListener('submit',function(e){
  e.preventDefault();var f=new FormData(finder);
  var q='?dest='+encodeURIComponent(f.get('dest')||'')+'&tier='+encodeURIComponent(f.get('tier')||'');
  window.location.href=ROOT+'packages/index.html'+q+'#list';
});

/* ---------- generic tabs/filter (data-filter-group) ---------- */
$$('[data-tabs]').forEach(function(group){
  var target=$(group.getAttribute('data-tabs'));if(!target)return;
  group.addEventListener('click',function(e){
    var b=e.target.closest('[data-f]');if(!b)return;
    $$('[data-f]',group).forEach(function(x){x.classList.toggle('on',x===b)});
    var f=b.dataset.f;
    $$('[data-cat]',target).forEach(function(it){it.classList.toggle('hidden',!(f==='all'||it.dataset.cat.split(' ').indexOf(f)>-1))});
    $$('[data-cat]',target).forEach(function(it){it.style.display=it.classList.contains('hidden')?'none':''});
  });
});

/* ---------- packages listing: category + search + sort + URL params ---------- */
var plist=$('#pkList');
if(plist){
  var state={cat:'all',q:'',sort:'rec',tier:'midrange'};
  var qs=new URLSearchParams(location.search);
  if(qs.get('dest')){state.q=qs.get('dest')}
  if(qs.get('tier'))state.tier=qs.get('tier');
  var pre=plist.getAttribute('data-start');if(pre)state.cat=pre;
  var cards=$$('.pk-card',plist),count=$('#pkCount'),sInput=$('#pkSearch'),sSel=$('#pkSort');
  if(sInput)sInput.value=state.q;
  var apply=function(){
    var q=state.q.trim().toLowerCase(),n=0;
    cards.forEach(function(c){
      var ok=(state.cat==='all'||c.dataset.cats.split(' ').indexOf(state.cat)>-1)&&(!q||c.dataset.search.indexOf(q)>-1);
      c.style.display=ok?'':'none';if(ok)n++;
    });
    var arr=cards.slice();
    if(state.sort==='low')arr.sort(function(a,b){return a.dataset.price-b.dataset.price});
    else if(state.sort==='high')arr.sort(function(a,b){return b.dataset.price-a.dataset.price});
    else if(state.sort==='short')arr.sort(function(a,b){return a.dataset.days-b.dataset.days});
    else arr.sort(function(a,b){return a.dataset.idx-b.dataset.idx});
    arr.forEach(function(c){plist.appendChild(c)});
    var emp=$('#pkEmpty');if(emp)emp.style.display=n?'none':'';
    if(count)count.textContent=n+' journey'+(n===1?'':'s');
    $$('#pkChips [data-f]').forEach(function(b){b.classList.toggle('on',b.dataset.f===state.cat)});
  };
  $('#pkChips').addEventListener('click',function(e){var b=e.target.closest('[data-f]');if(!b)return;state.cat=b.dataset.f;apply()});
  if(sInput)sInput.addEventListener('input',function(){state.q=sInput.value;apply()});
  if(sSel)sSel.addEventListener('change',function(){state.sort=sSel.value;apply()});
  var clr=$('#pkClear');if(clr)clr.addEventListener('click',function(){state.q='';state.cat='all';if(sInput)sInput.value='';apply()});
  apply();
}

/* ---------- blog listing filter ---------- */
var blist=$('#blogList');
if(blist){
  var bs={cat:'all',q:''},posts=$$('.post',blist);
  var bapply=function(){var n=0,q=bs.q.trim().toLowerCase();
    posts.forEach(function(p){var ok=(bs.cat==='all'||p.dataset.cat===bs.cat)&&(!q||p.dataset.search.indexOf(q)>-1);p.style.display=ok?'':'none';if(ok)n++});
    var e=$('#blogEmpty');if(e)e.style.display=n?'none':'';
    $$('#blogChips [data-f]').forEach(function(b){b.classList.toggle('on',b.dataset.f===bs.cat)});};
  $('#blogChips').addEventListener('click',function(e){var b=e.target.closest('[data-f]');if(!b)return;bs.cat=b.dataset.f;bapply()});
  $('#blogSearch').addEventListener('input',function(e){bs.q=e.target.value;bapply()});
}

/* ---------- accordions (faq / itinerary) ---------- */
document.addEventListener('click',function(e){
  var b=e.target.closest('.fq > button, .it > button');if(!b)return;
  var item=b.parentElement,open=!item.classList.contains('open');
  if(item.classList.contains('fq')){$$('.fq',item.parentElement).forEach(function(x){x.classList.remove('open');x.firstElementChild.setAttribute('aria-expanded','false')})}
  item.classList.toggle('open',open);b.setAttribute('aria-expanded',open);
});
var exAll=$('#expandAll');
if(exAll)exAll.addEventListener('click',function(){var its=$$('.it'),all=its.every(function(i){return i.classList.contains('open')});its.forEach(function(i){i.classList.toggle('open',!all);i.firstElementChild.setAttribute('aria-expanded',!all)});exAll.textContent=all?'Expand all days':'Collapse all days'});

/* ---------- lightbox ---------- */
var lb=$('#lb'),lbItems=[],lbI=0;
function showLB(i){if(!lbItems.length)return;lbI=(i+lbItems.length)%lbItems.length;$('img',lb).src=lbItems[lbI].src;$('img',lb).alt=lbItems[lbI].alt;$('.cap',lb).textContent=lbItems[lbI].alt+'  •  '+(lbI+1)+' / '+lbItems.length;lb.classList.add('open');document.body.style.overflow='hidden'}
function closeLB(){if(lb&&lb.classList.contains('open')){lb.classList.remove('open');document.body.style.overflow=''}}
document.addEventListener('click',function(e){
  var t=e.target.closest('[data-lb]');
  if(t){var grp=t.getAttribute('data-lb');lbItems=$$('[data-lb="'+grp+'"]').filter(function(x){return x.offsetParent!==null}).map(function(x){var im=$('img',x);return {src:im.dataset.full||im.currentSrc||im.src,alt:im.alt}});
    var idx=$$('[data-lb="'+grp+'"]').filter(function(x){return x.offsetParent!==null}).indexOf(t);showLB(idx);return}
  if(!lb)return;
  if(e.target.closest('.x')||e.target===lb)closeLB();
  else if(e.target.closest('.pv'))showLB(lbI-1);else if(e.target.closest('.nx'))showLB(lbI+1);
});
document.addEventListener('keydown',function(e){if(lb&&lb.classList.contains('open')){if(e.key==='ArrowLeft')showLB(lbI-1);if(e.key==='ArrowRight')showLB(lbI+1)}});

/* ---------- testimonials ---------- */
var tq=$('#tq');
if(tq){
  var T=JSON.parse($('#tdata').textContent),ti=0;
  var render=function(){var t=T[ti];$('#tq').textContent=t.quote;$('#tn').textContent=t.name;$('#td').textContent=t.role;var im=$('#tim');if(im&&t.img)im.src=t.img};
  $('#tprev').addEventListener('click',function(){ti=(ti-1+T.length)%T.length;render()});
  $('#tnext').addEventListener('click',function(){ti=(ti+1)%T.length;render()});
  setInterval(function(){ti=(ti+1)%T.length;render()},9000);render();
}

/* ---------- WhatsApp quick-chat widget ---------- */
var fab=$('.wa-fab');
if(fab){
  $('.wa-btn',fab).addEventListener('click',function(){fab.classList.toggle('open')});
  document.addEventListener('click',function(e){if(!e.target.closest('.wa-fab'))fab.classList.remove('open')});
}

/* ---------- cookie notice ---------- */
var ck=$('#cookie');
if(ck){var seen=null;try{seen=localStorage.getItem('pop-cookie')}catch(e){}
  if(!seen)setTimeout(function(){ck.classList.add('show')},1800);
  ck.addEventListener('click',function(e){var b=e.target.closest('[data-ck]');if(!b)return;try{localStorage.setItem('pop-cookie',b.dataset.ck)}catch(e){}ck.classList.remove('show')});}

/* ---------- newsletter (mailto fallback — no backend in this UI build) ---------- */
var nl=$('#newsForm');
if(nl)nl.addEventListener('submit',function(e){e.preventDefault();var v=$('input',nl).value.trim();
  if(!/^\S+@\S+\.\S+$/.test(v)){toast('Please enter a valid email address.');return}
  window.location.href='mailto:'+EMAIL+'?subject='+encodeURIComponent('Subscribe me to travel updates')+'&body='+encodeURIComponent('Please add '+v+' to your travel updates list.');
  toast('Opening your email app to confirm…');});

/* ---------- package booking card / estimator ---------- */
var book=$('#book');
if(book){
  var P=JSON.parse($('#pdata').textContent),tier=P.defaultTier,pax=2;
  var set=function(){
    var t=P.tiers[tier];
    $('#bPrice').textContent=kes(t.price);
    $('#bTierName').textContent=t.label+(t.stay?' · '+t.stay:'');
    $('#bEst').textContent=kes(t.price*pax);
    $('#bPax').textContent=pax;
    $$('.tier').forEach(function(b){b.classList.toggle('on',b.dataset.k===tier)});
    $('#bTier').value=tier;
    var msg='Hi Pocket of Paradise! I’d like a quote for "'+P.title+'" ('+t.label+', '+pax+' traveller'+(pax>1?'s':'')+')'+($('#bMonth').value?' in '+$('#bMonth').value:'')+'. Estimated '+kes(t.price*pax)+'.';
    $('#bWa').href=waLink(msg);
    $('#bQuote').href=ROOT+'create-tour-plan/index.html?package='+P.id+'&tier='+tier+'&pax='+pax+($('#bMonth').value?'&month='+encodeURIComponent($('#bMonth').value):'');
    var mb=$('#mbQuote');if(mb)mb.href=$('#bQuote').href;
    var mp=$('#mbPrice');if(mp)mp.textContent=kes(t.price);
  };
  $$('.tier').forEach(function(b){b.addEventListener('click',function(){tier=b.dataset.k;set()})});
  $('#bTier').addEventListener('change',function(e){tier=e.target.value;set()});
  $('#bMonth').addEventListener('change',set);
  $('#bMinus').addEventListener('click',function(){pax=Math.max(1,pax-1);set()});
  $('#bPlus').addEventListener('click',function(){pax=Math.min(20,pax+1);set()});
  set();
  document.body.classList.add('has-mbar');
}

/* ---------- share / copy ---------- */
document.addEventListener('click',function(e){
  var c=e.target.closest('[data-copy]');
  if(c){var u=location.href;(navigator.clipboard?navigator.clipboard.writeText(u):Promise.reject()).then(function(){toast('Link copied')}).catch(function(){toast(u)})}
  var p=e.target.closest('[data-print]');if(p)window.print();
});

/* ---------- multi-step enquiry (create-tour-plan) + contact form ---------- */
function monthOptions(sel){
  if(!sel)return;var d=new Date(),out='<option value="">Select month…</option>';
  var names=['January','February','March','April','May','June','July','August','September','October','November','December'];
  for(var i=0;i<24;i++){var x=new Date(d.getFullYear(),d.getMonth()+i,1);var v=names[x.getMonth()]+' '+x.getFullYear();out+='<option>'+v+'</option>'}
  sel.innerHTML=out;
}
$$('select[data-months]').forEach(monthOptions);

var plan=$('#plan');
if(plan){
  var steps=$$('.fs',plan),pbars=$$('#prog span'),si=0,qp=new URLSearchParams(location.search);
  var show=function(i){si=i;steps.forEach(function(s,k){s.classList.toggle('on',k===i)});pbars.forEach(function(b,k){b.classList.toggle('on',k<=i)});$('#stepNo').textContent='STEP '+(i+1)+' OF '+steps.length;window.scrollTo({top:plan.getBoundingClientRect().top+window.scrollY-110,behavior:'smooth'});if(i===steps.length-1)summary()};
  var val=function(n){var el=plan.elements[n];if(!el)return '';if(el.length&&el[0]&&el[0].type==='radio'){var r=plan.querySelector('input[name="'+n+'"]:checked');return r?r.value:''}return (el.value||'').trim()};
  var checked=function(n){return $$('input[name="'+n+'"]:checked',plan).map(function(x){return x.value}).join(', ')};
  var validate=function(i){
    var ok=true;$$('[data-req]',steps[i]).forEach(function(f){
      var wrap=f.closest('.fld'),v=(f.value||'').trim(),bad=!v;
      if(f.type==='email'&&v&&!/^\S+@\S+\.\S+$/.test(v))bad=true;
      if(f.type==='tel'&&v&&v.replace(/[^\d]/g,'').length<9)bad=true;
      if(f.type==='checkbox')bad=!f.checked;
      f.classList.toggle('bad',bad);wrap.classList.toggle('has-err',bad);if(bad)ok=false});
    if(!ok)toast('Please complete the highlighted fields.');return ok};
  plan.addEventListener('click',function(e){
    if(e.target.closest('[data-next]')){if(validate(si))show(si+1)}
    if(e.target.closest('[data-prev]'))show(si-1);
  });
  var buildMsg=function(){
    var L=['*New trip enquiry — Pocket of Paradise website*','',
      'Name: '+val('name'),'Phone/WhatsApp: '+val('phone'),'Email: '+val('email'),
      'Preferred contact: '+(val('channel')||'WhatsApp')+(val('besttime')?' ('+val('besttime')+')':''),'',
      'Package: '+(plan.elements.package.options[plan.elements.package.selectedIndex].text),
      'Interested in: '+(checked('interest')||'Not specified'),
      'Comfort level: '+(val('comfort')||'Not sure yet'),
      'Travel month: '+(val('month')||'Flexible')+(plan.elements.flex.checked?' (dates flexible)':''),
      'Trip length: '+(val('length')||'Not specified'),
      'Travellers: '+val('adults')+' adult(s), '+(val('children')||0)+' child(ren)',
      'Travel style: '+(val('style')||'Not specified'),
      'Budget per person: '+(val('budget')||'Not specified'),'',
      'Notes: '+(val('notes')||'—')];
    return L.join('\n')};
  var summary=function(){
    var rows=[['Package',plan.elements.package.options[plan.elements.package.selectedIndex].text],['Comfort',val('comfort')||'Not sure yet'],['When',(val('month')||'Flexible')+(plan.elements.flex.checked?' (flexible)':'')],['Travellers',val('adults')+' adult(s), '+(val('children')||0)+' child(ren)'],['Budget / person',val('budget')||'Not specified'],['Name',val('name')],['Contact',(val('channel')||'WhatsApp')+' · '+val('phone')]];
    $('#sum').innerHTML=rows.map(function(r){return '<dt>'+r[0]+'</dt><dd>'+r[1].replace(/</g,'&lt;')+'</dd>'}).join('');
    $('#sendWa').href=waLink(buildMsg());
    $('#sendMail').href='mailto:'+EMAIL+'?subject='+encodeURIComponent('Trip enquiry from '+val('name'))+'&body='+encodeURIComponent(buildMsg());
  };
  var n=$('#notes');if(n)n.addEventListener('input',function(){$('#ncnt').textContent=n.value.length+'/300 characters'});
  $('#copyMsg').addEventListener('click',function(){(navigator.clipboard?navigator.clipboard.writeText(buildMsg()):Promise.reject()).then(function(){toast('Enquiry copied')}).catch(function(){toast('Copy not available')})});
  // prefill from URL
  if(qp.get('package')){var o=plan.elements.package;for(var k=0;k<o.options.length;k++)if(o.options[k].value===qp.get('package'))o.selectedIndex=k}
  var tmap={budget:'Budget',midrange:'Mid-range',luxury:'Luxury'};
  if(qp.get('tier')&&tmap[qp.get('tier')]){var r=plan.querySelector('input[name="comfort"][value="'+tmap[qp.get('tier')]+'"]');if(r)r.checked=true}
  if(qp.get('pax'))plan.elements.adults.value=qp.get('pax');
  if(qp.get('month')){var mm=plan.elements.month;for(var j=0;j<mm.options.length;j++)if(mm.options[j].value===qp.get('month'))mm.selectedIndex=j}
  show(0);window.scrollTo(0,0);
}

var cform=$('#contactForm');
if(cform)cform.addEventListener('submit',function(e){
  e.preventDefault();var ok=true;
  $$('[data-req]',cform).forEach(function(f){var v=(f.value||'').trim(),bad=!v;if(f.type==='email'&&v&&!/^\S+@\S+\.\S+$/.test(v))bad=true;if(f.type==='checkbox')bad=!f.checked;f.classList.toggle('bad',bad);f.closest('.fld').classList.toggle('has-err',bad);if(bad)ok=false});
  if(!ok){toast('Please complete the highlighted fields.');return}
  var g=function(n){return (cform.elements[n].value||'').trim()};
  var msg='*Website enquiry — Pocket of Paradise*\n\nName: '+g('name')+'\nEmail: '+g('email')+'\nPhone: '+g('phone')+'\nTopic: '+g('topic')+'\nPrefers: '+g('channel')+'\n\n'+g('message');
  $('#cWa').href=waLink(msg);$('#cMail').href='mailto:'+EMAIL+'?subject='+encodeURIComponent(g('topic')+' — '+g('name'))+'&body='+encodeURIComponent(msg);
  $('#cSend').hidden=false;cform.querySelector('[type=submit]').hidden=true;toast('Almost done — choose how to send it.');
});

/* ---------- image fallback (broken images get a branded placeholder) ---------- */
document.addEventListener('error',function(e){var t=e.target;if(t&&t.tagName==='IMG'&&!t.dataset.fb){t.dataset.fb=1;t.style.visibility='hidden'}},true);
})();
