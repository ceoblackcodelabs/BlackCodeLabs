# Home/management/commands/seed_services.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from Home.models import TechServices
import json

class Command(BaseCommand):
    help = 'Seed the database with default tech services data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing services before seeding',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually saving',
        )

    def handle(self, *args, **options):
        services_data = [
            {
                'icon': '<i class="fas fa-code"></i>',
                'name': 'Full-Stack Development',
                'description': 'Custom websites, applications, and backend systems built with cutting-edge technologies tailored to your business needs.'
            },
            {
                'icon': '<i class="fas fa-robot"></i>',
                'name': 'Process Automation',
                'description': 'Streamline operations with custom automation solutions, bot development, and workflow optimization systems.'
            },
            {
                'icon': '<i class="fas fa-chart-line"></i>',
                'name': 'Data Intelligence',
                'description': 'Advanced data scraping, analysis, and predictive modeling that turns information into actionable business insights.'
            },
            {
                'icon': '<i class="fas fa-comments"></i>',
                'name': 'Chatbot Systems',
                'description': 'Intelligent conversational interfaces that enhance customer service and automate communication workflows.'
            },
            {
                'icon': '<i class="fas fa-tools"></i>',
                'name': 'Custom AI Solutions',
                'description': 'Build specialized AI tools and machine learning models designed to solve your unique business challenges.'
            },
            {
                'icon': '<i class="fas fa-shield-alt"></i>',
                'name': 'Security & Threat Analysis',
                'description': 'Comprehensive security assessments, bug bounty programs, and threat intelligence solutions.'
            },
            {
                'icon': '<i class="fas fa-server"></i>',
                'name': 'Infrastructure & Systems',
                'description': 'CCTV installation, cable management, POS systems, and standalone enterprise solutions.'
            },
            {
                'icon': '<i class="fas fa-graduation-cap"></i>',
                'name': 'Technology Training',
                'description': 'Professional development courses and workshops in modern software development and data science.'
            }
        ]

        dry_run = options['dry_run']
        clear_existing = options['clear']
        
        if clear_existing:
            if dry_run:
                self.stdout.write(
                    self.style.WARNING('DRY RUN: Would delete all existing services')
                )
            else:
                deleted_count, _ = TechServices.objects.all().delete()
                self.stdout.write(
                    self.style.SUCCESS(f'Deleted {deleted_count} existing services')
                )
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        
        for service_data in services_data:
            name = service_data['name']
            
            # Check if service already exists
            existing_service = TechServices.objects.filter(name=name).first()
            
            if existing_service:
                # Update existing service
                if not dry_run:
                    existing_service.icon = service_data['icon']
                    existing_service.description = service_data['description']
                    existing_service.save()
                    updated_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Would update: {name}')
                    )
                    skipped_count += 1
            else:
                # Create new service
                if not dry_run:
                    TechServices.objects.create(**service_data)
                    created_count += 1
                else:
                    self.stdout.write(
                        self.style.SUCCESS(f'Would create: {name}')
                    )
                    skipped_count += 1
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'\nDRY RUN SUMMARY:\n'
                    f'Would create: {len(services_data) - skipped_count}\n'
                    f'Would skip: {skipped_count}\n'
                    f'Total services in data: {len(services_data)}'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nSEEDING COMPLETE:\n'
                    f'Created: {created_count}\n'
                    f'Updated: {updated_count}\n'
                    f'Total in database: {TechServices.objects.count()}'
                )
            )