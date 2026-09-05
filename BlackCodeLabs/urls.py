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
import re

from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve as serve_static_file
from django.contrib.sitemaps.views import sitemap

from Home import views as Home_views
from Home.sitemaps import sitemaps

urlpatterns = [
    path('devAdmin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('projects/', include('Pitchs.urls')),
    path("Blogs/", include("Blogs.urls")),
    path("affiliate/", include(("Affiliate.urls", "affiliate"), namespace="affiliate")),
    path('robots.txt', Home_views.robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('Home.urls')),
    path('auth/', include('Users.urls')),
]

# Serve MEDIA_ROOT (user uploads: portfolio covers, blog images, client
# pictures, etc.) directly through Django.
#
# NOTE: django.conf.urls.static.static() is deliberately NOT used here.
# It contains a hard-coded check that registers NO url pattern at all
# whenever settings.DEBUG is False — regardless of any condition you wrap
# around the call. That's what was silently 404-ing every /media/ URL in
# production while working fine on localhost (DEBUG=True there).
#
# Wiring django.views.static.serve directly, gated by our own explicit
# flag, avoids that trap and makes the behavior obvious/toggleable.
if settings.SERVE_MEDIA_VIA_DJANGO:
    _media_url_path = settings.MEDIA_URL.lstrip("/")
    urlpatterns += [
        re_path(
            r"^%s(?P<path>.*)$" % re.escape(_media_url_path),
            serve_static_file,
            {"document_root": settings.MEDIA_ROOT},
        ),
    ]

handler400 = 'Home.views.error_400'
handler403 = 'Home.views.error_403'
handler404 = 'Home.views.error_404'
handler500 = 'Home.views.error_500'