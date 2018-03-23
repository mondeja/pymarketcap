Contributing
============

|Issues| |Percentage of issues still open| |Average time solving issues|

`TODO <https://github.com/mondeja/pymarketcap/milestone/2>`__

Basic guidelines
----------------

-  Each new method developed needs to be accompanied with their
   respective complete unittest as shown in ``tests/`` directory.
-  Each new pull request needs to be good performed. Plase, don't make a
   pull request with 4 commits for change a line in the code.

--------------

Basic benchmarking
~~~~~~~~~~~~~~~~~~

You can test basically benchmarking of ``Pymarketcap`` class methods running
``python3 bench/main.py``. You can filter by name of benchmarks, change
the number of repetitions for each one or change file where
benchmarks results are stored: run ``python3 bench/main.py --help``.

How does pymarketcap works in depth?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Some pieces of code are precompiled before compile with Cython, so if
   you see missing parts on the source code before install (like the
   property method ``ticker_badges``), understand that these are not bugs.
   Run ``make precompile-sources`` to do manual code precompilation and
   ``make restore-sources`` for restore souce code to original state.
-  The numerical values returned by the scraper are the real values with
   which coinmarketcap.com works, not the values displayed on their
   frontend (see source HTML code of the web).


.. |Issues| image:: https://img.shields.io/github/issues/mondeja/pymarketcap.svg
   :target: https://github.com/mondeja/pymarketcap/issues
.. |Percentage of issues still open| image:: http://isitmaintained.com/badge/open/mondeja/pymarketcap.svg
   :target: http://isitmaintained.com/project/mondeja/pymarketcap
.. |Average time solving issues| image:: http://isitmaintained.com/badge/resolution/mondeja/pymarketcap.svg
   :target: https://github.com/mondeja/pymarketcap/issues
