#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import choice

from pymarketcap.processer import _is_symbol
from pymarketcap.consts import exceptional_coin_slugs_keys
from pymarketcap import Pymarketcap

pym = Pymarketcap()

def test_types():
    symbol = choice(pym.symbols)
    print("(Symbol: %s)" % symbol, end=" ")
    res = _is_symbol(symbol)
    assert type(res) == bool

    slug = choice(pym.coins)
    res = _is_symbol(slug)
    assert type(res) == bool

def test_consistence():
    # Symbol existent
    symbol = choice(pym.symbols)
    print("(Symbol: %s)" % symbol, end=" ")
    res = _is_symbol(symbol)
    assert res and symbol in pym.symbols

    # Eceptional symbol existent
    symbol = None
    for symbol in exceptional_coin_slugs_keys:
        if symbol in pym.symbols:
            assert _is_symbol(symbol)
            break

    # Symbol not existent
    res = _is_symbol("OUBSAFYAIVADDOHNA")
    assert res  # It's True, see: processer._is_symbol.__doc__

    # Not symbol
    res = _is_symbol("ethereum")
    assert not res
