#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from pymarketcap.tests.exchange import (
    assert_types,
    assert_consistence
)
from pymarketcap import (
    AsyncPymarketcapScraper,
    Pymarketcap
)
pym = Pymarketcap()


@pytest.mark.end2end
@pytest.mark.asyncio
async def test_every_currency(event_loop):
    async with AsyncPymarketcapScraper(debug=True,
                                       queue_size=50,
                                       consumers=50) as apym:
        res = []
        async for exc in apym.every_exchange():
            res.append(exc)

            assert_types(exc)
            assert_consistence(exc)
        assert type(res) == list
        assert len(res) < len(pym.exchange_slugs) + 100
        assert len(res) > len(pym.exchange_slugs) - 100



