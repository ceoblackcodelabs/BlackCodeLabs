"""
URL configuration for BlackCodeLabs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from Home import views as Home_views
from Home.sitemaps import sitemaps

urlpatterns = [
    path('devAdmin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('projects/', include('Pitchs.urls')),
    path("BCL/", include("BCL.urls")),
    path("Blogs/", include("Blogs.urls")),
    path("affiliate/", include(("Affiliate.urls", "affiliate"), namespace="affiliate")),
    path('robots.txt', Home_views.robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('Home.urls')),
    path('auth/', include('Users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'Home.views.error_400'
handler403 = 'Home.views.error_403'
handler404 = 'Home.views.error_404'
handler500 = 'Home.views.error_500'