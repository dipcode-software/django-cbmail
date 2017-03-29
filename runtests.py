import django
import sys
import os

from django.test.runner import DiscoverRunner
from django.conf import settings

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'mailings',
    ),
    MAILINGS={
        'DEFAULT_REPLY_TO': "replyto@unittest.com",
        'DEFAULT_SUJECT': "Unit test default",
        'BASE_URL': "https://domain.com",
    },
    DEFAULT_FROM_EMAIL="unit@unit.com",
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.abspath(os.path.dirname(__file__)),
                 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }]
)


if __name__ == "__main__":
    django.setup()
    runner = DiscoverRunner()
    failures = runner.run_tests(['mailings'])
    if failures:
        sys.exit(failures)
