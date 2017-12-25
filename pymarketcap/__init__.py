#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Pymarketcap source"""

__title__ = "pymarketcap"
__version__ = "3.3.126"
__author__ = "Alvaro Mondejar Rubio <mondejar1994@gmail.com>"
__repo__ = "https://github.com/mondeja/pymarketcap"
__license__ = "BSD License"

from .core import Pymarketcap
from .errors import (
    CoinmarketcapError,
    CoinmarketcapHTTPError,
    CoinmarketcapCurrencyNotFoundError
)
