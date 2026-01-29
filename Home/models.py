from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.html import format_html
import PIL
import uuid
from PIL import Image
from django.utils import timezone
import ipaddress
from django.urls import reverse
from django.core.validators import RegexValidator
import os
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

class TechServices(models.Model):
    id = models.BigAutoField(primary_key=True)
    icon = models.TextField("Icon HTML")
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Order by creation date by default
    class Meta:
        verbose_name = "Tech Service"
        verbose_name_plural = "Tech Services"
        ordering = ['created_at']

    def __str__(self):
        return self.name
    
class DataCounter(models.Model):
    id = models.BigAutoField(primary_key=True)
    projects_delivered = models.IntegerField("Projects Delivered", default=1000)
    systems_automated = models.IntegerField("Systems Automated", default=1000)
    happy_clients = models.IntegerField("Happy Clients", default=0)
    returning_clients = models.IntegerField("Returning Clients", default=1000)
    is_active = models.BooleanField("Active", default=True, 
                                   help_text="Uncheck to hide from website")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Data Counter"
        verbose_name_plural = "Data Counters"
    
    def __str__(self):
        return f"Counter Stats (Active: {self.is_active})"

def validate_square_image(image):
    """Validate that image is square"""
    img = Image.open(image)
    if img.width != img.height:
        raise ValidationError('Image must be square (same width and height)')

def validate_image_size(image, max_size_mb=2):
    """Validate image file size"""
    filesize = image.size
    if filesize > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Max file size is {max_size_mb}MB")

class TeamMember(models.Model):
    id = models.BigAutoField(primary_key=True)
    picture = models.ImageField(
        upload_to='team_pictures/',
        validators=[validate_image_size],
        help_text="Upload a square image (passport size: 2x2 inches or 600x600 pixels)"
    )
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    linkedin_url = models.URLField("LinkedIn URL", blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0, 
                                               help_text="Higher number appears first")
    is_active = models.BooleanField("Active", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ['-display_order', 'name']
    
    def save(self, *args, **kwargs):
        # Check if picture exists and is being updated
        if self.pk:
            try:
                old_instance = TeamMember.objects.get(pk=self.pk)
                if old_instance.picture != self.picture:
                    # Delete old picture if new one is uploaded
                    old_instance.picture.delete(save=False)
            except TeamMember.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
        
        if self.picture:
            try:
                img = Image.open(self.picture.path)
                
                # Make image square and passport size (600x600 pixels for web)
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Convert RGBA to RGB
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Resize to square (passport size: 600x600 for web)
                desired_size = 600
                
                # Calculate new dimensions maintaining aspect ratio
                img.thumbnail((desired_size, desired_size), Image.Resampling.LANCZOS)
                
                # Create square canvas
                new_img = Image.new('RGB', (desired_size, desired_size), (255, 255, 255))
                
                # Calculate position to center the image
                img_width, img_height = img.size
                left = (desired_size - img_width) // 2
                top = (desired_size - img_height) // 2
                
                # Paste resized image onto canvas
                new_img.paste(img, (left, top))
                
                # Save the image
                new_img.save(self.picture.path, 'JPEG', quality=85)
                
            except Exception as e:
                # Log error but don't break the save
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error processing team member image: {e}")
    
    def image_preview(self):
        if self.picture:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />', self.picture.url)
        return "No Image"
    image_preview.short_description = 'Preview'
    
    def __str__(self):
        return f"{self.name} - {self.position}"

class ClientReview(models.Model):
    id = models.BigAutoField(primary_key=True)
    client_name = models.CharField(max_length=100)
    client_position = models.CharField(max_length=100)
    client_company = models.CharField(max_length=100, blank=True, null=True)
    client_picture = models.ImageField(
        upload_to='client_pictures/',
        validators=[validate_image_size],
        help_text="Upload a profile picture (recommended: 400x400 pixels)"
    )
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')],
        default=5
    )
    is_featured = models.BooleanField("Featured Review", default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Client Review"
        verbose_name_plural = "Client Reviews"
        ordering = ['-is_featured', '-display_order', '-created_at']
    
    def save(self, *args, **kwargs):
        # Check if picture exists and is being updated
        if self.pk:
            try:
                old_instance = ClientReview.objects.get(pk=self.pk)
                if old_instance.client_picture != self.client_picture:
                    # Delete old picture if new one is uploaded
                    old_instance.client_picture.delete(save=False)
            except ClientReview.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
        
        if self.client_picture:
            try:
                img = Image.open(self.client_picture.path)
                
                # Convert if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Resize to profile picture size (400x400 for web)
                profile_size = 400
                
                # Resize maintaining aspect ratio
                img.thumbnail((profile_size, profile_size), Image.Resampling.LANCZOS)
                
                # Create circular mask for profile picture style (optional)
                # Or save as square with rounded corners
                img.save(self.client_picture.path, 'JPEG', quality=85)
                
            except Exception as e:
                # Log error but don't break the save
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error processing client image: {e}")
    
    def stars_display(self):
        return '★' * self.rating + '☆' * (5 - self.rating)
    stars_display.short_description = 'Rating'
    
    def image_preview(self):
        if self.client_picture:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />', self.client_picture.url)
        return "No Image"
    image_preview.short_description = 'Profile Picture'
    
    def __str__(self):
        return f"Review by {self.client_name} ({self.rating} stars)"
    
# CONTACT FORM SUBMISSION MODEL FOR ADMIN PANEL VIEWING
class ContactInquiry(models.Model):
    id = models.BigAutoField(primary_key=True)
    DEPARTMENT_CHOICES = [
        ('sales', 'Sales & Demos'),
        ('support', 'Technical Support'),
        ('partnership', 'Partnerships'),
        ('careers', 'Careers'),
        ('general', 'General Inquiry'),
        ('other', 'Other'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')]
    )
    company = models.CharField(max_length=200, blank=True, null=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default='general')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    # Additional fields
    newsletter_subscribed = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)
    
    # Status tracking
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('responded', 'Responded'),
        ('closed', 'Closed'),
        ('spam', 'Spam'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.PositiveSmallIntegerField(default=1, choices=[(1, 'Low'), (2, 'Medium'), (3, 'High'), (4, 'Urgent')])
    
    assigned_to = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='contact_assignments'
    )
    
    # Response tracking
    response_notes = models.TextField(blank=True, null=True)
    responded_at = models.DateTimeField(blank=True, null=True)
    responded_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='contact_responses'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_ip_location_info(self):
        """Get location info from IP (this would require an external service in production)"""
        if not self.ip_address:
            return "Unknown"
        
        try:
            # In production, you might want to use a service like ipinfo.io or maxmind
            ip_obj = ipaddress.ip_address(self.ip_address)
            return str(ip_obj)
        except ValueError:
            return "Invalid IP"
        

# DEMO -----------------------------------------------------
class DemoBooking(models.Model):
    SERVICE_CHOICES = [
        ('automation', 'Process Automation'),
        ('ai', 'AI Solutions'),
        ('development', 'Custom Development'),
        ('data', 'Data Intelligence'),
        ('security', 'Security Solutions'),
        ('training', 'Technology Training'),
        ('consulting', 'Consulting'),
        ('other', 'Other'),
    ]
    
    TIME_SLOTS = [
        ('09:00', '9:00 AM'),
        ('09:30', '9:30 AM'),
        ('10:00', '10:00 AM'),
        ('10:30', '10:30 AM'),
        ('11:00', '11:00 AM'),
        ('11:30', '11:30 AM'),
        ('12:00', '12:00 PM'),
        ('13:00', '1:00 PM'),
        ('13:30', '1:30 PM'),
        ('14:00', '2:00 PM'),
        ('14:30', '2:30 PM'),
        ('15:00', '3:00 PM'),
        ('15:30', '3:30 PM'),
        ('16:00', '4:00 PM'),
        ('16:30', '4:30 PM'),
        ('17:00', '5:00 PM'),
    ]
    
    # Unique identifier
    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    
    # Contact Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=200)
    job_title = models.CharField(max_length=100)
    
    # Demo Details
    demo_date = models.DateField()
    demo_time = models.CharField(max_length=5, choices=TIME_SLOTS)
    demo_title = models.CharField(max_length=200)
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES, blank=True, null=True)
    demo_message = models.TextField(blank=True, null=True)
    
    # Status Tracking
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Additional Fields
    terms_accepted = models.BooleanField(default=False)
    number_of_attendees = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(50)])
    meeting_platform = models.CharField(max_length=50, default='Zoom', choices=[
        ('zoom', 'Zoom'),
        ('teams', 'Microsoft Teams'),
        ('google', 'Google Meet'),
        ('other', 'Other'),
    ])
    
    # Technical Information
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)
    
    # Response Tracking
    meeting_link = models.URLField(blank=True, null=True)
    meeting_id = models.CharField(max_length=100, blank=True, null=True)
    meeting_password = models.CharField(max_length=50, blank=True, null=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    confirmed_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='confirmed_demos'
    )
    notes = models.TextField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Demo Booking"
        verbose_name_plural = "Demo Bookings"
        ordering = ['-demo_date', 'demo_time']
        indexes = [
            models.Index(fields=['demo_date', 'demo_time']),
            models.Index(fields=['email']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.demo_title} ({self.get_demo_datetime()})"
    
    def get_demo_datetime(self):
        """Combine date and time into a datetime object"""
        from datetime import datetime
        return datetime.combine(self.demo_date, datetime.strptime(self.demo_time, '%H:%M').time())
    
    def is_upcoming(self):
        """Check if demo is in the future"""
        return self.get_demo_datetime() > timezone.now()
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def formatted_date(self):
        return self.demo_date.strftime('%B %d, %Y')
    
    def formatted_time(self):
        return dict(self.TIME_SLOTS).get(self.demo_time, self.demo_time)
    
    def formatted_datetime(self):
        return f"{self.formatted_date()} at {self.formatted_time()}"
    
    
class Solution(models.Model):
    """Model to store technology solutions information."""
    
    # Icon choices (using FontAwesome classes)
    ICON_CHOICES = [
        ('fa-code', 'Code'),
        ('fa-robot', 'Robot'),
        ('fa-database', 'Database'),
        ('fa-comments', 'Comments'),
        ('fa-shield-alt', 'Shield'),
        ('fa-server', 'Server'),
        ('fa-network-wired', 'Network'),
        ('fa-graduation-cap', 'Graduation Cap'),
    ]
    
    # Slug/id for URL identification
    slug = models.SlugField(max_length=50, unique=True, help_text="Used in URLs and for identification", primary_key=True)
    
    # Basic information
    title = models.CharField(max_length=100)
    short_description = models.TextField(max_length=200)
    detailed_description = models.TextField()
    
    # Visual elements
    icon_class = models.CharField(max_length=50, choices=ICON_CHOICES)
    z_index = models.IntegerField(default=0, help_text="CSS z-index value for styling")
    
    # Features
    features = models.TextField(
        help_text="Enter features separated by new lines. Each line will become a list item."
    )
    
    # Call to action
    cta_text = models.CharField(max_length=50, default="Learn More")
    cta_link = models.CharField(max_length=200, default="#")
    
    # Meta
    display_order = models.IntegerField(
        default=0,
        help_text="Order in which solutions are displayed (lower numbers first)"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', 'title']
        verbose_name = "Technology Solution"
        verbose_name_plural = "Technology Solutions"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('solutions_detail', kwargs={'slug': self.slug})
    
    def get_features_list(self):
        """Convert features text field to list."""
        if self.features:
            return [feature.strip() for feature in self.features.split('\n') if feature.strip()]
        return []
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug and self.title:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
        
class Course(models.Model):
    """Model for storing course information."""
    
    # Category choices
    CATEGORY_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('iot', 'IoT'),
        ('ai', 'AI & ML'),
        ('scratch', 'Scratch for Kids'),
        ('web', 'Web Development'),
        ('mobile', 'Mobile Development'),
        ('data', 'Data Science'),
        ('security', 'Security'),
    ]
    
    # Level choices
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('all', 'All Levels'),
    ]
    
    # Badge choices
    BADGE_CHOICES = [
        ('popular', 'Most Popular'),
        ('new', 'New'),
        ('advanced', 'Advanced'),
        ('kids', 'For Kids'),
        ('', 'No Badge'),
    ]
    
    # Icon choices (FontAwesome classes)
    ICON_CHOICES = [
        ('fab fa-python', 'Python'),
        ('fab fa-js-square', 'JavaScript'),
        ('fas fa-microchip', 'Microchip/IoT'),
        ('fas fa-robot', 'Robot/AI'),
        ('fas fa-server', 'Server'),
        ('fas fa-chart-line', 'Chart/Data'),
        ('fas fa-shield-alt', 'Shield/Security'),
        ('fas fa-gamepad', 'Gamepad/Kids'),
        ('fab fa-node-js', 'Node.js'),
        ('fas fa-laptop-code', 'Laptop Code'),
        ('fas fa-database', 'Database'),
        ('fas fa-cloud', 'Cloud'),
    ]
    
    # Basic Information
    id = models.BigAutoField(primary_key=True)  # Keep ID as primary key
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    badge = models.CharField(max_length=50, choices=BADGE_CHOICES, blank=True)
    icon_class = models.CharField(max_length=50, choices=ICON_CHOICES)
    color = models.CharField(max_length=7, default='#3776AB', help_text="Hex color code")
    
    # Description
    short_description = models.CharField(max_length=200)
    detailed_description = models.TextField()
    
    # Course Details
    duration = models.CharField(max_length=50, help_text="e.g., 12 Weeks")
    lessons = models.CharField(max_length=50, help_text="e.g., 48 Lessons")
    students_enrolled = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5, 
                                validators=[MinValueValidator(0), MaxValueValidator(5)])
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Instructor Information
    instructor_name = models.CharField(max_length=100)
    instructor_bio = models.TextField()
    instructor_title = models.CharField(max_length=100, blank=True, 
                                        help_text="e.g., Senior AI Engineer")
    
    # Course Details (JSON-like structure stored as text)
    details = models.JSONField(default=dict, blank=True, 
                              help_text="JSON format: {'Mode': 'Online', 'Schedule': 'Mon & Wed'}")
    
    # Curriculum (stored as JSON for flexibility)
    curriculum = models.JSONField(default=list, blank=True, 
                                 help_text="JSON array of modules with lessons")
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = "Course"
        verbose_name_plural = "Courses"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})
    
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0
    
    def formatted_price(self):
        return f"${self.price:.2f}"
    
    def formatted_original_price(self):
        if self.original_price:
            return f"${self.original_price:.2f}"
        return ""
    
    def get_details_dict(self):
        """Convert details JSON to dictionary."""
        return self.details if isinstance(self.details, dict) else {}
    
    def get_curriculum_list(self):
        """Convert curriculum JSON to list."""
        return self.curriculum if isinstance(self.curriculum, list) else []


class CourseEnrollment(models.Model):
    """Model for student course enrollments."""
    
    # Enrollment Status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Payment Status
    PAYMENT_CHOICES = [
        ('pending', 'Pending Payment'),
        ('paid', 'Paid'),
        ('failed', 'Payment Failed'),
        ('refunded', 'Refunded'),
    ]
    
    # Experience Level
    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner (0-1 years)'),
        ('intermediate', 'Intermediate (1-3 years)'),
        ('advanced', 'Advanced (3+ years)'),
    ]
    
    # Student Information
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Course Information
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    
    # Additional Information
    country = models.CharField(max_length=100)
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES)
    learning_goals = models.TextField(blank=True)
    
    # Enrollment Details
    enrollment_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='pending')
    payment_id = models.CharField(max_length=100, blank=True)
    
    # Payment Details
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Additional Fields
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-enrollment_date']
        unique_together = ['email', 'course']
        verbose_name = "Course Enrollment"
        verbose_name_plural = "Course Enrollments"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.course.title}"
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def calculate_total_amount(self):
        """Calculate total amount including fees and tax."""
        base_amount = self.course.price
        platform_fee = self.platform_fee
        tax_rate = 0.10  # 10% tax
        tax_amount = (base_amount + platform_fee) * tax_rate
        return base_amount + platform_fee + tax_amount
    
    def save(self, *args, **kwargs):
        # Auto-calculate total amount if not set
        if not self.total_amount:
            self.total_amount = self.calculate_total_amount()
            self.tax_amount = (self.course.price + self.platform_fee) * 0.10
        
        # Auto-set amount_paid if payment is marked as paid
        if self.payment_status == 'paid' and self.amount_paid == 0:
            self.amount_paid = self.total_amount
        
        super().save(*args, **kwargs)


class CourseStat(models.Model):
    """Model for storing course statistics."""
    id = models.BigAutoField(primary_key=True)
    total_courses = models.IntegerField(default=0)
    total_students = models.IntegerField(default=0)
    satisfaction_rate = models.DecimalField(max_digits=4, decimal_places=1, default=98.0)
    total_instructors = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Course Statistic"
        verbose_name_plural = "Course Statistics"
    
    def __str__(self):
        return f"Course Statistics ({self.last_updated.date()})"