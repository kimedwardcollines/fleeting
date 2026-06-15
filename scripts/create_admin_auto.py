#!/usr/bin/env python
"""Automated script to create/update an admin superuser with hardcoded credentials."""
"""WARNING: Delete this file after use!"""

import os
import sys
import traceback

print("=" * 50)
print("ADMIN USER CREATION SCRIPT")
print("=" * 50)

try:
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_project.settings')
    
    print("Setting up Django...")
    import django
    django.setup()
    print("Django setup complete.")

    from django.contrib.auth import get_user_model
    User = get_user_model()

    # Configure your admin credentials here
    ADMIN_USERNAME = "admin"
    ADMIN_EMAIL = "admin@fleeting.com"
    ADMIN_PASSWORD = "admin123"

    print(f"\nCreating/updating admin user: {ADMIN_USERNAME}")
    
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
        print(f"✅ Admin user '{ADMIN_USERNAME}' CREATED successfully!")
    else:
        print(f"✅ Admin user '{ADMIN_USERNAME}' UPDATED successfully!")

    print(f"\nLogin credentials:")
    print(f"  URL: https://fleeting-g9x8.onrender.com/admin/")
    print(f"  Username: {ADMIN_USERNAME}")
    print(f"  Password: {ADMIN_PASSWORD}")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 50)
print("SCRIPT COMPLETED SUCCESSFULLY")
print("=" * 50)
