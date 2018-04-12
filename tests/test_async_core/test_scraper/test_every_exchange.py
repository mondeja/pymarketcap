#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from pymarketcap.tests.consts import asyncparms
from pymarketcap.tests.exchange import (
    assert_types,
    assert_consistence
)
from pymarketcap import (
    AsyncPymarketcap,
    Pymarketcap
)
pym = Pymarketcap()


@pytest.mark.end2end
def test_every_exchange(event_loop):
    async def wrapper():
        async with AsyncPymarketcap(**asyncparms) as apym:
            res = []
            show_msg = True
            async for exc in apym.every_exchange():
                if show_msg:
                    print("Testing all responses...")
                    show_msg = False
                res.append(exc)

                assert_types(exc)
                assert_consistence(exc)
            assert type(res) == list
    event_loop.run_until_complete(wrapper())



