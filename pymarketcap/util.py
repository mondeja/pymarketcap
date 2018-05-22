# -*- coding: utf-8 -*-

"""Pymarketcap utilities module."""

# Standard python modules
import sys
import time
from datetime import datetime


def get_timestamp(dt):
    if not isinstance(dt, datetime):
        raise ValueError('Argument `dt` must be is instance `datetime`')

    if sys.version_info < (3, 3):
        return time.mktime(dt.timetuple()) + dt.microsecond / 1000000.
    return dt.timestamp()


def cmc_timestamp(dt):
    return int(get_timestamp(dt) * 1000)
