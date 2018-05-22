#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

import pytest

from pymarketcap import AsyncPymarketcap
from pymarketcap.tests import disabled_decorator
from pymarketcap.tests.consts import asyncparms

asyncparms["debug"] = False

cache_file = os.path.join(
    os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
    "cache", "every_currency.json"
)
exists_cache_file = os.path.exists(cache_file)

res = []

end2end_marked_if_not_cache = \
    pytest.mark.end2end if not exists_cache_file else disabled_decorator


@pytest.mark.order1
@end2end_marked_if_not_cache
def test_all_currencies(event_loop):
    async def get_all_currencies():
        async with AsyncPymarketcap(**asyncparms) as apym:
            async for currency in apym.every_currency():
                res.append(currency)

    if exists_cache_file:
        with open(cache_file, "r") as f:
            for curr in json.loads(f.read()):
                res.append(curr)
    else:
        event_loop.run_until_complete(get_all_currencies())


def assert_any_field_in_response(field, readable_field):
    found = False
    for curr in res:
        value = curr[field]

        if isinstance(value, list):
            if len(value) > 0:
                found = True
        elif isinstance(value, str):
            if value != "":
                found = True
        elif isinstance(value, (int, float, bool)):
            found = True
        elif value is None:
            continue
        else:
            msg = "Case not anticipated. 'type(value) == %r'"
            raise NotImplementedError(msg % type(value))
    try:
        assert found == True
    except AssertionError as err:
        print("Any %s found searching all currencies." % readable_field \
              + "Check 'processer:currency()' function.")
        raise err


@end2end_marked_if_not_cache
def test_chats():
    assert_any_field_in_response("chats", "chat")


@end2end_marked_if_not_cache
def test_webs():
    assert_any_field_in_response("webs", "website")


@end2end_marked_if_not_cache
def test_explorers():
    assert_any_field_in_response("explorers", "explorer")


@end2end_marked_if_not_cache
def test_webs():
    assert_any_field_in_response("message_boards", "message board")


@end2end_marked_if_not_cache
def test_source_code():
    assert_any_field_in_response("source_code", "source code link")


@end2end_marked_if_not_cache
def test_announcement():
    assert_any_field_in_response("announcement", "announcement")


@end2end_marked_if_not_cache
def test_mineable():
    assert_any_field_in_response("mineable", "'mineable == True' flag")


@end2end_marked_if_not_cache
def test_rank():
    assert_any_field_in_response("rank", "'rank != None'")


@end2end_marked_if_not_cache
def test_max_supply():
    assert_any_field_in_response("max_supply", "'max_supply != None'")


@end2end_marked_if_not_cache
def test_total_supply():
    assert_any_field_in_response("total_supply", "'total_supply != None'")


@end2end_marked_if_not_cache
def test_circulating_supply():
    assert_any_field_in_response("circulating_supply",
                                 "'circulating_supply != None'")
