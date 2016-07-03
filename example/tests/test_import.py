# -*- coding: utf-8 -*-
# pylint: disable=wildcard-import,no-member

"""
This module tests import of django-split-setting.
"""

import unittest
import types


class TestModuleImport(unittest.TestCase):
    """ Tests different cases of import. """

    def _assert_types(self, _version, _include, _optional):
        """ This helper function tests all parameters.
        :param _version: version string.
        :param _include: include function.
        :param _optional: optional class.
        """
        self.assertEqual(type(_version), str)
        self.assertEqual(type(_include), types.FunctionType)
        self.assertEqual(type(_optional), types.FunctionType)

    def test_module_import(self):
        """ Import base functionality. """
        try:
            from split_settings import __version__
            from split_settings.tools import include
            from split_settings.tools import optional

            self._assert_types(__version__, include, optional)

        except ImportError as import_error:
            self.fail(msg=import_error)

    def test_wildcard_import(self):
        """ Imports all from all modules """
        try:
            from split_settings.tools import __all__
            self.assertIn('optional', __all__)
            self.assertIn('include', __all__)

        except ImportError as import_error:
            self.fail(msg=import_error)

    def test_class_import(self):
        """ This test case covers #7 issue. """

        from example.settings.components import testing as _testing
        from example import settings as merged

        self.assertEqual(merged.STATIC_ROOT,
                         _testing.TestingConfiguration('').get_path())
