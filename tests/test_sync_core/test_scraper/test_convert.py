#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import choice, uniform
from operator import lt, gt, eq

import pytest

from pymarketcap import Pymarketcap
pym = Pymarketcap()

currencies_to_convert = pym.currencies_to_convert
currencies_to_convert.remove("USD")

def test_USD_to_USD():
    value = uniform(1, 1000)
    res = pym.convert(value, "USD", "USD")

    # Test types
    assert isinstance(res, float)

    # Test consistence
    assert res == value

def test_USD_to_x():
    value = uniform(1, 1000)
    symbol = choice(currencies_to_convert)
    print("(Symbol: %s)" % symbol, end=" ")
    res = pym.convert(value, "USD", symbol)

    """
    # Test types
    assert isinstance(res, float)

    # Test consistence
    rates = pym.currency_exchange_rates
    for op in (lt, gt):
        if not op(rates[symbol], rates["USD"]):  # Inverted
            assert op(res, value)
    """

def test_x_to_USD():
    value = uniform(1, 1000)
    symbol = choice(currencies_to_convert)
    print("(Symbol: %s)" % symbol, end=" ")
    res = pym.convert(value, symbol, "USD")

    # Test types
    assert isinstance(res, float)

    # Test consistence
    rates = pym.currency_exchange_rates
    for op in (lt, gt, eq):
        if op(rates[symbol], rates["USD"]):  # Multiplied
            assert op(res, value)

def test_x_to_y():
    value = uniform(1, 1000)
    symbol_1 = choice(currencies_to_convert)
    symbol_2 = choice(currencies_to_convert)
    print("(Symbol 1: %s | Symbol 2: %s)" \
          % (symbol_1, symbol_2), end=" ")
    res = pym.convert(value, symbol_1, symbol_2)

    # Test types
    assert isinstance(res, float)

    # Test consistence
    rates = pym.currency_exchange_rates
    for op in (lt, gt, eq):
        if op(rates[symbol_1], rates[symbol_2]):  # Multiplied
            assert op(res, value)

def test_invalid_symbol():
    symbol = "OUDBASDFADB"
    with pytest.raises(ValueError) as excinfo:
        pym.convert(0, symbol, "USD")
    assert "Invalid currency: '%s'" % symbol in str(excinfo.value)

def test_zero():
    symbol_1 = choice(currencies_to_convert)
    symbol_2 = choice(currencies_to_convert)
    print("(Symbol 1: %s | Symbol 2: %s)" \
          % (symbol_1, symbol_2), end=" ")
    res = pym.convert(0, symbol_1, symbol_2)
    assert res == 0
