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
    response = loads("[%s]" % raw_badges.group(1))
    response.append("USD")
    return sorted(response)
