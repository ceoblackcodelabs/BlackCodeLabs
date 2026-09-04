from django.views.generic import TemplateView, ListView, DetailView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import (
    TechServices, DataCounter,
    ClientReview, Solution,
    PricingPlan, PricingFAQ,
    PortfolioProject,
)
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactForm
from .telegram_notify import notify_new_contact_inquiry
import json
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)

# Cache timeout for rarely-changing marketing content (tech services, pricing,
# reviews, portfolio, etc). Saved to cache under a fixed key so repeat page
# views skip the database entirely until the timeout expires or the admin
# edits the underlying data (see Home/signals.py for cache-busting on save).
CONTENT_CACHE_TTL = 60 * 15  # 15 minutes


# Full-response cache for pages that render the same HTML for every visitor
# (no per-user content, no CSRF-bearing forms). This skips the DB query +
# template render entirely for the ~5 minutes the cache is warm, on top of
# the low-level `cache.get/set` calls already used inside get_context_data
# — the two work together: this is what makes repeat homepage/portfolio/
# pricing hits nearly instant. Never applied to contact_view (its form
# embeds a per-session CSRF token that must stay fresh).
PAGE_CACHE_SECONDS = 60 * 5  # 5 minutes


@method_decorator(cache_page(PAGE_CACHE_SECONDS), name='dispatch')
class HomePageView(TemplateView):
    template_name = "Home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cached = cache.get("home_page_context")
        if cached is None:
            data_counter = DataCounter.objects.filter(is_active=True).first()
            if not data_counter:
                # Create a default counter if none exists
                data_counter = DataCounter.objects.create(
                    projects_delivered=1247,
                    systems_automated=892,
                    happy_clients=765,
                    returning_clients=423,
                    is_active=True
                )
            cached = {
                "tech_services": list(TechServices.objects.all()),
                "data_counters": data_counter,
                "client_reviews": list(ClientReview.objects.all()[:6]),
            }
            cache.set("home_page_context", cached, CONTENT_CACHE_TTL)

        context.update(cached)
        return context

@method_decorator(cache_page(PAGE_CACHE_SECONDS), name='dispatch')
class GamesPageView(TemplateView):
    template_name = "Home/games.html"

@method_decorator(cache_page(PAGE_CACHE_SECONDS), name='dispatch')
class Pricing(TemplateView):
    template_name = "Home/pricing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cached = cache.get("pricing_page_context")
        if cached is None:
            cached = {
                "plans": list(PricingPlan.objects.filter(is_active=True).prefetch_related('features')),
                "faqs": list(PricingFAQ.objects.filter(is_active=True)),
            }
            cache.set("pricing_page_context", cached, CONTENT_CACHE_TTL)
        context.update(cached)
        return context


@method_decorator(cache_page(PAGE_CACHE_SECONDS), name='dispatch')
class PortfolioPageView(ListView):
    model = PortfolioProject
    template_name = "Home/portfolio.html"
    context_object_name = "projects"
    paginate_by = 9

    def get_queryset(self):
        qs = PortfolioProject.objects.filter(is_active=True)
        category = self.request.GET.get('category')
        if category and category != 'all':
            qs = qs.filter(category=category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = PortfolioProject.CATEGORY_CHOICES
        context['active_category'] = self.request.GET.get('category', 'all')
        featured = cache.get("portfolio_featured_projects")
        if featured is None:
            featured = list(PortfolioProject.objects.filter(is_active=True, is_featured=True)[:3])
            cache.set("portfolio_featured_projects", featured, CONTENT_CACHE_TTL)
        context['featured_projects'] = featured
        return context


@method_decorator(cache_page(PAGE_CACHE_SECONDS), name='dispatch')
class PortfolioDetailView(DetailView):
    model = PortfolioProject
    template_name = "Home/portfolio_detail.html"
    context_object_name = "project"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return PortfolioProject.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_projects'] = PortfolioProject.objects.filter(
            is_active=True, category=self.object.category
        ).exclude(pk=self.object.pk)[:3]
        return context


@csrf_protect
def contact_view(request):
    """Handle contact form submissions"""

    # Initialize context
    context = {'active_page': 'contact'}

    if request.method == 'POST':
        # Create form with POST data
        form = ContactForm(request.POST)

        if form.is_valid():
            try:
                # Save the contact inquiry
                inquiry = form.save(commit=False)

                # Capture additional information
                inquiry.ip_address = get_client_ip(request)
                inquiry.user_agent = request.META.get('HTTP_USER_AGENT', '')
                inquiry.referrer = request.META.get('HTTP_REFERER', '')

                # Check for spam (simple check based on submission speed)
                if 'submission_time' in request.session:
                    previous_time = request.session['submission_time']
                    current_time = timezone.now().timestamp()
                    if current_time - previous_time < 5:  # Less than 5 seconds between submissions
                        inquiry.status = 'spam'
                        inquiry.priority = 1

                # Save to database
                inquiry.save()

                # Store submission time for spam detection
                request.session['submission_time'] = timezone.now().timestamp()

                # Send email notifications (optional - comment out if not configured)
                try:
                    send_contact_notification(inquiry)
                    send_auto_response(inquiry)
                except Exception as e:
                    logger.warning(f"Email sending failed: {e}")

                # Push an instant Telegram alert. This runs on a background
                # thread (see Home/telegram_notify.py) so a slow or
                # unreachable Telegram API can NEVER delay the response the
                # client sees below — they still get immediate feedback,
                # while the notification lands on Telegram a moment later.
                # Any failure is caught and written to logs/telegram.log,
                # never raised here.
                notify_new_contact_inquiry(inquiry)

                # Success message
                messages.success(
                    request,
                    'Thank you for your message! We have received your inquiry and '
                    'will get back to you within 24 hours.'
                )

                # Clear the form by creating a new instance
                form = ContactForm()

                # Add success flag to context
                context['form_submitted'] = True
                context['success'] = True

                logger.info(f"New contact inquiry from {inquiry.email} - IP: {inquiry.ip_address}")

                # You can either render the page with success message or redirect
                # Option 1: Render with success message (keeps form empty)
                context['form'] = form
                return render(request, 'Home/contact.html', context)

                # Option 2: Redirect to same page with success message
                # return redirect('contact')

            except Exception as e:
                logger.error(f"Error saving contact inquiry: {e}")
                messages.error(
                    request,
                    'There was an error submitting your form. Please try again.'
                )
        else:
            # Form has errors
            messages.error(
                request,
                'Please correct the errors in the form below.'
            )
    else:
        # GET request - create empty form
        form = ContactForm()

    # Add form to context for both GET and failed POST
    context['form'] = form

    return render(request, 'Home/contact.html', context)

def get_client_ip(request):
    """Get the client's IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def send_contact_notification(inquiry):
    """Send notification email to admin with better debugging"""

    # Check if email is configured
    if not hasattr(settings, 'EMAIL_BACKEND'):
        logger.info("EMAIL_BACKEND not configured - skipping email")
        return

    # If using console backend or SMTP is configured
    subject = f"New Contact Inquiry: {inquiry.subject}"
    message = f"""
    New contact inquiry received:

    Name: {inquiry.first_name} {inquiry.last_name}
    Email: {inquiry.email}
    Phone: {inquiry.phone or 'Not provided'}
    Company: {inquiry.company or 'Not provided'}
    Subject: {inquiry.subject}

    Message:
    {inquiry.message}

    Technical Information:
    IP Address: {inquiry.ip_address or 'Unknown'}
    User Agent: {inquiry.user_agent or 'Unknown'}
    Created: {inquiry.created_at.strftime('%Y-%m-%d %H:%M:%S')}

    You can view this inquiry in the admin panel.
    """

    try:
        # Determine recipient
        recipient_email = None
        if hasattr(settings, 'CONTACT_NOTIFICATION_EMAIL'):
            recipient_email = settings.CONTACT_NOTIFICATION_EMAIL
        elif hasattr(settings, 'EMAIL_HOST_USER'):
            recipient_email = settings.EMAIL_HOST_USER

        if not recipient_email:
            logger.info("No recipient email configured - skipping notification")
            return

        # Determine sender
        sender_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@blackcodelabs.com')

        logger.info(f"Attempting to send notification email to: {recipient_email}")

        send_mail(
            subject=subject,
            message=message,
            from_email=sender_email,
            recipient_list=[recipient_email],
            fail_silently=False,  # Set to True in production
        )

        logger.info(f"Notification email sent successfully to {recipient_email}")

    except Exception as e:
        logger.error(f"Failed to send contact notification email: {e}")
        # Don't raise the error - we don't want form submission to fail because of email

def send_auto_response(inquiry):
    """Send auto-response email to the user with better debugging"""
    if not inquiry.email:
        logger.info("No user email provided - skipping auto-response")
        return

    subject = f"We've received your inquiry: {inquiry.subject}"
    message = f"""
    Dear {inquiry.first_name},

    Thank you for contacting BlackCodeLabs. We have received your inquiry and our team will review it shortly.

    Inquiry Details:
    - Subject: {inquiry.subject}
    - Submitted: {inquiry.created_at.strftime('%Y-%m-%d %H:%M:%S')}

    Our team typically responds within 24 hours during business days. If you have urgent matters, please call our support line at +1 (555) 123-4567.

    Best regards,
    The BlackCodeLabs Team

    ---
    This is an automated response. Please do not reply to this email.
    """

    try:
        # Determine sender
        sender_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@blackcodelabs.com')

        logger.info(f"Attempting to send auto-response to user: {inquiry.email}")

        send_mail(
            subject=subject,
            message=message,
            from_email=sender_email,
            recipient_list=[inquiry.email],
            fail_silently=False,  # Set to True in production
        )

        logger.info(f"Auto-response email sent successfully to {inquiry.email}")

    except Exception as e:
        logger.error(f"Failed to send auto-response email: {e}")
        # Don't raise the error - we don't want form submission to fail because of email



@method_decorator(cache_page(PAGE_CACHE_SECONDS), name='dispatch')
class SolutionsPageView(ListView):
    model = Solution
    template_name = 'Home/solutions.html'
    context_object_name = 'solutions'

    def get_queryset(self):
        return Solution.objects.filter(is_active=True).order_by('display_order', 'title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context if needed
        return context

@method_decorator(cache_page(PAGE_CACHE_SECONDS), name='dispatch')
class SolutionDetailView(DetailView):
    model = Solution
    template_name = 'Home/solutions_detail.html'
    context_object_name = 'solution'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

# ---------------------------------------------------------------------------
# QR CODE GENERATOR
# ---------------------------------------------------------------------------
@method_decorator(cache_page(PAGE_CACHE_SECONDS), name='dispatch')
class QRGeneratorPageView(TemplateView):
    """Public page with a form to turn any URL/text into a downloadable QR code."""
    template_name = "Home/qr_generator.html"


def qr_code_image(request):
    """Generates a PNG QR code on the fly for ?data=<text or url> and streams it back.
    No text/url is stored — this is a stateless generator anyone can hit."""
    import io
    import qrcode
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
    from qrcode.image.styles.colormasks import SolidFillColorMask
    from django.http import HttpResponse

    data = request.GET.get('data', '').strip()
    if not data:
        return HttpResponseBadRequest("Missing 'data' parameter")
    if len(data) > 2000:
        return HttpResponseBadRequest("Data too long")

    try:
        size = int(request.GET.get('size', 10))
        size = max(4, min(size, 20))
    except (TypeError, ValueError):
        size = 10

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=size,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    try:
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            color_mask=SolidFillColorMask(front_color=(192, 57, 43), back_color=(255, 255, 255)),
        )
    except Exception:
        # Fallback to a plain black/white code if the styled renderer isn't available
        img = qr.make_image(fill_color="#c0392b", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type="image/png")
    download = request.GET.get('download')
    if download:
        response['Content-Disposition'] = 'attachment; filename="qrcode.png"'
    response['Cache-Control'] = 'no-store'
    return response


# ---------------------------------------------------------------------------
# ROBOTS.TXT
# ---------------------------------------------------------------------------
def robots_txt(request):
    from django.http import HttpResponse
    site_url = getattr(settings, 'SITE_URL', f"https://{request.get_host()}")
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        f"Sitemap: {site_url}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


# ---------------------------------------------------------------------------
# CUSTOM ERROR HANDLERS (registered as handler400/403/404/500 in urls.py)
# ---------------------------------------------------------------------------
def error_400(request, exception=None):
    from django.shortcuts import render
    return render(request, "errors/400.html", status=400)


def error_403(request, exception=None):
    from django.shortcuts import render
    return render(request, "errors/403.html", status=403)


def error_404(request, exception=None):
    from django.shortcuts import render
    return render(request, "errors/404.html", status=404)


def error_500(request):
    from django.shortcuts import render
    return render(request, "errors/500.html", status=500)


# ---------------------------------------------------------------------------
# /socials/ — Black Sheep (Odhiambo Churchill) personal portfolio page.
# Everything below is a plain Python list/dict so the page content can be
# edited in one place without touching the template. Update these as real
# products, partners, testimonials and numbers become available.
# ---------------------------------------------------------------------------
class SocialsPageView(TemplateView):
    template_name = "Home/socials.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Single source of truth for every social link on the page (floating
        # button overlay, footer, contact section, community pills). Add a
        # Google Reviews link, a new platform, etc. — it will show up
        # everywhere automatically.
        socials = [
            {"name": "Instagram", "abbr": "IG", "url": "https://instagram.com/b74ck5h33p"},
            {"name": "TikTok", "abbr": "TT", "url": "https://tiktok.com/@blackcodelab5"},
            {"name": "YouTube", "abbr": "YT", "url": "https://youtube.com/@Blackcodelab5"},
            {"name": "Facebook", "abbr": "FB", "url": "https://facebook.com/b74ck5h33p"},
            {"name": "LinkedIn", "abbr": "LI", "url": "https://linkedin.com/in/odhiambo-churchill"},
            {"name": "GitHub", "abbr": "GH", "url": "https://github.com/ceoblackcodelabs"},
            {"name": "WhatsApp", "abbr": "WA", "url": "https://wa.me/254799804185"},
            {"name": "Google Reviews", "abbr": "★", "url": "https://g.page/r/CVeAWbmwdPZoEBI/review"},
        ]

        services = [
            {"num": "01", "title": "Full-Stack Development", "desc": "Building complete web and mobile products end-to-end — Django and React Native backends, polished production-ready interfaces."},
            {"num": "02", "title": "Penetration Testing", "desc": "Probing systems and applications for vulnerabilities before attackers do, with clear, actionable security reports."},
            {"num": "03", "title": "Entrepreneurship", "desc": "Spotting opportunity, building ventures from the ground up, and owning the outcome."},
            {"num": "04", "title": "Events Management", "desc": "Planning and coordinating events end-to-end, from concept to flawless execution on the day."},
            {"num": "05", "title": "Philanthropy", "desc": "Giving back through community-focused initiatives and support for causes that matter."},
            {"num": "06", "title": "Brand Building", "desc": "Shaping identity, voice, and presence for people and businesses who want to stand out from the herd."},
            {"num": "07", "title": "Social Media Management", "desc": "Growing and managing social presence with content, strategy, and consistency."},
            {"num": "08", "title": "Automation", "desc": "Designing scripts and systems that remove repetitive work and let people and businesses run leaner."},
            {"num": "09", "title": "CCTV Installation", "desc": "Planning and installing surveillance systems that keep homes and businesses secure."},
        ]

        # Rotating hero tagline — cycles through these under the "BLACK SHEEP" title.
        hero_taglines = [
            "Full-Stack Development.",
            "Penetration Testing.",
            "Automation & Systems.",
            "Brand Building.",
            "Different, By Design.",
        ]

        # Stats marquee under the hero. Swap in real figures once you're tracking them.
        stats = [
            {"num": "09", "label": "Core Services"},
            {"num": "01", "label": "One-Person Team"},
            {"num": "100%", "label": "Hands-On"},
            {"num": "24/7", "label": "Automation Mindset"},
            {"num": "Nairobi", "label": "Based In"},
        ]

        # "My Impact" counters. Kept modest/true by default — replace with
        # real project/client counts as you start tracking them.
        impact_numbers = [
            {"count": 9, "suffix": "", "label": "Core Services", "desc": "From full-stack development to CCTV installation — one person, many disciplines."},
            {"count": 100, "suffix": "%", "label": "Hands-On", "desc": "Every project built, secured and shipped personally — no outsourcing shortcuts."},
            {"count": 1, "suffix": "", "label": "One-Person Team", "desc": "A single point of contact from first call to final delivery."},
            {"count": 24, "suffix": "/7", "label": "Automation Mindset", "desc": "Always looking for the repetitive task worth scripting away."},
        ]

        # Leave empty until real products are ready to sell — the merch
        # section shows a friendly placeholder automatically when this is empty.
        merch_products = []
        # Example of how to add one later:
        # merch_products = [{"name": "Black Sheep Tee", "price": "KSh 1,500", "image": "", "badge": "New"}]

        # Leave empty until you have real partner/collab logos — placeholder
        # cells are shown automatically when this is empty.
        collab_partners = []

        # Placeholder testimonials — replace with real client quotes as you collect them.
        testimonials = [
            {"text": "Black Sheep rebuilt our platform from the ground up and tightened up security we didn't even know was weak. Fast, thorough, and easy to work with.", "name": "Client Name", "role": "Founder, Company"},
            {"text": "Automated a process that used to eat half our week. It just runs now — exactly what we needed.", "name": "Client Name", "role": "Operations Lead, Company"},
            {"text": "Sharp technical work paired with real brand thinking. Rare combination.", "name": "Client Name", "role": "Marketing Lead, Company"},
        ]

        context.update({
            "socials": socials,
            "services": services,
            "hero_taglines": hero_taglines,
            "hero_taglines_json": json.dumps(hero_taglines),
            "stats": stats,
            "impact_numbers": impact_numbers,
            "merch_products": merch_products,
            "collab_partners": collab_partners,
            "testimonials": testimonials,
            "total_reach": 0,
        })
        return context
