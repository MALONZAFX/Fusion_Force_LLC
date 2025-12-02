# main/management/commands/create_superuser.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates a superuser if not exists'

    def handle(self, *args, **options):
        if not User.objects.filter(username='Pamela').exists():
            User.objects.create_superuser(
                username='Pamela',
                email='pamela@fusionforce.com',
                password='Pamela@2025'
            )
            self.stdout.write(self.style.SUCCESS('Superuser "Pamela" created'))
        else:
            self.stdout.write('Superuser "Pamela" already exists')