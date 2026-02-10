# courses/management/commands/clean_course_data.py
from django.core.management.base import BaseCommand
from Home.models import Course
import json
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Clean course data to fix encoding issues'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be fixed without making changes',
        )
    
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        self.stdout.write('Cleaning course data...')
        if dry_run:
            self.stdout.write('DRY RUN MODE - No changes will be saved')
        
        fixed_count = 0
        error_count = 0
        
        for course in Course.objects.all():
            try:
                needs_saving = False
                
                # Clean string fields
                string_fields = [
                    'title', 'short_description', 'detailed_description',
                    'instructor_name', 'instructor_bio', 'instructor_title',
                    'duration', 'lessons', 'badge', 'icon_class', 'color'
                ]
                
                for field in string_fields:
                    original_value = getattr(course, field)
                    if original_value:
                        cleaned_value = self.clean_string(original_value)
                        if cleaned_value != original_value:
                            setattr(course, field, cleaned_value)
                            needs_saving = True
                
                # Clean JSON fields
                if course.details:
                    try:
                        # Try to parse as JSON first
                        if isinstance(course.details, str):
                            course.details = json.loads(course.details)
                        cleaned_details = self.clean_json(course.details)
                        if cleaned_details != course.details:
                            course.details = cleaned_details
                            needs_saving = True
                    except (json.JSONDecodeError, TypeError) as e:
                        logger.warning(f"Course {course.id} details JSON error: {e}")
                        # Reset to empty dict
                        course.details = {}
                        needs_saving = True
                
                if course.curriculum:
                    try:
                        # Try to parse as JSON first
                        if isinstance(course.curriculum, str):
                            course.curriculum = json.loads(course.curriculum)
                        cleaned_curriculum = self.clean_json(course.curriculum)
                        if cleaned_curriculum != course.curriculum:
                            course.curriculum = cleaned_curriculum
                            needs_saving = True
                    except (json.JSONDecodeError, TypeError) as e:
                        logger.warning(f"Course {course.id} curriculum JSON error: {e}")
                        # Reset to empty list
                        course.curriculum = []
                        needs_saving = True
                
                if needs_saving:
                    if not dry_run:
                        course.save()
                        fixed_count += 1
                        self.stdout.write(f'✓ Fixed course: {course.id} - {course.title[:50]}...')
                    else:
                        fixed_count += 1
                        self.stdout.write(f'✓ Would fix course: {course.id} - {course.title[:50]}...')
                
            except Exception as e:
                error_count += 1
                self.stdout.write(self.style.ERROR(f'✗ Error fixing course {course.id}: {e}'))
        
        self.stdout.write("\n" + "="*50)
        if dry_run:
            self.stdout.write(self.style.WARNING(
                f'DRY RUN RESULTS:\n'
                f'• Would fix: {fixed_count} courses\n'
                f'• Errors: {error_count} courses\n'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'CLEANUP COMPLETE:\n'
                f'• Fixed: {fixed_count} courses\n'
                f'• Errors: {error_count} courses\n'
            ))
        self.stdout.write("="*50)
    
    def clean_string(self, value):
        """Clean a string by removing invalid UTF-8 characters."""
        if value is None:
            return ""
        
        if isinstance(value, bytes):
            # If it's bytes, decode it
            try:
                value = value.decode('utf-8', 'ignore')
            except:
                try:
                    value = value.decode('latin-1', 'ignore')
                except:
                    value = str(value, errors='ignore')
        
        if isinstance(value, str):
            # Remove control characters and invalid Unicode
            cleaned = []
            for char in value:
                try:
                    char.encode('utf-8')
                    # Only keep printable characters
                    if ord(char) >= 32 or char in '\n\r\t':
                        cleaned.append(char)
                except UnicodeEncodeError:
                    # Skip invalid characters
                    continue
            return ''.join(cleaned)
        
        return str(value)
    
    def clean_json(self, data):
        """Recursively clean JSON data."""
        if isinstance(data, dict):
            cleaned = {}
            for key, value in data.items():
                cleaned_key = self.clean_string(key)
                cleaned_value = self.clean_json(value)
                cleaned[cleaned_key] = cleaned_value
            return cleaned
        
        elif isinstance(data, list):
            cleaned = []
            for item in data:
                cleaned.append(self.clean_json(item))
            return cleaned
        
        elif isinstance(data, (str, bytes)):
            return self.clean_string(data)
        
        else:
            # For numbers, booleans, None
            return data