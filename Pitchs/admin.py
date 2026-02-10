from django.contrib import admin
from .models import Project, ProjectRequest

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_available', 'created_at')
    list_filter = ('category', 'is_available', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_available',)
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Pricing', {
            'fields': ('documentation_price', 'coding_price', 'price')
        }),
        ('Status', {
            'fields': ('is_available',)
        }),
    )

@admin.register(ProjectRequest)
class ProjectRequestAdmin(admin.ModelAdmin):
    list_display = ('custom_title', 'email', 'phone_number', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('custom_title', 'email', 'phone_number', 'description')
    list_editable = ('status',)
    readonly_fields = ('created_at',)