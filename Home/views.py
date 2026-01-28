from django.views.generic import TemplateView, ListView
from django.contrib import messages
from .models import (
    TechServices, TeamMember, DataCounter,
    ClientReview, ContactInquiry
)
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
import logging
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect

logger = logging.getLogger(__name__)

class HomePageView(ListView):
    template_name = "Home/index.html"
    model = TechServices
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tech_services'] = TechServices.objects.all()
        context['team_members'] = TeamMember.objects.all()
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
        context['data_counters'] = data_counter
        context["client_reviews"] = ClientReview.objects.all()[:6]
        return context
    
class AboutPageView(TemplateView):
    template_name = "Home/about.html"

class ContactPageView(TemplateView):
    template_name = "Home/contact.html"
    
class TechPageView(TemplateView):
    template_name = "Home/tech.html"
    
class SolutionsPageView(TemplateView):
    template_name = "Home/solutions.html"
    
class CoursesPageView(TemplateView):
    template_name = "Home/courses.html"
    
class CareersPageView(TemplateView):
    template_name = "Home/careers.html"
    
class BlogPageView(TemplateView):
    template_name = "Home/blog.html"
    
class GamesPageView(TemplateView):
    template_name = "Home/games.html"
    
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
    Department: {inquiry.get_department_display()}
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
    - Department: {inquiry.get_department_display()}
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

class DemoPageView(TemplateView):
    template_name = "Home/demo.html"