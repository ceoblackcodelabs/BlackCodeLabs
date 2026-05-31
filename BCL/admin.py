from django.contrib import admin
from .models import ContactMessage, ContactSettings, AboutSection, Merch

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject_display', 'status_badge', 'created_at']
    list_filter = ['status', 'subject', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at', 'updated_at', 'ip_address', 'user_agent', 'responded_at']

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('subject', 'subject_other', 'message')
        }),
        ('Status & Response', {
            'fields': ('status', 'responded_at')
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def subject_display(self, obj):
        return obj.full_subject
    subject_display.short_description = 'Subject'

    def status_badge(self, obj):
        colors = {
            'new': 'red',
            'read': 'orange',
            'replied': 'green',
            'archived': 'gray'
        }
        from django.utils.html import format_html
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    actions = ['mark_as_read', 'mark_as_replied', 'archive_messages']

    def mark_as_read(self, request, queryset):
        updated = queryset.exclude(status='read').update(status='read')
        self.message_user(request, f'{updated} message(s) marked as read.')
    mark_as_read.short_description = 'Mark selected messages as read'

    def mark_as_replied(self, request, queryset):
        updated = queryset.update(status='replied')
        self.message_user(request, f'{updated} message(s) marked as replied.')
    mark_as_replied.short_description = 'Mark selected messages as replied'

    def archive_messages(self, request, queryset):
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} message(s) archived.')
    archive_messages.short_description = 'Archive selected messages'


@admin.register(ContactSettings)
class ContactSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Contact Information', {
            'fields': ('email_general', 'email_booking', 'phone', 'address')
        }),
        ('Social Media', {
            'fields': ('instagram', 'tiktok', 'youtube', 'facebook', 'twitter')
        }),
        ('Business Hours', {
            'fields': ('business_hours',)
        }),
        ('Auto-Reply Settings', {
            'fields': ('auto_reply_enabled', 'auto_reply_subject', 'auto_reply_message')
        }),
        ('Map Settings', {
            'fields': ('google_maps_api_key', 'map_latitude', 'map_longitude'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Prevent adding multiple instances (singleton pattern)
        return not ContactSettings.objects.exists()


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    fieldsets = (
        ('Content', {
            'fields': ('title', 'content', 'image', 'video')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Merch)
class MerchAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    list_editable = ['price']  # Allows inline editing of price
    readonly_fields = ['created_at', 'updated_at', 'image_preview']

    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'description', 'price', 'image')
        }),
        ('Preview', {
            'fields': ('image_preview',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def price_display(self, obj):
        """Display price with currency symbol"""
        return f"€{obj.price}"
    price_display.short_description = 'Price'

    def image_preview(self, obj):
        """Display image preview in admin"""
        if obj.image:
            from django.utils.html import format_html
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 200px;" />',
                obj.image.url
            )
        return "No image uploaded"
    image_preview.short_description = 'Image Preview'

    actions = ['duplicate_items']

    def duplicate_items(self, request, queryset):
        """Duplicate selected merchandise items"""
        for item in queryset:
            item.pk = None  # Create new instance
            item.name = f"{item.name} (Copy)"
            item.save()
        count = queryset.count()
        self.message_user(request, f'{count} item(s) duplicated successfully.')
    duplicate_items.short_description = 'Duplicate selected items'