# Django settings for example project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

SITE_ID = 1

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'a2j43z$c+s#v@9^7$zlqjty)s--v655_8*lkkvuz7&d-6(9d=v'

ROOT_URLCONF = 'example.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'example.wsgi.application'
