#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pprint import pprint

import pytest

from pymarketcap import (
    Pymarketcap,
    AsyncPymarketcapScraper,
)

@pytest.mark.asyncio
async def test_sync_interface():
    async with AsyncPymarketcapScraper(debug=True) as apym:
        sync_interface = apym.sync
    assert isinstance(sync_interface, Pymarketcap)

@pytest.mark.asyncio
async def test_cached_properties():
    async with AsyncPymarketcapScraper(debug=True) as apym:
        properties = [
            "symbols", "coins", "exchange_names", "exchange_slugs"
        ]
        for prop in properties:
            res = eval("apym.%s" % prop)
            assert type(res) == list
            assert len(res) > 0

