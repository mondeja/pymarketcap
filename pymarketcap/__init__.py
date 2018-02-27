# -*- coding: utf-8 -*-

"""Pymarketcap source code."""

import sys

__title__ = "pymarketcap"
__version__ = "3.9.119"
__author__ = "Alvaro Mondejar Rubio <mondejar1994@gmail.com>"
__repo__ = "https://github.com/mondeja/pymarketcap"
__license__ = "BSD License"

from .core import Pymarketcap
from .errors import (
    CoinmarketcapError,
    CoinmarketcapHTTPError,
    CoinmarketcapTooManyRequestsError
)
if sys.version_info >= (3,6):
    from .pymasyncore import AsyncPymarketcap
