import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Creates a superuser from env vars if one doesn't already exist.
    Safe to run on every deploy - it's a no-op if the user already exists.

    Reads: ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD
    """

    help = "Create a superuser from ADMIN_USERNAME/ADMIN_EMAIL/ADMIN_PASSWORD env vars"

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('ADMIN_USERNAME')
        email = os.environ.get('ADMIN_EMAIL', '')
        password = os.environ.get('ADMIN_PASSWORD')

        if not username or not password:
            self.stdout.write(self.style.WARNING(
                'ADMIN_USERNAME or ADMIN_PASSWORD not set - skipping superuser creation.'
            ))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(
                f'Superuser "{username}" already exists - skipping.'
            ))
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created.'))