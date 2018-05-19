#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for ticker() method"""

from random import choice, randint

from pymarketcap.tests import type_test
from pymarketcap.tests.utils import random_cryptocurrency
from pymarketcap import Pymarketcap
pym = Pymarketcap()


def assert_types(res):
    map_types = {
        "id":                   int,
        "name":                 str,
        "symbol":               str,
        "rank":                 int,
        "quotes":               dict,
        "website_slug":         str,
        "circulating_supply":   (float, int, type(None)),
        "total_supply":         (float, int, type(None)),
        "max_supply":           (float, int, type(None)),
        "last_updated":         (int, type(None))
    }

    quotes_map_types = {
        "market_cap":           (float, int, type(None)),
        "percent_change_1h":    (float, type(None)),
        "percent_change_24h":   (float, type(None)),
        "percent_change_7d":    (float, type(None)),
        "price":                (float, type(None)),
        "volume_24h":           (float, type(None)),
    }

    assert isinstance(res, dict)
    for key, value in res.items():
        if key == "quotes":
            for _key, _value in value.items():
                for __key, __value in _value.items():
                    type_test(quotes_map_types, __key, __value)
        type_test(map_types, key, value)


def assert_consistence(res):
    assert len(res) == 10


def test_consistence():
    res = pym.ticker()
    for _id, curr_data in res["data"].items():
        assert_types(curr_data)
        assert_consistence(curr_data)

def test_limit():
    res = pym.ticker(limit=40)["data"]   # Max 100
    assert len(res) == 40
    res = pym.ticker(limit=90)["data"]
    assert len(res) == 90

def test_symbol():
    symbol = random_cryptocurrency(pym)["symbol"]
    print('(<currency>["symbol"] == "%s")' % symbol, end=" ")
    res = pym.ticker(symbol)["data"]

    assert_types(res)
    assert_consistence(res)

def test_name():
    name = random_cryptocurrency(pym)["name"]
    print('(<currency>["name"] == "%s")' % name, end=" ")
    res = pym.ticker(name)["data"]

    assert_types(res)
    assert_consistence(res)

def test_start():
    pos = randint(0, len(pym.cryptocurrencies))
    res = pym.ticker(start=pos)["data"]
    curr_id = list(res.keys())[0]
    assert res[curr_id]["rank"] == pos
    assert_types(res[curr_id])
    assert_consistence(res[curr_id])

def test_convert():
    for currency in [True, False]:  # With and without currency
        symbol = None
        badge = choice(pym.ticker_badges)
        if currency:
            symbol = random_cryptocurrency(pym)["symbol"]
            print('(<currency>["name"] == "%s") - Badge: %s)' \
                      % (symbol, badge), end=" | ")
        else:
            print("(Badge: %s)" % badge, end=" ")

        res = pym.ticker(currency=symbol, convert=badge)["data"]
        if currency:
            assert_types(res)
            assert_consistence(res)


def test_ticker_all():
    res = pym.ticker_all()
    for curr in res:
        assert_types(curr)
        assert_consistence(curr)
