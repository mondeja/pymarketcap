# -*- coding: utf-8 -*-

import os
import json
import time
import socket

import pytest

from pymarketcap import Pymarketcap
from pymarketcap.errors import CoinmarketcapHTTPError

def tor_proxy_closed():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock.connect_ex(("127.0.0.1", 9050)) == 1

ON_TRAVIS = os.environ.get("TRAVIS", None) != None
ON_APPVEYOR = os.environ.get("APPVEYOR", None) != None
ON_CI = ON_TRAVIS or ON_APPVEYOR

@pytest.mark.skipif(tor_proxy_closed(),
                    reason="Requires the opening of local Tor proxy (9050).")
@pytest.mark.skipif(ON_CI,
                    reason="Pymarketcap doesn't support Tor browser proxies" \
                          + " inside CI environments.")
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


