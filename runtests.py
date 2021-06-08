import sys

import django

from django.conf import settings
from django.test.runner import DiscoverRunner


settings.configure(
    INSTALLED_APPS=(
        'cbmail',
    ),
    CBMAIL={
        'DEFAULT_REPLY_TO': "replyto@unittest.com",
        'DEFAULT_SUBJECT': "Unit test default",
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
    failures = runner.run_tests(['cbmail'])
    if failures:
        sys.exit(failures)
