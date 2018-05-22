#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymarketcap import Pymarketcap

pym = Pymarketcap()

currencies = pym.recently()


def assert_any_field_in_response(field, readable_field):
    found = False
    for curr in currencies:
        value = curr[field]
        if isinstance(value, (int, float)):
            found = True
        elif isinstance(value, str):
            if value != "":
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
              + "Check 'processer:recently()' function.")
        raise err


def test_name():
    assert_any_field_in_response("name", "currency name")


def test_symbol():
    assert_any_field_in_response("symbol", "currency symbol")


def test_added():
    assert_any_field_in_response("added", "added date")


def test_circulating_supply():
    assert_any_field_in_response("circulating_supply", "circulating_supply")


def test_market_cap():
    assert_any_field_in_response("market_cap", "market_cap")


def test_percent_change():
    assert_any_field_in_response("percent_change", "percent_change")


def test_price():
    assert_any_field_in_response("price", "price")


def test_volume_24h():
    assert_any_field_in_response("volume_24h", "volume_24h")
