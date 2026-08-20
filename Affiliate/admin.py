from django.contrib import admin
from .models import AffiliateApplication


@admin.register(AffiliateApplication)
class AffiliateApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'audience_size', 'status', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'audience_size')
    search_fields = ('full_name', 'email')
    readonly_fields = ('ip_address', 'created_at')
