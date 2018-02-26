Reference
=========

pymarketcap.core
----------------

.. autoclass:: pymarketcap.core.Pymarketcap

    .. centered:: Coinmarketcap API

    .. automethod:: stats
    .. automethod:: ticker
    .. autoattribute:: symbols
    .. autoattribute:: coins
    .. autoattribute:: ticker_badges

    .. centered:: Web scraper

    .. automethod:: currency
    .. automethod:: exchange
    .. automethod:: exchanges
    .. autoattribute:: exchange_slugs
    .. autoattribute:: exchange_names
    .. automethod:: historical
    .. automethod:: markets
    .. automethod:: exchange
    .. automethod:: ranks
    .. automethod:: recently
    .. automethod:: tokens

    .. centered:: Graphs API
    .. note:: The next methods can be called also as ``graphs.currency()``, ``graphs.global_cap()`` and ``graphs.dominance()``.

    .. automethod:: _currency
    .. automethod:: _global_cap
    .. automethod:: _dominance

    .. centered:: Utils

    .. automethod:: convert
    .. automethod:: download_logo

pymarketcap.pymasyncore
-----------------------
.. autoclass:: pymarketcap.pymasyncore.AsyncPymarketcapScraper

    .. note:: All scraper methods described in ``Pymarketcap`` object and almost all the properties also exists in ``AsyncPymarketcapScraper``.
    .. automethod:: every_currency
    .. automethod:: every_markets
    .. automethod:: every_historical
    .. automethod:: every_exchange

pymarketcap.errors
------------------

.. automodule:: pymarketcap.errors
    :members:
    :undoc-members:
    :show-inheritance:
