#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from re import findall as re_findall
from urllib.request import urlopen

from pymarketcap import Pymarketcap
pym = Pymarketcap()

class TypeTester:
    def _name(self, value): assert type(value) == str
    def _symbol(self, value): assert type(value) == str
    def _platform(self, value): assert type(value) in [str, type(None)]
    def _market_cap(self, value): assert type(value) in [float, type(None)]
    def _price(self, value): assert type(value) in [float, type(None)]
    def _circulating_supply(self, value): assert type(value) in [float, type(None)]
    def _volume_24h(self, value): assert type(value) in [float, type(None)]

tt = TypeTester()

def assert_types(res):
    for currency in res:
        for key, value in currency.items():
            eval("tt._{}({})".format(
                key,  # Strings need to be "quoted":
                value if type(value) != str else '"%s"' % value
            ))

def test_types():
    res = pym.tokens()
    assert_types(res)

def assert_number_of_tokens(res):
    req = urlopen("https://coinmarketcap.com/tokens/views/all/")
    data = req.read()
    req.close()
    indexes = int(
        re_findall(r'<td class="text-center">\n(\d+)\n</td>', data.decode())[-1]
    )
    assert len(res) in [indexes-1, indexes, indexes+1]

def test_consistence():
    res = pym.tokens()
    assert_number_of_tokens(res)
