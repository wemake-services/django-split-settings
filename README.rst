
.. image:: https://github.com/sobolevn/django-split-settings/blob/master/media/logo-black.png?raw=true
     :target: https://github.com/sobolevn/django-split-settings
     :align: center

----------

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

Organize Django settings into multiple files and directories. Easily
override and modify settings. Use wildcards in settings file paths
and mark settings files as optional.


Requirements
------------

We support ``django`` versions from ``1.5`` up to the most recent one.


Installation
------------

Install by using ``pip``:

.. code:: bash

    pip install django-split-settings


Usage
-----

Replace your existing ``settings.py`` with a list of components that
make up your Django settings.  Preferably create a settings package
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


Tips and tricks
---------------

You can use wildcards in file paths:

.. code:: python

    include('components/my_app/*.py')

Note that files are included in the order that ``glob`` returns them,
probably in the same order as what ``ls -U`` would list them. The
files are NOT in alphabetical order.


Windows only!

You can improve settings files loading speed if requirements are satisfied:
* running on Windows 7 or above
* pypiwin32 library installed

What you'll get:

.. code:: python

     # Testing file "test.bin" with size ~ 100 Kb

     code = '''
     with open("test.bin", "rb") as f:
       data = f.read()
     '''

     loop_first = timeit.Timer(stmt=code)

     setup = '''
     from f_open.file import FastOpen
     '''

     code = '''
     with FastOpen("test.bin") as file:
       data = file.read()
     '''

     loop_second = timeit.Timer(stmt=code, setup=setup)

     >>> print('Best of 3 open() running time: {} sec.'.format(min(loop_first.repeat(repeat=3, number=1000))))
     >>> print('Best of 3 FastOpen running time: {} sec.'.format(min(loop_second.repeat(repeat=3, number=1000))))

     Best of 3 open() running time: 0.08507176789928023 sec.
     Best of 3 f_open running time: 0.05143420851690639 sec.


Do you want to contribute?
--------------------------

Read the `contributing`_ file.

.. _contributing: https://github.com/sobolevn/django-split-settings/blob/master/CONTRIBUTING.rst


Version history
---------------

See `changelog`_ file.

.. _changelog: https://github.com/sobolevn/django-split-settings/blob/master/CHANGELOG.rst
