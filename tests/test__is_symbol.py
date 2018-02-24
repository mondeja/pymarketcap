#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import choice

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
    for symbol in pym.exceptional_coin_slugs_keys:
        if symbol in pym.symbols:
            break
    res = pym._is_symbol(symbol)
    assert res

    # Symbol not existent
    res = pym._is_symbol("OUBSAFYAIVADDOHNA")
    assert res  # It's True, see: pym._is_symbol.__doc__

    # Not symbol
    res = pym._is_symbol("ethereum")
    assert not res
