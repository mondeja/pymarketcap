#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio

import pytest

from pymarketcap.tests.exchange import assert_types
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
        async for exc in apym.every_exchange():
            res.append(exc)

            # Test types
            assert_types(exc)
        assert type(res) == list

        # Assert consistence
        assert len(res) < len(pym.exchange_slugs) + 100
        assert len(res) > len(pym.exchange_slugs) - 100
