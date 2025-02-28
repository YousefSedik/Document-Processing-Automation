from django.core.management.base import BaseCommand
from document.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        Category.objects.all().delete()
        Category.objects.create(name="Financial Documents")
        Category.objects.create(name="Legal Documents")
        Category.objects.create(name="Personal Documents")
        Category.objects.create(name="Business Documents")
