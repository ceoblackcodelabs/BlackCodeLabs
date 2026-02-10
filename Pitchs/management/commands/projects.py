import random
from django.core.management.base import BaseCommand
from Pitchs.models import Project

class Command(BaseCommand):
    help = 'Generate 50 random website project ideas for final year students'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Generating 50 random projects...'))
        
        # Clear existing projects (optional)
        # Project.objects.all().delete()
        
        # Project templates
        project_types = [
            "Management System",
            "E-commerce Platform",
            "Social Network",
            "Learning Platform",
            "Booking System",
            "Analytics Dashboard",
            "Mobile Application",
            "AI Assistant",
            "IoT System",
            "Data Analysis Tool"
        ]
        
        industries = [
            "Healthcare", "Education", "Finance", "Retail", "Hospitality",
            "Agriculture", "Transportation", "Entertainment", "Real Estate",
            "Manufacturing", "Energy", "Government", "Non-profit"
        ]
        
        features = [
            "with real-time notifications",
            "with AI-powered recommendations",
            "with mobile app integration",
            "with data visualization",
            "with secure payment processing",
            "with user authentication",
            "with admin dashboard",
            "with reporting tools",
            "with API integration",
            "with cloud storage"
        ]
        
        descriptions = [
            "A comprehensive solution designed to streamline operations and improve efficiency.",
            "An innovative platform that leverages cutting-edge technology to solve real-world problems.",
            "User-friendly interface with robust backend functionality for optimal performance.",
            "Scalable architecture that can grow with your business needs.",
            "Secure and reliable system built with industry best practices.",
            "Customizable features to meet specific organizational requirements.",
            "Integrated analytics for data-driven decision making.",
            "Multi-platform support for maximum accessibility.",
            "Automated processes to reduce manual work and errors.",
            "Collaborative features for team coordination and communication."
        ]
        
        categories = ['web', 'mobile', 'desktop', 'ai', 'iot', 'data']
        
        created_count = 0
        for i in range(1, 51):
            # Generate unique project title
            industry = random.choice(industries)
            project_type = random.choice(project_types)
            feature = random.choice(features)
            
            title = f"{industry} {project_type} {feature}"
            
            # Check if title already exists
            if Project.objects.filter(title=title).exists():
                title = f"{industry} {project_type} {feature} v{i}"
            
            # Generate description
            base_desc = random.choice(descriptions)
            description = f"{base_desc} This system includes features like user management, data tracking, and reporting capabilities. Perfect for {industry.lower()} organizations looking to digitalize their operations."
            
            # Random category
            category = random.choice(categories)
            
            # Random pricing (around 1500 KES)
            base_price = 1500.00
            variation = random.uniform(-200, 200)
            price = round(base_price + variation, 2)
            
            doc_price = round(price * 0.33, 2)
            coding_price = round(price * 0.67, 2)
            
            try:
                Project.objects.create(
                    title=title,
                    description=description,
                    category=category,
                    price=price,
                    documentation_price=doc_price,
                    coding_price=coding_price,
                    is_available=random.choice([True, True, True, False])  # Mostly available
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created project {i}: {title}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating project {i}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} projects!'))
        self.stdout.write(self.style.SUCCESS('Total projects in database: ' + str(Project.objects.count())))