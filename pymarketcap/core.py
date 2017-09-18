#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests as r
from json import loads as _loads
from decimal import Decimal
from bs4 import BeautifulSoup

def _reimport(update=False):
    """ Internal function for serves symbols correspondences """
    from os import path
    p = path.dirname(path.abspath(__file__))
    if update == True:
        from sys import path as pth
        pth.insert(1, p)
        import up
        up.update_currencies()
        pth.remove(p)
        if '' in pth:
            pth.remove('')
    with open(p + '/tmp/symbols.txt', 'r') as f:
        availables = f.read()
        from ast import literal_eval as l
        return l(availables)

def _convert(currency):
    try:
        availables = _reimport()
    except IOError:
        availables = _reimport(update=True)
    if currency in availables:
        return availables[currency]
    else: # If the coin isn't in the dict
        availables = _reimport(update=True)
        if currency not in availables:
            exc = "The currency %s isn't in coinmarketcap" % currency
            raise NameError(exc)

class CoinmarketcapError(Exception):
    """
    Exception for catch invalid commands and other repsonses
    that don't match with 200 code responses.
    """ 
    def __init__(self, err):
        print(err)

class Pymarketcap(object):
    """ Main class for retrieve data from coinmarketcap

    :param parse_float: parser used by json.loads() for
        retrieve float type returns (optional, default == Decimal)
    :type parse_float: any

    :param parse_int: parser used by json.loads() for
        retrieve int type returns (optional, default == int) 
    :type parse_int: any

    :param pair_separator: Separator in pair returns 
        (ie: pair_separator='_' -> BTC_USD) (optional, default == '-')
    :type pair_separator: str
        
    :param verbose: With True returns is parsed by
        json.dumps(indent=<indent param>) (optional, default == False)
    :type verbose: bool

    :param indent: Number of indentations in dumped response .
        Only works with verbose == True (optional, default == 2)
    :type indent: int

    :return: Pymarketcap object
    :rtype: <class 'core.Pymarketcap'>
    """

    def __init__(self, parse_float=Decimal, parse_int=int,
                 pair_separator='-', verbose=False, indent=2):
        base_url, api_version = ('https://', 'v1')
        self.api_url = '{}api.coinmarketcap.com/{}/'.format(base_url, 
                                                            api_version)
        self.web_url = 'https://coinmarketcap.com/'
        self.parse_float = parse_float
        self.parse_int = parse_int
        self.verbose = verbose
        self._indent = indent
        self.pair_separator = pair_separator

        self.symbols = self.symbols()
        self.exchange_names = self._exchange_names()

    def _urljoin(self, *args):
        """ Internal urljoin function """
        urljoin = "/".join(map(lambda x: str(x).rstrip('/'), args))
        return urljoin

    def _up(self, param=None):
        """ Internal function for update symbols currencies """
        url = self._urljoin(self.api_url, 'ticker/')
        response = r.get(url).json()
        return response
    
    def symbols(self):
        """ Return all symbols availables in coinmarketcap
        
        :return: Symbols currencies in coinmarketcap
        :rtype: list
        """
        url = self._urljoin(self.api_url, 'ticker/')
        currencies = r.get(url).json()
        response = []
        for c in currencies:
            response.append(c['symbol'])

        if self.verbose == True:
            from json import dumps
            return dumps(response, indent=self._indent)
        return response

    " ####### API METHODS ####### "
    
    def ticker(self, currency=None, convert=None, limit=None):
        """ 
        Returns currencies with other aditional data.
        
        Return example (currency != None):
            {'name': 'Bitcoin', 
            'market_cap_usd': Decimal('75281205275.0'), 
            'percent_change_24h': Decimal('-0.89'), 
            'percent_change_7d': Decimal('9.4'), 
            'price_usd': Decimal('4553.16'), 
            'price_btc': Decimal('1.0'), 
            'last_updated': 1504131565, 
            'rank': 1, 
            'total_supply': Decimal('16533837.0'), 
            'available_supply': Decimal('16533837.0'), 
            'symbol': 'BTC', 
            'id': 'bitcoin',
            '24h_volume_usd': Decimal('1953710000.0'), 
            'percent_change_1h': Decimal('0.03')}

        Endpoints: 
            /ticker/?convert=<convert>&limit=<limit>
            /ticker/<currency>/?convert=<convert>&limit=<limit>

        :param currency: Specify currency only, in this case
            method returns a dict (default == None) (optional)
        :type currency: str

        :param convert: Allow to convert the prices in response
            on one of this badges:
            "AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", 
            "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", 
            "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN", 
            "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR", "USD"
            (default == None) (optional)
        :type convert: str
        
        :param limit: limit the amount of coins in response
            only works if currency == None (optional)
        :type limit: int

        :return: Currencies/currency with other metadata
        :rtype: list (currency == None) or dict (currency != None)
        """
        if not convert:
            convert = "USD"

        if currency != None:
            if currency.isupper() == True:
                currency = _convert(currency)

        url = self._urljoin(self.api_url, 'ticker/')
        if currency:
            url = self._urljoin(url, currency)
            if convert:
                url += '?convert={}'.format(convert)
        else:
            if convert != None or limit != None:
                url += '?'
                if convert:
                    url += 'convert={}'.format(convert)
                    if limit:
                        url += '&'
                if limit:
                    url += 'limit={}'.format(str(limit))

        def parse_currency(raw_data):
            value_types = {'price_btc': self.parse_float, 
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
                           'id': str}
            data = {}
            for key, value in raw_data.items():
                try:

                    data[key] = value_types[key](value)
                except TypeError as e:
                    if 'conversion from NoneType' in repr(e):
                        data[key] = None
                    else:
                        print(e)
                        raise AssertionError
            return data


        #response = self.opener.open(url).read()
        _response = r.get(url).json()
        
        if currency:
            response = parse_currency(_response[0])
        else:
            response = []
            for currency in _response:
                response.append(parse_currency(currency))

        if self.verbose == True:
            from json import dumps
            return dumps(response, indent=self._indent)
        return response

    def stats(self):
        """ Returns global cryptocurrencies statistics.

        Return example:
            {'total_market_cap_usd': Decimal('166537487011.0'), 
            'active_currencies': 866, 
            'active_assets': 229, 
            'active_markets': 5373, 
            'total_24h_volume_usd': Decimal('5735337860.0'), 
            'bitcoin_percentage_of_market_cap': Decimal('45.18')}

        Endpoint: 
            /global/

        :return: Global criptocurrencies statitics.
        :rtype: dict
        """
        url = self._urljoin(self.api_url, 'global/')
        response = r.get(url).json(parse_int=self.parse_int,
                                   parse_float=self.parse_float)
        if self.verbose == True:
            from json import dumps
            return dumps(response, indent=self._indent)
        return response

    " ####### WEB PARSER METHODS ####### "

    def _html(self, url):
        """ Internal function for get html """
        req = r.get(url)
        status_code = req.status_code
        if status_code == 200:
            return BeautifulSoup(req.text, "html.parser")
        else:
            raise CoinmarketcapError("Status Code %d" % status_code)

    def markets(self, currency):
        """ 
        Function that returns information from markets. 
        It needs a currency as argument.
        
        Examples calls:
            markets('STEEM'), markets('ethereum', V=True)

        Example response:
            [{'price_usd': Decimal('4626.18'), 
            '24h_volume_usd': 657502, 
            'percent_volume': Decimal('0.00'), 
            'pair': 'BTC-USD', 
            'exchange': 'Quoine'}, ... ] 

        Endpoint: 
            /currencies/<currency>/#markets

        :param currency: Currency to get data information
        :type currency: str

        :return: All markets where the currency is bought and sold
        :rtype: list
        """
        from re import sub
        if currency.isupper():
            currency = _convert(currency)

        url = self.web_url + 'currencies/' + currency + '/'
        html = self._html(url)

        response = []
        marks = html.find('tbody').find_all('tr')

        for m in marks:
            _volume_24h = m.find('span', {'class': 'volume'}).getText()
            volume_24h = self.parse_int(sub(r'\D', '', _volume_24h))
            _price = m.find('span', {'class': 'price'}).getText()
            price = self.parse_float(sub(r'\$| |\*', '', _price))

            _childs, childs = (m.contents, [])
            for c in _childs:
                if c != '\n':
                    childs.append(c)
            for n, c in enumerate(childs):
                nav = c.string
                if n == 1:
                    exchange = str(nav)
                elif n == 2:
                    pair = str(c.getText()).replace('/', self.pair_separator)
                    if pair[-1] == '*':
                        pair = pair.replace(' *', '')
                elif n == 5:
                    percent_volume = self.parse_float(nav.replace('%', ''))
            market = {'exchange': exchange, 'pair': pair, 
                      '24h_volume_usd': volume_24h, 
                      'price_usd': price,
                      'percent_volume': percent_volume}
            response.append(market)
            
        if self.verbose == True:
            from json import dumps
            return dumps(response, indent=self._indent)
        return response

    def _get_ranks(self, query, temp):
        """ Internal function for get gainers and losers """
        from re import sub
        url = self.web_url + 'gainers-losers/'
        html = self._html(url)
        
        call = str(query) + '-' + str(temp)

        response = []
        html_rank = html.find('div', {'id': call}).find_all('tr')
        from sys import version
        for curr in html_rank[1:]:
            _childs, childs = (curr.contents, [])
            for c in _childs:
                if c != '\n':
                    childs.append(c)
            for n, g in enumerate(childs):
                if n == 1:
                    name = str(g.a.getText())
                elif n == 2:
                    symbol = str(g.string)
                elif n == 3:
                    _volume_24h = sub(r'\$|,', '', g.a.getText())
                    volume_24h = self.parse_int(_volume_24h)
                elif n == 4:
                    _price = sub(r'\$', '', g.a.getText())
                    price = self.parse_float(_price)
                elif n == 5:
                    percent = self.parse_float(sub(r'%', '', g.string))
            currency = {'symbol': symbol, 'name': name, 
                        '24h_volume_usd': volume_24h,
                        'price_usd': price, 'percent_change': percent}
            response.append(currency)

        return response
    
    def ranks(self, *args):
        """ 
        Returns information from gainers and losers rankings:
        
        Examples calls:
            ranks(), ranks('gainers'), ranks('1h')...

        Example response:
            {'gainers': 
                {'7d': [
                    {'percent_change': Decimal('578.41'),
                     '24h_volume_usd': 273802, 
                     'symbol': 'CV2', 
                     'price_usd': Decimal('0.000203'),
                      'name': 'Colossuscoin V2'}, ... 
                       ]
                },
                {'24h': [...]}, 
                {'1h': [...]},

             'losers': ... 
             }

        Enpoint: 
            /gainers-losers/

        :param *args: period times for filter responses
            Valid args: ['7d', '24h', '1h', 
                         'gainers', 'losers']
        :type args: str
        
        :return: Gainers and losers rankings ordered
        :rtype: dict
        """
        all_temps = ['1h', '24h', '7d']
        all_queries = ['gainers', 'losers']

        if len(args) == 0:
            temps = all_temps
            queries = all_queries
        else:
            temps = []
            queries = []
            for a in args:
                if a in all_temps:
                    temps.append(a)
                elif a in all_queries:
                    queries.append(a)
                elif a not in all_temps and \
                     a not in all_queries:
                    msg = '%s is not a valid argument' % a
                    raise AttributeError(msg)
            if len(temps) == 0:
                temps = all_temps
            if len(queries) == 0:
                queries = all_queries

        response = {}
        if len(queries) > 1:
            for q in queries:
                response[q] = {}
            for q in queries:
                rankings = {}
                for t in temps:
                    ranking = self._get_ranks(q, t)
                    rankings[t] = ranking
                response[q] = rankings
        else:
            for q in queries:
                rankings = {}
                for t in temps:
                    ranking = self._get_ranks(q, t)
                    rankings[t] = ranking
                response = rankings

        if self.verbose == True:
            from json import dumps
            return dumps(response, indent=self._indent)
        return response

    def historical(self, currency, start, end):
        """ 
        Returns historical data for a currency. 
        

        Example calls:
            historical_data('STEEM', 20170624, 20170825) 
            historical_data('ethereum', 20140101, 20160215)

        Example response:
            [
               {datetime.datetime(2017, 8, 25, 0, 0): 
                      {'close': Decimal('4371.60'), 
                       'low': Decimal('4307.35'), 
                       'usd_volume': 1727970000, 
                       'open': Decimal('4332.82'), 
                       'usd_market_cap': 71595100000, 
                       'high': Decimal('4455.70')}
               }, {}, ...
            ]

        Endpoint:
            /currencies/<currency>/historical-data/

        :param currency: Currency to scrap historical data
        :type currency: str

        :param start: Time for start scraping periods,
            in the form yearmonthday (ie: 20140101)
        :type start: int or str

        :param end: Time for end scraping periods,
            in the form yearmonthday (ie: 20160215)
        :type end: int or str

        :return: historical data for a currency
        :rtype: list
        """
        from datetime import datetime
        if currency.isupper():
            currency = _convert(currency)

        url = self.web_url + 'currencies/' + currency + '/historical-data/'
        url += '?start={}&end={}'.format(str(start), str(end))

        html = self._html(url)

        response = []
        marks = html.find('tbody').find_all('tr')
        #print(marks[0])
        for m in marks:
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
            response.append({date: indicators})

        if self.verbose == True:
            from json import dumps
            return dumps(response, indent=self._indent)
        return response

    def recently(self):
        """ 
        Returns recently addeds currencies along
        with other metadata

        Example response:
            [
             {'price_usd': Decimal('0.176407'), 
             'mineable': True, 
             'symbol': 'LLT', 
             'usd_market_cap': '?', 
             'circulating_supply': '?', 
             'volume_24h_usd': 4181750, 
             'days_ago': 1, 
             'name': 'LLToken'}
             }
            ]

        Endpoint:
            /new/

        :return: Recently added currencies
        :rtype: list
         """
        from re import sub
        url = self.web_url + 'new/'

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
                    _usd_market_cap = c.getText().replace('\n', '')
                    usd_market_cap = str(_usd_market_cap.replace(' ', ''))
                    if '$' in usd_market_cap:
                        usd_market_cap = sub(r'\$|,', '', usd_market_cap)
                elif n == 4:
                    _price_usd = c.getText().replace('\n', '')
                    price_usd = self.parse_float(sub(r' |\$', '', _price_usd))
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
                    _volume_24h_usd = c.getText().replace('\n', '')
                    volume_24h_usd = sub(r'\$|,', '', _volume_24h_usd)
                    if volume_24h_usd != 'Low Vol':
                        try:
                            volume_24h_usd = self.parse_int(volume_24h_usd)
                        except ValueError:
                            # Is a '?' value?
                            if volume_24h_usd == '?':
                                pass
                            else:
                                raise ValueError('volume_24h_usd ==', volume_24h_usd)
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

        if self.verbose == True:
            from json import dumps
            return dumps(response, indent=self._indent)
        return response

    def _exchange_names(self):
        """ Internal function for return all exchange 
        names available currently in coinmarketcap.
        You can call it as attributte:
            Pymarketcap().exchange_names """
        exchs = self.exchanges(limit=10000)
        response = []
        for e in exchs:
            if e['name'] not in response:
                response.append(e['name'])
        return response

    def exchange(self, exchange_name):
        """ 
        Returns data from a exchange passed as argument
        
        Example call:
            exchange('poloniex')

        Example response:
            [
              {'perc_volume': Decimal('18.21'), 
               'price_usd': Decimal('385.84'), 
               'volume_rank': 1, 
               'market': 'ETH-BTC', 
               'name': 'Ethereum', 
               'volume_24h_usd': 50556000},
              {...}, ...
            ]

        Endpoint:
            exchanges/<exchange_name>/

        :param exchange_name: Exchange to retrieve data
            For see all posible exchanges call:
                Pymarketcap().exchange_names
        :type exchange_name: str

        :return: Data from all markets in exchange
        :rtype: list

        """
        from re import sub
        url = self.web_url + 'exchanges/%s/' % exchange_name
        html = self._html(url)

        marks = html.find('table').find_all('tr')
        response = []
        for m in marks[1:]:
            _childs, childs = (m.contents, [])
            for c in _childs:
                if c != '\n':
                    childs.append(c)
            for n, c in enumerate(childs):
                if n == 0:
                    rank = self.parse_int(c.getText())
                elif n == 1:
                    name = str(c.getText())
                elif n == 2:
                    market = str(c.getText().replace('/',
                                    self.pair_separator))
                elif n == 3:
                    _volume_24h_usd = sub(r'\$|,', '', c.getText())
                    volume_24h_usd = self.parse_int(_volume_24h_usd)
                elif n == 4:
                    _price_usd = sub(r'\$| |\*', '', c.getText())
                    price_usd = self.parse_float(_price_usd)
                elif n == 5:
                    _perc_volume = c.getText().replace('%', '')
                    perc_volume = self.parse_float(_perc_volume)
            indicators = {'rank': rank,
                          'name': name,
                          'market': market,
                          'volume_24h_usd': volume_24h_usd,
                          'price_usd': price_usd,
                          'perc_volume': perc_volume}
            response.append(indicators)

        if self.verbose == True:
            from json import dumps
            return dumps(response, indent=self._indent)
        return response

    def exchanges(self, limit=50):
        """ 
        Returns all the exchanges markets data
        in coninmarketcap ranked by volumes.

        Example response:
            [
              {'rank': 1, 
               'volume_usd': 507619219, 
               'name': 'bittrex', 
               'markets': [
                            {'volume_24h_usd': 50465200, 
                            'rank': 1, 
                            'perc_change': Decimal('9.94'),
                            'market': 'MCO/BTC', 
                            'price_usd': Decimal('14.69')},
                            ...
                          ]
              },
              ...
            ]

        Endpoint: 
            /exchanges/volume/24-hour/all/
        
        :param limit: Limit the amount of exchanges
            in response (optional, default == 50)
        :type limit: int

        :return: Exchanges ranked by volumes 
            with his markets ordered also
            by volumes of transactions
        :rtype: list
        """

        from re import sub
        url = self.web_url + 'exchanges/volume/24-hour/all/'
        html = self._html(url)

        exs = html.find('table').find_all('tr') # Exchanges
        dating = False
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
                                volume_24h_usd = self.parse_int(c.getText().replace('$', '').replace(',', ''))
                            elif n == 4:
                                price_usd = self.parse_float(c.getText().replace('$', '').replace(',', ''))
                            elif n == 5:
                                perc_change = self.parse_float(c.getText().replace('%', ''))
                        
                        market_data = {'rank': rank,
                                       'market': market,
                                       'volume_24h_usd': volume_24h_usd,
                                       'price_usd': price_usd,
                                       'perc_change': perc_change}
                        exist = False
                        for _market_data in exchange_data['markets']:
                            if market_data['rank'] == _market_data['rank']:
                                exist = True
                        if exist == False:
                            exchange_data['markets'].append(market_data)
            else:
                try:
                    response.append(exchange_data)
                except UnboundLocalError:
                    pass
                else:
                    if len(response) >= limit:
                        break
                # In this case is the exchange name
                exchange_data = {}
                rank = int(sub(r'\D', '', e.getText()))
                exchange_data['rank'] = rank
                # We create a dict where we will save the markets data
                exchange_data['name'] = exchange
                exchange_data['markets'] = []

        if self.verbose == True:
            from json import dumps
            return dumps(response, indent=self._indent)
        return response
