# -*- coding: utf-8 -*-
# Copyright (c) 2017 the Pockets team, see AUTHORS.
# Licensed under the BSD License, see LICENSE for details.

"""
An easy to import AutoLogger instance!

>>> import logging, sys
>>> logging.basicConfig(format="%(name)s: %(message)s", stream=sys.stdout)
>>> from pockets.autolog import log
>>> log.error("Always log from the correct module.Class!")
pockets.autolog: Always log from the correct module.Class!

See Also:
    `pockets.logger.AutoLogger`
"""

from __future__ import absolute_import
from pockets.logging import AutoLogger


__all__ = ['log']


log = AutoLogger()
