from django.test import SimpleTestCase

from djangomailings.mailings import BaseMailing

from .utils import create_attachment


class TestBaseObject(BaseMailing):
    template_name = 'djangomailings/base.html'
    mail_to = [('dev', 'dev@unit.com')]
    mail_cc = ['dev@unit.com']
    mail_bcc = ['dev@unit.com']
    mail_reply_to = ['dev@unit.com']
    mail_from = 'dev@unit.com'
    subject = 'Unit test'

    def get_attachments(self):
        return create_attachment()


class TestBaseNoInfoObject(BaseMailing):
    template_name = 'djangomailings/base.html'
    mail_to = [('dev', 'dev@unit.com')]
    mail_cc = ['dev@unit.com']
    mail_bcc = ['dev@unit.com']


class MailingsSimpleTest(SimpleTestCase):

    def setUp(self):
        self.object = TestBaseObject(context={})
        self.no_info_object = TestBaseNoInfoObject()

    def test_get_attachments(self):
        result = self.object.get_attachments()
        expected = [('test.txt', 'unit test', 'text/plain')]
        self.assertEqual(result, expected)

    def test_get_context_data(self):
        result = self.object.get_context_data()
        self.assertEqual(result, {})

    def test_get_mail_to(self):
        result = self.object.get_mail_to()
        self.assertEqual(result, [('dev', 'dev@unit.com')])

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
        self.assertEqual(result, ['default@unit.com'])

    def test_get_mail_from(self):
        result = self.object.get_mail_from()
        self.assertEqual(result, 'dev@unit.com')

    def test_get_mail_no_info_from(self):
        result = self.no_info_object.get_mail_from()
        self.assertEqual(result, 'default@unit.com')

    def test_get_subject(self):
        result = self.object.get_subject()
        self.assertEqual(result, 'Unit test')

    def test_get_no_info_subject(self):
        result = self.no_info_object.get_subject()
        self.assertEqual(result, 'Unit test default')

    def test_get_template_name(self):
        result = self.object.get_template_name()
        self.assertEqual(result, 'djangomailings/base.html')
