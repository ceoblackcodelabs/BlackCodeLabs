from django.conf import settings
from django.db import models


class GeneratedDocument(models.Model):
    """A document generated from the Studio forms.

    The form payload (`data`) and the rendered PDF (`pdf`) are both stored in the
    database: the PDF is the backup copy, `data` lets us edit and regenerate it.
    The PDF is deliberately NOT a file under MEDIA_ROOT, because that folder is
    served publicly; documents are only reachable through staff-only views.
    """

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("sent", "Sent"),
        ("accepted", "Accepted / Paid"),
        ("declined", "Declined / Cancelled"),
    ]

    doc_type = models.CharField(max_length=30, db_index=True)
    reference = models.CharField(max_length=40, unique=True)
    title = models.CharField(max_length=200)
    client_name = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="draft")

    amount = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True,
                                 help_text="Total value of the document (see each document type for how it is worked out)")
    currency = models.CharField(max_length=4, default="KES")

    data = models.JSONField(default=dict)
    pdf = models.BinaryField(editable=False)
    revision = models.PositiveIntegerField(default=1)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                   on_delete=models.SET_NULL, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["doc_type", "-created_at"]),
                   models.Index(fields=["status"])]

    def __str__(self):
        return f"{self.reference} - {self.client_name or self.title}"

    @property
    def filename(self):
        return f"{self.reference}.pdf"
