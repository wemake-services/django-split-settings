<p align="center">
  <img src="https://raw.githubusercontent.com/sobolevn/django-split-settings/master/docs/_static/logo-black.png"
       alt="django-split-settings logo">
</p>

---

[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services)
[![Build Status](https://travis-ci.com/wemake-services/docker-image-size-limit.svg?branch=master)](https://travis-ci.com/sobolevn/django-split-settings)
[![Coverage](https://coveralls.io/repos/github/sobolevn/django-split-settings/badge.svg?branch=master)](https://coveralls.io/github/sobolevn/django-split-settings?branch=master)
[![Docs](https://readthedocs.org/projects/django-split-settings/badge/?version=latest)](http://django-split-settings.readthedocs.io/en/latest/?badge=latest)
[![Python Version](https://img.shields.io/pypi/pyversions/django-split-settings.svg)](https://pypi.org/project/django-split-settings/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/docker-image-size-limit)



Organize Django settings into multiple files and directories. Easily
override and modify settings. Use wildcards in settings file paths
and mark settings files as optional.

Read [this blog post](https://sobolevn.me/2017/04/managing-djangos-settings)
for more information.
Also, check this [example project](https://github.com/wemake-services/wemake-django-template).


## Requirements

While this package will most likely work with the most versions of `django`, we [officially support](https://github.com/sobolevn/django-split-settings/blob/master/.travis.yml):

- 1.11
- 2.2
- 3.0

This package has no dependencies itself.

In case you need older `python` / `django` versions support,
then consider using older versions.


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

We also made a in-depth [tutorial](https://sobolevn.me/2017/04/managing-djangos-settings).


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


## Do you want to contribute?

Read the [CONTRIBUTING.md](https://github.com/sobolevn/django-split-settings/blob/master/CONTRIBUTING.md) file.


## Version history

See [CHANGELOG.md](https://github.com/sobolevn/django-split-settings/blob/master/CHANGELOG.md) file.
