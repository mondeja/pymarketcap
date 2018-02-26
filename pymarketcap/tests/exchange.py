#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class TypeTester:
    def _currency(self, value): assert type(value) == str
    def _pair(self, value): assert type(value) == str
    def _vol_24h(self, value): assert type(value) in [float, type(None)]
    def _price(self, value): assert type(value) == float
    def _perc_volume(self, value): assert type(value) == float
    def _updated(self, value): assert type(value) == bool
    def _name(self, value): assert type(value) == str

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