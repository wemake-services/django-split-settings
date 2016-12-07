# -*- coding: utf-8 -*-

import os

import django

from split_settings.tools import optional, include

# Must bypass this block if another settings module was specified.
if os.environ['DJANGO_SETTINGS_MODULE'] == 'tests.settings':

    include(
        '*.py'
    )
