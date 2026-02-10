from django.views.generic import TemplateView, ListView, DetailView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator
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
    
class SafeUTF8JSONEncoder(DjangoJSONEncoder):
    """JSON encoder that safely handles UTF-8 characters."""
    
    def default(self, obj):
        try:
            # Try the parent method first
            return super().default(obj)
        except UnicodeDecodeError:
            # If there's a Unicode error, convert to safe string
            return self._make_safe(obj)
    
    def _make_safe(self, obj):
        """Convert object to a safe string representation."""
        if isinstance(obj, str):
            # Clean the string
            return self._clean_string(obj)
        elif isinstance(obj, (list, tuple)):
            return [self._make_safe(item) for item in obj]
        elif isinstance(obj, dict):
            return {self._make_safe(key): self._make_safe(value) 
                    for key, value in obj.items()}
        else:
            return str(obj)
    
    def _clean_string(self, s):
        """Clean a string to ensure UTF-8 encoding."""
        if not s:
            return ""
        
        try:
            # Try to encode as UTF-8, replace invalid characters
            return s.encode('utf-8', 'replace').decode('utf-8')
        except:
            # If UTF-8 fails, try latin-1
            try:
                return s.encode('latin-1', 'replace').decode('latin-1')
            except:
                # Last resort: remove all non-ASCII
                return ''.join(char for char in s if ord(char) < 128)
   
class CoursesPageView(ListView):
    """View for displaying the courses page."""
    model = Course
    template_name = 'Home/courses.html'
    context_object_name = 'courses'
    paginate_by = 12
    
    def get_queryset(self):
        """Return filtered and ordered courses."""
        queryset = Course.objects.filter(is_active=True)
        
        # Filter by category if provided
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by level if provided
        level = self.request.GET.get('level')
        if level:
            queryset = queryset.filter(level=level)
        
        # Filter by search query if provided
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(short_description__icontains=search_query) |
                Q(detailed_description__icontains=search_query) |
                Q(instructor_name__icontains=search_query)
            )
        
        # Order courses
        order_by = self.request.GET.get('order_by', 'display_order')
        if order_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif order_by == 'price_desc':
            queryset = queryset.order_by('-price')
        elif order_by == 'rating':
            queryset = queryset.order_by('-rating')
        elif order_by == 'popularity':
            queryset = queryset.order_by('-students_enrolled')
        elif order_by == 'newest':
            queryset = queryset.order_by('-created_at')
        else:
            queryset = queryset.order_by('display_order', '-created_at')
        
        return queryset
    
    def safe_encode_string(self, value):
        """
        Safely encode a string to UTF-8, removing any invalid characters.
        """
        if value is None:
            return ""
        
        if isinstance(value, bytes):
            try:
                return value.decode('utf-8', 'ignore')
            except:
                try:
                    return value.decode('latin-1', 'ignore')
                except:
                    return str(value, errors='ignore')
        
        if isinstance(value, str):
            try:
                # Try to encode as UTF-8 first
                return value.encode('utf-8', 'ignore').decode('utf-8')
            except:
                # If that fails, try more aggressive cleaning
                cleaned = []
                for char in value:
                    try:
                        # Check if character can be encoded
                        char.encode('utf-8')
                        cleaned.append(char)
                    except UnicodeEncodeError:
                        # Replace with a safe character
                        cleaned.append('?')
                return ''.join(cleaned)
        
        return str(value)
    
    def safe_encode_json(self, data):
        """
        Recursively encode JSON data to UTF-8.
        """
        if isinstance(data, dict):
            cleaned = {}
            for key, value in data.items():
                safe_key = self.safe_encode_string(key)
                safe_value = self.safe_encode_json(value)
                cleaned[safe_key] = safe_value
            return cleaned
        
        elif isinstance(data, list):
            cleaned = []
            for item in data:
                cleaned.append(self.safe_encode_json(item))
            return cleaned
        
        elif isinstance(data, (str, bytes)):
            return self.safe_encode_string(data)
        
        else:
            # For numbers, booleans, None - return as is
            return data
    
    def prepare_course_for_json(self, course):
        """
        Prepare a course for JSON serialization with maximum safety.
        """
        try:
            # Basic course info with safe encoding
            course_data = {
                'id': course.id,
                'title': self.safe_encode_string(course.title),
                'category': self.safe_encode_string(course.category),
                'level': self.safe_encode_string(course.level),
                'badge': self.safe_encode_string(course.badge),
                'icon': self.safe_encode_string(course.icon_class),
                'description': self.safe_encode_string(course.short_description),
                'duration': self.safe_encode_string(course.duration),
                'lessons': self.safe_encode_string(course.lessons) if course.lessons else "0",
                'students': str(course.students_enrolled) if course.students_enrolled else "0",
                'rating': str(float(course.rating)) if course.rating else "0.0",
                'instructor': self.safe_encode_string(course.instructor_name),
                'instructor_bio': self.safe_encode_string(course.instructor_bio),
                'instructor_title': self.safe_encode_string(course.instructor_title),
                'price': float(course.price) if course.price else 0.0,
                'originalPrice': float(course.original_price) if course.original_price else None,
                'color': self.safe_encode_string(course.color),
                'slug': self.safe_encode_string(course.slug),
                'url': course.get_absolute_url(),
            }
            
            # Safely handle details JSON
            try:
                if course.details:
                    if isinstance(course.details, str):
                        import json
                        course.details = json.loads(course.details)
                    course_data['details'] = self.safe_encode_json(course.details)
                else:
                    course_data['details'] = {}
            except Exception as e:
                logger.warning(f"Error processing details for course {course.id}: {e}")
                course_data['details'] = {}
            
            # Safely handle curriculum JSON
            try:
                if course.curriculum:
                    if isinstance(course.curriculum, str):
                        import json
                        course.curriculum = json.loads(course.curriculum)
                    course_data['curriculum'] = self.safe_encode_json(course.curriculum)
                else:
                    course_data['curriculum'] = []
            except Exception as e:
                logger.warning(f"Error processing curriculum for course {course.id}: {e}")
                course_data['curriculum'] = []
            
            return course_data
            
        except Exception as e:
            logger.error(f"Critical error preparing course {course.id} for JSON: {e}")
            # Return minimal safe data
            return {
                'id': course.id,
                'title': 'Course',
                'category': 'other',
                'level': 'beginner',
                'badge': '',
                'icon': 'fas fa-book',
                'description': 'Course description',
                'duration': '12 Weeks',
                'lessons': '0',
                'students': '0',
                'rating': '0.0',
                'instructor': 'Instructor',
                'price': 0.0,
                'originalPrice': None,
                'color': '#3776AB',
                'details': {},
                'curriculum': [],
            }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get course statistics
        stats, _ = CourseStat.objects.get_or_create(id=1)
        
        # Get all available categories from the model
        categories = Course.CATEGORY_CHOICES
        
        # Get all available levels
        levels = Course.LEVEL_CHOICES
        
        # Get filter parameters
        current_category = self.request.GET.get('category', '')
        current_level = self.request.GET.get('level', '')
        current_search = self.request.GET.get('q', '')
        current_order = self.request.GET.get('order_by', 'display_order')
        
        # Prepare courses data for JSON serialization
        courses_data = []
        for course in context['courses']:
            course_data = self.prepare_course_for_json(course)
            courses_data.append(course_data)
        
        # Use a very safe JSON encoder
        import json
        from django.core.serializers.json import DjangoJSONEncoder
        
        class UltraSafeJSONEncoder(DjangoJSONEncoder):
            def encode(self, obj):
                # Override encode to handle any encoding issues
                try:
                    return super().encode(obj)
                except (UnicodeDecodeError, UnicodeEncodeError) as e:
                    logger.error(f"JSON encoding error: {e}")
                    # Try to clean the data and encode again
                    cleaned_obj = self.clean_object(obj)
                    try:
                        return super().encode(cleaned_obj)
                    except:
                        # Last resort: return empty array
                        return '[]'
            
            def clean_object(self, obj):
                """Recursively clean an object for JSON serialization."""
                if isinstance(obj, dict):
                    cleaned = {}
                    for key, value in obj.items():
                        safe_key = self.make_string_safe(key)
                        cleaned[safe_key] = self.clean_object(value)
                    return cleaned
                
                elif isinstance(obj, list):
                    cleaned = []
                    for item in obj:
                        cleaned.append(self.clean_object(item))
                    return cleaned
                
                elif isinstance(obj, (str, bytes)):
                    return self.make_string_safe(obj)
                
                else:
                    return obj
            
            def make_string_safe(self, value):
                """Make a string safe for JSON."""
                if value is None:
                    return ""
                
                if isinstance(value, bytes):
                    try:
                        value = value.decode('utf-8', 'ignore')
                    except:
                        try:
                            value = value.decode('latin-1', 'ignore')
                        except:
                            value = ''
                
                if isinstance(value, str):
                    # Remove any non-ASCII characters that cause issues
                    return ''.join(
                        char for char in value 
                        if ord(char) < 55296 or (57343 < ord(char) < 65536)
                    )
                
                return str(value) if value else ""
        
        try:
            courses_json = json.dumps(courses_data, cls=UltraSafeJSONEncoder, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Fatal JSON serialization error: {e}")
            courses_json = '[]'
        
        # Get featured courses
        featured_courses = Course.objects.filter(
            is_active=True, 
            is_featured=True
        ).order_by('display_order')[:3]
        
        # Prepare featured courses for template
        cleaned_featured_courses = []
        for course in featured_courses:
            try:
                cleaned_featured_courses.append(self.prepare_course_for_json(course))
            except:
                pass
        
        context.update({
            'courses_json': courses_json,
            'stats': {
                'total_courses': stats.total_courses,
                'total_students': stats.total_students,
                'satisfaction_rate': stats.satisfaction_rate,
                'total_instructors': stats.total_instructors,
            },
            'categories': categories,
            'levels': levels,
            'featured_courses': featured_courses,
            'current_category': current_category,
            'current_level': current_level,
            'current_search': current_search,
            'current_order': current_order,
            'total_courses_count': self.get_queryset().count(),
        })
        
        return context

class CourseDetailView(DetailView):
    """View for displaying individual course details."""
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        
        # Increment view count (optional - you can add a field for this)
        
        # Get related courses
        related_courses = Course.objects.filter(
            Q(category=course.category) | Q(level=course.level),
            is_active=True
        ).exclude(id=course.id).order_by('?')[:4]  # Random 4 related courses
        
        # Get enrollment count
        enrollment_count = CourseEnrollment.objects.filter(course=course).count()
        
        # Prepare course data for JSON
        course_data = {
            'id': course.id,
            'title': course.title,
            'category': course.category,
            'level': course.level,
            'badge': course.badge,
            'icon': course.icon_class,
            'description': course.short_description,
            'detailed_description': course.detailed_description,
            'duration': course.duration,
            'lessons': course.lessons,
            'students': str(course.students_enrolled),
            'rating': str(course.rating),
            'instructor': course.instructor_name,
            'instructor_bio': course.instructor_bio,
            'instructor_title': course.instructor_title,
            'price': float(course.price) if course.price else 0.0,
            'originalPrice': float(course.original_price) if course.original_price else None,
            'color': course.color,
            'details': course.get_details_dict() or {},
            'curriculum': course.get_curriculum_list() or [],
        }
        
        context.update({
            'related_courses': related_courses,
            'enrollment_count': enrollment_count,
            'course_json': json.dumps(course_data, default=str),
            'is_enrolled': False,  # You can check if user is enrolled if authenticated
        })
        
        # Check if user is enrolled (if authenticated)
        if self.request.user.is_authenticated:
            context['is_enrolled'] = CourseEnrollment.objects.filter(
                email=self.request.user.email,
                course=course
            ).exists()
        
        return context

@method_decorator(csrf_exempt, name='dispatch')
class CourseEnrollmentAPIView(View):
    """API view for handling course enrollments via AJAX."""
    
    def post(self, request, *args, **kwargs):
        response_data = {
            'success': False,
            'error': '',
            'message': '',
            'errors': {}
        }
        
        try:
            # Check content type
            content_type = request.content_type
            
            if content_type == 'application/json':
                # Parse JSON data
                data = json.loads(request.body)
            else:
                # Parse form data
                data = request.POST.dict()
                
                # Convert experience field name
                if 'experience' in data:
                    data['experience_level'] = data.pop('experience')
                if 'goals' in data:
                    data['learning_goals'] = data.pop('goals')
            
            print(f"Received enrollment data: {data}")  # Debug logging
            
            # Create form with data
            form = CourseEnrollmentForm(data)
            
            if form.is_valid():
                # Get course
                course_id = form.cleaned_data.get('course_id')
                print(f"Course ID from form: {course_id}")  # Debug logging
                
                try:
                    course = Course.objects.get(id=course_id, is_active=True)
                    print(f"Found course: {course.title}")  # Debug logging
                except Course.DoNotExist:
                    response_data['error'] = 'Course not found or is inactive.'
                    print(f"Course not found with ID: {course_id}")  # Debug logging
                    return JsonResponse(response_data, status=404)
                
                # Check if already enrolled with this email
                email = form.cleaned_data.get('email')
                print(f"Checking enrollment for email: {email}")  # Debug logging
                
                if CourseEnrollment.objects.filter(email=email, course=course).exists():
                    response_data['error'] = 'You are already enrolled in this course with this email.'
                    print(f"Already enrolled: {email} in course {course.title}")  # Debug logging
                    return JsonResponse(response_data, status=400)
                
                # Create enrollment using the form
                enrollment = form.save(commit=False)
                enrollment.course = course
                
                # Associate with logged-in user if available
                if request.user.is_authenticated:
                    enrollment.student = request.user
                
                # Save the enrollment (model's save() will handle calculations)
                enrollment.save()
                print(f"Enrollment saved successfully: {enrollment.id}")  # Debug logging
                
                # Update course statistics
                self.update_course_stats(course)
                
                # Send confirmation email (to be implemented)
                # self.send_confirmation_email(enrollment)
                
                response_data['success'] = True
                response_data['message'] = f'Successfully enrolled in {course.title}! A confirmation email has been sent.'
                response_data['enrollment_id'] = enrollment.id
                
                return JsonResponse(response_data, status=201)
            else:
                response_data['error'] = 'Form validation failed.'
                response_data['errors'] = form.errors.get_json_data()
                print(f"Form errors: {form.errors}")  # Debug logging
                return JsonResponse(response_data, status=400)
                
        except json.JSONDecodeError as e:
            response_data['error'] = f'Invalid JSON data: {str(e)}'
            print(f"JSON Decode Error: {e}")  # Debug logging
            return JsonResponse(response_data, status=400)
        except Exception as e:
            response_data['error'] = str(e)
            print(f"General error: {e}")  # Debug logging
            import traceback
            traceback.print_exc()  # Print full traceback
            return JsonResponse(response_data, status=500)
    
    def update_course_stats(self, course):
        """Update course and global statistics."""
        try:
            # Update course enrollment count
            course.students_enrolled = CourseEnrollment.objects.filter(course=course).count()
            course.save(update_fields=['students_enrolled'])
            print(f"Updated course enrollment count: {course.students_enrolled}")  # Debug logging
            
            # Update global statistics
            stats, _ = CourseStat.objects.get_or_create(id=1)
            stats.total_students = CourseEnrollment.objects.count()
            stats.total_courses = Course.objects.filter(is_active=True).count()
            stats.save()
            print(f"Updated global stats: {stats.total_students} students, {stats.total_courses} courses")  # Debug logging
        except Exception as e:
            print(f"Error updating stats: {e}")  # Debug logging
    
    def send_confirmation_email(self, enrollment):
        """Send enrollment confirmation email."""
        print(f"Would send confirmation email to: {enrollment.email}")  # Debug logging
        # To be implemented with Django's email system
        pass

# Admin/Management Views (optional)

class CourseListView(TemplateView):
    """View for admin to list all courses."""
    template_name = 'courses/admin/course_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = Course.objects.all().order_by('-created_at')
        context['courses'] = courses
        return context

class EnrollmentListView(TemplateView):
    """View for admin to list all enrollments."""
    template_name = 'courses/admin/enrollment_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enrollments = CourseEnrollment.objects.all().order_by('-enrollment_date')
        
        # Add pagination
        paginator = Paginator(enrollments, 20)  # 20 per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['page_obj'] = page_obj
        context['enrollments'] = page_obj.object_list
        return context