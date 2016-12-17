# -*- coding: utf-8 -*-

"""
Visit https://pypi.python.org/pypi/django-split-settings
for more information.
"""

from setuptools import setup
from split_settings import __version__

INSTALL_REQUIRES = ['Django>=1.5', ]
# pylint is not happy without this line:
TESTS_REQUIRE = ['pytest', 'six', 'pytest-env', ]
SETUP_REQUIRES = ['pytest-runner', ]

setup(
    name='django-split-settings',
    version=__version__,
    description=(
        'Organize Django settings into multiple files and directories. '
        'Easily override and modify settings. Use wildcards and optional '
        'settings files.'
    ),
    author='Nikita Sobolev, Visa Kopu, Antti Kaihola',
    author_email='mail@sobolevn.me',
    url='http://github.com/sobolevn/django-split-settings',
    packages=[
        'split_settings',
    ],
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    setup_requires=SETUP_REQUIRES,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.5',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
