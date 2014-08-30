from fabric.api import *

@hosts('applepicke@chores.willyc.me')
def production():
  code_dir = '/home/applepicke/webapps/chores/chores/'
  python = '/home/applepicke/webapps/chores/env/default/bin/python'
  with cd(code_dir):
    run("git pull")
    run('%s manage.py syncdb' % python)
    run('bower install')
    run('%s manage.py collectstatic' % python)
    run('touch chores/wsgi.py')
