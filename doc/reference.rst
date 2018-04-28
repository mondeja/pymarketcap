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
    .. note:: The ``graphs`` methods can be called also as ``cmc.graphs.currency()``, ``cmc.graphs.global_cap()`` and ``cmc.graphs.dominance()``, being ``cmc`` a instance of ``Pymarketcap`` or ``AyncPymarketcap`` classes.

    .. automethod:: _currency
    .. automethod:: _global_cap
    .. automethod:: _dominance

    .. centered:: Utils

    .. automethod:: convert
    .. automethod:: download_logo
    .. automethod:: download_exchange_logo

pymarketcap.pymasyncore
-----------------------
.. autoclass:: pymarketcap.pymasyncore.AsyncPymarketcap
    :show-inheritance:

    .. note:: All scraper methods described in ``Pymarketcap`` object and almost all the properties also exists in ``AsyncPymarketcap``.

    .. automethod:: every_currency
    .. automethod:: every_markets
    .. automethod:: every_historical
    .. automethod:: every_exchange

    .. note:: The next method can be called also as ``graphs.every_currency()``.
    .. automethod:: _every_currency

pymarketcap.errors
------------------

.. automodule:: pymarketcap.errors
    :members:
    :undoc-members:
    :show-inheritance:
