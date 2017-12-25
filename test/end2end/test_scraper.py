#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard libraries:
import unittest
from decimal import Decimal
from tqdm import tqdm

# External libraries
from requests import get

# Internal modules:
from pymarketcap import Pymarketcap


class TestScraperCoinmarketcapFull(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.coinmarketcap = Pymarketcap()
        self.config = {
            "COIN": 'BTC',
		    "COIN_NAME": 'bitcoin',
		    "EXCHANGE": 'poloniex',
        }

    def test_endpoints(self):

        web_endpoints = [
            "currencies/%s/" % self.config["COIN_NAME"],
            "gainers-losers/",
            "currencies/%s/historical-data/"\
                 % self.config["COIN_NAME"],
            "new",
            "exchanges/%s/" % self.config["EXCHANGE"],
            "exchanges/volume/24-hour/all/"
                    ]

        graphs_api_endpoints = [
            "global/marketcap-altcoin/",
            "global/marketcap-total/",
            "global/dominance/"
        ]

        print("Testing all endpoints schema:")
        for endpoint in web_endpoints + graphs_api_endpoints:
            if endpoint in web_endpoints:
                _url = self.coinmarketcap.web_url + endpoint
            else:
                _url = self.coinmarketcap.graphs_api_url + endpoint
            _status_code = get(_url).status_code
            print(_url)
            self.assertEqual(_status_code, 200)

if __name__ == "__main__":
    unittest.main()
