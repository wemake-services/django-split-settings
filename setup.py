# -*- coding: utf-8 -*-

"""
Visit https://pypi.python.org/pypi/django-split-settings
for more information.
"""

from setuptools import setup
from split_settings import __version__

INSTALL_REQUIRES = ['Django>=1.5.1', ]

TEST_REQUIRE = [
    'nose>=1.3.6',
    'pep8>=1.6.2',
    'pylint>=1.4.3'
]

SETUP_REQUIRES = ['setuptools-git>=0.4.2', ]


setup(
    name='django-split-settings',
    version=__version__,
    description=(
        'Organize Django settings into multiple files and directories. '
        'Easily override and modify settings. Use wildcards and optional '
        'settings files.'
    ),
    author='Visa Kopu, Antti Kaihola (2General Ltd.)',
    author_email='visa@2general.com',
    url='http://github.com/sobolevn/django-split-settings',
    packages=['split_settings'],    # find_packages(exclude=['example']),
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    setup_requires=SETUP_REQUIRES,
    tests_require=TEST_REQUIRE,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Environment :: Web Environment'
    ]
)
