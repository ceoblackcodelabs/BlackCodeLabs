import qrcode
import random
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

def create_gradient_background(width, height, color1, color2):
    """Create a gradient background"""
    gradient = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(gradient)

    for i in range(height):
        ratio = i / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, i), (width, i)], fill=(r, g, b, 100))

    return gradient

def generate_random_colors():
    """Generate random but harmonious colors"""
    # Random color schemes: 'vibrant', 'pastel', 'neon', 'dark'
    schemes = ['vibrant', 'pastel', 'neon', 'dark']
    scheme = random.choice(schemes)

    if scheme == 'vibrant':
        colors = [
            (random.randint(200, 255), random.randint(0, 100), random.randint(0, 100)),  # Red-ish
            (random.randint(0, 100), random.randint(200, 255), random.randint(0, 100)),  # Green-ish
            (random.randint(0, 100), random.randint(0, 100), random.randint(200, 255)),  # Blue-ish
        ]
    elif scheme == 'pastel':
        colors = [
            (random.randint(180, 220), random.randint(150, 200), random.randint(150, 200)),
            (random.randint(150, 200), random.randint(180, 220), random.randint(150, 200)),
            (random.randint(150, 200), random.randint(150, 200), random.randint(180, 220)),
        ]
    elif scheme == 'neon':
        colors = [
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        ]
    else:  # dark
        colors = [
            (random.randint(50, 100), random.randint(0, 50), random.randint(0, 50)),
            (random.randint(0, 50), random.randint(50, 100), random.randint(0, 50)),
            (random.randint(0, 50), random.randint(0, 50), random.randint(50, 100)),
        ]

    return random.choice(colors), random.choice(colors)

# Get URL from user input
url = input("Enter the URL: ")
name = input("Enter a name for the QR code (optional): ")
if name:
    name = name.strip().replace(" ", "_")
else:
    name = f"qr_{random.randint(1000, 9999)}"

# Generate random colors
primary_color, secondary_color = generate_random_colors()
bg_color1, bg_color2 = generate_random_colors()

print(f"🎨 Color scheme generated!")

# Create QR code
qr = qrcode.QRCode(
    version=3,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

qr.add_data(url)
qr.make(fit=True)

# Create base QR
qr_base = qr.make_image(fill_color="black", back_color="white").convert('RGBA')

# Create gradient background
width, height = qr_base.size
background = create_gradient_background(width, height, bg_color1, bg_color2)

# Apply colors to QR data
qr_data = qr_base.load()
for y in range(height):
    for x in range(width):
        if qr_data[x, y][0] < 128:  # If it's black (QR data)
            # Create gradient effect on QR data too
            ratio = (x + y) / (width + height)
            r = int(primary_color[0] * (1 - ratio) + secondary_color[0] * ratio)
            g = int(primary_color[1] * (1 - ratio) + secondary_color[1] * ratio)
            b = int(primary_color[2] * (1 - ratio) + secondary_color[2] * ratio)
            qr_data[x, y] = (r, g, b, 255)

# Composite images
final = Image.alpha_composite(background, qr_base)
final = final.filter(ImageFilter.SMOOTH)

# Save
output_filename = f"./QRs/{name}.png"
final.save(output_filename, "PNG")

print(f"✨ Supreme-style QR code saved as '{output_filename}'")
print(f"🎨 Random color scheme applied!")