Contributing
============

|Issues| |Percentage of issues still open| |Closed issues|

|Average time solving issues| |Issues closed in|

|Contributors| |Codetriage| |Last commit|

Known issues and enhacements
----------------------------

|Enhancement|


- Total: |Total bugs|
- Tests: |Test bugs|


Basic guidelines
----------------

-  Each new method developed needs to be accompanied with their
   respective complete unittest as shown in ``tests/`` directory.
-  Each new pull request needs to be good performed. Plase, don't make a
   pull request with 4 commits for change a line in the code.

--------------

Basic benchmarking
------------------

You can test basically benchmarking of ``Pymarketcap`` class methods running
``python3 bench/main.py``. You can filter by name of benchmarks, change
the number of repetitions for each one or change file where
benchmarks results are stored: run ``python3 bench/main.py --help``.

How does pymarketcap works in depth?
------------------------------------

|Repo size| |Code size|

-  Some pieces of code are precompiled before compile with Cython, so if
   you see missing parts on the source code before install (like the
   property method ``ticker_badges``), understand that these are not bugs.
   Run ``make precompile-sources`` to do manual code precompilation and
   ``make restore-sources`` for restore souce code to original state.
-  Numerical values returned by the scraper are real values with
   which `coinmarketcap.com <https://www.coinmarketcap.com>`__ works, not the values displayed on their frontend (see source HTML code of the web).

--------------

Contributors
------------

Pull requesters
~~~~~~~~~~~~~~~

- `badele <https://github.com/badele>`__
- `nkoshell <https://github.com/nkoshell>`__
- `wilcollins <https://github.com/wilcollins>`__

Bug hunters
~~~~~~~~~~~

- `Abolah <https://github.com/Abolah>`__
- `badele <https://github.com/badele>`__
- `Bragegs <https://github.com/Bragegs>`__
- `criptonaut1357 <https://github.com/criptonaut1357>`__
- `Prophetic-Pariah <https://github.com/Prophetic-Pariah>`__
- `reteps <https://github.com/reteps>`__
- `run2dev <https://github.com/run2dev>`__
- `Wingie <https://github.com/Wingie>`__

.. |Issues| image:: https://img.shields.io/github/issues/mondeja/pymarketcap.svg
   :target: https://github.com/mondeja/pymarketcap/issues
.. |Percentage of issues still open| image:: http://isitmaintained.com/badge/open/mondeja/pymarketcap.svg
   :target: http://isitmaintained.com/project/mondeja/pymarketcap
.. |Closed issues| image:: https://img.shields.io/github/issues-closed/mondeja/pymarketcap.svg
   :target: https://github.com/mondeja/pymarketcap/issues?q=is%3Aissue+is%3Aclosed
.. |Average time solving issues| image:: http://isitmaintained.com/badge/resolution/mondeja/pymarketcap.svg
   :target: https://github.com/mondeja/pymarketcap/issues
.. |Issues closed in| image:: https://img.shields.io/issuestats/i/long/github/mondeja/pymarketcap.svg
   :target: https://github.com/mondeja/pymarketcap/issues
.. |Contributors| image:: https://img.shields.io/github/contributors/mondeja/pymarketcap.svg
   :target: https://github.com/mondeja/pymarketcap/graphs/contributors
.. |Codetriage| image:: https://www.codetriage.com/mondeja/pymarketcap/badges/users.svg
   :target: https://www.codetriage.com/mondeja/pymarketcap
.. |Last commit| image:: https://img.shields.io/github/last-commit/mondeja/pymarketcap.svg
.. |Enhancement| image:: https://img.shields.io/github/issues/mondeja/pymarketcap/enhancement.svg
   :target: https://github.com/mondeja/pymarketcap/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement
.. |Test bugs| image:: https://img.shields.io/github/issues/mondeja/pymarketcap/test_bug.svg
   :target: https://github.com/mondeja/pymarketcap/issues?q=is%3Aissue+is%3Aopen+label%3Atest_bug
.. |Total bugs| image:: https://img.shields.io/github/issues/mondeja/pymarketcap/bug.svg
   :target: https://github.com/mondeja/pymarketcap/issues?q=is%3Aissue+is%3Aopen+label%3Abug
.. |Repo size| image:: https://img.shields.io/github/repo-size/mondeja/pymarketcap.svg
.. |Code size| image:: https://img.shields.io/github/languages/code-size/mondeja/pymarketcap.svg
