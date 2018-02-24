#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import choice
from urllib.request import urlopen
from re import findall as re_findall

from pymarketcap import Pymarketcap
pym = Pymarketcap()

class TypeTester:
    def _source(self, value): assert type(value) == str
    def _pair(self, value): assert type(value) == str
    def _volume_24h(self, value): assert type(value) == float
    def _price(self, value): assert type(value) == float
    def _percent_volume(self, value): assert type(value) == float
    def _updated(self, value): assert type(value) == bool

tt = TypeTester()

def assert_types(res):
    assert type(res) == list
    for source in res:
        assert type(source) == dict
        for key, value in source.items():
            eval("tt._{}({})".format(
                    key,  # Strings need to be "quoted":
                    value if type(value) != str else '"%s"' % value
                ))

def assert_number_of_markets(res, coin_slug):
    req = urlopen("https://coinmarketcap.com/currencies/%s/" % coin_slug)
    data = req.read()
    req.close()
    indexes = re_findall(r'<td class="text-right">(.+)</td>', data.decode())
    assert len(res) == int(indexes[-1])

def assert_consistence(res, coin_slug):
    for i, source in enumerate(res):
        assert len(source.keys()) == 6
        slash_count = 0
        assert source["pair"].count("/") == 1
        assert source["percent_volume"] <= 100

    assert_number_of_markets(res, coin_slug)

def test_without_convert():
    coin = choice(pym.coins)
    print("(Currency: %s)" % coin, end=" ")
    res = pym.markets(coin)
    assert_types(res)
    assert_consistence(res, coin)

def test_with_convert():
    coin = choice(pym.coins)
    print("(Currency: %s)" % coin, end=" ")
    res = pym.markets(coin, convert="BTC")
    assert_types(res)
    assert_consistence(res, coin)
