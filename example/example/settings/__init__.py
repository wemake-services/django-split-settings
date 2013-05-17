from split_settings.tools import optional, include
import os
import socket

if os.environ['DJANGO_SETTINGS_MODULE'] == 'example.settings':
    # must bypass this block if another settings module was specified
    include(
        "components/base.py",
        "components/locale.py",
        "components/apps_middleware.py",
        "components/static.py",
        "components/templates.py",
        "components/database.py",
        "components/logging.py",

        # OVERRIDE SETTINGS

        # hostname-based override, in settings/env/ directory
        optional("env/%s.py" % socket.gethostname().split(".", 1)[0]),

        # local settings (do not commit to version control)
        optional(os.path.join(os.getcwd(), "local_settings.py")),

        scope=locals()
    )
