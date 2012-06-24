"""
To automatically load fixtures in "iconfig/fixtures/project_data"

Usage:

$ python manage.py init_project_data

"""
from django.core.management.base import BaseCommand, CommandError
from iconfig import fixtures_path,loaddata

class Command(BaseCommand):



    def handle(self, *args, **options):
        #loaddata_in_folder('project_data')
        verbosity=1
        loaddata(fixtures_path('project_data', 'site.xml' ), verbosity)