# -*- coding: utf-8 -*-

"""
This module is created to test the `python2`'s `unicode_literals`.
See https://github.com/sobolevn/django-split-settings/issues/9
"""

from __future__ import unicode_literals

from split_settings.tools import include

__author__ = 'sobolevn'


def test_unicode_filename():
    """ This represents the `hidden-unicode` situation. """

    include(
        'fixture_to_include.py',
        scope=globals(),
    )

    assert 'FIXTURE_VALUE' in globals()
