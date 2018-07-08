#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from time import sleep
from timeit import timeit
import statistics as st
from datetime import date, datetime, timedelta
import argparse
from decimal import Decimal

from tqdm import tqdm
from tabulate import tabulate

REPEAT_EACH_BENCH = 5
TEARDOWN_TIME_SLEEP = .7

# Basic manual benchs filtering
START_BENCHING_AT = 0
RUN_ONLY = False #[]

# Basic configuration for results file
RESULTS_FILE = os.path.join("bench", "last_results.json")
SAVE_RESULTS = True
LAST_RESULTS_FILE = RESULTS_FILE
LAST_RESULTS = None

# ============================================================
#                    BENCHMARKING SUITE                      #

basic_setup = "from pymarketcap import Pymarketcap"

common_init = light_init = "cmc = Pymarketcap()"

common_setup = "%s;%s" % (basic_setup, common_init)
common_light_setup = "%s;%s" % (basic_setup, light_init)

BENCHS = [
    {"setup": basic_setup, "run": common_init, "name": "__init__"},
    # Deprecated in version 4.0.0
    # {"setup": common_light_setup, "run": "cmc._cache_symbols_ids()", "name": "_cache_symbols"},
    {"setup": common_light_setup, "run": "cmc.ticker()", "name": "ticker"},
    #{"setup": common_setup, "run": "cmc.ticker('STEEM', convert='EUR')",
    #    "name": "ticker", "kwargs": dict(currency="STEEM", convert="EUR")},
    {"setup": common_light_setup, "run": "cmc.stats()", "name": "stats"},
    {"setup": common_light_setup, "run": "cmc.stats(convert='EUR')",
        "name": "stats", "kwargs": dict(convert="EUR")},
    {"setup": common_setup, "run": "cmc.convert(1, 'USD', 'EUR')", "name": "convert",
        "args": [1, "USD", "EUR"]},
    {"setup": common_setup, "run": "cmc.currency('BTC')", "name": "currency", "args": ["BTC"]},
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

# ============================================================

def show_bench_results(name, stats, setup, run_exec, params):
    print("\nNAME: %s" % name)
    if params["args"]:
          print("\tARGS: %s" % params["args"])
    if params["kwargs"]:
           print("\tKWARGS: %s" \
               % {"%s=%s" % (str(key), str(value)) for key, value in params["kwargs"].items()})
    print("\nSETUP: %s\nRUN: %7s\n" % (setup, run_exec))

    print("TIME SPENT (in sec):\n")

    table = [[key.capitalize(), value] for key, value in stats.items()]
    headers = ["Ind", "Actual"]

    if LAST_RESULTS:
        for last_bench in LAST_RESULTS["benchs"]:
            if last_bench["name"] == name and \
              last_bench.get("args", None) == params["args"] and \
              last_bench.get("kwargs", None) == params["kwargs"]:
                headers.append("Last")
                for row in table:
                    for key, value in last_bench["stats"].items():
                        if row[0].lower() == key:
                            row.append(value)
                break

    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


def run_benchmarks():
    sep = "="*20
    print("\n%s Running pymarketcap benchmarking suite %s\n" % (sep, sep))

    # Save all results
    results = {"date": str(datetime.now()),
               "benchs": [],
               "repeat": REPEAT_EACH_BENCH}

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
        stats = {"mean": st.mean(chunks),
                 "median": st.median(chunks),
                 "stdev": st.stdev(chunks),
                 "slowest": max(chunks),
                 "fastest": min(chunks)}

        show_bench_results(bench["name"], stats, bench["setup"], bench["run"], params)
        bench.update({"stats": stats})
        results["benchs"].append(bench)

    print("\n%s Pymarketcap benchmarking suite ended %s\n" % (sep, sep))

    def json_serial(obj):
        """JSON serializer for datetime objects"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()

    if SAVE_RESULTS:
        with open(RESULTS_FILE, "w") as f:
            f.write(json.dumps(results, indent=4, default=json_serial))

def argparsing():
    parser = argparse.ArgumentParser(description="Pymarketcap benchmarking suite")
    parser.add_argument("--benchs", "-b",
        help="Filter by benchs names. You can pass various names with comma separated format.")
    parser.add_argument("--number", "-n", type=int,
        help="Set number of repetitions in each benchmark to calculate statistics." \
             + "The minimum posible value is 2.")
    parser.add_argument("--save", "-s", help="Set filepath for save benchmarking results.")
    parser.add_argument("--compare", "-c",
        help="Set previous filepath results file for compare against actual benchmarking results."
    )
    args = parser.parse_args()
    if args.benchs:
        global RUN_ONLY
        RUN_ONLY = args.benchs.split(",")
    if args.number:
        global REPEAT_EACH_BENCH
        n = args.number if args.number > 1 else 2
        REPEAT_EACH_BENCH = n

    if args.save:
        global RESULTS_FILE
        if args.save != "None":
            RESULTS_FILE = args.save
        else:
            RESULTS_FILE = None

    if args.compare:
        global LAST_RESULTS_FILE
        if os.path.exists(args.compare):
            LAST_RESULTS_FILE = args.compare
        else:
            raise FileNotFoundError(args.compare)
    return None

def file_prepare_results():
    global SAVE_RESULTS
    SAVE_RESULTS = True
    global RESULTS_FILE
    if not RESULTS_FILE:
        if not os.path.exists("bench"):
            os.chdir("..")
            if not os.path.exists("bench"):
                print("You need to stay at pymarketcap tree folder root " \
                      + "in order to save benchmarking results as a file.")
                SAVE_RESULTS = False
    else:
        if not os.path.exists(RESULTS_FILE):
            f = open(RESULTS_FILE, "w")
            f.close()

    global LAST_RESULTS_FILE
    global LAST_RESULTS
    if os.path.exists(LAST_RESULTS_FILE):
        try:
            with open(LAST_RESULTS_FILE, "r") as f:
                LAST_RESULTS = json.loads(f.read())
        except json.decoder.JSONDecodeError:
            LAST_RESULTS = None


if __name__ == "__main__":
    argparsing()
    file_prepare_results()
    run_benchmarks()
