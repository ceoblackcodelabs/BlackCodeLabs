"""
Cache invalidation for Home app.

The views cache marketing content (tech services, counters, reviews, pricing
plans, portfolio featured list) for CONTENT_CACHE_TTL. Without this, an admin
edit wouldn't show up on the live site until the cache entry expired. These
signals clear the relevant cache key the moment the underlying data changes,
so editors see updates immediately while everyone else still benefits from
the cache between edits.
"""
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import (
    TechServices, DataCounter, ClientReview,
    PricingPlan, PricingFeature, PricingFAQ,
    PortfolioProject,
)


def _clear(*keys):
    for key in keys:
        cache.delete(key)


@receiver([post_save, post_delete], sender=TechServices)
@receiver([post_save, post_delete], sender=DataCounter)
@receiver([post_save, post_delete], sender=ClientReview)
def clear_home_cache(sender, **kwargs):
    _clear("home_page_context")


@receiver([post_save, post_delete], sender=PricingPlan)
@receiver([post_save, post_delete], sender=PricingFeature)
@receiver([post_save, post_delete], sender=PricingFAQ)
def clear_pricing_cache(sender, **kwargs):
    _clear("pricing_page_context")


@receiver([post_save, post_delete], sender=PortfolioProject)
def clear_portfolio_cache(sender, **kwargs):
    _clear("portfolio_featured_projects")
