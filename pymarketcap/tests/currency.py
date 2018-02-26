#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class TypeTester:
    def _source_code(self, value): assert type(value) in [str, type(None)]
    def _announcement(self, value): assert type(value) in [str, type(None)]
    def _explorers(self, value): assert type(value) == list
    def _total_markets_volume_24h(self, value): assert type(value) in [float, type(None)]
    def _price(self, value): assert type(value) in [float, type(None)]
    def _rank(self, value): assert type(value) == int
    def _total_markets_cap(self, value): assert type(value) in [float, type(None)]
    def _chats(self, value): assert type(value) == list
    def _message_boards(self, value): assert type(value) == list
    def _circulating_supply(self, value): assert type(value) in [float, type(None)]
    def _total_supply(self, value): assert type(value) in [float, type(None)]
    def _max_supply(self, value): assert type(value) in [float, type(None)]
    def _mineable(self, value): assert type(value) == bool
    def _webs(self, value): assert type(value) == list
    def _name(self, value): assert type(value) == str

tt = TypeTester()

def assert_types(res):
    assert type(res) == dict
    for key, value in res.items():
        eval("tt._{}({})".format(
            key,
            value if type(value) != str else '"%s"' % value
        ))

