#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymarketcap import Pymarketcap
pym = Pymarketcap()

tokens = pym.tokens()

def assert_any_field_in_response(field, readable_field):
    found = False
    for token in tokens:
        value = token[field]
        if isinstance(value, str):
            if value != "":
                found = True
        elif isinstance(value, (int, float)):
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
              + "Check 'processer:tokens()' function.")
        raise err

def test_name():
    assert_any_field_in_response("name", "currency name")

def test_symbol():
    assert_any_field_in_response("symbol", "currency symbol")

def test_platform():
    assert_any_field_in_response("platform", "platform")

def test_circulating_supply():
    assert_any_field_in_response("circulating_supply", "circulating_supply")

def test_market_cap():
    assert_any_field_in_response("market_cap", "market_cap")

def test_price():
    assert_any_field_in_response("price", "price")

def test_volume_24h():
    assert_any_field_in_response("volume_24h", "volume_24h")
