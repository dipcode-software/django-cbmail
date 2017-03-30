from __future__ import unicode_literals

from django.conf import settings
from django.template import loader
from django.core.mail.message import EmailMultiAlternatives
from django.core.mail import get_connection
from django.utils.html import strip_tags


class BaseMailing(object):
    """
    This class represents the base of a templated email
    TODO: add prefix support to subject
    """
    template_name = None
    mail_cc = []
    mail_bcc = []
    mail_reply_to = []
    mail_from = None
    subject = None

    def get_attachments(self):
        """ Return a list of Attachment instances """
        return []

    def get_context_data(self):
        """ Return a dictionary with context to be used on template """
        return {}

    def get_mail_to(self, object_or_list):
        """
        Returns the list of emails to be used on to email field

        objects_or_list can be a list of emails or a object instance
        with the get_mailing_list method defined
        """
        if isinstance(object_or_list, list):
            return object_or_list
        elif isinstance(object_or_list, object) and\
                hasattr(object_or_list, 'get_mailing_list'):
            return object_or_list.get_mailing_list()
        raise ValueError('object_or_list must be object with get_mailing_list'
                         ' method defined or list instance.')

    def get_mail_cc(self):
        """ Returns the list of emails to be used on cc email field """
        return self.mail_cc

    def get_mail_bcc(self):
        """ Returns the list of emails to be used on bcc email field """
        return self.mail_bcc

    def get_mail_reply_to(self):
        """
        Returns the email to be used on the reply to email field
        If one is not provided it will get the DEFAULT_REPLY_TO setting
        """
        if self.mail_reply_to:
            return self.mail_reply_to
        return settings.MAILINGS.get('DEFAULT_REPLY_TO', None)

    def get_mail_from(self):
        """
        Returns the email to be used on the from email field
        If one is not provided it will get the Django default email setting
        """
        if self.mail_from:
            return self.mail_from
        return settings.DEFAULT_FROM_EMAIL

    def get_subject(self):
        """
        Returns the subject to be used on the subject email field
        If one is not provided it will get the DEFAULT_SUJECT setting
        """
        if self.subject:
            return self.subject
        return settings.MAILINGS.get('DEFAULT_SUJECT')

    def get_template_name(self):
        """ Returns the template name to be used to render the email """
        return self.template_name

    def get_base_url(self):
        """ Returns the base url to be used on the email """
        return settings.MAILINGS.get('BASE_URL')

    def send(self, object_or_list):
        """
        Given an object_or_list creates a EmailMultiAlternatives and
        send it to the respective destination.
        If Attachments exist, also adds them to the messsage.
        """
        context = self.get_context_data()

        context.update(settings.MAILINGS.get('EXTRA_DATA', {}))
        context.update({
            'base_url': self.get_base_url(),
            'subject': self.get_subject()
        })

        # Contacts is a list of emails for now
        html_as_string = loader.render_to_string(
            self.get_template_name(), context)
        text_part = strip_tags(html_as_string)

        msg = EmailMultiAlternatives(
            self.get_subject(),
            text_part,
            self.get_mail_from(),
            to=self.get_mail_to(object_or_list),
            cc=self.get_mail_cc(),
            bcc=self.get_mail_bcc(),
            reply_to=self.get_mail_reply_to())

        # Attach the html version of email
        msg.attach_alternative(html_as_string, "text/html")

        # If there is attachments attach them to the email
        for attachment in self.get_attachments():
            msg.attach(*attachment.get_triple())

        return get_connection().send_messages([msg])


class Attachment(object):
    """ This class represents one email attachment """
    filename = None
    contents = None
    mimetype = None

    def __init__(self, filename, contents, mimetype, *args, **kwargs):
        self.filename = filename
        self.contents = contents
        self.mimetype = mimetype
        super(Attachment, self).__init__(*args, **kwargs)

    def get_triple(self):
        """ Returns the triple to be user when attached to message """
        return self.filename, self.contents, self.mimetype
