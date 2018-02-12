#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from pymarketcap import Pymarketcap
pym = Pymarketcap(cache=False)

def teardown_function():
    time.sleep(1)

class TypeTester:
    def _name(self, value): assert type(value) == str
    def _symbol(self, value): assert type(value) == str
    def _volume_24h(self, value): assert type(value) == float
    def _price(self, value): assert type(value) == float
    def _percent_change(self, value): assert type(value) == float


tt = TypeTester()

def _test_data_structure_types(data):
    assert type(data) == dict
    for rank, rdata in data.items():
        assert type(rank) == str
        assert type(rdata) == dict
        for period, pdata in rdata.items():
            assert type(period) == str
            assert type(pdata) == list
            for currency in pdata:
                assert type(currency) == dict
                for key, value in currency.items():
                    eval("tt._{}({})".format(
                        key,  # Strings need to be "quoted":
                        value if type(value) != str else '"%s"' % value
                    ))

def test_types():
    _test_data_structure_types(pym.ranks())

def _test_currencies_order(data):
    # Assert if currencies are in order
    for rank, rdata in data.items():
        for period, pdata in rdata.items():
            for i, currency in enumerate(pdata):
                if i < len(pdata)-1:
                    assert pdata[i+1]["percent_change"] >= currency["percent_change"]

def test_consistence():
    _test_currencies_order(pym.ranks())


def test_convert():
    res_btc = pym.ranks(convert="BTC")

    # Test types
    _test_data_structure_types(res_btc)

    # Test consistence
    _test_currencies_order(res_btc)
