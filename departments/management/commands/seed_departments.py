from django.core.management.base import BaseCommand

from departments.models import Department


class Command(BaseCommand):
    help = "Seed SarvaHConn departments"

    def handle(self, *args, **options):

        departments = [
            {
                "code": "REVENUE",
                "name": "Revenue Department",
                "description": "Handles revenue, domicile and residence related government services.",
                "icon": "bi-building",
            },
            {
                "code": "EDUCATION",
                "name": "Education Department",
                "description": "Handles scholarships, education certificates and student benefit schemes.",
                "icon": "bi-mortarboard",
            },
            {
                "code": "HEALTH",
                "name": "Health Department",
                "description": "Handles health schemes, benefit verification and medical assistance.",
                "icon": "bi-heart-pulse",
            },
        ]

        for data in departments:

            department, created = Department.objects.update_or_create(
                code=data["code"],
                defaults={
                    "name": data["name"],
                    "description": data["description"],
                    "icon": data["icon"],
                    "is_active": True,
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created department: {department.name}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Updated department: {department.name}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS("Departments seeded successfully.")
        )