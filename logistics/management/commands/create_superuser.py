"""
Django management command to create a superuser from environment variables.

This command reads DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, and
DJANGO_SUPERUSER_PASSWORD from environment variables and creates a superuser
if one with the given username doesn't already exist.

Usage:
    python manage.py create_superuser

Environment Variables Required:
    - DJANGO_SUPERUSER_USERNAME: The username for the superuser
    - DJANGO_SUPERUSER_EMAIL: The email for the superuser
    - DJANGO_SUPERUSER_PASSWORD: The password for the superuser

The command is idempotent - running it multiple times is safe and won't
create duplicate users.
"""

import os
import sys

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Creates a superuser from environment variables DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, and DJANGO_SUPERUSER_PASSWORD'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update password even if user exists',
        )

    def handle(self, *args, **options):
        User = get_user_model()

        # Get environment variables
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        # Check if required environment variables are set (email is optional)
        missing = []
        if not username:
            missing.append('DJANGO_SUPERUSER_USERNAME')
        if not password:
            missing.append('DJANGO_SUPERUSER_PASSWORD')

        if missing:
            self.stderr.write(
                self.style.ERROR(
                    f"Missing required environment variables: {', '.join(missing)}"
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    "Set these environment variables before running this command."
                )
            )
            sys.exit(1)

        # Use empty string for email if not provided
        if not email:
            email = ''

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            self.stdout.write(
                self.style.NOTICE(
                    f"User '{username}' already exists."
                )
            )
            if options['force']:
                user.email = email
                user.is_staff = True
                user.is_superuser = True
                user.set_password(password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Password updated for user '{username}'."
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        "Use --force to update the existing user's password."
                    )
                )
            return

        # Create the superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ Superuser '{username}' created successfully!"
            )
        )
        self.stdout.write(f"   Email: {email}")
        self.stdout.write(f"   Admin URL: /admin/")
