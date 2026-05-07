#!/bin/bash
# reset_db.sh - Run this in your terminal

echo "🔄 COMPLETE DATABASE RESET"
echo "========================="

# 1. Delete the database
echo "📁 Deleting database..."
rm -f db.sqlite3

# 2. Delete all migration files
echo "🗑 Deleting migration files..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/__pycache__" -exec rm -rf {} + 2>/dev/null

# 3. Remove __pycache__ folders
echo "🧹 Cleaning cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# 4. Create new migrations
echo "🔧 Creating migrations..."
python manage.py makemigrations Users
python manage.py makemigrations

# 5. Apply migrations
echo "⚡ Applying migrations..."
python manage.py migrate

# 6. Create superuser
echo "👤 Create a superuser:"
python manage.py createsuperuser

# 7. Run server
echo "🚀 Starting server..."
python manage.py runserver