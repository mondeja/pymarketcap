
"""API wraper and web scraper module."""

# Standard Python modules
from re import sub as re_sub
from re import findall as re_findall
from json import loads
from datetime import datetime
from time import time
from urllib.request import urlretrieve
from urllib.error import HTTPError

# Internal Cython modules
from pymarketcap.curl import get_to_memory
from pymarketcap import processer

# Internal Python modules
from pymarketcap.consts import (
    DEFAULT_TIMEOUT,
    EXCEPTIONAL_COIN_SLUGS,
    INVALID_COINS
)
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


cdef class Pymarketcap:
    """Synchronous class for retrieve data from coinmarketcap.com

    Args:
        timeout (int, optional): Set timeout value for get requests.
            As default ``20``.
        debug: (bool, optional): Show low level data in get requests.
            As default, ``False``.
    """
    cdef readonly dict _correspondences
    cdef readonly dict _ids_correspondences
    cdef readonly list _symbols
    cdef readonly list _coins
    cdef readonly int  _total_currencies
    cdef readonly int  _total_exchanges
    cdef readonly list _currencies_to_convert
    cdef readonly list _converter_cache
    cdef readonly list _exchange_names
    cdef readonly list _exchange_slugs
    cdef readonly dict __repeated_symbols

    cdef public long timeout
    cdef public object graphs
    cdef public bint debug

    def __init__(self, timeout=DEFAULT_TIMEOUT, debug=False):
        self.timeout = timeout
        self.debug = debug

        #: object: Initialization of graphs internal interface
        self.graphs = type("Graphs", (), self._graphs_interface)

    # ====================================================================

                         #######   UTILS   #######

    @property
    def _graphs_interface(self):
        return {
            "currency": self._currency,
            "global_cap": self._global_cap,
            "dominance": self._dominance
        }

    @property
    def correspondences(self):
        res = self._correspondences
        if res:
            return res
        else:
            main_cache = self._cache_symbols_ids()
            self._correspondences = main_cache[0]
            self._ids_correspondences = main_cache[1]
            return self._correspondences

    @property
    def ids_correspondences(self):
        """Get symbols with their correspondient numeric
        id (used for debug purposes)."""
        res = self._ids_correspondences
        if res:
            return res
        else:
            main_cache = self._cache_symbols_ids()
            self._correspondences = main_cache[0]
            self._ids_correspondences = main_cache[1]
            return self._ids_correspondences

    cpdef _is_symbol(self, unicode currency):
        """Internal function for check
        if a currency string may be a symbol or not.
        This function is not strict, so if you pass
        self._is_symbol("OBASDFPAFFFOUASVBF") will returns True
        but in this context we don't need to check if
        the user has introduced a valid symbol.

        Returns bint:
            1 if True, 0 if False
        """
        cdef bint response
        response = 0
        if currency.isupper() or currency in EXCEPTIONAL_COIN_SLUGS:
            try:
                if currency in self.__repeated_symbols:
                    msg = 'The symbol "%s" has more than one correspondence ' % currency \
                        + "with coin slugs in Coinmarketcap. Please get this currency as slug. " \
                        + "\nPossible valid slug names: %r." % self.__repeated_symbols[currency]
                    raise ValueError(msg)
            except TypeError:
                pass
            response = 1
        return response

    cpdef _quick_search(self):
        """Internal pymarketcap JSON cache file ``quick_search.json``."""
        cdef bytes url
        url = b"https://s2.coinmarketcap.com/generated/search/quick_search.json"
        return loads(self._get(url))

    cpdef _cache_symbols_ids(self):
        """Internal function for load in cache all symbols
        in coinmarketcap with their respectives currency names."""
        self.__repeated_symbols = {}
        symbols_slugs, symbols_ids = {}, {}
        for currency in self._quick_search():
            symbol = currency["symbol"]
            slug = currency["slug"].replace(" ", "")
            if symbol in symbols_slugs:    # Repeated symbols are stored internally
                if symbol in self.__repeated_symbols.keys():
                    self.__repeated_symbols[symbol].append(slug)
                else:
                    self.__repeated_symbols[symbol] = [symbols_slugs[symbol], slug]
            else:
                symbols_slugs[symbol] = slug
            symbols_ids[symbol] = currency["id"]
        for original, correct in EXCEPTIONAL_COIN_SLUGS.items():
            symbols_slugs[original] = correct
        return (symbols_slugs, symbols_ids)

    @property
    def symbols(self):
        """Symbols of currencies (in capital letters).

        Returns (list):
            All currency symbols provided by coinmarketcap.
        """
        res = self._symbols
        if res:
            return res
        else:
            self._symbols = sorted(list(self.correspondences.keys()))
            for invalid_symbol in self.__repeated_symbols:
                self._symbols.remove(invalid_symbol)
            return self._symbols

    @property
    def coins(self):
        """Coins not formatted names for all currencies
        (in lowercase letters) used internally by urls.

        Returns (list):
            All currency coins names provided by coinmarketcap.
        """
        res = self._coins
        if res:
            return res
        else:
            self._coins = []
            for coin_or_coins in list(self.correspondences.values()):
                if isinstance(coin_or_coins, list):
                    for coin in coin_or_coins:
                        self._coins.append(coin)
                else:
                    self._coins.append(coin_or_coins)
            for invalid_coin in INVALID_COINS:
                try:
                    self._coins.remove(invalid_coin)
                except ValueError:
                    pass
            self._coins = sorted(self._coins)
            return self._coins

    @property
    def total_currencies(self):
        res = self._total_currencies
        if res:
            return res
        else:
            self._total_currencies = self.ticker()[-1]["rank"]
            return self._total_currencies

    @property
    def currencies_to_convert(self):
        res = self._currencies_to_convert
        if res:
            return res
        else:
            self._currencies_to_convert = self.__currencies_to_convert()
            return self._currencies_to_convert

    cpdef __currencies_to_convert(self):
        """Internal function for get currencies from and to convert
            values in convert() method. Don't use this, but cached
            :attr:`~pymarketcap.core.Pymarketcap.currencies_to_convert`
            instance attribute instead.

        Returns (list):
            All currencies that could be passed to
            :meth:`~pymarketcap.core.Pymarketcap.convert`.
        """
        res = self._get(b"https://coinmarketcap.com")
        currencies = re_findall(r'data-([a-z]+)="\d', res[-10000:-2000])
        response = [currency.upper() for currency in currencies]
        response.extend([str(currency["symbol"]) for currency in self.ticker()])
        return sorted(response)

    @property
    def exchange_names(self):
        """Get all exchange formatted names provided by coinmarketcap."""
        res = self._exchange_names
        if res:
            return res
        else:
            self._exchange_names = sorted(list(self.__exchange_names_slugs().keys()))
            return self._exchange_names

    cpdef __exchange_names_slugs(self):
        """Internal function for get all exchange names
            available currently in coinmarketcap. Check ``exchange_names``
            instance attribute for the cached method counterpart.

        Returns (list):
            All exchanges names formatted in coinmarketcap.
        """
        res = self._get(b"https://s2.coinmarketcap.com/generated/search/quick_search_exchanges.json")
        return {exc["name"]: exc["slug"] for exc in loads(res)}

    @property
    def exchange_slugs(self):
        """Get all exchange raw names provided by coinmarketcap."""
        res = self._exchange_slugs
        if res:
            return res
        else:
            self._exchange_slugs = sorted(list(self.__exchange_names_slugs().values()))
            return self._exchange_slugs

    @property
    def total_exchanges(self):
        res = self._total_exchanges
        if res:
            return res
        else:
            self._total_exchanges = len(self.exchanges())
            return self._total_exchanges

    @property
    def converter_cache(self):
        res = self._converter_cache
        if res:
            return res
        else:
            self._converter_cache = [self.currency_exchange_rates, time()]
            return self._converter_cache

    cdef _get(self, char *url):
        """Internal function to make and HTTP GET request
        using the curl Cython bridge to C library or urllib
        standard library, depending on the installation."""
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

    # ====================================================================

                        #######   PUBLIC API   #######

    cpdef stats(self, convert="USD"):
        """ Get global cryptocurrencies statistics.

        Args:
            convert (str, optional): return 24h volume, and
                market cap in terms of another currency.
                See ticker_badges property to get valid values.
                As default ``"USD"``.

        Returns (dict):
            Global markets statistics.
        """
        return loads(self._get(
            b"https://api.coinmarketcap.com/v1/global/?convert=%s" % convert.encode()
        ))

    @property
    def ticker_badges(self):
        """Badges in wich you can convert prices in ``ticker()`` method."""
        return

    cpdef ticker(self, currency=None, limit=0, start=0, convert="USD"):
        """Get currencies with other aditional data.

        Args:
            currency (str, optional): Specify a currency to return data,
                that can be a symbol or coin slug (see ``symbols`` and ``coins``
                properties). In this case the method returns a dict, otherwise
                returns a list. If you dont specify a currency,
                returns data for all in coinmarketcap. As default, ``None``.
            limit (int, optional): Limit amount of coins on response.
                If ``limit == 0``, returns all coins in coinmarketcap.
                Only works if ``currency == None``. As default ``0``.
            start (int, optional): Rank of first currency to retrieve.
                The count starts at 0 for the first currency ranked.
                Only works if ``currency == None``. As default ``0``.
            convert (str, optional): Allows to convert prices, 24h volumes
                and market capitalizations in terms of one of badges
                returned by ``ticker_badges`` property. As default, ``"USD"``.

        Returns (dict/list):
            The type depends if currency param is provided or not.
        """
        cdef short i, len_i
        if not currency:
            url =  "https://api.coinmarketcap.com/v1/ticker/?limit=%d" % limit
            url += "&start=%d" % start
            url += "&convert=%s" % convert
            res = self._get(url.encode())
            response = loads(re_sub(r'"(-*\d+(?:\.\d+)?)"', r"\1", res))
            len_i = len(response)
            for i in range(len_i):
                response[i]["symbol"] = str(response[i]["symbol"])
        else:
            if self._is_symbol(currency):
                currency = self.correspondences[currency]
            url = "https://api.coinmarketcap.com/v1/ticker/%s" % currency
            url += "?convert=%s" % convert
            res = self._get(url.encode())
            response = loads(re_sub(r'"(-*\d+(?:\.\d+)?)"', r"\1", res))[0]
            response["symbol"] = str(response["symbol"])
        return response


    # ====================================================================

                       #######    WEB SCRAPER    #######

    @property
    def currency_exchange_rates(self):
        """Currency exchange rates against $ for all currencies (fiat + crypto).

        Returns (dict):
            All currencies rates used internally by coinmarketcap to calculate
            the prices shown.
        """
        res = self._get(b"https://coinmarketcap.com")
        rates = re_findall(r'data-([a-z]+)="(\d+\.*[\d|e|-]*)"', res[-10000:-2000])
        response = {currency.upper(): float(rate) for currency, rate in rates}
        for currency in self.ticker():
            try:
                response[currency["symbol"]] = float(currency["price_usd"])
            except TypeError:
                continue
        return response

    cpdef convert(self, value, unicode currency_in, unicode currency_out):
        """Convert prices between currencies. Provide a value, the currency
        of the value and the currency to convert it and get the value in
        currency converted rate. For see all available currencies to convert
        see ``currencies_to_convert`` property.

        Args:
            value (int/float): Value to convert betweeen two currencies.
            currency_in (str): Currency in which is expressed the value passed.
            currency_out (str): Currency to convert.

        Returns (float):
            Value expressed in currency_out parameter provided.
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
                fields ``total_markets_cap``, ``total_markets_volume_24h``
                and ``price`` between USD and BTC. As default ``"USD"``.

        Returns (dict):
            Aditional general metadata not supported by other methods.
        """
        response = {}
        if self._is_symbol(name):
            response["symbol"] = name
            name = self.correspondences[name]
            response["slug"] = name
        else:
            response["slug"] = name
            for symbol, slug in self.correspondences.items():
                if slug == name:
                    response["symbol"] = symbol
                    break
        convert = convert.lower()

        try:
            res = self._get(
                b"https://coinmarketcap.com/currencies/%s/" % name.encode()
            )[20000:]
        except CoinmarketcapHTTPError404:
            if name not in self.coins:
                raise ValueError("%s is not a valid currency name. See 'symbols' or 'coins'" % name \
                                 + " properties for get all valid currencies.")
            else:
                raise NotImplementedError

        response.update(processer.currency(res, convert))
        return response

    cpdef markets(self, unicode name, convert="USD"):
        """Get available coinmarketcap markets data.
        It needs a currency as argument.

        Args:
            currency (str): Currency to get market data.
            convert (str, optional): Currency to convert response
                fields ``volume_24h`` and ``price`` between USD
                and BTC. As default ``"USD"``.

        Returns (list):
            Markets on wich provided currency is currently tradeable.
        """
        response = {}
        if self._is_symbol(name):
            response["symbol"] = name
            name = self.correspondences[name]
            response["slug"] = name
        else:
            response["slug"] = name
            for symbol, slug in self.correspondences.items():
                if slug == name:
                    response["symbol"] = symbol
                    break
        convert = convert.lower()

        try:
            res = self._get(
                b"https://coinmarketcap.com/currencies/%s/" % name.encode()
            )[20000:]
        except CoinmarketcapHTTPError404:
            if name not in self.coins:
                raise ValueError("%s is not a valid currrency name. See 'symbols'" % name \
                                 + " or 'coins' properties for get all valid currencies.")
            else:
                raise NotImplementedError

        response["markets"] = processer.markets(res, convert)
        return response

    cpdef ranks(self):
        """Returns gainers and losers for 1 hour, 24 hours and 7 days.

        Returns (dict):
            A dictionary with 2 keys (gainers and losers) whose values
            are the periods ``"1h"``, ``"24h"`` and ``"7d"``.
        """
        res = self._get(b"https://coinmarketcap.com/gainers-losers/")

        return processer.ranks(res)

    def historical(self, unicode name,
                   start=datetime(2008, 8, 18),
                   end=datetime.now(),
                   revert=False):
        """Get historical data for a currency.

        Args:
            name (str): Currency to scrap historical data.
            start (date, optional): Time to start scraping
                periods as datetime.datetime type.
                As default ``datetime(2008, 8, 18)``.
            end (date, optional): Time to end scraping periods
                as datetime.datetime type. As default ``datetime.now()``.
            revert (bool, optional): If ``False``, return first date
                first, in chronological order, otherwise returns
                reversed list of periods. As default ``False``.

        Returns (list):
            Historical dayly OHLC for a currency.
        """
        response = {}

        if self._is_symbol(name):
            response["symbol"] = name
            response["slug"] = self.correspondences[name]
            name = response["slug"]
        else:
            response["slug"] = name
            for symbol, slug in self.correspondences.items():
                if slug == name:
                    response["symbol"] = symbol
                    break

        url = "https://coinmarketcap.com/currencies/%s/historical-data/" % name
        _start = "%d" % start.year + "%02d" % start.month + "%02d" % start.day
        _end = "%d" % end.year + "%02d" % end.month + "%02d" % end.day
        url += "?start=%s" % _start + "&" + "end=%s" % _end

        try:
            res = self._get(url.encode())[50000:]
        except CoinmarketcapHTTPError404:
            if name not in self.coins:
                raise ValueError("%s is not a valid currrency name. See 'symbols'" % name \
                                 + " or 'coins' properties for get all valid currencies.")
            else:
                raise NotImplementedError

        response["history"] = processer.historical(res, start, end, revert)
        return response

    def recently(self, convert="USD"):
        """Get recently added currencies along with other metadata.

        Args:
            convert (str, optional): Convert market_caps, prices,
                volumes and percent_changes between USD and BTC.
                As default ``"USD"``.

        Returns (list):
            Recently added currencies data.
        """
        convert = convert.lower()
        url = b"https://coinmarketcap.com/new/"
        res = self._get(url)

        return list(processer.recently(res, convert))

    cpdef exchange(self, unicode name, convert="USD"):
        """Obtain data from a exchange passed as argument. See ``exchanges_slugs``
        property for obtain all posibles values.

        Args:
            name (str): Exchange to retrieve data. Check ``exchange_slugs``
                instance attribute for get all posible values passed
                in this parameter.
            convert (str, optional): Convert prices and 24h volumes in
                return between USD and BTC. As default ``"USD"``.

        Returns (dict):
            Data from a exchange. Keys: ``"name"``, ``"website"``,
            ``"volume"`` (total), ``"social"`` and ``"markets"``.
        """
        url = "https://coinmarketcap.com/exchanges/%s/" % name
        try:
            res = self._get(url.encode())[20000:]
        except CoinmarketcapHTTPError404:
            if name not in self.exchange_slugs:
                raise ValueError("%s is not a valid exchange name. See exchange_slugs" % name \
                                 + " property for get all valid exchanges.")
            else:
                raise NotImplementedError
        else:
            response = {"slug": name}
        convert = convert.lower()

        response.update(processer.exchange(res, convert))
        return response

    cpdef exchanges(self, convert="USD"):
        """Get all the exchanges in coinmarketcap ranked by volumes
        along with other metadata.

        Args:
            convert (str, optional): Convert volumes and prices
                between USD and BTC. As default ``"USD"``.

        Returns (list):
            Exchanges with markets and other data included.
        """
        cdef bytes url
        url = b"https://coinmarketcap.com/exchanges/volume/24-hour/all/"
        res = self._get(url)[45000:]
        convert = convert.lower()
        return processer.exchanges(res, convert)

    cpdef tokens(self, convert="USD"):
        """Get data from platforms tokens

        Args:
            convert (str, optional): Convert ``"market_cap"``,
                ``"price"`` and ``"volume_24h"`` values between
                USD and BTC. As default ``"USD"``.

        Returns (list):
            Platforms tokens data.
        """
        url = b"https://coinmarketcap.com/tokens/views/all/"
        res = self._get(url)[40000:]
        convert = convert.lower()

        return processer.tokens(res, convert)

    # ====================================================================

                       #######   INTERNAL API   #######

    cpdef _currency(self, unicode name, start=None, end=None):
        """Get graphs data of a currency.

        Args:
            currency (str): Currency to retrieve graphs data.
            start (datetime, optional): Time to start retrieving
                graphs data in datetime. As default ``None``.
            end (datetime, optional): Time to end retrieving
                graphs data in datetime. As default ``None``.

        Returns (dict):
            Dict info with next keys: ``"market_cap_by_available_supply"``,
            ``"price_btc"``, ``"price_usd"``, ``"volume_usd":``
            and ``"price_platform"``.
            For each value, a list of lists where each one
            has two values [<datetime>, <value>]
        """
        if self._is_symbol(name):
            name = self.correspondences[name]

        url = b"https://graphs2.coinmarketcap.com/currencies/%s/" % name.encode()
        res = loads(self._get(url))

        return processer.graphs(res, start, end)

    cpdef _global_cap(self, bitcoin=True, start=None, end=None):
        """Get global market capitalization graphs, including
        or excluding Bitcoin.

        Args:
            bitcoin (bool, optional): Indicates if Bitcoin will
                be includedin global market capitalization graph.
                As default ``True``.
            start (int, optional): Time to start retrieving
                graphs data in datetime. As default ``None``.
            end (optional, datetime): Time to start retrieving
                graphs data in datetime. As default ``None``.

        Returns (dict):
            Whose values are lists of lists with timestamp and values,
            a data structure with the keys: ``"volume_usd"`` and
            ``"market_cap_by_available_supply"``.
        """
        if bitcoin:
            url = b"https://graphs2.coinmarketcap.com/global/marketcap-total/"
        else:
            url = b"https://graphs2.coinmarketcap.com/global/marketcap-altcoin/"

        res = loads(self._get(url))

        return processer.graphs(res, start, end)

    cpdef _dominance(self, start=None, end=None):
        """Get currencies dominance percentage graph

        Args:
            start (int, optional): Time to start retrieving
                graphs data in datetime. As default ``None``.
            end (optional, datetime): Time to start retrieving
                graphs data in datetime. As default ``None``.

        Returns (dict):
            Altcoins and dominance percentage values with timestamps.
        """
        url = b"https://graphs2.coinmarketcap.com/global/dominance/"

        res = loads(self._get(url))

        return processer.graphs(res, start, end)

    cpdef download_logo(self, unicode name, size=64, filename=None):
        """Download a currency image logo providing their size.

        Args:
            currency (str): Currency name or symbol to download.
            size (int, optional): Size in pixels. Valid sizes are:
                ``[16, 32, 64, 128, 200]``. As default ``128``.
            filename (str, optional): Filename for store the logo.
                Must be in ``.png`` extension. As default ``None``.

        Returns (str):
            Filename of downloaded file if all was correct.
        """
        if self._is_symbol(name):
            try:
                _name = self.ids_correspondences[name]
            except KeyError:
                if name not in list(self.ids_correspondences.keys()):
                    raise ValueError(
                        "The currency %s is not valid. See 'symbols' instance attribute." % name
                    )
        else:
            _name = name

        url_schema = "https://s2.coinmarketcap.com/static/img/coins/%dx%d/%d.png"
        url = url_schema % (size, size, _name)
        if not filename:
            filename = "%s_%dx%d.png" % (self.correspondences[name], size, size)
        try:
            res = urlretrieve(url, filename)
        except HTTPError as e:
            if e.code == 403:
                valid_sizes = [16, 32, 64, 128, 200]
                if size in valid_sizes:
                    raise ValueError(
                        ("Seems that %s currency doesn't allows to be downloaded with " \
                        + "size %dx%d. Try another size.") % (name, size, size)
                    )
                else:
                    raise ValueError("%dx%d is not a valid size." % (size, size))
            raise e
        else:
            return filename
