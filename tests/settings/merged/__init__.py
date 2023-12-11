from split_settings.tools import include, optional

include(
    # Components:
    'components/base.py',
    'components/locale.py',
    'components/apps_middleware.py',
    'components/static.py',
    'components/templates.py',
    'components/database.py',
    'components/logging.py',

    # Override settings for testing:
    optional('components/testing.py'),

    # Missing file:
    optional('components/missing_file.py'),

    # Conditional inclusion:
    optional('components/conditional.py' if False else None),  # noqa: WPS314

    # Scope:
    scope=globals(),  # noqa: WPS421
)
