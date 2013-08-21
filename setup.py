# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from split_settings import __version__

setup(name='django-split-settings',
    version=__version__,
    description=(
        'Organize Django settings into multiple files and directories. '
        'Easily override and modify settings. Use wildcards and optional '
        'settings files.'),
    author='Visa Kopu, Antti Kaihola (2General Ltd.)',
    author_email='visa@2general.com',
    url='http://github.com/2general/django-split-settings',
    packages=find_packages(exclude=['example']),
    include_package_data=True,
    setup_requires=['setuptools-git>=0.4.2'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: BSD License',
    ]
)
