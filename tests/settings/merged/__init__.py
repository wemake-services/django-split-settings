from split_settings.tools import compiled, include, optional

include(
    # Components:
    'components/base.py',
    'components/locale.py',
    'components/apps_middleware.py',
    'components/static.py',
    'components/templates.py',
    compiled('components/database.pyc'),
    'components/logging.py',

    # Override settings for testing:
    optional('components/testing.py'),

    # Missing file:
    optional('components/missing_file.py'),

    # Missing compiled file
    optional(compiled('components/missing_file.pyc')),

    # Scope:
    scope=globals(),  # noqa: WPS421
)
