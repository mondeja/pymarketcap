#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from subprocess import check_call

import pytest

examples_folder = os.path.join(
	os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
	"examples"
)

def assert_exec(f):
    filepath = os.path.join(examples_folder, f)
    print("Testing example %s" % filepath)
    ret_code = check_call([sys.executable, filepath])
    assert ret_code == 0

def test_basic_api_call():
    assert_exec("basic_api_call.py")

def test_basic_sync_scraper():
    assert_exec("basic_sync_scraper.py")

@pytest.mark.end2end
def test_ticker_pagination():
    assert_exec("ticker_pagination.py")

@pytest.mark.end2end
def test_basic_async_scraper():
    assert_exec("basic_async_scraper.py")

@pytest.mark.end2end
def test_fast_async_scraper():
    assert_exec("fast_async_scraper.py")
