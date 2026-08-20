from django.urls import path
from . import views
from . import test
from Affiliate.views import AffiliateView

urlpatterns = [
    path('test-email/', test.test_email_config, name='test_email'),

    path('', views.HomePageView.as_view(), name='home'),
    path('solutions/', views.SolutionsPageView.as_view(), name='solutions'),
    path('solutions/<slug:slug>/', views.SolutionDetailView.as_view(), name='solution_detail'),
    path('pricing/', views.Pricing.as_view(), name="pricing"),
    path('portfolio/', views.PortfolioPageView.as_view(), name='portfolio'),
    path('portfolio/<slug:slug>/', views.PortfolioDetailView.as_view(), name='portfolio_detail'),
    path('games/', views.GamesPageView.as_view(), name='games'),
    path('contact/', views.contact_view, name='contact'),
    path("affiliates/", AffiliateView.as_view(), name="affiliate"),

    path('qr-code/', views.QRGeneratorPageView.as_view(), name='qr_generator'),
    path('qr-code/image/', views.qr_code_image, name='qr_code_image'),
]
