from split_settings.tools import include, optional

include(
    # Components:
    'components/base.py',
    'components/locale.py',
    'components/apps_middleware.py',
    'components/static.py',
    'components/templates.py',
    'components/database.pyc',
    'components/logging.py',

    # Override settings for testing:
    optional('components/testing.py'),

    # Missing file:
    optional('components/missing_file.py'),

    # Scope:
    scope=globals(),  # noqa: WPS421
)
