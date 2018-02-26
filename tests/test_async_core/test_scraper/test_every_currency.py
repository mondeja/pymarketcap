#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio

import pytest

from pymarketcap.tests.currency import assert_types
from pymarketcap import (
    AsyncPymarketcapScraper,
    Pymarketcap
)
pym = Pymarketcap()

@pytest.mark.skip
@pytest.mark.end2end
@pytest.mark.asyncio
async def test_every_currency(event_loop):
    async with AsyncPymarketcapScraper(debug=True,
                                       queue_size=30,
                                       consumers=30) as apym:
        res = []
        async for (currency) in apym.every_currency():
            res.append(currency)

            # Test types
            assert_types(currency)
        assert type(res) == list

        # Assert consistence
        assert len(res) < pym.total_currencies + 100
        assert len(res) > pym.total_currencies - 100


