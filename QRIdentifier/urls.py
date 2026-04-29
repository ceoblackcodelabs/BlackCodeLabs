from django.urls import path
from .views import QRview

urlpatterns = [
    path('', QRview.as_view(), name='qr_view'),
]