# -*- coding: utf-8 -*-

"""
To run these test
"""

import unittest
import pep8
from os.path import join, dirname


class TestCodeFormat(unittest.TestCase):
    """ Test
     This project uses pep8 and pylint.
    """

    def test_pep8_conformance(self):
        """Test that code conforms to PEP8."""

        parent = dirname(dirname(dirname(__file__)))
        pep8_style = pep8.StyleGuide()
        pep8_style = pep8_style.check_files([
            join(parent, 'split_settings'),
            join(parent, 'example', 'tests'),
            join(parent, 'setup.py')
        ])

        # Using a strict policy:
        self.assertEqual(pep8_style.total_errors, 0,
                         'Found code style errors, fix it.')


if __name__ == '__main__':
    unittest.main()
