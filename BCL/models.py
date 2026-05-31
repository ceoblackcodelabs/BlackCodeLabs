from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class ContactMessage(models.Model):
    """Model for storing contact form submissions"""

    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('booking', 'Booking Request'),
        ('collaboration', 'Collaboration'),
        ('workshop', 'Workshop Inquiry'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]

    # Personal Information
    name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phone Number")

    # Message Details
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, default='general')
    subject_other = models.CharField(max_length=200, blank=True, null=True, verbose_name="Custom Subject")
    message = models.TextField(verbose_name="Message")

    # Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Response tracking
    responded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.name} - {self.get_subject_display()} ({self.created_at.strftime('%Y-%m-%d')})"

    def mark_as_read(self):
        if self.status == 'new':
            self.status = 'read'
            self.save(update_fields=['status'])

    def mark_as_replied(self, response_text=None, responder=None):
        self.status = 'replied'
        if response_text:
            self.response_message = response_text
        if responder:
            self.responded_by = responder
        self.responded_at = timezone.now()
        self.save()

    @property
    def full_subject(self):
        if self.subject == 'other' and self.subject_other:
            return self.subject_other
        return self.get_subject_display()


class ContactSettings(models.Model):
    """Model for contact page settings (singleton)"""

    # Contact Information
    email_general = models.EmailField(default='info@bclproduction.com')
    email_booking = models.EmailField(default='booking@bclproduction.com')
    phone = models.CharField(max_length=20, default='+254 799 804 185')
    address = models.TextField(default='Nairobi, Kenya\n00100 Ngara')

    # Social Media Links
    instagram = models.URLField(blank=True, null=True)
    tiktok = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)

    # Business Hours
    business_hours = models.CharField(max_length=200, blank=True, null=True)

    # Auto-reply Settings
    auto_reply_enabled = models.BooleanField(default=True)
    auto_reply_subject = models.CharField(max_length=200, default="Thank you for contacting BCL PRODUCTION")
    auto_reply_message = models.TextField(
        default="Thank you for reaching out to BCL PRODUCTION. We have received your message and will get back to you within 24-48 business hours.\n\nBest regards,\nBCL PRODUCTION Team"
    )

    # Map Settings
    google_maps_api_key = models.CharField(max_length=200, blank=True, null=True)
    map_latitude = models.DecimalField(max_digits=10, decimal_places=7, default=-1.286389)
    map_longitude = models.DecimalField(max_digits=10, decimal_places=7, default=36.817223)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contact Settings"
        verbose_name_plural = "Contact Settings"

    def save(self, *args, **kwargs):
        if not self.pk and ContactSettings.objects.exists():
            raise ValidationError("There can only be one ContactSettings instance")
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        """Get or create singleton settings"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings

    def __str__(self):
        return "Contact Page Settings"

class AboutSection(models.Model):
    """Model for about section content"""

    title = models.CharField(max_length=200, default="About BCL PRODUCTION")
    content = models.TextField(default="BCL PRODUCTION is a leading media production company based in Nairobi, Kenya...")
    image = models.ImageField(upload_to='about_images/', blank=True, null=True)
    video = models.FileField(
        upload_to='about_videos/',
        blank=True,
        null=True,
        help_text="Upload MP4, WebM, or MOV files"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Sections"

    def __str__(self):
        return self.title

class Merch(models.Model):
    """Model for merchandise items"""

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='merch_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Merchandise Item"
        verbose_name_plural = "Merchandise Items"

    def __str__(self):
        return self.name