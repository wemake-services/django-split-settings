
.. image:: https://github.com/sobolevn/django-split-settings/blob/master/docs/_static/logo-black.png?raw=true
   :target: https://github.com/sobolevn/django-split-settings
   :align: center

----------

.. image:: https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D
   :target: https://wemake.services

.. image:: https://travis-ci.org/sobolevn/django-split-settings.svg?branch=master
   :target: https://travis-ci.org/sobolevn/django-split-settings

.. image:: https://coveralls.io/repos/github/sobolevn/django-split-settings/badge.svg?branch=master
   :target: https://coveralls.io/github/sobolevn/django-split-settings?branch=master

.. image:: https://badge.fury.io/py/django-split-settings.svg
   :target: http://badge.fury.io/py/django-split-settings

.. image:: https://img.shields.io/pypi/pyversions/django-split-settings.svg
   :target: https://pypi.python.org/pypi/django-split-settings

.. image:: https://readthedocs.org/projects/django-split-settings/badge/?version=latest
   :target: http://django-split-settings.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/style-wemake-000000.svg
   :target: https://github.com/wemake-services/wemake-python-styleguide


Organize Django settings into multiple files and directories. Easily
override and modify settings. Use wildcards in settings file paths
and mark settings files as optional.

Read this `blog`_ post for more information. Also, check this `example project`_.

.. _blog: https://sobolevn.me/2017/04/managing-djangos-settings
.. _`example project`: https://github.com/wemake-services/wemake-django-template

Requirements
------------

While this package will most likely work with the most versions of ``django``, we do not officially support any versions except the latest release and the current LTS version, which are ``1.11`` and ``2.2`` right now.

This package has no dependencies itself.


Installation
------------

.. code:: bash

    pip install django-split-settings


Usage
-----

Replace your existing ``settings.py`` with a list of components that
make up your Django settings. Preferably create a settings package
that contains all the files.

Here's a minimal example:

.. code:: python

    from split_settings.tools import optional, include

    include(
        'components/base.py',
        'components/database.py',
        optional('local_settings.py')
    )

In the example, the files ``base.py`` and ``database.py`` are included
in that order from the subdirectory called ``components/``.
``local_settings.py`` in the same directory is included if it exists.

**Note:** The local context is passed on to each file, so each
following file can access and modify the settings declared in the
previous files.

We also made a in-depth `tutorial`_.

.. _tutorial: https://medium.com/wemake-services/managing-djangos-settings-e2b7f496120d


Tips and tricks
---------------


You can use wildcards in file paths:

.. code:: python

    include('components/my_app/*.py')

Note that files are included in the order that ``glob`` returns them,
probably in the same order as what ``ls -U`` would list them. The
files are NOT in alphabetical order.

You can modify common settings in environment settings simply importing them

.. code:: python

    # local_settings.py
    from components.base import INSTALLED_APPS

    INSTALLED_APPS += (
      'raven.contrib.django.raven_compat',
    )


Do you want to contribute?
--------------------------

Read the `contributing`_ file.

.. _contributing: https://github.com/sobolevn/django-split-settings/blob/master/CONTRIBUTING.rst


Version history
---------------

See `changelog`_ file.

.. _changelog: https://github.com/sobolevn/django-split-settings/blob/master/CHANGELOG.rst
