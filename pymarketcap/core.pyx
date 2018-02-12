# Standard Python modules
import re
from json import loads
from datetime import datetime, timedelta
from time import time, sleep
from collections import OrderedDict

# Internal Cython modules
from pymarketcap.curl import get_to_memory

# Internal Python modules
from pymarketcap.errors import (
    CoinmarketcapHTTPError,
    CoinmarketcapHTTPError404,
    CoinmarketcapTooManyRequestsError
)

# HTTP errors mapper
http_errors_map = {
    "429": CoinmarketcapTooManyRequestsError,
    "404": CoinmarketcapHTTPError404,
}

http_error_numbers = [int(number) for number in http_errors_map.keys()]

# Common RegEx
PAIRS_REGEX = "[\s\$@\w\.]+/[\s\$@\w\.]+"

cdef class Pymarketcap:
    """Main class for retrieve data from coinmarketcap.com

    Args:
        timeout (int, optional): Set timeout value for get requests.
            As default 20.
        debug: (bool, optional): Show low level data in get requests.
            As default, False.
        cache (bool, optional): Enable or disable cache at instantiation
            time. ¡Warning -> some methods couldn't be called, use
            this attribute with caution! As default, True.
    """

    cdef readonly dict correspondences
    cdef readonly list symbols
    cdef readonly list coins
    cdef readonly int total_currencies
    cdef readonly list currencies_to_convert
    cdef readonly list converter_cache
    cdef readonly list exchange_names
    cdef readonly list exchange_slugs

    cdef public long timeout
    cdef public object graphs
    cdef public bint debug

    cdef readonly dict exceptional_coin_slugs
    cdef readonly list exceptional_coin_slugs_keys
    cdef readonly list exceptional_coin_slugs_values

    def __init__(self, timeout=20, debug=False, cache=True):
        self.timeout = timeout
        self.debug = debug

        self.graphs = type("Graphs", (), self._graphs_interface)

        self.exceptional_coin_slugs = {
            "42": "42-coin",
            "808": "808coin",
            "611": "sixeleven",
            "300": "300-token",
            "888": "octocoin",
            "$$$": "money",
            "BTBc": "bitbase",
        }

        self.exceptional_coin_slugs_keys = list(self.exceptional_coin_slugs.keys())
        self.exceptional_coin_slugs_values = list(self.exceptional_coin_slugs.values())

        if cache:
            self._renew_cache()

    ######   RUNTIME INIT   #######

    def _renew_cache(self):
        """Internal function to renew cached instance attributes."""
        if self.debug:
            print("Caching useful data...")
        self.correspondences = self._cache_symbols()
        self.symbols = list(self.correspondences.keys())
        self.coins = list(self.correspondences.values())
        self.total_currencies = self.ticker()[-1]["rank"]
        sleep(.5)
        self.currencies_to_convert = self._currencies_to_convert()
        self.converter_cache = [self.currency_exchange_rates, time()]
        sleep(.5)
        self.exchange_names = sorted(self._exchange_names())
        self.exchange_slugs = sorted(self._exchange_slugs())

    @property
    def _graphs_interface(self):
        return {
            "currency": self._currency,
            "global_cap": self.global_cap,
            "dominance": self.dominance
        }

    ######   UTILS   #######

    cdef _get(self, char *url):
        """Internal function to make and HTTP GET request
        using the curl Cython bridge to C library."""
        cdef int status
        req = get_to_memory(<char *>url, self.timeout, <bint>self.debug)
        status = req.status_code
        if status == 200:
            return req.text.decode()
        else:
            msg = "Status code -> %d | Url -> %s" % (status, url.decode())
            if status in http_error_numbers:
                raise http_errors_map[str(status)](msg)
            else:
                print("DEBUG: ")
                print(req.text)
                print(req.url)
                raise CoinmarketcapHTTPError(msg)

    cpdef _is_symbol(self, unicode currency):
        """Internal function for check
        if a currency string may be a symbol or not.
        This function is not strict, so if you pass
        _is_symbol("OBASDFPAFFFOUASVBF") will returns True
        but in this context we don't need to check if
        the user has introduced a valid symbol.

        Returns bint:
            1 if True, 0 if False
        """
        cdef bint response
        response = 0        # Is not strictly:
        if currency.isupper() or currency in self.exceptional_coin_slugs_keys:
            response = 1
        return response

    cpdef _cache_symbols(self):
        """Internal function for load in cache al symbols
        in coinmarketcap with their respectives currency names."""
        cdef bytes url
        url = b"https://files.coinmarketcap.com/generated/search/quick_search.json"
        res = loads(self._get(url))
        response = {}
        for currency in res:
            response[currency["symbol"]] = currency["slug"].replace(" ", "")
        for original, correct in self.exceptional_coin_slugs.items():
            response[original] = correct
        return response

    @property
    def ticker_badges(self):
        """Badges that you can convert prices in ticker() method."""
        return

    # ====================================================================

    #######   API   #######

    cpdef stats(self, convert="USD"):
        """ Get global cryptocurrencies statistics.

        Args:
            convert (str, optional): return 24h volume, and
                market cap in terms of another currency.
                See ticker_badges property to get valid values.
                As default "USD".

        Returns:
            dict: Global markets statistics
        """
        return loads(self._get(b"https://api.coinmarketcap.com/v1/global/?convert=%s" % convert.encode()))

    cpdef ticker(self, currency=None, limit=0, start=0, convert="USD"):
        """Get currencies with other aditional data.

        Args:
            currency (str, optional): Specify a currency to return,
                in this case the method returns a dict, otherwise
                returns a list. If you dont specify a currency,
                returns data for all in coinmarketcap. As default, None.
            limit (int, optional): Limit amount of coins on response.
                if limit == 0, returns all coins in coinmarketcap.
                Only works if currency == None. As default 0.
            start (int, optional): Rank of first currency to retrieve.
                The count starts at 0 for the first currency ranked.
                Only works if currency == None. As default 0.
            convert (str, optional): As default, "USD". Allow to
                convert price, 24h volume and market cap in terms
                of one of next badges:

        Returns:
            dict/list: If currency param is provided or not.

        """
        cdef bytes url
        if not currency:
            url = b"https://api.coinmarketcap.com/v1/ticker/?%s" % b"limit=%d" % limit
            url += b"&start=%d" % start
            url += b"&convert=%s" % convert.encode()
            res = self._get(url)
            return loads(re.sub(r'"(-*\d+(?:\.\d+)?)"', r"\1", res))
        else:
            if self._is_symbol(currency):
                currency = self.correspondences[currency]
            url = b"https://api.coinmarketcap.com/v1/ticker/%s" % currency.encode()
            url += b"?convert=%s" % convert.encode()
            res = self._get(url)
            return loads(re.sub(r'"(-*\d+(?:\.\d+)?)"', r"\1", res))[0]

    # ====================================================================

    #######    WEB SCRAPER    #######

    @property
    def currency_exchange_rates(self):
        """Get currency exchange rates against $ for the next currencies:

        Returns (dict):
            All currencies rates used internally by coinmarketcap to calculate
                the prices shown.
        """
        res = self._get(b"https://coinmarketcap.com")
        rates = re.findall(r'data-(\w+)="(\d+\.*[\d|e|-]*)"', res[-4000:-2000])
        return {currency.upper(): float(rate) for currency, rate in rates}

    cpdef _currencies_to_convert(self):
        """Internal function for get currencies from and to convert
            values in convert() method. Don't use this, but cached
            currencies_to_convert instance attribute instead.

        Returns (list):
            All currencies that could be passed to convert() method.
        """
        res = self._get(b"https://coinmarketcap.com")
        currencies = re.findall(r'data-(\w+)="\d', res[-4000:-2000])
        return [currency.upper() for currency in currencies]

    cpdef convert(self, value, unicode currency_in, unicode currency_out):
        """Convert prices between currencies. Provides a value,
            the currency of the value and the currency to convert it
            and get the value in currency converted rate.
            For see all available currencies to convert see
                currencies_to_convert property.

        Args:
            value (int/float): Value to convert betweeen two currencies.
            currency_in (str): Currency in which is expressed the value passed.
            currency_out (str): Currency to convert.

        Returns (float): Value expressed in currency_out parameter provided.
        """
        if time() - self.converter_cache[1] > 600:
            self.converter_cache[0] = self.currency_exchange_rates
        try:
            if currency_in == "USD":
                return value / self.converter_cache[0][currency_out]
            elif currency_out == "USD":
                return value * self.converter_cache[0][currency_in]
            else:
                rates = self.converter_cache[0]
                return value * rates[currency_in] / rates[currency_out]
        except KeyError:
            msg = "Invalid currency: '%s'. See currencies_to_convert instance attribute."
            for param in [currency_in, currency_out]:
                if param not in self.currencies_to_convert:
                    raise ValueError(msg % param)
            raise NotImplementedError

    cpdef currency(self, unicode name, convert="USD"):
        """Get currency metadata like total markets capitalization,
        websites, source code link, if mineable...

        Args:
            currency (str): Currency to get metadata.
            convert (str, optional): Currency to convert response
                fields total_markets_cap, total_markets_volume_24h
                and price between "USD" and "BTC". As default "USD".

        Returns (dict):
            Aditional general metadata not supported by other methods.
        """
        if self._is_symbol(name):
            name = self.correspondences[name]
        convert = convert.lower()

        res = self._get(
            b"https://coinmarketcap.com/currencies/%s/" % name.encode()
        )[20000:]

        # Total market capitalization and volume 24h
        if convert == "usd":
            _total_markets_cap = re.search(
                r'data-currency-market-cap.+data-usd="(\?|\d+\.*\d*e*[-|+]*\d*)"', res
            )
            _total_markets_volume = re.search(
                r'data-currency-volume.+data-usd="(\?|\d+\.*\d*e*[-|+]*\d*)"', res
            )
            _price = re.search(r'quote_price.+data-usd="(\?|\d+\.*\d*e*[-|+]*\d*)"', res)
        else:
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
        try: total_cap = _total_markets_cap.group(1)
        except AttributeError: total_cap = "?"
        response = {"total_markets_cap": float(total_cap) if total_cap != "?" else None,
                    "total_markets_volume_24h": float(vol_24h) if vol_24h != "?" else None,
                    "price": float(_price.group(1)) if _price else None}

        # Circulating, total and maximum supply
        supply = re.findall(
            r'data-format-supply.+data-format-value="(\?|\d+\.*\d*e*[-|+]*\d*)"', res
        )
        response["circulating_supply"] = float(supply[0]) if supply[0] != "?" else None
        if len(supply) > 1:
            response["max_supply"] = float(supply[-1])
        if len(supply) > 2:
            response["total_supply"] = float(supply[1])

        response["webs"] = re.findall(r'<a href="(.+)" target="_blank">Website\s*\d*</a>', res)

        response["explorers"] = re.findall(
            r'<a href="(.+)" target="_blank">Explorer\s*\d*</a>', res
        )

        source_code = re.search(r'<a href="(.+)" target="_blank">Source Code</a>', res)
        response["source_code"] = source_code.group(1) if source_code else None

        response["message_boards"] = re.findall(
            r'<a href="(.+)" target="_blank">Message Board\s*\d*</a>', res
        )

        response["chats"] = re.findall(
            r'<a href="(.+)" target="_blank">Chat\s*\d*</a>', res
        )

        response["mineable"] = True if re.search(r'label-warning">Mineable', res) else False

        response["rank"] = int(re.search(r'Rank (\d+)</span>', res).group(1))

        announcement = re.search(r'<a href="(.+)" target="_blank">Announcement</a>', res)
        response["announcement"] = announcement.group(1) if announcement else None

        return response

    cpdef markets(self, unicode name, convert="USD"):
        """Get available coinmarketcap markets data.
        It needs a currency as argument.

        Args:
            currency (str): Currency to get market data.
            convert (str, optional): Currency to convert response
                fields volume_24h and price between "USD" and "BTC".
                As default "USD".

        Returns:
            list: markets on wich provided currency is currently tradeable
        """
        if self._is_symbol(name):
            name = self.correspondences[name]
        convert = convert.lower()

        res = self._get(
            b"https://coinmarketcap.com/currencies/%s/" % name.encode()
        )[20000:]

        sources = re.findall(r'<a href="/exchanges/.+/">([\s\w\.-]+)</a>', res)
        markets = re.findall(r'target="_blank">(%s)</a>' % PAIRS_REGEX, res)
        volume_24h = re.findall(r'ume" .*data-%s="(\d+\.\d+)' % convert, res)
        price = re.findall(r'ice" .*data-%s="(\d+\.[\d|e|-]*[\d|e|-]*)' % convert, res)
        perc_volume = re.findall(r'percentage data-format-value="(-*\d+\.*[\d|e|-]*[\d|e|-]*)">', res)
        updated = re.findall(r'text-right\s.*">(.+)</td>', res)


        for v in [sources, markets, volume_24h, price, perc_volume, updated]:
            #print(v)
            print(len(v))

        return [
            {
                "source": src,
                "pair": mark,
                "volume_24h": float(vol),
                "price": float(price),
                "percent_volume": float(perc),
                "updated": up == "Recently"
            } for src, mark, vol, price, perc, up in zip(sources, markets, volume_24h,
                                                  price, perc_volume[2:], updated)
        ]

    cpdef ranks(self):
        """Returns gainers and losers for the periods 1h, 24h and 7d.

        Args:
            convert (str, optional): Convert volume, price and percentages
                between USD and BTC. As default "USD".

        Returns (dict):
            A dictionary with 2 keys (gainers and losers) whose values
                are the periods "1h", "24h" and "7d"
        """
        cdef int i = 30
        res = self._get(b"https://coinmarketcap.com/gainers-losers/")

        names = re.findall(r'<a href="/currencies/.+/">(.+)</a>.*', res)[6:]
        symbols = re.findall(r'<td class="text-left">(\w+)</td>', res)
        volume_24h = re.findall(r'ume" .*data-usd="(\d+\.*[\d|e|-]*)"', res)
        price = re.findall(r'ice" .*data-usd="(\d+\.*[\d|e|-]*)"', res)
        percent_change = re.findall(r'right" .*data-usd="(-*\d+\.*[\d|e|-]*)"', res)

        index_map = {
            "gainers": {"1h": 0, "7d": 30, "24h": 60},
            "losers": {"1h": 90, "7d": 150, "24h": 120}
        }

        return {rank: {period: [{
            "name": names[index_map[rank][period]],
            "symbol": symbols[index_map[rank][period]],
            "volume_24h": float(volume_24h[index_map[rank][period]]),
            "price": float(price[index_map[rank][period]]),
            "percent_change": float(percent_change[index_map[rank][period]])
        } for _ in range(i)] \
             for period in ["1h", "24h", "7d"] } for rank in ["gainers", "losers"]}

    def historical(self, unicode currency,
                   start=datetime(2008, 8, 18),
                   end=datetime.now(),
                   revert=False):
        """Get historical data for a currency.

        Args:
            currency (str): Currency to scrap historical data
            start (date, optional): Time to start scraping
                periods as datetime.datetime type.
                As default datetime(2008, 8, 18)
            end (date, optional): Time to end scraping periods
                as datetime.datetime type.
                As default datetime.now()
            revert (bool, optional): If False, return first date
                first, in chronological order, otherwise returns
                reversed list of periods. As default False

        Returns (list):
            Historical dayly OHLC for a currency.
        """
        cdef bytes url, _start, _end
        cdef long len_i, i, i2, i3

        if self._is_symbol(currency):
            currency = self.correspondences[currency]

        url = b"https://coinmarketcap.com/currencies/%s/historical-data/" % currency.encode()
        _start = b"%d" % start.year + b"%02d" % start.month + b"%02d" % start.day
        _end = b"%d" % end.year + b"%02d" % end.month + b"%02d" % end.day
        url += b"?start=%s" % _start + b"&" + b"end=%s" % _end
        res = self._get(url)[50000:]

        dates = re.findall(r'<td class="text-left">(.+)</td>', res)
        vol_marketcap = re.findall(r'cap [\w|-]+="(-|\d+\.*[\d+-e]*)"', res)
        ohlc = re.findall(r'fiat data-format-value="(-|\d+\.*[\d+-e]*)"', res)

        len_i = len(dates)
        i = 0
        i2 = 0
        i3 = 0

        response = []
        for _ in range(len_i):
            date = datetime.strptime(dates[i], '%b %d, %Y')
            if date < start:
                continue
            else:
                if date <= end:
                    response.append({
                        "date": date,
                        "open": float(ohlc[i3]),
                        "high": float(ohlc[i3+1]),
                        "low": float(ohlc[i3+2]),
                        "close": float(ohlc[i3+3]),
                        "volume": float(ohlc[i2]),
                        "market_cap": float(ohlc[i2+1])
                    })
                else:
                    break
            i += 1
            i2 += 2
            i3 += 4
        return list(reversed(response)) if revert else response

    def recently(self, convert="USD"):
        """Get recently added currencies along with other metadata.

        Args:
            convert (str, optional): Convert market_caps, prices,
                volumes and percent_changes between USD and BTC.
                As default "USD".

        Returns (generator):
            Recently added currencies data.
        """
        convert = convert.lower()
        url = b"https://coinmarketcap.com/new/"
        res = self._get(url)

        names = re.findall(r'<a href="/currencies/.+/">(.+)</a>', res)[6:]
        symbols = re.findall(r'<td class="text-left">(.+)</td>', res)
        added = re.findall(r'<td class="text-right.*">(Today|\d+ days ago)</td>', res)
        mcap = re.findall(r'cap .*data-%s="(\?|\d+\.*[\d|e|-|\+]*)"' % convert, res)
        prices = re.findall(r'price" .*data-%s="(\d+\.*[\d|e|-|\+]*)"' % convert, res)
        supply = re.findall(r'data-supply="(\?|\d+\.*[\d|e|-|\+]*)"', res)
        vol_24h = re.findall(r'ume" .*data-%s="(\?|\d+\.*[\d|e|-|\+]*)"' % convert, res)
        p_change = re.findall(
            r'change .*data-%s="(\?|-*\d+\.*[\d|e|-|\+]*)"|<td class="text-right">(\?)</td>' \
            % convert, res
        )

        for n, sym, add, mcp, pr, sup, vol, perc in zip(
                names, symbols, added, mcap, prices, supply, vol_24h, p_change
            ):
            try: perc_change = float(perc[0])
            except ValueError: perc_change = None
            try: market_cap = float(mcp)
            except ValueError: market_cap = None
            try: csupply = float(sup)
            except ValueError: csupply = None
            try: volume_24h = float(vol)
            except ValueError: volume_24h = None
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

    cpdef exchange(self, unicode name, convert="USD"):
        """Obtain data from a exchange passed as argument.
            See exchanges_names instance attribute for obtain
            all posibles values.

        Example:
            exchange('poloniex')

        Args:
            name (str): Exchange to retrieve data. Check exchange_slugs
                instance attribute for get all posible values for pass
                to this parameter.
            convert (str, optional): Convert prices and
                24h volumes in return between USD and BTC.
                As default "USD".

        Returns (dict):
            Data from a exchange. Keys: "name", "website",
                "volume" (total), "social" and "markets".
        """
        url = b"https://coinmarketcap.com/exchanges/%s/" % name.encode()
        try:
            res = self._get(url)[20000:]
        except CoinmarketcapHTTPError404:
            if name not in self.exchange_slugs:
                raise ValueError("%s is not a valid exchange name. See exchange_slugs" % name \
                    + " instance attribute for get all valid exchanges.")
            else:
                raise NotImplementedError
        convert = convert.lower()

        currencies = re.findall(r'"market-name">(.+)</a>', res)
        pairs = re.findall(r'target="_blank">(%s)</a>' % PAIRS_REGEX, res)
        vol_24h = re.findall(r'ume" .*data-%s="(\?|\d+\.*\d*e{0,1}-{0,1}\d*)"' % convert, res)
        prices = re.findall(r'price" .*data-%s="(\d+\.*\d*e{0,1}-{0,1}\d*)"' % convert, res)
        perc_vols = re.findall(r'percentage data-format-value="(\d+\.*\d*e{0,1}-{0,1}\d*)"', res)
        updated = re.findall(r'text-right\s.*"\s*>(.+)</td>', res)

        twitter_username = re.search(r'target="_blank">(@.+)</a>', res)
        twitter_link = re.findall(r'"(https://twitter.com/[^\s]+)"', res) \
            if twitter_username else None

        formatted_name = re.search(r'<h1 class="text-large">\s*(.+)\s*</h1>', res).group(1)
        web = re.search(r'title="Website">.*href="\s*([^\s|"]+)', res)

        markets = []
        for curr, pair, vol, price, perc_vol, up in zip(
            currencies, pairs, vol_24h, prices, perc_vols, updated
            ):
            try: vol = float(vol)
            except ValueError: vol = None
            markets.append({
                "currency": curr,
                "pair": pair,
                "vol_24h": vol,
                "price": float(price),
                "perc_volume": float(perc_vol),
                "updated": up == "Recently"
            })
        if convert == "btc":
            try: total_volume = float(perc_vols[0])
            except ValueError: total_volume = None
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

    cpdef _exchange_names(self):
        """Internal function for get all exchange names
            available currently in coinmarketcap. Check exchange_names
            instance attribute for the cached method counterpart.

        Returns (list):
            All exchanges in coinmarketcap.
        """
        res = self._get(b"https://coinmarketcap.com/exchanges/volume/24-hour/all/")
        return re.findall('<a href="/exchanges/.+/">((?!View More).+)</a>', res)[5:]

    def _exchange_slugs(self):
        """Internal function for obtain all exchanges slugs."""
        res = self._get(b"https://coinmarketcap.com/exchanges/volume/24-hour/all/")
        parsed = re.findall('<a href="/exchanges/(.+)/">', res)[5:]
        return list(OrderedDict.fromkeys(parsed)) # Remove duplicates without change order

    def exchanges(self, convert="USD"):
        """Get all the exchanges in coninmarketcap ranked by volumes
        along with other metadata.

        Args:
            convert (str, optional): Convert volumes and prices
                between "USD" and "BTC". As default "USD".

        Returns (list):
            Exchanges with markets and other data included.
        """
        cdef int i
        res = self._get(b"https://coinmarketcap.com/exchanges/volume/24-hour/all/")[45000:]
        convert = convert.lower()

        exchanges = re.findall(r'\. <a href="/exchanges/.+/">(.+)</a>', res)
        indexes = re.findall(r'<td>(\d+)</td>', res)
        currencies = re.findall(r'/currencies/.+/">(.+)</a>', res)[2:]
        links_pairs = re.findall(r'<a href="(.*)" .*_blank">(%s)</a>' % PAIRS_REGEX, res)
        volumes = re.findall(
            r'class="text-right .*volume" .*data-%s="(\?|\d+\.*\d*e{0,1}-{0,1}\d*)"' % convert, res
        )
        prices = re.findall(r'ice" .*data-%s="(\?|\d+\.*\d*e{0,1}-{0,1}\d*)"' % convert, res)
        perc_volumes = re.findall(r'"percent-volume">(\d+\.*\d*)</span>', res)

        response = []
        for exc in exchanges:
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
                    "perc_volume": float(perc_volumes[i-1])
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
                "markets": markets,
            })

        return response

    cpdef tokens(self, convert="USD"):
        """Get data from platforms tokens

        Args:
            convert (str, optional): Convert "market_cap", "price"
                and "volume_24h" values between "USD" and "BTC".
                As default "USD".

        Returns (list):
            Platforms tokens data.
        """
        url = b"https://coinmarketcap.com/tokens/views/all/"
        res = self._get(url)[40000:]
        convert = convert.lower()

        names = re.findall(r'currency-name-container" href="/currencies/.+/">(.+)</a>', res)
        symbols = re.findall(r'currency-symbol"><a href="/currencies/.+/">(.+)</a>', res)
        platforms = re.findall(r'platform-name"><a href="/currencies/[\w-]*/">(.*)</a>', res)
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

    # ====================================================================

    ######   GRAPHS API   #######

    cpdef _currency(self, unicode name, start=None, end=None):
        """Get graphs data of a currency.

        Args:
            currency (str): Currency to retrieve graphs data.
            start (int, optional): Time to start retrieving
                graphs data in microseconds unix timestamps.
                Only works with times provided by the times
                returned in graphs functions. As default None.
            end (optional, datetime): Time to end retrieving
                graphs data in microseconds unix timestamps.
                Only works with times provided by the times
                returned in graphs functions. As default None.

        Returns (dict):
            Dict info with next keys:
            `
                {"market_cap_by_available_supply": [...],
                 "price_btc": [...],
                 "price_usd": [...],
                 "volume_usd": [...],
                 "price_platform": [...],
                 }
            `
            For each value, a list of lists where each one
            has two values [<timestamp>, <value>]
        """
        if self._is_symbol(name):
            name = self.correspondences[name]

        url = b"https://graphs2.coinmarketcap.com/currencies/%s/" % name.encode()

        if start and end:
            url += b"%s/%s/" % (str(start).encode(), str(end).encode())

        return loads(self._get(url))

    cpdef global_cap(self, bitcoin=True, start=None, end=None):
        """Get global market capitalization graphs, including
        or excluding Bitcoin

        Args:
            bitcoin (bool, optional): Indicates if Bitcoin will
                be includedin global market capitalization graph.
                As default True.
            start (int, optional): Time to start retrieving
                graphs data in microseconds unix timestamps.
                Only works with times provided by the times
                returned in graphs functions. As default None.
            end (optional, datetime): Time to end retrieving
                graphs data in microseconds unix timestamps.
                Only works with times provided by the times
                returned in graphs functions. As default None.

        Returns (dict):
            Whose values are lists of lists with timestamp and values,
                a data structure with the form:
                    `
                        {'market_cap_by_available_supply': [...],
                         'volume_usd': [...]
                        }
                    `
        """
        if bitcoin:
            url = b"https://graphs2.coinmarketcap.com/global/marketcap-total/"
        else:
            url = b"https://graphs2.coinmarketcap.com/global/marketcap-altcoin/"

        if start and end:
            url += b"%s/%s/" % (str(start).encode(), str(end).encode())

        return loads(self._get(url))

    cpdef dominance(self, start=None, end=None):
        """Get currencies dominance percentage graph

        Args:
            start (int, optional): Time to start retrieving
                graphs data in microseconds unix timestamps.
                Only works with times provided by the times
                returned in graphs functions. As default None.
            end (optional, datetime): Time to end retrieving
                graphs data in microseconds unix timestamps.
                Only works with times provided by the times
                returned in graphs functions. As default None.

        Returns (dict):
            Altcoins dict and dominance percentage values with timestamps
        """
        url = b"https://graphs2.coinmarketcap.com/global/dominance/"

        if start and end:
            url += b"%s/%s/" % (str(start).encode(), str(end).encode())

        return loads(self._get(url))
