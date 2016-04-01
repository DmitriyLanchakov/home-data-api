from homes.settings import *


os.environ['HTTPS'] = ""

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


