# """
# core/admin.py
# """

# from django.contrib import admin
# from django.utils.html import format_html

# from .models import (
#     SiteSettings,
#     HeroContent,
#     PerspectiveSection,
#     Service,
#     SocialStat,
# )


# @admin.register(SiteSettings)
# class SiteSettingsAdmin(admin.ModelAdmin):
#     fieldsets = (
#         ('Branding', {'fields': ('site_name', 'tagline', 'founded_year', 'base_city')}),
#         ('Contact', {'fields': ('email_general', 'email_booking', 'phone', 'address_line1', 'address_line2')}),
#         ('Social Links', {'fields': ('instagram_url', 'tiktok_url', 'youtube_url', 'facebook_url')}),
#         ('Footer', {'fields': ('footer_about', 'powered_by')}),
#     )

#     def has_add_permission(self, request):
#         # Only one record ever
#         return not SiteSettings.objects.exists()

#     def has_delete_permission(self, request, obj=None):
#         return False


# @admin.register(HeroContent)
# class HeroContentAdmin(admin.ModelAdmin):
#     fieldsets = (
#         ('Text', {'fields': ('eyebrow', 'headline', 'subtext')}),
#         ('Calls to Action', {'fields': (
#             'cta_primary_label', 'cta_primary_url',
#             'cta_outline_label', 'cta_outline_url',
#         )}),
#     )

#     def has_add_permission(self, request):
#         return not HeroContent.objects.exists()

#     def has_delete_permission(self, request, obj=None):
#         return False


# @admin.register(PerspectiveSection)
# class PerspectiveSectionAdmin(admin.ModelAdmin):
#     def has_add_permission(self, request):
#         return not PerspectiveSection.objects.exists()

#     def has_delete_permission(self, request, obj=None):
#         return False


# @admin.register(Service)
# class ServiceAdmin(admin.ModelAdmin):
#     list_display  = ('order', 'title', 'is_active', 'image_preview')
#     list_editable = ('order', 'is_active')
#     list_display_links = ('title',)
#     ordering      = ('order',)

#     def image_preview(self, obj):
#         if obj.image:
#             return format_html(
#                 '<img src="{}" style="height:50px;border-radius:4px;" />',
#                 obj.image.url,
#             )
#         return '—'
#     image_preview.short_description = 'Preview'


# @admin.register(SocialStat)
# class SocialStatAdmin(admin.ModelAdmin):
#     list_display  = ('order', 'label', 'value', 'show_in_marquee', 'show_in_community')
#     list_editable = ('order', 'show_in_marquee', 'show_in_community')
#     list_display_links = ('label',)
#     ordering      = ('order',)