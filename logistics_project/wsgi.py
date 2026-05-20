"""
WSGI config for logistics_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_project.settings')

# Run migrations automatically on startup
try:
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    print("Migrations complete!")
except Exception as e:
    print(f"Migration error: {e}")

# Create admin user on startup
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@fleeting.com', 'admin123')
        print("Admin created: admin / admin123")
except Exception as e:
    print(f"Admin creation error: {e}")

application = get_wsgi_application()
