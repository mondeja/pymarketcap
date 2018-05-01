#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from json import loads

from precompiler.utils import GET

def get_badges_list():
    """Get list of convertible badges from coinmarketcap documentation"""
    url = "https://coinmarketcap.com/api/"
    res = GET(url).decode()
    #print(res)
    fiat_currs = re.search(r"Valid fiat currency values are:\s*(.*)\s*<br>", res)
    response = loads("[%s]" % fiat_currs.group(1))
    crypto_currs_raw = re.search(r"Valid cryptocurrency values are:\s*(.*)\s*</li>", res)
    crypto_currs = loads("[%s]" \
        % crypto_currs_raw.group(1).replace(" and", "").replace('" ', '", '))
    response.extend(crypto_currs)
    response.append("USD")
    return sorted(response)
