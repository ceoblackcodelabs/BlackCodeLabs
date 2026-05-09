import qrcode
import io
import base64
from PIL import Image, ImageDraw
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from Users.models import User, SeekerProfile
from io import BytesIO
from django.http import HttpResponse
import traceback
from colorama import Fore, Style, Back



def generate_vcard_qr_code(seeker_profile):
    """
    Generate a vCard QR code with custom brand colors using real seeker data
    """
    try:
        print(f"{Fore.GREEN}=== QR CODE DEBUG START ==={Style.RESET_ALL}")
        print(f"{Back.CYAN}Generating QR for: {seeker_profile.user.full_name}{Style.RESET_ALL}")

        # Create vCard content with actual seeker data
        vcard_content = f"""BEGIN:VCARD
VERSION:3.0
FN:{seeker_profile.user.full_name or 'Professional'}
ORG:TenaWork
TITLE:{seeker_profile.get_primary_trade_display() or 'Skilled Professional'}
TEL:{getattr(seeker_profile.user, 'contact', 'Not provided')}
EMAIL:{seeker_profile.user.email}
URL:https://blackcodelab.com//auth/find-talent/Resume/{seeker_profile.pk}/
ADR:;;{seeker_profile.location or 'Location not specified'};;;
NOTE:Available for {seeker_profile.get_primary_trade_display() or 'professional'} projects
END:VCARD"""

        print(f"{Back.CYAN}vCard content created with real data{Style.RESET_ALL}")

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=3,
        )
        qr.add_data(vcard_content)
        qr.make(fit=True)

        print(f"{Back.CYAN}QR code data added successfully{Style.RESET_ALL}")

        # Create QR code with your brand colors
        qr_image = qr.make_image(
            fill_color="#2563eb",  # --primary (blue)
            back_color="#f8fafc"   # --light (light gray)
        ).convert('RGB')

        print(f"{Back.CYAN}QR image created with brand colors{Style.RESET_ALL}")

        # Add a stylish border
        border_size = 15
        original_width, original_height = qr_image.size
        new_width = original_width + (border_size * 2)
        new_height = original_height + (border_size * 2)

        # Create new image with colored border
        bordered_image = Image.new('RGB', (new_width, new_height), '#f59e0b')  # --secondary (amber)
        bordered_image.paste(qr_image, (border_size, border_size))

        # Convert to base64
        buffer = io.BytesIO()
        bordered_image.save(buffer, format='PNG', quality=100)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        buffer.close()

        print(f"{Back.CYAN}Base64 encoding successful{Style.RESET_ALL}")
        print(f"{Fore.GREEN}=== QR CODE DEBUG END ==={Style.RESET_ALL}")

        return f"data:image/png;base64,{image_base64}"

    except Exception as e:
        print(f"=== QR CODE ERROR ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return None



def digital_card_qr_code(theModel, username, request=None):
    """
    Generate a digital card QR code with custom brand colors using real seeker data

    Args:
        theModel: The model class (e.g., SeekerProfile, CompanyProfile)
        username: The username of the user
        request: HttpRequest object (required for absolute URLs)
    """
    try:
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(theModel, user=user)

        print(f"{Fore.GREEN}\n=== DIGITAL CARD QR CODE DEBUG START ==={Style.RESET_ALL}")
        print(f"{Back.CYAN}Generating digital card QR for: {profile.user.full_name}{Style.RESET_ALL}")
        print(f"{Back.CYAN}Profile PK: {profile.pk}{Style.RESET_ALL}")

        # Check if request is provided
        if request is None:
            print(f"{Fore.RED}ERROR: Request object is required for building absolute URIs{Style.RESET_ALL}")
            return None

        # Create digital card content with actual seeker data
        # Generate QR Code as base64 using the request object
        qr_url = request.build_absolute_uri(reverse('profile', kwargs={'pk': profile.pk}))
        print(f"QR URL: {qr_url}")

        qr = qrcode.QRCode(
            version=1,
            box_size=5,
            border=2,
            error_correction=qrcode.constants.ERROR_CORRECT_M
        )
        qr.add_data(qr_url)
        qr.make(fit=True)

        # Use brand colors instead of black/white
        img = qr.make_image(
            fill_color="#2563eb",  # Brand blue color
            back_color="#ffffff"   # White background
        )

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_image_base64 = base64.b64encode(buffer.getvalue()).decode()
        buffer.close()

        print(f"Digital card QR generated successfully - length: {len(qr_image_base64)}")
        print(f"{Fore.GREEN}=== DIGITAL CARD QR CODE DEBUG END ==={Style.RESET_ALL}")

        # Return as data URI for use in img src
        return f"data:image/png;base64,{qr_image_base64}"

    except Exception as e:
        print(f"=== DIGITAL CARD QR CODE ERROR ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return None