from fabric.api import *

@hosts('applepicke@chores.willyc.me')
def production():
  code_dir = '/home/applepicke/webapps/chores/chores/'
  with cd(code_dir):
    with prefix('. /home/applepicke/.virtualenvs/chores/bin/activate'):
      run("git pull")
      run('bower install')
      run('./manage.py syncdb')
      run('./manage.py migrate chores')
      run('./manage.py collectstatic --noinput')
      run('touch chores/wsgi.py')
