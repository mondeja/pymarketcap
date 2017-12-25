#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Run:
# All tests benchmarking:
#     python3 test.py --with-timer -v
# Only API tests without benchmarking:
#     nosetests units/test_api.py -v

# Standard libraries
import sys
import os
import json

# External libraries
import nose
from nosetimer import plugin

# Internal modules
from config import ConfigTest


def configure_plugins():
    """Configure nose plugins"""
    def conf_timer():
        timer = plugin.TimerPlugin()
        timer.enabled = True
        timer.timer_ok = 1000
        timer.timer_warning = 2000
        timer.timer_no_color = False
        return timer

    return {
        "timer": conf_timer(),
    }

def run_tests(plugins, config):
    """Run nosetests"""
    nose.run(plugins=plugins.values(),
             defaultTest=config.TESTS_DIR)
    return plugins["timer"]._timed_tests  # Benchmarking results

def save_benchs(results, config):
    """Store benchmarking results"""
    with open(config.BENCH_RESULTS_FILE, "a") as benchs:
        benchs.write("\n%s\n" % str(results))

def main():
    """Run nosetests with timr plugin and store
    benchmarking results in a JSON file"""
    config = ConfigTest()
    results = run_tests(configure_plugins(), config)
    errors = False
    for test_name, result in results.items():
        if result["status"] == "error":
            errors = True
            break

    if not errors:
        save_benchs(json.dumps(results, indent=4, sort_keys=True),
                    config)
        return sys.exit(0)
    return sys.exit(1)



if __name__ == "__main__":
    main()
