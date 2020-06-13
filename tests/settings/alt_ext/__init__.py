# -*- coding: utf-8 -*-

from split_settings.tools import include, optional

# Includes files with non-standard extensions:
include(
    'include',
    '*.conf',
    optional('optional.ext'),
)
