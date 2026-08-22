#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import build
from pages_home import INDEX_BODY
from pages_secondary import COURSES_BODY, BRANCHES_BODY, ABOUT_BODY
from pages_gallery_contact import GALLERY_BODY, CONTACT_BODY
from pages_help1 import PRICES_BODY, PAYMENT_OPTIONS_BODY, REGISTER_BODY
from pages_faq_404 import FAQ_BODY, NOT_FOUND_BODY

SITE = "https://heltzdrivingschool.com"

PAGES = [
    dict(
        slug="index.html", active="index.html",
        title="Heltz Driving Academy | Driving School In Nairobi, Kenya",
        description="Heltz Driving Academy has taught Nairobi to drive for over 35 years. NTSA-curriculum lessons for cars, motorbikes, trucks and vans across 13 branches.",
        body=INDEX_BODY,
    ),
    dict(
        slug="courses.html", active="courses.html",
        title="Driving Courses — Class A, B, C & D | Heltz Driving Academy",
        description="Practical and theoretical driving courses at Heltz: Class A motorbikes, Class B cars, Class C trucks and Class D vans/PSV, per the NTSA curriculum.",
        body=COURSES_BODY,
    ),
    dict(
        slug="branches.html", active="branches.html",
        title="Branches Across Nairobi | Heltz Driving Academy",
        description="Find your nearest Heltz Driving Academy branch — 13 locations across Nairobi including Tom Mboya, Westlands, Donholm, Umoja and more.",
        body=BRANCHES_BODY,
    ),
    dict(
        slug="prices.html", active="prices.html",
        title="Course Prices | Heltz Driving Academy",
        description="Heltz Driving Academy pricing for Class A, B, C and D courses, refresher lessons, and NTSA fees payable separately.",
        body=PRICES_BODY,
    ),
    dict(
        slug="payment-options.html", active="payment-options.html",
        title="Payment Options — M-Pesa & Bank | Heltz Driving Academy",
        description="Pay your Heltz Driving Academy course fees via M-Pesa Buy Goods or bank deposit to our Equity Bank account. No cash accepted.",
        body=PAYMENT_OPTIONS_BODY,
    ),
    dict(
        slug="register.html", active="register.html",
        title="Registration — Enroll Now | Heltz Driving Academy",
        description="Register for a driving course at Heltz Driving Academy. Choose your class, branch and preferred start date.",
        body=REGISTER_BODY,
    ),
    dict(
        slug="faq.html", active="faq.html",
        title="Frequently Asked Questions | Heltz Driving Academy",
        description="Answers to common questions about Heltz Driving Academy: licence age, curriculum, payments, and how to get in touch.",
        body=FAQ_BODY,
    ),
    dict(
        slug="about.html", active="about.html",
        title="About Heltz Driving Academy | 35+ Years In Nairobi",
        description="For over 35 years, Heltz Driving Academy has taught responsible, competent driving across Nairobi. Learn about our story and instructors.",
        body=ABOUT_BODY,
    ),
    dict(
        slug="gallery.html", active="gallery.html",
        title="Gallery | Heltz Driving Academy",
        description="Photos from Heltz Driving Academy — lessons, vehicles and branches from across Nairobi.",
        body=GALLERY_BODY,
    ),
    dict(
        slug="contact.html", active="contact.html",
        title="Contact Us | Heltz Driving Academy",
        description="Get in touch with Heltz Driving Academy — call, WhatsApp, email or visit one of our 13 Nairobi branches.",
        body=CONTACT_BODY,
    ),
]

for p in PAGES:
    html = build.page(
        slug=p["slug"],
        title=p["title"],
        description=p["description"],
        body=p["body"],
        active=p["active"],
    )
    build.write(p["slug"], html)

# 404 page (no header active state, keep header for nav)
html_404 = build.page(
    slug="404.html", active="",
    title="Page Not Found | Heltz Driving Academy",
    description="The page you're looking for could not be found.",
    body=NOT_FOUND_BODY,
)
build.write("404.html", html_404)

# robots.txt
robots = f"""User-agent: *
Allow: /

Sitemap: {SITE}/sitemap.xml
"""
with open(os.path.join(build.OUT_DIR, "robots.txt"), "w") as f:
    f.write(robots)
print("wrote robots.txt")

# sitemap.xml
urls = [p["slug"] for p in PAGES]
url_entries = "\n".join(
    f"""  <url>
    <loc>{SITE}/{'' if u == 'index.html' else u}</loc>
    <changefreq>weekly</changefreq>
    <priority>{'1.0' if u == 'index.html' else '0.7'}</priority>
  </url>"""
    for u in urls
)
sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{url_entries}
</urlset>
"""
with open(os.path.join(build.OUT_DIR, "sitemap.xml"), "w") as f:
    f.write(sitemap)
print("wrote sitemap.xml")

print("\nDone — generated", len(PAGES) + 1, "HTML pages.")
