from datetime import date, timedelta
from decimal import Decimal

from Studio.pdf import engine as E
from Studio.schema import (DocType, date_, lines, money, number, rows, section, select, text, textarea)


def _today():
    return date.today()


SAMPLE = {
    "client_name": "Click & Go Builders Solutions",
    "client_contact": "The Management Team",
    "client_location": "Nairobi, Kenya",
    "website": "clickandgobuilders.com",
    "title": "Proposal for Website Management & Maintenance",
    "salutation": "Dear Management Team,",
    "intro": [
        "Thank you for the opportunity to put this proposal forward. We went through clickandgobuilders.com page by page, covering the home page, About, Projects, Designs, Construction Rates, Blog and Contact pages, and we looked at it the way a first-time client would: can I trust this company, can I see its work, and how easily can I get in touch?",
        "The website has a solid foundation. It presents a wide range of services clearly, and it already carries the things that win building clients: real project photos from across the country, client testimonials and useful guides. What holds it back is in the details, and the details are fixable. Two different phone numbers, a rates page that is a screenshot, gallery photos with no project information, and no new content since launch each sit between a visitor and an enquiry.",
        "This proposal sets out what we found, the updates we recommend over the first three months, and a single flat monthly fee under which Black Code Labs would manage, secure and steadily improve the site.",
    ],
    "stats": [
        {"value": "18", "label": "service lines presented"},
        {"value": "13", "label": "client testimonials"},
        {"value": "40+", "label": "project photos and videos"},
        {"value": "10", "label": "published building guides"},
    ],
    "fee_amount": "20000", "term_months": "3",
    "fee_note": "No setup fee and no per-task charges inside the plan.",
    "glance": [
        {"label": "Initial term", "text": "Three months, then month to month on 30 days’ notice."},
        {"label": "Covers", "text": "Updates, security, daily backups, uptime monitoring, 10 hours of changes each month, one SEO article each month and a monthly report."},
        {"label": "Improvement programme", "text": "The three-month roadmap in Section 2 is delivered inside the same fee."},
        {"label": "Start", "text": "Within three working days of approval."},
    ],
    "review_intro": "We reviewed the live site as a visitor would. This section lists what is working and what we would change, in order of how much each item affects enquiries.",
    "working": [
        {"title": "Clear service structure", "text": "Architectural drawings, interior works and exterior works are laid out simply in the menu and on the home page."},
        {"title": "Strong social proof", "text": "Thirteen client testimonials from across Kenya and the diaspora."},
        {"title": "A real portfolio", "text": "More than 40 project photos and videos covering ongoing and completed work in over 25 locations."},
        {"title": "Useful content", "text": "Ten long-form guides on building in Kenya, a good base for search traffic."},
        {"title": "Enquiry tools", "text": "A request form with file upload for drawings and references, and clear “Request a Service” buttons."},
        {"title": "Search basics in place", "text": "Page titles, descriptions and Search Console verification are set up, and page caching is active."},
    ],
    "findings": [
        {"area": "Contact details", "saw": "Two different phone numbers appear: +254 786 255 866 in the header and +254 717 737 373 in the footer, on the contact page and behind the Request a Service button.", "recommend": "Use one primary number everywhere. Add tap-to-call and a WhatsApp link with a pre-filled message.", "priority": "High"},
        {"area": "Construction rates", "saw": "Rates are published as a single screenshot with no date, so they cannot be searched and are hard to read on a phone.", "recommend": "Rebuild as a dated, searchable price table and review it monthly.", "priority": "High"},
        {"area": "Project gallery", "saw": "Photos are labelled by location only, several simply read “Completed project”, and a job marked 90% complete sits in the Completed list.", "recommend": "Turn the gallery into case-study cards: service, location, scope, duration and before/after, with a filter by service.", "priority": "High"},
        {"area": "Home page", "saw": "Opens with a seven-slide full-width carousel. Offers and calls to action compete for attention, and few visitors see past slide one.", "recommend": "One focused hero with a single call to action. Move the offers into cards below it.", "priority": "Medium"},
        {"area": "Designs page", "saw": "Designs have no pricing guidance and no enquiry button. The page description reads “Latest Trending Designs”.", "recommend": "Add “Request this design” to every image, pre-filling the enquiry form, and write a proper page description.", "priority": "Medium"},
        {"area": "Images", "saw": "Photos and the header logo carry camera file names as their image text (for example “WhatsApp Image 2026-01-19”).", "recommend": "Rename files, add descriptive alt text and compress to WebP. This helps speed, accessibility and image search.", "priority": "Medium"},
        {"area": "About page", "saw": "Four repeated “About Click & Go Builders Solutions” headings link to a blog post and read as template leftovers. The home page presents an in-house team while the About page describes a matching platform.", "recommend": "Replace them with real related content and use one consistent description of the business across the site.", "priority": "Medium"},
        {"area": "Blog", "saw": "Ten guides from the launch period and nothing newer. Two posts have no featured image.", "recommend": "Publish one article a month targeting searches such as “cost of building a house in Kenya”, and add the missing images.", "priority": "Medium"},
        {"area": "Site polish", "saw": "“Alluminium” is misspelt in the menu and service cards. Cabro and Landscaping appear twice in the footer. LinkedIn, X and YouTube icons go nowhere. A copy-protection script blocks right-click, so visitors cannot copy a phone number or email.", "recommend": "Correct the spelling, tidy the footer, link or remove the icons and remove the copy-blocking script.", "priority": "Low"},
        {"area": "Testimonials", "saw": "Thirteen reviews, several one-liners, with no photos or project links.", "recommend": "Add the project name and a photo where permitted, and show a live Google Reviews feed.", "priority": "Low"},
    ],
    "updates_intro": "We recommend working through the findings in three stages. All three stages are delivered inside the flat monthly fee, so the site improves steadily without separate project quotes.",
    "roadmap": [
        {"label": "Month 1", "title": "Foundation and quick wins", "items": [
            "Full backup and a private staging copy of the site",
            "Update WordPress core, theme, Elementor and all plugins, tested before going live",
            "One primary phone number everywhere, with tap-to-call",
            "Fix spelling, footer links and empty social icons",
            "Rename, compress and add alt text to images",
            "Remove the copy-blocking script",
            "Rebuild the construction rates as a dated web table",
            "Set up uptime monitoring, form-delivery tests and monthly reporting"]},
        {"label": "Month 2", "title": "Turning visitors into enquiries", "items": [
            "New home page hero with one clear call to action",
            "Project case-study layout with filter by service",
            "“Request this design” buttons across the Designs page",
            "One consolidated request form with instant email and WhatsApp alert, an automatic reply to the client and a lead log",
            "Replace the About page placeholders and align the business description across the site"]},
        {"label": "Month 3", "title": "Reach and growth", "items": [
            "Location pages for the areas you serve most: Nairobi, Machakos, Kajiado, Kisumu, Bungoma and Eldoret",
            "Structured data for the business, services and reviews, and a matching Google Business Profile",
            "Testimonials upgraded with projects and a Google Reviews feed",
            "First SEO article published, with a six-month content calendar",
            "Month-three review of enquiries, traffic and next priorities"]},
    ],
    "plan_intro": "Every month, for the flat fee, Black Code Labs looks after the following.",
    "plan_groups": [
        {"title": "Care and security", "items": [
            "Updates to WordPress, theme, Elementor and plugins, tested on a staging copy first",
            "Daily off-site backups kept for 30 days, with restores on request",
            "Malware scans, firewall, login protection and spam filtering",
            "Renewal reminders for the domain, hosting and SSL certificate"]},
        {"title": "Speed and uptime", "items": [
            "24/7 uptime monitoring with instant alerts",
            "Monthly speed check, image optimisation and cache management",
            "Monthly broken-link check and a test enquiry through every form"]},
        {"title": "Content and improvements", "items": [
            "Up to 10 hours each month for changes: new projects, rates, designs, banners, text and pages",
            "One SEO-focused article each month, written and published by us",
            "Extra hours beyond the allocation at KES 1,500 per hour, agreed before work starts"]},
        {"title": "Reporting and support", "items": [
            "A report by the 5th of each month: uptime, visitors, top pages, enquiries and work completed",
            "Urgent issues acknowledged within 4 business hours, routine requests completed within 2 working days",
            "Support by phone, WhatsApp and email"]},
    ],
    "fee_period": "per month, invoiced in advance",
    "includes": [
        "Everything in the monthly management plan",
        "The three-month improvement programme in Section 2",
        "Onboarding, first-week audit and backup, at no setup fee",
        "No per-task charges inside the plan",
    ],
    "not_included": "Hosting, domain renewal and any paid plugin licences are billed at cost and stay in your name, so you always own your accounts. Larger new builds, such as those listed under growth features, are quoted separately. Fees are exclusive of applicable taxes.",
    "growth_intro": "These are larger builds. They are not part of the monthly fee and are quoted separately, only if you want them. Each one is aimed at a specific kind of client the business already serves.",
    "growth": [
        {"name": "Online cost estimator", "text": "Visitors enter house size and finish level and receive a budget range, then leave their details to receive a full quote. This turns the rates page into a lead source."},
        {"name": "Diaspora client portal", "text": "A private page where clients abroad see progress photos, milestones and updates for their own project. It speaks directly to the local and diaspora clients the site is built for."},
        {"name": "WhatsApp enquiry assistant", "text": "An automated assistant that answers common questions, collects project details and books site visits, so no enquiry waits until morning."},
        {"name": "Site-visit booking", "text": "Clients choose a date and time for a site visit online, and the visit lands straight in your calendar."},
    ],
    "terms": [
        {"label": "Term", "text": "Three months from the start date, then month to month. Either side may end the plan with 30 days’ written notice."},
        {"label": "Billing", "text": "Invoiced on the 1st of each month in advance, payable by M-Pesa or bank transfer within five days."},
        {"label": "Access we need", "text": "Administrator access to the WordPress dashboard, the hosting control panel, the domain DNS, and Google Analytics and Search Console."},
        {"label": "Ownership", "text": "All content, accounts and data remain the property of Click & Go Builders Solutions."},
        {"label": "Working method", "text": "Changes are built and tested on a private copy of the site and published only once checked. Logins are held in an encrypted password manager."},
    ],
    "steps": [
        {"title": "Approve", "text": "Sign the acceptance below and return it by email."},
        {"title": "Share access", "text": "Send the logins listed above, or add us as administrators."},
        {"title": "Week-one audit", "text": "Full backup, staging copy and update audit, then Month 1 work begins."},
    ],
    "about": "Black Code Labs is a Nairobi web and software development company. We build web applications, business automation and chatbots in Python, Django, JavaScript and React Native, and we treat security as part of every build rather than an afterthought. We would be glad to look after the Click & Go Builders Solutions website the same way.",
    "signatory": "Odhiambo Churchill",
}

# Reusable parts only. Everything about the client is left for the form.
DEFAULTS = {
    "title": "Proposal for Website Management & Maintenance",
    "intro": [SAMPLE["intro"][0].replace("clickandgobuilders.com page by page, covering the home page, About, Projects, Designs, Construction Rates, Blog and Contact pages, and we looked at it the way a first-time client would", "the website page by page, and we looked at it the way a first-time client would"), "", SAMPLE["intro"][2]],
    "fee_amount": "20000", "term_months": "3",
    "fee_note": SAMPLE["fee_note"],
    "glance": SAMPLE["glance"],
    "review_intro": SAMPLE["review_intro"],
    "updates_intro": SAMPLE["updates_intro"],
    "roadmap": [SAMPLE["roadmap"][0], {"label": "Month 2", "title": "", "items": []}, {"label": "Month 3", "title": "", "items": []}],
    "plan_intro": SAMPLE["plan_intro"],
    "plan_groups": SAMPLE["plan_groups"],
    "fee_period": SAMPLE["fee_period"],
    "includes": SAMPLE["includes"],
    "not_included": SAMPLE["not_included"].replace("Larger new builds, such as those listed under growth features, are quoted separately.", "Larger new builds are quoted separately."),
    "growth_intro": SAMPLE["growth_intro"],
    "terms": [SAMPLE["terms"][0], SAMPLE["terms"][1], SAMPLE["terms"][2], {"label": "Ownership", "text": "All content, accounts and data remain the property of the client."}, SAMPLE["terms"][4]],
    "steps": SAMPLE["steps"],
    "about": SAMPLE["about"].replace(" We would be glad to look after the Click & Go Builders Solutions website the same way.", " We would be glad to look after your website the same way."),
    "signatory": "",
}


class WebsiteManagementProposal(DocType):
    key = "proposal"
    label = "Website Management Proposal"
    code = "WM"
    description = "Site review, improvement roadmap and a flat monthly management fee."
    amount_label = "Contract value (fee × initial term)"

    sections = [
        section("Client & document", [
            text("client_name", "Client / company", required=True),
            text("client_contact", "Contact / team", placeholder="The Management Team"),
            text("client_location", "Client location", placeholder="Nairobi, Kenya"),
            text("website", "Website reviewed", placeholder="clientsite.com"),
            date_("date", "Document date", required=True),
            date_("valid_until", "Valid until", required=True),
            text("title", "Proposal title", required=True, max_len=120),
            text("salutation", "Salutation", placeholder="Dear Management Team,"),
        ]),
        section("Introduction", [
            lines("intro", "Introduction paragraphs", item_kind="textarea", max_items=6,
                  placeholder="Write a paragraph about what you found and why it matters"),
            rows("stats", "“What the site already has” tiles (up to 4)", [
                text("value", "Number", required=True, max_len=12, placeholder="18"),
                text("label", "Label", required=True, max_len=40, placeholder="service lines presented"),
            ], max_items=4),
        ], hint="Tiles are optional. Leave them empty to skip the strip."),
        section("At a glance", [
            money("fee_amount", "Monthly fee", required=True, min=0),
            text("fee_note", "Note after the fee", max_len=160),
            rows("glance", "Other rows", [
                text("label", "Label", required=True, max_len=40),
                textarea("text", "Text", required=True, max_len=600),
            ], max_items=8),
        ]),
        section("01 · Website review", [
            textarea("review_intro", "Introduction", max_len=800),
            rows("working", "What is working", [
                text("title", "Headline", required=True, max_len=80),
                textarea("text", "Detail", required=True, max_len=500),
            ], max_items=12),
            rows("findings", "Priority findings", [
                text("area", "Area", required=True, max_len=60),
                textarea("saw", "What we saw", required=True, max_len=700),
                textarea("recommend", "What we recommend", required=True, max_len=700),
                select("priority", "Priority", ["High", "Medium", "Low"], required=True),
            ], max_items=20),
        ], hint="Leave both lists empty to leave the review section out."),
        section("02 · Recommended updates", [
            textarea("updates_intro", "Introduction", max_len=800),
            rows("roadmap", "Stages (usually 3 months)", [
                text("label", "Label", required=True, max_len=24, placeholder="Month 1"),
                text("title", "Stage title", max_len=60),
                lines("items", "Deliverables", max_items=14, max_len=300),
            ], max_items=4),
        ]),
        section("03 · Monthly management plan", [
            textarea("plan_intro", "Introduction", max_len=500),
            rows("plan_groups", "Groups", [
                text("title", "Group title", required=True, max_len=60),
                lines("items", "Included", max_items=10, max_len=300),
            ], max_items=6),
        ]),
        section("04 · Investment", [
            text("fee_period", "Under the fee", max_len=80),
            number("term_months", "Initial term (months)", min=1, max=60,
                   help="Used for the total value shown in your dashboard."),
            lines("includes", "What the fee includes", max_items=8, max_len=200),
            textarea("not_included", "Not included", max_len=800),
            textarea("growth_intro", "Optional extras intro", max_len=600),
            rows("growth", "Optional growth features", [
                text("name", "Feature", required=True, max_len=60),
                textarea("text", "Description", required=True, max_len=500),
            ], max_items=8),
        ]),
        section("05 · Terms, steps & sign-off", [
            rows("terms", "Terms", [
                text("label", "Label", required=True, max_len=40),
                textarea("text", "Text", required=True, max_len=600),
            ], max_items=10),
            rows("steps", "How we get started", [
                text("title", "Step", required=True, max_len=40),
                textarea("text", "Text", required=True, max_len=300),
            ], max_items=4),
            textarea("about", "About us paragraph", max_len=1200),
            text("signatory", "Signed for us by", placeholder="Name of signatory"),
        ]),
    ]

    def defaults(self):
        d = dict(DEFAULTS)
        d["date"] = _today().isoformat()
        d["valid_until"] = (_today() + timedelta(days=30)).isoformat()
        return d

    def sample(self):
        s = dict(SAMPLE)
        s["date"] = _today().isoformat()
        s["valid_until"] = (_today() + timedelta(days=30)).isoformat()
        return s

    def title(self, data):
        return data.get("title") or self.label

    def amount(self, data):
        fee = E.D(data.get("fee_amount"))
        months = E.D(data.get("term_months"), "1")
        return (fee * months) if fee else None

    # ------------------------------------------------------------------ render
    def render(self, d, meta):
        S = E.styles()
        brand = meta["brand"]
        cur = meta.get("currency", "KES")
        client = d.get("client_name", "")
        story = []

        story.append(E.meta_block(
            S,
            ("Prepared for", [client, d.get("client_contact"), d.get("client_location")]),
            [("Date", E.fmt_date(d.get("date"))), ("Reference", meta["reference"])],
            [("Valid until", E.fmt_date(d.get("valid_until")))]))
        story.append(E.Spacer(1, 24))
        story.append(E.P(d.get("title") or self.label, S["title"]))
        if d.get("website"):
            story.append(E.P(d["website"], S["subtitle"]))
        else:
            story.append(E.Spacer(1, 10))
        if d.get("salutation"):
            story.append(E.P(d["salutation"], S["body"]))
        for para in d.get("intro", []):
            story.append(E.P(para, S["body"]))

        tiles = E.stat_tiles(S, d.get("stats", []))
        if tiles is not None:
            story += [E.Spacer(1, 6), E.caption(S, "What the site already has"), E.Spacer(1, 5), tiles]

        fee_text = f"{E.fmt_money(d.get('fee_amount'), cur)}, flat. {d.get('fee_note', '')}".strip()
        glance = [("Monthly fee", fee_text)] + [(r["label"], r["text"]) for r in d.get("glance", [])]
        story += [E.Spacer(1, 16), E.caption(S, "The proposal at a glance"), E.Spacer(1, 4), E.kv_table(S, glance, key_w=E.CW * 0.235)]

        n = 0

        def heading(title, new_page=False):
            nonlocal n
            n += 1
            if new_page:
                story.append(E.PageBreak())
            else:
                story.append(E.CondPageBreak(160))
                story.append(E.Spacer(1, 12))
            story.append(E.section_heading(S, f"{n:02d}", title))
            story.append(E.Spacer(1, 5))

        # 01 review
        if d.get("working") or d.get("findings"):
            heading("Website review", new_page=True)
            if d.get("review_intro"):
                story.append(E.P(d["review_intro"], S["body"]))
            if d.get("working"):
                story.append(E.P("What is working", S["h3"]))
                for w in d["working"]:
                    story.append(E.Paragraph(f"<b>{E.esc(w['title'])}.</b> {E.rich(w['text'])}", S["bullet"], bulletText="•"))
            if d.get("findings"):
                story.append(E.P("Priority findings", S["h3"]))
                body = []
                for f in d["findings"]:
                    colr = E.PRIORITY.get(f["priority"], E.INK).hexval()[2:]
                    body.append([E.P(f["area"], S["cell_b"]), E.P(f["saw"], S["cell"]), E.P(f["recommend"], S["cell"]),
                                 E.Paragraph(f'<font color="#{colr}"><b>{E.esc(f["priority"])}</b></font>', S["cell"])])
                story.append(E.data_table(S, ["Area", "What we saw", "What we recommend", "Priority"], body,
                                          [E.CW * 0.148, E.CW * 0.366, E.CW * 0.366, E.CW * 0.12]))

        # 02 roadmap
        if d.get("roadmap"):
            heading("Recommended updates")
            if d.get("updates_intro"):
                story.append(E.P(d["updates_intro"], S["body"]))
            story.append(E.Spacer(1, 4))
            story.append(E.roadmap(S, d["roadmap"]))

        # 03 plan
        if d.get("plan_groups"):
            heading("Monthly management plan", new_page=True)
            if d.get("plan_intro"):
                story.append(E.P(d["plan_intro"], S["body"]))
            story.append(E.Spacer(1, 4))
            story.append(E.grid2(S, d["plan_groups"]))

        # 04 investment
        heading("Investment")
        story.append(E.fee_box(S, "Flat monthly fee", E.fmt_money(d.get("fee_amount"), cur), d.get("fee_period", ""), d.get("includes", [])))
        story.append(E.Spacer(1, 9))
        if d.get("not_included"):
            story.append(E.Paragraph(f"<b>Not included.</b> {E.rich(d['not_included'])}", S["small"]))
        if d.get("growth"):
            story.append(E.CondPageBreak(120))
            story.append(E.P("Optional growth features", S["h3"]))
            if d.get("growth_intro"):
                story.append(E.P(d["growth_intro"], S["body"]))
            story.append(E.kv_table(S, [(g["name"], g["text"]) for g in d["growth"]], key_w=E.CW * 0.26, pad=5))

        # 05 terms
        heading("Terms and next steps", new_page=True)
        terms = [(t["label"], t["text"]) for t in d.get("terms", [])]
        terms.append(("Validity", f"This proposal is valid until {E.fmt_date(d.get('valid_until'))}."))
        story.append(E.kv_table(S, terms, key_w=E.CW * 0.19))
        if d.get("steps"):
            story += [E.Spacer(1, 12), E.P("How we get started", S["h3"])]
            cells = [[E.Paragraph(f"{i}", S["step_n"]), E.Paragraph(f"<b>{E.esc(s['title'])}</b>", S["small"]), E.P(s["text"], S["cell"])]
                     for i, s in enumerate(d["steps"], 1)]
            story.append(E.columns(cells, gap=3, pad=11))
        if d.get("about"):
            story += [E.Spacer(1, 6), E.P(f"About {brand['name']}", S["h3"]), E.P(d["about"], S["body"])]
        story += [E.Spacer(1, 8), E.signature_block(S, f"Accepted for {client}" if client else "Accepted for the client",
                                    f"For {brand['name']}", d.get("signatory") or brand["signatory"])]

        return E.build_pdf(story, brand=brand, running_title=f"{self.label}   |   {client}" if client else self.label,
                           title=f"{self.label} {meta['reference']}")
