# your_app_name/management/commands/seed_merch.py

from django.core.management.base import BaseCommand
from BCL.models import Merch

class Command(BaseCommand):
    help = 'Seed merchandise items into the database'

    def handle(self, *args, **options):
        merch_items = [
            {
                'name': 'Signature Hoodie',
                'description': 'Premium quality hoodie with BCL PRODUCTION embroidered logo. Made from 100% organic cotton. Features a kangaroo pocket and adjustable hood.',
                'price': 89.00,
            },
            {
                'name': 'Classic Tee',
                'description': 'Essential BCL PRODUCTION t-shirt. Screen-printed logo on front. 100% combed ring-spun cotton for maximum comfort.',
                'price': 45.00,
            },
            {
                'name': 'Logo Cap',
                'description': 'Adjustable snapback cap with embroidered BCL logo. One size fits all. Premium cotton twill construction.',
                'price': 35.00,
            },
            {
                'name': 'Bomber Jacket',
                'description': 'Limited edition satin bomber jacket. Embroidered patches on chest and back. Ribbed cuffs and hem.',
                'price': 120.00,
            },
            {
                'name': 'Winter Beanie',
                'description': 'Warm knit beanie with woven BCL patch. Acrylic wool blend. One size fits most.',
                'price': 25.00,
            },
            {
                'name': 'Duffle Bag',
                'description': 'Water-resistant duffle bag with BCL branding. Multiple compartments and adjustable shoulder strap.',
                'price': 65.00,
            },
        ]

        for item in merch_items:
            merch, created = Merch.objects.get_or_create(
                name=item['name'],
                defaults={
                    'description': item['description'],
                    'price': item['price'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created: {merch.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Already exists: {merch.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded merchandise items!'))