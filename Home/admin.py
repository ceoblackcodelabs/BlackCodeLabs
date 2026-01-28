from django.contrib import admin
from django.utils.html import format_html
from .models import TechServices, DataCounter, TeamMember, ClientReview
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.core.exceptions import ValidationError

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