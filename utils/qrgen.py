import qrcode
import io
import base64
from PIL import Image, ImageDraw

def generate_vcard_qr_code(seeker_profile):
    """
    Generate a vCard QR code with custom brand colors using real seeker data
    """
    try:
        print("=== QR CODE DEBUG START ===")
        print(f"Generating QR for: {seeker_profile.user.full_name}")

        # Create vCard content with actual seeker data
        vcard_content = f"""BEGIN:VCARD
VERSION:3.0
FN:{seeker_profile.user.full_name or 'Professional'}
ORG:TenaWork
TITLE:{seeker_profile.get_primary_trade_display() or 'Skilled Professional'}
TEL:{getattr(seeker_profile.user, 'contact', 'Not provided')}
EMAIL:{seeker_profile.user.email}
URL:https://tenawork.com
ADR:;;{seeker_profile.location or 'Location not specified'};;;
NOTE:Available for {seeker_profile.get_primary_trade_display() or 'professional'} projects
END:VCARD"""

        print(f"vCard content created with real data")

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=3,
        )
        qr.add_data(vcard_content)
        qr.make(fit=True)

        print("QR code data added successfully")

        # Create QR code with your brand colors
        qr_image = qr.make_image(
            fill_color="#2563eb",  # --primary (blue)
            back_color="#f8fafc"   # --light (light gray)
        ).convert('RGB')

        print("QR image created with brand colors")

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

        print(f"Base64 encoding successful")
        print("=== QR CODE DEBUG END ===")

        return f"data:image/png;base64,{image_base64}"

    except Exception as e:
        print(f"=== QR CODE ERROR ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return None