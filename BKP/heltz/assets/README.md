# /assets/images

This site currently hotlinks its photography directly from the
original heltzdrivingschool.com WordPress media library (see the
`media` / `image` / `src` URLs in `js/data.js`), since this project
was generated without direct file-system access to download them.

To make the site fully self-hosted:

1. Download the images referenced in `js/data.js` (hero slides,
   course images, fleet images, gallery items) and the logo/favicon
   used in `dev/build.py`.
2. Save them here, e.g. `assets/images/hero-1.jpg`.
3. Update the corresponding URLs in `js/data.js` to the local path,
   e.g. `assets/images/hero-1.jpg` instead of the full
   `https://heltzdrivingschool.com/...` URL.

Everything else about the site (rendering, lazy loading, responsive
sizing) already works with local paths — only the URLs need to change.
