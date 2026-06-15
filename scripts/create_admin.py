#!/usr/bin/env python
"""Script to create or update an admin superuser."""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = input("Enter admin username (default: admin): ").strip() or "admin"
email = input("Enter admin email (default: admin@fleeting.com): ").strip() or "admin@fleeting.com"
password = input("Enter admin password: ").strip()

if not password:
    print("Error: Password cannot be empty.")
    sys.exit(1)

user, created = User.objects.get_or_create(
    username=username,
    defaults={'email': email, 'is_staff': True, 'is_superuser': True}
)

user.email = email
user.is_staff = True
user.is_superuser = True
user.set_password(password)
user.save()

if created:
    print(f"✅ Admin user '{username}' created successfully!")
else:
    print(f"✅ Admin user '{username}' updated successfully!")

print(f"\nLogin at: /admin/")
print(f"Username: {username}")
print(f"Email: {email}")
