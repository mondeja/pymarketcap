#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from timeit import timeit
import statistics as st
from datetime import datetime, timedelta

from tqdm import tqdm

basic_setup = "from pymarketcap import Pymarketcap"

common_init = "cmc = Pymarketcap()"
light_init = "cmc = Pymarketcap(cache=False)"

common_setup = "%s;%s" % (basic_setup, common_init)
common_light_setup = "%s;%s" % (basic_setup, light_init)

BENCHS = [
    {"setup": basic_setup, "run": common_init, "name": "__init__"},
    {"setup": common_light_setup, "run": "cmc._cache_symbols()", "name": "_cache_symbols"},
    {"setup": common_light_setup, "run": "cmc.ticker()", "name": "ticker"},
    {"setup": common_setup, "run": "cmc.ticker('BTC')",
        "name": "ticker", "kwargs": dict(currency="BTC")},
    {"setup": common_setup, "run": "cmc.ticker('BTC', convert='EUR')",
        "name": "ticker", "kwargs": dict(currency="BTC", convert="EUR")},
    {"setup": common_light_setup, "run": "cmc.stats()", "name": "stats"},
    {"setup": common_light_setup, "run": "cmc.stats(convert='EUR')",
        "name": "stats", "kwargs": dict(convert="EUR")},
    {"setup": common_setup, "run": "cmc.convert(1, 'USD', 'EUR')", "name": "convert",
        "args": [1, "USD", "EUR"]},
    {"setup": common_setup, "run": "cmc.markets('BTC')", "name": "markets", "args": ["BTC"]},
    {"setup": common_light_setup, "run": "cmc.ranks()", "name": "ranks"},
    {"setup": common_setup, "run": "cmc.historical('BTC')", "name": "historical",
        "args": ["BTC"]},
    {"setup": common_setup, "run": "cmc.historical('BTC', revert=True)",
        "name": "historical", "args": ["BTC"], "kwargs": dict(revert=True)},
    {"setup": "%s;from datetime import datetime, timedelta;" % common_setup \
        + "START=datetime.now()-timedelta(days=30)",
        "run": "cmc.historical('BTC', start=START)",
        "name": "historical", "args": ["BTC"],
        "kwargs": dict(start=datetime.now()-timedelta(days=30))},
    {"setup": common_light_setup, "run": "cmc.recently()", "name": "recently"},
    {"setup": common_light_setup, "run": "cmc.exchange('bittrex')", "name": "exchange",
        "args": ["bittrex"]},
    {"setup": common_light_setup, "run": "cmc.exchanges()", "name": "exchanges"},
    {"setup": common_light_setup, "run": "cmc.tokens()", "name": "tokens"},
    {"setup": common_setup, "run": "cmc.graphs.currency('BTC')", "name": "graphs.currency",
        "args": ["BTC"]},
    {"setup": common_light_setup, "run": "cmc.graphs.global_cap()", "name": "graphs.global_cap"},
    {"setup": common_light_setup, "run": "cmc.graphs.dominance()", "name": "graphs.dominance"}
]

REPEAT_EACH_BENCH = 5
TEARDOWN_TIME_SLEEP = 1

# Basic manual benchs filtering
START_BENCHING_AT = 0
RUN_ONLY = False #[]

def show_bench_results(name, chunks, setup, run_exec, params):
    mean = float(st.mean(chunks))
    median = float(st.median(chunks))
    stdev = float(st.pstdev(chunks, mean))
    print("\nNAME: %s" % name)
    if params["args"]:
      	print("\tARGS: %s" % params["args"])
    if params["kwargs"]:
       	print("\tKWARGS: %s" \
       		% {"%s=%s" % (str(key), str(value)) for key, value in params["kwargs"].items()})
    print("\nSETUP: %s\nRUN: %7s\n" % (setup, run_exec))
    print("TIME SPENT (in sec)\n\tMean: %f\n\tMedian: %f\n\tStdev: %f\n" % (mean, median, stdev))
    print("\tLowest: %f\n\tFastest: %f\n" % (max(chunks), min(chunks)))


def run_benchmarks():
    sep = "="*20
    print("\n%s Running pymarketcap benchmarking suite %s\n" % (sep, sep))

    for i, bench in enumerate(BENCHS[START_BENCHING_AT:]):
        if RUN_ONLY:
            if bench["name"] not in RUN_ONLY:
                continue
        if i > 0:
        	print("%s \n" % ("_"*100))
        chunks = []
        for i in tqdm(range(REPEAT_EACH_BENCH)):
            if i == 0:
            	tqdm.write("%s;%s" % (bench["setup"], bench["run"]))
            chunks.append(
            	timeit(bench["run"], bench["setup"], number=1)
            )
            sleep(TEARDOWN_TIME_SLEEP)
        params = {"args": bench.get("args", None),
                  "kwargs": bench.get("kwargs", None)}

        show_bench_results(bench["name"], chunks, bench["setup"], bench["run"], params)

    print("\n%s Pymarketcap benchmarking suite ended %s\n" % (sep, sep))

if __name__ == "__main__":
    run_benchmarks()
