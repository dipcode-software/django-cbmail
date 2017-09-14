Django CBMail
================

|Build Status| |Codacy Badge| |Coverage Status| |BCH compliance|

Django module to easily send templated emails in a DRY way using
classes, just like Class Based Views.

Table of contents:
 * `How to install`_;
 * `Example usage`_;
 * `Settings reference`_;
 * `License`_.

How to install
--------------

To install the app run :

.. code:: shell

    pip install django-cbmail

or add it to the list of requirements of your project.

Example usage
-------------

Create a mails.py and use the BaseMail class to define your email like:

.. code:: python

    from cbmail.base import BaseMail

    class ExampleEmail(BaseMail):
        """ """
        template_name = "myapp/mails/myemail.html"
        subject = "Example subject of email"

And send it using:

.. code:: python

    ExampleEmail().send(['example@example.com'])

Where ``['example@example.com']`` is a list of emails of destination or
a object with ``get_mailing_list`` method defined

Settings reference
------------------

To give support to this app we need to declare de following django
settings:

.. code:: python

    DEFAULT_FROM_EMAIL = "example@example.com"

    CBMAIL = {
        'DEFAULT_REPLY_TO': "examplereplyto@example.com",
        'DEFAULT_SUJECT': "Example subject",
        'BASE_URL': "https://domain.com",
        'EXTRA_DATA': {},
        'WHITELIST': []
    }

-  **DEFAULT\_FROM\_EMAIL**: Default setting of Django that defines the
   from email
-  **DEFAULT\_REPLY\_TO**: Default reply to be used on emails
-  **DEFAULT\_SUJECT**: Default subject to be used on emails
-  **WHITELIST**: List of valid emails to send to
-  **BASE\_URL**: The base url of your website
-  **EXTRA\_DATA**: Any extra data intended to be used on all emails
   (This is injected on context of template)

License
-------

MIT license, see the LICENSE file. You can use obfuscator in open source
projects and commercial products.

.. _How to install: #how-to-install
.. _Example usage: #example-usage
.. _Settings reference: #settings-reference
.. _License: #license

.. |Build Status| image:: https://travis-ci.org/dipcode-software/django-cbmail.svg?branch=master
   :target: https://travis-ci.org/dipcode-software/django-cbmail
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/d01ebbe43c684d478cacc530e44633ad
   :target: https://www.codacy.com/app/srtabs/django-cbmail?utm_source=github.com&utm_medium=referral&utm_content=dipcode-software/django-cbmail&utm_campaign=Badge_Grade
.. |Coverage Status| image:: https://coveralls.io/repos/github/dipcode-software/django-cbmail/badge.svg?branch=master
   :target: https://coveralls.io/github/dipcode-software/django-cbmail?branch=master
.. |BCH compliance| image:: https://bettercodehub.com/edge/badge/dipcode-software/django-cbmail?branch=master
   :target: https://bettercodehub.com/
