


    @property
    def ticker_badges(self):
        """Badges that you can convert prices in ticker() method"""
        return ["AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK",
                "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY",
                "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN",
                "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR"]

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
                   ["AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK",
                    "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY",
                    "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN",
                    "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR"]

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

    # En tests/test_api/test_ticker.py
    @pytest.mark.skip(reason="ticker_badges property needed but not built yet")
    def test_convert(self):
        for currency in [True, False]:  # With and without currency
            symbol = None
            badge = choice(pym.ticker_badges)
            if currency:
                symbol = choice(all_symbols)
                print("(Currency: %s - Badge: %s)" % (symbol, badge), end=" | ")
            else:
                print("(Badge: %s)" % badge, end=" ")

            res = pym.ticker(currency=symbol, convert=badge)
            keys = res.keys() if currency else res[0].keys()
            badges_in_keys_count = 0
            for key in keys:
                if badge.lower() in key:
                    badges_in_keys_count += 1
            assert badges_in_keys_count == 3
