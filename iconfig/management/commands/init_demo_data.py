"""
To automatically load fixtures in "iconfig/fixtures/project_data"

Usage:

$ python manage.py init_demo_data

"""

from init_project_data import Command as Init_Command
from iconfig import fixtures_path, loaddata

class Command(Init_Command):

    def handle(self, *args, **options):
        verbosity=1
        loaddata(fixtures_path('demo_data', 'school.classroom.json' ), verbosity)
        loaddata(fixtures_path('demo_data', 'school.student.json' ), verbosity)
        loaddata(fixtures_path('demo_data', 'auth.group.json' ), verbosity)
        loaddata(fixtures_path('demo_data', 'auth.json' ), verbosity)
        loaddata(fixtures_path('demo_data', 'finance.invoice.json' ), verbosity)
        loaddata(fixtures_path('demo_data', 'finance.invoiceitem.json' ), verbosity)
        loaddata(fixtures_path('demo_data', 'finance.receipt.json' ), verbosity)
        loaddata(fixtures_path('demo_data', 'finance.receiptitem.json' ), verbosity)