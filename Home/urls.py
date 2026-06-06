from django.urls import path
from . import views
from . import test

urlpatterns = [
    path('test-email/', test.test_email_config, name='test_email'),

    path('', views.HomePageView.as_view(), name='home'),
    path('solutions/', views.SolutionsPageView.as_view(), name='solutions'),
    path('careers/', views.CareersPageView.as_view(), name='careers'),
    path('pricing', views.Pricing.as_view(), name="pricing"),
    path('blog/', views.BlogPageView.as_view(), name='blog'),
    path('games/', views.GamesPageView.as_view(), name='games'),
    path('contact/', views.contact_view, name='contact'),
    path('demo/', views.DemoBookingView.as_view(), name='demo'),
    path("affiliates/", views.AffiliateView.as_view(), name="affiliate"),


]
