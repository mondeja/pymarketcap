#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from pymarketcap import AsyncPymarketcap

@pytest.mark.asyncio
async def test_types():
    async with AsyncPymarketcap(debug=True) as apym:
        res = await apym._cache_symbols()

        assert type(res) == dict
        for symbol, slug in res.items():
            assert type(symbol) == str
            assert type(slug) == str

@pytest.mark.asyncio
async def test_consistence():
    async with AsyncPymarketcap() as apym:
        res = await apym._cache_symbols()
        assert len(res) > 0
