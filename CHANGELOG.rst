=========
Changelog
=========

0.2.2
-----

* Now supporting `unicode` filenames, fixes https://github.com/sobolevn/django-split-settings/issues/9
* Tests structure is changed
* Removed example
* Changed how `MANIFEST.in` is defined

0.2.1
-----

* Changed ``optional`` to be a function.
* Added ``test_tools.py``, achieved 100% in coverage.
* Removed ``setuptools-git`` from ``setup.py``, now ``Manifest`` is only way to provide ``dist`` sources.
* Added ``run_coveralls.py`` to work on both ``CI`` and local tests.
* Style fixes.

0.2.0
-----

* Now ``tox`` is used for testing.
* Added ``coverage`` information and badge.
* Removed ``pep8`` utility, now using ``pylint``.

0.1.3
-----

* Python 3.5 support, Django 1.9 test-support, documentation updates.

0.1.2
-----

* Fixed Python 3 compatibility. Fixed `issue #7`_.

0.1.1
-----

* Fixed `issue #1`_: now works with Gunicorn, too

0.1.0
-----

* Initial version

.. _`issue #1`: https://github.com/sobolevn/django-split-settings/issues/1
.. _`issue #7`: https://github.com/sobolevn/django-split-settings/issues/7
