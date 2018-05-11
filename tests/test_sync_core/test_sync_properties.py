#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test wrapper properties"""

from pymarketcap import Pymarketcap
from pymarketcap.tests import assert_cryptocurrency_or_exchange_types
pym = Pymarketcap()


###   API METHOD CACHERS   ###

def test_cryptoexchanges():
    res = pym.cryptoexchanges

    # Test types
    assert isinstance(res, list)
    for exchange in res:
        assert_cryptocurrency_or_exchange_types(exchange)
        # Test consistency
        for field in ["website_slug", "id", "name"]:
            assert field in exchange
    assert len(res) > 0

def test_cryptocurrencies():
    res = pym.cryptocurrencies

    # Test types
    assert isinstance(res, list)
    for currency in res:
        assert_cryptocurrency_or_exchange_types(currency)
        for field in ["website_slug", "id", "name", "symbol"]:
            assert field in currency
    assert len(res) > 0


###   WEB SCRAPER METHOD CACHERS   ###

def test_currency_exchange_rates():
    # Test types
    res = pym.currency_exchange_rates
    for key, value in res.items():
        assert isinstance(key, str)
        assert isinstance(value, float)

def test_currencies_to_convert():
    # Test types
    currencies = pym.currencies_to_convert
    assert isinstance(currencies,  list)
    for curr in currencies:
        assert isinstance(curr, str)

    # Test consistence
    assert len(currencies) > 0
