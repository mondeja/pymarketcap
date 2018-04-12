#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from pymarketcap.tests.consts import asyncparms
from pymarketcap.tests.currency import (
    assert_types,
    assert_consistence
)
from pymarketcap import (
    AsyncPymarketcap,
    Pymarketcap
)
pym = Pymarketcap()

@pytest.mark.end2end
def test_every_currency(event_loop):
    async def wrapper():
        async with AsyncPymarketcap(**asyncparms) as apym:
            res = []
            show_msg = True
            async for (currency) in apym.every_currency():
                if show_msg:
                    print("Testing all responses...")
                    show_msg = False
                res.append(currency)

                # Test types
                assert_types(currency)
                assert_consistence(currency)
            assert type(res) == list
    event_loop.run_until_complete(wrapper())


