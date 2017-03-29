from __future__ import unicode_literals

from django.conf import settings
from django.template import loader
from django.core.mail.message import EmailMultiAlternatives
from django.core.mail import get_connection
from django.utils.html import strip_tags


class BaseMailing(object):
    """ TODO: add prefix support to subject """

    template_name = None
    mail_cc = []
    mail_bcc = []
    mail_reply_to = []
    mail_from = None
    subject = None

    def get_attachments(self):
        return []

    def get_context_data(self):
        return {}

    def get_mail_to(self, object_or_list):
        if isinstance(object_or_list, list):
            return object_or_list
        elif isinstance(object_or_list, object) and\
                hasattr(object_or_list, 'get_mailing_list'):
            return object_or_list.get_mailing_list()
        raise ValueError('object_or_list must be object with get_mailing_list'
                         'method defined or list instance.')

    def get_mail_cc(self):
        return self.mail_cc

    def get_mail_bcc(self):
        return self.mail_bcc

    def get_mail_reply_to(self):
        if self.mail_reply_to:
            return self.mail_reply_to
        return settings.MAILINGS.get('DEFAULT_REPLY_TO', None)

    def get_mail_from(self):
        if self.mail_from:
            return self.mail_from
        return settings.get('DEFAULT_FROM_EMAIL')

    def get_subject(self):
        if self.subject:
            return self.subject
        return settings.MAILINGS.get('DEFAULT_SUJECT')

    def get_template_name(self):
        return self.template_name

    def get_base_url(self):
        return settings.MAILINGS.get('BASE_URL')

    def send(self, object_or_list):
        messages = list()
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
            msg.attach(
                attachment.get_filename(),
                attachment.get_contents(),
                attachment.get_mimetype()
            )

        messages.append(msg)

        return get_connection().send_messages(messages)


class Attachment(object):
    filename = None
    contents = None
    mimetype = None

    def get_filename(self):
        return self.filename

    def get_contents(self):
        return self.contents

    def get_mimetype(self):
        return self.mimetype
