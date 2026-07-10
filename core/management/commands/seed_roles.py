from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

ROLES = [
    "Admin", "Manager", "Accountant", "Sales", "Purchase",
    "Inventory", "HR", "Payroll", "CRM", "Auditor",
    "Branch Manager", "Cashier", "Store Keeper",
]

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for name in ROLES:
            group, created = Group.objects.get_or_create(name=name)
            self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Exists'}: {name}"))