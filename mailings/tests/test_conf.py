# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase
from mailings.conf import settings


class MailingsSettingsTest(SimpleTestCase):

    def test_getattr_not_defined(self):
        with self.assertRaises(AttributeError):
            settings.__getattr__('DUMMY')

    def test_getattr_default(self):
        self.assertEqual(settings.WHITELIST, [])

    def test_getattr_user(self):
        with self.settings(MAILINGS={'BASE_URL': 'https://domain.com'}):
            self.assertEqual(settings.BASE_URL, 'https://domain.com')

    def test_check_settings(self):
        with self.settings(MAILINGS={}):
            with self.assertRaises(ImproperlyConfigured):
                settings.check_settings()
