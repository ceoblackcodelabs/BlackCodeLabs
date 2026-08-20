from django.conf import settings


def site_meta(request):
    """Makes site-wide SEO/identity settings available in every template
    (base templates, error pages, blog, affiliate, etc.) without importing
    settings directly in each view."""
    return {
        "SITE_URL": settings.SITE_URL,
        "SITE_DOMAIN": settings.SITE_DOMAIN,
        "SITE_NAME": settings.SITE_NAME,
        "GOOGLE_SITE_VERIFICATION": settings.GOOGLE_SITE_VERIFICATION,
        "BING_SITE_VERIFICATION": settings.BING_SITE_VERIFICATION,
        "WHATSAPP_NUMBER": settings.WHATSAPP_NUMBER,
    }
