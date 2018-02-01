#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Pymarketcap core, web parser and API wrapper"""

# Python standard library
from datetime import datetime
from re import sub
from re import compile as re_compile
from decimal import Decimal, InvalidOperation
try:
    from json import JSONDecodeError
except ImportError:
    try:
        from simplejson import JSONDecodeError
    except ImportError:
        pass

# Third party libraries
from requests import Session
from requests.compat import urljoin, urlencode
from bs4 import BeautifulSoup, FeatureNotFound

# Internal modules:
from .errors import (
    CoinmarketcapHTTPError,
    CoinmarketcapCurrencyNotFoundError,
    CoinmarketcapTooManyRequestsError
)

# Global variables
ANY_REG = re_compile(r".*") # Any value regex

class Pymarketcap(object):
    """Main class for retrieve data from coinmarketcap.com

    Args:
        parse_float (any, optional): Parser used by json.loads()
            for retrieve float type data. As default, decimal.Decimal
        parse_int (any, optional): Parser used by json.loads()
            for retrieve int type data. As default, int
        pair_separator (str, optional): Separator between base and
            quote pair in responses. As default "-"
            (ie: ``pair_separator="_"`` -> ``"BTC_USD"``)
        timeout (float, optional): Add timeout for get requests.
            As default 20.
        proxies (dict, optional): Add proxies to be used for get requests.
            See http://docs.python-requests.org/en/master/user/advanced/#proxies
            for details. As default {}.
    """
    def __init__(self, parse_float=Decimal,
                 parse_int=int, pair_separator="-",
                 timeout=20, proxies=None):
        self.urls = dict(
            api="https://api.coinmarketcap.com/v1/",
            web="https://coinmarketcap.com/",
            graphs_api="https://graphs2.coinmarketcap.com/"
        )
        self.parse_float = parse_float
        self.parse_int = parse_int
        self.pair_separator = pair_separator

        self.session = Session()
        self.timeout = timeout

        self.proxies = proxies or {}

        # Information attributes
        self.correspondences = self._cache_symbols()
        self.coins = list(self.correspondences.values())
        self.symbols = list(self.correspondences.keys())

        # Graphs API sugar syntax
        self.graphs = type("Graphs", (), self._graphs_interface)


    ######   RUNTIME INIT   #######

    @property
    def _graphs_interface(self):
        """Sugar syntax for graphs API methods"""
        return {
            "currency": self.currency,
            "global_cap": self.global_cap,
            "dominance": self.dominance
        }

    def _cache_symbols(self):
        """Internal function for load in cache al symbols
        in coinmarketcap with their respectives currency names"""
        self._exceptional_coin_slugs = {
            "42": "42-coin",
            "808": "808coin",
            "611": "sixeleven",
            "300": "300-token",
            "888": "octocoin",
            "$$$": "money",
            "BTBc": "bitbase",
        }
        response = {}
        url = "https://files.coinmarketcap.com/generated/search/quick_search.json"
        currencies = self.session.get(url, proxies=self.proxies).json()
        for currency in currencies:
            response[currency["symbol"]] = currency["slug"].replace(" ", "")
        for original, correct in self._exceptional_coin_slugs.items():
            response[original] = correct
        return response

    def is_symbol(self, currency):
        # Improve velocity (`if currency in self.symbols` is slower)
        if currency.isupper() or currency in self._exceptional_coin_slugs.keys():
            return True
        return False

    #######   API METHODS   #######

    def ticker(self, currency=None, convert=None, limit=None):
        """Get currencies with other aditional data.

        Args:
            currency (str, optional): Specify a currency to return,
                in this case the method returns a dict, otherwise
                returns a list. As default, None.
            convert (str, optional): As default, None. Allow to
                convert prices in response on one of next badges:
                ["AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK",
                "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY",
                "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN",
                "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR", "USD"]
            limit (int, optional): Limit amount of coins on response.
                Only works if ``currency == None``.

        Returns:
            dict/list: If currency param is provided or not.

        """
        if not convert:
            convert = "USD"

        url = urljoin(self.urls["api"], "ticker/")

        if currency:
            if self.is_symbol(currency):
                currency = self.correspondences[currency]
            url += "%s/" % currency

        params = dict(convert=convert)
        if limit:
            params["limit"] = limit

        url += "?" + urlencode(params)

        def parse_currency(raw_data):
            """Internal function to parse every currency
            in the provided types in constructor

            Args:
                raw_data: Response provided by the API on ticker method

            Returns:
                dict: Parsed values
            """
            value_types = {
                'price_btc': self.parse_float,
                'price_usd': self.parse_float,
                'percent_change_7d': self.parse_float,
                'percent_change_1h': self.parse_float,
                'name': str,
                'percent_change_24h': self.parse_float,
                'market_cap_usd': self.parse_float,
                'market_cap_%s' % convert.lower(): self.parse_float,
                'last_updated': self.parse_int,
                'rank': self.parse_int,
                'available_supply': self.parse_float,
                'price_%s' % convert.lower(): self.parse_float,
                'symbol': str,
                '24h_volume_%s' % convert.lower(): self.parse_float,
                '24h_volume_usd': self.parse_float,
                'total_supply': self.parse_float,
                'max_supply': self.parse_float,
                'id': str
            }

            data = {}
            for key, value in raw_data.items():
                try:
                    data[key] = value_types[key](value)
                except (TypeError, KeyError):
                    data[key] = None
            return data

        req = self.session.get(url, proxies=self.proxies, timeout=self.timeout)
        try:
            data = req.json()
        except JSONDecodeError as error:
            if req.status_code == 429: # Too many requests
                raise CoinmarketcapTooManyRequestsError(429, "Too many requests")
            print(error)
            print(url)
            print(data)
            print("If you see this error report it to " + \
                "https://github.com/mondeja/pymarketcap/issues")
            print(currency)
            import sys
            sys.exit(1)

        if currency:
            try:
                response = parse_currency(data[0])
            except KeyError as error:  # Id currency error?
                if type(data) is dict:
                    try:
                        msg = data["error"]
                    except KeyError:
                        raise error
                    else:
                        if msg == "id not found":
                            raise CoinmarketcapCurrencyNotFoundError(currency, url)

                        else:
                            raise Exception(data["error"])
                else:
                    raise error
        else:
            response = []
            for curr in data:
                response.append(parse_currency(curr))

        return response


    def stats(self):
        """ Get global cryptocurrencies statistics.

        Returns:
            dict: Global markets statistics
        """
        url = urljoin(self.urls["api"], 'global/')
        req = self.session.get(url, proxies=self.proxies, timeout=self.timeout)
        if req.status_code == 200:
            response = req.json(parse_int=self.parse_int,
                                parse_float=self.parse_float)
        else:
            raise CoinmarketcapHTTPError(req.status_code,
                                         "%s not found" % url)
        return response


    #######    WEB PARSER METHODS    #######

    def _html(self, url):
        """Internal function for get plain html pages

        Args:
            url: Url page to obtain plain html code

        Raises:
            CoinmarketcapError: if status code is not equal to 200

        Returns:
            str: Plain html parsed with BeautifulSoup html parser
        """
        req = self.session.get(url, proxies=self.proxies, timeout=self.timeout)
        status_code = req.status_code
        if status_code == 200:
            try:
                return BeautifulSoup(req.text, "lxml")
            except FeatureNotFound:
                return BeautifulSoup(req.text, "html.parser")
        else:
            raise CoinmarketcapHTTPError(status_code, url)

    def _select(self, html, selector, attribute=None):
        """Internal function to avoid redundant error checking code when
        using CSS selectors."""
        try:
            el = html.select(selector)[0]
            return el[attribute].strip() if attribute else el.getText().strip()
        except (IndexError, KeyError):
            return None

    def markets(self, currency):
        """Get available coinmarketcap markets data.
        It needs a currency as argument.

        Args:
            currency (str): Currency to get market data

        Returns:
            list: markets on wich provided currency is currently tradeable
        """
        if self.is_symbol(currency):
            currency = self.correspondences[currency]

        url = urljoin(self.urls["web"], "currencies/%s/" % currency)
        html = self._html(url)

        # Updated field regex
        updated_field_reg = re_compile(r"text-right .*")

        response = []
        marks = html.find(id="markets-table").find("tbody").find_all('tr')

        for m in marks:
            _volume_24h = m.find(class_="volume").getText()
            _volume_24h = _volume_24h.replace("*", "").replace(".", "").replace(",", "")
            volume_24h = self.parse_int(_volume_24h.replace("$", "").replace("\n", ""))
            _price = m.find(class_="price").getText()
            _price = _price.replace("$", "").replace(" ", "").replace("*", "")
            price = self.parse_float(_price.replace(",", ""))
            pair_exc = m.find_all("a")
            exchange = pair_exc[0].getText()
            pair = pair_exc[1].getText()

            _percent_volume = m.find("span", {"data-format-percentage": ANY_REG})
            percent_volume = self.parse_float(_percent_volume.getText().replace("%", ""))
            updated = m.find(class_=updated_field_reg).getText() == "Recently"

            market = {'exchange': exchange, 'pair': pair,
                      '24h_volume_usd': volume_24h,
                      'price_usd': price,
                      'percent_volume': percent_volume,
                      "updated": updated}
            response.append(market)

        return response

    def _get_ranks(self, query, temp):
        """Internal function for get gainers and losers

        Args:
            query: Query to obtain ranks, gainers or losers
            temp: Temporal period obtaining gainers or losers,
                1h, 24h or 7d
        """
        url = urljoin(self.urls["web"], 'gainers-losers/')
        html = self._html(url)

        call_reg = re_compile(query + '-' + temp)
        percent_reg = re_compile("percent-" + temp)

        response = []
        html_rank = html.find('div', {'id': call_reg}).find_all('tr')

        for curr in html_rank[1:]:
            name = curr.find(class_="currency-name").find("a").getText()
            symbol = curr.find(class_="text-left").getText()
            _volume_24h = curr.find(class_="volume").getText()
            _volume_24h = _volume_24h.replace("$", "").replace(",", "")
            volume_24h = self.parse_int(_volume_24h)
            _price = curr.find(class_="price").getText()
            _price = _price.replace("$", "").replace(",", "")
            price = self.parse_float(_price)
            _percent = curr.find(class_=percent_reg).getText().replace("%", "")
            percent = self.parse_float(_percent)
            currency = {'symbol': symbol, 'name': name,
                        '24h_volume_usd': volume_24h,
                        'price_usd': price, 'percent_change': percent}
            response.append(currency)
        return response

    def ranks(self, *args):
        """Returns data from gainers and losers rankings:

        Args:
            *args (str, optional): Positional arguments
                for filter rankings. Valid arguments:
                     ['7d', '24h', '1h', 'gainers', 'losers']

        Returns:
            dict: Gainers, losers or both rankings, depends of arguments filter
        """
        all_temps = ['1h', '24h', '7d']
        all_queries = ['gainers', 'losers']

        if not args:   # if len(args) == 0
            temps, queries = (all_temps, all_queries)
        else:
            temps, queries = ([], [])
            for a in args:
                if a in all_temps:
                    temps.append(a)
                elif a in all_queries:
                    queries.append(a)
                else:
                    msg = '%s is not a valid argument' % a
                    raise AttributeError(msg)

            if not temps:
                temps = all_temps
            if not queries:
                queries = all_queries

        response = {}
        for q in queries:
            rankings = {}
            for t in temps:
                ranking = self._get_ranks(q, t)
                rankings[t] = ranking
            if len(queries) > 1:
                response[q] = rankings
            else:
                response = rankings

        return response

    def historical(self, currency, start=None,
                   end=None, revert=False):
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

        Return:
            list: Historical dayly results for a currency
        """
        if not start: start = datetime(2008, 8, 18)
        if not end: end = datetime.now()

        if self.is_symbol(currency):
            currency = self.correspondences[currency]

        url = self.urls["web"] + 'currencies/' + currency + '/historical-data/'
        url += '?start={}&end={}'.format(
            str(start.year) + "%02d" % start.month + "%02d" % start.day,
            str(end.year) + "%02d" % end.month + "%02d" % end.day
        )
        html = self._html(url)

        response = []
        marks = html.find('tbody').find_all('tr')

        for m in marks:
            insert = True # Ignore all dates not in range
            _childs, childs = (m.contents, [])
            for c in _childs:
                if c != '\n':
                    childs.append(c)
            indicators = {}
            for n, c in enumerate(childs):
                if n == 0:
                    _date = c.getText().replace(',', '')
                    try:
                        date = datetime.strptime(_date, '%b %d %Y')
                    except ValueError:
                        date = _date #datetime.strptime('Jan 01 0001', '%b %d %Y')
                    else:
                        if date < start or date > end:
                            insert = False
                            break
                    indicators['date'] = date
                if n == 1:
                    _open = self.parse_float(c.getText())
                    indicators['open'] = _open
                if n == 2:
                    _high = self.parse_float(c.getText())
                    indicators['high'] = _high
                if n == 3:
                    _low = self.parse_float(c.getText())
                    indicators['low'] = _low
                if n == 4:
                    _close = self.parse_float(c.getText())
                    indicators['close'] = _close
                if n == 5:
                    _usd_volume = c.getText().replace(',', '')
                    try:
                        _usd_volume = self.parse_int(_usd_volume)
                    except ValueError:
                        pass
                    indicators['usd_volume'] = _usd_volume
                if n == 6:
                    _usd_market_cap = c.getText().replace(',', '')
                    try:
                        _usd_market_cap = self.parse_int(_usd_market_cap)
                    except ValueError:
                        pass
                    indicators['usd_market_cap'] = _usd_market_cap
            if insert:
                response.append(indicators)

        if not revert:
            response.reverse()

        return response

    def recently(self):
        """Get recently added currencies along
        with other metadata

        Returns:
            list: Recently added currencies
        """
        url = urljoin(self.urls["web"], 'new/')

        html = self._html(url)

        response = []
        marks = html.find('tbody').find_all('tr')
        for m in marks:
            _childs, childs = (m.contents, [])
            for c in _childs:
                if c != '\n':
                    childs.append(c)
            for n, c in enumerate(childs):
                if n == 0:
                    name = str(c.getText().replace('\n', ''))
                elif n == 1:
                    symbol = str(c.getText())
                elif n == 2:
                    days_ago = sub(r'\D', '', c.getText())
                    try:
                        days_ago = self.parse_int(days_ago)
                    except ValueError:
                        pass
                elif n == 3:
                    _usd_market_cap = c.getText().replace('\n', '').replace("$", "")
                    usd_market_cap = _usd_market_cap.replace(' ', '').replace(",", "")
                elif n == 4:
                    price_usd = c.getText()
                    try:
                        price_usd = self.parse_float(sub(r' |\$|\n', '', price_usd))
                    except InvalidOperation:
                        pass
                elif n == 5:
                    circulating_supply = c.getText().replace('\n', '').replace(' ', '')
                    if '*' in circulating_supply:
                        circulating_supply = circulating_supply.replace('*', '')
                        mineable = True
                    else:
                        mineable = False
                    if '?' not in circulating_supply:
                        _circulating_supply = circulating_supply.replace(',', '')
                        circulating_supply = self.parse_int(_circulating_supply)
                elif n == 6:
                    _volume_24h_usd = c.getText().replace('\n', '').replace("$", "")
                    volume_24h_usd = _volume_24h_usd.replace(",", "")
                    if volume_24h_usd != 'Low Vol':
                        try:
                            volume_24h_usd = self.parse_int(volume_24h_usd)
                        except ValueError:
                            pass
                elif n == 7:
                    percent_change = c.getText().replace(' %', '')
                    if '?' not in percent_change:
                        percent_change = self.parse_float(percent_change)
            indicators = {'name': name,
                          'symbol': symbol,
                          'days_ago': days_ago,
                          'usd_market_cap': usd_market_cap,
                          'price_usd': price_usd,
                          'circulating_supply': circulating_supply,
                          'mineable': mineable,
                          'volume_24h_usd': volume_24h_usd}
            response.append(indicators)

        return response

    @property
    def exchange_names(self):
        """Get all exchange names available
        currently in coinmarketcap.

        Returns:
            list: All exchanges in coinmarketcap.

        """
        exchanges = self.exchanges(limit=None)
        response = []
        for exchange in exchanges:
            exch = exchange["name"]
            if exch not in response:
                response.append(exch)
        return response

    def exchange(self, name, metadata=False):
        """Obtain data from a exchange passed as argument

        Example:
            exchange('poloniex')

        Args:
            name (str): Exchange to retrieve data
            metadata (bool): Include formatted name, website
                and twitter links for the exchange. False as default

        Returns:
            list/dict (if metadata == False/True):
                Data from all markets in a exchange
        """
        url = urljoin(self.urls["web"], 'exchanges/%s/' % name)
        html = self._html(url)

        marks = html.find('table').find_all('tr')

        response = []

        if metadata:
            response = {
                'markets': []
            }

            response['formatted_name'] = self._select(html, 'h1.text-large')
            response['website'] = self._select(html, 'span[title=Website] + a', 'href')
            response['twitter'] = self._select(html, 'img[alt=Twitter] + a', 'href')

        for m in marks[1:]:
            _childs, childs = (m.contents, [])
            for c in _childs:
                if c != '\n':
                    childs.append(c)
            for n, c in enumerate(childs):
                if n == 0:
                    rank = self.parse_int(c.getText())
                elif n == 1:
                    name = c.getText()
                elif n == 2:
                    market = c.getText().replace('/', self.pair_separator)
                elif n == 3:
                    _volume_24h_usd = c.getText().replace(" ", "").replace("*", "")
                    _volume_24h_usd = _volume_24h_usd.replace("$", "").replace(",", "")
                    volume_24h_usd = self.parse_int(_volume_24h_usd)
                elif n == 4:
                    _price_usd = c.getText().replace("$", "").replace("*", "")
                    price_usd = self.parse_float(_price_usd.replace(" ", ""))
                elif n == 5:
                    _perc_volume = c.getText().replace('%', '')
                    perc_volume = self.parse_float(_perc_volume)
            indicators = {'rank': rank,
                          'name': name,
                          'market': market,
                          'volume_24h_usd': volume_24h_usd,
                          'price_usd': price_usd,
                          'perc_volume': perc_volume}
            markets = response['markets'] if metadata else response

            markets.append(indicators)

        return response

    def exchanges(self, limit=50):
        """Get all the exchanges markets data
        in coninmarketcap ranked by volumes.

        Args:
            limit (int, optional): Limit the amount
                of exchanges in response. As default, 50.

        Returns:
            list: Markets by exchanges and volumes
        """
        url = urljoin(self.urls["web"], 'exchanges/volume/24-hour/all/')
        html = self._html(url)

        exs = html.find('table').find_all('tr') # Exchanges
        response = []
        for e in exs:
            try:
                exchange = e['id']
            except KeyError:
                if 'Pair' not in str(e):
                    if 'Total' in str(e):
                        _total = sub(r'\$|,|Total', '', e.getText())
                        total = self.parse_int(_total)
                        exchange_data['volume_usd'] = total
                    if 'View More' in str(e):
                        pass
                    else:
                        # In this case is market data
                        _childs, childs = (e.contents, [])
                        for c in _childs:
                            if c != '\n' and 'Total' not in str(c) \
                                        and 'bold text-right volume' not in str(c) \
                                        and str(c) != '<td></td>':
                                childs.append(c)
                        for n, c in enumerate(childs):
                            if n == 0:
                                rank = self.parse_int(c.getText())
                            elif n == 2:
                                market = str(c.getText())
                            elif n == 3:
                                volume_24h_usd = self.parse_int(
                                    c.getText().replace('$', '').replace(',', '')
                                )
                            elif n == 4:
                                price_usd = self.parse_float(
                                    c.getText().replace('$', '').replace(',', '')
                                )
                            elif n == 5:
                                perc_change = self.parse_float(
                                    c.getText().replace('%', '')
                                )

                        market_data = {'rank': rank,
                                       'market': market,
                                       'volume_24h_usd': volume_24h_usd,
                                       'price_usd': price_usd,
                                       'perc_change': perc_change}
                        exist = False
                        for _market_data in exchange_data['markets']:
                            if market_data['rank'] == _market_data['rank']:
                                exist = True
                        if not exist:
                            exchange_data['markets'].append(market_data)
            else:
                try:
                    response.append(exchange_data)
                except UnboundLocalError:
                    pass
                else:
                    if limit and len(response) >= limit:
                        break
                # In this case is the exchange name
                exchange_data = {}
                rank = int(sub(r'\D', '', e.getText()))
                exchange_data['rank'] = rank
                # We create a dict where we will save the markets data
                exchange_data['name'] = exchange
                exchange_data['markets'] = []

                exchange_data['formatted_name'] = self._select(
                    e, '.volume-header a')

        return response


    #######   GRAPHS API METHODS   #######

    @staticmethod
    def _parse_start_end(start, end):
        """Internal function for parse start and end datetimes"""
        return (
            str(int(start.timestamp())*1000),
            str(int(end.timestamp())*1000)
        )

    @staticmethod
    def _add_start_end(url, start, end):
        """Internal function for add start and end to url"""
        start, end = Pymarketcap._parse_start_end(start, end)
        return "%s/%s/" % (start, end)


    def currency(self, currency, start=None, end=None):
        """Get graphs data of a currency.

        Args:
            currency (str): Currency to retrieve graphs data.
            start (optional, datetime): Time to start retrieving
                graphs data. If not provided get As default None
            end (optional, datetime): Time to end retrieving
                graphs data.

        Returns (dict):
            Dict info with next keys:
            `
                {"market_cap_by_available_supply": [...],
                 "price_btc": [...],
                 "price_usd": [...],
                 "volume_usd": [...]
                 }
            `
            and for each key, a list of lists where each one
            has two values [<timestamp>, <value>]
        """
        if self.is_symbol(currency):
            currency = self.correspondences[currency]
        url = self.urls["graphs_api"] + "currencies/%s/" % currency

        if start and end:
            url += Pymarketcap._add_start_end(url, start, end)

        return self.session.get(url, proxies=self.proxies, timeout=self.timeout).json()

    def global_cap(self, bitcoin=True, start=None, end=None):
        """Get global market capitalization graphs, including
        or excluding Bitcoin

        Args:
            bitcoin (bool, optional): Indicates if Bitcoin will
                be includedin global market capitalization graph.
                As default True
            start (optional, datetime): Time to start retrieving
                graphs data. If not provided get As default None
            end (optional, datetime): Time to end retrieving
                graphs data.

        Returns (dict):
            List of lists with timestamp and values
        """
        base_url = self.urls["graphs_api"]
        if bitcoin:
            endpoint = "global/marketcap-total/"
        else:
            endpoint = "global/marketcap-altcoin/"
        url = urljoin(base_url, endpoint)

        if start and end:
            url += Pymarketcap._add_start_end(url, start, end)

        return self.session.get(url, proxies=self.proxies, timeout=self.timeout).json()

    def dominance(self, start=None, end=None):
        """Get currencies dominance percentage graph

        Args:
            start (optional, datetime): Time to start retrieving
                graphs data. If not provided get As default None
            end (optional, datetime): Time to end retrieving
                graphs data.

        Returns (dict): Altcoins dict and dominance percentage
            values with timestamps
        """
        url = urljoin(self.urls["graphs_api"], "global/dominance/")

        if start and end:
            url += Pymarketcap._add_start_end(url, start, end)

        return self.session.get(url, proxies=self.proxies, timeout=self.timeout).json()

    def download_logo(self, currency, size=64, imagepath=None):
        """Download currency logo

        Args:
            currency (str): Currency name of symbol to download
            size (str): Size in pixels. Valid sizes are:
                [8, 16, 32, 64, 128, 200]
        """
        if self.is_symbol(currency):
            currency = self.correspondences[currency]

        url_schema = "https://files.coinmarketcap.com/static/img/coins/%dx%d/%s.png"
        url = url_schema % (size, size, currency)
        req = self.session.get(url, proxies=self.proxies, stream=True, timeout=self.timeout)
        if req.status_code == 200:
            if not imagepath:
                imagepath = "%s.png" % currency
            else:
                if imagepath[-4:] != ".png":
                    raise ValueError("The imagepath param must be in .png format")
            with open(imagepath, "wb") as image:
                for chunk in req.iter_content(1024):
                    image.write(chunk)
            return imagepath
        else:
            raise CoinmarketcapHTTPError(req.status_code, "%s not found" % url)
