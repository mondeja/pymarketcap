# -*- coding: utf-8 -*-

"""Constants used by Pymarketcap interfaces."""

import logging

# Parameters
DEFAULT_TIMEOUT = 15

# Data
EXCEPTIONAL_COIN_SLUGS = {
    "42": "42-coin",
    "808": "808coin",
    "611": "sixeleven",
    "300": "300-token",
    "888": "octocoin",
    "$$$": "money",
    "BTBc": "bitbase",
    "1337": "1337coin",
    "AMMO": "ammo-reloaded",
    "BTW": "bitwhite"
}

EXCEPTIONAL_COIN_SLUGS_KEYS = list(EXCEPTIONAL_COIN_SLUGS.keys())

# Coins retrieved by cache but not found in coinmarketcap
INVALID_COINS = [
    "coindash"
]

# Logging

DEFAULT_FORMAT = "%(asctime)s %(levelname)-8s %(name)s:%(lineno)d: %(message)s"
DEFAULT_FORMATTER = logging.Formatter(DEFAULT_FORMAT)
