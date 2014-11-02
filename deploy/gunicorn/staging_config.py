pidfile = '/tmp/gunicorn_{{ project_name }}.pid'
proc_name = '{{ project_name }}'
workers = 1
bind = 'unix:/tmp/gunicorn_{{ project_name }}.sock'