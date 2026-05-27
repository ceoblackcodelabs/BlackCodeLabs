from django.urls import path
from .views import landing


urlpatterns = [
    # Homepage (single-page layout)
    path('', landing.as_view(), name='bcl_home'),

    # Services
    # path('services/', ServiceListView.as_view(), name='service_list'),
    # path('services/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
]