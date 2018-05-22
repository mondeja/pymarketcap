# -*- coding: utf-8 -*-

"""Pymarketcap source code."""

import sys

__title__ = "pymarketcap"
__version__ = "4.0.009"
__version_info__ = (int(num) for num in __version__.split("."))
__author__ = "Álvaro Mondéjar Rubio <mondejar1994@gmail.com>"
__repo__ = "https://github.com/mondeja/pymarketcap"
__license__ = "BSD License"

from pymarketcap.core import Pymarketcap
from pymarketcap.errors import (
    CoinmarketcapError,
    CoinmarketcapHTTPError,
    CoinmarketcapTooManyRequestsError
)
if sys.version_info >= (3, 6):
    from pymarketcap.pymasyncore import AsyncPymarketcap
