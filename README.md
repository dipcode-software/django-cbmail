# Django maillings
Django module to easily send templated emails

## Settings
To give support to this app we need to declare de following django settings:

    DEFAULT_FROM_EMAIL="example@example.com",
	MAILINGS={
        'DEFAULT_REPLY_TO': "examplereplyto@example.com",
        'DEFAULT_SUJECT': "Example subject",
        'BASE_URL': "https://domain.com",
        'EXTRA_DATA': {}
    },

- **DEFAULT_FROM_EMAIL**: Default setting of Django that defines the from email
- **DEFAULT_REPLY_TO**: Default reply to be used on emails
- **DEFAULT_SUJECT**: Default subject to be used on emails
- **BASE_URL**: The base url of your website
- **EXTRA_DATA**: Any extra data intended to be used on all emails (This is injected on context of template)
