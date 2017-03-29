from django.test import SimpleTestCase

from mailings.mailings import BaseMailing, Attachment
from mailings.mixins import MailingListMixin

from tempfile import NamedTemporaryFile


class TestBaseObject(BaseMailing):
    template_name = 'mailings/base.html'
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


class TestBaseNoInfoObject(BaseMailing):
    template_name = 'mailings/base.html'
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
        self.assertEqual(result, 'mailings/base.html')

    def test_get_base_url(self):
        result = self.object.get_base_url()
        self.assertEqual(result, 'https://domain.com')


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
