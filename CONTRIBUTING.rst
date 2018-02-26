Contributing and testing
========================

Testing
-------

You need to install ``pytest`` for run unittests and ``tox`` for run
tests against different versions:

::

    pip3 install -r dev-requirements.txt

You can run tests with ``pytest`` command:
  - Run all unittests: ``pytest tests``
  - Run also end2end tests: ``pytest tests --end2end``
  - `Run individual tests <https://docs.pytest.org/en/latest/usage.html#specifying-tests-selecting-tests>`__:

    + Run API tests: ``pytest tests/test_api``
    + Run ``historical()`` scraper method's consistence: ``pytest tests/test_scraper/test_historical.py::test_consistence``


Also, if your system is Unix, you can use ``make`` for run tests, install, precompile/restore source code, build and clean the whole directory (see `Makefile <https://github.com/mondeja/pymarketcap/blob/master/Makefile>`__).

--------------

Contributing guidelines
-----------------------

-  Each new method developed needs to be accompanied with their
   respective complete unittest as is shown in ``tests/`` directory.
-  Each new pull request needs to be good performed. Plase, don't make a
   pull request with 4 commits for change a line in the code.

Basic benchmarking
~~~~~~~~~~~~~~~~~~

You can test basically benchmarking of ``Pymarketcap`` class methods running
``python3 bench/main.py``. You can filter by name of benchmarks, change
the number of repetitions for each one or change file where store
benchmarks results: run ``python3 bench/main.py --help``.

TODO
~~~~
- Add posibility of return asynchronous responses in ``pandas.DataFrames`` objects or download it in ``.csv`` format.

--------------

How does pymarketcap works in depth?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Some pieces of code are precompiled before compile with Cython, so if
   you see missing parts on the source code before install (like the
   property method ``ticker_badges``), understand that they aren't bugs.
   Run ``make precompile-sources`` to do manual code precompilation and
   ``make restore-sources`` for restore souce code to original state.
-  The numerical values returned by the scraper are the real values with
   which coinmarketcap.com works, not the values displayed on their
   frontend (see source HTML code of the web).
-  Several methods are cached at instantiation time, so they can be
   obtained later without perform more HTTP requests. You can avoid this
   behavoiur passing ``cache=False`` to ``Pymarketcap`` object, but this
   will cause that some methods will not work.
