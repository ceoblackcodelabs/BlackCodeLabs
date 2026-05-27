# """
# core/views.py

# All class-based views for the core / homepage functionality.
# """

from django.views.generic import TemplateView, DetailView, ListView
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page

# from .models import (
#     SiteSettings,
#     HeroContent,
#     PerspectiveSection,
#     Service,
#     SocialStat,
# )
# from .models import MerchItem
# # from .models import Testimonial
# # from .models import Collaborator


# # ─── Homepage ─────────────────────────────────────────────────────────────────

# @method_decorator(cache_page(60 * 5), name='dispatch')   # cache 5 minutes
# class HomeView(TemplateView):
#     """
#     Renders the single-page marketing site.
#     Aggregates data from every app into one template context.
#     """

#     template_name = 'core/home.html'

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)

#         # Singletons
#         ctx['hero']        = HeroContent.load()
#         ctx['perspective'] = PerspectiveSection.load()

#         # Merchandise — only published items, up to 6
#         # ctx['merch_items'] = (
#         #     MerchItem.objects
#         #     .filter(is_published=True)
#         #     .order_by('order')[:6]
#         # )

#         # Services / What We Do — active, ordered
#         ctx['services'] = Service.objects.filter(is_active=True)

#         # Testimonials — featured ones first, then by order
#         # ctx['testimonials'] = (
#         #     Testimonial.objects
#         #     .filter(is_active=True)
#         #     .order_by('-is_featured', 'order')
#         # )

#         # Community stats (marquee)
#         ctx['social_stats'] = SocialStat.objects.filter(show_in_marquee=True)

#         # The one stat that powers the animated counter
#         ctx['community_stat'] = (
#             SocialStat.objects
#             .filter(show_in_community=True)
#             .first()
#         )

#         # Collaborators / logos
#         # ctx['collaborators'] = (
#         #     Collaborator.objects
#         #     .filter(is_active=True)
#         #     .order_by('order')
#         # )

#         return ctx


# # ─── Service Detail ───────────────────────────────────────────────────────────

# class ServiceDetailView(DetailView):
#     """
#     Optional detail page for a single service.
#     Reached via /service/<pk>/ or linked from the What We Do grid.
#     """

#     model               = Service
#     template_name       = 'core/service_detail.html'
#     context_object_name = 'service'
#     queryset            = Service.objects.filter(is_active=True)


# # ─── Service List ─────────────────────────────────────────────────────────────

# class ServiceListView(ListView):
#     """Standalone page listing all services (useful for SEO / sharing)."""

#     model               = Service
#     template_name       = 'core/service_list.html'
#     context_object_name = 'services'
#     queryset            = Service.objects.filter(is_active=True)

class landing(TemplateView):
    template_name = "BCL/index.html"