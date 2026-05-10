# your_app/management/commands/seed_company_reviews.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from Users.models import Company, CompanyReview

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds CompanyReview model with 3 reviews for churchilkodhiambo@gmail.com\'s company'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting company reviews seeding...'))

        # Find the user by email
        try:
            user = User.objects.get(email='churchilkodhiambo@gmail.com')
            self.stdout.write(self.style.SUCCESS(f'✅ Found user: {user.full_name} ({user.email})'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ User with email churchilkodhiambo@gmail.com not found!'))
            self.stdout.write(self.style.WARNING('💡 Please ensure the user exists before running this command.'))
            return
        except User.MultipleObjectsReturned:
            self.stdout.write(self.style.WARNING('⚠️ Multiple users found with this email. Using the first one.'))
            user = User.objects.filter(email='churchilkodhiambo@gmail.com').first()

        # Find or create the company
        company, created = Company.objects.get_or_create(
            owner=user,
            defaults={
                'name': 'BlackCode Software Labs',
                'industry': 'Software Development',
                'location': 'Nairobi, Kenya',
                'description': 'Premium software development company specializing in web applications, mobile apps, and enterprise solutions.',
                'email': user.email,
                'phone': user.contact if user.contact else '+254712345678',
                'year_founded': 2019,
                'website': 'https://blackcodelabs.com'
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'✅ Created new software company: {company.name}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'✅ Found existing company: {company.name}'))

        # Clear existing reviews (optional - comment out if you want to keep old reviews)
        existing_count = CompanyReview.objects.filter(company_name=company).count()
        if existing_count > 0:
            self.stdout.write(self.style.WARNING(f'⚠️ Found {existing_count} existing reviews. Deleting them...'))
            CompanyReview.objects.filter(company_name=company).delete()
            self.stdout.write(self.style.SUCCESS('🗑️ Existing reviews deleted.'))

        # Create 3 different reviews with the new service field
        reviews_data = [
            {
                'name': 'Dr. James Mwangi',
                'email': 'james.mwangi@techinnovate.co.ke',
                'service': 'Custom CRM software solution with AI-powered analytics for customer relationship management',
                'review_text': """I have had the pleasure of working with BlackCode Software Labs on multiple projects over the past two years. Their technical expertise is exceptional, and they consistently deliver high-quality software solutions. The team is responsive, professional, and truly cares about their clients' success. They transformed our outdated legacy system into a modern, efficient platform that has saved us countless hours. I cannot recommend them enough for any software development needs.""",
                'rating': 5,
                'date': timezone.now().date() - timedelta(days=15)
            },
            {
                'name': 'Sarah Wanjiku Kimani',
                'email': 'sarah.kimani@swiftlogistics.ke',
                'service': 'Real-time logistics tracking and fleet management system with mobile integration',
                'review_text': """Working with BlackCode Software Labs was a game-changer for our logistics company. They developed a custom tracking system that integrates perfectly with our existing operations. The project was delivered on time and within budget. Their communication throughout the development process was excellent. The only minor hiccup was a small bug in the initial release, but their support team fixed it within hours. Overall, a great experience and value for money.""",
                'rating': 4,
                'date': timezone.now().date() - timedelta(days=30)
            },
            {
                'name': 'Michael Otieno Ochieng',
                'email': 'michael.ochieng@retailplus.co.ke',
                'service': 'Full e-commerce platform rebuild with payment gateway integration and inventory management system',
                'review_text': """BlackCode Software Labs rebuilt our entire e-commerce platform, and the results exceeded our expectations. The new site is fast, responsive, and user-friendly. Our sales have increased by 40% since the launch. Their team's attention to detail and innovative solutions set them apart from other developers we've worked with. They provided valuable insights that improved our business processes beyond just the technical implementation. Highly recommended for any serious business looking for quality software development.""",
                'rating': 5,
                'date': timezone.now().date() - timedelta(days=45)
            }
        ]

        # Create the reviews
        created_reviews = []
        for idx, review_data in enumerate(reviews_data, 1):
            try:
                review = CompanyReview.objects.create(
                    company_name=company,
                    name=review_data['name'],
                    email=review_data['email'],
                    service=review_data['service'],
                    review_text=review_data['review_text'],
                    rating=review_data['rating'],
                    date=review_data['date']
                )
                created_reviews.append(review)

                # Display star rating
                stars = '⭐' * review_data['rating']
                empty_stars = '☆' * (5 - review_data['rating'])

                self.stdout.write(f"\n{self.style.SUCCESS(f'✅ Review {idx}:')}")
                self.stdout.write(f"   {self.style.MIGRATE_HEADING(f'Reviewer: {review_data["name"]}')}")
                self.stdout.write(f"   {self.style.MIGRATE_HEADING(f'Email: {review_data["email"]}')}")
                self.stdout.write(f"   {self.style.MIGRATE_HEADING(f'Service: {review_data["service"]}')}")
                self.stdout.write(f"   {self.style.SUCCESS(f'Rating: {stars}{empty_stars} ({review_data["rating"]}/5)')}")
                self.stdout.write(f"   {self.style.MIGRATE_HEADING(f'Date: {review_data["date"]}')}")
                self.stdout.write(f"   {self.style.WARNING(f'Review preview: {review_data["review_text"][:120]}...')}")

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error creating review {idx}: {str(e)}'))

        # Display summary
        self.stdout.write("\n" + "="*70)
        self.stdout.write(self.style.SUCCESS("📊 SEEDING SUMMARY 📊"))
        self.stdout.write("="*70)
        self.stdout.write(self.style.SUCCESS(f"✅ Successfully created {len(created_reviews)} reviews for {company.name}"))

        # Calculate average rating
        if created_reviews:
            avg_rating = sum(r.rating for r in created_reviews) / len(created_reviews)
            self.stdout.write(self.style.SUCCESS(f"⭐ Average Rating: {avg_rating:.1f}/5 stars"))

            # Rating distribution
            rating_counts = {}
            for review in created_reviews:
                rating_counts[review.rating] = rating_counts.get(review.rating, 0) + 1

            self.stdout.write(self.style.MIGRATE_HEADING("\n📈 Rating Distribution:"))
            for rating in sorted(rating_counts.keys(), reverse=True):
                bar = "█" * rating_counts[rating]
                self.stdout.write(f"   {rating} stars: {bar} ({rating_counts[rating]} review{'s' if rating_counts[rating] > 1 else ''})")

        # Display all reviews in a formatted way
        self.stdout.write(self.style.MIGRATE_HEADING("\n📝 ALL REVIEWS:"))
        for idx, review in enumerate(created_reviews, 1):
            stars_display = '★' * review.rating + '☆' * (5 - review.rating)
            self.stdout.write(f"\n{self.style.SUCCESS(f'{idx}. {stars_display} ({review.rating}/5)')}")
            self.stdout.write(f"   {self.style.MIGRATE_HEADING(f'By: {review.name}')}")
            self.stdout.write(f"   {self.style.MIGRATE_HEADING(f'Service: {review.service}')}")
            self.stdout.write(f"   {self.style.WARNING(f'Date: {review.date}')}")
            self.stdout.write(f"   {review.review_text[:200]}{'...' if len(review.review_text) > 200 else ''}")

        self.stdout.write("\n" + "="*70)
        self.stdout.write(self.style.SUCCESS("🎉 Company reviews seeding completed successfully!"))
        self.stdout.write("="*70)


# Simpler version without styling (alternative)
class CommandSimple(BaseCommand):
    help = 'Seeds CompanyReview model with 3 reviews (simple version)'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Starting company reviews seeding...")

        # Find the user
        try:
            user = User.objects.get(email='churchilkodhiambo@gmail.com')
            self.stdout.write(f"✅ Found user: {user.full_name}")
        except User.DoesNotExist:
            self.stdout.write("❌ User not found!")
            return

        # Find or create company
        company, created = Company.objects.get_or_create(
            owner=user,
            defaults={
                'name': 'BlackCode Software Labs',
                'industry': 'Software Development',
                'location': 'Nairobi, Kenya',
                'description': 'Premium software development company',
                'email': user.email,
                'year_founded': 2019,
            }
        )

        if created:
            self.stdout.write(f"✅ Created new company: {company.name}")
        else:
            self.stdout.write(f"✅ Found existing company: {company.name}")

        # Clear existing reviews
        existing_count = CompanyReview.objects.filter(company_name=company).count()
        if existing_count > 0:
            self.stdout.write(f"🗑️ Clearing {existing_count} existing reviews...")
            CompanyReview.objects.filter(company_name=company).delete()

        # Create reviews with service field
        reviews = [
            CompanyReview(
                company_name=company,
                name='Dr. James Mwangi',
                email='james.mwangi@techinnovate.co.ke',
                service='Custom CRM software solution with AI-powered analytics for customer relationship management',
                review_text='Exceptional software development company! Their technical expertise and professionalism are outstanding. They delivered our project on time and exceeded our expectations. Highly recommended!',
                rating=5,
                date=timezone.now().date() - timedelta(days=15)
            ),
            CompanyReview(
                company_name=company,
                name='Sarah Wanjiku Kimani',
                email='sarah.kimani@swiftlogistics.ke',
                service='Real-time logistics tracking and fleet management system with mobile integration',
                review_text='Great experience working with this team. They developed a custom tracking system for our logistics company. Very responsive and professional. Would definitely work with them again.',
                rating=4,
                date=timezone.now().date() - timedelta(days=30)
            ),
            CompanyReview(
                company_name=company,
                name='Michael Otieno Ochieng',
                email='michael.ochieng@retailplus.co.ke',
                service='Full e-commerce platform rebuild with payment gateway integration and inventory management system',
                review_text='BlackCode transformed our e-commerce platform. The new site is fast, modern, and user-friendly. Our sales increased significantly after the relaunch. Excellent work!',
                rating=5,
                date=timezone.now().date() - timedelta(days=45)
            )
        ]

        # Bulk create reviews
        CompanyReview.objects.bulk_create(reviews)

        self.stdout.write(f"✅ Created {len(reviews)} reviews for {company.name}")

        # Show summary
        all_reviews = CompanyReview.objects.filter(company_name=company)
        avg_rating = sum(r.rating for r in all_reviews) / all_reviews.count()
        self.stdout.write(f"⭐ Average Rating: {avg_rating:.1f}/5 stars")

        # Display each review
        self.stdout.write("\n📝 Review Details:")
        for review in all_reviews:
            self.stdout.write(f"\n   Name: {review.name}")
            self.stdout.write(f"   Service: {review.service[:80]}...")
            self.stdout.write(f"   Rating: {review.rating}/5 stars")
            self.stdout.write(f"   Review: {review.review_text[:100]}...")

        self.stdout.write("\n🎉 Seeding completed!")