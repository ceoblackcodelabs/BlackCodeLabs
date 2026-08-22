# Heltz Driving Academy — Website

A modern, fast, fully static revamp of heltzdrivingschool.com. Built
with plain HTML5, CSS3 and vanilla JavaScript — no framework, no
build step, no Node required. Deploy by uploading these files
straight to GitHub Pages.

## Deploying to GitHub Pages

1. Push the contents of this folder (everything **except** `/dev`,
   which is optional tooling — see below) to a GitHub repository.
2. In the repo, go to **Settings → Pages**.
3. Set the source to the branch/folder containing these files
   (e.g. `main` / `/root`).
4. Save. GitHub will publish the site at
   `https://<your-username>.github.io/<repo-name>/`.

No `npm install`, no build command, no server — it's ready as-is.

## Project structure

```
/index.html            Home page
/courses.html          All driving courses (Class A–D, VIP)
/branches.html         All 13 Nairobi branches
/prices.html           Help Center → Prices
/payment-options.html  Help Center → Payment Options (M-Pesa / Bank)
/register.html         Help Center → Registration form
/faq.html              Help Center → FAQ (searchable accordion)
/about.html             About Heltz
/gallery.html           Full photo gallery (filter + lightbox)
/contact.html           Contact page + form
/404.html               Custom not-found page

/css/style.css          Design tokens, base styles, every component
/css/responsive.css     Breakpoints (1180 / 980 / 720 / 460px)

/js/data.js             ALL site content lives here — single source
                         of truth for hero slides, courses, prices,
                         branches, FAQs, gallery, fleet, stats, etc.
/js/icons.js             Shared inline SVG icon set
/js/navigation.js        Header scroll state, dropdown + mobile drawer
/js/carousel.js           Hero carousel (mixed image/video slides)
/js/fleet.js              Infinite auto-scrolling vehicle showcase
/js/counters.js           Animated stat counters
/js/gallery.js            Gallery grid, filtering, lightbox
/js/forms.js               Form validation → WhatsApp handoff
/js/main.js                 Renders everything else from data.js

/assets/images, /videos, /icons   Currently empty — see below.

/robots.txt, /sitemap.xml   SEO basics, already wired to all pages.

/dev/   Optional — the Python scripts used to assemble the HTML
        pages from shared header/footer partials. Not needed to run
        the site; only useful if you want to regenerate the pages
        after changing the shared header/footer/nav structure.
```

## Editing content

Almost everything you'll want to change lives in **`js/data.js`**:
business contact info, hero carousel slides, courses and prices,
branches, FAQs, gallery photos, the vehicle fleet, and homepage
stats. Change the data there and the whole site updates — nothing
is hardcoded into the HTML for these sections.

To add a **video** hero slide, just add an entry with
`type: "video"` and a `media` URL ending in `.mp4` — the carousel
renders it as `<video>` automatically, no HTML changes needed.

## About the images

This build was generated without local file-system access to the
original site's media library, so the hero, course, fleet and
gallery images currently **hotlink directly** to
`heltzdrivingschool.com`'s existing WordPress uploads. The site
works as-is, but for full independence from the old site (and to
avoid depending on it staying online), download those images into
`/assets/images` and update the URLs in `js/data.js` — see
`/assets/README.md` for the short version of that process.

The color palette (asphalt ink, hazard-sign amber, Kenyan-forest
green) and typefaces were chosen to fit a driving school rather than
lifted from the old site's WordPress theme, since the actual logo
file couldn't be downloaded in this environment either. Swap the
`<span class="brand-mark">H</span>` text-logo treatment for an
`<img>` of the real logo if you'd like to use the original artwork —
it appears once in the header and once in the footer of each page
(search for `brand-mark` in the HTML, or regenerate via `/dev` after
editing `header()`/`footer()` in `dev/build.py`).

## Forms

There's no backend yet. Submitting the Registration or Contact form
validates the fields client-side, then opens WhatsApp with the
message pre-filled so it reaches the school's number directly. Swap
the `open(waHref)` call in `js/forms.js` for a real `fetch()` POST
once there's an API to send to.

## Browser support

Modern evergreen browsers (Chrome, Safari, Firefox, Edge). Uses
`IntersectionObserver` (scroll reveals, stat counters — both degrade
gracefully without it) and CSS custom properties throughout.
