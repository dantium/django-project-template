pidfile = '/var/run/gunicorn_{{ project_name }}.pid'
proc_name = '{{ project_name }}'
workers = 3
bind = 'unix:/tmp/gunicorn_{{ project_name }}.sock'