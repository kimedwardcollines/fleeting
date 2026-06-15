#!/usr/bin/env python
"""Automated script to create/update an admin superuser with hardcoded credentials."""
"""WARNING: Delete this file after use!"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Configure your admin credentials here
ADMIN_USERNAME = "admin"
ADMIN_EMAIL = "admin@fleeting.com"
ADMIN_PASSWORD = "admin123"

user, created = User.objects.get_or_create(
    username=ADMIN_USERNAME,
    defaults={'email': ADMIN_EMAIL, 'is_staff': True, 'is_superuser': True}
)

user.email = ADMIN_EMAIL
user.is_staff = True
user.is_superuser = True
user.set_password(ADMIN_PASSWORD)
user.save()

if created:
    print(f"✅ Admin user '{ADMIN_USERNAME}' created successfully!")
else:
    print(f"✅ Admin user '{ADMIN_USERNAME}' updated successfully!")

print(f"\nLogin at: /admin/")
print(f"Username: {ADMIN_USERNAME}")
print(f"Email: {ADMIN_EMAIL}")
