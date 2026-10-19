import io
import json
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from pypdf import PdfReader

from . import doctypes
from .branding import brand
from .models import GeneratedDocument
from .schema import clean_document
from .doctypes.billing import totals

STATIC_PLAIN = {"default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
                "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}}


def pages(pdf_bytes):
    return len(PdfReader(io.BytesIO(bytes(pdf_bytes))).pages)


def text_of(pdf_bytes):
    return "\n".join(p.extract_text() for p in PdfReader(io.BytesIO(bytes(pdf_bytes))).pages)


@override_settings(STORAGES=STATIC_PLAIN, ALLOWED_HOSTS=["*"])
class StudioTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        U = get_user_model()
        cls.staff = U.objects.create_user("boss", password="x", is_staff=True)
        cls.plain = U.objects.create_user("visitor", password="x")

    def setUp(self):
        self.client.force_login(self.staff)

    def save(self, key, data=None, **extra):
        t = doctypes.get(key)
        body = {"type": key, "data": data if data is not None else t.sample(), **extra}
        return self.client.post(reverse("studio:document_save"), json.dumps(body), content_type="application/json")

    # ------------------------------------------------------------- access
    def test_anonymous_is_sent_to_login_and_non_staff_is_forbidden(self):
        doc = self.save("invoice").json()
        pk = doc["url"].strip("/").split("/")[-1]
        urls = [reverse("studio:dashboard"), reverse("studio:document_list"), reverse("studio:document_new"),
                reverse("studio:document_pdf", args=[pk]), reverse("studio:document_detail", args=[pk])]
        self.client.logout()
        for u in urls:
            r = self.client.get(u)
            self.assertEqual(r.status_code, 302, u)
            self.assertIn("/accounts/login/", r["Location"])
        self.client.force_login(self.plain)
        for u in urls:
            self.assertEqual(self.client.get(u).status_code, 403, u)
        self.assertEqual(self.save("invoice").status_code, 403)

    def test_pages_render_for_staff(self):
        for t in doctypes.all_types():
            self.assertEqual(self.client.get(reverse("studio:document_new") + f"?type={t.key}").status_code, 200)
        self.assertEqual(self.client.get(reverse("studio:document_new") + "?type=nope").status_code, 404)
        self.assertEqual(self.client.get(reverse("studio:dashboard")).status_code, 200)
        self.assertEqual(self.client.get(reverse("studio:document_list")).status_code, 200)

    # ------------------------------------------------------------- generation
    def test_every_type_renders_a_real_pdf_from_its_example(self):
        for t in doctypes.all_types():
            data, errors = clean_document(t.sections, t.sample())
            self.assertFalse(errors, (t.key, dict(errors)))
            pdf = t.render(data, {"brand": brand(), "reference": "BCL-XX-2610-01", "currency": "KES"})
            self.assertTrue(pdf.startswith(b"%PDF-"))
            self.assertIn("BLACK CODE LABS", text_of(pdf).upper())
        data, _ = clean_document(doctypes.get("proposal").sections, doctypes.get("proposal").sample())
        pdf = doctypes.get("proposal").render(data, {"brand": brand(), "reference": "R", "currency": "KES"})
        self.assertEqual(pages(pdf), 5)  # same length as the reference proposal

    def test_save_stores_data_and_pdf_and_serves_it_back(self):
        r = self.save("proposal")
        self.assertEqual(r.status_code, 200, r.content)
        doc = GeneratedDocument.objects.get()
        self.assertRegex(doc.reference, r"^BCL-WM-\d{4}-01$")
        self.assertEqual(doc.client_name, "Click & Go Builders Solutions")
        self.assertEqual(doc.amount, Decimal("60000"))  # 20,000 x 3 months
        self.assertTrue(bytes(doc.pdf).startswith(b"%PDF-"))
        self.assertIn(doc.reference, text_of(doc.pdf))
        resp = self.client.get(reverse("studio:document_pdf", args=[doc.pk]) + "?download=1")
        self.assertEqual(resp["Content-Type"], "application/pdf")
        self.assertIn(f'attachment; filename="{doc.reference}.pdf"', resp["Content-Disposition"])
        self.assertEqual(resp.content, bytes(doc.pdf))
        self.assertEqual(resp["X-Frame-Options"], "SAMEORIGIN")  # so the preview iframe works

    def test_references_increment_per_type_and_month(self):
        self.save("invoice")
        self.save("invoice")
        self.save("quotation")
        refs = sorted(GeneratedDocument.objects.values_list("reference", flat=True))
        suffix = refs[0][-7:-3]
        self.assertEqual(refs, sorted([f"BCL-INV-{suffix}-01", f"BCL-INV-{suffix}-02", f"BCL-QT-{suffix}-01"]))

    def test_edit_regenerates_in_place(self):
        self.save("quotation")
        doc = GeneratedDocument.objects.get()
        data = dict(doctypes.get("quotation").sample(), client_name="New Client Ltd")
        r = self.save("quotation", data, id=doc.pk)
        self.assertEqual(r.status_code, 200)
        doc.refresh_from_db()
        self.assertEqual((GeneratedDocument.objects.count(), doc.revision, doc.client_name), (1, 2, "New Client Ltd"))
        self.assertIn("New Client Ltd", text_of(doc.pdf))

    def test_validation_errors_are_reported_per_field_and_nothing_is_saved(self):
        data = dict(doctypes.get("quotation").sample(), client_name="", valid_until="not-a-date", vat_rate="abc",
                    items=[{"description": "", "details": "", "qty": "1", "unit_price": "10"}])
        r = self.save("quotation", data)
        self.assertEqual(r.status_code, 422)
        errs = r.json()["errors"]
        self.assertIn("client_name", errs)
        self.assertIn("valid_until", errs)
        self.assertIn("vat_rate", errs)
        self.assertIn("items.0.description", errs)
        self.assertEqual(GeneratedDocument.objects.count(), 0)

    def test_hostile_text_cannot_break_the_pdf(self):
        data = dict(doctypes.get("quotation").sample(), client_name='<b>Tom & "Jerry"</b> <unclosed',
                    intro="5 < 6 & 7 > 3 </para> <font color=red>x", project_title="<script>alert(1)</script>")
        self.assertEqual(self.save("quotation", data).status_code, 200)
        pdf = GeneratedDocument.objects.get().pdf
        self.assertIn("<script>alert(1)</script>", text_of(pdf))  # shown literally, not interpreted

    # ------------------------------------------------------------- schema + maths
    def test_blank_rows_are_dropped_and_numbers_normalised(self):
        t = doctypes.get("quotation")
        data, errors = clean_document(t.sections, dict(t.sample(), items=[
            {"description": "A", "details": "", "qty": "2", "unit_price": "1,500.50"},
            {"description": "", "details": "", "qty": "", "unit_price": ""}]))
        self.assertFalse(errors)
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["items"][0]["unit_price"], "1500.50")

    def test_totals(self):
        t = totals({"items": [{"qty": "2", "unit_price": "100"}, {"qty": "1", "unit_price": "50.50"}],
                    "discount": "50", "vat_rate": "16", "amount_paid": "100"})
        self.assertEqual((t["subtotal"], t["discount"], t["vat"], t["total"], t["balance"]),
                         (Decimal("250.50"), Decimal("50.00"), Decimal("32.08"), Decimal("232.58"), Decimal("132.58")))

    def test_discount_cannot_exceed_subtotal(self):
        self.assertEqual(totals({"items": [{"qty": "1", "unit_price": "100"}], "discount": "999"})["total"], Decimal("0.00"))

    # ------------------------------------------------------------- actions
    def test_status_duplicate_delete(self):
        self.save("invoice")
        doc = GeneratedDocument.objects.get()
        r = self.client.post(reverse("studio:document_status", args=[doc.pk]), {"status": "accepted", "next": "https://evil.example/"})
        self.assertEqual(r.status_code, 302)
        self.assertNotIn("evil.example", r["Location"])  # open redirects are refused
        doc.refresh_from_db()
        self.assertEqual(doc.status, "accepted")
        self.client.post(reverse("studio:document_status", args=[doc.pk]), {"status": "bogus"})
        doc.refresh_from_db()
        self.assertEqual(doc.status, "accepted")
        self.client.post(reverse("studio:document_duplicate", args=[doc.pk]))
        self.assertEqual(GeneratedDocument.objects.count(), 2)
        copy = GeneratedDocument.objects.exclude(pk=doc.pk).get()
        self.assertEqual((copy.status, copy.client_name), ("draft", doc.client_name))
        self.assertNotEqual(copy.reference, doc.reference)
        self.client.post(reverse("studio:document_delete", args=[doc.pk]))
        self.assertEqual(GeneratedDocument.objects.count(), 1)

    def test_actions_require_post(self):
        self.save("invoice")
        doc = GeneratedDocument.objects.get()
        for name in ("document_delete", "document_duplicate", "document_status"):
            self.assertEqual(self.client.get(reverse(f"studio:{name}", args=[doc.pk])).status_code, 405)

    def test_dashboard_and_list_with_data(self):
        for k in ("proposal", "quotation", "invoice"):
            self.save(k)
        r = self.client.get(reverse("studio:dashboard"))
        self.assertContains(r, "chart-data")
        charts = r.context["charts"]
        self.assertEqual(sum(sum(s["data"]) for s in charts["by_month"]["series"]), 3)
        self.assertEqual(r.context["stats"]["docs"], 3)
        listing = self.client.get(reverse("studio:document_list") + "?type=invoice&q=Click")
        self.assertEqual(len(listing.context["page"].object_list), 1)

    def test_pdf_is_not_stored_under_public_media(self):
        self.save("invoice")
        self.assertFalse(hasattr(GeneratedDocument._meta.get_field("pdf"), "upload_to"))


@override_settings(STORAGES=STATIC_PLAIN, ALLOWED_HOSTS=["*"])
class LoginRedirectTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        U = get_user_model()
        U.objects.create_user("boss", password="pw-12345-x", is_staff=True)
        U.objects.create_user("visitor", password="pw-12345-x")

    def login(self, user, next_=""):
        url = reverse("accounts:login") + (f"?next={next_}" if next_ else "")
        return self.client.post(url, {"username": user, "password": "pw-12345-x", "next": next_})

    def test_staff_without_next_go_to_studio(self):
        self.assertEqual(self.login("boss")["Location"], reverse("studio:dashboard"))

    def test_regular_user_goes_to_blog(self):
        self.assertEqual(self.login("visitor")["Location"], reverse("blog:list"))

    def test_next_is_honoured_but_only_for_local_urls(self):
        self.assertEqual(self.login("visitor", "/pricing/")["Location"], "/pricing/")
        self.client.logout()
        self.assertEqual(self.login("visitor", "https://evil.example/")["Location"], reverse("blog:list"))
