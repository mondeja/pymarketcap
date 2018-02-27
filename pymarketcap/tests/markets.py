#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class TypeTester:
    def _source(self, value): assert type(value) == str
    def _pair(self, value): assert type(value) == str
    def _volume_24h(self, value): assert type(value) == float
    def _price(self, value): assert type(value) == float
    def _percent_volume(self, value): assert type(value) == float
    def _updated(self, value): assert type(value) == bool


tt = TypeTester()

def assert_types(res):
    assert type(res["markets"]) == list
    assert type(res["symbol"]) == str
    assert type(res["slug"]) == str
    for source in res["markets"]:
        assert type(source) == dict
        for key, value in source.items():
            eval("tt._{}({})".format(
                    key,  # Strings need to be "quoted":
                    value if type(value) != str else '"%s"' % value
                ))

def assert_consistence(res):
    for i, source in enumerate(res["markets"]):
        assert len(source.keys()) == 6
        slash_count = 0
        assert source["pair"].count("/") == 1
        assert source["percent_volume"] <= 100

