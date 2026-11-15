# Pocket of Paradise — website revamp (UI only)

Plain HTML + CSS + JavaScript. No framework, no build step needed to *view* it: open `index.html`.

- `assets/css/style.css`, `assets/js/main.js` — shared styles and behaviour
- `assets/img/` — every image from the original site (WebP, ≤1600px)
- `tools/build.py` + `tools/data/site.json` — optional generator used to produce the 66 pages from the
  cloned content. Edit the data/script and run `python3 tools/build.py` to regenerate.

## To do before launch
- Real social links (`data-social` placeholders in the top bar and footer)
- Confirm what each phone line is for (all six are listed; the main WhatsApp line is 0115167384)
- Move email to the main domain (infrastructure) — currently info@pocketofparadise.com as on the old site
- Forms hand off to WhatsApp/email (no backend); connect a CRM/WhatsApp API in the Smart Engine phase
