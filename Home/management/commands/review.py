# yourapp/management/commands/seed_reviews.py

import random
from django.core.management.base import BaseCommand
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from Home.models import ClientReview

from io import BytesIO
from PIL import Image, ImageDraw
import os


class Command(BaseCommand):
    help = 'Seed ClientReview model with sample data for BlackCodeLabs'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed ClientReview data...'))

        # Clear existing reviews (optional - uncomment if you want to replace data)
        # ClientReview.objects.all().delete()
        # self.stdout.write('Cleared existing reviews.')

        # Sample review data
        reviews_data = [
            {
                'client_name': 'Sarah Johnson',
                'client_position': 'CTO',
                'client_company': 'TechInnovate Solutions',
                'review_text': 'BlackCodeLabs transformed our digital infrastructure. Their team delivered a scalable cloud solution that reduced our operational costs by 40%. The professionalism and technical expertise were outstanding.',
                'rating': 5,
                'is_featured': True,
                'display_order': 1,
            },
            {
                'client_name': 'Michael Chen',
                'client_position': 'Product Director',
                'client_company': 'FinTech Global',
                'review_text': 'Working with BlackCodeLabs was a game-changer for our fintech platform. They built a secure, high-performance system that our users love. The attention to security and compliance was impressive.',
                'rating': 5,
                'is_featured': True,
                'display_order': 2,
            },
            {
                'client_name': 'Dr. Emily Rodriguez',
                'client_position': 'Head of Innovation',
                'client_company': 'HealthTech Dynamics',
                'review_text': 'The AI-powered analytics dashboard BlackCodeLabs created for us has revolutionized how we process patient data. Their expertise in machine learning and healthcare technology is exceptional.',
                'rating': 5,
                'is_featured': True,
                'display_order': 3,
            },
            {
                'client_name': 'David Omondi',
                'client_position': 'CEO',
                'client_company': 'AfriCommerce',
                'review_text': 'BlackCodeLabs delivered our e-commerce platform ahead of schedule and under budget. The mobile-first design and seamless payment integration have boosted our sales by 65%. Highly recommended!',
                'rating': 5,
                'is_featured': False,
                'display_order': 4,
            },
            {
                'client_name': 'Priya Patel',
                'client_position': 'Operations Manager',
                'client_company': 'LogisticsPro',
                'review_text': 'The custom ERP system built by BlackCodeLabs has streamlined our entire supply chain. Real-time tracking and automated reporting have saved us countless hours. Excellent support team!',
                'rating': 4,
                'is_featured': False,
                'display_order': 5,
            },
            {
                'client_name': 'James Wilson',
                'client_position': 'Marketing Director',
                'client_company': 'DigitalEdge Agency',
                'review_text': 'BlackCodeLabs developed a powerful CRM that integrated perfectly with our existing tools. The lead scoring and automation features have increased our conversion rate by 50%.',
                'rating': 5,
                'is_featured': False,
                'display_order': 6,
            },
            {
                'client_name': 'Grace Muthoni',
                'client_position': 'Founder',
                'client_company': 'GreenEnergy Kenya',
                'review_text': 'From concept to deployment, BlackCodeLabs was with us every step of the way. Their IoT solution for monitoring solar installations has given us unprecedented insights into energy usage.',
                'rating': 5,
                'is_featured': False,
                'display_order': 7,
            },
            {
                'client_name': 'Robert Taylor',
                'client_position': 'VP of Engineering',
                'client_company': 'CloudScale Systems',
                'review_text': 'The DevOps and cloud architecture expertise at BlackCodeLabs is top-notch. They helped us migrate to a microservices architecture that scales effortlessly. Truly world-class engineers.',
                'rating': 5,
                'is_featured': False,
                'display_order': 8,
            },
            {
                'client_name': 'Isabella Santos',
                'client_position': 'Education Technology Lead',
                'client_company': 'EduFuture',
                'review_text': 'Our learning management system built by BlackCodeLabs has been adopted by over 50 schools. The intuitive UI and robust backend handle thousands of concurrent users seamlessly.',
                'rating': 4,
                'is_featured': False,
                'display_order': 9,
            },
            {
                'client_name': 'Thomas Anderson',
                'client_position': 'Security Analyst',
                'client_company': 'CyberGuard Inc.',
                'review_text': 'BlackCodeLabs conducted a thorough security audit and penetration testing for our systems. Their detailed report and actionable recommendations significantly improved our security posture.',
                'rating': 5,
                'is_featured': False,
                'display_order': 10,
            },
        ]

        # Create profile pictures
        profile_pictures = self.create_sample_images()

        # Create reviews
        created_count = 0
        for idx, review_data in enumerate(reviews_data):
            # Check if review already exists (optional - by client name and company)
            existing_review = ClientReview.objects.filter(
                client_name=review_data['client_name'],
                client_company=review_data['client_company']
            ).first()

            if not existing_review:
                # Assign a profile picture (cycle through available images)
                picture_key = idx % len(profile_pictures)
                picture = profile_pictures[picture_key]

                review = ClientReview(
                    client_name=review_data['client_name'],
                    client_position=review_data['client_position'],
                    client_company=review_data['client_company'],
                    client_picture=picture,
                    review_text=review_data['review_text'],
                    rating=review_data['rating'],
                    is_featured=review_data['is_featured'],
                    display_order=review_data['display_order'],
                    created_at=timezone.now()
                )
                review.save()
                created_count += 1
                self.stdout.write(f'✓ Created review for {review_data["client_name"]}')
            else:
                self.stdout.write(f'⚠ Review for {review_data["client_name"]} already exists, skipping...')

        # Display summary
        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully seeded {created_count} client reviews for BlackCodeLabs!'))
        self.stdout.write(self.style.SUCCESS(f'📊 Total reviews in database: {ClientReview.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'⭐ Featured reviews: {ClientReview.objects.filter(is_featured=True).count()}'))

    def create_sample_images(self):
        """Create sample profile pictures programmatically"""
        from django.core.files.base import ContentFile

        pictures = []
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22', '#34495e']
        initials = ['SJ', 'MC', 'ER', 'DO', 'PP', 'JW', 'GM', 'RT', 'IS', 'TA']

        for i, (color, initials_text) in enumerate(zip(colors, initials)):
            # Create a simple colored image with initials
            img = Image.new('RGB', (400, 400), color=color)
            draw = ImageDraw.Draw(img)

            # Get font (use default font)
            try:
                from PIL import ImageFont
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
            except:
                font = ImageFont.load_default()

            # Get text size and position
            bbox = draw.textbbox((0, 0), initials_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            x = (400 - text_width) // 2
            y = (400 - text_height) // 2

            # Draw white text
            draw.text((x, y), initials_text, fill='white', font=font)

            # Save to bytes
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)

            # Create Django file
            filename = f'client_{i+1}_{initials_text.lower()}.png'
            picture = SimpleUploadedFile(
                filename,
                img_byte_arr.read(),
                content_type='image/png'
            )
            pictures.append(picture)

        return pictures


# Alternative: Simple version without PIL dependency
class CommandSimple(BaseCommand):
    help = 'Seed ClientReview model with sample data (simple version without image generation)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding ClientReview data for BlackCodeLabs...'))

        reviews_data = [
            {
                'client_name': 'Sarah Johnson',
                'client_position': 'CTO',
                'client_company': 'TechInnovate Solutions',
                'review_text': 'BlackCodeLabs transformed our digital infrastructure. Their team delivered a scalable cloud solution that reduced our operational costs by 40%.',
                'rating': 5,
                'is_featured': True,
                'display_order': 1,
            },
            # ... add more review data as above
        ]

        # Note: For client_picture, you'll need to manually add images
        # or create a placeholder. You can skip the image field or use a default.

        for review_data in reviews_data:
            review, created = ClientReview.objects.get_or_create(
                client_name=review_data['client_name'],
                client_company=review_data['client_company'],
                defaults={
                    'client_position': review_data['client_position'],
                    'review_text': review_data['review_text'],
                    'rating': review_data['rating'],
                    'is_featured': review_data['is_featured'],
                    'display_order': review_data['display_order'],
                    # 'client_picture': 'default_avatar.png',  # Use a default image
                }
            )
            if created:
                self.stdout.write(f'✓ Created review for {review_data["client_name"]}')

        self.stdout.write(self.style.SUCCESS(f'✅ Successfully seeded ClientReview data for BlackCodeLabs!'))