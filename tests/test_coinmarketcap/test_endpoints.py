#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from random import choice
from urllib.request import urlopen
from tqdm import tqdm

import pytest

from pymarketcap import Pymarketcap
pym = Pymarketcap()

coin = choice(pym.coins)
exchange = choice(pym.exchange_slugs)

endpoints = [
    ("_cache_symbols_ids",     "https://s2.coinmarketcap.com/generated/search/quick_search.json"),
    ("_exchange_names_slugs",  "https://s2.coinmarketcap.com/generated/search/quick_search_exchanges.json"),
    ("ticker",                ["https://api.coinmarketcap.com/v1/ticker/",
                               "https://api.coinmarketcap.com/v1/ticker/%s" % coin]),
    ("markets",                "https://coinmarketcap.com/currencies/%s/" % coin),
    ("ranks",                  "https://coinmarketcap.com/gainers-losers/"),
    ("historical",             "https://coinmarketcap.com/currencies/%s/historical-data/" % coin),
    ("recently",               "https://coinmarketcap.com/new/"),
    ("exchange",               "https://coinmarketcap.com/exchanges/%s/" % exchange),
    ("exchanges",              "https://coinmarketcap.com/exchanges/volume/24-hour/all/"),
    ("tokens",                 "https://coinmarketcap.com/tokens/views/all/"),
    ("graphs.currency",        "https://graphs2.coinmarketcap.com/currencies/%s/" % coin),
    ("graphs.global_cap",     ["https://graphs2.coinmarketcap.com/global/marketcap-total/",
                               "https://graphs2.coinmarketcap.com/global/marketcap-altcoin/"]),
    ("graphs.dominance",       "https://graphs2.coinmarketcap.com/global/dominance/"),
    ("download_logo",          "https://s2.coinmarketcap.com/static/img/coins/64x64/1.png"),
    ("download_exchange_logo", "https://s2.coinmarketcap.com/static/img/coins/64x64/1.png")
]

def assert_up(ep):
    req = urlopen(ep)
    assert req.getcode() != 404
    req.close()

@pytest.mark.end2end
def test_endpoints():
    for i, (method, eps) in enumerate(tqdm(endpoints)):
        if i == 0:
            tqdm.write("tests/test_endpoints.py::test_endpoints")
        if type(eps) != list:
            eps = [eps]
        for ep in eps:
            tqdm.write("%23s() --> %s" % (method, ep))
            assert_up(ep)
            sleep(.1)
