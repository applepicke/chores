from fabric.api import *

@hosts('applepicke@chores.willyc.me')
def production():
  code_dir = '/home/applepicke/webapps/chores/chores/'
  supervisor_dir = '/home/applepicke/etc/'

  with prefix('. /home/applepicke/.virtualenvs/chores/bin/activate'):
    with cd(code_dir):
      run("git pull")
      run('bower install')
      run('./manage.py syncdb')
      run('./manage.py migrate chores')
      run('./manage.py collectstatic --noinput')
      run('touch chores/wsgi.py')
    with cd(supervisor_dir):
      run('supervisorctl restart chores-celery-tasks')
      run('supervisorctl restart chores-celery-periodic')


