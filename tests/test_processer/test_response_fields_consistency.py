#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pprint import pprint

from tqdm import tqdm

from pymarketcap.tests.utils import (
    random_cryptocurrency,
    random_exchange
)
from pymarketcap import Pymarketcap
pym = Pymarketcap()

METHODS = [
    ["exchanges"],
    ["exchange", random_exchange(pym)["website_slug"]],
    ["currency", random_cryptocurrency(pym)["website_slug"]],
    ["markets", random_cryptocurrency(pym)["website_slug"]],
    ["ranks"],
    ["recently"],
    ["tokens"],
    ["graphs.currency", random_cryptocurrency(pym)["website_slug"]],
    ["graphs.global_cap"],
    ["graphs.dominance"]
]

def test_fields():
    keys = []
    keys_method_map = {}
    for method in tqdm(METHODS, desc="Testing all response names consistency"):
        _exec = "pym.%s(%s)" % (method[0], '"%s"' % method[1] if len(method) == 2 else "")
        tqdm.write(_exec)
        try:
            res = eval(_exec)
        except IndexError:
            continue

        attempts = 5
        while attempts > 0:
            try:
                if method[0] == "ranks":
                    keys_from_method = list(res["gainers"]["1h"][0].keys())
                    keys.extend(keys_from_method)
                elif method[0] == "markets":
                    keys_from_method = list(res["markets"][0].keys())
                    keys.extend(keys_from_method)
                elif method[0] in ["currency", "stats",
                                   "graphs.currency",
                                   "graphs.global_cap",
                                   "graphs.dominance"]:
                    keys_from_method = list(res.keys())
                    keys.extend(keys_from_method)
                elif method[0] == "exchange":
                    keys_from_method = list(res.keys())
                    keys_from_method.extend(list(res["markets"][0].keys()))
                    keys.extend(keys_from_method)
                elif method[0] == "exchanges":
                    keys_from_method = list(res[0]["markets"][0].keys())
                    keys.extend(keys_from_method)
                elif method[0] in ["ticker", "tokens", "recently"]:
                    keys_from_method = list(res[0].keys())
                    keys.extend(keys_from_method)
                else:
                    tqdm.write("\nWARNING: Method %s() not tested" % method[0])
                    tqdm.write("RESPONSE: %r\n" % res)
            except Exception as err:
                tqdm.write(str(err))
                attempts -= 1
            else:
                for key in keys_from_method:
                    keys_method_map[key] = method[0]
                break

    # If you want to know from what method is every field,
    # insert it here and run the test:
    stops = [
        "website",
        "total_markets_cap",
        "total_markets_volume_24h"
    ]

    # Useful for maintainance
    #print(set(keys))

    for key in set(keys):
        if key in stops:
            msg = 'Key "%s" from method %s() not allowed.' % (key, keys_method_map[key])
            raise AssertionError(msg)
