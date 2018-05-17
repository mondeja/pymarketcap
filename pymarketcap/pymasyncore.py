#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Asynchronous Pymarketcap interface module."""

# Standard Python modules
import logging
from json import loads
from json.decoder import JSONDecodeError
from datetime import datetime
from asyncio import (
    ensure_future,
    Queue,
)
from asyncio import TimeoutError as AsyncioTimeoutError

# External Python dependencies
from aiohttp import ClientSession
from tqdm import tqdm

# Internal Cython modules
from pymarketcap import Pymarketcap
from pymarketcap import processer

# Internal Python modules
from pymarketcap.consts import DEFAULT_FORMATTER

# Logging initialization
LOGGER_NAME = "/pymarketcap%s" % __file__.split("pymarketcap")[-1]
LOGGER = logging.getLogger(LOGGER_NAME)
LOGGER_HANDLER = logging.StreamHandler()
LOGGER_HANDLER.setFormatter(DEFAULT_FORMATTER)
LOGGER.addHandler(LOGGER_HANDLER)

class AsyncPymarketcap(ClientSession):
    """Asynchronous scraper for coinmarketcap.com

    Args:
        queue_size (int): Number of maximum simultanenous
           get requests performing together in methods
           involving several requests. As default ``10``.
        progress_bar (bool): Select ``True`` or ``False`` if you
            want to show a progress bar in methods that involve
            processing of several requests (requires :mod:`tqdm`
            module). As default, ``True``.
        consumers (int): Number of consumers resolving HTTP
            requests from an internal
            :class:`asyncio.Queue <~asyncio.Queue>`.
            As default, ``10``.
        timeout (int/float, optional): Limit max time
            waiting for a response. As default, ``15``.
        logger (logging.logger): As default is a logger
            with a :class:`~python.logging.StreamHandler`.
        debug (bool, optional): If ``True``, the logger
            level will be setted as :data:`~logging.DEBUG`.
            As default ``False``.
        sync (object, optional): Synchronous version instance
            of pymarketcap. As default
            :py:class:`pymarketcap.core.Pymarketcap`
        **kwargs: arguments that corresponds to the
            :class:`aiohttp.client.ClientSession <~aiohttp.ClientSession>`
            parent class.
    """
    def __init__(self, queue_size=10, progress_bar=True,
                 consumers=10, timeout=15, logger=LOGGER,
                 debug=False, json=None, sync=Pymarketcap(),
                 **kwargs):
        super(AsyncPymarketcap, self).__init__(**kwargs)
        self.timeout = timeout
        self.logger = logger
        self.sync = sync

        # Async queue
        self.queue_size = queue_size
        self.connector_limit = self.connector.limit
        self._responses = []
        self.progress_bar = progress_bar
        self.consumers = consumers

        self.graphs = type(
            "Graphs", (),
            {"every_currency": self._every_currency}
        )

        if debug:
            self.logger.setLevel(logging.DEBUG)

    # ====================================================================

                         #######   UTILS   #######

    async def _get(self, url):
        async with self.get(url, timeout=self.timeout) as response:
            return await response.text()

    async def _async_multiget(self, itr, build_url_callback,
                              num_of_consumers=None, desc=""):
        queue, dlq, responses = Queue(maxsize=self.queue_size), Queue(), []
        try:
            itr_len = len(itr)
        except TypeError:
            itr_len = 1000000
        num_of_consumers = num_of_consumers or min(self.connector_limit, itr_len)
        consumers = [ensure_future(
            self._consumer(main_queue=queue, dlq=dlq, responses=responses)) for _ in
                     range(num_of_consumers or self.connector_limit)]
        dlq_consumers = [ensure_future(
            self._consumer(dlq, dlq, responses)) for _ in range(num_of_consumers)]
        await self._producer(itr, build_url_callback, queue, desc=desc)
        await queue.join()
        await dlq.join()

        all_consumers = consumers
        all_consumers.extend(dlq_consumers)
        for consumer in all_consumers:
            consumer.cancel()
        return responses

    async def _producer(self, items,
                        build_url_callback,
                        queue, desc=""):
        for item in tqdm(items, desc=desc, disable=not self.progress_bar):
            await queue.put(await build_url_callback(item))

    async def _consumer(self, main_queue, dlq, responses):
        while True:
            try:
                url = await main_queue.get()
                responses.append([url, await self._get(url)])
                # Notify the queue that the item has been processed
                main_queue.task_done()
            except AsyncioTimeoutError:
                self.logger.debug("Problem with %s, Moving to DLQ" % url)
                await dlq.put(url)
                main_queue.task_done()

    # ====================================================================

                         #######   SCRAPER   #######

    async def _base_currency_url(self, curr):
        parms = (self.sync.field_type(curr), curr)
        response = self.sync.cryptocurrency_by_field_value(*parms)
        if not response:
            raise ValueError(
                "Any cryptocurrency found matching %s == %r." % parms
            )
        else:
            curr = response["website_slug"]
        return "https://coinmarketcap.com/currencies/%s" % curr

    async def every_currency(self, currencies=None,
                             convert="USD", consumers=None):
        """Return general data from every currency in coinmarketcap
        passing a list of currencies as first parameter.
        As default returns data for all currencies.

        Args:
            currencies (list, optional): Iterator with all the
                currencies that you want to retrieve.
                As default ``None`` (:meth:`pymarketcap.Pymarketcap.coins`
                will be used in that case).
            convert (str, optional): Convert prices in response
                between "USD" and BTC. As default ``"USD"``.
            consumers (int, optional): Number of consumers
                processing the requests simultaneously.
                As default ``None``
                (see :attr:`pymarketcap.AsyncPymarketcap.consumers`).

        Returns (list): Data for all currencies.
        """
        currencies = currencies if currencies else \
             [curr["website_slug"] for curr in self.sync.cryptocurrencies]
        res = await self._async_multiget(
            currencies,
            self._base_currency_url,
            consumers if consumers else self.consumers,
            desc="Retrieving every currency data " \
                 + "for %d currencies from coinmarketcap" % len(currencies)
        )
        for url, raw_res in res:
            self.logger.debug("Processing data from %s" % url)
            response = processer.currency(raw_res[20000:], convert.lower())
            response.update(
                self.sync.cryptocurrency_by_field_value(
                    "website_slug", url.split("/")[-1]
                )
            )
            yield response

    async def every_markets(self, currencies=None,
                            convert="USD", consumers=None):
        """Returns markets data from every currency in coinmarketcap
        passing a list of currencies as first parameter.
        As default returns data for all currencies.

        Args:
            currencies (list, optional): Iterator with
                all the currencies that you want to retrieve.
                As default ``None`` (:meth:`pymarketcap.Pymarketcap.coins`
                will be used in that case).
            convert (str, optional): Convert prices in
                response between "USD" and BTC.
                As default ``"USD"``.
            consumers (int, optional): Number of consumers
                processing the requests simultaneously.
                As default ``None``
                (see :attr:`pymarketcap.AsyncPymarketcap.consumers`).

        Returns (async iterator):
                Data for all currencies.
        """
        currencies = currencies if currencies else \
            [curr["website_slug"] for curr in self.sync.cryptocurrencies]
        res = await self._async_multiget(
            currencies,
            self._base_currency_url,
            consumers if consumers else self.consumers,
            desc="Retrieving all markets " \
                 + "for %d currencies from coinmarketcap" % len(currencies)
        )
        for url, raw_res in res:
            self.logger.debug("Processing data from %s" % url)
            response = {"markets": processer.markets(raw_res[20000:], convert.lower()),
                        "slug": url.split("/")[-1]}
            response.update(
                self.sync.cryptocurrency_by_field_value(
                    "website_slug", url.split("/")[-1]
                )
            )
            yield response

    async def _base_historical_url(self, curr):
        parms = (self.sync.field_type(curr), curr)
        response = self.sync.cryptocurrency_by_field_value(*parms)
        if not response:
            raise ValueError(
                "Any cryptocurrency found matching %s == %r." % parms
            )
        else:
            curr = response["website_slug"]
        url = "https://coinmarketcap.com/currencies/%s/historical-data" % curr
        _start = "%d%02d%02d" % (self.__start.year, self.__start.month, self.__start.day)
        _end = "%d%02d%02d" % (self.__end.year, self.__end.month, self.__end.day)
        url += "?start=%s&end=%s" % (_start, _end)
        return url

    async def every_historical(self, currencies=None,
                               start=datetime(2008, 8, 18),
                               end=datetime.now(),
                               revert=False,
                               consumers=None):
        """Returns historical data from every currency
        in coinmarketcap passing a list of currencies
        as first parameter. As default returns data
        for all currencies.

        Args:
            currencies (list, optional): Iterator with all
                the currencies that you want to retrieve.
                As default ``None`` (:meth:`pymarketcap.Pymarketcap.coins`
                will be used in that case).
            start (date, optional): Time to start scraping
                periods as ``datetime.datetime`` type.
                As default ``datetime(2008, 8, 18)``.
            end (date, optional): Time to end scraping periods
                as datetime.datetime type.
                As default ``datetime.now()``.
            revert (bool, optional): If ``False``, return first date
                first, in chronological order, otherwise returns
                reversed list of periods. As default ``False``.
            consumers (int, optional): Number of consumers
                processing the requests simultaneously.
                As default ``None``
                (see :attr:`pymarketcap.AsyncPymarketcap.consumers`).

        Returns (async iterator):
            Historical data for all currencies.
        """
        self.__start = start
        self.__end = end
        currencies = currencies if currencies else \
            [curr["website_slug"] for curr in self.sync.cryptocurrencies]
        res = await self._async_multiget(
            currencies,
            self._base_historical_url,
            consumers if consumers else self.consumers,
            desc="Retrieving all historical data " \
                 + "for %d currencies from coinmarketcap" % len(currencies)
        )
        for url, raw_res in res:
            self.logger.debug("Processing data from %s" % url)
            response = {"history": processer.historical(raw_res[50000:],
                                                        start, end, revert),
                        "slug": url.split("/historical-data")[0].split("/")[-2]}
            response.update(
                self.sync.cryptocurrency_by_field_value(
                    "website_slug", url.split("/")[-2]
                )
            )
            yield response

    async def _base_exchange_url(self, exc):
        return "https://coinmarketcap.com/exchanges/%s" % exc

    async def exchange(self, name, convert="USD"):
        convert = convert.lower()
        res = await self._get(_base_exchange_url(name))[20000:]
        return processer.exchange(res, convert)

    async def every_exchange(self, exchanges=None, convert="USD", consumers=None):
        """Returns general data from every exchange
        in coinmarketcap passing a list of exchanges
        as first parameter. As default returns data
        for all exchanges.

        Args:
            exchanges (list, optional): Iterator with all
                the exchanges that you want to retrieve.
                As default ``None``
                (:meth:`pymarketcap.Pymarketcap.exchange_slugs`
                will be used in that case).
            convert (str, optional): Convert market_caps, prices,
                volumes and percent_changes between USD and BTC.
                As default ``"USD"``.
            consumers (int, optional): Number of consumers
                processing the requests simultaneously.
                As default ``None``
                (see :attr:`pymarketcap.AsyncPymarketcap.consumers`).

        Returns (async iterator):
            General data from all exchanges.
        """
        convert = convert.lower()
        exchanges = exchanges if exchanges else \
            [exc["website_slug"] for exc in self.sync.cryptoexchanges]
        res = await self._async_multiget(
            exchanges,
            self._base_exchange_url,
            consumers if consumers else self.consumers,
            desc="Retrieving all exchange data " \
                 + "for %d exchanges from coinmarketcap" % len(exchanges)
        )
        for url, raw_res in res:
            self.logger.debug("Processing data from %s" % url)
            response = processer.exchange(raw_res, convert)
            response.update(
                self.sync.exchange_by_field_value(
                    "website_slug", url.split("/")[-1]
                )
            )
            yield response

    # ====================================================================

                        #######   GRAPHS API   #######

    async def _base_graphs_currency_url(self, curr):
        parms = (self.sync.field_type(curr), curr)
        response = self.sync.cryptocurrency_by_field_value(*parms)
        if not response:
            raise ValueError(
                "Any cryptocurrency found matching %s == %r." % parms
            )
        else:
            curr = response["website_slug"]
        return "https://graphs2.coinmarketcap.com/currencies/%s" % curr

    async def _every_currency(self, currencies=None,
                              start=None, end=None, consumers=None):
        """Returns graphs data from every currency in
        coinmarketcap passing a list of currencies as
        first parameter. As default returns graphs data
        for all currencies.

        Args:
            currencies (list, optional): Iterator with all
                the currencies that you want to retrieve.
                As default ``None`` (:meth:`pymarketcap.Pymarketcap.coins`
                will be used in that case).
            start (datetime, optional): Time to start retrieving
                graphs data in datetime. As default ``None``.
            end (datetime, optional): Time to end retrieving
                graphs data in datetime. As default ``None``.
            consumers (int, optional): Number of consumers
                processing the requests simultaneously.
                As default ``None``
                (see :attr:`pymarketcap.AsyncPymarketcap.consumers`).

        Returns (async iterator): Graphs data from all currencies.
        """
        currencies = currencies if currencies else \
            [curr["website_slug"] for curr in self.sync.cryptocurrencies]
        res = await self._async_multiget(
            currencies,
            self._base_graphs_currency_url,
            consumers if consumers else self.consumers,
            desc="Retrieving all graphs data " \
                 + "for %d currencies from coinmarketcap" % len(currencies)
        )
        for url, raw_res in res:
            self.logger.debug("Processing data from %s" % url)
            raw_res = loads(raw_res)
            response = processer.graphs(raw_res, start, end)
            response.update(
                self.sync.cryptocurrency_by_field_value(
                    "website_slug", url.split("/")[-1]
                )
            )
            yield response
