import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-iota-auth',
    version='0.1a',
    packages=find_packages(),
    include_package_data=True,
    license='GNU GPL3 License',  # example license
    description='A Django app to authenticate a User and connect them to the tangle.',
    long_description=README,
    url='https://github.com/davidjguinane/django-iota-auth',
    author='David Guinane',
    author_email='david.j.guinane@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: X.Y',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU GPL3 License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    python_requires='>=3',
    keywords='iota django authentication',
    install_requires=['pyota', 'pillow', 'django']
)

