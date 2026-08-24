from django.apps import AppConfig


class BlogsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Blogs"

    def ready(self):
        from . import signals  # noqa: F401
