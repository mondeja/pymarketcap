#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

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
        return availables.get(currency)
    else: # If the coin isn't in the dict
        availables = _reimport(update=True)
        if currency not in availables:
            exc = "The currency %s isn't in coinmarketcap" % currency
            raise NameError(exc)

class Pymarketcap(object):
    def __init__(self, base_url='https://'):
        self.base_url = base_url
        self.opener = urllib2.build_opener()
        self.opener.addheaders.append(('Content-Type', 'application/json'))
        self.opener.addheaders.append(('User-agent', 'coinmarketcap - python wrapper \
        around coinmarketcap.com (github.com/mrsmn/coinmarketcap-api)'))
    
    def _api_url(self):
        return 'api.coinmarketcap.com/v1/'
    
    def _urljoin(self, *args):
        """ Internal urljoin function because urlparse.urljoin sucks """
        urljoin = "/".join(map(lambda x: str(x).rstrip('/'), args))
        return urljoin
    
    def _get(self, api_call, query):
        url = self._urljoin(self.base_url + self._api_url(), api_call)
        if query == None:
            response = self.opener.open(url).read()
        else:
            response_url = self._urljoin(url, query)
            response = self.opener.open(response_url).read()
        return response

    def _up(self, param=None):
        """ Internal function for update symbols currencies """
        data = self._get('ticker/', query=param)
        import json, sys
        if int(sys.version[0]) < 3:
            return json.loads(data)
        else:
            return json.loads(data.decode('utf-8'))

    ''' API METHODS '''
    
    def ticker(self, currency=None, VERBOSE=False, V=False):
        """ ticker() returns a dict containing all the currencies
            ticker(currency) returns a dict containing only the currency you
            passed as an argument.
            
            VERBOSE=False (as default) -> ticker() return in json
            VERBOSE=True or V=True -> ticker() return a string
        """
        if currency != None:
            if currency.isupper() == True:
                currency = _convert(currency)
                
        data = self._get('ticker/', query=currency)
        if VERBOSE == True or V == True:
            return data
        else:
            import json, sys
            if int(sys.version[0]) < 3:
                return json.loads(data)
            else:
                return json.loads(data.decode('utf-8'))
        
        
    def stats(self, VERBOSE=False, V=False):
        """ stats() returns a dict containing cryptocurrency statistics.

            VERBOSE=False (as default) -> stats() return a dict
            VERBOSE=True or V=True -> stats() return a string
        """
        data = self._get('global/', query=None)
        if VERBOSE == True or V == True:
            return data
        else:
            import json, sys
            if int(sys.version[0]) < 3:
                return json.loads(data)
            else:
                return json.loads(data.decode('utf-8'))

    ''' WEB PARSER METHODS '''
    
    def _html_url(self, currency_id):
        """ Internal function for build currencies urls """
        return 'http://coinmarketcap.com/currencies/' + currency_id + '/'

    def _html(self, currency_id):
        """ Internal function for parse currencies htmls """
        req = urllib2.urlopen(self._html_url(currency_id))
        status_code = req.getcode()
        if status_code == 200:
            return BeautifulSoup(req.read(), "html.parser")
        else:
            print("Status Code %d" % status_code)
            return 'Error'

    def markets(self, currency, VERBOSE=False, V=False):
        """ Function that returns information from markets. It needs a currency as argument.
        pass VERBOSE=True or V=True for return a more readable string reponse

        Examples:
        markets('STEEM'), markets(ethereum, V=True)
        """
        if currency.isupper():
            currency = _convert(currency)
        
        markets = []
        html = self._html(currency)
        marks = html.find('tbody').find_all('tr')

        from sys import version
        for m in marks:
            volume_24h = int(m.find('span', {'class': 'volume'}).getText().replace('$', '').replace(',', ''))
            price = float(m.find('span', {'class': 'price'}).getText().replace('$', ''))
            childs = m.contents
            for n, c in enumerate(childs):
                if version[0] > 2:
                    nav = c.string
                else:
                    nav = unicode(c.string)
                if n == 3:
                    source = str(nav)
                elif n == 4:
                    pair = str(c.getText())
                    if pair[-1] == '*':
                        pair = pair.replace(' *', '')
                elif n == 10:
                    percent_volume = float(nav.replace('%', ''))
            market = {'source': source, 'pair': pair, '24h_volume_usd': volume_24h, 'price_usd': price, 'percent_volume': percent_volume}
            markets.append(market)
            
        if VERBOSE == True or V == True:
            from json import dumps
            return dumps(markets, indent=2)
        else:
            return markets

    def _get_ranks(self, query, temp):
        """ Internal function for get gainers and losers """
        
        url = 'http://coinmarketcap.com/gainers-losers/'
        req = req = urllib2.urlopen(url)
        status_code = req.getcode()
        if status_code == 200:
            html = BeautifulSoup(req.read(), "html.parser")
        else:
            print("Status Code %d" % status_code)
            return 'Error'
        
        call = str(query) + '-' + str(temp)

        final_list = []
        html_rank = html.find('div', {'id': call}).find_all('tr')
        from sys import version
        for curr in html_rank[1:]:
            for n, g in enumerate(curr.contents):
                if n == 3:
                    name = str(g.img.getText().replace('\n', ''))
                elif n == 5:
                    if int(version[0]) > 2:
                        symbol = str(g.string)
                    else:
                        symbol = str(unicode(g.string))
                elif n == 7:
                    volume_24h = int(str(g.a.getText()).replace('$', '').replace(',', ''))
                elif n == 9:
                    price = float(str(g.a.getText()).replace('$', ''))
                elif n == 11:
                    if int(version[0]) > 2:
                        percent = float(str(g.string).replace('%', ''))
                    else:
                        percent = float(str(unicode(g.string)).replace('%', ''))
            currency = {'name': name, 'symbol': symbol, '24h_volume_usd': volume_24h, 'price_usd': price, 'percent_change': percent}
            final_list.append(currency)

        return final_list
    
    def ranks(self, *args, **kwargs):
        """ Function that returns information from gainers and losers rankings:
        You can pass '7d', '24h', '1h', 'gainers' and 'losers' for filter response

        pass VERBOSE=True or V=True for return a more readable string reponse

        Here is the ranks -> http://www.coinmarketcap.com/gainers-losers/
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
                elif a not in all_temps and a not in all_queries:
                    exc = '%s is not a valid argument' % a
                    raise AttributeError(exc)
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


        if 'VERBOSE' in kwargs or 'V' in kwargs:
            if kwargs.get('VERBOSE') == True or kwargs.get('V') == True :
                from json import dumps
                return dumps(response, indent=2)
            else:
                return response
        else:
            return response
