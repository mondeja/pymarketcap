#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from json import loads

from precompiler.utils import GET

def get_badges_list():
    """Get list of convertible badges from coinmarketcap documentation"""
    url = "https://coinmarketcap.com/api/"
    res = GET(url).decode()
    raw_badges = re.search(r"Valid values are: <br>\s*(.*)\s*</li>", res)
    return sorted(loads("[%s]" % raw_badges.group(1)))

def get_currency_exchange_rates_list():
    url = "https://coinmarketcap.com/"
    res = GET(url).decode()
    currencies = re.findall(r'data-(\w+)="\d+\.*[\d|e|-]*"', res[-4000:-2000])
    return sorted([currency.upper() for currency in currencies])
