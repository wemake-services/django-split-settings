# -*- coding: utf-8 -*-

"""
This module is created to test the `python2`'s `unicode_literals`.
See https://github.com/sobolevn/django-split-settings/issues/9
"""

from __future__ import unicode_literals

import os

from split_settings.tools import include

__author__ = 'sobolevn'


def test_unicode_filename(scope):
    """
    This represents the `hidden-unicode` situation.
    """

    file_path = os.path.join(
        'settings',  # this should be written as string
        'fixture_to_include.py'
    )

    include(
        file_path,
        scope=scope,
    )

    assert 'FIXTURE_VALUE' in scope
