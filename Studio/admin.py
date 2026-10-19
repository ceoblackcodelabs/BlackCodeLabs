from django.contrib import admin

from .models import GeneratedDocument


@admin.register(GeneratedDocument)
class GeneratedDocumentAdmin(admin.ModelAdmin):
    list_display = ("reference", "doc_type", "client_name", "amount", "status", "revision", "created_at")
    list_filter = ("doc_type", "status")
    search_fields = ("reference", "client_name", "title")
    readonly_fields = ("reference", "doc_type", "revision", "created_by", "created_at", "updated_at")
    exclude = ("pdf",)

    def get_queryset(self, request):
        return super().get_queryset(request).defer("pdf")  # don't pull every PDF blob into the list
