/* ===== Scholar Voice — Shared JS ===== */

const POSTS = [
  {
    id: 'graduation-2026',
    category: 'Graduation',
    title: 'Class of 2026 Graduation Ceremony: Dates & Schedule Announced',
    excerpt: 'The Office of the Registrar is pleased to announce the official graduation schedule, dress code, and rehearsal dates for the outgoing Class of 2026.',
    author: 'Office of the Registrar',
    date: '2026-06-08',
    readTime: '5 min',
    image: 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1200&q=80',
    featured: true,
    content: `
      <p>The Office of the Registrar, together with the Vice Chancellor's office, is pleased to officially announce the graduation programme for the Class of 2026. After four remarkable years marked by academic excellence, resilience and community service, we look forward to celebrating the achievements of more than 2,400 graduating students.</p>
      <h2>Ceremony Schedule</h2>
      <ul>
        <li><strong>Friday, 17 July 2026</strong> — Graduation rehearsal, Main Auditorium, 9:00 AM</li>
        <li><strong>Saturday, 18 July 2026</strong> — Faculty of Science & Engineering ceremony, 10:00 AM</li>
        <li><strong>Sunday, 19 July 2026</strong> — Faculty of Arts, Business & Social Sciences ceremony, 10:00 AM</li>
      </ul>
      <blockquote>"This is more than a milestone — it is a recognition of every late night, every revision, every act of courage you have shown."</blockquote>
      <h2>Dress Code & Gown Collection</h2>
      <p>Graduating students may collect their gowns from the Student Affairs office between 1–15 July upon presentation of valid student identification and clearance form. Strict adherence to academic dress code is required.</p>
      <h2>Tickets for Family</h2>
      <p>Each graduand will receive two complimentary tickets for family members. Additional tickets may be requested via the student portal subject to seating availability.</p>
    `,
  },
  {
    id: 'scholarship-2026',
    category: 'Scholarships',
    title: 'Merit Scholarship Applications Now Open for 2026/2027 Academic Year',
    excerpt: 'Up to 150 fully-funded scholarships available for outstanding returning and incoming students across all faculties.',
    author: 'Financial Aid Office',
    date: '2026-06-05',
    readTime: '4 min',
    image: 'https://images.unsplash.com/photo-1606761568499-6d2451b23c66?w=1200&q=80',
    content: `
      <p>The institution is delighted to announce that applications for the 2026/2027 Merit and Need-Based Scholarship Programme are now officially open. This year, the scholarship pool has been expanded to 150 awards thanks to the generosity of our alumni network and corporate partners.</p>
      <h2>Eligibility</h2>
      <ul>
        <li>Minimum CGPA of 3.5 (returning students) or 3.7 secondary school average (new applicants)</li>
        <li>Demonstrated leadership or community service involvement</li>
        <li>Complete application submitted before <strong>30 June 2026</strong></li>
      </ul>
      <p>All shortlisted candidates will be invited for an interview during the first week of July. Awards will be announced before the start of the new academic year.</p>
    `,
  },
  {
    id: 'library-extended-hours',
    category: 'Campus Life',
    title: 'Central Library Extends Operating Hours During Exam Period',
    excerpt: 'To support students preparing for end-of-semester examinations, the Central Library will operate 24/7 starting 15 June.',
    author: 'University Library',
    date: '2026-06-04',
    readTime: '2 min',
    image: 'https://images.unsplash.com/photo-1568667256549-094345857637?w=1200&q=80',
    content: `
      <p>In response to overwhelming student requests, the University Library will operate on a 24-hour schedule from 15 June through 5 July 2026 to accommodate exam preparation. Quiet study zones, group rooms and digital resource terminals will all be available round the clock. A valid student ID is required for entry after 10:00 PM.</p>
      <p>Complimentary tea, coffee and biscuits will be served between midnight and 4:00 AM, courtesy of the Student Welfare Committee.</p>
    `,
  },
  {
    id: 'tech-symposium',
    category: 'Events',
    title: 'Annual Tech Symposium 2026: AI, Robotics & The Future of Learning',
    excerpt: 'Join industry leaders, alumni and faculty for two days of keynote talks, workshops and student innovation showcases.',
    author: 'Faculty of Engineering',
    date: '2026-06-02',
    readTime: '6 min',
    image: 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1200&q=80',
    content: `
      <p>The Faculty of Engineering is proud to host the 8th Annual Tech Symposium on <strong>12–13 July 2026</strong>. This year's theme — <em>AI, Robotics &amp; The Future of Learning</em> — brings together more than 40 speakers from leading technology companies, research institutions and our distinguished alumni community.</p>
      <h2>Highlights</h2>
      <ul>
        <li>Opening keynote by a Fortune 500 CTO</li>
        <li>Student innovation showcase with $10,000 in prizes</li>
        <li>Hands-on workshops in machine learning, robotics and product design</li>
        <li>Career fair with 30+ recruiting partners</li>
      </ul>
      <p>Registration is free for all enrolled students. Sign up via the student portal before 5 July.</p>
    `,
  },
  {
    id: 'student-elections',
    category: 'Announcements',
    title: 'Student Government Elections: Nominations Open',
    excerpt: 'All registered students are invited to nominate themselves or peers for the 2026/2027 Student Representative Council.',
    author: 'Dean of Students',
    date: '2026-05-30',
    readTime: '3 min',
    image: 'https://images.unsplash.com/photo-1577896851231-70ef18881754?w=1200&q=80',
    content: `
      <p>Nominations for the Student Representative Council (SRC) are now open. The SRC is the official voice of the student body and works directly with university leadership on academic, welfare and policy matters.</p>
      <h2>Positions Available</h2>
      <ul>
        <li>President &amp; Vice President</li>
        <li>Secretary General</li>
        <li>Treasurer</li>
        <li>Faculty Representatives (one per faculty)</li>
      </ul>
      <p>Submit nominations to the Dean of Students office before 20 June 2026. Election week begins 1 July.</p>
    `,
  },
  {
    id: 'sports-week',
    category: 'Sports',
    title: 'Inter-Faculty Sports Week Concludes With Record Participation',
    excerpt: 'Over 1,800 students from all six faculties competed across 14 disciplines during this year\'s most spirited sports week to date.',
    author: 'Sports Department',
    date: '2026-05-28',
    readTime: '4 min',
    image: 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=1200&q=80',
    content: `
      <p>This year's Inter-Faculty Sports Week wrapped up on Sunday evening with the Faculty of Engineering taking home the overall championship trophy for the third year running. With over 1,800 student-athletes participating across 14 sporting disciplines, this was the largest and most competitive edition to date.</p>
      <p>Special recognition goes to the Faculty of Arts for the Spirit Award and to all student volunteers, medical teams and officials who made the week possible.</p>
    `,
  },
];

const CATEGORIES = ['All', 'Graduation', 'Scholarships', 'Campus Life', 'Events', 'Announcements', 'Sports'];

/* ===== Helpers ===== */
function formatDate(iso) {
  return new Date(iso).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}
function timeAgo(iso) {
  const diff = (Date.now() - new Date(iso).getTime()) / 1000;
  if (diff < 60) return 'just now';
  if (diff < 3600) return `${Math.floor(diff/60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff/3600)}h ago`;
  if (diff < 604800) return `${Math.floor(diff/86400)}d ago`;
  return formatDate(iso);
}
function initials(name) {
  return name.split(' ').map(w => w[0]).slice(0,2).join('').toUpperCase();
}
function toast(msg, type = '') {
  let el = document.querySelector('.toast');
  if (!el) {
    el = document.createElement('div');
    el.className = 'toast';
    document.body.appendChild(el);
  }
  el.className = 'toast ' + type;
  el.textContent = msg;
  requestAnimationFrame(() => el.classList.add('show'));
  clearTimeout(el._t);
  el._t = setTimeout(() => el.classList.remove('show'), 3200);
}

/* ===== Mobile Menu ===== */
function initMobileMenu() {
  const toggle = document.querySelector('.menu-toggle');
  const links = document.querySelector('.nav-links');
  if (!toggle || !links) return;
  toggle.addEventListener('click', () => links.classList.toggle('open'));
}

/* ===== Auth Header State ===== */
function getUser() {
  try { return JSON.parse(localStorage.getItem('sv_user') || 'null'); }
  catch { return null; }
}
function setUser(u) { localStorage.setItem('sv_user', JSON.stringify(u)); }
function logout() { localStorage.removeItem('sv_user'); location.reload(); }

function renderAuthButton() {
  const slot = document.querySelector('[data-auth-slot]');
  if (!slot) return;
  const u = getUser();
  if (u) {
    slot.innerHTML = `
      <div class="avatar" style="width:36px;height:36px;font-size:13px" title="${u.name}">${initials(u.name)}</div>
      <button class="btn btn-ghost" id="logoutBtn">Sign out</button>
    `;
    document.getElementById('logoutBtn').addEventListener('click', logout);
  } else {
    slot.innerHTML = `<a href="auth.html" class="btn btn-primary">Sign in</a>`;
  }
}

/* ===== Listing Page ===== */
function renderListing() {
  const grid = document.getElementById('postsGrid');
  const featuredWrap = document.getElementById('featuredWrap');
  const filters = document.getElementById('filters');
  const search = document.getElementById('searchInput');
  if (!grid) return;

  // filters
  CATEGORIES.forEach((c, i) => {
    const b = document.createElement('button');
    b.className = 'chip' + (i === 0 ? ' active' : '');
    b.textContent = c;
    b.dataset.cat = c;
    b.addEventListener('click', () => {
      document.querySelectorAll('.chip').forEach(x => x.classList.remove('active'));
      b.classList.add('active');
      render();
    });
    filters.appendChild(b);
  });

  // featured
  const f = POSTS.find(p => p.featured);
  if (f && featuredWrap) {
    featuredWrap.innerHTML = `
      <article class="featured">
        <div class="featured-img"><img src="${f.image}" alt="${f.title}" loading="lazy"></div>
        <div class="featured-body">
          <span class="tag">Featured · ${f.category}</span>
          <h2>${f.title}</h2>
          <p>${f.excerpt}</p>
          <div class="card-meta">
            <div class="avatar" style="width:32px;height:32px;font-size:12px">${initials(f.author)}</div>
            <span><strong style="color:var(--navy)">${f.author}</strong></span>
            <span class="sep"></span>
            <span>${formatDate(f.date)}</span>
            <span class="sep"></span>
            <span>${f.readTime} read</span>
          </div>
          <a href="post.html?id=${f.id}" class="btn btn-primary" style="width:fit-content;margin-top:6px">
            Read full story →
          </a>
        </div>
      </article>
    `;
  }

  function render() {
    const cat = document.querySelector('.chip.active')?.dataset.cat || 'All';
    const q = (search?.value || '').toLowerCase().trim();
    const list = POSTS.filter(p => {
      if (cat !== 'All' && p.category !== cat) return false;
      if (q && !(p.title.toLowerCase().includes(q) || p.excerpt.toLowerCase().includes(q))) return false;
      return true;
    });
    if (!list.length) {
      grid.innerHTML = `<div class="empty" style="grid-column:1/-1"><h4>No posts found</h4><p>Try a different category or search term.</p></div>`;
      return;
    }
    grid.innerHTML = list.map((p, i) => `
      <article class="card" style="animation-delay:${i * 70}ms">
        <a href="post.html?id=${p.id}" class="card-img">
          <span class="card-cat">${p.category}</span>
          <img src="${p.image}" alt="${p.title}" loading="lazy">
        </a>
        <div class="card-body">
          <div class="card-meta">
            <span>${formatDate(p.date)}</span>
            <span class="sep"></span>
            <span>${p.readTime} read</span>
          </div>
          <h3><a href="post.html?id=${p.id}">${p.title}</a></h3>
          <p>${p.excerpt}</p>
          <div class="card-foot">
            <div class="card-meta">
              <div class="avatar" style="width:28px;height:28px;font-size:11px">${initials(p.author)}</div>
              <span>${p.author}</span>
            </div>
            <a href="post.html?id=${p.id}" class="read-more">Read more →</a>
          </div>
        </div>
      </article>
    `).join('');
  }

  search?.addEventListener('input', render);
  render();

  // newsletter
  document.getElementById('newsletterForm')?.addEventListener('submit', e => {
    e.preventDefault();
    e.target.reset();
    toast('Subscribed — updates coming straight to your phone.', 'success');
  });
}

/* ===== Detail Page ===== */
function renderDetail() {
  const root = document.getElementById('articleRoot');
  if (!root) return;
  const id = new URLSearchParams(location.search).get('id') || POSTS[0].id;
  const p = POSTS.find(x => x.id === id) || POSTS[0];

  document.title = `${p.title} — Scholar Voice`;

  root.innerHTML = `
    <a href="index.html" class="back-link">← Back to all posts</a>
    <article class="article">
      <div class="article-hero"><img src="${p.image}" alt="${p.title}"></div>
      <span class="tag">${p.category}</span>
      <h1>${p.title}</h1>
      <div class="article-meta">
        <div class="avatar">${initials(p.author)}</div>
        <div class="author-info">
          <span class="author-name">${p.author}</span>
          <span>${formatDate(p.date)} · ${p.readTime} read</span>
        </div>
      </div>
      <div class="article-body">${p.content}</div>
      <div class="share-bar">
        <span>Share:</span>
        <button class="icon-btn" data-share="twitter" title="Share on X">𝕏</button>
        <button class="icon-btn" data-share="facebook" title="Share on Facebook">f</button>
        <button class="icon-btn" data-share="linkedin" title="Share on LinkedIn">in</button>
        <button class="icon-btn" data-share="copy" title="Copy link">🔗</button>
      </div>
    </article>

    <section class="comments">
      <h3 id="commentsTitle">Comments</h3>
      <div class="comment-form">
        <div class="form-row two">
          <div><label class="label">Your name</label><input class="input" id="cName" placeholder="Jane Doe" value="${getUser()?.name || ''}"></div>
          <div><label class="label">Email (private)</label><input class="input" id="cEmail" placeholder="jane@school.edu" value="${getUser()?.email || ''}"></div>
        </div>
        <div class="form-row">
          <div><label class="label">Your comment</label><textarea class="textarea" id="cBody" placeholder="Share your thoughts respectfully..."></textarea></div>
        </div>
        <button class="btn btn-primary" id="postComment">Post comment</button>
      </div>
      <div class="comment-list" id="commentList"></div>
    </section>

    <section style="margin-top:60px">
      <div class="section-head"><div><h2 class="section-title">Continue reading</h2><p class="section-sub">More from your institution</p></div></div>
      <div class="grid" id="relatedGrid"></div>
    </section>
  `;

  // share buttons
  root.querySelectorAll('[data-share]').forEach(btn => {
    btn.addEventListener('click', () => {
      const url = location.href;
      const text = encodeURIComponent(p.title);
      const u = encodeURIComponent(url);
      const map = {
        twitter: `https://twitter.com/intent/tweet?text=${text}&url=${u}`,
        facebook: `https://facebook.com/sharer/sharer.php?u=${u}`,
        linkedin: `https://linkedin.com/sharing/share-offsite/?url=${u}`,
      };
      const t = btn.dataset.share;
      if (t === 'copy') { navigator.clipboard.writeText(url); toast('Link copied to clipboard', 'success'); }
      else window.open(map[t], '_blank', 'noopener,width=600,height=540');
    });
  });

  // related
  const related = POSTS.filter(x => x.id !== p.id).slice(0, 3);
  document.getElementById('relatedGrid').innerHTML = related.map((r, i) => `
    <article class="card" style="animation-delay:${i*80}ms">
      <a href="post.html?id=${r.id}" class="card-img">
        <span class="card-cat">${r.category}</span>
        <img src="${r.image}" alt="${r.title}" loading="lazy">
      </a>
      <div class="card-body">
        <div class="card-meta"><span>${formatDate(r.date)}</span><span class="sep"></span><span>${r.readTime}</span></div>
        <h3><a href="post.html?id=${r.id}">${r.title}</a></h3>
        <p>${r.excerpt}</p>
        <div class="card-foot"><span></span><a href="post.html?id=${r.id}" class="read-more">Read more →</a></div>
      </div>
    </article>
  `).join('');

  initComments(p.id);
}

/* ===== Comments ===== */
function getComments(postId) {
  try { return JSON.parse(localStorage.getItem('sv_comments_' + postId) || '[]'); }
  catch { return []; }
}
function saveComments(postId, list) {
  localStorage.setItem('sv_comments_' + postId, JSON.stringify(list));
}

function initComments(postId) {
  const list = document.getElementById('commentList');
  const title = document.getElementById('commentsTitle');

  function render() {
    const comments = getComments(postId);
    title.textContent = `Comments (${countAll(comments)})`;
    if (!comments.length) {
      list.innerHTML = `<div class="empty"><h4>Be the first to comment</h4><p>Start the conversation about this post.</p></div>`;
      return;
    }
    list.innerHTML = comments.map(c => commentHTML(c)).join('');
    bindActions();
  }

  function countAll(arr) {
    return arr.reduce((n, c) => n + 1 + (c.replies?.length || 0), 0);
  }

  function commentHTML(c, isReply = false) {
    return `
      <div class="comment" data-id="${c.id}">
        <div class="comment-head">
          <div class="avatar">${initials(c.name)}</div>
          <div>
            <div class="comment-name">${c.name}</div>
            <div class="comment-time">${timeAgo(c.date)}</div>
          </div>
        </div>
        <div class="comment-body">${escapeHTML(c.body)}</div>
        <div class="comment-actions">
          <button class="like-btn ${c.liked ? 'liked' : ''}" data-id="${c.id}">♥ <span>${c.likes || 0}</span></button>
          ${!isReply ? `<button class="reply-btn" data-id="${c.id}">↩ Reply</button>` : ''}
        </div>
        ${!isReply ? `
          <form class="reply-form" data-id="${c.id}">
            <div class="form-row two" style="margin-top:12px">
              <input class="input reply-name" placeholder="Your name" value="${getUser()?.name || ''}">
              <input class="input reply-email" placeholder="Email">
            </div>
            <textarea class="textarea reply-body" placeholder="Write a reply..."></textarea>
            <button type="submit" class="btn btn-primary" style="margin-top:10px">Post reply</button>
          </form>
        ` : ''}
        ${c.replies?.length ? `<div class="replies">${c.replies.map(r => commentHTML(r, true)).join('')}</div>` : ''}
      </div>
    `;
  }

  function bindActions() {
    list.querySelectorAll('.like-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.dataset.id;
        const comments = getComments(postId);
        const c = findComment(comments, id);
        if (!c) return;
        c.liked = !c.liked;
        c.likes = (c.likes || 0) + (c.liked ? 1 : -1);
        saveComments(postId, comments);
        render();
      });
    });
    list.querySelectorAll('.reply-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const form = list.querySelector(`.reply-form[data-id="${btn.dataset.id}"]`);
        form.classList.toggle('open');
      });
    });
    list.querySelectorAll('.reply-form').forEach(form => {
      form.addEventListener('submit', e => {
        e.preventDefault();
        const id = form.dataset.id;
        const name = form.querySelector('.reply-name').value.trim();
        const body = form.querySelector('.reply-body').value.trim();
        if (!name || !body) { toast('Please add your name and a reply', 'error'); return; }
        const comments = getComments(postId);
        const c = comments.find(x => x.id === id);
        if (!c) return;
        c.replies = c.replies || [];
        c.replies.push({ id: crypto.randomUUID(), name, body, date: new Date().toISOString(), likes: 0 });
        saveComments(postId, comments);
        render();
        toast('Reply posted', 'success');
      });
    });
  }

  function findComment(arr, id) {
    for (const c of arr) {
      if (c.id === id) return c;
      if (c.replies) {
        const r = c.replies.find(x => x.id === id);
        if (r) return r;
      }
    }
  }

  document.getElementById('postComment').addEventListener('click', () => {
    const name = document.getElementById('cName').value.trim();
    const body = document.getElementById('cBody').value.trim();
    if (!name || !body) { toast('Please add your name and a comment', 'error'); return; }
    const comments = getComments(postId);
    comments.unshift({ id: crypto.randomUUID(), name, body, date: new Date().toISOString(), likes: 0, replies: [] });
    saveComments(postId, comments);
    document.getElementById('cBody').value = '';
    render();
    toast('Comment posted', 'success');
  });

  render();
}

function escapeHTML(s) {
  return s.replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
}

/* ===== Auth Page ===== */
function initAuth() {
  const tabs = document.querySelectorAll('.auth-tab');
  const panels = document.querySelectorAll('.tab-panel');
  if (!tabs.length) return;

  // tab from hash
  const initial = location.hash.replace('#','') || 'login';
  switchTab(initial);

  tabs.forEach(t => t.addEventListener('click', () => switchTab(t.dataset.tab)));

  function switchTab(name) {
    tabs.forEach(t => t.classList.toggle('active', t.dataset.tab === name));
    panels.forEach(p => p.classList.toggle('active', p.dataset.panel === name));
  }

  document.getElementById('loginForm').addEventListener('submit', e => {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value.trim();
    const name = email.split('@')[0].replace(/[._]/g,' ').replace(/\b\w/g, c => c.toUpperCase());
    setUser({ name, email });
    toast('Welcome back! Redirecting...', 'success');
    setTimeout(() => location.href = 'index.html', 900);
  });

  document.getElementById('registerForm').addEventListener('submit', e => {
    e.preventDefault();
    const name = document.getElementById('regName').value.trim();
    const email = document.getElementById('regEmail').value.trim();
    const pwd = document.getElementById('regPassword').value;
    const pwd2 = document.getElementById('regPassword2').value;
    if (pwd !== pwd2) { toast('Passwords do not match', 'error'); return; }
    if (pwd.length < 6) { toast('Password must be at least 6 characters', 'error'); return; }
    setUser({ name, email });
    toast('Account created! Welcome to Scholar Voice.', 'success');
    setTimeout(() => location.href = 'index.html', 1000);
  });
}

/* ===== Boot ===== */
document.addEventListener('DOMContentLoaded', () => {
  initMobileMenu();
  renderAuthButton();
  renderListing();
  renderDetail();
  initAuth();
});
