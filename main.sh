#!/bin/bash

# ============================================
# Django Migration and SQLite Database Manager
# ============================================
# This script:
# 1. Backs up the SQLite database
# 2. Deletes all migration files
# 3. Deletes the SQLite database
# 4. Restores the backup (optional)
# ============================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="."  # Change this to your Django project root
DB_FILE="db.sqlite3"
BACKUP_DIR="database_backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="db_backup_${TIMESTAMP}.sqlite3"

# Function to print colored messages
print_message() {
    echo -e "${2}${1}${NC}"
}

# Function to show usage
show_usage() {
    print_message "Usage: $0 [OPTIONS]" "$BLUE"
    echo ""
    print_message "OPTIONS:" "$YELLOW"
    print_message "  -b, --backup-only     Create backup only (don't delete anything)" "$GREEN"
    print_message "  -d, --delete-only     Delete migrations and DB without backup" "$GREEN"
    print_message "  -r, --restore FILE    Restore from specific backup file" "$GREEN"
    print_message "  -l, --list-backups    List all available backups" "$GREEN"
    print_message "  -h, --help            Show this help message" "$GREEN"
    echo ""
    print_message "Examples:" "$YELLOW"
    print_message "  $0                    # Backup, delete all, then restore (full reset)" "$GREEN"
    print_message "  $0 --backup-only      # Create backup only" "$GREEN"
    print_message "  $0 --delete-only      # Delete migrations and DB only" "$GREEN"
    print_message "  $0 --restore db_backup_20240101_120000.sqlite3  # Restore specific backup" "$GREEN"
    print_message "  $0 --list-backups     # Show all backups" "$GREEN"
}

# Function to create backup
create_backup() {
    print_message "📦 Creating database backup..." "$BLUE"

    # Create backup directory if it doesn't exist
    if [ ! -d "$BACKUP_DIR" ]; then
        mkdir -p "$BACKUP_DIR"
        print_message "✓ Created backup directory: $BACKUP_DIR" "$GREEN"
    fi

    # Check if database exists
    if [ -f "$DB_FILE" ]; then
        # Copy database to backup
        cp "$DB_FILE" "$BACKUP_DIR/$BACKUP_NAME"
        print_message "✓ Database backed up to: $BACKUP_DIR/$BACKUP_NAME" "$GREEN"

        # Get file size
        FILE_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_NAME" | cut -f1)
        print_message "  Backup size: $FILE_SIZE" "$YELLOW"

        echo "$BACKUP_NAME"
    else
        print_message "⚠ No database file found to backup!" "$YELLOW"
        echo ""
    fi
}

# Function to list backups
list_backups() {
    print_message "\n📋 Available Database Backups:" "$BLUE"
    echo "================================"

    if [ -d "$BACKUP_DIR" ] && [ "$(ls -A $BACKUP_DIR)" ]; then
        ls -lh "$BACKUP_DIR" | grep -v "^total" | awk '{print "  " $9 " (" $5 ")"}'
        echo ""
        print_message "Total backups: $(ls -1 $BACKUP_DIR | wc -l)" "$GREEN"
    else
        print_message "  No backups found in $BACKUP_DIR" "$YELLOW"
    fi
}

# Function to delete migration files
delete_migrations() {
    print_message "\n🗑 Deleting migration files..." "$BLUE"

    # Find and delete all migration files (except __init__.py)
    MIGRATION_COUNT=0

    # Find all apps with migrations
    for app_dir in $(find . -type d -name "migrations" -not -path "*/venv/*" -not -path "*/env/*" -not -path "*/__pycache__/*"); do
        if [ -d "$app_dir" ]; then
            # Delete all migration files except __init__.py
            for migration_file in "$app_dir"/*.py; do
                if [ -f "$migration_file" ] && [ "$(basename "$migration_file")" != "__init__.py" ]; then
                    rm "$migration_file"
                    print_message "  ✓ Deleted: $migration_file" "$GREEN"
                    ((MIGRATION_COUNT++))
                fi
            done

            # Also delete __pycache__ migration files
            if [ -d "$app_dir/__pycache__" ]; then
                rm -rf "$app_dir/__pycache__"/*.pyc 2>/dev/null
                print_message "  ✓ Cleared __pycache__ in $app_dir" "$GREEN"
            fi
        fi
    done

    print_message "\n✓ Deleted $MIGRATION_COUNT migration files" "$GREEN"
}

# Function to delete SQLite database
delete_database() {
    print_message "\n🗄 Deleting SQLite database..." "$BLUE"

    if [ -f "$DB_FILE" ]; then
        rm "$DB_FILE"
        print_message "✓ Database deleted: $DB_FILE" "$GREEN"
    else
        print_message "⚠ No database file found to delete" "$YELLOW"
    fi
}

# Function to restore database
restore_database() {
    local backup_file=$1

    print_message "\n🔄 Restoring database from backup..." "$BLUE"

    # If no backup file specified, use the latest
    if [ -z "$backup_file" ]; then
        if [ -d "$BACKUP_DIR" ] && [ "$(ls -A $BACKUP_DIR 2>/dev/null)" ]; then
            backup_file=$(ls -t "$BACKUP_DIR"/*.sqlite3 2>/dev/null | head -1)
            if [ -n "$backup_file" ]; then
                backup_file=$(basename "$backup_file")
                print_message "  Using latest backup: $backup_file" "$YELLOW"
            fi
        fi
    fi

    # Check if backup exists
    if [ -f "$BACKUP_DIR/$backup_file" ]; then
        cp "$BACKUP_DIR/$backup_file" "$DB_FILE"
        print_message "✓ Database restored from: $BACKUP_DIR/$backup_file" "$GREEN"

        # Get file size
        FILE_SIZE=$(du -h "$DB_FILE" | cut -f1)
        print_message "  Restored size: $FILE_SIZE" "$YELLOW"
    else
        print_message "✗ Backup file not found: $BACKUP_DIR/$backup_file" "$RED"
        print_message "  Use --list-backups to see available backups" "$YELLOW"
        exit 1
    fi
}

# Function to run Django migrations
run_migrations() {
    print_message "\n🔄 Running Django migrations..." "$BLUE"

    # Check if we're in a Django environment
    if command -v python &> /dev/null; then
        # Create new migrations
        python manage.py makemigrations
        if [ $? -eq 0 ]; then
            print_message "✓ Migrations created" "$GREEN"
        else
            print_message "✗ Failed to create migrations" "$RED"
            return 1
        fi

        # Apply migrations
        python manage.py migrate
        if [ $? -eq 0 ]; then
            print_message "✓ Migrations applied successfully" "$GREEN"
        else
            print_message "✗ Failed to apply migrations" "$RED"
            return 1
        fi
    else
        print_message "⚠ Python not found. Please run migrations manually." "$YELLOW"
    fi
}

# Function to create superuser (optional)
create_superuser() {
    print_message "\n👤 Do you want to create a superuser? (y/n)" "$YELLOW"
    read -r create_su

    if [[ $create_su == "y" || $create_su == "Y" ]]; then
        python manage.py createsuperuser
    fi
}

# Function to run full reset
full_reset() {
    print_message "\n🔄 Starting Full Database Reset..." "$BLUE"
    print_message "======================================" "$BLUE"

    # Step 1: Create backup
    backup_name=$(create_backup)

    # Step 2: Delete migrations
    delete_migrations

    # Step 3: Delete database
    delete_database

    # Step 4: Run migrations
    run_migrations

    # Step 5: Option to restore backup
    if [ -n "$backup_name" ]; then
        print_message "\n💾 Do you want to restore the backup? (y/n)" "$YELLOW"
        read -r restore_choice

        if [[ $restore_choice == "y" || $restore_choice == "Y" ]]; then
            restore_database "$backup_name"
        else
            print_message "  Skipping restore. Fresh database created." "$YELLOW"
            create_superuser
        fi
    fi

    print_message "\n✅ Database reset completed!" "$GREEN"
}

# Function to clean Python cache files
clean_cache() {
    print_message "\n🧹 Cleaning Python cache files..." "$BLUE"

    # Find and delete all __pycache__ directories
    find . -type d -name "__pycache__" -not -path "*/venv/*" -not -path "*/env/*" -exec rm -rf {} + 2>/dev/null
    print_message "✓ Removed all __pycache__ directories" "$GREEN"

    # Delete .pyc files
    find . -type f -name "*.pyc" -not -path "*/venv/*" -not -path "*/env/*" -delete 2>/dev/null
    print_message "✓ Removed all .pyc files" "$GREEN"
}

# Main script logic
case "${1}" in
    -b|--backup-only)
        create_backup
        ;;

    -d|--delete-only)
        print_message "⚠ WARNING: This will delete all migrations and database!" "$RED"
        print_message "Type 'yes' to confirm: " "$YELLOW"
        read -r confirm

        if [ "$confirm" = "yes" ]; then
            delete_migrations
            delete_database
            clean_cache
            print_message "\n✓ Deletion completed!" "$GREEN"
        else
            print_message "Operation cancelled." "$YELLOW"
        fi
        ;;

    -r|--restore)
        restore_database "$2"
        run_migrations
        ;;

    -l|--list-backups)
        list_backups
        ;;

    -h|--help)
        show_usage
        ;;

    *)
        # Default: Full reset
        print_message "⚠ WARNING: This will backup, delete ALL migrations, and reset the database!" "$RED"
        print_message "Type 'yes' to continue: " "$YELLOW"
        read -r confirm

        if [ "$confirm" = "yes" ]; then
            full_reset
            clean_cache
        else
            print_message "Operation cancelled." "$YELLOW"
        fi
        ;;
esac

# Print final summary if full reset was done
if [ -z "${1}" ] && [ "$confirm" = "yes" ]; then
    print_message "\n📊 Summary:" "$BLUE"
    print_message "==========" "$BLUE"
    print_message "✓ Backups stored in: $BACKUP_DIR/" "$GREEN"
    print_message "✓ Migration files: Reset" "$GREEN"
    print_message "✓ Database: Fresh state" "$GREEN"
    print_message "✓ Cache files: Cleaned" "$GREEN"
    print_message "\n💡 Tip: Run 'python manage.py runserver' to start your app" "$YELLOW"
fi