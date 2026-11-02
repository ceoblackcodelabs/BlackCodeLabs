import json
from pathlib import Path

from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Solution, TechServices

TOKEN = "test-token-123"
OFFERINGS = Path(__file__).resolve().parent.parent / "scripts" / "content" / "offerings.json"


@override_settings(API_TOKEN=TOKEN, ALLOWED_HOSTS=["*"])
class ContentApiTests(TestCase):
    def setUp(self):
        cache.clear()  # solution pages sit behind cache_page

    def call(self, method, url, data=None, token=TOKEN):
        headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"} if token else {}
        return getattr(self.client, method)(
            url, data=json.dumps(data) if data is not None else None,
            content_type="application/json", **headers)

    # ---- auth
    def test_requires_token(self):
        url = reverse("api_services")
        self.assertEqual(self.call("get", url, token=None).status_code, 401)
        self.assertEqual(self.call("get", url, token="wrong").status_code, 401)
        self.assertEqual(self.call("get", url).status_code, 200)

    @override_settings(API_TOKEN="")
    def test_disabled_without_configured_token(self):
        self.assertEqual(self.call("get", reverse("api_services"), token="anything").status_code, 503)

    # ---- services
    def test_service_upsert_by_name(self):
        url = reverse("api_services")
        payload = {"name": "CCTV", "description": "d", "icon": '<i class="fas fa-video"></i>'}
        r = self.call("post", url, payload)
        self.assertEqual(r.status_code, 201)
        r = self.call("post", url, {**payload, "description": "changed", "name": "cctv"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(TechServices.objects.count(), 1)
        self.assertEqual(TechServices.objects.get().description, "changed")

    def test_service_validation(self):
        url = reverse("api_services")
        r = self.call("post", url, {"name": "X", "description": "d", "icon": "<script>alert(1)</script>"})
        self.assertEqual(r.status_code, 422)
        self.assertIn("icon", r.json()["fields"])
        self.assertEqual(self.call("post", url, {"name": "X"}).status_code, 422)
        self.assertEqual(self.call("post", url, {"name": "X", "description": "d", "icon": '<i class="a"></i>', "bogus": 1}).status_code, 400)
        self.assertEqual(TechServices.objects.count(), 0)

    def test_service_patch_and_delete(self):
        s = TechServices.objects.create(name="A", description="d", icon='<i class="a"></i>')
        url = reverse("api_service_item", args=[s.pk])
        self.assertEqual(self.call("patch", url, {"description": "new"}).status_code, 200)
        s.refresh_from_db()
        self.assertEqual(s.description, "new")
        self.assertEqual(self.call("put", url, {"name": "A"}).status_code, 422)  # PUT needs all fields
        self.assertEqual(self.call("delete", url).status_code, 200)
        self.assertEqual(self.call("get", url).status_code, 404)

    # ---- solutions
    def solution(self, **kw):
        base = {"title": "CCTV Systems", "short_description": "s", "detailed_description": "d",
                "icon_class": "fa-video", "features": ["one", "two"]}
        return {**base, **kw}

    def test_solution_create_update_and_slug(self):
        url = reverse("api_solutions")
        r = self.call("post", url, self.solution())
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["slug"], "cctv-systems")
        self.assertEqual(r.json()["features"], ["one", "two"])
        r = self.call("post", url, self.solution(short_description="updated", display_order=5))
        self.assertEqual(r.status_code, 200)
        sol = Solution.objects.get(slug="cctv-systems")
        self.assertEqual((sol.short_description, sol.display_order, sol.features), ("updated", 5, "one\ntwo"))

    def test_solution_validation(self):
        url = reverse("api_solutions")
        self.assertEqual(self.call("post", url, self.solution(icon_class="javascript:x")).status_code, 422)
        self.assertEqual(self.call("post", url, self.solution(short_description="x" * 201)).status_code, 422)
        self.assertEqual(self.call("post", url, self.solution(display_order="3")).status_code, 422)
        self.assertEqual(self.call("post", url, self.solution(is_active="yes")).status_code, 422)
        self.assertEqual(Solution.objects.count(), 0)

    def test_solution_hide_and_list(self):
        self.call("post", reverse("api_solutions"), self.solution(slug="cctv"))
        item = reverse("api_solution_item", args=["cctv"])
        self.assertEqual(self.call("patch", item, {"is_active": False}).status_code, 200)
        self.assertEqual(len(self.call("get", reverse("api_solutions")).json()["results"]), 0)
        self.assertEqual(len(self.call("get", reverse("api_solutions") + "?all=1").json()["results"]), 1)
        self.assertEqual(self.call("patch", item, {"slug": "other"}).status_code, 422)

    # ---- the real content file passes the real validation
    def test_offerings_file_is_valid_and_idempotent(self):
        data = json.loads(OFFERINGS.read_text())
        for _ in range(2):  # second pass must update, not duplicate
            for s in data["services"]:
                self.assertIn(self.call("post", reverse("api_services"), s).status_code, (200, 201), s["name"])
            for s in data["solutions"]:
                self.assertIn(self.call("post", reverse("api_solutions"), s).status_code, (200, 201), s["slug"])
        self.assertEqual(TechServices.objects.count(), len(data["services"]))
        self.assertEqual(Solution.objects.count(), len(data["solutions"]))
        page = self.client.get(reverse("solution_detail", args=["cctv-surveillance"]))
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, "Free site survey")

    def test_pages_show_api_content_and_hide_inactive(self):
        for s in json.loads(OFFERINGS.read_text())["solutions"]:
            self.call("post", reverse("api_solutions"), s)
        listing = self.client.get(reverse("solutions"))
        self.assertContains(listing, "CCTV &amp; Surveillance Systems")
        self.assertContains(listing, reverse("solution_detail", args=["access-control"]))
        self.call("patch", reverse("api_solution_item", args=["access-control"]), {"is_active": False})
        cache.clear()
        self.assertEqual(self.client.get(reverse("solution_detail", args=["access-control"])).status_code, 404)
        self.assertNotContains(self.client.get(reverse("solutions")), "Access Control &amp; Biometrics")


# ---------------------------------------------------------------------------- posts + portfolio
import base64
import io
import shutil
import tempfile

from django.core.cache import cache as _cache
from django.test import TestCase as _TestCase


def png_b64(size=(40, 30), fmt="PNG"):
    from PIL import Image
    buf = io.BytesIO()
    Image.new("RGB", size, (200, 40, 40)).save(buf, fmt)
    return base64.b64encode(buf.getvalue()).decode()


@override_settings(API_TOKEN=TOKEN, ALLOWED_HOSTS=["*"])
class PostsAndPortfolioApiTests(_TestCase):
    @classmethod
    def setUpTestData(cls):
        from django.contrib.auth import get_user_model
        U = get_user_model()
        cls.boss = U.objects.create_superuser("boss", "b@x.co", "pw")
        cls.other = U.objects.create_user("writer", password="pw")

    def setUp(self):
        _cache.clear()
        self.media = tempfile.mkdtemp()
        self._ov = override_settings(MEDIA_ROOT=self.media)
        self._ov.enable()
        self.addCleanup(self._ov.disable)
        self.addCleanup(shutil.rmtree, self.media, True)

    def call(self, method, url, data=None, token=TOKEN):
        headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"} if token else {}
        return getattr(self.client, method)(url, data=json.dumps(data) if data is not None else None,
                                            content_type="application/json", **headers)

    def post_data(self, **kw):
        base = {"title": "Hello Kenya", "excerpt": "A short summary", "body": "<p>Body text</p>", "category": "Web Development"}
        return {**base, **kw}

    # ---- posts
    def test_posts_require_the_token(self):
        for url in (reverse("api_posts"), reverse("api_portfolio")):
            self.assertEqual(self.call("get", url, token=None).status_code, 401)
            self.assertEqual(self.call("post", url, {}, token="nope").status_code, 401)

    def test_create_post_defaults_author_to_first_superuser_and_appears_on_blog(self):
        r = self.call("post", reverse("api_posts"), self.post_data())
        self.assertEqual(r.status_code, 201, r.content)
        out = r.json()
        self.assertEqual((out["slug"], out["author"], out["category"], out["status"]), ("hello-kenya", "boss", "Web Development", "published"))
        self.assertContains(self.client.get(reverse("blog:list")), "Hello Kenya")
        self.assertEqual(self.client.get(reverse("blog:detail", args=["hello-kenya"])).status_code, 200)

    def test_post_upsert_patch_and_delete(self):
        url = reverse("api_posts")
        self.call("post", url, self.post_data(slug="my-post"))
        r = self.call("post", url, self.post_data(slug="my-post", title="Changed"))
        self.assertEqual((r.status_code, r.json()["title"]), (200, "Changed"))
        item = reverse("api_post_item", args=["my-post"])
        self.assertEqual(self.call("patch", item, {"featured": True, "read_minutes": 9}).json()["read_minutes"], 9)
        self.assertEqual(self.call("put", item, {"title": "x"}).status_code, 422)  # PUT needs every required field
        self.assertEqual(self.call("patch", item, {"slug": "other"}).status_code, 422)
        self.assertEqual(self.call("delete", item).status_code, 200)
        self.assertEqual(self.call("get", item).status_code, 404)

    def test_drafts_are_hidden_until_published(self):
        self.call("post", reverse("api_posts"), self.post_data(slug="wip", status="draft"))
        self.assertEqual(len(self.call("get", reverse("api_posts")).json()["results"]), 0)
        self.assertEqual(len(self.call("get", reverse("api_posts") + "?all=1").json()["results"]), 1)
        self.assertNotContains(self.client.get(reverse("blog:list")), "Hello Kenya")
        self.call("patch", reverse("api_post_item", args=["wip"]), {"status": "published"})
        self.assertContains(self.client.get(reverse("blog:list")), "Hello Kenya")

    def test_explicit_author_and_validation(self):
        r = self.call("post", reverse("api_posts"), self.post_data(author="writer"))
        self.assertEqual(r.json()["author"], "writer")
        for bad in ({"author": "ghost"}, {"status": "live"}, {"excerpt": "x" * 321}, {"image_url": "javascript:x"},
                    {"published_at": "yesterday"}, {"read_minutes": 0}, {"featured": "yes"}, {"bogus": 1}):
            r = self.call("post", reverse("api_posts"), self.post_data(slug=f"t-{abs(hash(str(bad)))}", **bad))
            self.assertIn(r.status_code, (400, 422), bad)

    def test_script_content_is_refused(self):
        for body in ("<script>alert(1)</script>", '<img src=x onerror="alert(1)">', '<a href="javascript:alert(1)">x</a>',
                     "<iframe src='//evil'></iframe>", "<form action=/x></form>"):
            r = self.call("post", reverse("api_posts"), self.post_data(body=body))
            self.assertEqual(r.status_code, 422, body)
            self.assertIn("body", r.json()["fields"])
        ok = self.call("post", reverse("api_posts"), self.post_data(body='<p>Fine <a href="/contact/">link</a> and <code>code</code></p><div class="tbl"><table><tr><td>x</td></tr></table></div>'))
        self.assertEqual(ok.status_code, 201)

    def test_post_image_upload_and_replacement(self):
        r = self.call("post", reverse("api_posts"), self.post_data(slug="pic", image_base64=png_b64()))
        self.assertEqual(r.status_code, 201, r.content)
        first = r.json()["image"]
        self.assertTrue(first.endswith("pic.png") or "/pic" in first, first)
        from Blogs.models import Post
        p = Post.objects.get(slug="pic")
        self.assertTrue(p.image and p.image.size > 0)
        r2 = self.call("patch", reverse("api_post_item", args=["pic"]), {"image_base64": "data:image/jpeg;base64," + png_b64(fmt="JPEG")})
        self.assertEqual(r2.status_code, 200, r2.content)
        self.assertTrue(r2.json()["image"].endswith(".jpg"))

    def test_bad_images_are_refused(self):
        url = reverse("api_posts")
        garbage = base64.b64encode(b"<?php echo 1; ?>").decode()
        for bad, why in ((garbage, "not an image"), ("%%%notbase64", "bad base64"), (png_b64(fmt="GIF"), "gif not allowed")):
            r = self.call("post", url, self.post_data(slug="bad", image_base64=bad))
            self.assertEqual(r.status_code, 422, why)
            self.assertIn("image_base64", r.json()["fields"])
        from Blogs.models import Post
        self.assertFalse(Post.objects.filter(slug="bad").exists())

    # ---- portfolio
    def project(self, **kw):
        base = {"title": "Acme Store", "summary": "An online store for Acme", "category": "ecommerce",
                "technologies": ["Django", "PostgreSQL", "M-Pesa"], "completed_year": 2026,
                "project_url": "https://acme.example.com", "client_name": "Acme Ltd"}
        return {**base, **kw}

    def test_portfolio_create_update_and_public_pages(self):
        r = self.call("post", reverse("api_portfolio"), self.project(cover_image_base64=png_b64(), is_featured=True))
        self.assertEqual(r.status_code, 201, r.content)
        out = r.json()
        self.assertEqual((out["slug"], out["technologies"], out["completed_year"]), ("acme-store", ["Django", "PostgreSQL", "M-Pesa"], 2026))
        self.assertTrue(out["cover_image"])
        self.assertContains(self.client.get(reverse("portfolio")), "Acme Store")
        detail = self.client.get(reverse("portfolio_detail", args=["acme-store"]))
        self.assertEqual(detail.status_code, 200)
        r = self.call("post", reverse("api_portfolio"), self.project(summary="Updated summary"))
        self.assertEqual((r.status_code, r.json()["summary"]), (200, "Updated summary"))
        item = reverse("api_portfolio_item", args=["acme-store"])
        self.assertEqual(self.call("patch", item, {"is_active": False}).status_code, 200)
        _cache.clear()
        self.assertNotContains(self.client.get(reverse("portfolio")), "Acme Store")
        slugs = [p["slug"] for p in self.call("get", reverse("api_portfolio")).json()["results"]]
        self.assertNotIn("acme-store", slugs)  # hidden projects are left out of the default list
        self.assertEqual(self.call("delete", item).status_code, 200)

    def test_portfolio_validation(self):
        url = reverse("api_portfolio")
        for bad in ({"category": "pottery"}, {"completed_year": 1850}, {"completed_year": "2026"}, {"summary": "x" * 281},
                    {"project_url": "ftp://x"}, {"technologies": [1, 2]}, {"display_order": -1}, {"description": "<script>x</script>"}):
            r = self.call("post", url, self.project(slug=f"p-{abs(hash(str(bad)))}", **bad))
            self.assertEqual(r.status_code, 422, bad)
        self.assertEqual(self.call("post", url, {"title": "No summary"}).status_code, 422)
