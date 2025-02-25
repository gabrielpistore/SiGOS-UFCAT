import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from orders.models import Category, Department, Employee, WorkOrder

fake = Faker("pt_BR")


class Command(BaseCommand):
    help = "Populate database for development."

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting...")

        # Create superuser
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "", "admin")

        # Create categories
        categories = list(Category.objects.all())
        if not categories:
            call_command("populate_categories")
            categories = list(Category.objects.all())

        # Create departments
        departments = list(Department.objects.all())
        if not departments:
            call_command("populate_dept")
            departments = list(Department.objects.all())

        # Create employees
        employees = []
        for _ in range(10):
            employee = Employee.objects.create(
                name=fake.name(),
                email=fake.email(),
                mobile_phone=fake.phone_number(),
            )
            employees.append(employee)
        self.stdout.write(self.style.SUCCESS(f"Created {len(employees)} employees."))

        levels = [choice[0] for choice in WorkOrder.LEVEL]
        statuses = [choice[0] for choice in WorkOrder.STATUS]

        # Create orders
        for _ in range(50):
            service_start_date = timezone.now()
            service_end_date = service_start_date + timedelta(
                days=random.randint(1, 10)
            )

            WorkOrder.objects.create(
                requested_by=fake.name(),
                dept_name=random.choice(departments),
                email=fake.email(),
                phone=fake.phone_number(),
                category=random.choice(categories),
                responsible_employee=random.choice(employees),
                impact=random.choice(levels),
                urgency=random.choice(levels),
                priority=random.choice(levels),
                location=fake.sentence(nb_words=3),
                service_start_date=service_start_date,
                service_end_date=service_end_date,
                status=random.choice(statuses),
                title=fake.sentence(nb_words=3),
                report_description=fake.paragraph(nb_sentences=5),
                image=None,
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )

        self.stdout.write(self.style.SUCCESS("Created 50 work orders."))
        self.stdout.write(self.style.SUCCESS("Completed."))
