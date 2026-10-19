from django.urls import path

from . import views

app_name = "studio"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("documents/", views.document_list, name="document_list"),
    path("documents/new/", views.document_form, name="document_new"),
    path("documents/save/", views.document_save, name="document_save"),
    path("documents/<int:pk>/", views.document_detail, name="document_detail"),
    path("documents/<int:pk>/edit/", views.document_form, name="document_edit"),
    path("documents/<int:pk>/pdf/", views.document_pdf, name="document_pdf"),
    path("documents/<int:pk>/status/", views.document_status, name="document_status"),
    path("documents/<int:pk>/duplicate/", views.document_duplicate, name="document_duplicate"),
    path("documents/<int:pk>/delete/", views.document_delete, name="document_delete"),
]
