"""Shared look-and-feel for every generated PDF (fonts, colours, header/footer, components).

Pure ReportLab, so it installs from a wheel anywhere (no system libraries needed).
All user text goes through esc()/para() which escape markup, so a stray "<" or "&"
in a form can never break the document.
"""
import io
from datetime import date
from decimal import Decimal
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, Image, KeepTogether, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)
from reportlab.platypus.flowables import HRFlowable

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "fonts"
LOGO = ROOT / "assets" / "logo.png"

# ---- palette (sampled from the reference proposal)
INK = colors.HexColor("#111111")
BODY = colors.HexColor("#222626")
MUTED = colors.HexColor("#6B7373")
LINE = colors.HexColor("#DDE1E1")
TILE = colors.HexColor("#F1F3F3")
GREEN = colors.HexColor("#1C8F6E")
GREEN_LIGHT = colors.HexColor("#8FD3BC")
WHITE = colors.white
PRIORITY = {"High": colors.HexColor("#B83227"), "Medium": colors.HexColor("#C76F12"), "Low": colors.HexColor("#3C7F55")}

PAGE_W, PAGE_H = A4
LM = RM = 57
CW = PAGE_W - LM - RM
FIRST_TOP = 150      # space reserved for the full letterhead on page 1
LATER_TOP = 76
BOTTOM = 58

_fonts_ready = False


def register_fonts():
    global _fonts_ready
    if _fonts_ready:
        return
    for name, fn in [("Poppins", "Poppins-Regular"), ("Poppins-Medium", "Poppins-Medium"),
                     ("Poppins-SemiBold", "Poppins-SemiBold"), ("Poppins-Bold", "Poppins-Bold"),
                     ("Lato", "Lato-Regular"), ("Lato-Bold", "Lato-Bold")]:
        pdfmetrics.registerFont(TTFont(name, str(FONTS / f"{fn}.ttf")))
    # Lato italics aren't bundled; map them to upright so <i> never breaks.
    pdfmetrics.registerFontFamily("Lato", normal="Lato", bold="Lato-Bold", italic="Lato", boldItalic="Lato-Bold")
    _fonts_ready = True


# ---- text helpers
def esc(text):
    return escape(str(text if text is not None else ""))


def rich(text):
    """Escape, then turn newlines into line breaks."""
    return esc(text).replace("\r\n", "\n").replace("\n", "<br/>")


def _style(name, **kw):
    base = dict(fontName="Lato", fontSize=10, leading=15, textColor=BODY, splitLongWords=True)
    base.update(kw)
    return ParagraphStyle(name, **base)


def styles():
    register_fonts()
    S = {}
    S["body"] = _style("body", spaceAfter=7)
    S["title"] = _style("title", fontName="Poppins-Bold", fontSize=17.2, leading=23, textColor=INK, spaceAfter=3)
    S["subtitle"] = _style("subtitle", fontSize=10.5, textColor=MUTED, spaceAfter=14)
    S["label"] = _style("label", fontName="Lato-Bold", fontSize=6.8, leading=9, textColor=MUTED)
    S["meta"] = _style("meta", fontSize=10, leading=14.5)
    S["meta_b"] = _style("meta_b", fontName="Lato-Bold", fontSize=10, leading=14.5, textColor=INK)
    S["h2"] = _style("h2", fontName="Poppins-Bold", fontSize=16.5, leading=21, textColor=INK)
    S["h3"] = _style("h3", fontName="Poppins-Medium", fontSize=11.5, leading=15, textColor=INK, spaceBefore=6, spaceAfter=5)
    S["bullet"] = _style("bullet", leftIndent=12, bulletIndent=2, spaceAfter=4, leading=14.5)
    S["small"] = _style("small", fontSize=8.5, leading=12, textColor=BODY)
    S["small_b"] = _style("small_b", fontName="Lato-Bold", fontSize=8.5, leading=12, textColor=INK)
    S["cell"] = _style("cell", fontSize=8.6, leading=12)
    S["cell_b"] = _style("cell_b", fontName="Lato-Bold", fontSize=8.6, leading=12, textColor=INK)
    S["cell_r"] = _style("cell_r", fontSize=8.6, leading=12, alignment=TA_RIGHT)
    S["cell_rb"] = _style("cell_rb", fontName="Lato-Bold", fontSize=8.6, leading=12, textColor=INK, alignment=TA_RIGHT)
    S["th"] = _style("th", fontName="Lato-Bold", fontSize=7.4, leading=10, textColor=WHITE)
    S["th_r"] = _style("th_r", fontName="Lato-Bold", fontSize=7.4, leading=10, textColor=WHITE, alignment=TA_RIGHT)
    S["kv_k"] = _style("kv_k", fontName="Lato-Bold", fontSize=9.4, leading=13, textColor=INK)
    S["kv_v"] = _style("kv_v", fontSize=9, leading=13, textColor=colors.HexColor("#3B4141"))
    S["stat_n"] = _style("stat_n", fontName="Poppins-Bold", fontSize=19, leading=24, textColor=INK, alignment=TA_CENTER)
    S["stat_l"] = _style("stat_l", fontSize=8.6, leading=11, textColor=MUTED, alignment=TA_CENTER)
    S["card_t"] = _style("card_t", fontName="Poppins-Medium", fontSize=10, leading=14, textColor=INK, spaceAfter=3)
    S["card_b"] = _style("card_b", fontSize=8.5, leading=11.4, leftIndent=10, bulletIndent=0, spaceAfter=2)
    S["white_label"] = _style("white_label", fontSize=7.4, leading=10, textColor=GREEN_LIGHT)
    S["fee"] = _style("fee", fontName="Poppins-Bold", fontSize=27, leading=32, textColor=WHITE)
    S["white_small"] = _style("white_small", fontSize=8.6, leading=12, textColor=colors.HexColor("#CFD6D6"))
    S["white_bullet"] = _style("white_bullet", fontSize=9.4, leading=13.5, textColor=WHITE, leftIndent=12, bulletIndent=2, spaceAfter=3)
    S["step_n"] = _style("step_n", fontName="Poppins-Bold", fontSize=16, leading=20, textColor=GREEN)
    S["sig_l"] = _style("sig_l", fontSize=7.6, leading=10, textColor=MUTED)
    S["sig_v"] = _style("sig_v", fontSize=9.5, leading=12, textColor=INK)
    S["clause"] = _style("clause", fontName="Poppins-SemiBold", fontSize=11.5, leading=15, textColor=INK)
    S["sub"] = _style("sub", leftIndent=28, bulletIndent=0, spaceAfter=5, leading=14.2, fontSize=9.6)
    S["stamp"] = _style("stamp", fontName="Poppins-Bold", fontSize=11, leading=14, textColor=GREEN, alignment=TA_RIGHT)
    return S


def P(text, style):
    return Paragraph(rich(text), style)


def bullets(items, style, char="•"):
    return [Paragraph(rich(i), style, bulletText=char) for i in items if i]


# ---- formatting
def fmt_date(value):
    if not value:
        return ""
    try:
        d = date.fromisoformat(value) if isinstance(value, str) else value
    except ValueError:
        return str(value)
    return f"{d.day} {d.strftime('%B %Y')}"


def D(value, default="0"):
    try:
        return Decimal(str(value).replace(",", "")) if value not in ("", None) else Decimal(default)
    except Exception:
        return Decimal(default)


def fmt_money(value, currency="KES", decimals=None):
    d = D(value)
    if decimals is None:
        decimals = 0 if d == d.to_integral() else 2
    return f"{currency} {d:,.{decimals}f}"


# ---- page furniture
class NumberedCanvas(rl_canvas.Canvas):
    """Two-pass canvas so the footer can say 'Page X of Y'."""

    footer_left = ""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._saved = []

    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved)
        for state in self._saved:
            self.__dict__.update(state)
            self._footer(total)
            super().showPage()
        super().save()

    def _footer(self, total):
        self.setStrokeColor(LINE)
        self.setLineWidth(0.7)
        self.line(LM, 44, PAGE_W - RM, 44)
        self.setFont("Lato", 7.8)
        self.setFillColor(MUTED)
        self.drawString(LM, 32, self.footer_left)
        self.drawRightString(PAGE_W - RM, 32, f"Page {self._pageNumber} of {total}")


def build_pdf(story, *, brand, running_title, footer_left=None, title="Document", author=None):
    """Lays out `story` on A4 with the letterhead on page 1 and a slim running header after."""
    register_fonts()
    buf = io.BytesIO()
    footer = footer_left or f"{brand['name']}   |   {brand['website']}   |   {brand['email']}   |   {brand['phone']}"

    def first_page(c, doc):
        c.saveState()
        top = PAGE_H
        if LOGO.exists():
            c.drawImage(str(LOGO), LM, top - 98, width=76, height=76, mask="auto")
        c.saveState()
        c.setFillColor(INK)
        t = c.beginText(152, top - 66)
        t.setCharSpace(1.6)
        t.setFont("Poppins-Bold", 17)
        t.textOut(brand["name"].upper())
        c.drawText(t)
        c.restoreState()
        c.setFillColor(MUTED)
        c.setFont("Lato", 9.2)
        c.drawString(152, top - 84, brand["tagline"])
        c.setFillColor(BODY)
        c.setFont("Lato", 9.2)
        for i, line in enumerate([brand["phone"], brand["email"], brand["website"], brand["city"]]):
            c.drawRightString(PAGE_W - RM, top - 43 - i * 15.5, line)
        c.setStrokeColor(LINE)
        c.setLineWidth(1)
        c.line(LM, top - 124, PAGE_W - RM, top - 124)
        c.setStrokeColor(GREEN)
        c.setLineWidth(3.2)
        c.line(LM, top - 124, LM + 80, top - 124)
        c.restoreState()

    def later_page(c, doc):
        c.saveState()
        top = PAGE_H
        if LOGO.exists():
            c.drawImage(str(LOGO), LM, top - 53, width=26, height=26, mask="auto")
        c.saveState()
        t = c.beginText(LM + 34, top - 44)
        t.setCharSpace(1.3)
        t.setFont("Poppins-Bold", 8.4)
        t.setFillColor(INK)
        t.textOut(brand["name"].upper())
        c.drawText(t)
        c.restoreState()
        c.setFont("Lato", 8.4)
        c.setFillColor(MUTED)
        c.drawRightString(PAGE_W - RM, top - 44, running_title)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.7)
        c.line(LM, top - 62, PAGE_W - RM, top - 62)
        c.restoreState()

    doc = BaseDocTemplate(buf, pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=LATER_TOP, bottomMargin=BOTTOM,
                          title=title, author=author or brand["name"], creator=brand["name"])
    f_first = Frame(LM, BOTTOM, CW, PAGE_H - FIRST_TOP - BOTTOM, id="first", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    f_later = Frame(LM, BOTTOM, CW, PAGE_H - LATER_TOP - BOTTOM, id="later", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="first", frames=[f_first], onPage=first_page, autoNextPageTemplate="later"),
                          PageTemplate(id="later", frames=[f_later], onPage=later_page)])

    class _Canvas(NumberedCanvas):
        pass
    _Canvas.footer_left = footer
    doc.build(story, canvasmaker=_Canvas)
    return buf.getvalue()


# ---- components
def meta_block(S, left, middle, right):
    """left: (label, [lines]) with first line bold; middle: [(label, value)...]; right: [(label, value)...]"""
    def stack(pairs):
        out = []
        for label, value in pairs:
            out.append(Paragraph(esc(label.upper()), S["label"]))
            out.append(Paragraph(rich(value), S["meta"]))
            out.append(Spacer(1, 4))
        return out[:-1] if out else out

    lab, lines_ = left
    first = [Paragraph(esc(lab.upper()), S["label"]), Paragraph(rich(lines_[0]), S["meta_b"])]
    first += [Paragraph(rich(x), S["meta"]) for x in lines_[1:] if x]
    t = Table([[first, stack(middle), stack(right)]], colWidths=[CW * 0.50, CW * 0.285, CW * 0.215])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return t


def section_heading(S, num, title):
    t = Table([[Paragraph(f'<font color="#1C8F6E">{esc(num)}</font>', S["h2"]), Paragraph(esc(title), S["h2"])]],
              colWidths=[30, CW - 30])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "BOTTOM"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 6), ("LINEBELOW", (0, 0), (-1, -1), 0.7, LINE)]))
    t.keepWithNext = True
    return t


def caption(S, text):
    p = Paragraph(esc(text.upper()), S["label"])
    p.keepWithNext = True
    return p


def stat_tiles(S, items):
    items = items[:4]
    if not items:
        return None
    n = len(items)
    gap = 4
    w = (CW - gap * (n - 1)) / n
    cells, widths = [], []
    for i, it in enumerate(items):
        cells.append([Paragraph(esc(it["value"]), S["stat_n"]), Paragraph(esc(it["label"]), S["stat_l"])])
        widths.append(w)
        if i < n - 1:
            cells.append("")
            widths.append(gap)
    t = Table([cells], colWidths=widths)
    style = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 10),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 10), ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6)]
    for i in range(n):
        style.append(("BACKGROUND", (i * 2, 0), (i * 2, 0), TILE))
    t.setStyle(TableStyle(style))
    return t


def kv_table(S, rows, key_w=110, pad=6):
    """Label/value rows between two heavy rules (the 'at a glance' / 'terms' tables)."""
    data = [[Paragraph(esc(k), S["kv_k"]), Paragraph(rich(v), S["kv_v"])] for k, v in rows]
    if not data:
        return None
    t = Table(data, colWidths=[key_w, CW - key_w])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 3),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 3), ("TOPPADDING", (0, 0), (-1, -1), pad),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), pad), ("LINEABOVE", (0, 0), (-1, 0), 1.4, INK),
                           ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE), ("LINEBELOW", (0, -1), (-1, -1), 1.4, INK)]))
    return t


def data_table(S, headers, body, widths, right_cols=(), zebra=True):
    """Black header row + zebra body; header repeats on every page."""
    head = [Paragraph(esc(h.upper()), S["th_r"] if i in right_cols else S["th"]) for i, h in enumerate(headers)]
    t = Table([head] + body, colWidths=widths, repeatRows=1)
    st = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("BACKGROUND", (0, 0), (-1, 0), INK), ("LEFTPADDING", (0, 0), (-1, -1), 7),
          ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, 0), 6), ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
          ("TOPPADDING", (0, 1), (-1, -1), 7), ("BOTTOMPADDING", (0, 1), (-1, -1), 7),
          ("LINEBELOW", (0, 1), (-1, -2), 0.5, LINE), ("LINEBELOW", (0, -1), (-1, -1), 1.4, INK)]
    if zebra:
        for r in range(2, len(body) + 1, 2):
            st.append(("BACKGROUND", (0, r), (-1, r), TILE))
    t.setStyle(TableStyle(st))
    return t


def columns(cells, gap=3, bg=TILE, header_bg=None, pad=10):
    """Equal-width boxed columns (roadmap, steps). cells: list of flowable-lists (or (header, body))."""
    n = len(cells)
    w = (CW - gap * (n - 1)) / n
    row, widths = [], []
    for i, c in enumerate(cells):
        row.append(c)
        widths.append(w)
        if i < n - 1:
            row.append("")
            widths.append(gap)
    t = Table([row], colWidths=widths)
    st = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), pad), ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
          ("LEFTPADDING", (0, 0), (-1, -1), pad), ("RIGHTPADDING", (0, 0), (-1, -1), pad)]
    for i in range(n):
        st.append(("BACKGROUND", (i * 2, 0), (i * 2, 0), bg))
    for i in range(n - 1):
        st.append(("LEFTPADDING", (i * 2 + 1, 0), (i * 2 + 1, 0), 0))
        st.append(("RIGHTPADDING", (i * 2 + 1, 0), (i * 2 + 1, 0), 0))
    t.setStyle(TableStyle(st))
    return t


def roadmap(S, months):
    n = len(months)
    gap = 3
    w = (CW - gap * (n - 1)) / n
    head_row, body_row, widths = [], [], []
    for i, m in enumerate(months):
        head_row.append([Paragraph(esc((m.get("label") or f"Month {i + 1}").upper()), S["white_label"] if False else
                                   ParagraphStyle("mh", parent=S["th"], fontSize=7.6, textColor=WHITE, fontName="Lato")),
                         Paragraph(esc(m.get("title", "")), ParagraphStyle("mt", parent=S["card_t"], textColor=GREEN_LIGHT,
                                                                           fontName="Poppins-SemiBold", fontSize=9.4, leading=13))])
        body_row.append(bullets(m.get("items", []), S["card_b"]))
        widths.append(w)
        if i < n - 1:
            head_row.append("")
            body_row.append("")
            widths.append(gap)
    t = Table([head_row, body_row], colWidths=widths)
    st = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
          ("TOPPADDING", (0, 0), (-1, 0), 9), ("BOTTOMPADDING", (0, 0), (-1, 0), 9), ("TOPPADDING", (0, 1), (-1, 1), 10),
          ("BOTTOMPADDING", (0, 1), (-1, 1), 10)]
    for i in range(n):
        st += [("BACKGROUND", (i * 2, 0), (i * 2, 0), INK), ("BACKGROUND", (i * 2, 1), (i * 2, 1), TILE)]
    for i in range(n - 1):
        for r in (0, 1):
            st += [("LEFTPADDING", (i * 2 + 1, r), (i * 2 + 1, r), 0), ("RIGHTPADDING", (i * 2 + 1, r), (i * 2 + 1, r), 0)]
    t.setStyle(TableStyle(st))
    return t


def grid2(S, groups):
    """2-up grid of gray cards: each group = {title, items}."""
    cells = [[Paragraph(esc(g["title"]), S["card_t"])] + bullets(g.get("items", []), S["card_b"]) for g in groups]
    if len(cells) % 2:
        cells.append("")
    gap = 3
    w = (CW - gap) / 2
    data, st = [], [("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]
    for r in range(0, len(cells), 2):
        data.append([cells[r], "", cells[r + 1]])
    t = Table(data, colWidths=[w, gap, w])
    for r in range(len(data)):
        st += [("BACKGROUND", (0, r), (0, r), TILE), ("LEFTPADDING", (1, r), (1, r), 0), ("RIGHTPADDING", (1, r), (1, r), 0)]
        if data[r][2] != "":
            st.append(("BACKGROUND", (2, r), (2, r), TILE))
        if r:
            st.append(("LINEABOVE", (0, r), (-1, r), 3, WHITE))
    t.setStyle(TableStyle(st))
    return t


def fee_box(S, label, amount_text, sub, includes):
    left = [Paragraph(esc(label.upper()), S["white_label"]), Spacer(1, 4), Paragraph(esc(amount_text), S["fee"]),
            Paragraph(esc(sub), S["white_small"])]
    right = [Paragraph("WHAT THE FEE INCLUDES", S["white_label"]), Spacer(1, 5)] + bullets(includes, S["white_bullet"])
    t = Table([[left, right]], colWidths=[CW * 0.395, CW * 0.605])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), INK), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 20), ("RIGHTPADDING", (0, 0), (-1, -1), 16),
                           ("TOPPADDING", (0, 0), (-1, -1), 15), ("BOTTOMPADDING", (0, 0), (-1, -1), 13),
                           ("LINEAFTER", (0, 0), (0, 0), 0.6, colors.HexColor("#555555"))]))
    return t


def signature_block(S, left_title, right_title, right_name="", heading="Acceptance", left_name=""):
    def col(title, name):
        items = [Paragraph(esc(title.upper()), ParagraphStyle("st", parent=S["small_b"], fontSize=8, leading=11)), Spacer(1, 16)]
        for label, value in (("Name", name), ("Signature", ""), ("Date", "")):
            line = Table([[Paragraph(esc(value) if value else "&nbsp;", S["sig_v"])]], colWidths=[CW * 0.44])
            line.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.9, INK), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                      ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
            items += [line, Paragraph(label, S["sig_l"]), Spacer(1, 10)]
        return items
    t = Table([[col(left_title, left_name), col(right_title, right_name)]], colWidths=[CW * 0.5, CW * 0.5])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    return KeepTogether([Paragraph(esc(heading), S["h3"]), t])


def clause_heading(S, num, title):
    """'7   Revisions and changes': green number, bold title, hairline underneath."""
    t = Table([[Paragraph(f'<font color="#1C8F6E">{esc(num)}</font>', S["clause"]), Paragraph(esc(title), S["clause"])]],
              colWidths=[28, CW - 28])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "BOTTOM"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 4), ("LINEBELOW", (0, 0), (-1, -1), 0.6, LINE)]))
    t.keepWithNext = True
    return t


def subclauses(S, num, texts):
    """Numbered sub-paragraphs: 7.1, 7.2 ... (hanging indent)."""
    return [Paragraph(rich(t), S["sub"], bulletText=f"{num}.{i}") for i, t in enumerate([t for t in texts if t], 1)]
