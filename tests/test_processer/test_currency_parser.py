#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from pymarketcap import AsyncPymarketcap
from pymarketcap.tests.consts import asyncparms

asyncparms["debug"] = False

@pytest.mark.end2end
def test_webs(event_loop):
    res = []
    async def get_all_currencies():
        async with AsyncPymarketcap(**asyncparms) as apym:
            async for currency in apym.every_currency():
                res.append(currency)

    event_loop.run_until_complete(get_all_currencies())

    web_found = False
    for r in res:
        print(r)
        if len(r["webs"]) > 0:
            web_found = True
    try:
        assert web_found == True
    except AssertionError as err:
        print("Any website found searching all currencies." \
        	  + "See 'processer:currency()' function.")
        raise err