# ignored in .gitignore by default

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '{{ project_name }}.db',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

DEBUG = True

# testng
WSGI_APPLICATION = None
ROOT_URLCONF = 'project_name.urls'
ALLOWED_HOSTS = ['localhost']

INTERNAL_IPS = ('10.0.2.2',)