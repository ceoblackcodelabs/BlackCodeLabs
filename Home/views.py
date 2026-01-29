from django.views.generic import TemplateView, ListView, DetailView, View
from django.urls import reverse_lazy
from django.contrib import messages
from .models import (
    TechServices, TeamMember, DataCounter,
    ClientReview, ContactInquiry, DemoBooking,
    Solution, Course, CourseStat,
    CourseEnrollment
)
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactForm, DemoBookingForm, CourseEnrollmentForm
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
    
@method_decorator(csrf_protect, name='dispatch')
class DemoBookingView(FormView):
    template_name = 'Home/demo.html'
    form_class = DemoBookingForm
    success_url = reverse_lazy('demo')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'demo'
        
        # Add tomorrow's date for the form
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        context['tomorrow_date'] = tomorrow.strftime('%Y-%m-%d')
        
        return context
    
    def form_valid(self, form):
        try:
            # Save the demo booking
            demo_booking = form.save(commit=False)
            
            # Add technical information
            demo_booking.ip_address = self.get_client_ip()
            demo_booking.user_agent = self.request.META.get('HTTP_USER_AGENT', '')
            demo_booking.referrer = self.request.META.get('HTTP_REFERER', '')
            
            # Save to database
            demo_booking.save()
            
            # Store submission time for spam detection
            self.request.session['demo_submission_time'] = timezone.now().timestamp()
            
            # Send email notifications
            try:
                self.send_admin_notification(demo_booking)
                self.send_user_confirmation(demo_booking)
            except Exception as e:
                logger.warning(f"Email sending failed: {e}")
            
            # Success message
            messages.success(
                self.request,
                f'Your demo has been scheduled for {demo_booking.formatted_datetime()}! '
                f'Confirmation has been sent to {demo_booking.email}.'
            )
            
            logger.info(f"New demo booking from {demo_booking.email} - Booking ID: {demo_booking.booking_id}")
            
            return super().form_valid(form)
            
        except Exception as e:
            logger.error(f"Error saving demo booking: {e}")
            messages.error(
                self.request,
                'There was an error scheduling your demo. Please try again.'
            )
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            'Please correct the errors in the form below.'
        )
        return super().form_invalid(form)
    
    def get_client_ip(self):
        """Get the client's IP address"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip
    
    def send_admin_notification(self, demo_booking):
        """Send notification email to admin"""
        if not hasattr(settings, 'EMAIL_BACKEND'):
            return
        
        subject = f"New Demo Booking: {demo_booking.demo_title}"
        message = f"""
        New demo booking received:
        
        Contact Information:
        - Name: {demo_booking.full_name()}
        - Email: {demo_booking.email}
        - Company: {demo_booking.company}
        - Job Title: {demo_booking.job_title}
        
        Demo Details:
        - Title: {demo_booking.demo_title}
        - Date: {demo_booking.formatted_date()}
        - Time: {demo_booking.formatted_time()}
        - Service: {demo_booking.get_service_type_display() or 'Not specified'}
        - Attendees: {demo_booking.number_of_attendees}
        
        Message:
        {demo_booking.demo_message or 'No additional message'}
        
        Technical Information:
        - Booking ID: {demo_booking.booking_id}
        - IP Address: {demo_booking.ip_address or 'Unknown'}
        - User Agent: {demo_booking.user_agent or 'Unknown'}
        
        Status: {demo_booking.get_status_display()}
        
        View in admin: {self.request.build_absolute_uri(reverse_lazy('admin:Home_demobooking_change', args=[demo_booking.id]))}
        """
        
        recipient_email = getattr(settings, 'DEMO_NOTIFICATION_EMAIL', 
                                getattr(settings, 'CONTACT_NOTIFICATION_EMAIL', 
                                      getattr(settings, 'EMAIL_HOST_USER', None)))
        
        if recipient_email:
            send_mail(
                subject=subject,
                message=message,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@blackcodelabs.com'),
                recipient_list=[recipient_email],
                fail_silently=True,
            )
            logger.info(f"Demo notification sent to {recipient_email}")
    
    def send_user_confirmation(self, demo_booking):
        """Send confirmation email to user"""
        if not demo_booking.email:
            return
        
        subject = f"Demo Confirmation: {demo_booking.demo_title}"
        message = f"""
        Dear {demo_booking.first_name},
        
        Thank you for scheduling a demo with BlackCodeLabs! Your booking has been confirmed.
        
        Demo Details:
        - Title: {demo_booking.demo_title}
        - Date: {demo_booking.formatted_date()}
        - Time: {demo_booking.formatted_time()} EST
        - Duration: 45 minutes
        
        Booking ID: {demo_booking.booking_id}
        
        What to Expect:
        1. Our team will review your requirements and send any preparation materials within 1 business day.
        2. You'll receive a calendar invitation with the meeting link 24 hours before your scheduled time.
        3. The demo will be conducted via {demo_booking.get_meeting_platform_display()}.
        
        Need to make changes?
        - Reply to this email for any modifications or questions
        - Reschedule up to 4 hours before your demo time
        
        We look forward to showing you how our solutions can transform your business!
        
        Best regards,
        The BlackCodeLabs Team
        
        ---
        This is an automated confirmation. Please do not reply to this email.
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@blackcodelabs.com'),
            recipient_list=[demo_booking.email],
            fail_silently=True,
        )
        logger.info(f"Demo confirmation sent to {demo_booking.email}")
        
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

class SolutionDetailView(DetailView):
    model = Solution
    template_name = 'solutions_detail.html' 
    context_object_name = 'solution'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
class CoursesPageView(View):
    """Handle both GET and POST requests for courses page."""
    
    template_name = 'Home/courses.html'
    
    def get(self, request):
        """Handle GET request - display courses page."""
        # Get all active courses
        courses = Course.objects.filter(is_active=True).order_by('display_order', '-created_at')
        
        # Get course statistics
        stats, _ = CourseStat.objects.get_or_create(id=1)
        
        # Prepare course data for JavaScript
        courses_data = [
            {
                'id': course.id,
                'title': course.title,
                'category': course.category,
                'level': course.level,
                'badge': course.badge,
                'icon': course.icon_class,
                'description': course.short_description,
                'duration': course.duration,
                'lessons': course.lessons,
                'students': str(course.students_enrolled),
                'rating': str(course.rating),
                'instructor': course.instructor_name,
                'price': float(course.price),
                'originalPrice': float(course.original_price) if course.original_price else None,
                'color': course.color,
                'details': course.get_details_dict(),
                'curriculum': course.get_curriculum_list(),
            }
            for course in courses
        ]
        
        context = {
            'courses': courses,
            'courses_json': json.dumps(courses_data, cls=DjangoJSONEncoder),
            'stats': stats,
            'categories': Course.CATEGORY_CHOICES,
            'levels': Course.LEVEL_CHOICES,
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        """Handle POST request - process course enrollment."""
        course_id = request.POST.get('course_id')
        
        if not course_id:
            return HttpResponseBadRequest("Course ID is required")
        
        course = get_object_or_404(Course, id=course_id, is_active=True)
        
        # Create form with POST data
        form = CourseEnrollmentForm(request.POST)
        
        if form.is_valid():
            try:
                # Check for existing enrollment
                existing_enrollment = CourseEnrollment.objects.filter(
                    email=form.cleaned_data['email'],
                    course=course,
                    is_active=True
                ).exists()
                
                if existing_enrollment:
                    messages.warning(
                        request, 
                        f"You are already enrolled in {course.title}. Check your email for details."
                    )
                    return redirect('courses')
                
                # Create enrollment
                enrollment = form.save(commit=False)
                enrollment.course = course
                enrollment.total_amount = enrollment.calculate_total_amount()
                
                # If user is authenticated, link to user account
                if request.user.is_authenticated:
                    enrollment.student = request.user
                
                enrollment.save()
                
                # Update course student count
                course.students_enrolled += 1
                course.save()
                
                # Update global stats
                stats, _ = CourseStat.objects.get_or_create(id=1)
                stats.total_students += 1
                stats.save()
                
                messages.success(
                    request,
                    f"Thank you {enrollment.first_name}! Your enrollment in '{course.title}' has been submitted. "
                    f"We'll contact you shortly with payment details."
                )
                
                # In production, you would:
                # 1. Send confirmation email
                # 2. Process payment
                # 3. Redirect to payment gateway
                
                return redirect('courses')
                
            except Exception as e:
                messages.error(
                    request,
                    f"An error occurred during enrollment: {str(e)}. Please try again."
                )
                return redirect('courses')
        else:
            # Form is invalid, show errors
            messages.error(
                request,
                "Please correct the errors below and try again."
            )
            
            # Re-render the page with form errors
            courses = Course.objects.filter(is_active=True).order_by('display_order', '-created_at')
            stats, _ = CourseStat.objects.get_or_create(id=1)
            
            courses_data = [
                {
                    'id': course.id,
                    'title': course.title,
                    'category': course.category,
                    'level': course.level,
                    'badge': course.badge,
                    'icon': course.icon_class,
                    'description': course.short_description,
                    'duration': course.duration,
                    'lessons': course.lessons,
                    'students': str(course.students_enrolled),
                    'rating': str(course.rating),
                    'instructor': course.instructor_name,
                    'price': float(course.price),
                    'originalPrice': float(course.original_price) if course.original_price else None,
                    'color': course.color,
                    'details': course.get_details_dict(),
                    'curriculum': course.get_curriculum_list(),
                }
                for course in courses
            ]
            
            context = {
                'courses': courses,
                'courses_json': json.dumps(courses_data, cls=DjangoJSONEncoder),
                'stats': stats,
                'categories': Course.CATEGORY_CHOICES,
                'levels': Course.LEVEL_CHOICES,
                'enrollment_form': form,
                'selected_course_id': course_id,
            }
            
            return render(request, self.template_name, context)


@method_decorator(csrf_exempt, name='dispatch')
class CourseEnrollmentAPIView(View):
    """API endpoint for course enrollment (for AJAX calls)."""
    
    def post(self, request):
        """Handle AJAX enrollment requests."""
        try:
            data = json.loads(request.body)
            course_id = data.get('course_id')
            
            if not course_id:
                return JsonResponse({'success': False, 'error': 'Course ID is required'})
            
            course = get_object_or_404(Course, id=course_id, is_active=True)
            
            # Create enrollment
            enrollment_data = {
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
                'email': data.get('email'),
                'phone': data.get('phone'),
                'country': data.get('country'),
                'experience_level': data.get('experience'),
                'learning_goals': data.get('goals'),
            }
            
            form = CourseEnrollmentForm(enrollment_data)
            
            if form.is_valid():
                # Check for existing enrollment
                existing = CourseEnrollment.objects.filter(
                    email=form.cleaned_data['email'],
                    course=course,
                    is_active=True
                ).exists()
                
                if existing:
                    return JsonResponse({
                        'success': False,
                        'error': f'You are already enrolled in {course.title}'
                    })
                
                enrollment = form.save(commit=False)
                enrollment.course = course
                
                if request.user.is_authenticated:
                    enrollment.student = request.user
                
                enrollment.save()
                
                # Update stats
                course.students_enrolled += 1
                course.save()
                
                stats, _ = CourseStat.objects.get_or_create(id=1)
                stats.total_students += 1
                stats.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Enrollment successful! We will contact you soon.',
                    'enrollment_id': enrollment.id
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Please check your form data',
                    'errors': form.errors
                })
                
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


class CourseDetailView(View):
    """View for individual course details."""
    
    template_name = 'course_detail.html'
    
    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug, is_active=True)
        
        context = {
            'course': course,
            'enrollment_form': CourseEnrollmentForm(),
        }
        
        return render(request, self.template_name, context)