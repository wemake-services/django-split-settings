# -*- coding: utf-8 -*-

from split_settings.tools import include, optional
from tests.settings import resource

include(
    # Components:
    ('tests.settings.alt_ext', 'base.conf'),
    ('tests.settings.alt_ext', 'locale.conf'),
    ('tests.settings.alt_ext', 'apps_middleware'),
    (resource, 'static.settings'),
    (resource, 'templates.py'),
    optional((resource, 'database.conf')),
    'logging.py',

    # Missing file:
    optional((resource, 'missing_file.py')),
    optional(('tests.settings.alt_ext', 'missing_file.py')),

    # Scope:
    scope=globals(),  # noqa: WPS421
)
