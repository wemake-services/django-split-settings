=====================
django-split-settings
=====================

.. image:: https://travis-ci.org/sobolevn/django-split-settings.svg?branch=master
   :target: https://travis-ci.org/sobolevn/django-split-settings

.. image:: https://coveralls.io/repos/github/sobolevn/django-split-settings/badge.svg?branch=master
   :target: https://coveralls.io/github/sobolevn/django-split-settings?branch=master

.. image:: https://badge.fury.io/py/django-split-settings.svg
   :target: http://badge.fury.io/py/django-split-settings

.. image:: https://img.shields.io/pypi/pyversions/django-split-settings.svg
   :target: https://pypi.python.org/pypi/django-split-settings

Organize Django settings into multiple files and directories.  Easily
override and modify settings.  Use wildcards in settings file paths
and mark settings files as optional.


Requirements
============

Python 2.7, 3.4, 3.5

Django >= 1.5, <= 1.10 (depends on your Python version)


Installation
============

Install by using ``pip``:

.. code-block:: bash

    pip install django-split-settings


Usage
=====

Replace your existing ``settings.py`` with a list of components that
make up your Django settings.  Preferably create a settings package
that contains all the files.

Here's a minimal example:

.. code-block:: python

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


Tips and tricks
===============

You can use wildcards in file paths:

.. code-block:: python

    include('components/my_app/*.py')

Note that files are included in the order that ``glob`` returns them,
probably in the same order as what ``ls -U`` would list them. The
files are NOT in alphabetical order.


Do you want to contribute?
==========================

Read the `contributing`_ file.

Authors
=======

    * `akaihola`_
    * `roxeteer`_
    * `sobolevn`_
    * `phpdude`_


Changelog
=========

See `changelog`_ file.


.. _`contribute`: https://github.com/sobolevn/django-split-settings/blob/master/CONTRIBUTING.rst
.. _`akaihola`: https://github.com/akaihola
.. _`roxeteer`: https://github.com/roxeteer
.. _`sobolevn`: https://github.com/sobolevn
.. _`phpdude`: https://github.com/phpdude
.. _`changelog`: https://github.com/sobolevn/django-split-settings/blob/master/CHANGELOG.rst
