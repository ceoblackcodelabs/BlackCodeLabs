from django.db import models


class AffiliateApplication(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    AUDIENCE_CHOICES = [
        ("under_1k", "Under 1,000"),
        ("1k_10k", "1,000 - 10,000"),
        ("10k_50k", "10,000 - 50,000"),
        ("50k_plus", "50,000+"),
    ]

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    website_or_social = models.URLField(blank=True, help_text="Website, YouTube, Instagram, TikTok, etc.")
    audience_size = models.CharField(max_length=20, choices=AUDIENCE_CHOICES, blank=True)
    promotion_channels = models.CharField(
        max_length=300, blank=True,
        help_text="Comma-separated, e.g. Blog, YouTube, Instagram, Email list"
    )
    strategy = models.TextField(blank=True, help_text="How they plan to promote BlackCodeLabs")

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Affiliate Application"
        verbose_name_plural = "Affiliate Applications"

    def __str__(self):
        return f"{self.full_name} ({self.email})"
