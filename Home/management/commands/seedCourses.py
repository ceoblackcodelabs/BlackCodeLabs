from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Home.models import Course, CourseStat
import json

class Command(BaseCommand):
    help = 'Seed the database with sample courses'
    
    def handle(self, *args, **kwargs):
        sample_courses = [
            {
                'title': 'Python Masterclass',
                'slug': 'python-masterclass',
                'category': 'python',
                'level': 'beginner',
                'badge': 'popular',
                'icon_class': 'fab fa-python',
                'color': '#3776AB',
                'short_description': 'Master Python programming from basics to advanced concepts with hands-on projects and real-world applications.',
                'detailed_description': 'This comprehensive Python course covers everything from basic syntax to advanced topics. Perfect for beginners and intermediate developers.',
                'duration': '12 Weeks',
                'lessons': '48 Lessons',
                'students_enrolled': 2450,
                'rating': 4.9,
                'price': 199.00,
                'original_price': 299.00,
                'instructor_name': 'Dr. Alex Johnson',
                'instructor_title': 'Senior AI Engineer',
                'instructor_bio': 'Senior AI Engineer with 10+ years of experience in Python development and machine learning. Former lead developer at TechGiant Inc.',
                'details': {
                    'Mode': 'Online Live Classes',
                    'Schedule': 'Mon & Wed, 7-9 PM EST',
                    'Projects': '5 Real-world Projects',
                    'Support': '24/7 Mentor Support'
                },
                'curriculum': [
                    {
                        'title': 'Week 1-3: Python Fundamentals',
                        'lessons': [
                            'Introduction to Python',
                            'Variables and Data Types',
                            'Control Structures',
                            'Functions and Modules',
                            'File Handling'
                        ]
                    },
                    {
                        'title': 'Week 4-6: Object-Oriented Programming',
                        'lessons': [
                            'Classes and Objects',
                            'Inheritance and Polymorphism',
                            'Encapsulation and Abstraction',
                            'Advanced OOP Concepts'
                        ]
                    }
                ],
                'is_active': True,
                'is_featured': True,
                'display_order': 1,
            },
            {
                'title': 'Scratch Programming for Kids',
                'slug': 'scratch-programming-for-kids',
                'category': 'scratch',
                'level': 'beginner',
                'badge': 'kids',
                'icon_class': 'fas fa-gamepad',
                'color': '#FF8C42',
                'short_description': 'Introduce children to coding through fun, visual programming with Scratch. Create games, animations, and interactive stories.',
                'detailed_description': 'A fun and engaging course designed specifically for children aged 8-12. Learn programming concepts through game development.',
                'duration': '6 Weeks',
                'lessons': '24 Lessons',
                'students_enrolled': 3200,
                'rating': 4.9,
                'price': 99.00,
                'original_price': 149.00,
                'instructor_name': 'Ms. Emily Carter',
                'instructor_title': 'Certified STEM Educator',
                'instructor_bio': 'Certified STEM educator with 8+ years experience teaching coding to children. Creator of CodeKids program.',
                'details': {
                    'Age Group': '8-12 Years',
                    'Format': 'Game-based Learning',
                    'Projects': '10+ Fun Projects',
                    'Support': 'Weekly Progress Reports'
                },
                'curriculum': [
                    {
                        'title': 'Week 1: Scratch Basics & First Project',
                        'lessons': [
                            'Introduction to Scratch Interface',
                            'Meet the Sprite Characters',
                            'Creating Your First Animation',
                            'Adding Sounds and Music',
                            'Save and Share Your Project'
                        ]
                    }
                ],
                'is_active': True,
                'is_featured': True,
                'display_order': 2,
            },
            # Add more courses as needed
        ]
        
        created_count = 0
        updated_count = 0
        
        for course_data in sample_courses:
            # Extract curriculum and details
            curriculum = course_data.pop('curriculum')
            details = course_data.pop('details')
            
            # Create or update course
            obj, created = Course.objects.update_or_create(
                slug=course_data['slug'],
                defaults=course_data
            )
            
            # Set JSON fields
            obj.curriculum = curriculum
            obj.details = details
            obj.save()
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created course: {obj.title}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'Updated course: {obj.title}'))
        
        # Create or update stats
        total_courses = Course.objects.filter(is_active=True).count()
        total_students = sum(course.students_enrolled for course in Course.objects.all())
        
        stats, created = CourseStat.objects.get_or_create(id=1)
        stats.total_courses = total_courses
        stats.total_students = total_students
        stats.total_instructors = User.objects.filter(is_staff=True).count()
        stats.save()
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created course statistics'))
        else:
            self.stdout.write(self.style.WARNING('Updated course statistics'))
        
        self.stdout.write(self.style.SUCCESS(
            f'\nSeeding complete! Created: {created_count}, Updated: {updated_count}, Total Courses: {total_courses}, Total Students: {total_students}'
        ))