Changelog
---------

3.9.0
~~~~~

-  All the wrapper rewritten with Cython language.
-  The data is obtained and processed by regular expressions instead of
   parsing the DOM tree.
-  Core functionality of the wrapper rewritten for work with ``libcurl``
   C library through a Cython wrap at compilation time.
   Also, you can use the wrapper with ``urllib`` standard library only
   installing by ``python setup.py install --no-curl``.
-  Tests now performed with ``pytest`` instead of standard library
   ``unittest``.
-  ``request``, ``lxml`` and ``bs4`` dependencies removed, only
   ``cython``, ``gcc`` and ``libcurl`` required for compile the code.
-  A precompiler added for insert some code and documentation hardcoded
   before compile the program.
-  All the data now is taken from values provided for the code that
   builds coinmarketcap instead the values displayed in the frontend
   page, as before. Is possible select between USD or BTC to returns
   these in most methods.
-  New method ``convert()`` for convert between currencies as
   coinmarketcap currencies calculator: https://coinmarketcap.com/calculator/
-  New method ``tokens()`` convering partially
   https://coinmarketcap.com/tokens/views/all/ endpoint.
-  New method ``currency()`` for get all metadata from a currency.
-  New asynchronous class interface with methods for retrieve
   faster long lists of exchanges or currencies: ``every_currency()``,
   ``every_exchange()``, ``every_historical()``.
-  Improvements in both speed and accuracy in exchanges and currencies
   cache, from ``quick_search.json`` and ``quick_search_exchanges.json``
   files of coinmarketcap server.

3.3.0
~~~~~

-  New method ``download_logo()`` that downloads images for all coins in
   coinmarketcap in various sizes.
-  New methods for retrieve info from ``graphs`` coinmarketcap internal
   API: ``graphs.currency``, ``graphs.global_cap`` and
   ``graphs.dominance``
-  Some symbols recognition improvements and bugs fixed.

--------------

    This proyect is originally a fork from
    https://github.com/barnumbirr/coinmarketcap
