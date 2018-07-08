# -*- coding: utf-8 -*-

import json
import time

from pymarketcap import Pymarketcap
from pymarketcap.errors import CoinmarketcapHTTPError

def test_proxy():
    HTTPerror = True
    attempts = 10

    while HTTPerror and attempts > 0:
        # First, check exposed IP without proxy
        try:
            pym_no_proxy = Pymarketcap()
        
            ip_url = b"http://httpbin.org/ip"
        
            response = pym_no_proxy._get(ip_url)
            original_ip = json.loads(response)["origin"]
        
            # Second, check exposed IP using Tor proxy
            # You need to install Tor
            pym_proxy = Pymarketcap(proxy_addr=b"socks5://127.0.0.1:9050")
            response = pym_proxy._get(ip_url)
        
            masked_ip = json.loads(response)["origin"]
        except CoinmarketcapHTTPError as err:
        	attempts -= 1
        	time.sleep(2)
        else:
        	HTTPerror = False

    if not HTTPerror:
        assert original_ip != masked_ip
        return
    print("Max attempts reached retrieving IP from: %s" % str(ip_url))
    raise err


