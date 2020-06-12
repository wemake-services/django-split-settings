# -*- coding: utf-8 -*-

from split_settings.tools import include, optional, resource
from tests.settings import resources

include(
    # Components:
    resource('tests.settings.resources', 'base.conf'),
    resource('tests.settings.resources', 'locale.conf'),
    resource('tests.settings.resources', 'apps_middleware'),
    resource(resources, 'static.settings'),
    resource(resources, 'templates.py'),
    resource(resources, 'multiple/subdirs/file.conf'),
    optional(resource(resources, 'database.conf')),
    'logging.py',

    # Missing file:
    optional(resource(resources, 'missing_file.py')),
    optional(resource('tests.settings.resources', 'missing_file.conf')),
    resource('tests.settings.resources', 'error.conf'),

    # Missing module
    optional(resource('module.does.not.exist', 'settings.conf')),

    # Scope:
    scope=globals(),  # noqa: WPS421
)
