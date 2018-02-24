#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import choice

from pymarketcap import Pymarketcap
pym = Pymarketcap()

class TypeTester:
    def _source_code(self, value): assert type(value) in [str, type(None)]
    def _announcement(self, value): assert type(value) in [str, type(None)]
    def _explorers(self, value): assert type(value) == list
    def _total_markets_volume_24h(self, value): assert type(value) in [float, type(None)]
    def _price(self, value): assert type(value) == float
    def _rank(self, value): assert type(value) == int
    def _total_markets_cap(self, value): assert type(value) in [float, type(None)]
    def _chats(self, value): assert type(value) == list
    def _message_boards(self, value): assert type(value) == list
    def _circulating_supply(self, value): assert type(value) in [float, type(None)]
    def _total_supply(self, value): assert type(value) in [float, type(None)]
    def _max_supply(self, value): assert type(value) in [float, type(None)]
    def _mineable(self, value): assert type(value) == bool
    def _webs(self, value): assert type(value) == list

tt = TypeTester()

def assert_types(res):
    assert type(res) == dict
    for key, value in res.items():
        eval("tt._{}({})".format(
            key,
            value if type(value) != str else '"%s"' % value
        ))

def test_types():
    symbol = choice(pym.symbols)
    print("(Currency: %s)" % symbol, end=" ")
    res = pym.currency(symbol)
    assert_types(res)

def assert_consistence(res):
    assert res["price"] != None
    assert len(list(res.keys())) in list(range(12, 15))

def test_consistence():
    symbol = choice(pym.symbols)
    print("(Currency: %s)" % symbol, end=" ")
    res = pym.currency(symbol)
    assert_consistence(res)

def test_convert():
    symbol = choice(pym.symbols)
    print("(Currency: %s)" % symbol, end=" ")
    res = pym.currency(symbol, convert="BTC")

    assert_types(res)
    assert_consistence(res)
