from django.urls import path
from . import views

app_name = "affiliate"

urlpatterns = [
    path("apply/", views.affiliate_apply, name="apply"),
]
