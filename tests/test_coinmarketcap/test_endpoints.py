#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from random import choice
from urllib.request import urlopen
from tqdm import tqdm

import pytest

from pymarketcap import Pymarketcap
from pymarketcap.tests.utils import (
    random_cryptocurrency,
    random_exchange
)
pym = Pymarketcap()

cryptocurrency = random_cryptocurrency(pym)
exchange = random_exchange(pym)["website_slug"]

base_public_api_url = "https://api.coinmarketcap.com/v2/"
base_web_url = "https://coinmarketcap.com/"
base_internal_api_url = "https://s2.coinmarketcap.com/"
base_graphs_api_url = "https://graphs2.coinmarketcap.com/"

endpoints = [
    ("_quick_search",           "%sgenerated/search/quick_search.json" % base_internal_api_url),
    ("_quick_search_exchanges", "%sgenerated/search/quick_search_exchanges.json" % base_internal_api_url),
    ("download_logo",           "%sstatic/img/coins/64x64/1.png" % base_internal_api_url),
    ("download_exchange_logo",  "%sstatic/img/exchanges/64x64/270.png" % base_internal_api_url),

    ("listings",                "%slistings/" % base_public_api_url),
    ("stats",                   "%sglobal/" % base_public_api_url),
    ("ticker",                 ["%sticker/" % base_public_api_url,
                                "%sticker/%s" % (base_public_api_url, cryptocurrency["id"])]),

    ("markets",                 "%scurrencies/%s/" % (base_web_url, cryptocurrency["website_slug"])),
    ("ranks",                   "%sgainers-losers/" % base_web_url),
    ("historical",              "%scurrencies/%s/historical-data/" % (base_web_url, cryptocurrency["website_slug"])),
    ("recently",                "%snew/" % base_web_url),
    ("exchange",                "%sexchanges/%s/" % (base_web_url, exchange)),
    ("exchanges",               "%sexchanges/volume/24-hour/all/" % base_web_url),
    ("tokens",                  "%stokens/views/all/" % base_web_url),

    ("graphs.currency",         "%scurrencies/%s/" % (base_graphs_api_url, cryptocurrency["website_slug"])),
    ("graphs.dominance",        "%sglobal/dominance/" % base_graphs_api_url),
    ("graphs.global_cap",      ["%sglobal/marketcap-total/" % base_graphs_api_url,
                                "%sglobal/marketcap-altcoin/" % base_graphs_api_url]),
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
