"""Service Agreement: a universal software / web project contract.

You enter the client, the scope, the price, the timeline and how they pay. The standard
clauses (IP, revisions, support, termination, governing law ...) are written from the
parameters on the form, so numbering and cross-references can never drift out of sync.
"""
from datetime import date
from decimal import ROUND_HALF_UP, Decimal

from Studio.pdf import engine as E
from Studio.schema import DocType, date_, lines, money, number, rows, section, select, text, textarea

CURRENCIES = ["KES", "USD", "EUR", "GBP"]
Q = Decimal("0.01")

DEFAULT_TIMELINE_NOTE = ("The timeline assumes the Client supplies content, feedback and approvals on time. "
                         "Delays on the Client's side move the delivery date by the same number of days.")
DEFAULT_LATE = "If a payment is more than 7 days overdue, the Developer may pause work until it is received, and the delivery date moves accordingly."
DEFAULT_THIRD_PARTY = ("Domain names, hosting, paid plugins and licences, SMS and email credits, payment-gateway fees and app-store accounts "
                       "are not included in the Contract Price. They are billed at cost, without mark-up, and registered in the Client's name.")
DEFAULT_METHODS = "M-Pesa or bank transfer. Payment details are on each invoice."


def money_of(d):
    """Contract price, VAT and total payable, from the form data."""
    price = E.D(d.get("total_price")).quantize(Q, ROUND_HALF_UP)
    vat = (price * E.D(d.get("vat_rate")) / 100).quantize(Q, ROUND_HALF_UP)
    return price, vat, price + vat


def schedule(d):
    """Each instalment's amount; the last one absorbs rounding so the rows always add up to the total."""
    _, _, payable = money_of(d)
    out, running = [], Decimal("0")
    items = d.get("payment_schedule", [])
    for i, r in enumerate(items):
        amt = payable - running if i == len(items) - 1 else (payable * E.D(r.get("percent")) / 100).quantize(Q, ROUND_HALF_UP)
        running += amt
        out.append((r, amt))
    return out


SAMPLE = {
    "client_name": "Mwangi & Daughters Ltd", "client_reg": "Company No. CPR/2019/123456",
    "client_representative": "Grace Mwangi, Managing Director", "client_address": "Westlands, Nairobi, Kenya",
    "client_contact": "grace@mwangidaughters.co.ke  |  0722 000 000",
    "title": "Website Development Agreement", "project_title": "Online store with M-Pesa checkout",
    "project_summary": "The Developer will design, build and launch an online store for the Client where customers can browse products, pay by M-Pesa or card, and track their orders, together with an admin dashboard for the Client's team.",
    "deliverables": [
        {"title": "Online store", "description": "Mobile-first storefront with up to 60 products, categories, search, filters, cart and checkout."},
        {"title": "M-Pesa and card payments", "description": "Safaricom Daraja STK Push checkout with automatic order confirmation, plus card payments through the Client's gateway account."},
        {"title": "Admin dashboard", "description": "Secure back office to manage products, orders, customers, discounts and delivery fees."},
        {"title": "Notifications", "description": "Order confirmation by email and SMS to the customer, and an instant alert to the Client's team."},
        {"title": "SEO and analytics setup", "description": "Page titles, descriptions, sitemap, Google Search Console and Google Analytics."},
        {"title": "Training and handover", "description": "A half-day training session and a short user guide for the Client's staff."},
    ],
    "out_of_scope": ["Product photography and copywriting", "Mobile apps", "Ongoing marketing and advertising"],
    "assumptions": ["The Client supplies product names, prices and images before development starts", "The Client holds an active M-Pesa Paybill or Till number"],
    "client_provides": ["Logo and brand colours", "Product information and images", "Access to the domain name and M-Pesa Daraja credentials"],
    "start_date": "2026-11-02", "duration": "6 weeks from receipt of the deposit", "completion_date": "2026-12-14",
    "milestones": [
        {"phase": "1. Design", "delivers": "Approved homepage and product page designs", "when": "End of week 1"},
        {"phase": "2. Build", "delivers": "Working store with catalogue and cart", "when": "End of week 3"},
        {"phase": "3. Payments", "delivers": "M-Pesa and card checkout, notifications", "when": "End of week 5"},
        {"phase": "4. Launch", "delivers": "Testing, training, go-live", "when": "End of week 6"},
    ],
    "timeline_note": DEFAULT_TIMELINE_NOTE,
    "currency": "KES", "total_price": "165000", "vat_rate": "0",
    "price_breakdown": [{"item": "Online store and admin dashboard", "amount": "120000"}, {"item": "M-Pesa and card payment integration", "amount": "35000"},
                        {"item": "Training and handover", "amount": "10000"}],
    "payment_schedule": [{"label": "Deposit", "percent": "50", "due": "On signing this Agreement"},
                         {"label": "Balance", "percent": "50", "due": "On delivery, before the store goes live"}],
    "payment_methods": "M-Pesa Paybill 000000 (Account: the invoice number), or bank transfer. Details are on each invoice.",
    "late_payment": DEFAULT_LATE, "third_party": DEFAULT_THIRD_PARTY,
    "revision_rounds": "2", "hourly_rate": "2500", "support_days": "30", "termination_days": "14", "feedback_days": "3",
    "governing_law": "Kenya", "city": "Nairobi",
    "extra_clauses": [],
    "our_signatory": "Odhiambo Churchill", "our_title": "Director", "client_signatory": "Grace Mwangi", "client_title": "Managing Director",
    "include_witness": "No",
}

DEFAULTS = {
    "title": "Service Agreement", "currency": "KES", "vat_rate": "0",
    "deliverables": [{"title": "", "description": ""}],
    "payment_schedule": SAMPLE["payment_schedule"], "payment_methods": DEFAULT_METHODS,
    "late_payment": DEFAULT_LATE, "third_party": DEFAULT_THIRD_PARTY, "timeline_note": DEFAULT_TIMELINE_NOTE,
    "revision_rounds": "2", "support_days": "30", "termination_days": "14", "feedback_days": "3",
    "governing_law": "Kenya", "city": "Nairobi", "our_title": "Director", "include_witness": "No",
}


class ServiceAgreement(DocType):
    key = "contract"
    label = "Service Agreement"
    code = "AGR"
    description = "Contract for a build: scope of work, price, timeline, payment schedule and standard terms."
    amount_label = "Contract value (incl. VAT)"

    sections = [
        section("Parties & project", [
            text("client_name", "Client (legal name)", required=True),
            text("client_reg", "Client ID / registration / KRA PIN", help="Optional. Printed under the client's name."),
            text("client_representative", "Client representative", placeholder="Name and title"),
            text("client_address", "Client address"),
            text("client_contact", "Client email / phone"),
            date_("date", "Agreement date", required=True),
            date_("effective_date", "Effective from", help="Leave empty to use the agreement date."),
            text("title", "Agreement title", required=True, max_len=100),
            text("project_title", "Project name", required=True, max_len=140, placeholder="Online store with M-Pesa checkout"),
            textarea("project_summary", "What we are going to build", required=True, max_len=1500,
                     help="A short plain-English description of the project."),
        ]),
        section("Scope of work", [
            rows("deliverables", "Deliverables", [
                text("title", "Deliverable", required=True, max_len=100),
                textarea("description", "What it includes", required=True, max_len=600),
            ], min_items=1, max_items=40),
            lines("out_of_scope", "Not included (out of scope)", max_items=15, max_len=250),
            lines("assumptions", "Assumptions", max_items=15, max_len=300),
            lines("client_provides", "What the client must provide", max_items=15, max_len=250),
        ]),
        section("Timeline", [
            date_("start_date", "Start date"),
            text("duration", "Delivery time", required=True, max_len=120, placeholder="6 weeks from receipt of the deposit"),
            date_("completion_date", "Target completion date"),
            rows("milestones", "Milestones (optional)", [
                text("phase", "Phase", required=True, max_len=80),
                text("delivers", "What is delivered", max_len=250),
                text("when", "When", max_len=80),
            ], max_items=15),
            textarea("timeline_note", "Timeline note", max_len=600),
        ]),
        section("Price & payment", [
            select("currency", "Currency", CURRENCIES, required=True),
            money("total_price", "Contract price", required=True, min=1),
            number("vat_rate", "VAT %", min=0, max=30, help="0 if you do not charge VAT. Kenya VAT is 16%."),
            rows("price_breakdown", "Price breakdown (optional)", [
                text("item", "Item", required=True, max_len=140),
                money("amount", "Amount", required=True, min=0),
            ], max_items=20, help="If used, the items must add up to the contract price."),
            rows("payment_schedule", "Payment schedule", [
                text("label", "Payment", required=True, max_len=60, placeholder="Deposit"),
                number("percent", "% of total", required=True, min=0.01, max=100),
                text("due", "When due", required=True, max_len=120, placeholder="On signing this Agreement"),
            ], min_items=1, max_items=10, help="The percentages must add up to 100."),
            textarea("payment_methods", "Payment mode", required=True, max_len=600,
                     help="How the client pays: M-Pesa Paybill / Till, bank details, etc."),
            textarea("late_payment", "Late payment", max_len=600),
            textarea("third_party", "Third-party costs", max_len=800),
        ]),
        section("Terms", [
            number("revision_rounds", "Included revision rounds", min=0, max=20),
            money("hourly_rate", "Rate for extra work (per hour)", min=0, help="Optional."),
            number("support_days", "Free bug-fix support after delivery (days)", min=0, max=365),
            number("termination_days", "Termination notice (days)", min=1, max=180),
            number("feedback_days", "Client feedback time (working days)", min=1, max=30),
            text("governing_law", "Governing law", max_len=60),
            text("city", "Courts / mediation in", max_len=60),
            rows("extra_clauses", "Extra clauses (optional)", [
                text("heading", "Heading", required=True, max_len=80),
                textarea("text", "Clause text", required=True, max_len=1500),
            ], max_items=8, help="Added after the standard clauses and numbered automatically."),
        ]),
        section("Signatures", [
            text("our_signatory", "Signed for us by", placeholder="Name"),
            text("our_title", "Our signatory's title"),
            text("client_signatory", "Client signatory"),
            text("client_title", "Client signatory's title"),
            select("include_witness", "Witness lines", ["No", "Yes"]),
        ]),
    ]

    def defaults(self):
        d = dict(DEFAULTS)
        d["date"] = date.today().isoformat()
        return d

    def sample(self):
        d = dict(SAMPLE)
        d["date"] = date.today().isoformat()
        return d

    def title(self, data):
        return data.get("project_title") or data.get("title") or self.label

    def amount(self, data):
        return money_of(data)[2] or None

    def currency(self, data):
        return data.get("currency") or "KES"

    def validate(self, d):
        errors = {}
        pct = sum((E.D(r.get("percent")) for r in d.get("payment_schedule", [])), Decimal("0"))
        if pct != Decimal("100"):
            errors["payment_schedule"] = f"The percentages add up to {pct.normalize():f}%. They must add up to 100%."
        if d.get("price_breakdown"):
            total = sum((E.D(r.get("amount")) for r in d["price_breakdown"]), Decimal("0"))
            if total != E.D(d.get("total_price")):
                errors["price_breakdown"] = f"The items add up to {total:,.2f}, but the contract price is {E.D(d.get('total_price')):,.2f}."
        if d.get("start_date") and d.get("completion_date") and d["completion_date"] < d["start_date"]:
            errors["completion_date"] = "Completion date is before the start date."
        return errors

    # ------------------------------------------------------------------ render
    def render(self, d, meta):
        S, brand, cur = E.styles(), meta["brand"], meta.get("currency", "KES")
        dev = brand["name"]
        client = d.get("client_name", "")
        price, vat, payable = money_of(d)
        eff = d.get("effective_date") or d.get("date")
        law = d.get("governing_law") or "Kenya"
        city = d.get("city") or "Nairobi"
        fb = d.get("feedback_days") or "3"
        story = []

        story.append(E.meta_block(S, ("Client", [client, d.get("client_representative"), d.get("client_address"), d.get("client_reg")]),
                                  [("Date", E.fmt_date(d.get("date"))), ("Reference", meta["reference"])],
                                  [("Effective from", E.fmt_date(eff))]))
        story += [E.Spacer(1, 22), E.P(d.get("title") or self.label, S["title"]), E.P(d.get("project_title", ""), S["subtitle"])]
        story.append(E.P(f"This Agreement is made on {E.fmt_date(d.get('date'))} between {dev}, of {brand['city']} (the “Developer”), "
                         f"and {client}{', ' + d['client_address'] if d.get('client_address') else ''} (the “Client”). "
                         "It sets out what the Developer will build, when, for how much, and how it will be paid for.", S["body"]))

        glance = [("Project", d.get("project_title", "")), ("Contract price", self._price_line(cur, price, vat, payable, d)),
                  ("Timeline", d.get("duration", "") + (f" (target completion {E.fmt_date(d['completion_date'])})" if d.get("completion_date") else "")),
                  ("Payment", " · ".join(f"{r['label']} {E.fmt_money(a, cur, 2)}" for r, a in schedule(d))),
                  ("Support", f"{d['support_days']} days of free bug-fix support after delivery" if E.D(d.get("support_days")) else "As agreed")]
        story += [E.Spacer(1, 6), E.caption(S, "The agreement at a glance"), E.Spacer(1, 4), E.kv_table(S, glance, key_w=E.CW * 0.2)]

        n = 0

        def clause(title):
            nonlocal n
            n += 1
            story.append(E.CondPageBreak(110))
            story.extend([E.Spacer(1, 11), E.clause_heading(S, f"{n}", title), E.Spacer(1, 5)])
            return n

        # 1 Parties
        c = clause("Parties")
        parts = [f"<b>The Developer:</b> {dev}, {brand['city']}. Email {brand['email']}, phone {brand['phone']}.",
                 f"<b>The Client:</b> {client}"
                 + (f" ({d['client_reg']})" if d.get("client_reg") else "")
                 + (f", {d['client_address']}" if d.get("client_address") else "")
                 + (f". Represented by {d['client_representative']}" if d.get("client_representative") else "")
                 + (f". Contact: {d['client_contact']}" if d.get("client_contact") else "") + "."]
        story += [E.Paragraph(p_, S["sub"], bulletText=f"{c}.{i}") for i, p_ in enumerate(parts, 1)]

        # 2 Project
        c = clause("Project overview")
        story += E.subclauses(S, c, [d.get("project_summary", ""), "In this Agreement, the “Project” means everything described under Scope of Work, and the “Deliverables” are the items listed there."])

        # 3 Scope
        c = clause("Scope of work")
        story.append(E.Paragraph(f"The Developer will deliver the following:", S["sub"], bulletText=f"{c}.1"))
        body = [[E.P(str(i), S["cell"]), E.P(x["title"], S["cell_b"]), E.P(x["description"], S["cell"])] for i, x in enumerate(d.get("deliverables", []), 1)]
        story += [E.Spacer(1, 2), E.data_table(S, ["No.", "Deliverable", "What it includes"], body, [E.CW * 0.07, E.CW * 0.27, E.CW * 0.66])]
        k = 2
        if d.get("out_of_scope"):
            story += [E.Spacer(1, 6), E.Paragraph("<b>Not included.</b> The following is outside this Agreement and, if wanted, will be quoted separately:", S["sub"], bulletText=f"{c}.{k}")]
            story += E.bullets(d["out_of_scope"], ParagraphStyleIndent(S))
            k += 1
        if d.get("assumptions"):
            story += [E.Spacer(1, 3), E.Paragraph("<b>Assumptions.</b> The price and timeline are based on these assumptions:", S["sub"], bulletText=f"{c}.{k}")]
            story += E.bullets(d["assumptions"], ParagraphStyleIndent(S))

        # 4 Timeline
        c = clause("Timeline")
        rowsk = [("Start date", E.fmt_date(d.get("start_date")) or "On receipt of the deposit"), ("Delivery time", d.get("duration", ""))]
        if d.get("completion_date"):
            rowsk.append(("Target completion", E.fmt_date(d["completion_date"])))
        story.append(E.kv_table(S, rowsk, key_w=E.CW * 0.2))
        if d.get("milestones"):
            story.append(E.Spacer(1, 7))
            body = [[E.P(m["phase"], S["cell_b"]), E.P(m.get("delivers", ""), S["cell"]), E.P(m.get("when", ""), S["cell"])] for m in d["milestones"]]
            story.append(E.data_table(S, ["Phase", "What is delivered", "When"], body, [E.CW * 0.25, E.CW * 0.5, E.CW * 0.25]))
        if d.get("timeline_note"):
            story += [E.Spacer(1, 6)] + E.subclauses(S, c, [d["timeline_note"]])

        # 5 Price and payment
        c = clause("Price and payment")
        story.append(E.Paragraph(f"The price for the Project is <b>{E.fmt_money(price, cur, 2)}</b>"
                                 + (f", plus VAT of {E.fmt_money(vat, cur, 2)} ({E.D(d['vat_rate']).normalize():f}%), a total of <b>{E.fmt_money(payable, cur, 2)}</b>" if vat else "")
                                 + " (the “Contract Price”).", S["sub"], bulletText=f"{c}.1"))
        if d.get("price_breakdown"):
            body = [[E.P(r["item"], S["cell"]), E.Paragraph(E.fmt_money(r["amount"], cur, 2), S["cell_r"])] for r in d["price_breakdown"]]
            story += [E.Spacer(1, 2), E.data_table(S, ["Price breakdown", "Amount"], body, [E.CW * 0.72, E.CW * 0.28], right_cols=(1,), zebra=False)]
        sched = [[E.P(r["label"], S["cell_b"]), E.Paragraph(f"{E.D(r['percent']).normalize():f}%", S["cell_r"]),
                  E.Paragraph(f"<b>{E.fmt_money(a, cur, 2)}</b>", S["cell_r"]), E.P(r["due"], S["cell"])] for r, a in schedule(d)]
        story += [E.Spacer(1, 7), E.Paragraph("The Client will pay the Contract Price in these instalments:", S["sub"], bulletText=f"{c}.2"),
                  E.Spacer(1, 2), E.data_table(S, ["Payment", "% of total", "Amount", "When due"], sched,
                                               [E.CW * 0.2, E.CW * 0.14, E.CW * 0.22, E.CW * 0.44], right_cols=(1, 2))]
        story.append(E.Spacer(1, 7))
        story += [E.Paragraph(f"<b>Payment mode.</b> {E.rich(d.get('payment_methods', ''))}", S["sub"], bulletText=f"{c}.3")]
        more = [d.get("late_payment"), d.get("third_party")]
        story += [E.Paragraph(E.rich(t), S["sub"], bulletText=f"{c}.{i}") for i, t in enumerate([m for m in more if m], 4)]

        # 6.. standard clauses
        c = clause("Client responsibilities")
        story += E.subclauses(S, c, [
            f"The Client will provide the materials, information, access and decisions the Developer reasonably needs, and will give feedback and approvals within {fb} working days of each request."
            + (" The Client will in particular provide: " + "; ".join(d["client_provides"]) + "." if d.get("client_provides") else ""),
            "The Client will name one contact person who can give approvals on the Client's behalf.",
            "The Client confirms that it owns, or has the right to use, all content and materials it supplies, and that they do not infringe anyone else's rights."])

        c = clause("Revisions and changes")
        rate = f"{E.fmt_money(d['hourly_rate'], cur)} per hour" if E.D(d.get("hourly_rate")) else "a rate agreed in advance"
        story += E.subclauses(S, c, [
            f"The Contract Price includes {d.get('revision_rounds') or '2'} rounds of revisions to the design and functionality described in the Scope of Work.",
            "A request that goes beyond the Scope of Work is a change request. The Developer will state in writing what it would add to the price and the timeline, and will start only after the Client approves in writing (email is enough).",
            f"Approved extra work is charged at {rate}."])

        c = clause("Intellectual property")
        story += E.subclauses(S, c, [
            "When the Client has paid the Contract Price in full, ownership of the Deliverables created specifically for the Client (including the source code, designs and content) passes to the Client. Until then they remain the Developer's.",
            f"The Developer keeps ownership of its pre-existing tools, frameworks, libraries and know-how, and grants the Client a perpetual, royalty-free licence to use them as part of the Deliverables. Third-party and open-source components stay under their own licences.",
            "The Developer may describe the Project in its portfolio, unless the Client asks in writing for it to stay private."])

        c = clause("Confidentiality")
        story += E.subclauses(S, c, [
            "Each party will keep the other's confidential information (business information, credentials, customer data and unpublished plans) private, use it only for this Project, and not share it except with people who need it and are bound to keep it private.",
            "This does not cover information that is public through no fault of the receiving party, was already known to it, or must be disclosed by law. This clause continues for 3 years after the Agreement ends."])

        c = clause("Warranty and support")
        sd = d.get("support_days") or "0"
        story += E.subclauses(S, c, [
            "The Developer will carry out the work with reasonable skill and care, and the Deliverables will materially match the Scope of Work.",
            f"For {sd} days after delivery, the Developer will fix defects in the Deliverables that are reported in writing, free of charge." if E.D(sd) else "Support after delivery is available on request under a separate arrangement.",
            "This does not cover new features, changes made by anyone other than the Developer, failures of hosting or third-party services, or misuse. Ongoing maintenance can be agreed separately."])

        c = clause("Data protection")
        story += E.subclauses(S, c, [
            "Each party will comply with the Data Protection Act, 2019 of Kenya and any related regulations when handling personal data in connection with the Project.",
            "The Developer will process personal data only to deliver the Project and on the Client's instructions, and will keep it secure."])

        c = clause("Limitation of liability")
        story += E.subclauses(S, c, [
            "Neither party is liable for indirect or consequential loss, such as lost profit, lost business or lost data.",
            "The Developer's total liability under this Agreement is limited to the amount the Client has paid under it. Nothing here limits liability that cannot be limited by law.",
            "The Developer is not responsible for delays or failures caused by third-party services outside its control."])

        c = clause("Termination")
        td = d.get("termination_days") or "14"
        story += E.subclauses(S, c, [
            f"Either party may end this Agreement by giving {td} days' written notice.",
            "Either party may end it immediately by written notice if the other commits a serious breach and does not fix it within 7 days of being told.",
            "If the Agreement ends early, the Client will pay for the work completed up to that date and for third-party costs already committed. The Developer will then hand over the completed work, subject to that payment."])

        c = clause("Disputes and governing law")
        story += E.subclauses(S, c, [
            "The parties will first try to settle any dispute by talking in good faith. If that fails within 14 days, they will try mediation before going to court.",
            f"This Agreement is governed by the laws of {law}. Any dispute not settled by mediation will be heard by the courts of {law} sitting in {city}."])

        for x in d.get("extra_clauses", []):
            c = clause(x["heading"])
            story += E.subclauses(S, c, [x["text"]])

        c = clause("General")
        story += E.subclauses(S, c, [
            "This Agreement is the whole agreement between the parties about the Project and replaces anything said or written before it. It can be changed only in writing signed or approved by both parties.",
            "Notices may be sent by email to the addresses on the first page. Neither party may transfer its rights or duties under this Agreement without the other's written consent.",
            "Neither party is liable for failure caused by events beyond its reasonable control, such as power or internet outages, natural disasters or government action.",
            "If any part of this Agreement is found unenforceable, the rest stays in force. The parties may sign in counterparts, and electronic signatures are valid."])

        # signatures
        story.append(E.Spacer(1, 12))
        def who(name, title):
            return ", ".join(x for x in (name, title) if x)
        story.append(E.signature_block(S, f"For the Client: {client}", f"For the Developer: {dev}",
                                       who(d.get("our_signatory") or brand["signatory"], d.get("our_title")), heading="Signed by the parties",
                                       left_name=who(d.get("client_signatory"), d.get("client_title"))))
        if d.get("include_witness") == "Yes":
            story.append(E.Spacer(1, 6))
            story.append(E.signature_block(S, "Witness for the Client", "Witness for the Developer", "", heading="Witnesses"))

        return E.build_pdf(story, brand=brand, running_title=f"{self.label}   |   {client}" if client else self.label,
                           title=f"{self.label} {meta['reference']}")

    @staticmethod
    def _price_line(cur, price, vat, payable, d):
        if vat:
            return f"{E.fmt_money(price, cur, 2)} + VAT {E.fmt_money(vat, cur, 2)} = {E.fmt_money(payable, cur, 2)}"
        return E.fmt_money(price, cur, 2)


def ParagraphStyleIndent(S):
    from reportlab.lib.styles import ParagraphStyle
    return ParagraphStyle("sub_b", parent=S["sub"], leftIndent=40, bulletIndent=28, spaceAfter=2)
