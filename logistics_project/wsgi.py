"""
WSGI config for logistics_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_project.settings')

# Run migrations automatically on startup (for Render deployment)
# Also create admin user if not exists
try:
    from django.core.management import execute_from_command_line
    from django.db import connection
    from django.contrib.auth import get_user_model
    
    # Check if tables exist
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='logistics_booking'")
        if not cursor.fetchone():
            print("Running initial migrations...")
            execute_from_command_line(['manage.py', 'migrate', '--noinput'])
            print("Migrations complete!")
    
    # Create admin user if not exists
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        print("Creating admin user...")
        User.objects.create_superuser('admin', 'admin@fleeting.com', 'admin123')
        print("Admin created: admin / admin123")
except Exception as e:
    print(f"Auto-setup: {e}")

application = get_wsgi_application()
