from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="list"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="detail"),
    path("post/<slug:slug>/comment/", views.CommentCreateView.as_view(), name="comment_create"),
    path("post/<slug:slug>/like/", views.PostLikeView.as_view(), name="post_like"),
    path("comment/<int:pk>/like/", views.CommentLikeView.as_view(), name="comment_like"),
]
