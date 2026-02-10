from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Web Development'),
        ('mobile', 'Mobile Application'),
        ('desktop', 'Desktop Application'),
        ('ai', 'Artificial Intelligence'),
        ('iot', 'IoT & Hardware'),
        ('data', 'Data Science'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=1500.00,
        validators=[MinValueValidator(0)]
    )
    documentation_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=500.00,
        validators=[MinValueValidator(0)]
    )
    coding_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=1000.00,
        validators=[MinValueValidator(0)]
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class ProjectRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    project = models.ForeignKey(
        Project, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="Leave blank for custom project"
    )
    custom_title = models.CharField(max_length=200)
    description = models.TextField()
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+254712345678'. Up to 15 digits allowed."
            )
        ]
    )
    email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.custom_title} - {self.email}"
    
    class Meta:
        ordering = ['-created_at']