# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings as dj_settings
from django.core.exceptions import ImproperlyConfigured


APP_NAME = 'CBMAIL'

DEFAULTS = {
    'DEFAULT_REPLY_TO': 'examplereplyto@example.com',
    'DEFAULT_SUJECT': 'Example subject',
    'BASE_URL': None,
    'EXTRA_DATA': {},
    'WHITELIST': []
}


class MailingsSettings(object):
    """
    A settings object, that allows settings to be accessed as properties.
    """
    def __init__(self, defaults=None):
        self.defaults = defaults or DEFAULTS
        self.check_settings()

    def check_settings(self):
        if 'BASE_URL' not in self.user_settings:
            raise ImproperlyConfigured(
                'Settings not configured correctly. '
                'You have to configure a BASE_URL')

    @property
    def user_settings(self):
        return getattr(dj_settings, APP_NAME, {})

    def __getattr__(self, attr):
        """ """
        if attr not in self.defaults:
            raise AttributeError("Invalid setting: '%s'" % attr)
        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]
        return val


settings = MailingsSettings(DEFAULTS)
