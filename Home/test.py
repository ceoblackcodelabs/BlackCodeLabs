# views.py
from django.conf import settings
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

def test_email_config(request):
    """Test endpoint to check email configuration"""
    info = []
    
    # Check email backend
    email_backend = getattr(settings, 'EMAIL_BACKEND', 'Not configured')
    info.append(f"EMAIL_BACKEND: {email_backend}")
    
    # Check other email settings
    email_settings = [
        'EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_USE_TLS',
        'EMAIL_HOST_USER', 'DEFAULT_FROM_EMAIL', 'CONTACT_NOTIFICATION_EMAIL'
    ]
    
    for setting in email_settings:
        if hasattr(settings, setting):
            value = getattr(settings, setting)
            # Mask passwords for security
            if 'PASSWORD' in setting:
                value = '***' if value else 'Not set'
            elif 'EMAIL_HOST_USER' in setting:
                value = value if value else 'Not set'
            info.append(f"{setting}: {value}")
        else:
            info.append(f"{setting}: Not configured")
    
    # Try to send a test email
    try:
        from django.core.mail import send_mail
        send_mail(
            subject='Test Email from BlackCodeLabs',
            message='This is a test email to check configuration.',
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'test@blackcodelabs.com'),
            recipient_list=['test@example.com'],
            fail_silently=True,
        )
        info.append("Test email sent (check console if using console backend)")
    except Exception as e:
        info.append(f"Test email failed: {e}")
    
    return HttpResponse("<br>".join(info))