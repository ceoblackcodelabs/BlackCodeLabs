from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Solution, PortfolioProject


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return [
            "home", "solutions", "pricing", "portfolio",
            "affiliate", "contact", "qr_generator",
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == "home" else 0.7


class SolutionSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Solution.objects.filter(is_active=True)

    def location(self, obj):
        return reverse("solution_detail", kwargs={"slug": obj.slug})

    def lastmod(self, obj):
        return getattr(obj, "updated_at", None)


class PortfolioSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return PortfolioProject.objects.filter(is_active=True)

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.updated_at


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        try:
            from Blogs.models import Post
            return Post.objects.filter(status="published")
        except Exception:
            return []

    def location(self, obj):
        return reverse("blog:detail", kwargs={"slug": obj.slug})

    def lastmod(self, obj):
        return obj.published_at


sitemaps = {
    "static": StaticViewSitemap,
    "solutions": SolutionSitemap,
    "portfolio": PortfolioSitemap,
    "blog": BlogSitemap,
}
