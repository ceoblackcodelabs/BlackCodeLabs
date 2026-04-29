import qrcode

# Get URL from user input
url = input("Enter the URL: ")

# Create QR code instance
qr = qrcode.QRCode(
    version=1,  # Controls size (1-40)
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,  # Size of each box in pixels
    border=4,  # Border size (boxes)
)

# Add data to QR code
qr.add_data(url)
qr.make(fit=True)

# Create the QR code image
qr_image = qr.make_image(fill_color="black", back_color="white")

# Save the image
qr_image.save("qr_code.png")

print("QR code generated and saved as 'qr_code.png'")