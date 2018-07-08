# -*- coding: utf-8 -*-

from random import choice
from pymarketcap.tests import restart_if_http_error

def random_cryptocurrency(instance=None):
    if not instance:
        from pymarketcap import Pymarketcap
        return choice(Pymarketcap().cryptocurrencies)
    else:
        return choice(instance.cryptocurrencies)

def random_exchange(instance=None):
    if not instance:
        from pymarketcap import Pymarketcap
        return choice(Pymarketcap().cryptoexchanges)
    else:
        return choice(instance.cryptoexchanges)
