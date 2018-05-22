#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

import pytest

from pymarketcap import (
    AsyncPymarketcap,
    Pymarketcap,
)
from pymarketcap.tests.consts import asyncparms
from pymarketcap.tests.exchange import (assert_consistence, assert_types)

pym = Pymarketcap()

cache_file = os.path.join(
    os.path.abspath(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    ),
    "cache", "every_exchange.json"
)

res = []


@pytest.mark.end2end
def test_every_exchange(event_loop):
    async def wrapper():
        async with AsyncPymarketcap(**asyncparms) as apym:
            show_msg = True
            async for exc in apym.every_exchange():
                if show_msg:
                    print("Testing all responses...")
                    show_msg = False
                res.append(exc)

                assert_types(exc)
                assert_consistence(exc)
            assert isinstance(res, list)

        with open(cache_file, "w") as f:
            f.write(json.dumps(res, ensure_ascii=False))

    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            for curr in json.loads(f.read()):
                res.append(curr)

        assert isinstance(res, list)
        for currency in res:
            assert_types(currency)
            assert_consistence(currency)
    else:
        event_loop.run_until_complete(wrapper())
