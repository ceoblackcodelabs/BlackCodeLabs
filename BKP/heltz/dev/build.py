#!/usr/bin/env python3
"""
build.py — assembles the static HTML pages for the Heltz Driving
Academy site from shared partials (topbar/header/drawer/footer) plus
per-page content blocks defined in pages/*.py.

This script is a DEV-TIME convenience only. It runs once (right now,
by me) to produce plain .html files. The output requires no build
step, no Node, and no server — it's ready to upload straight to
GitHub Pages.
"""
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

NAV_ITEMS = [
    ("Home", "index.html"),
    ("Courses", "courses.html"),
    ("Branches", "branches.html"),
]
HELP_CENTER = [
    ("Prices", "prices.html"),
    ("Payment Options", "payment-options.html"),
    ("Registration", "register.html"),
    ("FAQ", "faq.html"),
]
NAV_TAIL = [
    ("About Heltz", "about.html"),
    ("Gallery", "gallery.html"),
    ("Contact", "contact.html"),
]

ICON_SVGS = {
    "phone": '<svg class="icon-16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.362 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.338 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "mail": '<svg class="icon-16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 6c0-1.1-.9-2-2-2H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6Z"/><path d="m2 7 10 6 10-6"/></svg>',
    "pin": '<svg class="icon-16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
    "clock": '<svg class="icon-16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
    "whatsapp": '<svg viewBox="0 0 24 24" fill="currentColor" width="26" height="26"><path d="M17.5 14.4c-.3-.1-1.7-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.3-1.5-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6.1-.1.3-.3.4-.5.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5C10.1 9 9.5 7.6 9.2 7c-.1-.5-.3-.4-.5-.4h-.5c-.2 0-.5.1-.7.3-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.1 5 4.3.7.3 1.2.5 1.7.6.7.2 1.3.2 1.8.1.5-.1 1.7-.7 1.9-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.3ZM12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2Z"/></svg>',
    "facebook": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.4h-1.2c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.4v7A10 10 0 0 0 22 12Z"/></svg>',
    "twitter": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.9 3H21l-6.5 7.4L22.2 21h-6.9l-5.4-6.7L3.6 21H1.4l7-8-7.7-10h7l4.9 6.2L18.9 3Zm-1.2 16h1.9L7.4 5H5.4l12.3 14Z"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>',
    "tiktok": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M16.7 2h-3.3v14.2a2.6 2.6 0 1 1-2.6-2.6c.2 0 .5 0 .7.1V10.4a6 6 0 1 0 5.2 6V8.6c1.2.9 2.6 1.4 4.1 1.4V6.7A5 5 0 0 1 16.7 2Z"/></svg>',
    "chevronDown": '<svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>',
    "close": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18M6 6l12 12"/></svg>',
    "menu_line": '<span></span><span></span><span></span>',
}


def social_icons(css_class="topbar-social", extra_attrs=""):
    links = [
        ("facebook", ICON_SVGS["facebook"]),
        ("twitter", ICON_SVGS["twitter"]),
        ("instagram", ICON_SVGS["instagram"]),
        ("tiktok", ICON_SVGS["tiktok"]),
    ]
    items = "\n".join(
        f'<a href="#" data-field="{name}" target="_blank" rel="noopener" aria-label="Heltz on {name.title()}">{svg}</a>'
        for name, svg in links
    )
    return f'<div class="{css_class}" {extra_attrs}>{items}</div>'


def dropdown_menu():
    items = "\n".join(f'<a href="{href}">{label}</a>' for label, href in HELP_CENTER)
    items += '\n<a href="#" data-field="brochure" target="_blank" rel="noopener">Download Brochure</a>'
    return items


def topbar():
    return f"""
  <div class="topbar">
    <div class="container">
      <div class="topbar-info">
        <span>{ICON_SVGS['pin']}<span data-field="address">1st Floor, City Square Sheikh House, Tom Mboya Street, Nairobi</span></span>
        <a href="#" data-field="email-href">{ICON_SVGS['mail']}<span data-field="email">heltzdrivingschool@gmail.com</span></a>
        <a href="#" data-field="phone-href">{ICON_SVGS['phone']}<span data-field="phone">+254 743 552541</span></a>
      </div>
      {social_icons()}
    </div>
  </div>"""


def header(active):
    def nav_link(label, href):
        cls = "nav-link" + (" active" if href == active else "")
        return f'<a class="{cls}" href="{href}">{label}</a>'

    main_items = "\n".join(f"<li>{nav_link(l, h)}</li>" for l, h in NAV_ITEMS)
    tail_items = "\n".join(f"<li>{nav_link(l, h)}</li>" for l, h in NAV_TAIL)
    help_active = active in [h for _, h in HELP_CENTER]

    return f"""
  <header class="site-header">
    <div class="container header-inner">
      <a href="index.html" class="brand" aria-label="Heltz Driving Academy — home">
        <span class="brand-mark">H</span>
        <span class="brand-text">
          <span class="name">Heltz</span>
          <span class="tag">Driving Academy</span>
        </span>
      </a>

      <nav class="main-nav" aria-label="Primary">
        <ul>
          {main_items}
          <li class="nav-item-dropdown{' open' if help_active else ''}">
            <button class="nav-link" aria-haspopup="true">Help Center {ICON_SVGS['chevronDown']}</button>
            <div class="dropdown-menu">
              {dropdown_menu()}
            </div>
          </li>
          {tail_items}
        </ul>
      </nav>

      <div class="header-cta">
        <a class="btn btn-outline" href="#" data-field="whatsapp-href" target="_blank" rel="noopener">Call Us</a>
        <a class="btn btn-amber" href="register.html">Enroll Now</a>
        <button class="hamburger" aria-label="Open menu" aria-expanded="false">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>

  <div class="mobile-drawer">
    <div class="drawer-backdrop"></div>
    <div class="drawer-panel">
      <div class="drawer-top">
        <a href="index.html" class="brand">
          <span class="brand-mark">H</span>
          <span class="brand-text"><span class="name">Heltz</span></span>
        </a>
        <button class="drawer-close" aria-label="Close menu">{ICON_SVGS['close']}</button>
      </div>
      <nav class="drawer-nav" aria-label="Mobile">
        <a href="index.html">Home</a>
        <a href="courses.html">Courses</a>
        <a href="branches.html">Branches</a>
        <button class="drawer-accordion" aria-expanded="false" aria-controls="drawer-help-submenu">
          Help Center {ICON_SVGS['chevronDown']}
        </button>
        <div class="drawer-submenu" id="drawer-help-submenu">
          {"".join(f'<a href="{h}">{l}</a>' for l, h in HELP_CENTER)}
        </div>
        <a href="about.html">About Heltz</a>
        <a href="gallery.html">Gallery</a>
        <a href="contact.html">Contact</a>
      </nav>
      <div class="drawer-foot">
        <a class="btn btn-amber btn-block" href="register.html">Enroll Now</a>
        <a class="btn btn-outline btn-block" href="#" data-field="whatsapp-href" target="_blank" rel="noopener" style="margin-bottom:1.2rem;">Chat On WhatsApp</a>
        {social_icons("drawer-social")}
      </div>
    </div>
  </div>"""


def footer():
    course_links = "".join(
        f'<li><a href="courses.html">Class {c} ({n})</a></li>'
        for c, n in [("A", "Motorbikes"), ("B", "Cars"), ("C", "Trucks"), ("D", "Vans")]
    )
    help_links = "".join(f'<li><a href="{h}">{l}</a></li>' for l, h in HELP_CENTER)
    quick_links = "".join(
        f'<li><a href="{h}">{l}</a></li>'
        for l, h in [("Home", "index.html"), ("Courses", "courses.html"), ("Branches", "branches.html"), ("About Us", "about.html"), ("Gallery", "gallery.html"), ("Contact", "contact.html")]
    )

    return f"""
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col footer-brand">
          <a href="index.html" class="brand">
            <span class="brand-mark">H</span>
            <span class="brand-text"><span class="name">Heltz</span><span class="tag">Driving Academy</span></span>
          </a>
          <p class="footer-about">Heltz Driving Academy has earned a reputation for responsible and competent driving instruction within Nairobi.</p>
          {social_icons("footer-social")}
        </div>
        <div class="footer-col">
          <h4>Courses</h4>
          <ul>{course_links}</ul>
        </div>
        <div class="footer-col">
          <h4>Help Center</h4>
          <ul>{help_links}</ul>
        </div>
        <div class="footer-col">
          <h4>Contact</h4>
          <address>
            <span data-field="address">1st Floor, City Square Sheikh House, Tom Mboya Street, Nairobi, Kenya</span><br>
            <span data-field="pobox">P.O. Box 71300-006622, Nairobi</span><br>
            <a href="#" data-field="phone-href" style="display:block;margin-top:.5rem;" data-field-text><span data-field="phone">+254 743 552541</span></a>
            <a href="#" data-field="email-href"><span data-field="email">heltzdrivingschool@gmail.com</span></a>
          </address>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; <span data-field="year">2026</span> Heltz Driving Academy. All rights reserved.</span>
        <span>Powered by <a href="#">Black Code Labs</a></span>
      </div>
    </div>
  </footer>

  <a class="wa-float" href="#" data-field="whatsapp-href" target="_blank" rel="noopener" aria-label="Chat with Heltz on WhatsApp">
    {ICON_SVGS['whatsapp']}
  </a>"""


def page(
    slug,
    title,
    description,
    body,
    active,
    extra_head="",
    body_class="",
):
    canonical = f"https://heltzdrivingschool.com/{slug}" if slug != "index.html" else "https://heltzdrivingschool.com/"
    og_image = "https://heltzdrivingschool.com/wp-content/uploads/2021/02/HeltznEW-lOGO@2x.png"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow">

<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{og_image}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{og_image}">

<link rel="icon" type="image/png" href="https://heltzdrivingschool.com/wp-content/uploads/2021/02/HeltzFavicon@2x.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;700;800&family=Work+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">

<link rel="stylesheet" href="css/style.css">
<link rel="stylesheet" href="css/responsive.css">
{extra_head}
</head>
<body class="{body_class}">
<a class="skip-link" href="#main">Skip to content</a>
{topbar()}
{header(active)}
<main id="main">
{body}
</main>
{footer()}

<script src="js/data.js"></script>
<script src="js/icons.js"></script>
<script src="js/navigation.js"></script>
<script src="js/carousel.js"></script>
<script src="js/fleet.js"></script>
<script src="js/counters.js"></script>
<script src="js/gallery.js"></script>
<script src="js/forms.js"></script>
<script src="js/main.js"></script>
</body>
</html>"""


def write(slug, html):
    path = os.path.join(OUT_DIR, slug)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path, len(html), "bytes")
