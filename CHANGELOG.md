# Version history

We follow Semantic Version.


## 1.1.0

### Features

- Adds `python3.9` support
- Adds `django3.1` support

### Misc

- Moves to Github Actions


## 1.0.1

### Bugfixes

- Fixes that django's dev server was not catching split setting filechanges


## 1.0.0

Breaking changes:

- Drops `python2` support
- Drops `django2.0` support

Improvements:

- Moves to `poetry`
- Adds `mypy` support
- Adds `wemake-python-styleguide` support
- Adds extra CI checks: `safety`, `doc8`
- Adds `py.typed` file to package type information


## 0.3.1

Improvements:

- Added support for django till to 2.2 version.


## 0.3.0

Improvements:

- Added `Django==2.0`
- Removed old versions of `Django` from test matrix
- Removed `python3.4` from test matrix
- Documentation updates
- Adds more `flake8` plugins to enforce strict style

Bugs:

- Fixes Windows problems via [#21](https://github.com/sobolevn/django-split-settings/pull/21)


## 0.2.5

Improvements:

- Added `python3.6` and `Django==1.11`
- Fixed `tests/settings` structure with `basic/` folder
- Added documentation, which is built with `Sphinx`
- Updated `README.rst` with new logo
- Updated `README.rst` with `docs` badge
- Updated `CONTRIBUTING.rst` with new information

Bugs:

- Updated `README.rst` to be compatible with `PyPI`


## 0.2.4

- Changed the default Django version in the requirements from `>= 1.5.1` to `>= 1.5`
- Added `setup.cfg` to support `python setup.py test` command
- Refactored how the tests work
- Added `tests/conftest.py` file with the fixtures, used fixtures widely
- Changed all test to be functions instead of classes
- Added new classifiers
- Added `pytest-env` to read env variables from `setup.cfg`
- Removed `run_coveralls.py`, added `after_success` section in `.travis.yml`
- Changed the `README.rst` to be shorter


## 0.2.3

- Added `django@1.10` support
- Now `include` function finds parent `globals()` scope automatically if not provided
- Added protection against infinite recursion
- Added tests for stackable settings definition. See `tests/settings/stacked/`
- Added tests for the new functionality
- Added tests for `django@1.10` in `tox` and `travis`
- Removed `3.2` and `3.3` from `setup.py` since these versions were not tested anyway


## 0.2.2

- Now supporting `unicode` filenames, fixes [#9](https://github.com/sobolevn/django-split-settings/issues/9)
- Tests structure is changed
- Removed example
- Changed how `MANIFEST.in` is defined


## 0.2.1

- Changed `optional` to be a function.
- Added `test_tools.py`, achieved 100% in coverage.
- Removed `setuptools-git` from `setup.py`, now `Manifest` is only way to provide `dist` sources.
- Added `run_coveralls.py` to work on both `CI` and local tests.
- Style fixes.


## 0.2.0

- Now `tox` is used for testing.
- Added `coverage` information and badge.
- Removed `pep8` utility, now using `pylint`.


## 0.1.3

- Python 3.5 support, Django 1.9 test-support, documentation updates.


## 0.1.2

- Fixed Python 3 compatibility. Fixed [#7](https://github.com/sobolevn/django-split-settings/issues/7).


## 0.1.1

- Fixed issue [#1](https://github.com/sobolevn/django-split-settings/issues/1): now works with Gunicorn, too


## 0.1.0

- Initial version
