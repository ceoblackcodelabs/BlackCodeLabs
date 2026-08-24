"""
Cache invalidation for the Blogs app.

The blog list/detail views cache the category list (with post counts) and
list-page stats for BLOG_CACHE_TTL. These signals clear those cache keys the
moment a Post or Category changes, so a newly published post or a renamed
category shows up immediately instead of waiting out the TTL.
"""
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver

from .models import Post, Category


def _clear(*keys):
    for key in keys:
        cache.delete(key)


@receiver([post_save, post_delete], sender=Post)
def clear_post_caches(sender, **kwargs):
    _clear("blog_categories_with_counts", "blog_list_stats")


@receiver([post_save, post_delete], sender=Category)
def clear_category_caches(sender, **kwargs):
    _clear("blog_categories_with_counts", "blog_list_stats")
