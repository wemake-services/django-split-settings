# -*- coding: utf-8 -*-

"""
This file contains different utils.
"""

__author__ = 'sobolevn'


class Scope(dict):
    """
    This class emulates `globals()`,
    but does not share state across all tests.
    """
    def __init__(self, *args, **kwargs):
        """
        Adding `__file__` to make things work in `tools.py`.
        """
        super(Scope, self).__init__(*args, **kwargs)
        self['__file__'] = __file__
