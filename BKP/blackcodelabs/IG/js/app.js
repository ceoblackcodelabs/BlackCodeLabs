// ===== LOOPSTA APP JS =====

// Fake avatar images using picsum
const avatars = [
  'https://i.pravatar.cc/150?img=1','https://i.pravatar.cc/150?img=2',
  'https://i.pravatar.cc/150?img=3','https://i.pravatar.cc/150?img=4',
  'https://i.pravatar.cc/150?img=5','https://i.pravatar.cc/150?img=6',
  'https://i.pravatar.cc/150?img=7','https://i.pravatar.cc/150?img=8',
  'https://i.pravatar.cc/150?img=9','https://i.pravatar.cc/150?img=10',
  'https://i.pravatar.cc/150?img=11','https://i.pravatar.cc/150?img=12',
];

const postImages = [
  'https://picsum.photos/seed/loop1/600/600',
  'https://picsum.photos/seed/loop2/600/600',
  'https://picsum.photos/seed/loop3/600/600',
  'https://picsum.photos/seed/loop4/600/600',
  'https://picsum.photos/seed/loop5/600/600',
  'https://picsum.photos/seed/loop6/600/800',
  'https://picsum.photos/seed/loop7/600/600',
  'https://picsum.photos/seed/loop8/800/600',
  'https://picsum.photos/seed/loop9/600/600',
  'https://picsum.photos/seed/loop10/600/600',
  'https://picsum.photos/seed/loop11/600/600',
  'https://picsum.photos/seed/loop12/600/600',
];

const users = [
  { name: 'Zara Osei', handle: 'zara.osei', role: 'creator', verified: true, avatar: avatars[0], followers: '128K' },
  { name: 'Kemi Adeleke', handle: 'kemi_creates', role: 'creator', verified: true, avatar: avatars[1], followers: '89K' },
  { name: 'Jabari Mensah', handle: 'jabari_m', role: 'user', verified: false, avatar: avatars[2], followers: '3.2K' },
  { name: 'Nia Carter', handle: 'nia.carter', role: 'creator', verified: true, avatar: avatars[3], followers: '201K' },
  { name: 'Tolu Obi', handle: 'tolu_obi', role: 'user', verified: false, avatar: avatars[4], followers: '890' },
  { name: 'Chidi Eze', handle: 'chidi_eze', role: 'creator', verified: false, avatar: avatars[5], followers: '45K' },
  { name: 'Aisha Diallo', handle: 'aisha.d', role: 'user', verified: false, avatar: avatars[6], followers: '1.1K' },
  { name: 'Kwame Asante', handle: 'kwame_a', role: 'creator', verified: true, avatar: avatars[7], followers: '320K' },
];

const captions = [
  'Golden hour hits different when you\'re in the zone ✨ <span class="hashtag">#photography</span> <span class="hashtag">#goldenhour</span> <span class="hashtag">#loopsta</span>',
  'New collection just dropped 🔥 Everything curated with love. <span class="hashtag">#fashion</span> <span class="hashtag">#style</span> <span class="hashtag">#creator</span>',
  'Weekend vibes only 🌿 <span class="hashtag">#lifestyle</span> <span class="hashtag">#weekend</span>',
  'Building something incredible one frame at a time 📸 <span class="hashtag">#art</span> <span class="hashtag">#creative</span> <span class="hashtag">#loopsta</span>',
  'This view never gets old 🌅 <span class="hashtag">#travel</span> <span class="hashtag">#sunsets</span> <span class="hashtag">#explore</span>',
  'Consistency is the new talent 💪 Keep creating! <span class="hashtag">#motivation</span> <span class="hashtag">#grind</span>',
  'Food is art and art is food 🍜 <span class="hashtag">#foodie</span> <span class="hashtag">#foodphotography</span>',
  'Late night thoughts and city lights ✨ <span class="hashtag">#nightlife</span> <span class="hashtag">#city</span>',
];

const times = ['2m','14m','1h','2h','5h','8h','12h','1d','2d'];
const likesCounts = [1203,892,4501,12800,234,7890,456,23100,1567,88];
const commentCounts = [43,17,201,892,9,445,32,1203,78,5];

// Current user state
const currentUser = {
  name: 'Alex Kamau',
  handle: 'alex.kamau',
  role: 'creator',
  avatar: 'https://i.pravatar.cc/150?img=13',
  followers: '12.4K',
  following: 389,
  posts: 147
};

let likedPosts = new Set();
let savedPosts = new Set();
let followedUsers = new Set();

// ===== NAVIGATION =====
function navigate(pageId) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.querySelectorAll('.bottom-nav-item').forEach(n => n.classList.remove('active'));

  const page = document.getElementById('page-' + pageId);
  if (page) page.classList.add('active');

  document.querySelectorAll(`[data-page="${pageId}"]`).forEach(el => el.classList.add('active'));

  // Close mobile sidebar
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('sidebarOverlay').classList.remove('open');

  // Initialize page content
  if (pageId === 'feed') renderFeed();
  if (pageId === 'explore') renderExplore();
  if (pageId === 'notifications') renderNotifications();
  if (pageId === 'profile') renderProfile();
  if (pageId === 'messages') renderMessages();
  if (pageId === 'reels') renderReels();

  window.scrollTo(0, 0);
}

// ===== MOBILE SIDEBAR =====
function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');
  sidebar.classList.toggle('open');
  overlay.classList.toggle('open');
}

// ===== TOAST =====
function showToast(msg, type = 'info') {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  const icons = { success: '✓', info: '💜', error: '✕' };
  toast.innerHTML = `<span>${icons[type]}</span><span>${msg}</span>`;
  container.appendChild(toast);
  setTimeout(() => { toast.style.opacity = '0'; toast.style.transform = 'translateX(20px)'; toast.style.transition = '0.3s'; setTimeout(() => toast.remove(), 300); }, 3000);
}

// ===== LIKE / SAVE =====
function toggleLike(btn, postId) {
  if (likedPosts.has(postId)) {
    likedPosts.delete(postId);
    btn.classList.remove('liked');
    const count = parseInt(btn.querySelector('.count').textContent.replace(/[^0-9]/g, ''));
    btn.querySelector('.count').textContent = formatCount(count - 1);
    btn.innerHTML = btn.innerHTML.replace('❤️', '🤍');
  } else {
    likedPosts.add(postId);
    btn.classList.add('liked');
    const count = parseInt(btn.querySelector('.count').textContent.replace(/[^0-9]/g, ''));
    btn.querySelector('.count').textContent = formatCount(count + 1);
    btn.innerHTML = btn.innerHTML.replace('🤍', '❤️');
    // Heart burst animation
    btn.style.transform = 'scale(1.3)';
    setTimeout(() => btn.style.transform = '', 200);
  }
}

function toggleSave(btn, postId) {
  if (savedPosts.has(postId)) {
    savedPosts.delete(postId);
    btn.classList.remove('saved');
    btn.innerHTML = '🔖';
    showToast('Removed from saved', 'info');
  } else {
    savedPosts.add(postId);
    btn.classList.add('saved');
    btn.innerHTML = '🔖';
    showToast('Saved to collection! 🔖', 'success');
  }
}

function toggleFollow(btn, userId) {
  if (followedUsers.has(userId)) {
    followedUsers.delete(userId);
    btn.textContent = 'Follow';
    btn.className = 'btn btn-outline btn-xs';
  } else {
    followedUsers.add(userId);
    btn.textContent = 'Following';
    btn.className = 'btn btn-ghost btn-xs';
    showToast(`Following @${userId} 💜`, 'success');
  }
}

function formatCount(n) {
  if (n >= 1000000) return (n/1000000).toFixed(1) + 'M';
  if (n >= 1000) return (n/1000).toFixed(1) + 'K';
  return n.toString();
}

// ===== RENDER FEED =====
function renderFeed() {
  const storiesEl = document.getElementById('storiesRow');
  const feedEl = document.getElementById('feedPosts');
  if (!storiesEl || !feedEl) return;

  // Stories
  let storiesHTML = `<div class="story-item add-story">
    <div class="story-ring"><div class="add-story-icon">＋</div></div>
    <span class="story-name">Your Story</span>
  </div>`;
  users.forEach((u, i) => {
    const seen = i > 3;
    storiesHTML += `<div class="story-item" onclick="showToast('Watching ${u.name}\'s story 👀', 'info')">
      <div class="story-ring ${seen ? 'seen' : ''}">
        <div class="story-inner"><img src="${u.avatar}" alt="${u.name}" loading="lazy"></div>
      </div>
      <span class="story-name">${u.name.split(' ')[0]}</span>
    </div>`;
  });
  storiesEl.innerHTML = storiesHTML;

  // Posts
  let postsHTML = '';
  for (let i = 0; i < 6; i++) {
    const user = users[i % users.length];
    const img = postImages[i % postImages.length];
    const caption = captions[i % captions.length];
    const time = times[i % times.length];
    const likes = likesCounts[i % likesCounts.length];
    const comments = commentCounts[i % commentCounts.length];
    const aspectClass = i === 2 ? 'portrait' : i === 5 ? 'landscape' : '';

    postsHTML += `
    <div class="post-card" id="post-${i}">
      <div class="post-header">
        <img class="avatar" src="${user.avatar}" width="38" height="38" onclick="navigate('profile')" style="cursor:pointer" alt="${user.name}" loading="lazy">
        <div class="post-user-info" onclick="navigate('profile')" style="cursor:pointer">
          <div class="post-username">
            ${user.name} ${user.verified ? '<span class="verified">✦</span>' : ''}
            <span class="tag ${user.role === 'creator' ? 'tag-creator' : 'tag-user'}">${user.role}</span>
          </div>
          <div class="post-meta">@${user.handle} · ${time} ago</div>
        </div>
        <button class="post-options" onclick="showPostMenu(${i})">⋯</button>
      </div>
      <img class="post-image ${aspectClass}" src="${img}" alt="Post" loading="lazy">
      <div class="post-actions">
        <button class="action-btn" onclick="toggleLike(this, ${i})" id="like-${i}">
          🤍 <span class="count">${formatCount(likes)}</span>
        </button>
        <button class="action-btn" onclick="navigate('messages')">
          💬 <span class="count">${formatCount(comments)}</span>
        </button>
        <button class="action-btn" onclick="sharePost(${i})">↗️</button>
        <span class="spacer"></span>
        <button class="action-btn" onclick="toggleSave(this, ${i})" id="save-${i}">🔖</button>
      </div>
      <div class="post-likes">${formatCount(likes)} likes</div>
      <div class="post-caption">
        <span class="username" onclick="navigate('profile')">${user.name}</span>
        ${caption}
      </div>
      <div class="post-comments-link" onclick="showToast('Loading comments... 💬', 'info')">View all ${formatCount(comments)} comments</div>
      <div class="comment-input-row">
        <img class="avatar" src="${currentUser.avatar}" width="28" height="28" alt="You">
        <input class="comment-input" placeholder="Add a comment..." onkeydown="if(event.key==='Enter'){addComment(this, ${i})}">
        <button class="comment-post-btn" onclick="addComment(this.previousElementSibling, ${i})">Post</button>
      </div>
    </div>`;
  }
  feedEl.innerHTML = postsHTML;
}

function addComment(input, postId) {
  if (!input.value.trim()) return;
  showToast('Comment posted! 💬', 'success');
  input.value = '';
}

function showPostMenu(postId) {
  showToast('Post options coming soon ⚙️', 'info');
}

function sharePost(postId) {
  showToast('Link copied to clipboard! ↗️', 'success');
}

// ===== RENDER EXPLORE =====
function renderExplore() {
  const grid = document.getElementById('exploreGrid');
  if (!grid) return;
  let html = '';
  for (let i = 0; i < 15; i++) {
    html += `<div class="explore-item" onclick="navigate('profile')">
      <img src="${postImages[i % postImages.length]}" alt="Explore" loading="lazy">
      <div class="explore-overlay">
        <span style="color:#fff;font-size:12px;font-weight:600;">❤️ ${formatCount(likesCounts[i%likesCounts.length])}</span>
      </div>
    </div>`;
  }
  grid.innerHTML = html;
}

// ===== RENDER NOTIFICATIONS =====
const notifData = [
  { user: users[0], action: 'liked your photo', time: '2m', media: postImages[0], unread: true },
  { user: users[1], action: 'started following you', time: '12m', unread: true },
  { user: users[3], action: 'commented: "Absolutely stunning! 🔥"', time: '1h', media: postImages[2], unread: true },
  { user: users[2], action: 'liked your reel', time: '2h', media: postImages[4], unread: false },
  { user: users[5], action: 'mentioned you in a comment', time: '3h', unread: false },
  { user: users[7], action: 'started following you', time: '5h', unread: false },
  { user: users[4], action: 'liked your photo', time: '8h', media: postImages[1], unread: false },
  { user: users[6], action: 'sent you a message', time: '1d', unread: false },
];

function renderNotifications() {
  const list = document.getElementById('notifList');
  if (!list) return;
  let html = '';
  notifData.forEach((n, i) => {
    html += `<div class="notif-item ${n.unread ? 'unread' : ''}" onclick="handleNotif(${i})">
      ${n.unread ? '<div class="notif-dot"></div>' : '<div style="width:8px;flex-shrink:0"></div>'}
      <img class="avatar" src="${n.user.avatar}" width="44" height="44" alt="${n.user.name}">
      <div class="notif-content">
        <div class="notif-text"><span class="notif-name">${n.user.name}</span> ${n.action}</div>
        <div class="notif-time">${n.time} ago</div>
      </div>
      ${n.media ? `<img class="notif-media" src="${n.media}" alt="">` : ''}
    </div>`;
  });
  list.innerHTML = html;
}

function handleNotif(i) {
  const notif = document.querySelectorAll('.notif-item')[i];
  notif.classList.remove('unread');
  const dot = notif.querySelector('.notif-dot');
  if (dot) { dot.style.background = 'transparent'; }
}

// ===== RENDER PROFILE =====
function renderProfile() {
  const grid = document.getElementById('profileGrid');
  if (!grid) return;
  let html = '';
  for (let i = 0; i < 12; i++) {
    html += `<div class="grid-post">
      <img src="${postImages[i % postImages.length]}" alt="Post" loading="lazy">
      <div class="grid-post-overlay">
        <span class="grid-stat">❤️ ${formatCount(likesCounts[i % likesCounts.length])}</span>
        <span class="grid-stat">💬 ${formatCount(commentCounts[i % commentCounts.length])}</span>
      </div>
    </div>`;
  }
  grid.innerHTML = html;
}

// ===== RENDER MESSAGES =====
const threads = [
  { user: users[0], preview: 'That shoot was 🔥 let\'s do another!', time: '2m', unread: true },
  { user: users[3], preview: 'Check out my new collection drop!', time: '14m', unread: true },
  { user: users[7], preview: 'Thanks for the collab 💜', time: '1h', unread: false },
  { user: users[1], preview: 'Are you going to the event?', time: '3h', unread: false },
  { user: users[5], preview: 'Loved the reel! So inspiring', time: '1d', unread: false },
  { user: users[2], preview: 'Can we connect sometime?', time: '2d', unread: false },
];

let activeThread = 0;

function renderMessages() {
  renderThreadList();
  renderChat(0);
}

function renderThreadList() {
  const list = document.getElementById('threadList');
  if (!list) return;
  let html = '';
  threads.forEach((t, i) => {
    html += `<div class="msg-thread ${i === activeThread ? 'active' : ''} ${t.unread ? 'unread' : ''}" onclick="openThread(${i})">
      <img class="avatar" src="${t.user.avatar}" width="44" height="44" alt="${t.user.name}">
      <div class="thread-info">
        <div class="thread-name">
          <span>${t.user.name}</span>
          <span class="thread-time">${t.time}</span>
        </div>
        <div class="thread-preview">${t.preview}</div>
      </div>
      ${t.unread ? '<div class="thread-unread-dot"></div>' : ''}
    </div>`;
  });
  list.innerHTML = html;
}

const chatMessages = [
  { mine: false, text: 'Hey! Loved your latest post 🔥', time: '2:30 PM' },
  { mine: true, text: 'Thanks so much! Took me all morning to edit 😅', time: '2:31 PM' },
  { mine: false, text: 'It really shows! The lighting is perfect', time: '2:33 PM' },
  { mine: false, text: 'That shoot was 🔥 let\'s do another!', time: '2:34 PM' },
  { mine: true, text: 'Definitely! I\'m free next Saturday', time: '2:36 PM' },
];

function openThread(index) {
  activeThread = index;
  threads[index].unread = false;
  renderThreadList();
  renderChat(index);
  // On mobile, show chat area
  document.getElementById('chatArea').classList.add('show');
}

function renderChat(index) {
  const thread = threads[index];
  const header = document.getElementById('chatHeader');
  const msgs = document.getElementById('chatMessages');
  if (!header || !msgs) return;

  header.innerHTML = `
    <button class="icon-btn" onclick="closeMobileChat()" style="display:none" id="backBtn">←</button>
    <img class="avatar" src="${thread.user.avatar}" width="40" height="40" alt="${thread.user.name}">
    <div class="chat-header-info">
      <div class="chat-header-name">${thread.user.name} ${thread.user.verified ? '<span class="verified">✦</span>' : ''}</div>
      <div class="chat-header-status" style="color: #48bb78; font-size: 12px;">● Active now</div>
    </div>
    <button class="icon-btn" onclick="showToast('Video call starting... 📹', 'info')">📹</button>
    <button class="icon-btn" onclick="showToast('Voice call starting... 📞', 'info')">📞</button>
  `;

  // Show back button on mobile
  if (window.innerWidth <= 640) {
    document.getElementById('backBtn').style.display = 'block';
  }

  let html = '';
  chatMessages.forEach(m => {
    html += `<div class="msg-group ${m.mine ? 'mine' : ''}">
      ${!m.mine ? `<img class="avatar" src="${thread.user.avatar}" width="32" height="32" alt="">` : ''}
      <div>
        <div class="msg-bubble">${m.text}</div>
        <div class="msg-time">${m.time}</div>
      </div>
    </div>`;
  });
  msgs.innerHTML = html;
  msgs.scrollTop = msgs.scrollHeight;
}

function closeMobileChat() {
  document.getElementById('chatArea').classList.remove('show');
}

function sendMessage() {
  const input = document.getElementById('chatInputField');
  if (!input || !input.value.trim()) return;
  chatMessages.push({ mine: true, text: input.value, time: new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'}) });
  input.value = '';
  renderChat(activeThread);
}

// ===== RENDER REELS =====
function renderReels() {
  const grid = document.getElementById('reelsGrid');
  if (!grid) return;
  let html = '';
  for (let i = 0; i < 9; i++) {
    const user = users[i % users.length];
    html += `<div class="reel-thumb" onclick="showToast('Playing reel 🎬', 'info')">
      <img src="${postImages[i % postImages.length]}" alt="Reel" loading="lazy">
      <div class="reel-overlay">
        <div style="display:flex;align-items:center;justify-content:space-between;width:100%">
          <div class="reel-views">▶ ${formatCount(likesCounts[i%likesCounts.length] * 3)}</div>
          ${i === 0 ? '<span class="live-badge">LIVE</span>' : ''}
        </div>
        <div style="display:flex;align-items:center;gap:6px;margin-top:6px">
          <img class="avatar" src="${user.avatar}" width="22" height="22" alt="">
          <span style="font-size:12px;color:#fff;font-weight:500">${user.handle}</span>
        </div>
      </div>
    </div>`;
  }
  grid.innerHTML = html;
}

// ===== SEARCH =====
function handleSearch(input) {
  const query = input.value.toLowerCase();
  if (query.length > 2) {
    showToast(`Searching for "${input.value}"... 🔍`, 'info');
  }
}

// ===== CREATE POST MODAL =====
function openCreateModal() {
  document.getElementById('createModal').classList.add('open');
}
function closeCreateModal() {
  document.getElementById('createModal').classList.remove('open');
}

// ===== AUTH =====
function selectRole(role) {
  document.querySelectorAll('.role-option').forEach(el => el.classList.remove('selected'));
  document.querySelector(`[data-role="${role}"]`).classList.add('selected');
}

function handleLogin(e) {
  e.preventDefault();
  showToast('Welcome back to Loopsta! 💜', 'success');
  setTimeout(() => {
    document.getElementById('authPage').classList.remove('active');
    navigate('feed');
  }, 800);
}

function handleSignup(e) {
  e.preventDefault();
  showToast('Account created! Welcome to Loopsta 🎉', 'success');
  setTimeout(() => {
    document.getElementById('authPage').classList.remove('active');
    navigate('feed');
  }, 800);
}

function showLogin() {
  document.getElementById('loginForm').style.display = 'block';
  document.getElementById('signupForm').style.display = 'none';
  document.getElementById('authTitle').textContent = 'Welcome back';
  document.getElementById('authSub').textContent = 'Sign in to your Loopsta account';
}

function showSignup() {
  document.getElementById('loginForm').style.display = 'none';
  document.getElementById('signupForm').style.display = 'block';
  document.getElementById('authTitle').textContent = 'Join Loopsta';
  document.getElementById('authSub').textContent = 'Create your account and start creating';
}

// ===== TOGGLE =====
function toggleSwitch(btn) {
  btn.classList.toggle('on');
}

// ===== PROFILE TABS =====
function switchProfileTab(tabEl, tabName) {
  document.querySelectorAll('.profile-tab').forEach(t => t.classList.remove('active'));
  tabEl.classList.add('active');
  if (tabName === 'posts') {
    document.getElementById('profileGrid').style.display = 'grid';
    document.getElementById('reelsGrid2') && (document.getElementById('reelsGrid2').style.display = 'none');
  }
  showToast(`Viewing ${tabName} 📂`, 'info');
}

// ===== KEYBOARD SHORTCUTS =====
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeCreateModal();
    closeMobileChat();
  }
});

// ===== INIT =====
document.addEventListener('DOMContentLoaded', () => {
  navigate('feed');

  // Sidebar overlay click
  document.getElementById('sidebarOverlay').addEventListener('click', () => {
    document.getElementById('sidebar').classList.remove('open');
    document.getElementById('sidebarOverlay').classList.remove('open');
  });

  // Chat enter key
  const chatInput = document.getElementById('chatInputField');
  if (chatInput) {
    chatInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
    });
  }

  // Create modal backdrop click
  document.getElementById('createModal').addEventListener('click', (e) => {
    if (e.target === document.getElementById('createModal')) closeCreateModal();
  });
});