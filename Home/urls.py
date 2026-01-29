from django.urls import path
from . import views
from . import test

urlpatterns = [
    path('test-email/', test.test_email_config, name='test_email'),
    
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('tech/', views.TechPageView.as_view(), name='tech'),
    path('solutions/', views.SolutionsPageView.as_view(), name='solutions'),
    path('courses/', views.CoursesPageView.as_view(), name='courses'),
    path('careers/', views.CareersPageView.as_view(), name='careers'),
    path('blog/', views.BlogPageView.as_view(), name='blog'),
    path('games/', views.GamesPageView.as_view(), name='games'),
    path('contact/', views.contact_view, name='contact'),
    path('demo/', views.DemoBookingView.as_view(), name='demo'),
    
    path('courses/', views.CoursesPageView.as_view(), name='courses'),
    path('courses/enroll/', views.CourseEnrollmentAPIView.as_view(), name='course_enroll_api'), 
    path('courses/<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    
    
]
