#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pprint import pprint

import pytest

from pymarketcap import (
    Pymarketcap,
    AsyncPymarketcap,
)

def test_sync_interface(event_loop):
    async def wrapper():
        async with AsyncPymarketcap(debug=True) as apym:
            sync_interface = apym.sync
        assert isinstance(sync_interface, Pymarketcap)
    event_loop.run_until_complete(wrapper())

def test_cached_properties(event_loop):
    async def wrapper():
        async with AsyncPymarketcap(debug=True) as apym:
            properties = [
                "symbols", "coins", "exchange_names", "exchange_slugs"
            ]
            for prop in properties:
                res = eval("apym.%s" % prop)
                assert isinstance(res, list)
                assert len(res) > 0
    event_loop.run_until_complete(wrapper())

