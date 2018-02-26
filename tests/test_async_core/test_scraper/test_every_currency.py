#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio

import pytest

from pymarketcap import (
    AsyncPymarketcapScraper,
    Pymarketcap
)
pym = Pymarketcap()

@pytest.mark.asyncio
async def test_every_currency(event_loop):
    async with AsyncPymarketcapScraper(debug=True) as apym:
        res = []
        async for (currency) in apym.every_currency():
            res.append(currency)

            # Test types
            assert type(currency) == dict
        assert type(res) == list

        # Assert consistence
        assert len(res) < pym.total_currencies + 100 and \
               len(res) > pym.total_currencies - 100


