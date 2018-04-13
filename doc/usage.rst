Basic usage
===========

Check out `complete live demos hosted at Binderhub <https://mybinder.org/v2/gh/mondeja/pymarketcap/master?filepath=docs%2Fsync_live.ipynb>`__.

.. centered:: Synchronous Interface
.. code-block:: python

   from pymarketcap import Pymarketcap
   cmc = Pymarketcap()

   cmc.exchanges()

.. centered:: Asynchronous Scraper
.. code-block:: python

    import asyncio
    from pymarketcap import AsyncPymarketcap

    async def main():
        async with AsyncPymarketcap() as apym:
            async for currency in apym.every_currency():
                print(currency)

    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())