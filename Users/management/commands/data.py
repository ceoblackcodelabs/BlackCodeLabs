# Home/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta
from Users.models import *

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed database with initial data for BlackSheep developer portfolio'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        
        # 1. Create or get user
        user, created = User.objects.get_or_create(
            username='BlackSheep',
            defaults={
                'first_name': 'Black',
                'last_name': 'Sheep',
                'email': 'blacksheep@devportfolio.com',
                'role': 'seeker',
                'is_active': True,
                'is_staff': True,
            }
        )
        
        if created:
            user.set_password('BlackSheep@2024')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'User "BlackSheep" created with password: BlackSheep@2024'))
        else:
            self.stdout.write(self.style.SUCCESS('User "BlackSheep" already exists'))
        
        # 2. Create Profile
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={
                'name': 'BlackSheep Developer',
                'title': 'Full Stack Developer & Tech Enthusiast',
                'about_text': '''I am a passionate Full Stack Developer with over 8 years of experience in building web applications. I specialize in Django, React, and creating scalable solutions that solve real-world problems.

Throughout my career, I've worked with startups and enterprises alike, helping them transform their ideas into robust digital products. I believe in writing clean, maintainable code and continuously learning new technologies.

When I'm not coding, I enjoy contributing to open-source projects, mentoring junior developers, and exploring new tech trends. I'm always excited to take on challenging projects that push the boundaries of what's possible on the web.''',
                'phone': '+1 (234) 567-8900',
                'email': 'blacksheep@devportfolio.com',
                'address': 'San Francisco, CA, USA',
                'birthday': date(1992, 3, 15),
                'degree': 'Master in Computer Science',
                'experience_years': 8,
                'freelance_status': 'available',
                'years_of_experience': 8,
                'happy_clients': 45,
                'completed_projects': 120,
                'twitter': 'https://twitter.com/blacksheep_dev',
                'facebook': 'https://facebook.com/blacksheep.dev',
                'linkedin': 'https://linkedin.com/in/blacksheep-dev',
                'instagram': 'https://instagram.com/blacksheep_codes',
                'github': 'https://github.com/blacksheep-dev',
                'typed_texts': 'Full Stack Developer, Django Expert, React Developer, Tech Lead, Open Source Contributor, Problem Solver'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Profile created for BlackSheep'))
        else:
            self.stdout.write('Profile already exists, updating...')
            profile.name = 'BlackSheep Developer'
            profile.title = 'Full Stack Developer & Tech Enthusiast'
            profile.save()
            self.stdout.write(self.style.SUCCESS('Profile updated'))
        
        # 3. Add Skills
        skills_data = [
            {'name': 'Python/Django', 'percentage': 95, 'color': 'primary', 'order': 1},
            {'name': 'React.js', 'percentage': 90, 'color': 'danger', 'order': 2},
            {'name': 'JavaScript/ES6', 'percentage': 92, 'color': 'warning', 'order': 3},
            {'name': 'PostgreSQL', 'percentage': 85, 'color': 'success', 'order': 4},
            {'name': 'Docker/K8s', 'percentage': 78, 'color': 'info', 'order': 5},
            {'name': 'REST APIs', 'percentage': 88, 'color': 'primary', 'order': 6},
            {'name': 'Git/GitHub', 'percentage': 90, 'color': 'secondary', 'order': 7},
            {'name': 'AWS Cloud', 'percentage': 75, 'color': 'warning', 'order': 8},
        ]
        
        for skill_data in skills_data:
            skill, created = Skill.objects.get_or_create(
                profile=profile,
                name=skill_data['name'],
                defaults=skill_data
            )
            if created:
                self.stdout.write(f'  - Added skill: {skill_data["name"]}')
        
        # 4. Add Work Experience
        experiences_data = [
            {
                'title': 'Senior Full Stack Developer',
                'company': 'Tech Innovations Inc.',
                'start_date': date(2021, 1, 1),
                'end_date': None,
                'is_current': True,
                'description': '''Leading the development of enterprise-level web applications using Django and React. 
- Architecting scalable backend services serving 100k+ users
- Mentoring a team of 5 junior developers
- Implementing CI/CD pipelines reducing deployment time by 40%
- Optimizing database queries improving response time by 60%''',
                'order': 1
            },
            {
                'title': 'Software Engineer',
                'company': 'Digital Solutions Ltd',
                'start_date': date(2018, 6, 1),
                'end_date': date(2020, 12, 31),
                'is_current': False,
                'description': '''Developed and maintained multiple client projects. 
- Built RESTful APIs serving mobile and web applications
- Collaborated with cross-functional teams to deliver projects on time
- Implemented automated testing reducing bugs by 30%
- Received "Employee of the Quarter" award twice''',
                'order': 2
            },
            {
                'title': 'Junior Developer',
                'company': 'StartUp Hub',
                'start_date': date(2016, 1, 1),
                'end_date': date(2018, 5, 31),
                'is_current': False,
                'description': '''Started career as a junior developer. 
- Assisted in developing features for e-commerce platforms
- Learned modern web technologies and best practices
- Contributed to code reviews and documentation
- Quickly advanced from junior to mid-level developer''',
                'order': 3
            },
        ]
        
        for exp_data in experiences_data:
            exp, created = Experience.objects.get_or_create(
                profile=profile,
                title=exp_data['title'],
                company=exp_data['company'],
                defaults=exp_data
            )
            if created:
                self.stdout.write(f'  - Added experience: {exp_data["title"]} at {exp_data["company"]}')
        
        # 5. Add Education
        education_data = [
            {
                'degree': 'Master of Science in Computer Science',
                'institution': 'Stanford University',
                'start_year': 2014,
                'end_year': 2016,
                'description': 'Specialized in Artificial Intelligence and Web Technologies. GPA: 3.8/4.0',
                'order': 1
            },
            {
                'degree': 'Bachelor of Engineering in Computer Science',
                'institution': 'University of Technology',
                'start_year': 2010,
                'end_year': 2014,
                'description': 'Graduated with honors. Active member of coding club and hackathon organizer.',
                'order': 2
            },
        ]
        
        for edu_data in education_data:
            edu, created = Education.objects.get_or_create(
                profile=profile,
                degree=edu_data['degree'],
                institution=edu_data['institution'],
                defaults=edu_data
            )
            if created:
                self.stdout.write(f'  - Added education: {edu_data["degree"]}')
        
        # 6. Add Services
        services_data = [
            {
                'icon': 'fa-laptop-code',
                'title': 'Web Development',
                'description': 'Custom web applications built with Django, React, and modern technologies. Responsive, scalable, and secure solutions tailored to your needs.',
                'order': 1
            },
            {
                'icon': 'fa-mobile-alt',
                'title': 'Mobile App Development',
                'description': 'Cross-platform mobile applications using React Native. Native-like performance with shared codebase for iOS and Android.',
                'order': 2
            },
            {
                'icon': 'fa-database',
                'title': 'Database Design',
                'description': 'Efficient database architecture and optimization. PostgreSQL, MySQL, MongoDB expertise with focus on performance and scalability.',
                'order': 3
            },
            {
                'icon': 'fa-cloud',
                'title': 'Cloud Solutions',
                'description': 'AWS, Google Cloud, and Azure deployment. Serverless architecture, containerization with Docker, and orchestration with Kubernetes.',
                'order': 4
            },
            {
                'icon': 'fa-search',
                'title': 'SEO Optimization',
                'description': 'Improve your website visibility with SEO best practices. Technical SEO, performance optimization, and analytics setup.',
                'order': 5
            },
            {
                'icon': 'fa-edit',
                'title': 'Technical Consulting',
                'description': 'Expert advice on technology stack, architecture decisions, and best practices. Code reviews and team training available.',
                'order': 6
            },
        ]
        
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                profile=profile,
                title=service_data['title'],
                defaults=service_data
            )
            if created:
                self.stdout.write(f'  - Added service: {service_data["title"]}')
        
        # 7. Add Portfolio Categories
        categories_data = [
            {'name': 'Web Applications', 'slug': 'web-apps', 'filter_class': 'first'},
            {'name': 'Mobile Apps', 'slug': 'mobile-apps', 'filter_class': 'second'},
            {'name': 'E-commerce', 'slug': 'ecommerce', 'filter_class': 'first'},
            {'name': 'API Development', 'slug': 'api', 'filter_class': 'second'},
        ]
        
        for cat_data in categories_data:
            category, created = PortfolioCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'  - Added category: {cat_data["name"]}')
        
        # 8. Add Testimonials
        testimonials_data = [
            {
                'client_name': 'Sarah Johnson',
                'client_profession': 'CEO, TechStart Inc.',
                'testimonial_text': 'Working with BlackSheep was an absolute pleasure. He delivered our project ahead of schedule and exceeded all expectations. His technical expertise and problem-solving skills are outstanding. Highly recommended!',
                'rating': 5,
                'order': 1,
                'is_active': True
            },
            {
                'client_name': 'Michael Chen',
                'client_profession': 'Product Manager, Digital Solutions',
                'testimonial_text': 'BlackSheep is one of the most talented developers I have worked with. He not only writes clean code but also provides valuable insights that improved our product architecture. Will definitely work with him again.',
                'rating': 5,
                'order': 2,
                'is_active': True
            },
            {
                'client_name': 'Emily Rodriguez',
                'client_profession': 'Startup Founder',
                'testimonial_text': 'Exceptional work! BlackSheep transformed our idea into a fully functional web application in record time. His communication was excellent throughout the process. Best investment we made for our startup.',
                'rating': 5,
                'order': 3,
                'is_active': True
            },
        ]
        
        for test_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                profile=profile,
                client_name=test_data['client_name'],
                defaults=test_data
            )
            if created:
                self.stdout.write(f'  - Added testimonial from: {test_data["client_name"]}')
        
        # 9. Create Site Settings
        site_settings, created = SiteSetting.objects.get_or_create(
            profile=profile,
            defaults={
                'site_name': 'BlackSheep Dev Portfolio',
                'footer_text': '© 2024 BlackSheep Developer. All rights reserved. Built with Django',
                'show_subscribe_section': True,
                'subscribe_title': 'Subscribe to My Newsletter',
                'subscribe_text': 'Get the latest updates on my projects and tech insights delivered to your inbox.',
                'contact_form_active': True,
                'contact_form_message': 'I\'ll get back to you within 24 hours. Looking forward to hearing from you!'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Site settings created'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Database seeding completed successfully!'))
        self.stdout.write('\n📊 Summary:')
        self.stdout.write(f'   - User: BlackSheep (Password: BlackSheep@2024)')
        self.stdout.write(f'   - Profile: {profile.name}')
        self.stdout.write(f'   - Skills: {Skill.objects.filter(profile=profile).count()}')
        self.stdout.write(f'   - Experiences: {Experience.objects.filter(profile=profile).count()}')
        self.stdout.write(f'   - Services: {Service.objects.filter(profile=profile).count()}')
        self.stdout.write(f'   - Testimonials: {Testimonial.objects.filter(profile=profile).count()}')