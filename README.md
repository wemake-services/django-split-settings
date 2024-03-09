<p align="center">
  <img src="https://raw.githubusercontent.com/sobolevn/django-split-settings/master/docs/_static/logo-black.png"
       alt="django-split-settings logo">
</p>

---

[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services)
[![test](https://github.com/wemake-services/django-split-settings/actions/workflows/test.yml/badge.svg?branch=master&event=push)](https://github.com/wemake-services/django-split-settings/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/sobolevn/django-split-settings/branch/master/graph/badge.svg)](https://codecov.io/gh/sobolevn/django-split-settings)
[![Docs](https://readthedocs.org/projects/django-split-settings/badge/?version=latest)](http://django-split-settings.readthedocs.io/en/latest/?badge=latest)
[![Python Version](https://img.shields.io/pypi/pyversions/django-split-settings.svg)](https://pypi.org/project/django-split-settings/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)



Organize Django settings into multiple files and directories. Easily
override and modify settings. Use wildcards in settings file paths
and mark settings files as optional.

Read [this blog post](https://sobolevn.me/2017/04/managing-djangos-settings)
for more information.
Also, check this [example project](https://github.com/wemake-services/wemake-django-template).


## Requirements

While this package will most likely work with the most versions of `django`, we [officially support](https://github.com/sobolevn/django-split-settings/blob/master/.github/workflows/test.yml):

- 4.2
- 5.0
- 5.1

This package has no dependencies itself.

In case you need older `python` / `django` versions support,
then consider using older versions of `django-split-settings`.


## Installation

```bash
pip install django-split-settings
```


## Usage

Replace your existing `settings.py` with a list of components that
make up your Django settings. Preferably create a settings package
that contains all the files.

Here's a minimal example:

```python
from split_settings.tools import optional, include

include(
    'components/base.py',
    'components/database.py',
    optional('local_settings.py')
)
```

In the example, the files `base.py` and `database.py` are included
in that order from the subdirectory called `components/`.
`local_settings.py` in the same directory is included if it exists.

**Note:** The local context is passed on to each file, so each
following file can access and modify the settings declared in the
previous files.

We also made an in-depth [tutorial](https://sobolevn.me/2017/04/managing-djangos-settings).


## Tips and tricks

You can use wildcards in file paths:

```python
include('components/my_app/*.py')
```

Note that files are included in the order that `glob` returns them,
probably in the same order as what `ls -U` would list them. The
files are NOT in alphabetical order.

You can modify common settings in environment settings simply importing them

```python
# local_settings.py
from components.base import INSTALLED_APPS

INSTALLED_APPS += (
  'raven.contrib.django.raven_compat',
)
```


## Updating `BASE_DIR`

The `django create-project` command will create a variable in your `settings.py` called `BASE_DIR`, which is often used to locate static files, media files, and templates.

```python
# Created by django create-project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/")
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles/")
```

The expression for `BASE_DIR` means: get the path to the current file (`settings.py`), get the parent folder (whatever you named your project), get the parent folder (the root of the project). So `STATIC_ROOT` will then be evaluated to `/staticfiles` (with `/` meaning the root of your project/repo).

With `django-split-settings` `settings` is now a module (instead of a file), so `os.path.dirname(os.path.dirname(os.path.abspath(__file__)))` will evaluate to `/whatever-you-named-your-project` as opposed to `/`.

To fix this `BASE_DIR` needs to be set to the parent folder of `/whatever-you-named-your-project`:

```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

## Do you want to contribute?

Read the [CONTRIBUTING.md](https://github.com/sobolevn/django-split-settings/blob/master/CONTRIBUTING.md) file.


## Version history

See [CHANGELOG.md](https://github.com/sobolevn/django-split-settings/blob/master/CHANGELOG.md) file.
