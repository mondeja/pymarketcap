#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json

import pytest

from pymarketcap import AsyncPymarketcap
from pymarketcap.tests import disabled_decorator
from pymarketcap.tests.consts import asyncparms

asyncparms["debug"] = False

cache_file = os.path.join(
    os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
    "cache", "every_markets.json"
)
exists_cache_file = os.path.exists(cache_file)

res = []

end2end_marked_if_not_cache = \
    pytest.mark.end2end if not exists_cache_file else disabled_decorator

@pytest.mark.order1
@end2end_marked_if_not_cache
def test_all_markets(event_loop):
    async def get_all_markets():
        async with AsyncPymarketcap(**asyncparms) as apym:
            async for currency in apym.every_markets():
                res.append(currency)
    if exists_cache_file:
        with open(cache_file, "r") as f:
            for exc in json.loads(f.read()):
                res.append(exc)
    else:
        event_loop.run_until_complete(get_all_markets())

def assert_any_field_in_response(field, readable_field):
    found = False
    for curr in res:
        value = curr[field]

        if isinstance(value, str):
            if value != "":
                found = True
        elif isinstance(value, (list, dict)):
            if len(value) > 0:
                found = True
        elif isinstance(value, (int, float, bool)):
            found = True
        elif value == None:
            continue
        else:
            msg = "Case not anticipated. 'type(value) == %r'"
            raise NotImplementedError(msg % type(value))
    try:
        assert found == True
    except AssertionError as err:
        print("Any %s found searching all currencies." % readable_field \
              + "Check 'processer:markets()' function.")
        raise err

@end2end_marked_if_not_cache
def test_name():
    assert_any_field_in_response("name", "currency name")

@end2end_marked_if_not_cache
def test_website_slug():
    assert_any_field_in_response("website_slug", "website_slug")

@end2end_marked_if_not_cache
def test_symbol():
    assert_any_field_in_response("symbol", "currency symbol")

@end2end_marked_if_not_cache
def test_id():
    assert_any_field_in_response("id", "currency id")

@end2end_marked_if_not_cache
def test_markets():
    assert_any_field_in_response("markets", "market")