import random

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from core.models import Category, Employee, WorkOrder

fake = Faker("pt_BR")


class Command(BaseCommand):
    help = "Generate fake data for testing purposes"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting...")

        # Create Categories
        categories = []
        for _ in range(10):
            category = Category.objects.create(name=fake.word().capitalize())
            categories.append(category)
        self.stdout.write(f"Created {len(categories)} categories.")

        # Create Employees
        employees = []
        for _ in range(20):
            employee = Employee.objects.create(
                name=fake.name(),
                email=fake.email(),
                mobile_phone=fake.phone_number(),
            )
            employees.append(employee)
        self.stdout.write(f"Created {len(employees)} employees.")

        # Create orders
        dept_names = [choice[0] for choice in WorkOrder.DEPT_NAMES]
        levels = [choice[0] for choice in WorkOrder.LEVEL]
        statuses = [choice[0] for choice in WorkOrder.STATUS]
        for _ in range(50):
            opening_date = timezone.make_aware(fake.date_time_this_year(), timezone.get_current_timezone())
            closing_date = timezone.make_aware(fake.date_time_this_year(), timezone.get_current_timezone())
            service_start_date = timezone.make_aware(fake.date_time_this_year(), timezone.get_current_timezone())
            service_end_date = timezone.make_aware(fake.date_time_this_year(), timezone.get_current_timezone())

            WorkOrder.objects.create(
                requested_by=fake.name(),
                dept_name=random.choice(dept_names),
                email=fake.email(),
                phone=fake.phone_number(),
                category=random.choice(categories),
                responsible_employee=random.choice(employees),
                impact=random.choice(levels),
                urgency=random.choice(levels),
                priority=random.choice(levels),
                location=fake.address(),
                opening_date=opening_date,
                closing_date=closing_date,
                service_start_date=service_start_date,
                service_end_date=service_end_date,
                status=random.choice(statuses),
                title=fake.sentence(nb_words=6),
                report_description=fake.paragraph(nb_sentences=5),
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )

        self.stdout.write("Created 50 work orders.")
        self.stdout.write(self.style.SUCCESS("Completed."))
