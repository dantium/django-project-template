from fabric.api import env
from deploy.fabric_common import *

# common settings
env.forward_agent = True
env.git_path =  '{{ git_path }}' # 'git@bitbucket.org:dantium/{{ project_name }}.git'
env.app_name = '{{ project_name }}'

#env.key_filename = '/path/to/keyfile.pem'
        
def _configure():
    #env.use_ssh_config = True
    env.project_path = '%(base_path)s/sites/%(app_name)s' % env
    env.app_path = '/%(project_path)s/%(app_name)s/' % env
    env.virtualenv = '%(base_path)s/virtualenvs/%(app_name)s' % env
    env.activate = 'source %(virtualenv)s/bin/activate' % env
    env.settings = '%(app_name)s.settings.%(build)s' % env
    env.nginx_conf = 'deploy/nginx/%(build)s.conf' % env
    env.wsgi = 'deploy/wsgi/%(build)s.wsgi' % env
    if not env.hosts: env.hosts = [env.domain]
  

@task
def production():
    #env.port = 2222
    env.app_port = 8000
    env.production = True
    env.domain = "production.{{ domain_name }}"
    env.build = "production"
    env.base_path = '/home'
    env.user = "root"
    _configure()

@task
def staging():
    #env.port = 2222
    env.app_port = 8000
    env.production = False
    env.domain  = "staging.{{ domain_name }}"
    env.build = "staging" 
    env.user = "root"
    env.base_path = '/home'
    _configure()