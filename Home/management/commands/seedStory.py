# Home/management/commands/seed_success_stories.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from Home.models import ClientReview
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Seed the database with realistic client success stories and testimonials'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing reviews before seeding',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of success stories to create (default: 10)',
        )
        parser.add_argument(
            '--featured',
            type=int,
            default=3,
            help='Number of featured reviews (default: 3)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually saving',
        )

    def handle(self, *args, **options):
        clear_existing = options['clear']
        count = options['count']
        featured_count = options['featured']
        dry_run = options['dry_run']
        
        success_stories = [
            {
                'client_name': 'Robert Williams',
                'client_position': 'Chief Technology Officer',
                'client_company': 'TechGlobal Inc.',
                'review_text': 'BlackCode Labs transformed our entire data infrastructure. Their automation solutions saved us 40+ hours per week in manual work. The team was professional, responsive, and delivered beyond our expectations. Exceptional work!',
                'rating': 5,
                'is_featured': True,
            },
            {
                'client_name': 'Jennifer Martinez',
                'client_position': 'Operations Director',
                'client_company': 'RetailChain Pro',
                'review_text': 'The chatbot system they built for our customer service has reduced response time by 85%. Our customer satisfaction scores have never been higher. The implementation was seamless and the training provided was comprehensive.',
                'rating': 5,
                'is_featured': True,
            },
            {
                'client_name': 'Thomas Anderson',
                'client_position': 'Security Head',
                'client_company': 'SecureBank Ltd.',
                'review_text': 'Their security assessment identified vulnerabilities we had missed for years. The penetration testing was thorough and their recommendations were practical. Professional, thorough, and highly recommended for any financial institution.',
                'rating': 5,
                'is_featured': True,
            },
            {
                'client_name': 'Lisa Wong',
                'client_position': 'Startup Founder',
                'client_company': 'InnovateAI Solutions',
                'review_text': 'As a startup, we needed cost-effective solutions. BlackCode Labs delivered a custom AI model that exceeded our expectations at a fraction of the expected cost. Their team worked closely with us to understand our unique needs.',
                'rating': 5,
                'is_featured': False,
            },
            {
                'client_name': 'James Wilson',
                'client_position': 'IT Manager',
                'client_company': 'Manufacturing Corp',
                'review_text': 'The full-stack application they developed has streamlined our inventory management completely. The team was responsive and delivered ahead of schedule. We\'ve seen a 30% increase in operational efficiency since implementation.',
                'rating': 5,
                'is_featured': False,
            },
            {
                'client_name': 'Sarah Johnson',
                'client_position': 'Marketing Director',
                'client_company': 'Digital Growth Agency',
                'review_text': 'Their data analytics platform gave us insights that transformed our marketing strategy. The predictive models helped us increase conversion rates by 45%. The dashboard is intuitive and provides real-time data we can act on.',
                'rating': 4,
                'is_featured': False,
            },
            {
                'client_name': 'Michael Rodriguez',
                'client_position': 'CEO',
                'client_company': 'HealthTech Innovations',
                'review_text': 'BlackCode Labs developed a HIPAA-compliant patient management system for us. They handled all security requirements meticulously and delivered a robust solution that has improved our patient care delivery significantly.',
                'rating': 5,
                'is_featured': False,
            },
            {
                'client_name': 'Emily Chen',
                'client_position': 'Product Manager',
                'client_company': 'E-commerce Platform',
                'review_text': 'The automation system they built for order processing eliminated manual errors and sped up fulfillment by 60%. Their team was excellent at understanding our complex workflows and creating efficient solutions.',
                'rating': 5,
                'is_featured': False,
            },
            {
                'client_name': 'David Kim',
                'client_position': 'Operations Manager',
                'client_company': 'Logistics Solutions',
                'review_text': 'Their custom logistics tracking system integrated perfectly with our existing infrastructure. Real-time tracking has improved delivery accuracy to 99.8%. The support during implementation was outstanding.',
                'rating': 4,
                'is_featured': False,
            },
            {
                'client_name': 'Amanda Thompson',
                'client_position': 'HR Director',
                'client_company': 'Global Consulting Firm',
                'review_text': 'The employee portal and automation tools they developed have streamlined our HR processes dramatically. Onboarding time reduced by 70% and employee satisfaction with HR services increased significantly.',
                'rating': 5,
                'is_featured': False,
            },
            {
                'client_name': 'Brian O\'Connor',
                'client_position': 'Financial Controller',
                'client_company': 'Accounting Partners LLP',
                'review_text': 'Their financial automation system has reduced manual data entry by 90% and eliminated calculation errors. The audit trail feature is particularly impressive. ROI was achieved within the first 3 months.',
                'rating': 5,
                'is_featured': False,
            },
            {
                'client_name': 'Jessica Park',
                'client_position': 'Research Lead',
                'client_company': 'BioResearch Labs',
                'review_text': 'The data processing and analysis pipeline they built for our research team has accelerated our findings. What used to take weeks now takes hours. Their understanding of scientific data was exceptional.',
                'rating': 4,
                'is_featured': False,
            },
            {
                'client_name': 'Samuel Green',
                'client_position': 'Development Director',
                'client_company': 'Real Estate Developers',
                'review_text': 'Their project management and CRM system tailored for construction has improved our project completion times by 25%. The mobile app for field teams is particularly well-designed and reliable.',
                'rating': 5,
                'is_featured': False,
            },
            {
                'client_name': 'Olivia White',
                'client_position': 'Customer Experience Head',
                'client_company': 'Hospitality Group',
                'review_text': 'The customer feedback analysis system they implemented provides us with actionable insights in real-time. Our response to customer concerns has improved dramatically, leading to higher satisfaction scores.',
                'rating': 5,
                'is_featured': False,
            },
            {
                'client_name': 'Daniel Harris',
                'client_position': 'Supply Chain Manager',
                'client_company': 'Consumer Goods Inc.',
                'review_text': 'The supply chain optimization system they developed predicted disruptions before they happened. We avoided significant losses during the recent supply chain challenges thanks to their predictive models.',
                'rating': 5,
                'is_featured': False,
            },
        ]
        
        # Limit to requested count
        stories_to_create = success_stories[:count]
        
        if clear_existing:
            if dry_run:
                self.stdout.write(
                    self.style.WARNING('DRY RUN: Would delete all existing client reviews')
                )
            else:
                deleted_count, _ = ClientReview.objects.all().delete()
                self.stdout.write(
                    self.style.SUCCESS(f'Deleted {deleted_count} existing client reviews')
                )
        
        created_count = 0
        updated_count = 0
        
        for i, story_data in enumerate(stories_to_create):
            # Mark as featured based on position and featured_count
            if i < featured_count:
                story_data['is_featured'] = True
                story_data['display_order'] = 100 - i * 10
            else:
                story_data['is_featured'] = False
                story_data['display_order'] = (len(stories_to_create) - i) * 10
            
            # Add created_at with some variance (simulate reviews over time)
            days_ago = random.randint(1, 365)
            story_data['created_at'] = timezone.now() - timedelta(days=days_ago)
            
            # Check if review already exists
            existing_review = ClientReview.objects.filter(
                client_name=story_data['client_name'],
                client_company=story_data['client_company']
            ).first()
            
            if existing_review:
                if dry_run:
                    self.stdout.write(
                        self.style.WARNING(f'Would update: {story_data["client_name"]} from {story_data["client_company"]}')
                    )
                else:
                    for key, value in story_data.items():
                        if hasattr(existing_review, key):
                            setattr(existing_review, key, value)
                    existing_review.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Updated: {story_data["client_name"]} (ID: {existing_review.id})')
                    )
            else:
                if dry_run:
                    self.stdout.write(
                        self.style.SUCCESS(f'Would create: {story_data["client_name"]} - {story_data["client_position"]} at {story_data["client_company"]}')
                    )
                else:
                    # Remove created_at as it's auto-generated
                    story_data.pop('created_at', None)
                    review = ClientReview.objects.create(**story_data)
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Created: {story_data["client_name"]} (ID: {review.id})')
                    )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'\nDRY RUN SUMMARY:\n'
                    f'Would process: {len(stories_to_create)} success stories\n'
                    f'Featured reviews: {featured_count}\n'
                    f'Regular reviews: {len(stories_to_create) - featured_count}'
                )
            )
        else:
            total_in_db = ClientReview.objects.count()
            featured_in_db = ClientReview.objects.filter(is_featured=True).count()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nSEEDING COMPLETE:\n'
                    f'Created: {created_count}\n'
                    f'Updated: {updated_count}\n'
                    f'Total in database: {total_in_db}\n'
                    f'Featured reviews: {featured_in_db}\n'
                    f'Regular reviews: {total_in_db - featured_in_db}'
                )
            )