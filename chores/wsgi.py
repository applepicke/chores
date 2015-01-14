"""
WSGI config for chores project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, sys, site
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chores.settings")

site.addsitedir('/home/applepicke/.virtualenvs/chores/lib/python2.7/site-packages')

activate_this = os.path.expanduser("~/.virtualenvs/chores/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

# Calculate the path based on the location of the WSGI script
project = '/home/applepicke/webapps/chores/'
workspace = os.path.dirname(project)
sys.path.append(workspace)

sys.path = ['/home/applepicke/webapps/chores/chores', '/home/applepicke/webapps/chores'] + sys.path

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()