#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
from random import choice

import pytest
from tqdm import tqdm

from pymarketcap import Pymarketcap
pym = Pymarketcap()

def teardown_function():
    time.sleep(1)

def test_consistence():
    print("\nTesting download_logo sizes...\n")
    for size in tqdm([16, 32, 64, 128, 200]):
        symbol = choice(pym.symbols)
        tqdm.write("(Currency: %s | Size: %d)" % (symbol, size))
        res = pym.download_logo(symbol, size=size)
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
    map_coin_errmsg = {
        "OADVDOVASDYIV": "See 'symbols' instance attribute.",
        "aspifhaspfias": "See 'coins' instance attribute."
    }
    for fakecoin, errmsg in map_coin_errmsg.items():
        with pytest.raises(ValueError) as excinfo:
            pym.download_logo(fakecoin)
        assert errmsg in str(excinfo)
