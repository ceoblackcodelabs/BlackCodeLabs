import json
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from .models import AffiliateApplication

logger = logging.getLogger(__name__)


class AffiliateView(TemplateView):
    template_name = "Affiliates/affiliate.html"


def _client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    return xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR')


@csrf_protect
@require_POST
def affiliate_apply(request):
    """Handles the affiliate signup form via fetch(). Returns JSON so the page
    can show a success/error state without a full reload."""
    try:
        if request.content_type == 'application/json':
            payload = json.loads(request.body or '{}')
        else:
            payload = request.POST

        full_name = (payload.get('full_name') or '').strip()
        email = (payload.get('email') or '').strip()

        if not full_name or not email:
            return JsonResponse(
                {'success': False, 'error': 'Name and email are required.'}, status=400
            )

        AffiliateApplication.objects.create(
            full_name=full_name,
            email=email,
            phone=(payload.get('phone') or '').strip(),
            website_or_social=(payload.get('website_or_social') or '').strip(),
            audience_size=(payload.get('audience_size') or '').strip(),
            promotion_channels=(payload.get('promotion_channels') or '').strip(),
            strategy=(payload.get('strategy') or '').strip(),
            ip_address=_client_ip(request),
        )
        return JsonResponse({'success': True})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid request format.'}, status=400)
    except Exception as e:
        logger.error(f"Affiliate application failed: {e}")
        return JsonResponse({'success': False, 'error': 'Something went wrong. Please try again.'}, status=500)
