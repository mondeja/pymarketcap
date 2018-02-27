Basic usage
===========

Check out `complete live demos hosted at Binderhub <https://mybinder.org/v2/gh/mondeja/pymarketcap/master?filepath=docs%2Flive.ipynb>`__.

.. centered:: Synchronous Interface
.. code-block:: python

   from pymarketcap import Pymarketcap
   cmc = Pymarketcap()

   cmc.exchanges()

.. centered:: Asynchronous Scraper
.. code-block:: python

   from pymarketcap import AsyncPymarketcap
   import asyncio

   res = []
   async def get_every_exchange():
       async for exc in AsyncPymarketcap() as apym:
           res.append(exc)

   loop = asyncio.get_event_loop()
   loop.run_until_complete(get_every_exchange())
   print(res)