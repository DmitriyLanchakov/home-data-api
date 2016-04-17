from homes.settings import *

SECRET_KEY = '!0n!j@xhrmmspj0)l5^^d8utem*y*k-5*4jbb1x9p&wz6_h+ju'

JWT_AUTH['JWT_SECRET_KEY'] = SECRET_KEY

os.environ['HTTPS'] = ""

DEBUG = True

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False
SECURE_PROXY_SSL_HEADER = () #('HTTP_X_FORWARDED_PROTOCOL', 'https')

DATABASES = {
        'default': {
            'NAME': 'tests.db',
            'ENGINE': 'django.db.backends.sqlite3'
        }
}

LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                },
            },
        'loggers': {
            'api.models': {
                'handlers': ['console'],
                'level': 'INFO',
                },
            },
        }


