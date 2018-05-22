#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymarketcap import Pymarketcap

pym = Pymarketcap()

tokens = pym.tokens()


def validate(value, may_be_empty=False):
    found = False
    if isinstance(value, str):
        found = may_be_empty or value != ""
    elif isinstance(value, (int, float)):
        found = True
    elif value is None:
        if may_be_empty:
            found = True
    else:
        raise NotImplementedError(
            "Case not anticipated. 'type(value) == %r'" % type(value)
        )
    return found


def assert_any_field_in_response(field, readable_field, may_be_empty=False):
    msg = ("Any %s found searching all currencies. "
           "Check 'processer:tokens()' function." % readable_field)
    try:
        assert all(validate(t[field], may_be_empty) for t in tokens), msg
    except AssertionError as err:
        print(msg)
        raise err


def test_name():
    assert_any_field_in_response("name", "currency name")


def test_symbol():
    assert_any_field_in_response("symbol", "currency symbol")


def test_platform():
    assert_any_field_in_response("platform", "platform")


def test_circulating_supply():
    assert_any_field_in_response(
        field="circulating_supply",
        readable_field="circulating_supply",
        may_be_empty=True
    )


def test_market_cap():
    assert_any_field_in_response(
        field="market_cap",
        readable_field="market_cap",
        may_be_empty=True
    )


def test_price():
    assert_any_field_in_response("price", "price")


def test_volume_24h():
    assert_any_field_in_response(
        field="volume_24h",
        readable_field="volume_24h",
        may_be_empty=True
    )
