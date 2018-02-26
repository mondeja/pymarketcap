#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Python modules
import re
import logging
from json import loads
from datetime import datetime
from collections import OrderedDict

# External Python dependencies
from aiohttp import ClientSession

# Internal Cython modules
from pymarketcap import Pymarketcap

# Internal Python modules
from pymarketcap.consts import (
    DEFAULT_TIMEOUT,
    exceptional_coin_slugs,
    DEFAULT_FORMATTER
)
from pymarketcap import processer

# Logging initialization
logger_name = "/pymarketcap%s" % __file__.split("pymarketcap")[-1]
logger = logging.getLogger(logger_name)
handler = logging.StreamHandler()
handler.setFormatter(DEFAULT_FORMATTER)
logger.addHandler(handler)

class AsyncPymarketcapScraper(ClientSession):

    def __init__(self, timeout=DEFAULT_TIMEOUT,
                 logger=logger, debug=False, **kwargs):
        super(AsyncPymarketcapScraper, self).__init__(**kwargs)
        self.timeout = timeout
        self.logger = logger

        if debug:
            self.logger.setLevel(logging.DEBUG)

    @property
    def correspondences(self):
        try:
            return self._correspondences
        except AttributeError:
            self._correspondences = self._cache_symbols()
            return self._correspondences

    @property
    def symbols(self):
        try:
            return self._symbols
        except AttributeError:
            self._symbols = sorted(list(self.correspondences.keys()))
            return self._symbols

    async def _cache_symbols(self):
        url = "https://files.coinmarketcap.com/generated/search/quick_search.json"
        res = await self._get(url)
        symbols = {}
        for currency in loads(res):
            symbols[currency["symbol"]] = currency["slug"].replace(" ", "")
        for original, correct in exceptional_coin_slugs.items():
            symbols[original] = correct
        return symbols

    async def _get(self, url):
        async with self.get(url, timeout=self.timeout) as response:
            return await response.text()

    async def currency(self, name, convert="USD"):
        if self._is_symbol(name):
            name = self.correspondences[name]
        convert = convert.lower()

        url = "https://coinmarketcap.com/currencies/%s/" % name
        res = await self._get()

        # Total market capitalization and volume 24h
        return processer.currency(res[20000:], convert)

    async def markets(self, name, convert="USD"):
        if _is_symbol(name):
            name = self.correspondences[name]
        convert = convert.lower()

        url = "https://coinmarketcap.com/currencies/%s/" % name
        res = await self._get(url)

        return processer.markets(res[20000:], convert)

    async def ranks(self):
        res = await self._get("https://coinmarketcap.com/gainers-losers/")
        return processer.ranks(res)

    async def historical(self, currency,
                         start=datetime(2008, 8, 18),
                         end=datetime.now(),
                         revert=False):
        if _is_symbol(currency):
            currency = self.correspondences[currency]

        url = "https://coinmarketcap.com/currencies/%s/historical-data/" % currency
        _start = "%d%02d%02d" % (start.year, start.month, start.day)
        _end = "%d%02d%02d" % (end.year, end.month, end.day)
        url += "?start=%s&end=%s" % (_start, _end)
        res = await self._get(url)

        return processer.historical(res[50000:], start, end, revert)

    async def recently(self, convert="USD"):
        convert = convert.lower()
        url = "https://coinmarketcap.com/new/"
        res = await self._get(url)
        return list(processer.recently(res, convert))

