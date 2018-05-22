
"""This module process all core scraper methods raw responses."""

# Standard Python modules
import re
from datetime import datetime, date

from pymarketcap.consts import DATETIME_MIN_TIME, DATETIME_MAX_TIME
# RegEx parsing
PAIRS_REGEX = "[\s\$@\w\.]+/[\s\$@\w\.]+"

cpdef currency(res, convert):
    if convert == "usd":
        _total_markets_cap = re.search(
            r'data-currency-market-cap.+data-usd="(\?|\d+\.*\d*e*[-|+]*\d*)"', res
        )
        _total_markets_volume = re.search(
            r'data-currency-volume.+data-usd="(\?|\d+\.*\d*e*[-|+]*\d*)"', res
        )
        _price = re.search(r'quote_price.+data-usd="(\?|\d+\.*\d*e*[-|+]*\d*)"', res)
    else:  # convert == "btc"
        _total_markets_cap = re.search(
            r'data-format-market-cap.+data-format-value="(\?|\d+\.*\d*e*[-|+]*\d*)"', res
        )
        _total_markets_volume = re.search(
            r'data-format-volume-crypto.+data-format-value="(\?|\d+\.*\d*e*[-|+]*\d*)"', res
        )
        _price = re.search(
            r'data-format-price-crypto.+data-format-value="(\?|\d+\.*\d*e*[-|+]*\d*)"', res
        )

    vol_24h = _total_markets_volume.group(1)
    try:
        vol_24h = _total_markets_volume.group(1)
        vol_24h = float(vol_24h)
    except AttributeError:
        vol_24h = None
    except ValueError:
        if vol_24h != "?":
            raise
        vol_24h = None
    try:
        total_cap = _total_markets_cap.group(1)
        total_cap = float(total_cap)
    except AttributeError:
        total_cap = None
    except ValueError:
        if total_cap != "?":
            raise
        total_cap = None
    try:
        price = _price.group(1)
        price = float(price)
    except AttributeError:
        price = None
    except ValueError:
        if price != "?":
            raise
        price = None

    response = {
        "markets_cap": total_cap,
        "markets_volume_24h": vol_24h,
        "price": price
    }

    # Circulating, maximum and total supply
    supply = re.findall(
        r'data-format-supply.+data-format-value="(\?|\d+\.*\d*e*[-|+]*\d*)"', res
    )

    response["circulating_supply"] = float(supply[0]) if supply[0] != "?" else None
    if len(supply) > 1:
        response["max_supply"] = float(supply[-1])
    else:
        response["max_supply"] = None
    if len(supply) > 2:
        response["total_supply"] = float(supply[1])
    else:
        response["total_supply"] = None

    response["webs"] = re.findall(r'<a href="(.+)" target="_blank".*>Website\s*\d*</a>', res)

    response["explorers"] = re.findall(
        r'<a href="(.+)" target="_blank.*">Explorer\s*\d*</a>', res
    )

    source_code = re.search(r'<a href="(.+)" target="_blank".*>Source Code</a>', res)
    response["source_code"] = source_code.group(1) if source_code else None

    response["message_boards"] = re.findall(
        r'<a href="(.+)" target="_blank".*>Message Board\s*\d*</a>', res
    )

    response["chats"] = re.findall(
        r'<a href="(.+)" target="_blank".*>Chat\s*\d*</a>', res
    )

    response["mineable"] = True if re.search(r'label-warning">Mineable', res) else False

    try:
        response["rank"] = int(re.search(r'Rank (\d+)</span>', res).group(1))
    except AttributeError:
        response["rank"] = None

    announcement = re.search(r'<a href="(.+)" target="_blank".*>Announcement</a>', res)
    response["announcement"] = announcement.group(1) if announcement else None

    return response

cpdef markets(res, convert):
    sources = re.findall(r'<a.*?href="/exchanges/.+/".*?>([\s\w\.-]+)</a>', res)
    markets = re.findall(r'target="_blank">(%s)</a>' % PAIRS_REGEX, res)
    volume_24h = re.findall(r'ume" .*data-%s="(\d+\.\d+)' % convert, res)
    price = re.findall(r'"price" .*data-%s="(\?|\d+\.*\d*e*[-|+]*\d*)' % convert, res)
    perc_volume = re.findall(
        r'[^(]<span data-format-percentage data-format-value="(-*\d+\.*[\d|e|-]*[\d|e|-]*)">',
        res
    )
    updated = re.findall(r'text-right\s.*">(.+)</td>', res)

    return [
        {
            "source": src,
            "pair": mark,
            "volume_24h": float(vol),
            "price": float(price),
            "percent_volume": float(perc),
            "updated": up == "Recently"
        } for src, mark, vol, price, perc, up in zip(sources, markets, volume_24h,
                                              price, perc_volume, updated)
    ]

cpdef ranks(res):
    cdef int rank_len = 30

    names_slugs = re.findall(
        r'<a.*?href="/currencies/([^/]+?)/".*?>([^<>]+?)</a>', res
    )
    symbols = re.findall(r'<td class="text-left">(.+)</td>', res)
    volume_24h = re.findall(r'ume" .*data-usd="(\d+\.*[\d|e|-]*)"', res)
    price = re.findall(r'ice" .*data-usd="(\d+\.*[\d|e|-]*)"', res)
    percent_change = re.findall(r'right" .*data-usd="(-*\d+\.*[\d|e|-]*)"', res)

    periods = ["1h", "24h", "7d"]
    index_map ={
        "gainers": dict(zip(periods, (0, 30, 60))),
        "losers": dict(zip(periods, (90, 150, 120)))
    }

    return {
        rank: {
            period: [{
                "name": names_slugs[index_map[rank][period] + i][1].strip(),
                "website_slug": names_slugs[index_map[rank][period] + i][0],
                "symbol": symbols[index_map[rank][period] + i],
                "volume_24h": float(volume_24h[index_map[rank][period] + i]),
                "price": float(price[index_map[rank][period] + i]),
                "percent_change": float(percent_change[index_map[rank][period] + i])
            } for i in range(rank_len)]
            for period in periods
        }
        for rank in index_map
    }

cpdef historical(res, start, end, revert):
    cdef long len_i, i, i2, i3

    dates = re.findall(r'<td class="text-left">(.+)</td>', res)
    vol_marketcap = re.findall(r'cap data-format-value="(-|\d+\.*[\d+-e]*)"', res)
    ohlc = re.findall(r'fiat data-format-value="(-|\d+\.*[\d+-e]*)"', res)

    len_i = len(dates)
    i = 0
    i2 = min([len(vol_marketcap*2) - len(ohlc), 2])
    i3 = 0

    response = []
    for _ in range(len_i):
        date = datetime.strptime(dates[i], '%b %d, %Y')
        if date < start:
            continue
        else:
            if date <= end:
                try:
                    close = float(ohlc[i3+3])
                except ValueError:
                    close = None
                try:
                    volume = float(vol_marketcap[i2-1])
                except ValueError:
                    volume = None
                try:
                    market_cap = float(vol_marketcap[i2])
                except ValueError:
                    market_cap = None

                response.append({
                    "date": date,
                    "open": float(ohlc[i3]),
                    "high": float(ohlc[i3+1]),
                    "low": float(ohlc[i3+2]),
                    "close": close,
                    "volume": volume,
                    "market_cap": market_cap
                })
            else:
                break
        i += 1
        i2 += 2
        i3 += 4
    return list(reversed(response)) if revert else response

def recently(res, convert):
    names =  re.findall(
        r'<a.*?href="/currencies/[^/]+?/".*?>([^<>]+?)</a>', res
    )
    symbols = re.findall(r'<td class="text-left">(.+)</td>', res)
    added = re.findall(r'<td class="text-right.*">(Today|\d+ days ago)</td>', res)
    mcap = re.findall(r'cap .*data-%s="(\?|\d+\.*[\d|e|-|\+]*)"' % convert, res)
    prices = re.findall(r'price" .*data-%s="(\d+\.*[\d|e|-|\+]*)"' % convert, res)
    supply = re.findall(r'data-supply="(\?|\d+\.*[\d|e|-|\+]*)"', res)
    vol_24h = re.findall(r'ume" .*data-%s="(\?|\d+\.*[\d|e|-|\+]*)"' % convert, res)
    p_change = re.findall(r'data-symbol=".+" data-sort="(-*\d+\.\d*)"', res)

    for n, sym, add, mcp, pr, sup, vol, perc in zip(
            names, symbols, added, mcap, prices, supply, vol_24h, p_change
        ):
        try:
            perc_change = float(perc[0])
        except ValueError:
            perc_change = None
        try:
            market_cap = float(mcp)
        except ValueError:
            market_cap = None
        try:
            csupply = float(sup)
        except ValueError:
            csupply = None
        try:
            volume_24h = float(vol)
        except ValueError:
            volume_24h = None

        yield {
            "name": n,
            "symbol": sym,
            "added": add,
            "market_cap": market_cap,
            "price": float(pr),
            "circulating_supply": csupply,
            "volume_24h": volume_24h,
            "percent_change": perc_change
        }

cpdef exchange(res, convert):
    currencies = re.findall(r'".*?market-name.*?">(.+)</a>', res)
    pairs = re.findall(r'target="_blank">(%s)</a>' % PAIRS_REGEX, res)
    vol_24h = re.findall(r'ume" .*data-%s="(\?|\d+\.*\d*e{0,1}-{0,1}\d*)"' % convert, res)
    prices = re.findall(r'price" .*data-%s="(\d+\.*\d*e{0,1}-{0,1}\d*)"' % convert, res)
    perc_vols = re.findall(r'percentage data-format-value="(\d+\.*\d*e{0,1}-{0,1}\d*)"', res)
    updated = re.findall(r'text-right\s.*"\s*>(.+)</td>', res)

    twitter_username = re.search(r'target="_blank">(@.+)</a>', res)
    twitter_link = re.findall(r'"(https://twitter.com/[^\s]+)"', res) \
        if twitter_username else None

    formatted_name = re.search(r'class="logo-.+" alt="(.+)">', res).group(1)
    web = re.search(r'title="Website">.*href="\s*([^\s|"]+)', res)

    markets = []
    for curr, pair, vol, price, perc_vol, up in zip(
        currencies, pairs, vol_24h, prices, perc_vols, updated
        ):
        try:
            vol = float(vol)
        except ValueError:
            vol = None
        markets.append({
            "currency": curr,
            "pair": pair,
            "volume_24h": vol,
            "price": float(price),
            "percent_volume": float(perc_vol),
            "updated": up == "Recently"
        })
    if convert == "btc":
        try:
            total_volume = float(perc_vols[0])
        except (ValueError, IndexError):
            total_volume = None
    else:
        try:
            total_volume = float(
                re.search(r'currency-volume data-usd="(\d+\.*[\d|e|-|\+]*)">', res).group(1)
            )
        except (AttributeError, ValueError):
            total_volume = None

    return {
        "name": formatted_name,
        "web": web.group(1) if web else None,
        "volume": total_volume,
        "social": {
            "twitter": {
                "link": twitter_link[0] if twitter_link else None,
                "username": twitter_username.group(1) if twitter_username else None
            }
        },
        "markets": markets
    }

cpdef exchanges(res, convert):
    cdef int i
    exchanges =  re.findall(
        r'<a.*?href="/exchanges/([^/]+?)/">([^<>]+?)</a>', res
    )
    indexes = re.findall(r'<td>(\d+)</td>', res)
    currencies =  re.findall(
        r'<a.*?href="/currencies/[^/]+?/".*?>([^<>]+?)</a>', res
    )
    links_pairs = re.findall(r'<a href="(.*)" .*_blank">(%s)</a>' % PAIRS_REGEX, res)
    volumes = re.findall(
        r'class="text-right .*volume" .*data-%s="(\?|\d+\.*\d*e{0,1}-{0,1}\d*)"' % convert, res
    )
    prices = re.findall(r'ice" .*data-%s="(\?|\d+\.*\d*e{0,1}-{0,1}\d*)"' % convert, res)
    perc_volumes = re.findall(r'"percent-volume">(\d+\.*\d*)</span>', res)

    response = []
    for slug, exc in exchanges:
        markets = []
        for _ in indexes:
            i = int(_)
            try: vol = float(volumes[i-1])
            except ValueError: vol = None
            try: price = float(prices[i-1])
            except ValueError: price = None

            markets.append({
                "name": currencies[i-1],
                "web": links_pairs[i-1][0],
                "pair": links_pairs[i-1][1],
                "volume": vol,
                "price": price,
                "percent_volume": float(perc_volumes[i-1])
            })

            try:
                if indexes[i] == "1":
                    indexes = indexes[i:]
                    currencies = currencies[i:]
                    break
            except IndexError:
                break

        response.append({
            "name": exc,
            "website_slug": slug,
            "markets": markets,
        })

    return response

cpdef tokens(res, convert):
    names = re.findall(
        r'currency-name-container.*?".*?href="/currencies/[^/]+?/".*?>([^<>]+?)</a>',
        res
    )
    symbols = re.findall(
        r'currency-symbol.*?".*?href="/currencies/[^/]+?/".*?>([^<>]+?)</a>',
        res
    )
    platforms = re.findall(r'platform-name" data-sort="([^"]+)">', res)
    caps = re.findall(
        r'market-cap .*data-%s="(\?|\d+\.*\d*e{0,1}-{0,1}\d*)"' % convert, res
    )
    prices = re.findall(r'price" .*data-%s="(\?|\d+\.*\d*e{0,1}-{0,1}\d*)"' % convert, res)
    supplys = re.findall(r'data-supply="(None|\d+\.*\d*e{0,1}[+-]{0,1}\d*)"', res)
    vols_24h = re.findall(
        r'volume" .*data-%s="(None|\d+\.*\d*e{0,1}[+-]{0,1}\d*)"' % convert, res
    )

    response = []
    for n, sym, plat, mcap, price, sup, vol in zip(
        names, symbols, platforms, caps, prices, supplys, vols_24h
        ):
        if plat == "": plat = None
        try: mcap = float(mcap)
        except ValueError: mcap = None
        try: price = float(price)
        except ValueError: price = None
        try: sup = float(sup)
        except ValueError: sup = None
        try: vol = float(vol)
        except ValueError: vol = None
        response.append({
            "name": n,
            "symbol": sym,
            "platform": plat,
            "market_cap": mcap,
            "price": price,
            "circulating_supply": sup,
            "volume_24h": vol
        })
    return response

cpdef graphs(res, start, end):
    is_start = isinstance(start, datetime)
    is_end = isinstance(end, datetime)
    is_both = is_start and is_end

    dt_filter = _get_dt_filter(start, end)

    response = {}
    for key, value in res.items():
        group = []
        for _tmp, data in value:
            tmp = datetime.fromtimestamp(_tmp / 1000)
            if dt_filter(tmp):
                group.append([tmp, data])
        response[key] = group
    return response

cdef _get_dt_filter(start, end):
    if isinstance(start, date):
        start = datetime.combine(start, DATETIME_MIN_TIME)
    if isinstance(end, date):
        end = datetime.combine(end, DATETIME_MAX_TIME)

    is_start = isinstance(start, datetime)
    is_end = isinstance(end, datetime)
    is_both = is_start and is_end

    if is_both:
        return lambda dt: start <= dt <= end
    elif is_start:
        return lambda dt: dt >= start
    elif is_end:
        return lambda dt: dt <= end
    else:
        return lambda dt: dt
