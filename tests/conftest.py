#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import asyncio
import pytest

sys.path.append(os.path.join(os.getcwd(), "pymarketcap"))

def pytest_addoption(parser):
    parser.addoption("--end2end", action="store_true",
                     default=False, help="Run slower tests.")

def pytest_collection_modifyitems(config, items):
    if config.getoption("--end2end"):
        # Run end2end tests
        return
    skip_end2end = pytest.mark.skip(reason="Need --end2end option to run")
    for item in items:
        if "end2end" in item.keywords:
            item.add_marker(skip_end2end)

@pytest.yield_fixture()
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    #loop.close()
    pass


