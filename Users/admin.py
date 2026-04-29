from django.contrib import admin
from django.utils.html import format_html
from .models import *

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'role')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('role',)


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1

class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1

class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1

class PortfolioItemInline(admin.TabularInline):
    model = PortfolioItem
    extra = 1

class TestimonialInline(admin.TabularInline):
    model = Testimonial
    extra = 1

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email', 'phone', 'experience_years']
    search_fields = ['name', 'email', 'title']
    inlines = [SkillInline, ExperienceInline, EducationInline, ServiceInline, PortfolioItemInline, TestimonialInline]
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'name', 'title', 'profile_image', 'about_text')
        }),
        ('Contact Details', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Professional Details', {
            'fields': ('birthday', 'degree', 'experience_years', 'freelance_status')
        }),
        ('Statistics', {
            'fields': ('years_of_experience', 'happy_clients', 'completed_projects')
        }),
        ('Social Media', {
            'fields': ('twitter', 'facebook', 'linkedin', 'instagram', 'github')
        }),
        ('Additional', {
            'fields': ('typed_texts', 'cv_file')
        })
    )

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'percentage', 'color', 'profile']
    list_filter = ['color', 'profile']
    search_fields = ['name']

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'get_date_range', 'is_current', 'profile']
    list_filter = ['is_current', 'profile']
    search_fields = ['title', 'company']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon_preview', 'profile', 'order']
    list_filter = ['profile']
    
    def icon_preview(self, obj):
        return format_html('<i class="fab {}"></i>', obj.icon)
    icon_preview.short_description = 'Icon'

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'image_preview', 'profile']
    list_filter = ['category', 'profile']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;"/>', obj.image.url)
        return 'No Image'
    image_preview.short_description = 'Preview'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_profession', 'rating', 'is_active', 'profile']
    list_filter = ['rating', 'is_active', 'profile']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    actions = ['mark_as_read']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active']
    list_filter = ['is_active', 'subscribed_at']

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['profile', 'site_name', 'show_subscribe_section', 'contact_form_active']