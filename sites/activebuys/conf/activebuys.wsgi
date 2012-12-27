import os, sys, site

site.addsitedir('/apps/.virtualenvs/activebuys-env/lib/python2.6/site-packages')

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
sys.path.insert(0, PROJECT_ROOT)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

os.environ['DJANGO_SETTINGS_MODULE'] = 'activebuys.settings'
os.environ['SITE_KEY'] = 'activebuys'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()