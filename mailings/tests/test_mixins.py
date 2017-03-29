from django.test import SimpleTestCase

from evotemailings.mixins import MailingListMixin


class MixinsTest(SimpleTestCase):

    class NokObject(MailingListMixin):
        """ """

    def test_mixin_nok(self):
        object = self.NokObject()
        self.assertRaises(NotImplementedError, object.get_mailing_list)
