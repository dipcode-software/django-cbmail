from setuptools import find_packages, setup


setup(
    name='django-mailings',
    version=__import__("mailings").__version__,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Django module to easily send templated emails.',
    url='https://github.com/dipcode-software/django-mailings/',
    author='Dipcode',
    author_email='info@dipcode.com',
    keywords=['django', 'mailing', 'templating'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)
