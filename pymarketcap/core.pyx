
"""API wraper and web scraper module."""

# Standard Python modules
import warnings
from re import (
    sub as re_sub,
    findall as re_findall
)
from time import time
from datetime import datetime
from json import loads
from urllib.request import urlretrieve
from urllib.error import HTTPError

# Internal Cython modules
from pymarketcap.curl import get_to_memory
from pymarketcap import processer

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


cdef class Pymarketcap:
    """Synchronous class for retrieve data from https://coinmarketcap.com.

    Args:
        timeout (int, optional): Set timeout value for requests.
            As default ``20``.
        debug: (bool, optional): Show low level data in get requests.
            As default, ``False``.
    """
    cdef readonly dict _cryptocurrencies
    cdef readonly list _cryptoexchanges
    cdef readonly list _currencies_to_convert
    cdef readonly list _converter_cache

    cdef public long timeout
    cdef public object graphs
    cdef public bint debug

    def __init__(self, timeout=15, debug=False):
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

    cpdef _quick_search(self, exchanges=False):
        """Retrieve internal pymarketcap JSON cache
        files :file:`quick_search.json` and
        :file:`quick_search_exchanges.json` from
        ``https://s2.coinmarketcap.com/generated/search/``
        endpoint.

        Args:
            exchanges (bool, optional): If ``True``, returns
                :file:`quick_search_exchanges.json` and other file
                otherwise.

        Returns (list):
            All cryptocurrencies or exchanges information
        """
        cdef bytes url
        if exchanges:
            url = b"https://s2.coinmarketcap.com/generated/search/quick_search_exchanges.json"
        else:
            url = b"https://s2.coinmarketcap.com/generated/search/quick_search.json"
        return loads(self._get(url))

    @property
    def cryptocurrencies(self):
        """Return all cryptocurrencies listed at coinmarketcap.
        This is the cached version of public API listings method
        but without low level fields like ``"data"`` and ``"metadata"``.
        """
        if not self._cryptocurrencies:
            self._cryptocurrencies = self.listings()
        return self._cryptocurrencies["data"]

    cpdef cryptocurrency_by_field_value(self, unicode field, unicode value):
        """Returns a currency listed given a field and value
        if ``field`` and ``value`` parameters matches for a currency,
        otherwise returns ``None``.

        Args:
            field (str): Valid criptocurrency data field. Valid data fields
                are ``"id"``, ``"name"``, ``"symbol"`` and ``"website_slug"``.
            value (str): Value to compare for defined currency field.

        Returns (dict):
            A currency with ``"id"``, ``"name"``, ``"symbol"``
            and ``"website_slug"`` and their values mapped if the currency
            was found, else ``None``.
        """
        for currency in self.cryptocurrencies:
            if currency[field] == value:
                return currency
        return None

    @property
    def cryptoexchanges(self):
        """Returns all exchanges listed at coinmarketcap,
        as dictionaries with ``"name"``, ``"id"`` and
        ``"website_slug"`` keys.
        """
        if not self._cryptoexchanges:
            response = []
            for exchange in self._quick_search(exchanges=True):
                response.append({
                    "name": exchange["name"],
                    "id":   exchange["id"],
                    "website_slug": exchange["slug"]
                })
            self._cryptoexchanges = response
        else:
            response = self._cryptoexchanges
        return response

    cpdef exchange_by_field_value(self, unicode field, unicode value):
        """Returns a exchange listed given a field and value
        if ``field`` and ``value`` parameters matches for a exchange,
        otherwise returns ``None``.

        Args:
            field (str): Valid exchange data field. Valid data fields
                are ``"id"``, ``"name"`` and ``"website_slug"``.
            value (str): Value to compare for defined exchange field.

        Returns (dict):
            A currency with ``"id"``, ``"name"`` and ``"website_slug"``
            and their values mapped if the exchange was found,
            otherwise returns ``None``.
        """
        for exchange in self.cryptoexchanges:
            if exchange[field] == value:
                return exchange
        return None

    cpdef field_type(self, value):
        """Get a field type between ``"name"``, ``"symbol"``,
        ``"id"`` or ``"website_slug"``given a value. This
        method maybe is not strict, but used with previous
        methods works fine.

        Args:
            value (any): Value to guess field type.
        """
        try:
            _value = int(value)
        except ValueError:
            if value.isupper():
                return "symbol"
            elif value.islower():
                return "website_slug"
            else:
                return "name"
        else:
            return "id"

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
        values in ``convert()`` method. Don't use this, but cached
        :attr:`~pymarketcap.core.Pymarketcap.currencies_to_convert`
        instance attribute instead.

        Returns (list):
            All currencies that could be passed to
            :meth:`~pymarketcap.core.Pymarketcap.convert`.
        """
        res = self._get(b"https://coinmarketcap.com")
        response = re_findall(r'data-([a-z]+)="\d', res[-15000:-2000])
        response.append("USD")
        response.extend(
            [currency["symbol"] for currency in self.cryptocurrencies]
        )
        return sorted([curr.upper() for curr in response])

    @property
    def converter_cache(self):
        res = self._converter_cache
        if res:
            return res
        else:
            self._converter_cache = [self.currency_exchange_rates, time()]
            return self._converter_cache

    cdef _get(self, char *url):
        """Internal function to make a HTTP GET request
        using the curl Cython bridge to C library or urllib
        standard library, depending of installation."""
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

                        #######   DEPRECATED   #######

    @property
    def coins(self):
        warnings.warn(
            "'coins()' method is deprecated. Use 'cryptocurrencies()' instead."
        )
        return [coin["website_slug"] for coin in self.cryptocurrencies]

    @property
    def symbols(self):
        warnings.warn(
            "'symbols()' method is deprecated. Use 'cryptocurrencies()' instead."
        )
        return [coin["symbol"] for coin in self.cryptocurrencies]

    @property
    def exchange_slugs(self):
        warnings.warn(
            "'exchange_slugs()' method is deprecated. Use 'exchanges()' instead."
        )
        return [exchange["website_slug"] for exchange in self.cryptoexchanges]

    @property
    def exchange_names(self):
        warnings.warn(
            "'exchange_names()' method is deprecated. Use 'exchanges()' instead."
        )
        return [exchange["name"] for exchange in self.cryptoexchanges]

    # ====================================================================

                        #######   PUBLIC API   #######

    cpdef listings(self):
        """List all criptocurrencies with their ids, names, symbol
        and website slug.

        .. seealso:

           `Coinmarketcap API documentation <https://coinmarketcap.com/api/>`__

        Returns (dict):
            Coinmarketcap API raw response.
        """
        return loads(self._get(b"https://api.coinmarketcap.com/v2/listings/"))

    cpdef stats(self, convert="USD"):
        """ Get global cryptocurrencies statistics.

        .. seealso:

           `Coinmarketcap API documentation <https://coinmarketcap.com/api/>`__

        Args:
            convert (str, optional): return 24h volume, and
                market cap in terms of another currency.
                See ``ticker_badges`` property to get valid values.
                As default ``"USD"``.

        Returns (dict):
            Global markets statistics on a raw response.
        """
        return loads(self._get(
            b"https://api.coinmarketcap.com/v2/global/?convert=%s" % convert.encode()
        ))

    @property
    def ticker_badges(self):
        """Badges in which you can convert prices in ``ticker()`` method."""
        return

    cpdef ticker(self, currency=None, limit=0, start=0, convert="USD"):
        """Get currencies with other aditional data.
        Only returns 100 currencies in each request. Use
        :py:meth:`pymarketcap.Pymarketcap.ticker_all` method
        for retrieve all currencies navegation through API
        pagination.


        .. seealso:

           `Coinmarketcap API documentation <https://coinmarketcap.com/api/>`__

        Args:
            currency (str, optional): Specify a currency to return data,
                that can be a ``name``, ``symbol``, ``id`` or
                ``website_slug`` fields from
                :py:class:`pymarketcap.core.Pymarketcap.cryptocurrencies`
                property. If you dont specify a currency, returns data
                for all in coinmarketcap. As default, ``None``.
            convert (str, optional): Allows to convert prices, 24h volumes
                and market capitalizations in terms of one of badges
                returned by ``ticker_badges`` property.
                As default, ``"USD"``.

        Returns (dict):
            Data from all currencies or a currency from coinmarketcap.
        """
        cdef short i, len_i
        if not currency:
            url =  "https://api.coinmarketcap.com/v2/ticker/?&convert=%s" % convert
            url += "&start=%d" % start
            url += "&limit=%s" % limit
            return loads(self._get(url.encode()))
        else:
            parms = (self.field_type(currency), currency)
            _id = self.cryptocurrency_by_field_value(*parms)["id"]
            url = "https://api.coinmarketcap.com/v2/ticker/%s" % _id
            url += "?convert=%s" % convert
            return loads(self._get(url.encode()))

    cpdef ticker_all(self, convert="USD"):
        """Get all currencies in coinmarketcap from
        :py:meth:`pymarketcap.Pymarketcap.ticker` method.
        Takes some time to be completed.

        Args:
            convert: (str, optional): Allows to convert prices, 24h volumes
                and market capitalizations in terms of one of badges
                returned by ``ticker_badges`` property.
                As default, ``"USD"``.

        Returns (list):
            All currencies metadata.
        """
        cdef short start = 1
        response = []

        num_cryptocurrencies = None
        while True:
            cryptocurrencies = self.ticker(start=start, convert="USD")
            if not num_cryptocurrencies:
                num_cryptocurrencies = \
                    cryptocurrencies["metadata"]["num_cryptocurrencies"]
            for curr in cryptocurrencies["data"].values():
                response.append(curr)
            start += 100
            if start > num_cryptocurrencies:
                break
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
        cdef short start = 1

        res = self._get(b"https://coinmarketcap.com")
        rates = re_findall(
            r'data-([a-z]+)="(\d+\.*[\d|e|-]*)"', res[-10000:-2000]
        )
        response = {currency.upper(): float(rate) for currency, rate in rates}

        # Ticker API method pagination
        num_cryptocurrencies = None
        while True:
            cryptocurrencies = self.ticker(start=start)
            if not num_cryptocurrencies:
                num_cryptocurrencies = \
                    cryptocurrencies["metadata"]["num_cryptocurrencies"]
            for _id, currency in cryptocurrencies["data"].items():
                symbol = cryptocurrencies["data"][_id]["symbol"]
                usd_price = cryptocurrencies["data"][_id]["quotes"]["USD"]["price"]
                if usd_price:
                    response[symbol] = usd_price
            start += 100
            if start > num_cryptocurrencies:
                break
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
        except KeyError as err:
            msg = "Invalid currency: '%s'. " \
                + "See currencies_to_convert instance attribute."
            for param in [currency_in, currency_out]:
                if param not in self.currencies_to_convert:
                    raise ValueError(msg % param)
            raise err

    cpdef currency(self, unicode curr, convert="USD"):
        """Get currency metadata like total markets capitalization,
        websites, source code link, if mineable...

        Args:
            curr (str): Currency to get metadata. Can be a ``name``,
                ``symbol``, ``id`` or ``website_slug`` fields from
                :class:`pymarketcap.core.Pymarketcap.cryptocurrencies`.
            convert (str, optional): Currency to convert response
                fields ``total_markets_cap``, ``total_markets_volume_24h``
                and ``price`` between USD and BTC. As default ``"USD"``.

        Returns (dict):
            Aditional general metadata not supported by other methods.
        """
        parms = (self.field_type(curr), curr)
        response = self.cryptocurrency_by_field_value(*parms)
        if not response:
            raise ValueError(
                "Any cryptocurrency found matching %s == %r." % parms
            )
        else:
            curr = response["website_slug"]

        res = self._get(
            b"https://coinmarketcap.com/currencies/%s/" % curr.encode()
        )[20000:]

        response.update(processer.currency(res, convert.lower()))
        return response

    cpdef exchange(self, unicode exc, convert="USD"):
        """Obtain data from a exchange passed as argument.
        See :class:`pymarketcap.core.Pymarketcap.cryptoexchanges`
        property for obtain all posibles values.

        Args:
            exc (str): Exchange to retrieve data. Can be a ``name``,
                ``id`` or ``website_slug`` fields from
                :py:class:`pymarketcap.core.Pymarketcap.cryptoexchanges`.
            convert (str, optional): Convert prices and 24h volumes in
                return between USD and BTC. As default ``"USD"``.

        Returns (dict):
            Data from a exchange. Fields: ``"currency"``,
            ``"pair"``, ``"name"``, ``"volume_24h"`` (total),
            ``"price"``, ``"percent_volume"``, ``"updated"``.
            ``"slug"``, ``"website_slug"``, ``"id"``,
            ``"volume"``, ``"markets"``.
        """
        parms = (self.field_type(exc), exc)
        response = self.exchange_by_field_value(*parms)
        if not response:
            raise ValueError(
                "Any exchange found matching %s == %r." % parms
            )
        else:
            exc = response["website_slug"]

        res = self._get(
            b"https://coinmarketcap.com/exchanges/%s/" % exc.encode()
        )[20000:]

        response.update(processer.exchange(res, convert.lower()))
        return response

    cpdef exchanges(self, convert="USD"):
        """Get all exchanges in coinmarketcap ranked by volumes
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
        return processer.exchanges(res, convert.lower())

    cpdef historical(self, unicode curr,
                     start=datetime(2008, 8, 18),
                     end=datetime.now(),
                     revert=False):
        """Get historical data for a currency.

        Args:
            curr (str): Currency to scrap historical data.
                Can be a ``name``,  ``"symbol"``, ``id``
                or ``website_slug`` fields from
                :py:class:`pymarketcap.core.Pymarketcap.cryptocurrencies`.
            start (date, optional): Time to start scraping
                periods as datetime.datetime type.
                As default :py:func:`datetime.datetime(2008, 8, 18)`.
            end (date, optional): Time to end scraping periods
                as datetime.datetime type. As default
                :py:func:`datetime.datetime.now()`.
            revert (bool, optional): If ``False``, return first date
                first, in chronological order, otherwise returns
                reversed list of periods. As default ``False``.

        Returns (list):
            Historical dayly OHLC for a currency.
        """
        parms = (self.field_type(curr), curr)
        response = self.cryptocurrency_by_field_value(*parms)
        if not response:
            raise ValueError(
                "Any cryptocurrency found matching %s == %r." % parms
            )
        else:
            curr = response["website_slug"]

        url = "https://coinmarketcap.com/currencies/%s/historical-data/" % curr
        _start = "%d" % start.year + "%02d" % start.month + "%02d" % start.day
        _end = "%d" % end.year + "%02d" % end.month + "%02d" % end.day
        url += "?start=%s" % _start + "&" + "end=%s" % _end

        res = self._get(url.encode())[50000:]
        response["history"] = processer.historical(res, start, end, revert)
        return response

    cpdef markets(self, unicode curr, convert="USD"):
        """Get available coinmarketcap markets data for a currency.

        Args:
            curr (str): Currency to get market data.
                Can be a ``name``,  ``"symbol"``, ``id``
                or ``website_slug`` fields from
                :py:class:`pymarketcap.core.Pymarketcap.cryptocurrencies`.
            convert (str, optional): Currency to convert response
                fields ``volume_24h`` and ``price`` between USD
                and BTC. As default ``"USD"``.

        Returns (list):
            Markets on wich provided currency is currently tradeable.
        """
        parms = (self.field_type(curr), curr)
        response = self.cryptocurrency_by_field_value(*parms)
        if not response:
            raise ValueError(
                "Any cryptocurrency found matching %s == %r." % parms
            )
        else:
            curr = response["website_slug"]

        res = self._get(
            b"https://coinmarketcap.com/currencies/%s/" % curr.encode()
        )[20000:]

        response["markets"] = processer.markets(res, convert.lower())
        return response

    cpdef ranks(self):
        """Returns gainers and losers for 1 hour, 24 hours and 7 days.

        Returns (dict):
            A dictionary with 2 keys (gainers and losers) whose values
            are the periods ``"1h"``, ``"24h"`` and ``"7d"``.
        """
        res = self._get(b"https://coinmarketcap.com/gainers-losers/")
        return processer.ranks(res)

    cpdef recently(self, convert="USD"):
        """Get recently added currencies along with other metadata.

        Args:
            convert (str, optional): Convert market_caps, prices,
                volumes and percent_changes between USD and BTC.
                As default ``"USD"``.

        Returns (list):
            Recently added currencies data.
        """
        res = self._get(b"https://coinmarketcap.com/new/")
        return list(processer.recently(res, convert.lower()))

    cpdef tokens(self, convert="USD"):
        """Get data from platforms tokens

        Args:
            convert (str, optional): Convert ``"market_cap"``,
                ``"price"`` and ``"volume_24h"`` values between
                USD and BTC. As default ``"USD"``.

        Returns (list):
            Platforms tokens data.
        """
        res = self._get(
            b"https://coinmarketcap.com/tokens/views/all/"
        )[40000:]
        return processer.tokens(res, convert.lower())

    # ====================================================================

                       #######   GRAPHS API   #######

    cpdef _currency(self, unicode curr, start=None, end=None):
        """Get graphs data of a currency.

        Args:
            curr (str): Currency to retrieve graphs data.
            start (datetime, optional): Time to start retrieving
                graphs data in datetime type. As default ``None``.
            end (datetime, optional): Time to end retrieving
                graphs data in datetime type. As default ``None``.

        Returns (dict):
            Dict info with next keys: ``"market_cap_by_available_supply"``,
            ``"price_btc"``, ``"price_usd"``, ``"volume_usd":``
            and ``"price_platform"``.
            For each value, a list of lists where each one
            has two values [<datetime>, <value>]
        """
        parms = (self.field_type(curr), curr)
        response = self.cryptocurrency_by_field_value(*parms)
        if not response:
            raise ValueError(
                "Any cryptocurrency found matching %s == %r." % parms
            )
        else:
            curr = response["website_slug"]

        url = b"https://graphs2.coinmarketcap.com/currencies/%s/" % curr.encode()
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
        res = loads(self._get(
            b"https://graphs2.coinmarketcap.com/global/dominance/")
        )
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
        cdef bytes url
        url = b"https://graphs2.coinmarketcap.com/global/marketcap-altcoin/"
        if bitcoin:
            url = b"https://graphs2.coinmarketcap.com/global/marketcap-total/"

        res = loads(self._get(url))
        return processer.graphs(res, start, end)

    # ====================================================================

                       #######   INTERNAL API   #######

    cpdef download_logo(self, unicode curr, size=64, filename=None):
        """Download a currency image logo providing their size.

        Args:
            curr (str): Currency name, id, website_slug or symbol
                to download.
            size (int, optional): Size in pixels. Valid sizes are:
                ``[16, 32, 64, 128, 200]``. As default ``128``.
            filename (str, optional): Filename for store the logo.
                Doesn't include the extension (will be ".png").
                As default ``None``.

        Returns (str):
            Filename of downloaded file if all was correct.
        """
        parms = (self.field_type(curr), curr)
        response = self.cryptocurrency_by_field_value(*parms)
        if not response:
            raise ValueError(
                "Any cryptocurrency found matching %s == %r." % parms
            )
        else:
            _id = response["id"]

        url_schema = "https://s2.coinmarketcap.com/static/img/coins/%dx%d/%d.png"
        url = url_schema % (size, size, _id)
        if not filename:
            filename = "%s_%dx%d.png" % (response["website_slug"], size, size)
        try:
            res = urlretrieve(url, filename)
        except HTTPError as e:
            if e.code == 403:
                valid_sizes = [16, 32, 64, 128, 200]
                if size in valid_sizes:
                    raise ValueError(
                        ("Seems that %s currency doesn't allows to be " \
                         + "downloaded with size %dx%d. Try another size.") \
                             % (response["website_slug"], size, size)
                    )
                else:
                    raise ValueError("%dx%d is not a valid size." % (size, size))
            raise e
        else:
            return filename

    cpdef download_exchange_logo(self, unicode exc, size=64, filename=None):
        """Download a exchange logo passing his name or
        id or website slug as first parameter and
        optionally a filename without extension.

        Args:
            exc (str): Exchange name, id or website slug
                to download.
            size (int): Size in pixels. Valid values are:
                ``[16, 32, 64, 128, 200]``.
            filename (str, optional): Filename for store the logo,
                without include file extension (will be ".png").
                As default ``None``.

        Returns (str):
            Filename of downloaded file if all was correct.
        """
        parms = (self.field_type(exc), exc)
        response = self.exchange_by_field_value(*parms)
        if not response:
            raise ValueError(
                "Any exchange found matching %s == %r." % parms
            )
        else:
            _id = response["id"]
            _website_slug = response["website_slug"]

        filename = "%s_%dx%d.png" % (_website_slug, size, size) \
            if not filename else "%s.png" % filename

        url = "https://s2.coinmarketcap.com/static/img/exchanges/%dx%d/%s.png" % \
             (size, size, _id)

        try:
            res = urlretrieve(url, filename)
        except HTTPError as e:
            if e.code == 403:
                valid_sizes = [16, 32, 64, 128, 200]
                if size in valid_sizes:
                    raise ValueError(
                        ("Seems that %s exchange doesn't allows to be " \
                         + "downloaded with size %dx%d. Try another size.")  \
                            % (_website_slug, size, size)
                    )
                else:
                    raise ValueError("%dx%d is not a valid size." % (size, size))
            raise e
        else:
            return filename
