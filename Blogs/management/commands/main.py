# yourapp/management/commands/seed_campus_blog.py
import random
import os
from datetime import timedelta
from io import BytesIO
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.core.files.images import ImageFile
from PIL import Image, ImageDraw, ImageFont
from Blogs.models import Category, Post, Comment

class Command(BaseCommand):
    help = 'Seeds the campus blog with sample data including generated images'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🌱 Starting campus blog seeding...'))

        # Ensure media directory exists
        os.makedirs('media/posts/', exist_ok=True)

        # Create categories
        categories = self.create_categories()

        # Create users (students, faculty, staff)
        users = self.create_users()

        # Create posts with generated images
        posts = self.create_posts(categories, users)

        # Create comments
        self.create_comments(posts, users)

        self.stdout.write(self.style.SUCCESS('✅ Campus blog seeding completed!'))

    def create_categories(self):
        """Create campus-relevant categories"""
        campus_categories = [
            {"name": "Campus News", "slug": "campus-news"},
            {"name": "Academics", "slug": "academics"},
            {"name": "Student Life", "slug": "student-life"},
            {"name": "Events", "slug": "events"},
            {"name": "Sports", "slug": "sports"},
            {"name": "Arts & Culture", "slug": "arts-culture"},
            {"name": "Career & Internships", "slug": "career-internships"},
            {"name": "Research", "slug": "research"},
            {"name": "Alumni Stories", "slug": "alumni-stories"},
            {"name": "Clubs & Organizations", "slug": "clubs-organizations"},
            {"name": "Health & Wellness", "slug": "health-wellness"},
            {"name": "International Students", "slug": "international-students"},
            {"name": "Cultural Events", "slug": "cultural-events"},
            {"name": "Religious & Spiritual", "slug": "religious-spiritual"},
        ]

        categories = []
        for cat_data in campus_categories:
            category, created = Category.objects.get_or_create(
                name=cat_data["name"],
                defaults={"slug": cat_data["slug"]}
            )
            categories.append(category)
            self.stdout.write(f"  📁 Created category: {category.name}")

        return categories

    def create_users(self):
        """Create campus users (students, faculty, admin)"""
        users = []

        # Create admin/superuser if doesn't exist
        admin, created = User.objects.get_or_create(
            username="campus_admin",
            defaults={
                "email": "admin@campus.edu",
                "first_name": "Campus",
                "last_name": "Admin",
                "is_staff": True,
                "is_superuser": True,
            }
        )
        if created:
            admin.set_password("admin123")
            admin.save()
            self.stdout.write(f"  👨‍💼 Created admin: {admin.username}")
        users.append(admin)

        # Create faculty users with diverse backgrounds
        faculty_list = [
            {"username": "prof_smith", "first_name": "Sarah", "last_name": "Smith", "email": "s.smith@campus.edu", "dept": "English"},
            {"username": "prof_johnson", "first_name": "Michael", "last_name": "Johnson", "email": "m.johnson@campus.edu", "dept": "History"},
            {"username": "dr_williams", "first_name": "Emily", "last_name": "Williams", "email": "e.williams@campus.edu", "dept": "Anthropology"},
            {"username": "prof_brown", "first_name": "David", "last_name": "Brown", "email": "d.brown@campus.edu", "dept": "Sociology"},
            {"username": "dr_martinez", "first_name": "Elena", "last_name": "Martinez", "email": "e.martinez@campus.edu", "dept": "Cultural Studies"},
            {"username": "prof_okonkwo", "first_name": "Chidi", "last_name": "Okonkwo", "email": "c.okonkwo@campus.edu", "dept": "African Studies"},
        ]

        for faculty_data in faculty_list:
            user, created = User.objects.get_or_create(
                username=faculty_data["username"],
                defaults={
                    "email": faculty_data["email"],
                    "first_name": faculty_data["first_name"],
                    "last_name": faculty_data["last_name"],
                }
            )
            if created:
                user.set_password("faculty123")
                user.save()
                self.stdout.write(f"  👨‍🏫 Created faculty: {user.get_full_name()} ({faculty_data['dept']})")
            users.append(user)

        # Create student users with diverse cultural backgrounds
        student_names = [
            ("Aisha", "Khan", "Pakistan", "Computer Science"),
            ("Carlos", "Rodriguez", "Mexico", "Business"),
            ("Yuki", "Tanaka", "Japan", "Engineering"),
            ("Kwame", "Asante", "Ghana", "Medicine"),
            ("Priya", "Patel", "India", "Pharmacy"),
            ("Omar", "Hassan", "Egypt", "Architecture"),
            ("Maya", "Cohen", "Israel", "Psychology"),
            ("Liam", "O'Connor", "Ireland", "Literature"),
            ("Fatima", "Al-Sayed", "UAE", "Chemistry"),
            ("Dmitri", "Volkov", "Russia", "Physics"),
            ("Grace", "Mbeki", "Kenya", "Law"),
            ("Wei", "Zhang", "China", "Economics"),
            ("Sofia", "Silva", "Brazil", "Biology"),
            ("Ahmed", "Rahman", "Bangladesh", "Mathematics"),
            ("Zoe", "Papadopoulos", "Greece", "Philosophy"),
        ]

        for first, last, country, major in student_names:
            username = f"{first.lower()}_{last.lower()}"
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{first.lower()}.{last.lower()}@students.campus.edu",
                    "first_name": first,
                    "last_name": last,
                }
            )
            if created:
                user.set_password("student123")
                user.save()
                self.stdout.write(f"  👨‍🎓 Created student: {user.get_full_name()} ({country} - {major})")
            users.append(user)

        return users

    def generate_image(self, title, category_name, width=1200, height=630):
        """Generate a custom image using PIL based on post content"""
        # Create a new image with gradient background
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)

        # Create gradient background based on category
        colors = {
            "Cultural Events": [(255, 100, 100), (255, 200, 100)],  # Warm sunset
            "Events": [(100, 150, 255), (50, 200, 255)],  # Blue sky
            "Campus News": [(50, 50, 100), (100, 100, 200)],  # Deep blue
            "Student Life": [(100, 200, 100), (50, 150, 50)],  # Green
            "Sports": [(255, 100, 50), (200, 50, 50)],  # Orange/Red
            "Arts & Culture": [(200, 100, 200), (150, 50, 150)],  # Purple
            "Academics": [(200, 200, 50), (150, 150, 0)],  # Gold
            "Career & Internships": [(50, 150, 200), (0, 100, 150)],  # Teal
            "Health & Wellness": [(100, 200, 150), (50, 150, 100)],  # Mint
        }

        color1, color2 = colors.get(category_name, [(100, 100, 100), (50, 50, 50)])

        # Draw gradient
        for i in range(height):
            ratio = i / height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            draw.line([(0, i), (width, i)], fill=(r, g, b))

        # Add decorative patterns based on category
        if category_name == "Cultural Events":
            # Add geometric patterns (African/Aztec inspired)
            for x in range(0, width, 100):
                draw.line([(x, 0), (x + 50, height)], fill=(255, 255, 255, 50), width=3)
                draw.line([(x + 50, 0), (x, height)], fill=(255, 255, 255, 50), width=3)

        elif category_name == "Arts & Culture":
            # Add paint splatter effect
            for _ in range(50):
                x = random.randint(0, width)
                y = random.randint(0, height)
                r2 = random.randint(5, 30)
                draw.ellipse([x - r2, y - r2, x + r2, y + r2], fill=(255, 255, 255, 100))

        elif category_name == "Sports":
            # Add stadium lines
            for y in range(100, height, 100):
                draw.line([(0, y), (width, y)], fill=(255, 255, 255, 80), width=2)

        # Add main text overlay
        try:
            # Try to use a default font, fall back to default if not available
            font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
            font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        except:
            font_title = ImageFont.load_default()
            font_subtitle = ImageFont.load_default()

        # Draw semi-transparent overlay for text
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle([(50, height - 200), (width - 50, height - 80)], fill=(0, 0, 0, 180))
        image.paste(overlay, (0, 0), overlay)

        # Add title text
        wrapped_title = self.wrap_text(title, 35)
        y_pos = height - 180
        for line in wrapped_title:
            draw.text((70, y_pos), line, fill=(255, 255, 255), font=font_title)
            y_pos += 60

        # Add category as subtitle
        draw.text((70, height - 70), f"📌 {category_name}", fill=(255, 255, 200), font=font_subtitle)

        # Add decorative elements
        draw.rectangle([(40, height - 210), (width - 40, height - 70)], outline=(255, 255, 255, 100), width=2)

        # Save image to BytesIO
        buffer = BytesIO()
        image.save(buffer, format='JPEG', quality=85)
        buffer.seek(0)

        return ImageFile(buffer, name=f"{slugify(title)[:50]}.jpg")

    def wrap_text(self, text, max_chars):
        """Wrap text for image display"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            if current_length + len(word) + 1 <= max_chars:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word) + 1

        if current_line:
            lines.append(' '.join(current_line))

        return lines[:3]  # Max 3 lines

    def create_posts(self, categories, users):
        """Create sample blog posts about campus life with generated images"""

        posts_data = [
            # ============ CULTURAL DAY POSTS ============
            {
                "title": "Cultural Day 2026: A Spectacular Celebration of Diversity!",
                "excerpt": "Over 30 countries represented at our biggest cultural event of the year. See the highlights!",
                "body": """
                    <h2>🌈 A Day to Remember</h2>
                    <p>Last Saturday, our campus transformed into a vibrant global village as we celebrated Cultural Day 2026. Students, faculty, and staff from over 30 countries came together to share their traditions, food, music, and art.</p>

                    <h3>🎭 Main Stage Performances</h3>
                    <p>The energy was electric as performers took the stage throughout the day:</p>
                    <ul>
                        <li><strong>African Drum Circle</strong> - Led by the African Student Association, the rhythmic beats had everyone dancing</li>
                        <li><strong>Bollywood Fusion Dance</strong> - A stunning performance combining classical Indian dance with modern moves</li>
                        <li><strong>Latin American Salsa Showcase</strong> - Professional dancers taught workshops between performances</li>
                        <li><strong>Chinese Lion Dance</strong> - The traditional dance brought luck and excitement to the crowd</li>
                        <li><strong>Irish Step Dancing</strong> - Students from the Celtic Club impressed with their precision and energy</li>
                    </ul>

                    <h3>🌍 International Food Village</h3>
                    <p>The food was undoubtedly a highlight! Student organizations prepared authentic dishes from their home countries:</p>
                    <ul>
                        <li>🇲🇽 Mexican tacos and churros</li>
                        <li>🇯🇵 Japanese sushi and mochi</li>
                        <li>🇳🇬 Nigerian jollof rice (spice level: perfect!)</li>
                        <li>🇮🇹 Italian pasta and tiramisu</li>
                        <li>🇰🇷 Korean kimchi and bibimbap</li>
                        <li>🇧🇷 Brazilian brigadeiros (chocolate truffles)</li>
                    </ul>

                    <h3>👗 Cultural Fashion Show</h3>
                    <p>Students walked the runway wearing traditional attire from their cultures, explaining the significance of each garment. From Japanese kimonos to Nigerian agbadas, from Scottish kilts to Indian saris, it was a beautiful display of global heritage.</p>

                    <h3>🏆 Winners of Cultural Day 2026</h3>
                    <ul>
                        <li><strong>Best Booth:</strong> Nigerian Student Association</li>
                        <li><strong>Best Performance:</strong> Bollywood Dance Crew</li>
                        <li><strong>Best Traditional Dish:</strong> Japanese Sushi (tie with Mexican Churros!)</li>
                        <li><strong>Spirit of Cultural Day:</strong> The entire campus community! 🎉</li>
                    </ul>

                    <p>Thank you to everyone who made this day unforgettable. Mark your calendars for next year's Cultural Day - it's going to be even bigger! 🎊</p>
                """,
                "category": "Cultural Events",
                "featured": True,
                "read_minutes": 6,
                "image_generate": True,
            },
            {
                "title": "Behind the Scenes: Organizing Cultural Day 2026",
                "excerpt": "Meet the student leaders who spent 6 months planning our biggest cultural celebration.",
                "body": """
                    <h2>The Team Behind the Magic</h2>
                    <p>Cultural Day doesn't happen by accident. We sat down with the student organizing committee to learn about the challenges, triumphs, and unforgettable moments from planning this year's event.</p>

                    <h3>Meet the Committee</h3>
                    <p><strong>Maria Chen (President, International Student Association)</strong> - "We started planning in September. The first thing we did was reach out to every cultural club on campus to get them involved."</p>
                    <p><strong>Kwame Asante (Cultural Day Coordinator)</strong> - "The biggest challenge was scheduling. We had 25 different performances to coordinate across two stages!"</p>
                    <p><strong>Priya Patel (Food Village Lead)</strong> - "Organizing the food was intense. We had to ensure food safety, accommodate dietary restrictions, and keep everything fresh. Worth it when I saw the smiles!"</p>

                    <h3>By The Numbers</h3>
                    <ul>
                        <li>📅 6 months of planning</li>
                        <li>👥 50+ student volunteers</li>
                        <li>🌍 32 countries represented</li>
                        <li>🍽️ 1,500+ meals served</li>
                        <li>🎭 25 performances</li>
                        <li>🎟️ 3,000+ attendees</li>
                        <li>💵 $5,000 raised for cultural scholarships</li>
                    </ul>

                    <h3>Memorable Moments</h3>
                    <p>"When the African Drum Circle started playing and people from EVERY cultural background started dancing together - I got emotional," shares Maria. "That's what Cultural Day is really about."</p>
                    <p>The committee is already taking notes for next year. Want to join the planning team? Contact the Office of Multicultural Affairs!</p>
                """,
                "category": "Cultural Events",
                "featured": False,
                "read_minutes": 4,
                "image_generate": True,
            },
            {
                "title": "Cultural Fashion Show: A Runway Around the World",
                "excerpt": "Students showcase traditional attire from over 20 countries in stunning display of global fashion.",
                "body": """
                    <h2>👗 More Than Just Clothing</h2>
                    <p>The Cultural Fashion Show was one of the most anticipated events of Cultural Day, and it did not disappoint. Student models walked the runway in stunning traditional attire, each outfit telling a story of heritage, identity, and pride.</p>

                    <h3>Featured Outfits & Their Meanings</h3>

                    <p><strong>🇯🇵 Japanese Kimono</strong> - Worn by Yuki Tanaka, this silk kimono featured cherry blossom patterns representing the beauty and短暂 nature of life.</p>

                    <p><strong>🇳🇬 Nigerian Agbada</strong> - Kwame Asante wore a flowing royal blue agbada with gold embroidery, traditionally worn by Yoruba chiefs for special ceremonies.</p>

                    <p><strong>🇮🇳 Indian Lehenga</strong> - Priya Patel stunned in a deep red lehenga with intricate mirror work, representing celebration and joy.</p>

                    <p><strong>🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scottish Kilt</strong> - Liam O'Connor wore his family tartan, with each color representing a different aspect of his clan's history.</p>

                    <p><strong>🇲🇽 Mexican China Poblana</strong> - Sofia Silva wore the traditional dress of Puebla, with its iconic green, white, and red sequins representing the Mexican flag.</p>

                    <p><strong>🇪🇬 Egyptian Galabeya</strong> - Omar Hassan showcased a white cotton galabeya, the traditional garment worn for centuries along the Nile.</p>

                    <h3>Student Reactions</h3>
                    <p>"I was nervous to walk at first, but seeing everyone cheer made me so proud to represent my culture," shares Yuki. "My grandmother sent me this kimono from Japan, and wearing it here made me feel connected to my roots."</p>

                    <p>The fashion show will return next year with even more participants. Interested in modeling your cultural attire? Sign up at the International Student Office!</p>
                """,
                "category": "Cultural Events",
                "featured": True,
                "read_minutes": 5,
                "image_generate": True,
            },
            {
                "title": "Taste the World: Best Dishes from Cultural Day 2026",
                "excerpt": "Our food critic reviews the top 10 dishes from the International Food Village.",
                "body": """
                    <h2>🍜 A Culinary Journey</h2>
                    <p>As someone who ate my way through Cultural Day (for research purposes, of course), I'm here to share the absolute must-try dishes for next year's event.</p>

                    <h3>Top 10 Dishes (In No Particular Order Because Everything Was Amazing)</h3>

                    <p><strong>1. Nigerian Jollof Rice 🇳🇬</strong> - The legendary West African one-pot rice dish lived up to the hype. Perfectly spiced, with tender chicken and a subtle smoky flavor. Worth the 30-minute wait!</p>

                    <p><strong>2. Japanese Matcha Mochi 🇯🇵</strong> - These soft, chewy rice cakes filled with sweet red bean paste were a hit. The subtle bitterness of matcha balanced the sweetness perfectly.</p>

                    <p><strong>3. Mexican Street Tacos 🇲🇽</strong> - Al pastor tacos with pineapple, cilantro, and onions on fresh corn tortillas. Simple, authentic, and absolutely delicious.</p>

                    <p><strong>4. Italian Tiramisu 🇮🇹</strong> - Layers of coffee-soaked ladyfingers and mascarpone cream. Nonna would be proud.</p>

                    <p><strong>5. Korean Kimchi 🇰🇷</strong> - Fermented to perfection with just the right amount of heat. Served with fresh rice and sesame oil.</p>

                    <p><strong>6. Brazilian Brigadeiros 🇧🇷</strong> - These chocolate truffles were flying off the table. Made with condensed milk and coated in chocolate sprinkles - dangerously addictive!</p>

                    <p><strong>7. Indian Butter Chicken 🇮🇳</strong> - Creamy, buttery, and aromatic. Served with fluffy naan bread for dipping.</p>

                    <p><strong>8. Lebanese Baklava 🇱🇧</strong> - Layers of flaky phyllo dough, honey, and pistachios. Sweet, sticky, and irresistible.</p>

                    <p><strong>9. Thai Pad Thai 🇹🇭</strong> - Perfect balance of sweet, sour, and savory with fresh shrimp and crushed peanuts.</p>

                    <p><strong>10. German Bratwurst 🇩🇪</strong> - Grilled to perfection and served with sauerkraut and spicy mustard. Prost!</p>

                    <h3>Honorable Mentions</h3>
                    <p>Special shoutout to the Ethiopian injera with doro wat, Filipino lumpia, Greek spanakopita, and Peruvian ceviche. My stomach is still thanking me!</p>

                    <p>Can't wait for next year's food lineup. My advice: come hungry and bring friends so you can sample more dishes! 🍽️</p>
                """,
                "category": "Cultural Events",
                "featured": False,
                "read_minutes": 5,
                "image_generate": True,
            },
            # ============ OTHER CAMPUS POSTS ============
            {
                "title": "Spring Semester 2026: What You Need to Know",
                "excerpt": "Important dates, deadlines, and updates for the upcoming spring semester including new multicultural initiatives.",
                "body": """
                    <h2>Welcome Back, Students!</h2>
                    <p>The spring semester is just around the corner, and we're excited to welcome everyone back to campus. This semester brings exciting new cultural programs and diversity initiatives!</p>

                    <h3>Key Dates</h3>
                    <ul>
                        <li>January 15: Residence halls open</li>
                        <li>January 18: First day of classes</li>
                        <li>January 25: Last day to add/drop courses</li>
                        <li>February 10-14: International Education Week</li>
                        <li>March 9-13: Spring Break</li>
                        <li>April 15-20: Cultural Heritage Celebration Week</li>
                        <li>May 5: Last day of classes</li>
                    </ul>

                    <h3>New Diversity Initiatives</h3>
                    <p>We're proud to announce new cultural programs this semester including language exchange partners, international film series, and heritage month celebrations.</p>
                """,
                "category": "Campus News",
                "featured": True,
                "read_minutes": 4,
                "image_generate": True,
            },
            {
                "title": "International Student Orientation: A Guide to Campus Life",
                "excerpt": "Tips and resources for our new international students joining us this semester.",
                "body": """
                    <h2>🌍 Welcome International Students!</h2>
                    <p>We're thrilled to have students from over 50 countries joining our campus community. Here's everything you need to know to get started.</p>

                    <h3>Essential Resources</h3>
                    <ul>
                        <li><strong>International Student Office</strong> - Visa support, cultural adjustment, and community events</li>
                        <li><strong>English Language Support</strong> - Free tutoring and conversation partners</li>
                        <li><strong>Cultural Clubs</strong> - Connect with students from your home country or explore new cultures</li>
                        <li><strong>Global Mentorship Program</strong> - Get paired with an upperclassman international student</li>
                    </ul>

                    <h3>Upcoming Events for International Students</h3>
                    <p>Don't miss our International Coffee Hour every Friday at 3 PM in the Global Center. Free coffee and snacks from around the world!</p>

                    <p>Welcome to your home away from home. We're so glad you're here! 🎉</p>
                """,
                "category": "International Students",
                "featured": True,
                "read_minutes": 4,
                "image_generate": True,
            },
            {
                "title": "Black History Month Celebration: Events You Can't Miss",
                "excerpt": "Join us for a month-long celebration honoring Black history, culture, and achievement.",
                "body": """
                    <h2>✊🏾 Celebrating Black History Month</h2>
                    <p>February is Black History Month, and our campus has planned an incredible lineup of events to honor Black heritage, achievements, and contributions.</p>

                    <h3>Event Schedule</h3>
                    <ul>
                        <li><strong>Feb 1:</strong> Opening Ceremony & Keynote Speaker - Dr. Angela Davis</li>
                        <li><strong>Feb 5:</strong> African American Film Festival (free screening of "The Black Panthers")</li>
                        <li><strong>Feb 10:</strong> Soul Food Cook-Off - Taste traditional African American cuisine</li>
                        <li><strong>Feb 15:</strong> Poetry Slam - "Voices of Our Generation"</li>
                        <li><strong>Feb 20:</strong> Career Panel - Black Excellence in Business, Tech, and Arts</li>
                        <li><strong>Feb 28:</strong> Gospel Concert & Closing Celebration</li>
                    </ul>

                    <h3>Educational Opportunities</h3>
                    <p>The library has curated a special collection of books by Black authors. All events are free and open to everyone. Let's celebrate, learn, and grow together!</p>
                """,
                "category": "Arts & Culture",
                "featured": True,
                "read_minutes": 3,
                "image_generate": True,
            },
            {
                "title": "Diwali Celebration: Festival of Lights on Campus",
                "excerpt": "Hundreds gather for traditional Indian celebration with music, dance, and thousands of lights.",
                "body": """
                    <h2>🪔 Diwali: Triumph of Light Over Darkness</h2>
                    <p>The South Asian Student Association hosted our annual Diwali celebration, and it was magical. The Student Union was transformed with hundreds of diyas (oil lamps), colorful rangoli patterns, and the aroma of traditional Indian sweets.</p>

                    <h3>Evening Highlights</h3>
                    <ul>
                        <li><strong>Lighting Ceremony</strong> - 500 diyas lit simultaneously at sunset</li>
                        <li><strong>Bhangra Dance Workshop</strong> - Everyone learned energetic Punjabi folk dances</li>
                        <li><strong>Henna Art</strong> - Professional artists created stunning mehndi designs</li>
                        <li><strong>Indian Street Food</strong> - Samosas, chaat, and gulab jamun</li>
                        <li><strong>Fireworks Display</strong> - Spectacular show over the campus quad</li>
                    </ul>

                    <p>"Diwali is about community and hope," says Priya Patel, event organizer. "Seeing students from all backgrounds celebrating together made me so happy."</p>

                    <p>Mark your calendars for next year's Diwali - it's an experience you won't forget!</p>
                """,
                "category": "Cultural Events",
                "featured": True,
                "read_minutes": 4,
                "image_generate": True,
            },
            {
                "title": "Chinese New Year: Year of the Dragon Celebration",
                "excerpt": "Lion dances, dumpling-making, and red envelopes - celebrate Lunar New Year on campus.",
                "body": """
                    <h2>🐉 Welcome Year of the Dragon!</h2>
                    <p>The Chinese Student Association brought the energy with their annual Lunar New Year celebration. The Year of the Dragon symbolizes power, luck, and success - perfect energy for the new semester!</p>

                    <h3>Festival Activities</h3>
                    <ul>
                        <li><strong>Lion Dance Performance</strong> - Professional dancers brought good luck to campus</li>
                        <li><strong>Dumpling Making Workshop</strong> - Learn to fold dumplings like a pro</li>
                        <li><strong>Calligraphy Station</strong> - Get your name written in Chinese characters</li>
                        <li><strong>Red Envelope Giveaway</strong> - Traditional lucky money for students</li>
                        <li><strong>Firecracker Display</strong> - Scare away evil spirits and welcome good fortune</li>
                    </ul>

                    <p>Gong hei fat choy! Happy Lunar New Year to all celebrating.</p>
                """,
                "category": "Cultural Events",
                "featured": False,
                "read_minutes": 3,
                "image_generate": True,
            },
            {
                "title": "Cinco de Mayo: Celebrating Mexican Heritage",
                "excerpt": "Mariachi music, folkloric dancing, and authentic cuisine mark the celebration.",
                "body": """
                    <h2>🇲🇽 Cinco de Mayo Fiesta!</h2>
                    <p>The Latin American Student Organization threw an unforgettable Cinco de Mayo celebration, honoring Mexican culture and heritage.</p>

                    <h3>Festival Features</h3>
                    <ul>
                        <li>Mariachi band live performance</li>
                        <li>Ballet Folklórico traditional dancers</li>
                        <li>Taco eating competition</li>
                        <li>Pinata breaking for all ages</li>
                        <li>Salsa dancing lessons</li>
                        <li>Mexican hot chocolate and churros</li>
                    </ul>

                    <p>"Cinco de Mayo is often misunderstood in the US," explains Carlos Rodriguez, club president. "We wanted to share the real history while celebrating the beautiful culture."</p>

                    <p>¡Vamos a celebrar! 🎉</p>
                """,
                "category": "Cultural Events",
                "featured": False,
                "read_minutes": 3,
                "image_generate": True,
            },
        ]

        posts = []
        for i, post_data in enumerate(posts_data, start=1):
            category = next((cat for cat in categories if cat.name == post_data["category"]), categories[0])
            author = random.choice(users)

            # Randomize published date (within last 30 days)
            days_ago = random.randint(0, 30)
            published_at = timezone.now() - timedelta(days=days_ago)

            # Randomize status
            status = random.choice(["published", "published", "published", "published", "draft"])

            # Create the post
            post = Post(
                title=post_data["title"],
                excerpt=post_data["excerpt"],
                body=post_data["body"],
                category=category,
                author=author,
                featured=post_data["featured"],
                read_minutes=post_data["read_minutes"],
                status=status if status == "draft" else "published",
                published_at=published_at if status == "published" else timezone.now(),
            )

            # Generate and assign image if requested
            if post_data.get("image_generate", False):
                image_file = self.generate_image(post_data["title"], post_data["category"])
                post.image.save(image_file.name, image_file, save=False)
                self.stdout.write(f"  🖼️ Generated image for: {post_data['title'][:40]}...")

            post.save()

            # Add likes to featured posts
            if post_data["featured"]:
                num_likes = random.randint(15, 60)
                liked_by = random.sample(users, min(num_likes, len(users)))
                post.likes.add(*liked_by)

            posts.append(post)
            self.stdout.write(f"  📝 Created post: {post.title[:50]}...")

        return posts

    def create_comments(self, posts, users):
        """Create comments and replies on posts"""
        comment_templates = [
            "This Cultural Day was amazing! Can't wait for next year! 🎉",
            "I loved seeing everyone's traditions. So beautiful!",
            "The food was incredible. Still dreaming about those churros!",
            "This article captures the energy perfectly. Well written!",
            "As an international student, this made me feel so welcomed. Thank you!",
            "The fashion show was my favorite part! So many beautiful outfits.",
            "I brought my roommate from a different country and we both learned so much.",
            "This is what makes our campus special. Unity in diversity! ❤️",
            "The drum circle had everyone dancing! Best part of the day.",
            "I wish every day was Cultural Day! So much fun.",
            "My family came to visit and they were blown away. Great job organizers!",
            "The henna artists were incredible. Still have mine a week later!",
            "This should be a monthly event! So much culture to celebrate.",
            "I tried foods I've never heard of before. My taste buds are grateful!",
            "Shoutout to the volunteers who made this happen! 👏",
        ]

        reply_templates = [
            "Absolutely agree! It was magical ✨",
            "Thanks for sharing your experience!",
            "Couldn't have said it better myself!",
            "The organizers really outdid themselves this year.",
            "I'm already excited for next year's event!",
            "Which country's food was your favorite?",
            "The energy was truly something special.",
            "This is why I love our campus community! 🥰",
        ]

        for post in posts:
            # Add 5-12 comments per post
            num_comments = random.randint(5, 12)
            commenters = random.sample(users, min(num_comments, len(users)))

            for i, commenter in enumerate(commenters):
                comment_body = random.choice(comment_templates)
                created_days_ago = random.randint(0, 10)

                comment = Comment(
                    post=post,
                    author=commenter,
                    body=f"{comment_body} - {commenter.first_name}",
                    created_at=timezone.now() - timedelta(days=created_days_ago)
                )
                comment.save()

                self.stdout.write(f"  💬 Added comment by {commenter.first_name} on '{post.title[:30]}...'")

                # Add replies to some comments (25% chance)
                if random.random() < 0.25 and len(users) > 1:
                    replier = random.choice([u for u in users if u != commenter])
                    reply_body = random.choice(reply_templates)

                    reply = Comment(
                        post=post,
                        author=replier,
                        parent=comment,
                        body=f"{reply_body} - {replier.first_name}",
                        created_at=comment.created_at + timedelta(hours=random.randint(1, 48))
                    )
                    reply.save()
                    self.stdout.write(f"    ↳ Added reply by {replier.first_name}")

                # Add likes to comments (30% chance)
                if random.random() < 0.3:
                    likers = random.sample(users, min(random.randint(1, 5), len(users)))
                    comment.likes.add(*likers)

        self.stdout.write(self.style.SUCCESS(f"  ✨ Created comments on {len(posts)} posts"))

    def slugify(self, text):
        """Simple slugify function"""
        from django.utils.text import slugify
        return slugify(text)