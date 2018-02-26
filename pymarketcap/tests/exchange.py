#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from re import findall
from urllib.request import urlopen

class TypeTester:
    def _currency(self, value): assert type(value) == str
    def _pair(self, value): assert type(value) == str
    def _vol_24h(self, value): assert type(value) in [float, type(None)]
    def _price(self, value): assert type(value) == float
    def _perc_volume(self, value): assert type(value) == float
    def _updated(self, value): assert type(value) == bool
    def _name(self, value): assert type(value) == str
    def _slug(self, value): assert type(value) == str

tt = TypeTester()

def assert_types(res):
    assert type(res) == dict

    assert type(res["name"]) == str
    assert type(res["website"]) == str
    assert type(res["volume"]) in [float, type(None)]
    assert type(res["social"]) == dict

    for key, fields in res["social"].items():
        assert type(key) == str
        for field, data in fields.items():
            assert type(field) == str
            assert type(data) in [str, type(None)]

    for market in res["markets"]:
        assert type(market) == dict
        for key, value in market.items():
            eval("tt._{}({})".format(
                key,
                value if type(value) != str else '"%s"' % value
            ))

def assert_number_of_markets(res):
    req = urlopen("https://coinmarketcap.com/exchanges/%s/" % res["slug"])
    data = req.read()
    req.close()
    indexes = findall(r'<td class="text-right">(\d+)</td>', data.decode())
    assert len(res["markets"]) == int(indexes[-1])

def assert_consistence(res):
    assert len(res["name"]) > 0
    assert res["name"] != None
    assert len(res["website"]) > 0
    assert res["website"] != None
    assert_number_of_markets(res)
