# -*- coding: utf-8 -*-
# pylint: disable=invalid-name,no-member

"""
This file contains tests with base functionality.
"""

import unittest
from django.conf import settings as result
from example import settings as merged


class TestSplitSettings(unittest.TestCase):
    """ Test basic functionality.
    This test case needs to be wider.
    """

    def test_merge(self):   # TODO: dynamic module loading
        """ Test that all values from settings are present. """

        self.assertIn('SECRET_KEY', merged.__dict__.keys())
        self.assertIn('STATIC_ROOT', merged.__dict__.keys())

    def test_override(self):
        """ This setting must be overridden in the testing.py """

        self.assertEqual(merged.STATIC_ROOT, result.STATIC_ROOT)


if __name__ == '__main__':
    unittest.main()
