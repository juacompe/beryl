import os
from copy import copy
from django.core.management import call_command
from django.conf import settings
from django import db
from django.core.management.base import BaseCommand, CommandError

fixtures_path = lambda *p: os.path.abspath(os.path.join(settings.CURDIR, 'iconfig', 'fixtures', *p))

def loaddata(filename, verbosity=0 ):
    path = fixtures_path(filename)
    if not os.path.exists(path):
        raise IOError("File does not exist: " + path)

    call_command('loaddata', path, verbosity=verbosity)



def loaddata_in_folder( folder_name ):
        # list all file in fixtures
        allfilepath = [fixtures_path(folder_name, filename) for filename in (fixtures_path(folder_name))]

        # filter only file (not directory)
        fixtures = filter(lambda p: not os.path.isdir(p), allfilepath)

        failure = []
        fixtures_length = len(fixtures)

        # keep trying load data, maybe its dependencee is not loaded yet.
        while len(fixtures) and (len(failure) < fixtures_length):
            failure = []
            for filepath in fixtures:
                try:
                    loaddata(filepath, verbosity=1)
                    print 'Loaded:', filepath
                except Exception, e:
                    db.close_connection()
                    failure.insert(0, filepath)

            fixtures_length = len(fixtures)
            fixtures = failure