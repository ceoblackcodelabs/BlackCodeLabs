from django.contrib import admin
from django.utils.html import format_html
from .models import (
    TechServices, DataCounter, TeamMember, 
    ClientReview, ContactInquiry, DemoBooking,
    Solution, Course, CourseEnrollment, CourseStat
)
from django.utils import timezone
from django.utils.safestring import mark_safe

@admin.register(TechServices)
class TechServicesAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_preview', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'icon_preview_detailed')
    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'description')
        }),
        ('Icon Settings', {
            'fields': ('icon', 'icon_preview_detailed'),
            'description': 'Paste HTML/icon code here (Font Awesome, SVG, etc.)'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def icon_preview(self, obj):
        if obj.icon:
            return mark_safe(f'<div style="font-size: 20px;">{obj.icon}</div>')
        return "No Icon"
    icon_preview.short_description = 'Icon'
    
    def icon_preview_detailed(self, obj):
        if obj.icon:
            return mark_safe(f'''
                <div style="margin: 10px 0;">
                    <div style="font-size: 30px; margin-bottom: 10px;">{obj.icon}</div>
                    <div style="background: #f5f5f5; padding: 10px; border-radius: 5px;">
                        <code>{obj.icon}</code>
                    </div>
                </div>
            ''')
        return "No Icon"
    icon_preview_detailed.short_description = 'Icon Preview'

@admin.register(DataCounter)
class DataCounterAdmin(admin.ModelAdmin):
    list_display = ('is_active', 'projects_delivered', 'systems_automated', 
                    'happy_clients', 'returning_clients', 'updated_at')
    list_editable = ('projects_delivered', 'systems_automated', 'happy_clients', 'returning_clients')
    list_filter = ('is_active', 'updated_at')
    readonly_fields = ('updated_at',)
    actions = ['activate_counters', 'deactivate_counters']
    
    def activate_counters(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f'{queryset.count()} counter(s) activated.')
    activate_counters.short_description = "Activate selected counters"
    
    def deactivate_counters(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f'{queryset.count()} counter(s) deactivated.')
    deactivate_counters.short_description = "Deactivate selected counters"

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'position', 'email', 'is_active', 'display_order')
    list_display_links = ('image_preview', 'name')
    list_editable = ('position', 'display_order', 'is_active')
    list_filter = ('is_active', 'position', 'created_at')
    search_fields = ('name', 'position', 'email')
    readonly_fields = ('created_at', 'image_preview_large')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'position', 'email', 'linkedin_url')
        }),
        ('Image', {
            'fields': ('picture', 'image_preview_large'),
            'description': 'Upload a square passport-style photo'
        }),
        ('Display Settings', {
            'fields': ('display_order', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.picture:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />', 
                obj.picture.url
            )
        return "No Image"
    image_preview.short_description = 'Photo'
    
    def image_preview_large(self, obj):
        if obj.picture:
            return format_html(
                '<img src="{}" width="150" height="150" style="border-radius: 50%; object-fit: cover; border: 3px solid #eee;" />', 
                obj.picture.url
            )
        return "No Image"
    image_preview_large.short_description = 'Current Photo'

@admin.register(ClientReview)
class ClientReviewAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'client_name', 'client_position', 
                    'rating_stars', 'is_featured', 'created_at')
    list_display_links = ('image_preview', 'client_name')
    list_editable = ('is_featured', 'client_position')
    list_filter = ('is_featured', 'rating', 'created_at')
    search_fields = ('client_name', 'client_position', 'review_text')
    readonly_fields = ('created_at', 'image_preview_large')
    fieldsets = (
        ('Client Information', {
            'fields': ('client_name', 'client_position', 'client_company')
        }),
        ('Review Content', {
            'fields': ('review_text', 'rating')
        }),
        ('Profile Picture', {
            'fields': ('client_picture', 'image_preview_large'),
            'description': 'Upload a professional profile picture'
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'display_order')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def rating_stars(self, obj):
        return format_html(
            '<span style="color: #ffc107; font-size: 14px;">{}</span>', 
            obj.stars_display()
        )
    rating_stars.short_description = 'Rating'
    
    def image_preview(self, obj):
        if obj.client_picture:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />', 
                obj.client_picture.url
            )
        return "No Image"
    image_preview.short_description = 'Client'
    
    def image_preview_large(self, obj):
        if obj.client_picture:
            return format_html(
                '<img src="{}" width="150" height="150" style="border-radius: 50%; object-fit: cover; border: 3px solid #eee;" />', 
                obj.client_picture.url
            )
        return "No Image"
    image_preview_large.short_description = 'Current Photo'

# Customize admin site
admin.site.site_header = "Company Dashboard"
admin.site.site_title = "Company Admin"
admin.site.index_title = "Welcome to Company Administration"


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'department', 'status', 'created_at')
    list_filter = ('status', 'department', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at', 'ip_address', 'user_agent', 'referrer')
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'company')
        }),
        ('Inquiry Details', {
            'fields': ('department', 'subject', 'message', 'newsletter_subscribed')
        }),
        ('Status', {
            'fields': ('status', 'priority')
        }),
        ('Technical Information', {
            'fields': ('ip_address', 'user_agent', 'referrer'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'
    
    # Simple actions without complex HTML
    actions = ['mark_as_new', 'mark_as_responded', 'mark_as_closed']
    
    def mark_as_new(self, request, queryset):
        updated = queryset.update(status='new')
        self.message_user(request, f'{updated} inquiries marked as new.')
    mark_as_new.short_description = "Mark as New"
    
    def mark_as_responded(self, request, queryset):
        updated = queryset.update(status='responded')
        self.message_user(request, f'{updated} inquiries marked as responded.')
    mark_as_responded.short_description = "Mark as Responded"
    
    def mark_as_closed(self, request, queryset):
        updated = queryset.update(status='closed')
        self.message_user(request, f'{updated} inquiries marked as closed.')
    mark_as_closed.short_description = "Mark as Closed"
    
@admin.register(DemoBooking)
class DemoBookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id_short', 'full_name', 'company', 'demo_datetime', 'status_badge', 'created_at')
    list_filter = ('status', 'demo_date', 'service_type', 'meeting_platform', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'company', 'demo_title', 'booking_id')
    readonly_fields = ('created_at', 'updated_at', 'ip_address', 'user_agent', 'referrer', 'booking_id')
    fieldsets = (
        ('Contact Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'company', 'job_title')
        }),
        ('Demo Details', {
            'fields': ('demo_date', 'demo_time', 'demo_title', 'service_type', 'demo_message',
                      'number_of_attendees', 'meeting_platform')
        }),
        ('Meeting Information', {
            'fields': ('meeting_link', 'meeting_id', 'meeting_password'),
            'classes': ('collapse',)
        }),
        ('Status & Tracking', {
            'fields': ('status', 'terms_accepted', 'notes')
        }),
        ('Technical Information', {
            'fields': ('booking_id', 'ip_address', 'user_agent', 'referrer'),
            'classes': ('collapse',)
        }),
        ('Confirmation Details', {
            'fields': ('confirmed_at', 'confirmed_by'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['confirm_selected', 'mark_as_completed', 'mark_as_cancelled', 'send_reminder_email']
    
    def booking_id_short(self, obj):
        return str(obj.booking_id)[:8] + "..."
    booking_id_short.short_description = 'Booking ID'
    
    def demo_datetime(self, obj):
        return obj.formatted_datetime()
    demo_datetime.short_description = 'Demo Date & Time'
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'confirmed': 'green',
            'completed': 'blue',
            'cancelled': 'red',
            'no_show': 'gray',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 12px; font-size: 12px; font-weight: bold;">{}</span>',
            color, obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'
    
    def confirm_selected(self, request, queryset):
        updated = queryset.update(
            status='confirmed',
            confirmed_at=timezone.now(),
            confirmed_by=request.user
        )
        self.message_user(request, f'{updated} demo(s) confirmed.')
    confirm_selected.short_description = "Confirm selected demos"
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} demo(s) marked as completed.')
    mark_as_completed.short_description = "Mark as completed"
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} demo(s) marked as cancelled.')
    mark_as_cancelled.short_description = "Mark as cancelled"
    
    def send_reminder_email(self, request, queryset):
        # This would send reminder emails - you'd implement the email sending logic
        self.message_user(request, f'Reminder emails would be sent for {queryset.count()} demo(s).')
    send_reminder_email.short_description = "Send reminder email"
    
    def get_queryset(self, request):
        # Show upcoming demos first
        qs = super().get_queryset(request)
        return qs.order_by('demo_date', 'demo_time')
    
@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_order', 'is_active', 'icon_preview', 'created_at')
    list_filter = ('is_active', 'icon_class', 'created_at')
    search_fields = ('title', 'short_description', 'detailed_description')
    list_editable = ('display_order', 'is_active')
    readonly_fields = ('slug', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'detailed_description')
        }),
        ('Visual Elements', {
            'fields': ('icon_class', 'z_index')
        }),
        ('Content', {
            'fields': ('features', 'cta_text', 'cta_link')
        }),
        ('Display Settings', {
            'fields': ('display_order', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def icon_preview(self, obj):
        return format_html('<i class="fas {}"></i> {}', obj.icon_class, obj.get_icon_class_display())
    icon_preview.short_description = 'Icon'
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('display_order', 'title')
    

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'level', 'price', 'students_enrolled', 
                   'rating', 'is_active', 'display_order', 'created_at')
    list_filter = ('category', 'level', 'is_active', 'is_featured', 'created_at')
    search_fields = ('title', 'short_description', 'instructor_name')
    list_editable = ('display_order', 'is_active', 'price')
    readonly_fields = ('slug', 'created_at', 'updated_at', 'students_enrolled')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'detailed_description')
        }),
        ('Course Details', {
            'fields': ('category', 'level', 'badge', 'icon_class', 'color')
        }),
        ('Content & Structure', {
            'fields': ('duration', 'lessons', 'details', 'curriculum')
        }),
        ('Instructor', {
            'fields': ('instructor_name', 'instructor_title', 'instructor_bio')
        }),
        ('Pricing', {
            'fields': ('price', 'original_price')
        }),
        ('Statistics', {
            'fields': ('students_enrolled', 'rating')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'is_featured', 'display_order')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('display_order', '-created_at')


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'course', 'email', 'status', 'payment_status', 
                   'total_amount', 'enrollment_date')
    list_filter = ('status', 'payment_status', 'enrollment_date', 'course', 'country')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'course__title')
    readonly_fields = ('enrollment_date', 'created_at', 'updated_at')
    fieldsets = (
        ('Student Information', {
            'fields': ('student', 'first_name', 'last_name', 'email', 'phone')
        }),
        ('Course Information', {
            'fields': ('course',)
        }),
        ('Additional Information', {
            'fields': ('country', 'experience_level', 'learning_goals')
        }),
        ('Enrollment Details', {
            'fields': ('start_date', 'completion_date')
        }),
        ('Payment Information', {
            'fields': ('status', 'payment_status', 'payment_id',
                      'amount_paid', 'platform_fee', 'tax_amount', 'total_amount')
        }),
        ('Administrative', {
            'fields': ('notes', 'is_active')
        }),
    )
    
    def full_name(self, obj):
        return obj.full_name()
    full_name.short_description = 'Student Name'
    
    actions = ['mark_as_confirmed', 'mark_as_completed', 'mark_payment_paid']
    
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} enrollments marked as confirmed.')
    mark_as_confirmed.short_description = "Mark selected as confirmed"
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} enrollments marked as completed.')
    mark_as_completed.short_description = "Mark selected as completed"
    
    def mark_payment_paid(self, request, queryset):
        updated = queryset.update(payment_status='paid')
        self.message_user(request, f'{updated} payments marked as paid.')
    mark_payment_paid.short_description = "Mark selected payments as paid"


@admin.register(CourseStat)
class CourseStatAdmin(admin.ModelAdmin):
    list_display = ('total_courses', 'total_students', 'satisfaction_rate', 
                   'total_instructors', 'last_updated')
    readonly_fields = ('last_updated',)
    
    def has_add_permission(self, request):
        # Only allow one stats record
        return not CourseStat.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False