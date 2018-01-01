from setuptools import setup
setup(
  name = 'iota_auth',
  packages = ['iota_auth'], # this must be the same as the name above
  version = '0.1',
  description = 'A custom authentication backend for Django Users to connect to the IOTA Tangle.',
  author = 'David Guinane',
  author_email = 'david.j.guinane@gmail.com',
  url = 'https://github.com/davidjguinane', # use the URL to the github repo
  download_url = 'https://github.com/davidjguinane/django-iota-auth/archive/0.1.tar.gz', # I'll explain this in a second
  keywords = ['iota', 'django', 'authentication'], # arbitrary keywords
  classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Framework :: Django :: 2.0',
    'Natural Language :: English',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)', # example license
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.6',
  ],
  install_requires=[
  'django-encrypted-cookie-session >= 3.2.0',
  'pyota',
  'six >=1.11.8',
  'filters >= 1.3.2',
  'request >= 2.18.4',
  'pysha3 >= 1.0.2',
  ]
)