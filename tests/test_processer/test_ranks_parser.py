#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymarketcap import Pymarketcap
pym = Pymarketcap()

currencies = pym.ranks()

def assert_any_field_in_response(field, readable_field):
    found = False
    for rank in ["gainers", "losers"]:
        for period in ["1h", "24h", "7d"]:
            for curr in currencies[rank][period]:
                value = curr[field]
                if isinstance(value, (int, float)):
                    found = True
                elif isinstance(value, str):
                    if value != "":
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
              + "Check 'processer:ranks()' function.")
        raise err

def test_name():
    assert_any_field_in_response("name", "currency name")

def test_website_slug():
    assert_any_field_in_response("website_slug", "website_slug")

def test_symbol():
    assert_any_field_in_response("symbol", "currency symbol")

def test_percent_change():
    assert_any_field_in_response("percent_change", "percent_change")

def test_price():
    assert_any_field_in_response("price", "price")

def test_volume_24h():
    assert_any_field_in_response("volume_24h", "volume_24h")
