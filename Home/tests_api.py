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
