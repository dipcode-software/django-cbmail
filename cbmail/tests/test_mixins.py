from django.test import SimpleTestCase

from cbmail.mixins import MailingListMixin


class MixinsTest(SimpleTestCase):

    class NokObject(MailingListMixin):
        """ """

    def test_mixin_nok(self):
        result = self.NokObject()
        self.assertRaises(NotImplementedError, result.get_mailing_list)
