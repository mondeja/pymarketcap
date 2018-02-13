#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
from random import choice
from urllib.error import HTTPError

import pytest
from tqdm import tqdm

from pymarketcap import Pymarketcap
pym = Pymarketcap()

def teardown_function():
    time.sleep(1)

def test_consistence():
	print("tests/test_scraper/test_download_logo.py::test_consistence")
    for size in tqdm([16, 32, 64, 128, 200]):
        attempts = 5
        _assert = True
        while attempts > 0:
            symbol = choice(pym.symbols)
            tqdm.write("(Currency: %s | Size: %d)" % (symbol, size))
            try:
                res = pym.download_logo(symbol, size=size)
            except HTTPError:
                attempts -= 1
                if attempts == 0:
                    _assert = False
                    break
            else:
                break
        if _assert:
            assert res == "%s_%dx%d.png" % (pym.correspondences[symbol], size, size)
            time.sleep(.5)

            assert os.path.exists(res)
            os.remove(res)
            assert os.path.exists(res) == False

def test_with_filename():
    coin = choice(pym.coins)
    filename = "%s.png" % coin
    res = pym.download_logo(coin, filename=filename)

    assert os.path.exists(res)
    os.remove(res)
    assert os.path.exists(res) == False

def test_invalid():
    # Invalid currencies
    map_coin_errmsg = {
        "OADVDOVASDYIV": "See 'symbols' instance attribute.",
        "aspifhaspfias": "See 'coins' instance attribute."
    }
    for fakecoin, errmsg in map_coin_errmsg.items():
        with pytest.raises(ValueError) as excinfo:
            pym.download_logo(fakecoin)
        assert errmsg in str(excinfo)

    # Invalid size
    size = 250
    with pytest.raises(ValueError) as excinfo:
        pym.download_logo("BTC", size=size)
    assert "%dx%d is not a valid size." % (size, size) in str(excinfo)

    # Valid size that doesn't exist for a currency.
    symbol = "BEST"
    size = 200
    with pytest.raises(ValueError) as excinfo:
        pym.download_logo(symbol, size=size)
    assert "currency doesn't allows to be downloaded with size %dx%d." \
        % (size, size) in str(excinfo)
