# -*- coding: utf-8 -*-

"""Constants used by Pymarketcap interfaces."""

import logging
from datetime import datetime

DEFAULT_FORMAT = "%(asctime)s %(levelname)-8s %(name)s:%(lineno)d: %(message)s"
DEFAULT_FORMATTER = logging.Formatter(DEFAULT_FORMAT)
DATETIME_MIN_TIME = datetime.min.time()
DATETIME_MAX_TIME = datetime.max.time()
