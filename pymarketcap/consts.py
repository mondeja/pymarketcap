# -*- coding: utf-8 -*-

import logging

# Parameters
DEFAULT_TIMEOUT = 15

# Data
exceptional_coin_slugs = {
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

exceptional_coin_slugs_keys = list(exceptional_coin_slugs.keys())

# Coins retrieved by cache but not found in coinmarketcap
invalid_coins = [
    "coindash"
]

# Logging

DEFAULT_FORMAT = "%(asctime)s %(levelname)-8s %(name)s:%(lineno)d: %(message)s"
DEFAULT_FORMATTER = logging.Formatter(DEFAULT_FORMAT)
