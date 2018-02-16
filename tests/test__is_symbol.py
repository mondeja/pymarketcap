#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from random import choice

from pymarketcap import Pymarketcap
pym = Pymarketcap()

all_symbols = list(pym.correspondences.keys())
all_slugs = list(pym.correspondences.values())

def teardown_function(function):
    time.sleep(2)

def test_types():
    symbol = choice(all_symbols)
    print("(Symbol: %s)" % symbol, end=" ")
    res = pym._is_symbol(symbol)
    assert type(res) == bool

    slug = choice(all_slugs)
    res = pym._is_symbol(slug)
    assert type(res) == bool

def test_consistence():
    existent_symbols = pym.correspondences.keys()

    # Symbol existent
    symbol = choice(all_symbols)
    print("(Symbol: %s)" % symbol, end=" ")
    res = pym._is_symbol(symbol)
    assert res and symbol in existent_symbols

    # Eceptional symbol existent
    symbol = None
    for symbol in pym.exceptional_coin_slugs_keys:
        if symbol in existent_symbols:
            break
    res = pym._is_symbol(symbol)
    assert res

    # Symbol not existent
    res = pym._is_symbol("OUBSAFYAIVADDOHNA")
    assert res  # It's True, see: pym._is_symbol.__doc__

    # Not symbol
    res = pym._is_symbol("ethereum")
    assert not res
