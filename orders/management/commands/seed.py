import os

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

load_dotenv()


class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting...")

        # Create superuser
        User = get_user_model()
        if not User.objects.filter(username=os.getenv("SUPERUSER_USERNAME")).exists():
            User.objects.create_superuser(
                os.getenv("SUPERUSER_USERNAME"), "", os.getenv("SUPERUSER_PASSWORD")
            )

        # Create Categories
        call_command("populate_categories")

        # Create departments
        call_command("populate_dept")
