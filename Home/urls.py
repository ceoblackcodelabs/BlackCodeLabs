from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('contact/', views.ContactPageView.as_view(), name='contact'),
    path('tech/', views.TechPageView.as_view(), name='tech'),
    path('solutions/', views.SolutionsPageView.as_view(), name='solutions'),
    path('courses/', views.CoursesPageView.as_view(), name='courses'),
    path('careers/', views.CareersPageView.as_view(), name='careers'),
    path('blog/', views.BlogPageView.as_view(), name='blog'),
    path('games/', views.GamesPageView.as_view(), name='games'),
    path('contacts/', views.ContactsPageView.as_view(), name='contacts'),
    path('demo/', views.DemoPageView.as_view(), name='demo'),
]
