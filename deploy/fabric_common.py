import datetime
import os

from fabric.decorators import runs_once
from fabric.operations import put, prompt
from fabric.colors import green, red
from fabric.api import cd, run, env, task, require, put, sudo
from fabric.contrib.files import upload_template



def notify(msg):
    bar = '+' + '-' * (len(msg) + 2) + '+'
    print green('')
    print green(bar)
    print green("| %s |" % msg)
    print green(bar)
    print green('')

def pull_source_code():
    with cd(env.project_path):
        run('git pull')
        run('git submodule init')                
        run('git submodule update')

def virtualenv( command ):
    " Run a specified command inside the virtual env "
    with cd(env.project_path):
        run("%s && %s" % (env.activate, command))

def update_virtualenv():
    """
    Install the dependencies in the requirements file
    """
    notify("Running pip requierments")
    virtualenv('pip install -r requirements/server.txt')

def collect_static_files():
    notify("Collecting static files")
    virtualenv('python manage.py collectstatic --settings=%(settings)s --noinput > /dev/null' % env)

def migrate():
    """
    Apply any schema alterations
    """
    notify("Applying database migrations")
    with cd(env.project_path):
        run('%(activate)s && python manage.py syncdb --settings=%(settings)s --noinput > /dev/null' % env)
        run('%(activate)s && python manage.py migrate --settings=%(settings)s --ignore-ghost-migrations' % env)


def deploy_nginx_config():
    notify('Moving nginx config into place')
    with cd(env.project_path):
        upload_template('deploy/nginx/template.conf', 
            '/etc/nginx/conf.d/%(app_name)s.conf' % env, context=env, mode=0777)

def deploy_supervisor_config():
    notify('Moving supervisor config into place')
    with cd(env.project_path):
        upload_template('deploy/supervisor/template.conf', 
            '/etc/supervisor/conf.d/%(project_name)s.conf' % env, context=env, mode=0777)


def reload_nginx():
    notify('Reloading nginx configuration')
    sudo('/etc/init.d/nginx force-reload')

def restart_app():
    notify('Restarting supervisord instance')
    run("sudo supervisorctl restart %(project_name)s" % env)


# Server setup
def install_less():
    virtualenv('pip install nodeenv')
    virtualenv('nodeenv --python-virtualenv')
    virtualenv('npm install -g less')



@task
def setup_deployment():
    """
    Setup the deployment configuration
    """
    pull_source_code()
    deploy_supervisor_config()
    deploy_nginx_config()
    reload_nginx()
    restart_app()

@task
def deploy():   
    pull_source_code()
    update_virtualenv()            
    migrate()
    collect_static_files()
    restart_app()


