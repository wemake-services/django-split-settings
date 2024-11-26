from split_settings.tools import compiled, include, one_of, optional

include(
    # Components:
    'components/base.py',
    'components/locale.py',
    'components/apps_middleware.py',
    'components/static.py',
    'components/templates.py',
    'components/logging.py',

    # Compiled file
    compiled('components/database.pyc'),

    # Override settings for testing:
    optional('components/testing.py'),

    # Missing file:
    optional('components/missing_file.py'),

    # Missing compiled file
    optional(compiled('components/missing_file.pyc')),

    # One of the given files
    one_of('components/choice_left.py', 'components/choice_right.py'),

    # Scope:
    scope=globals(),  # noqa: WPS421
)
