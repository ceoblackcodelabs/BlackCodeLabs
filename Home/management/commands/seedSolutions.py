from django.core.management.base import BaseCommand
from Home.models import Solution
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seed the database with initial technology solutions data'
    
    def handle(self, *args, **kwargs):
        solutions_data = [
            {
                'slug': 'development',
                'title': 'Web & App Development',
                'short_description': 'Build responsive, high-performance websites, mobile applications, and backend systems with modern technologies.',
                'detailed_description': 'Full-stack development services including frontend, backend, mobile apps, and e-commerce solutions.',
                'icon_class': 'fa-code',
                'z_index': 0,
                'features': """Responsive Website Design
E-commerce Platforms
Mobile Applications (iOS/Android)
Custom Backend Systems
Progressive Web Apps""",
                'cta_text': 'View Projects',
                'cta_link': '#',
                'display_order': 1,
            },
            {
                'slug': 'automation',
                'title': 'Process Automation',
                'short_description': 'Streamline operations with custom automation solutions, bot development, and workflow optimization systems.',
                'detailed_description': 'Automate repetitive tasks and optimize business processes with custom automation solutions.',
                'icon_class': 'fa-robot',
                'z_index': 1,
                'features': """Workflow Automation
Custom Bot Development
Data Entry Automation
Task Scheduling Systems
API Integration Automation""",
                'cta_text': 'Learn More',
                'cta_link': '#',
                'display_order': 2,
            },
            {
                'slug': 'data',
                'title': 'Data Intelligence',
                'short_description': 'Advanced data solutions including web scraping, analysis, predictive modeling, and business intelligence dashboards.',
                'detailed_description': 'Turn data into insights with our comprehensive data intelligence solutions.',
                'icon_class': 'fa-database',
                'z_index': 1,
                'features': """Web Data Extraction
Big Data Processing
Predictive Analytics
Interactive Dashboards
Custom AI Models""",
                'cta_text': 'Explore Solutions',
                'cta_link': '#',
                'display_order': 3,
            },
            {
                'slug': 'chatbots',
                'title': 'Chatbot Systems',
                'short_description': 'Intelligent conversational interfaces that enhance customer service and automate communication workflows.',
                'detailed_description': 'Build intelligent chatbots for customer support, lead generation, and more.',
                'icon_class': 'fa-comments',
                'z_index': 0,
                'features': """24/7 Customer Support
Multi-platform Integration
Natural Language Processing
Lead Generation Bots
Order Processing Automation""",
                'cta_text': 'View Demos',
                'cta_link': '#',
                'display_order': 4,
            },
            {
                'slug': 'security',
                'title': 'Security Solutions',
                'short_description': 'Comprehensive security assessments, bug bounty programs, and threat intelligence solutions.',
                'detailed_description': 'Protect your business with our comprehensive security solutions.',
                'icon_class': 'fa-shield-alt',
                'z_index': 0,
                'features': """Vulnerability Assessment
Bug Bounty Program Management
Threat Analysis & Monitoring
Security Audits
Incident Response Planning""",
                'cta_text': 'Get Assessment',
                'cta_link': '#',
                'display_order': 5,
            },
            {
                'slug': 'infrastructure',
                'title': 'Infrastructure & Systems',
                'short_description': 'CCTV installation, cable management, POS systems, and standalone enterprise solutions.',
                'detailed_description': 'Complete infrastructure solutions for your business needs.',
                'icon_class': 'fa-server',
                'z_index': 1,
                'features': """CCTV Security Systems
Network Cable Management
Custom POS Solutions
Standalone Business Systems
Hardware Integration""",
                'cta_text': 'Learn More',
                'cta_link': '#',
                'display_order': 6,
            },
            {
                'slug': 'api',
                'title': 'API Development',
                'short_description': 'Create robust, scalable, and secure APIs to connect your applications and services.',
                'detailed_description': 'Build powerful APIs to connect your systems and services.',
                'icon_class': 'fa-network-wired',
                'z_index': 1,
                'features': """RESTful API Design
GraphQL Implementation
API Documentation
Authentication & Authorization
WebSocket APIs""",
                'cta_text': 'Explore APIs',
                'cta_link': '#',
                'display_order': 7,
            },
            {
                'slug': 'training',
                'title': 'Technology Training',
                'short_description': 'Professional development courses and workshops in modern software development and data science.',
                'detailed_description': 'Upskill your team with our technology training programs.',
                'icon_class': 'fa-graduation-cap',
                'z_index': 1,
                'features': """Web Development Bootcamps
Data Science Workshops
Automation Training
Security Best Practices
Team Technology Upskilling""",
                'cta_text': 'View Courses',
                'cta_link': '/courses/',
                'display_order': 8,
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for solution_data in solutions_data:
            slug = solution_data.pop('slug')
            obj, created = Solution.objects.update_or_create(
                slug=slug,
                defaults=solution_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created solution: {obj.title}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'Updated solution: {obj.title}'))
        
        self.stdout.write(self.style.SUCCESS(
            f'\nSeeding complete! Created: {created_count}, Updated: {updated_count}, Total: {created_count + updated_count}'
        ))