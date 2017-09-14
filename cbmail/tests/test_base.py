from tempfile import NamedTemporaryFile

from cbmail.base import Attachment, BaseMail
from cbmail.mixins import MailingListMixin
from django.test import SimpleTestCase
from mock import patch


class TestBaseObject(BaseMail):
    template_name = 'cbmail/base.html'
    mail_to = [('dev', 'dev@unit.com')]
    mail_cc = ['dev@unit.com']
    mail_bcc = ['dev@unit.com']
    mail_reply_to = ['dev@unit.com']
    mail_from = 'dev@unit.com'
    subject = 'Unit test'

    def get_attachments(self):
        f = NamedTemporaryFile()
        f.write('unit test')
        f.seek(0)
        attachment = open(f.name, 'rb')
        att = Attachment(
            filename="test.txt",
            contents=attachment.read(),
            mimetype="text/plain")
        return [att]


class TestBaseNoInfoObject(BaseMail):
    template_name = 'cbmail/base.html'
    mail_to = [('dev', 'dev@unit.com')]
    mail_cc = ['dev@unit.com']
    mail_bcc = ['dev@unit.com']


class MailInstance(MailingListMixin):

    def get_mailing_list(self):
        return ['dev@unit.com']


class MailingsSimpleTest(SimpleTestCase):

    def setUp(self):
        self.object = TestBaseObject()
        self.no_info_object = TestBaseNoInfoObject()
        self.mailinstance = MailInstance()

    def test_get_attachments(self):
        result = self.object.get_attachments()
        self.assertEqual(len(result), 1)

    def test_get_attachments_empty(self):
        result = self.no_info_object.get_attachments()
        self.assertEqual(result, [])

    def test_get_context_data(self):
        result = self.object.get_context_data()
        self.assertEqual(result, {})

    def test_get_mail_to_list(self):
        result = self.object.get_mail_to(['dev@unit.com'])
        self.assertEqual(result, ['dev@unit.com'])

    def test_get_mail_to_object(self):
        result = self.object.get_mail_to(self.mailinstance)
        self.assertEqual(result, ['dev@unit.com'])

    def test_get_mail_to_error(self):
        self.assertRaises(
            ValueError, self.object.get_mail_to, '"invalid type"')

    def test_filter_whitelist(self):
        with self.settings(CBMAIL={'WHITELIST': ['a@unit.c', 'b@unit.c']}):
            result = BaseMail._filter_whitelist(['a@unit.c', 'c@unit.c'])
        self.assertEqual(result, ['a@unit.c'])

    def test_filter_whitelist_not_defined(self):
        with self.settings(CBMAIL={}):
            result = BaseMail._filter_whitelist(['a@unit.c', 'c@unit.c'])
        self.assertEqual(result, ['a@unit.c', 'c@unit.c'])

    def test_filter_whitelist_empty(self):
        with self.settings(CBMAIL={'WHITELIST': ['a@unit.c', 'b@unit.c']}):
            result = BaseMail._filter_whitelist(['c@unit.c', 'd@unit.c'])
        self.assertEqual(result, [])

    def test_get_mail_cc(self):
        result = self.object.get_mail_cc()
        self.assertEqual(result, ['dev@unit.com'])

    def test_get_mail_bcc(self):
        result = self.object.get_mail_bcc()
        self.assertEqual(result, ['dev@unit.com'])

    def test_get_mail_reply_to(self):
        result = self.object.get_mail_reply_to()
        self.assertEqual(result, ['dev@unit.com'])

    def test_get_mail_no_info_reply_to(self):
        result = self.no_info_object.get_mail_reply_to()
        self.assertEqual(result, 'replyto@unittest.com')

    def test_get_mail_from(self):
        result = self.object.get_mail_from()
        self.assertEqual(result, 'dev@unit.com')

    def test_get_mail_no_info_from(self):
        result = self.no_info_object.get_mail_from()
        self.assertEqual(result, 'unit@unit.com')

    def test_get_subject(self):
        result = self.object.get_subject()
        self.assertEqual(result, 'Unit test')

    def test_get_no_info_subject(self):
        result = self.no_info_object.get_subject()
        self.assertEqual(result, 'Unit test default')

    def test_get_template_name(self):
        result = self.object.get_template_name()
        self.assertEqual(result, 'cbmail/base.html')

    def test_get_base_url(self):
        result = self.object.get_base_url()
        self.assertEqual(result, 'https://domain.com')

    @patch('cbmail.base.loader.render_to_string')
    def test_render(self, render_to_string):
        render_to_string.return_value = "dummy"
        result = self.object.render()
        self.assertEqual(result, "dummy")
        render_to_string.assert_called_with(
            self.object.get_template_name(),
            {
                'base_url': self.object.get_base_url(),
                'subject': self.object.get_subject()
            })

    @patch('cbmail.base.loader.render_to_string')
    def test_render_extra_data(self, render_to_string):
        with self.settings(CBMAIL={
                'EXTRA_DATA': {'dummy_key': 'dummy_value'}}):
            render_to_string.return_value = "dummy"
            result = self.object.render()
            self.assertEqual(result, "dummy")
            render_to_string.assert_called_with(
                self.object.get_template_name(),
                {
                    'base_url': self.object.get_base_url(),
                    'subject': self.object.get_subject(),
                    'dummy_key': 'dummy_value'
                })

    @patch('cbmail.base.get_connection')
    def test_get_send_empty(self, get_connection):
        self.assertEqual(self.object.send([]), 0)

    @patch('cbmail.base.get_connection')
    def test_get_send(self, get_connection):
        self.object.send(['dev@unit.com'])
        get_connection().send_messages.assert_called_once()


class AttachmentsSimpleTest(SimpleTestCase):

    def setUp(self):
        self.object = Attachment(
            filename="test.txt",
            contents="This is the content of the file",
            mimetype="text/plain")

    def test_get_triple(self):
        result = self.object.get_triple()
        self.assertEqual(
            result,
            ('test.txt', 'This is the content of the file', 'text/plain')
        )
