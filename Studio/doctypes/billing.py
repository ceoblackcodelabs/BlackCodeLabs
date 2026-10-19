"""Quotation and Invoice: both are 'client + line items + totals', so they share one renderer."""
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal

from Studio.pdf import engine as E
from Studio.schema import DocType, date_, lines, money, number, rows, section, select, text, textarea

CURRENCIES = ["KES", "USD", "EUR", "GBP"]


def totals(d):
    """All arithmetic lives here so the PDF, the dashboard value and the tests agree."""
    q = Decimal("0.01")
    sub = Decimal("0")
    for it in d.get("items", []):
        sub += E.D(it.get("qty"), "1") * E.D(it.get("unit_price"))
    sub = sub.quantize(q, ROUND_HALF_UP)
    discount = min(E.D(d.get("discount")), sub).quantize(q, ROUND_HALF_UP)
    taxable = sub - discount
    vat = (taxable * E.D(d.get("vat_rate")) / 100).quantize(q, ROUND_HALF_UP)
    total = taxable + vat
    paid = E.D(d.get("amount_paid"))
    return {"subtotal": sub, "discount": discount, "vat": vat, "total": total, "paid": paid,
            "balance": (total - paid).quantize(q, ROUND_HALF_UP)}


def _num(v):
    d = E.D(v, "1")
    return f"{d:,.2f}".rstrip("0").rstrip(".") if d != d.to_integral() else f"{d:,.0f}"


def _client_fields():
    return [
        text("client_name", "Client / company", required=True),
        text("client_contact", "Contact person"),
        text("client_location", "Location"),
        text("client_email", "Email / phone"),
    ]


def _items_section(extra_hint=""):
    return section("Line items", [
        select("currency", "Currency", CURRENCIES, required=True),
        rows("items", "Items", [
            text("description", "Item", required=True, max_len=160),
            textarea("details", "Details (optional)", max_len=400),
            number("qty", "Qty", min=0, placeholder="1"),
            money("unit_price", "Unit price", required=True, min=0),
        ], min_items=1, max_items=40),
        money("discount", "Discount (amount)", min=0),
        number("vat_rate", "VAT %", min=0, max=30, help="Leave 0 if you don't charge VAT (Kenya VAT is 16%)."),
    ], hint=extra_hint)


class _Billing(DocType):
    kind_word = ""       # "Quotation" | "Invoice"
    right_label = ""     # "Valid until" | "Due date"
    right_field = ""

    def amount(self, d):
        return totals(d)["total"]

    def title(self, d):
        return d.get("project_title") or self.label

    def currency(self, d):
        return d.get("currency") or "KES"

    def _items_table(self, S, d, cur):
        body = []
        for it in d.get("items", []):
            qty = E.D(it.get("qty"), "1")
            amt = qty * E.D(it.get("unit_price"))
            desc = [E.Paragraph(f"<b>{E.esc(it['description'])}</b>", S["cell"])]
            if it.get("details"):
                desc.append(E.P(it["details"], S["small"]))
            body.append([desc, E.Paragraph(_num(it.get("qty") or 1), S["cell_r"]),
                         E.Paragraph(E.fmt_money(it.get("unit_price"), cur, 2), S["cell_r"]),
                         E.Paragraph(f"<b>{E.fmt_money(amt, cur, 2)}</b>", S["cell_r"])])
        return E.data_table(S, ["Description", "Qty", "Unit price", "Amount"], body,
                            [E.CW * 0.52, E.CW * 0.09, E.CW * 0.19, E.CW * 0.20], right_cols=(1, 2, 3), zebra=False)

    def _totals_box(self, S, d, cur, balance=False):
        t = totals(d)
        r = [("Subtotal", E.fmt_money(t["subtotal"], cur, 2))]
        if t["discount"]:
            r.append(("Discount", "- " + E.fmt_money(t["discount"], cur, 2)))
        if E.D(d.get("vat_rate")):
            r.append((f"VAT ({_num(d['vat_rate'])}%)", E.fmt_money(t["vat"], cur, 2)))
        data = [[E.Paragraph(k, S["cell"]), E.Paragraph(v, S["cell_r"])] for k, v in r]
        data.append([E.Paragraph("<b>TOTAL</b>", ParagraphStyleWhite(S)), E.Paragraph(f"<b>{E.fmt_money(t['total'], cur, 2)}</b>", ParagraphStyleWhite(S, right=True))])
        if balance and t["paid"]:
            data.append([E.Paragraph("Paid", S["cell"]), E.Paragraph("- " + E.fmt_money(t["paid"], cur, 2), S["cell_r"])])
            data.append([E.Paragraph("<b>Balance due</b>", S["cell_b"]), E.Paragraph(f"<b>{E.fmt_money(t['balance'], cur, 2)}</b>", S["cell_rb"])])
        w = E.CW * 0.48
        tb = E.Table(data, colWidths=[w * 0.45, w * 0.55], hAlign="RIGHT")
        total_row = len(r)
        st = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
              ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
              ("BACKGROUND", (0, total_row), (-1, total_row), E.INK), ("LINEBELOW", (0, 0), (-1, total_row - 1), 0.5, E.LINE)]
        if balance and t["paid"]:
            st.append(("LINEBELOW", (0, -1), (-1, -1), 1.4, E.INK))
        tb.setStyle(E.TableStyle(st))
        return tb

    def _head(self, S, d, meta, bill_label):
        client = d.get("client_name", "")
        return [E.meta_block(
            S,
            (bill_label, [client, d.get("client_contact"), d.get("client_location"), d.get("client_email")]),
            [("Date", E.fmt_date(d.get("date"))), ("Reference", meta["reference"])],
            [(self.right_label, E.fmt_date(d.get(self.right_field)))])]


def ParagraphStyleWhite(S, right=False):
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_RIGHT
    return ParagraphStyle("tw", parent=S["cell_b"], textColor=E.WHITE, fontSize=10, leading=13, alignment=TA_RIGHT if right else 0)


# ----------------------------------------------------------------------------- quotation
class Quotation(_Billing):
    key = "quotation"
    label = "Quotation"
    code = "QT"
    description = "Priced quote with line items, optional VAT, payment terms and acceptance."
    amount_label = "Quoted total"
    kind_word = "Quotation"
    right_label = "Valid until"
    right_field = "valid_until"

    sections = [
        section("Client & quotation", _client_fields() + [
            date_("date", "Quotation date", required=True),
            date_("valid_until", "Valid until", required=True),
            text("project_title", "Project / quote title", required=True, max_len=140, placeholder="Website redevelopment"),
            textarea("intro", "Introduction", max_len=1500),
        ]),
        _items_section(),
        section("Scope & terms", [
            lines("scope", "What is included / assumptions", max_items=15, max_len=300),
            text("timeline", "Delivery time", max_len=200, placeholder="4 to 6 weeks from receipt of deposit"),
            textarea("payment_terms", "Payment terms", max_len=800),
            textarea("notes", "Other notes", max_len=1000),
            text("signatory", "Signed for us by"),
        ]),
    ]

    def defaults(self):
        return {"date": date.today().isoformat(), "valid_until": (date.today() + timedelta(days=14)).isoformat(),
                "currency": "KES", "vat_rate": "0", "items": [{"description": "", "details": "", "qty": "1", "unit_price": ""}],
                "payment_terms": "50% deposit to begin work and 50% on delivery. Payable by M-Pesa or bank transfer.",
                "intro": "Thank you for the opportunity to quote. Below is our proposed scope and pricing for your project."}

    def sample(self):
        d = self.defaults()
        d.update({"client_name": "Mwangi & Daughters Ltd", "client_contact": "Grace Mwangi", "client_location": "Westlands, Nairobi",
                  "client_email": "grace@mwangidaughters.co.ke", "project_title": "Online store with M-Pesa checkout",
                  "items": [{"description": "E-commerce website", "details": "Up to 40 products, mobile-first design, product search and filters.", "qty": "1", "unit_price": "120000"},
                            {"description": "M-Pesa (Daraja) payment integration", "details": "STK Push checkout with automatic order confirmation.", "qty": "1", "unit_price": "35000"},
                            {"description": "Staff training", "details": "Half-day session on managing products and orders.", "qty": "2", "unit_price": "5000"}],
                  "discount": "10000", "vat_rate": "16",
                  "scope": ["Domain and hosting set up in your name", "Two rounds of revisions", "30 days of free support after launch"],
                  "timeline": "6 weeks from receipt of the deposit", "signatory": "Odhiambo Churchill"})
        return d

    def render(self, d, meta):
        S, brand, cur = E.styles(), meta["brand"], meta.get("currency", "KES")
        story = self._head(S, d, meta, "Prepared for")
        story += [E.Spacer(1, 22), E.P(d.get("project_title") or "Quotation", S["title"]), E.P("Quotation", S["subtitle"])]
        if d.get("intro"):
            story.append(E.P(d["intro"], S["body"]))
        story += [E.Spacer(1, 6), self._items_table(S, d, cur), E.Spacer(1, 10), self._totals_box(S, d, cur)]
        if d.get("scope"):
            story += [E.Spacer(1, 12), E.P("What is included", S["h3"])] + E.bullets(d["scope"], S["bullet"])
        terms = []
        if d.get("timeline"):
            terms.append(("Delivery", d["timeline"]))
        if d.get("payment_terms"):
            terms.append(("Payment", d["payment_terms"]))
        terms.append(("Validity", f"This quotation is valid until {E.fmt_date(d.get('valid_until'))}."))
        if d.get("notes"):
            terms.append(("Notes", d["notes"]))
        story += [E.Spacer(1, 10), E.kv_table(S, terms, key_w=E.CW * 0.17)]
        client = d.get("client_name", "")
        story += [E.Spacer(1, 14), E.signature_block(S, f"Accepted for {client}" if client else "Accepted for the client", f"For {brand['name']}",
                                    d.get("signatory") or brand["signatory"])]
        return E.build_pdf(story, brand=brand, running_title=f"Quotation   |   {client}" if client else "Quotation",
                           title=f"Quotation {meta['reference']}")


# ----------------------------------------------------------------------------- invoice
class Invoice(_Billing):
    key = "invoice"
    label = "Invoice"
    code = "INV"
    description = "Tax-style invoice with line items, payments received and balance due."
    amount_label = "Invoice total"
    kind_word = "Invoice"
    right_label = "Due date"
    right_field = "due_date"

    sections = [
        section("Client & invoice", _client_fields() + [
            date_("date", "Invoice date", required=True),
            date_("due_date", "Due date", required=True),
            text("project_title", "For (project / description)", max_len=140, placeholder="Website maintenance, November"),
        ]),
        _items_section(),
        section("Payment", [
            money("amount_paid", "Amount already paid", min=0),
            textarea("payment_details", "How to pay", max_len=800,
                     placeholder="M-Pesa Paybill / Till number, bank name and account number"),
            textarea("notes", "Notes", max_len=1000),
        ]),
    ]

    def defaults(self):
        return {"date": date.today().isoformat(), "due_date": (date.today() + timedelta(days=7)).isoformat(),
                "currency": "KES", "vat_rate": "0", "items": [{"description": "", "details": "", "qty": "1", "unit_price": ""}],
                "notes": "Thank you for your business."}

    def sample(self):
        d = self.defaults()
        d.update({"client_name": "Click & Go Builders Solutions", "client_contact": "Accounts", "client_location": "Nairobi, Kenya",
                  "project_title": "Website management, November 2026",
                  "items": [{"description": "Website management plan", "details": "Updates, security, backups, 10 hours of changes and one SEO article.", "qty": "1", "unit_price": "20000"}],
                  "amount_paid": "0", "payment_details": "M-Pesa Paybill: 000000   Account: INV\nBank transfer: ask us for details"})
        return d

    def render(self, d, meta):
        S, brand, cur = E.styles(), meta["brand"], meta.get("currency", "KES")
        t = totals(d)
        story = self._head(S, d, meta, "Bill to")
        story += [E.Spacer(1, 22), E.P("Invoice", S["title"])]
        story.append(E.P(d.get("project_title") or " ", S["subtitle"]))
        if t["total"] and t["balance"] <= 0:
            story.append(E.P("PAID IN FULL", S["stamp"]))
        story += [E.Spacer(1, 6), self._items_table(S, d, cur), E.Spacer(1, 10), self._totals_box(S, d, cur, balance=True), E.Spacer(1, 14)]
        info = []
        if d.get("payment_details"):
            info.append(("How to pay", d["payment_details"]))
        info.append(("Due date", E.fmt_date(d.get("due_date"))))
        if d.get("notes"):
            info.append(("Notes", d["notes"]))
        story.append(E.kv_table(S, info, key_w=E.CW * 0.17))
        client = d.get("client_name", "")
        return E.build_pdf(story, brand=brand, running_title=f"Invoice   |   {client}" if client else "Invoice",
                           title=f"Invoice {meta['reference']}")
