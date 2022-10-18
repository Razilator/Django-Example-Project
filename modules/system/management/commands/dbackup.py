from django.core.management import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    """
    Команда для создания резервной копии базы данных
    """
    def handle(self, *args, **options):
        self.stdout.write('Waiting for database dump...')
        call_command('dumpdata', '--natural-foreign', '--natural-primary', '--exclude=contenttypes', '--exclude=admin.logentry', '--exclude=auth.permission', '--indent=4', '--output=db.json')
        self.stdout.write(self.style.SUCCESS('Database successfully backed up'))