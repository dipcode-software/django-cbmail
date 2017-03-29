class MailingListMixin(object):

    def get_mailing_list(self):
        """
        This method should return a list of emails
        to be user in to field of the message
        """
        raise NotImplementedError
