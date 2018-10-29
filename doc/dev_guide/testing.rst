Testing
=======

|TravisCI| |AppVeyor|

You need to install ``pytest`` for run unittests:

::

    pip3 install -r dev-requirements.txt

You can run tests with ``pytest`` command:
  - Run all unittests: ``pytest tests``
  - Run also tests for asynchronous interface: ``pytest tests --end2end``
  - `Run individual tests <https://docs.pytest.org/en/latest/usage.html#specifying-tests-selecting-tests>`__:

    + Run API tests: ``pytest tests/test_sync_core/test_public_api``
    + Run ``every_historical()`` async scraper method's consistence: ``pytest tests/test_async_core/test_scraper/test_every_historical.py``


Also, if your system is Unix, you can use ``make`` for run tests, install, precompile/restore source code, build and clean the whole directory (see `Makefile <https://github.com/mondeja/pymarketcap/blob/master/Makefile>`__).


You can see online tests for Linux/Mac and Windows based systems at TravisCI and AppVeyor:

- `TravisCI <https://travis-ci.org/mondeja/pymarketcap>`__
- `AppVeyor <https://ci.appveyor.com/project/mondeja/pymarketcap>`__

.. |TravisCI| image:: https://travis-ci.org/mondeja/pymarketcap.svg?branch=master
   :target: https://travis-ci.org/mondeja/pymarketcap
.. |AppVeyor| image:: https://ci.appveyor.com/api/projects/status/puy2p0qhjna4hosc?svg=true
   :target: https://ci.appveyor.com/project/mondeja/pymarketcap
