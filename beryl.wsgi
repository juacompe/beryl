#!/usr/bin/env python

import sys, os, site

reload(sys)
sys.setdefaultencoding('utf-8')

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.abspath(os.path.dirname(CUR_DIR))
##/ve/bargain/
ALLDIRS = ['/home/www-data/beryl/beryl_env27/lib/python2.7/site-packages/']
prev_sys_path = list(sys.path)

for directory in ALLDIRS:
    site.addsitedir(directory)

new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
       new_sys_path.append(item)
       sys.path.remove(item)

sys.path[:0] = new_sys_path

sys.path.insert(0, PARENT_DIR)
sys.path.insert(0, CUR_DIR)


os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
