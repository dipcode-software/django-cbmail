# Django maillings

[![Build Status](https://travis-ci.org/dipcode-software/django-mailings.svg?branch=master)](https://travis-ci.org/dipcode-software/django-mailings)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d01ebbe43c684d478cacc530e44633ad)](https://www.codacy.com/app/srtabs/django-mailings?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=dipcode-software/django-mailings&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/dipcode-software/django-mailings/badge.svg?branch=master)](https://coveralls.io/github/dipcode-software/django-mailings?branch=master)
[![BCH compliance](https://bettercodehub.com/edge/badge/dipcode-software/django-mailings?branch=master)](https://bettercodehub.com/)

Django module to easily send templated emails in a DRY way using classes, just like Class Based Views.

Table of contents:
 * [How to install](#how-to-install);
 * [Example usage](#example-usage);
 * [Settings reference](#settings-reference);
 * [License](#license).

## How to install
To install the app run :
```shell
pip install django-mailings
```
or add it to the list of requirements of your project.

## Example usage
Use the BaseMailing class to define your email like:
```python
from mailings.mailings import BaseMailing

class ExampleEmail(BaseMailing):
	""" """
	template_name = "myapp/mails/myemail.html"
	subject = "Example subject of email"
```

And send it using:
```python
ExampleEmail().send(['example@example.com'])
```
Where `['example@example.com']` is a list of emails of destination or a object with `get_mailing_list` method defined

## Settings reference
To give support to this app we need to declare de following django settings:
```python
DEFAULT_FROM_EMAIL = "example@example.com"

MAILINGS = {
    'DEFAULT_REPLY_TO': "examplereplyto@example.com",
    'DEFAULT_SUJECT': "Example subject",
    'BASE_URL': "https://domain.com",
    'EXTRA_DATA': {},
    'WHITELIST': []
}
```

- **DEFAULT_FROM_EMAIL**: Default setting of Django that defines the from email
- **DEFAULT_REPLY_TO**: Default reply to be used on emails
- **DEFAULT_SUJECT**: Default subject to be used on emails
- **WHITELIST**: List of valid emails to send to
- **BASE_URL**: The base url of your website
- **EXTRA_DATA**: Any extra data intended to be used on all emails (This is injected on context of template)


## License

MIT license, see the LICENSE file. You can use obfuscator in open source projects and commercial products.
