from split_settings.tools import optional, include
import os

# Must bypass this block if another settings module was specified.
if os.environ['DJANGO_SETTINGS_MODULE'] == 'example.settings':

    include(
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

        # hostname-based override, in settings/env/ directory
        # optional('env/%s.py' % socket.gethostname().split('.', 1)[0]),

        # local settings (do not commit to version control)
        # optional(os.path.join(os.getcwd(), 'local_settings.py')),

        scope=globals()
    )
