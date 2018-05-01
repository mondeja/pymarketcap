#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json

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

cache_file = os.path.join("tests", "cache", "every_currency.json")

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

        with open(cache_file, "w") as f:
            f.write(json.dumps(res, ensure_ascii=False))

    event_loop.run_until_complete(wrapper())


