#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" ##########  TESTS CONFIGURATION  ########### """

import os

class ConfigTest:
    """
    Configuration for Pymarketcap tests.
    """
    COIN = 'BTC'
    COIN_NAME = 'bitcoin'
    EXCHANGE = 'poloniex'

    # Tests default directory
    TESTS_DIR = os.path.join(os.path.dirname(__file__), "units")

    # Store results from benchmarking
    BENCH_RESULTS_FILE = os.path.join(os.path.dirname(__file__),
                                      "benchmarking.json")
