#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from pymarketcap import AsyncPymarketcap
from pymarketcap.tests.consts import asyncparms

def test_types(event_loop):
    async def wrapper():
        async with AsyncPymarketcap(**asyncparms) as apym:
            res = await apym._cache_symbols()

            assert type(res) == dict
            for symbol, slug in res.items():
                assert type(symbol) == str
                assert type(slug) == str
    event_loop.run_until_complete(wrapper())


def test_consistence(event_loop):
    async def wrapper():
        async with AsyncPymarketcap() as apym:
            res = await apym._cache_symbols()
            assert len(res) > 0
    event_loop.run_until_complete(wrapper())
