from django.urls import path
from . import views
from . import test

urlpatterns = [
    path('test-email/', test.test_email_config, name='test_email'),

    path('', views.HomePageView.as_view(), name='home'),
    path('solutions/', views.SolutionsPageView.as_view(), name='solutions'),
    path('pricing', views.Pricing.as_view(), name="pricing"),
    path('games/', views.GamesPageView.as_view(), name='games'),
    path('contact/', views.contact_view, name='contact'),
    path("affiliates/", views.AffiliateView.as_view(), name="affiliate"),


]
