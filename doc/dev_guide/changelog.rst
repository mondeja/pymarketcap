Changelog
---------

4.1.0 (in process)
~~~~~~~~~~~~~~~~~~

- Some tests added which assert if a field is ``None`` between all fields methods responses (see `#46 <https://github.com/mondeja/pymarketcap/issues/46>`__). These check if a field are not being parsed by ``processer.pyx`` regular expressions.
- New method ``ticker_all`` due to `coinmarketcap API <https://coinmarketcap.com/api/>`__ has implemented a limit of 100 for the number of currencies in ``/ticker/`` endpoint responses. With ``ticker_all`` we can retrieve all currencies from ``ticker`` method responses.

4.0.0
~~~~~

-  `Coinmarketcap API <https://coinmarketcap.com/es/api/>`__ is updated to version 2  providing the `listing endpoint <https://api.coinmarketcap.com/v2/listings/>`__ in their API. Also, parameters like ``usd_market_cap`` have been missing and instead a ``quotes`` field list prices by currencies in responses.
-  Some methods of ``Pymarketcap`` class have been deprecated: ``correspondences``, ``ids_correspondences``, ``_is_symbol``, ``_cache_symbols_ids``, ``_cache_exchanges_ids``, ``symbols``, ``coins``, ``total_currencies``, ``exchange_names``, ``__exchange_names_slugs``, ``exchange_slugs`` and ``total_exchanges``.
-  Next methods have been added instead: ``cryptocurrencies``, ``cryptocurrency_by_field_value``, ``cryptoexchanges``, ``exchange_by_field_value``, ``field_type`` and ``listings``. All methods listed in previous point have been replaced by these 6 methods, simplifying the process of access to cryptocurrencies and exchanges and allowing to retrieve them through any field: ``name``, ``symbol``, ``website_slug`` and ``id`` (cryptocurrencies) or ``name``, ``website_slug`` and ``id`` (exchanges).
- New method ``download_exchange_logo`` for synchronous interface.


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
