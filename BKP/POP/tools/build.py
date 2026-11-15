#!/usr/bin/env python3
"""
Pocket of Paradise — static site generator.
Reads tools/data/site.json (content cloned from the live site) and writes plain
HTML pages next to this folder. The OUTPUT is pure HTML + CSS + JS (no framework).
Run:  python3 tools/build.py
"""
import json, os, re, html, shutil, datetime
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, 'tools/data/site.json'), encoding='utf-8'))
IMGDIR = os.path.join(ROOT, 'assets/img')
HAVE = {f[:-5] for f in os.listdir(IMGDIR) if f.endswith('.webp')}
# Public base URL used for canonical/OG/sitemap. Preview host below; switch to the live domain at launch.
SITE = 'https://ceoblackcodelabs.github.io/BlackCodeLabs/BKP/POP'
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import og as OG
WA = '254115167384'
PHONES = ['0115167384', '0115174163', '0115171096', '0115172189', '0115172784', '0115175475']
EMAIL = 'info@pocketofparadise.com'
esc = html.escape

SOCIAL_URL = {'Instagram': 'https://www.instagram.com/pocketofparadisetravelco/'}  # add the other accounts here when known
def social(n, t, extra=''):
    url = SOCIAL_URL.get(n)
    if url:
        return '<a href="%s" target="_blank" rel="noopener" aria-label="%s on %s">%s</a>' % (url, 'Follow us', n, t)
    return '<a href="#" data-social="%s" aria-label="%s" title="%s (link coming soon)">%s</a>' % (n, n, n, t)

def phone_fmt(p):  # 0115167384 -> +254 115 167 384
    p = re.sub(r'\D', '', p)
    p = p[1:] if p.startswith('0') else p
    return '+254 %s %s %s' % (p[:3], p[3:6], p[6:])

# ------------------------------------------------------------------ images
def stem(ref):
    if 'unsplash.com' in ref:
        m = re.search(r'photo-([\w-]+)', ref)
        return 'u-' + m.group(1)[:24]
    b = os.path.splitext(os.path.basename(ref.split('?')[0]))[0]
    from urllib.parse import unquote
    return re.sub(r'[^\w\-]+', '-', unquote(b)).strip('-').lower()

FALLBACK = 'u-1547970810-dc1eac37d174'
def img(ref, fb=FALLBACK):
    s = stem(ref) if ref else fb
    if s not in HAVE:
        s = fb if fb in HAVE else next(iter(HAVE))
    return s
def ipath(R, name):
    name = name if name in HAVE else img(name)
    return '%sassets/img/%s.webp' % (R, name)

# ------------------------------------------------------------------ helpers
def num(s):
    return int(re.sub(r'\D', '', s))
def kes(n):
    return 'KES {:,}'.format(n)
def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
def wa(text):
    return 'https://wa.me/%s?text=%s' % (WA, quote(text))
def ic(name, cls=''):
    return '<svg class="icon %s" aria-hidden="true"><use href="#i-%s"/></svg>' % (cls, name)

ICONS = {
 'arrow': '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>', 'chev': '<path d="m6 9 6 6 6-6"/>', 'check': '<path d="M20 6 9 17l-5-5"/>',
 'x': '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>', 'menu': '<path d="M3 12h18"/><path d="M3 6h18"/><path d="M3 18h18"/>',
 'phone': '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
 'mail': '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>', 'pin': '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
 'cal': '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>', 'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
 'compass': '<circle cx="12" cy="12" r="10"/><path d="m16 8-2 6-6 2 2-6z"/>', 'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
 'heart': '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7Z"/>',
 'star': '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.9-6.2-3.3-6.2 3.3L7 14.2 2 9.3l6.9-1z"/>', 'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 'search': '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>', 'up': '<path d="m18 15-6-6-6 6"/>', 'left': '<path d="m15 18-6-6 6-6"/>', 'right': '<path d="m9 18 6-6-6-6"/>',
 'wa': '<path d="M3 21l1.7-5A9 9 0 1 1 8 19.4z"/><path d="M9 10c.5 2 2.5 4 5 5l1.5-1.5-2-1-1 .7a4 4 0 0 1-2-2l.7-1-1-2z"/>',
 'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
 'bed': '<path d="M2 20v-8a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v8M2 16h20M6 10V6a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v4"/>', 'map': '<path d="M3 6l6-3 6 3 6-3v15l-6 3-6-3-6 3z"/><path d="M9 3v15M15 6v15"/>',
 'camera': '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>',
 'share': '<path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="m16 6-4-4-4 4"/><path d="M12 2v13"/>', 'print': '<path d="M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/>',
 'leaf': '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10z"/><path d="M2 21c0-3 1.9-5.4 5.4-7"/>', 'gift': '<rect x="3" y="8" width="18" height="4"/><path d="M12 8v13M19 12v9H5v-9M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
 'instagram': '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/>',
 'facebook': '<path d="M14 8h3V4h-3a4 4 0 0 0-4 4v2H7v4h3v8h4v-8h3l1-4h-4V8.5a.5.5 0 0 1 .5-.5z"/>',
 'tiktok': '<path d="M15 3v11.5a3.5 3.5 0 1 1-3.5-3.5"/><path d="M15 3c.4 2.6 2 4.2 5 4.5"/>',
 'youtube': '<rect x="2" y="5" width="20" height="14" rx="4"/><path d="m10 9 5 3-5 3z" fill="currentColor"/>',
 'tripadvisor': '<circle cx="7" cy="14" r="3.5"/><circle cx="17" cy="14" r="3.5"/><circle cx="7" cy="14" r=".8" fill="currentColor"/><circle cx="17" cy="14" r=".8" fill="currentColor"/><path d="M2 10.5C5 8 8.5 7 12 7s7 1 10 3.5"/>',
 'bolt': '<path d="m13 2-9 12h7l-1 8 9-12h-7z"/>', 'msg': '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>', 'plane': '<path d="M17.8 19.2 16 11l3.5-3.5a2.1 2.1 0 0 0-3-3L13 8 4.8 6.2 3.4 7.6l6.4 3.4-3.3 3.3-3-.5-1.1 1.1 3.5 2 2 3.5 1.1-1.1-.5-3 3.3-3.3 3.4 6.4z"/>',
}
SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + ''.join('<symbol id="i-%s" viewBox="0 0 24 24">%s</symbol>' % (k, v) for k, v in ICONS.items()) + '</defs></svg>'

# ------------------------------------------------------------------ data model
def parse_tiers(opts):
    tiers = {}
    for k in ('budget', 'midrange', 'luxury'):
        if k in opts:
            o = opts[k]
            tiers[k] = {'label': o.get('label') or {'budget': 'Budget', 'midrange': 'Mid-range', 'luxury': 'Luxury'}[k],
                        'price': num(o['price']), 'stay': o.get('property', '')}
    if len({t['price'] for t in tiers.values()}) == 1 and len(tiers) > 1:  # identical tiers => single package price
        t = list(tiers.values())[1]
        t['label'] = 'Package price'
        tiers = {'midrange': t}
    return tiers

EXTRA_GAL = {
 'zanzibar-escape': ['activities-dhow', 'u-1575999502951-4ab25b5ca8', 'u-1590523277543-a94d2e4eb0', 'u-1573843981267-be1999ff37', 'u-1504598318550-17eba1008a'],
 'zanzibar-romance': ['u-1590523741831-ab7e8b8f9c', 'u-1575999502951-4ab25b5ca8', 'activities-dhow', 'u-1573843981267-be1999ff37'],
 'mara-honeymoon': ['couples-2', 'ashnil-mara-3', 'mara-engai-3', 'u-1516321318423-f06f85e504'],
 'safari-beach-honeymoon': ['couples-3', 'u-1575999502951-4ab25b5ca8', 'mara-engai-1', 'couples-5'],
 'maldives-honeymoon': ['u-1540541338287-41700207de', 'u-1573790387438-4da9050393', 'u-1586500036706-41963de24d', 'u-1514282401047-d79a71a590'],
 'bali-love-journey': ['u-1518548419970-58e3b4079a', 'u-1555400038-63f5ba517a47', 'u-1537996194471-e657df975a', 'u-1544161515-4ab6ce6db874'],
 'cape-town-experience': ['u-1580060839134-75a5edca2e', 'u-1469854523086-cc02fe5d88', 'u-1507525428034-b723cf961d'],
 'thailand-phuket-krabi': ['u-1552465011-b4e21bf6e79a', 'u-1506665531195-3566af2b4d', 'u-1528181304800-259b088485', 'u-1504214208698-ea1916a219'],
 'dubai-holiday': ['u-1512453979798-5ea266f888', 'u-1504598318550-17eba1008a', 'u-1507608616759-54f48f0af0'],
 'malaysia-singapore-holiday': ['u-1596422846543-75c6fc197f', 'u-1558618666-fcd25c85cd64', 'u-1535941339077-2dd1c79630'],
}
PLACES = {'zanzibar-escape': 'Zanzibar', 'zanzibar-romance': 'Zanzibar', 'mara-honeymoon': 'Masai Mara', 'safari-beach-honeymoon': 'Masai Mara · Zanzibar',
          'maldives-honeymoon': 'Maldives', 'bali-love-journey': 'Bali', 'cape-town-experience': 'Cape Town', 'thailand-phuket-krabi': 'Phuket · Krabi',
          'dubai-holiday': 'Dubai', 'malaysia-singapore-holiday': 'Malaysia · Singapore'}
CATNAME = {'kenya': 'Kenya Safari', 'zanzibar': 'Zanzibar', 'couples': 'Couples', 'outbound': 'Outbound'}

PK = []
for i, p in enumerate(D['kenya_packages']):
    tiers = parse_tiers(p['priceOptions'])
    cats = ['kenya'] + (['couples'] if 'honeymoon' in p['id'] else [])
    PK.append(dict(id=p['id'], title=p['title'], subtitle=p['subtitle'], days=p['durationDays'], duration=p['duration'], cat='kenya', cats=cats,
                   image=img(p['image']), gallery=[img(g) for g in p['gallery']], region=p['region'], journey=p['journeyType'], best=p['bestTime'], pace=p['pace'],
                   tiers=tiers, overview=p['overview'], highlights=p['highlights'], stay=p['whereYoullStay'],
                   inc=p['inclusions'], exc=p['exclusions'], itin=[(d['day'], d['title'], d['description']) for d in p['itinerary']],
                   url='destinations/kenya/%s/' % p['id']))
for p in D['other_packages']:
    cat = p['category'].lower()
    cats = [cat] + (['couples'] if p.get('forCouples') and cat != 'couples' else [])
    days = int(re.search(r'\d+', p['duration']).group())
    PK.append(dict(id=p['id'], title=p['title'], subtitle=p['description'], days=days, duration='%d Days / %d Nights' % (days, days - 1), cat=cat, cats=cats,
                   image=img(p['image']), gallery=[img(p['image'])] + [g for g in EXTRA_GAL.get(p['id'], []) if g in HAVE],
                   region=PLACES.get(p['id'], ''), journey='International' if cat == 'outbound' else ('Beach' if cat == 'zanzibar' else 'Safari & Honeymoon'),
                   best='', pace='', tiers=parse_tiers(p['priceOptions']), overview=p['description'], highlights=p['highlights'], stay=[],
                   inc=p['inclusions'], exc=p['exclusions'], itin=[(d['day'], d['title'], d['activities']) for d in p['itinerary']],
                   url='packages/%s/' % p['id']))
for p in PK:
    p['from'] = min(t['price'] for t in p['tiers'].values())
PKID = {p['id']: p for p in PK}

# ------------------------------------------------------------------ layout
def u(R, path):
    return R + path + 'index.html'

NAV_DEST = [d['id'] for d in D['destinations']]
def header(R, active):
    def a(label, path, key):
        return '<li><a href="%s"%s>%s</a></li>' % (u(R, path), ' class="active"' if active == key else '', label)
    dests = ''.join('<a href="%s"><img src="%s" alt="" loading="lazy" width="46" height="46"/><span>%s<small>%s</small></span></a>' % (
        u(R, 'destinations/%s/' % d['id']), ipath(R, img(d['coverImage'])), d['name'], esc(d['countryTag'])) for d in D['destinations'])
    kpk = ''.join('<a href="%s"><span>%s<small>from %s</small></span></a>' % (u(R, p['url']), esc(p['title']), kes(p['from'])) for p in PK if p['cat'] == 'kenya')
    styles = ''.join('<a href="%s"><img src="%s" alt="" loading="lazy" width="46" height="46"/><span>%s</span></a>' % (
        u(R, 'travel-styles/%s/' % s['id']), ipath(R, img(s['image'])), esc(s['title'])) for s in D['styles'])
    exps = ''.join('<a href="%s"><img src="%s" alt="" loading="lazy" width="46" height="46"/><span>%s</span></a>' % (
        u(R, 'experiences/%s/' % k), ipath(R, img(v['heroImage'])), esc(v['title'])) for k, v in D['experience_categories'].items())
    pk_menu = ''.join('<a href="%s"><span>%s<small>%d journeys</small></span></a>' % (u(R, 'packages/%s/' % c if c != 'all' else 'packages/'), n, cnt)
                      for c, n, cnt in [('all', 'All packages', len(PK))] + [(c, CATNAME[c] + ' packages', len([p for p in PK if c in p['cats']])) for c in CATNAME])
    mega_d = '<div class="mega"><h5>Explore destinations</h5>%s<h5>Kenya safari packages</h5>%s</div>' % (dests, kpk)
    return '''<header class="site-header" id="header"><div class="container nav">
<a class="logo" href="%(home)s" aria-label="Pocket of Paradise — home"><img src="%(R)sassets/img/logo.png" alt="Pocket of Paradise logo" width="58" height="58"/></a>
<ul class="menu" aria-label="Main navigation">
<li><button type="button" class="%(a_d)s" aria-haspopup="true">Destinations %(chev)s</button>%(mega_d)s</li>
<li><button type="button" class="%(a_p)s" aria-haspopup="true">Packages %(chev)s</button><div class="mega narrow"><h5>Ready-to-book journeys</h5>%(pk_menu)s</div></li>
<li><button type="button" class="%(a_s)s" aria-haspopup="true">Travel Styles %(chev)s</button><div class="mega narrow"><h5>How do you want to travel?</h5>%(styles)s</div></li>
<li><button type="button" class="%(a_e)s" aria-haspopup="true">Experiences %(chev)s</button><div class="mega"><h5>Things to do</h5>%(exps)s</div></li>
%(about)s%(blog)s%(contact)s
</ul>
<div class="nav-cta"><a class="btn btn-gold btn-sm" href="%(plan)s">Plan Your Trip %(arrow)s</a>
<button class="burger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="drawer">%(menu)s</button></div>
</div></header>''' % dict(
        home=u(R, ''), R=R, chev=ic('chev'), mega_d=mega_d, pk_menu=pk_menu, styles=styles, exps=exps,
        a_d='active' if active == 'dest' else '', a_p='active' if active == 'pk' else '', a_s='active' if active == 'style' else '', a_e='active' if active == 'exp' else '',
        about=a('About', 'about-us/', 'about'), blog=a('Blog', 'blog/', 'blog'), contact=a('Contact', 'contact/', 'contact'),
        plan=u(R, 'create-tour-plan/'), arrow=ic('arrow'), menu=ic('menu'))

def drawer(R):
    def grp(title, items):
        return '<details class="dr"><summary class="dr-sum">%s %s</summary><div class="dr-sub">%s</div></details>' % (title, ic('chev'), ''.join('<a href="%s">%s</a>' % (u(R, p), n) for n, p in items))
    return '''<div class="drawer" id="drawer" aria-hidden="false"><div class="drawer-panel" role="dialog" aria-label="Menu">
<div class="drawer-top"><img src="%sassets/img/logo.png" alt="Pocket of Paradise" width="48" height="48"/><button class="burger" style="display:inline-flex" data-close aria-label="Close menu">%s</button></div>
%s%s%s%s
<a class="dr-link" href="%s">About Us</a><a class="dr-link" href="%s">Blog</a><a class="dr-link" href="%s">Contact</a><a class="dr-link" href="%s">FAQs</a>
<a class="btn btn-gold btn-block" style="margin-top:20px" href="%s">Plan Your Trip</a>
<a class="btn btn-wa btn-block" style="margin-top:10px" href="%s">%s Chat on WhatsApp</a>
</div></div>''' % (R, ic('x'),
        grp('Destinations', [(d['name'], 'destinations/%s/' % d['id']) for d in D['destinations']]),
        grp('Packages', [('All packages', 'packages/')] + [(CATNAME[c] + ' packages', 'packages/%s/' % c) for c in CATNAME]),
        grp('Travel Styles', [(s['title'], 'travel-styles/%s/' % s['id']) for s in D['styles']]),
        grp('Experiences', [(v['title'], 'experiences/%s/' % k) for k, v in D['experience_categories'].items()]),
        u(R, 'about-us/'), u(R, 'blog/'), u(R, 'contact/'), u(R, 'faqs/'), u(R, 'create-tour-plan/'),
        wa('Hi Pocket of Paradise! I’d like to speak to a safari expert.'), ic('wa'))

def topbar(R):
    soc = ''.join(social(n, t) for n, t in
                  [('Instagram', ic('instagram')), ('Facebook', ic('facebook')), ('TikTok', ic('tiktok')), ('YouTube', ic('youtube')), ('TripAdvisor', ic('tripadvisor'))])
    return '''<div class="topbar"><div class="container"><div class="tb-l">
<a href="tel:+254115167384">%s %s</a><a class="mail" href="mailto:%s">%s %s</a></div>
<div class="tb-r"><a class="season-pill" data-season-pill href="%s">● Plan your journey</a><div class="socials">%s</div></div></div></div>''' % (
        ic('phone'), phone_fmt(PHONES[0]), EMAIL, ic('mail'), EMAIL, u(R, 'packages/'), soc)

def footer(R):
    more = ''.join('<a href="tel:+254%s">%s</a>' % (p[1:], phone_fmt(p)) for p in PHONES[1:])
    strip = ''.join('<a href="%s#gallery" tabindex="-1" aria-hidden="true"><img src="%s" alt="" loading="lazy" width="200" height="200"/></a>' % (u(R, ''), ipath(R, i)) for i in
                    ['maasai-mara-8', 'diani-almara', 'mara-engai-2', 'couples-3', 'amboseli-elephants-850x540', 'u-1590523741831-ab7e8b8f9c'])
    soc = ''.join(social(n, t) for n, t in [('Instagram', ic('instagram')), ('Facebook', ic('facebook')), ('TikTok', ic('tiktok')), ('YouTube', ic('youtube'))])
    def lk(path, label):
        return '<li><a href="%s">%s</a></li>' % (u(R, path), label)
    return '''<footer><div class="container">
<div class="f-news reveal"><div><span class="eyebrow" style="color:var(--ink);opacity:.75">Stay inspired</span><h3>Safari ideas &amp; seasonal offers, in your inbox</h3><p>One thoughtful email a month from our travel team. No spam.</p></div>
<form id="newsForm" novalidate><label class="sr-only" for="nl">Email address</label><input id="nl" type="email" placeholder="Your email address" autocomplete="email"/><button class="btn btn-dark" type="submit">Subscribe %(arrow)s</button></form></div>
<div class="f-grid">
<div class="f-brand"><a class="logo" href="%(home)s" aria-label="Pocket of Paradise home"><img src="%(R)sassets/img/logo.png" alt="Pocket of Paradise" width="48" height="66"/></a>
<p>At <b>Pocket of Paradise</b>, you are assured of experiencing the African adventure in the finest way possible. Explore Kenya\u2019s breathtaking landscapes and discover your perfect getaway.</p>
<div class="socials">%(soc)s</div></div>
<div><h4>Destinations</h4><ul class="f-links">%(dest)s</ul></div>
<div><h4>Explore</h4><ul class="f-links">%(ex)s</ul></div>
<div><h4>Get in touch</h4><ul class="f-contact">
<li><span class="fi">%(phone)s</span><span><a href="tel:+254115167384"><b>%(p0)s</b></a><small>Calls &amp; WhatsApp</small>
<details class="more-lines"><summary>More ways to call</summary><div>%(more)s</div></details></span></li>
<li><span class="fi">%(mail)s</span><span><a href="mailto:%(email)s">%(email)s</a><small>We reply within a day</small></span></li>
<li><span class="fi">%(pin)s</span><span>Nord Mall, 1st Floor<br/>Ruiru, Kenya<small>Visits by appointment</small></span></li></ul>
<a class="btn btn-wa btn-sm" style="margin-top:6px" href="%(waurl)s" target="_blank" rel="noopener">%(waic)s Chat with a consultant</a></div>
</div>
<div class="f-strip" aria-label="Photos from our journeys">%(strip)s</div>
<div class="f-bot"><span>\u00A9 %(yr)s <b>Pocket of Paradise</b>. All rights reserved.</span><span class="f-legal"><a href="%(tm)s">Terms &amp; Conditions</a><a href="%(pv)s">Privacy Policy</a><a href="%(fq)s">FAQs</a></span></div>
</div><div class="f-mark" aria-hidden="true">Pocket of Paradise</div></footer>''' % dict(
        home=u(R, ''), R=R, soc=soc, strip=strip, arrow=ic('arrow'),
        dest=''.join(lk('destinations/%s/' % d['id'], d['name']) for d in D['destinations']),
        ex=lk('packages/', 'Packages') + lk('travel-styles/', 'Travel Styles') + lk('experiences/', 'Experiences') + lk('about-us/', 'About Us') + lk('blog/', 'Blog') + lk('contact/', 'Contact Us') + lk('create-tour-plan/', 'Plan Your Trip'),
        pin=ic('pin'), phone=ic('phone'), mail=ic('mail'), p0=phone_fmt(PHONES[0]), more=more, email=EMAIL,
        waurl=wa('Hi Pocket of Paradise! I\u2019d like to speak to a travel consultant.'), waic=ic('wa'),
        yr=datetime.date.today().year, tm=u(R, 'terms/'), pv=u(R, 'privacy/'), fq=u(R, 'faqs/'))

def widgets(R):
    qs = [('Plan my safari', 'Hi! I’d like help planning a safari.'), ('Honeymoon ideas', 'Hi! I’m looking for honeymoon ideas.'),
          ('Beach holiday', 'Hi! I’m interested in a beach holiday.'), ('Prices & availability', 'Hi! Could you share prices and availability for my dates?')]
    return '''<div class="wa-fab"><div class="wa-pop" role="dialog" aria-label="Chat with Pocket of Paradise on WhatsApp"><div class="wa-head"><img src="%(R)sassets/img/logo.png" alt=""/><div><b>Pocket of Paradise</b><small>Typically replies in minutes</small></div></div>
<div class="wa-body"><div class="wa-bub">Karibu! \U0001F44B How can we help you plan your trip? Pick a topic and we’ll open WhatsApp with your message ready.</div><div class="wa-q">%(q)s</div></div></div>
<button class="wa-btn" aria-label="Chat on WhatsApp">%(wa)s</button></div>
<button id="top" aria-label="Back to top">%(up)s</button>
<div class="cookie" id="cookie" role="dialog" aria-label="Cookie notice"><p>We use cookies to understand how visitors use our site and improve your experience. Read our <a href="%(pv)s">Privacy Policy</a>.</p><div><button class="btn btn-gold btn-sm" data-ck="accept">Accept</button> <button class="btn btn-outline btn-sm" data-ck="decline">Decline</button></div></div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<div class="lb" id="lb" role="dialog" aria-label="Image viewer"><button class="x" aria-label="Close">%(x)s</button><button class="pv" aria-label="Previous">%(l)s</button><img src="" alt=""/><button class="nx" aria-label="Next">%(r)s</button><div class="cap"></div></div>''' % dict(
        R=R, q=''.join('<a href="%s" target="_blank" rel="noopener">%s</a>' % (wa(t), n) for n, t in qs), wa=ic('wa'), up=ic('up'), pv=u(R, 'privacy/'), x=ic('x'), l=ic('left'), r=ic('right'))

def newsletter():
    return '''<div class="news"><div class="container news-in"><div><h3>Get safari inspiration &amp; seasonal offers</h3><p>Monthly travel ideas from our team. No spam.</p></div>
<form id="newsForm" novalidate><label class="sr-only" for="nl">Email address</label><input id="nl" type="email" placeholder="Your email address" autocomplete="email"/><button class="btn btn-dark" type="submit">Subscribe</button></form></div></div>'''

def cta_band(R, title='Your Journey Awaits', text='Start planning a travel experience that reconnects, inspires, and moves you. Let us craft your perfect escape.', bg='laikiapia-sanctuary-ol-lentile-3'):
    return '''<section class="cta"><img class="bg" src="%s" alt="" loading="lazy"/><div class="container reveal"><span class="eyebrow" style="color:var(--gold2)">Ready to explore?</span><h2>%s</h2><p>%s</p>
<div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap"><a class="btn btn-gold" href="%s">Start Your Journey %s</a><a class="btn btn-wa" href="%s" target="_blank" rel="noopener">%s Speak to an Expert</a></div></div></section>''' % (
        ipath(R, bg), esc(title), esc(text), u(R, 'create-tour-plan/'), ic('arrow'), wa('Hi Pocket of Paradise! I’d like to speak to a safari expert.'), ic('wa'))

def schema_org(R=''):
    return {"@context": "https://schema.org", "@type": "TravelAgency", "name": "Pocket of Paradise", "url": SITE, "logo": SITE + "/assets/img/logo.png",
            "telephone": "+254115167384", "email": EMAIL, "address": {"@type": "PostalAddress", "streetAddress": "Nord Mall, 1st Floor", "addressLocality": "Ruiru", "addressCountry": "KE"},
            "description": "Boutique luxury safari, beach and international holidays from Kenya."}

def page(path, title, desc, body, active='', og=None, ld=None, extra_head='', body_class=''):
    """Write one HTML page. path like 'destinations/kenya/' ('' = home)."""
    R = '../' * (path.count('/')) if path else ''
    full_title = title if title.endswith('Pocket of Paradise') else title + ' | Pocket of Paradise'
    og = og or 'laikiapia-sanctuary-ol-lentile-3'
    og = og if og in HAVE else FALLBACK
    url = SITE + '/' + path
    ogfile = (path.strip('/').replace('/', '-') or 'home') + '.jpg'
    seg = path.strip('/').split('/')
    kick, foot, ogt = 'Pocket of Paradise', '', re.sub(r' \| Pocket of Paradise$', '', title)
    if not path:
        kick, foot, ogt = 'Luxury safaris \u00B7 Beach escapes \u00B7 Kenya', 'Plan your journey', 'Travel that moves you. Moments that stay with you.'
    elif seg[-1] in PKID and seg[0] in ('packages', 'destinations'):
        pk_ = PKID[seg[-1]]
        kick, foot, ogt = CATNAME[pk_['cat']] + ' package \u00B7 ' + pk_['duration'].split('/')[0].strip(), 'From %s pp' % kes(pk_['from']), pk_['title']
    else:
        kick = {'destinations': 'Destination', 'travel-styles': 'Travel style', 'experiences': 'Experiences', 'blog': 'Travel journal', 'packages': 'Journeys', 'about-us': 'About us', 'contact': 'Get in touch', 'faqs': 'FAQs', 'create-tour-plan': 'Plan your trip'}.get(seg[0], 'Pocket of Paradise')
        ogt = re.sub(r' \u2014 .*$', '', ogt) if seg[0] in ('destinations', 'travel-styles', 'experiences') and len(seg) > 1 else ogt
    OG.make(os.path.join(ROOT, 'assets/og', ogfile), og, kick, ogt[:90], foot)
    lds = [schema_org()] + ([ld] if isinstance(ld, dict) else (ld or []))
    crumbs = ''
    ldh = ''.join('<script type="application/ld+json">%s</script>\n' % json.dumps(x, ensure_ascii=False) for x in lds)
    doc = '''<!DOCTYPE html>
<html lang="en" class="no-js" data-root="%(R)s">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>%(t)s</title>
<meta name="description" content="%(d)s"/>
<meta name="referrer" content="strict-origin-when-cross-origin"/>
<meta name="theme-color" content="#1a1411"/>
<link rel="canonical" href="%(url)s"/>
<meta property="og:type" content="website"/><meta property="og:site_name" content="Pocket of Paradise"/>
<meta property="og:title" content="%(t)s"/><meta property="og:description" content="%(d)s"/><meta property="og:url" content="%(url)s"/>
<meta property="og:image" content="%(site)s/assets/og/%(ogfile)s"/><meta property="og:image:type" content="image/jpeg"/><meta property="og:image:width" content="1200"/><meta property="og:image:height" content="630"/><meta property="og:image:alt" content="%(ogalt)s"/><meta property="og:locale" content="en_KE"/>
<meta name="twitter:card" content="summary_large_image"/><meta name="twitter:title" content="%(t)s"/><meta name="twitter:description" content="%(d)s"/><meta name="twitter:image" content="%(site)s/assets/og/%(ogfile)s"/>
<link rel="icon" type="image/png" href="%(R)sassets/img/logo.png"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Mulish:wght@400;500;600;700;800&family=Poppins:wght@500;600;700;800&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="%(R)sassets/css/style.css"/>
<script>document.documentElement.classList.remove('no-js');document.documentElement.classList.add('js')</script>
%(ldh)s%(extra)s
</head>
<body class="%(bc)s">
%(sprite)s<a class="skip" href="#main">Skip to content</a>
%(topbar)s%(header)s%(drawer)s
<main id="main">
%(body)s
</main>
%(footer)s%(widgets)s
<script src="%(R)sassets/js/main.js" defer></script>
</body></html>''' % dict(R=R, t=esc(full_title), d=esc(desc), url=url, site=SITE, ogfile=ogfile, ogalt=esc(ogt), ldh=ldh, extra=extra_head, bc=body_class,
                         sprite=SPRITE, topbar=topbar(R), header=header(R, active), drawer=drawer(R), body=body, footer=footer(R), widgets=widgets(R))
    out = os.path.join(ROOT, path, 'index.html') if path else os.path.join(ROOT, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(doc)

def phero(R, title, sub, bg, crumbs, eyebrow=''):
    cr = '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="sep">/</span>'.join(
        ('<a href="%s">%s</a>' % (u(R, p), n)) if p is not None else '<span aria-current="page">%s</span>' % n for n, p in crumbs) + '</nav>'
    return '''<section class="phero" style="padding-bottom:clamp(56px,7vw,90px)"><img src="%s" alt="" fetchpriority="high"/><div class="container">%s%s<h1>%s</h1>%s</div></section>''' % (
        ipath(R, bg), cr, ('<span class="eyebrow">%s</span><br/>' % esc(eyebrow)) if eyebrow else '', esc(title), ('<p class="sub">%s</p>' % esc(sub)) if sub else '')

def sh(eyebrow, title, text='', center=False, extra=''):
    return '<div class="sh%s reveal"><span class="eyebrow">%s</span><h2>%s</h2>%s</div>' % (' center' if center else '', esc(eyebrow), title, ('<p>%s</p>' % text) if text else '')

# ------------------------------------------------------------------ components
def pk_card(R, p, idx=0, listing=False):
    attrs = ''
    if listing:
        attrs = ' data-cat="%s" data-cats="%s" data-price="%d" data-days="%d" data-idx="%d" data-search="%s"' % (
            p['cat'], ' '.join(p['cats']), p['from'], p['days'], idx, esc((p['title'] + ' ' + p['region'] + ' ' + p['subtitle'] + ' ' + ' '.join(p['highlights']) + ' ' + CATNAME[p['cat']]).lower()))
    chips = ''.join('<span>%s</span>' % esc(h) for h in p['highlights'][:3])
    return '''<article class="card pk-card reveal"%s><a class="card-img" href="%s" tabindex="-1" aria-hidden="true"><img src="%s" alt="%s" loading="lazy" width="640" height="440"/>
<span class="tag">%s</span><span class="dur">%s %s</span></a><div class="card-b"><h3><a href="%s">%s</a></h3><p>%s</p><div class="mini">%s</div>
<div class="card-foot"><div class="price"><small>From</small><b>%s</b> <em>pp sharing</em></div><a class="btn btn-dark btn-sm" href="%s">View journey</a></div></div></article>''' % (
        attrs, u(R, p['url']), ipath(R, p['image']), esc(p['title'] + ' — ' + (p['region'] or CATNAME[p['cat']])), esc(p['region'] or CATNAME[p['cat']]),
        ic('clock'), esc(p['duration']), u(R, p['url']), esc(p['title']), esc(p['subtitle']), chips, kes(p['from']), u(R, p['url']))

def faq_html(items, first_open=False):
    out = ''
    for i, (q, a) in enumerate(items):
        out += '<div class="fq reveal%s"><button type="button" aria-expanded="%s">%s %s</button><div class="fq-a"><div><p>%s</p></div></div></div>' % (
            ' open' if (first_open and i == 0) else '', 'true' if (first_open and i == 0) else 'false', esc(q), ic('chev'), esc(a))
    return '<div class="faq">' + out + '</div>'

ALL_FAQ = [(f['question'], f['answer']) for g in D['faq'] for f in g['faqs']]
ALL_FAQ = [(q, a.replace('0115167384 or 011 5171096 or 0115172189 or 254115172784 or 011 5175475', '+254 115 167 384 (more lines are listed on our Contact page)')) for q, a in ALL_FAQ]

def seasons_block(compact=False):
    cls = ['festive', 'shoulder', 'shoulder', 'green', 'green', 'shoulder', 'peak', 'peak', 'peak', 'peak', 'shoulder', 'festive']
    names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    cal = '<div class="seasons reveal">' + ''.join('<div class="mo %s">%s</div>' % (c, n) for c, n in zip(cls, names)) + '</div>'
    leg = '<div class="legend"><span><i style="background:#c0622a"></i>Great Migration / peak</span><span><i style="background:var(--gold-d)"></i>Festive peak</span><span><i style="background:var(--sage)"></i>Shoulder</span><span><i style="background:#3f7d68"></i>Green season value</span></div>'
    k = D['destinations'][0]['bestTimeToVisit']
    cards = ''.join('<div class="sc reveal"><b>%s</b><h3>%s</h3><p>%s</p></div>' % ('Best time', esc(x['name']), esc(x['description'])) for x in k)
    return cal + leg + ('' if compact else '<div class="season-cards">%s</div>' % cards)

def breadcrumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + '/' + p} for i, (n, p) in enumerate(items)]}

# ------------------------------------------------------------------ HOME
def build_home():
    R = ''
    slides = ['laikiapia-sanctuary-ol-lentile-3', 'gamedrives', 'diani-almara', 'couples-2', 'manda-scene-2']
    sl = ''.join('<div class="hero-slide%s"><img src="%s" alt="%s" %s/></div>' % (' on' if i == 0 else '', ipath(R, s), ['Luxury safari lodge at Laikipia', 'Game drive in the Masai Mara', 'Resort pool at Diani Beach', 'Couple on a private bush experience', 'Beach at Manda Bay, Lamu'][i], 'fetchpriority="high"' if i == 0 else 'loading="lazy"') for i, s in enumerate(slides))
    dopts = ''.join('<option value="%s">%s</option>' % (d['name'], d['name']) for d in D['destinations'])
    hero = '''<section class="hero" style="padding:0"><div class="hero-slides">%s</div>
<div class="container"><div class="hero-in"><span class="kicker">%s Boutique safaris &amp; beach escapes</span>
<h1>Travel that moves you. <span>Moments that stay with you.</span></h1>
<p class="lead">Curated safaris, beach escapes, and adventures designed to reconnect you with yourself, your loved ones, and the soul of every place.</p>
<div class="hero-btns"><a class="btn btn-gold" href="%s">Explore Our Experiences %s</a><a class="btn btn-outline" href="%s" target="_blank" rel="noopener">%s Speak to an Expert</a></div></div></div>
<div class="hero-dots" aria-label="Slides"></div></section>
<div class="finder"><div class="container"><form class="finder-box" id="finder" aria-label="Find your journey">
<div><label for="f1">Where to?</label><select id="f1" name="dest"><option value="">Anywhere</option>%s</select></div>
<div><label for="f2">Comfort level</label><select id="f2" name="tier"><option value="budget">Budget</option><option value="midrange" selected>Mid-range</option><option value="luxury">Luxury</option></select></div>
<div><label for="f3">Travelling as</label><select id="f3" name="style"><option>Couple</option><option>Family</option><option>Friends</option><option>Solo</option><option>Multi-generational</option></select></div>
<div><label for="f4">Season</label><select id="f4" name="season"><option>Any time</option><option>Great Migration (Jul–Oct)</option><option>Festive (Dec–Jan)</option><option>Green season (Apr–May)</option></select></div>
<button class="btn btn-gold" type="submit">%s Find my journey</button></form></div></div>''' % (
        sl, ic('star'), u(R, 'experiences/'), ic('arrow'), wa('Hi Pocket of Paradise! I’d like to speak to a safari expert.'), ic('wa'), dopts, ic('search'))

    trust = '<section class="trust" style="padding:26px 0 26px"><div class="container trust-row">%s</div></section>' % ''.join(
        '<div class="trust-it"><span class="ic">%s</span><div><b>%s</b><span>%s</span></div></div>' % (ic(i), t, s) for i, t, s in [
            ('msg', 'Replies in minutes', 'Chat to a consultant on WhatsApp'), ('compass', 'Tailor-made itineraries', 'Every journey shaped around you'),
            ('shield', 'Transparent pricing', 'Clear per-person prices in KES'), ('heart', '24/7 trip support', 'We’re on call throughout your trip')])

    intro = '''<section class="sec-paper"><div class="container intro"><div class="intro-img reveal"><div class="main"><img src="%s" alt="Safari lodge bedroom with thatched ceiling" loading="lazy"/></div>
<div class="badge"><b>10+</b>years of experience</div></div><div class="reveal"><span class="eyebrow">Who we are</span><h2 style="font-size:clamp(1.9rem,3.8vw,3rem);margin-bottom:16px">Boutique Travel. Thoughtfully Crafted.</h2>
<p class="muted">At Pocket of Paradise, we believe travel should be more than visiting a place — it should move you, inspire connection, and create unforgettable moments.</p>
<ul class="checks"><li>%s Personalized itineraries for couples, families, friends, and solo travelers</li><li>%s Access to hidden gems and boutique properties</li><li>%s Experience-first adventures curated by experts</li></ul>
<a class="btn btn-dark" href="%s">Discover How We Travel Differently %s</a></div></div></section>''' % (
        ipath(R, 'base-camp-masai-mara-1'), ic('check'), ic('check'), ic('check'), u(R, 'about-us/'), ic('arrow'))

    featured = ['masai-mara-express', 'great-migration-safari', 'diani-beach-escape', 'romantic-kenya-honeymoon', 'zanzibar-escape', 'maldives-honeymoon']
    tabs = '<div class="chips" data-tabs="#homePk" role="group" aria-label="Filter journeys">' + ''.join(
        '<button class="chip%s" data-f="%s">%s</button>' % (' on' if c == 'all' else '', c, n) for c, n in [('all', 'Featured'), ('kenya', 'Kenya Safari'), ('zanzibar', 'Zanzibar'), ('couples', 'Couples'), ('outbound', 'Outbound')]) + '</div>'
    hp = [PKID[i] for i in featured]
    for c in ['kenya', 'zanzibar', 'couples', 'outbound']:
        for p in PK:
            if c in p['cats'] and p not in hp and len([x for x in hp if c in x['cats']]) < 3:
                hp.append(p)
    homepk = '<div class="grid g3" id="homePk">' + ''.join(pk_card(R, p).replace('<article class="card pk-card reveal"', '<article class="card pk-card reveal" %sdata-cat="%s"' % ('' if p['id'] in featured else 'style="display:none" ', ' '.join(p['cats']) + (' all' if p['id'] in featured else '')), 1) for p in hp) + '</div>'
    packages = '''<section class="sec-light"><div class="container"><div class="sh-row"><div class="sh reveal"><span class="eyebrow">Ready-to-book journeys</span><h2>Handpicked packages for every kind of traveller</h2><p>Clear per-person prices in KES, three comfort levels, named lodges and day-by-day itineraries.</p></div>%s</div>%s
<div style="text-align:center;margin-top:40px"><a class="btn btn-dark" href="%s">View all %d journeys %s</a></div></div></section>''' % (tabs, homepk, u(R, 'packages/'), len(PK), ic('arrow'))

    dgrid = '<div class="dest-grid">' + ''.join('<a class="dest reveal" href="%s"><img src="%s" alt="%s" loading="lazy"/><div><h3>%s</h3><span>%s</span></div><span class="go">%s</span></a>' % (
        u(R, 'destinations/%s/' % d['id']), ipath(R, img(d['coverImage'])), esc(d['name']), d['name'], esc(d['countryTag']), ic('arrow')) for d in D['destinations']) + '</div>'
    dests = '<section class="sec-paper"><div class="container">%s%s</div></section>' % (
        sh('Destinations', 'Explore the world with us', 'From African safaris to tropical islands, discover handpicked destinations curated for unforgettable experiences.'), dgrid)

    seasons = '<section class="sec-light"><div class="container">%s%s</div></section>' % (sh('Safari seasons', 'When is the best time to go?', 'Every month has its magic. Use the calendar to match your dates to the season that suits you — rates can vary between peak, shoulder and value seasons.'), seasons_block())

    sg = '<div class="style-grid">' + ''.join('<a class="style reveal" href="%s"><img src="%s" alt="%s" loading="lazy"/><div><h3>%s</h3><p>%s</p></div></a>' % (
        u(R, 'travel-styles/%s/' % s['id']), ipath(R, img(s['image'])), esc(s['title']), esc(s['title']), esc(s['tagline'])) for s in D['styles']) + '</div>'
    styles = '<section class="sec-dark"><div class="container">%s%s</div></section>' % (sh('Travel styles', 'Curated experiences for every traveler', 'No two travelers are the same. We design journeys around emotion, connection, and intention.'), sg)

    promise = '<section class="sec-paper"><div class="container">%s<div class="grid g3">%s</div></div></section>' % (
        sh('Our promise', 'Travel made intimate, effortless, and unforgettable', center=True),
        ''.join('<div class="feat reveal"><div class="ic">%s</div><h3>%s</h3><p>%s</p></div>' % (ic(i), t, d) for i, t, d in [
            ('heart', 'Connection', 'Every journey brings you closer — to yourself, your loved ones, and the places you visit.'),
            ('compass', 'Expertise', 'Local knowledge, curated experiences, and seamless planning.'),
            ('star', 'Wonder', 'From safaris to beaches to hidden escapes, each moment is designed to inspire awe.')]))

    cats = D['experience_categories']
    ex = '<div class="exp">' + ''.join('<a href="%s" class="reveal"><img src="%s" alt="%s" loading="lazy"/><div><h3>%s</h3><p>%s</p></div></a>' % (
        u(R, 'experiences/%s/' % k), ipath(R, img(v['heroImage'])), esc(v['title']), esc(v['title']), esc(v['tagline'])) for k, v in cats.items()) + '</div>'
    exps = '<section class="sec-light"><div class="container"><div class="sh-row"><div class="sh reveal"><span class="eyebrow">Experiences</span><h2>Beyond lodges — travel that feels like home</h2><p>From private quad-biking in the dunes to sundowners overlooking the savannah, we craft moments that transform ordinary vacations into something extraordinary.</p></div><a class="btn btn-line" href="%s">Explore all experiences %s</a></div>%s</div></section>' % (u(R, 'experiences/'), ic('arrow'), ex)

    lod = []
    for p in D['kenya_packages']:
        for s in p['whereYoullStay']:
            if s['name'] not in [x[0] for x in lod]:
                lod.append((s['name'], s['tier'], s['description'], s['images'][0], p['id']))
    lodges = '<section class="sec-dark"><div class="container">%s<div class="lodges">%s</div></div></section>' % (
        sh('Where you’ll stay', 'Boutique lodges, camps &amp; beach resorts', 'Named properties on every package — from comfortable tented camps to exclusive luxury lodges.'),
        ''.join('<a class="lodge" href="%s"><img src="%s" alt="%s" loading="lazy"/><div><small>%s</small><h3>%s</h3><p>%s</p></div></a>' % (u(R, 'destinations/kenya/%s/' % pid), ipath(R, img(im)), esc(n), esc(t), esc(n), esc(dsc)) for n, t, dsc, im, pid in lod))

    stats = '<section class="stats"><div class="container stats-row">%s</div></section>' % ''.join(
        '<div class="stat reveal"><b data-count="%d" data-suffix="+">0</b><span>%s</span></div>' % (n, l) for n, l in [(10, 'Years of Experience'), (2500, 'Happy Travellers'), (50, 'Destinations Covered'), (500, 'Safaris Organized')])

    gal_items = [('Wildlife', 'u-1547970810-dc1eac37d174', 'Elephant in golden grass'), ('Wildlife', 'maasai-mara-8', 'Great Migration crossing'), ('Wildlife', 'african-lion-couple-and-safari-jeep', 'Lions and a safari jeep'),
                 ('Wildlife', 'amboseli-elephants-850x540', 'Elephants beneath Kilimanjaro'), ('Lodges', 'mara-engai-2', 'Mara Engai Wilderness Lodge'), ('Lodges', 'ashnil-mara-1', 'Ashnil Mara Camp'),
                 ('Lodges', 'samburu-accommodation', 'Samburu lodge'), ('Lodges', 'laikiapia-sanctuary-ol-lentile-5', 'Laikipia suite'), ('Beach', 'diani-almara', 'Diani Beach pool'),
                 ('Beach', 'activities-dhow', 'Dhow in turquoise water'), ('Beach', 'manda-scene-2', 'Manda Bay beach'), ('Beach', 'u-1590523741831-ab7e8b8f9c', 'Zanzibar shoreline'),
                 ('Culture', 'culture-2', 'Meeting the Maasai'), ('Culture', 'couples-5', 'Sunset at the bush camp'), ('Culture', 'camel-safaris', 'Camel safari'), ('Culture', 'horse', 'Horseback safari')]
    gal = '<div class="gal" id="gal">' + ''.join('<button data-cat="%s" data-lb="home"><img src="%s" alt="%s" loading="lazy"/></button>' % (c.lower(), ipath(R, i), a) for c, i, a in gal_items) + '</div>'
    gtabs = '<div class="chips" data-tabs="#gal" style="margin-bottom:28px">' + ''.join('<button class="chip%s" data-f="%s">%s</button>' % (' on' if c == 'all' else '', c, n) for c, n in [('all', 'All'), ('wildlife', 'Wildlife'), ('lodges', 'Lodges'), ('beach', 'Beaches'), ('culture', 'Culture')]) + '</div>'
    gallery = '<section class="sec-paper" id="gallery"><div class="container">%s%s%s</div></section>' % (sh('Gallery', 'Moments from the journey'), gtabs, gal)

    how = '<section class="sec-light"><div class="container">%s<div class="steps">%s</div></div></section>' % (
        sh('How it works', 'From first message to the trip of a lifetime', center=True),
        ''.join('<div class="step reveal"><span class="feat" style="padding:0;border:0;background:none"><span class="ic" style="width:52px;height:52px;margin-bottom:0">%s</span></span><h3>%s</h3><p>%s</p></div>' % (ic(i), t, d) for i, t, d in [
            ('msg', 'Tell us your dream', 'Share dates, budget and who’s travelling — by form or WhatsApp.'),
            ('map', 'We design your journey', 'A tailor-made itinerary with named lodges and clear pricing.'),
            ('shield', 'Confirm with a deposit', 'Secure your dates; balance is due before departure.'),
            ('sun', 'Travel with support', 'Guides, transfers and 24/7 ground support throughout.')]))

    T = [{'quote': 'Our safari through the Masai Mara was absolutely breathtaking — every sunrise felt like magic. The team at Pocket of Paradise made everything seamless!', 'name': 'Sarah M.', 'role': 'Adventure Traveller', 'img': ipath(R, 'u-1547970810-dc1eac37d174')},
         {'quote': 'From Diani’s white sands to Amboseli’s elephants, this trip redefined luxury travel for us. Thank you for the unforgettable memories!', 'name': 'James K.', 'role': 'Photographer', 'img': ipath(R, 'maasai-mara-8')},
         {'quote': 'Every detail was thoughtfully planned — from our private lodge to the sunset dinners in the wild. Highly recommended!', 'name': 'Lydia W.', 'role': 'Luxury Explorer', 'img': ipath(R, 'u-1575999502951-4ab25b5ca8')}]
    tst = '''<section class="sec-dark"><div class="container">%s<div class="tst"><div class="tst-img"><img id="tim" src="%s" alt="Guest photo from a Pocket of Paradise journey"/></div>
<div><div class="stars" aria-label="5 out of 5 stars">★★★★★</div><p class="tst-q" id="tq" aria-live="polite"></p><div class="tst-who"><b id="tn"></b><span id="td"></span></div>
<div class="arrows"><button id="tprev" aria-label="Previous review">%s</button><button id="tnext" aria-label="Next review">%s</button></div>
<p style="margin-top:22px;font-size:.88rem;color:#b3a695">Travelled with us? <a style="color:var(--gold2);text-decoration:underline" href="%s">Share your story</a>.</p></div></div>
<script type="application/json" id="tdata">%s</script></div></section>''' % (sh('Guest stories', 'What our guests are saying'), T[0]['img'], ic('left'), ic('right'), u(R, 'contact/'), json.dumps(T).replace('</', '<\\/'))

    blog = sorted(D['blog'], key=lambda b: datetime.datetime.strptime(b['date'], '%B %d, %Y'), reverse=True)[:3]
    blogsec = '<section class="sec-light"><div class="container"><div class="sh-row"><div class="sh reveal"><span class="eyebrow">Travel journal</span><h2>Guides, tips &amp; stories</h2></div><a class="btn btn-line" href="%s">Visit the blog %s</a></div><div class="grid g3">%s</div></div></section>' % (
        u(R, 'blog/'), ic('arrow'), ''.join(blog_card(R, b) for b in blog))

    faq = '<section class="sec-paper"><div class="container"><div class="faq-wrap"><div>%s%s</div><aside class="side-card reveal"><h3>Still have questions?</h3><p>Our travel consultants reply quickly on WhatsApp and are happy to help you plan.</p><a class="btn btn-wa btn-block" href="%s" target="_blank" rel="noopener">%s Chat with us</a><a class="btn btn-outline btn-block" style="margin-top:10px" href="%s">All FAQs</a></aside></div></div></section>' % (
        sh('FAQs', 'Quick answers before you book'), faq_html(ALL_FAQ[:5], True), wa('Hi Pocket of Paradise! I have a question about booking.'), ic('wa'), u(R, 'faqs/'))

    body = hero + trust + intro + packages + dests + seasons + styles + promise + exps + lodges + stats + gallery + how + tst + blogsec + faq + cta_band(R)
    page('', 'Luxury Safari & Beach Holidays in Kenya, Maldives, Bali', 'Handcrafted luxury safaris in Kenya, beach escapes in Zanzibar and the Maldives, and romantic getaways — boutique travel from Pocket of Paradise.', body, 'home', og='laikiapia-sanctuary-ol-lentile-3')

def blog_image(b):
    M = {'discover-kenyas-majestic-masai-mara': 'u-1547970810-dc1eac37d174', 'top-5-luxury-safari-lodges-2025': 'mara-engai-1', 'capturing-the-magic-photography-on-safari': 'u-1516426122078-c23e763198',
         'cultural-journeys-meet-the-samburu-maasai': 'culture-2', 'how-to-prepare-for-your-first-safari': 'gamedrives', 'diani-diaries-beach-bliss-after-safari': 'couples-3',
         'best-time-to-visit-masai-mara-safari-guide': 'maasai-mara-8', 'kenya-safari-cost-budget-vs-luxury-2026': 'u-1493246507139-91e8fad997', 'honeymoon-safari-kenya-romantic-itineraries': 'couples-2',
         'family-safari-kenya-traveling-with-kids-guide': 'family-and-friends', 'amboseli-national-park-safari-guide-elephants-kilimanjaro': 'amboseli-elephants-850x540', 'kenya-vs-tanzania-safari-which-is-better': 'u-1544735716-392fe2489ffa'}
    return M.get(b['id']) or img(b['heroImage'])

def blog_card(R, b, listing=False):
    attrs = ' data-cat="%s" data-search="%s"' % (esc(b['category']), esc((b['title'] + ' ' + b['excerpt'] + ' ' + ' '.join(b['tags'])).lower())) if listing else ''
    return '''<article class="card post reveal"%s><a class="card-img" href="%s" tabindex="-1" aria-hidden="true"><img src="%s" alt="%s" loading="lazy" width="640" height="440"/><span class="tag gold">%s</span></a>
<div class="card-b"><div class="meta"><span>%s</span><span>%s</span></div><h3><a href="%s">%s</a></h3><p>%s</p><div class="card-foot"><a class="btn btn-line btn-sm" href="%s">Read article %s</a></div></div></article>''' % (
        attrs, u(R, 'blog/%s/' % b['id']), ipath(R, blog_image(b)), esc(b['title']), esc(b['category']), esc(b['date']), esc(b['readTime']), u(R, 'blog/%s/' % b['id']), esc(b['title']), esc(b['excerpt']), u(R, 'blog/%s/' % b['id']), ic('arrow'))

# ------------------------------------------------------------------ PACKAGES
def build_packages():
    R = '../'
    def listing(path, start, title, sub, active_label):
        R = '../' * path.count('/')
        chips = '<div class="chips" id="pkChips" role="group" aria-label="Filter by category">' + ''.join(
            '<button class="chip" data-f="%s">%s</button>' % (c, n) for c, n in [('all', 'All Packages'), ('kenya', 'Kenya'), ('zanzibar', 'Zanzibar'), ('couples', 'Couples'), ('outbound', 'Outbound')]) + '</div>'
        cards = ''.join(pk_card(R, p, i, True) for i, p in enumerate(PK))
        body = phero(R, title, sub, 'diani-almara-2', [('Home', ''), ('Packages', None)], 'Packages') + '''<section class="sec-light" id="list"><div class="container">
<div class="toolbar">%s<div style="display:flex;gap:10px;flex-wrap:wrap;flex:1;justify-content:flex-end"><div class="search">%s<label class="sr-only" for="pkSearch">Search journeys</label><input id="pkSearch" type="search" placeholder="Search destinations, lodges…"/></div>
<label class="sr-only" for="pkSort">Sort</label><select class="sel" id="pkSort"><option value="rec">Recommended</option><option value="low">Price: low to high</option><option value="high">Price: high to low</option><option value="short">Shortest first</option></select></div></div>
<p id="pkCount" style="font-weight:700;margin-bottom:20px;color:var(--muted)" aria-live="polite"></p>
<div class="grid g3" id="pkList" data-start="%s">%s<div class="empty" id="pkEmpty" style="display:none"><h3>No journeys match your search</h3><p class="muted" style="margin:8px 0 18px">Try another destination or clear the filters.</p><button class="btn btn-dark" id="pkClear">Clear filters</button></div></div>
<div class="note" style="margin-top:34px;text-align:center;color:var(--muted);font-size:.9rem">All prices are in Kenya shillings (KES), per person sharing. Rates can vary by season — request a quote to confirm your dates.</div></div></section>''' % (
            chips, ic('search'), start, cards)
        body += '''<section class="sec-dark" style="padding:70px 0"><div class="container" style="text-align:center"><h2 style="font-size:clamp(1.7rem,3.2vw,2.4rem);margin-bottom:12px">Need a custom package?</h2><p class="muted" style="margin-bottom:24px">Can’t find exactly what you’re looking for? Let us design a bespoke itinerary just for you.</p><a class="btn btn-gold" href="%s">Build my custom tour %s</a></div></section>''' % (u(R, 'create-tour-plan/'), ic('arrow'))
        page(path, title, sub, body, 'pk', ld=breadcrumbs_ld([('Home', ''), ('Packages', 'packages/')]))
    listing('packages/', 'all', 'Ready-to-Book Journeys', 'Carefully crafted itineraries with flexible options to suit every budget and preference.', 'All')
    for c in CATNAME:
        listing('packages/%s/' % c, c, '%s Packages' % CATNAME[c], 'Handpicked %s journeys with clear per-person prices.' % CATNAME[c].lower(), CATNAME[c])
    for p in PK:
        build_package_detail(p)

def build_package_detail(p):
    R = '../' * p['url'].count('/')
    gal = p['gallery'][:5]
    while len(gal) < 3 and gal:
        gal.append(gal[0])
    pg = '<div class="pk-gal">' + ''.join('<button data-lb="pk" aria-label="Open photo %d"><img src="%s" data-full="%s" alt="%s — photo %d" %s/>%s</button>' % (
        i + 1, ipath(R, g), ipath(R, g), esc(p['title']), i + 1, 'fetchpriority="high"' if i == 0 else 'loading="lazy"', ('<span class="more">%s View all photos</span>' % ic('camera')) if i == 0 and len(p['gallery']) > 1 else '') for i, g in enumerate(gal)) + '</div>'
    facts = [('Duration', p['duration']), ('Journey type', p['journey']), ('Region', p['region'])]
    if p['best']:
        facts.append(('Best time', p['best']))
    if p['pace']:
        facts.append(('Pace', p['pace']))
    facts.append(('From', kes(p['from']) + ' pp'))
    facts = [f for f in facts if f[1]][:5]
    fh = '<div class="facts">' + ''.join('<div class="fact"><small>%s</small><b>%s</b></div>' % (a, esc(b)) for a, b in facts) + '</div>'
    multi = len(p['tiers']) > 1
    tier_h = ''
    if multi:
        tier_h = '<h2>Choose your comfort level</h2><p>All prices in KES, per person sharing. Select a level to update your estimate.</p><div class="tiers">' + ''.join(
            '<button type="button" class="tier%s" data-k="%s"><small>%s</small><b>%s</b><span>%s</span></button>' % (' on' if k == 'midrange' else '', k, t['label'], kes(t['price']), esc(t['stay'])) for k, t in p['tiers'].items()) + '</div>'
    stay_h = ''
    if p['stay']:
        stay_h = '<h2>Where you’ll stay</h2><div class="stay">' + ''.join('<div class="stay-c"><img src="%s" alt="%s" loading="lazy"/><div><small>%s</small><h3>%s</h3><p>%s</p></div></div>' % (
            ipath(R, img(s['images'][0])), esc(s['name']), esc(s['tier']), esc(s['name']), esc(s['description'])) for s in p['stay']) + '</div>'
    elif list(p['tiers'].values())[0]['stay']:
        stay_h = '<h2>Where you’ll stay</h2><p><b>%s</b></p>' % esc(list(p['tiers'].values())[0]['stay'])
    itin = '<div class="itin">' + ''.join('<div class="it%s"><button type="button" aria-expanded="%s"><span class="d"><span><small>DAY</small>%s</span></span><b>%s</b>%s</button><div class="it-a"><div><p>%s</p></div></div></div>' % (
        ' open' if i == 0 else '', 'true' if i == 0 else 'false', d, esc(t), ic('chev'), esc(desc)) for i, (d, t, desc) in enumerate(p['itin'])) + '</div>'
    tiers_json = {k: dict(label=t['label'], price=t['price'], stay=t['stay']) for k, t in p['tiers'].items()}
    default = 'midrange' if 'midrange' in tiers_json else list(tiers_json)[0]
    pdata = json.dumps(dict(id=p['id'], title=p['title'], tiers=tiers_json, defaultTier=default)).replace('</', '<\\/')
    tier_select = '<div class="f-row"><label for="bTier">Comfort level</label><select id="bTier">%s</select></div>' % ''.join('<option value="%s"%s>%s — %s</option>' % (k, ' selected' if k == default else '', t['label'], kes(t['price'])) for k, t in p['tiers'].items())
    book = '''<aside class="book" id="book"><h3>Your estimate</h3><div class="pr" id="bPrice">%s</div><small class="muted" id="bTierName"></small><span class="muted" style="font-size:.8rem"> per person sharing</span>
%s<div class="f-row"><label for="bMonth">Travel month</label><select id="bMonth" data-months><option value="">Select month…</option></select></div>
<div class="f-row"><span class="lbl" style="display:block;font-weight:800;font-size:.74rem;letter-spacing:.1em;text-transform:uppercase;color:var(--gold-d);margin-bottom:6px">Travellers</span><div class="stepper"><button type="button" id="bMinus" aria-label="Fewer travellers">−</button><output id="bPax" aria-live="polite">2</output><button type="button" id="bPlus" aria-label="More travellers">+</button></div></div>
<div class="est"><small>Estimated total (sharing basis)</small><b id="bEst">—</b></div>
<a class="btn btn-gold btn-block" id="bQuote" href="#">Request this quote %s</a><a class="btn btn-wa btn-block" id="bWa" href="#" target="_blank" rel="noopener">%s Chat on WhatsApp</a>
<button class="btn btn-line btn-block" data-print type="button">%s Save itinerary as PDF</button>
<div class="share"><span>Share</span><a href="https://wa.me/?text=%s" target="_blank" rel="noopener" aria-label="Share on WhatsApp">wa</a><a href="https://www.facebook.com/sharer/sharer.php?u=%s" target="_blank" rel="noopener" aria-label="Share on Facebook">f</a><button type="button" data-copy aria-label="Copy link">%s</button></div>
<p class="note">Estimate only. Final rates depend on travel dates, season and availability, and are confirmed in your written quote. Single supplements may apply.</p></aside>''' % (
        kes(p['tiers'][default]['price']), tier_select, ic('arrow'), ic('wa'), ic('print'), quote(SITE + '/' + p['url']), quote(SITE + '/' + p['url']), ic('share'))
    hl = '<ul class="hl">' + ''.join('<li>%s<span>%s</span></li>' % (ic('check'), esc(h)) for h in p['highlights']) + '</ul>'
    inex = '<div class="inex"><div class="yes"><h3>What’s included</h3><ul>%s</ul></div><div class="no"><h3>What’s not included</h3><ul>%s</ul></div></div>' % (
        ''.join('<li>%s<span>%s</span></li>' % (ic('check'), esc(x)) for x in p['inc']), ''.join('<li>%s<span>%s</span></li>' % (ic('x'), esc(x)) for x in p['exc']))
    rel = [x for x in PK if x['id'] != p['id'] and (x['cat'] == p['cat'] or set(x['cats']) & set(p['cats']))][:3]
    relh = '<section class="sec-light"><div class="container">%s<div class="grid g3">%s</div></div></section>' % (sh('You may also like', 'More journeys to explore'), ''.join(pk_card(R, x) for x in rel))
    season = '<h2>Seasons &amp; rates</h2><p>Prices are shown per person sharing and can change with the season. Peak periods (Great Migration, July–October, and the festive season) are the busiest — book early for the best choice of lodges.</p>' + seasons_block(True)
    main = '<div class="pk-main"><h2>Trip overview</h2><p>%s</p><h2>Trip highlights</h2>%s%s%s<h2>Day-by-day itinerary</h2><p><button class="btn btn-line btn-sm" id="expandAll" type="button">Expand all days</button></p>%s%s<h2>Inclusions &amp; exclusions</h2>%s</div>' % (
        esc(p['overview']), hl, tier_h, stay_h, itin, season, inex)
    sub = p['subtitle']
    crumbs = [('Home', ''), ('Destinations', 'destinations/'), ('Kenya', 'destinations/kenya/'), (p['title'], None)] if p['cat'] == 'kenya' else [('Home', ''), ('Packages', 'packages/'), (CATNAME[p['cat']], 'packages/%s/' % p['cat']), (p['title'], None)]
    body = phero(R, p['title'], sub, p['gallery'][0], crumbs, CATNAME[p['cat']] + ' package') + '<section class="sec-light" style="padding-top:0"><div class="container">' + fh + '<div style="height:36px"></div>' + pg + '<div class="pk-layout">' + main + book + '</div></div></section>' + relh + cta_band(R, 'Ready to book this journey?', '%s — from %s per person sharing. Contact us for a personalised quote or to customise this itinerary.' % (p['title'], kes(p['from'])), p['gallery'][0])
    mbar = '<div class="mbar"><div class="price"><small>From</small><b id="mbPrice">%s</b></div><a class="btn btn-gold btn-sm" id="mbQuote" href="#">Request quote</a></div>' % kes(p['from'])
    ld = [{"@context": "https://schema.org", "@type": "TouristTrip", "name": p['title'], "description": p['overview'], "image": SITE + '/assets/img/%s.webp' % p['image'],
           "offers": {"@type": "Offer", "priceCurrency": "KES", "price": str(p['from']), "url": SITE + '/' + p['url']}, "provider": {"@type": "TravelAgency", "name": "Pocket of Paradise"}},
          breadcrumbs_ld([(n, pp or p['url']) for n, pp in crumbs])]
    page(p['url'], '%s — %s' % (p['title'], CATNAME[p['cat']] + ' Package'), '%s From %s per person sharing. %s' % (sub, kes(p['from']), p['overview'][:110]), body + mbar + '<script type="application/json" id="pdata">%s</script>' % pdata, 'pk' if p['cat'] != 'kenya' else 'dest', og=p['image'], ld=ld)

# ------------------------------------------------------------------ DESTINATIONS
def build_destinations():
    R = '../'
    cards = ''
    for d in D['destinations']:
        txt = d['overview']
        cards += '''<div class="two reveal" style="margin-bottom:64px"><div style="order:%d"><span class="eyebrow">%s</span><h2 style="font-size:clamp(1.8rem,3.4vw,2.6rem);margin-bottom:10px">%s</h2><p style="font-weight:700;color:var(--gold-d);margin-bottom:10px">%s</p><p class="muted" style="margin-bottom:22px">%s</p>
<a class="btn btn-dark" href="%s">Explore %s %s</a></div><img src="%s" alt="%s" loading="lazy"/></div>''' % (
            0 if D['destinations'].index(d) % 2 == 0 else 1, 'Destination', d['name'], esc(d['countryTag']), esc(txt[:330] + ('…' if len(txt) > 330 else '')),
            u(R, 'destinations/%s/' % d['id']), d['name'], ic('arrow'), ipath(R, img(d['coverImage'])), esc(d['name']))
    body = phero(R, 'Explore the World With Us', 'From African safaris to tropical islands, discover handpicked destinations curated for unforgettable experiences.', 'hero-image-1', [('Home', ''), ('Destinations', None)], 'Discover') + \
        '<section class="sec-light"><div class="container">%s</div></section>' % cards + cta_band(R, 'Can’t decide where to go?', 'Let our travel experts help you choose the perfect destination based on your interests, budget, and travel style.')
    page('destinations/', 'Safari & Beach Destinations', 'Discover handpicked destinations — Kenya, Tanzania, Zanzibar, Maldives, Bali and Thailand — curated for unforgettable experiences.', body, 'dest', ld=breadcrumbs_ld([('Home', ''), ('Destinations', 'destinations/')]))

    REL = {'kenya': lambda p: p['cat'] == 'kenya', 'zanzibar': lambda p: p['cat'] == 'zanzibar', 'maldives': lambda p: p['id'] == 'maldives-honeymoon', 'bali': lambda p: p['id'] == 'bali-love-journey', 'thailand': lambda p: p['id'] == 'thailand-phuket-krabi', 'tanzania': lambda p: p['id'] in ('great-migration-safari', 'zanzibar-escape')}
    for d in D['destinations']:
        R = '../../'
        gal = [img(x) for x in d['coverImages']][:5]
        covers = '<div class="pk-gal">' + ''.join('<button data-lb="dg" aria-label="Open photo %d"><img src="%s" data-full="%s" alt="%s photo %d" loading="lazy"/></button>' % (i + 1, ipath(R, g), ipath(R, g), esc(d['name']), i + 1) for i, g in enumerate(gal)) + '</div>'
        best = '<div class="grid g4">' + ''.join('<div class="sc reveal"><b>Best time</b><h3>%s</h3><p>%s</p></div>' % (esc(b['name']), esc(b['description'])) for b in d['bestTimeToVisit']) + '</div>'
        todo = '<div class="grid g3">' + ''.join('<div class="act reveal"><h3>%s</h3><p>%s</p></div>' % (esc(t['todoName']), esc(t['todoDescription'])) for t in d['whatToDo']) + '</div>'
        pkgs = [p for p in PK if REL[d['id']](p)]
        pk_sec = ''
        if pkgs:
            pk_sec = '<section class="sec-light"><div class="container">%s<div class="grid g3">%s</div></div></section>' % (sh('%s packages' % d['name'], 'Carefully curated %s journeys' % d['name'], 'All prices in KES per person sharing.'), ''.join(pk_card(R, p) for p in pkgs))
        seas = '<section class="sec-paper"><div class="container">%s%s</div></section>' % (sh('Seasons', 'Plan around the seasons'), seasons_block(True)) if d['id'] == 'kenya' else ''
        body = phero(R, d['name'], d['countryTag'], img(d['coverImage']), [('Home', ''), ('Destinations', 'destinations/'), (d['name'], None)], 'Discover') + \
            '<section class="sec-paper"><div class="container"><div style="max-width:860px"><span class="eyebrow">Overview</span><h2 style="font-size:clamp(1.8rem,3.4vw,2.6rem);margin-bottom:14px">Why visit %s</h2><p class="muted" style="font-size:1.08rem">%s</p></div><div style="height:34px"></div>%s</div></section>' % (d['name'], esc(d['overview']), covers) + \
            '<section class="sec-light"><div class="container">%s%s</div></section>' % (sh('Best time to visit', 'When to go to %s' % d['name']), best) + \
            '<section class="sec-paper"><div class="container">%s%s</div></section>' % (sh('What to do', 'Experiences in %s' % d['name']), todo) + seas + pk_sec + cta_band(R, 'Ready to explore %s?' % d['name'], 'Let us craft your perfect %s experience.' % d['name'], img(d['coverImage']))
        page('destinations/%s/' % d['id'], '%s — %s' % (d['name'], d['countryTag']), d['overview'][:155], body, 'dest', og=img(d['coverImage']), ld=breadcrumbs_ld([('Home', ''), ('Destinations', 'destinations/'), (d['name'], 'destinations/%s/' % d['id'])]))

# ------------------------------------------------------------------ STYLES / EXPERIENCES
STYLE_REL = {'couples-escapes': lambda p: 'couples' in p['cats'], 'family-journeys': lambda p: p['id'] in ('kenya-bush-and-beach', 'diani-beach-escape', 'amboseli-mara-classic'),
             'solo-travel': lambda p: p['id'] in ('masai-mara-express', 'laikipia-wilderness-mara', 'diani-beach-escape'), 'multi-generational': lambda p: p['id'] in ('amboseli-mara-classic', 'kenya-bush-and-beach', 'zanzibar-escape'),
             'outbound-travel': lambda p: p['cat'] == 'outbound'}
def build_styles():
    R = '../'
    tiles = ''.join('''<div class="two reveal" style="margin-bottom:60px"><div style="order:%d"><span class="eyebrow">Travel style</span><h2 style="font-size:clamp(1.7rem,3.2vw,2.5rem);margin-bottom:8px">%s</h2><p style="font-weight:700;color:var(--gold-d);margin-bottom:10px">%s</p><p class="muted" style="margin-bottom:16px">%s</p>
<p class="mini" style="margin-bottom:20px"><span>%s</span></p><a class="btn btn-dark" href="%s">Explore %s %s</a></div><img src="%s" alt="%s" loading="lazy"/></div>''' % (
        i % 2, esc(s['title']), esc(s['tagline']), esc(s['description']), esc(s['howItFeels']), u(R, 'travel-styles/%s/' % s['id']), esc(s['title']), ic('arrow'), ipath(R, img(s['image'])), esc(s['title'])) for i, s in enumerate(D['styles']))
    pillars = '<div class="grid g4">' + ''.join('<div class="feat reveal"><div class="ic">%s</div><h3>%s</h3><p>%s</p></div>' % (ic(i), t, d) for i, t, d in [
        ('heart', 'Emotion over itinerary', 'We design journeys around how you want to feel, not just where you want to go.'), ('users', 'Connection first', 'Every experience is crafted to deepen relationships and create shared memories.'),
        ('compass', 'Personalization', 'No two journeys are the same. Each trip is tailored to your unique story.'), ('sun', 'Unhurried pace', 'We believe in slow travel that allows you to truly absorb each moment.')]) + '</div>'
    feat = '<div class="grid g4">' + ''.join('<a class="card reveal" href="%s"><div class="card-img"><img src="%s" alt="%s" loading="lazy"/><span class="dur">%s %s</span></div><div class="card-b"><h3>%s</h3><p>%s</p></div></a>' % (
        u(R, 'create-tour-plan/'), ipath(R, img(j['image'])), esc(j['title']), ic('clock'), esc(j['duration']), esc(j['title']), esc(j['style'])) for j in D['featured_journeys']) + '</div>'
    body = phero(R, 'Travel Styles', 'No two travelers are the same. We design journeys around emotion, connection, and intention.', 'laikiapia-sanctuary-ol-lentile-2', [('Home', ''), ('Travel Styles', None)], 'Discover') + \
        '<section class="sec-paper"><div class="container">%s%s</div></section>' % (sh('Travel designed around meaning', 'How do you want to travel?', 'Our travel styles reflect different life moments, relationships, and ways of exploring the world. Each journey is tailored, unhurried, and deeply personal.', True), pillars) + \
        '<section class="sec-light"><div class="container">%s</div></section>' % tiles + \
        '<section class="sec-dark"><div class="container">%s%s</div></section>' % (sh('Featured journeys', 'Sample trips to spark ideas'), feat) + cta_band(R, 'Ready to design your journey?', 'Tell us about your travel dreams, and we’ll craft a journey that reflects your unique story, relationships, and the way you want to feel.')
    page('travel-styles/', 'Travel Styles — Journeys Designed Around How You Want to Feel', 'Couples escapes, family journeys, solo travel, multi-generational trips and outbound holidays, tailored around emotion and connection.', body, 'style', ld=breadcrumbs_ld([('Home', ''), ('Travel Styles', 'travel-styles/')]))
    for s in D['styles']:
        R = '../../'
        ideal = '<ul class="hl">' + ''.join('<li>%s<span>%s</span></li>' % (ic('check'), esc(x)) for x in s.get('idealFor', [])) + '</ul>'
        sig = '<ul class="hl">' + ''.join('<li>%s<span>%s</span></li>' % (ic('star'), esc(x)) for x in s['signatureExperiences']) + '</ul>'
        dest = ('<h2>Destinations include</h2><p class="mini" style="margin-bottom:10px">%s</p>' % ''.join('<span>%s</span>' % esc(x) for x in s['destinations'])) if s.get('destinations') else ''
        rel = [p for p in PK if STYLE_REL[s['id']](p)][:3]
        relh = '<section class="sec-light"><div class="container">%s<div class="grid g3">%s</div></div></section>' % (sh('Journeys for you', 'Suggested %s journeys' % s['title'].lower()), ''.join(pk_card(R, p) for p in rel)) if rel else ''
        others = '<section class="sec-paper"><div class="container">%s<div class="chips">%s</div></div></section>' % (sh('More ways to travel', 'Explore other travel styles'), ''.join('<a class="chip" href="%s">%s</a>' % (u(R, 'travel-styles/%s/' % x['id']), esc(x['title'])) for x in D['styles'] if x['id'] != s['id']))
        body = phero(R, s['title'], s['tagline'], img(s['image']), [('Home', ''), ('Travel Styles', 'travel-styles/'), (s['title'], None)], 'Travel style') + \
            '<section class="sec-paper"><div class="container"><div class="two"><div><span class="eyebrow">How it feels</span><h2 style="font-size:clamp(1.8rem,3.4vw,2.6rem);margin-bottom:14px">%s</h2><p class="muted" style="font-size:1.08rem;margin-bottom:18px">%s</p><div class="mini"><span style="font-size:.9rem;padding:6px 16px">%s</span></div></div><img src="%s" alt="%s" loading="lazy"/></div>' % (
                esc(s['tagline']), esc(s['description']), esc(s['howItFeels']), ipath(R, img(s['image'])), esc(s['title'])) + \
            '<div class="pk-main" style="margin-top:50px">%s<h2>Signature experiences</h2>%s%s</div></div></section>' % (('<h2>Ideal for</h2>' + ideal) if s.get('idealFor') else '', sig, dest) + relh + others + cta_band(R, 'Ready to design your %s journey?' % s['title'].lower(), 'Tell us what you have in mind and we’ll craft a journey around how you want to feel.', img(s['image']))
        page('travel-styles/%s/' % s['id'], '%s — %s' % (s['title'], s['tagline']), s['description'][:155], body, 'style', og=img(s['image']), ld=breadcrumbs_ld([('Home', ''), ('Travel Styles', 'travel-styles/'), (s['title'], 'travel-styles/%s/' % s['id'])]))

def build_experiences():
    R = '../'
    cats = D['experience_categories']
    tiles = '<div class="grid g3">' + ''.join('<a class="card reveal" href="%s"><div class="card-img"><img src="%s" alt="%s" loading="lazy"/></div><div class="card-b"><h3>%s</h3><p>%s</p><div class="card-foot"><span class="price"><small>Best time</small><em style="font-size:.8rem">%s</em></span>%s</div></div></a>' % (
        u(R, 'experiences/%s/' % k), ipath(R, img(v['heroImage'])), esc(v['title']), esc(v['title']), esc(v['tagline']), esc(v['bestTime'][:44]), ic('arrow')) for k, v in cats.items()) + '</div>'
    groups = ''
    for g in D['experience_groups']:
        groups += '<div style="margin-bottom:56px">%s<div class="grid g2">' % sh(g['title'], g['subtitle'], g['description'])
        for e in g['experiences']:
            groups += '<article class="card exp-card reveal"><div class="card-img"><img src="%s" alt="%s" loading="lazy"/></div><div class="card-b"><h3>%s</h3><p style="font-weight:700;color:var(--gold-d);-webkit-line-clamp:2">%s</p><p style="-webkit-line-clamp:5">%s</p><div class="badge-row">%s</div><div class="badge-row" style="margin-top:4px">%s</div></div></article>' % (
                ipath(R, img(e['image'])), esc(e['title']), esc(e['title']), esc(e['tagline']), esc(e['overview']),
                ''.join('<span>● %s</span>' % esc(x) for x in e['bestPlaces'][:4]), ''.join('<span style="background:#fff3d4">%s</span>' % esc(x) for x in e['greatFor'][:4]))
        groups += '</div></div>'
    body = phero(R, 'Experiences', 'Intimate encounters with the wild, the coast and the culture — curated by people who know the places best.', 'gamedrives', [('Home', ''), ('Experiences', None)], 'Discover') + \
        '<section class="sec-paper"><div class="container">%s%s</div></section>' % (sh('Browse by interest', 'What would you love to do?', center=True), tiles) + '<section class="sec-light"><div class="container">%s</div></section>' % groups + cta_band(R, 'Let’s build your experience', 'Tell us what excites you and we’ll weave it into your journey.')
    page('experiences/', 'Experiences — Safaris, Beach Escapes, Wellness & Culture', 'Game drives, walking safaris, beach escapes, wellness retreats, cultural encounters and adventure — experiences curated by Pocket of Paradise.', body, 'exp', ld=breadcrumbs_ld([('Home', ''), ('Experiences', 'experiences/')]))
    for k, v in cats.items():
        R = '../../'
        acts = '<div class="grid g3">' + ''.join('<div class="act reveal"><h3>%s</h3><p>%s</p></div>' % (esc(a['name']), esc(a['description'])) for a in v['activities']) + '</div>'
        props = ''
        if v.get('properties'):
            props = '<div class="grid g4">' + ''.join('<div class="stay-c reveal"><img src="%s" alt="%s" loading="lazy"/><div><small>%s</small><h3>%s</h3><p class="muted">%s</p></div></div>' % (
                ipath(R, img(p['images'][0] if p.get('images') else '')), esc(p['name']), esc(p.get('tier', '')), esc(p['name']), esc(p.get('location', ''))) for p in v['properties']) + '</div>'
        pr = v.get('pricing') or {}
        prh = '<div class="tiers">' + ''.join('<div class="tier"><small>%s</small><b style="font-size:1.1rem">%s</b><span>%s</span></div>' % (kk.title() if kk != 'midrange' else 'Mid-range', esc(x['range']), esc(x['description'])) for kk, x in pr.items()) + '</div>' if pr else ''
        inc = '<ul class="hl">' + ''.join('<li>%s<span>%s</span></li>' % (ic('check'), esc(x)) for x in v.get('includes', [])) + '</ul>'
        ideal = '<div class="mini">' + ''.join('<span style="font-size:.85rem;padding:5px 14px">%s</span>' % esc(x) for x in v.get('idealFor', [])) + '</div>'
        sam = ''.join('<div class="act"><h3>%s</h3><p>%d days · %s</p></div>' % (esc(x['name']), x['days'], esc(', '.join(x['highlights']))) for x in v.get('sampleItineraries', []))
        samh = '<div class="grid g3">%s</div>' % sam if sam else ''
        others = '<div class="chips">' + ''.join('<a class="chip" href="%s">%s</a>' % (u(R, 'experiences/%s/' % kk), esc(vv['title'])) for kk, vv in cats.items() if kk != k) + '</div>'
        body = phero(R, v['title'], v['tagline'], img(v['heroImage']), [('Home', ''), ('Experiences', 'experiences/'), (v['title'], None)], 'Experience') + \
            '<section class="sec-paper"><div class="container"><div class="two"><div><span class="eyebrow">Overview</span><h2 style="font-size:clamp(1.8rem,3.4vw,2.6rem);margin-bottom:14px">%s</h2><p class="muted" style="font-size:1.06rem;margin-bottom:16px">%s</p>%s<div style="margin-top:18px" class="facts" ><div class="fact"><small>Best time</small><b>%s</b></div><div class="fact"><small>Recommended</small><b>%s</b></div></div></div><img src="%s" alt="%s" loading="lazy"/></div></div></section>' % (
                esc(v['tagline']), esc(v['description']), ideal, esc(v.get('bestTime', '')), esc(v.get('duration', '')), ipath(R, img(v.get('featureImage') or v['heroImage'])), esc(v['title'])) + \
            '<section class="sec-light"><div class="container">%s%s</div></section>' % (sh('Things to do', 'Popular %s activities' % v['title'].lower()), acts) + \
            ('<section class="sec-paper"><div class="container">%s%s</div></section>' % (sh('Where to stay', 'Featured properties'), props) if props else '') + \
            '<section class="sec-light"><div class="container"><div class="grid g2" style="align-items:start"><div>%s%s</div><div>%s%s</div></div>%s</div></section>' % (sh('What’s included', 'Typical inclusions'), inc, sh('Indicative pricing', 'What it can cost', 'Per person sharing, depending on season and property.'), prh, ('<div style="margin-top:40px">%s%s</div>' % (sh('Sample itineraries', 'Ideas to start from'), samh)) if samh else '') + \
            '<section class="sec-paper"><div class="container">%s%s</div></section>' % (sh('Keep exploring', 'More experiences'), others) + cta_band(R, 'Plan your %s experience' % v['title'].lower(), 'Tell us your dates and we’ll build the experience around you.', img(v['heroImage']))
        page('experiences/%s/' % k, '%s Experiences' % v['title'], v['description'][:155], body, 'exp', og=img(v['heroImage']), ld=breadcrumbs_ld([('Home', ''), ('Experiences', 'experiences/'), (v['title'], 'experiences/%s/' % k)]))

# ------------------------------------------------------------------ ABOUT / WHY / BLOG / CONTACT / FAQ / PLAN / LEGAL
def build_about():
    R = '../'
    vals = [('leaf', 'Sustainability', 'Responsible travel that protects wildlife and supports local communities.'), ('compass', 'Authenticity', 'Experiences rooted in real stories, local traditions, and genuine encounters.'), ('star', 'Excellence', 'Seamless planning, premium accommodation, and unmatched care at every step.')]
    why = [('users', 'Expert Local Guides', 'Certified guides with deep expertise in African destinations.'), ('map', 'Tailor-Made Itineraries', 'Every journey customized to match your dream experience.'), ('bed', 'Luxury & Comfort', 'Premium eco-lodges and resorts for an elegant experience.'), ('shield', '24/7 Support', 'Our team is on call throughout your trip — anytime, anywhere.')]
    body = phero(R, 'About Us', 'We bring the heart of Africa closer to you — through exceptional safaris, cultural tours, and luxury travel experiences designed for explorers who seek the extraordinary.', 'image-1', [('Home', ''), ('About Us', None)], 'Discover') + '''
<section class="sec-paper"><div class="container two"><div class="reveal"><span class="eyebrow">Our story</span><h2 style="font-size:clamp(1.9rem,3.8vw,3rem);margin-bottom:16px">Crafting unforgettable African journeys</h2>
<p class="muted" style="margin-bottom:14px">Pocket of Paradise Safaris was born from a simple idea — to share the magic of Africa with the world in a responsible and luxurious way.</p>
<p class="muted" style="margin-bottom:22px">From Kenya’s savannahs to Zanzibar’s turquoise shores, we create tailor-made itineraries that reflect your curiosity and style. Every detail is handled with personal care and local expertise.</p>
<a class="btn btn-gold" href="%s">Plan my safari %s</a></div><img class="reveal" src="%s" alt="Guests enjoying a safari" loading="lazy"/></div></section>
<section class="sec-dark"><div class="container"><div class="grid g2"><div class="feat reveal"><div class="ic">%s</div><h3>Our Mission</h3><p>To curate meaningful, sustainable, and memorable travel experiences that connect people to Africa’s wild beauty while empowering local communities and protecting our planet.</p></div>
<div class="feat reveal"><div class="ic">%s</div><h3>Our Vision</h3><p>To be Africa’s most trusted name in authentic luxury travel — inspiring discovery, promoting conservation, and redefining the art of exploration.</p></div></div></div></section>
<section class="sec-light"><div class="container">%s<div class="grid g3">%s</div></div></section>
<section class="sec-paper"><div class="container">%s<div class="grid g4">%s</div></div></section>''' % (
        u(R, 'create-tour-plan/'), ic('arrow'), ipath(R, 'pexels-photo-248797'), ic('compass'), ic('eye') if False else ic('star'),
        sh('Our core values', 'The foundation of our work', 'Built upon respect for nature, authenticity, and human connection.', True),
        ''.join('<div class="feat reveal"><div class="ic">%s</div><h3>%s</h3><p>%s</p></div>' % (ic(i), t, d) for i, t, d in vals),
        sh('Why choose us', 'We create journeys that tell stories', 'We go beyond just planning trips — we create journeys that tell stories, build connections, and last a lifetime.', True),
        ''.join('<div class="feat reveal"><div class="ic">%s</div><h3>%s</h3><p>%s</p></div>' % (ic(i), t, d) for i, t, d in why)) + \
        '<div></div>' + cta_band(R, 'Your journey to paradise begins here', 'From the wild plains of the Mara to the turquoise shores of Diani — Pocket of Paradise turns every journey into a story worth telling.', 'safari-pattern' if 'safari-pattern' in HAVE else 'u-1547970810-dc1eac37d174')
    page('about-us/', 'About Us — Boutique Travel Agency Kenya', 'Pocket of Paradise Safaris shares the magic of Africa responsibly and luxuriously — tailor-made itineraries across Kenya, Zanzibar and beyond.', body, 'about', ld=breadcrumbs_ld([('Home', ''), ('About Us', 'about-us/')]))

def build_why():
    R = '../'
    items = [('compass', 'Authentic Safari Experiences', 'Every Pocket of Paradise journey is designed to immerse you into Kenya’s natural rhythm — from majestic savannas to golden beaches.'),
             ('shield', 'Trusted & Licensed Operator', 'We are a fully licensed and accredited safari operator, trusted by travelers across the globe for safe, reliable, and ethical adventures.'),
             ('map', 'Personalized Itineraries', 'No two safaris are ever the same — we tailor every route, lodge, and experience to match your travel dreams and comfort preferences.'),
             ('users', 'Expert Local Guides', 'Our professional guides are born storytellers with deep knowledge of wildlife, culture, and Kenya’s best-kept secrets.'),
             ('leaf', 'Sustainable Tourism', 'We actively support community projects and conservation programs to ensure that tourism leaves a positive footprint.'),
             ('star', 'Award-Winning Service', 'Our commitment to excellence has earned us glowing reviews and returning guests who travel with us year after year.')]
    steps = [('Plan', 'We listen, dream, and design your adventure with precision — ensuring each journey is as unique as you are.'), ('Explore', 'Discover Kenya’s breathtaking wilderness and vibrant cultures through curated routes and world-class hospitality.'), ('Cherish', 'Take home more than photos — take home memories that whisper of Africa long after the journey ends.')]
    body = phero(R, 'Why Choose Pocket of Paradise', 'Where your dream African adventure meets warmth, expertise, and a touch of luxury. Discover why travelers around the world trust us to turn moments into memories.', 'gamedrives', [('Home', ''), ('Why Choose Us', None)], 'Why us') + \
        '<section class="sec-paper"><div class="container">%s<div class="grid g3">%s</div></div></section>' % (sh('Our promise to you', 'Authenticity, safety, and seamless adventure', 'Whether you’re chasing the Big Five or the soft whisper of the Indian Ocean breeze, we make it personal.', True), ''.join('<div class="feat reveal"><div class="ic">%s</div><h3>%s</h3><p>%s</p></div>' % (ic(i), t, d) for i, t, d in items)) + \
        '<section class="sec-dark"><div class="container">%s<div class="steps" style="grid-template-columns:repeat(3,1fr)">%s</div></div></section>' % (sh('Our journey together', 'Plan. Explore. Cherish.', center=True), ''.join('<div class="step reveal" style="background:var(--ink2);border-color:var(--line-d)"><h3 style="color:#fff">%s</h3><p style="color:#b3a695">%s</p></div>' % (t, d) for t, d in steps)) + \
        '<section class="sec-light"><div class="container"><div class="two"><div><span class="eyebrow">Our impact &amp; partnerships</span><h2 style="font-size:clamp(1.8rem,3.4vw,2.6rem);margin-bottom:14px">Travel that gives back</h2><p class="muted">At Pocket of Paradise, we believe that true travel should give back. Through our partnerships with conservation groups, community projects, and eco-conscious lodges, your journey helps sustain Kenya’s wildlife and empower local communities.</p></div><img src="%s" alt="Meeting the Maasai community" loading="lazy"/></div></div></section>' % ipath(R, 'culture-2') + cta_band(R)
    page('why-choose-us/', 'Why Choose Pocket of Paradise', 'Authentic safari experiences, personalized itineraries, expert local guides and sustainable tourism — why travelers trust Pocket of Paradise.', body, 'about')

def build_blog():
    R = '../'
    posts = sorted(D['blog'], key=lambda b: datetime.datetime.strptime(b['date'], '%B %d, %Y'), reverse=True)
    cats = sorted({b['category'] for b in posts})
    chips = '<div class="chips" id="blogChips">' + '<button class="chip on" data-f="all">All</button>' + ''.join('<button class="chip" data-f="%s">%s</button>' % (esc(c), esc(c)) for c in cats) + '</div>'
    f = posts[0]
    feat = '<article class="post-feat reveal post" data-cat="%s" data-search="%s"><a class="card-img" href="%s"><img src="%s" alt="%s" loading="lazy"/></a><div class="card-b"><span class="eyebrow">Latest article</span><div class="meta"><span>%s</span><span>%s</span><span>%s</span></div><h3><a href="%s">%s</a></h3><p>%s</p><div><a class="btn btn-dark" href="%s">Read article %s</a></div></div></article>' % (
        esc(f['category']), esc((f['title'] + f['excerpt']).lower()), u(R, 'blog/%s/' % f['id']), ipath(R, blog_image(f)), esc(f['title']), esc(f['category']), esc(f['date']), esc(f['readTime']), u(R, 'blog/%s/' % f['id']), esc(f['title']), esc(f['excerpt']), u(R, 'blog/%s/' % f['id']), ic('arrow'))
    grid = '<div class="grid g3" id="blogList">%s%s<div class="empty" id="blogEmpty" style="display:none"><h3>No articles found</h3><p class="muted">Try a different search or category.</p></div></div>' % (feat.replace('post-feat reveal post', 'post-feat reveal post').replace('<article class="post-feat', '<article style="grid-column:1/-1" class="post-feat'), ''.join(blog_card(R, b, True) for b in posts[1:]))
    body = phero(R, 'Kenya Safari Guides, Tips & Stories', 'Month-by-month Masai Mara guides, luxury lodge breakdowns, honeymoon and family itineraries — from a Kenya-based luxury safari team.', 'u-1547970810-dc1eac37d174', [('Home', ''), ('Blog', None)], 'Travel journal') + \
        '<section class="sec-light"><div class="container"><div class="toolbar">%s<div class="search">%s<label class="sr-only" for="blogSearch">Search articles</label><input id="blogSearch" type="search" placeholder="Search articles…"/></div></div>%s</div></section>' % (chips, ic('search'), grid) + cta_band(R)
    page('blog/', 'Kenya Safari Guides, Tips & Stories', 'Kenya safari guides, tips and stories — Masai Mara timing, lodge reviews, honeymoon and family itineraries.', body, 'blog', ld=breadcrumbs_ld([('Home', ''), ('Blog', 'blog/')]))
    for b in D['blog']:
        R = '../../'
        secs = b['content']['sections']
        toc = '<nav class="toc" aria-label="In this article"><b>In this article</b>' + ''.join('<a href="#s%d">%s</a>' % (i, esc(s['title'])) for i, s in enumerate(secs)) + '</nav>'
        art = '<p class="lead">%s</p>%s%s' % (esc(b['content']['intro']), toc, ''.join('<h2 id="s%d">%s</h2><p>%s</p>' % (i, esc(s['title']), esc(s['content'])) for i, s in enumerate(secs)))
        art += '<h2>Final thoughts</h2><p>%s</p>' % esc(b['content']['conclusion'])
        art += '<div class="tags">%s</div>' % ''.join('<span>#%s</span>' % esc(t) for t in b['tags'])
        art += '<div class="callout"><h3>Ready to plan your safari?</h3><p style="margin-bottom:20px">Talk to our team — we’ll turn this guide into a tailor-made itinerary.</p><a class="btn btn-gold" href="%s">Start planning %s</a></div>' % (u(R, 'create-tour-plan/'), ic('arrow'))
        share = '<div class="share" style="margin:0 0 30px"><span>Share this article</span><a href="https://wa.me/?text=%s" target="_blank" rel="noopener" aria-label="Share on WhatsApp">wa</a><a href="https://www.facebook.com/sharer/sharer.php?u=%s" target="_blank" rel="noopener" aria-label="Share on Facebook">f</a><a href="https://twitter.com/intent/tweet?url=%s" target="_blank" rel="noopener" aria-label="Share on X">X</a><button type="button" data-copy aria-label="Copy link">%s</button></div>' % (
            quote(SITE + '/blog/%s/' % b['id']), quote(SITE + '/blog/%s/' % b['id']), quote(SITE + '/blog/%s/' % b['id']), ic('share'))
        rel = [x for x in posts if x['id'] != b['id'] and (x['category'] == b['category'])][:3]
        rel = (rel + [x for x in posts if x['id'] != b['id'] and x not in rel])[:3]
        body = phero(R, b['title'], '%s · %s · %s' % (b['category'], b['date'], b['readTime']), blog_image(b), [('Home', ''), ('Blog', 'blog/'), (b['category'], None)], 'Travel journal') + \
            '<section class="sec-paper"><div class="container"><article class="article">%s%s</article></div></section>' % (share, art) + \
            '<section class="sec-light"><div class="container">%s<div class="grid g3">%s</div></div></section>' % (sh('Keep reading', 'Related articles'), ''.join(blog_card(R, x) for x in rel))
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": b['title'], "datePublished": datetime.datetime.strptime(b['date'], '%B %d, %Y').strftime('%Y-%m-%d'), "author": {"@type": "Organization", "name": b['author']}, "image": SITE + '/assets/img/%s.webp' % blog_image(b), "description": b['metaDescription']}
        page('blog/%s/' % b['id'], b['title'], b['metaDescription'], body, 'blog', og=blog_image(b), ld=[ld, breadcrumbs_ld([('Home', ''), ('Blog', 'blog/'), (b['title'], 'blog/%s/' % b['id'])])])

def build_faqs():
    R = '../'
    groups = ''.join('<div style="margin-bottom:40px"><h3 style="font-size:1.3rem;margin-bottom:16px">%s</h3>%s</div>' % (esc(g['title']), faq_html([(f['question'], f['answer']) for f in g['faqs']])) for g in D['faq'])
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in ALL_FAQ]}
    body = phero(R, 'Frequently Asked Questions', 'We’ve answered the most common questions about planning, booking, and enjoying your dream safari with us.', 'u-1516426122078-c23e763198', [('Home', ''), ('FAQs', None)], 'Help') + \
        '<section class="sec-light"><div class="container"><div class="faq-wrap"><div>%s</div><aside class="side-card"><h3>Didn’t find what you’re looking for?</h3><p>Our support team is happy to help.</p><a class="btn btn-wa btn-block" href="%s" target="_blank" rel="noopener">%s Chat on WhatsApp</a><a class="btn btn-outline btn-block" style="margin-top:10px" href="%s">Contact us</a></aside></div></div></section>' % (groups, wa('Hi Pocket of Paradise! I have a question.'), ic('wa'), u(R, 'contact/'))
    page('faqs/', 'FAQs — Kenya Safari & Luxury Travel Questions Answered', 'Answers about booking, payment, what’s included, safety, packing, insurance, customization and support.', body, '', ld=[ld, breadcrumbs_ld([('Home', ''), ('FAQs', 'faqs/')])])

def contact_fields():
    return '''<div class="r2"><div class="fld"><label for="c_name">Full name *</label><input id="c_name" name="name" type="text" autocomplete="name" data-req/><div class="err">Please enter your name.</div></div>
<div class="fld"><label for="c_email">Email *</label><input id="c_email" name="email" type="email" autocomplete="email" data-req/><div class="err">Please enter a valid email.</div></div></div>
<div class="r2"><div class="fld"><label for="c_phone">Phone / WhatsApp</label><input id="c_phone" name="phone" type="tel" autocomplete="tel" placeholder="+254 7XX XXX XXX"/></div>
<div class="fld"><label for="c_topic">I’m enquiring about</label><select id="c_topic" name="topic"><option>Planning a safari</option><option>Beach holiday</option><option>Honeymoon / couples trip</option><option>International holiday</option><option>Existing booking</option><option>Something else</option></select></div></div>
<div class="fld"><span class="lbl">How should we reply?</span><div class="opts"><label class="opt"><input type="radio" name="channel" value="WhatsApp" checked/><span>WhatsApp</span></label><label class="opt"><input type="radio" name="channel" value="Phone call"/><span>Phone call</span></label><label class="opt"><input type="radio" name="channel" value="Email"/><span>Email</span></label></div></div>
<div class="fld"><label for="c_msg">Message *</label><textarea id="c_msg" name="message" data-req placeholder="Tell us about your trip: dates, travellers, budget, interests…"></textarea><div class="err">Please write a short message.</div></div>
<label class="check fld"><input type="checkbox" data-req/> <span>I agree to Pocket of Paradise contacting me about this enquiry (see our <a style="text-decoration:underline" href="%sprivacy/index.html">Privacy Policy</a>).</span></label><div class="err" style="margin-top:-10px">Consent is required.</div>'''

def build_contact():
    R = '../'
    more = ''.join('<a href="tel:+254%s">%s</a>' % (p[1:], phone_fmt(p)) for p in PHONES[1:])
    q = 'Nord Mall Ruiru Kenya'
    body = phero(R, 'Get in Touch With Us', 'We’d love to hear from you! Whether you have questions, need a quote, or want to start your next adventure, our team is ready to assist.', 'pexels-photo-3184465', [('Home', ''), ('Contact', None)], 'Contact') + '''
<section class="sec-light"><div class="container c-wrap"><div class="reveal"><span class="eyebrow">We’re here to help</span><h2 style="font-size:clamp(1.9rem,3.6vw,2.8rem);margin-bottom:14px">Talk to a travel consultant</h2>
<p class="muted" style="margin-bottom:28px">Have a question or special request? Our travel consultants will get back to you as soon as possible. WhatsApp is the fastest way to reach us.</p>
<a class="btn btn-wa" style="margin-bottom:28px" href="%(wa)s" target="_blank" rel="noopener">%(waic)s Chat on WhatsApp</a>
<div class="ci"><span class="ic">%(pin)s</span><div><small>Visit us</small><b>Nord Mall, 1st Floor, Ruiru, Kenya</b><div class="muted" style="font-size:.88rem">Visits by appointment — message us to book a time.</div></div></div>
<div class="ci"><span class="ic">%(phone)s</span><div><small>Call or WhatsApp</small><b><a href="tel:+254115167384">%(p0)s</a></b>
<details class="more-lines"><summary style="color:var(--gold-d)">More ways to call</summary><div>%(more)s</div></details></div></div>
<div class="ci"><span class="ic">%(mail)s</span><div><small>Email</small><b><a href="mailto:%(email)s">%(email)s</a></b></div></div>
<div class="map"><iframe title="Map showing Nord Mall, Ruiru" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=%(q)s&amp;output=embed"></iframe>
<div class="m-foot"><span>%(pin)s Nord Mall, 1st Floor, Ruiru</span><a class="btn btn-dark btn-sm" href="https://www.google.com/maps/dir/?api=1&amp;destination=%(q)s" target="_blank" rel="noopener">Get directions</a></div></div></div>
<div class="form-card reveal"><h3 style="font-size:1.5rem;margin-bottom:6px">Send us an enquiry</h3><p class="muted" style="margin-bottom:22px">A few details help us reply with the right answer first time.</p>
<form id="contactForm" novalidate>%(fields)s<button class="btn btn-gold btn-block" type="submit">Continue %(arrow)s</button>
<div id="cSend" hidden style="margin-top:6px"><p style="font-weight:700;margin-bottom:12px">Choose how to send your enquiry:</p><a id="cWa" class="btn btn-wa btn-block" target="_blank" rel="noopener" href="#">%(waic)s Send via WhatsApp</a><a id="cMail" class="btn btn-line btn-block" style="margin-top:10px" href="#">%(mail)s Send via email</a></div></form></div></div></section>''' % dict(
        wa=wa('Hi Pocket of Paradise! I’d like to speak to a travel consultant.'), waic=ic('wa'), pin=ic('pin'), phone=ic('phone'), mail=ic('mail'), p0=phone_fmt(PHONES[0]), more=more, email=EMAIL,
        q=q.replace(' ', '+'), fields=contact_fields() % R, arrow=ic('arrow'))
    body += cta_band(R)
    ld = {"@context": "https://schema.org", "@type": "ContactPage", "name": "Contact Pocket of Paradise"}
    page('contact/', 'Contact Us — Plan Your Safari', 'Contact Pocket of Paradise — chat on WhatsApp, call or visit our office at Nord Mall, Ruiru.', body, 'contact', ld=ld)

def build_plan():
    R = '../'
    pkopts = '<option value="">Not sure yet — design something for me</option>' + ''.join('<optgroup label="%s">%s</optgroup>' % (CATNAME[c], ''.join('<option value="%s">%s — from %s</option>' % (p['id'], esc(p['title']), kes(p['from'])) for p in PK if p['cat'] == c)) for c in CATNAME)
    interest = ''.join('<label class="opt"><input type="checkbox" name="interest" value="%s"/><span>%s</span></label>' % (x, x) for x in ['Masai Mara', 'Amboseli', 'Samburu', 'Laikipia', 'Diani / Coast', 'Zanzibar', 'Maldives', 'Bali', 'Thailand', 'Dubai', 'Cape Town', 'Other'])
    comfort = ''.join('<label class="opt"><input type="radio" name="comfort" value="%s"/><span>%s</span></label>' % (x, x) for x in ['Budget', 'Mid-range', 'Luxury', 'Not sure yet'])
    style = '<option value="">Select…</option>' + ''.join('<option>%s</option>' % x for x in ['Couple / honeymoon', 'Family with children', 'Group of friends', 'Solo traveller', 'Multi-generational family', 'Corporate / group'])
    budget = '<option value="">Select…</option>' + ''.join('<option>%s</option>' % x for x in ['Under KES 100,000', 'KES 100,000 – 200,000', 'KES 200,000 – 350,000', 'KES 350,000 – 500,000', 'KES 500,000+', 'Not sure — advise me'])
    length = '<option value="">Select…</option>' + ''.join('<option>%s</option>' % x for x in ['Weekend (2–3 days)', '4–5 days', '6–7 days', '8–10 days', '10+ days'])
    body = phero(R, 'Custom Tour Plan', 'Let us craft your perfect escape — from Kenya’s savannah sunsets to tropical beaches. Answer a few quick questions and our travel experts will design a journey that’s truly yours.', 'couples-5', [('Home', ''), ('Custom Tour Plan', None)], 'Plan your trip') + '''
<section class="sec-light"><div class="container" style="max-width:860px"><div class="form-card"><div class="prog" id="prog"><span class="on"></span><span></span><span></span><span></span></div>
<form id="plan" novalidate onsubmit="return false">
<div class="fs on"><div class="step-t"><h3>Your trip</h3><small id="stepNo">STEP 1 OF 4</small></div>
<div class="fld"><label for="p_pk">Package</label><select id="p_pk" name="package">%(pk)s</select></div>
<div class="fld"><span class="lbl">Places you’re interested in</span><div class="opts">%(interest)s</div></div>
<div class="fld"><span class="lbl">Comfort level</span><div class="opts">%(comfort)s</div></div>
<div class="r2"><div class="fld"><label for="p_month">Travel month</label><select id="p_month" name="month" data-months></select></div><div class="fld"><label for="p_len">Trip length</label><select id="p_len" name="length">%(len)s</select></div></div>
<label class="check fld"><input type="checkbox" name="flex"/> <span>My dates are flexible</span></label>
<div class="f-nav"><span></span><button class="btn btn-dark" type="button" data-next>Next: travellers %(arrow)s</button></div></div>

<div class="fs"><div class="step-t"><h3>Who’s travelling</h3></div>
<div class="r3"><div class="fld"><label for="p_ad">Adults</label><input id="p_ad" name="adults" type="number" min="1" max="30" value="2"/></div><div class="fld"><label for="p_ch">Children (under 12)</label><input id="p_ch" name="children" type="number" min="0" max="20" value="0"/></div>
<div class="fld"><label for="p_st">Travelling as</label><select id="p_st" name="style">%(style)s</select></div></div>
<div class="fld"><label for="p_bud">Budget per person</label><select id="p_bud" name="budget">%(budget)s</select></div>
<div class="fld"><label for="notes">Special requests</label><textarea id="notes" name="notes" maxlength="300" placeholder="Honeymoon, dietary needs, accessibility, celebrations…"></textarea><div class="cnt" id="ncnt">0/300 characters</div></div>
<div class="f-nav"><button class="btn btn-line" type="button" data-prev>Back</button><button class="btn btn-dark" type="button" data-next>Next: your details %(arrow)s</button></div></div>

<div class="fs"><div class="step-t"><h3>Your details</h3></div>
<div class="r2"><div class="fld"><label for="p_n">Full name *</label><input id="p_n" name="name" type="text" autocomplete="name" data-req/><div class="err">Please enter your name.</div></div><div class="fld"><label for="p_e">Email *</label><input id="p_e" name="email" type="email" autocomplete="email" data-req/><div class="err">Please enter a valid email.</div></div></div>
<div class="fld"><label for="p_p">Phone / WhatsApp *</label><input id="p_p" name="phone" type="tel" autocomplete="tel" placeholder="+254 7XX XXX XXX" data-req/><div class="err">Please enter a valid phone number.</div></div>
<div class="fld"><span class="lbl">How should we reach you?</span><div class="opts"><label class="opt"><input type="radio" name="channel" value="WhatsApp" checked/><span>WhatsApp</span></label><label class="opt"><input type="radio" name="channel" value="Phone call"/><span>Phone call</span></label><label class="opt"><input type="radio" name="channel" value="Email"/><span>Email</span></label></div></div>
<div class="fld"><label for="p_bt">Best time to reach you</label><select id="p_bt" name="besttime"><option value="">Anytime</option><option>Morning</option><option>Afternoon</option><option>Evening</option></select></div>
<label class="check fld"><input type="checkbox" data-req/> <span>I agree to Pocket of Paradise contacting me about this enquiry. See our <a style="text-decoration:underline" href="%(pv)s">Privacy Policy</a>.</span></label><div class="err" style="margin-top:-10px">Consent is required.</div>
<div class="f-nav"><button class="btn btn-line" type="button" data-prev>Back</button><button class="btn btn-gold" type="button" data-next>Review &amp; send %(arrow)s</button></div></div>

<div class="fs"><div class="step-t"><h3>Review &amp; send</h3></div><div class="summary"><dl id="sum"></dl></div>
<p class="muted" style="margin-bottom:16px">Choose how to send your enquiry. We’ll reply on your preferred channel. Submitting an enquiry doesn’t commit you to anything.</p>
<a id="sendWa" class="btn btn-wa btn-block" target="_blank" rel="noopener" href="#">%(wa)s Send via WhatsApp</a>
<a id="sendMail" class="btn btn-line btn-block" style="margin-top:10px" href="#">%(mail)s Send via email</a>
<button id="copyMsg" class="btn btn-line btn-block" style="margin-top:10px" type="button">Copy my enquiry</button>
<div class="f-nav"><button class="btn btn-line" type="button" data-prev>Back</button><span></span></div></div>
</form></div></div></section>''' % dict(pk=pkopts, interest=interest, comfort=comfort, len=length, style=style, budget=budget, arrow=ic('arrow'), pv=u(R, 'privacy/'), wa=ic('wa'), mail=ic('mail'))
    page('create-tour-plan/', 'Custom Tour Plan — Design Your Journey', 'Tell us your dates, travellers, budget and interests — our experts will design a tailor-made Kenya safari, beach escape or international holiday.', body, '', ld=breadcrumbs_ld([('Home', ''), ('Custom Tour Plan', 'create-tour-plan/')]))

def build_legal():
    for key, path, title in (('terms', 'terms/', 'Terms & Conditions'), ('privacy', 'privacy/', 'Privacy Policy')):
        R = '../'
        out, ul = '', False
        for t, x in D[key]:
            if t == 'h1' or (t == 'p' and x == 'LEGAL'):
                continue
            if t != 'li' and ul:
                out += '</ul>'; ul = False
            if t == 'li':
                if not ul:
                    out += '<ul>'; ul = True
                out += '<li>%s</li>' % esc(x)
            elif t == 'h2':
                out += '<h2>%s</h2>' % esc(x)
            elif t == 'h3':
                out += '<h3>%s</h3>' % esc(x)
            else:
                out += '<p>%s</p>' % esc(re.sub(r'(Last updated:).*', r'\1 November 2026', x) if x.startswith('Last updated') else x)
        if ul:
            out += '</ul>'
        body = phero(R, title, '', 'u-1547970810-dc1eac37d174', [('Home', ''), (title, None)], 'Legal') + '<section class="sec-paper"><div class="container"><div class="legal prose">%s</div></div></section>' % out
        page(path, title, '%s for Pocket of Paradise.' % title, body, '')

def build_404():
    body = '<section class="sec-light nf"><div class="container"><h1>404</h1><h2 style="margin:6px 0 14px">This trail has gone cold</h2><p class="muted" style="margin-bottom:26px">The page you’re looking for doesn’t exist or has moved.</p><a class="btn btn-gold" href="index.html">Back to home</a> <a class="btn btn-line" href="packages/index.html">Browse packages</a></div></section>'
    # 404 served from site root on GitHub Pages / nginx: use root-relative assets
    page('404/', 'Page not found', 'The page you are looking for could not be found.', body.replace('href="index.html"', 'href="../index.html"').replace('href="packages/index.html"', 'href="../packages/index.html"'), '')
    shutil.move(os.path.join(ROOT, '404/index.html'), os.path.join(ROOT, '404.html'))
    os.rmdir(os.path.join(ROOT, '404'))
    # fix relative paths for root-level file
    p = os.path.join(ROOT, '404.html')
    s = open(p, encoding='utf-8').read().replace('"../assets/', '"assets/').replace('"../index.html', '"index.html').replace('"../', '"')
    s = s.replace('data-root="../"', 'data-root=""')
    open(p, 'w', encoding='utf-8').write(s)

def build_sitemap():
    urls = []
    for dp, dn, fn in os.walk(ROOT):
        if '/tools' in dp or '/assets' in dp:
            continue
        if 'index.html' in fn:
            rel = os.path.relpath(dp, ROOT)
            urls.append('' if rel == '.' else rel + '/')
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('<url><loc>%s/%s</loc></url>\n' % (SITE, x) for x in sorted(urls)) + '</urlset>\n')
    open(os.path.join(ROOT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n' % SITE)

if __name__ == '__main__':
    build_home(); build_packages(); build_destinations(); build_styles(); build_experiences(); build_about(); build_why()
    build_blog(); build_faqs(); build_contact(); build_plan(); build_legal(); build_404(); build_sitemap()
    n = sum(1 for dp, dn, fn in os.walk(ROOT) for f in fn if f.endswith('.html') and '/tools' not in dp)
    print('built', n, 'pages')
