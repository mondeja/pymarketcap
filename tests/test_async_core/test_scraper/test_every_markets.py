#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from pymarketcap.tests.markets import (
    assert_types,
    assert_consistence
)
from pymarketcap import (
    AsyncPymarketcap,
    Pymarketcap
)
pym = Pymarketcap()

@pytest.mark.end2end
def test_every_markets(event_loop):
    async def wrapper():
        async with AsyncPymarketcap(debug=True,
                                    queue_size=50,
                                    consumers=50) as apym:
            res = []
            show_msg = True
            async for (currency) in apym.every_markets():
                if show_msg:
                    print("Testing all responses...")
                    show_msg = False
                res.append(currency)

                assert_types(currency)
                assert_consistence(currency)

            assert type(res) == list
            assert len(res) < pym.total_currencies + 100
            assert len(res) > pym.total_currencies - 100
    event_loop.run_until_complete(wrapper())
