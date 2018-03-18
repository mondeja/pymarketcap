#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import choice

from pymarketcap.consts import EXCEPTIONAL_COIN_SLUGS_KEYS
from pymarketcap import Pymarketcap

pym = Pymarketcap()

def test_types():
    symbol = choice(pym.symbols)
    print("(Symbol: %s)" % symbol, end=" ")
    res = pym._is_symbol(symbol)
    assert type(res) == bool

    slug = choice(pym.coins)
    res = pym._is_symbol(slug)
    assert type(res) == bool

def test_consistence():
    # Symbol existent
    symbol = choice(pym.symbols)
    print("(Symbol: %s)" % symbol, end=" ")
    res = pym._is_symbol(symbol)
    assert res and symbol in pym.symbols

    # Eceptional symbol existent
    symbol = None
    for symbol in EXCEPTIONAL_COIN_SLUGS_KEYS:
        if symbol in pym.symbols:
            assert pym._is_symbol(symbol)
            break

    # Symbol not existent
    res = pym._is_symbol("OUBSAFYAIVADDOHNA")
    assert res  # It's True, see: processer._is_symbol.__doc__

    # Not symbol
    res = pym._is_symbol("ethereum")
    assert not res
