#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

def pytest_addoption(parser):
    parser.addoption("--end2end", action="store_true",
                     default=False, help="Run slower tests.")

def pytest_collection_modifyitems(config, items):
    if config.getoption("--end2end"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_end2end = pytest.mark.skip(reason="Need --end2end option to run")
    for item in items:
        if "end2end" in item.keywords:
            item.add_marker(skip_end2end)
