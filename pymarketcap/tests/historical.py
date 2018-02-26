#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

class TypeTester:
    def _date(self, value): assert type(value) == datetime
    def _open(self, value): assert type(value) == float
    def _high(self, value): assert type(value) == float
    def _low(self, value): assert type(value) == float
    def _close(self, value): assert type(value) in [float, type(None)]
    def _volume(self, value): assert type(value) == float
    def _market_cap(self, value): assert type(value) == float
    def _name(self, value): assert type(value) == str

tt = TypeTester()

def assert_types(res):
    assert type(res["history"]) == list
    assert type(res["symbol"]) == str
    assert type(res["slug"]) == str
    for tick in res["history"]:
        assert type(tick) == dict
        for key, value in tick.items():
            eval("tt._{}({})".format(
                key,
                value if type(value) != datetime else "value"
            ))