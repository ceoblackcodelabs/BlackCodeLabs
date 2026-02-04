from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Home.models import Course, CourseStat
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seed the database with sample courses from JavaScript array'
    
    def handle(self, *args, **kwargs):
        courses_data = [
            {
                "id": 1,
                "title": "Python Masterclass",
                "category": "python",
                "level": "beginner",
                "badge": "popular",
                "icon": "fab fa-python",
                "description": "Master Python programming from basics to advanced concepts with hands-on projects and real-world applications.",
                "duration": "12 Weeks",
                "lessons": "48 Lessons",
                "students": "2450",
                "rating": "4.9",
                "instructor": "Dr. Alex Johnson",
                "price": 199,
                "originalPrice": 299,
                "color": "#3776AB",
                "details": {
                    "Mode": "Online Live Classes",
                    "Schedule": "Mon & Wed, 7-9 PM EST",
                    "Projects": "5 Real-world Projects",
                    "Support": "24/7 Mentor Support"
                },
                "curriculum": [
                    {
                        "title": "Week 1-3: Python Fundamentals",
                        "lessons": [
                            "Introduction to Python",
                            "Variables and Data Types",
                            "Control Structures",
                            "Functions and Modules",
                            "File Handling"
                        ]
                    },
                    {
                        "title": "Week 4-6: Object-Oriented Programming",
                        "lessons": [
                            "Classes and Objects",
                            "Inheritance and Polymorphism",
                            "Encapsulation and Abstraction",
                            "Advanced OOP Concepts"
                        ]
                    },
                    {
                        "title": "Week 7-10: Advanced Python",
                        "lessons": [
                            "Decorators and Generators",
                            "Context Managers",
                            "Multithreading and Multiprocessing",
                            "Network Programming"
                        ]
                    },
                    {
                        "title": "Week 11-12: Final Project",
                        "lessons": [
                            "Project Planning",
                            "Building a Complete Application",
                            "Testing and Debugging",
                            "Deployment",
                            "Presentation"
                        ]
                    }
                ]
            },
            {
                "id": 2,
                "title": "JavaScript & React Bootcamp",
                "category": "javascript",
                "level": "intermediate",
                "badge": "new",
                "icon": "fab fa-js-square",
                "description": "Become a frontend developer by mastering JavaScript, React, and modern web development tools.",
                "duration": "10 Weeks",
                "lessons": "40 Lessons",
                "students": "1890",
                "rating": "4.8",
                "instructor": "Sarah Chen",
                "price": 249,
                "originalPrice": 349,
                "color": "#F7DF1E",
                "details": {
                    "Mode": "Hybrid (Online + Recorded)",
                    "Schedule": "Tue & Thu, 6-8 PM EST",
                    "Projects": "8 Portfolio Projects",
                    "Support": "Code Review Sessions"
                },
                "curriculum": [
                    {
                        "title": "Week 1-3: JavaScript Fundamentals",
                        "lessons": [
                            "Modern JavaScript ES6+",
                            "DOM Manipulation",
                            "Async Programming",
                            "APIs and Fetch",
                            "Debugging Tools"
                        ]
                    },
                    {
                        "title": "Week 4-6: React Core Concepts",
                        "lessons": [
                            "Components and Props",
                            "State and Lifecycle",
                            "Hooks (useState, useEffect)",
                            "React Router",
                            "Context API"
                        ]
                    },
                    {
                        "title": "Week 7-10: Advanced React",
                        "lessons": [
                            "Custom Hooks",
                            "Performance Optimization",
                            "Testing with Jest",
                            "Redux State Management",
                            "Next.js Basics"
                        ]
                    }
                ]
            },
            {
                "id": 3,
                "title": "IoT Development with Arduino",
                "category": "iot",
                "level": "beginner",
                "badge": "",
                "icon": "fas fa-microchip",
                "description": "Learn to build Internet of Things devices with Arduino, sensors, and cloud integration.",
                "duration": "8 Weeks",
                "lessons": "32 Lessons",
                "students": "1250",
                "rating": "4.7",
                "instructor": "Michael Rodriguez",
                "price": 179,
                "originalPrice": 249,
                "color": "#00979C",
                "details": {
                    "Mode": "Online with Kit",
                    "Schedule": "Weekend Workshops",
                    "Projects": "3 Hardware Projects",
                    "Support": "Hardware Troubleshooting"
                },
                "curriculum": [
                    {
                        "title": "Week 1-2: Arduino Basics",
                        "lessons": [
                            "Introduction to Arduino",
                            "Setting up Development Environment",
                            "Basic Electronics",
                            "LED Blink Project",
                            "Serial Communication"
                        ]
                    },
                    {
                        "title": "Week 3-4: Sensors & Actuators",
                        "lessons": [
                            "Temperature & Humidity Sensors",
                            "Motion Detection",
                            "Light & Sound Sensors",
                            "Motor Control",
                            "Relay Modules"
                        ]
                    },
                    {
                        "title": "Week 5-6: IoT Communication",
                        "lessons": [
                            "Wi-Fi with ESP8266",
                            "MQTT Protocol",
                            "Cloud Integration",
                            "Mobile App Control",
                            "Data Logging"
                        ]
                    }
                ]
            },
            {
                "id": 4,
                "title": "Advanced React & Node.js",
                "category": "javascript",
                "level": "advanced",
                "badge": "advanced",
                "icon": "fab fa-node-js",
                "description": "Build full-stack applications with React, Node.js, Express, and MongoDB.",
                "duration": "14 Weeks",
                "lessons": "56 Lessons",
                "students": "980",
                "rating": "4.9",
                "instructor": "David Wilson",
                "price": 299,
                "originalPrice": 399,
                "color": "#68A063",
                "details": {
                    "Mode": "Online Live Classes",
                    "Schedule": "Mon, Wed, Fri 8-10 PM EST",
                    "Projects": "Full-stack Applications",
                    "Support": "Career Guidance"
                },
                "curriculum": [
                    {
                        "title": "Week 1-4: Advanced React Patterns",
                        "lessons": [
                            "Advanced Hooks",
                            "Render Props & HOCs",
                            "State Management Patterns",
                            "Server-Side Rendering",
                            "TypeScript with React"
                        ]
                    },
                    {
                        "title": "Week 5-8: Node.js Backend",
                        "lessons": [
                            "Express.js Framework",
                            "RESTful API Design",
                            "Authentication & Authorization",
                            "Database Integration",
                            "WebSockets & Real-time"
                        ]
                    },
                    {
                        "title": "Week 9-12: Full-Stack Integration",
                        "lessons": [
                            "MongoDB & Mongoose",
                            "JWT Authentication",
                            "File Uploads",
                            "Deployment Strategies",
                            "Performance Optimization"
                        ]
                    }
                ]
            },
            {
                "id": 5,
                "title": "AI & Machine Learning Fundamentals",
                "category": "ai",
                "level": "intermediate",
                "badge": "popular",
                "icon": "fas fa-robot",
                "description": "Introduction to AI and ML concepts with Python, TensorFlow, and real-world datasets.",
                "duration": "16 Weeks",
                "lessons": "64 Lessons",
                "students": "2100",
                "rating": "4.8",
                "instructor": "Dr. Priya Sharma",
                "price": 349,
                "originalPrice": 449,
                "color": "#FF6B6B",
                "details": {
                    "Mode": "Online with Labs",
                    "Schedule": "Weekend Intensive",
                    "Projects": "ML Models & Deployments",
                    "Support": "Research Paper Guidance"
                },
                "curriculum": [
                    {
                        "title": "Week 1-4: Python for Data Science",
                        "lessons": [
                            "NumPy & Pandas",
                            "Data Visualization",
                            "Statistical Analysis",
                            "Data Preprocessing",
                            "Exploratory Data Analysis"
                        ]
                    },
                    {
                        "title": "Week 5-8: Machine Learning Basics",
                        "lessons": [
                            "Linear Regression",
                            "Logistic Regression",
                            "Decision Trees",
                            "Clustering Algorithms",
                            "Model Evaluation"
                        ]
                    },
                    {
                        "title": "Week 9-12: Deep Learning",
                        "lessons": [
                            "Neural Networks",
                            "TensorFlow & Keras",
                            "CNNs for Images",
                            "RNNs for Sequences",
                            "Transfer Learning"
                        ]
                    }
                ]
            },
            {
                "id": 6,
                "title": "IoT with Raspberry Pi & Python",
                "category": "iot",
                "level": "intermediate",
                "badge": "",
                "icon": "fas fa-server",
                "description": "Advanced IoT course focusing on Raspberry Pi, Python, and home automation projects.",
                "duration": "10 Weeks",
                "lessons": "40 Lessons",
                "students": "870",
                "rating": "4.6",
                "instructor": "Robert Kim",
                "price": 229,
                "originalPrice": 299,
                "color": "#C51A4A",
                "details": {
                    "Mode": "Online with Kit",
                    "Schedule": "Flexible with Recordings",
                    "Projects": "Smart Home System",
                    "Support": "Community Forum Access"
                },
                "curriculum": [
                    {
                        "title": "Week 1-2: Raspberry Pi Setup",
                        "lessons": [
                            "Raspberry Pi Introduction",
                            "OS Installation",
                            "GPIO Pins & Wiring",
                            "Python on Raspberry Pi",
                            "Remote Access"
                        ]
                    },
                    {
                        "title": "Week 3-5: Sensors & Camera",
                        "lessons": [
                            "Temperature & Humidity",
                            "Motion Detection",
                            "Camera Module",
                            "Voice Recognition",
                            "Sensor Networks"
                        ]
                    },
                    {
                        "title": "Week 6-8: Home Automation",
                        "lessons": [
                            "Smart Lights Control",
                            "Security System",
                            "Weather Station",
                            "Mobile Dashboard",
                            "Cloud Integration"
                        ]
                    }
                ]
            },
            {
                "id": 7,
                "title": "Data Science with Python",
                "category": "python",
                "level": "intermediate",
                "badge": "new",
                "icon": "fas fa-chart-line",
                "description": "Master data analysis, visualization, and statistical modeling with Python libraries.",
                "duration": "12 Weeks",
                "lessons": "48 Lessons",
                "students": "1650",
                "rating": "4.7",
                "instructor": "Jennifer Lee",
                "price": 279,
                "originalPrice": 349,
                "color": "#4B8BBE",
                "details": {
                    "Mode": "Online Live Classes",
                    "Schedule": "Tue & Thu, 7-9 PM EST",
                    "Projects": "Data Analysis Projects",
                    "Support": "Dataset Access"
                },
                "curriculum": [
                    {
                        "title": "Week 1-3: Data Analysis",
                        "lessons": [
                            "Pandas for Data Manipulation",
                            "Data Cleaning Techniques",
                            "Exploratory Data Analysis",
                            "Statistical Summary",
                            "Handling Missing Data"
                        ]
                    },
                    {
                        "title": "Week 4-6: Data Visualization",
                        "lessons": [
                            "Matplotlib Basics",
                            "Seaborn for Statistical Plots",
                            "Interactive Plots with Plotly",
                            "Dashboard Creation",
                            "Storytelling with Data"
                        ]
                    },
                    {
                        "title": "Week 7-9: Statistical Modeling",
                        "lessons": [
                            "Hypothesis Testing",
                            "Regression Analysis",
                            "Time Series Analysis",
                            "A/B Testing",
                            "Predictive Modeling"
                        ]
                    }
                ]
            },
            {
                "id": 8,
                "title": "IoT Security & Ethical Hacking",
                "category": "iot",
                "level": "advanced",
                "badge": "advanced",
                "icon": "fas fa-shield-alt",
                "description": "Learn to secure IoT devices and networks against cyber threats and vulnerabilities.",
                "duration": "8 Weeks",
                "lessons": "32 Lessons",
                "students": "540",
                "rating": "4.9",
                "instructor": "Kevin O'Brien",
                "price": 319,
                "originalPrice": 399,
                "color": "#2E8B57",
                "details": {
                    "Mode": "Online with Virtual Labs",
                    "Schedule": "Weekend Intensive",
                    "Projects": "Security Audits",
                    "Support": "Certification Prep"
                },
                "curriculum": [
                    {
                        "title": "Week 1-2: IoT Security Basics",
                        "lessons": [
                            "IoT Security Landscape",
                            "Common Vulnerabilities",
                            "Network Security",
                            "Device Hardening",
                            "Encryption for IoT"
                        ]
                    },
                    {
                        "title": "Week 3-4: Penetration Testing",
                        "lessons": [
                            "Reconnaissance Techniques",
                            "Vulnerability Scanning",
                            "Exploitation Methods",
                            "Post-Exploitation",
                            "Reporting Findings"
                        ]
                    },
                    {
                        "title": "Week 5-6: Secure Development",
                        "lessons": [
                            "Secure Coding Practices",
                            "Authentication Mechanisms",
                            "Data Protection",
                            "Secure Communication",
                            "Compliance Standards"
                        ]
                    }
                ]
            },
            {
                "id": 9,
                "title": "Scratch Programming for Kids",
                "category": "scratch",
                "level": "beginner",
                "badge": "kids",
                "icon": "fas fa-gamepad",
                "description": "Introduce children to coding through fun, visual programming with Scratch. Create games, animations, and interactive stories.",
                "duration": "6 Weeks",
                "lessons": "24 Lessons",
                "students": "3200",
                "rating": "4.9",
                "instructor": "Ms. Emily Carter",
                "price": 99,
                "originalPrice": 149,
                "color": "#FF8C42",
                "details": {
                    "Age Group": "8-12 Years",
                    "Format": "Game-based Learning",
                    "Projects": "10+ Fun Projects",
                    "Support": "Weekly Progress Reports"
                },
                "curriculum": [
                    {
                        "title": "Week 1: Scratch Basics & First Project",
                        "lessons": [
                            "Introduction to Scratch Interface",
                            "Meet the Sprite Characters",
                            "Creating Your First Animation",
                            "Adding Sounds and Music",
                            "Save and Share Your Project"
                        ]
                    },
                    {
                        "title": "Week 2: Animation & Storytelling",
                        "lessons": [
                            "Creating Animated Stories",
                            "Character Movement & Dialogues",
                            "Scene Transitions",
                            "Adding Background Music",
                            "Interactive Story Project"
                        ]
                    },
                    {
                        "title": "Week 3: Game Development Basics",
                        "lessons": [
                            "Design Your First Game",
                            "Score Keeping & Variables",
                            "Game Controls (Keyboard/Mouse)",
                            "Win/Lose Conditions",
                            "Maze Runner Game Project"
                        ]
                    },
                    {
                        "title": "Week 4: Advanced Games",
                        "lessons": [
                            "Creating Multiple Levels",
                            "Power-ups and Bonuses",
                            "Enemy AI Basics",
                            "Game Physics (Gravity, Bouncing)",
                            "Space Adventure Game"
                        ]
                    },
                    {
                        "title": "Week 5: Art & Music Projects",
                        "lessons": [
                            "Digital Drawing with Scratch",
                            "Creating Music Beats",
                            "Dance Party Animation",
                            "Interactive Art Gallery",
                            "Virtual Band Project"
                        ]
                    },
                    {
                        "title": "Week 6: Final Project & Showcase",
                        "lessons": [
                            "Planning Your Own Game",
                            "Combining All Skills",
                            "Debugging & Testing",
                            "Polishing Your Project",
                            "Virtual Showcase Day"
                        ]
                    }
                ]
            },
            {
                "id": 10,
                "title": "Web Development Fundamentals",
                "category": "web",
                "level": "beginner",
                "badge": "popular",
                "icon": "fas fa-laptop-code",
                "description": "Learn HTML, CSS, and JavaScript to build responsive websites from scratch.",
                "duration": "8 Weeks",
                "lessons": "32 Lessons",
                "students": "1850",
                "rating": "4.7",
                "instructor": "Marcus Thompson",
                "price": 159,
                "originalPrice": 229,
                "color": "#3498DB",
                "details": {
                    "Mode": "Online Live Classes",
                    "Schedule": "Mon & Wed, 6-8 PM EST",
                    "Projects": "4 Website Projects",
                    "Support": "Weekly Code Reviews"
                },
                "curriculum": [
                    {
                        "title": "Week 1-2: HTML & CSS",
                        "lessons": [
                            "HTML Structure & Semantics",
                            "CSS Styling & Layouts",
                            "Responsive Design",
                            "Flexbox & Grid",
                            "CSS Animations"
                        ]
                    },
                    {
                        "title": "Week 3-4: JavaScript Basics",
                        "lessons": [
                            "JavaScript Fundamentals",
                            "DOM Manipulation",
                            "Event Handling",
                            "Forms Validation",
                            "Basic Algorithms"
                        ]
                    }
                ]
            },
            {
                "id": 11,
                "title": "Mobile App Development with React Native",
                "category": "mobile",
                "level": "intermediate",
                "badge": "new",
                "icon": "fas fa-mobile-alt",
                "description": "Build cross-platform mobile apps for iOS and Android using React Native.",
                "duration": "10 Weeks",
                "lessons": "40 Lessons",
                "students": "1320",
                "rating": "4.6",
                "instructor": "Lisa Wang",
                "price": 269,
                "originalPrice": 349,
                "color": "#9B59B6",
                "details": {
                    "Mode": "Online with Projects",
                    "Schedule": "Tue & Thu, 7-9 PM EST",
                    "Projects": "3 Mobile Apps",
                    "Support": "App Store Guidance"
                },
                "curriculum": [
                    {
                        "title": "Week 1-3: React Native Basics",
                        "lessons": [
                            "Setting up Environment",
                            "Components & Styling",
                            "Navigation",
                            "State Management",
                            "Debugging Tools"
                        ]
                    },
                    {
                        "title": "Week 4-6: Advanced Features",
                        "lessons": [
                            "Native Modules",
                            "APIs Integration",
                            "Push Notifications",
                            "Offline Storage",
                            "Performance Optimization"
                        ]
                    }
                ]
            },
            {
                "id": 12,
                "title": "Cybersecurity Essentials",
                "category": "security",
                "level": "beginner",
                "badge": "",
                "icon": "fas fa-shield-alt",
                "description": "Learn the fundamentals of cybersecurity, threats, and protection mechanisms.",
                "duration": "8 Weeks",
                "lessons": "32 Lessons",
                "students": "950",
                "rating": "4.8",
                "instructor": "James Peterson",
                "price": 189,
                "originalPrice": 259,
                "color": "#E74C3C",
                "details": {
                    "Mode": "Online with Labs",
                    "Schedule": "Weekend Sessions",
                    "Projects": "Security Assessments",
                    "Support": "Career Path Guidance"
                },
                "curriculum": [
                    {
                        "title": "Week 1-2: Security Fundamentals",
                        "lessons": [
                            "Security Principles",
                            "Threat Landscape",
                            "Cryptography Basics",
                            "Network Security",
                            "Risk Management"
                        ]
                    },
                    {
                        "title": "Week 3-4: Defensive Techniques",
                        "lessons": [
                            "Firewalls & IDS/IPS",
                            "Endpoint Security",
                            "Security Policies",
                            "Incident Response",
                            "Security Auditing"
                        ]
                    }
                ]
            }
        ]
        
        created_count = 0
        updated_count = 0
        
        self.stdout.write("Starting to seed courses...")
        
        for course_js in courses_data:
            # Generate slug from title
            from django.utils.text import slugify
            course_slug = slugify(course_js['title'])
            
            # Prepare data for Django model
            course_data = {
                'title': course_js['title'],
                'slug': course_slug,
                'category': course_js['category'],
                'level': course_js['level'],
                'badge': course_js['badge'],
                'icon_class': course_js['icon'],
                'color': course_js['color'],
                'short_description': course_js['description'],
                'detailed_description': f"Comprehensive course on {course_js['title']}. {course_js['description']}",
                'duration': course_js['duration'],
                'lessons': course_js['lessons'],
                'students_enrolled': int(course_js['students'].replace(',', '')) if ',' in course_js['students'] else int(course_js['students']),
                'rating': float(course_js['rating']),
                'price': Decimal(str(course_js['price'])),
                'original_price': Decimal(str(course_js['originalPrice'])) if course_js.get('originalPrice') else None,
                'instructor_name': course_js['instructor'],
                'instructor_title': self.get_instructor_title(course_js['instructor'], course_js['category']),
                'instructor_bio': self.get_instructor_bio(course_js['instructor'], course_js['category']),
                'details': course_js.get('details', {}),
                'curriculum': course_js.get('curriculum', []),
                'is_active': True,
                'is_featured': course_js['badge'] in ['popular', 'new', 'advanced'],
                'display_order': course_js['id'],
            }
            
            # Create or update course
            obj, created = Course.objects.update_or_create(
                slug=course_data['slug'],
                defaults=course_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {obj.title}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'↻ Updated: {obj.title}'))
        
        # Create or update stats
        total_courses = Course.objects.filter(is_active=True).count()
        total_students = sum(course.students_enrolled for course in Course.objects.all())
        
        # Get unique instructors count
        unique_instructors = Course.objects.values('instructor_name').distinct().count()
        
        stats, created = CourseStat.objects.get_or_create(id=1)
        stats.total_courses = total_courses
        stats.total_students = total_students
        stats.total_instructors = unique_instructors
        stats.satisfaction_rate = 98.5  # Average satisfaction rate
        stats.save()
        
        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS(
            f'\n🎉 Seeding Complete!\n'
            f'• Created: {created_count} courses\n'
            f'• Updated: {updated_count} courses\n'
            f'• Total Active Courses: {total_courses}\n'
            f'• Total Students Enrolled: {total_students:,}\n'
            f'• Total Instructors: {unique_instructors}\n'
        ))
        self.stdout.write("="*50)
    
    def get_instructor_title(self, instructor_name, category):
        """Generate appropriate instructor title based on category"""
        titles = {
            'python': 'Senior Python Developer',
            'javascript': 'Full-Stack JavaScript Developer',
            'iot': 'IoT Solutions Architect',
            'ai': 'AI/ML Specialist',
            'scratch': 'Certified STEM Educator',
            'web': 'Frontend Developer',
            'mobile': 'Mobile App Developer',
            'data': 'Data Scientist',
            'security': 'Cybersecurity Expert',
        }
        return titles.get(category, 'Technology Instructor')
    
    def get_instructor_bio(self, instructor_name, category):
        """Generate appropriate instructor bio based on category"""
        bios = {
            'python': f'{instructor_name} has extensive experience in Python development with 8+ years in software engineering and teaching.',
            'javascript': f'{instructor_name} specializes in modern JavaScript frameworks and has contributed to open-source projects.',
            'iot': f'{instructor_name} has worked on numerous IoT projects and has expertise in embedded systems and cloud integration.',
            'ai': f'{instructor_name} holds a PhD in Computer Science and has published research papers in AI/ML conferences.',
            'scratch': f'{instructor_name} is passionate about teaching coding to children and has developed award-winning educational programs.',
            'web': f'{instructor_name} has built websites for Fortune 500 companies and specializes in responsive design.',
            'mobile': f'{instructor_name} has published multiple apps on both App Store and Google Play with millions of downloads.',
            'data': f'{instructor_name} has worked with large datasets and has expertise in statistical analysis and visualization.',
            'security': f'{instructor_name} has conducted security audits for major corporations and holds multiple cybersecurity certifications.',
        }
        return bios.get(category, f'{instructor_name} is an experienced instructor passionate about technology education.')