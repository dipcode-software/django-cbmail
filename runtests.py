import django
import sys

from django.test.runner import DiscoverRunner
from django.conf import settings

settings.configure(
    INSTALLED_APPS=(
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
        'APP_DIRS': True,
    }]
)


if __name__ == "__main__":
    django.setup()
    runner = DiscoverRunner()
    failures = runner.run_tests(['mailings'])
    if failures:
        sys.exit(failures)
